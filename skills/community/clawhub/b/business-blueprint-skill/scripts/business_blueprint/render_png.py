from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PngRenderResult:
    ok: bool
    skipped: bool
    svg_path: Path
    png_path: Path | None
    renderer: str | None
    reason: str


def _import_cairosvg() -> Any | None:
    try:
        import cairosvg  # type: ignore
    except Exception:
        return None
    return cairosvg


def render_svg_to_png(svg_path: Path, png_path: Path | None = None, *, scale: float = 2) -> PngRenderResult:
    svg_path = Path(svg_path)
    output = Path(png_path) if png_path else svg_path.with_suffix(".png")
    cairosvg = _import_cairosvg()
    if cairosvg is None:
        return PngRenderResult(
            ok=False,
            skipped=True,
            svg_path=svg_path,
            png_path=output,
            renderer=None,
            reason="cairosvg_unavailable",
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(url=str(svg_path), write_to=str(output), scale=scale)
    return PngRenderResult(
        ok=True,
        skipped=False,
        svg_path=svg_path,
        png_path=output,
        renderer="cairosvg",
        reason="rendered",
    )


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(prog="render-png")
    parser.add_argument("svg")
    parser.add_argument("--output")
    parser.add_argument("--scale", type=float, default=2)
    args = parser.parse_args()

    result = render_svg_to_png(
        Path(args.svg),
        Path(args.output) if args.output else None,
        scale=args.scale,
    )
    print(json.dumps(_to_json(result), ensure_ascii=False, indent=2))
    return 0 if result.ok or result.skipped else 1


def _to_json(result: PngRenderResult) -> dict[str, str | bool | None]:
    return {
        "ok": result.ok,
        "skipped": result.skipped,
        "svgPath": str(result.svg_path),
        "pngPath": str(result.png_path) if result.png_path else None,
        "renderer": result.renderer,
        "reason": result.reason,
    }


if __name__ == "__main__":
    raise SystemExit(main())
