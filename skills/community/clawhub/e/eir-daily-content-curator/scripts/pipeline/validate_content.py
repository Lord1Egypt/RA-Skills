#!/usr/bin/env python3
"""
Pre-POST content validation script.
Checks generated content JSON against content-spec rules before POST.

Usage:
  python3 -m pipeline.validate_content                    # validate all in generated/
  python3 -m pipeline.validate_content --file <path>.json # validate one file
  python3 -m pipeline.validate_content --fix              # auto-fix where possible

Exit code 0 = all pass, 1 = has errors (blocks POST), 2 = has warnings only.
"""

import json
import sys
from pathlib import Path

from .config import GENERATED_DIR, V9_DIR

VALID_CATEGORIES = {"focus", "attention", "seed", "whisper"}


def validate_content(data, task_data=None, fix=False):
    """Validate a content JSON object. Returns (errors, warnings, fixes)."""
    errors = []   # blocks POST
    warnings = [] # quality issues
    fixes = []    # auto-fixed issues

    slug = data.get("slug", "?")

    # --- Required fields ---
    if not data.get("lang") or data["lang"] not in ("zh", "en"):
        errors.append("missing or invalid lang (must be 'zh' or 'en')")

    if not data.get("dot"):
        errors.append("missing dot object")
    else:
        dot = data["dot"]
        hook = dot.get("hook", "")
        if not hook:
            errors.append("dot.hook is empty")
        elif len(hook) > 100:
            errors.append(f"dot.hook too long ({len(hook)} chars, max 100)")
        elif len(hook) > 50:
            warnings.append(f"dot.hook is {len(hook)} chars (recommend ≤10 CJK / ≤6 EN words)")

        cat = dot.get("category", "")
        if cat not in VALID_CATEGORIES:
            errors.append(f"dot.category '{cat}' not in {VALID_CATEGORIES}")


    if not data.get("l1"):
        errors.append("missing l1 object")
    else:
        l1 = data["l1"]
        title = l1.get("title", "")
        if not title:
            errors.append("l1.title is empty")
        elif len(title) > 200:
            errors.append(f"l1.title too long ({len(title)} chars, max 200)")

        summary = l1.get("summary", "")
        if not summary:
            warnings.append("l1.summary is empty")

        bullets = l1.get("bullets", [])
        if not isinstance(bullets, list):
            errors.append("l1.bullets must be an array")
        elif len(bullets) > 10:
            errors.append(f"l1.bullets has {len(bullets)} items (max 10)")
        elif len(bullets) == 0:
            warnings.append("l1.bullets is empty")

        # via should NOT be set by writer
        if l1.get("via"):
            warnings.append("l1.via is set (pipeline auto-generates this)")

        kq = l1.get("key_quote")
        if kq is not None and not isinstance(kq, str):
            errors.append("l1.key_quote must be a string, not " + type(kq).__name__)

    # --- l2 (recommended) ---
    l2 = data.get("l2")
    if not l2:
        warnings.append("l2 is missing (strongly recommended)")
    else:
        content = l2.get("content", "")
        if not content:
            warnings.append("l2.content is empty")
        elif len(content) < 300:
            warnings.append(f"l2.content is short ({len(content)} chars, recommend ≥300)")

        # Check for literal \n\n (double-escaped newlines)
        if "\\n" in content:
            if fix:
                data["l2"]["content"] = content.replace("\\n\\n", "\n\n").replace("\\n", "\n")
                fixes.append("l2.content: fixed literal \\n to real newlines")
            else:
                errors.append("l2.content contains literal '\\n' (should be real newlines)")

        eir_take = l2.get("eir_take", "")
        if not eir_take:
            warnings.append("l2.eir_take is empty")

        context = l2.get("context", "")
        if not context:
            warnings.append("l2.context is empty")

        l2_bullets = l2.get("bullets", [])
        if l2_bullets and not isinstance(l2_bullets, list):
            errors.append("l2.bullets must be an array")

    # --- sources ---
    sources = data.get("sources", [])
    if not sources:
        errors.append("sources is empty (at least 1 required)")
    elif len(sources) > 10:
        errors.append(f"sources has {len(sources)} items (max 10)")
    else:
        for i, s in enumerate(sources):
            url = s.get("url", "")
            if not url:
                errors.append(f"sources[{i}].url is empty")
            elif not url.startswith("http"):
                errors.append(f"sources[{i}].url is not a valid URL: {url[:50]}")

    # --- interests ---
    interests = data.get("interests")
    if not interests:
        warnings.append("interests is missing (recommended)")
    else:
        anchor = interests.get("anchor", [])
        if not anchor:
            warnings.append("interests.anchor is empty")
        topic_slug = data.get("topicSlug", "")
        if anchor and topic_slug and anchor[0] != topic_slug:
            errors.append(f"interests.anchor[0] '{anchor[0]}' != topicSlug '{topic_slug}'")

    # --- topicSlug vs task cross-check ---
    if task_data:
        expected_topic = task_data.get("topic_slug", "")
        actual_topic = data.get("topicSlug", "")
        if expected_topic and actual_topic != expected_topic:
            if fix:
                data["topicSlug"] = expected_topic
                if data.get("interests", {}).get("anchor"):
                    data["interests"]["anchor"] = [expected_topic]
                fixes.append(f"topicSlug: '{actual_topic}' → '{expected_topic}' (from task)")
            else:
                errors.append(f"topicSlug '{actual_topic}' doesn't match task topic_slug '{expected_topic}'")

    # --- null check ---
    def check_nulls(obj, path=""):
        if obj is None:
            errors.append(f"null value at {path} (use '' or [] instead)")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                check_nulls(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                check_nulls(v, f"{path}[{i}]")
    check_nulls(data)

    return errors, warnings, fixes


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate content before POST")
    parser.add_argument("--file", help="Validate a specific file")
    parser.add_argument("--fix", action="store_true", help="Auto-fix where possible")
    args = parser.parse_args()

    tasks_dir = V9_DIR / "tasks"

    if args.file:
        files = [Path(args.file)]
    else:
        files = sorted(GENERATED_DIR.glob("*_zh.json"))

    total_errors = 0
    total_warnings = 0
    total_fixes = 0

    for f in files:
        data = json.loads(f.read_text())
        slug = data.get("slug", f.stem)

        # Try to load matching task file for cross-check
        content_slug = slug
        task_file = tasks_dir / f"{content_slug}.json"
        task_data = json.loads(task_file.read_text()) if task_file.exists() else None

        errors, warnings, fixes = validate_content(data, task_data, fix=args.fix)

        if errors or warnings or fixes:
            print(f"\n{'❌' if errors else '⚠️'} {f.name}")
            for e in errors:
                print(f"  ERROR: {e}")
            for w in warnings:
                print(f"  WARN:  {w}")
            for fx in fixes:
                print(f"  FIXED: {fx}")

            if args.fix and fixes:
                f.write_text(json.dumps(data, ensure_ascii=False, indent=2))
                print(f"  💾 Saved fixes to {f.name}")

        total_errors += len(errors)
        total_warnings += len(warnings)
        total_fixes += len(fixes)

    print(f"\n📊 Validation: {len(files)} files, {total_errors} errors, {total_warnings} warnings, {total_fixes} fixes")

    if total_errors > 0:
        sys.exit(1)
    elif total_warnings > 0:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
