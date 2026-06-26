# 配置说明

## 快速开始（推荐）

首次安装推荐使用交互式配置向导：

```bash
cd scripts
python init_config.py
```

按提示回答几个问题，自动生成 `config.py`。

## 配置项说明

```python
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
RECEIVER_ID = "xxx"

# ========== 分类名称配置（可选） ==========
# 自定义早报分类，默认为：
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
# **智能模式（推荐）：留空列表 `[]`**
# AI会自动根据你配置的领域，分析判断该领域有哪些优质核心信息源，无需用户记忆
# 
# 如果有特别想要优先的信息源，可以手动列出：
# 大健康领域: ["WHO官网", "NEJM", "柳叶刀", "顶级医学期刊", "国际医药论坛", "FDA官网"]
# AI领域: ["Twitter", "GitHub", "Hugging Face", "arXiv", "科技媒体"]
# 区块链: ["CoinDesk", "CoinTelegraph", "Twitter", "GitHub"]
# 金融: ["华尔街见闻", "财新", "路透社", "Bloomberg"]
SOURCE_PRIORITY = []

# 是否优先保留指定来源的信息
PREFER_PRIORITY_SOURCES = True

# ========== 定时任务配置（cron格式）==========
# 北京时间每日8:30: 30 8 * * *
# 北京时间每日9:00: 0 9 * * *
SCHEDULE_CRON = "30 8 * * *"
```

## 各渠道说明

### 企业微信 (wecom)

企业微信渠道使用 `wecom_mcp` 工具发送，需要确保：

1. `wecom_mcp` 已加入工具白名单
2. 企业微信已正确配置 MCP Server

### 飞书 (feishu)

飞书渠道使用飞书 IM 接口发送：

1. 需要飞书 OAuth 授权
2. `RECEIVER_ID` 格式：单聊为 `ou_xxx` (open_id)，群聊为 `oc_xxx` (chat_id)

### Webhook

通用 Webhook 渠道，向指定 URL 发送 POST 请求：

请求体格式：
```json
{
  "domain": "领域名称",
  "title": "早报标题",
  "text": "早报完整内容（Markdown）",
  "date": "YYYY-MM-DD",
  "timestamp": 1234567890
}
```

## 完整配置示例

### 企业微信单聊，AI领域，每日8:30

```python
NEWS_DOMAIN = "AI人工智能"
DOMAIN_NAME = "AI"
CHANNEL_TYPE = "wecom"
RECEIVER_ID = "YeFeng"
WECOM_CHAT_TYPE = 1
SCHEDULE_CRON = "30 8 * * *"
```

### 飞书群聊，区块链领域，每日9:00

```python
NEWS_DOMAIN = "区块链 加密货币"
DOMAIN_NAME = "区块链"
CHANNEL_TYPE = "feishu"
RECEIVER_ID = "oc_xxxxxxxxx"
FEISHU_RECEIVE_ID_TYPE = "chat_id"
SCHEDULE_CRON = "0 9 * * *"
```
