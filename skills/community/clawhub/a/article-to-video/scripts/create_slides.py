# -*- coding: utf-8 -*-
"""
Stage 3: Visual Generation
Generates slide images from scenes using HTML templates or AI image generation.

Two modes:
  - template: Render HTML → PNG using Pillow (fast, no API needed)
  - ai:      Use GenerateImage tool (higher quality, slower)

Usage:
    python create_slides.py --scenes scenes.json --outdir ./slides --mode template
    python create_slides.py --scenes scenes.json --outdir ./slides --mode template --theme dark
"""

import argparse
import json
import os
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import SLIDE_CONFIG, VIDEO_CONFIG, CONTENT_TYPE_STYLES, KEN_BURNS_SPEED_MAP, AI_IMAGE_CONFIG


# ============================================================
# Color Theme Resolution
# ============================================================

def get_theme(theme_name: str) -> dict:
    """Get color theme by name."""
    themes = SLIDE_CONFIG["themes"]
    return themes.get(theme_name, themes[SLIDE_CONFIG["default_theme"]])


def resolve_style(content_type: str, user_theme: str = None) -> dict:
    """Resolve visual style from content type, with optional user override.

    Returns a dict with:
        - theme: merged color dict (base theme + override colors)
        - theme_name: the base theme name used
        - font_title: title font family
        - font_body: body font family
        - ken_burns_speed: speed preset name
        - content_type: the resolved content type
    """
    # Get style preset for content type (fallback to "default")
    style = CONTENT_TYPE_STYLES.get(content_type, CONTENT_TYPE_STYLES["default"])

    # Determine theme name: user override > content type default
    theme_name = user_theme if user_theme else style["theme"]

    # Get base theme colors
    theme = get_theme(theme_name).copy()

    # Apply content-type-specific color overrides if present
    override = style.get("theme_override")
    if override:
        for key in ("bg", "accent", "text"):
            if key in override:
                theme[key] = override[key]
        # Store secondary accent for advanced layouts
        if "accent_secondary" in override:
            theme["accent_secondary"] = override["accent_secondary"]

    return {
        "theme": theme,
        "theme_name": theme_name,
        "font_title": style["font_title"],
        "font_body": style["font_body"],
        "ken_burns_speed": style["ken_burns_speed"],
        "content_type": content_type,
    }


# ============================================================
# Template Slide Rendering (Pillow-based)
# ============================================================

def render_template_slide(scene: dict, output_path: str, theme: dict,
                           width: int, height: int):
    """Render a text-based slide image using Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    # Create background
    img = Image.new('RGB', (width, height), theme["bg"])
    draw = ImageDraw.Draw(img)

    # Accent bar at top
    accent = theme["accent"]
    bar_height = 8
    draw.rectangle([0, 0, width, bar_height], fill=accent)

    # Fonts
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",      # Microsoft YaHei
        "C:/Windows/Fonts/msyhbd.ttc",     # Microsoft YaHei Bold
        "C:/Windows/Fonts/simhei.ttf",     # SimHei
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]

    def load_font(size: int, bold: bool = False):
        paths = font_paths if not bold else [
            "C:/Windows/Fonts/msyhbd.ttc",
            "C:/Windows/Fonts/simhei.ttf",
        ] + font_paths
        for fp in paths:
            if os.path.exists(fp):
                try:
                    return ImageFont.truetype(fp, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    # Layout positions
    margin_x = 80
    margin_y = 60
    current_y = margin_y + bar_height

    # Scene number badge
    badge_text = f"{scene['index'] + 1}"
    font_badge = load_font(48, bold=True)
    draw.text((margin_x, current_y), badge_text, fill=accent, font=font_badge)
    current_y += 70

    # Heading
    heading = scene.get("heading", "")
    if heading:
        font_heading = load_font(40, bold=True)
        # Wrap heading text
        wrapped = textwrap.wrap(heading, width=25)
        for line in wrapped[:2]:  # Max 2 lines for heading
            draw.text((margin_x, current_y), line, fill=theme["text"], font=font_heading)
            current_y += 52
        current_y += 20

    # Divider line
    draw.rectangle([margin_x, current_y, margin_x + 120, current_y + 3], fill=accent)
    current_y += 30

    # Body text (slide_text)
    slide_text = scene.get("slide_text", scene.get("narration", ""))
    font_body = load_font(28)

    # Estimate chars per line based on width
    chars_per_line = max(20, (width - 2 * margin_x) // 32)
    wrapped_lines = []
    for paragraph in slide_text.split('\n'):
        wrapped_lines.extend(textwrap.wrap(paragraph, width=chars_per_line))

    # Limit lines to fit on screen
    max_lines = (height - current_y - margin_y) // 42
    if len(wrapped_lines) > max_lines:
        wrapped_lines = wrapped_lines[:max_lines]
        if wrapped_lines[-1][-3:] != "...":
            wrapped_lines[-1] = wrapped_lines[-1][:-3] + "..."

    for line in wrapped_lines:
        draw.text((margin_x, current_y), line, fill=theme["text"], font=font_body)
        current_y += 42

    # Footer: progress indicator
    font_footer = load_font(20)
    footer_y = height - 50
    draw.text((margin_x, footer_y), scene.get("heading", "")[:30],
              fill=accent, font=font_footer)

    # Save
    img.save(output_path, 'PNG', optimize=True)
    return output_path


def render_title_slide(title: str, output_path: str, theme: dict,
                       width: int, height: int, subtitle: str = ""):
    """Render a title slide (used as the first frame)."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new('RGB', (width, height), theme["bg"])
    draw = ImageDraw.Draw(img)

    # Accent bar
    draw.rectangle([0, 0, width, 8], fill=theme["accent"])

    # Center title vertically
    font_paths = [
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]

    def load_font(size: int, bold: bool = True):
        paths = font_paths if bold else [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
        ]
        for fp in paths:
            if os.path.exists(fp):
                try:
                    return ImageFont.truetype(fp, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    # Title (centered)
    font_title = load_font(56, bold=True)
    import textwrap
    wrapped = textwrap.wrap(title, width=20)
    total_h = len(wrapped) * 72
    start_y = (height - total_h) // 2 - 40

    for i, line in enumerate(wrapped):
        bbox = draw.textbbox((0, 0), line, font=font_title)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        draw.text((x, start_y + i * 72), line, fill=theme["text"], font=font_title)

    # Subtitle
    if subtitle:
        font_sub = load_font(28, bold=False)
        sub_y = start_y + len(wrapped) * 72 + 30
        bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        draw.text((x, sub_y), subtitle, fill=theme["accent"], font=font_sub)

    # Bottom accent line
    draw.rectangle([width//2 - 80, height - 100, width//2 + 80, height - 97],
                   fill=theme["accent"])

    img.save(output_path, 'PNG', optimize=True)
    return output_path


# ============================================================
# AI Image Generation — Request Manifest
# ============================================================

def generate_ai_manifest(scenes: list, output_dir: str, content_type: str,
                         width: int, height: int) -> str:
    """Generate a JSON manifest of AI image generation requests.

    The manifest is saved to <output_dir>/ai_image_requests.json and contains
    one request per scene. Each request includes the full prompt (from
    scenes.json image_prompt field), output path, and image dimensions.

    The AI agent (or skill caller) reads this manifest and calls GenerateImage
    for each request. If generation fails for a scene, the caller should
    fall back to render_template_slide().

    Args:
        scenes: List of scene dicts from scenes.json
        output_dir: Directory where slide images will be saved
        content_type: Content type for style reference
        width: Target image width
        height: Target image height

    Returns: Path to the generated manifest JSON file.
    """
    requests = []
    for scene in scenes:
        output_path = os.path.join(output_dir, f"scene_{scene['index']:03d}.png")
        requests.append({
            "scene_index": scene["index"],
            "heading": scene.get("heading", ""),
            "prompt": scene.get("image_prompt", ""),
            "output_path": output_path,
            "image_size": AI_IMAGE_CONFIG.get("image_size", "landscape_16_9"),
            "content_type": content_type,
        })

    manifest = {
        "mode": "ai",
        "content_type": content_type,
        "image_size": AI_IMAGE_CONFIG.get("image_size", "landscape_16_9"),
        "resolution": f"{width}x{height}",
        "total_requests": len(requests),
        "requests": requests,
        "instructions": (
            "For each request, call GenerateImage with the 'prompt' and 'image_size' fields. "
            "Save the generated image to the 'output_path'. "
            "If generation fails, fall back to render_template_slide() in create_slides.py."
        ),
    }

    manifest_path = os.path.join(output_dir, "ai_image_requests.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return manifest_path


# ============================================================
# Main Pipeline
# ============================================================

def run_slide_pipeline(scenes_path: str, output_dir: str, mode: str,
                       theme_name: str, platform: str):
    """Generate all slide images from scenes.

    Args:
        theme_name: User-specified theme override. If None, the content type's
                    default theme is used. If a string (including "default"),
                    it overrides the content type's theme.
    """
    with open(scenes_path, 'r', encoding='utf-8') as f:
        scenes_data = json.load(f)

    scenes = scenes_data["scenes"]
    title = scenes_data["title"]
    total = len(scenes)
    content_type = scenes_data.get("content_type", "default")

    # Resolve visual style from content type (with optional user theme override)
    # Pass theme_name as user_theme only if it was explicitly specified
    style = resolve_style(content_type, user_theme=theme_name)
    theme = style["theme"]

    print(f"Slide Generation: {total} scenes, mode={mode}")
    print(f"  Content type: {content_type} → theme={style['theme_name']}, "
          f"ken_burns={style['ken_burns_speed']}")
    print(f"Output: {output_dir}")
    print()

    os.makedirs(output_dir, exist_ok=True)

    # Get resolution
    platforms = VIDEO_CONFIG["platforms"]
    platform_cfg = platforms.get(platform, platforms[VIDEO_CONFIG["default_platform"]])
    width = platform_cfg["width"]
    height = platform_cfg["height"]

    # Generate title slide
    title_path = os.path.join(output_dir, "title.png")
    subtitle = f"{scenes_data.get('estimated_duration_sec', 0) / 60:.1f} min video"
    render_title_slide(title, title_path, theme, width, height, subtitle)
    print(f"  Title slide: {title_path}")

    # Generate scene slides
    results = []
    if mode == "ai":
        # AI mode: generate template slides as fallback, then create manifest
        print("--- Generating template fallback slides ---")
        for i, scene in enumerate(scenes):
            print(f"[{i+1}/{total}] Scene {scene['index']}")
            output_path = os.path.join(output_dir, f"scene_{scene['index']:03d}.png")
            render_template_slide(scene, output_path, theme, width, height)
            results.append({"index": scene["index"], "image": output_path})
            print(f"    Saved (fallback): {output_path}")

        # Generate AI image request manifest
        manifest_path = generate_ai_manifest(scenes, output_dir, content_type, width, height)
        print(f"\n--- AI Image Request Manifest ---")
        print(f"  Manifest: {manifest_path}")
        print(f"  Total requests: {len(scenes)}")
        print(f"  Image size: {AI_IMAGE_CONFIG.get('image_size', 'landscape_16_9')}")
        print(f"  Instructions: Read the manifest and call GenerateImage for each request.")
        print(f"  Generated images will overwrite the fallback template slides.")
    else:
        # Template mode: render all slides directly
        for i, scene in enumerate(scenes):
            print(f"[{i+1}/{total}] Scene {scene['index']}")
            output_path = os.path.join(output_dir, f"scene_{scene['index']:03d}.png")
            render_template_slide(scene, output_path, theme, width, height)
            results.append({"index": scene["index"], "image": output_path})
            print(f"    Saved: {output_path}")

    # Save manifest
    manifest = {
        "title_slide": title_path,
        "scenes": results,
        "theme": style["theme_name"],
        "content_type": content_type,
        "ken_burns_speed": style["ken_burns_speed"],
        "resolution": f"{width}x{height}",
        "platform": platform,
        "mode": mode,
    }
    if mode == "ai":
        manifest["ai_manifest_path"] = os.path.join(output_dir, "ai_image_requests.json")
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\nDone! {total + 1} images generated (1 title + {total} scenes)")
    print(f"Manifest: {manifest_path}")

    return manifest


# ============================================================
# Main Entry Point
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Generate slide images from scenes")
    parser.add_argument("--scenes", "-s", required=True, help="scenes.json path")
    parser.add_argument("--outdir", "-o", required=True, help="Output image directory")
    parser.add_argument("--mode", "-m", default="template",
                       choices=["template", "ai"],
                       help="Generation mode (default: template)")
    parser.add_argument("--theme", "-t", default=None,
                       help="Color theme override (default, light, dark, warm, ocean). "
                            "If not specified, theme is auto-selected from content type.")
    parser.add_argument("--platform", "-p", default=VIDEO_CONFIG["default_platform"],
                       help="Target platform (youtube, tiktok, xiaohongshu)")
    args = parser.parse_args()

    run_slide_pipeline(args.scenes, args.outdir, args.mode, args.theme, args.platform)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
