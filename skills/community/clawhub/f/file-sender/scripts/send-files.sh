#!/bin/bash
# =============================================================================
# send-files.sh — 打包 workspace 中的文件并通知 Manager
#
# 用法: send-files.sh <源路径> <描述文本>
#
# 设计: 本地持久化优先，通知失败不影响文件安全
#   1. 文件始终先落盘到 .file-outbox/
#   2. 向 Manager 发送轻量通知 (仅元数据, 不传文件)
#   3. Manager 收到通知后由定时任务主动从 Agent 拉取文件
#   4. 通知失败也没关系: 文件安全在磁盘, Manager 定时任务兜底
#
# 环境变量 (实例创建时由 Manager 注入到 openclaw.env):
#   OPENCLAW_INSTANCE_NAME    — 实例名称 (如 openclaw-9d95e5c2)
#   OPENCLAW_MANAGER_URL      — File Push 服务地址
#   OPENCLAW_FILE_PUSH_TOKEN  — 实例专属文件推送 Token (非 Agent Key)
# =============================================================================

set -euo pipefail

SOURCE_PATH="${1:?用法: send-files.sh <源路径> <描述文本>}"
DESCRIPTION="${2:?缺少描述文本}"

WORKSPACE_PREFIX="/home/node/workspace"
OUTBOX="$WORKSPACE_PREFIX/.file-outbox"

# ── 路径安全校验 ──
REAL_PATH=$(readlink -f "$SOURCE_PATH" 2>/dev/null || echo "")
[ -z "$REAL_PATH" ] && { echo "❌ 路径不存在: $SOURCE_PATH"; exit 1; }
[[ "$REAL_PATH" != "$WORKSPACE_PREFIX"* ]] && { echo "❌ 仅允许 $WORKSPACE_PREFIX 下的文件"; exit 1; }
[[ "$REAL_PATH" == "$OUTBOX"* ]] && { echo "❌ 不能发送 .file-outbox 目录"; exit 1; }
[ ! -e "$REAL_PATH" ] && { echo "❌ 路径不存在: $SOURCE_PATH"; exit 1; }

# ── 环境变量检查 ──
: "${OPENCLAW_INSTANCE_NAME:?OPENCLAW_INSTANCE_NAME 未设置}"
: "${OPENCLAW_MANAGER_URL:?OPENCLAW_MANAGER_URL 未设置}"
: "${OPENCLAW_FILE_PUSH_TOKEN:?OPENCLAW_FILE_PUSH_TOKEN 未设置}"

# ── 打包 ──
mkdir -p "$OUTBOX"
FILE_ID=$(date +%Y%m%d%H%M%S)_$(head -c 4 /dev/urandom | od -An -tx1 | tr -d ' \n')
ZIP_PATH="$OUTBOX/${FILE_ID}.zip"
DESC_PATH="$OUTBOX/${FILE_ID}.txt"

echo "📦 正在打包文件..."
if [ -f "$REAL_PATH" ]; then
    (cd "$(dirname "$REAL_PATH")" && zip -q "$ZIP_PATH" "$(basename "$REAL_PATH")")
    ORIGINAL_NAME=$(basename "$REAL_PATH")
elif [ -d "$REAL_PATH" ]; then
    (cd "$(dirname "$REAL_PATH")" && zip -qr "$ZIP_PATH" "$(basename "$REAL_PATH")")
    ORIGINAL_NAME=$(basename "$REAL_PATH")
else
    echo "❌ 不支持的文件类型"; exit 1
fi

# 大小限制 500MB
ZIP_SIZE=$(stat -c%s "$ZIP_PATH" 2>/dev/null || echo "0")
if [ "$ZIP_SIZE" -gt $((500 * 1024 * 1024)) ]; then
    echo "❌ 文件过大: $(( ZIP_SIZE / 1024 / 1024 ))MB (上限 500MB)"
    rm -f "$ZIP_PATH"
    exit 1
fi

echo "$DESCRIPTION" > "$DESC_PATH"
echo "   文件ID: $FILE_ID | 大小: $(( ZIP_SIZE / 1024 ))KB"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ☑ 到此文件已安全落盘, 后续通知失败不影响文件安全
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 构建通知 payload (仅元数据, 不含文件本体)
# zip_path 使用容器内绝对路径, Manager 拉取时直接使用
# description 字段使用 python3 做 JSON 转义，python3 不可用时做基础转义
if command -v python3 &>/dev/null; then
    DESC_JSON=$(echo "$DESCRIPTION" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
else
    DESC_ESCAPED=$(echo "$DESCRIPTION" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr '\n' ' ')
    DESC_JSON="\"${DESC_ESCAPED}\""
fi

NOTIFY_PAYLOAD=$(cat <<EOF
{
  "file_id": "${FILE_ID}",
  "zip_path": "/home/node/workspace/.file-outbox/${FILE_ID}.zip",
  "original_name": "${ORIGINAL_NAME}",
  "size_bytes": ${ZIP_SIZE},
  "description": ${DESC_JSON}
}
EOF
)

echo "📤 正在通知 Manager..."

# ── 发送轻量通知 (使用实例专属 Token, 非全局 Agent Key) ──
HTTP_CODE=$(curl -s -o /tmp/notify_resp.json -w "%{http_code}" \
    -X POST "${OPENCLAW_MANAGER_URL}/file-push/v1/instances/${OPENCLAW_INSTANCE_NAME}/file-ready" \
    -H "Authorization: Bearer ${OPENCLAW_FILE_PUSH_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$NOTIFY_PAYLOAD" \
    --connect-timeout 5 \
    --max-time 15 \
    2>/dev/null)

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "✅ 通知成功！文件将自动发送给用户。"
elif [ "$HTTP_CODE" = "409" ]; then
    echo "✅ 文件已登记 (重复通知)，将自动发送给用户。"
else
    if [ "$HTTP_CODE" = "000" ]; then
        echo "⚠️  无法连接到 Manager，文件已安全保存在本地。"
    else
        RESP=$(cat /tmp/notify_resp.json 2>/dev/null || echo "无")
        echo "⚠️  通知失败 (HTTP $HTTP_CODE): $RESP"
    fi
    echo "   系统会自动重试发送，用户最终一定会收到文件。"
fi

rm -f /tmp/notify_resp.json
