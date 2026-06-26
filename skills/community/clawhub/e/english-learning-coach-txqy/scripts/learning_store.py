#!/usr/bin/env python3
"""Portable local store for the English Learning Coach skill."""

from __future__ import annotations

import argparse
import json
import os
from json import JSONDecodeError
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DATA_ENV = "ENGLISH_LEARNING_COACH_DATA_DIR"
SCORE_KEYS = ("grammar", "vocabulary", "naturalness", "clarity", "total")
OUTPUT_LEVELS = ("A1-A2", "A2-B1", "B1-B2", "B2-C1")
DEFAULT_OUTPUT_LEVEL = "A2-B1"
DEFAULT_OUTPUT_MODE = "adaptive"
DEFAULT_OUTPUT_OFFSET = "slightly_below_user"
DEFAULT_MAX_STRETCH_WORDS = 1


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve_data_dir(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    if os.environ.get(DATA_ENV):
        return Path(os.environ[DATA_ENV]).expanduser().resolve()
    return SKILL_ROOT / "data"


def profile_template() -> dict[str, Any]:
    return {
        "updated_at": None,
        "cefr_estimate": {
            "level": "unknown",
            "confidence": "low",
            "basis": "No learner messages have been recorded yet.",
            "history": [],
        },
        "output_level": output_level_template(),
        "active_vocabulary_count": 0,
        "message_count": 0,
        "pass_count": 0,
        "corrected_count": 0,
        "scores": {
            "grammar_avg": None,
            "vocabulary_avg": None,
            "naturalness_avg": None,
            "clarity_avg": None,
            "total_avg": None,
        },
        "error_rates": {},
        "recent_trend": "not_enough_data",
    }


def output_level_template() -> dict[str, Any]:
    return {
        "mode": DEFAULT_OUTPUT_MODE,
        "current": DEFAULT_OUTPUT_LEVEL,
        "default": DEFAULT_OUTPUT_LEVEL,
        "offset": DEFAULT_OUTPUT_OFFSET,
        "max_stretch_words_per_reply": DEFAULT_MAX_STRETCH_WORDS,
        "confidence": "low",
        "reason": "Default level before enough learner data.",
        "updated_at": None,
        "history": [],
    }


def vocab_template() -> dict[str, Any]:
    return {"updated_at": None, "active_vocabulary_count": 0, "lemmas": {}}


def checkpoints_template() -> dict[str, Any]:
    return {"updated_at": None, "checkpoints": []}


def error_book_template() -> str:
    return (
        "# Error Book\n\n"
        "This file records recurring English mistakes in a human-readable format.\n\n"
        "## Recurring Patterns\n\n"
        "No recurring patterns yet.\n\n"
        "## Recent Corrections\n\n"
        "No corrections yet.\n"
    )


def read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def init_store(data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    files: list[tuple[str, Any]] = [
        ("profile.json", profile_template()),
        ("vocab.json", vocab_template()),
        ("checkpoints.json", checkpoints_template()),
    ]
    for name, template in files:
        path = data_dir / name
        if not path.exists():
            write_json(path, template)
    events = data_dir / "events.jsonl"
    if not events.exists():
        events.write_text("", encoding="utf-8")
    error_book = data_dir / "error-book.md"
    if not error_book.exists():
        error_book.write_text(error_book_template(), encoding="utf-8")


def parse_json_arg(value: str) -> dict[str, Any]:
    if value == "-":
        value = input()
    try:
        data = json.loads(value)
    except JSONDecodeError:
        if '\\"' not in value:
            raise
        data = json.loads(value.replace('\\"', '"'))
    if not isinstance(data, dict):
        raise SystemExit("JSON argument must be an object.")
    return data


def normalized_verdict(value: Any) -> str:
    text = str(value or "pass").strip().lower()
    if text in {"pass", "passed", "correct", "ok"}:
        return "pass"
    if text in {"corrected", "needs_correction", "fail", "failed"}:
        return "corrected"
    return text


def ensure_output_level(profile: dict[str, Any]) -> dict[str, Any]:
    defaults = output_level_template()
    output_level = profile.setdefault("output_level", {})
    if not isinstance(output_level, dict):
        output_level = defaults
        profile["output_level"] = output_level
    for key, value in defaults.items():
        output_level.setdefault(key, value)
    if output_level.get("current") not in OUTPUT_LEVELS:
        output_level["current"] = DEFAULT_OUTPUT_LEVEL
    if output_level.get("mode") not in {"adaptive", "fixed"}:
        output_level["mode"] = DEFAULT_OUTPUT_MODE
    return output_level


def output_level_index(level: str) -> int:
    try:
        return OUTPUT_LEVELS.index(level)
    except ValueError:
        return OUTPUT_LEVELS.index(DEFAULT_OUTPUT_LEVEL)


def lower_output_level(level: str) -> str:
    idx = max(0, output_level_index(level) - 1)
    return OUTPUT_LEVELS[idx]


def raise_output_level(level: str) -> str:
    idx = min(len(OUTPUT_LEVELS) - 1, output_level_index(level) + 1)
    return OUTPUT_LEVELS[idx]


def set_output_level(
    profile: dict[str, Any],
    level: str,
    *,
    mode: str | None = None,
    reason: str,
    confidence: str = "medium",
    timestamp: str | None = None,
) -> dict[str, Any]:
    if level not in OUTPUT_LEVELS:
        raise SystemExit(f"Invalid output level: {level}. Use one of: {', '.join(OUTPUT_LEVELS)}")
    timestamp = timestamp or now_iso()
    output_level = ensure_output_level(profile)
    output_level["current"] = level
    if mode:
        output_level["mode"] = mode
    output_level["confidence"] = confidence
    output_level["reason"] = reason
    output_level["updated_at"] = timestamp
    history = output_level.setdefault("history", [])
    history.append({"timestamp": timestamp, "level": level, "mode": output_level.get("mode"), "reason": reason})
    output_level["history"] = history[-20:]
    return output_level


def recommended_level_from_cefr(cefr_value: Any) -> str:
    text = str(cefr_value or "").upper()
    if "C1" in text or "C2" in text:
        return "B2-C1"
    if "B2" in text:
        return "B1-B2"
    if "B1" in text:
        return "A2-B1"
    if "A1" in text or "A2" in text:
        return "A2-B1"
    return DEFAULT_OUTPUT_LEVEL


def apply_level_feedback(profile: dict[str, Any], feedback: Any, timestamp: str) -> bool:
    text = str(feedback or "").strip().lower()
    output_level = ensure_output_level(profile)
    if text in {"too_hard", "hard", "simpler", "lower", "太难了", "简单点"}:
        set_output_level(
            profile,
            lower_output_level(output_level["current"]),
            reason="User said the output was too difficult.",
            confidence="high",
            timestamp=timestamp,
        )
        return True
    if text in {"too_easy", "easy", "harder", "raise", "难一点", "挑战我"}:
        set_output_level(
            profile,
            raise_output_level(output_level["current"]),
            reason="User asked for a slightly harder level.",
            confidence="medium",
            timestamp=timestamp,
        )
        return True
    if text in {"auto", "adaptive"}:
        output_level["mode"] = "adaptive"
        output_level["reason"] = "Returned to adaptive output-level mode."
        output_level["updated_at"] = timestamp
        return True
    return False


def adapt_output_level(profile: dict[str, Any], timestamp: str, signal: dict[str, Any] | None = None) -> None:
    output_level = ensure_output_level(profile)
    if signal and apply_level_feedback(profile, signal.get("level_feedback"), timestamp):
        return
    if output_level.get("mode") != "adaptive":
        return

    message_count = int(profile.get("message_count", 0))
    checkpoint_count = int(profile.get("checkpoint_count", 0))
    if message_count < 30 and checkpoint_count < 1:
        if output_level.get("current") != DEFAULT_OUTPUT_LEVEL:
            set_output_level(
                profile,
                DEFAULT_OUTPUT_LEVEL,
                reason="Default level before enough learner data.",
                confidence="low",
                timestamp=timestamp,
            )
        return

    cefr = profile.get("cefr_estimate", {}).get("level")
    recommended = recommended_level_from_cefr(cefr)
    correction_rate = 0.0
    if message_count:
        correction_rate = int(profile.get("corrected_count", 0)) / message_count
    if correction_rate >= 0.4:
        recommended = lower_output_level(recommended)

    if recommended != output_level.get("current"):
        set_output_level(
            profile,
            recommended,
            reason="Adapted from CEFR estimate, correction rate, and checkpoint signals.",
            confidence="medium" if checkpoint_count else "low",
            timestamp=timestamp,
        )


def update_scores(profile: dict[str, Any], event_scores: dict[str, Any], n: int) -> None:
    scores = profile.setdefault("scores", {})
    for key in SCORE_KEYS:
        value = event_scores.get(key)
        if not isinstance(value, (int, float)):
            continue
        avg_key = f"{key}_avg"
        old = scores.get(avg_key)
        if old is None or n <= 1:
            scores[avg_key] = round(float(value), 2)
        else:
            scores[avg_key] = round(((float(old) * (n - 1)) + float(value)) / n, 2)


def update_vocab(vocab: dict[str, Any], event: dict[str, Any], timestamp: str) -> None:
    lemmas = vocab.setdefault("lemmas", {})
    example = str(event.get("input") or "")[:180]
    for raw in event.get("lemmas") or []:
        lemma = str(raw).strip().lower()
        if not lemma:
            continue
        entry = lemmas.setdefault(
            lemma,
            {
                "count": 0,
                "first_seen": timestamp,
                "last_seen": timestamp,
                "estimated_cefr": None,
                "examples": [],
            },
        )
        entry["count"] = int(entry.get("count", 0)) + 1
        entry["last_seen"] = timestamp
        if example and example not in entry.setdefault("examples", []):
            entry["examples"].append(example)
            entry["examples"] = entry["examples"][-3:]
    vocab["active_vocabulary_count"] = len(lemmas)
    vocab["updated_at"] = timestamp


def append_error_book(data_dir: Path, event: dict[str, Any], timestamp: str) -> None:
    if normalized_verdict(event.get("verdict")) != "corrected":
        return
    errors = event.get("errors") or []
    if not errors:
        return
    lines = [f"\n### Correction {timestamp}\n", f"- Original: {event.get('input', '')}\n"]
    if event.get("correction"):
        lines.append(f"- Correction: {event['correction']}\n")
    for error in errors:
        if not isinstance(error, dict):
            continue
        category = error.get("category", "unknown")
        span = error.get("span", "")
        fix = error.get("fix", "")
        note = error.get("note", "")
        lines.append(f"- [{category}] {span} -> {fix}. {note}\n")
    with (data_dir / "error-book.md").open("a", encoding="utf-8") as fh:
        fh.writelines(lines)


def record_event(data_dir: Path, event: dict[str, Any]) -> None:
    init_store(data_dir)
    timestamp = str(event.get("timestamp") or now_iso())
    event["timestamp"] = timestamp
    event["verdict"] = normalized_verdict(event.get("verdict"))

    with (data_dir / "events.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")

    profile_path = data_dir / "profile.json"
    vocab_path = data_dir / "vocab.json"
    profile = read_json(profile_path, profile_template())
    vocab = read_json(vocab_path, vocab_template())
    ensure_output_level(profile)

    profile["message_count"] = int(profile.get("message_count", 0)) + 1
    if event["verdict"] == "corrected":
        profile["corrected_count"] = int(profile.get("corrected_count", 0)) + 1
    else:
        profile["pass_count"] = int(profile.get("pass_count", 0)) + 1

    update_scores(profile, event.get("scores") or {}, profile["message_count"])
    update_vocab(vocab, event, timestamp)

    error_rates = profile.setdefault("error_rates", {})
    for error in event.get("errors") or []:
        if isinstance(error, dict):
            category = str(error.get("category") or "unknown")
            error_rates[category] = int(error_rates.get(category, 0)) + 1

    signals = event.get("cefr_signals") or {}
    cefr_range = signals.get("range")
    if cefr_range and str(cefr_range).lower() != "unknown":
        estimate = profile.setdefault("cefr_estimate", {})
        estimate["level"] = cefr_range
        estimate["confidence"] = signals.get("confidence", estimate.get("confidence", "low"))
        estimate["basis"] = signals.get("complexity", "Updated from recent practice event.")
        history = estimate.setdefault("history", [])
        history.append({"timestamp": timestamp, "level": cefr_range, "source": "event"})
        estimate["history"] = history[-20:]

    profile["active_vocabulary_count"] = vocab.get("active_vocabulary_count", 0)
    adapt_output_level(profile, timestamp, event)
    profile["updated_at"] = timestamp
    write_json(profile_path, profile)
    write_json(vocab_path, vocab)
    append_error_book(data_dir, event, timestamp)


def record_checkpoint(data_dir: Path, checkpoint: dict[str, Any]) -> None:
    init_store(data_dir)
    timestamp = str(checkpoint.get("timestamp") or now_iso())
    checkpoint["timestamp"] = timestamp
    path = data_dir / "checkpoints.json"
    data = read_json(path, checkpoints_template())
    data.setdefault("checkpoints", []).append(checkpoint)
    data["updated_at"] = timestamp
    write_json(path, data)

    profile_path = data_dir / "profile.json"
    profile = read_json(profile_path, profile_template())
    ensure_output_level(profile)
    cefr = checkpoint.get("cefr_estimate")
    if cefr:
        estimate = profile.setdefault("cefr_estimate", {})
        estimate["level"] = cefr
        estimate["confidence"] = checkpoint.get("confidence", "medium")
        estimate["basis"] = checkpoint.get("basis", "Updated from checkpoint.")
        history = estimate.setdefault("history", [])
        history.append({"timestamp": timestamp, "level": cefr, "source": "checkpoint"})
        estimate["history"] = history[-20:]
    profile["checkpoint_count"] = len(data.get("checkpoints", []))
    adapt_output_level(profile, timestamp, checkpoint)
    profile["updated_at"] = timestamp
    write_json(profile_path, profile)


def manage_level(
    data_dir: Path,
    *,
    set_level: str | None = None,
    auto: bool = False,
    feedback: str | None = None,
) -> dict[str, Any]:
    init_store(data_dir)
    timestamp = now_iso()
    profile_path = data_dir / "profile.json"
    profile = read_json(profile_path, profile_template())
    output_level = ensure_output_level(profile)

    if set_level:
        output_level = set_output_level(
            profile,
            set_level,
            mode="fixed",
            reason="User manually set output level.",
            confidence="high",
            timestamp=timestamp,
        )
    elif auto:
        output_level["mode"] = "adaptive"
        output_level["reason"] = "User returned output level to adaptive mode."
        output_level["updated_at"] = timestamp
        adapt_output_level(profile, timestamp)
    elif feedback:
        apply_level_feedback(profile, feedback, timestamp)

    profile["updated_at"] = timestamp
    write_json(profile_path, profile)
    return ensure_output_level(profile)


def stats(data_dir: Path) -> dict[str, Any]:
    init_store(data_dir)
    profile = read_json(data_dir / "profile.json", profile_template())
    ensure_output_level(profile)
    vocab = read_json(data_dir / "vocab.json", vocab_template())
    checkpoints = read_json(data_dir / "checkpoints.json", checkpoints_template())
    events_path = data_dir / "events.jsonl"
    event_count = 0
    if events_path.exists():
        event_count = sum(1 for line in events_path.read_text(encoding="utf-8").splitlines() if line.strip())
    return {
        "profile": profile,
        "active_vocabulary_count": vocab.get("active_vocabulary_count", 0),
        "event_count": event_count,
        "checkpoint_count": len(checkpoints.get("checkpoints", [])),
        "data_dir": str(data_dir),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage English Learning Coach local data.")
    parser.add_argument("--data-dir", default=None, help="Override data directory.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create missing data files.")

    record = sub.add_parser("record", help="Append an event and update profile/vocab.")
    record.add_argument("--event-json", required=True, help="Event JSON object, or '-' to read one line from stdin.")

    checkpoint = sub.add_parser("checkpoint", help="Append a checkpoint result.")
    checkpoint.add_argument("--checkpoint-json", required=True, help="Checkpoint JSON object, or '-' to read one line from stdin.")

    level = sub.add_parser("level", help="Show or update the agent output vocabulary level.")
    level.add_argument("--set", dest="set_level", choices=OUTPUT_LEVELS, help="Fix output level manually.")
    level.add_argument("--auto", action="store_true", help="Return to adaptive output-level mode.")
    level.add_argument("--feedback", choices=("too_hard", "too_easy", "auto"), help="Apply level feedback.")

    sub.add_parser("stats", help="Print current stats as JSON.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    data_dir = resolve_data_dir(args.data_dir)
    if args.command == "init":
        init_store(data_dir)
        print(json.dumps({"ok": True, "data_dir": str(data_dir)}, ensure_ascii=False))
    elif args.command == "record":
        record_event(data_dir, parse_json_arg(args.event_json))
        print(json.dumps({"ok": True, "data_dir": str(data_dir)}, ensure_ascii=False))
    elif args.command == "checkpoint":
        record_checkpoint(data_dir, parse_json_arg(args.checkpoint_json))
        print(json.dumps({"ok": True, "data_dir": str(data_dir)}, ensure_ascii=False))
    elif args.command == "level":
        output_level = manage_level(
            data_dir,
            set_level=args.set_level,
            auto=args.auto,
            feedback=args.feedback,
        )
        print(json.dumps({"ok": True, "output_level": output_level, "data_dir": str(data_dir)}, ensure_ascii=False, indent=2))
    elif args.command == "stats":
        print(json.dumps(stats(data_dir), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
