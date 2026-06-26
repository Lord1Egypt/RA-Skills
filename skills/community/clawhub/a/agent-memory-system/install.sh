#!/bin/bash

# agent-memory-system 安装脚本
# 用法：./install.sh [--uninstall]
#
# 功能：
#   - 检查依赖
#   - 创建目录结构
#   - 复制脚本和模板
#   - 配置 cron 任务
#   - 验证安装

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
SKILL_DIR="$WORKSPACE/skills/agent-memory-system"

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}==>${NC} $1"; }

show_help() {
    echo "agent-memory-system 安装脚本"
    echo ""
    echo "用法："
    echo "  $0             安装技能包"
    echo "  $0 --uninstall 卸载技能包"
    echo "  $0 --help      显示帮助"
    echo ""
    echo "环境变量："
    echo "  WORKSPACE      OpenClaw 工作目录（默认：~/.openclaw/workspace）"
}

# 卸载函数
uninstall() {
    log_step "卸载 agent-memory-system..."
    
    # 移除 cron 任务
    log_info "移除 cron 任务..."
    (
        crontab -l 2>/dev/null | grep -v "agent-memory-system" || true
    ) | crontab - 2>/dev/null || log_warn "无法修改 crontab"
    
    # 询问是否删除数据
    if [ -d "$MEMORY_DIR" ]; then
        echo ""
        read -p "是否删除记忆数据目录 $MEMORY_DIR？(y/N): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            rm -rf "$MEMORY_DIR"
            log_info "记忆数据已删除"
        else
            log_info "记忆数据已保留"
        fi
    fi
    
    log_info "卸载完成"
    exit 0
}

# 主安装流程
main() {
    echo "========================================"
    echo "  agent-memory-system 安装脚本"
    echo "========================================"
    echo ""
    
    # 0. 参数处理
    case "${1:-}" in
        --help|-h) show_help; exit 0 ;;
        --uninstall) uninstall ;;
    esac
    
    # 1. 检查依赖
    log_step "检查依赖..."
    
    DEPS_OK=true
    
    # Bash
    if command -v bash &> /dev/null; then
        log_info "✓ bash: $(bash --version | head -1)"
    else
        log_error "✗ bash 未安装"
        DEPS_OK=false
    fi
    
    # cron
    if command -v crontab &> /dev/null; then
        log_info "✓ crontab: 可用"
    else
        log_warn "✗ crontab 未安装（cron 任务将跳过）"
    fi
    
    # find
    if command -v find &> /dev/null; then
        log_info "✓ find: 可用"
    else
        log_error "✗ find 未安装"
        DEPS_OK=false
    fi
    
    if [ "$DEPS_OK" = false ]; then
        log_error "依赖检查失败，请先安装缺失的依赖"
        exit 1
    fi
    
    # 2. 创建目录结构
    log_step "创建目录结构..."
    
    mkdir -p "$MEMORY_DIR"
    mkdir -p "$MEMORY_DIR/lessons"
    mkdir -p "$MEMORY_DIR/decisions"
    mkdir -p "$MEMORY_DIR/people"
    mkdir -p "$MEMORY_DIR/reflections"
    mkdir -p "$MEMORY_DIR/.archive"
    
    log_info "目录已创建：$MEMORY_DIR"
    
    # 3. 初始化核心文件（如果不存在）
    log_step "初始化核心文件..."
    
    # MEMORY.md
    if [ ! -f "$WORKSPACE/MEMORY.md" ]; then
        if [ -f "$SCRIPT_DIR/templates/MEMORY-template.md" ]; then
            cp "$SCRIPT_DIR/templates/MEMORY-template.md" "$WORKSPACE/MEMORY.md"
            log_info "✓ 创建 MEMORY.md"
        else
            touch "$WORKSPACE/MEMORY.md"
            log_info "✓ 创建空 MEMORY.md"
        fi
    else
        log_info "✓ MEMORY.md 已存在"
    fi
    
    # INDEX.md
    if [ ! -f "$MEMORY_DIR/INDEX.md" ]; then
        cat > "$MEMORY_DIR/INDEX.md" << 'EOF'
# 记忆系统导航

> 自动生成于 agent-memory-system 安装

---

## 📁 目录结构

- `lessons/` - 经验教训
- `decisions/` - 重大决策
- `people/` - 人物档案
- `reflections/` - 反思记录
- `.archive/` - 归档数据

---

## 📊 健康度统计

| 类型 | 数量 | 最后更新 |
|------|------|----------|
| Lessons | 0 | - |
| Decisions | 0 | - |
| People | 0 | - |
| Reflections | 0 | - |

---

*由 agent-memory-system 自动生成*
EOF
        log_info "✓ 创建 INDEX.md"
    else
        log_info "✓ INDEX.md 已存在"
    fi
    
    # 4. 复制模板文件
    log_step "复制模板文件..."
    
    if [ -d "$SCRIPT_DIR/templates" ]; then
        for template in "$SCRIPT_DIR/templates"/*.md; do
            if [ -f "$template" ]; then
                filename=$(basename "$template")
                log_info "  - $filename"
            fi
        done
        log_info "模板文件位于：$SCRIPT_DIR/templates/"
    fi
    
    # 5. 配置 cron 任务
    log_step "配置 cron 任务..."
    
    GC_SCRIPT="$SCRIPT_DIR/scripts/memory-gc.sh"
    REFLECTION_SCRIPT="$SCRIPT_DIR/scripts/nightly-reflection.sh"
    LOG_DIR="$HOME/.openclaw/logs"
    
    mkdir -p "$LOG_DIR"
    
    # 检查 cron 任务是否已存在
    if crontab -l 2>/dev/null | grep -q "agent-memory-system"; then
        log_info "cron 任务已存在，跳过"
    else
        # 添加 cron 任务
        (
            crontab -l 2>/dev/null || true
            echo "# agent-memory-system - 每周日凌晨执行 GC"
            echo "0 0 * * 0 $GC_SCRIPT >> $LOG_DIR/memory-gc.log 2>&1"
            echo "# agent-memory-system - 每晚反思"
            echo "45 23 * * * $REFLECTION_SCRIPT >> $LOG_DIR/nightly-reflection.log 2>&1"
        ) | crontab -
        
        log_info "✓ cron 任务已配置"
    fi
    
    # 6. 验证安装
    log_step "验证安装..."
    
    CHECKS_PASSED=0
    CHECKS_TOTAL=5
    
    # 检查目录
    if [ -d "$MEMORY_DIR" ]; then
        log_info "✓ 记忆目录存在"
        ((CHECKS_PASSED++))
    fi
    
    # 检查子目录
    SUBDIRS_OK=true
    for subdir in lessons decisions people reflections .archive; do
        if [ ! -d "$MEMORY_DIR/$subdir" ]; then
            SUBDIRS_OK=false
        fi
    done
    if [ "$SUBDIRS_OK" = true ]; then
        log_info "✓ 子目录存在"
        ((CHECKS_PASSED++))
    fi
    
    # 检查 MEMORY.md
    if [ -f "$WORKSPACE/MEMORY.md" ]; then
        log_info "✓ MEMORY.md 存在"
        ((CHECKS_PASSED++))
    fi
    
    # 检查脚本
    if [ -f "$GC_SCRIPT" ] && [ -x "$GC_SCRIPT" ]; then
        log_info "✓ GC 脚本可执行"
        ((CHECKS_PASSED++))
    fi
    
    # 检查 cron
    if crontab -l 2>/dev/null | grep -q "agent-memory-system"; then
        log_info "✓ cron 任务已配置"
        ((CHECKS_PASSED++))
    fi
    
    # 7. 完成
    echo ""
    echo "========================================"
    echo "  安装完成！"
    echo "========================================"
    echo ""
    echo "验证结果：$CHECKS_PASSED/$CHECKS_TOTAL 项通过"
    echo ""
    echo "📋 快速开始："
    echo ""
    echo "  1. 编辑记忆文件："
    echo "     $WORKSPACE/MEMORY.md"
    echo ""
    echo "  2. 手动运行 GC："
    echo "     $GC_SCRIPT --dry-run"
    echo ""
    echo "  3. 手动运行反思："
    echo "     $REFLECTION_SCRIPT"
    echo ""
    echo "  4. 查看日志："
    echo "     tail -f $LOG_DIR/memory-gc.log"
    echo ""
    echo "📚 更多信息："
    echo "     cat $SCRIPT_DIR/SKILL.md"
    echo ""
}

main "$@"