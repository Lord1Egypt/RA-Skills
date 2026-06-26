"""
DeckCraft v6 Engine Package
"""
from .deck_engine import DeckEngine
from .chart_engine import (
    bar_chart, pie_chart, line_chart, gauge_chart,
    chart_funnel, chart_gantt, chart_swot, chart_porter, chart_sankey,
    chart_heatmap, chart_radar, chart_treemap, chart_waterfall,
)
from .constants import get_theme, THEMES, INDUSTRY_COLORS, get_industry_theme, CANVAS_ALIASES, list_canvases

# v5.3+: source importers (PDF, DOCX, TXT/MD → outline)
try:
    from . import importers  # noqa: F401
    from .importers import detect_and_import  # noqa: F401
except ImportError:
    pass

# v6.0+: icon library
try:
    from .icons import icon, ICON_NAMES  # noqa: F401
except ImportError:
    pass
