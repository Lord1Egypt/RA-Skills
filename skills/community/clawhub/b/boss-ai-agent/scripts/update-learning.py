#!/usr/bin/env python3
"""Update the learning field in boss-ai-agent config.json.

Usage: Claude runs at end of session to persist learned preferences:
  python update-learning.py \
    --config ~/.openclaw/skills/boss-ai-agent/config.json \
    --preferred-language zh \
    --session-context "Reviewed Q1 KPIs, flagged sprint velocity" \
    --add-pattern "promotes-internally" \
    --add-adopted '{"id":"rec_123","category":"engagement","date":"2026-04-20"}'

  python update-learning.py --config config.json --show   # display current state
  python update-learning.py --config config.json --reset   # clear all learning

All updates are immutable — a new config dict is built, never mutated in place.
Enforces limits: 20 decision_patterns, 50 ignored/adopted recommendations.
"""
import argparse
import json
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path


MAX_PATTERNS = 20
MAX_RECOMMENDATIONS = 50

DEFAULT_LEARNING = {
    "preferred_report_format": None,
    "preferred_language": None,
    "ignored_recommendations": [],
    "adopted_recommendations": [],
    "decision_patterns": [],
    "custom_check_in_questions": [],
    "last_session_context": None,
}


MAX_JSON_SIZE = 10 * 1024 * 1024  # 10MB


def load_config(path):
    config_path = Path(path).expanduser()
    if not config_path.exists():
        print(f"Config not found at {config_path}, creating with defaults.", file=sys.stderr)
        return {"learning": deepcopy(DEFAULT_LEARNING)}
    if config_path.stat().st_size > MAX_JSON_SIZE:
        print(f"Error: {config_path} exceeds 10MB size limit", file=sys.stderr)
        sys.exit(1)
    try:
        with open(config_path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading {config_path}: {e}", file=sys.stderr)
        sys.exit(1)


def save_config(path, config):
    config_path = Path(path).expanduser()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"Config saved to {config_path}", file=sys.stderr)


def show_learning(learning):
    """Display current learning state as formatted markdown."""
    lines = [
        "# Current Learning State",
        f"*Generated at {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n",
    ]

    lang = learning.get("preferred_language")
    fmt = learning.get("preferred_report_format")
    ctx = learning.get("last_session_context")
    lines.append(f"**Language**: {lang or 'not set'}")
    lines.append(f"**Report Format**: {fmt or 'not set'}")
    lines.append(f"**Last Session**: {ctx or 'none'}\n")

    patterns = learning.get("decision_patterns", [])
    lines.append(f"### Decision Patterns ({len(patterns)}/{MAX_PATTERNS})")
    if patterns:
        for p in patterns:
            lines.append(f"- {p}")
    else:
        lines.append("- (none)")
    lines.append("")

    questions = learning.get("custom_check_in_questions", [])
    lines.append(f"### Custom Check-in Questions ({len(questions)})")
    if questions:
        for q in questions:
            lines.append(f"- {q}")
    else:
        lines.append("- (none)")
    lines.append("")

    adopted = learning.get("adopted_recommendations", [])
    ignored = learning.get("ignored_recommendations", [])
    lines.append(f"### Adopted Recommendations ({len(adopted)}/{MAX_RECOMMENDATIONS})")
    if adopted:
        for r in adopted[-5:]:
            lines.append(f"- [{r.get('date', '?')}] {r.get('category', '?')} ({r.get('id', '?')})")
        if len(adopted) > 5:
            lines.append(f"  ... and {len(adopted) - 5} more")
    else:
        lines.append("- (none)")
    lines.append("")

    lines.append(f"### Ignored Recommendations ({len(ignored)}/{MAX_RECOMMENDATIONS})")
    if ignored:
        for r in ignored[-5:]:
            lines.append(f"- [{r.get('date', '?')}] {r.get('category', '?')} ({r.get('id', '?')})")
        if len(ignored) > 5:
            lines.append(f"  ... and {len(ignored) - 5} more")
    else:
        lines.append("- (none)")

    # Category analysis
    if ignored:
        cats = {}
        for r in ignored:
            cat = r.get("category", "unknown")
            cats[cat] = cats.get(cat, 0) + 1
        deprioritized = [f"{cat} ({n}x)" for cat, n in cats.items() if n >= 3]
        if deprioritized:
            lines.append(f"\n**Auto-deprioritized categories** (3+ ignores): {', '.join(deprioritized)}")

    return "\n".join(lines)


def apply_updates(learning, args):
    """Build a new learning dict with updates applied. Never mutates input."""
    updated = deepcopy(learning)
    changes = []

    if args.preferred_language is not None:
        updated["preferred_language"] = args.preferred_language
        changes.append(f"language → {args.preferred_language}")

    if args.preferred_report_format is not None:
        updated["preferred_report_format"] = args.preferred_report_format
        changes.append(f"report_format → {args.preferred_report_format}")

    if args.session_context is not None:
        updated["last_session_context"] = args.session_context
        changes.append(f"session_context → {args.session_context[:60]}...")

    for pattern_str in (args.add_pattern or []):
        patterns = updated.get("decision_patterns", [])
        if pattern_str not in patterns:
            patterns = patterns + [pattern_str]
            if len(patterns) > MAX_PATTERNS:
                removed = patterns[0]
                patterns = patterns[1:]
                changes.append(f"pattern evicted (oldest): {removed}")
            updated["decision_patterns"] = patterns
            changes.append(f"pattern added: {pattern_str}")
        else:
            changes.append(f"pattern already exists: {pattern_str}")

    for question_str in (args.add_checkin_question or []):
        questions = updated.get("custom_check_in_questions", [])
        if question_str not in questions:
            updated["custom_check_in_questions"] = questions + [question_str]
            changes.append(f"check-in question added: {question_str[:50]}")

    for rec_json in (args.add_adopted or []):
        rec = _parse_rec(rec_json)
        if rec:
            adopted = updated.get("adopted_recommendations", [])
            adopted = adopted + [rec]
            if len(adopted) > MAX_RECOMMENDATIONS:
                adopted = adopted[-MAX_RECOMMENDATIONS:]
            updated["adopted_recommendations"] = adopted
            changes.append(f"adopted: {rec.get('category', '?')} ({rec.get('id', '?')})")

    for rec_json in (args.add_ignored or []):
        rec = _parse_rec(rec_json)
        if rec:
            ignored = updated.get("ignored_recommendations", [])
            ignored = ignored + [rec]
            if len(ignored) > MAX_RECOMMENDATIONS:
                ignored = ignored[-MAX_RECOMMENDATIONS:]
            updated["ignored_recommendations"] = ignored
            changes.append(f"ignored: {rec.get('category', '?')} ({rec.get('id', '?')})")

    for pattern_str in (args.remove_pattern or []):
        patterns = updated.get("decision_patterns", [])
        if pattern_str in patterns:
            updated["decision_patterns"] = [p for p in patterns if p != pattern_str]
            changes.append(f"pattern removed: {pattern_str}")

    return updated, changes


def _parse_rec(rec_input):
    """Parse a recommendation from JSON string or structured input."""
    if isinstance(rec_input, dict):
        return rec_input
    try:
        rec = json.loads(rec_input)
        if "date" not in rec:
            rec["date"] = datetime.now().strftime("%Y-%m-%d")
        return rec
    except (json.JSONDecodeError, TypeError):
        print(f"Warning: could not parse recommendation: {rec_input}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Update boss-ai-agent learning config")
    parser.add_argument("--config", required=True, help="Path to config.json")

    # Display modes
    parser.add_argument("--show", action="store_true", help="Show current learning state")
    parser.add_argument("--reset", action="store_true", help="Reset all learning to defaults")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without saving")

    # Simple field updates
    parser.add_argument("--preferred-language", help="Set preferred language (e.g. 'zh', 'en')")
    parser.add_argument("--preferred-report-format", help="Set report format (e.g. 'concise', 'data-heavy')")
    parser.add_argument("--session-context", help="Set last session context summary")

    # List field updates (repeatable)
    parser.add_argument("--add-pattern", action="append", help="Add a decision pattern string")
    parser.add_argument("--remove-pattern", action="append", help="Remove a decision pattern string")
    parser.add_argument("--add-checkin-question", action="append", help="Add a custom check-in question")
    parser.add_argument("--add-adopted", action="append", help="Add adopted recommendation (JSON)")
    parser.add_argument("--add-ignored", action="append", help="Add ignored recommendation (JSON)")

    args = parser.parse_args()

    config = load_config(args.config)
    learning = config.get("learning", deepcopy(DEFAULT_LEARNING))

    # Show mode
    if args.show:
        print(show_learning(learning))
        return

    # Reset mode
    if args.reset:
        if args.dry_run:
            print("Would reset all learning fields to defaults.", file=sys.stderr)
            return
        new_config = {**config, "learning": deepcopy(DEFAULT_LEARNING)}
        save_config(args.config, new_config)
        print("Learning reset to defaults.")
        return

    # Apply updates
    new_learning, changes = apply_updates(learning, args)

    if not changes:
        print("No changes to apply.", file=sys.stderr)
        return

    # Report changes
    print(f"## Learning Updates ({len(changes)} changes)\n")
    for change in changes:
        print(f"- {change}")

    if args.dry_run:
        print(f"\n*Dry run — config not saved.*", file=sys.stderr)
        return

    new_config = {**config, "learning": new_learning}
    save_config(args.config, new_config)
    print(f"\nConfig updated successfully.")


if __name__ == "__main__":
    main()
