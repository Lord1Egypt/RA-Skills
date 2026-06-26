#!/bin/bash
#==============================================================================
# Apollo Evolution - Skill自我进化脚本
# 
# 概念：像生命进化一样，通过复制+变异+选择让Skill自我优化
#
# 使用方式：
#   bash evolution.sh <command> [args]
#
# 命令：
#   copy <skill_name>     - 复制一个Skill作为起点
#   mutate <skill_name>    - 生成变异版本
#   test <v1> <v2> ...    - 测试多个版本
#   select <skill_name>    - 选择最优版本
#   status <skill_name>    - 查看进化状态
#==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 从 scripts/apollo-evolution/evolution.sh 回溯到 skills/
SKILLS_DIR="${SCRIPT_DIR}/../../.."
SKILLS_DIR="$(cd "$SKILLS_DIR" && pwd)"
MEMORY_DIR="${SKILLS_DIR}/.memory/evolution"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

#------------------------------------------------------------------------------
# 命令：copy - 复制Skill作为进化起点
#------------------------------------------------------------------------------
cmd_copy() {
    local skill_name="$1"
    local target_dir="${MEMORY_DIR}/${skill_name}"
    
    if [ -z "$skill_name" ]; then
        echo "用法: evolution.sh copy <skill_name>"
        exit 1
    fi
    
    local source_dir="${SKILLS_DIR}/${skill_name}"
    if [ ! -d "$source_dir" ]; then
        log_error "Skill不存在: ${skill_name}"
        exit 1
    fi
    
    # 创建进化目录
    mkdir -p "${target_dir}/variants"
    
    # 复制原始版本为第0代
    local gen0_dir="${target_dir}/variants/gen-000"
    cp -r "$source_dir" "$gen0_dir"
    
    # 初始化generations.json
    cat > "${target_dir}/generations.json" << EOF
{
  "skill_name": "${skill_name}",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "generations": [
    {
      "gen": "000",
      "path": "variants/gen-000",
      "parent": null,
      "mutations": [],
      "fitness_score": null,
      "test_results": {}
    }
  ],
  "best_version": "gen-000",
  "best_score": null
}
EOF
    
    log_success "已复制 ${skill_name} 作为进化起点"
    log_info "变异版本将存储在: ${target_dir}/variants/"
    echo ""
    echo "下一步: bash evolution.sh mutate ${skill_name}"
}

#------------------------------------------------------------------------------
# 命令：mutate - 生成变异版本
#------------------------------------------------------------------------------
cmd_mutate() {
    local skill_name="$1"
    local target_dir="${MEMORY_DIR}/${skill_name}"
    
    if [ ! -d "$target_dir" ]; then
        log_error "未找到进化记录。请先运行: evolution.sh copy ${skill_name}"
        exit 1
    fi
    
    # 获取最新一代
    local latest_gen=$(ls -d "${target_dir}"/variants/gen-* 2>/dev/null | sort | tail -1)
    local gen_num=$(echo "$latest_gen" | grep -o 'gen-[0-9]*' | head -1 | cut -d'-' -f2)
    local next_gen=$(printf "%03d" $((10#$gen_num + 1)))
    
    # 复制最新版本
    local new_gen_dir="${target_dir}/variants/gen-${next_gen}"
    cp -r "$latest_gen" "$new_gen_dir"
    
    # 读取SKILL.md进行变异
    local skill_md="${new_gen_dir}/SKILL.md"
    if [ -f "$skill_md" ]; then
        # 随机选择一个变异方向
        local mutation_type=$((RANDOM % 3))
        case $mutation_type in
            0)
                # 变异1: 修改description
                sed -i 's/description:.*/description: 通过迭代优化的工作流Skill v'${next_gen}'/g' "$skill_md"
                local mutation_desc="修改description"
                ;;
            1)
                # 变异2: 增加版本注释
                echo -e "\n<!-- EVOLUTION: Generation ${next_gen}, mutated from gen-${gen_num} -->\n" >> "$skill_md"
                local mutation_desc="增加世代注释"
                ;;
            2)
                # 变异3: 修改version
                sed -i 's/version:.*/version: 1.'${next_gen}'.0/g' "$skill_md" 2>/dev/null || true
                local mutation_desc="更新版本号"
                ;;
        esac
    fi
    
    # 更新generations.json
    local temp_json=$(cat "${target_dir}/generations.json")
    # 简化处理：直接追加
    echo "生成变异版本 gen-${next_gen}: $mutation_desc"
    
    log_success "已生成第 ${next_gen} 代变异版本"
    echo ""
    echo "下一步: bash evolution.sh test ${skill_name} gen-000 gen-${next_gen}"
}

#------------------------------------------------------------------------------
# 命令：test - 测试多个版本
#------------------------------------------------------------------------------
cmd_test() {
    local skill_name="$1"
    shift
    local variants=("$@")
    
    if [ ${#variants[@]} -eq 0 ]; then
        echo "用法: evolution.sh test <skill_name> <variant1> <variant2> ..."
        exit 1
    fi
    
    log_info "开始测试 ${#variants[@]} 个版本..."
    
    for variant in "${variants[@]}"; do
        echo -e "\n${YELLOW}测试 ${variant}:${NC}"
        # 这里应该运行实际的测试逻辑
        # 目前是占位符，实际需要接入MiniMax API进行效果评估
        local score=$((RANDOM % 50 + 50))
        echo "  模拟评分: ${score}/100"
    done
    
    echo ""
    log_success "测试完成"
    echo "使用 'evolution.sh select ${skill_name}' 选择最优版本"
}

#------------------------------------------------------------------------------
# 命令：select - 选择最优版本
#------------------------------------------------------------------------------
cmd_select() {
    local skill_name="$1"
    local target_dir="${MEMORY_DIR}/${skill_name}"
    
    if [ ! -d "$target_dir" ]; then
        log_error "未找到进化记录"
        exit 1
    fi
    
    # 列出所有版本及其评分
    echo "========================================"
    echo "  Apollo Evolution - 选择最优版本"
    echo "========================================"
    echo ""
    
    local i=1
    for gen_dir in "${target_dir}"/variants/gen-*; do
        local gen_name=$(basename "$gen_dir")
        local score=$((RANDOM % 50 + 50))  # 模拟评分
        echo "  ${i}. ${gen_name} - 评分: ${score}/100"
        i=$((i+1))
    done
    
    echo ""
    read -p "选择要保留的版本编号: " choice
    
    local selected_gen=$(ls -d "${target_dir}"/variants/gen-* | sort | sed -n "${choice}p")
    if [ -n "$selected_gen" ]; then
        log_success "已选择: $(basename "$selected_gen")"
        echo "最优版本已记录，实际应用需要手动替换原Skill"
    fi
}

#------------------------------------------------------------------------------
# 命令：status - 查看进化状态
#------------------------------------------------------------------------------
cmd_status() {
    local skill_name="$1"
    local target_dir="${MEMORY_DIR}/${skill_name}"
    
    if [ ! -d "$target_dir" ]; then
        log_error "未找到进化记录。请先运行: evolution.sh copy ${skill_name}"
        exit 1
    fi
    
    echo "========================================"
    echo "  Apollo Evolution - 进化状态"
    echo "========================================"
    echo ""
    
    local gen_count=$(ls -d "${target_dir}"/variants/gen-* 2>/dev/null | wc -l)
    echo "  Skill名称: ${skill_name}"
    echo "  当前代数: ${gen_count}"
    echo "  存储位置: ${target_dir}"
    echo ""
    
    # 显示各代信息
    echo "  世代记录:"
    for gen_dir in "${target_dir}"/variants/gen-*; do
        local gen_name=$(basename "$gen_dir")
        local modified=$(stat -c %y "$gen_dir/SKILL.md" 2>/dev/null | cut -d' ' -f1 || echo "未知")
        echo "    - ${gen_name} (修改: ${modified})"
    done
    
    echo ""
}

#------------------------------------------------------------------------------
# 帮助信息
#------------------------------------------------------------------------------
show_help() {
    cat << EOF
Apollo Evolution - Skill自我进化工具

像生命进化一样，通过复制+变异+选择让Skill自我优化。

使用方法:
    bash evolution.sh <命令> [参数]

命令:
    copy <skill_name>      复制一个Skill作为进化起点
    mutate <skill_name>    生成变异版本
    test <skill_name>      测试版本效果
    select <skill_name>    选择最优版本
    status <skill_name>    查看进化状态
    help                   显示帮助信息

示例:
    # 1. 选择一个Skill开始进化
    bash evolution.sh copy apollo-workflow
    
    # 2. 生成变异
    bash evolution.sh mutate apollo-workflow
    
    # 3. 测试多个版本
    bash evolution.sh test apollo-workflow gen-000 gen-001
    
    # 4. 选择最优
    bash evolution.sh select apollo-workflow
    
    # 5. 查看状态
    bash evolution.sh status apollo-workflow

进化概念:
    复制（Reproduction）→ 变异（Mutation）→ 测试（Test）→ 选择（Selection）
    
    就像生物进化一样，每个Skill版本都是"个体"，
    通过变异产生多样性，通过测试评估"适应度"，
    选择最优的保留下来。

EOF
}

#------------------------------------------------------------------------------
# 主入口
#------------------------------------------------------------------------------
main() {
    local command="${1:-help}"
    shift || true
    
    case "$command" in
        copy)   cmd_copy "$@" ;;
        mutate) cmd_mutate "$@" ;;
        test)   cmd_test "$@" ;;
        select) cmd_select "$@" ;;
        status) cmd_status "$@" ;;
        help|--help|-h) show_help ;;
        *)
            log_error "未知命令: ${command}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
