#!/usr/bin/env python3
"""Shared CLI/runtime helpers for poster renderers."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any, Callable

from svg_image_converter import SvgConversionError, convert_svg_file, normalize_output_formats, suffix_for_format

JsonDict = dict[str, Any]
RenderSvgFn = Callable[[JsonDict, Path], str]
PrepareSpecFn = Callable[[JsonDict, Path], JsonDict]

POSTER_TYPE_ALIASES = {
    "daily": "daily",
    "daily_poster": "daily",
    "daily-poster": "daily",
    "moyu": "daily",
    "baidu_hot": "baidu_hot",
    "baidu-hot": "baidu_hot",
    "baidu": "baidu_hot",
    "hot": "baidu_hot",
}


def dig(data: JsonDict, path: str, default: Any = None) -> Any:
    current: Any = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def normalize_poster_type(value: Any, *, default: str | None = None) -> str | None:
    key = str(value or "").strip().lower()
    if not key:
        return default
    return POSTER_TYPE_ALIASES.get(key, key)


def build_parser(description: str, *, include_type: bool = False) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    if include_type:
        parser.add_argument(
            "--type",
            dest="poster_type",
            choices=sorted(set(POSTER_TYPE_ALIASES.values())),
            help="Poster type. When omitted, it is inferred from spec.poster_type or the JSON shape.",
        )
    parser.add_argument("--spec", required=True, help="Path to the JSON spec file.")
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path or basename. When spec.output.formats is set, sibling files are created from this stem.",
    )
    return parser


def load_spec(spec_arg: str) -> tuple[Path, JsonDict]:
    spec_path = Path(spec_arg).resolve()
    if not spec_path.exists():
        raise ValueError(f"Spec file does not exist: {spec_path}")
    if spec_path.suffix.lower() != ".json":
        raise ValueError(f"Spec file must be a .json file: {spec_path}")

    payload = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("Spec JSON must decode to an object.")
    return spec_path, payload


def resolve_output_formats(spec: JsonDict, output_path: Path) -> list[str]:
    configured = dig(spec, "output.formats")
    if configured is not None:
        formats = normalize_output_formats(configured)
        if formats:
            return formats
        raise ValueError("spec.output.formats must include at least one supported format.")

    suffix_source = output_path.suffix or "svg"
    formats = normalize_output_formats(suffix_source)
    if not formats:
        raise ValueError("Could not determine output format from the output path.")
    return formats


def build_output_paths(output_path: Path, formats: list[str]) -> dict[str, Path]:
    base_path = output_path.with_suffix("") if output_path.suffix else output_path
    resolved: dict[str, Path] = {}
    requested_format = normalize_output_formats(output_path.suffix or "svg")[0] if output_path.suffix else None
    for fmt in formats:
        if len(formats) == 1 and requested_format == fmt and output_path.suffix:
            resolved[fmt] = output_path
            continue
        resolved[fmt] = base_path.with_suffix(suffix_for_format(fmt))
    return resolved


def render_to_files(
    *,
    poster_type: str,
    spec_path: Path,
    output_path: Path,
    spec: JsonDict,
    render_svg: RenderSvgFn,
    default_scale: float,
    default_quality: int,
    default_background: str,
    prepare_spec: PrepareSpecFn | None = None,
) -> JsonDict:
    base_dir = spec_path.parent
    prepared_spec = prepare_spec(spec, base_dir) if prepare_spec else dict(spec)
    output_formats = resolve_output_formats(prepared_spec, output_path)
    output_paths = build_output_paths(output_path, output_formats)
    primary_output = next(iter(output_paths.values()))
    primary_output.parent.mkdir(parents=True, exist_ok=True)

    svg_markup = render_svg(prepared_spec, base_dir=base_dir)
    svg_path = output_paths.get("svg")
    temp_svg_path: Path | None = None
    if svg_path is None:
        with tempfile.NamedTemporaryFile(prefix=f"{poster_type}-", suffix=".svg", delete=False, dir=primary_output.parent) as handle:
            temp_svg_path = Path(handle.name)
        svg_path = temp_svg_path
    svg_path.write_text(svg_markup, encoding="utf-8")

    rendered_paths: list[tuple[str, Path]] = []
    quality = int(dig(prepared_spec, "output.quality", default_quality))
    scale = float(dig(prepared_spec, "output.scale", default_scale))
    background = str(dig(prepared_spec, "output.background", default_background))

    try:
        for fmt, target in output_paths.items():
            if fmt == "svg":
                rendered_paths.append((fmt, target))
                continue
            convert_svg_file(
                svg_path,
                target,
                fmt=fmt,
                scale=scale,
                quality=quality,
                background=background,
            )
            rendered_paths.append((fmt, target))
    finally:
        if temp_svg_path is not None and temp_svg_path.exists():
            temp_svg_path.unlink()

    return {
        "ok": True,
        "poster_type": poster_type,
        "spec_path": str(spec_path),
        "requested_output": str(output_path),
        "output_formats": output_formats,
        "primary_output": str(primary_output),
        "rendered_files": [{"format": fmt, "path": str(path)} for fmt, path in rendered_paths],
    }


def emit_json(payload: JsonDict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def emit_error(*, poster_type: str | None, error: Exception | str, spec_path: Path | None = None, output_path: Path | None = None) -> None:
    payload: JsonDict = {
        "ok": False,
        "poster_type": poster_type,
        "error": str(error),
    }
    if spec_path is not None:
        payload["spec_path"] = str(spec_path)
    if output_path is not None:
        payload["requested_output"] = str(output_path)
    emit_json(payload)


def run_renderer_cli(
    *,
    poster_type: str,
    description: str,
    render_svg: RenderSvgFn,
    default_scale: float,
    default_quality: int = 92,
    default_background: str = "#ffffff",
    prepare_spec: PrepareSpecFn | None = None,
) -> None:
    parser = build_parser(description)
    args = parser.parse_args()

    spec_path: Path | None = None
    output_path = Path(args.output).resolve()
    try:
        spec_path, spec = load_spec(args.spec)
        payload = render_to_files(
            poster_type=poster_type,
            spec_path=spec_path,
            output_path=output_path,
            spec=spec,
            render_svg=render_svg,
            default_scale=default_scale,
            default_quality=default_quality,
            default_background=default_background,
            prepare_spec=prepare_spec,
        )
    except (ValueError, json.JSONDecodeError, SvgConversionError, OSError) as exc:
        emit_error(poster_type=poster_type, error=exc, spec_path=spec_path, output_path=output_path)
        raise SystemExit(1) from exc

    emit_json(payload)
