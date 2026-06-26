#!/bin/bash
# =============================================================================
# AI Agent Skills Manager - 主入口
# =============================================================================

SKILLS_DIR="$HOME/.openclaw/skills"
SOURCE_DIR="/tmp/pskoett-ai-skills"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_banner() {
    cat << 'BANNER'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🦞 AI Agent Skills Manager                         ║
║                                                           ║
║        智能体技能管理工具                                  ║
║                                                           ║
║        基于 pskoett/pskoett-ai-skills                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

BANNER
}

show_skills() {
    cat << 'SKILLS'
可选技能:

  1. self-improvement
     📖 自我改进技能
     💡 记录错误、学习经验和功能请求
     🔄 支持自动技能提取

  2. simplify-and-harden
     🛠️ 代码质量审查
     🔒 安全加固
     📝 微型文档生成

  3. plan-interview
     🗣️ 需求访谈
     📋 结构化规划
     ⚠️ 防止做错东西

  4. intent-framed-agent
     🎯 范围监控
     📊 执行状态跟踪
     🛡️ 防止范围蔓延

  5. context-surfing
     🌊 上下文监控
     📈 质量评估
     🔄 智能断点和恢复

SKILLS
}

install_all() {
    echo -e "${CYAN}正在批量安装所有核心技能...${NC}"
    
    for skill in self-improvement simplify-and-harden plan-interview intent-framed-agent context-surfing; do
        echo -e "${BLUE}  安装：${GREEN}$skill${NC}"
        
        if [[ ! -d "$SKILLS_DIR/$skill" ]]; then
            if [[ ! -d "$SOURCE_DIR" ]]; then
                echo -e "${YELLOW}  克隆源仓库...${NC}"
                git clone --depth 1 https://github.com/pskoett/pskoett-ai-skills.git "$SOURCE_DIR" 2>&1 | head -3
            fi
            
            cp -r "$SOURCE_DIR/skills/$skill" "$SKILLS_DIR/"
        else
            echo -e "${GREEN}  已安装${NC}"
        fi
    done
    
    echo -e "${GREEN}✓ 批量安装完成！${NC}"
}

show_help() {
    cat << 'HELP'

使用说明:
  1. 安装所有技能：./manager.sh --all
  2. 查看技能列表：./manager.sh --list
  3. 查看帮助：./manager.sh --help

已安装技能:
  $(ls "$SKILLS_DIR/" 2>/dev/null | tr '\n' ' ')

相关链接:
  - 源项目：https://github.com/pskoett/pskoett-ai-skills
  - Agent Skills 规范：https://agentskills.io/specification
  - OpenClaw 文档：https://docs.openclaw.ai

提示:
  • OpenClaw 会自动加载这些技能
  • 查看技能文档：~/.openclaw/skills/<name>/SKILL.md
  • 运行任务时会自动激活相关技能

HELP
}

# Parse arguments
case "$1" in
    --all|install)
        install_all
        ;;
    --list)
        show_skills
        ;;
    --help|-h)
        show_help
        ;;
    *)
        print_banner
        show_skills
        echo ""
        echo -e "${CYAN}请选择操作:${NC}"
        echo "  1. 安装所有核心技能"
        echo "  2. 查看技能列表 (已安装)"
        echo "  3. 查看帮助"
        echo "  0. 退出"
        echo ""
        read -r -p "  选择： " choice
        
        case "$choice" in
            1) install_all ;;
            2) show_skills ;;
            3) show_help ;;
            0) exit 0 ;;
            *) echo "无效选择" ;;
        esac
        ;;
esac
