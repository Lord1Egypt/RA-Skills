#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
舞台服装设计板通用拼合脚本（costume-design-board skill）
基于关盼盼 V9.1 验证版参数。

用法：
    python build_design_board.py \
        --src <源图目录> \
        --out <输出目录> \
        --character <角色名> \
        --version <版本号> \
        --project <项目名称> \
        --role <角色定位> \
        --color <主色调> \
        --fabric <主要面料>

源图目录中每个文件按前缀自动匹配：
    front* / 01_*   -> 正面全身
    back* / 02_*    -> 背面全身
    side* / 03_*    -> 侧面全身
    chest* / 04_*   -> 胸口特写
    back_opening* / 05_* -> 背部开口特写
    sleeve* / 06_*  -> 广袖特写
    waist* / 07_*   -> 腰封特写
    skirt* / 08_*   -> 裙摆特写
    hair* / 09_*    -> 头饰特写
"""

from PIL import Image, ImageDraw, ImageFont
import os
import argparse

# ==================== 默认配置 ====================
MARGIN = 80
HEADER_HEIGHT = 280
FOOTER_HEIGHT = 260
SECTION_GAP = 90
FB_GAP = 44
DETAIL_GAP = 28
INFO_PANEL_HEIGHT = 260
INFO_TO_GRID_GAP = 40
FULL_BODY_TARGET_HEIGHT = 2400

BG_COLOR = (12, 12, 12)
DARK_PANEL = (32, 32, 32)
TEXT_WHITE = (255, 255, 255)
TEXT_GRAY = (190, 190, 190)
TEXT_GOLD = (210, 175, 120)
LINE_COLOR = (60, 60, 60)

TITLE_FONT_SIZE = 76
SUBTITLE_FONT_SIZE = 34
LABEL_FONT_SIZE = 28
INFO_TITLE_FONT_SIZE = 28
INFO_BODY_FONT_SIZE = 24
CAPTION_FONT_SIZE = 22

DEFAULT_LABELS = {
    "front": ("01", "正面全身"),
    "back": ("02", "背面全身"),
    "side": ("03", "侧面全身"),
    "chest": ("04", "胸口镂空"),
    "back_opening": ("05", "背部开口"),
    "sleeve": ("06", "广袖细节"),
    "waist": ("07", "腰封刺绣"),
    "skirt": ("08", "裙摆衬裙"),
    "hair": ("09", "高髻头饰"),
}


def get_font(size, bold=False):
    """按系统平台自动回退中文字体。"""
    candidates = []
    if os.name == "nt":
        if bold:
            candidates = [r"C:\Windows\Fonts\msyhbd.ttc"]
        candidates += [
            r"C:\Windows\Fonts\simhei.ttf",
            r"C:\Windows\Fonts\msyh.ttc",
            r"C:\Windows\Fonts\simsun.ttc",
        ]
    else:
        # macOS / Linux 常见中文字体
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def find_file(src_dir, prefix):
    """按语义前缀、数字前缀或中文关键词匹配文件。"""
    num_prefix = DEFAULT_LABELS[prefix][0] + "_"
    # 中文关键词回退
    keyword_map = {
        "front": ["正面全身", "正面"],
        "back": ["背面全身", "背面"],
        "side": ["侧面全身", "侧面"],
        "chest": ["胸口"],
        "back_opening": ["背部", "泪滴形", "背部开口"],
        "sleeve": ["广袖"],
        "waist": ["腰封"],
        "skirt": ["裙摆"],
        "hair": ["高髻", "头饰", "发簪"],
    }
    keywords = [prefix] + keyword_map.get(prefix, [])

    for name in sorted(os.listdir(src_dir)):
        low = name.lower()
        if low.endswith((".png", ".jpg", ".jpeg", ".webp")):
            if name.startswith(prefix) or name.startswith(num_prefix):
                return os.path.join(src_dir, name)
            for kw in keywords:
                if kw in name:
                    return os.path.join(src_dir, name)
    raise FileNotFoundError(f"找不到前缀匹配的文件: {prefix} (尝试 {prefix}* 或 {num_prefix}* 或中文关键词)")


def load_and_fit(path, target_size, bg=BG_COLOR, resample=Image.LANCZOS):
    """保持比例缩放并粘贴到目标框中，不裁切、不变形。"""
    img = Image.open(path).convert("RGB")
    tw, th = target_size
    iw, ih = img.size
    scale = min(tw / iw, th / ih)
    new_w = max(1, int(iw * scale))
    new_h = max(1, int(ih * scale))
    resized = img.resize((new_w, new_h), resample)
    canvas = Image.new("RGB", target_size, bg)
    x = (tw - new_w) // 2
    y = (th - new_h) // 2
    canvas.paste(resized, (x, y))
    return canvas


def draw_label_on_image(canvas, x, y, num, desc, font_num, font_desc, offset=10):
    """在图片左上角绘制带半透明背景的编号+描述标签。"""
    draw_tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bbox_num = draw_tmp.textbbox((0, 0), num, font=font_num)
    bbox_desc = draw_tmp.textbbox((0, 0), desc, font=font_desc)
    num_w = bbox_num[2] - bbox_num[0]
    num_h = bbox_num[3] - bbox_num[1]
    desc_w = bbox_desc[2] - bbox_desc[0]
    desc_h = bbox_desc[3] - bbox_desc[1]
    pad = 10
    total_w = num_w + desc_w + 3 * pad + 6
    total_h = max(num_h, desc_h) + 2 * pad + 4

    overlay = Image.new("RGBA", (total_w, total_h), (22, 22, 22, 215))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.text((pad, (total_h - num_h) // 2 - 2), num, fill=TEXT_GOLD, font=font_num)
    overlay_draw.text((pad + num_w + 6, (total_h - desc_h) // 2 - 2), desc, fill=TEXT_GRAY, font=font_desc)

    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.paste(overlay, (x + offset, y + offset), overlay)
    canvas.paste(canvas_rgba.convert("RGB"), (0, 0))


def build_board(
    src_dir,
    out_dir,
    character,
    version="1.0",
    project="",
    role_position="",
    color_scheme="",
    fabric="",
    design_notes=None,
):
    os.makedirs(out_dir, exist_ok=True)

    with Image.open(find_file(src_dir, "front")) as im:
        fb_w0, fb_h0 = im.size
    fb_ratio = fb_w0 / fb_h0

    full_body_height = FULL_BODY_TARGET_HEIGHT
    full_body_width = int(full_body_height * fb_ratio)
    left_width = 3 * full_body_width + 2 * FB_GAP

    grid_height = full_body_height - INFO_PANEL_HEIGHT - INFO_TO_GRID_GAP
    S = (grid_height - 2 * DETAIL_GAP) // 3
    right_width = 2 * S + DETAIL_GAP

    canvas_width = MARGIN + left_width + SECTION_GAP + right_width + MARGIN
    canvas_height = HEADER_HEIGHT + MARGIN + full_body_height + MARGIN + FOOTER_HEIGHT

    print(f"画布尺寸: {canvas_width} x {canvas_height}")
    print(f"全身图: {full_body_width} x {full_body_height}")
    print(f"特写: {S} x {S}, 2x3")

    canvas = Image.new("RGB", (canvas_width, canvas_height), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    font_title = get_font(TITLE_FONT_SIZE, bold=True)
    font_subtitle = get_font(SUBTITLE_FONT_SIZE)
    font_label = get_font(LABEL_FONT_SIZE, bold=True)
    font_label_desc = get_font(LABEL_FONT_SIZE)
    font_info_title = get_font(INFO_TITLE_FONT_SIZE, bold=True)
    font_info_body = get_font(INFO_BODY_FONT_SIZE)
    font_caption = get_font(CAPTION_FONT_SIZE)

    # 顶部标题
    title = f"{character} 服装设计参考板"
    draw.text((MARGIN, 50), title, fill=TEXT_WHITE, font=font_title)
    bbox = draw.textbbox((MARGIN, 50), title, font=font_title)
    draw.text((bbox[2] + 30, 66), version, fill=TEXT_GOLD, font=font_subtitle)
    subtitle_text = f"{project} · {role_position} · {color_scheme} · {fabric}".strip(" ·")
    draw.text((MARGIN, 160), subtitle_text, fill=TEXT_GRAY, font=font_caption)
    draw.line([(MARGIN, 240), (canvas_width - MARGIN, 240)], fill=LINE_COLOR, width=2)

    content_top = HEADER_HEIGHT + MARGIN

    # 左侧全身图
    full_body_keys = ["front", "back", "side"]
    for i, key in enumerate(full_body_keys):
        path = find_file(src_dir, key)
        x = MARGIN + i * (full_body_width + FB_GAP)
        y = content_top
        fitted = load_and_fit(path, (full_body_width, full_body_height))
        canvas.paste(fitted, (x, y))
        num, desc = DEFAULT_LABELS[key]
        draw_label_on_image(canvas, x, y, num, desc, font_label, font_label_desc)

    # 右侧信息面板 + 特写网格
    right_x = MARGIN + left_width + SECTION_GAP
    right_y = content_top

    draw.rectangle(
        (right_x, right_y, right_x + right_width, right_y + INFO_PANEL_HEIGHT),
        fill=DARK_PANEL
    )
    info_x = right_x + 26
    info_y = right_y + 20
    draw.text((info_x, info_y), "角色定位", fill=TEXT_GOLD, font=font_info_title)
    draw.text((info_x, info_y + 40), role_position, fill=TEXT_GRAY, font=font_info_body)

    col2_x = info_x + max(30, right_width // 2 - 4)
    info_y2 = info_y + 130
    draw.text((info_x, info_y2), "主色调", fill=TEXT_GOLD, font=font_info_title)
    draw.text((info_x, info_y2 + 40), color_scheme, fill=TEXT_GRAY, font=font_info_body)
    draw.text((col2_x, info_y2), "主要面料", fill=TEXT_GOLD, font=font_info_title)
    draw.text((col2_x, info_y2 + 40), fabric, fill=TEXT_GRAY, font=font_info_body)

    detail_keys = ["chest", "back_opening", "sleeve", "waist", "skirt", "hair"]
    grid_start_y = right_y + INFO_PANEL_HEIGHT + INFO_TO_GRID_GAP
    grid_total_w = 2 * S + DETAIL_GAP
    grid_x = right_x + (right_width - grid_total_w) // 2

    for i, key in enumerate(detail_keys):
        row = i // 2
        col = i % 2
        x = grid_x + col * (S + DETAIL_GAP)
        y = grid_start_y + row * (S + DETAIL_GAP)
        path = find_file(src_dir, key)
        fitted = load_and_fit(path, (S, S))
        canvas.paste(fitted, (x, y))
        num, desc = DEFAULT_LABELS[key]
        draw_label_on_image(canvas, x, y, num, desc, font_label, font_label_desc)

    # 底部设计说明
    footer_y = canvas_height - FOOTER_HEIGHT + 30
    draw.line([(MARGIN, footer_y - 20), (canvas_width - MARGIN, footer_y - 20)], fill=LINE_COLOR, width=1)
    draw.text((MARGIN, footer_y), "设计说明", fill=TEXT_GOLD, font=font_info_title)
    if not design_notes:
        design_notes = [
            "本板为视觉气氛参考，用于色彩、结构、材质沟通，不作为舞台成衣唯一标准。",
            "实际制作需以演员身体数据、动作需求、预算周期为准；建议先做面料小样与上身坯样。",
            "核心意象请根据角色具体设定补充。",
        ]
    for i, line in enumerate(design_notes):
        draw.text((MARGIN, footer_y + 48 + i * 42), line, fill=TEXT_GRAY, font=font_info_body)

    png_path = os.path.join(out_dir, f"{character}_设计板_拼合_v{version}.png")
    canvas.save(png_path, "PNG", quality=95)
    print(f"已保存 PNG: {png_path}")

    pdf_path = os.path.join(out_dir, f"{character}_设计板_拼合_v{version}.pdf")
    canvas.save(pdf_path, "PDF", resolution=300.0)
    print(f"已保存 PDF: {pdf_path}")

    return png_path, pdf_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成舞台服装设计板")
    parser.add_argument("--src", required=True, help="源图目录")
    parser.add_argument("--out", required=True, help="输出目录")
    parser.add_argument("--character", required=True, help="角色名")
    parser.add_argument("--version", default="1.0", help="版本号")
    parser.add_argument("--project", default="", help="项目名称")
    parser.add_argument("--role", default="", help="角色定位")
    parser.add_argument("--color", default="", help="主色调")
    parser.add_argument("--fabric", default="", help="主要面料")
    args = parser.parse_args()

    build_board(
        src_dir=args.src,
        out_dir=args.out,
        character=args.character,
        version=args.version,
        project=args.project,
        role_position=args.role,
        color_scheme=args.color,
        fabric=args.fabric,
    )
