#!/bin/bash
# Article Workflow 监控脚本
# 用法：./monitor.sh [status|report|cleanup]

set -e

# 获取脚本所在目录（相对路径，安全）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 路径定义（所有路径都在 Skill 目录内）
LOG_DIR="$SKILL_DIR/logs"
DATA_DIR="$SKILL_DIR/data"
CONFIG_FILE="$SKILL_DIR/config.json"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 创建目录
mkdir -p "$LOG_DIR" "$DATA_DIR"

# 日志文件
MAIN_LOG="$LOG_DIR/workflow.log"
ERROR_LOG="$LOG_DIR/error.log"
STATS_FILE="$DATA_DIR/stats.json"

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$MAIN_LOG"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$ERROR_LOG"
}

# 安全验证：确保所有路径在 Skill 目录内
validate_paths() {
    local skill_dir_resolved
    skill_dir_resolved="$(cd "$SKILL_DIR" && pwd)"
    
    local log_dir_resolved
    log_dir_resolved="$(cd "$LOG_DIR" && pwd)"
    
    # 检查日志目录是否在 Skill 目录内
    if [[ "$log_dir_resolved" != "$skill_dir_resolved"/* ]]; then
        log_error "安全错误：日志目录不在 Skill 目录内"
        log_error "  Skill 目录：$skill_dir_resolved"
        log_error "  日志目录：$log_dir_resolved"
        exit 1
    fi
    
    log "✅ 路径安全验证通过"
}

# 显示状态
show_status() {
    log "📊 文章分析工作流状态"
    echo ""
    
    # 检查日志文件
    if [ -f "$MAIN_LOG" ]; then
        LINES=$(wc -l < "$MAIN_LOG")
        log "✅ 主日志：$MAIN_LOG ($LINES 行)"
    else
        log "⚠️  主日志不存在"
    fi
    
    if [ -f "$ERROR_LOG" ]; then
        ERRORS=$(wc -l < "$ERROR_LOG")
        log "⚠️  错误日志：$ERROR_LOG ($ERRORS 行)"
    else
        log "✅ 无错误日志"
    fi
    
    # 检查缓存文件
    if [ -f "$DATA_DIR/url_cache.json" ]; then
        CACHE_SIZE=$(cat "$DATA_DIR/url_cache.json" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('urls', {})))")
        log "✅ URL 缓存：$CACHE_SIZE 条记录"
    else
        log "⚠️  URL 缓存不存在"
    fi
    
    # 检查统计数据
    if [ -f "$STATS_FILE" ]; then
        log "✅ 统计文件：$STATS_FILE"
        cat "$STATS_FILE" | python3 -m json.tool
    else
        log "⚠️  统计文件不存在"
    fi
    
    echo ""
}

# 生成报告
generate_report() {
    log "📈 生成周报..."
    
    # 获取本周数据
    WEEK_START=$(date -v -7d '+%Y-%m-%d' 2>/dev/null || date -d '7 days ago' '+%Y-%m-%d')
    
    cat > "$DATA_DIR/weekly-report.md" << EOF
# 文章分析周报

**报告周期：** $WEEK_START 至 $(date '+%Y-%m-%d')

## 统计数据

- 处理文章：X 篇
- 平均评分：X 分
- S 级文章：X 篇
- A 级文章：X 篇

## 高质量文章 Top 5

1. [文章标题](链接) - 评分
2. [文章标题](链接) - 评分
3. [文章标题](链接) - 评分
4. [文章标题](链接) - 评分
5. [文章标题](链接) - 评分

## 热门标签

- 标签 1: X 次
- 标签 2: X 次
- 标签 3: X 次

## 下周建议

[根据本周分析结果生成建议]

---
*生成时间：$(date '+%Y-%m-%d %H:%M:%S')*
EOF
    
    log "✅ 周报已生成：$DATA_DIR/weekly-report.md"
}

# 清理旧数据
cleanup() {
    log "🧹 清理旧数据..."
    
    # 清理 30 天前的日志
    find "$LOG_DIR" -name "*.log" -mtime +30 -delete
    log "✅ 已清理 30 天前的日志"
    
    # 清理缓存（保留最近 1000 条）
    if [ -f "$DATA_DIR/url_cache.json" ]; then
        python3 << 'PYTHON'
import json
from pathlib import Path

# 使用相对路径（安全）
script_dir = Path(__file__).parent.parent if '__file__' in dir() else Path.cwd()
data_dir = script_dir / "data"
cache_file = data_dir / "url_cache.json"

if cache_file.exists():
    with open(cache_file, 'r', encoding='utf-8') as f:
        cache = json.load(f)
    
    urls = cache.get('urls', {})
    if len(urls) > 1000:
        # 保留最近 1000 条
        sorted_urls = sorted(urls.items(), key=lambda x: x[1].get('added_at', ''), reverse=True)
        cache['urls'] = dict(sorted_urls[:1000])
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 缓存已清理：保留{len(cache['urls'])}条记录")
    else:
        print(f"✅ 缓存无需清理：当前{len(urls)}条记录")
PYTHON
    fi
    
    log "✅ 清理完成"
}

# 主程序
main() {
    # 安全验证
    validate_paths
    
    case "${1:-status}" in
        status)
            show_status
            ;;
        report)
            generate_report
            ;;
        cleanup)
            cleanup
            ;;
        *)
            echo "用法：$0 {status|report|cleanup}"
            echo ""
            echo "  status   - 显示工作流状态"
            echo "  report   - 生成周报"
            echo "  cleanup  - 清理旧数据"
            exit 1
            ;;
    esac
}

main "$@"
