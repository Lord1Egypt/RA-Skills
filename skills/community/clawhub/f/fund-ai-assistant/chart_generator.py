"""
基金分析图表生成模块 - PIL 实现
全套视觉升级：深色头部 + 卡片布局 + 渐变图表 + 指标色块 + 专业对比图

使用方式：
  python3 chart_generator.py              # 测试图表生成
  from chart_generator import generate_fund_analysis_image  # 作为模块导入使用
"""
import os
import math
from datetime import datetime
from io import BytesIO
from typing import Optional

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
# 字体路径：优先同目录 assets/，其次系统字体
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
FONT_PATH = os.path.join(FONT_DIR, "微软雅黑.ttf")

# 系统备选字体（跨平台）
SYSTEM_FONTS = [
    FONT_PATH,
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    None,  # PIL 内置默认字体
]


# ─── 颜色主题 ────────────────────────────────────────────────
C_BG         = (255, 255, 255)
C_HEADER     = (245, 247, 255)
C_HEADER2    = (220, 228, 255)
C_ACCENT     = (40, 90, 220)
C_UP         = (220, 38, 38)
C_DOWN       = (34, 197, 94)
C_TEXT       = (30, 30, 30)
C_GRAY       = (120, 120, 130)
C_LIGHT      = (242, 244, 250)
C_BORDER     = (180, 200, 240)
C_GRID       = (220, 228, 245)
C_MA5        = (255, 150, 0)
C_MA10       = (0, 120, 220)
C_MA20       = (140, 60, 220)
C_POS_FILL   = (255, 230, 230)
C_NEG_FILL   = (225, 247, 235)

C_RSI_OVERBOUGHT = (255, 80, 80)
C_RSI_OVERSOLD   = (60, 200, 100)
C_RSI_NEUTRAL    = (100, 150, 240)
C_KDJ_BUY        = (60, 200, 100)
C_KDJ_SELL       = (255, 80, 80)
C_KDJ_NEUTRAL    = (240, 180, 60)
C_MACD_GOLDEN    = (60, 200, 100)
C_MACD_DEAD      = (255, 80, 80)
C_MACD_NEUTRAL   = (180, 180, 180)


def get_font(size: int) -> Optional[ImageFont.FreeTypeFont]:
    if not PIL_AVAILABLE:
        return None
    for path in SYSTEM_FONTS:
        if path and os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _gradient_rect(draw, x0, y0, x1, y1, color_top, color_bot, steps=40):
    r0, g0, b0 = color_top
    r1, g1, b1 = color_bot
    for i in range(steps):
        t = i / steps
        r = int(r0 + (r1 - r0) * t)
        g = int(g0 + (g1 - g0) * t)
        b = int(b0 + (b1 - b0) * t)
        yy = y0 + int((y1 - y0) * i / steps)
        draw.line([(x0, yy), (x1, yy)], fill=(r, g, b))


def _card(draw, x, y, w, h, fill=None, border=None):
    if fill is None:   fill = C_LIGHT
    if border is None: border = C_BORDER
    r = 6
    draw.rectangle([x+r, y, x+w-r, y+h], fill=fill)
    draw.rectangle([x, y+r, x+w, y+h-r], fill=fill)
    draw.pieslice([x, y, x+2*r, y+2*r], 180, 270, fill=fill)
    draw.pieslice([x+w-2*r, y, x+w, y+2*r], 270, 360, fill=fill)
    draw.pieslice([x, y+h-2*r, x+2*r, y+h], 90, 180, fill=fill)
    draw.pieslice([x+w-2*r, y+h-2*r, x+w, y+h], 0, 90, fill=fill)
    draw.line([(x+r, y), (x+w-r, y)], fill=border, width=1)
    draw.line([(x+r, y+h), (x+w-r, y+h)], fill=border, width=1)
    draw.line([(x, y+r), (x, y+h-r)], fill=border, width=1)
    draw.line([(x+w, y+r), (x+w, y+h-r)], fill=border, width=1)


def _badge(draw, x, y, text, bg_color, text_color=(255,255,255), font=None):
    if font is None:
        font = get_font(10)
    bw = int(len(text) * 7.5) + 10
    bh = 18
    r = 4
    draw.pieslice([x, y, x+2*r, y+2*r], 180, 270, fill=bg_color)
    draw.pieslice([x+bw-2*r, y, x+bw, y+2*r], 270, 360, fill=bg_color)
    draw.pieslice([x, y+bh-2*r, x+2*r, y+bh], 90, 180, fill=bg_color)
    draw.pieslice([x+bw-2*r, y+bh-2*r, x+bw, y+bh], 0, 90, fill=bg_color)
    draw.rectangle([x+r, y, x+bw-r, y+bh], fill=bg_color)
    draw.rectangle([x, y+r, x+bw, y+bh-r], fill=bg_color)
    tx = x + (bw - int(len(text) * 7.5)) // 2
    draw.text((tx, y + 2), text, fill=text_color, font=font)


# ─── 主图：单基金分析报告图 ──────────────────────────────────
def generate_fund_analysis_image(
    fund_code: str,
    fund_name: str,
    latest_nav: float,
    nav_change: float,
    analysis: dict,
    position: dict = None,
    width: int = 600,
    height: int = 680,
) -> Optional[bytes]:
    if not PIL_AVAILABLE:
        return None

    font_sm   = get_font(10)
    font_md   = get_font(12)
    font_lg   = get_font(15)
    font_xl   = get_font(20)
    font_head = get_font(17)

    img = Image.new("RGB", (width, height), C_BG)
    draw = ImageDraw.Draw(img)

    # ── 头部：浅底 + 蓝色顶栏 + 深色文字 ───────────────────────
    header_h = 74
    ACCENT_STRIP = (40, 90, 220)
    # 顶部蓝色细条
    draw.rectangle([0, 0, width, 5], fill=ACCENT_STRIP)
    # 主体浅底
    draw.rectangle([0, 5, width, header_h], fill=C_HEADER)
    # 左侧：基金名称
    draw.text((18, 12), fund_name, fill=(20, 30, 80), font=font_xl)
    draw.text((18, 40), f"基金代码：{fund_code}", fill=(80, 100, 160), font=font_md)
    # 右侧：净值 + 涨跌幅
    nav_str = f"{latest_nav:.4f}"
    chg_str = f"{'+' if nav_change >= 0 else ''}{nav_change:.2f}%"
    chg_col = (34, 197, 94) if nav_change >= 0 else (220, 38, 38)
    draw.text((width - 158, 12), "最新净值", fill=(80, 100, 160), font=font_sm)
    draw.text((width - 158, 28), nav_str, fill=(20, 30, 80), font=font_xl)
    _badge(draw, width - 105, 52, chg_str, chg_col)

    # ── 走势图 ────────────────────────────────────────────────
    chart_y = header_h + 10
    chart_h = 180
    chart_x = 10
    chart_w = width - 20

    prices = analysis.get("prices", [])
    dates  = analysis.get("dates", [])

    if len(prices) >= 2:
        base = prices[-1]
        norm = [p / base * 100 - 100 for p in prices]
        min_v = min(norm)
        max_v = max(norm)
        pad   = (max_v - min_v) * 0.08 or 1
        v_min = min_v - pad
        v_max = max_v + pad

        def to_xy(i, v):
            xi = chart_x + 5 + int(i / (len(norm)-1) * (chart_w-10))
            yi = chart_y + chart_h - int((v - v_min) / (v_max - v_min) * chart_h)
            return xi, yi

        draw.rectangle([chart_x, chart_y, chart_x+chart_w, chart_y+chart_h], fill=(248,250,255))

        for g in range(5):
            gy = chart_y + int(g/4*chart_h)
            draw.line([(chart_x, gy), (chart_x+chart_w, gy)], fill=C_GRID, width=1)
            gv = v_max - g/4*(v_max-v_min)
            draw.text((chart_x+3, gy-7), f"{gv:+.1f}%", fill=C_GRAY, font=font_sm)

        if v_min < 0 < v_max:
            y0 = chart_y + chart_h - int((0-v_min)/(v_max-v_min)*chart_h)
            draw.line([(chart_x, y0), (chart_x+chart_w, y0)], fill=(200,210,230), width=1)

        is_up = norm[-1] >= 0
        line_col = C_UP if is_up else C_DOWN
        poly = [to_xy(i, v) for i, v in enumerate(norm)]
        for i in range(len(poly)-1):
            draw.line([poly[i], poly[i+1]], fill=line_col, width=3)

        lx, ly = poly[-1]

        # ── 持仓买卖标记线 ────────────────────────────────────
        if position:
            buy_records = [r for r in position.get("records", []) if r["type"] == "buy"]
            sell_records = [r for r in position.get("records", []) if r["type"] == "sell"]

            for r in buy_records:
                bp = r["price"]
                if bp is None: continue
                # 换算为图表内的Y坐标
                bp_norm = bp / base * 100 - 100
                if v_min <= bp_norm <= v_max:
                    by = chart_y + chart_h - int((bp_norm - v_min) / (v_max - v_min) * chart_h)
                    draw.line([(chart_x, by), (chart_x+chart_w, by)], fill=(34, 197, 94), width=1)
                    draw.text((chart_x + 4, by - 14), f"买入@{bp:.4f}", fill=(34, 197, 94), font=font_sm)

            for r in sell_records:
                sp = r["price"]
                if sp is None: continue
                sp_norm = sp / base * 100 - 100
                if v_min <= sp_norm <= v_max:
                    sy = chart_y + chart_h - int((sp_norm - v_min) / (v_max - v_min) * chart_h)
                    draw.line([(chart_x, sy), (chart_x+chart_w, sy)], fill=(220, 38, 38), width=1, dash=(4,3))
                    draw.text((chart_x + 4, sy - 14), f"卖出@{sp:.4f}", fill=(220, 38, 38), font=font_sm)
        draw.ellipse([lx-4, ly-4, lx+4, ly+4], fill=line_col, outline=(255,255,255), width=1)
        draw.text((lx+7, ly-16), f"{norm[-1]:+.2f}%", fill=line_col, font=font_md)

        for di in range(min(5, len(dates))):
            idx = int(di/4*(len(norm)-1))
            if idx < len(dates):
                xd, _ = to_xy(idx, norm[idx])
                draw.text((xd-15, chart_y+chart_h+4), dates[idx][-5:], fill=C_GRAY, font=font_sm)

    # ── 指标卡片区 ────────────────────────────────────────────
    gap    = 6
    card_w = (width - 30) // 2
    card_h = 76
    card_y = chart_y + chart_h + 22

    # RSI
    _card(draw, 10, card_y, card_w, card_h)
    draw.text((18, card_y+7), "RSI (14)", fill=C_ACCENT, font=font_lg)
    rsi = analysis.get("rsi14")
    if rsi is not None:
        rsi_col = C_RSI_OVERBOUGHT if rsi > 70 else (C_RSI_OVERSOLD if rsi < 30 else C_RSI_NEUTRAL)
        _badge(draw, 18, card_y+28, f"{rsi:.1f}", rsi_col)
        draw.text((18, card_y+52), "70以上超买 / 30以下超卖", fill=C_GRAY, font=font_sm)
    else:
        draw.text((18, card_y+30), "数据不足", fill=C_GRAY, font=font_md)

    # KDJ
    _card(draw, 20+card_w, card_y, card_w, card_h)
    draw.text((28+card_w, card_y+7), "KDJ", fill=C_ACCENT, font=font_lg)
    k = analysis.get("kdj_k"); d = analysis.get("kdj_d"); jj = analysis.get("kdj_j")
    if k is not None:
        if jj > 80:   kdj_col = C_KDJ_SELL
        elif jj < 20: kdj_col = C_KDJ_BUY
        else:          kdj_col = C_KDJ_NEUTRAL
        draw.text((28+card_w, card_y+28), f"K={k:.1f}  D={d:.1f}  J={jj:.1f}", fill=C_TEXT, font=font_sm)
        lbl = "超买区" if jj > 80 else ("超卖区" if jj < 20 else "中性")
        _badge(draw, 28+card_w, card_y+50, lbl, kdj_col)
    else:
        draw.text((28+card_w, card_y+30), "数据不足", fill=C_GRAY, font=font_md)

    # MACD
    card_y2 = card_y + card_h + gap
    _card(draw, 10, card_y2, card_w, card_h)
    draw.text((18, card_y2+7), "MACD", fill=C_ACCENT, font=font_lg)
    dif = analysis.get("macd_dif"); dea = analysis.get("macd_dea"); hist = analysis.get("macd_hist")
    if dif is not None:
        macd_col = C_MACD_GOLDEN if dif > dea else (C_MACD_DEAD if dif < dea else C_MACD_NEUTRAL)
        draw.text((18, card_y2+28), f"DIF={dif:.4f}  DEA={dea:.4f}", fill=C_TEXT, font=font_sm)
        draw.text((18, card_y2+44), f"MACD柱={hist:.4f}", fill=macd_col, font=font_sm)
        lbl = "金叉" if dif > dea else ("死叉" if dif < dea else "中性")
        _badge(draw, 18, card_y2+64, lbl, macd_col)
    else:
        draw.text((18, card_y2+30), "数据不足", fill=C_GRAY, font=font_md)

    # 布林带
    _card(draw, 20+card_w, card_y2, card_w, card_h)
    draw.text((28+card_w, card_y2+7), "布林带 (20,2)", fill=C_ACCENT, font=font_lg)
    bu = analysis.get("boll_upper"); bm = analysis.get("boll_middle"); bl = analysis.get("boll_lower")
    if bu is not None:
        draw.text((28+card_w, card_y2+28), f"上轨={bu:.4f}  中轨={bm:.4f}", fill=C_TEXT, font=font_sm)
        draw.text((28+card_w, card_y2+44), f"下轨={bl:.4f}", fill=C_TEXT, font=font_sm)
        if latest_nav > bu:   pos="上轨上方";   pos_col=C_UP
        elif latest_nav < bl: pos="下轨下方";   pos_col=C_DOWN
        elif latest_nav > bm: pos="中轨上方";   pos_col=C_UP
        else:                  pos="中轨下方";   pos_col=C_DOWN
        _badge(draw, 28+card_w, card_y2+64, pos, pos_col)
    else:
        draw.text((28+card_w, card_y2+30), "数据不足", fill=C_GRAY, font=font_md)

    # ── 风险收益 + 阶段收益 ────────────────────────────────────
    row_y = card_y2 + card_h + gap + 5
    vol = analysis.get("volatility", 0)
    dd  = analysis.get("max_drawdown", 0)
    shp = analysis.get("sharpe_ratio", 0)

    _card(draw, 10, row_y, card_w, 72)
    draw.text((18, row_y+6), "📊 风险收益", fill=C_ACCENT, font=font_lg)
    draw.text((18, row_y+28), f"年化波动率  {vol:.2f}%", fill=C_TEXT, font=font_sm)
    draw.text((18, row_y+45), f"最大回撤  {dd:.2f}%   夏普比率  {shp:.2f}", fill=C_TEXT, font=font_sm)

    _card(draw, 20+card_w, row_y, card_w, 72)
    draw.text((28+card_w, row_y+6), "📅 阶段收益", fill=C_ACCENT, font=font_lg)
    rets = [("1W",analysis.get("return_1w")),("1M",analysis.get("return_1m")),
            ("3M",analysis.get("return_3m")),("6M",analysis.get("return_6m")),("1Y",analysis.get("return_1y"))]
    for i,(lbl,val) in enumerate(rets):
        if val is None: continue
        col = C_UP if val >= 0 else C_DOWN
        draw.text((28+card_w+(i%3)*95, row_y+24+(i//3)*18), f"{lbl}:{'+' if val>=0 else ''}{val:.1f}%", fill=col, font=font_sm)

    # ── 趋势 + 均线 ────────────────────────────────────────────
    row2_y = row_y + 77
    trend = analysis.get("trend", "—")
    trend_col = C_UP if "上升" in trend or "偏强" in trend else (C_DOWN if "下降" in trend or "偏弱" in trend else C_ACCENT)
    _card(draw, 10, row2_y, width-20, 44)
    draw.text((18, row2_y+10), "趋势研判", fill=C_ACCENT, font=font_md)
    draw.text((90, row2_y+8), trend, fill=trend_col, font=font_lg)
    ma5=analysis.get("ma5"); ma10=analysis.get("ma10"); ma20=analysis.get("ma20"); ma60=analysis.get("ma60")
    ma_txt = "  |  ".join([
        f"MA5={'%.4f'%ma5 if ma5 else '—'}",
        f"MA10={'%.4f'%ma10 if ma10 else '—'}",
        f"MA20={'%.4f'%ma20 if ma20 else '—'}",
        f"MA60={'%.4f'%ma60 if ma60 else '—'}",
    ])
    draw.text((18, row2_y+28), ma_txt, fill=C_GRAY, font=font_sm)

    # ── 底部免责 ───────────────────────────────────────────────
    footer_y = height - 24
    draw.rectangle([0, footer_y, width, height], fill=(240,243,250))
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    draw.text((15, footer_y+5),
              f"数据来源：东方财富  |  生成时间：{now_str}  |  仅供参考，不构成投资建议",
              fill=C_GRAY, font=font_sm)

    buf = BytesIO()
    img.save(buf, format="PNG", quality=90)
    return buf.getvalue()


# ─── 单基金独立走势图 ────────────────────────────────────────
def generate_single_fund_chart(
    nav_history: list,
    dates: list,
    ma5_data: list = None,
    ma10_data: list = None,
    ma20_data: list = None,
    width: int = 560,
    height: int = 220,
) -> bytes:
    if not PIL_AVAILABLE or len(nav_history) < 2:
        return b""

    font_sm = get_font(10)
    font_md = get_font(12)
    pad_l, pad_r, pad_t, pad_b = 10, 10, 10, 25
    cw = width - pad_l - pad_r
    ch = height - pad_t - pad_b

    img = Image.new("RGB", (width, height), C_BG)
    draw = ImageDraw.Draw(img)

    prices = nav_history
    base = prices[-1]
    norm = [p / base * 100 - 100 for p in prices]
    min_v, max_v = min(norm), max(norm)
    pad = (max_v - min_v) * 0.02 or 0.5
    v_min, v_max = min_v - pad, max_v + pad

    def to_xy(i, v):
        xi = pad_l + int(i/(len(norm)-1)*cw)
        yi = pad_t + ch - int((v-v_min)/(v_max-v_min)*ch)
        return xi, yi

    draw.rectangle([0, 0, width-1, height-1], fill=(248,250,255))
    for g in range(5):
        gy = pad_t + int(g/4*ch)
        draw.line([(pad_l, gy), (pad_l+cw, gy)], fill=C_GRID, width=1)
        gv = v_max - g/4*(v_max-v_min)
        draw.text((2, gy-6), f"{gv:+.1f}%", fill=C_GRAY, font=font_sm)

    if v_min < 0 < v_max:
        y0 = pad_t + ch - int((0-v_min)/(v_max-v_min)*ch)
        draw.line([(pad_l, y0), (pad_l+cw, y0)], fill=(200,210,230), width=1)

    is_up = norm[-1] >= 0
    line_col = C_UP if is_up else C_DOWN
    poly = [to_xy(i, v) for i, v in enumerate(norm)]
    for i in range(len(poly)-1):
        draw.line([poly[i], poly[i+1]], fill=line_col, width=3)

    lx, ly = poly[-1]
    draw.ellipse([lx-3, ly-3, lx+3, ly+3], fill=line_col, outline=(255,255,255), width=1)
    draw.text((lx+5, ly-14), f"{norm[-1]:+.2f}%", fill=line_col, font=font_md)

    # 日期标签放在图下方
    for di in range(min(6, len(dates))):
        idx = int(di / max(min(6,len(dates))-1, 1) * (len(norm)-1)) if min(6,len(dates))>1 else 0
        idx = min(idx, len(norm)-1)
        xd, _ = to_xy(idx, norm[idx])
        draw.text((xd-20, pad_t + ch + 8), dates[idx][-5:], fill=C_GRAY, font=font_sm)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ─── 多基金对比图 ────────────────────────────────────────────
def generate_combined_chart(funds_data: list, width: int = 1400, height: int = 900) -> Optional[bytes]:
    if not PIL_AVAILABLE or not funds_data:
        return None

    font_sm   = get_font(10)
    font_md   = get_font(12)
    font_lg   = get_font(15)
    font_head = get_font(17)

    HEADER_H  = 54
    MARGIN    = 20
    CHART_H   = 340   # 稍微压缩，给X轴日期留空间
    LEGEND_H  = 50
    CHART_GAP = 10    # 图表和图例之间的间距
    YAXIS_W   = 52    # Y轴标签区宽度（留给左侧百分比标签）
    XLABEL_H  = 24    # X轴日期标签区高度
    LEGEND_GAP = 10   # X轴标签和图例之间的间距
    TABLE_TOP = HEADER_H + CHART_H + LEGEND_H + CHART_GAP + XLABEL_H + LEGEND_GAP + 20
    TABLE_ROW = 32
    TABLE_HDR = 30
    TABLE_START = TABLE_TOP + TABLE_HDR + 8

    total_h = TABLE_START + len(funds_data) * TABLE_ROW + 30
    img = Image.new("RGB", (width, total_h), C_BG)
    draw = ImageDraw.Draw(img)

    # 浅色标题栏 + 蓝色顶条
    draw.rectangle([0, 0, width, 6], fill=(40, 90, 220))
    draw.rectangle([0, 6, width, HEADER_H], fill=C_HEADER)
    draw.text((MARGIN, 14), "📊 基金追踪对比分析", fill=(20, 30, 80), font=font_head)
    draw.text((width-240, 18), datetime.now().strftime("%Y-%m-%d %H:%M"), fill=(80,100,160), font=font_sm)

    # ── 叠加走势图 ────────────────────────────────────────────
    chart_x = MARGIN + YAXIS_W   # Y轴标签独立区
    chart_y = HEADER_H + 12
    chart_w = width - chart_x - MARGIN
    chart_h = CHART_H

    all_norm = []
    all_mins, all_maxs = [], []
    for fd in funds_data:
        prices = fd.get("prices", [])
        if len(prices) < 2:
            all_norm.append([])
            all_mins.append(0); all_maxs.append(0)
            continue
        base = prices[-1]
        norm = [p / base * 100 - 100 for p in prices]
        all_norm.append(norm)
        all_mins.append(min(norm)); all_maxs.append(max(norm))

    v_min = min(all_mins); v_max = max(all_maxs)
    pad   = (v_max - v_min) * 0.02 or 0.5   # 收紧边距，图表更紧凑
    v_min -= pad; v_max += pad
    n = len(all_norm[0]) if all_norm else 0

    def to_xy(i, v):
        xi = chart_x + int(i/(n-1)*chart_w)
        yi = chart_y + chart_h - int((v-v_min)/(v_max-v_min)*chart_h)
        return xi, yi

    draw.rectangle([chart_x, chart_y, chart_x+chart_w, chart_y+chart_h], fill=(248,250,255))

    for g in range(5):
        gy = chart_y + int(g/4*chart_h)
        draw.line([(chart_x, gy), (chart_x+chart_w, gy)], fill=C_GRID, width=1)
        gv = v_max - g/4*(v_max-v_min)
        draw.text((MARGIN, gy-7), f"{gv:+.1f}%", fill=C_GRAY, font=font_sm)

    if v_min < 0 < v_max:
        y0 = chart_y + chart_h - int((0-v_min)/(v_max-v_min)*chart_h)
        draw.line([(chart_x, y0), (chart_x+chart_w, y0)], fill=(200,210,230), width=1)

    # Y轴区和图表区的分隔线
    draw.line([(chart_x, chart_y), (chart_x, chart_y+chart_h)], fill=(180,200,230), width=1)

    COLORS = [
        (220, 38, 38), (34, 197, 94), (255, 152, 0),
        (0, 120, 220), (155, 60, 220), (100, 80, 200), (0, 160, 160)
    ]

    dates_ref = funds_data[0].get("dates", [])
    for i, (fd, norm) in enumerate(zip(funds_data, all_norm)):
        if len(norm) < 2:
            continue
        color = COLORS[i % len(COLORS)]
        poly = [to_xy(j, v) for j, v in enumerate(norm)]
        for j in range(len(poly)-1):
            draw.line([poly[j], poly[j+1]], fill=color, width=4)
        lx, ly = poly[-1]
        draw.text((lx-30, ly-18), f"{norm[-1]:+.1f}%", fill=color, font=font_sm)

    if dates_ref:
        label_count = min(6, n)
        xlabel_y = chart_y + chart_h + 14   # 图表下方单独一行
        # 分隔线
        draw.line([(chart_x, chart_y+chart_h), (chart_x+chart_w, chart_y+chart_h)], fill=(200,210,230), width=1)
        for di in range(label_count):
            idx = int(di / max(label_count - 1, 1) * (n - 1)) if label_count > 1 else 0
            idx = min(idx, n - 1)
            xd = chart_x + int(idx / max(n - 1, 1) * chart_w)
            draw.text((xd - 20, xlabel_y), dates_ref[idx][-5:], fill=C_GRAY, font=font_sm)

    # 图例（4列）— 单独一行，在X轴日期下方
    legend_y = chart_y + chart_h + XLABEL_H + LEGEND_GAP
    cols = 4
    col_w = width // cols
    for i, fd in enumerate(funds_data):
        color = COLORS[i % len(COLORS)]
        lx = (i % cols) * col_w + 10
        ly = legend_y + (i // cols) * 22
        draw.rectangle([lx, ly+2, lx+14, ly+14], fill=color)
        name = (fd.get("name") or fd["code"])[:12]
        draw.text((lx+18, ly), name, fill=C_TEXT, font=font_sm)

    # ── 数据表格 ──────────────────────────────────────────────
    headers   = ["基金名称","代码","最新净值","日涨跌","RSI(14)","趋势","夏普","波动率","最大回撤","近1月","近3月"]
    col_wdths = [220, 76, 88, 82, 72, 90, 58, 72, 76, 72, 72]
    col_xs = [MARGIN]
    for w in col_wdths[:-1]:
        col_xs.append(col_xs[-1] + w)

    draw.rectangle([0, TABLE_TOP, width, TABLE_TOP+TABLE_HDR], fill=(60, 100, 220))
    for h, cx in zip(headers, col_xs):
        draw.text((cx+4, TABLE_TOP+7), h, fill=(255,255,255), font=font_md)

    for ri, fd in enumerate(funds_data):
        ry = TABLE_START + ri * TABLE_ROW
        bg = (248, 250, 255) if ri % 2 == 0 else (255,255,255)
        draw.rectangle([0, ry, width, ry+TABLE_ROW-1], fill=bg)

        ana    = fd.get("analysis", {})
        change = fd.get("change", 0)
        ch_col = C_UP if change >= 0 else C_DOWN
        sign   = "+" if change >= 0 else ""
        rsi    = ana.get("rsi14")
        rsi_s  = f"{rsi:.1f}" if rsi is not None else "—"
        trend  = (ana.get("trend") or "—")[:6]
        shp    = f"{ana.get('sharpe_ratio', 0):.2f}"
        vol    = f"{ana.get('volatility', 0):.1f}%"
        dd     = f"{ana.get('max_drawdown', 0):.1f}%"
        r1m    = f"{'+' if ana.get('return_1m',0)>=0 else ''}{ana.get('return_1m',0):.1f}%" if ana.get('return_1m') is not None else "—"
        r3m    = f"{'+' if ana.get('return_3m',0)>=0 else ''}{ana.get('return_3m',0):.1f}%" if ana.get('return_3m') is not None else "—"

        vals = [
            (fd.get("name") or "—")[:16],
            fd.get("code", "—"),
            f"{fd.get('nav', 0):.4f}",
            f"{sign}{change:.2f}%",
            rsi_s,
            trend,
            shp,
            vol,
            dd,
            r1m,
            r3m,
        ]
        for vi, (v, cx) in enumerate(zip(vals, col_xs)):
            c = ch_col if vi == 3 else C_TEXT
            draw.text((cx+2, ry+8), v, fill=c, font=font_sm)

    buf = BytesIO()
    img.save(buf, format="PNG", quality=85)
    return buf.getvalue()


# ─── 单元测试 ────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from fund_api import fetch_otc_fund_valuation, fetch_otc_fund_history
    from technical import analyze_fund

    print("=== 测试图表生成 ===")
    val = fetch_otc_fund_valuation("161226")
    hist = fetch_otc_fund_history("161226", days=90)
    if val and hist:
        analysis = analyze_fund("161226", hist)
        # 加上 dates
        analysis["dates"] = [d["date"] for d in hist]
        img = generate_fund_analysis_image(
            fund_code="161226",
            fund_name=val.get("name","基金"),
            latest_nav=val.get("nav", hist[0]["nav"]),
            nav_change=val.get("est_change", 0),
            analysis=analysis,
        )
        if img:
            out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
            os.makedirs(out_dir, exist_ok=True)
            out = os.path.join(out_dir, "test_fund.png")
            with open(out, "wb") as f:
                f.write(img)
            print(f"✅ 图表已保存: {out} ({len(img)//1024} KB)")
        else:
            print("⚠️ 图表生成失败")
    else:
        print("⚠️ 获取数据失败")
