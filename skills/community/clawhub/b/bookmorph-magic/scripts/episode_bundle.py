#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_OUTPUT_ROOT = (Path.cwd() / "output").resolve()
DEFAULT_EPISODE_DIR_PREFIX = "episode-"


def print_json(payload: dict[str, object]) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def normalize_episode_number(raw: str | int) -> int:
    text = str(raw).strip()
    match = re.search(r"(\d+)", text)
    if not match:
        raise SystemExit(f"could not extract episode number from: {raw}")
    number = int(match.group(1))
    if number <= 0:
        raise SystemExit("episode number must be positive")
    return number


def episode_slug(number: int) -> str:
    return f"ep{number}"


def episode_dir(number: int, output_root: Path, prefix: str) -> Path:
    return output_root / f"{prefix}{episode_slug(number)}"


def parse_episode_text(text: str) -> int:
    patterns = [
        re.compile(r"\bep\s*0*(\d+)\b", re.IGNORECASE),
        re.compile(r"episode\s*0*(\d+)\b", re.IGNORECASE),
        re.compile(r"第\s*0*(\d+)\s*[期集]", re.IGNORECASE),
    ]
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            return int(match.group(1))

    numbers = re.findall(r"\d+", text)
    if len(numbers) == 1:
        return int(numbers[0])
    raise SystemExit(f"could not uniquely determine episode number from: {text}")


def ensure_absolute_path(raw: str | None, *, label: str, require_exists: bool = True) -> Path | None:
    if raw is None:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        raise SystemExit(f"{label} must be an absolute path")
    resolved = path.resolve(strict=False)
    if require_exists and not resolved.exists():
        raise SystemExit(f"{label} not found: {resolved}")
    return resolved


def parse_failures(entries: list[str]) -> list[dict[str, str]]:
    parsed: list[dict[str, str]] = []
    for entry in entries:
        if "=" in entry:
            stage, message = entry.split("=", 1)
            stage = stage.strip() or "unknown"
            message = message.strip()
        else:
            stage = "unknown"
            message = entry.strip()
        if message:
            parsed.append({"stage": stage, "message": message})
    return parsed


def copy_if_present(source: Path | None, dest: Path | None) -> None:
    if source is None or dest is None:
        return
    shutil.copy2(source, dest)


def output_name(slug: str, kind: str, source: Path | None) -> str | None:
    if source is None:
        return None
    suffix = source.suffix.lower()
    if not suffix:
        raise SystemExit(f"missing file extension for {source}")
    return f"{slug}-{kind}{suffix}"


def command_parse_episode(args: argparse.Namespace) -> int:
    number = parse_episode_text(args.text)
    output_root = ensure_absolute_path(args.output_root, label="output-root", require_exists=False)
    assert output_root is not None
    return print_json(
        {
            "status": "ok",
            "episode_number": number,
            "episode_slug": episode_slug(number),
            "dest_dir": str(episode_dir(number, output_root, args.episode_dir_prefix)),
        }
    )


def command_prepare_dest(args: argparse.Namespace) -> int:
    number = normalize_episode_number(args.episode)
    output_root = ensure_absolute_path(args.output_root, label="output-root", require_exists=False)
    assert output_root is not None
    dest_dir = episode_dir(number, output_root, args.episode_dir_prefix)
    existed = dest_dir.exists()

    if existed and args.clear_existing:
        shutil.rmtree(dest_dir)

    dest_dir.mkdir(parents=True, exist_ok=True)
    return print_json(
        {
            "status": "prepared",
            "episode_number": number,
            "episode_slug": episode_slug(number),
            "dest_dir": str(dest_dir),
            "existed": existed,
            "cleared_existing": bool(existed and args.clear_existing),
        }
    )


def command_bundle(args: argparse.Namespace) -> int:
    number = normalize_episode_number(args.episode)
    slug = episode_slug(number)
    output_root = ensure_absolute_path(args.output_root, label="output-root", require_exists=False)
    assert output_root is not None
    dest_dir = episode_dir(number, output_root, args.episode_dir_prefix)
    dest_dir.mkdir(parents=True, exist_ok=True)

    book_path = ensure_absolute_path(args.book_path, label="book-path") if args.book_path else None
    source_paths = {
        "video": ensure_absolute_path(args.video, label="video") if args.video else None,
        "audio": ensure_absolute_path(args.audio, label="audio") if args.audio else None,
        "image_3x4": ensure_absolute_path(args.image_3x4, label="image-3x4") if args.image_3x4 else None,
        "image_4x3": ensure_absolute_path(args.image_4x3, label="image-4x3") if args.image_4x3 else None,
        "image_1x1": ensure_absolute_path(args.image_1x1, label="image-1x1") if args.image_1x1 else None,
    }
    prompt_archive = (
        ensure_absolute_path(args.prompt_archive, label="prompt-archive") if args.prompt_archive else None
    )
    selector_checkpoint = (
        ensure_absolute_path(args.selector_checkpoint, label="selector-checkpoint")
        if args.selector_checkpoint
        else None
    )
    longform_checkpoint = (
        ensure_absolute_path(args.longform_checkpoint, label="longform-checkpoint")
        if args.longform_checkpoint
        else None
    )
    cover_checkpoint = (
        ensure_absolute_path(args.cover_checkpoint, label="cover-checkpoint") if args.cover_checkpoint else None
    )

    if args.status == "success":
        missing = [key for key, path in source_paths.items() if path is None]
        if missing:
            raise SystemExit(f"missing required media for success bundle: {', '.join(sorted(missing))}")
        if not args.book_title or not args.author or book_path is None:
            raise SystemExit("missing required selected book metadata for success bundle")

    output_names = {
        "video": output_name(slug, "video", source_paths["video"]),
        "audio": output_name(slug, "audio", source_paths["audio"]),
        "image_3x4": output_name(slug, "cover-3x4", source_paths["image_3x4"]),
        "image_4x3": output_name(slug, "cover-4x3", source_paths["image_4x3"]),
        "image_1x1": output_name(slug, "cover-1x1", source_paths["image_1x1"]),
    }
    dest_paths = {key: (dest_dir / name if name else None) for key, name in output_names.items()}

    for key, source in source_paths.items():
        copy_if_present(source, dest_paths[key])

    failures = parse_failures(args.failure)
    manifest_path = dest_dir / "manifest.json"
    manifest = {
        "episode": slug,
        "episode_number": number,
        "status": args.status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "selection_round": args.selection_round,
        "selected_book": {
            "title": args.book_title,
            "author": args.author,
            "path": str(book_path) if book_path else None,
            "selector_adapter": args.selector_adapter,
            "selector_reference": args.selector_reference,
        },
        "attempts": {
            "selector_rounds": args.selection_round,
            "longform_attempts": args.longform_attempts,
            "cover_attempts": args.cover_attempts,
        },
        "outputs": {
            "video_path": str(dest_paths["video"]) if dest_paths["video"] else None,
            "audio_path": str(dest_paths["audio"]) if dest_paths["audio"] else None,
            "image_3x4_path": str(dest_paths["image_3x4"]) if dest_paths["image_3x4"] else None,
            "image_4x3_path": str(dest_paths["image_4x3"]) if dest_paths["image_4x3"] else None,
            "image_1x1_path": str(dest_paths["image_1x1"]) if dest_paths["image_1x1"] else None,
            "manifest_path": str(manifest_path),
        },
        "source_outputs": {
            "video_path": str(source_paths["video"]) if source_paths["video"] else None,
            "audio_path": str(source_paths["audio"]) if source_paths["audio"] else None,
            "image_3x4_path": str(source_paths["image_3x4"]) if source_paths["image_3x4"] else None,
            "image_4x3_path": str(source_paths["image_4x3"]) if source_paths["image_4x3"] else None,
            "image_1x1_path": str(source_paths["image_1x1"]) if source_paths["image_1x1"] else None,
            "prompt_archive_path": str(prompt_archive) if prompt_archive else None,
            "selector_checkpoint_path": str(selector_checkpoint) if selector_checkpoint else None,
            "longform_checkpoint_path": str(longform_checkpoint) if longform_checkpoint else None,
            "cover_checkpoint_path": str(cover_checkpoint) if cover_checkpoint else None,
        },
        "failures": failures,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return print_json(
        {
            "status": args.status,
            "episode": slug,
            "dest_dir": str(dest_dir),
            "manifest_path": str(manifest_path),
            "outputs": manifest["outputs"],
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bundle book-to-content outputs into a stable episode directory."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_episode = subparsers.add_parser("parse-episode", help="Extract the episode number from user text")
    parse_episode.add_argument("--text", required=True)
    parse_episode.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parse_episode.add_argument("--episode-dir-prefix", default=DEFAULT_EPISODE_DIR_PREFIX)
    parse_episode.set_defaults(func=command_parse_episode)

    prepare_dest = subparsers.add_parser("prepare-dest", help="Create or reset the episode output directory")
    prepare_dest.add_argument("--episode", required=True)
    prepare_dest.add_argument("--clear-existing", action="store_true")
    prepare_dest.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    prepare_dest.add_argument("--episode-dir-prefix", default=DEFAULT_EPISODE_DIR_PREFIX)
    prepare_dest.set_defaults(func=command_prepare_dest)

    bundle = subparsers.add_parser("bundle", help="Copy final media into the episode directory and write manifest")
    bundle.add_argument("--episode", required=True)
    bundle.add_argument("--video")
    bundle.add_argument("--audio")
    bundle.add_argument("--image-3x4", dest="image_3x4")
    bundle.add_argument("--image-4x3", dest="image_4x3")
    bundle.add_argument("--image-1x1", dest="image_1x1")
    bundle.add_argument("--book-title")
    bundle.add_argument("--author")
    bundle.add_argument("--book-path")
    bundle.add_argument("--selector-adapter")
    bundle.add_argument("--selector-reference")
    bundle.add_argument("--selection-round", type=int, required=True)
    bundle.add_argument("--longform-attempts", type=int, required=True)
    bundle.add_argument("--cover-attempts", type=int, required=True)
    bundle.add_argument("--prompt-archive")
    bundle.add_argument("--selector-checkpoint")
    bundle.add_argument("--longform-checkpoint")
    bundle.add_argument("--cover-checkpoint")
    bundle.add_argument("--failure", action="append", default=[])
    bundle.add_argument("--status", choices=("success", "partial", "failed"), default="success")
    bundle.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    bundle.add_argument("--episode-dir-prefix", default=DEFAULT_EPISODE_DIR_PREFIX)
    bundle.set_defaults(func=command_bundle)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
