#!/bin/bash
# launch-claudecode.sh - 启动 Claude Code 会话
# 用法：./launch-claudecode.sh [项目目录] [模型] [任务描述]

set -e

# 默认配置
DEFAULT_MODEL="claude-sonnet-4-5-20250929"
DEFAULT_TIMEOUT=3600

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查依赖
check_dependencies() {
    if ! command -v claude &> /dev/null; then
        echo -e "${RED}错误：Claude Code 未安装${NC}"
        echo "请运行：npm install -g @anthropic-ai/claude-code"
        exit 1
    fi
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo -e "${RED}错误：未设置 ANTHROPIC_API_KEY 环境变量${NC}"
        echo "请设置：export ANTHROPIC_API_KEY=\"your-key\""
        exit 1
    fi
}

# 检查项目配置
check_project_config() {
    local project_dir="$1"
    local config_file="$project_dir/.claude/settings.json"
    
    if [ ! -f "$config_file" ]; then
        echo -e "${YELLOW}提示：项目无 Claude 配置，创建默认配置...${NC}"
        mkdir -p "$project_dir/.claude"
        cat > "$config_file" << EOF
{
  "model": "$DEFAULT_MODEL",
  "allowedTools": ["bash", "edit", "write", "read"],
  "maxTurns": 50,
  "permissionMode": "auto"
}
EOF
    fi
}

# 主函数
main() {
    local project_dir="${1:-.}"
    local model="${2:-$DEFAULT_MODEL}"
    local task="${3:-}"
    
    echo -e "${GREEN}=== Claude Code 启动器 ===${NC}"
    echo "项目目录：$(cd "$project_dir" && pwd)"
    echo "使用模型：$model"
    echo ""
    
    check_dependencies
    check_project_config "$project_dir"
    
    # 进入项目目录
    cd "$project_dir"
    
    if [ -n "$task" ]; then
        echo -e "${GREEN}执行任务：$task${NC}"
        echo ""
        # 带任务启动
        claude --model "$model" "$task"
    else
        echo -e "${YELLOW}进入交互模式，输入任务描述或输入 /help 查看帮助${NC}"
        echo ""
        # 交互模式
        claude --model "$model"
    fi
}

# 执行
main "$@"
