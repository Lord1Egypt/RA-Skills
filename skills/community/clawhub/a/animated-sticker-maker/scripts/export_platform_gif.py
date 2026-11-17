#!/usr/bin/env python3
"""Export a validated sticker package as a constrained GIF and preview PNG."""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import re
import tempfile
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
from PIL import Image

from artifact_integrity import (
    fingerprint_files,
    package_fingerprint,
    render_track_fingerprint,
)


COLOR_CANDIDATES = (255, 224, 192, 160, 128, 96, 64, 48, 32)
MAX_PALETTE_SAMPLES = 500_000
TRANSPARENT_INDEX = 255
RESAMPLING_FILTERS = {
    "lanczos": Image.Resampling.LANCZOS,
    "nearest": Image.Resampling.NEAREST,
}
PLATFORM_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def is_positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def parse_size(value: str) -> tuple[int, int]:
    parts = value.lower().split("x", 1)
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("size must look like 400x400")
    try:
        width, height = (int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("size must look like 400x400") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("size must be positive")
    return width, height


def parse_fps_candidates(value: str) -> tuple[int, ...]:
    try:
        candidates = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "fps candidates must be comma-separated positive integers"
        ) from exc
    if not candidates or any(value <= 0 or value > 100 for value in candidates):
        raise argparse.ArgumentTypeError(
            "fps candidates must be comma-separated integers from 1 to 100"
        )
    if len(set(candidates)) != len(candidates):
        raise argparse.ArgumentTypeError("fps candidates must not contain duplicates")
    if any(left <= right for left, right in zip(candidates, candidates[1:])):
        raise argparse.ArgumentTypeError(
            "fps candidates must be ordered from highest to lowest"
        )
    return candidates


def parse_spec_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError(
            "spec URL must be an absolute http(s) URL to the verified platform specification"
        )
    return value


def parse_platform(value: str) -> str:
    if not PLATFORM_PATTERN.fullmatch(value) or value in {".", ".."}:
        raise argparse.ArgumentTypeError(
            "platform must be one safe path segment using letters, digits, dot, dash, or underscore"
        )
    return value


def parse_verified_on(value: str) -> str:
    try:
        verified = date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "verified-on must be an ISO date in YYYY-MM-DD form"
        ) from exc
    if verified > date.today():
        raise argparse.ArgumentTypeError("verified-on cannot be in the future")
    return verified.isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validation_status(report: dict[str, object]) -> dict[str, object]:
    aggregate = report.get("status")
    technical_validation = report.get("technical_validation")
    visual_validation = report.get("visual_validation")
    technical = (
        technical_validation.get("status")
        if isinstance(technical_validation, dict)
        else None
    )
    visual = (
        visual_validation.get("status")
        if isinstance(visual_validation, dict)
        else None
    )
    return {
        "aggregate": aggregate if isinstance(aggregate, str) else None,
        "technical": technical if isinstance(technical, str) else None,
        "visual": visual if isinstance(visual, str) else None,
        "deliverable_ready": report.get("deliverable_ready") is True,
    }


def validation_is_complete(validation: dict[str, object]) -> bool:
    return bool(
        validation.get("aggregate") == "pass"
        and validation.get("technical") == "pass"
        and validation.get("visual") == "pass"
        and validation.get("deliverable_ready") is True
    )


def export_validation_status(
    source_validation: dict[str, object],
    track_validation: dict[str, object] | None,
    track_required: bool = False,
) -> tuple[str, bool]:
    track_complete = (
        track_validation is not None and validation_is_complete(track_validation)
        if track_required
        else True
    )
    source_validation_complete = (
        validation_is_complete(source_validation) and track_complete
    )
    return (
        ("pending_visual_validation", True)
        if source_validation_complete
        else ("diagnostic_unvalidated", False)
    )


def direct_export_path(
    export_dir: Path,
    requested: Path | None,
    default_name: str,
    label: str,
) -> Path:
    if requested is None:
        path = export_dir / default_name
    elif not requested.is_absolute() and len(requested.parts) == 1:
        path = export_dir / requested
    else:
        path = requested
    if path.resolve().parent != export_dir.resolve():
        raise ValueError(f"{label} must be a direct child of {export_dir}")
    if path.exists() and not path.is_file():
        raise ValueError(f"{label} must not replace a directory: {path}")
    return path


def commit_staged_files(
    entries: list[tuple[Path, Path]], staging: Path
) -> None:
    """Replace a related export set together, restoring previous files on error."""
    backups: dict[Path, Path] = {}
    committed: list[Path] = []
    try:
        for index, (staged, final) in enumerate(entries):
            if final.exists():
                backup = staging / f".previous-{index}-{final.name}"
                final.replace(backup)
                backups[final] = backup
            staged.replace(final)
            committed.append(final)
    except Exception:
        for final in reversed(committed):
            final.unlink(missing_ok=True)
        for final, backup in backups.items():
            if backup.exists():
                backup.replace(final)
        raise


def safe_track_dir(source_dir: Path, value: object) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("render.frame_dir must be a non-empty relative path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("render.frame_dir must stay beneath the package source directory")
    track_dir = source_dir / relative
    if not track_dir.is_dir():
        raise FileNotFoundError(f"render frame directory not found: {track_dir}")
    if not track_dir.resolve().is_relative_to(source_dir.resolve()):
        raise ValueError("render.frame_dir must not escape through a symbolic link")
    return track_dir


def load_validated_package(
    package: Path,
    allow_unvalidated: bool,
    frame_track: str = "keyframes",
    track_report: Path | None = None,
) -> tuple[
    list[Image.Image],
    list[int],
    dict[str, object],
    dict[str, object],
    dict[str, object] | None,
]:
    motion_path = package / "source" / "motion.json"
    report_path = package / "validation" / "report.json"
    frames_dir = package / "source" / "frames"
    if not motion_path.is_file() or not report_path.is_file() or not frames_dir.is_dir():
        raise FileNotFoundError(
            "package must contain source/motion.json, source/frames, and "
            "validation/report.json"
        )

    motion = json.loads(motion_path.read_text(encoding="utf-8"))
    entries = motion.get("frames")
    if not isinstance(entries, list) or not entries:
        raise ValueError("source/motion.json must contain a non-empty frames array")
    durations = [entry.get("duration_ms") for entry in entries if isinstance(entry, dict)]
    if len(durations) != len(entries) or not all(
        is_positive_int(value) for value in durations
    ):
        raise ValueError("every motion frame must have a positive integer duration_ms")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    expected_fingerprint = report.get("artifact_fingerprint")
    if report.get("artifact_scope") != "package_source" or not isinstance(
        expected_fingerprint, str
    ):
        raise ValueError(
            "package validation report has no bound source artifact fingerprint"
        )
    actual_fingerprint = package_fingerprint(package)
    if actual_fingerprint != expected_fingerprint:
        raise ValueError(
            "package source changed after validation; repack and repeat validation"
        )
    source_validation = validation_status(report)
    validation_complete = validation_is_complete(source_validation)
    if not validation_complete and not allow_unvalidated:
        raise ValueError(
            "package validation is incomplete "
            f"(aggregate={source_validation['aggregate']!r}, "
            f"technical={source_validation['technical']!r}, "
            f"visual={source_validation['visual']!r}); pass both validations first "
            "or use --allow-unvalidated explicitly"
        )

    derived_validation = None
    if frame_track == "keyframes":
        frame_paths = sorted(frames_dir.glob("*.png"))
        if len(frame_paths) != len(entries):
            raise ValueError(
                f"source frame count {len(frame_paths)} does not match motion frame count {len(entries)}"
            )
    elif frame_track == "render":
        render = motion.get("render")
        if not isinstance(render, dict):
            raise ValueError("source/motion.json has no render track metadata")
        frame_paths = sorted(
            safe_track_dir(package / "source", render.get("frame_dir")).glob("*.png")
        )
        render_durations = render.get("frame_durations_ms")
        if not isinstance(render_durations, list) or not all(
            is_positive_int(value) for value in render_durations
        ):
            raise ValueError("render.frame_durations_ms must contain positive integers")
        durations = render_durations
        declared_count = render.get("frame_count")
        if (
            not is_positive_int(declared_count)
            or declared_count != len(frame_paths)
            or len(durations) != len(frame_paths)
        ):
            raise ValueError(
                "render frame count, frame_durations_ms, and files must have equal length"
            )
        declared_total = render.get("total_duration_ms")
        if not is_positive_int(declared_total):
            raise ValueError("render.total_duration_ms must be a positive integer")
        if declared_total != sum(durations):
            raise ValueError("render.total_duration_ms does not match frame durations")
        if track_report is None:
            if not allow_unvalidated:
                raise ValueError(
                    "render track export requires --track-report with aggregate, "
                    "technical/checks, and visual pass states"
                )
        else:
            derived_report = json.loads(track_report.read_text(encoding="utf-8"))
            expected_track_fingerprint = derived_report.get("artifact_fingerprint")
            if derived_report.get("artifact_scope") != "render_track" or not isinstance(
                expected_track_fingerprint, str
            ):
                raise ValueError(
                    "render-track validation has no bound artifact fingerprint"
                )
            if render_track_fingerprint(package) != expected_track_fingerprint:
                raise ValueError(
                    "render track changed after validation; regenerate and repeat "
                    "its validation"
                )
            derived_validation = validation_status(derived_report)
            derived_complete = validation_is_complete(derived_validation)
            if not derived_complete and not allow_unvalidated:
                raise ValueError(
                    "render track validation is incomplete "
                    f"({derived_validation}); pass its technical and visual "
                    "validations first"
                )
    else:
        raise ValueError(f"unsupported frame track: {frame_track}")

    frames: list[Image.Image] = []
    for path in frame_paths:
        with Image.open(path) as source:
            frames.append(source.convert("RGBA"))
    return frames, durations, motion, source_validation, derived_validation


def fit_frame(
    frame: Image.Image,
    size: tuple[int, int],
    resampling: str = "lanczos",
) -> Image.Image:
    if resampling not in RESAMPLING_FILTERS:
        raise ValueError("resampling must be 'lanczos' or 'nearest'")
    scale = min(size[0] / frame.width, size[1] / frame.height)
    fitted_size = (
        max(1, round(frame.width * scale)),
        max(1, round(frame.height * scale)),
    )
    fitted = frame.resize(fitted_size, RESAMPLING_FILTERS[resampling])
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
    return canvas


def collect_palette_samples(
    frames: list[Image.Image],
    alpha_threshold: int,
    max_samples: int = MAX_PALETTE_SAMPLES,
) -> np.ndarray:
    if max_samples <= 0:
        raise ValueError("max_samples must be positive")
    samples: list[np.ndarray] = []
    frame_count = len(frames)
    base_budget, extra_budget = divmod(max_samples, max(1, frame_count))
    for index, frame in enumerate(frames):
        budget = base_budget + (1 if index < extra_budget else 0)
        if budget == 0:
            continue
        rgba = np.asarray(frame)
        visible = rgba[..., :3][rgba[..., 3] >= alpha_threshold]
        if visible.size:
            if len(visible) > budget:
                step = max(1, (len(visible) + budget - 1) // budget)
                visible = visible[::step][:budget]
            samples.append(visible)
    if not samples:
        raise ValueError("frames contain no visible pixels at the selected alpha threshold")
    rgb = np.concatenate(samples, axis=0)
    if len(rgb) > max_samples:
        raise AssertionError("palette sample budget exceeded")
    return rgb


def make_global_palette(
    frames: list[Image.Image], colors: int, alpha_threshold: int
) -> Image.Image:
    rgb = collect_palette_samples(frames, alpha_threshold)
    sample_image = Image.fromarray(rgb.reshape(1, len(rgb), 3), mode="RGB")
    palette = sample_image.quantize(
        colors=colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    palette_data = palette.getpalette()
    palette_data[TRANSPARENT_INDEX * 3 : TRANSPARENT_INDEX * 3 + 3] = [0, 0, 0]
    palette.putpalette(palette_data)
    return palette


def quantize_frames(
    frames: list[Image.Image], colors: int, alpha_threshold: int
) -> list[Image.Image]:
    palette = make_global_palette(frames, colors, alpha_threshold)
    palette_data = palette.getpalette()
    result: list[Image.Image] = []
    for frame in frames:
        indexed = frame.convert("RGB").quantize(
            palette=palette,
            dither=Image.Dither.FLOYDSTEINBERG,
        )
        indices = np.asarray(indexed).copy()
        indices[np.asarray(frame.getchannel("A")) < alpha_threshold] = TRANSPARENT_INDEX
        indexed = Image.fromarray(indices, mode="P")
        indexed.putpalette(palette_data)
        indexed.info["transparency"] = TRANSPARENT_INDEX
        result.append(indexed)
    return result


def write_gif(
    frames: list[Image.Image],
    durations: list[int],
    path: Path,
    colors: int,
    alpha_threshold: int,
    loop: bool,
) -> None:
    indexed = quantize_frames(frames, colors, alpha_threshold)
    save_options = {
        "format": "GIF",
        "save_all": True,
        "append_images": indexed[1:],
        "duration": durations,
        "disposal": 2,
        "transparency": TRANSPARENT_INDEX,
        "optimize": True,
    }
    if loop:
        save_options["loop"] = 0
    indexed[0].save(path, **save_options)


def gif_safe_durations(total_ms: int, frame_count: int) -> list[int]:
    if frame_count <= 0:
        raise ValueError("frame count must be positive")
    rounded_total = max(10, round(total_ms / 10) * 10)
    boundaries = [
        round((index * rounded_total / frame_count) / 10) * 10
        for index in range(frame_count + 1)
    ]
    durations = [end - start for start, end in zip(boundaries, boundaries[1:])]
    if any(duration <= 0 for duration in durations):
        raise ValueError("requested fps is too high for GIF's 10 ms timing precision")
    return durations


def resample_timeline(
    frames: list[Image.Image], durations: list[int], fps: int
) -> tuple[list[Image.Image], list[int]]:
    if len(frames) != len(durations) or not frames:
        raise ValueError("frames and durations must have equal non-zero length")
    if fps <= 0 or fps > 100:
        raise ValueError("fps must be between 1 and 100")
    total_ms = sum(durations)
    target_count = max(2, round(total_ms * fps / 1000))
    source_ends: list[int] = []
    elapsed = 0
    for duration in durations:
        elapsed += duration
        source_ends.append(elapsed)
    samples: list[Image.Image] = []
    for index in range(target_count):
        timestamp = index * total_ms / target_count
        source_index = min(
            len(frames) - 1,
            bisect.bisect_right(source_ends, timestamp),
        )
        samples.append(frames[source_index])
    return samples, gif_safe_durations(total_ms, target_count)


def try_export_gif(
    frames: list[Image.Image],
    durations: list[int],
    output: Path,
    max_bytes: int | None,
    alpha_threshold: int,
    loop: bool,
    color_candidates: tuple[int, ...],
    nominal_fps: int | None,
) -> tuple[tuple[int, int] | None, list[dict[str, int | None]]]:
    candidate = output.with_suffix(output.suffix + ".candidate")
    attempts: list[dict[str, int | None]] = []
    try:
        for colors in color_candidates:
            write_gif(frames, durations, candidate, colors, alpha_threshold, loop)
            byte_size = candidate.stat().st_size
            attempts.append(
                {"fps": nominal_fps, "colors": colors, "bytes": byte_size}
            )
            if max_bytes is None or byte_size <= max_bytes:
                candidate.replace(output)
                return (colors, byte_size), attempts
    finally:
        candidate.unlink(missing_ok=True)
    return None, attempts


def export_gif(
    frames: list[Image.Image],
    durations: list[int],
    output: Path,
    max_bytes: int | None,
    alpha_threshold: int,
    loop: bool,
    min_colors: int = 32,
    fps_candidates: tuple[int, ...] | None = None,
) -> tuple[list[Image.Image], list[int], int, int, int | None, list[dict[str, int | None]]]:
    color_candidates = tuple(
        colors for colors in COLOR_CANDIDATES if colors >= min_colors
    )
    if not color_candidates:
        raise ValueError(
            f"minimum color count {min_colors} excludes every supported palette candidate"
        )
    variants: list[tuple[int | None, list[Image.Image], list[int]]]
    if fps_candidates:
        variants = [
            (fps, *resample_timeline(frames, durations, fps))
            for fps in fps_candidates
        ]
    else:
        variants = [(None, frames, durations)]

    all_attempts: list[dict[str, int | None]] = []
    for nominal_fps, variant_frames, variant_durations in variants:
        selected, attempts = try_export_gif(
            variant_frames,
            variant_durations,
            output,
            max_bytes,
            alpha_threshold,
            loop,
            color_candidates,
            nominal_fps,
        )
        all_attempts.extend(attempts)
        if selected is not None:
            colors, byte_size = selected
            return (
                variant_frames,
                variant_durations,
                colors,
                byte_size,
                nominal_fps,
                all_attempts,
            )

    smallest = min(all_attempts, key=lambda item: int(item["bytes"] or 0))
    raise ValueError(
        f"GIF cannot meet {max_bytes} bytes with the requested quality floor; "
        f"smallest candidate is {smallest['bytes']} bytes at "
        f"fps={smallest['fps']} and {smallest['colors']} colors"
    )


def write_preview(
    frame: Image.Image, output: Path, max_bytes: int | None
) -> tuple[str, int, int | None]:
    frame.save(output, format="PNG", optimize=True, compress_level=9)
    byte_size = output.stat().st_size
    if max_bytes is None or byte_size <= max_bytes:
        return "rgba", byte_size, None

    smallest: tuple[int, int] | None = None
    candidate = output.with_suffix(output.suffix + ".candidate")
    try:
        for colors in (256, 192, 128, 96, 64, 48, 32, 24, 16):
            indexed = frame.quantize(
                colors=colors,
                method=Image.Quantize.FASTOCTREE,
                dither=Image.Dither.FLOYDSTEINBERG,
            )
            indexed.save(candidate, format="PNG", optimize=True, compress_level=9)
            candidate_size = candidate.stat().st_size
            if smallest is None or candidate_size < smallest[1]:
                smallest = (colors, candidate_size)
            if candidate_size <= max_bytes:
                candidate.replace(output)
                return "indexed", candidate_size, colors
    finally:
        candidate.unlink(missing_ok=True)
    output.unlink(missing_ok=True)
    assert smallest is not None
    raise ValueError(
        f"preview PNG cannot meet {max_bytes} bytes at the requested size; "
        f"smallest candidate is {smallest[1]} bytes at {smallest[0]} colors"
    )


def automatic_preview_frame(
    package: Path,
    motion: dict[str, object],
    size: tuple[int, int],
    resampling: str = "lanczos",
) -> tuple[Image.Image, int]:
    entries = motion.get("frames")
    assert isinstance(entries, list) and entries
    preview_index = max(
        range(len(entries)),
        key=lambda index: int(entries[index]["duration_ms"]),
    )
    semantic_hold = motion.get("semantic_hold_frame")
    if isinstance(semantic_hold, str) and semantic_hold:
        relative = Path(semantic_hold)
        if not relative.is_absolute() and ".." not in relative.parts:
            candidate = package / "source" / relative
            if (
                candidate.is_file()
                and candidate.resolve().is_relative_to((package / "source").resolve())
            ):
                semantic_name = relative.as_posix()
                for index, entry in enumerate(entries):
                    if entry.get("file") == semantic_name:
                        preview_index = index
                        with Image.open(candidate) as source:
                            return (
                                fit_frame(source.convert("RGBA"), size, resampling),
                                preview_index,
                            )
                raise ValueError(
                    "semantic_hold_frame must match one authored keyframe entry"
                )
    keyframes = sorted((package / "source/frames").glob("*.png"))
    if len(keyframes) != len(entries):
        raise ValueError("cannot resolve automatic preview from package keyframes")
    with Image.open(keyframes[preview_index]) as source:
        return fit_frame(source.convert("RGBA"), size, resampling), preview_index


def validate_gif(
    path: Path,
    size: tuple[int, int],
    frame_count: int,
    durations: list[int],
    loop: bool,
    allow_frame_collapse: bool = False,
) -> dict[str, object]:
    expected_loop = 0 if loop else None
    actual_durations: list[int | None] = []
    transparent_borders: list[bool] = []
    with Image.open(path) as image:
        encoded_frame_count = getattr(image, "n_frames", 1)
        encoded_size = image.size
        for index in range(encoded_frame_count):
            image.seek(index)
            actual_durations.append(image.info.get("duration"))
            alpha = np.asarray(image.convert("RGBA").getchannel("A"))
            transparent_borders.append(
                bool(
                    np.all(alpha[0] == 0)
                    and np.all(alpha[-1] == 0)
                    and np.all(alpha[:, 0] == 0)
                    and np.all(alpha[:, -1] == 0)
                )
            )
        encoded_loop = image.info.get("loop")
    actual_duration_values = [
        value for value in actual_durations if isinstance(value, int)
    ]
    frame_count_matches = encoded_frame_count == frame_count
    if allow_frame_collapse:
        frame_count_matches = 1 < encoded_frame_count <= frame_count
    durations_preserved = len(actual_durations) == len(durations) and all(
        isinstance(actual, int) and abs(actual - expected) <= 10
        for actual, expected in zip(actual_durations, durations)
    )
    if allow_frame_collapse:
        durations_preserved = (
            len(actual_duration_values) == len(actual_durations)
            and abs(sum(actual_duration_values) - sum(durations)) <= 10
        )
    checks = {
        "size_matches": encoded_size == size,
        "frame_count_matches": frame_count_matches,
        "durations_preserved": durations_preserved,
        "loop_matches": encoded_loop == expected_loop,
        "all_borders_transparent": all(transparent_borders),
    }
    if not all(checks.values()):
        raise ValueError(f"exported GIF validation failed: {checks}")
    return {
        "checks": checks,
        "encoded_frame_count": encoded_frame_count,
        "durations_ms": actual_durations,
        "total_duration_ms": sum(actual_duration_values),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--platform", type=parse_platform, required=True)
    parser.add_argument("--size", type=parse_size, required=True)
    parser.add_argument("--max-bytes", type=int)
    parser.add_argument(
        "--frame-track",
        choices=("keyframes", "render"),
        default="keyframes",
        help="keyframes preserves authored frames; render uses motion.render metadata",
    )
    parser.add_argument(
        "--track-report",
        type=Path,
        help=(
            "required pass report for a render track unless --allow-unvalidated "
            "is diagnostic"
        ),
    )
    parser.add_argument(
        "--fps-candidates",
        type=parse_fps_candidates,
        help="render-track fallback order such as 30,24,20,15",
    )
    parser.add_argument(
        "--min-colors",
        type=int,
        default=32,
        help="minimum shared-palette size allowed during byte-limit search",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preview-output", type=Path)
    parser.add_argument("--preview-max-bytes", type=int)
    parser.add_argument("--preview-frame", default="auto", help="'auto' or a 1-based frame number")
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--alpha-threshold", type=int, default=96, choices=range(1, 255))
    parser.add_argument("--spec-url", type=parse_spec_url, required=True)
    parser.add_argument("--verified-on", type=parse_verified_on, required=True)
    parser.add_argument("--allow-unvalidated", action="store_true")
    args = parser.parse_args()
    if args.max_bytes is not None and args.max_bytes <= 0:
        parser.error("--max-bytes must be positive")
    if args.preview_max_bytes is not None and args.preview_max_bytes <= 0:
        parser.error("--preview-max-bytes must be positive")
    if not 1 <= args.min_colors <= 255:
        parser.error("--min-colors must be between 1 and 255")
    if args.fps_candidates and args.frame_track != "render":
        parser.error("--fps-candidates requires --frame-track render")
    if args.track_report and args.frame_track != "render":
        parser.error("--track-report requires --frame-track render")
    package = args.package.resolve()
    if args.track_report and not args.track_report.resolve().is_relative_to(package):
        parser.error("--track-report must stay beneath the package directory")

    export_dir = package / "exports" / args.platform
    export_dir.mkdir(parents=True, exist_ok=True)
    try:
        output = direct_export_path(export_dir, args.output, "sticker.gif", "--output")
        preview_output = (
            direct_export_path(
                export_dir,
                args.preview_output,
                "preview.png",
                "--preview-output",
            )
            if args.preview_output is not None
            else None
        )
        report_path = direct_export_path(
            export_dir,
            args.report_output,
            f"{output.stem}.export-report.json",
            "--report-output",
        )
    except ValueError as exc:
        parser.error(str(exc))
    if output.suffix.lower() != ".gif":
        parser.error("--output must end in .gif")
    if preview_output is not None and preview_output.suffix.lower() != ".png":
        parser.error("--preview-output must end in .png")
    if report_path.suffix.lower() != ".json":
        parser.error("--report-output must end in .json")
    final_paths = [output, report_path]
    if preview_output is not None:
        final_paths.append(preview_output)
    if len({path.resolve() for path in final_paths}) != len(final_paths):
        parser.error("GIF, preview, and report outputs must use distinct paths")

    # Invalidate any older validation report before starting a new export attempt.
    report_path.unlink(missing_ok=True)

    frames, durations, motion, source_validation, track_validation = (
        load_validated_package(
            package,
            args.allow_unvalidated,
            args.frame_track,
            args.track_report,
        )
    )
    source_report_path = package / "validation" / "report.json"
    source_report = json.loads(source_report_path.read_text(encoding="utf-8"))
    source_artifact_fingerprint = source_report.get("artifact_fingerprint")
    if not isinstance(source_artifact_fingerprint, str):
        raise ValueError("package validation report has no artifact fingerprint")
    loop = motion.get("loop", True)
    if not isinstance(loop, bool):
        raise ValueError("motion.loop must be a boolean")
    resampling = motion.get("resampling", "lanczos")
    if resampling not in RESAMPLING_FILTERS:
        raise ValueError("motion.resampling must be 'lanczos' or 'nearest'")
    resized = [fit_frame(frame, args.size, str(resampling)) for frame in frames]
    with tempfile.TemporaryDirectory(prefix=".export-staging-", dir=export_dir) as temporary:
        staging = Path(temporary)
        staged_output = staging / output.name
        (
            exported_frames,
            exported_durations,
            colors,
            gif_bytes,
            selected_fps,
            export_attempts,
        ) = export_gif(
            resized,
            durations,
            staged_output,
            args.max_bytes,
            args.alpha_threshold,
            loop,
            args.min_colors,
            args.fps_candidates,
        )
        validation = validate_gif(
            staged_output,
            args.size,
            len(exported_frames),
            exported_durations,
            loop,
            allow_frame_collapse=args.fps_candidates is not None,
        )

        preview_record = None
        staged_preview = None
        if preview_output is not None:
            if args.preview_frame == "auto":
                preview_frame, preview_index = automatic_preview_frame(
                    package,
                    motion,
                    args.size,
                    str(resampling),
                )
            else:
                try:
                    preview_index = int(args.preview_frame) - 1
                except ValueError as exc:
                    raise ValueError(
                        "--preview-frame must be 'auto' or a 1-based frame number"
                    ) from exc
                if not 0 <= preview_index < len(exported_frames):
                    raise ValueError("--preview-frame is outside the exported frame range")
                preview_frame = exported_frames[preview_index]
            staged_preview = staging / preview_output.name
            mode, preview_bytes, preview_colors = write_preview(
                preview_frame,
                staged_preview,
                args.preview_max_bytes,
            )
            preview_record = {
                "path": preview_output.name,
                "frame": preview_index + 1,
                "mode": mode,
                "colors": preview_colors,
                "bytes": preview_bytes,
                "sha256": sha256(staged_preview),
            }

        report_status, source_validation_complete = export_validation_status(
            source_validation,
            track_validation,
            track_required=args.frame_track == "render",
        )
        validation_artifact_entries = [(output.name, staged_output)]
        if staged_preview is not None and preview_output is not None:
            validation_artifact_entries.append((preview_output.name, staged_preview))
        artifact_fingerprint = fingerprint_files(
            [
                (f"artifact:{name}", path)
                for name, path in validation_artifact_entries
            ]
        )
        validation_artifacts = [
            {"path": name, "sha256": sha256(path)}
            for name, path in validation_artifact_entries
        ]
        report = {
            "status": report_status,
            "source_validation_complete": source_validation_complete,
            "deliverable_ready": False,
            "artifact_scope": "export_files",
            "artifact_fingerprint": artifact_fingerprint,
            "validation_artifacts": validation_artifacts,
            "technical_validation": {
                "status": "pass",
                "checks": validation["checks"],
            },
            "visual_validation": {
                "status": "pending",
                "required": ["identity", "meaning", "loop", "alpha", "small_size"],
                "notes": {},
            },
            "platform": args.platform,
            "verified_on": args.verified_on,
            "spec_url": args.spec_url,
            "source_package": "../..",
            "source_validation_status": source_validation["aggregate"],
            "source_validation": source_validation,
            "source_validation_report": {
                "path": "../../validation/report.json",
                "sha256": sha256(source_report_path),
                "artifact_fingerprint": source_artifact_fingerprint,
            },
            "frame_track": args.frame_track,
            "track_validation": track_validation,
            "track_report": (
                {
                    "path": str(args.track_report.resolve().relative_to(package)),
                    "sha256": sha256(args.track_report),
                }
                if args.track_report is not None
                else None
            ),
            "canvas": list(args.size),
            "resampling": resampling,
            "source_frame_count": len(resized),
            "source_total_duration_ms": sum(durations),
            "frame_count": len(exported_frames),
            "total_duration_ms": sum(exported_durations),
            "gif": {
                "path": output.name,
                "bytes": gif_bytes,
                "max_bytes": args.max_bytes,
                "colors": colors,
                "selected_fps": selected_fps,
                "min_colors": args.min_colors,
                "attempts": export_attempts,
                "alpha_threshold": args.alpha_threshold,
                "sha256": sha256(staged_output),
                "validation": validation,
            },
            "preview": preview_record,
        }
        staged_report = staging / report_path.name
        staged_report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        staged_entries = [(staged_output, output)]
        if staged_preview is not None and preview_output is not None:
            staged_entries.append((staged_preview, preview_output))
        staged_entries.append((staged_report, report_path))
        commit_staged_files(staged_entries, staging)
    print(f"Wrote {output} ({gif_bytes} bytes, {colors} colors)")
    if preview_record:
        print(f"Wrote {preview_output} ({preview_record['bytes']} bytes)")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
