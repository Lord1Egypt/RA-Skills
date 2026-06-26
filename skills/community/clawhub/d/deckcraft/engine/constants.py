"""
DeckCraft v5 — Design Constants
Colors, typography, grid, and spacing for all built-in styles.
"""

from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor

# ── Slide Dimensions (16:9 default) ─────────────────────────────
SLIDE_WIDTH = Inches(10)
SLIDE_HEIGHT = Inches(5.625)

# ── Grid System (16:9 default) ─────────────────────────────────
MARGIN_LEFT = Inches(0.6)
MARGIN_RIGHT = Inches(0.6)
MARGIN_TOP = Inches(0.3)
MARGIN_BOTTOM = Inches(0.4)
CONTENT_WIDTH = SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT  # 8.8"
CONTENT_TOP = Inches(1.2)  # below title area

# ── Canvas Presets (v5.2+) ───────────────────────────────────
# Key format: "aspect_name" or explicit name
# Values: (width_in, height_in, ml, mr, mt, mb, content_top_in)
# ── Canvas Aliases (v6.0+) ──────────────────────────────────────
# Short aliases that map to actual canvas preset names.
CANVAS_ALIASES = {
    "xiaohongshu": "9:16",   # 小红书(竖屏 3:4 实际用 9:16 容器)
    "moments": "1:1",         # 朋友圈方形
    "weibo": "1:1",           # 微博方形(同 moments)
    "story": "9:16",          # Instagram/TikTok Story
    "reels": "9:16",          # 同 story
    "ppt": "16:9",            # 别名
    "mobile": "9:16",         # 移动竖屏
    "square": "1:1",          # 方形
}

CANVAS_PRESETS = {
    # 16:9 宽屏（默认）
    "16:9":  (10.0,   5.625,  0.6, 0.6, 0.3, 0.4, 1.2),
    # 9:16 竖屏（小红书/抖音/朋友圈）
    "9:16":  (5.625,  10.0,   0.4, 0.4, 0.3, 0.4, 1.0),
    # 1:1 方形（小红书方形/微信头像/Instagram）
    "1:1":   (7.5,    7.5,    0.5, 0.5, 0.3, 0.4, 1.0),
    # 4:3 传统（投影/老式）
    "4:3":   (10.0,   7.5,    0.6, 0.6, 0.3, 0.4, 1.2),
    # A4 打印 (landscape & portrait)
    "A4":    (11.69,  8.27,   0.6, 0.6, 0.3, 0.4, 1.2),
    "A4-portrait": (8.27, 11.69, 0.6, 0.6, 0.3, 0.4, 1.0),
    # 别名
    "ppt-16x9": (10.0, 5.625, 0.6, 0.6, 0.3, 0.4, 1.2),
}


def _resolve_canvas(name: str) -> str:
    """Resolve canvas alias to actual preset name."""
    return CANVAS_ALIASES.get(name, name)


def get_canvas(name="16:9"):
    """Return canvas config dict by name. Fallback to 16:9.
    
    Accepts both preset names and aliases (e.g. 'xiaohongshu' → '9:16').
    Returns dict with keys: width, height, margin_left, margin_right,
    margin_top, margin_bottom, content_width, content_top (all as Inches()).
    """
    name = _resolve_canvas(name)
    if name not in CANVAS_PRESETS:
        name = "16:9"
    w, h, ml, mr, mt, mb, ct = CANVAS_PRESETS[name]
    return {
        "name": name,
        "width": Inches(w),
        "height": Inches(h),
        "margin_left": Inches(ml),
        "margin_right": Inches(mr),
        "margin_top": Inches(mt),
        "margin_bottom": Inches(mb),
        "content_width": Inches(w - ml - mr),
        "content_top": Inches(ct),
        # 原始英寸值（供计算缩放因子）
        "width_in": w,
        "height_in": h,
    }


def list_canvases():
    """List all available canvas preset names (including aliases)."""
    return list(CANVAS_PRESETS.keys()) + list(CANVAS_ALIASES.keys())

# ── Typography ────────────────────────────────────────────────────
FONT_CN = "Noto Sans CJK SC"
FONT_EN_TITLE = "Arial"
FONT_EN_BODY = "Calibri"

TITLE_SIZE = Pt(28)
SUBTITLE_SIZE = Pt(18)
SECTION_HEADER_SIZE = Pt(22)
BODY_SIZE = Pt(14)
BODY_SMALL = Pt(12)
CAPTION_SIZE = Pt(10)
TABLE_HEADER_SIZE = Pt(12)
TABLE_BODY_SIZE = Pt(11)
STAT_NUMBER_SIZE = Pt(60)
STAT_LABEL_SIZE = Pt(12)

# ── Spacing ───────────────────────────────────────────────────────
GAP_LARGE = Inches(0.5)
GAP_MEDIUM = Inches(0.35)
GAP_SMALL = Inches(0.2)
ACCENT_LINE_HEIGHT = Inches(0.04)
TOP_BAR_HEIGHT = Inches(0.06)

# ── Built-in Color Themes ────────────────────────────────────────
THEMES = {
    "business": {
        "name": "Navy Professional",
        "primary": (30, 60, 114),
        "secondary": (70, 130, 180),
        "accent": (255, 193, 7),
        "text": (51, 51, 51),
        "text_light": (255, 255, 255),
        "text_muted": (120, 120, 120),
        "bg": (255, 255, 255),
        "bg_dark": (30, 60, 114),
        "card_bg": (240, 245, 250),
        "chart_colors": [(30, 60, 114), (70, 130, 180), (255, 193, 7),
                         (46, 139, 87), (178, 34, 34), (128, 0, 128)],
    },
    "business_dark": {
        "name": "Deep Navy",
        "primary": (20, 40, 80),
        "secondary": (50, 100, 160),
        "accent": (0, 180, 220),
        "text": (220, 220, 220),
        "text_light": (255, 255, 255),
        "text_muted": (150, 160, 180),
        "bg": (25, 35, 60),
        "bg_dark": (15, 25, 50),
        "card_bg": (35, 50, 80),
        "chart_colors": [(0, 180, 220), (50, 100, 160), (255, 193, 7),
                         (46, 139, 87), (220, 80, 60), (160, 120, 220)],
    },
    "tech": {
        "name": "Dark Tech",
        "primary": (26, 26, 46),
        "secondary": (0, 210, 255),
        "accent": (124, 58, 237),
        "text": (255, 255, 255),
        "text_light": (204, 204, 204),
        "text_muted": (130, 130, 160),
        "bg": (26, 26, 46),
        "bg_dark": (18, 18, 30),
        "card_bg": (37, 37, 64),
        "chart_colors": [(0, 210, 255), (124, 58, 237), (255, 107, 107),
                         (46, 213, 115), (255, 193, 7), (70, 130, 180)],
    },
    "tech_gradient": {
        "name": "Gradient Tech",
        "primary": (10, 10, 30),
        "secondary": (0, 150, 255),
        "accent": (120, 0, 255),
        "text": (255, 255, 255),
        "text_light": (180, 200, 255),
        "text_muted": (120, 140, 180),
        "bg": (15, 15, 40),
        "bg_dark": (5, 5, 20),
        "card_bg": (25, 30, 60),
        "chart_colors": [(0, 150, 255), (120, 0, 255), (255, 107, 107),
                         (46, 213, 115), (255, 193, 7), (70, 130, 180)],
    },
    "minimal": {
        "name": "Clean Gray",
        "primary": (80, 80, 80),
        "secondary": (150, 150, 150),
        "accent": (0, 120, 200),
        "text": (60, 60, 60),
        "text_light": (255, 255, 255),
        "text_muted": (140, 140, 140),
        "bg": (255, 255, 255),
        "bg_dark": (240, 240, 240),
        "card_bg": (245, 245, 245),
        "chart_colors": [(0, 120, 200), (80, 80, 80), (46, 139, 87),
                         (255, 152, 0), (178, 34, 34), (128, 0, 128)],
    },
    "elegant": {
        "name": "Gold & Black",
        "primary": (30, 30, 30),
        "secondary": (180, 150, 100),
        "accent": (212, 175, 55),
        "text": (240, 240, 240),
        "text_light": (255, 255, 255),
        "text_muted": (160, 150, 130),
        "bg": (35, 35, 35),
        "bg_dark": (20, 20, 20),
        "card_bg": (50, 50, 50),
        "chart_colors": [(212, 175, 55), (180, 150, 100), (255, 255, 255),
                         (46, 139, 87), (220, 80, 60), (100, 140, 200)],
    },
    "creative": {
        "name": "Purple Energy",
        "primary": (102, 45, 140),
        "secondary": (155, 89, 182),
        "accent": (241, 196, 15),
        "text": (51, 51, 51),
        "text_light": (255, 255, 255),
        "text_muted": (130, 110, 150),
        "bg": (255, 255, 255),
        "bg_dark": (102, 45, 140),
        "card_bg": (245, 235, 255),
        "chart_colors": [(102, 45, 140), (155, 89, 182), (241, 196, 15),
                         (46, 139, 87), (220, 80, 60), (0, 120, 200)],
    },
    "green": {
        "name": "Fresh Green",
        "primary": (30, 120, 80),
        "secondary": (80, 180, 120),
        "accent": (200, 230, 50),
        "text": (40, 60, 40),
        "text_light": (255, 255, 255),
        "text_muted": (100, 140, 110),
        "bg": (255, 255, 255),
        "bg_dark": (30, 100, 70),
        "card_bg": (235, 250, 240),
        "chart_colors": [(30, 120, 80), (80, 180, 120), (200, 230, 50),
                         (0, 120, 200), (220, 80, 60), (128, 0, 128)],
    },
    "red": {
        "name": "Bold Red",
        "primary": (180, 30, 30),
        "secondary": (220, 80, 60),
        "accent": (255, 200, 0),
        "text": (60, 30, 30),
        "text_light": (255, 255, 255),
        "text_muted": (160, 100, 100),
        "bg": (255, 255, 255),
        "bg_dark": (160, 20, 20),
        "card_bg": (255, 240, 235),
        "chart_colors": [(180, 30, 30), (220, 80, 60), (255, 200, 0),
                         (0, 120, 200), (46, 139, 87), (128, 0, 128)],
    },
    "ocean": {
        "name": "Ocean Teal",
        "primary": (0, 80, 120),
        "secondary": (0, 160, 180),
        "accent": (0, 220, 200),
        "text": (240, 250, 255),
        "text_light": (255, 255, 255),
        "text_muted": (100, 160, 180),
        "bg": (0, 60, 90),
        "bg_dark": (0, 40, 60),
        "card_bg": (0, 90, 130),
        "chart_colors": [(0, 220, 200), (0, 160, 180), (255, 193, 7),
                         (46, 139, 87), (220, 80, 60), (200, 200, 255)],
    },
}


def c(rgb_tuple):
    """Convert (R, G, B) tuple to RGBColor."""
    return RGBColor(*rgb_tuple)


def get_theme(name):
    """Get theme dict by name, fallback to business."""
    return THEMES.get(name, THEMES["business"])


# ── Industry Color Templates (v6.0+) ────────────────────────────
INDUSTRY_COLORS = {
    "finance":       {"primary": "#003366", "secondary": "#1A5490", "accent": "#D4AF37", "label": "金融/商务"},
    "tech":          {"primary": "#1565C0", "secondary": "#42A5F5", "accent": "#FF6B35", "label": "科技/互联网"},
    "healthcare":    {"primary": "#00796B", "secondary": "#4DB6AC", "accent": "#FFA726", "label": "医疗/健康"},
    "government":    {"primary": "#C41E3A", "secondary": "#E74C3C", "accent": "#FFD700", "label": "政务/政府"},
    "education":     {"primary": "#6A1B9A", "secondary": "#9C27B0", "accent": "#FFC107", "label": "教育"},
    "retail":        {"primary": "#E91E63", "secondary": "#F06292", "accent": "#FFEB3B", "label": "零售/电商"},
    "manufacturing": {"primary": "#37474F", "secondary": "#607D8B", "accent": "#FF9800", "label": "制造/工业"},
    "energy":        {"primary": "#FF6F00", "secondary": "#FFA726", "accent": "#1565C0", "label": "能源"},
    "media":         {"primary": "#7B1FA2", "secondary": "#AB47BC", "accent": "#00BCD4", "label": "媒体/娱乐"},
    "real_estate":   {"primary": "#5D4037", "secondary": "#8D6E63", "accent": "#FFB300", "label": "房地产"},
    "fashion":       {"primary": "#000000", "secondary": "#424242", "accent": "#FF4081", "label": "时尚/服饰"},
    "food":          {"primary": "#D84315", "secondary": "#FF7043", "accent": "#FFC107", "label": "餐饮/食品"},
    "travel":        {"primary": "#0277BD", "secondary": "#4FC3F7", "accent": "#FFA726", "label": "旅游/出行"},
    "consulting":    {"primary": "#1A237E", "secondary": "#3949AB", "accent": "#FFD600", "label": "咨询/MBB"},
}


def get_industry_theme(industry: str) -> dict:
    """获取行业配色,返回 dict 包含 primary/secondary/accent/label."""
    if industry not in INDUSTRY_COLORS:
        raise ValueError(f"Unknown industry: {industry}. Available: {list(INDUSTRY_COLORS.keys())}")
    return INDUSTRY_COLORS[industry]


def chart_colors(theme_name):
    """Get chart color list for a theme."""
    return THEMES.get(theme_name, THEMES["business"])["chart_colors"]
