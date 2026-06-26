#!/usr/bin/env python3
"""LLM-based priority scoring for memory entries."""
import argparse
import json
import re
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

# Add lib/ to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from config_loader import load_config, get_default_config
from log_utils import get_logger

logger = get_logger("dreaming-optimizer.score_entries")

# ─────────────────────────────────────────────────────────────────────────────
# Scoring Constants
# ─────────────────────────────────────────────────────────────────────────────

BASE_SCORE = 50
MAX_FACT_BONUS = 30
MAX_ACTIONABLE_BONUS = 20
SHORT_ENTRY_PENALTY = 20
MIN_ENTRY_LENGTH = 20

# Default fact terms (can be overridden by config)
DEFAULT_FACT_TERMS_ZH = [
    "数据库", "API", "配置", "bug", "修复", "测试", "agent", "skill",
    "已修复", "已实现", "完成了", "测试通过", "deployed", "fixed",
    "代码", "函数", "模块", "架构", "部署", "上线", "发布", "创建",
]
DEFAULT_FACT_TERMS_EN = [
    "fixed", "deployed", "implemented", "completed", "tested",
    "bug", "api", "config", "module", "architecture", "created",
]

# Actionable terms
ACTIONABLE_TERMS = [
    "需要", "必须", "应该", "计划", "TODO", "fix", "implement",
    "需要修复", "需要实现", "下一步", "next step", "will do",
]

# Hedging / vague terms (penalize)
VAGUE_TERMS = [
    "可能", "也许", "大概", "似乎", "好像", "maybe", "perhaps",
    "probably", "might", "could be", "不确定",
]


# ─────────────────────────────────────────────────────────────────────────────
# Core Scoring Functions
# ─────────────────────────────────────────────────────────────────────────────

def normalize_for_scoring(text: str) -> str:
    """Normalize text for scoring (lowercase, strip)."""
    return text.lower().strip()


def count_fact_terms(content: str, fact_terms: list[str] = None) -> tuple[int, list[str]]:
    """Count fact terms found in content.
    
    Args:
        content: Entry content
        fact_terms: List of fact terms (default: DEFAULT_FACT_TERMS)
        
    Returns:
        (count, terms_found): Number of terms found and which ones
    """
    if fact_terms is None:
        fact_terms = DEFAULT_FACT_TERMS_ZH + DEFAULT_FACT_TERMS_EN
    
    content_lower = content.lower()
    found = []
    for term in fact_terms:
        if term.lower() in content_lower:
            found.append(term)
    
    return len(found), found


def count_actionable_terms(content: str) -> int:
    """Count actionable terms in content."""
    content_lower = content.lower()
    return sum(1 for term in ACTIONABLE_TERMS if term.lower() in content_lower)


def count_vague_terms(content: str) -> int:
    """Count vague/hedging terms in content."""
    content_lower = content.lower()
    return sum(1 for term in VAGUE_TERMS if term.lower() in content_lower)


def score_entry(
    content: str,
    mtime: datetime = None,
    fact_terms: list[str] = None,
    config: dict = None,
) -> dict:
    """Score a single memory entry (0-100).
    
    Scoring algorithm:
        - base: 50
        - +5 per concrete fact term found (max +30)
        - +10 if recently modified (within 7 days)
        - +10 if contains actionable language
        - -20 if very short (<20 chars)
        - -10 per vague hedging term (max -20)
        - final: clamp(0, 100)
    
    Args:
        content: Raw text content of the entry
        mtime: Last modified time (optional, defaults to now)
        fact_terms: Override fact terms list
        config: Config dict (optional, for future LLM-based scoring)
        
    Returns:
        dict: {
            "score": int,           # 0-100
            "content_preview": str, # First 500 chars
            "reasons": list[str],  # Why this score
            "fact_terms_found": list[str],
        }
    """
    score = BASE_SCORE
    reasons = []
    bonuses = []
    penalties = []
    
    content = content.strip()
    content_preview = content[:500]
    
    # Check for empty content
    if not content:
        return {
            "score": BASE_SCORE,
            "content_preview": "",
            "reasons": ["Empty content, using base score"],
            "fact_terms_found": [],
        }
    
    # ── Bonuses ──
    
    # Fact term bonus: +5 per term, max +30
    fact_count, fact_found = count_fact_terms(content, fact_terms)
    fact_bonus = min(fact_count * 5, MAX_FACT_BONUS)
    if fact_bonus > 0:
        bonuses.append(f"fact_terms:+{fact_bonus}")
        score += fact_bonus
    
    # Recency bonus: +10 if modified within 7 days
    if mtime is not None:
        now = datetime.now(tz=timezone.utc)
        if (now - mtime) <= timedelta(days=7):
            bonuses.append("recency:+10")
            score += 10
    
    # Actionable bonus: +10 if actionable terms found
    actionable_count = count_actionable_terms(content)
    if actionable_count > 0:
        actionable_bonus = min(actionable_count * 5, MAX_ACTIONABLE_BONUS)
        bonuses.append(f"actionable:+{actionable_bonus}")
        score += actionable_bonus
    
    # ── Penalties ──
    
    # Short entry penalty: -20 if < MIN_ENTRY_LENGTH chars
    if len(content) < MIN_ENTRY_LENGTH:
        penalties.append(f"short_content:-{SHORT_ENTRY_PENALTY}")
        score -= SHORT_ENTRY_PENALTY
    
    # Vague language penalty: -10 per vague term, max -20
    vague_count = count_vague_terms(content)
    if vague_count > 0:
        vague_penalty = min(vague_count * 10, 20)
        penalties.append(f"vague:-{vague_penalty}")
        score -= vague_penalty
    
    # ── Clamp and format reasons ──
    
    score = max(0, min(100, score))
    
    if bonuses:
        reasons.append("Bonuses: " + ", ".join(bonuses))
    if penalties:
        reasons.append("Penalties: " + ", ".join(penalties))
    if fact_found:
        reasons.append(f"Fact terms found: {', '.join(fact_found[:5])}")
    
    return {
        "score": score,
        "content_preview": content_preview,
        "reasons": reasons,
        "fact_terms_found": fact_found,
    }


def parse_memory_file(filepath: Path) -> list[dict]:
    """Parse a daily memory .md file into entry dicts.
    
    Splits on YAML front-matter style separators (---) or
    falls back to splitting by double newlines.
    
    Args:
        filepath: Path to YYYY-MM-DD.md file
        
    Returns:
        List of entry dicts with keys: content, filename, mtime, line_count
    """
    try:
        content = filepath.read_text(encoding="utf-8")
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime, tz=timezone.utc)
    except (IOError, OSError) as e:
        logger.warning(f"Failed to read {filepath}: {e}")
        return []
    
    entries = []
    
    # Split on --- separators (common in daily note format)
    if "---" in content:
        parts = content.split("---")
        for part in parts:
            part = part.strip()
            if part and len(part) >= 10:  # Skip very short fragments
                entries.append({
                    "content": part,
                    "filename": filepath.name,
                    "mtime": mtime,
                    "line_count": part.count("\n") + 1,
                })
    else:
        # Fall back to paragraph splitting
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        for para in paragraphs:
            if len(para) >= 10:
                entries.append({
                    "content": para,
                    "filename": filepath.name,
                    "mtime": mtime,
                    "line_count": para.count("\n") + 1,
                })
    
    return entries


def get_memory_files(
    input_dir: Path = None,
    glob_pattern: str = "????-??-??.md",
    max_age_days: int = None,
) -> list[Path]:
    """Find daily memory notes in the workspace.
    
    Args:
        input_dir: Directory to search (default: workspace/memory/)
        glob_pattern: File pattern to match
        max_age_days: Only return files modified within this many days
        
    Returns:
        List of Path objects sorted by modification time (newest first)
    """
    if input_dir is None:
        input_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    
    if not input_dir.exists():
        logger.warning(f"Memory directory does not exist: {input_dir}")
        return []
    
    files = sorted(input_dir.glob(glob_pattern), key=lambda f: f.stat().st_mtime, reverse=True)
    
    if max_age_days is not None:
        now = datetime.now(tz=timezone.utc)
        cutoff = now - timedelta(days=max_age_days)
        files = [
            f for f in files
            if datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc) >= cutoff
        ]
    
    return files


def score_entries(
    memory_files: list[Path] = None,
    threshold: int = 70,
    max_entries: int = 1000,
    input_dir: Path = None,
    config: dict = None,
) -> dict:
    """Score all entries from daily memory files.
    
    Args:
        memory_files: List of Path objects to memory .md files.
                      Defaults to all files in workspace/memory/.
        threshold: Minimum score to pass (default: 70)
        max_entries: Maximum entries to process (default: 1000)
        input_dir: Override input directory
        config: Config dict (optional)
        
    Returns:
        dict: {
            "scored": list[dict],    # All entries with scores
            "passed": list[dict],    # Entries with score >= threshold
            "archived": list[dict], # Entries with score < threshold
            "total_processed": int,
            "skipped": int,          # Entries skipped (too many)
        }
    """
    if config is None:
        config = load_config()
    
    if memory_files is None:
        memory_files = get_memory_files(input_dir=input_dir)
    
    archive_threshold = config.get("scoring", {}).get("archive_threshold", 35)
    fact_terms = config.get("fact_terms", {}).get("zh", []) + config.get("fact_terms", {}).get("en", [])
    
    all_entries = []
    for filepath in memory_files:
        entries = parse_memory_file(filepath)
        all_entries.extend(entries)
    
    # Cap at max_entries
    skipped = max(0, len(all_entries) - max_entries)
    if skipped > 0:
        logger.info(f"Skipping {skipped} entries (max_entries={max_entries})")
        all_entries = all_entries[:max_entries]
    
    scored = []
    for entry in all_entries:
        mtime = entry.get("mtime")
        result = score_entry(
            content=entry["content"],
            mtime=mtime,
            fact_terms=fact_terms,
            config=config,
        )
        result["source_file"] = entry["filename"]
        result["content_length"] = len(entry["content"])
        result["mtime"] = mtime.isoformat() if mtime else None
        scored.append(result)
    
    # Categorize by threshold
    passed = [e for e in scored if e["score"] >= threshold]
    archived = [e for e in scored if e["score"] < threshold]
    
    logger.info(
        f"Scored {len(scored)} entries: "
        f"{len(passed)} passed (>={threshold}), "
        f"{len(archived)} archived (<{threshold}), "
        f"{skipped} skipped"
    )
    
    return {
        "scored": scored,
        "passed": passed,
        "archived": archived,
        "total_processed": len(scored),
        "skipped": skipped,
        "threshold_used": threshold,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Score memory entries for Dreaming REM consolidation"
    )
    parser.add_argument(
        "--threshold", type=int, default=70,
        help="Minimum score threshold (default: 70)"
    )
    parser.add_argument(
        "--max-entries", type=int, default=1000,
        help="Maximum entries to process (default: 1000)"
    )
    parser.add_argument(
        "--input-dir", type=Path, default=None,
        help="Override input directory"
    )
    parser.add_argument(
        "--output-json", type=Path, default=None,
        help="Write results to JSON file"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose logging"
    )
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        logger.setLevel(logging.DEBUG)
    
    result = score_entries(
        threshold=args.threshold,
        max_entries=args.max_entries,
        input_dir=args.input_dir,
    )
    
    print(
        f"[score_entries] Scored: {len(result['scored'])}, "
        f"Passed: {len(result['passed'])}, "
        f"Archived: {len(result['archived'])}, "
        f"Skipped: {result['skipped']}"
    )
    
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"[score_entries] Written to {args.output_json}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
