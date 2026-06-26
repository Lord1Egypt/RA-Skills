#!/usr/bin/env python3
"""
overlay.py
使用 Pillow 将文案叠加到生成图片上。
支持：主标题、副标题，左/右/居中对齐，白色+阴影 或 深色文字。

用法：
  python3 overlay.py \
    --input-dir ./output/raw/ \
    --product '{"selling_points": [...], "product_name_zh": "..."}' \
    --lang en \
    --output-dir ./output/final/

依赖：pip install Pillow
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    print("请先安装 Pillow：pip install Pillow", file=sys.stderr)
    sys.exit(1)


# ── Helper: get selling point field ────────────────────────────────────────

def _sp(sp, i, field, lang):
    """Get selling point field, supporting both our doc format and py-version format.
    Our docs: en_title/zh_title/en_desc/zh_desc
    Py-version: en/zh (title only)
    """
    try:
        pt = sp[i]
    except IndexError:
        return ""
    prefix = "zh" if lang == "zh" else "en"
    # Try our doc format first, then fallback
    return pt.get(f"{prefix}_{field}", pt.get(prefix, pt.get(f"{prefix}_title", "")))


# ── Text overlay definitions ───────────────────────────────────────────────
# Overlay configs per image-types.md & providers.md Canvas规范
# Each returns a list of text items with: tx, x, y, fs, w, c, a, shadow

OVERLAY_CONFIGS = {
    "white_bg": None,   # 无文案叠加
    "model": None,      # 无文案叠加
    "key_features": lambda sp, lang: [
        {"tx": "为什么选择我们" if lang == "zh" else "WHY CHOOSE US",
         "x": .53, "y": .115, "fs": .031, "w": "bold", "c": "#1a1a1a", "a": "left"},
        {"tx": _sp(sp, 0, "title", lang),
         "x": .60, "y": .375, "fs": .021, "w": "regular", "c": "#333333", "a": "left"},
        {"tx": _sp(sp, 1, "title", lang),
         "x": .60, "y": .565, "fs": .021, "w": "regular", "c": "#333333", "a": "left"},
        {"tx": _sp(sp, 2, "title", lang),
         "x": .60, "y": .755, "fs": .021, "w": "regular", "c": "#333333", "a": "left"},
    ],
    "selling_pt": lambda sp, lang: [
        {"tx": _sp(sp, 1, "title", lang) or ("宽松版型设计" if lang == "zh" else "LOOSE FIT DESIGN"),
         "x": .06 if lang == "zh" else .05, "y": .095,
         "fs": .036 if lang == "zh" else .033, "w": "bold", "c": "#1a1a1a", "a": "left"},
        {"tx": _sp(sp, 1, "desc", lang) or ("活动自如无束缚" if lang == "zh" else "Unrestricted Movement"),
         "x": .06 if lang == "zh" else .05, "y": .888,
         "fs": .022, "w": "regular", "c": "#444444", "a": "left"},
        {"tx": _sp(sp, 2, "desc", lang) or ("显瘦舒适两不误" if lang == "zh" else "Comfortable and Flattering"),
         "x": .06 if lang == "zh" else .05, "y": .944,
         "fs": .022, "w": "regular", "c": "#444444", "a": "left"},
    ],
    "material": lambda sp, lang: [
        {"tx": _sp(sp, 0, "title", lang) or ("优质精梳棉" if lang == "zh" else "PREMIUM COMBED COTTON"),
         "x": .95, "y": .095,
         "fs": .034 if lang == "zh" else .027, "w": "bold", "c": "#1a1a1a", "a": "right"},
        {"tx": _sp(sp, 0, "desc", lang) or ("亲肤柔软不刺激" if lang == "zh" else "Soft and Skin-friendly"),
         "x": .95, "y": .500,
         "fs": .022, "w": "regular", "c": "#444444", "a": "right"},
        {"tx": _sp(sp, 2, "desc", lang) or ("干爽透气，全天舒适" if lang == "zh" else "Keep Dry and Breathable"),
         "x": .95, "y": .920,
         "fs": .022, "w": "regular", "c": "#444444", "a": "right"},
    ],
    "lifestyle": lambda sp, lang: [
        {"tx": "日常减龄穿搭" if lang == "zh" else "CASUAL EVERYDAY STYLE",
         "x": .05, "y": .095,
         "fs": .036 if lang == "zh" else .029, "w": "bold", "c": "#ffffff", "a": "left", "shadow": True},
        {"tx": "校园首选" if lang == "zh" else "Perfect for School",
         "x": .05, "y": .888,
         "fs": .022, "w": "regular", "c": "#ffffff", "a": "left", "shadow": True},
        {"tx": "百搭轻松" if lang == "zh" else "Easy to Match",
         "x": .05, "y": .944,
         "fs": .022, "w": "regular", "c": "#ffffff", "a": "left", "shadow": True},
    ],
    "multi_scene": lambda sp, lang: [
        {"tx": "一件多穿，随心切换" if lang == "zh" else "VERSATILE FOR ANY OCCASION",
         "x": .50, "y": .065,
         "fs": .029 if lang == "zh" else .025, "w": "bold", "c": "#ffffff", "a": "center", "shadow": True},
        {"tx": "居家慵懒风" if lang == "zh" else "Home Lounging",
         "x": .25, "y": .945,
         "fs": .022, "w": "regular", "c": "#ffffff", "a": "center", "shadow": True},
        {"tx": "出游活力风" if lang == "zh" else "Outdoor Outings",
         "x": .75, "y": .945,
         "fs": .022, "w": "regular", "c": "#ffffff", "a": "center", "shadow": True},
    ],
}


def get_font(size: int, bold: bool) -> ImageFont.ImageFont:
    """尝试加载系统字体，降级到默认字体"""
    font_candidates = (
        # macOS
        ["/System/Library/Fonts/HelveticaNeue.ttc",
         "/System/Library/Fonts/PingFang.ttc"]
        if sys.platform == "darwin" else
        # Linux
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
         "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"]
        if sys.platform == "linux" else
        # Windows
        ["C:/Windows/Fonts/Arial.ttf",
         "C:/Windows/Fonts/msyh.ttc"]
    )
    for path in font_candidates:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    # Absolute fallback
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def apply_shadow(draw: ImageDraw.ImageDraw, pos, text: str, font, color: str):
    """绘制文字阴影"""
    sx, sy = pos
    shadow_color = (0, 0, 0, 160)
    for dx, dy in [(-1,-1),(1,-1),(-1,1),(1,1),(0,2),(2,0)]:
        draw.text((sx+dx, sy+dy), text, font=font, fill=shadow_color)


def hex_to_rgba(hex_color: str, alpha: int = 255):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return (r, g, b, alpha)


def overlay_image(input_path: Path, output_path: Path, items: list):
    img = Image.open(input_path).convert("RGBA")
    W, H = img.size
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for item in items:
        fs = max(12, int(item["fs"] * W))
        font = get_font(fs, bold=(item.get("w") == "bold"))
        color = hex_to_rgba(item["c"])
        align = item.get("a", "left")
        use_shadow = item.get("shadow", False)

        text = item["tx"]
        if not text:
            continue

        # Calculate x position based on alignment
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
        except AttributeError:
            tw = draw.textsize(text, font=font)[0]  # older Pillow

        raw_x = item["x"] * W
        if align == "right":
            px = raw_x - tw
        elif align == "center":
            px = raw_x - tw / 2
        else:
            px = raw_x

        py = item["y"] * H

        if use_shadow:
            apply_shadow(draw, (px, py), text, font, item["c"])

        draw.text((px, py), text, font=font, fill=color)

    result = Image.alpha_composite(img, overlay).convert("RGB")
    result.save(output_path, "JPEG", quality=93)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="电商套图文案叠加脚本")
    parser.add_argument("--input-dir",  default="./output/raw/")
    parser.add_argument("--product",    required=True, help="商品 JSON 字符串")
    parser.add_argument("--lang",       default="en", choices=["en", "zh"])
    parser.add_argument("--output-dir", default="./output/final/")
    args = parser.parse_args()

    product = json.loads(args.product)
    sp = product.get("selling_points", [])
    lang = args.lang

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for type_id, config_fn in OVERLAY_CONFIGS.items():
        raw_path = input_dir / f"{type_id}_raw.jpg"
        if not raw_path.exists():
            continue

        out_path = output_dir / f"{type_id}.jpg"
        try:
            if config_fn is None:
                # No overlay needed — just copy
                import shutil
                shutil.copy2(raw_path, out_path)
                print(f"  ⬜ [{type_id}] 无文案叠加，直接复制 → {out_path}")
            else:
                items = config_fn(sp, lang)
                overlay_image(raw_path, out_path, items)
                print(f"  ✅ [{type_id}] 文案叠加完成 → {out_path}")
            results[type_id] = {"status": "ok", "path": str(out_path)}
        except Exception as e:
            print(f"  ❌ [{type_id}] 失败: {e}", file=sys.stderr)
            results[type_id] = {"status": "error", "error": str(e)}

    summary_path = output_dir / "overlay_result.json"
    with open(summary_path, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    ok = [k for k,v in results.items() if v["status"]=="ok"]
    print(f"\n✅ 叠加完成 {len(ok)} 张，最终图片保存于 {output_dir}")


if __name__ == "__main__":
    main()
