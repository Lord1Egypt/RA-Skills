#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cover_card.py — 点评首图：3:4 拼图 + 白字标题 + 浅黄事实行

版式对齐常见探店封面：上幅一张横图（约 64%），下面两张并排；
标题 `<地点 · 名称>` 白字黑边，下面 2–4 行「标签：事实」。
字只渲染调用方给的字符串，不补事实。

合成需要 Pillow：python3 -m pip install pillow
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from content_gate import (  # noqa: E402
    AI_FLAVOR_WORDS,
    DIVERSION_RE,
    HARD_SELL_WORDS,
    MERCHANT_VOICE_WORDS,
    NUMBER_RE,
    _num_key,
    fact_numbers,
    find_absolute_words,
    find_ai_cliches,
)

COVER_W, COVER_H = 1080, 1440
TOP_RATIO = 0.64
TITLE_FILL = (255, 255, 255)
TITLE_STROKE = (0, 0, 0)
LINE_FILL = (237, 224, 132)  # 参考图浅黄 #EDE084
LINE_STROKE = (28, 22, 8)

# 标题用黑体，事实行用细一号，避免两层字糊成一块。
_FONTS = {
    "bold": [
        ("/System/Library/Fonts/STHeiti Medium.ttc", 1),
        ("/System/Library/Fonts/Hiragino Sans GB.ttc", 2),
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 0),
        ("/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc", 0),
        (r"C:\Windows\Fonts\msyhbd.ttc", 0),
        (r"C:\Windows\Fonts\msyh.ttc", 0),
    ],
    "regular": [
        ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
        ("/System/Library/Fonts/STHeiti Light.ttc", 1),
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 0),
        ("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", 0),
        (r"C:\Windows\Fonts\msyh.ttc", 0),
    ],
}


class CoverError(Exception):
    pass


def normalize_title(title: str) -> str:
    inner = (title or "").strip().strip("<>＜＞〈〉《》「」").strip()
    if inner.count("·") != 1:
        raise CoverError("首图标题写成「地点 · 名称」，中间一个 ·，例如 <大邑 · 赵公山东线>")
    place, name = (part.strip() for part in inner.split("·"))
    if not place or not name:
        raise CoverError("首图标题的地点和名称都不能空")
    inner = f"{place} · {name}"
    if not 4 <= len(inner) <= 18:
        raise CoverError(f"首图标题（不含括号）要 4–18 字，现在 {len(inner)} 字：{inner}")
    return f"<{inner}>"


def validate_cover(cover, n_images: int, facts=None, check_facts: bool = True) -> dict:
    """检查封面文案和用图下标。返回可直接拿去画的 {title, lines, picks}。"""
    if n_images < 1:
        raise CoverError("封面至少要 1 张图")
    if not isinstance(cover, dict):
        raise CoverError("有图就要首图标题 cover：{title, lines}")
    title = normalize_title(cover.get("title") or "")
    raw_lines = cover.get("lines")
    if not isinstance(raw_lines, list) or not 2 <= len(raw_lines) <= 4:
        raise CoverError("首图 lines 要 2–4 行，每行「标签：事实」")
    lines = []
    for line in raw_lines:
        text = str(line).strip().replace("\n", "")
        if "：" not in text and ":" not in text:
            raise CoverError(f"首图每一行都写成「标签：事实」，这行不是：{text}")
        text = text.replace(":", "：", 1) if "：" not in text else text
        if len(text) > 36:
            raise CoverError(f"首图这一行太长（最多 36 字），缩短：{text}")
        lines.append(text)

    picks = cover.get("picks")
    if picks is None:
        picks = list(range(min(3, n_images)))
    if (not isinstance(picks, list) or not picks or len(picks) > 3
            or any(isinstance(i, bool) or not isinstance(i, int) or i < 0 or i >= n_images for i in picks)
            or len(set(picks)) != len(picks)):
        raise CoverError(f"cover.picks 是不重复的图片下标（0 到 {n_images - 1}），最多 3 张")

    if check_facts:
        text = title + "\n" + "\n".join(lines)
        hit_abs = find_absolute_words(text)
        if hit_abs:
            raise CoverError(f"首图文字有极限词: {hit_abs}")
        hit_div = sorted(set(DIVERSION_RE.findall(text)))
        if hit_div:
            raise CoverError(f"首图文字有站外联系方式: {hit_div}")
        hit_ai = sorted({w for w in AI_FLAVOR_WORDS if w.lower() in text.lower()}) + find_ai_cliches(text)
        if hit_ai:
            raise CoverError(f"首图文字有网感堆砌词或 AI 腔: {hit_ai}")
        hit_sell = sorted({w for w in HARD_SELL_WORDS + MERCHANT_VOICE_WORDS if w in text})
        if hit_sell:
            raise CoverError(f"首图文字有推销或商家口吻: {hit_sell}")
        if facts is None:
            raise CoverError("首图文字要对照事实卡，缺少 facts")
        allowed = fact_numbers(facts)
        orphan = sorted({n for n in NUMBER_RE.findall(text) if _num_key(n) not in allowed}, key=_num_key)
        if orphan:
            raise CoverError(f"首图里的数字事实卡没有: {orphan}")

    return {"title": title, "lines": lines, "picks": picks}


def _import_pil():
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as e:
        raise CoverError("合成首图需要 Pillow：python3 -m pip install pillow") from e
    return Image, ImageDraw, ImageFont, ImageOps


def _load_font(size: int, weight: str):
    _, _, ImageFont, _ = _import_pil()
    for path, index in _FONTS[weight]:
        if not Path(path).exists():
            continue
        try:
            return ImageFont.truetype(path, size, index=index)
        except OSError:
            continue
    raise CoverError("找不到中文字体。macOS 用黑体，Windows 用微软雅黑，Linux 安装 fonts-noto-cjk")


def _ink_width(font, text: str) -> int:
    return int(round(font.getlength(text)))


def _fit_font(text: str, max_w: int, start: int, minimum: int, weight: str):
    size = start
    font = _load_font(size, weight)
    while size > minimum and _ink_width(font, text) > max_w:
        size -= 2
        font = _load_font(size, weight)
    return font


def _ink_height(font, text: str) -> int:
    box = font.getbbox(text)
    return box[3] - box[1]


def _draw_text(draw, x, y, text, font, fill, stroke, sw):
    box = font.getbbox(text)
    draw.text((x - box[0], y - box[1]), text, font=font, fill=fill,
              stroke_width=sw, stroke_fill=stroke)


def _cover_crop(im, width: int, height: int, Image):
    scale = max(width / im.width, height / im.height)
    resized = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - width) // 2)
    top = max(0, (resized.height - height) // 2)
    return resized.crop((left, top, left + width, top + height))


def _panels(n: int):
    top_h = round(COVER_H * TOP_RATIO) if n >= 2 else COVER_H
    if n >= 3:
        mid = COVER_W // 2
        return [
            (0, 0, COVER_W, top_h),
            (0, top_h, mid, COVER_H),
            (mid, top_h, COVER_W, COVER_H),
        ]
    if n == 2:
        return [(0, 0, COVER_W, top_h), (0, top_h, COVER_W, COVER_H)]
    return [(0, 0, COVER_W, COVER_H)]


def paint_cover(paths, spec: dict, out_path) -> None:
    """paths 是全部原图；spec 来自 validate_cover。写出 1080×1440 JPEG。"""
    Image, ImageDraw, _, ImageOps = _import_pil()
    canvas = Image.new("RGB", (COVER_W, COVER_H))
    picks = spec["picks"]
    for box, index in zip(_panels(len(picks)), picks):
        try:
            with Image.open(paths[index]) as src:
                im = ImageOps.exif_transpose(src)
                tile = _cover_crop(im.convert("RGB"), box[2] - box[0], box[3] - box[1], Image)
        except CoverError:
            raise
        except Exception as e:
            raise CoverError(f"打不开图片: {paths[index]}") from e
        canvas.paste(tile, (box[0], box[1]))

    margin = 36
    max_w = COVER_W - margin * 2
    title_font = _fit_font(spec["title"], max_w, 128, 64, "bold")
    line_font = _fit_font(max(spec["lines"], key=len), max_w, 40, 28, "regular")
    title_h = _ink_height(title_font, spec["title"])
    line_h = _ink_height(line_font, "国")
    title_gap = max(10, title_font.size // 7)
    line_gap = max(6, line_font.size // 5)
    lines_h = len(spec["lines"]) * line_h + (len(spec["lines"]) - 1) * line_gap
    # 接缝落在行距里：最后一行跨进下幅，上面的行留在上幅，避免一行字被切成两半
    seam = round(COVER_H * TOP_RATIO) if len(spec["picks"]) >= 2 else round(COVER_H * 0.72)
    above = max(1, len(spec["lines"]) - 1)
    y_lines = seam - (above * line_h + max(0, above - 1) * line_gap) - 8
    y = y_lines - title_gap - title_h
    block_h = title_h + title_gap + lines_h
    if y + block_h > COVER_H - 36:
        y = COVER_H - 36 - block_h
    y = max(y, round(COVER_H * 0.18))

    draw = ImageDraw.Draw(canvas)
    title_sw = max(5, round(title_font.size / 16))
    line_sw = max(2, round(line_font.size / 13))
    _draw_text(draw, margin, y, spec["title"], title_font, TITLE_FILL, TITLE_STROKE, title_sw)
    y += title_h + title_gap
    for line in spec["lines"]:
        _draw_text(draw, margin, y, line, line_font, LINE_FILL, LINE_STROKE, line_sw)
        y += line_h + line_gap

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "JPEG", quality=92, subsampling=0)
