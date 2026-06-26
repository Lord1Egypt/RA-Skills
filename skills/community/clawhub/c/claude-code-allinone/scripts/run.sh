#!/usr/bin/env bash
# run.sh — 统一入口,执行用户的编程需求 (review / build 双模式智能路由)
#
# 用法:
#   bash run.sh "<用户需求原文>"
#   bash run.sh --mode review "<用户需求>"
#   bash run.sh --mode build  "<用户需求>"
#   bash run.sh --cwd /path/to/workspace "<用户需求>"
#   bash run.sh --timeout 110 "<用户需求>"
#
# 模式判定:
#   - 显式 --mode 优先
#   - 否则按用户需求关键词扫描:
#       review/评审/审查/分析/评估/检查/lint/code review → review 模式
#       否则                                            → build 模式
#
# 防挂死核心(v3.1 现网验证):
#   nohup setsid claude ... </dev/null > log 2>&1 &
#   while sleep 1; check 进程; check 日志末尾;
#   超过 timeout 主动 kill -9, 输出已生成日志
#
# ⛔ 主对话 Agent 调用本脚本时,禁止叠加 pty: true,会破坏 </dev/null 隔离

set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/helpers.sh"

MODE=""
CWD=""
TIMEOUT_SEC=110
PROMPT=""

# --- 解析参数 ---
while [ $# -gt 0 ]; do
  case "$1" in
    --mode)
      MODE="$2"; shift 2 ;;
    --cwd)
      CWD="$2"; shift 2 ;;
    --timeout)
      TIMEOUT_SEC="$2"; shift 2 ;;
    --help|-h)
      grep '^#' "$0" | sed 's/^#//'
      exit 0
      ;;
    --*)
      cc_err "未知参数: $1"
      exit 2
      ;;
    *)
      if [ -z "$PROMPT" ]; then
        PROMPT="$1"
      else
        PROMPT="$PROMPT $1"
      fi
      shift
      ;;
  esac
done

if [ -z "$PROMPT" ]; then
  cc_err "缺少用户需求 prompt"
  cc_err "用法: bash run.sh \"<用户需求>\""
  exit 2
fi

# --- 自动判定模式 ---
if [ -z "$MODE" ]; then
  # 关键词扫描 (中英文都查)
  case "$PROMPT" in
    *review*|*Review*|*REVIEW*|*评审*|*审查*|*分析*|*评估*|*检查*|*lint*|*Lint*|*只读*|*read-only*)
      MODE="review"
      ;;
    *)
      MODE="build"
      ;;
  esac
fi

case "$MODE" in
  review|build) ;;
  *)
    cc_err "无效的 mode: $MODE (只支持 review / build)"
    exit 2
    ;;
esac

# --- 切到工作目录 ---
if [ -n "$CWD" ]; then
  if [ ! -d "$CWD" ]; then
    cc_err "工作目录不存在: $CWD"
    exit 2
  fi
  cd "$CWD"
fi

# --- 准备日志路径 ---
RUN_TS="$(date +%Y%m%d_%H%M%S)"
LOG_DIR="$HOME/.claude-runs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/run-${MODE}-${RUN_TS}.log"

# --- 找到 claude 可执行文件 ---
if ! command -v claude >/dev/null 2>&1; then
  if [ -x "$HOME/.npm-global/bin/claude" ]; then
    export PATH="$HOME/.npm-global/bin:$PATH"
  fi
fi
if ! command -v claude >/dev/null 2>&1; then
  cc_err "claude 命令不可用,请先运行 bash scripts/install.sh"
  exit 3
fi

# --- 环境兜底:确保 onboarding 完成 ---
cc_ensure_onboarding_completed >/dev/null 2>&1 || true

# --- 拼装 claude 命令参数 ---
CLAUDE_ARGS=( -p "$PROMPT" )

case "$MODE" in
  review)
    CLAUDE_ARGS+=( --permission-mode plan )
    cc_log "模式: review (只读分析,--permission-mode plan)"
    ;;
  build)
    CLAUDE_ARGS+=( --allowedTools "Read,Glob,Grep,LS,Bash,Edit,Write" )
    cc_log "模式: build (允许的工具: Read,Glob,Grep,LS,Bash,Edit,Write)"
    ;;
esac

cc_log "工作目录: $(pwd)"
cc_log "日志文件: $LOG_FILE"
cc_log "超时: ${TIMEOUT_SEC}s"

# --- 启动: nohup setsid + </dev/null + log file ---
# setsid 把 claude 放进新会话,完全脱离任何可能的 controlling tty
# </dev/null 把 stdin 接到 /dev/null,claude 不会读到任何东西
# >$LOG_FILE 2>&1 把所有输出落盘
nohup setsid claude "${CLAUDE_ARGS[@]}" </dev/null >"$LOG_FILE" 2>&1 &
CLAUDE_PID=$!

cc_log "Claude PID: $CLAUDE_PID"

# --- 轮询: 进程存活就继续等,到点就 kill ---
elapsed=0
while kill -0 "$CLAUDE_PID" 2>/dev/null; do
  if [ "$elapsed" -ge "$TIMEOUT_SEC" ]; then
    cc_warn "超时 ${TIMEOUT_SEC}s,主动结束 PID $CLAUDE_PID"
    kill -9 "$CLAUDE_PID" 2>/dev/null || true
    sleep 1
    break
  fi
  sleep 1
  elapsed=$((elapsed + 1))
done

# 等 1 秒让最后的 buffer flush 到日志
sleep 1

# --- 输出: 取日志末尾若干行 ---
cc_log "================ Claude Code 输出 (来自 $LOG_FILE) ================"
if [ -s "$LOG_FILE" ]; then
  # 取最后 400 行避免太多;如果整体不到 400 行就全打
  TOTAL_LINES="$(wc -l < "$LOG_FILE" 2>/dev/null || echo 0)"
  if [ "$TOTAL_LINES" -le 400 ]; then
    cat "$LOG_FILE"
  else
    echo "...(前 $((TOTAL_LINES - 400)) 行已省略,完整日志见 $LOG_FILE)..."
    tail -n 400 "$LOG_FILE"
  fi
else
  cc_warn "日志为空,可能 claude 启动失败或网络中断"
fi

cc_log "================ 输出结束 ================"
cc_log "✅ run 结束,完整日志保留在: $LOG_FILE"
