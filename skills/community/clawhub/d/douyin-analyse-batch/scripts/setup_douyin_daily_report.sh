#!/bin/bash
# setup_douyin_daily_report.sh — 一键安装/重装抖音日报环境
set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$(dirname "$SKILL_DIR")"
VENV_DIR="/tmp/douyin_transcribe"
EMAIL_RECIPIENTS="${DOUYIN_EMAIL_RECIPIENTS:-3249331357@qq.com,1853026634@qq.com}"
DIGEST_LIMIT="${DOUYIN_DIGEST_LIMIT:-15}"

echo "=== 抖音日报环境安装 ==="

# 1. 创建虚拟环境
echo "[1/6] 创建 Python 虚拟环境..."
if [ -d "$VENV_DIR" ]; then
    echo "  虚拟环境已存在，跳过"
else
    /root/.local/bin/uv venv "$VENV_DIR" --python 3.12
fi
source "$VENV_DIR/bin/activate"

# 2. 安装依赖
echo "[2/6] 安装 Python 依赖..."
pip install --upgrade pip -q
pip install faster-whisper yt-dlp python-docx requests -q

# 3. 写入 .env 示例
echo "[3/6] 写入环境变量配置..."
ENV_FILE="$WORKSPACE_DIR/douyin-daily-report/.env"
cat > "$ENV_FILE" << 'EOF'
# SMTP 邮件（必填）
SMTP_USER=your_email@qq.com
SMTP_PASS=your_smtp授权码
SMTP_HOST=smtp.qq.com
SMTP_PORT=587

# 收件人（逗号分隔）
DOUYIN_EMAIL_RECIPIENTS=3249331357@qq.com,1853026634@qq.com

# 日报条数
DOUYIN_DIGEST_LIMIT=15

# Python 虚拟环境路径（自动检测，无需修改）
DOUYIN_VENV_PY=/tmp/douyin_transcribe/venv/bin/python3

# TikHub API Token（必填，写入 ~/.openclaw/config.json）
# 在 ~/.openclaw/config.json 中添加: "tikhub_api_token": "your_token"
EOF
echo "  环境变量示例已写入: $ENV_FILE"

# 4. 检查 TikHub Token
echo "[4/6] 检查 TikHub API Token..."
TIKHUB_TOKEN=""
if [ -f ~/.openclaw/config.json ]; then
    TIKHUB_TOKEN=$(python3 -c "import json; d=json.load(open('$HOME/.openclaw/config.json')); print(d.get('tikhub_api_token',''))" 2>/dev/null || echo "")
fi
if [ -z "$TIKHUB_TOKEN" ]; then
    echo "  警告: ~/.openclaw/config.json 中未找到 tikhub_api_token"
    echo "  请手动添加到 ~/.openclaw/config.json: {\"tikhub_api_token\": \"your_token\"}"
else
    echo "  Token 已配置 ✓"
fi

# 5. 设置 Cron 定时任务（08:00 和 16:00）
echo "[5/6] 设置 Cron 定时任务..."
CRON_WRAPPER="$SKILL_DIR/scripts/cron_daily_digest_wrapper.sh"
CRON_EXPR="0 8,16 * * *"
CRON_CMD="$CRON_EXPR  bash \"$CRON_WRAPPER\" $DIGEST_LIMIT >> /tmp/douyin_cron.log 2>&1"
(crontab -l 2>/dev/null | grep -v "douyin_daily_digest"; echo "$CRON_CMD") | crontab -
echo "  Cron 已设置: 每天 08:00 和 16:00 ✓"

# 6. 验证依赖
echo "[6/6] 验证 Python 依赖..."
source "$VENV_DIR/bin/activate"
python3 -c "import faster_whisper; import yt_dlp; import docx; import requests; print('  所有依赖 OK')" && echo "  依赖检查通过 ✓" || echo "  警告: 部分依赖导入失败"

echo ""
echo "=== 安装完成 ==="
echo ""
echo "下一步操作:"
echo "1. 编辑 ~/.openclaw/config.json，添加 TikHub Token:"
echo "   {\"tikhub_api_token\": \"your_token_from_tikhub.io\"}"
echo ""
echo "2. 编辑 $ENV_FILE，设置 SMTP 信息:"
echo "   SMTP_USER=你的QQ邮箱"
echo "   SMTP_PASS=QQ邮箱授权码"
echo ""
echo "3. 手动测试运行:"
echo "   bash $CRON_WRAPPER"
echo ""
echo "4. 查看日志:"
echo "   tail -f /tmp/douyin_cron.log"
