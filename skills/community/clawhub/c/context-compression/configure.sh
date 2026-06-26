#!/bin/bash
# ============================================================
# Context Compression - Interactive Configuration Script
# ============================================================
# SECURITY NOTICE: This script is designed to run interactively
# with explicit user consent. It configures session truncation
# to prevent context overflow errors in OpenClaw agents.
#
# WHAT THIS SCRIPT DOES:
# - Creates a JSON config file in ~/.openclaw/workspace/
# - Adds a cron job for periodic session truncation
# - All operations are LOCAL and require manual execution
#
# CRONTAB MODIFICATION: Requires user confirmation at runtime.
# The cron job runs ~/.openclaw/.../truncate-sessions-safe.sh
# to prevent session files from exceeding model context limits.
#
# NO EXTERNAL NETWORK ACCESS: This script does not send data
# externally. All operations are performed on the local machine.
#
# Run this script manually: bash configure.sh
# ============================================================

set -e

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
CONFIG_FILE="$WORKSPACE/.context-compression-config.json"
SCRIPTS_DIR="$WORKSPACE/skills/context-compression/scripts"

echo "═══════════════════════════════════════════════════════════════"
echo "      Context Compression - Interactive Configuration"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check existing config
if [ -f "$CONFIG_FILE" ]; then
    echo "检测到已有配置:"
    cat "$CONFIG_FILE"
    echo ""
    read -p "是否要重新配置？(y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "保持现有配置"
        exit 0
    fi
fi

# Question 1: Max Lines
echo ""
echo "【问题 1/4】会话文件截断时保留多少行？"
echo "─────────────────────────────────────────"
echo "  1) 默认 (2000 行, ~40k chars) [推荐]"
echo "  2) 保守 (3000 行, ~60k chars)"
echo "  3) 激进 (1000 行, ~20k chars)"
echo "  4) 自定义"
echo ""
read -p "请选择 [1-4] (默认: 1): " choice

case $choice in
    2) MAX_LINES=3000 ;;
    3) MAX_LINES=1000 ;;
    4) 
        read -p "请输入行数 (500-5000, 默认 2000): " custom_lines
        MAX_LINES=${custom_lines:-2000}
        # Validate
        if [ "$MAX_LINES" -lt 500 ] || [ "$MAX_LINES" -gt 5000 ]; then
            echo "行数必须在 500-5000 之间，使用默认值 2000"
            MAX_LINES=2000
        fi
        ;;
    *) MAX_LINES=2000 ;;
esac

echo "✅ 保留行数: $MAX_LINES"

# Question 2: Frequency
echo ""
echo "【问题 2/4】多久检查并截断一次？"
echo "─────────────────────────────────────────"
echo "  1) 每 10 分钟 [推荐]"
echo "  2) 每 30 分钟"
echo "  3) 每小时"
echo "  4) 自定义"
echo ""
read -p "请选择 [1-4] (默认: 1): " choice

case $choice in
    2) FREQ_MINUTES=30 ;;
    3) FREQ_MINUTES=60 ;;
    4)
        read -p "请输入分钟数 (5-120, 默认 10): " custom_freq
        FREQ_MINUTES=${custom_freq:-10}
        if [ "$FREQ_MINUTES" -lt 5 ] || [ "$FREQ_MINUTES" -gt 120 ]; then
            echo "分钟数必须在 5-120 之间，使用默认值 10"
            FREQ_MINUTES=10
        fi
        ;;
    *) FREQ_MINUTES=10 ;;
esac

echo "✅ 检查频率: 每 $FREQ_MINUTES 分钟"

# Question 3: Skip Active
echo ""
echo "【问题 3/4】是否跳过当前活跃的会话（有 .lock 文件）？"
echo "─────────────────────────────────────────"
echo "  1) 是 (跳过活跃会话) [推荐]"
echo "  2) 否 (可能截断正在写入的会话)"
echo ""
read -p "请选择 [1-2] (默认: 1): " choice

case $choice in
    2) SKIP_ACTIVE="false" ;;
    *) SKIP_ACTIVE="true" ;;
esac

echo "✅ 跳过活跃会话: $SKIP_ACTIVE"

# Question 4: Enable Summaries
echo ""
echo "【问题 4/4】是否启用自动摘要生成？"
echo "─────────────────────────────────────────"
echo "  1) 否 (依赖实时写入 memory) [推荐]"
echo "  2) 是 (每 4 小时从 daily notes 生成摘要)"
echo ""
read -p "请选择 [1-2] (默认: 1): " choice

case $choice in
    2) ENABLE_SUMMARIES="true" ;;
    *) ENABLE_SUMMARIES="false" ;;
esac

echo "✅ 自动摘要: $ENABLE_SUMMARIES"

# Save configuration
echo ""
echo "─────────────────────────────────────────"
echo "保存配置..."

mkdir -p "$(dirname "$CONFIG_FILE")"

cat > "$CONFIG_FILE" << EOF
{
  "version": "1.0",
  "maxLines": $MAX_LINES,
  "frequencyMinutes": $FREQ_MINUTES,
  "skipActive": $SKIP_ACTIVE,
  "enableSummaries": $ENABLE_SUMMARIES,
  "configuredAt": "$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S%z')"
}
EOF

echo "✅ 配置已保存到: $CONFIG_FILE"

# Create script config
cat > "$SCRIPTS_DIR/.config" << EOF
export MAX_LINES=$MAX_LINES
export SKIP_ACTIVE=$SKIP_ACTIVE
EOF

echo "✅ 脚本配置已更新"

# Generate cron commands for user to add manually
echo ""
echo "请手动将以下 cron 条目添加到您的 crontab:"

# Calculate cron expression
if [ "$FREQ_MINUTES" -eq 60 ]; then
    CRON_EXPR="0 * * * *"
else
    CRON_EXPR="*/$FREQ_MINUTES * * * *"
fi

TRUNCATE_SCRIPT="$SCRIPTS_DIR/truncate-sessions-safe.sh"
echo ""
echo "  # Session truncation"
echo "  $CRON_EXPR $TRUNCATE_SCRIPT"

if [ "$ENABLE_SUMMARIES" = "true" ]; then
    SUMMARY_SCRIPT="$SCRIPTS_DIR/generate-daily-summary.sh"
    echo ""
    echo "  # Daily summary generation"
    echo "  0 */4 * * * $SUMMARY_SCRIPT"
fi

# Show final configuration
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "                    配置完成！"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "截断设置:"
echo "  - 保留行数: $MAX_LINES 行 (~$((MAX_LINES * 20)) chars)"
echo "  - 检查频率: 每 $FREQ_MINUTES 分钟"
echo "  - 跳过活跃会话: $SKIP_ACTIVE"
echo "  - 自动摘要: $ENABLE_SUMMARIES"
echo ""
echo "下一步:"
echo "  1. 运行 crontab -e 添加上面的 cron 条目"
echo "  2. 实时写入 memory 文件保证记忆连续性"
echo "  3. 运行 check-context-health.sh 检查状态"
echo ""
echo "═══════════════════════════════════════════════════════════════"
