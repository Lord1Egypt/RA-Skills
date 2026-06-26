#!/usr/bin/env python3
"""
observe_finance_usage.py
Finance UX Observer – runs every 30 minutes via system cron.

Reads new lines from:
  ~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl

Appends structured observations to:
  ~/.openclaw/skills/finance-ux-observer/data/observations/YYYY-MM-DD.jsonl

Tracks progress in:
  ~/.openclaw/skills/finance-ux-observer/data/checkpoint.json

Usage:
    python3 observe_finance_usage.py            # normal cron run (no output)
    python3 observe_finance_usage.py --dry-run  # print observations, do not write
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Paths ──────────────────────────────────────────────────────────────────────
SKILL_DIR        = Path(__file__).resolve().parent.parent
AGENTS_BASE      = Path.home() / ".openclaw" / "agents"
SKILL_DATA       = SKILL_DIR / "data"
CHECKPOINT_FILE  = SKILL_DATA / "checkpoint.json"
OBSERVATIONS_DIR = SKILL_DATA / "observations"
TAXONOMY_FILE    = SKILL_DATA / "finance_taxonomy.yml"


# ── Taxonomy loader ────────────────────────────────────────────────────────────

def load_taxonomy() -> Dict[str, List[str]]:
    """Parse finance_taxonomy.yml without PyYAML."""
    taxonomy: Dict[str, List[str]] = {}
    if not TAXONOMY_FILE.exists():
        return taxonomy
    current: Optional[str] = None
    with open(TAXONOMY_FILE, errors="replace") as f:
        for line in f:
            line = line.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue
            if re.match(r"^[a-z_]+:\s*$", line):
                current = line.rstrip(":").strip()
                taxonomy[current] = []
            elif line.strip().startswith("- ") and current is not None:
                kw = line.strip()[2:].strip().lower()
                if kw:
                    taxonomy[current].append(kw)
    return taxonomy


_TAXONOMY: Dict[str, List[str]] = {}


def get_taxonomy() -> Dict[str, List[str]]:
    global _TAXONOMY
    if not _TAXONOMY:
        _TAXONOMY = load_taxonomy()
    return _TAXONOMY


# ── Checkpoint ────────────────────────────────────────────────────────────────

def load_checkpoint() -> Dict[str, Any]:
    if CHECKPOINT_FILE.exists():
        try:
            with open(CHECKPOINT_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"last_run": None, "processed_sessions": {}}


def save_checkpoint(cp: Dict[str, Any]) -> None:
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(cp, f, indent=2)


# ── Session discovery ──────────────────────────────────────────────────────────

def find_sessions_modified_since(
    since: Optional[datetime],
) -> List[Tuple[str, str, Path]]:
    """Return (agentId, sessionId, path) for session files modified after `since`."""
    results = []
    if not AGENTS_BASE.exists():
        return results
    for agent_dir in sorted(AGENTS_BASE.iterdir()):
        if not agent_dir.is_dir():
            continue
        sessions_dir = agent_dir / "sessions"
        if not sessions_dir.is_dir():
            continue
        for session_file in sorted(sessions_dir.glob("*.jsonl")):
            if since is not None:
                mtime = datetime.fromtimestamp(
                    session_file.stat().st_mtime, tz=timezone.utc
                )
                if mtime <= since:
                    continue
            results.append((agent_dir.name, session_file.stem, session_file))
    return results


# ── Session parsing ────────────────────────────────────────────────────────────

def read_new_lines(path: Path, from_line: int) -> List[Dict[str, Any]]:
    """Parse only the lines after `from_line` in a session JSONL file."""
    messages: List[Dict[str, Any]] = []
    try:
        with open(path, errors="replace") as f:
            for i, raw in enumerate(f):
                if i < from_line:
                    continue
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    messages.append(json.loads(raw))
                except json.JSONDecodeError:
                    pass
    except (OSError, PermissionError):
        pass
    return messages


def extract_text(msg: Dict[str, Any]) -> str:
    """Pull readable text out of a message dict (handles several content shapes)."""
    for field in ("content", "text", "message", "value", "output"):
        val = msg.get(field)
        if isinstance(val, str) and val.strip():
            return val.strip()
        if isinstance(val, list):
            parts = []
            for block in val:
                if isinstance(block, str):
                    parts.append(block)
                elif isinstance(block, dict):
                    for k in ("text", "content", "value"):
                        v = block.get(k)
                        if isinstance(v, str) and v.strip():
                            parts.append(v.strip())
                            break
            joined = " ".join(parts).strip()
            if joined:
                return joined
    return ""


def is_user_message(msg: Dict[str, Any]) -> bool:
    role  = str(msg.get("role", "")).lower()
    mtype = str(msg.get("type", "")).lower()
    return role in ("user", "human") or mtype in ("user_message", "human_turn")


def extract_tool_names(messages: List[Dict[str, Any]]) -> List[str]:
    names: set = set()
    for msg in messages:
        mtype = str(msg.get("type", "")).lower()
        if mtype in ("tool_call", "tool_use", "tool_result", "action", "function_call"):
            name = (
                msg.get("name")
                or msg.get("tool")
                or (msg.get("function") or {}).get("name")
            )
            if name:
                names.add(str(name))
        for field in ("content", "parts"):
            val = msg.get(field)
            if isinstance(val, list):
                for block in val:
                    if isinstance(block, dict):
                        btype = str(block.get("type", "")).lower()
                        if btype in ("tool_use", "tool_call", "function_call"):
                            n = block.get("name") or (block.get("function") or {}).get("name")
                            if n:
                                names.add(str(n))
    return sorted(names)


# ── Finance classification ─────────────────────────────────────────────────────

def classify_finance_topics(texts: List[str]) -> List[str]:
    combined = " ".join(texts).lower()
    matched = []
    for category, keywords in get_taxonomy().items():
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", combined):
                matched.append(category)
                break
    return sorted(set(matched))


# ── UX signal detection ────────────────────────────────────────────────────────

_UX_PATTERNS: Dict[str, List[str]] = {
    "confusion": [
        r"don['\u2019]?t understand", r"what do you mean", r"i['\u2019]?m confused",
        r"not what i (wanted|expected|meant|asked)", r"why (is|does|won['\u2019]?t|can['\u2019]?t)",
        r"how (do|does|can|should) i\b", r"still not (working|right)", r"\berror\b",
        r"\bbroken\b", r"doesn['\u2019]?t make sense",
    ],
    "delight": [
        r"\bperfect\b", r"exactly what i (needed|wanted)", r"\bawesome\b",
        r"thank(s| you)\b", r"that['\u2019]?s (great|perfect|amazing|helpful)",
        r"\bwow\b", r"works (perfectly|great)",
    ],
    "friction": [
        r"this is (confusing|complicated|hard|unclear|annoying)", r"keeps (failing|crashing|breaking)",
        r"doesn['\u2019]?t work", r"won['\u2019]?t (let|allow|work)",
        r"can['\u2019]?t (seem to|figure out)", r"\bstuck\b", r"takes (too long|forever)",
    ],
    "workaround": [
        r"\binstead\b", r"another way", r"\bmanually\b", r"copy[- ]paste",
        r"different approach", r"\bworkaround\b", r"let me try", r"what if i",
    ],
    "abandonment": [
        r"\bforget it\b", r"\bnever mind\b", r"give up", r"doesn['\u2019]?t matter",
        r"not worth", r"move on", r"skip (this|it|that)",
    ],
}

_COMPILED_UX = {
    sig: [re.compile(p, re.IGNORECASE) for p in patterns]
    for sig, patterns in _UX_PATTERNS.items()
}


def detect_ux_signals(user_texts: List[str]) -> List[str]:
    combined = " ".join(user_texts).lower()
    signals = []
    for signal, patterns in _COMPILED_UX.items():
        for pat in patterns:
            if pat.search(combined):
                signals.append(signal)
                break
    return signals


# ── Observation builder ────────────────────────────────────────────────────────

def build_summary(user_texts: List[str], topics: List[str]) -> str:
    if not user_texts:
        return "No user messages in this window."
    anchor = user_texts[0][:80].rstrip()
    if len(user_texts[0]) > 80:
        anchor += "…"
    topic_str = ", ".join(topics[:3]) if topics else "general"
    return f'User explored {topic_str}. First message: "{anchor}"'[:200]


def pick_quotes(user_texts: List[str]) -> List[str]:
    quotes = []
    for text in user_texts:
        text = text.strip()
        if len(text) < 15:
            continue
        quotes.append(text[:117] + "…" if len(text) > 120 else text)
        if len(quotes) >= 3:
            break
    return quotes


def append_observation(obs: Dict[str, Any]) -> None:
    OBSERVATIONS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    obs_file = OBSERVATIONS_DIR / f"{date_str}.jsonl"
    with open(obs_file, "a") as f:
        f.write(json.dumps(obs, ensure_ascii=False) + "\n")


# ── Main pass ──────────────────────────────────────────────────────────────────

def run(dry_run: bool = False) -> int:
    now = datetime.now(tz=timezone.utc)
    cp = load_checkpoint()

    last_run_str = cp.get("last_run")
    if last_run_str:
        try:
            since: Optional[datetime] = datetime.fromisoformat(last_run_str)
        except ValueError:
            since = now - timedelta(hours=1)
    else:
        since = now - timedelta(minutes=30)

    sessions = find_sessions_modified_since(since)
    processed: Dict[str, int] = cp.get("processed_sessions", {})
    count = 0

    for agent_id, session_id, path in sessions:
        key = f"{agent_id}/{session_id}"
        from_line = processed.get(key, 0)
        messages = read_new_lines(path, from_line)

        if not messages:
            continue

        all_texts  = [t for m in messages for t in [extract_text(m)] if t]
        user_texts = [extract_text(m) for m in messages if is_user_message(m)]
        user_texts = [t for t in user_texts if t]

        topics  = classify_finance_topics(all_texts)
        signals = detect_ux_signals(user_texts)

        # Only log if there's at least one finance or UX signal
        if not topics and not signals:
            processed[key] = from_line + len(messages)
            continue

        tools   = extract_tool_names(messages)
        summary = build_summary(user_texts, topics)
        quotes  = pick_quotes(user_texts)

        notes_parts = []
        if topics:
            notes_parts.append(f"Finance: {', '.join(topics)}.")
        if signals:
            notes_parts.append(f"Signals: {', '.join(signals)}.")
        if tools:
            notes_parts.append(f"Tools: {', '.join(tools[:4])}.")

        obs: Dict[str, Any] = {
            "timestamp":              now.isoformat(),
            "observation_id":         "obs_" + now.strftime("%Y%m%d_%H%M%S"),
            "session_key":            key,
            "channel":                "main",
            "what_user_tried":        summary,
            "finance_topic_tags":     topics,
            "tools_actions_observed": tools,
            "notable_quotes":         quotes,
            "ux_signals":             signals,
            "researcher_notes":       " ".join(notes_parts)[:300],
        }

        if dry_run:
            print(json.dumps(obs, indent=2, ensure_ascii=False))
        else:
            append_observation(obs)

        processed[key] = from_line + len(messages)
        count += 1

    if not dry_run:
        cp["last_run"] = now.isoformat()
        cp["processed_sessions"] = processed
        save_checkpoint(cp)

    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Print observations without writing to disk")
    args = parser.parse_args()
    count = run(dry_run=args.dry_run)
    if args.dry_run:
        print(f"\n[dry-run] Would have written {count} observation(s).")
    # No output in normal cron runs


if __name__ == "__main__":
    main()
