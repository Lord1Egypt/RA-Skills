# ============================================================
# 1688 Data Claw - Linux 环境变量
# Source: source ./env.sh
# ============================================================

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPTS_DIR")"

export CHROME="$SKILL_DIR/chromium/chrome-linux64/chrome"
export USER_DATA="/tmp/chromium"
export EXT_DIR="$SKILL_DIR/plugin"
export CDP_PORT=9222
export OUTPUT_DIR="$SKILL_DIR"
export SCREEN=1920x1080x24
export DISPLAY=:99

# --- 飞书（部署时填入：实际使用的群聊 chat_id，oc_ 开头）---
export FEISHU_CHAT_ID=""

# --- 飞书应用凭证（部署时填入，push_feishu_post.py 直接调飞书 open API 需要）---
export FEISHU_APP_ID=""
export FEISHU_APP_SECRET=""