#!/bin/bash

# Main Controller for Review Analyzer Skill
# Orchestrates the entire analysis workflow

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$(dirname "$ROOT_DIR")")"  # 项目根目录
PROMPTS_DIR="$ROOT_DIR/prompts"
TEMPLATES_DIR="$ROOT_DIR/templates"
UTILS_DIR="$ROOT_DIR/utils"
OUTPUT_DIR="$PROJECT_ROOT/output"  # 统一输出到项目根目录

# Source utility scripts
source "$UTILS_DIR/csv_reader.sh"
source "$UTILS_DIR/tagging_core.sh"
source "$UTILS_DIR/insights_generator.sh"
source "$UTILS_DIR/html_generator.sh"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Global variables
CSV_FILE=""
MAX_RECORDS=0
ASIN="unknown"
PRODUCT_NAME=""
OUTPUT_PREFIX=""
ANALYSIS_COUNT=100

# ============================================
# LOGGING FUNCTIONS
# ============================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_progress() {
    echo -e "${CYAN}[PROGRESS]${NC} $1"
}

# ============================================
# INITIALIZATION
# ============================================

init_output_dir() {
    mkdir -p "$OUTPUT_DIR"
    log_info "Output directory: $OUTPUT_DIR"
}

# ============================================
# PARAMETER COLLECTION
# ============================================

collect_parameters() {
    log_info "收集分析参数..."

    # This function is meant to be called from the main skill
    # The actual AskUserQuestion calls will be done by Claude

    # Set defaults
    ANALYSIS_COUNT=${ANALYSIS_COUNT:-100}
    OUTPUT_PREFIX=${OUTPUT_PREFIX:-""}

    log_info "分析数量: $ANALYSIS_COUNT"
}

# ============================================
# TASK SIZE EVALUATION
# ============================================

evaluate_task_size() {
    local count="$1"
    local threshold=1000

    if [[ "$count" -ge "$threshold" ]]; then
        log_info "检测到大型任务: $count 条评论 (≥$threshold)"
        log_info "将调用 planning-with-files skill 进行任务管理"
        return 0  # Large task
    else
        log_info "检测到小型任务: $count 条评论 (<$threshold)"
        return 1  # Small task
    fi
}

# ============================================
# CSV PROCESSING
# ============================================

process_csv() {
    local csv_file="$1"

    log_info "处理 CSV 文件: $csv_file"

    if [[ ! -f "$csv_file" ]]; then
        log_error "文件不存在: $csv_file"
        return 1
    fi

    # Get file info
    CSV_FILE="$csv_file"
    local count=$("$UTILS_DIR/csv_reader.sh" "$csv_file" "count")

    log_info "检测到 $count 条评论"

    # Evaluate task size
    evaluate_task_size "$count"
    local is_large_task=$?

    # Extract ASIN from filename if possible
    local basename=$(basename "$csv_file" .csv)
    if [[ "$basename" =~ [A-Z0-9]{10} ]]; then
        ASIN=$(echo "$basename" | grep -oE "[A-Z0-9]{10}")
        log_info "检测到 ASIN: $ASIN"
    fi

    # Determine output prefix
    if [[ -z "$OUTPUT_PREFIX" ]]; then
        OUTPUT_PREFIX="$OUTPUT_DIR/评论采集及打标数据_${ASIN}"
    fi

    return $is_large_task
}

# ============================================
# BATCH TAGGING
# ============================================

batch_tag_reviews() {
    log_info "开始批量标签提取..."

    local temp_reviews="$OUTPUT_DIR/reviews_extracted.json"
    local temp_tagged="$OUTPUT_DIR/reviews_tagged.json"

    # Extract reviews from CSV
    log_progress "提取评论数据..."
    "$UTILS_DIR/csv_reader.sh" "$CSV_FILE" "extract" "$ANALYSIS_COUNT" > "$temp_reviews"

    local extracted_count=$(jq '. | length' "$temp_reviews" 2>/dev/null || echo "0")
    log_info "已提取 $extracted_count 条评论"

    if [[ "$extracted_count" -eq 0 ]]; then
        log_error "未能提取任何评论"
        return 1
    fi

    # Split into batches of 30
    log_progress "分批处理 (每批最多30条)..."
    local batch_size=30
    local total_batches=$(( (extracted_count + batch_size - 1) / batch_size ))

    log_info "共 $total_batches 个批次"

    # Process batches
    local all_tagged="[]"
    local current_batch=1

    for ((i=0; i<extracted_count; i+=batch_size)); do
        local end=$((i + batch_size))
        if [[ $end -gt $extracted_count ]]; then
            end=$extracted_count
        fi

        log_progress "处理批次 $current_batch/$total_batches (评论 $((i+1))-$end)..."

        # Extract batch
        local batch_json=$(jq ".[$i:$end]" "$temp_reviews")

        # Create prompt for batch tagging
        local prompt=$(cat "$PROMPTS_DIR/tagging_batch.txt")
        prompt="${prompt//{batch_size}/$((end - i))}"
        prompt="${prompt//{reviews_json}/$batch_json}"

        # Save prompt for AI processing
        local prompt_file="$OUTPUT_DIR/batch_${current_batch}_prompt.txt"
        echo "$prompt" > "$prompt_file"

        log_info "批次 $current_batch 提示词已保存到: $prompt_file"
        log_info "等待 AI 处理..."

        # Note: The actual AI processing will be done by the main skill
        # For now, we save the prompts and expect results to be provided

        ((current_batch++))
    done

    log_success "批次准备完成，共 $total_batches 个批次"

    # Return the prompt files list
    ls "$OUTPUT_DIR"/batch_*_prompt.txt 2>/dev/null
}

# ============================================
# RESULTS PROCESSING
# ============================================

process_tagging_results() {
    local results_dir="$1"

    log_info "处理打标结果..."

    local all_tagged="[]"
    local tagged_count=0

    # Combine all batch results
    for result_file in "$results_dir"/batch_*_result.json; do
        if [[ -f "$result_file" ]]; then
            local batch_results=$(cat "$result_file")
            all_tagged=$(echo "$all_tagged" | jq ". + $batch_results")
            ((tagged_count+=$(echo "$batch_results" | jq '. | length')))
        fi
    done

    log_success "成功打标 $tagged_count 条评论"

    # Save combined results
    local output_json="$OUTPUT_DIR/reviews_tagged.json"
    echo "$all_tagged" > "$output_json"

    echo "$output_json"
}

# ============================================
# GENERATE OUTPUTS
# ============================================

generate_csv_output() {
    local tagged_json="$1"

    log_progress "生成 CSV 标签数据..."

    local output_csv="${OUTPUT_PREFIX}.csv"

    # Use Python to merge CSV with tags
    if command -v python3 &> /dev/null; then
        python3 "$UTILS_DIR/merge_csv.py" "$CSV_FILE" "$tagged_json" "$output_csv"

        if [[ $? -eq 0 ]]; then
            log_success "CSV 标签数据已生成: $output_csv"
        else
            log_warning "CSV 生成失败，使用原始数据"
        fi
    else
        log_warning "Python3 未安装，跳过 CSV 合并"
    fi
}

generate_insights_report() {
    local tagged_json="$1"

    log_progress "生成洞察分析报告..."

    # Calculate statistics
    local stats_json=$("$UTILS_DIR/insights_generator.sh" "stats" "$tagged_json")

    # Select golden samples
    local samples_json=$("$UTILS_DIR/insights_generator.sh" "samples" "$tagged_json" "12")

    # Extract personas
    local personas_json=$(echo "$stats_json" | jq '.personas')

    # Create insights prompt
    local insights_prompt=$("$UTILS_DIR/insights_generator.sh" "prompt" \
        "$stats_json" "$personas_json" "$samples_json" "$ASIN" "$PRODUCT_NAME")

    # Save prompt for AI processing
    local prompt_file="$OUTPUT_DIR/insights_prompt.txt"
    echo "$insights_prompt" > "$prompt_file"

    log_info "洞察报告提示词已保存到: $prompt_file"
    log_info "等待 AI 生成洞察报告..."

    echo "$prompt_file"
}

process_insights_result() {
    local insights_md="$1"

    log_progress "处理洞察报告结果..."

    local output_md="${OUTPUT_DIR}/../分析洞察报告_${ASIN}.md"

    # Save markdown report
    echo "$insights_md" > "$output_md"

    log_success "洞察分析报告已生成: $output_md"

    echo "$output_md"
}

generate_html_dashboard() {
    local stats_json="$1"
    local tagged_json="$2"
    local insights_md="$3"

    log_progress "生成 HTML 可视化看板..."

    local output_html="${OUTPUT_DIR}/../可视化洞察报告_${ASIN}.html"

    # Generate HTML
    "$UTILS_DIR/html_generator.sh" "generate" \
        "$stats_json" "$tagged_json" "$insights_md" "$output_html"

    if [[ -f "$output_html" ]]; then
        log_success "HTML 可视化看板已生成: $output_html"
    fi

    echo "$output_html"
}

# ============================================
# MAIN WORKFLOW
# ============================================

run_analysis() {
    log_info "=========================================="
    log_info "Review Analyzer - 开始分析"
    log_info "=========================================="

    # Initialize
    init_output_dir

    # Process CSV
    process_csv "$1"
    local is_large_task=$?

    if [[ $is_large_task -eq 0 ]]; then
        log_info "=========================================="
        log_info "大型任务处理流程"
        log_info "=========================================="
        log_info "请调用 planning-with-files skill 进行任务管理"
        log_info "任务描述：分析 $count 条电商评论"
        log_info "=========================================="
        return 0
    fi

    # Collect parameters (done by main skill)
    collect_parameters

    # Batch tagging
    local batch_prompts=$(batch_tag_reviews)

    # Note: At this point, control returns to the main skill
    # The skill will process each prompt with AI and collect results

    log_info "=========================================="
    log_info "批次准备完成"
    log_info "=========================================="
    log_info "请使用 AI 处理以下提示词文件："
    echo "$batch_prompts"
    log_info "=========================================="
}

show_results() {
    log_info "=========================================="
    log_info "分析完成！"
    log_info "=========================================="
    log_info "输出文件位置："
    log_info "  - CSV 标签数据: ${OUTPUT_PREFIX}.csv"
    log_info "  - 洞察分析报告: ${OUTPUT_DIR}/../分析洞察报告_${ASIN}.md"
    log_info "  - HTML 可视化看板: ${OUTPUT_DIR}/../可视化洞察报告_${ASIN}.html"
    log_info "=========================================="
}

# ============================================
# MAIN ENTRY POINT
# ============================================

main() {
    local action="$1"
    shift

    case "$action" in
        "analyze")
            run_analysis "$@"
            ;;
        "results")
            show_results
            ;;
        "collect")
            collect_parameters "$@"
            ;;
        *)
            echo "Usage: $0 {analyze|results|collect} ..."
            exit 1
            ;;
    esac
}

main "$@"
