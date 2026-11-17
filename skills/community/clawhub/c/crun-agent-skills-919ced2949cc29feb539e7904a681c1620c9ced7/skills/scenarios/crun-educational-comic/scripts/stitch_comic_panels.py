#!/usr/bin/env python3
"""
Multi-Panel Educational Comic Stitcher & Caption Overlay Script
Assembles individual panel images into a clean comic grid layout with title banner,
panel numbers, border gutters, and text caption boxes.
"""

import os
import sys
import json
import argparse
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont


def find_system_cjk_font(font_size: int = 18) -> ImageFont.ImageFont:
    """Find a system CJK font (Windows/Linux/macOS) for PIL rendering."""
    candidate_paths = [
        # Windows
        "C:\\Windows\\Fonts\\msyh.ttc",       # YaHei
        "C:\\Windows\\Fonts\\msyhbd.ttc",     # YaHei Bold
        "C:\\Windows\\Fonts\\simhei.ttf",     # SimHei
        "C:\\Windows\\Fonts\\simsun.ttc",     # SimSun
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        # Linux
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, font_size)
            except Exception:
                continue
                
    # Fallback to default
    try:
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
    """Wrap text (supporting CJK and English) to fit within specified max_width."""
    if not text:
        return []
        
    lines = []
    current_line = ""
    
    # Process text character by character or word by word
    # For CJK, character-by-character; for English, space-separated
    words = []
    buffer = ""
    for char in text:
        if ord(char) > 127: # CJK or special unicode
            if buffer:
                words.append(buffer)
                buffer = ""
            words.append(char)
        elif char in (' ', '\n'):
            if buffer:
                words.append(buffer)
                buffer = ""
            if char == '\n':
                words.append('\n')
            else:
                words.append(' ')
        else:
            buffer += char
    if buffer:
        words.append(buffer)
        
    for item in words:
        if item == '\n':
            lines.append(current_line)
            current_line = ""
            continue
            
        test_line = current_line + item
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = item.lstrip()
            
    if current_line:
        lines.append(current_line)
        
    return lines


def calculate_grid_dimensions(num_panels: int, grid_arg: str) -> Tuple[int, int]:
    """Calculate rows and columns based on panel count or user argument."""
    if grid_arg and grid_arg != "auto" and "x" in grid_arg:
        parts = grid_arg.lower().split("x")
        try:
            cols = int(parts[0])
            rows = int(parts[1])
            return cols, rows
        except ValueError:
            pass
            
    if num_panels <= 1:
        return 1, 1
    elif num_panels == 2:
        return 2, 1
    elif num_panels == 3:
        return 3, 1
    elif num_panels == 4:
        return 2, 2
    elif num_panels <= 6:
        return 2, 3
    elif num_panels <= 8:
        return 2, 4
    elif num_panels <= 9:
        return 3, 3
    else:
        cols = 3
        rows = (num_panels + cols - 1) // cols
        return cols, rows


def create_comic_strip(
    image_paths: List[str],
    captions: List[str],
    title: str = "Educational Comic",
    output_path: str = "comic_output.png",
    grid: str = "auto",
    target_panel_size: Tuple[int, int] = (800, 800),
    gutter: int = 24,
    banner_height: int = 100,
    bg_color: str = "#F8FAFC",
    banner_bg: str = "#0F172A",
    banner_text_color: str = "#FFFFFF",
    caption_bg: str = "#FFFFFF",
    caption_border_color: str = "#E2E8F0",
    text_color: str = "#1E293B",
) -> dict:
    """Stitch N panel images into a structured comic grid with title and captions."""
    if not image_paths:
        return {"code": 1, "status": "error", "message": "No image paths provided"}
        
    num_panels = len(image_paths)
    cols, rows = calculate_grid_dimensions(num_panels, grid)
    
    # Load and resize panel images
    panel_width, panel_height = target_panel_size
    caption_box_height = 140 # Space allocated for bottom caption overlay under each image
    
    single_cell_width = panel_width
    single_cell_height = panel_height + caption_box_height
    
    total_width = cols * single_cell_width + (cols + 1) * gutter
    total_height = banner_height + rows * single_cell_height + (rows + 1) * gutter
    
    # Create canvas
    canvas = Image.new("RGB", (total_width, total_height), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    # Fonts
    title_font = find_system_cjk_font(font_size=36)
    panel_num_font = find_system_cjk_font(font_size=18)
    caption_font = find_system_cjk_font(font_size=20)
    
    # Render Top Title Banner
    draw.rectangle([(0, 0), (total_width, banner_height)], fill=banner_bg)
    if title:
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_w = title_bbox[2] - title_bbox[0]
        title_h = title_bbox[3] - title_bbox[1]
        title_x = (total_width - title_w) // 2
        title_y = (banner_height - title_h) // 2
        draw.text((title_x, title_y), title, font=title_font, fill=banner_text_color)
        
    # Render Panels
    for idx, path in enumerate(image_paths):
        r = idx // cols
        c = idx % cols
        
        cell_x = gutter + c * (single_cell_width + gutter)
        cell_y = banner_height + gutter + r * (single_cell_height + gutter)
        
        # Load panel image
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGB")
                img = img.resize((panel_width, panel_height), Image.Resampling.LANCZOS)
            except Exception as e:
                # Create placeholder error image
                img = Image.new("RGB", (panel_width, panel_height), "#E2E8F0")
                err_draw = ImageDraw.Draw(img)
                err_draw.text((20, 20), f"Error loading:\n{path}\n{str(e)}", font=caption_font, fill="#EF4444")
        else:
            img = Image.new("RGB", (panel_width, panel_height), "#CBD5E1")
            err_draw = ImageDraw.Draw(img)
            err_draw.text((20, 20), f"File not found:\n{path}", font=caption_font, fill="#64748B")
            
        # Paste image onto canvas
        canvas.paste(img, (cell_x, cell_y))
        
        # Draw Panel Border
        draw.rectangle(
            [(cell_x, cell_y), (cell_x + panel_width, cell_y + panel_height)],
            outline="#94A3B8",
            width=3
        )
        
        # Draw Panel Number Badge (Top-Left of panel image)
        badge_text = f"Panel {idx + 1}"
        badge_bbox = draw.textbbox((0, 0), badge_text, font=panel_num_font)
        badge_w = badge_bbox[2] - badge_bbox[0] + 20
        badge_h = badge_bbox[3] - badge_bbox[1] + 10
        
        draw.rectangle(
            [(cell_x, cell_y), (cell_x + badge_w, cell_y + badge_h)],
            fill="#0F172A"
        )
        draw.text(
            (cell_x + 10, cell_y + 5),
            badge_text,
            font=panel_num_font,
            fill="#FFFFFF"
        )
        
        # Render Caption Box Below Panel Image
        caption_box_y = cell_y + panel_height
        draw.rectangle(
            [(cell_x, caption_box_y), (cell_x + panel_width, caption_box_y + caption_box_height)],
            fill=caption_bg,
            outline=caption_border_color,
            width=2
        )
        
        # Text wrapping and rendering inside caption box
        caption_text = captions[idx] if idx < len(captions) else ""
        if caption_text:
            lines = wrap_text(caption_text, caption_font, panel_width - 30, draw)
            line_height = 28
            start_y = caption_box_y + 15
            
            for line_idx, line in enumerate(lines[:4]): # Max 4 lines
                draw.text(
                    (cell_x + 15, start_y + line_idx * line_height),
                    line,
                    font=caption_font,
                    fill=text_color
                )
                
    # Save stitched image
    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
        
    canvas.save(output_path, quality=95)
    
    return {
        "code": 0,
        "status": "success",
        "title": title,
        "output_file": os.path.abspath(output_path),
        "total_width": total_width,
        "total_height": total_height,
        "cols": cols,
        "rows": rows,
        "panel_count": num_panels
    }


def main():
    parser = argparse.ArgumentParser(description="Stitch N image panels into an educational comic strip")
    parser.add_argument("images", nargs="+", help="Paths to panel image files")
    parser.add_argument("--captions", nargs="*", default=[], help="Captions for each panel in corresponding order")
    parser.add_argument("--title", default="Educational Comic", help="Comic header title banner")
    parser.add_argument("--output", "-o", default="comic_output.png", help="Output PNG/JPG file path")
    parser.add_argument("--grid", default="auto", help="Grid layout: e.g. 2x2, 1x4, 2x3, auto")
    parser.add_argument("--width", type=int, default=800, help="Target width per panel in pixels")
    parser.add_argument("--height", type=int, default=800, help="Target height per panel in pixels")
    
    args = parser.parse_args()
    
    result = create_comic_strip(
        image_paths=args.images,
        captions=args.captions,
        title=args.title,
        output_path=args.output,
        grid=args.grid,
        target_panel_size=(args.width, args.height)
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["code"] != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
