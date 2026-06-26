#!/usr/bin/env python3
"""Unified poster entrypoint for every poster type in this repository."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from poster_runtime import (
    build_parser,
    emit_error,
    emit_json,
    load_spec,
    normalize_poster_type,
    render_to_files,
)
from render_baidu_hot import (
    DEFAULT_OUTPUT_SCALE as BAIDU_DEFAULT_OUTPUT_SCALE,
    POSTER_TYPE as BAIDU_POSTER_TYPE,
    THEME as BAIDU_THEME,
    normalize_baidu_hot_spec,
    render_baidu_hot_poster,
)
from render_daily_poster import (
    DEFAULT_OUTPUT_BACKGROUND as DAILY_DEFAULT_OUTPUT_BACKGROUND,
    DEFAULT_OUTPUT_SCALE as DAILY_DEFAULT_OUTPUT_SCALE,
    POSTER_TYPE as DAILY_POSTER_TYPE,
    normalize_daily_spec,
    render_poster as render_daily_poster,
)

RENDERERS = {
    DAILY_POSTER_TYPE: {
        "render_svg": render_daily_poster,
        "prepare_spec": normalize_daily_spec,
        "default_scale": DAILY_DEFAULT_OUTPUT_SCALE,
        "default_background": DAILY_DEFAULT_OUTPUT_BACKGROUND,
    },
    BAIDU_POSTER_TYPE: {
        "render_svg": render_baidu_hot_poster,
        "prepare_spec": normalize_baidu_hot_spec,
        "default_scale": BAIDU_DEFAULT_OUTPUT_SCALE,
        "default_background": BAIDU_THEME["page_bg"],
    },
}


def infer_poster_type(spec: dict[str, Any], explicit_type: str | None) -> str:
    normalized_explicit = normalize_poster_type(explicit_type)
    if normalized_explicit:
        return normalized_explicit

    for candidate in (spec.get("poster_type"), spec.get("type"), spec.get("poster")):
        normalized = normalize_poster_type(candidate)
        if normalized:
            return normalized

    content = spec.get("content")
    if isinstance(content, dict) and any(key in content for key in ("items", "api_url", "limit")):
        return BAIDU_POSTER_TYPE

    legacy_baidu_keys = ("api_url", "limit", "items")
    if any(key in spec for key in legacy_baidu_keys):
        return BAIDU_POSTER_TYPE

    if "lead_story" in spec or "sidebar_note" in spec or "countdown" in spec:
        return DAILY_POSTER_TYPE

    return DAILY_POSTER_TYPE


def main() -> None:
    parser = build_parser("Render any supported poster type from a JSON spec.", include_type=True)
    args = parser.parse_args()

    spec_path: Path | None = None
    output_path = Path(args.output).resolve()
    poster_type: str | None = None

    try:
        spec_path, spec = load_spec(args.spec)
        poster_type = infer_poster_type(spec, args.poster_type)
        renderer = RENDERERS.get(poster_type)
        if renderer is None:
            raise ValueError(f"Unsupported poster type: {poster_type}")

        payload = render_to_files(
            poster_type=poster_type,
            spec_path=spec_path,
            output_path=output_path,
            spec=spec,
            render_svg=renderer["render_svg"],
            default_scale=renderer["default_scale"],
            default_quality=92,
            default_background=renderer["default_background"],
            prepare_spec=renderer["prepare_spec"],
        )
    except Exception as exc:
        emit_error(poster_type=poster_type, error=exc, spec_path=spec_path, output_path=output_path)
        raise SystemExit(1) from exc

    emit_json(payload)


if __name__ == "__main__":
    main()
