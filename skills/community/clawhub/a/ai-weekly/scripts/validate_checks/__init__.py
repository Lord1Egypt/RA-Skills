# validate_checks/__init__.py — 子包公开 API（供 validate_report.py 薄入口复用）
from .common import (_detect_format, check_file_exists, check_data_sources, _extract_js_var)
from .news_v3 import (
    check_news_v3, check_editorial_c0, check_editorial_c1, check_search_v3,
    check_charts_v3, _extract_balanced_brace, check_ranking_v3,
    _extract_leaderboard_data, check_leaderboard_quality, _fallback_leaderboard_quality,
)
from .v2 import (check_news_v2, check_kpi_v2, check_charts_v2)
from .market import (
    check_market_disclaimer, check_market_signals, check_market_structure,
    check_trend_evidence, check_market_data, check_en_cn_summary, check_market_signals_cn,
)
from .keywords import (
    check_empty_category_tabs, check_keyword_filter, check_keyword_clustering,
    check_weekly_dashboard, check_xss_safe,
)
from .source import (_iter_source_files, check_no_bare_except, check_iso8601, check_module_size)
from .constraints import check_constraints

__all__ = [
    "_detect_format", "check_file_exists", "check_data_sources", "_extract_js_var",
    "check_news_v3", "check_editorial_c0", "check_editorial_c1", "check_search_v3",
    "check_charts_v3", "_extract_balanced_brace", "check_ranking_v3",
    "_extract_leaderboard_data", "check_leaderboard_quality", "_fallback_leaderboard_quality",
    "check_news_v2", "check_kpi_v2", "check_charts_v2",
    "check_market_disclaimer", "check_market_signals", "check_market_structure",
    "check_trend_evidence", "check_market_data", "check_en_cn_summary", "check_market_signals_cn",
    "check_empty_category_tabs", "check_keyword_filter", "check_keyword_clustering",
    "check_weekly_dashboard", "check_xss_safe",
    "_iter_source_files", "check_no_bare_except", "check_iso8601", "check_module_size",
    "check_constraints",
]
