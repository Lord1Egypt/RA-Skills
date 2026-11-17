"""生成微信视频号竖屏封面 1080x1920, 关键信息居中防裁切"""
from PIL import Image, ImageDraw, ImageFont
import os, sys

W, H = 1080, 1920
FONT_REG = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"


def wrap(draw, text, font, max_w):
    """按像素宽度折行(支持中英文混排)"""
    lines, cur = [], ""
    for ch in text:
        t = cur + ch
        if draw.textbbox((0, 0), t, font=font)[2] > max_w and cur:
            lines.append(cur); cur = ch
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def make_cover(out, book, quote, idx=None, total=5, bg=(18, 22, 34)):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    # 顶部装饰条
    d.rectangle([0, 0, W, 14], fill=(217, 119, 6))

    f_book = ImageFont.truetype(FONT_BOLD, 76)
    f_quote = ImageFont.truetype(FONT_REG, 56)
    f_tag = ImageFont.truetype(FONT_REG, 40)

    # 安全区: 垂直居中区域 (视频号裁上下, 关键信息放中间60%)
    safe_top, safe_bot = int(H * 0.20), int(H * 0.80)
    max_w = W - 140

    # 序号标签
    y = safe_top
    if idx:
        d.text((70, y), f"0{idx} / 0{total}", font=f_tag, fill=(217, 119, 6))
        y += 70

    # 书名(加粗大字, 可折行)
    for line in wrap(d, book, f_book, max_w):
        d.text((70, y), line, font=f_book, fill=(255, 255, 255))
        y += f_book.size + 22

    y += 46
    # 分隔线
    d.rectangle([70, y, 70 + 160, y + 8], fill=(217, 119, 6))
    y += 70

    # 金句
    for line in wrap(d, quote, f_quote, max_w):
        d.text((70, y), line, font=f_quote, fill=(235, 232, 226))
        y += f_quote.size + 26

    # 底部引导
    d.text((70, H - 150), "完整版见主页", font=f_tag, fill=(150, 148, 142))

    img.save(out, quality=95)
    print(f"cover -> {out}")
    return out


if __name__ == "__main__":
    # 由主流程调用; 单独测试:
    make_cover("output/cover_01数据会撒谎.png", "《学会提问》",
               "统计数据看起来最科学，但它经常撒谎", 1, total=1)
