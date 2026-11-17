#!/usr/bin/env python
"""Publication-style matplotlib setup for report figures (Chinese + English).

    from fig_style import setup, save, BLUE, DARK, LBLUE, GRAY, RED

    fig = setup(width_cm=14.5, height_cm=8.6)   # 14.5 cm = usual text width
    ax = fig.add_subplot(111)
    ...
    save(fig, "figs/fig2.png")

Design defaults: Times New Roman digits with SimSun Chinese, 9 pt base size,
no top/right spines, light horizontal grid, 300 dpi, tight bounding box.
"""

import os
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

EN_FONT = "Times New Roman"
CN_FONT = "SimSun"

BLUE = "#2E5A88"
DARK = "#1F3A56"
LBLUE = "#9DB7D0"
GRAY = "#8C8C8C"
RED = "#A34A3F"
GRID = "#D9D9D9"


def _register_fonts():
    """Register Windows/Linux font files when the family name is not installed."""
    candidates = [
        (r"C:\Windows\Fonts\time.ttf", r"C:\Windows\Fonts\times.ttf"),
        (r"C:\Windows\Fonts\simsun.ttc",),
        ("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",),
        ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",),
    ]
    for group in candidates:
        for path in group:
            if os.path.exists(path):
                try:
                    font_manager.fontManager.addfont(path)
                except Exception:
                    pass


def setup(width_cm=14.5, height_cm=None, base_pt=9.0, grid_axis="y"):
    _register_fonts()
    if height_cm is None:
        height_cm = width_cm * 0.62
    plt.rcParams.update({
        "font.family": [EN_FONT, CN_FONT],
        "font.size": base_pt,
        "axes.labelsize": base_pt,
        "axes.titlesize": base_pt + 1,
        "xtick.labelsize": base_pt - 0.5,
        "ytick.labelsize": base_pt - 0.5,
        "legend.fontsize": base_pt - 0.5,
        "axes.unicode_minus": False,
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": grid_axis is not None,
        "axes.grid.axis": grid_axis or "y",
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "axes.axisbelow": True,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "savefig.dpi": 300,
        "figure.dpi": 100,
    })
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return plt.figure(figsize=(width_cm / 2.54, height_cm / 2.54))


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.02, dpi=300)
    plt.close(fig)
    print("wrote", path)


def label_bars(ax, bars, fmt="{:.0f}", dy=0.02, color="#222222", size=None):
    """Write the value above each bar (keeps the chart readable without a table)."""
    top = ax.get_ylim()[1]
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h + top * dy, fmt.format(h),
                ha="center", va="bottom", color=color,
                fontsize=size if size else plt.rcParams["font.size"] - 0.5)

