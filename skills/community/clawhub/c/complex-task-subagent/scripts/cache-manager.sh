#!/bin/bash
# 子代理缓存管理脚本
# 用于管理子代理的临时缓存文件

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助信息
show_help() {
    cat << EOF
子代理缓存管理脚本

用法: $0 <action> [options]

操作:
  create <phase> <subagent>    为指定阶段和子代理创建缓存文件
  read <cache_file>             读取缓存文件内容
  update <cache_file> <data>    更新缓存文件
  delete <cache_file>           删除缓存文件
  list [pattern]                列出所有缓存文件（支持模式匹配）
  recover <cache_file>          从缓存恢复任务
  cleanup [days]                清理超过指定天数的旧缓存（默认: 7天）
  stats                         显示缓存统计信息

选项:
  -h, --help                    显示此帮助信息
  -v, --verbose                 详细输出模式
  --cache-dir <path>            缓存目录路径
  --dry-run                     只显示将要执行的操作，不实际执行

示例:
  # 为 phase3 创建缓存
  $0 create phase3 subagent-cdp-guide

  # 读取缓存文件
  $0 read phase3-cache.json

  # 更新缓存文件
  $0 update phase3-cache.json '{"step": 2, "data": {...}}'

  # 列出所有缓存
  $0 list

  # 清理7天前的旧缓存
  $0 cleanup 7

  # 从缓存恢复任务
  $0 recover phase3-cache.json

  # 查看缓存统计
  $0 stats
EOF
}

# 默认值
CACHE_DIR="./cache"
VERBOSE=false
DRY_RUN=false

# 解析全局参数
shift_count=0
for arg in "$@"; do
    case $arg in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift_count=$((shift_count + 1))
            ;;
        --cache-dir)
            CACHE_DIR="$2"
            shift_count=$((shift_count + 2))
            ;;
        --dry-run)
            DRY_RUN=true
            shift_count=$((shift_count + 1))
            ;;
        *)
            # 不是全局参数，停止解析
            break
            ;;
    esac
done

# 移除已解析的全局参数
shift $shift_count

# 检查是否提供了操作
if [ $# -lt 1 ]; then
    log_error "缺少操作参数"
    show_help
    exit 1
fi

ACTION="$1"
shift

# 创建缓存目录
ensure_cache_dir() {
    if [ ! -d "$CACHE_DIR" ]; then
        log_info "创建缓存目录: $CACHE_DIR"
        if [ "$DRY_RUN" = false ]; then
            mkdir -p "$CACHE_DIR"
        fi
    fi
}

# 创建缓存文件
create_cache() {
    local phase="$1"
    local subagent="$2"
    local cache_file="${phase}-cache.json"
    local cache_path="$CACHE_DIR/$cache_file"

    ensure_cache_dir

    log_info "创建缓存文件: $cache_path"

    if [ -f "$cache_path" ]; then
        log_warn "缓存文件已存在，将被覆盖"
    fi

    local cache_content=$(cat << EOF
{
  "phase": "$phase",
  "subagent": "$subagent",
  "status": "in_progress",
  "currentStep": 0,
  "totalSteps": 1,
  "data": {},
  "metadata": {
    "createdAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "updatedAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "version": "1.0"
  }
}
EOF
)

    if [ "$DRY_RUN" = false ]; then
        echo "$cache_content" > "$cache_path"
        log_info "✅ 缓存文件已创建"
    else
        log_info "[DRY RUN] 将创建缓存文件: $cache_path"
        echo "$cache_content"
    fi
}

# 读取缓存文件
read_cache() {
    local cache_file="$1"
    local cache_path="$CACHE_DIR/$cache_file"

    if [ ! -f "$cache_path" ]; then
        log_error "缓存文件不存在: $cache_path"
        exit 1
    fi

    if [ "$VERBOSE" = true ]; then
        log_info "读取缓存文件: $cache_path"
    fi

    cat "$cache_path"
}

# 更新缓存文件
update_cache() {
    local cache_file="$1"
    local data="$2"
    local cache_path="$CACHE_DIR/$cache_file"

    if [ ! -f "$cache_path" ]; then
        log_error "缓存文件不存在: $cache_path"
        exit 1
    fi

    log_info "更新缓存文件: $cache_path"

    # 更新缓存文件
    local updated_content=$(jq --argjson new_data "$data" \
       '.data = $new_data |
        .currentStep += 1 |
        .metadata.updatedAt = "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"' \
       "$cache_path")

    if [ "$DRY_RUN" = false ]; then
        echo "$updated_content" > "$cache_path"
        log_info "✅ 缓存文件已更新"
    else
        log_info "[DRY RUN] 将更新缓存文件: $cache_path"
        echo "$updated_content"
    fi
}

# 删除缓存文件
delete_cache() {
    local cache_file="$1"
    local cache_path="$CACHE_DIR/$cache_file"

    if [ ! -f "$cache_path" ]; then
        log_error "缓存文件不存在: $cache_path"
        exit 1
    fi

    log_info "删除缓存文件: $cache_path"

    if [ "$DRY_RUN" = false ]; then
        rm -f "$cache_path"
        log_info "✅ 缓存文件已删除"
    else
        log_info "[DRY RUN] 将删除缓存文件: $cache_path"
    fi
}

# 列出缓存文件
list_cache() {
    local pattern="${1:-*}"
    local cache_files=("$CACHE_DIR"/${pattern}*.json)

    if [ ! -d "$CACHE_DIR" ]; then
        log_warn "缓存目录不存在: $CACHE_DIR"
        return
    fi

    local count=0
    log_info "缓存文件列表:"

    for cache_file in "${cache_files[@]}"; do
        if [ -f "$cache_file" ]; then
            count=$((count + 1))
            local filename=$(basename "$cache_file")

            if [ "$VERBOSE" = true ]; then
                echo ""
                echo "  文件: $filename"
                echo "  路径: $cache_file"
                echo "  大小: $(stat -c%s "$cache_file") bytes"
                echo "  修改时间: $(stat -c%y "$cache_file")"
                echo "  内容:"
                jq -r '"    Phase: \(.phase)\n    子代理: \(.subagent)\n    状态: \(.status)\n    步骤: \(.currentStep)/\(.totalSteps)"' "$cache_file"
            else
                echo "  - $filename"
            fi
        fi
    done

    echo ""
    if [ "$count" -eq 0 ]; then
        log_info "未找到匹配的缓存文件"
    else
        log_info "共找到 $count 个缓存文件"
    fi
}

# 从缓存恢复任务
recover_cache() {
    local cache_file="$1"
    local cache_path="$CACHE_DIR/$cache_file"

    if [ ! -f "$cache_path" ]; then
        log_error "缓存文件不存在: $cache_path"
        exit 1
    fi

    log_info "从缓存恢复任务: $cache_path"

    # 读取缓存信息
    local phase=$(jq -r '.phase' "$cache_path")
    local subagent=$(jq -r '.subagent' "$cache_path")
    local current_step=$(jq -r '.currentStep' "$cache_path")
    local total_steps=$(jq -r '.totalSteps' "$cache_path")
    local data=$(jq -c '.data' "$cache_path")

    echo ""
    echo "=========================================="
    echo "      缓存恢复信息"
    echo "=========================================="
    echo ""
    echo "阶段: $phase"
    echo "子代理: $subagent"
    echo "当前步骤: $current_step / $total_steps"
    echo "缓存数据: $data"
    echo ""

    if [ "$DRY_RUN" = false ]; then
        log_info "准备重新启动子代理..."

        # 这里应该调用 sessions_spawn 重新启动子代理
        # 但由于这个脚本可能不在 OpenClaw 环境中运行，我们只输出恢复信息
        log_warn "请手动使用以下命令重新启动子代理："
        echo ""
        echo "sessions_spawn \\"
        echo "  --task '任务描述 - 从缓存恢复: $data' \\"
        echo "  --label '${subagent}-retry' \\"
        echo "  --runtime 'subagent' \\"
        echo "  --mode 'run' \\"
        echo "  --timeoutSeconds 3600"
    else
        log_info "[DRY RUN] 将从缓存恢复任务: $cache_path"
    fi
}

# 清理旧缓存
cleanup_cache() {
    local days="${1:-7}"
    local cutoff_time=$(date -d "$days days ago" +%s)

    log_info "清理 $days 天前的旧缓存文件..."

    if [ ! -d "$CACHE_DIR" ]; then
        log_warn "缓存目录不存在: $CACHE_DIR"
        return
    fi

    local count=0
    local total_size=0

    while IFS= read -r -d '' cache_file; do
        local file_mtime=$(stat -c%Y "$cache_file")
        if [ "$file_mtime" -lt "$cutoff_time" ]; then
            count=$((count + 1))
            local file_size=$(stat -c%s "$cache_file")
            total_size=$((total_size + file_size))

            if [ "$DRY_RUN" = false ]; then
                rm -f "$cache_file"
                log_info "已删除: $(basename "$cache_file")"
            else
                log_info "[DRY RUN] 将删除: $(basename "$cache_file")"
            fi
        fi
    done < <(find "$CACHE_DIR" -name "*.json" -print0)

    echo ""
    if [ "$count" -eq 0 ]; then
        log_info "没有需要清理的缓存文件"
    else
        log_info "✅ 已清理 $count 个旧缓存文件，释放空间: $(numfmt --to=iec $total_size)"
    fi
}

# 显示缓存统计信息
show_stats() {
    if [ ! -d "$CACHE_DIR" ]; then
        log_warn "缓存目录不存在: $CACHE_DIR"
        return
    fi

    log_info "缓存统计信息:"

    local total_files=0
    local total_size=0
    local in_progress=0
    local completed=0
    local failed=0

    while IFS= read -r -d '' cache_file; do
        if [ -f "$cache_file" ]; then
            total_files=$((total_files + 1))
            total_size=$((total_size + $(stat -c%s "$cache_file")))

            local status=$(jq -r '.status' "$cache_file" 2>/dev/null || echo "unknown")
            case "$status" in
                in_progress)
                    in_progress=$((in_progress + 1))
                    ;;
                completed)
                    completed=$((completed + 1))
                    ;;
                failed)
                    failed=$((failed + 1))
                    ;;
            esac
        fi
    done < <(find "$CACHE_DIR" -name "*.json" -print0)

    echo ""
    echo "  总文件数: $total_files"
    echo "  总大小: $(numfmt --to=iec $total_size)"
    echo "  进行中: $in_progress"
    echo "  已完成: $completed"
    echo "  已失败: $failed"
    echo ""

    if [ "$total_files" -gt 0 ]; then
        echo "  缓存目录: $CACHE_DIR"
    fi
}

# 执行操作
case "$ACTION" in
    create)
        if [ $# -lt 2 ]; then
            log_error "create 操作需要 phase 和 subagent 参数"
            show_help
            exit 1
        fi
        create_cache "$1" "$2"
        ;;
    read)
        if [ $# -lt 1 ]; then
            log_error "read 操作需要 cache_file 参数"
            show_help
            exit 1
        fi
        read_cache "$1"
        ;;
    update)
        if [ $# -lt 2 ]; then
            log_error "update 操作需要 cache_file 和 data 参数"
            show_help
            exit 1
        fi
        update_cache "$1" "$2"
        ;;
    delete)
        if [ $# -lt 1 ]; then
            log_error "delete 操作需要 cache_file 参数"
            show_help
            exit 1
        fi
        delete_cache "$1"
        ;;
    list)
        list_cache "$@"
        ;;
    recover)
        if [ $# -lt 1 ]; then
            log_error "recover 操作需要 cache_file 参数"
            show_help
            exit 1
        fi
        recover_cache "$1"
        ;;
    cleanup)
        cleanup_cache "$@"
        ;;
    stats)
        show_stats
        ;;
    *)
        log_error "未知操作: $ACTION"
        show_help
        exit 1
        ;;
esac

exit 0
