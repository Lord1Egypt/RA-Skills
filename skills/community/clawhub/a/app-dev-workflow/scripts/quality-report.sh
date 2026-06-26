#!/bin/bash
#
# 质量报告生成工具 - 生成详细的项目质量报告
#
# 用法: bash scripts/quality-report.sh [选项]
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️${NC}  $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $1"; }
error() { echo -e "${RED}❌${NC} $1"; }
step() { echo -e "${CYAN}▶ $1${NC}"; }

REPORT_DIR="docs/reports"
REPORT_DATE=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="$REPORT_DIR/quality-report-${REPORT_DATE}.md"
JSON_REPORT="$REPORT_DIR/quality-report-${REPORT_DATE}.json"

# 确保报告目录存在
ensure_report_dir() {
    mkdir -p "$REPORT_DIR"
}

# 收集代码统计
collect_code_stats() {
    local stats="{}"

    # 文件数量
    local total_files=0
    local ts_files=0
    local ets_files=0
    local test_files=0

    if [ -d "src" ]; then
        total_files=$(find src -type f | wc -l)
        ts_files=$(find src -name "*.ts" -type f 2>/dev/null | wc -l)
        ets_files=$(find src -name "*.ets" -type f 2>/dev/null | wc -l)
    fi

    if [ -d "test" ]; then
        test_files=$(find test -name "*.test.ts" -o -name "*.spec.ts" 2>/dev/null | wc -l)
    fi

    # 代码行数
    local loc=0
    if [ -d "src" ]; then
        loc=$(find src -name "*.ts" -o -name "*.ets" 2>/dev/null | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}' || echo 0)
    fi

    echo "{\"totalFiles\": $total_files, \"tsFiles\": $ts_files, \"etsFiles\": $ets_files, \"testFiles\": $test_files, \"loc\": $loc}"
}

# 分析 TODO
count_todos() {
    local count=0
    local critical=0

    if [ -d "src" ]; then
        count=$(grep -r "\[TODO\]" src/ 2>/dev/null | wc -l || echo 0)
        critical=$(grep -r "\[CRITICAL\]" src/ 2>/dev/null | wc -l || echo 0)
    fi

    echo "{\"total\": $count, \"critical\": $critical}"
}

# 检查文档
check_docs() {
    local readme=0
    local prd=0
    local api=0
    local architecture=0

    [ -f "README.md" ] && readme=1
    [ -f "PROJECT.md" ] && readme=1
    [ -d "docs/prd" ] && prd=$(find docs/prd -name "*.md" 2>/dev/null | wc -l)
    [ -d "docs/api" ] && api=$(find docs/api -name "*.md" 2>/dev/null | wc -l)
    [ -d "docs/architecture" ] && architecture=$(find docs/architecture -name "*.mmd" 2>/dev/null | wc -l)

    echo "{\"readme\": $readme, \"prdCount\": $prd, \"apiCount\": $api, \"diagrams\": $architecture}"
}

# 分析 Git
collect_git_stats() {
    if [ ! -d ".git" ]; then
        echo "{\"commits\": 0, \"branches\": 0, \"contributors\": 0, \"lastCommit\": \"\"}"
        return
    fi

    local commits=$(git rev-list --count HEAD 2>/dev/null || echo 0)
    local branches=$(git branch -a | wc -l)
    local contributors=$(git log --format='%an' | sort -u | wc -l)
    local last_commit=$(git log -1 --format=%cd --date=iso 2>/dev/null || echo "")

    echo "{\"commits\": $commits, \"branches\": $branches, \"contributors\": $contributors, \"lastCommit\": \"$last_commit\"}"
}

# 计算综合得分
calculate_score() {
    local stats="$1"
    local score=0
    local max_score=100

    # 代码覆盖率评分 (30分)
    local test_files=$(echo "$stats" | grep -o '"testFiles": [0-9]*' | awk '{print $2}')
    local ts_files=$(echo "$stats" | grep -o '"tsFiles": [0-9]*' | awk '{print $2}')

    if [ "$ts_files" -gt 0 ]; then
        local coverage=$((test_files * 100 / ts_files))
        if [ "$coverage" -ge 80 ]; then
            score=$((score + 30))
        elif [ "$coverage" -ge 60 ]; then
            score=$((score + 25))
        elif [ "$coverage" -ge 40 ]; then
            score=$((score + 20))
        elif [ "$coverage" -ge 20 ]; then
            score=$((score + 10))
        else
            score=$((score + 5))
        fi
    fi

    # 文档评分 (20分)
    local docs=$(check_docs)
    local has_readme=$(echo "$docs" | grep -o '"readme": [0-9]*' | awk '{print $2}')
    local prd_count=$(echo "$docs" | grep -o '"prdCount": [0-9]*' | awk '{print $2}')

    [ "$has_readme" -eq 1 ] && score=$((score + 10))
    [ "$prd_count" -gt 0 ] && score=$((score + 10))

    # TODO处理评分 (20分)
    local todos=$(count_todos)
    local todo_count=$(echo "$todos" | grep -o '"total": [0-9]*' | awk '{print $2}')

    if [ "$todo_count" -eq 0 ]; then
        score=$((score + 20))
    elif [ "$todo_count" -lt 5 ]; then
        score=$((score + 15))
    elif [ "$todo_count" -lt 10 ]; then
        score=$((score + 10))
    elif [ "$todo_count" -lt 20 ]; then
        score=$((score + 5))
    fi

    # 代码规范评分 (15分)
    if [ -f "scripts/lint.sh" ]; then
        if bash scripts/lint.sh --check 2>/dev/null; then
            score=$((score + 15))
        else
            score=$((score + 8))
        fi
    else
        score=$((score + 10))
    fi

    # 架构图评分 (15分)
    local has_arch=0
    [ -d "docs/architecture" ] && has_arch=1
    [ "$has_arch" -eq 1 ] && score=$((score + 15))

    echo "$score"
}

# 生成 Markdown 报告
generate_markdown_report() {
    local stats="$1"
    local todos="$2"
    local docs="$3"
    local git="$4"
    local score="$5"

    cat > "$REPORT_FILE" << EOF
# 📊 项目质量报告

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')

---

## 📈 质量评分

<div align="center">

### 综合得分: $score / 100

$(if [ "$score" -ge 90 ]; then echo "🟢 优秀"; elif [ "$score" -ge 70 ]; then echo "🟡 良好"; elif [ "$score" -ge 50 ]; then echo "🟠 一般"; else echo "🔴 需改进"; fi)

</div>

---

## 📁 代码统计

| 指标 | 数值 |
|------|------|
| 总文件数 | $(echo "$stats" | grep -o '"totalFiles": [0-9]*' | awk '{print $2}') |
| TypeScript 文件 | $(echo "$stats" | grep -o '"tsFiles": [0-9]*' | awk '{print $2}') |
| ArkTS 文件 | $(echo "$stats" | grep -o '"etsFiles": [0-9]*' | awk '{print $2}') |
| 测试文件 | $(echo "$stats" | grep -o '"testFiles": [0-9]*' | awk '{print $2}') |
| 代码行数 | $(echo "$stats" | grep -o '"loc": [0-9]*' | awk '{print $2}') |

---

## 📝 待办事项

| 类型 | 数量 | 状态 |
|------|------|------|
| TODO | $(echo "$todos" | grep -o '"total": [0-9]*' | awk '{print $2}') | $(if [ "$(echo "$todos" | grep -o '"total": [0-9]*' | awk '{print $2}')" -eq 0 ]; then echo "✅ 已清理"; else echo "⚠️ 待处理"; fi) |
| CRITICAL | $(echo "$todos" | grep -o '"critical": [0-9]*' | awk '{print $2}') | $(if [ "$(echo "$todos" | grep -o '"critical": [0-9]*' | awk '{print $2}')" -eq 0 ]; then echo "✅ 无严重"; else echo "🔴 需关注"; fi) |

### 待办详情

EOF

    if [ -d "src" ]; then
        echo "| 文件 | 行号 | 内容 |" >> "$REPORT_FILE"
        echo "|------|------|------|" >> "$REPORT_FILE"
        grep -rn "\[TODO\]" src/ 2>/dev/null | head -20 | while IFS=: read -r file line content; do
            local todo_content=$(echo "$content" | sed 's/.*\[TODO\]//' | head -c 50)
            echo "| $file | $line | $todo_content... |" >> "$REPORT_FILE"
        done || echo "| - | - | 无 |" >> "$REPORT_FILE"
    fi

    cat >> "$REPORT_FILE" << EOF

---

## 📚 文档状况

| 文档类型 | 状态 |
|----------|------|
| README | $(if [ "$(echo "$docs" | grep -o '"readme": [0-9]*' | awk '{print $2}')" -eq 1 ]; then echo "✅ 存在"; else echo "❌ 缺失"; fi) |
| PRD 文档 | $(echo "$docs" | grep -o '"prdCount": [0-9]*' | awk '{print $2}') 个 |
| API 文档 | $(echo "$docs" | grep -o '"apiCount": [0-9]*' | awk '{print $2}') 个 |
| 架构图 | $(echo "$docs" | grep -o '"diagrams": [0-9]*' | awk '{print $2}') 个 |

---

## 🌿 Git 统计

| 指标 | 数值 |
|------|------|
| 提交数 | $(echo "$git" | grep -o '"commits": [0-9]*' | awk '{print $2}') |
| 分支数 | $(echo "$git" | grep -o '"branches": [0-9]*' | awk '{print $2}') |
| 贡献者 | $(echo "$git" | grep -o '"contributors": [0-9]*' | awk '{print $2}') |
| 最后提交 | $(echo "$git" | grep -o '"lastCommit": "[^"]*"' | cut -d'"' -f4 | head -c 19) |

---

## 🎯 改进建议

$(generate_suggestions "$score" "$todos" "$docs")

---

## 📊 评分详情

| 维度 | 满分 | 得分 | 说明 |
|------|------|------|------|
| 测试覆盖 | 30 | $(if [ "$score" -ge 90 ]; then echo "30"; elif [ "$score" -ge 80 ]; then echo "25"; elif [ "$score" -ge 70 ]; then echo "20"; else echo "15"; fi) | 测试文件比例 |
| 文档完整 | 20 | $(if [ "$(echo "$docs" | grep -o '"readme": [0-9]*' | awk '{print $2}')" -eq 1 ]; then echo "20"; elif [ "$(echo "$docs" | grep -o '"prdCount": [0-9]*' | awk '{print $2}')" -gt 0 ]; then echo "10"; else echo "5"; fi) | README + PRD |
| 代码清理 | 20 | $(if [ "$(echo "$todos" | grep -o '"total": [0-9]*' | awk '{print $2}')" -eq 0 ]; then echo "20"; elif [ "$(echo "$todos" | grep -o '"total": [0-9]*' | awk '{print $2}')" -lt 5 ]; then echo "15"; else echo "10"; fi) | TODO 处理 |
| 代码规范 | 15 | $(if [ -f "scripts/lint.sh" ]; then echo "15"; else echo "8"; fi) | Lint 检查 |
| 架构文档 | 15 | $(if [ "$(echo "$docs" | grep -o '"diagrams": [0-9]*' | awk '{print $2}')" -gt 0 ]; then echo "15"; else echo "0"; fi) | 架构图 |

---

*报告由 AppDev-Skill 质量工具生成*
EOF
}

# 生成改进建议
generate_suggestions() {
    local score="$1"
    local todos="$2"
    local docs="$3"

    local suggestions=""
    local todo_count=$(echo "$todos" | grep -o '"total": [0-9]*' | awk '{print $2}')
    local has_readme=$(echo "$docs" | grep -o '"readme": [0-9]*' | awk '{print $2}')
    local prd_count=$(echo "$docs" | grep -o '"prdCount": [0-9]*' | awk '{print $2}')
    local diagram_count=$(echo "$docs" | grep -o '"diagrams": [0-9]*' | awk '{print $2}')

    if [ "$score" -ge 90 ]; then
        suggestions="1. 项目质量优秀，继续保持！\n"
    else
        if [ "$todo_count" -gt 0 ]; then
            suggestions="${suggestions}1. 处理 $todo_count 个 TODO 项\n"
        fi
        if [ "$has_readme" -eq 0 ]; then
            suggestions="${suggestions}2. 添加 README.md 文档\n"
        fi
        if [ "$prd_count" -eq 0 ]; then
            suggestions="${suggestions}3. 创建产品需求文档\n"
        fi
        if [ "$diagram_count" -eq 0 ]; then
            suggestions="${suggestions}4. 生成架构图: bash scripts/visualize.sh\n"
        fi
        if [ ! -f "scripts/lint.sh" ]; then
            suggestions="${suggestions}5. 添加代码规范检查\n"
        fi
    fi

    echo -e "$suggestions"
}

# 生成 JSON 报告
generate_json_report() {
    local stats="$1"
    local todos="$2"
    local docs="$3"
    local git="$4"
    local score="$5"

    cat > "$JSON_REPORT" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "score": $score,
  "rating": "$(if [ "$score" -ge 90 ]; then echo "excellent"; elif [ "$score" -ge 70 ]; then echo "good"; elif [ "$score" -ge 50 ]; then echo "fair"; else echo "poor"; fi)",
  "codeStats": $stats,
  "todos": $todos,
  "documentation": $docs,
  "gitStats": $git
}
EOF
}

# 主函数
main() {
    local format="markdown"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --json)
                format="json"
                shift
                ;;
            --both)
                format="both"
                shift
                ;;
            --help|-h)
                echo "质量报告生成工具"
                echo ""
                echo "用法: bash scripts/quality-report.sh [选项]"
                echo ""
                echo "选项:"
                echo "  --json     生成 JSON 格式报告"
                echo "  --both     同时生成 Markdown 和 JSON"
                echo ""
                exit 0
                ;;
            *)
                shift
                ;;
        esac
    done

    step "生成质量报告..."
    ensure_report_dir

    # 收集数据
    info "收集代码统计..."
    local stats=$(collect_code_stats)

    info "分析 TODO..."
    local todos=$(count_todos)

    info "检查文档..."
    local docs=$(check_docs)

    info "收集 Git 统计..."
    local git=$(collect_git_stats)

    info "计算综合得分..."
    local score=$(calculate_score "$stats")

    # 生成报告
    if [ "$format" = "markdown" ] || [ "$format" = "both" ]; then
        generate_markdown_report "$stats" "$todos" "$docs" "$git" "$score"
        success "Markdown 报告: $REPORT_FILE"
    fi

    if [ "$format" = "json" ] || [ "$format" = "both" ]; then
        generate_json_report "$stats" "$todos" "$docs" "$git" "$score"
        success "JSON 报告: $JSON_REPORT"
    fi

    # 输出摘要
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo "  📊 质量报告摘要"
    echo "═══════════════════════════════════════════════════"
    echo ""
    echo "  综合评分: $score / 100"
    echo "  代码文件: $(echo "$stats" | grep -o '"tsFiles": [0-9]*' | awk '{print $2}') .ts + $(echo "$stats" | grep -o '"etsFiles": [0-9]*' | awk '{print $2}') .ets"
    echo "  测试文件: $(echo "$stats" | grep -o '"testFiles": [0-9]*' | awk '{print $2}')"
    echo "  待办事项: $(echo "$todos" | grep -o '"total": [0-9]*' | awk '{print $2}')"
    echo "  文档状态: README:$(if [ "$(echo "$docs" | grep -o '"readme": [0-9]*' | awk '{print $2}')" -eq 1 ]; then echo "✅"; else echo "❌"; fi) PRD:$(echo "$docs" | grep -o '"prdCount": [0-9]*' | awk '{print $2}')"
    echo ""

    if [ "$score" -ge 90 ]; then
        success "🎉 项目质量优秀！"
    elif [ "$score" -ge 70 ]; then
        warn "📝 项目质量良好，还有提升空间"
    else
        error "🔧 项目需要改进"
    fi

    echo ""
    echo "详细报告: $REPORT_FILE"
    echo "═══════════════════════════════════════════════════"
}

main "$@"
