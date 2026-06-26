#!/bin/bash
# 优设读报 - 自动抓取脚本
# 用途: 定时自动抓取优设读报最新新闻
# 使用: 配合 cron 定时任务使用

set -e

# 配置
SCRIPT_DIR="$HOME/.qclaw/workspace/scripts"
FETCH_SCRIPT="$SCRIPT_DIR/fetch_uisdc_news.py"
OUTPUT_DIR="$HOME/.qclaw/workspace/news_archive"
LOG_DIR="$HOME/.qclaw/workspace/logs"
LOG_FILE="$LOG_DIR/uisdc_news_fetch.log"

# 创建必要的目录
mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 错误处理
error_exit() {
    log "❌ 错误: $1"
    exit 1
}

# 开始日志
log "🚀 开始抓取优设读报新闻..."

# 检查脚本是否存在
if [ ! -f "$FETCH_SCRIPT" ]; then
    error_exit "抓取脚本不存在: $FETCH_SCRIPT"
fi

# 执行抓取
if python3 "$FETCH_SCRIPT" --output "$OUTPUT_DIR" --hours 24; then
    log "✅ 抓取成功"
    
    # 统计文件
    FILE_COUNT=$(find "$OUTPUT_DIR" -name "uisdc_news_*.txt" -type f | wc -l)
    log "📊 已保存 $FILE_COUNT 个文件"
    
    # 清理旧文件 (保留最近 30 天)
    find "$OUTPUT_DIR" -name "uisdc_news_*.txt" -type f -mtime +30 -delete
    log "🧹 已清理 30 天前的旧文件"
    
else
    error_exit "抓取失败"
fi

log "✅ 任务完成"
