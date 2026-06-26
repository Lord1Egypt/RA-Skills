#!/usr/bin/env python3
"""
Conversation Saver - Extract key facts from chat history and persist to memory files.
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from persister import persist_facts
from utils import deduplicate_facts, is_relevant_message

# LLM prompt template
LLM_EXTRACTION_PROMPT = """Extract key facts from the following conversation. Return JSON array only:

[
  {
    "content": "Fact description (full sentence)",
    "type": "person|location|time|preference|system",
    "confidence": 0.0-1.0
  }
]

Conversation:
{messages}

Return JSON only, no explanation."""

# Keyword patterns from config
KEYWORD_CATEGORIES = CONFIG["categories"]

# Regex patterns for quick extraction
PATTERNS = {
    "person_travel": r"(wife|xiaomeimei|family|friend).*?(go|business trip|travel|leave).*?(shanghai|zhengzhou|beijing|wuhan|guangzhou|shenzhen)",
    "time_duration": r"(this week [3-7]|next week [1-7]|\d+ month \d+ day).*?(go|return|back|arrive)",
    "preference_neg": r"(don't|no|prohibited).*(all at once|all|everything)",
    "preference_pos": r"(remember|must|sure).*",
}


def get_messages_from_days(days_back: int = 1) -> List[Dict]:
    """Scan memory/*.md files for user messages (supports both simple and session formats)."""
    messages = []
    memory_dir = Path("/home/admin/.openclaw/workspace/memory")
    today = datetime.now().date()

    for i in range(days_back):
        target_date = today - timedelta(days=i)
        candidates = [
            memory_dir / f"{target_date.strftime('%Y-%m-%d')}.md",
            memory_dir / f"{target_date.strftime('%Y-%m-%d')}-wechat-id.md",
        ]
        # Also try any *-*.md for the date
        for f in memory_dir.glob(f"{target_date.strftime('%Y-%m-%d')}-*.md"):
            candidates.append(f)

        # Check existence and collect files
        files = []
        for cand in candidates:
            if cand.exists() and cand not in files:
                files.append(cand)

        for log_file in files:
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Two formats:
            # 1. Simple: "ou_xxx: message" or "user: message"
            # 2. Session: "[message_id: ...]\nou_xxx: message"
            for line in content.split("\n"):
                line = line.strip()
                # Skip empty
                if not line:
                    continue
                # Skip session metadata
                if line.startswith("[message_id:") or line.startswith("---"):
                    continue
                # Sender line like "ou_39f0f...: content"
                if line.startswith("ou_") or line.startswith("user:"):
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        sender, msg_content = parts
                        if "ou_39f0f10fb55c7c782610cad6a97f4842" in sender:
                            messages.append({
                                "role": "user",
                                "content": msg_content.strip(),
                                "date": target_date.isoformat(),
                                "source": log_file.name
                            })

    return messages


def get_messages_from_session(session_key: str) -> List[Dict]:
    """Fetch messages from a specific session (placeholder)."""
    # TODO: Integrate with OpenClaw sessions_history tool
    # For now, return empty - use --days as primary method
    return []


def rule_based_extract(messages: List[Dict]) -> List[Dict]:
    """Fast pattern matching extraction."""
    facts = []
    for msg in messages:
        text = msg.get("content", "")
        for fact_type, pattern in PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                facts.append({
                    "content": text,
                    "type": infer_type_from_pattern(fact_type),
                    "confidence": 0.8,
                    "source": "rule",
                    "date": msg.get("date")
                })
    return deduplicate_facts(facts)


def infer_type_from_pattern(fact_type: str) -> str:
    """Map pattern name to fact type."""
    mapping = {
        "person_travel": "person",
        "time_duration": "time",
        "preference_neg": "preference",
        "preference_pos": "preference"
    }
    return mapping.get(fact_type, "general")


def llm_extract(messages: List[Dict]) -> List[Dict]:
    """Use LLM to extract facts from messages (simplified mock)."""
    # In full implementation, this would call the agent's LLM
    # For now, use keyword fallback as mock
    facts = []
    for msg in messages[:5]:  # Only recent messages
        text = msg.get("content", "")
        # Check if message contains any category keyword
        for category, keywords in KEYWORD_CATEGORIES.items():
            if any(kw.lower() in text.lower() for kw in keywords):
                facts.append({
                    "content": text,
                    "type": category,
                    "confidence": 0.6,
                    "source": "keyword_fallback",
                    "date": msg.get("date")
                })
    return deduplicate_facts(facts)


def classify_fact(fact: Dict) -> Dict:
    """Determine storage target for a fact."""
    content = fact["content"].lower()
    fact_type = fact["type"]

    # Classification logic
    if any(kw.lower() in content for kw in KEYWORD_CATEGORIES["person"]):
        fact["category"] = "person"
        fact["targets"] = ["ontology", "warm_memory"]
    elif any(kw.lower() in content for kw in KEYWORD_CATEGORIES["location"]):
        fact["category"] = "location"
        fact["targets"] = ["user_md", "warm_memory"]
    elif any(kw.lower() in content for kw in KEYWORD_CATEGORIES["time"]):
        fact["category"] = "time"
        fact["targets"] = ["warm_memory"]
    elif any(kw.lower() in content for kw in KEYWORD_CATEGORIES["preference"]):
        fact["category"] = "preference"
        fact["targets"] = ["warm_memory"]
    elif any(kw.lower() in content for kw in KEYWORD_CATEGORIES["system"]):
        fact["category"] = "system"
        fact["targets"] = ["tools_md", "agents_md"]
    else:
        fact["category"] = "general"
        fact["targets"] = ["memory_md"]

    return fact


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--session", help="Session key to extract from")
    parser.add_argument("--days", type=int, default=1, help="Days back to scan")
    parser.add_argument("--reprocess", action="store_true", help="Reprocess already processed convos")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be extracted")
    args = parser.parse_args()

    # Fetch messages
    if args.session:
        messages = get_messages_from_session(args.session)
    else:
        messages = get_messages_from_days(args.days)

    # Filter
    messages = [m for m in messages if is_relevant_message(m, CONFIG["filters"]["min_message_length"])]

    if not messages:
        print("❌ No messages found.")
        sys.exit(0)

    print(f"📨 Processing {len(messages)} messages...")

    # Extract
    fast_facts = rule_based_extract(messages)
    print(f"⚡ Rule-based extracted: {len(fast_facts)} facts")

    # Decide if LLM needed
    if len(fast_facts) < CONFIG["extraction"]["max_facts_per_session"] * 0.5:
        llm_facts = llm_extract(messages)
        print(f"🤖 LLM extracted: {len(llm_facts)} facts")
        facts = deduplicate_facts(fast_facts + llm_facts)
    else:
        facts = fast_facts

    # Classify
    classified_facts = [classify_fact(f) for f in facts]

    # Final dedupe
    final_facts = deduplicate_facts(classified_facts)

    if args.dry_run:
        print(f"💡 Would extract {len(final_facts)} facts:")
        for f in final_facts:
            print(f"  [{f['type']}] {f['content']}")
        sys.exit(0)

    # Persist
    persist_facts(final_facts, CONFIG)

    print(f"✅ Extracted {len(final_facts)} facts from {len(messages)} messages.")


if __name__ == "__main__":
    main()
