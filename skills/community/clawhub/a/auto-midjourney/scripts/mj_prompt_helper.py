#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mj_alpha import (
    apply_preset,
    append_negative_terms,
    normalize_prompt,
    print_json,
    resolve_named_suffix,
)


TEMPLATES: dict[str, list[str]] = {
    "portrait": ["subject", "framing", "camera", "lighting", "background", "mood", "details"],
    "product": ["subject", "material", "camera", "surface", "lighting", "background", "mood", "details"],
    "environment": ["subject", "time_of_day", "camera", "hero_details", "materials", "mood", "palette", "details"],
    "character": ["subject", "wardrobe", "pose", "expression", "background", "lighting", "style", "details"],
    "character_sheet": ["sheet_layout", "closeup", "subject", "wardrobe", "pose", "background", "lighting", "style", "details"],
    "custom": ["subject", "details"],
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a Midjourney V8-friendly prompt from structured fields.")
    parser.add_argument("--template", choices=sorted(TEMPLATES), default="custom", help="Prompt template")
    parser.add_argument("--subject", required=True, help="Main subject or scene")
    parser.add_argument("--framing", help="Portrait framing or crop style")
    parser.add_argument("--camera", help="Lens, focal length, or camera feel")
    parser.add_argument("--lighting", help="Lighting style")
    parser.add_argument("--background", help="Background or environment")
    parser.add_argument("--mood", help="Mood or art direction")
    parser.add_argument("--details", help="Additional details")
    parser.add_argument("--sheet-layout", dest="sheet_layout", help="Sheet composition or multi-view layout")
    parser.add_argument("--closeup", help="Close-up panel description for split-view sheets")
    parser.add_argument("--material", help="Materials or finishes")
    parser.add_argument("--surface", help="Surface under the subject")
    parser.add_argument("--time-of-day", dest="time_of_day", help="Time of day or weather")
    parser.add_argument("--hero-details", dest="hero_details", help="Hero objects or focal details")
    parser.add_argument("--materials", help="Architectural or scene materials")
    parser.add_argument("--palette", help="Color palette")
    parser.add_argument("--wardrobe", help="Wardrobe or costume")
    parser.add_argument("--pose", help="Pose")
    parser.add_argument("--expression", help="Expression")
    parser.add_argument("--style", help="Rendering or illustration style")
    parser.add_argument("--preset", help="Preset name from config/presets.example.json")
    parser.add_argument("--presets-file", default="config/presets.example.json", help="Path to presets JSON")
    parser.add_argument("--quality-profile", help="Quality profile name from config/quality-profiles.example.json")
    parser.add_argument("--quality-profiles-file", default="config/quality-profiles.example.json", help="Path to quality profiles JSON")
    parser.add_argument("--negative", help="Negative terms appended as --no ... when absent")
    parser.add_argument("--default-version", default="8", help="Default Midjourney version")
    parser.add_argument("--no-raw", action="store_true", help="Do not auto-append --raw")
    parser.add_argument("--json", action="store_true", help="Print structured JSON instead of plain prompt")
    return parser


def build_prompt_from_template(args) -> str:
    parts: list[str] = []
    for field_name in TEMPLATES[args.template]:
        value = getattr(args, field_name, None)
        if isinstance(value, str) and value.strip():
            parts.append(" ".join(value.strip().split()))
    return ", ".join(parts)


def main() -> int:
    args = build_parser().parse_args()
    prompt = build_prompt_from_template(args)
    preset_suffix = resolve_named_suffix(args.presets_file, args.preset, label="preset")
    if preset_suffix:
        prompt = apply_preset(prompt, preset_suffix)
    quality_suffix = resolve_named_suffix(args.quality_profiles_file, args.quality_profile, label="quality profile")
    if quality_suffix:
        prompt = apply_preset(prompt, quality_suffix)
    prompt = append_negative_terms(prompt, args.negative)
    final_prompt = normalize_prompt(prompt, default_version=args.default_version, add_raw=not args.no_raw)

    if args.json:
        print_json(
            {
                "template": args.template,
                "preset": args.preset,
                "quality_profile": args.quality_profile,
                "negative": args.negative,
                "prompt": final_prompt,
                "run_imagine_command": " ".join(
                    [
                        "python3",
                        "scripts/run_imagine.py",
                        shlex.quote(final_prompt),
                        "--transport",
                        "browser",
                        "--sync-user-state",
                    ]
                ),
            }
        )
        return 0

    print(final_prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
