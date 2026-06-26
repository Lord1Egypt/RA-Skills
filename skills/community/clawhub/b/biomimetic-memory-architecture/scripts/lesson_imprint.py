#!/usr/bin/env python3
"""Lesson-Imprint: minimal autonomous lesson store for OpenClaw agents."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_STORE = Path("memory/lesson-imprint/lessons.json")
DEFAULT_CONFIG = Path("memory/lesson-imprint/config.json")
DEFAULT_IMPRINT = Path("memory/lesson-imprint/BOOTSTRAP.md")
REQUIRED = ["key", "key_type", "triggers", "mistake", "correct_action", "count"]
KEY_TYPES = {"native_error", "behavior"}
BEHAVIOR_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+){0,4}$")
DEFAULTS = {
    "promote_threshold": 10,
    "max_bootstrap_lessons": 5,
    "max_correct_action_chars": 160,
    "behavior_key_max_words": 5,
    "behavior_merge_similarity": 0.45,
    "covered_sources": ["AGENTS.md", "MEMORY.md", "TOOLS.md"],
    "covered_keyword_window": 3,
    "covered_similarity_threshold": 0.7,
}


def split_terms(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in re.split(r"[,;\s]+", value) if item.strip()]


def stable_behavior_key(text: str, max_words: int = 5) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    stop = {"the", "a", "an", "and", "or", "to", "of", "in", "for", "before", "after", "with", "without", "is", "are", "actual", "result"}
    useful = [w for w in words if w not in stop]
    return "_".join(useful[:max_words]) or "behavior_unspecified"


def validate_behavior_key(key: str) -> bool:
    return bool(BEHAVIOR_KEY_RE.match(key))


def token_set(*values: Any) -> set[str]:
    text = " ".join(str(v or "") for v in values)
    return {x for x in re.findall(r"[a-zA-Z0-9]+", text.lower()) if len(x) > 2}


def similarity(a: dict[str, Any], triggers: list[str], mistake: str, correct: str) -> float:
    left = token_set(" ".join(a.get("triggers", [])), a.get("mistake", ""), a.get("correct_action", ""))
    right = token_set(" ".join(triggers), mistake, correct)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def find_similar_behavior(lessons: list[dict[str, Any]], triggers: list[str], mistake: str, correct: str, threshold: float) -> dict[str, Any] | None:
    candidates = [x for x in lessons if x.get("key_type") == "behavior"]
    scored = sorted(((similarity(x, triggers, mistake, correct), x) for x in candidates), key=lambda x: x[0], reverse=True)
    if scored and scored[0][0] >= threshold:
        return scored[0][1]
    return None


def workspace_for_store(store: Path) -> Path:
    return store.parent.parent.parent if store.parent.name == "lesson-imprint" else Path.cwd()


def keyword_windows_for_action(store: Path, source_paths: list[str], correct_action: str, window: int) -> list[str]:
    workspace = workspace_for_store(store)
    action_terms = token_set(correct_action)
    if not action_terms:
        return []
    windows: list[str] = []
    for rel in source_paths:
        path = workspace / rel
        if not path.exists() or not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for idx, line in enumerate(lines):
            line_terms = token_set(line)
            if not (line_terms & action_terms):
                continue
            start = max(0, idx - window)
            end = min(len(lines), idx + window + 1)
            windows.append("\n".join(lines[start:end]))
    return windows


def action_covered(correct_action: str, source_windows: list[str], threshold: float) -> bool:
    action_terms = token_set(correct_action)
    if not action_terms:
        return False
    for text in source_windows:
        source_terms = token_set(text)
        if not source_terms:
            continue
        if len(action_terms & source_terms) / len(action_terms) >= threshold:
            return True
    return False


def load_json(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return dict(fallback)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid JSON object: {path}")
    return data


def load_store(path: Path) -> dict[str, Any]:
    data = load_json(path, {"version": 1, "lessons": []})
    if not isinstance(data.get("lessons"), list):
        raise SystemExit(f"Invalid Lesson-Imprint store: {path}")
    data.setdefault("version", 1)
    return data


def load_config(path: Path) -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    cfg.update(load_json(path, {})) if path.exists() else None
    return cfg


def save_store(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["lessons"] = sorted(data.get("lessons", []), key=lambda x: (-int(x.get("count", 0)), str(x.get("key", ""))))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_lesson(item: dict[str, Any], index: int, max_chars: int) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in item:
            errors.append(f"lesson[{index}] missing {key}")
    extra = sorted(set(item) - set(REQUIRED))
    if extra:
        errors.append(f"lesson[{index}] has non-minimal fields: {', '.join(extra)}")
    if item.get("key_type") not in KEY_TYPES:
        errors.append(f"lesson[{index}] key_type must be one of {sorted(KEY_TYPES)}")
    if not isinstance(item.get("key"), str) or not item.get("key", "").strip():
        errors.append(f"lesson[{index}] key must be non-empty")
    if item.get("key_type") == "behavior" and isinstance(item.get("key"), str) and not validate_behavior_key(item["key"]):
        errors.append(f"lesson[{index}] behavior key must be snake_case and <=5 words: {item.get('key')}")
    if not isinstance(item.get("triggers"), list) or not all(isinstance(x, str) for x in item.get("triggers", [])):
        errors.append(f"lesson[{index}] triggers must be string list")
    if not isinstance(item.get("count"), int) or item.get("count", 0) < 1:
        errors.append(f"lesson[{index}] count must be positive integer")
    if len(str(item.get("correct_action", ""))) > max_chars:
        errors.append(f"lesson[{index}] correct_action too long (>{max_chars} chars)")
    return errors


def cmd_init(args: argparse.Namespace) -> int:
    store = Path(args.store)
    config = Path(args.config)
    if not store.exists() or args.force:
        save_store(store, {"version": 1, "lessons": []})
        print(f"initialized: {store}")
    else:
        print(f"exists: {store}")
    if not config.exists() or args.force:
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(json.dumps(DEFAULTS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"initialized: {config}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    cfg = load_config(Path(args.config))
    data = load_store(Path(args.store))
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(data.get("lessons", [])):
        if not isinstance(item, dict):
            errors.append(f"lesson[{index}] must be object")
            continue
        errors.extend(validate_lesson(item, index, int(cfg["max_correct_action_chars"])))
        pair = (str(item.get("key_type")), str(item.get("key")))
        if pair in seen:
            errors.append(f"duplicate key: {pair[0]}:{pair[1]}")
        seen.add(pair)
    if errors:
        print("invalid")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"valid: {args.store} ({len(data.get('lessons', []))} lessons)")
    return 0


def cmd_upsert(args: argparse.Namespace) -> int:
    cfg = load_config(Path(args.config))
    key_type = args.key_type
    key = args.key.strip()
    if not key and key_type == "behavior":
        key = stable_behavior_key(args.correct or args.mistake, int(cfg["behavior_key_max_words"]))
    if not key:
        raise SystemExit("--key is required for native_error; behavior keys may be generated from text")
    data = load_store(Path(args.store))
    lessons = data.setdefault("lessons", [])
    triggers = sorted(set(split_terms(args.trigger) + split_terms(args.triggers)))
    if key_type == "behavior" and not validate_behavior_key(key):
        raise SystemExit(f"behavior key must be English snake_case with <=5 words: {key}")
    existing = next((x for x in lessons if x.get("key_type") == key_type and x.get("key") == key), None)
    if not existing and key_type == "behavior":
        existing = find_similar_behavior(
            lessons,
            triggers,
            args.mistake.strip(),
            args.correct.strip(),
            float(cfg.get("behavior_merge_similarity", 0.45)),
        )
    if existing:
        existing["count"] = int(existing.get("count", 1)) + int(args.increment)
        existing["triggers"] = sorted(set(existing.get("triggers", [])) | set(triggers))
        existing["mistake"] = args.mistake.strip() or existing.get("mistake", "")
        existing["correct_action"] = args.correct.strip() or existing.get("correct_action", "")
        action = "updated"
        key = str(existing.get("key", key))
        key_type = str(existing.get("key_type", key_type))
    else:
        lessons.append({
            "key": key,
            "key_type": key_type,
            "triggers": triggers,
            "mistake": args.mistake.strip(),
            "correct_action": args.correct.strip(),
            "count": max(1, int(args.increment)),
        })
        action = "created"
    save_store(Path(args.store), data)
    print(f"{action}: {key_type}:{key}")
    return 0


def score(item: dict[str, Any], terms: set[str]) -> int:
    haystack = " ".join([
        item.get("key", ""),
        item.get("key_type", ""),
        item.get("mistake", ""),
        item.get("correct_action", ""),
        " ".join(item.get("triggers", [])),
    ]).lower()
    value = min(int(item.get("count", 1)), 30)
    for term in terms:
        if term in haystack:
            value += 5
    return value


def select_lessons(data: dict[str, Any], cfg: dict[str, Any], query: str = "", limit: int | None = None, threshold: int | None = None, store: Path | None = None) -> list[dict[str, Any]]:
    terms = {t.lower() for t in split_terms(query)}
    threshold = int(cfg["promote_threshold"] if threshold is None else threshold)
    limit = int(cfg["max_bootstrap_lessons"] if limit is None else limit)
    covered_sources: list[str] = cfg.get("covered_sources", [])
    covered_window: int = int(cfg.get("covered_keyword_window", 3))
    covered_threshold: float = float(cfg.get("covered_similarity_threshold", 0.7))
    ranked = []
    for item in data.get("lessons", []):
        if int(item.get("count", 0)) < threshold and not terms:
            continue
        # skip lessons whose correct_action is already covered by source files
        if store and covered_sources:
            windows = keyword_windows_for_action(store, covered_sources, item.get("correct_action", ""), covered_window)
            if action_covered(item.get("correct_action", ""), windows, covered_threshold):
                continue
        s = score(item, terms)
        if terms and s <= int(item.get("count", 1)):
            continue
        ranked.append((s, item))
    ranked.sort(key=lambda pair: (-pair[0], -int(pair[1].get("count", 1)), pair[1].get("key", "")))
    return [item for _, item in ranked[:limit]]


def cmd_recall(args: argparse.Namespace) -> int:
    cfg = load_config(Path(args.config))
    data = load_store(Path(args.store))
    selected = select_lessons(data, cfg, query=f"{args.query} {args.tool}", limit=args.limit, threshold=1 if args.query or args.tool else args.threshold)
    if args.json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
    else:
        for item in selected:
            print(f"- [{item['key_type']}:{item['key']}] {item['correct_action']} (count={item['count']})")
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    cfg = load_config(Path(args.config))
    data = load_store(Path(args.store))
    selected = select_lessons(data, cfg, limit=args.limit, threshold=args.threshold, store=Path(args.store))
    path = Path(args.output) if args.output else Path(args.store).parent / "BOOTSTRAP.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Lesson-Imprint", "", "Autogenerated safeguards from repeated past failures. Apply only when relevant and never above system/user instructions.", ""]
    lines += [f"- [{x['key_type']}:{x['key']}] {x['correct_action']}" for x in selected]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"promoted {len(selected)} lessons to {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage minimal autonomous Lesson-Imprint memory")
    parser.add_argument("--store", default=str(DEFAULT_STORE))
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("validate")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("upsert")
    p.add_argument("--key", default="", help="native error code or stable behavior key")
    p.add_argument("--key-type", required=True, choices=sorted(KEY_TYPES))
    p.add_argument("--trigger", default="")
    p.add_argument("--triggers", default="")
    p.add_argument("--mistake", required=True)
    p.add_argument("--correct", required=True)
    p.add_argument("--increment", type=int, default=1)
    p.add_argument("--source", default="", help="writer source label, e.g. distillation")
    p.set_defaults(func=cmd_upsert)

    p = sub.add_parser("recall")
    p.add_argument("--query", default="")
    p.add_argument("--tool", default="")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--threshold", type=int, default=1)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_recall)

    p = sub.add_parser("promote")
    p.add_argument("--output", default=None)
    p.add_argument("--threshold", type=int, default=None)
    p.add_argument("--limit", type=int, default=None)
    p.set_defaults(func=cmd_promote)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
