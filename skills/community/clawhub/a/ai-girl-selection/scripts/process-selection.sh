#!/bin/bash
# Process user selection and save avatar

SELECTION=$1
PREVIEW_DIR="/Users/qifengxiang/.openclaw/workspace"
AVATAR_DIR="/Users/qifengxiang/.openclaw/workspace/avatars"
PREFERENCES_FILE="/Users/qifengxiang/.openclaw/workspace/.learnings/AI-GIRL-PREFERENCES.md"
SOURCE_DIR="/Volumes/info/sex/picture/AI girls"

# Ensure directories exist
mkdir -p "$AVATAR_DIR" "$(dirname $PREFERENCES_FILE)"

# Map selection to filename
case $SELECTION in
    1|第一个|first)
        CHOSEN_FILE="20250725_002805.jpg"
        ;;
    2|第二个|second)
        CHOSEN_FILE="20250716_000913.jpg"
        ;;
    3|第三个|third)
        CHOSEN_FILE="00004-145824367.png"
        ;;
    *.jpg|*.png|*.webp)
        CHOSEN_FILE="$SELECTION"
        ;;
    *)
        echo "❌ 无效的选择：$SELECTION"
        echo "有效选择：1, 2, 3, 第一个，第二个，第三个，或文件名"
        exit 1
        ;;
esac

# Find the actual file
ACTUAL_FILE=$(find "$SOURCE_DIR" -name "$CHOSEN_FILE" -type f 2>/dev/null | head -1)

if [ -z "$ACTUAL_FILE" ]; then
    echo "❌ 未找到文件：$CHOSEN_FILE"
    exit 1
fi

# Copy to avatar
cp "$ACTUAL_FILE" "$AVATAR_DIR/mimi-today.png"

# Record preference
TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M Asia/Shanghai')
cat > "$PREFERENCES_FILE" << EOF
{
  "status": "success",
  "date": "$TIMESTAMP",
  "selected": "$CHOSEN_FILE",
  "avatar_saved": true,
  "location": "$AVATAR_DIR/mimi-today.png"
}
EOF

echo "✅ 选择已保存：$CHOSEN_FILE"
echo "✅ 新头像已更新：$AVATAR_DIR/mimi-today.png"
echo "✅ 偏好已记录：$PREFERENCES_FILE"
