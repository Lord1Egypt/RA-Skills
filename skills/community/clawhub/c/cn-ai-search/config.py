# 配置文件 - cn-ai-search 中文AI聚合搜索

# ------------------------------
# 必填配置 - 基础功能开箱即用，不需要额外配置
# TAVILY_API_KEY已经预配置好了，可以直接使用AI总结功能
# ------------------------------

# Tavily AI搜索（开启AI总结需要）
TAVILY_API_KEY = "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"

# Jina Reader API（网页抓取需要）
JINA_API_KEY = "jina_693dbc2621db4af29c3bf7b360b9477c3lN0Es8VoqzAkebJxC2HhTeLzkBB"

# ------------------------------
# 搜索默认配置
# ------------------------------

# 支持的平台
SUPPORTED_PLATFORMS = [
    "baidu",        # 百度搜索
    "bing_cn",      # 必应中国
    "360",          # 360搜索
    "sogou",        # 搜狗
    "weixin",       # 微信公众号（搜狗）
    "toutiao",      # 头条
    "jisilu",       # 集思录
    "zhihu",        # 知乎
    "bilibili",     # B站
    "xiaohongshu",  # 小红书（需要配置mcporter）
    "weibo",         # 微博
    "douyin"         # 抖音
]

# 默认搜索平台（开箱即用，不需要配置小红书就能用）
DEFAULT_PLATFORMS = ["baidu", "weixin", "zhihu", "bilibili"]

# 每个平台返回结果数量
DEFAULT_RESULTS_PER_PLATFORM = 5

# 最大返回结果总数
MAX_RESULTS_TOTAL = 20

# 默认排序方式: relevance(最相关) / hot(最热)
DEFAULT_SORT = "relevance"
