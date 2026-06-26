# 每日天气新闻推送配置文件
# 请根据需要修改以下配置

# 推送目标用户ID (飞书用户ID)
TARGET_USER="ou_3a0705a4c7b5f068fff0b2b719d37978"

# 推送地点 (用于天气查询)
LOCATION="广州市黄埔区"

# Tavily API密钥 (用于新闻搜索)
# 请使用环境变量 TAVILY_API_KEY 设置，例如：
# export TAVILY_API_KEY="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"
# 或添加到 ~/.bashrc 或 ~/.zshrc:
# echo 'export TAVILY_API_KEY="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"' >> ~/.bashrc
# source ~/.bashrc
TAVILY_API_KEY="${TAVILY_API_KEY:-}"

# 日志文件路径
LOG_FILE="/home/alanchan/.openclaw/workspace/daily_push.log"

# 推送时间配置 (cron格式)
# 默认为每天早上7:30
CRON_TIME="30 7 * * *"

# 天气API配置
WEATHER_API_BASE="https://api.open-meteo.com/v1/forecast"

# 广州市黄埔区经纬度坐标（更精确）
LATITUDE="23.1201"
LONGITUDE="113.3826"

# 新闻搜索配置 - 优化为更精准的中文国际新闻
NEWS_SOURCES="site:news.cn 国际新闻 最新 OR site:xinhuanet.com 国际新闻 最新 OR site:people.com.cn 国际新闻 最新 OR site:guancha.cn 国际新闻 OR site:thediplomat.com 中文"

# 推送内容模板
PUSH_TEMPLATE="🌅 每日天气和新闻推送 {date}
📍 {location}

🌦️ 天气情况：
{weather}

👔 穿衣建议：
{clothing_advice}

🌍 今日国际重要新闻：
{news}"

# 是否启用推送 (true/false)
ENABLE_PUSH="true"

# 测试模式 (true/false)
TEST_MODE="false"