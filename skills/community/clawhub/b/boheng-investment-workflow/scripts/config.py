#!/usr/bin/env python3
"""
投资研究系统 - 统一配置
集中管理所有路径和参数

版本: 1.2.5 (新增AKShare支持)

安全说明：
- 仅访问白名单域名
- 数据存储在 ~/.openclaw/workspace/investment/
- 不执行任何系统命令或敏感操作
- AKShare 为可选依赖，启用方式: --akshare

数据源说明：
- 基础模式（默认）：腾讯财经API，部分财务数据为估算值
- AKShare模式（--akshare）：真实财报数据，需 pip install akshare
"""
import os
import sys

# ===========================================
# 📁 数据存储配置
# ===========================================

# 主数据目录（统一使用 workspace 目录）
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/investment")

# 自选股文件
WATCHLIST_FILE = os.path.join(DATA_DIR, "watchlist.txt")

# 分析报告目录
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

# 确保目录存在
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# ===========================================
# 🔌 数据源配置
# ===========================================

# 数据源模式配置
# 可选值: "tencent" (基础模式) | "akshare" (真实财务数据)
DATA_SOURCE_MODE = os.getenv("INVESTMENT_DATA_SOURCE", "tencent")

# 数据源优先级（按此顺序尝试）
DATA_SOURCES_PRIORITY = ["tencent", "akshare"]

# 外部数据源域名白名单
ALLOWED_DOMAINS = [
    "qt.gtimg.cn",         # 腾讯财经（主数据源）
    "web.ifzq.gtimg.cn",   # 腾讯财经子域名（K线数据）
    "push2.eastmoney.com", # 东方财富（AKShare使用）
    "stock.xueqiu.com",    # 雪球（AKShare使用）
    "finance.sina.com.cn", # 新浪财经（AKShare使用）
]

# AKShare配置
AKSHARE_OPTIONAL = True  # True=可选, False=强制
AKSHARE_CACHE_HOURS = 24  # 缓存时间（小时）

# Tushare配置（可选，备用数据源）
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")

# ===========================================
# ⏱️ 网络请求配置
# ===========================================

# 请求间隔（秒），避免被反爬
REQUEST_DELAY = 1.0

# 超时时间（秒）
REQUEST_TIMEOUT = 10

# 最大重试次数
MAX_RETRIES = 3

# ===========================================
# 👥 分析师权重配置
# ===========================================

ANALYST_WEIGHTS = {
    "宏观经济分析师": 1.0,
    "行业研究员": 1.5,
    "基本面分析师": 1.5,
    "技术分析师": 1.0,
    "风险控制师": 1.2,
    "量化分析师": 1.0,
    "情绪分析师": 0.8,
    "估值分析师": 1.2,
}

# 投票选项
VOTE_BUY = "✅"       # 建议投资
VOTE_CAUTION = "⚠️"   # 谨慎投资
VOTE_SELL = "❌"      # 不建议投资

# ===========================================
# 📊 行业分类
# ===========================================

INDUSTRY_CATEGORIES = {
    "银行": ["银行", "商业银行", "股份制银行", "城商行"],
    "地产": ["房地产", "地产开发", "物业管理"],
    "科技": ["半导体", "软件", "互联网", "人工智能"],
    "消费": ["食品饮料", "家电", "零售", "餐饮"],
    "医药": ["制药", "生物科技", "医疗器械"],
    "新能源": ["光伏", "锂电", "风电", "储能"],
    "金融": ["证券", "保险", "信托"],
    "制造": ["机械", "汽车", "军工", "化工"],
}

# ===========================================
# 📈 估值分位参考
# ===========================================

VALUATION_LEVELS = {
    (0, 20): "严重低估",
    (20, 40): "偏低",
    (40, 60): "合理",
    (60, 80): "偏高",
    (80, 100): "严重高估",
}