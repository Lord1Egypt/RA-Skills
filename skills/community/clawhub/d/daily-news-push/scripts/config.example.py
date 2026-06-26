"""
通用每日早报配置文件
运行 `python init_config.py` 可以交互式生成，也可以手动修改此文件
复制此文件为 config.py 然后修改以下配置
"""

# ========== 核心配置 ==========

# 关注的领域
# 例如：AI人工智能, 区块链, 生物医药, 互联网科技, 金融财经...
NEWS_DOMAIN = "AI人工智能"

# 领域名称（用于标题显示）
DOMAIN_NAME = "AI"

# 推送渠道类型
# 可选值: wecom (企业微信), feishu (飞书), webhook (通用Webhook)
CHANNEL_TYPE = "wecom"

# 接收人ID
# - wecom: 单聊时为 userid，群聊时为群ID
# - feishu: 单聊时为 open_id (ou_xxx)，群聊时为 chat_id (oc_xxx)
# - webhook: 不需要此项，看下方 WEBHOOK_* 配置
RECEIVER_ID = "YeFeng"

# ========== 分类名称配置（可选） ==========
# 自定义早报分类名称
CATEGORY_NAMES = {
    "headline": "头条",
    "international": "国际动态",
    "domestic": "国内动态",
    "academic": "深度/学术",
    "observation": "今日观察"
}

# ========== 企业微信额外配置 ==========
# 会话类型: 1-单聊，2-群聊
WECOM_CHAT_TYPE = 1

# ========== 飞书额外配置 ==========
# 接收人ID类型: open_id (单聊), chat_id (群聊)
FEISHU_RECEIVE_ID_TYPE = "open_id"

# ========== Webhook 额外配置 ==========
# WEBHOOK_URL = "https://your-webhook-url.com"
# WEBHOOK_HEADERS = {
#     "Content-Type": "application/json",
#     "Authorization": "Bearer your-token"
# }

# ========== 内容配置 ==========

# 每条分类最大条数
MAX_NEWS_PER_CATEGORY = {
    "international": 3,  # 国际动态
    "domestic": 3,       # 国内动态
    "academic": 2        # 深度/学术
}

# 是否每条都必须有来源链接
REQUIRE_SOURCE_LINK = True

# ========== 信息源优先级配置 ==========
# 根据不同领域，优先推荐优质信息源
# AI会优先从这些来源抓取信息
# 
# 留空列表 `[]` 表示：**让AI自动判断**
# AI会根据你配置的领域，自行分析该领域有哪些优质核心信息源，智能选择
# 
# 如果有特别想要优先的信息源，可以手动列出：
# 大健康领域示例: ["WHO官网", "NEJM", "柳叶刀", "顶级医学期刊", "FDA官网"]
# AI领域示例: ["Twitter", "GitHub", "Hugging Face", "arXiv"]
# 区块链领域示例: ["CoinDesk", "CoinTelegraph", "Twitter"]
# 金融领域示例: ["华尔街见闻", "财新", "路透社", "Bloomberg"]
SOURCE_PRIORITY = []

# 是否优先保留指定来源的信息（开启后质量更高）
PREFER_PRIORITY_SOURCES = True

# ========== 定时任务配置（cron格式，北京时间）==========
# 北京时间每日8:30: 30 8 * * *
# 北京时间每日9:00: 0 9 * * *
SCHEDULE_CRON = "30 8 * * *"
