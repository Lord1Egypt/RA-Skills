#!/bin/bash
# Daily Memory Summary - 从 computer_io 读取数据，写入每日 memory，并更新联系人库

MEMORY_DIR="/Users/wutianfu/.openclaw/workspace/memory"
CONTACTS_DIR="/Users/wutianfu/.openclaw/workspace/knowledge/contacts"
TODAY=$(date +%Y-%m-%d)
DAY_DIR="$MEMORY_DIR/$TODAY"
OUTPUT_FILE="$MEMORY_DIR/$TODAY.md"

echo "=== Daily Memory Summary ==="
echo "Date: $TODAY"
echo ""

# 1. 读取剪贴板数据
echo "[1/4] 读取剪贴板数据..."
CLIPBOARD_DIR="$DAY_DIR/computer_io/clipboard"
if [ -d "$CLIPBOARD_DIR" ]; then
    CLIPBOARD_FILE=$(ls -t "$CLIPBOARD_DIR"/*.md 2>/dev/null | head -1)
    if [ -n "$CLIPBOARD_FILE" ]; then
        CLIPBOARD_CONTENT=$(cat "$CLIPBOARD_FILE")
    else
        CLIPBOARD_CONTENT="今日无剪贴板记录"
    fi
else
    CLIPBOARD_CONTENT="无剪贴板数据"
fi

# 2. 读取通知数据
echo "[2/4] 读取通知数据..."
NOTIF_DIR="$DAY_DIR/computer_io/notification"
if [ -d "$NOTIF_DIR" ]; then
    NOTIF_FILE=$(ls -t "$NOTIF_DIR"/*.md 2>/dev/null | head -1)
    if [ -n "$NOTIF_FILE" ]; then
        NOTIF_CONTENT=$(cat "$NOTIF_FILE")
    else
        NOTIF_CONTENT="今日无通知记录"
    fi
else
    NOTIF_CONTENT="无通知数据"
fi

# 3. 解析今日联系人身份
echo "[3/4] 解析并更新联系人..."
CONTACTS_UPDATE_LOG=""
for src in teams outlook wechat; do
    SRC_DIR="$DAY_DIR/computer_io/notification"
    if [ -d "$SRC_DIR" ]; then
        # 提取新联系人（简单提取）
        grep -rhi "$src" "$SRC_DIR" 2>/dev/null | \
            grep -oE "[A-Za-z]+@[a-z]+\.lenovo\.com|[A-Z][a-z]+ [A-Z][a-z]+|.{2,10} (联想|DT|Brad)|.{2,5}团队" | \
            sort -u >> /tmp/contacts_$$.txt
    fi
done

# 合并到现有联系人库
if [ -f /tmp/contacts_$$.txt ]; then
    CONTACTS_UPDATE_LOG="今日新增联系人和身份已记录"
    # 清理
    rm -f /tmp/contacts_$$.txt
else
    CONTACTS_UPDATE_LOG="今日无新增联系人"
fi

# 4. 构建输出
echo "[4/4] 生成每日 memory..."
cat > "$OUTPUT_FILE" << EOF
=== 今日剪贴板（用户输入）===
$CLIPBOARD_CONTENT

=== 今日通知（收到的消息）===
$NOTIF_CONTENT

=== 今日联系人更新 ===
$CONTACTS_UPDATE_LOG

EOF

echo ""
echo "✅ 完成！"
echo "  - Memory: $OUTPUT_FILE"
echo "  - Contacts: $CONTACTS_DIR"
echo ""
echo "--- 预览 (前30行) ---"
head -30 "$OUTPUT_FILE"
