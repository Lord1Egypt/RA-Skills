#!/bin/bash

# 每日待确认规则检查脚本
# 由 cron 定时执行，读取 config.yaml 配置发送钉钉提醒

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/config/config.yaml"
PROPOSALS_DIR="$SKILL_DIR/memory/proposals"
LOGS_DIR="$SKILL_DIR/memory/logs"

# 确保日志目录存在
mkdir -p "$LOGS_DIR"

# 从 config.yaml 读取配置
if [ -f "$CONFIG_FILE" ]; then
    DINGTALK_TARGET=$(awk -F': ' '/^dingtalk_target:/{print $2}' "$CONFIG_FILE" | tr -d '"')
    DINGTALK_CHANNEL=$(awk -F': ' '/^dingtalk_channel:/{print $2}' "$CONFIG_FILE" | tr -d '"')
    ENABLE_REMINDER=$(awk -F': ' '/^enable_reminder:/{print $2}' "$CONFIG_FILE" | tr -d '"')
    LOG_FILE=$(awk -F': ' '/^log_file:/{print $2}' "$CONFIG_FILE" | tr -d '"')
else
    echo "❌ 配置文件不存在：$CONFIG_FILE"
    echo "   请先创建配置文件并配置 dingtalk_target"
    exit 1
fi

# 验证 dingtalk_target 是否已配置
if [ -z "$DINGTALK_TARGET" ] || [ "$DINGTALK_TARGET" = "YOUR_DINGTALK_ID" ]; then
    echo "❌ dingtalk_target 未配置或为默认占位符"
    echo "   请修改 config/config.yaml"
    echo "   设置 dingtalk_target: \"你的钉钉 ID\""
    exit 1
fi

# 检查是否启用提醒
if [ "$ENABLE_REMINDER" != "true" ]; then
    echo "✅ 定时提醒已禁用"
    exit 0
fi

# 检查待审规则数量（支持按日期合并的文件格式）
pending_count=0
message_content=""

if [ -d "$PROPOSALS_DIR" ]; then
    for file in "$PROPOSALS_DIR"/*.md; do
        if [ -f "$file" ]; then
            # 读取文件中的所有规则 ID
            while IFS= read -r rule_id; do
                if [ -n "$rule_id" ]; then
                    pending_count=$((pending_count + 1))
                    
                    # 从文件中提取规则详情
                    # 使用 awk 提取规则块
                    rule_block=$(awk -v rid="$rule_id" '
                        $0 ~ "### 【规则 ID】"rid { found=1; next }
                        found && /^---$/ && ++count==3 { found=0; count=0 }
                        found { print }
                    ' "$file")
                    
                    scene=$(echo "$rule_block" | grep "^### 【场景】" | cut -d: -f2 | tr -d ' ' || echo "未知")
                    problem=$(echo "$rule_block" | grep "^### 【问题/模式】" | cut -d: -f2- || echo "未知")
                    suggestion=$(echo "$rule_block" | grep "^### 【建议规则】" | cut -d: -f2- || echo "待确认")
                    confidence=$(echo "$rule_block" | grep "^### 【可信度】" | cut -d: -f2 | tr -d ' ' || echo "未知")
                    
                    # 构建规则详情
                    message_content="$message_content
📌 $rule_id
   场景：$scene
   问题：$problem
   建议：$suggestion
   可信度：$confidence
"
                fi
            done < <(grep "^### 【规则 ID】" "$file" | sed 's/### 【规则 ID】//')
        fi
    done
fi

# 有待审规则时发送钉钉消息
if [ "$pending_count" -gt 0 ]; then
    # 构建完整消息
    full_message="⏰ 有待确认规则 ($pending_count 条)
$message_content
💬 直接回复确认：
   同意 [规则 ID]  或  忽略 [规则 ID]
   
   示例：同意 auto_ios_d651215e"
    
    # 发送钉钉消息
    if [ -n "$DINGTALK_CHANNEL" ]; then
        openclaw message send \
            --channel "$DINGTALK_CHANNEL" \
            --target "$DINGTALK_TARGET" \
            --message "$full_message"
    else
        openclaw message send \
            --target "$DINGTALK_TARGET" \
            --message "$full_message"
    fi
    
    echo "✅ 已发送钉钉提醒（$pending_count 条规则）"
else
    echo "✅ 无待确认规则"
fi
