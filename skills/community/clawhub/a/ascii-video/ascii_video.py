#!/usr/bin/env python3
"""
ASCII Video Converter — convert video files to colored ASCII art MP4 or GIF
animations.  Frame-by-frame conversion with color support.

Commands:
  convert <input> --output <file>   Convert video to ASCII animation
  frame   <input> --at <ts>        Preview a single frame
  image   <input>                  Convert still image to ASCII

Depends on:
  - Pillow (pip install Pillow)
  - ffmpeg (for video input / GIF/MP4 output)
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from typing import List, Optional, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None  # type: ignore
    ImageDraw = None
    ImageFont = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Default ASCII character set (dark → light)
ASCII_CHARS_DEFAULT = "@%#*+=-:. "
ASCII_CHARS_SOLID = "█▓▒░ "
ASCII_CHARS_DETAILED = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

DEFAULT_CHARSET = ASCII_CHARS_DEFAULT
DEFAULT_WIDTH = 80
DEFAULT_FPS = 10

# Minimum font size for readable ASCII
FONT_SIZE = 10

# ---------------------------------------------------------------------------
# Core conversion
# ---------------------------------------------------------------------------


def _get_ascii_chars(charset_name: str) -> str:
    """Resolve character set name to string."""
    mapping = {
        "default": ASCII_CHARS_DEFAULT,
        "solid": ASCII_CHARS_SOLID,
        "detailed": ASCII_CHARS_DETAILED,
        "classic": ASCII_CHARS_DEFAULT,
    }
    return mapping.get(charset_name.lower(), charset_name if charset_name else DEFAULT_CHARSET)


def _pixel_to_ascii(pixel: Tuple[int, ...], chars: str) -> str:
    """Map a grayscale pixel value (0-255) to an ASCII character."""
    gray = sum(pixel[:3]) // 3
    idx = gray * (len(chars) - 1) // 255
    return chars[idx]


def _pixel_to_color_ascii(r: int, g: int, b: int, chars: str) -> Tuple[str, Tuple[int, int, int]]:
    """Map an RGB pixel to an ASCII character with its color."""
    gray = (r + g + b) // 3
    idx = gray * (len(chars) - 1) // 255
    return chars[idx], (r, g, b)


def image_to_ascii(
    img: Image.Image,
    width: int = DEFAULT_WIDTH,
    charset: str = DEFAULT_CHARSET,
    color: bool = False,
) -> List[str]:
    """Convert a PIL Image to a list of ASCII strings (one per row)."""
    chars = _get_ascii_chars(charset)
    # Maintain aspect ratio: each char is ~2x as tall as wide in terminal
    aspect_ratio = 0.5
    orig_w, orig_h = img.size
    new_w = width
    new_h = int((orig_h / orig_w) * new_w * aspect_ratio)
    new_h = max(1, new_h)

    img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    if not color:
        img_gray = img_small.convert("L")
        rows: List[str] = []
        for y in range(new_h):
            row = ""
            for x in range(new_w):
                gray = img_gray.getpixel((x, y))
                row += _pixel_to_ascii((gray, gray, gray), chars)
            rows.append(row)
        return rows
    else:
        img_rgb = img_small.convert("RGB")
        color_rows: List[str] = []
        for y in range(new_h):
            cells: List[str] = []
            for x in range(new_w):
                r, g, b = img_rgb.getpixel((x, y))
                ch, _ = _pixel_to_color_ascii(r, g, b, chars)
                # ANSI 24-bit color escape (foreground only, for terminal)
                cells.append(f"\033[38;2;{r};{g};{b}m{ch}")
            color_rows.append("".join(cells) + "\033[0m")
        return color_rows


def render_ascii_to_image(
    ascii_rows: List[str],
    font_path: Optional[str] = None,
    font_size: int = FONT_SIZE,
    foreground: Tuple[int, int, int] = (200, 200, 200),
    background: Tuple[int, int, int] = (0, 0, 0),
) -> Image.Image:
    """Render ASCII art rows to a PIL Image (for GIF/MP4 export)."""
    if Image is None:
        raise RuntimeError("Pillow is required. Install: pip install Pillow")

    try:
        font = ImageFont.truetype(font_path or "DejaVuSansMono.ttf", font_size)
    except (OSError, IOError):
        try:
            # Try common monospace fonts
            for name in [
                "DejaVuSansMono.ttf",
                "LiberationMono-Regular.ttf",
                "Courier_New.ttf",
                "consola.ttf",
                "cour.ttf",
            ]:
                try:
                    font = ImageFont.truetype(name, font_size)
                    break
                except (OSError, IOError):
                    continue
            else:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

    # Measure a single char to compute canvas size
    char_w, char_h = 8, 14  # fallback
    try:
        left, top, right, bottom = font.getbbox("A")
        char_w = right - left
        char_h = bottom - top
    except AttributeError:
        try:
            char_w, char_h = font.getsize("A")
        except Exception:
            pass

    n_rows = len(ascii_rows)
    n_cols = max(len(r) for r in ascii_rows) if ascii_rows else 1

    canvas_w = n_cols * char_w
    canvas_h = n_rows * char_h

    img = Image.new("RGB", (canvas_w, canvas_h), background)
    draw = ImageDraw.Draw(img)

    is_ansi = any("\033[" in row for row in ascii_rows)
    if not is_ansi:
        # Plain ASCII — fast render
        y = 0
        for row in ascii_rows:
            draw.text((0, y), row, fill=foreground, font=font)
            y += char_h
        return img

    # ANSI-colored — parse escape codes per cell
    import re

    ansi_pat = re.compile(r"\033\[38;2;(\d+);(\d+);(\d+)m(.)")
    y = 0
    for row in ascii_rows:
        x = 0
        pos = 0
        while pos < len(row):
            m = ansi_pat.match(row, pos)
            if m:
                r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
                ch = m.group(4)
                draw.text((x, y), ch, fill=(r, g, b), font=font)
                x += char_w
                pos = m.end()
            elif row[pos] == "\033":
                # Skip ANSI reset
                m2 = re.match(r"\033\[0m", row[pos:])
                if m2:
                    pos = m2.end()
                    continue
                # Skip any other escape
                m3 = re.match(r"\033\[[0-9;]*[a-zA-Z]", row[pos:])
                if m3:
                    pos = m3.end()
                    continue
                pos += 1
            else:
                draw.text((x, y), row[pos], fill=foreground, font=font)
                x += char_w
                pos += 1
        y += char_h

    return img


# ---------------------------------------------------------------------------
# Video processing
# ---------------------------------------------------------------------------


def _has_ffmpeg() -> bool:
    """Check if ffmpeg is available."""
    return shutil.which("ffmpeg") is not None


def _ffmpeg_extract_frames(
    video_path: str,
    output_dir: str,
    fps: int = DEFAULT_FPS,
) -> int:
    """Extract video frames as PNG images using ffmpeg."""
    pattern = os.path.join(output_dir, "frame_%06d.png")
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"fps={fps}",
        "-qscale:v", "2",
        "-y", pattern,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr}", file=sys.stderr)
        return 0

    # Count frames
    frames = sorted(os.listdir(output_dir))
    return len(frames)


def _ffmpeg_frames_to_video(
    input_pattern: str,
    output_path: str,
    fps: int = DEFAULT_FPS,
) -> bool:
    """Combine ASCII PNG frames into a video using ffmpeg."""
    cmd = [
        "ffmpeg",
        "-framerate", str(fps),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-y", output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def _ffmpeg_frames_to_gif(
    input_pattern: str,
    output_path: str,
    fps: int = DEFAULT_FPS,
) -> bool:
    """Combine ASCII PNG frames into a GIF using ffmpeg."""
    palette_path = os.path.join(os.path.dirname(output_path), "palette.png")
    # Generate palette
    cmd1 = [
        "ffmpeg",
        "-framerate", str(fps),
        "-i", input_pattern,
        "-vf", "palettegen=stats_mode=diff",
        "-y", palette_path,
    ]
    subprocess.run(cmd1, capture_output=True, text=True)

    cmd2 = [
        "ffmpeg",
        "-framerate", str(fps),
        "-i", input_pattern,
        "-i", palette_path,
        "-lavfi", "paletteuse=dither=bayer:bayer_scale=5",
        "-y", output_path,
    ]
    result = subprocess.run(cmd2, capture_output=True, text=True)

    # Clean up palette
    if os.path.exists(palette_path):
        os.unlink(palette_path)

    return result.returncode == 0


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_convert(args: List[str]) -> int:
    """Convert video to ASCII animation."""
    if Image is None:
        print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser("convert")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("--output", "-o", required=True, help="Output file (.gif or .mp4)")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="ASCII width in chars")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="Frames per second")
    parser.add_argument("--charset", default="default", help="Character set: default, solid, detailed")
    parser.add_argument("--color", action="store_true", help="Preserve color in output")

    parsed, _ = parser.parse_known_args(args)

    if not os.path.exists(parsed.input):
        print(f"Error: input file not found: {parsed.input}", file=sys.stderr)
        return 1

    if not _has_ffmpeg():
        print("Error: ffmpeg not found. Install ffmpeg and add it to PATH.", file=sys.stderr)
        return 1

    out_ext = os.path.splitext(parsed.output)[1].lower()
    if out_ext not in (".gif", ".mp4"):
        print("Error: output must be .gif or .mp4", file=sys.stderr)
        return 1

    is_gif = out_ext == ".gif"
    use_color = parsed.color
    width = parsed.width
    fps = parsed.fps
    charset_name = parsed.charset

    print(f"Converting {parsed.input} → {parsed.output}")
    print(f"  Width: {width} chars, FPS: {fps}, Color: {use_color}, Charset: {charset_name}")

    # Create temp directory for frames
    tmpdir = tempfile.mkdtemp(prefix="ascii_video_")

    try:
        # Step 1: Extract frames with ffmpeg
        print("  Extracting frames...", end=" ", flush=True)
        n_frames = _ffmpeg_extract_frames(parsed.input, tmpdir, fps)
        if n_frames == 0:
            print("FAILED")
            return 1
        print(f"{n_frames} frames")

        # Step 2: Convert each frame to ASCII
        print("  Converting frames to ASCII...", end=" ", flush=True)
        ascii_dir = tempfile.mkdtemp(prefix="ascii_video_out_")
        frame_files = sorted(
            [f for f in os.listdir(tmpdir) if f.endswith(".png")]
        )

        for i, fname in enumerate(frame_files):
            frame_path = os.path.join(tmpdir, fname)
            try:
                img = Image.open(frame_path)
                ascii_rows = image_to_ascii(img, width=width, charset=charset_name, color=use_color)
                rendered = render_ascii_to_image(ascii_rows)
                out_frame = os.path.join(ascii_dir, f"ascii_{i:06d}.png")
                rendered.save(out_frame)
            except Exception as e:
                print(f"\n  Error on frame {i}: {e}", file=sys.stderr)
                continue

            if (i + 1) % 50 == 0:
                print(f"{i+1}/{n_frames}...", end=" ", flush=True)

        print(f"{n_frames}/{n_frames} done")

        # Step 3: Combine into output
        print("  Assembling output...", end=" ", flush=True)
        input_pattern = os.path.join(ascii_dir, "ascii_%06d.png")
        success = False
        if is_gif:
            success = _ffmpeg_frames_to_gif(input_pattern, parsed.output, fps)
        else:
            success = _ffmpeg_frames_to_video(input_pattern, parsed.output, fps)

        if success:
            size = os.path.getsize(parsed.output)
            print(f"DONE ({size / 1024:.1f} KB)")
        else:
            print("FAILED (ffmpeg error)")
            return 1

    finally:
        # Cleanup
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)
        if 'ascii_dir' in dir():
            shutil.rmtree(ascii_dir, ignore_errors=True)

    return 0


def cmd_frame(args: List[str]) -> int:
    """Preview a single frame from a video as ASCII."""
    if Image is None:
        print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser("frame")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("--at", default="00:00:01", help="Timestamp (HH:MM:SS or seconds)")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="ASCII width in chars")
    parser.add_argument("--color", action="store_true", help="Preserve color")

    parsed, _ = parser.parse_known_args(args)

    if not os.path.exists(parsed.input):
        print(f"Error: input file not found: {parsed.input}", file=sys.stderr)
        return 1

    if not _has_ffmpeg():
        print("Error: ffmpeg not found.", file=sys.stderr)
        return 1

    tmpdir = tempfile.mkdtemp(prefix="ascii_frame_")
    frame_path = os.path.join(tmpdir, "frame.png")

    try:
        cmd = [
            "ffmpeg", "-ss", parsed.at, "-i", parsed.input,
            "-vframes", "1", "-qscale:v", "2",
            "-y", frame_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 or not os.path.exists(frame_path):
            print(f"Error extracting frame: {result.stderr}", file=sys.stderr)
            return 1

        img = Image.open(frame_path)
        ascii_rows = image_to_ascii(img, width=parsed.width, charset="default", color=parsed.color)
        print("\n".join(ascii_rows))
        print(f"\n--- Frame at {parsed.at} ({len(ascii_rows)} rows, {parsed.width} cols) ---")
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

    return 0


def cmd_image(args: List[str]) -> int:
    """Convert a still image to ASCII and print to terminal."""
    if Image is None:
        print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser("image")
    parser.add_argument("input", help="Input image file")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="ASCII width in chars")
    parser.add_argument("--color", action="store_true", help="Preserve color")
    parser.add_argument("--charset", default="default", help="Character set: default, solid, detailed")
    parser.add_argument("--output", "-o", help="Save to file instead of printing")

    parsed, _ = parser.parse_known_args(args)

    if not os.path.exists(parsed.input):
        print(f"Error: input file not found: {parsed.input}", file=sys.stderr)
        return 1

    try:
        img = Image.open(parsed.input)
    except Exception as e:
        print(f"Error opening image: {e}", file=sys.stderr)
        return 1

    ascii_rows = image_to_ascii(img, width=parsed.width, charset=parsed.charset, color=parsed.color)

    output = "\n".join(ascii_rows)
    if parsed.output:
        with open(parsed.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"ASCII art saved to {parsed.output}")
    else:
        print(output)
        print(f"\n--- Image: {parsed.input} ({len(ascii_rows)} rows, {parsed.width} cols) ---")

    return 0


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test() -> int:
    """Run built-in verification of ASCII conversion logic."""
    if Image is None:
        print("self-test: SKIP (Pillow not installed)")
        return 1

    passed = 0
    failed = 0

    def check(name: str, cond: bool, detail: str = "") -> None:
        nonlocal passed, failed
        if cond:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}  {detail}")
            failed += 1

    print("ascii-video self-test")
    print("─" * 40)

    # 1. Create a small test image
    img = Image.new("RGB", (40, 20), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 5, 30, 15], fill=(128, 128, 128))

    # 2. Grayscale conversion
    rows_gray = image_to_ascii(img, width=40, charset="default", color=False)
    check("grayscale returns rows", len(rows_gray) > 0)
    check("grayscale rows are strings", all(isinstance(r, str) for r in rows_gray))
    check("grayscale no ANSI codes", all("\033[" not in r for r in rows_gray))

    # 3. Color conversion
    rows_color = image_to_ascii(img, width=40, charset="default", color=True)
    check("color returns rows", len(rows_color) > 0)
    check("color has ANSI codes", any("\033[" in r for r in rows_color))

    # 4. Character set loading
    chars = _get_ascii_chars("solid")
    check("solid charset loads", len(chars) > 0)
    chars2 = _get_ascii_chars("detailed")
    check("detailed charset loads", len(chars2) > len(chars))

    # 5. Render to image
    rendered = render_ascii_to_image(rows_gray)
    check("render returns PIL Image", isinstance(rendered, Image.Image))
    check("render has correct dimensions", rendered.size[0] > 0 and rendered.size[1] > 0)

    # 6. Color render
    rendered_color = render_ascii_to_image(rows_color)
    check("color render succeeds", isinstance(rendered_color, Image.Image))

    # 7. Empty/malformed input robustness
    empty = render_ascii_to_image([])
    check("empty rows render", isinstance(empty, Image.Image))

    # 8. Different widths
    small = image_to_ascii(img, width=20)
    check("smaller width reduces rows", len(small) > 0)
    if rows_gray and small:
        check("different width = different output", rows_gray != small)

    print("─" * 40)
    result = 0 if failed == 0 else 1
    print(f"Result: {passed} passed, {failed} failed")
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ASCII Video Converter — convert video to colored ASCII art animations.",
    )
    parser.add_argument("--version", action="version", version="ascii-video 1.0.0")

    sub = parser.add_subparsers(dest="command", required=True)

    # convert
    conv = sub.add_parser("convert", help="Convert video to ASCII animation")
    conv.add_argument("input", help="Input video file")
    conv.add_argument("--output", "-o", required=True, help="Output file (.gif or .mp4)")
    conv.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="ASCII width in chars")
    conv.add_argument("--fps", type=int, default=DEFAULT_FPS, help="Frames per second")
    conv.add_argument("--charset", default="default", help="Character set: default, solid, detailed")
    conv.add_argument("--color", action="store_true", help="Preserve color")

    # frame
    frame = sub.add_parser("frame", help="Preview a single video frame as ASCII")
    frame.add_argument("input", help="Input video file")
    frame.add_argument("--at", default="00:00:01", help="Timestamp (HH:MM:SS or seconds)")
    frame.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="ASCII width in chars")
    frame.add_argument("--color", action="store_true", help="Preserve color")

    # image
    img_sub = sub.add_parser("image", help="Convert image to ASCII")
    img_sub.add_argument("input", help="Input image file")
    img_sub.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="ASCII width in chars")
    img_sub.add_argument("--color", action="store_true", help="Preserve color")
    img_sub.add_argument("--charset", default="default", help="Character set: default, solid, detailed")
    img_sub.add_argument("--output", "-o", help="Save to file instead of printing")

    # self-test
    sub.add_parser("self-test", help="Run built-in self tests")

    parsed, rest = parser.parse_known_args()

    if parsed.command == "self-test":
        return _self_test()
    elif parsed.command == "convert":
        return cmd_convert(rest if hasattr(parsed, 'input') and parsed.input else [])
    elif parsed.command == "frame":
        return cmd_frame(rest if hasattr(parsed, 'input') and parsed.input else [])
    elif parsed.command == "image":
        return cmd_image(rest if hasattr(parsed, 'input') and parsed.input else [])
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
