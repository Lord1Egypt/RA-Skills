#!/usr/bin/env python3
"""图片水印工具 - 文字/图片水印，支持批量"""
import sys
import os
import json
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    print("❌ 缺少 Pillow，请运行: pip3 install Pillow")
    sys.exit(1)

POSITIONS = {
    "top-left":     (0.05, 0.05),
    "top-center":   (0.5,  0.05),
    "top-right":    (0.90, 0.05),
    "center-left":  (0.05, 0.5),
    "center":       (0.5,  0.5),
    "center-right": (0.90, 0.5),
    "bottom-left":  (0.05, 0.90),
    "bottom-center":(0.5,  0.90),
    "bottom-right": (0.90, 0.90),
}

def get_font(size=20):
    """获取中文字体，优先系统字体"""
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STSong.ttf",
        "/System/Library/Fonts/Arial Unicode.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

def add_text_watermark(input_path, output_path, text, position="bottom-right",
                       opacity=60, font_size=20, color=(255,255,255)):
    """添加文字水印"""
    try:
        img = Image.open(input_path).convert("RGBA")
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        font = get_font(font_size)
        # 计算文字尺寸
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # 文字位置
        rx, ry = POSITIONS.get(position, (0.90, 0.90))
        margin = 20
        x = int(img.width * rx - tw - margin if "right" in position else
                img.width * rx - tw // 2 if "center" in position else margin)
        y = int(img.height * ry - th - margin if "bottom" in position else
                img.height * ry - th // 2 if "center" in position else margin)

        alpha = int(255 * opacity / 100)
        text_color = color + (alpha,)
        draw.text((x, y), text, fill=text_color, font=font)

        watermarked = Image.alpha_composite(img, overlay)
        final = watermarked.convert("RGB")
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        final.save(output_path, "JPEG", quality=95)
        return True
    except Exception as e:
        print(f"❌ 处理失败: {e}", file=sys.stderr)
        return False

def add_image_watermark(input_path, output_path, logo_path, position="bottom-right", opacity=60):
    """添加图片水印（Logo）"""
    try:
        img = Image.open(input_path).convert("RGBA")
        logo = Image.open(logo_path).convert("RGBA")

        # 缩放Logo为原图的10%
        ratio = 0.10
        new_w = int(img.width * ratio)
        new_h = int(logo.height * (new_w / logo.width))
        logo = logo.resize((new_w, new_h), Image.LANCZOS)

        # 透明度
        if opacity < 100:
            enhancer = ImageEnhance.Brightness(logo)
            logo = enhancer.enhance(opacity / 100)

        rx, ry = POSITIONS.get(position, (0.90, 0.90))
        x = int(img.width * rx - new_w - 20)
        y = int(img.height * ry - new_h - 20)

        # 创建透明画布，贴Logo
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        layer.paste(logo, (x, y), logo)
        watermarked = Image.alpha_composite(img, layer).convert("RGB")
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        watermarked.save(output_path, "JPEG", quality=95)
        return True
    except Exception as e:
        print(f"❌ 处理失败: {e}", file=sys.stderr)
        return False

def batch_process(input_dir, output_dir, text=None, logo_path=None,
                  position="bottom-right", opacity=60):
    """批量处理"""
    os.makedirs(output_dir, exist_ok=True)
    exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    results = []
    for fp in Path(input_dir).rglob("*"):
        if fp.suffix.lower() in exts:
            out = os.path.join(output_dir, fp.name)
            ok = False
            if text:
                ok = add_text_watermark(str(fp), out, text, position, opacity)
            elif logo_path:
                ok = add_image_watermark(str(fp), out, logo_path, position, opacity)
            results.append({"file": str(fp), "output": out, "status": "ok" if ok else "failed"})
    return results

def main():
    p = argparse.ArgumentParser(description="图片水印工具")
    sub = p.add_subparsers(dest="cmd", required=True)

    # text subcommand
    t = sub.add_parser("text", help="文字水印")
    t.add_argument("input", help="输入图片")
    t.add_argument("text", help="水印文字")
    t.add_argument("--output", "-o", help="输出路径（默认添加_watermarked后缀）")
    t.add_argument("--position", default="bottom-right",
                   choices=list(POSITIONS.keys()), help="位置")
    t.add_argument("--opacity", type=int, default=60, help="透明度0-100")
    t.add_argument("--font-size", type=int, default=20, help="字体大小")
    t.add_argument("--color", default="255,255,255", help="颜色RGB")

    # image subcommand
    i = sub.add_parser("image", help="图片水印")
    i.add_argument("input", help="输入图片")
    i.add_argument("logo", help="水印图片（Logo）")
    i.add_argument("--output", "-o")
    i.add_argument("--position", default="bottom-right", choices=list(POSITIONS.keys()))
    i.add_argument("--opacity", type=int, default=60)

    # batch subcommand
    b = sub.add_parser("batch", help="批量处理")
    b.add_argument("input_dir", help="输入文件夹")
    b.add_argument("output_dir", help="输出文件夹")
    b.add_argument("--text", help="文字水印")
    b.add_argument("--logo", help="Logo水印")
    b.add_argument("--position", default="bottom-right", choices=list(POSITIONS.keys()))
    b.add_argument("--opacity", type=int, default=60)

    args = p.parse_args()

    def get_output(input_path, user_output):
        if user_output:
            return user_output
        p = Path(input_path)
        return str(p.parent / f"{p.stem}_watermarked{p.suffix}")

    result = None
    if args.cmd == "text":
        color = tuple(int(x) for x in args.color.split(","))
        out = get_output(args.input, args.output)
        ok = add_text_watermark(args.input, out, args.text, args.position,
                                args.opacity, args.font_size, color)
        result = {"cmd": "text", "input": args.input, "output": out,
                  "text": args.text, "position": args.position,
                  "status": "ok" if ok else "failed"}
    elif args.cmd == "image":
        out = get_output(args.input, args.output)
        ok = add_image_watermark(args.input, out, args.logo, args.position, args.opacity)
        result = {"cmd": "image", "input": args.input, "output": out,
                  "logo": args.logo, "position": args.position, "status": "ok" if ok else "failed"}
    elif args.cmd == "batch":
        logo = args.logo if hasattr(args, "logo") and args.logo else None
        results = batch_process(args.input_dir, args.output_dir,
                                args.text, logo, args.position, args.opacity)
        result = {"cmd": "batch", "total": len(results), "details": results}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] == "ok" else 1)

if __name__ == "__main__":
    main()
