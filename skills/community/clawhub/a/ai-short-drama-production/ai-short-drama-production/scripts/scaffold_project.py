#!/usr/bin/env python3
"""Create a standard AI short-drama project tree and artifact templates."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

DIRS = [
    "00_admin",
    "01_story/scripts",
    "02_visual_bible/typography",
    "03_characters/refs",
    "03_characters/outfits",
    "03_characters/expressions",
    "04_scenes",
    "05_props",
    "06_shots/keyframes",
    "06_shots/raw_generations",
    "06_shots/selected_takes",
    "07_audio/dialogue",
    "07_audio/music",
    "07_audio/sfx",
    "08_subtitles",
    "09_lipsync",
    "10_edit",
    "11_deliverables",
    "12_archive",
]

TEMPLATES = {
    "01_story/scene_breakdown.csv": "scene_breakdown.csv",
    "01_story/continuity_ledger.csv": "continuity_ledger.csv",
    "01_story/retention_plan.csv": "retention_plan.csv",
    "02_visual_bible/technique_plan.csv": "technique_plan.csv",
    "02_visual_bible/cover_copy.csv": "cover_copy.csv",
    "06_shots/shot_manifest.csv": "shot_manifest.csv",
    "03_characters/character_registry.csv": "asset_registry.csv",
    "07_audio/voice_timeline.csv": "voice_timeline.csv",
    "11_deliverables/delivery_manifest.csv": "delivery_manifest.csv",
}


def write_if_missing(path: Path, content: str) -> str:
    if path.exists():
        return f"skip {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"write {path}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", help="Destination project directory")
    parser.add_argument("--project-name", default="AI Short Drama Project")
    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--series", default="main")
    args = parser.parse_args()

    root = Path(args.project_dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    for rel in DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)

    skill_root = Path(__file__).resolve().parent.parent
    template_root = skill_root / "assets" / "templates"
    for rel, template_name in TEMPLATES.items():
        src = template_root / template_name
        dst = root / rel
        if dst.exists():
            print(f"skip {dst}")
            continue
        if src.exists():
            shutil.copyfile(src, dst)
            print(f"copy {src} -> {dst}")
        else:
            write_if_missing(dst, "")

    brief = f"""# {args.project_name}

- Series: {args.series}
- Planned episodes: {args.episodes}
- Canvas: 9:16 / 1080x1920
- Test resolution: 720p
- Frame rate: 24 fps
- Dialogue policy: clean video + separate voice
- Text policy: all final text in post
- Status: pre-production

## Gates

- [ ] Scope and rights
- [ ] Story spine and scene map
- [ ] Scene turns and continuity ledger
- [ ] Visual lock and technique plan
- [ ] Character lock
- [ ] Shot lock
- [ ] Paid-generation approval
- [ ] Audio/subtitle/lip-sync lock
- [ ] Picture lock
- [ ] Delivery and archive
"""
    write_if_missing(root / "00_admin" / "production_brief.md", brief)
    write_if_missing(
        root / "00_admin" / "rights_manifest.csv",
        "asset_id,asset_type,name,source,rights_owner,license,territory,expiry,notes\n",
    )
    write_if_missing(
        root / "00_admin" / "paid_task_ledger.csv",
        "task_id,model,prompt_version,duration_sec,resolution,status,output_path,sha256,operator,created_at\n",
    )
    profile_src = template_root / "project_profile.json"
    profile_dst = root / "project_profile.json"
    if profile_src.exists() and not profile_dst.exists():
        profile = json.loads(profile_src.read_text(encoding="utf-8"))
        project_id = "".join(ch.lower() if ch.isalnum() else "-" for ch in args.project_name).strip("-") or "project"
        profile["project"]["project_id"] = project_id
        profile["project"]["project_name"] = args.project_name
        profile["format"]["episodes"] = args.episodes
        profile.setdefault("audience", {})
        profile.setdefault("release", {})["season_episodes"] = args.episodes
        if profile.get("series"):
            profile["series"][0]["series_id"] = args.series
            profile["series"][0]["title"] = args.project_name
        profile_dst.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"write {profile_dst}")

    manifest = {
        "project_name": args.project_name,
        "series": args.series,
        "episodes": args.episodes,
        "project_profile": "project_profile.json",
        "canvas": "9:16",
        "final_resolution": "1080x1920",
        "test_resolution": "720p",
        "fps": 24,
        "dialogue_policy": "clean video + separate voice",
        "text_policy": "all final text in post",
    }
    write_if_missing(root / "project_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"project ready: {root}")


if __name__ == "__main__":
    main()
