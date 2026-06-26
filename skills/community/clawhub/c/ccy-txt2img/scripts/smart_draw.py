#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCY 智能绘图工具
离线规则驱动：将简单文字描述或 scene 规范渲染为 PNG/JPEG 图片。
仅依赖 Pillow。

增强版特性：
- 更丰富的颜色/场景/对象识别
- 更智能的自然语言理解（规则驱动）
- 支持场景模板与简笔画组合
"""

from PIL import Image, ImageDraw
import argparse
import json
import os
import re
import sys

# 复用文本能力
sys.path.append(os.path.dirname(__file__))
from txt2img import _hex_to_rgb, render_text_image  # noqa


COLOR_MAP = {
    "red": "#ff4d4f", "红": "#ff4d4f", "红色": "#ff4d4f",
    "blue": "#1677ff", "蓝": "#1677ff", "蓝色": "#1677ff",
    "green": "#52c41a", "绿": "#52c41a", "绿色": "#52c41a",
    "yellow": "#fadb14", "黄": "#fadb14", "黄色": "#fadb14",
    "black": "#000000", "黑": "#000000", "黑色": "#000000",
    "white": "#ffffff", "白": "#ffffff", "白色": "#ffffff",
    "gray": "#8c8c8c", "grey": "#8c8c8c", "灰": "#8c8c8c", "灰色": "#8c8c8c",
    "orange": "#fa8c16", "橙": "#fa8c16", "橙色": "#fa8c16",
    "purple": "#722ed1", "紫": "#722ed1", "紫色": "#722ed1",
    "pink": "#eb2f96", "粉": "#eb2f96", "粉色": "#eb2f96",
    "brown": "#8b5a2b", "棕": "#8b5a2b", "棕色": "#8b5a2b", "咖啡色": "#8b5a2b",
    "cyan": "#13c2c2", "青": "#13c2c2", "青色": "#13c2c2",
    "gold": "#d4b106", "金": "#d4b106", "金色": "#d4b106",
    "silver": "#bfbfbf", "银": "#bfbfbf", "银色": "#bfbfbf",
    "beige": "#f5f5dc", "米色": "#f5f5dc",
}

COLOR_WORDS = sorted(COLOR_MAP.keys(), key=len, reverse=True)

ADJECTIVE_MAP = {
    "可爱": "cute", "萌": "cute", "卡通": "cartoon", "简笔画": "simple",
    "现代": "modern", "极简": "minimal", "温馨": "warm", "科技": "tech",
    "商务": "business", "明亮": "bright", "柔和": "soft"
}

SCENE_KEYWORDS = {
    "office": ["办公室", "办公", "office", "工位", "会议室"],
    "nature": ["自然", "森林", "草地", "公园", "户外", "风景"],
    "home": ["客厅", "卧室", "家里", "居家", "房间"],
    "sky": ["天空", "白云", "太阳", "sun", "cloud"],
}

OBJECT_KEYWORDS = {
    "cat": ["猫", "猫咪", "小猫", "cat", "kitty"],
    "dog": ["狗", "小狗", "dog", "puppy"],
    "house": ["房子", "小屋", "house", "home"],
    "tree": ["树", "大树", "tree"],
    "flower": ["花", "小花", "flower"],
    "sun": ["太阳", "sun"],
    "cloud": ["云", "白云", "cloud"],
    "mountain": ["山", "山峰", "mountain"],
    "desk": ["桌子", "办公桌", "书桌", "desk", "table"],
    "chair": ["椅子", "chair"],
    "computer": ["电脑", "显示器", "computer", "monitor", "笔记本"],
    "lamp": ["台灯", "灯", "lamp"],
    "book": ["书", "书本", "book"],
    "cup": ["杯子", "马克杯", "cup"],
    "person": ["人", "人物", "person", "man", "woman"],
    "car": ["汽车", "小车", "car"],
    "star": ["星星", "star"],
    "heart": ["爱心", "心形", "heart"],
    "circle": ["圆", "circle"],
    "rect": ["矩形", "长方形", "rect", "rectangle"],
    "line": ["线", "line"],
}


def normalize_color(value, default="#000000"):
    if not value:
        return default
    value = value.strip()
    if value.startswith("#"):
        return value
    return COLOR_MAP.get(value.lower(), COLOR_MAP.get(value, default))


def detect_format(output_path, fmt=None):
    if fmt:
        return fmt.upper()
    ext = os.path.splitext(output_path.lower())[1]
    if ext in [".jpg", ".jpeg"]:
        return "JPEG"
    return "PNG"


def _append_text_layer(image, layer, x, y, width, height):
    txt = render_text_image(
        text=layer.get("text", ""),
        font_size=int(layer.get("font_size", 24)),
        text_color=normalize_color(layer.get("color"), "#000000"),
        background_color="transparent",
        width=int(layer.get("w", width)),
        height=int(layer.get("h", height)),
        font_path=layer.get("font_path"),
        padding=int(layer.get("padding", 8)),
        align=layer.get("align", "center"),
        valign=layer.get("valign", "middle"),
        verbose=False,
    ).convert("RGBA")
    if image.mode == "RGBA":
        image.alpha_composite(txt, (x, y))
    else:
        image.paste(txt, (x, y), txt)


def draw_icon(draw, icon, box, fill="#cccccc", stroke="#222222", stroke_width=2):
    x, y, w, h = box
    fill_rgb = _hex_to_rgb(normalize_color(fill, "#cccccc"))
    stroke_rgb = _hex_to_rgb(normalize_color(stroke, "#222222"))

    if icon == "cat":
        draw.ellipse((x + w*0.2, y + h*0.25, x + w*0.8, y + h*0.85), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.polygon([(x + w*0.28, y + h*0.32), (x + w*0.40, y + h*0.08), (x + w*0.48, y + h*0.34)], fill=fill_rgb, outline=stroke_rgb)
        draw.polygon([(x + w*0.52, y + h*0.34), (x + w*0.60, y + h*0.08), (x + w*0.72, y + h*0.32)], fill=fill_rgb, outline=stroke_rgb)
        draw.ellipse((x + w*0.38, y + h*0.48, x + w*0.44, y + h*0.54), fill=stroke_rgb)
        draw.ellipse((x + w*0.56, y + h*0.48, x + w*0.62, y + h*0.54), fill=stroke_rgb)
        draw.polygon([(x + w*0.50, y + h*0.57), (x + w*0.46, y + h*0.62), (x + w*0.54, y + h*0.62)], fill="#ff85c0", outline=stroke_rgb)
        draw.line((x + w*0.46, y + h*0.62, x + w*0.40, y + h*0.66), fill=stroke_rgb, width=1)
        draw.line((x + w*0.54, y + h*0.62, x + w*0.60, y + h*0.66), fill=stroke_rgb, width=1)
        draw.arc((x + w*0.62, y + h*0.42, x + w*0.96, y + h*0.90), 200, 320, fill=stroke_rgb, width=stroke_width)
    elif icon == "dog":
        draw.ellipse((x + w*0.25, y + h*0.25, x + w*0.75, y + h*0.80), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.ellipse((x + w*0.15, y + h*0.30, x + w*0.32, y + h*0.58), fill=fill_rgb, outline=stroke_rgb)
        draw.ellipse((x + w*0.68, y + h*0.30, x + w*0.85, y + h*0.58), fill=fill_rgb, outline=stroke_rgb)
        draw.ellipse((x + w*0.40, y + h*0.48, x + w*0.46, y + h*0.54), fill=stroke_rgb)
        draw.ellipse((x + w*0.54, y + h*0.48, x + w*0.60, y + h*0.54), fill=stroke_rgb)
        draw.ellipse((x + w*0.46, y + h*0.58, x + w*0.54, y + h*0.66), fill="#000000")
    elif icon == "house":
        draw.rectangle((x + w*0.20, y + h*0.40, x + w*0.80, y + h*0.85), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.polygon([(x + w*0.16, y + h*0.42), (x + w*0.50, y + h*0.14), (x + w*0.84, y + h*0.42)], fill="#ff7875", outline=stroke_rgb)
        draw.rectangle((x + w*0.44, y + h*0.58, x + w*0.58, y + h*0.85), fill="#ffffff", outline=stroke_rgb)
    elif icon == "tree":
        draw.rectangle((x + w*0.44, y + h*0.55, x + w*0.56, y + h*0.88), fill="#8b5a2b", outline=stroke_rgb)
        draw.ellipse((x + w*0.22, y + h*0.20, x + w*0.78, y + h*0.65), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
    elif icon == "flower":
        for px, py in [(0.50,0.26),(0.34,0.40),(0.66,0.40),(0.40,0.58),(0.60,0.58)]:
            draw.ellipse((x + w*(px-0.10), y + h*(py-0.10), x + w*(px+0.10), y + h*(py+0.10)), fill=fill_rgb, outline=stroke_rgb)
        draw.ellipse((x + w*0.42, y + h*0.42, x + w*0.58, y + h*0.58), fill="#fadb14", outline=stroke_rgb)
        draw.line((x + w*0.50, y + h*0.58, x + w*0.50, y + h*0.92), fill="#389e0d", width=stroke_width)
    elif icon == "sun":
        draw.ellipse((x + w*0.30, y + h*0.30, x + w*0.70, y + h*0.70), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        for dx, dy in [(0.5,0.08),(0.5,0.92),(0.08,0.5),(0.92,0.5),(0.18,0.18),(0.82,0.18),(0.18,0.82),(0.82,0.82)]:
            draw.line((x + w*0.5, y + h*0.5, x + w*dx, y + h*dy), fill=stroke_rgb, width=stroke_width)
    elif icon == "cloud":
        draw.ellipse((x + w*0.20, y + h*0.42, x + w*0.48, y + h*0.72), fill=fill_rgb, outline=stroke_rgb)
        draw.ellipse((x + w*0.38, y + h*0.28, x + w*0.66, y + h*0.68), fill=fill_rgb, outline=stroke_rgb)
        draw.ellipse((x + w*0.56, y + h*0.40, x + w*0.84, y + h*0.72), fill=fill_rgb, outline=stroke_rgb)
        draw.rectangle((x + w*0.26, y + h*0.54, x + w*0.78, y + h*0.74), fill=fill_rgb, outline=fill_rgb)
    elif icon == "mountain":
        draw.polygon([(x + w*0.10, y + h*0.88), (x + w*0.38, y + h*0.24), (x + w*0.66, y + h*0.88)], fill=fill_rgb, outline=stroke_rgb)
        draw.polygon([(x + w*0.38, y + h*0.88), (x + w*0.66, y + h*0.36), (x + w*0.92, y + h*0.88)], fill="#b7eb8f", outline=stroke_rgb)
    elif icon == "desk":
        draw.rectangle((x + w*0.14, y + h*0.42, x + w*0.86, y + h*0.56), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.line((x + w*0.22, y + h*0.56, x + w*0.22, y + h*0.90), fill=stroke_rgb, width=stroke_width)
        draw.line((x + w*0.78, y + h*0.56, x + w*0.78, y + h*0.90), fill=stroke_rgb, width=stroke_width)
    elif icon == "chair":
        draw.rectangle((x + w*0.34, y + h*0.46, x + w*0.66, y + h*0.64), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.rectangle((x + w*0.30, y + h*0.22, x + w*0.66, y + h*0.46), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.line((x + w*0.38, y + h*0.64, x + w*0.34, y + h*0.92), fill=stroke_rgb, width=stroke_width)
        draw.line((x + w*0.62, y + h*0.64, x + w*0.66, y + h*0.92), fill=stroke_rgb, width=stroke_width)
    elif icon == "computer":
        draw.rectangle((x + w*0.18, y + h*0.18, x + w*0.82, y + h*0.62), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.rectangle((x + w*0.24, y + h*0.24, x + w*0.76, y + h*0.56), fill="#e6f4ff", outline=stroke_rgb)
        draw.line((x + w*0.50, y + h*0.62, x + w*0.50, y + h*0.78), fill=stroke_rgb, width=stroke_width)
        draw.rectangle((x + w*0.34, y + h*0.78, x + w*0.66, y + h*0.84), fill="#d9d9d9", outline=stroke_rgb)
    elif icon == "lamp":
        draw.line((x + w*0.50, y + h*0.26, x + w*0.50, y + h*0.74), fill=stroke_rgb, width=stroke_width)
        draw.polygon([(x + w*0.34, y + h*0.30), (x + w*0.66, y + h*0.30), (x + w*0.58, y + h*0.48), (x + w*0.42, y + h*0.48)], fill=fill_rgb, outline=stroke_rgb)
        draw.rectangle((x + w*0.40, y + h*0.74, x + w*0.60, y + h*0.82), fill="#d9d9d9", outline=stroke_rgb)
    elif icon == "book":
        draw.rectangle((x + w*0.28, y + h*0.20, x + w*0.72, y + h*0.84), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.line((x + w*0.50, y + h*0.20, x + w*0.50, y + h*0.84), fill=stroke_rgb, width=1)
    elif icon == "cup":
        draw.rectangle((x + w*0.34, y + h*0.34, x + w*0.66, y + h*0.74), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.arc((x + w*0.58, y + h*0.42, x + w*0.82, y + h*0.66), 270, 90, fill=stroke_rgb, width=stroke_width)
    elif icon == "person":
        draw.ellipse((x + w*0.38, y + h*0.10, x + w*0.62, y + h*0.32), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.line((x + w*0.50, y + h*0.32, x + w*0.50, y + h*0.70), fill=stroke_rgb, width=stroke_width)
        draw.line((x + w*0.32, y + h*0.44, x + w*0.68, y + h*0.44), fill=stroke_rgb, width=stroke_width)
        draw.line((x + w*0.50, y + h*0.70, x + w*0.36, y + h*0.92), fill=stroke_rgb, width=stroke_width)
        draw.line((x + w*0.50, y + h*0.70, x + w*0.64, y + h*0.92), fill=stroke_rgb, width=stroke_width)
    elif icon == "car":
        draw.rectangle((x + w*0.18, y + h*0.44, x + w*0.82, y + h*0.72), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)
        draw.polygon([(x + w*0.32, y + h*0.44), (x + w*0.44, y + h*0.28), (x + w*0.68, y + h*0.28), (x + w*0.78, y + h*0.44)], fill=fill_rgb, outline=stroke_rgb)
        draw.ellipse((x + w*0.26, y + h*0.64, x + w*0.40, y + h*0.82), fill="#333333")
        draw.ellipse((x + w*0.60, y + h*0.64, x + w*0.74, y + h*0.82), fill="#333333")
    elif icon == "star":
        pts = [(0.50,0.08),(0.60,0.38),(0.92,0.38),(0.66,0.56),(0.76,0.88),(0.50,0.68),(0.24,0.88),(0.34,0.56),(0.08,0.38),(0.40,0.38)]
        draw.polygon([(x + w*px, y + h*py) for px, py in pts], fill=fill_rgb, outline=stroke_rgb)
    elif icon == "heart":
        draw.polygon([(x + w*0.50, y + h*0.84), (x + w*0.18, y + h*0.48), (x + w*0.24, y + h*0.24), (x + w*0.42, y + h*0.18), (x + w*0.50, y + h*0.30), (x + w*0.58, y + h*0.18), (x + w*0.76, y + h*0.24), (x + w*0.82, y + h*0.48)], fill=fill_rgb, outline=stroke_rgb)
    else:
        draw.rectangle((x, y, x + w, y + h), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)


def render_scene(scene, output_path=None, format=None):
    canvas = scene.get("canvas", {})
    width = int(canvas.get("width", 800))
    height = int(canvas.get("height", 600))
    background = canvas.get("background", "#ffffff")
    mode = "RGBA" if str(background).lower() == "transparent" else "RGB"
    bg = (255, 255, 255, 0) if mode == "RGBA" else _hex_to_rgb(normalize_color(background, "#ffffff"))

    image = Image.new(mode, (width, height), bg)
    draw = ImageDraw.Draw(image)

    for layer in scene.get("layers", []):
        t = layer.get("type")
        fill = layer.get("fill")
        stroke = normalize_color(layer.get("stroke"), "#000000")
        stroke_width = int(layer.get("stroke_width", 1))
        fill_rgb = None if fill in [None, "none", "transparent"] else _hex_to_rgb(normalize_color(fill, "#000000"))
        stroke_rgb = _hex_to_rgb(stroke)

        if t == "point":
            x, y = int(layer.get("x", 0)), int(layer.get("y", 0))
            r = int(layer.get("radius", 2))
            draw.ellipse((x-r, y-r, x+r, y+r), fill=fill_rgb or stroke_rgb, outline=stroke_rgb, width=stroke_width)

        elif t == "line":
            x1, y1 = int(layer.get("x1", 0)), int(layer.get("y1", 0))
            x2, y2 = int(layer.get("x2", width)), int(layer.get("y2", height))
            draw.line((x1, y1, x2, y2), fill=stroke_rgb, width=stroke_width)

        elif t == "rect":
            x, y = int(layer.get("x", 0)), int(layer.get("y", 0))
            w, h = int(layer.get("w", 100)), int(layer.get("h", 100))
            draw.rectangle((x, y, x+w, y+h), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)

        elif t == "circle":
            cx, cy = int(layer.get("cx", width//2)), int(layer.get("cy", height//2))
            r = int(layer.get("r", 50))
            draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)

        elif t == "ellipse":
            x, y = int(layer.get("x", 0)), int(layer.get("y", 0))
            w, h = int(layer.get("w", 120)), int(layer.get("h", 80))
            draw.ellipse((x, y, x+w, y+h), fill=fill_rgb, outline=stroke_rgb, width=stroke_width)

        elif t == "polygon":
            points = [tuple(p) for p in layer.get("points", [])]
            if points:
                draw.polygon(points, fill=fill_rgb, outline=stroke_rgb)

        elif t == "text":
            x, y = int(layer.get("x", 0)), int(layer.get("y", 0))
            _append_text_layer(image, layer, x, y, width, height)

        elif t == "image":
            src = layer.get("path")
            if src and os.path.exists(src):
                overlay = Image.open(src).convert("RGBA")
                ow = layer.get("w")
                oh = layer.get("h")
                if ow and oh:
                    overlay = overlay.resize((int(ow), int(oh)))
                x, y = int(layer.get("x", 0)), int(layer.get("y", 0))
                image.alpha_composite(overlay, (x, y)) if image.mode == "RGBA" else image.paste(overlay, (x, y), overlay)

        elif t == "icon":
            box = (int(layer.get("x", 0)), int(layer.get("y", 0)), int(layer.get("w", 120)), int(layer.get("h", 120)))
            draw_icon(draw, layer.get("icon", "rect"), box, fill=layer.get("fill", "#cccccc"), stroke=layer.get("stroke", "#222222"), stroke_width=stroke_width)

    if not output_path:
        output_path = scene.get("output", {}).get("path", "output.png")
    fmt = detect_format(output_path, format or scene.get("output", {}).get("format"))

    if fmt == "JPEG":
        base = Image.new("RGB", image.size, (255, 255, 255))
        if image.mode == "RGBA":
            base.paste(image, mask=image.split()[-1])
        else:
            base.paste(image)
        base.save(output_path, format="JPEG")
    else:
        image.save(output_path, format="PNG")

    return output_path


def extract_colors(desc):
    found = []
    for word in COLOR_WORDS:
        if word.lower() in desc.lower() or word in desc:
            color = normalize_color(word)
            if color not in found:
                found.append(color)
    return found


def extract_styles(desc):
    tags = []
    for key, val in ADJECTIVE_MAP.items():
        if key in desc or key.lower() in desc.lower():
            tags.append(val)
    return tags


def detect_scene_type(desc):
    for scene_type, keywords in SCENE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in desc.lower() or kw in desc:
                return scene_type
    return None


def detect_objects(desc):
    result = []
    for name, keywords in OBJECT_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in desc.lower() or kw in desc:
                result.append(name)
                break
    return result


def add_background_scene(scene, scene_type, width, height):
    if scene_type == "office":
        scene["canvas"]["background"] = "#f7f8fa"
        scene["layers"].append({"type": "rect", "x": 0, "y": int(height*0.78), "w": width, "h": int(height*0.22), "fill": "#d9d9d9", "stroke": "#d9d9d9"})
        scene["layers"].append({"type": "line", "x1": 0, "y1": int(height*0.30), "x2": width, "y2": int(height*0.30), "stroke": "#e5e6eb", "stroke_width": 2})
    elif scene_type == "nature":
        scene["canvas"]["background"] = "#e6f7ff"
        scene["layers"].append({"type": "rect", "x": 0, "y": int(height*0.72), "w": width, "h": int(height*0.28), "fill": "#b7eb8f", "stroke": "#b7eb8f"})
    elif scene_type == "home":
        scene["canvas"]["background"] = "#fff7e6"
        scene["layers"].append({"type": "rect", "x": 0, "y": int(height*0.74), "w": width, "h": int(height*0.26), "fill": "#d6b588", "stroke": "#d6b588"})
    elif scene_type == "sky":
        scene["canvas"]["background"] = "#bae7ff"


def add_object_layers(scene, objects, width, height, styles, colors):
    icon_objects = [obj for obj in objects if obj not in {"circle", "rect", "line"}]
    palette = colors or ["#1677ff", "#52c41a", "#fa8c16", "#eb2f96"]

    if icon_objects:
        if len(icon_objects) == 1 and icon_objects[0] in {"cat", "dog", "person", "tree", "flower", "house", "car"}:
            obj = icon_objects[0]
            fill = palette[0]
            if obj == "cat" and "cute" in styles:
                fill = "#ffd6e7"
            scene["layers"].append({"type": "icon", "icon": obj, "x": int(width*0.22), "y": int(height*0.16), "w": int(width*0.56), "h": int(height*0.62), "fill": fill, "stroke": "#222222", "stroke_width": 3})
            return

        cols = min(3, max(1, len(icon_objects)))
        cell_w = width // cols
        rows = (len(icon_objects) + cols - 1) // cols
        cell_h = max(140, int(height * 0.56 / max(1, rows)))
        base_y = int(height * 0.18)
        for i, obj in enumerate(icon_objects):
            row = i // cols
            col = i % cols
            box_w = int(cell_w * 0.58)
            box_h = int(cell_h * 0.58)
            x = col * cell_w + (cell_w - box_w) // 2
            y = base_y + row * cell_h
            scene["layers"].append({"type": "icon", "icon": obj, "x": x, "y": y, "w": box_w, "h": box_h, "fill": palette[i % len(palette)], "stroke": "#222222", "stroke_width": 2})

    if "circle" in objects:
        scene["layers"].append({"type": "circle", "cx": width//2, "cy": height//2, "r": min(width, height)//6, "fill": palette[0], "stroke": "#222222", "stroke_width": 2})
    if "rect" in objects:
        scene["layers"].append({"type": "rect", "x": width//6, "y": height//5, "w": width//3, "h": height//4, "fill": palette[min(1, len(palette)-1)], "stroke": "#222222", "stroke_width": 2})
    if "line" in objects:
        scene["layers"].append({"type": "line", "x1": 60, "y1": height-80, "x2": width-60, "y2": 80, "stroke": palette[min(2, len(palette)-1)], "stroke_width": 4})


def parse_description(description, width=800, height=600, background="#ffffff"):
    desc = description.strip()
    scene = {
        "canvas": {"width": width, "height": height, "background": background},
        "layers": [],
        "output": {"path": "output.png", "format": "PNG"}
    }

    lower_desc = desc.lower()
    colors = extract_colors(desc)
    styles = extract_styles(desc)
    scene_type = detect_scene_type(desc)
    objects = detect_objects(desc)

    for key in COLOR_MAP.keys():
        if f"背景{key}" in desc or f"background {key}" in lower_desc:
            scene["canvas"]["background"] = normalize_color(key, background)
            break

    if scene_type:
        add_background_scene(scene, scene_type, width, height)

    add_object_layers(scene, objects, width, height, styles, colors)

    if scene_type == "office":
        existing = {layer.get("icon") for layer in scene["layers"] if layer.get("type") == "icon"}
        if "desk" not in existing:
            scene["layers"].append({"type": "icon", "icon": "desk", "x": int(width*0.16), "y": int(height*0.48), "w": int(width*0.32), "h": int(height*0.32), "fill": "#d6b588", "stroke": "#222222", "stroke_width": 2})
        if "computer" not in existing:
            scene["layers"].append({"type": "icon", "icon": "computer", "x": int(width*0.26), "y": int(height*0.36), "w": int(width*0.20), "h": int(height*0.20), "fill": "#d9d9d9", "stroke": "#222222", "stroke_width": 2})
        if "chair" not in existing:
            scene["layers"].append({"type": "icon", "icon": "chair", "x": int(width*0.52), "y": int(height*0.50), "w": int(width*0.16), "h": int(height*0.26), "fill": "#91caff", "stroke": "#222222", "stroke_width": 2})
        if "lamp" in objects:
            scene["layers"].append({"type": "icon", "icon": "lamp", "x": int(width*0.10), "y": int(height*0.32), "w": int(width*0.14), "h": int(height*0.28), "fill": "#ffe58f", "stroke": "#222222", "stroke_width": 2})
        if "cup" in objects:
            scene["layers"].append({"type": "icon", "icon": "cup", "x": int(width*0.38), "y": int(height*0.48), "w": int(width*0.08), "h": int(height*0.16), "fill": "#ffffff", "stroke": "#222222", "stroke_width": 2})

    if scene_type == "nature" or any(obj in objects for obj in ["sun", "cloud", "mountain", "tree", "flower"]):
        existing = {layer.get("icon") for layer in scene["layers"] if layer.get("type") == "icon"}
        if "sun" in objects or scene_type == "nature":
            if "sun" not in existing:
                scene["layers"].append({"type": "icon", "icon": "sun", "x": int(width*0.06), "y": int(height*0.05), "w": int(width*0.14), "h": int(height*0.18), "fill": "#fadb14", "stroke": "#d48806", "stroke_width": 2})
        if "cloud" in objects or scene_type == "nature":
            scene["layers"].append({"type": "icon", "icon": "cloud", "x": int(width*0.68), "y": int(height*0.08), "w": int(width*0.18), "h": int(height*0.14), "fill": "#ffffff", "stroke": "#91d5ff", "stroke_width": 2})
        if "mountain" in objects:
            scene["layers"].append({"type": "icon", "icon": "mountain", "x": int(width*0.50), "y": int(height*0.30), "w": int(width*0.34), "h": int(height*0.34), "fill": "#95de64", "stroke": "#389e0d", "stroke_width": 2})

    text_match = re.search(r"写上[：:\s]*(.+)$", desc) or re.search(r"文字[：:\s]*(.+)$", desc)
    if not text_match:
        text_match = re.search(r"[\"“](.+?)[\"”]", desc)
    if text_match:
        scene["layers"].append({
            "type": "text", "text": text_match.group(1).strip(),
            "x": 40, "y": height - 160, "w": width - 80, "h": 120,
            "font_size": 32, "color": "#111111"
        })

    if not scene["layers"]:
        scene["layers"].append({
            "type": "text", "text": desc,
            "x": 40, "y": 40, "w": width - 80, "h": height - 80,
            "font_size": 28, "color": "#111111"
        })

    return scene


def smart_draw(description, output_path, width=800, height=600, background="#ffffff", format=None):
    scene = parse_description(description, width=width, height=height, background=background)
    scene["output"]["path"] = output_path
    scene["output"]["format"] = detect_format(output_path, format)
    return render_scene(scene, output_path=output_path, format=format)


def load_scene_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="本地离线智能绘图 / scene 渲染工具")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt", "-p", help="自然语言绘图描述")
    source.add_argument("--scene", "-s", help="scene JSON 文件路径")
    parser.add_argument("--out", "-o", required=True, help="输出图片路径，如 out.png / out.jpg")
    parser.add_argument("--width", type=int, default=800, help="画布宽度，prompt 模式有效")
    parser.add_argument("--height", type=int, default=600, help="画布高度，prompt 模式有效")
    parser.add_argument("--background", default="#ffffff", help="背景色，prompt 模式有效")
    parser.add_argument("--format", choices=["PNG", "JPEG", "JPG", "png", "jpeg", "jpg"], help="输出格式，不传则按扩展名判断")
    parser.add_argument("--print-scene", action="store_true", help="prompt 模式下同时打印解析出的 scene JSON")
    args = parser.parse_args()

    if args.scene:
        scene = load_scene_file(args.scene)
        scene.setdefault("output", {})["path"] = args.out
        if args.format:
            scene["output"]["format"] = detect_format(args.out, args.format)
        out = render_scene(scene, output_path=args.out, format=args.format)
    else:
        scene = parse_description(args.prompt, width=args.width, height=args.height, background=args.background)
        scene["output"]["path"] = args.out
        scene["output"]["format"] = detect_format(args.out, args.format)
        out = render_scene(scene, output_path=args.out, format=args.format)
        if args.print_scene:
            print(json.dumps(scene, ensure_ascii=False, indent=2))

    status = f"图片已保存至: {out}"
    print(status, file=sys.stderr if args.print_scene else sys.stdout)


if __name__ == "__main__":
    main()
