#!/usr/bin/env bash
# desktop-notify 一键全局配置 (macOS / Linux)
# 作用：把"每次回答完自动发通知"规则写入用户级全局记忆 ~/.workbuddy/MEMORY.md
# 运行一次即可，之后所有对话全局生效。可重复运行，不会重复写入。

set -e

# 1. 定位路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
NOTIFY_SH="$SKILL_DIR/scripts/notify.sh"
MEMORY_DIR="$HOME/.workbuddy"
MEMORY_MD="$MEMORY_DIR/MEMORY.md"

# 2. 确保目录/文件存在
mkdir -p "$MEMORY_DIR"
touch "$MEMORY_MD"

# 3. 幂等检查
MARKER="<!-- desktop-notify-auto -->"
if grep -qF "$MARKER" "$MEMORY_MD"; then
    echo "[skip] 全局通知规则已存在，无需重复配置。"
    echo "位置: $MEMORY_MD"
    exit 0
fi

# 4. 追加规则
cat >> "$MEMORY_MD" <<EOF

$MARKER
## 自动通知规则 (desktop-notify)
- 每次回答完成后，必须运行以下命令触发桌面通知（提示音 + 系统通知）：
  \`bash "$NOTIFY_SH" "任务完成，请查看" "WorkBuddy"\`
- 此规则全局生效（所有项目 / 所有对话）。
EOF

echo "[ok] 全局通知规则已写入。"
echo "位置: $MEMORY_MD"
echo "通知脚本: $NOTIFY_SH"
echo "重启对话或新开会话后，AI 每次回答完都会自动发通知。"
