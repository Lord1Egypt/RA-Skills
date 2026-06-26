#!/bin/bash
# ==============================================
# 每日记忆 AI 整理（每天 23:59 执行）
# 功能：读取原始记忆 → AI 分析提炼 → 生成结构化记忆
# ==============================================

# 移除 set -e，避免任何错误立即退出
# 保留 pipefail 以便捕获管道错误
set -o pipefail

readonly WORKSPACE_DIR="/home/admin/.openclaw/workspace"
readonly SKILL_DIR="${WORKSPACE_DIR}/skills/daily-learning-cards"
readonly LOG_DIR="${WORKSPACE_DIR}/logs"
readonly LOG_FILE="${LOG_DIR}/refine-memory-cron.log"

init() {
  mkdir -p "${LOG_DIR}"
}

log() {
  local level="$1"
  local msg="$2"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${level}] ${msg}" >> "${LOG_FILE}"
}

main() {
  local today=$(date '+%Y-%m-%d')
  log "INFO" "=== 每日记忆 AI 整理任务启动 [${today}] ==="
  
  # 检查 Node.js 是否可用
  if ! command -v node &> /dev/null; then
    log "ERROR" "Node.js 未安装或不在 PATH 中"
    log "ERROR" "=== 每日记忆 AI 整理任务失败：环境检查未通过 ==="
    return 1
  fi
  
  # 检查脚本是否存在
  if [[ ! -f "${SKILL_DIR}/scripts/refine-memory.js" ]]; then
    log "ERROR" "脚本文件不存在: ${SKILL_DIR}/scripts/refine-memory.js"
    log "ERROR" "=== 每日记忆 AI 整理任务失败：脚本不存在 ==="
    return 1
  fi
  
  local output
  local exit_code=0
  
  # 执行 Node.js 脚本，捕获输出和退出码
  output=$(cd "${SKILL_DIR}" && node scripts/refine-memory.js 2>&1) || exit_code=$?
  
  if [[ $exit_code -eq 0 ]]; then
    log "INFO" "脚本执行成功"
    if [[ -n "$output" ]]; then
      log "INFO" "输出: ${output}"
    fi
    log "INFO" "=== 每日记忆 AI 整理任务完成 ==="
  else
    log "ERROR" "脚本执行失败，退出码: ${exit_code}"
    if [[ -n "$output" ]]; then
      log "ERROR" "错误输出: ${output}"
    fi
    log "ERROR" "=== 每日记忆 AI 整理任务失败 ==="
  fi
  
  return $exit_code
}

init
main
exit $?

