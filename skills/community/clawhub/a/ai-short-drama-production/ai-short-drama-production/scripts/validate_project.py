#!/usr/bin/env python3
"""Validate a reusable AI short-drama project structure and key CSVs."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REQUIRED_FILES = {
    "project_profile.json": [],
    "00_admin/production_brief.md": [],
    "01_story/scene_breakdown.csv": ["scene_id", "objective", "obstacle", "tactic", "turn", "exit_hook"],
    "01_story/continuity_ledger.csv": ["scene_id", "character_id", "state_start", "state_end"],
    "01_story/retention_plan.csv": ["series", "episode", "opening_hook", "opening_question", "midpoint_turn", "cliffhanger", "payoff", "comment_prompt", "shareable_moment", "next_episode_tease"],
    "02_visual_bible/technique_plan.csv": ["technique_id", "story_purpose", "originality_check"],
    "03_characters/character_registry.csv": ["asset_id", "name", "path", "rights_owner", "status"],
    "06_shots/shot_manifest.csv": ["shot_id", "prompt", "duration_sec", "coverage_role", "camera_intention", "character_ids"],
    "07_audio/voice_timeline.csv": ["shot_id", "character", "line", "lipsync_required"],
    "11_deliverables/delivery_manifest.csv": ["deliverable_id", "file_path", "sha256", "status"],
}

PROFILE_REQUIRED = ["project", "format", "series", "characters", "models", "generation", "policies", "audience", "release"]
SENSITIVE_TOKENS = ("api_key", "secret", "token", "password")


def find_sensitive_keys(obj, prefix=""):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            if any(t in k.lower() for t in SENSITIVE_TOKENS) and v not in ("", None, [], {}):
                found.append(key)
            found.extend(find_sensitive_keys(v, key))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found.extend(find_sensitive_keys(v, f"{prefix}[{i}]"))
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir")
    parser.add_argument("--require-data", action="store_true", help="Treat empty production CSVs as failures")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_dir).expanduser().resolve()
    errors, warnings, info = [], [], {"project_dir": str(root), "files": {}}
    if not root.exists():
        print(f"Project directory does not exist: {root}")
        sys.exit(1)

    for rel, required_headers in REQUIRED_FILES.items():
        p = root / rel
        if not p.exists():
            errors.append(f"missing file: {rel}")
            continue
        info["files"][rel] = {"bytes": p.stat().st_size}
        if p.suffix.lower() == ".csv":
            with p.open(encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                rows = list(reader)
            missing = [h for h in required_headers if h not in headers]
            if missing:
                errors.append(f"{rel}: missing headers {missing}")
            info["files"][rel].update({"rows": len(rows), "headers": headers})
            if args.require_data and not rows:
                errors.append(f"{rel}: no data rows")

    profile_path = root / "project_profile.json"
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"project_profile.json: invalid JSON: {e}")
            profile = {}
        missing = [k for k in PROFILE_REQUIRED if k not in profile]
        if missing:
            errors.append(f"project_profile.json: missing keys {missing}")
        sensitive = find_sensitive_keys(profile)
        if sensitive:
            errors.append(f"project_profile.json: possible secrets in {sensitive}")
        if profile.get("policies", {}).get("paid_generation_requires_approval") is not True:
            warnings.append("paid_generation_requires_approval is not true")
        if profile.get("policies", {}).get("text_in_post") is not True:
            warnings.append("text_in_post is not true")
        info["profile"] = {
            "project_id": profile.get("project", {}).get("project_id"),
            "project_name": profile.get("project", {}).get("project_name"),
            "deliverable_type": profile.get("project", {}).get("deliverable_type"),
        }

    # seedance task ranges
    shot_path = root / "06_shots/shot_manifest.csv"
    if shot_path.exists():
        with shot_path.open(encoding="utf-8-sig", newline="") as f:
            for i, row in enumerate(csv.DictReader(f), start=2):
                try:
                    d = float(row.get("duration_sec") or 0)
                except ValueError:
                    warnings.append(f"shot_manifest row {i}: invalid duration_sec")
                    continue
                if d and not (4 <= d <= 30):
                    warnings.append(f"shot_manifest row {i}: duration {d} outside common 4-30s task range")
                if not (row.get("prompt") or "").strip():
                    warnings.append(f"shot_manifest row {i}: empty prompt")

    result = {"status": "fail" if errors else "pass", "errors": errors, "warnings": warnings, "info": info}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"STATUS: {result['status'].upper()}")
        print(f"Project: {root}")
        for e in errors:
            print(f"[FAIL] {e}")
        for w in warnings:
            print(f"[WARN] {w}")
        for rel, meta in info["files"].items():
            print(f"[FILE] {rel}: {meta.get('bytes', 0)} bytes, rows={meta.get('rows', '-')}")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
