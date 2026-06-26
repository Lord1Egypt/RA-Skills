"""
Shared chart style for A-share analyzer.
Dark theme, yellow main line for target stock, red-up-green-down (A-share convention).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os
import sys


# === Color palette ===
BG_COLOR = "#1a2332"          # dark navy background
GRID_COLOR = "#2a3544"        # subtle grid
TEXT_COLOR = "#d0d5dc"        # soft white text
FG_MUTED = "#8892a0"          # muted labels

# A-share convention: red = up, green = down
UP_COLOR = "#e74c3c"          # red (涨)
DOWN_COLOR = "#2ecc71"        # green (跌)

# Target stock highlight
TARGET_COLOR = "#f5c518"      # vivid yellow

# Moving averages
MA5_COLOR = "#f5c518"         # yellow
MA10_COLOR = "#e74c3c"        # red/pink
MA20_COLOR = "#1abc9c"        # teal
MA60_COLOR = "#9b6dd7"        # purple

# Peer comparison palette (for 3-5 peers + index)
PEER_PALETTE = [
    "#1abc9c",   # teal
    "#e67e8a",   # salmon pink
    "#9b6dd7",   # purple
    "#3498db",   # blue
    "#f39c12",   # orange
]
INDEX_COLOR = "#8892a0"       # grey dashed for CSI 300

# Bollinger bands
BB_COLOR = "#8892a0"          # grey

# MACD
MACD_DIF_COLOR = "#f5c518"    # yellow
MACD_DEA_COLOR = "#1abc9c"    # teal


def setup_chinese_font():
    """Register Chinese fonts. Falls back gracefully if none found."""
    candidates = [
        "Noto Sans CJK SC",
        "Noto Sans CJK TC",
        "WenQuanYi Micro Hei",
        "WenQuanYi Zen Hei",
        "SimHei",
        "Microsoft YaHei",
        "PingFang SC",
        "Heiti SC",
        "Source Han Sans SC",
        "Source Han Sans CN",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    picked = None
    for name in candidates:
        if name in available:
            picked = name
            break

    if picked:
        plt.rcParams["font.sans-serif"] = [picked] + plt.rcParams["font.sans-serif"]
    else:
        # Try to load common Linux locations
        for path in [
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            # Windows paths
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/msyhbd.ttc",
        ]:
            if os.path.exists(path):
                font_manager.fontManager.addfont(path)
                try:
                    prop = font_manager.FontProperties(fname=path)
                    name = prop.get_name()
                    plt.rcParams["font.sans-serif"] = [name] + plt.rcParams["font.sans-serif"]
                    picked = name
                    break
                except Exception:
                    continue

    plt.rcParams["axes.unicode_minus"] = False
    if not picked:
        print("[chart_style] WARN: no Chinese font found; labels may render as tofu.",
              file=sys.stderr)
    return picked


def apply_dark_style(fig, axes):
    """Apply dark-theme cosmetics to a figure and its axes."""
    fig.patch.set_facecolor(BG_COLOR)
    if not hasattr(axes, "__iter__"):
        axes = [axes]
    for ax in axes:
        ax.set_facecolor(BG_COLOR)
        ax.tick_params(colors=TEXT_COLOR, labelsize=9)
        for spine in ax.spines.values():
            spine.set_color(GRID_COLOR)
        ax.grid(True, color=GRID_COLOR, alpha=0.4, linewidth=0.6)
        ax.yaxis.label.set_color(TEXT_COLOR)
        ax.xaxis.label.set_color(TEXT_COLOR)
        if ax.get_title():
            ax.title.set_color(TEXT_COLOR)


def style_legend(legend):
    """Apply dark theme to a legend."""
    if legend is None:
        return
    legend.get_frame().set_facecolor(BG_COLOR)
    legend.get_frame().set_edgecolor(GRID_COLOR)
    legend.get_frame().set_alpha(0.85)
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)
