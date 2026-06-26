#!/bin/bash
# =============================================================================
# AI Agent Skills Installer
# 技能安装管理器 - 推广版本 v1.0
# =============================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Paths
SKILLS_DIR="$HOME/.openclaw/skills"
SOURCE_DIR="/tmp/pskoett-ai-skills"
LOG_FILE="$HOME/.ai_agent_skills/install.log"

# Skills data
declare -A SKILLS=(
    [self-improvement]="Captures learnings, errors, and corrections for continuous improvement"
    [simplify-and-harden]="Post-completion self-review for code quality and security"
    [plan-interview]="Structured requirements interview before implementation"
    [intent-framed-agent]="Monitors scope drift during task execution"
    [context-surfing]="Monitors context quality during multi-step execution"
)

# Track selected skills
SELECTED_SKILLS=()

# =============================================================================
# Functions
# =============================================================================

log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
    
    # Also print to console
    case $level in
        "INFO")   echo -e "${GREEN}[INFO]${NC} $message" ;;
        "WARN")   echo -e "${YELLOW}[WARN]${NC} $message" ;;
        "ERROR")  echo -e "${RED}[ERROR]${NC} $message" ;;
        "HEADER") echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
                  echo -e "${BLUE}  $message${NC}"
                  echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
                  ;;
        "FOOTER") echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
                  echo -e "${NC}"
                  ;;
    esac
}

print_header() {
    log "HEADER" "$1"
}

print_footer() {
    log "FOOTER"
}

show_banner() {
    cat << 'BANNER'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🦞 AI Agent Skills Installer                       ║
║                                                           ║
║        智能体技能安装管理工具                              ║
║                                                           ║
║        基于 pskoett/pskoett-ai-skills                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
BANNER
}

show_skills_menu() {
    echo ""
    echo -e "${CYAN}请选择要安装的技能 (可多选)${NC}"
    echo ""
    echo " 按空格键选择/取消选择，Enter 确认，q 退出"
    echo ""
    
    # Show skill list with numbers
    local i=1
    for skill in "${!SKILLS[@]}"; do
        echo -e "  $i. ${BLUE}$skill${NC} - ${SKILLS[$skill]}"
        i=$((i + 1))
    done
    
    echo ""
    echo "  0. 取消安装"
    echo ""
}

select_skills() {
    SELECTED_SKILLS=()
    
    while true; do
        show_skills_menu
        
        read -r -p "  选择技能编号 (用逗号分隔，如：1,3,5): " input
        
        if [[ "$input" =~ ^q$ ]]; then
            return 1
        fi
        
        if [[ -z "$input" ]]; then
            continue
        fi
        
        # Parse input
        IFS=',' read -ra choices <<< "$input"
        
        for choice in "${choices[@]}"; do
            # Remove spaces
            choice=$(echo "$choice" | tr -d ' ')
            
            if [[ "$choice" =~ ^[0-9]+$ ]]; then
                # Calculate skill index (1-based to 0-based)
                local skill_index=$((choice - 1))
                
                # Find the skill name from the array
                local found_skill=""
                local count=0
                for skill in "${!SKILLS[@]}"; do
                    if ((count == skill_index)); then
                        found_skill="$skill"
                        break
                    fi
                    count=$((count + 1))
                done
                
                if [[ -n "$found_skill" ]]; then
                    if [[ " ${SELECTED_SKILLS[@]} " =~ " ${found_skill} " ]]; then
                        echo -e "${YELLOW}取消选择：$found_skill${NC}"
                        SELECTED_SKILLS=("${SELECTED_SKILLS[@]/$found_skill}")
                    else
                        echo -e "${GREEN}选择：$found_skill${NC}"
                        SELECTED_SKILLS+=("$found_skill")
                    fi
                fi
            fi
        done
        
        echo ""
        read -r -p "  继续选择？(y/n): " continue_choice
        
        if [[ "$continue_choice" =~ ^[Nn]$ ]]; then
            break
        fi
    done
    
    echo ""
    if (( ${#SELECTED_SKILLS[@]} == 0 )); then
        echo -e "${YELLOW}未选择任何技能${NC}"
        return 1
    fi
    
    return 0
}

install_skill() {
    local skill=$1
    local skill_path="${SOURCE_DIR}/skills/$skill"
    local dest_path="${SKILLS_DIR}/${skill}"
    
    echo ""
    echo -e "${CYAN}正在安装：${GREEN}$skill${NC}"
    echo "  来源：$skill_path"
    echo "  目标：$dest_path"
    
    if [[ ! -d "$skill_path" ]]; then
        echo -e "${RED}错误：技能目录不存在：$skill_path${NC}"
        return 1
    fi
    
    if [[ -d "$dest_path" ]]; then
        echo -e "${YELLOW}警告：技能已存在，将覆盖${NC}"
        read -r -p "  是否继续？(y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}已取消${NC}"
            return 0
        fi
    fi
    
    # Clone if source doesn't exist
    if [[ ! -d "$SOURCE_DIR" ]]; then
        echo ""
        echo -e "${CYAN}克隆源仓库...${NC}"
        # 使用安全的 TLS 连接克隆 GitHub（不使用 GIT_SSL_NO_VERIFY）
        git clone --depth 1 https://github.com/pskoett/pskoett-ai-skills.git "$SOURCE_DIR" 2>&1 | head -5
    fi
    
    # Copy skill
    cp -r "$skill_path" "$dest_path"
    
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✓ 成功安装：$skill${NC}"
        return 0
    else
        echo -e "${RED}✗ 安装失败：$skill${NC}"
        return 1
    fi
}

show_completion() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  安装完成！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    echo "已安装的技能："
    for skill in "${SELECTED_SKILLS[@]}"; do
        echo "  • ${GREEN}$skill${NC}"
    done
    
    echo ""
    echo "技能位置：${SKILLS_DIR}"
    echo ""
    
    echo -e "${CYAN}使用提示:${NC}"
    echo "  1. OpenClaw 会自动加载这些技能"
    echo "  2. 查看技能文档：${SKILLS_DIR}/${skill}/SKILL.md"
    echo "  3. 查看源仓库：https://github.com/pskoett/pskoett-ai-skills"
    echo ""
    
    echo -e "${YELLOW}下一步:${NC}"
    echo "  • 运行计划访谈：/plan-interview <你的任务>"
    echo "  • 开始任务时会自动激活相关技能"
    echo "  • 查看技能集成：${SKILLS_DIR}/README.md (如果存在)"
    echo ""
    
    echo -e "${YELLOW}推广建议:${NC}"
    echo "  • 将此脚本分享给其他开发者"
    echo "  • 创建 README 说明安装方法"
    echo "  • 在 GitHub 上发布此工具"
    echo ""
    
    echo -e "${GREEN}需要推广支持请运行：${NC}"
    echo "  ./skill-installer.sh --help"
    echo ""
}

# =============================================================================
# Main
# =============================================================================

main() {
    print_header "AI Agent Skills Installer - 智能体技能安装管理器"
    
    # Check if source exists
    if [[ ! -d "$SOURCE_DIR" ]]; then
        echo ""
        read -r -p "首次运行，需要克隆源仓库，是否继续？(Y/n): " confirm
        if [[ "$confirm" =~ ^[Nn]$ ]]; then
            echo -e "${YELLOW}已取消${NC}"
            exit 0
        fi
    fi
    
    # Select skills
    select_skills
    
    if (( ${#SELECTED_SKILLS[@]} == 0 )); then
        echo -e "${YELLOW}已取消安装${NC}"
        exit 0
    fi
    
    # Install selected skills
    local errors=0
    for skill in "${SELECTED_SKILLS[@]}"; do
        if ! install_skill "$skill"; then
            errors=$((errors + 1))
        fi
    done
    
    # Summary
    echo ""
    echo "共安装 ${#SELECTED_SKILLS[@]} 个技能，${errors} 个失败"
    
    if (( errors > 0 )); then
        print_footer
        exit 1
    fi
    
    show_completion
    print_footer
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
