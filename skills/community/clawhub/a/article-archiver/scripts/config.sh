#!/bin/bash
# Article Archiver Configuration

# 飞书知识库配置
FEISHU_ROOT_NODE="PS7lwR0vfiryRckijxBcFmXhnWd"
FEISHU_ROOT_URL="https://qingzhao.feishu.cn/wiki/PS7lwR0vfiryRckijxBcFmXhnWd"
ARCHIVE_FOLDER_NAME="原始文章"

# 本地配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
STATE_DIR="${SKILL_DIR}/state"
LOG_DIR="${SKILL_DIR}/logs"

# 创建必要目录
mkdir -p "$STATE_DIR" "$LOG_DIR"

# 状态文件
ARCHIVED_URLS_FILE="${STATE_DIR}/archived_urls.txt"
FOLDER_CACHE_FILE="${STATE_DIR}/folder_cache.json"

# 日志文件
LOG_FILE="${LOG_DIR}/archive_$(date +%Y-%m-%d).log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $*" | tee -a "$LOG_FILE" >&2
}
