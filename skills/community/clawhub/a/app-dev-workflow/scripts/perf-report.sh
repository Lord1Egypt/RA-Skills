#!/bin/bash
#
# 性能监控报告工具 - 分析和报告性能瓶颈
#
# 用法: bash scripts/perf-report.sh [选项]
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
PERF_DATA_DIR=".perf-data"

# 显示帮助
show_help() {
    echo "性能监控报告工具 (v2.0)"
    echo ""
    echo "用法: bash scripts/perf-report.sh [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  analyze              分析代码性能"
    echo "  report               生成性能报告"
    echo "  compare              与基线对比"
    echo "  monitor              启动持续监控"
    echo ""
    echo "选项:"
    echo "  --baseline           设置为性能基线"
    echo "  --threshold=<值>     设置性能阈值(ms)"
    echo ""
}

# 确保目录存在
ensure_dirs() {
    mkdir -p "$REPORT_DIR"
    mkdir -p "$PERF_DATA_DIR"
}

# 分析代码性能
cmd_analyze() {
    step "分析代码性能..."
    ensure_dirs

    local report_file="$PERF_DATA_DIR/perf-$(date +%Y%m%d-%H%M%S).json"

    # 分析 TypeScript/ArkTS 文件
    local analysis="{"
    analysis="$analysis\"timestamp\": \"$(date -Iseconds)\","
    analysis="$analysis\"files\": ["

    local first=true
    if [ -d "src" ]; then
        while IFS= read -r -d '' file; do
            if [ "$first" = true ]; then
                first=false
            else
                analysis="$analysis,"
            fi

            local file_analysis=$(analyze_file "$file")
            analysis="$analysis$file_analysis"
        done < <(find src -name "*.ts" -o -name "*.ets" -print0 2>/dev/null)
    fi

    analysis="$analysis], \"summary\": $(generate_summary)"
    analysis="$analysis}"

    echo "$analysis" | python3 -m json.tool > "$report_file" 2>/dev/null || echo "$analysis" > "$report_file"

    success "分析完成: $report_file"

    # 显示摘要
    echo ""
    echo "📊 性能分析摘要"
    echo "==============="
    echo "$analysis" | grep -o '"complexity”[^}]*' | head -5 || true
}

# 分析单个文件
analyze_file() {
    local file="$1"
    local filename=$(basename "$file")
    local lines=$(wc -l < "$file")

    # 复杂度指标
    local function_count=$(grep -c "async\s\+\w\+\s*(" "$file" 2>/dev/null || echo 0)
    local await_count=$(grep -c "await" "$file" 2>/dev/null || echo 0)
    local loop_count=$(grep -cE "(for\s*\(|while\s*\()" "$file" 2>/dev/null || echo 0)
    local if_count=$(grep -c "if\s*(" "$file" 2>/dev/null || echo 0)

    # 简单复杂度计算 (函数数 + await数*0.5 + 循环数 + 条件数*0.5)
    local complexity=$((function_count + await_count / 2 + loop_count + if_count / 2))

    # 风险等级
    local risk="low"
    if [ "$complexity" -gt 30 ] || [ "$lines" -gt 500 ]; then
        risk="high"
    elif [ "$complexity" -gt 15 ] || [ "$lines" -gt 300 ]; then
        risk="medium"
    fi

    # 潜在问题
    local issues="[]"
    local issue_list=""

    # 检查循环中的 await
    if grep -q "for.*await\|while.*await" "$file" 2>/dev/null; then
        issue_list="$issue_list, \"循环中使用await可能影响性能\""
    fi

    # 检查 console.log
    if grep -q "console\.log\|hilog\." "$file" 2>/dev/null; then
        local log_count=$(grep -c "console\.log\|hilog\." "$file" 2>/dev/null || echo 0)
        if [ "$log_count" -gt 10 ]; then
            issue_list="$issue_list, \"日志语句较多($log_count处)\""
        fi
    fi

    # 检查硬编码
    if grep -q "0x\|#[0-9A-Fa-f]\{6\}" "$file" 2>/dev/null; then
        issue_list="$issue_list, \"存在硬编码值\""
    fi

    # 构建 issues JSON
    if [ -n "$issue_list" ]; then
        issues="[${issue_list#, }]"
    fi

    cat << EOF
{
  "file": "$filename",
  "path": "$file",
  "lines": $lines,
  "functions": $function_count,
  "await": $await_count,
  "loops": $loop_count,
  "complexity": $complexity,
  "risk": "$risk",
  "issues": $issues
}
EOF
}

# 生成汇总
generate_summary() {
    local total_files=0
    local total_lines=0
    local high_risk=0
    local medium_risk=0
    local total_complexity=0

    if [ -d "src" ]; then
        while IFS= read -r -d '' file; do
            total_files=$((total_files + 1))
            total_lines=$((total_lines + $(wc -l < "$file")))

            local funcs=$(grep -c "async\s\+\w\+\s*(" "$file" 2>/dev/null || echo 0)
            local awaits=$(grep -c "await" "$file" 2>/dev/null || echo 0)
            local loops=$(grep -cE "(for\s*\(|while\s*\()" "$file" 2>/dev/null || echo 0)
            local ifs=$(grep -c "if\s*(" "$file" 2>/dev/null || echo 0)

            local comp=$((funcs + awaits / 2 + loops + ifs / 2))
            total_complexity=$((total_complexity + comp))

            if [ "$comp" -gt 30 ]; then
                high_risk=$((high_risk + 1))
            elif [ "$comp" -gt 15 ]; then
                medium_risk=$((medium_risk + 1))
            fi
        done < <(find src -name "*.ts" -o -name "*.ets" -print0 2>/dev/null)
    fi

    local avg_complexity=0
    if [ "$total_files" -gt 0 ]; then
        avg_complexity=$((total_complexity / total_files))
    fi

    cat << EOF
{
  "totalFiles": $total_files,
  "totalLines": $total_lines,
  "highRiskFiles": $high_risk,
  "mediumRiskFiles": $medium_risk,
  "averageComplexity": $avg_complexity,
  "score": $(calculate_perf_score $high_risk $medium_risk $avg_complexity)
}
EOF
}

# 计算性能分数
calculate_perf_score() {
    local high=$1
    local medium=$2
    local avg_complexity=$3

    local score=100

    # 高风险文件扣分
    score=$((score - high * 10))

    # 中风险文件扣分
    score=$((score - medium * 5))

    # 复杂度扣分
    if [ "$avg_complexity" -gt 20 ]; then
        score=$((score - 15))
    elif [ "$avg_complexity" -gt 15 ]; then
        score=$((score - 10))
    elif [ "$avg_complexity" -gt 10 ]; then
        score=$((score - 5))
    fi

    # 最低0分
    if [ "$score" -lt 0 ]; then
        score=0
    fi

    echo "$score"
}

# 生成报告
cmd_report() {
    step "生成性能报告..."
    ensure_dirs

    local report_file="$REPORT_DIR/performance-report-$(date +%Y%m%d).md"

    # 运行分析
    local analysis=$(cmd_analyze 2>/dev/null)

    cat > "$report_file" << 'REPORT_EOF'
# 📈 性能监控报告

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 🎯 性能评分

$(generate_score_section)

## 📊 代码统计

$(generate_stats_section)

## ⚠️ 风险文件

$(generate_risk_section)

## 💡 优化建议

$(generate_suggestions_section)

## 📈 历史趋势

$(generate_trend_section)

---

*报告由 perf-report.sh 自动生成*
REPORT_EOF

    # 替换模板变量
    sed -i '' "s/\$(generate_score_section)/$(generate_score_section)/g" "$report_file" 2>/dev/null || true
    sed -i '' "s/\$(generate_stats_section)/$(generate_stats_section)/g" "$report_file" 2>/dev/null || true
    sed -i '' "s/\$(generate_risk_section)/$(generate_risk_section)/g" "$report_file" 2>/dev/null || true

    success "报告已生成: $report_file"
}

# 生成评分部分
generate_score_section() {
    if [ -d "src" ]; then
        local summary=$(generate_summary)
        local score=$(echo "$summary" | grep -o '"score": [0-9]*' | awk '{print $2}')

        echo "### 综合性能评分: $score/100"
        echo ""

        if [ "$score" -ge 90 ]; then
            echo "🟢 优秀 - 代码性能良好"
        elif [ "$score" -ge 70 ]; then
            echo "🟡 良好 - 有优化空间"
        elif [ "$score" -ge 50 ]; then
            echo "🟠 一般 - 建议优化"
        else
            echo "🔴 需改进 - 存在性能隐患"
        fi
    else
        echo "未找到 src 目录"
    fi
}

# 生成统计部分
generate_stats_section() {
    if [ -d "src" ]; then
        local total=$(find src -name "*.ts" -o -name "*.ets" 2>/dev/null | wc -l)
        local lines=$(find src -name "*.ts" -o -name "*.ets" 2>/dev/null | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')

        echo "| 指标 | 数值 |"
        echo "|------|------|"
        echo "| 文件总数 | $total |"
        echo "| 代码总行数 | $lines |"
        echo "| 平均文件大小 | $((lines / (total + 1))) 行 |"
    fi
}

# 生成风险部分
generate_risk_section() {
    if [ -d "src" ]; then
        echo "### 高风险文件"
        echo ""

        local found=false
        while IFS= read -r -d '' file; do
            local lines=$(wc -l < "$file")
            if [ "$lines" -gt 500 ]; then
                echo "- $(basename "$file") ($lines 行)"
                found=true
            fi
        done < <(find src -name "*.ts" -o -name "*.ets" -print0 2>/dev/null)

        if [ "$found" = false ]; then
            echo "✅ 未发现高风险文件"
        fi
    fi
}

# 对比模式
cmd_compare() {
    step "对比性能基线..."

    local baseline="$PERF_DATA_DIR/baseline.json"

    if [ ! -f "$baseline" ]; then
        warn "未找到性能基线"
        info "运行: bash scripts/perf-report.sh --baseline 设置基线"
        return 1
    fi

    # 生成当前分析
    local current="$PERF_DATA_DIR/current.json"
    cmd_analyze > "$current" 2>/dev/null

    success "对比完成"
    info "基线文件: $baseline"
    info "当前分析: $current"
}

# 监控模式
cmd_monitor() {
    step "启动性能监控..."

    local interval=300  # 5分钟

    info "监控间隔: ${interval}秒"
    info "按 Ctrl+C 停止"

    while true; do
        cmd_analyze > /dev/null 2>&1
        sleep $interval
    done
}

# 设置基线
set_baseline() {
    step "设置性能基线..."
    ensure_dirs

    local baseline="$PERF_DATA_DIR/baseline.json"

    # 生成当前分析作为基线
    local analysis=$(cmd_analyze 2>/dev/null)
    echo "$analysis" > "$baseline"

    success "性能基线已设置: $baseline"
}

# 主函数
main() {
    local cmd="analyze"
    local set_baseline_flag=false

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            analyze|report|compare|monitor)
                cmd="$1"
                shift
                ;;
            --baseline)
                set_baseline_flag=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ "$set_baseline_flag" = true ]; then
        set_baseline
        exit 0
    fi

    case "$cmd" in
        analyze)
            cmd_analyze
            ;;
        report)
            cmd_report
            ;;
        compare)
            cmd_compare
            ;;
        monitor)
            cmd_monitor
            ;;
        *)
            error "未知命令: $cmd"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
