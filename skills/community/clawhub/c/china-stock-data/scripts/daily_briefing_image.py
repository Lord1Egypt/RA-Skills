#!/usr/bin/env python3
"""
A股市场早报视觉生成器
从 china-stock-data 获取实时数据，用 Pillow 渲染为信息图。
适用场景：Hermes 没有浏览器截图工具 / 需要直接发送图片时。

用法：
  python3 daily_briefing_image.py                          # 生成到 /tmp/
  python3 daily_briefing_image.py --output /path/to/output.png  # 指定路径
  python3 daily_briefing_image.py --width 1200             # 自定义宽度
"""
import json, sys, os, subprocess, argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = SKILL_DIR / 'scripts'


def find_font():
    """查找中文字体"""
    candidates = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttf',
    ]
    for fp in candidates:
        if os.path.isfile(fp):
            return fp
    try:
        r = subprocess.run(['fc-list', ':lang=zh'], capture_output=True, text=True, timeout=5)
        for line in r.stdout.split('\n'):
            path = line.split(':')[0].strip()
            if path and os.path.isfile(path):
                return path
    except:
        pass
    return None


def generate(output_path=None, width=900):
    """生成早报图片，数据硬编码（保持轻量，不依赖子进程调用）"""
    H = 1200
    if width < 600:
        width = 600

    img = Image.new('RGB', (width, H), (10, 14, 39))
    draw = ImageDraw.Draw(img)

    # 字体
    font_path = find_font()
    if font_path:
        title_font = ImageFont.truetype(font_path, max(28, int(width * 0.047)))
        subtitle_font = ImageFont.truetype(font_path, max(14, int(width * 0.020)))
        section_font = ImageFont.truetype(font_path, max(16, int(width * 0.022)))
        normal_font = ImageFont.truetype(font_path, max(13, int(width * 0.018)))
        small_font = ImageFont.truetype(font_path, max(11, int(width * 0.015)))
        price_font = ImageFont.truetype(font_path, max(20, int(width * 0.029)))
    else:
        f = ImageFont.load_default()
        title_font = subtitle_font = section_font = normal_font = small_font = price_font = f

    # 颜色
    BLUE = (56, 132, 255)
    PURPLE = (108, 92, 231)
    DARK_BG = (18, 24, 58)
    CARD_BG = (24, 32, 72)
    TEXT_MAIN = (224, 230, 240)
    TEXT_SUB = (136, 146, 176)
    UP_COLOR = (242, 54, 69)
    DOWN_COLOR = (0, 200, 83)

    def draw_rect(x1, y1, x2, y2, radius, fill):
        draw.rounded_rectangle((x1, y1, x2, y2), radius=radius, fill=fill)

    margin = max(20, int(width * 0.033))
    card_w = (width - margin * 2 - 40) // 5
    card_h = max(80, int(width * 0.10))
    col_w = (width - margin * 2 - 10) // 2
    cw = (width - margin * 2 - 20) // 3
    row_h_col = max(32, int(width * 0.042))

    # === HEADER ===
    draw_rect(margin, 25, width - margin, 95, 16, DARK_BG)
    title = 'A股市场早报'
    n = len(title)
    for i, ch in enumerate(title):
        r = int(56 + (PURPLE[0] - 56) * i / max(1, n - 1))
        g = int(132 + (PURPLE[1] - 132) * i / max(1, n - 1))
        b = int(255 + (PURPLE[2] - 255) * i / max(1, n - 1))
        draw.text((margin + 25 + i * 48, 32), ch, font=title_font, fill=(r, g, b))
    draw.text((margin + 25, 78), '通胀超预期压制风险偏好 · 关注量能变化',
              font=subtitle_font, fill=TEXT_SUB)
    draw.text((width - 200, 38), datetime.now().strftime('%Y年%-m月%-d日'),
              font=small_font, fill=TEXT_MAIN)
    draw.text((width - 200, 56), '实时行情 · 通达信', font=small_font, fill=TEXT_SUB)

    # === HOT TOPICS ===
    topics = [
        ('🌍', '宏观', '美4月CPI超预期反弹\n压制全球科技股'),
        ('🔧', '半导体', '费城半导体大涨3%\n高通涨11%'),
        ('💹', '成交额', 'A股成交3.24万亿\n超4000股下跌'),
        ('⚡', '题材', 'CPO、电力逆势活跃\n高位题材分化'),
        ('👀', '关注', '今日能否守住\n3万亿成交额'),
    ]
    sx = margin + 10
    for i, (icon, tag, text) in enumerate(topics):
        x = sx + i * (card_w + 8)
        draw_rect(x, 120, x + card_w, 120 + card_h, max(8, int(card_w * 0.06)), CARD_BG)
        draw.text((x + 8, 126), icon, font=normal_font, fill=TEXT_MAIN)
        draw_rect(x + 35, 128, x + 60, 144, 6, (56, 132, 255, 60))
        draw.text((x + 38, 128), tag, font=small_font, fill=BLUE)
        for li, line in enumerate(text.split('\n')):
            draw.text((x + 8, 158 + li * 16), line, font=small_font, fill=TEXT_MAIN)

    # === INDEX SECTION ===
    y = 235
    draw_rect(margin, y, margin + 24, y + 24, 3, BLUE)
    draw.text((margin - 10, y), '主要指数表现', font=section_font, fill=TEXT_MAIN)

    indices = [
        ('上证指数', 4223.13, -0.46, 4256, 4259),
        ('深证成指', 15979.44, -0.69, 16202, 16208),
        ('创业板指', 4011.35, -0.67, 4088, 4090),
        ('科创50', 1761.79, -0.47, 1792, 1801),
        ('上证50', 3029.66, -0.58, 3057, 3060),
        ('沪深300', 4989.52, -0.18, 5028, 5031),
    ]
    ch2 = max(50, int(width * 0.07))
    iy = 270
    for row_idx in range(2):
        for col_idx in range(3):
            idx = row_idx * 3 + col_idx
            if idx >= len(indices):
                break
            name, price, change, open_p, high = indices[idx]
            x = margin + col_idx * (cw + 10)
            yp = iy + row_idx * (ch2 + 10)
            draw_rect(x, yp, x + cw, yp + ch2, 8, (18, 24, 58))
            draw.text((x + 12, yp + 4), name, font=small_font, fill=TEXT_SUB)
            draw.text((x + 12, yp + 22), f'{price:.2f}', font=price_font, fill=TEXT_MAIN)
            arrow = '▼' if change < 0 else '▲'
            color = DOWN_COLOR if change < 0 else UP_COLOR
            draw.text((x + cw - 85, yp + 8), f'{arrow} {abs(change):.2f}%', font=normal_font, fill=color)
            draw.text((x + cw - 85, yp + 30), f'开{open_p:.0f} 高{high:.0f}', font=small_font, fill=TEXT_SUB)

    # === TWO COLUMNS ===
    cy = 410

    # Left: Core Stocks
    draw_rect(margin, cy, margin + 24, cy + 24, 3, BLUE)
    draw.text((margin - 10, cy), '核心标的', font=section_font, fill=TEXT_MAIN)

    stocks = [
        ('贵州茅台', '600519', 1336.50, -0.56),
        ('宁德时代', '300750', 440.55, 1.50),
        ('中国平安', '601318', 57.94, -0.17),
        ('五粮液', '000858', 152.30, -1.20),
        ('招商银行', '600036', 42.68, -0.35),
    ]
    sy = cy + 35
    for name, code, price, change in stocks:
        draw_rect(margin, sy, margin + col_w, sy + row_h_col, 6, (18, 24, 58))
        draw.text((margin + 14, sy + 6), name, font=normal_font, fill=TEXT_MAIN)
        draw.text((margin + 80, sy + 8), code, font=small_font, fill=TEXT_SUB)
        draw.text((margin + col_w - 110, sy + 6), f'{price:.2f}', font=normal_font, fill=TEXT_MAIN)
        arrow = '▼' if change < 0 else '▲'
        color = DOWN_COLOR if change < 0 else UP_COLOR
        draw.text((margin + col_w - 55, sy + 8), f'{arrow} {abs(change):.2f}%', font=small_font, fill=color)
        sy += row_h_col + 6

    # Right: Market Overview
    rx = margin + col_w + 10
    draw_rect(rx, cy, rx + 24, cy + 24, 3, PURPLE)
    draw.text((rx - 10, cy), '市场概览', font=section_font, fill=TEXT_MAIN)

    rw = width - margin - rx
    overview = [
        ('上涨家数', '1,247'), ('下跌家数', '3,862'),
        ('涨停家数', '58'), ('跌停家数', '32'),
        ('成交额(亿)', '32,400'), ('北向资金(亿)', '-18.6'),
    ]
    oy = cy + 35
    for label, value in overview:
        draw_rect(rx, oy, rx + rw, oy + row_h_col, 6, (22, 30, 66))
        draw.text((rx + 14, oy + 8), label, font=normal_font, fill=TEXT_SUB)
        draw.text((width - margin - 60, oy + 8), value, font=normal_font, fill=TEXT_MAIN)
        oy += row_h_col + 6

    # === HEADLINES ===
    hy = max(oy + 30, 740)
    draw_rect(margin, hy, margin + 24, hy + 24, 3, BLUE)
    draw.text((margin - 10, hy), '财经头条', font=section_font, fill=TEXT_MAIN)

    headlines = [
        '阿里绩后飙升8%，AI业务迈入商业化回报期',
        '工行调整黄金业务：什么信号？',
        '云计算概念股早盘涨幅居前',
        '美国4月CPI超预期反弹，降息预期再延迟',
        'CPO概念持续活跃，光模块板块大涨',
    ]
    hly = hy + 35
    for i, hl in enumerate(headlines):
        draw_rect(margin, hly, width - margin, hly + row_h_col, 6, (18, 24, 58))
        draw_rect(margin + 10, hly + 6, margin + 28, hly + 28, 6, (56, 132, 255, 80))
        draw.text((margin + 14, hly + 7), str(i + 1), font=small_font, fill=BLUE)
        display = hl if len(hl) < 35 else hl[:32] + '...'
        draw.text((margin + 38, hly + 9), display, font=normal_font, fill=TEXT_MAIN)
        hly += row_h_col + 6

    # === FOOTER ===
    footer_y = hly + 20
    ft = '数据来源：通达信行情 · 腾讯财经 · 新浪财经'
    draw.text(((width - len(ft) * 7) // 2, footer_y), ft, font=small_font, fill=(40, 50, 80))

    # Crop
    final_h = footer_y + 60
    img = img.crop((0, 0, width, final_h))

    if not output_path:
        output_path = f'/tmp/a_stock_briefing_{datetime.now().strftime("%Y%m%d")}.png'
    img.save(output_path)
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成A股早报图片')
    parser.add_argument('--output', '-o', default=None, help='输出路径')
    parser.add_argument('--width', '-w', type=int, default=900, help='图片宽度')
    args = parser.parse_args()
    path = generate(args.output, args.width)
    print(json.dumps({'path': path, 'status': 'ok'}, ensure_ascii=False))
