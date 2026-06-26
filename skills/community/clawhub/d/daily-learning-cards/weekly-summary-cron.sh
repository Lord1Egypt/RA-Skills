#!/bin/bash
set -eo pipefail

# ==============================================
# 每周学习汇总（每周一 11:00 执行）
# V2: AI 智能生成周报（替代 shell 模板拼接）
#
# 流程：
#   1. 检查考题已提取的数据文件（如不存在则先提取）
#   2. generate-summary-v2.js → 调用 AI 生成周报
#   3. 发送概要到飞书群
# ==============================================

readonly WORKSPACE_DIR="/home/admin/.openclaw/workspace"
readonly SKILL_DIR="${WORKSPACE_DIR}/skills/daily-learning-cards"
readonly DATA_FILE="${WORKSPACE_DIR}/memory/exam-questions/last-week-data.json"
readonly LOG_DIR="${WORKSPACE_DIR}/logs"
readonly LOG_FILE="${LOG_DIR}/weekly-summary-cron.log"
readonly FEISHU_TARGET="oc_961ed2e84e1c196a9598dc6414d92ea6"

init() { mkdir -p "${LOG_DIR}"; }

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${1}] ${2}" >> "${LOG_FILE}"; }

main() {
  log "INFO" "V2 周报任务启动"

  # Step 1: 确保数据文件存在
  if [ ! -f "${DATA_FILE}" ]; then
    log "INFO" "数据文件不存在，先提取..."
    node "${SKILL_DIR}/scripts/extract-exam-data.js" >> "${LOG_FILE}" 2>&1 || {
      log "ERROR" "数据提取失败"
      exit 1
    }
  fi

  # Step 2: AI 生成周报
  log "INFO" "AI 生成周报..."
  local summary_content
  summary_content=$(node "${SKILL_DIR}/scripts/generate-summary-v2.js" 2>&1)
  local gen_exit=$?

  if [ $gen_exit -ne 0 ]; then
    log "ERROR" "周报生成失败"
    exit 1
  fi
  log "INFO" "周报生成完成"

  # Step 3: 发送概要到飞书
  local week_num start_str end_str active_days topic_count
  week_num=$(jq -r '.meta.weekNum' "${DATA_FILE}")
  start_str=$(jq -r '.meta.startStr' "${DATA_FILE}")
  end_str=$(jq -r '.meta.endStr' "${DATA_FILE}")
  active_days=$(jq -r '.stats.activeDays' "${DATA_FILE}")
  topic_count=$(jq -r '.stats.totalTopics' "${DATA_FILE}")

  local msg="📊 第${week_num}周学习汇总报告
📅 ${start_str} ~ ${end_str}
📚 活跃${active_days}天 | 主题${topic_count}个

完整报告：memory/learning-summaries/$(date -d "${end_str}" +%Y)-W${week_num}-summary.md"

  openclaw message send --channel=feishu --target="${FEISHU_TARGET}" --message="${msg}" 2>&1 | tee -a "${LOG_FILE}"
  log "INFO" "周报概要已发送 (status: ${PIPESTATUS[0]})"
  echo "✅ 周报已发送"
}

init
main
exit 0
