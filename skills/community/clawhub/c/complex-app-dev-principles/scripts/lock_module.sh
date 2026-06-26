#!/bin/bash
# I漫剧APP开发技能 - 模块锁定脚本
# 用于锁定已确认的模块代码

set -e

MODULE_NAME=$1
LOCK_DIR=".locks"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

if [ -z "$MODULE_NAME" ]; then
    echo "用法: bash lock_module.sh <模块名称>"
    exit 1
fi

# 创建锁定记录目录
mkdir -p "$LOCK_DIR"

# 创建锁定记录文件
LOCK_FILE="$LOCK_DIR/${MODULE_NAME}_${TIMESTAMP}.lock"

cat > "$LOCK_FILE" << EOF
{
    "module": "$MODULE_NAME",
    "locked_at": "$(date -Iseconds)",
    "locked_by": "${USER:-developer}",
    "status": "locked",
    "reason": "开发者确认通过"
}
EOF

# 创建符号链接指向最新锁定
ln -sf "$LOCK_FILE" "$LOCK_DIR/${MODULE_NAME}_latest.lock"

echo "✓ 模块 '$MODULE_NAME' 已锁定"
echo "  锁定记录: $LOCK_FILE"
