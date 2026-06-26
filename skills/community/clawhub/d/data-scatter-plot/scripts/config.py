# -*- coding: utf-8 -*-
"""
配置文件
"""

# 第22行（Result行）的索引（从0开始）
RESULT_ROW_INDEX = 21

# 固定行名称
MIN_LIMIT_ROW_NAME = "Min Limit"
MAX_LIMIT_ROW_NAME = "Max Limit"
RESULT_ROW_NAME = "Result"

# 列标题行索引（从0开始，默认第1行）
TITLE_ROW_INDEX = 0

# 散点图配置
SCATTER_PLOT_CONFIG = {
    "marker": "o",
    "marker_size": 50,
    "marker_color": "#1f77b4",  # 蓝色
    "limit_line_color": "#d62728",  # 红色
    "limit_line_style": "--",
    "limit_line_width": 2,
    "figure_size": (16, 9),  # 16:9 比例
    "dpi": 300
}

# Y轴标签行索引（从0开始），留空则从列标题中自动识别
Y_AXIS_LABEL_ROW = None

# 输出配置
DEFAULT_OUTPUT_DIR = "./plots"
DEFAULT_OUTPUT_FORMAT = "png"
