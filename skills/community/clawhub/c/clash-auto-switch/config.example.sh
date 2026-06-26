# Clash Auto Switch 配置

# API 配置
CLASH_API="http://127.0.0.1:58871"
CLASH_SECRET="your-secret-here"
PROXY_URL="http://127.0.0.1:7890"

# 测试目标 (用逗号分隔)
TEST_TARGETS="https://api.telegram.org,https://api.anthropic.com,https://www.google.com,https://api.openai.com"

# 健康检查阈值 (百分比)
HEALTH_THRESHOLD=60

# 优先区域 (用逗号分隔)
PREFERRED_REGIONS="新加坡,香港,日本,美国"

# 日志文件
LOG_FILE="/var/log/clash-switch.log"

# 状态文件
STATE_FILE="/tmp/clash-switch-state.json"

# 切换后等待秒数
WAIT_AFTER_SWITCH=5

# 测试超时 (秒)
TEST_TIMEOUT=5
