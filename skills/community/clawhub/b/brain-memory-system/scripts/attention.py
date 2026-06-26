#!/usr/bin/env python3
"""
Thalamic Attention Filter — decides what deserves to become a memory.

The brain discards ~90% of sensory input before it reaches conscious processing.
This filter scores incoming events and decides: store, summarize, or discard.

Usage:
  # From CLI
  brain filter "GPU temp check passed, all normal" --source cron
  brain filter "Puddin' asked about car mode bluetooth" --source conversation
  brain filter "person detected at front door [90% confidence]" --source frigate

  # From Python
  from attention import should_store
  result = should_store(content, source="mqtt", context={...})
  # result: {"action": "store|summarize|discard", "score": 7.2, "reason": "..."}
"""
import re
import sqlite3
import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

BRAIN_DB = os.environ.get("BRAIN_DB", str(Path(__file__).parent / "brain.db"))
AGENT = os.environ.get("BRAIN_AGENT", "margot")

# ============================================================
# ATTENTION SCORES — what makes something worth remembering?
# ============================================================

# Source weights — how important is this channel?
SOURCE_WEIGHTS = {
    "conversation": 8,    # Puddin' talking = always important
    "decision": 8,        # Decisions are always worth storing
    "error": 7,           # Errors need to be remembered
    "alert_critical": 9,  # Critical alerts
    "alert_warning": 5,   # Warnings
    "alert_info": 2,      # Info alerts — mostly noise
    "frigate": 3,         # Camera detections — usually routine
    "cron": 2,            # Cron outputs — mostly routine
    "heartbeat": 1,       # Heartbeat results — very routine
    "mqtt": 3,            # MQTT events
    "handoff": 6,         # Agent handoffs
    "manual": 7,          # Manually stored = intentional
}

# Novelty boosters — keywords that signal something new/important
NOVELTY_KEYWORDS = {
    # High novelty (+3)
    "first time": 3, "never seen": 3, "new feature": 3, "breakthrough": 3,
    "discovered": 3, "root cause": 3, "figured out": 3,
    # Medium novelty (+2)
    "fixed": 2, "broke": 2, "failed": 2, "crash": 2, "error": 2,
    "deployed": 2, "built": 2, "created": 2, "shipped": 2,
    "lesson": 2, "learned": 2, "mistake": 2,
    # Low novelty (+1)
    "updated": 1, "changed": 1, "migrated": 1, "upgraded": 1,
    "installed": 1, "configured": 1,
}

# Suppression patterns — things we've seen too many times
SUPPRESSION_PATTERNS = [
    r"heartbeat.?ok",
    r"nothing.?new",
    r"no.?action.?needed",
    r"all.?(?:checks?\s+)?(?:pass|clean|green|healthy|nominal)",
    r"routine\s+check",
    r"cron\s+completed?\s+successfully",
    r"up\s+\d+\s+(?:hours?|days?)",  # "Up 3 hours" status messages
]

# Dedup window — don't store similar content within this period
DEDUP_WINDOW_HOURS = 4


def calculate_attention_score(content: str, source: str = "manual", context: dict = None) -> dict:
    """
    Score an incoming event for attention worthiness.
    Returns: {"score": float, "action": str, "reason": str, "factors": dict}
    
    Score ranges:
      0-3: DISCARD — routine noise, not worth storing
      4-5: SUMMARIZE — batch with similar events, store summary later  
      6+:  STORE — important enough for episodic memory
    """
    context = context or {}
    content_lower = content.lower()
    factors = {}
    
    # 1. Source weight
    source_score = SOURCE_WEIGHTS.get(source, 4)
    factors["source"] = source_score
    
    # 2. Content length — very short = probably not substantive
    length_score = 0
    if len(content) > 500:
        length_score = 2
    elif len(content) > 100:
        length_score = 1
    factors["length"] = length_score
    
    # 3. Novelty keywords
    novelty_score = 0
    matched_keywords = []
    for keyword, boost in NOVELTY_KEYWORDS.items():
        if keyword in content_lower:
            novelty_score += boost
            matched_keywords.append(keyword)
    novelty_score = min(novelty_score, 5)  # Cap at 5
    factors["novelty"] = novelty_score
    if matched_keywords:
        factors["novelty_keywords"] = matched_keywords[:5]
    
    # 4. Suppression — routine patterns get penalized
    suppression = 0
    for pattern in SUPPRESSION_PATTERNS:
        if re.search(pattern, content_lower):
            suppression += 3
            factors["suppressed_by"] = pattern
            break
    factors["suppression"] = -suppression
    
    # 5. Emotional signals
    emotion_score = 0
    emotion_words = ["frustrated", "proud", "excited", "worried", "relieved", 
                     "angry", "happy", "scared", "confused", "amazed",
                     "electric", "alive", "heavy", "tender", "uneasy"]
    for word in emotion_words:
        if word in content_lower:
            emotion_score = 2
            factors["emotion_detected"] = word
            break
    factors["emotion"] = emotion_score
    
    # 6. Entity mentions (Puddin', specific systems, agents)
    entity_score = 0
    important_entities = ["puddin", "darian", "lisa", "charlie", "mae",
                         "security", "breach", "vulnerability", "critical"]
    for entity in important_entities:
        if entity in content_lower:
            entity_score = 2
            factors["entity_detected"] = entity
            break
    factors["entity"] = entity_score
    
    # 7. Recency dedup — check if similar content was stored recently
    dedup_penalty = 0
    try:
        conn = sqlite3.connect(BRAIN_DB)
        cutoff = (datetime.now() - timedelta(hours=DEDUP_WINDOW_HOURS)).isoformat()
        
        # Simple check: same first 50 chars in recent episodes
        # Use substr() exact match instead of LIKE to prevent wildcard injection
        content_prefix = content[:50]
        recent = conn.execute(
            "SELECT COUNT(*) FROM episodes WHERE substr(content,1,50) = ? AND created_at > ? AND agent = ?",
            (content_prefix, cutoff, AGENT)
        ).fetchone()[0]
        
        if recent > 0:
            dedup_penalty = 4
            factors["dedup"] = f"similar content found within {DEDUP_WINDOW_HOURS}h"
        
        conn.close()
    except Exception:
        pass  # DB not available, skip dedup
    factors["dedup_penalty"] = -dedup_penalty
    
    # Calculate total score
    # Source is base (0-9), boosted by novelty/emotion/entity/length
    total = (
        source_score +             # Base: 1-9 from source type
        novelty_score * 0.5 +      # Novelty boost: 0-2.5
        emotion_score * 0.5 +      # Emotion boost: 0-1
        entity_score * 0.5 +       # Entity boost: 0-1
        length_score * 0.3 -       # Length boost: 0-0.6
        suppression -              # Suppression penalty: 0-3
        dedup_penalty              # Dedup penalty: 0-4
    ) / 1.5  # Scale to 0-10 range
    
    total = round(max(0, min(10, total)), 1)
    
    # Determine action
    if total >= 6:
        action = "store"
        reason = "High attention score — worth remembering"
    elif total >= 4:
        action = "summarize"
        reason = "Medium attention — batch for later summary"
    else:
        action = "discard"
        reason = "Below attention threshold — routine noise"
    
    return {
        "score": total,
        "action": action,
        "reason": reason,
        "factors": factors,
        "source": source,
    }


def should_store(content: str, source: str = "manual", context: dict = None) -> dict:
    """Convenience wrapper — returns the attention assessment."""
    return calculate_attention_score(content, source, context)


def main():
    """CLI interface for testing attention filter."""
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print("Usage: python3 attention.py <content> [--source <source>] [--json]")
        print(f"\nSources: {', '.join(sorted(SOURCE_WEIGHTS.keys()))}")
        print("\nActions: store (≥6), summarize (4-5), discard (<4)")
        return
    
    content = sys.argv[1]
    source = "manual"
    as_json = "--json" in sys.argv
    
    for i, arg in enumerate(sys.argv):
        if arg == "--source" and i + 1 < len(sys.argv):
            source = sys.argv[i + 1]
    
    result = should_store(content, source)
    
    if as_json:
        print(json.dumps(result, indent=2))
    else:
        action_icon = {"store": "✅", "summarize": "📋", "discard": "🗑️"}
        icon = action_icon.get(result["action"], "❓")
        print(f"{icon} {result['action'].upper()} (score: {result['score']})")
        print(f"   Reason: {result['reason']}")
        print(f"   Source: {result['source']} (weight: {result['factors'].get('source', '?')})")
        if result['factors'].get('novelty_keywords'):
            print(f"   Novelty: {', '.join(result['factors']['novelty_keywords'])}")
        if result['factors'].get('emotion_detected'):
            print(f"   Emotion: {result['factors']['emotion_detected']}")
        if result['factors'].get('suppressed_by'):
            print(f"   Suppressed: matched '{result['factors']['suppressed_by']}'")
        if result['factors'].get('dedup'):
            print(f"   Dedup: {result['factors']['dedup']}")


if __name__ == "__main__":
    main()
