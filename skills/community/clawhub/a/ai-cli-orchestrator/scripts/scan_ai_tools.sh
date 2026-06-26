#!/bin/bash
# AI CLI 工具扫描脚本
# 功能：1.扫描系统中已安装的AI CLI工具 2.测试可用性 3.生成配置文件

# 加载环境变量
[ -f "$HOME/.zshrc" ] && source "$HOME/.zshrc"

CONFIG_FILE="$HOME/.ai-cli-config.json"

# 要扫描的 AI CLI 工具列表（真正的命令行AI工具）
AI_TOOLS=(
    "gemini:Gemini CLI:Google AI - 网络搜索/问答"
    "cursor-agent:Cursor Agent:AI代码编辑器 - 代码生成/调试"
    "claude:Claude Code:Anthropic AI - 代码/问答"
    "codex:Codex:OpenAI - 代码生成"
    "aider:aider:AI编程助手 - 代码编辑"
)

echo "🤖 AI CLI 工具扫描器"
echo "======================"
echo ""

available_tools=()
unavailable_tools=()

for tool_info in "${AI_TOOLS[@]}"; do
    IFS=':' read -r cmd name desc <<< "$tool_info"
    
    # 检查命令是否存在
    if command -v "$cmd" &> /dev/null; then
        echo "✅ $name ($cmd) - 已安装"
        
        # 测试可用性 - 直接运行帮助命令
        if "$cmd" --help &> /dev/null || "$cmd" -h &> /dev/null || "$cmd" --version &> /dev/null || "$cmd" -v &> /dev/null; then
            echo "   └─ 可用"
            available_tools+=("$cmd:$name:$desc")
        else
            echo "   └─ 已安装但不可用"
            unavailable_tools+=("$cmd:$name:$desc:installed")
        fi
    else
        echo "❌ $name ($cmd) - 未安装"
        unavailable_tools+=("$cmd:$name:$desc:not_installed")
    fi
done

echo ""
echo "======================"
echo "可用工具: ${#available_tools[@]}"
echo "不可用工具: ${#unavailable_tools[@]}"

# 生成配置文件
echo "生成配置文件: $CONFIG_FILE"

cat > "$CONFIG_FILE" << EOF
{
  "version": "1.0",
  "scan_time": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "available": [
$(for tool in "${available_tools[@]}"; do
    IFS=':' read -r cmd name desc <<< "$tool"
    echo "    {\"cmd\": \"$cmd\", \"name\": \"$name\", \"desc\": \"$desc\"},"
done | sed '$ s/,$//')
  ],
  "unavailable": [
$(for tool in "${unavailable_tools[@]}"; do
    IFS=':' read -r cmd name desc status <<< "$tool"
    echo "    {\"cmd\": \"$cmd\", \"name\": \"$name\", \"desc\": \"$desc\", \"status\": \"$status\"},"
done | sed '$ s/,$//')
  ]
}
EOF

echo "✅ 配置已保存到: $CONFIG_FILE"
echo ""
echo "======================"
echo "🎯 下一步操作："
echo ""
echo "1. 设置优先级："
echo "   编辑 ~/.ai-cli-config.json 为可用工具设置 priority 字段"
echo ""
echo "2. 选择执行策略："
echo "   - cli_first: 优先使用 AI CLI"
echo "   - direct: 直接回答"
echo "   - hybrid: 混合模式"
echo ""
echo "3. 运行任务："
echo "   使用此技能时，我会自动按优先级调用 AI CLI"
echo ""
echo "======================"
echo "配置示例："
cat << 'EOF'
{
  "strategy": "cli_first",
  "available": [
    {"cmd": "gemini", "name": "Gemini CLI", "priority": 1},
    {"cmd": "cursor-agent", "name": "Cursor Agent", "priority": 2},
    {"cmd": "claude", "name": "Claude Code", "priority": 3}
  ]
}
EOF
