#!/usr/bin/env python3
"""Convert SVG files into image formats with local backends."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

SUPPORTED_FORMATS = {"svg", "png", "jpg", "jpeg", "webp"}


class SvgConversionError(RuntimeError):
    """Raised when SVG conversion cannot be completed."""


def normalize_output_formats(value: str | Iterable[str] | None) -> list[str]:
    if value is None:
        return []
    items = [value] if isinstance(value, str) else list(value)
    normalized: list[str] = []
    for item in items:
        fmt = str(item or "").strip().lower().lstrip(".")
        if not fmt:
            continue
        if fmt not in SUPPORTED_FORMATS:
            supported = ", ".join(sorted(SUPPORTED_FORMATS))
            raise SvgConversionError(f"Unsupported output format '{fmt}'. Supported: {supported}.")
        if fmt not in normalized:
            normalized.append(fmt)
    return normalized


def suffix_for_format(fmt: str) -> str:
    normalized = fmt.lower().lstrip(".")
    if normalized not in SUPPORTED_FORMATS:
        raise SvgConversionError(f"Unsupported output format '{fmt}'.")
    return ".jpg" if normalized == "jpg" else f".{normalized}"


def output_format_from_path(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    formats = normalize_output_formats(suffix or "svg")
    if not formats:
        raise SvgConversionError(f"Could not determine output format from path '{path}'.")
    return formats[0]


def convert_svg_file(
    svg_path: Path,
    output_path: Path,
    *,
    fmt: str | None = None,
    scale: float = 1.0,
    quality: int = 92,
    background: str = "#ffffff",
) -> Path:
    svg_path = svg_path.resolve()
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    target_format = normalize_output_formats(fmt or output_path.suffix or "svg")[0]

    if target_format == "svg":
        if svg_path != output_path:
            shutil.copyfile(svg_path, output_path)
        return output_path

    errors: list[str] = []
    for converter in _candidate_converters(target_format):
        try:
            converter(svg_path, output_path, scale=scale, quality=quality, background=background)
            if output_path.exists():
                return output_path
            raise SvgConversionError(f"Backend '{converter.__name__}' finished without creating '{output_path.name}'.")
        except SvgConversionError as exc:
            errors.append(str(exc))

    message = " ; ".join(errors) if errors else "No supported conversion backend was found."
    raise SvgConversionError(message)


def _candidate_converters(fmt: str) -> list:
    normalized = fmt.lower()
    if normalized == "png":
        return [_convert_with_magick, _convert_with_inkscape, _convert_with_rsvg_convert, _convert_with_resvg]
    if normalized in {"jpg", "jpeg", "webp"}:
        return [_convert_with_magick, _convert_with_resvg]
    return []


def _convert_with_magick(svg_path: Path, output_path: Path, *, scale: float, quality: int, background: str) -> None:
    executable = shutil.which("magick")
    if not executable:
        raise SvgConversionError("ImageMagick 'magick' was not found on PATH.")

    width, height = read_svg_size(svg_path)
    resize = f"{max(1, round(width * scale))}x{max(1, round(height * scale))}!"
    target_format = output_format_from_path(output_path)
    bg = background if target_format in {"jpg", "jpeg", "webp"} else "none"
    command = [
        executable,
        "-background",
        bg,
        str(svg_path),
        "-resize",
        resize,
    ]
    if target_format in {"jpg", "jpeg", "webp"}:
        command.extend(["-quality", str(max(1, min(100, int(quality))))])
    command.append(str(output_path))
    _run_command(command, f"ImageMagick failed to convert '{svg_path.name}' to '{output_path.suffix}'.")


def _convert_with_inkscape(svg_path: Path, output_path: Path, *, scale: float, quality: int, background: str) -> None:
    del quality, background
    if output_format_from_path(output_path) != "png":
        raise SvgConversionError("Inkscape backend only supports PNG in this converter.")
    executable = shutil.which("inkscape")
    if not executable:
        raise SvgConversionError("Inkscape was not found on PATH.")

    width, height = read_svg_size(svg_path)
    command = [
        executable,
        str(svg_path),
        "--export-type=png",
        f"--export-filename={output_path}",
        f"--export-width={max(1, round(width * scale))}",
        f"--export-height={max(1, round(height * scale))}",
    ]
    _run_command(command, f"Inkscape failed to convert '{svg_path.name}' to PNG.")


def _convert_with_rsvg_convert(svg_path: Path, output_path: Path, *, scale: float, quality: int, background: str) -> None:
    del quality, background
    if output_format_from_path(output_path) != "png":
        raise SvgConversionError("rsvg-convert backend only supports PNG in this converter.")
    executable = shutil.which("rsvg-convert")
    if not executable:
        raise SvgConversionError("librsvg 'rsvg-convert' was not found on PATH.")

    width, height = read_svg_size(svg_path)
    command = [
        executable,
        "-f",
        "png",
        "-w",
        str(max(1, round(width * scale))),
        "-h",
        str(max(1, round(height * scale))),
        "-o",
        str(output_path),
        str(svg_path),
    ]
    _run_command(command, f"rsvg-convert failed to convert '{svg_path.name}' to PNG.")


def _convert_with_resvg(svg_path: Path, output_path: Path, *, scale: float, quality: int, background: str) -> None:
    """Convert SVG using resvg — tries resvg_py Python package first, then resvg CLI binary."""
    target_format = output_format_from_path(output_path)
    bg = background if background and background.lower() not in {"none", "transparent"} else ""

    # --- Tier 1: resvg_py Python package (in-process, no subprocess) ---
    try:
        import resvg_py

        kwargs: dict = {"svg_path": str(svg_path), "zoom": max(1, int(scale))}
        if bg:
            kwargs["background"] = bg
        try:
            png_bytes = bytes(resvg_py.svg_to_bytes(**kwargs))
        except Exception as exc:
            raise SvgConversionError(f"resvg_py failed to render '{svg_path.name}': {exc}") from exc

        _write_resvg_output(png_bytes, output_path, target_format, quality, background)
        return
    except ImportError:
        pass  # fall through to Tier 2

    # --- Tier 2: resvg CLI binary (subprocess) ---
    executable = shutil.which("resvg")
    if not executable:
        raise SvgConversionError(
            "No resvg backend available. Install one of:\n"
            "  pip install resvg_py          (Python package, recommended)\n"
            "  cargo install resvg           (Rust CLI)\n"
            "  brew install resvg            (macOS)\n"
            "  scoop install resvg           (Windows)"
        )

    if target_format == "png":
        command = [executable, "-z", f"{max(0.1, float(scale)):g}"]
        if bg:
            command.extend(["--background", bg])
        command.extend([str(svg_path), str(output_path)])
        _run_command(command, f"resvg CLI failed to convert '{svg_path.name}' to PNG.")
        return

    # For JPG/WEBP: render to a temporary PNG first, then convert via Pillow
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_png = Path(tmp.name)
    try:
        command = [executable, "-z", f"{max(0.1, float(scale)):g}"]
        if bg:
            command.extend(["--background", bg])
        command.extend([str(svg_path), str(tmp_png)])
        _run_command(command, f"resvg CLI failed to render '{svg_path.name}'.")
        png_bytes = tmp_png.read_bytes()
    finally:
        tmp_png.unlink(missing_ok=True)

    _write_resvg_output(png_bytes, output_path, target_format, quality, background)


def _write_resvg_output(
    png_bytes: bytes, output_path: Path, target_format: str, quality: int, background: str
) -> None:
    """Write PNG bytes to *output_path*, converting to JPG/WEBP via Pillow when needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if target_format == "png":
        output_path.write_bytes(png_bytes)
        return

    try:
        from PIL import Image
    except ImportError:
        raise SvgConversionError(
            f"Pillow is required for {target_format.upper()} output via resvg. "
            "Run 'pip install Pillow' to enable it."
        )

    import io

    img = Image.open(io.BytesIO(png_bytes))
    if target_format in {"jpg", "jpeg"}:
        if img.mode in ("RGBA", "LA", "PA"):
            bg_color = background if background and background.lower() not in {"none", "transparent"} else "#ffffff"
            bg_img = Image.new("RGB", img.size, bg_color)
            bg_img.paste(img, mask=img.split()[-1])
            img = bg_img
        elif img.mode != "RGB":
            img = img.convert("RGB")
        img.save(str(output_path), format="JPEG", quality=max(1, min(100, int(quality))))
    elif target_format == "webp":
        img.save(str(output_path), format="WEBP", quality=max(1, min(100, int(quality))))
    else:
        raise SvgConversionError(f"resvg backend does not support '{target_format}' format.")


def read_svg_size(svg_path: Path) -> tuple[float, float]:
    try:
        root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
    except (OSError, ET.ParseError) as exc:
        raise SvgConversionError(f"Could not parse SVG size from '{svg_path.name}': {exc}") from exc

    width = _parse_svg_length(root.get("width"))
    height = _parse_svg_length(root.get("height"))
    if width and height:
        return width, height

    view_box = root.get("viewBox") or root.get("viewbox")
    if view_box:
        parts = re.split(r"[\s,]+", view_box.strip())
        if len(parts) == 4:
            try:
                return float(parts[2]), float(parts[3])
            except ValueError:
                pass

    raise SvgConversionError(f"SVG '{svg_path.name}' is missing usable width/height or viewBox data.")


def _parse_svg_length(value: str | None) -> float | None:
    if not value:
        return None
    match = re.match(r"^\s*(\d+(?:\.\d+)?)", str(value))
    if not match:
        return None
    return float(match.group(1))


def _run_command(command: list[str], failure_message: str) -> None:
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SvgConversionError(f"{failure_message} {exc}") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise SvgConversionError(f"{failure_message} {detail}") from exc

    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise SvgConversionError(f"{failure_message} {detail}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert an SVG poster into raster image formats.")
    parser.add_argument("--input", required=True, help="Path to the input SVG file.")
    parser.add_argument("--output", required=True, help="Target output image path.")
    parser.add_argument("--format", help="Optional explicit output format. Defaults to the output file suffix.")
    parser.add_argument("--scale", type=float, default=1.0, help="Raster scale factor for PNG/JPG/WEBP output.")
    parser.add_argument("--quality", type=int, default=92, help="JPEG/WEBP quality from 1 to 100.")
    parser.add_argument("--background", default="#ffffff", help="Fallback background color for opaque image formats.")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    if input_path.suffix.lower() != ".svg":
        raise SystemExit("The converter input must be an .svg file.")

    converted = convert_svg_file(
        input_path,
        output_path,
        fmt=args.format,
        scale=args.scale,
        quality=args.quality,
        background=args.background,
    )
    print(f"Converted image: {converted}")


if __name__ == "__main__":
    main()
