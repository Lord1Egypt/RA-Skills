#!/usr/bin/env python3
"""
MapTileRenderer — 纯 Python 渲染完整路线图卡片（含地图+统计+景点+贴士）
用法: python3 render.py <input.html> <output.png> [--accent #hex] [--zoom N]
"""
import sys, os, json, math, time, re, io, argparse
import requests
from PIL import Image, ImageDraw, ImageFont

TILE_SIZE = 256
DEFAULT_ZOOM = 13
TARGET_W = 700  # 输出图片宽度

# ── 字体（回退方案）─────────────────────────────────────────────────────────

def make_font(size, bold=False):
    """加载字体，优先用支持中文的"""
    candidates = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ] if not bold else [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for f in candidates:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except Exception:
                pass
    return ImageFont.load_default()

# ── 地理计算──────────────────────────────────────────────────────────────────

# WGS84 → GCJ-02（高德/腾讯坐标）
def wgs84_to_gcj02(lat, lon):
    a, ee = 6378245.0, 0.00669342
    def tl(y, x):
        ret = -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*x*y + 0.2*math.sqrt(abs(x))
        ret += (20.0*math.sin(6.0*x*math.pi) + 20.0*math.sin(2.0*x*math.pi)) * 2.0/3.0
        ret += (20.0*math.sin(y*math.pi) + 40.0*math.sin(y/3.0*math.pi)) * 2.0/3.0
        ret += (160.0*math.sin(y/12.0*math.pi) + 320.0*math.sin(y*math.pi/30.0)) * 2.0/3.0
        return ret
    def tL(y, x):
        ret = 300.0 + x + 2.0*y + 0.1*x*x + 0.1*x*y + 0.1*math.sqrt(abs(x))
        ret += (20.0*math.sin(6.0*x*math.pi) + 20.0*math.sin(2.0*x*math.pi)) * 2.0/3.0
        ret += (20.0*math.sin(x*math.pi) + 40.0*math.sin(x/3.0*math.pi)) * 2.0/3.0
        ret += (150.0*math.sin(x/12.0*math.pi) + 300.0*math.sin(x/30.0*math.pi)) * 2.0/3.0
        return ret
    dLat = tl(lon - 105.0, lat - 35.0)
    dLon = tL(lon - 105.0, lat - 35.0)
    rlat = lat / 180.0 * math.pi
    magic = 1.0 - ee * (math.sin(rlat) ** 2)
    dLat = (dLat * 180.0) / ((a * (1.0 - ee)) / (magic * math.sqrt(magic)) * math.pi)
    dLon = (dLon * 180.0) / (a / math.sqrt(magic) * math.cos(rlat) * math.pi)
    return lat + dLat, lon + dLon

def lat2tile(lat, lon, zoom):
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    lat_r = math.radians(lat)
    y_merc = (1.0 - math.log(math.tan(lat_r) + 1.0/math.cos(lat_r)) / math.pi) / 2.0 * n
    return max(0, x), max(0, int(y_merc))

def deg2px(lat, lon, zoom, tx_min, ty_min):
    n = 2 ** zoom
    x_px = ((lon + 180.0) / 360.0 * n - tx_min) * TILE_SIZE
    lat_r = math.radians(lat)
    y_px = ((1.0 - math.log(math.tan(lat_r) + 1/math.cos(lat_r)) / math.pi) / 2.0 * n - ty_min) * TILE_SIZE
    return x_px, y_px

def accent_to_rgb(h):
    if h.startswith('#') and len(h) >= 7:
        return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
    return (233, 69, 96)

def darken_rgb(rgb, factor=0.72):
    return tuple(min(255, int(c * factor)) for c in rgb)

# ── Tile 下载─────────────────────────────────────────────────────────────────

def get_tile(tx, ty, zoom, retries=3):
    # OSM 法国节点（图块数据质量高、国外覆盖好）
    url = f"https://a.tile.openstreetmap.fr/osmfr/{zoom}/{tx}/{ty}.png"
    for i in range(retries):
        try:
            r = requests.get(url, headers={'User-Agent': 'CitywalkMapRenderer/3.0'}, timeout=15)
            if r.status_code == 200 and len(r.content) > 5000 and r.content[:4] == b'\x89PNG':
                img = Image.open(io.BytesIO(r.content))
                if img.mode == 'P':
                    img = img.convert('RGB')
                return img
            time.sleep(1)
        except Exception:
            if i < retries - 1:
                time.sleep(2 ** i)
    return Image.new('RGB', (TILE_SIZE, TILE_SIZE), (220, 220, 220))

# ── 完整渲染────────────────────────────────────────────────────────────────

def render_full_card(waypoints, route_coords, title, subtitle, dist, dur, walk,
                     tips, accent, output, zoom=DEFAULT_ZOOM):
    """渲染完整路线图卡片（地图+统计+景点+贴士）"""

    # ── 底图 ────────────────────────────────────────────────────────────────
    all_c = route_coords + [[w['lat'], w['lon']] for w in waypoints]
    lats = [c[0] for c in all_c]
    lons = [c[1] for c in all_c]
    pad = 0.008
    tx_lo, ty_hi = lat2tile(max(lats) + pad, min(lons) - pad, zoom)
    tx_hi, ty_lo = lat2tile(min(lats) - pad, max(lons) + pad, zoom)
    tx_min = max(0, tx_lo - 1)
    tx_max = tx_hi + 2
    ty_min = max(0, ty_hi - 1)
    ty_max = ty_lo + 2
    cols = tx_max - tx_min
    rows = ty_max - ty_min
    total = cols * rows
    print(f"  底图: zoom={zoom}, tiles={cols}x{rows} ({total}张)")

    base = Image.new('RGB', (cols * TILE_SIZE, rows * TILE_SIZE))
    for ty_i in range(ty_min, ty_max):
        for tx_i in range(tx_min, tx_max):
            base.paste(get_tile(tx_i, ty_i, zoom),
                       ((tx_i - tx_min) * TILE_SIZE, (ty_i - ty_min) * TILE_SIZE))
        pct = (ty_i - ty_min + 1) * 100 // rows
        print(f"  下载进度 {pct}%...", end='\r')
    print(f"  底图完成 ({total}张)")

    # 画路线
    draw = ImageDraw.Draw(base)
    pts = [deg2px(c[0], c[1], zoom, tx_min, ty_min) for c in route_coords]
    if len(pts) > 1:
        draw.line(pts, fill=accent_to_rgb(accent), width=5)

    # 画站点
    for i, wp in enumerate(waypoints):
        px, py = deg2px(wp['lat'], wp['lon'], zoom, tx_min, ty_min)
        col = (accent_to_rgb(accent) if i == 0
               else (34, 197, 94) if i == len(waypoints) - 1
               else (255, 159, 67))
        r = 12
        draw.ellipse([px - r, py - r, px + r, py + r], fill=col, outline='white', width=3)
        name = wp['name']
        draw.text((px + 16, py - 9), name, fill=(30, 30, 30))

    # 缩放到底图目标尺寸（宽=TARGET_W）
    ratio = TARGET_W / base.width
    map_h = int(base.height * ratio)
    base = base.resize((TARGET_W, map_h), Image.LANCZOS)

    # ── 布局参数 ────────────────────────────────────────────────────────────
    bar_h  = 60    # 标题栏
    stats_h = 72   # 统计栏
    pad_h   = 12   # 间距
    info_h  = 90   # 下方景点+贴士栏高度
    radius  = 16    # 卡片圆角

    total_h = bar_h + map_h + stats_h + pad_h + info_h
    accent_rgb = accent_to_rgb(accent)
    accent_dark = darken_rgb(accent_rgb)
    bg = (245, 247, 250)   # 卡片背景灰
    white = (255, 255, 255)

    # 创建成品图
    card = Image.new('RGB', (TARGET_W, total_h), bg)
    d = ImageDraw.Draw(card)

    # ── 标题栏 ─────────────────────────────────────────────────────────────
    card.paste(base, (0, bar_h))                          # 底图贴在标题栏下方

    # 统计栏背景（白色圆角卡片）
    stats_y = bar_h + map_h
    card_raw = Image.new('RGB', (TARGET_W, stats_h + radius), bg)
    card_raw.paste(white, (0, 0, TARGET_W, stats_h))
    # 简单圆角遮罩（只做顶部）
    for x in range(TARGET_W):
        for dy in range(radius):
            alpha = int(255 * (1 - dy / radius) ** 2)
            if 0 <= x < radius:
                card_raw.putpixel((x, dy), white)
            if TARGET_W - radius <= x < TARGET_W:
                card_raw.putpixel((x, dy), white)
    card.paste(card_raw, (0, stats_y))

    # ── 统计栏数据 ─────────────────────────────────────────────────────────
    stat_items = [
        (dist,  '步行距离'),
        (dur,   '游览时长'),
        (f"{len(waypoints)}站", '途经景点'),
        (walk,  '纯步行'),
    ]
    stat_w = TARGET_W // 4
    fnt_num  = make_font(18, bold=True)
    fnt_lbl  = make_font(10)
    for i, (val, lbl) in enumerate(stat_items):
        x = i * stat_w
        # 数字
        d.text((x + stat_w//2, stats_y + 14), str(val),
               fill=accent_rgb, font=fnt_num, anchor='mm')
        # 标签
        d.text((x + stat_w//2, stats_y + 44), lbl,
               fill=(136, 136, 136), font=fnt_lbl, anchor='mm')

    # ── 下方信息栏 ──────────────────────────────────────────────────────────
    info_y = stats_y + stats_h + pad_h
    info_raw = Image.new('RGB', (TARGET_W, info_h), bg)
    # 左栏：途经景点
    left = Image.new('RGB', (int(TARGET_W * 0.58) - 6, info_h - 12), white)
    ld = ImageDraw.Draw(left)
    ld.text((10, 8), '途经景点', fill=(136, 136, 136), font=make_font(10))
    for i, wp in enumerate(waypoints):
        col = (accent_rgb if i == 0
               else (34, 197, 94) if i == len(waypoints) - 1
               else (255, 159, 67))
        num_str = str(i + 1)
        y = 26 + i * 22
        # 圆形编号
        ld.ellipse([8, y - 8, 8 + 16, y + 8], fill=col)
        ld.text((8 + 8, y), num_str, fill=white, font=make_font(9), anchor='mm')
        # 景点名
        ld.text((32, y), wp['name'], fill=(50, 50, 50), font=make_font(11), anchor='mm')
    info_raw.paste(left, (6, 6))

    # 右栏：实用贴士
    right = Image.new('RGB', (TARGET_W - int(TARGET_W * 0.58) - 12, info_h - 12), white)
    rd = ImageDraw.Draw(right)
    rd.text((10, 8), '实用贴士', fill=(136, 136, 136), font=make_font(10))
    for j, tip in enumerate(tips[:4]):
        rd.text((10, 26 + j * 18), f"• {tip}", fill=(60, 60, 60), font=make_font(10))
    info_raw.paste(right, (int(TARGET_W * 0.58) + 6, 6))

    card.paste(info_raw, (0, info_y))

    # ── 标题栏（覆盖在地图顶部）─────────────────────────────────────────────
    title_raw = Image.new('RGBA', (TARGET_W, bar_h + radius), (0, 0, 0, 0))
    td = ImageDraw.Draw(title_raw)
    # 渐变标题栏
    for y in range(bar_h):
        alpha = int(200 * (1 - y / bar_h))
        col = accent_dark + (alpha,)
        td.line([(0, y), (TARGET_W, y)], fill=accent_dark)
    td.rectangle([0, 0, TARGET_W, bar_h], fill=accent_dark)
    title_img = Image.new('RGB', (TARGET_W, bar_h), accent_dark)
    card.paste(title_img, (0, 0))
    d = ImageDraw.Draw(card)
    d.text((18, 14), f"🚶  {title}", fill=white, font=make_font(17, bold=True))
    d.text((18, 36), subtitle, fill=(230, 230, 230), font=make_font(10))

    card.save(output)
    print(f"  输出: {output}  ({TARGET_W}x{total_h})")
    return output

# ── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('html',   help='输入 HTML 路径')
    p.add_argument('output', help='输出 PNG 路径')
    p.add_argument('--accent', '-a', default=None, help='主题色，如 #228B22')
    p.add_argument('--zoom', '-z', type=int, default=DEFAULT_ZOOM,
                   help=f'缩放级别（默认 {DEFAULT_ZOOM}）')
    args = p.parse_args()

    with open(args.html, 'r', encoding='utf-8') as f:
        html = f.read()

    # 解析 HTML 中的数据
    wp_match  = re.search(r'var waypoints = (\[.*?\]);', html, re.DOTALL)
    rt_match  = re.search(r'var routeCoords = (\[.*?\]);', html, re.DOTALL)
    title_m   = re.search(r'<title>(.*?)</title>', html)
    # stats: 从 .stat .num 抓
    stat_nums = re.findall(r'<div class="num">(.*?)</div>', html)
    stat_lbls = re.findall(r'<div class="label">(.*?)</div>', html)
    # tips — 只取 class="tips" 列表中的项
    tips_section = re.search(r'<ul class="tips">(.*?)</ul>', html, re.DOTALL)
    tips = re.findall(r'<li>(.*?)</li>', tips_section.group(1)) if tips_section else []

    if not wp_match or not rt_match:
        print("错误: 无法解析 HTML 中的 waypoints/routeCoords"); sys.exit(1)

    waypoints = json.loads(wp_match.group(1))
    route     = json.loads(rt_match.group(1))
    title     = title_m.group(1) if title_m else 'Citywalk Map'

    # 副标题：.header 里的 <p>
    sub_m = re.search(r'<div class="header".*?<p>(.*?)</p>', html, re.DOTALL)
    subtitle = sub_m.group(1) if sub_m else ''

    # 主题色
    accent = args.accent
    if not accent:
        m = re.search(r'background:\s*#([0-9a-fA-F]{6})', html)
        accent = '#' + m.group(1) if m else '#e94560'

    # stats（按顺序取前4个）
    stats = list(zip(stat_nums[:4], stat_lbls[:4]))
    dist = stats[0][0] if len(stats) > 0 else '—'
    dur  = stats[1][0] if len(stats) > 1 else '—'
    walk = stats[3][0] if len(stats) > 3 else '—'

    # tips 清理 HTML 标签
    clean_tips = []
    for t in tips:
        t = re.sub(r'<[^>]+>', '', t).strip()
        if t:
            clean_tips.append(t)
    # 如果上面提取失败，用原始 <li> 文本兜底
    if not clean_tips:
        li_items = re.findall(r'<li>(.*?)</li>', html)
        for t in li_items:
            t = re.sub(r'<[^>]+>', '', t).strip()
            if t and len(t) > 3:
                clean_tips.append(t)

    print(f"主题色: {accent} | 标题: {title}")
    print(f"统计: {dist} / {dur} / {len(waypoints)}站 / {walk}")
    print(f"贴士: {clean_tips[:3]}")

    render_full_card(
        waypoints=waypoints,
        route_coords=route,
        title=title,
        subtitle=subtitle,
        dist=dist,
        dur=dur,
        walk=walk,
        tips=clean_tips,
        accent=accent,
        output=args.output,
        zoom=args.zoom,
    )
