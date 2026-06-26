#!/bin/bash
set -eo pipefail

# ==============================================
# 每周学习测试生成（每周一 11:30 执行）
# V2: 数据提取器 + AI 智能出题（替代模板生成）
# 
# 流程：
#   1. extract-exam-data.js → 提取数据到 JSON
#   2. generate-exam-v2.js → 调用 AI API 生成 20 道考题
#   3. openclaw message send → 推送到飞书群
# ==============================================

readonly WORKSPACE_DIR="/home/admin/.openclaw/workspace"
readonly SKILL_DIR="${WORKSPACE_DIR}/skills/daily-learning-cards"
readonly EXAMS_DIR="${WORKSPACE_DIR}/memory/exam-questions"
readonly DATA_FILE="${EXAMS_DIR}/last-week-data.json"
readonly LOG_DIR="${WORKSPACE_DIR}/logs"
readonly LOG_FILE="${LOG_DIR}/weekly-exam-cron.log"
readonly FEISHU_TARGET="oc_961ed2e84e1c196a9598dc6414d92ea6"

init() { mkdir -p "${EXAMS_DIR}" "${LOG_DIR}"; }

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${1}] ${2}" >> "${LOG_FILE}"; }

main() {
  log "INFO" "V2 考题任务启动"

  # Step 1: 提取数据
  log "INFO" "提取学习数据..."
  local extract_result
  extract_result=$(cd "${SKILL_DIR}" && node "scripts/extract-exam-data.js" 2>&1)
  local extract_exit=$?

  if [ $extract_exit -ne 0 ]; then
    log "ERROR" "数据提取失败"
    exit 1
  fi
  log "INFO" "数据提取完成"

  # Step 2: AI 生成考题
  log "INFO" "AI 生成考题..."
  local exam_content
  exam_content=$(cd "${SKILL_DIR}" && node "scripts/generate-exam-v2.js" 2>&1)
  local gen_exit=$?

  if [ $gen_exit -ne 0 ]; then
    log "ERROR" "考题生成失败，回退到旧版"
    # Fallback to old generator
    exam_content=$(cd "${SKILL_DIR}" && node "scripts/generate-exam.js" 2>&1) || {
      log "ERROR" "旧版也失败"
      exit 1
    }
  fi

  log "INFO" "考题生成完成"

  # Step 3: 发送到飞书
  log "INFO" "发送考题到飞书..."
  openclaw message send --channel=feishu --target="${FEISHU_TARGET}" --message="${exam_content}" 2>&1 | tee -a "${LOG_FILE}"
  local send_status=${PIPESTATUS[0]}

  if [ $send_status -eq 0 ]; then
    log "INFO" "考题已推送到飞书"
    echo "✅ 考题已发送"
  else
    log "ERROR" "考题发送失败 (status: $send_status)"
    exit 1
  fi

  log "INFO" "考题任务完成"
}

init
main
exit 0