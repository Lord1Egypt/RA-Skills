#!/bin/bash
# 配置验证脚本
# 用法: ./validate.sh ~/.openclaw/openclaw.json

CONFIG_FILE="${1:-~/.openclaw/openclaw.json}"

echo "🔍 验证配置文件: $CONFIG_FILE"

# 1. 检查文件是否存在
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ 错误: 文件不存在"
    exit 1
fi

# 2. 检查 JSON 语法
if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
    echo "❌ JSON 语法错误"
    exit 1
fi

# 3. 检查必需字段
REQUIRED_FIELDS=("models" "agents" "channels" "gateway")
for field in "${REQUIRED_FIELDS[@]}"; do
    if jq -e "has(\"$field\")" "$CONFIG_FILE" >/dev/null 2>&1; then
        echo "✅ $field 存在"
    else
        echo "⚠️  缺少可选字段: $field"
    fi
done

# 4. 检查模型配置
PRIMARY_MODEL=$(jq -r '.agents.defaults.model.primary // "未设置"' "$CONFIG_FILE")
echo "📌 主模型: $PRIMARY_MODEL"

# 5. 检查 channel 状态
CHANNELS=$(jq -r '.channels | keys | join(", ")' "$CONFIG_FILE" 2>/dev/null || echo "无")
echo "📌 已配置 channels: $CHANNELS"

echo ""
echo "✅ 验证完成，无严重错误"
