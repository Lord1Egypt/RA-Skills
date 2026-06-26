#!/usr/bin/env python3
"""Write optimized entries to persistent B-layer memory."""
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from config_loader import load_config
from blayer_client import get_client, BLayerClient
from log_utils import get_logger

logger = get_logger("dreaming-optimizer.commit")

# ─────────────────────────────────────────────────────────────────────────────
# Tag Patterns
# ─────────────────────────────────────────────────────────────────────────────

TAG_PATTERNS = {
    "fact": [
        "已修复", "已实现", "完成了", "测试通过", "deployed", "fixed",
        "创建了", "删除了", "更新了", "上线", "发布",
    ],
    "opinion": [
        "我觉得", "认为", "可能", "应该", "probably", "think", "believe",
        "似乎", "大概", "也许", "might", "may",
    ],
    "preference": [
        "我喜欢", "偏好", "prefer", "不喜欢", "dont like",
        "倾向于", "习惯用", "更倾向于",
    ],
    "learning": [
        "学到", "发现", "learned", "realized", "insight",
        "认识到", "理解到", "明白了",
    ],
}


def tag_entry(content: str) -> str:
    """Tag entry as fact/opinion/preference/learning/context.
    
    Uses rule-based pattern matching.
    Tie-break priority: fact > learning > context > opinion > preference
    
    Args:
        content: Entry content string
        
    Returns:
        str: One of: fact, opinion, preference, learning, context
    """
    scores = {}
    content_lower = content.lower()
    
    for tag, patterns in TAG_PATTERNS.items():
        score = sum(1 for p in patterns if p.lower() in content_lower)
        if score > 0:
            scores[tag] = score
    
    if not scores:
        return "context"
    
    priority = ["fact", "learning", "context", "opinion", "preference"]
    for tag in priority:
        if tag in scores:
            return tag
    
    return max(scores, key=scores.get)


def archive_entry(entry: dict, archive_dir: Path = None) -> Optional[Path]:
    """Archive a low-score entry to dreaming-archives/."""
    if archive_dir is None:
        archive_dir = Path.home() / ".openclaw" / "workspace" / "memory" / "dreaming-archives"
    
    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d-%H%M%S")
        content_preview = (entry.get("content_preview") or entry.get("content", ""))[:50]
        safe_preview = "".join(c if c.isalnum() else "_" for c in content_preview)
        filename = f"archived-{ts}-{safe_preview}.md"
        archive_path = archive_dir / filename
        
        content = entry.get("content", "")
        metadata = (
            f"---\n"
            f"archived_at: {datetime.now(tz=timezone.utc).isoformat()}\n"
            f"original_score: {entry.get('score', 'unknown')}\n"
            f"original_source: {entry.get('source_file', 'unknown')}\n"
            f"tag: {entry.get('tag', 'context')}\n"
            f"---\n\n{content}"
        )
        archive_path.write_text(metadata, encoding="utf-8")
        logger.info(f"Archived entry to {archive_path}")
        return archive_path
    except Exception as e:
        logger.error(f"Failed to archive entry: {e}")
        return None


def commit_to_blayer(
    entries: list[dict],
    agent: str = "main",
    dry_run: bool = False,
    auto_archive: bool = True,
    archive_threshold: int = None,
) -> dict:
    """Write entries to B-layer SQLite.
    
    Args:
        entries: List of entry dicts with keys:
                 - content: full content text
                 - content_preview: first 500 chars (optional)
                 - score: 0-100
                 - source_file: originating file
                 - is_merged: bool (optional)
                 - merged_into_id: int (optional)
        agent: Agent name for DB path (default: "main")
        dry_run: If True, don't actually write
        auto_archive: If True, archive entries below commit threshold
        archive_threshold: Min score to commit (default: from config or 35)
        
    Returns:
        dict: {
            "committed": int,
            "archived": int,
            "failed": int,
            "entry_ids": list[int],
            "errors": list[str],
        }
    """
    cfg = load_config()
    if archive_threshold is None:
        archive_threshold = cfg.get("scoring", {}).get("archive_threshold", 35)
    commit_threshold = cfg.get("scoring", {}).get("default_threshold", 70)
    
    client = get_client(agent=agent)
    committed = archived = failed = 0
    entry_ids = []
    errors = []
    
    for entry in entries:
        score = entry.get("score", 50)
        content = entry.get("content", "")
        
        if not content or len(content.strip()) == 0:
            errors.append(f"Skipped empty entry from {entry.get('source_file', 'unknown')}")
            failed += 1
            continue
        
        if len(content) > 100_000:
            content = content[:100_000]
            logger.warning(f"Truncated entry from {entry.get('source_file', 'unknown')} to 100KB")
        
        if score >= commit_threshold:
            action = "commit"
        elif score >= archive_threshold and auto_archive:
            action = "archive"
        else:
            action = "discard"
        
        if action == "discard":
            client.log_action(
                content=content, action="discarded", score=score,
                reason=f"score {score} below archive threshold {archive_threshold}",
                source_file=entry.get("source_file"),
            )
            continue
        
        if action == "archive":
            if archive_entry(entry):
                archived += 1
                client.log_action(
                    content=content, action="archived", score=score,
                    reason=f"score {score} below commit threshold {commit_threshold}",
                    source_file=entry.get("source_file"),
                )
            else:
                errors.append(f"Failed to archive from {entry.get('source_file', 'unknown')}")
            continue
        
        if dry_run:
            logger.info(f"[DRY RUN] Would commit: {content[:100]}...")
            committed += 1
            entry_ids.append(-1)
            continue
        
        tag = tag_entry(content)
        entry_id = client.commit_entry(
            content=content,
            score=score,
            tag=tag,
            source_file=entry.get("source_file", "dreaming-optimizer"),
            content_preview=entry.get("content_preview"),
            is_merged=entry.get("is_merged", False),
            merged_into=entry.get("merged_into_id"),
        )
        
        if entry_id is not None:
            committed += 1
            entry_ids.append(entry_id)
        else:
            failed += 1
            errors.append(f"Failed to commit from {entry.get('source_file', 'unknown')}")
    
    logger.info(f"Commit: committed={committed}, archived={archived}, failed={failed}, dry_run={dry_run}")
    
    return {
        "committed": committed,
        "archived": archived,
        "failed": failed,
        "entry_ids": entry_ids,
        "errors": errors,
        "dry_run": dry_run,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Commit optimized entries to B-layer")
    parser.add_argument("--dry-run", action="store_true", help="Dry run - don't actually commit")
    parser.add_argument("--agent", type=str, default="main", help="Agent name (default: main)")
    parser.add_argument("--no-archive", action="store_true", help="Disable auto-archive")
    parser.add_argument("--input-json", type=Path, default=None, help="Read entries from JSON file")
    parser.add_argument("--output-json", type=Path, default=None, help="Write results to JSON file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        logger.setLevel(logging.DEBUG)
    
    if args.input_json:
        entries = json.loads(args.input_json.read_text(encoding="utf-8"))
    else:
        entries = []
    
    result = commit_to_blayer(
        entries,
        agent=args.agent,
        dry_run=args.dry_run,
        auto_archive=not args.no_archive,
    )
    
    print(f"[commit] Committed: {result['committed']}, Archived: {result['archived']}, Failed: {result['failed']}")
    
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
