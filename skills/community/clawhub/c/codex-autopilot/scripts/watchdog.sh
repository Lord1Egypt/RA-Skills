#!/bin/bash
# watchdog.sh v4 — 统一 autopilot 守护进程 + Layer 1 自动检查
#
# 职责分工：
#   watchdog.sh (本脚本) — 快速响应，10-30秒级别
#     ✅ 权限提示 → 立即 auto-approve (p Enter)
#     ✅ idle 检测 → 5 分钟无活动自动 nudge (信号驱动)
#     ✅ 低上下文 → 发 /compact
#     ✅ shell 恢复 → codex resume
#     ✅ Layer 1: 新 commit → 自动 lint/tsc/pattern 扫描
#     ✅ 信号驱动 nudge: 连续 feat 无 test → 要求写测试
#   cron (10min) — 慢速汇报
#     ✅ 进度统计 → Telegram 报告
#     ✅ 智能 nudge → LLM 生成针对性指令
#
# 用法: 通过 launchd 管理，开机自启
# 日志: ~/.autopilot/logs/watchdog.log

# NOTE: do NOT add `set -e`.
# This script intentionally tolerates non-zero probe commands (e.g. grep no-match),
# and the ERR trap is diagnostic-only.
set -uo pipefail
TMUX="${TMUX_BIN:-$(command -v tmux || echo /opt/homebrew/bin/tmux)}"
CODEX="${CODEX_BIN:-$(command -v codex || echo /opt/homebrew/bin/codex)}"
SESSION="autopilot"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/autopilot-lib.sh"
if [ -f "${SCRIPT_DIR}/autopilot-constants.sh" ]; then
    # shellcheck disable=SC1091
    source "${SCRIPT_DIR}/autopilot-constants.sh"
fi

# ---- 时间参数 ----
TICK=10                   # 主循环间隔（秒）
NUDGE_COOLDOWN=300        # 同一窗口 nudge 冷却（秒），防止反复骚扰
PERMISSION_COOLDOWN=60    # 权限 approve 冷却（秒）
COMPACT_COOLDOWN=600      # compact 冷却（秒）
SHELL_COOLDOWN=300        # shell 恢复冷却（秒）
LOW_CONTEXT_THRESHOLD="${LOW_CONTEXT_THRESHOLD:-25}"
ACK_CHECK_MAX_JOBS="${ACK_CHECK_MAX_JOBS:-8}"
ACK_CHECK_LOCK_STALE_SECONDS="${ACK_CHECK_LOCK_STALE_SECONDS:-120}"

# ---- 路径 ----
LOG="$HOME/.autopilot/logs/watchdog.log"
LOCK_DIR="$HOME/.autopilot/locks"
STATE_DIR="$HOME/.autopilot/state"
COOLDOWN_DIR="$STATE_DIR/watchdog-cooldown"
ACTIVITY_DIR="$STATE_DIR/watchdog-activity"
COMMIT_COUNT_DIR="$STATE_DIR/watchdog-commits"
REVIEW_COOLDOWN=7200       # 增量 review 冷却（秒）= 2 小时
COMMITS_FOR_REVIEW=15      # 触发增量 review 的 commit 数
FEAT_WITHOUT_TEST_LIMIT=5  # 连续 feat 无 test 触发写测试 nudge
QUEUE_IN_PROGRESS_TIMEOUT_SECONDS="${QUEUE_IN_PROGRESS_TIMEOUT_SECONDS:-3600}"
TRACKED_TASK_TIMEOUT_SECONDS="${TRACKED_TASK_TIMEOUT_SECONDS:-3600}"
PRD_DONE_FILTER_RE='✅\|⛔\|blocked\|（done）\|(done)\|done\|完成\|^\- \[x\]\|^\- \[X\]'
mkdir -p "$(dirname "$LOG")" "$LOCK_DIR" "$COOLDOWN_DIR" "$ACTIVITY_DIR" "$COMMIT_COUNT_DIR"

count_prd_todo_remaining() {
    local project_dir="$1"
    local prd_todo="${project_dir}/prd-todo.md"
    local remaining=0

    if [ -f "$prd_todo" ]; then
        remaining=$(grep '^- ' "$prd_todo" | grep -vic "$PRD_DONE_FILTER_RE" || true)
        remaining=$(normalize_int "$remaining")
    fi

    echo "$remaining"
}

# 检测 prd-todo.md 是否有新增待办（对比上次快照）
detect_prd_todo_changes() {
    local safe="$1" project_dir="$2"
    local prd_todo="${project_dir}/prd-todo.md"
    local snapshot_file="${STATE_DIR}/prd-snapshot-${safe}.md5"
    
    [ -f "$prd_todo" ] || return 1
    
    local current_hash
    if command -v md5 >/dev/null 2>&1; then
        current_hash=$(md5 -q "$prd_todo" 2>/dev/null)
    elif command -v md5sum >/dev/null 2>&1; then
        current_hash=$(md5sum "$prd_todo" | awk '{print $1}')
    else
        return 1
    fi
    
    local prev_hash
    prev_hash=$(cat "$snapshot_file" 2>/dev/null || echo "")
    
    # 保存当前快照
    echo "$current_hash" > "$snapshot_file"
    
    # 首次运行不算变化
    [ -z "$prev_hash" ] && return 1
    
    # hash 不同 = 有变化
    [ "$current_hash" != "$prev_hash" ]
}

is_prd_todo_complete() {
    local project_dir="$1"
    [ -f "${project_dir}/prd-todo.md" ] || return 1
    [ "$(count_prd_todo_remaining "$project_dir")" -eq 0 ]
}

# ---- 项目配置 ----
# 项目配置来源（优先级）:
# 1) config.yaml 中 projects 段（统一配置源）
# 2) watchdog-projects.conf（兼容 fallback）
CONFIG_YAML_FILE="$HOME/.autopilot/config.yaml"
PROJECT_CONFIG_FILE="$HOME/.autopilot/watchdog-projects.conf"
DEFAULT_PROJECTS=(
    "Shike:/Users/wes/Shike"
    "agent-simcity:/Users/wes/projects/agent-simcity"
    "replyher_android-2:/Users/wes/replyher_android-2"
)
PROJECTS=()
BRANCH_MANAGER="${SCRIPT_DIR}/branch-manager.sh"
BRANCH_ISOLATION_ENABLED="true"
BRANCH_AUTO_MERGE_ENABLED="true"
BRANCH_REQUIRE_AUTO_CHECK="true"
BRANCH_REQUIRE_TESTS="false"
BRANCH_BASE_BRANCH="main"
TEST_AGENT_SCRIPT="${SCRIPT_DIR}/test-agent.sh"
TEST_AGENT_ENABLED="false"
TEST_AGENT_TRIGGER_REVIEW_CLEAN="true"
TEST_AGENT_TRIGGER_ON_COMMIT_EVALUATE="true"

# Gemini 前端路由（过渡方案，ACP 稳定后切换）
# 格式: "项目名:tmux窗口名" — 指定该项目的 frontend 任务发到哪个 Gemini 窗口
# 如果项目没有对应的 Gemini 窗口，frontend 任务仍走 Codex
GEMINI_WINDOWS=()
GEMINI_DEFAULT_WINDOW=""  # 没有项目特定映射时的默认 Gemini 窗口

load_gemini_config() {
    local yaml_file="$1"
    [ -f "$yaml_file" ] || return 0

    GEMINI_DEFAULT_WINDOW=$(grep -A5 '^gemini:' "$yaml_file" 2>/dev/null | grep 'default_window:' | sed 's/#.*//' | sed 's/.*default_window: *"\{0,1\}\([^"]*\)"\{0,1\}/\1/' | tr -d ' ' || true)

    # 读取 approval_mode（yolo/auto_edit/default）
    local mode
    mode=$(grep -A5 '^gemini:' "$yaml_file" 2>/dev/null | grep 'approval_mode:' | sed 's/.*approval_mode: *"\{0,1\}\([^"]*\)"\{0,1\}/\1/' | tr -d ' ' || true)
    [ -n "$mode" ] && GEMINI_APPROVAL_MODE="$mode"

    local mapping_lines
    mapping_lines=$(awk '
        /^gemini:/ { in_gemini = 1; next }
        in_gemini && /^[^ ]/ { in_gemini = 0 }
        in_gemini && /project_windows:/ { in_pw = 1; next }
        in_pw && /^[^ ]/ { in_pw = 0 }
        in_pw && /^    [a-zA-Z]/ { print }
    ' "$yaml_file" 2>/dev/null || true)
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        local proj win
        proj=$(echo "$line" | sed 's/#.*//' | cut -d: -f1 | tr -d ' ')
        win=$(echo "$line" | sed 's/#.*//' | cut -d: -f2- | tr -d ' "')
        [ -n "$proj" ] && [ -n "$win" ] && GEMINI_WINDOWS+=("${proj}:${win}")
    done <<< "$mapping_lines"
}

get_gemini_window() {
    local project="$1"
    local safe
    safe=$(echo "$project" | tr -cd 'a-zA-Z0-9_-' | tr '[:upper:]' '[:lower:]')

    for entry in "${GEMINI_WINDOWS[@]}"; do
        local p="${entry%%:*}"
        local w="${entry#*:}"
        if [ "$p" = "$safe" ] || [ "$p" = "$project" ]; then
            echo "$w"
            return 0
        fi
    done

    # fallback to default
    if [ -n "$GEMINI_DEFAULT_WINDOW" ]; then
        echo "$GEMINI_DEFAULT_WINDOW"
        return 0
    fi

    return 1
}

is_frontend_task() {
    local task_type="$1"
    task_type=$(printf '%s\n' "$task_type" | tr '[:upper:]' '[:lower:]')
    case "$task_type" in
        frontend|ui|h5) return 0 ;;
        *) return 1 ;;
    esac
}

GEMINI="${GEMINI_BIN:-$(command -v gemini || echo /opt/homebrew/bin/gemini)}"

# Gemini approval mode: yolo (auto-approve all), auto_edit, default
GEMINI_APPROVAL_MODE="${GEMINI_APPROVAL_MODE:-yolo}"

ensure_gemini_session() {
    local gemini_window="$1"
    local session_name="${gemini_window%%:*}"
    local window_name="${gemini_window#*:}"
    local project_dir="$2"  # optional workdir

    # 检查窗口是否已存在且 Gemini 正在运行
    if tmux has-session -t "$session_name" 2>/dev/null; then
        local pane_content
        pane_content=$(tmux capture-pane -t "$gemini_window" -p 2>/dev/null | tail -5)
        if echo "$pane_content" | grep -q "Type your message\|esc to cancel"; then
            return 0  # Gemini 已在运行
        fi
        # 窗口存在但 Gemini 没运行 — 检查是否有 shell prompt
        if echo "$pane_content" | grep -q '^\$\|^%\|^❯'; then
            log "🔄 Gemini not running in ${gemini_window}, starting with --${GEMINI_APPROVAL_MODE}..."
            local cd_cmd=""
            [ -n "$project_dir" ] && cd_cmd="cd ${project_dir} && "
            tmux send-keys -t "$gemini_window" "${cd_cmd}${GEMINI} --approval-mode ${GEMINI_APPROVAL_MODE}" Enter
            sleep 8  # Gemini 启动需要几秒
            return 0
        fi
    fi

    # 窗口不存在 — 创建
    if ! tmux has-session -t "$session_name" 2>/dev/null; then
        log "⚠️ tmux session ${session_name} not found"
        return 1
    fi

    local start_dir="${project_dir:-.}"
    tmux new-window -t "$session_name" -n "$window_name" -c "$start_dir" 2>/dev/null
    sleep 1
    tmux send-keys -t "$gemini_window" "${GEMINI} --approval-mode ${GEMINI_APPROVAL_MODE}" Enter
    sleep 8  # 等待 Gemini 启动
    log "🚀 Gemini started in ${gemini_window} (--${GEMINI_APPROVAL_MODE})"
    return 0
}

send_gemini_message() {
    local gemini_window="$1" message="$2"
    local output rc

    # 自动确保 Gemini 窗口存在且运行
    if ! ensure_gemini_session "$gemini_window"; then
        log "⚠️ Gemini window ${gemini_window} not found, falling back to Codex"
        return 1
    fi

    # 发送到 Gemini（和 Codex 一样用 tmux send-keys）
    tmux send-keys -t "$gemini_window" -l "$message" 2>/dev/null
    sleep 2
    tmux send-keys -t "$gemini_window" Enter 2>/dev/null
    rc=$?

    if [ "$rc" -ne 0 ]; then
        log "❌ Gemini send to ${gemini_window} failed (rc=${rc})"
        return "$rc"
    fi

    log "🎨 Gemini: sent frontend task to ${gemini_window}"
    return 0
}

# ---- 工具函数 ----
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

hash_text() {
    local content="$1"
    if command -v md5 >/dev/null 2>&1; then
        printf '%s' "$content" | md5 -q
        return 0
    fi
    if command -v md5sum >/dev/null 2>&1; then
        printf '%s' "$content" | md5sum | awk '{print $1}'
        return 0
    fi
    if command -v shasum >/dev/null 2>&1; then
        printf '%s' "$content" | shasum -a 256 | awk '{print $1}'
        return 0
    fi
    echo "nohash-$(now_ts)"
}

assert_runtime_ready() {
    if [ ! -x "$TMUX" ]; then
        echo "watchdog fatal: tmux not executable at $TMUX" >&2
        exit 1
    fi
    if [ ! -x "${SCRIPT_DIR}/codex-status.sh" ]; then
        echo "watchdog fatal: missing ${SCRIPT_DIR}/codex-status.sh" >&2
        exit 1
    fi
    if [ ! -x "${SCRIPT_DIR}/tmux-send.sh" ]; then
        echo "watchdog fatal: missing ${SCRIPT_DIR}/tmux-send.sh" >&2
        exit 1
    fi
    if [ ! -x "$CODEX" ]; then
        log "⚠️ watchdog: codex binary not found at $CODEX, shell recovery may fail"
    fi
}

load_projects() {
    local loaded_projects="" entry
    PROJECTS=()

    loaded_projects=$(autopilot_load_projects_entries "$CONFIG_YAML_FILE" "$PROJECT_CONFIG_FILE" "${DEFAULT_PROJECTS[@]}" 2>/dev/null || true)
    while IFS= read -r entry || [ -n "$entry" ]; do
        [ -n "$entry" ] || continue
        PROJECTS+=("$entry")
    done <<< "$loaded_projects"

    if [ "${#PROJECTS[@]}" -eq 0 ]; then
        PROJECTS=("${DEFAULT_PROJECTS[@]}")
        log "⚠️ project config missing/empty, fallback to defaults (${#PROJECTS[@]} projects)"
    else
        # AUTOPILOT_PROJECT_SOURCE is set in subshell and lost; infer source
        log "📁 loaded ${#PROJECTS[@]} projects from config"
    fi

    # 加载 Gemini 前端路由配置
    load_gemini_config "$CONFIG_YAML_FILE"
    if [ -n "$GEMINI_DEFAULT_WINDOW" ] || [ "${#GEMINI_WINDOWS[@]}" -gt 0 ]; then
        log "🎨 Gemini routing: default=${GEMINI_DEFAULT_WINDOW:-none}, project mappings=${#GEMINI_WINDOWS[@]}"
    fi
}

load_branch_isolation_config() {
    local config_file="$CONFIG_YAML_FILE"
    [ -f "$config_file" ] || return 0

    local enabled_val auto_merge_enabled_val require_auto_check_val require_tests_val base_branch_val
    enabled_val=$(awk '
        /^[[:space:]]*branch_isolation:[[:space:]]*$/ {in_branch=1; next}
        in_branch && /^[^[:space:]]/ {in_branch=0}
        in_branch && /^[[:space:]]*enabled:[[:space:]]*/ {
            sub(/^[[:space:]]*enabled:[[:space:]]*/, "", $0); print; exit
        }
    ' "$config_file" 2>/dev/null || true)
    base_branch_val=$(awk '
        /^[[:space:]]*branch_isolation:[[:space:]]*$/ {in_branch=1; next}
        in_branch && /^[^[:space:]]/ {in_branch=0}
        in_branch && /^[[:space:]]*base_branch:[[:space:]]*/ {
            sub(/^[[:space:]]*base_branch:[[:space:]]*/, "", $0); print; exit
        }
    ' "$config_file" 2>/dev/null || true)
    auto_merge_enabled_val=$(awk '
        /^[[:space:]]*branch_isolation:[[:space:]]*$/ {in_branch=1; next}
        in_branch && /^[^[:space:]]/ {in_branch=0}
        in_branch && /^[[:space:]]*auto_merge:[[:space:]]*$/ {in_auto=1; next}
        in_auto && /^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*:[[:space:]]*$/ && $0 !~ /^[[:space:]]*enabled:[[:space:]]*/ {next}
        in_auto && /^[[:space:]]*enabled:[[:space:]]*/ {
            sub(/^[[:space:]]*enabled:[[:space:]]*/, "", $0); print; exit
        }
    ' "$config_file" 2>/dev/null || true)
    require_auto_check_val=$(awk '
        /^[[:space:]]*branch_isolation:[[:space:]]*$/ {in_branch=1; next}
        in_branch && /^[^[:space:]]/ {in_branch=0}
        in_branch && /^[[:space:]]*auto_merge:[[:space:]]*$/ {in_auto=1; next}
        in_auto && /^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*:[[:space:]]*$/ && $0 !~ /^[[:space:]]*require_auto_check:[[:space:]]*/ {next}
        in_auto && /^[[:space:]]*require_auto_check:[[:space:]]*/ {
            sub(/^[[:space:]]*require_auto_check:[[:space:]]*/, "", $0); print; exit
        }
    ' "$config_file" 2>/dev/null || true)
    require_tests_val=$(awk '
        /^[[:space:]]*branch_isolation:[[:space:]]*$/ {in_branch=1; next}
        in_branch && /^[^[:space:]]/ {in_branch=0}
        in_branch && /^[[:space:]]*auto_merge:[[:space:]]*$/ {in_auto=1; next}
        in_auto && /^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*:[[:space:]]*$/ && $0 !~ /^[[:space:]]*require_tests:[[:space:]]*/ {next}
        in_auto && /^[[:space:]]*require_tests:[[:space:]]*/ {
            sub(/^[[:space:]]*require_tests:[[:space:]]*/, "", $0); print; exit
        }
    ' "$config_file" 2>/dev/null || true)

    enabled_val=$(echo "${enabled_val:-}" | tr '[:upper:]' '[:lower:]' | tr -d ' "'\''')
    auto_merge_enabled_val=$(echo "${auto_merge_enabled_val:-}" | tr '[:upper:]' '[:lower:]' | tr -d ' "'\''')
    require_auto_check_val=$(echo "${require_auto_check_val:-}" | tr '[:upper:]' '[:lower:]' | tr -d ' "'\''')
    require_tests_val=$(echo "${require_tests_val:-}" | tr '[:upper:]' '[:lower:]' | tr -d ' "'\''')
    base_branch_val=$(echo "${base_branch_val:-}" | sed 's/[[:space:]]*#.*$//' | tr -d ' "'\''')

    case "$enabled_val" in true|1|yes|on) BRANCH_ISOLATION_ENABLED="true" ;; false|0|no|off) BRANCH_ISOLATION_ENABLED="false" ;; esac
    case "$auto_merge_enabled_val" in true|1|yes|on) BRANCH_AUTO_MERGE_ENABLED="true" ;; false|0|no|off) BRANCH_AUTO_MERGE_ENABLED="false" ;; esac
    case "$require_auto_check_val" in true|1|yes|on) BRANCH_REQUIRE_AUTO_CHECK="true" ;; false|0|no|off) BRANCH_REQUIRE_AUTO_CHECK="false" ;; esac
    case "$require_tests_val" in true|1|yes|on) BRANCH_REQUIRE_TESTS="true" ;; false|0|no|off) BRANCH_REQUIRE_TESTS="false" ;; esac
    [ -n "$base_branch_val" ] && BRANCH_BASE_BRANCH="$base_branch_val"
}

load_test_agent_config() {
    local config_file="$CONFIG_YAML_FILE"
    [ -f "$config_file" ] || return 0

    local enabled_val on_review_clean_val on_commit_val
    enabled_val=$(awk '
        /^[[:space:]]*test_agent:[[:space:]]*$/ {in_test=1; next}
        in_test && /^[^[:space:]]/ {in_test=0}
        in_test && /^[[:space:]]*enabled:[[:space:]]*/ {
            sub(/^[[:space:]]*enabled:[[:space:]]*/, "", $0); print; exit
        }
    ' "$config_file" 2>/dev/null || true)
    on_review_clean_val=$(awk '
        /^[[:space:]]*test_agent:[[:space:]]*$/ {in_test=1; next}
        in_test && /^[^[:space:]]/ {in_test=0}
        in_test && /^[[:space:]]*trigger:[[:space:]]*$/ {in_trigger=1; next}
        in_trigger && in_test && /^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*:[[:space:]]*$/ && $0 !~ /^[[:space:]]*on_review_clean:[[:space:]]*/ {next}
        in_trigger && /^[[:space:]]*on_review_clean:[[:space:]]*/ {
            sub(/^[[:space:]]*on_review_clean:[[:space:]]*/, "", $0); print; exit
        }
    ' "$config_file" 2>/dev/null || true)
    on_commit_val=$(awk '
        /^[[:space:]]*test_agent:[[:space:]]*$/ {in_test=1; next}
        in_test && /^[^[:space:]]/ {in_test=0}
        in_test && /^[[:space:]]*trigger:[[:space:]]*$/ {in_trigger=1; next}
        in_trigger && in_test && /^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*:[[:space:]]*$/ && $0 !~ /^[[:space:]]*on_commit_evaluate:[[:space:]]*/ {next}
        in_trigger && /^[[:space:]]*on_commit_evaluate:[[:space:]]*/ {
            sub(/^[[:space:]]*on_commit_evaluate:[[:space:]]*/, "", $0); print; exit
        }
    ' "$config_file" 2>/dev/null || true)

    enabled_val=$(echo "${enabled_val:-}" | tr '[:upper:]' '[:lower:]' | tr -d ' "'\''')
    on_review_clean_val=$(echo "${on_review_clean_val:-}" | tr '[:upper:]' '[:lower:]' | tr -d ' "'\''')
    on_commit_val=$(echo "${on_commit_val:-}" | tr '[:upper:]' '[:lower:]' | tr -d ' "'\''')

    case "$enabled_val" in
        true|1|yes|on) TEST_AGENT_ENABLED="true" ;;
        false|0|no|off) TEST_AGENT_ENABLED="false" ;;
    esac
    case "$on_review_clean_val" in
        true|1|yes|on) TEST_AGENT_TRIGGER_REVIEW_CLEAN="true" ;;
        false|0|no|off) TEST_AGENT_TRIGGER_REVIEW_CLEAN="false" ;;
    esac
    case "$on_commit_val" in
        true|1|yes|on) TEST_AGENT_TRIGGER_ON_COMMIT_EVALUATE="true" ;;
        false|0|no|off) TEST_AGENT_TRIGGER_ON_COMMIT_EVALUATE="false" ;;
    esac
}

send_tmux_message() {
    local window="$1" message="$2" action="$3"
    local task_type="${4:-}"
    local branch_mode="${5:-off}"
    local output rc
    local safe_w
    safe_w=$(echo "$window" | tr -cd 'a-zA-Z0-9_-')

    # watchdog 自动发送不应写 tracked-task，避免与人工任务追踪混淆。
    if [ -n "$task_type" ]; then
        output=$("$SCRIPT_DIR/tmux-send.sh" --no-track --branch-mode "$branch_mode" --task-type "$task_type" "$window" "$message" 2>&1)
    else
        output=$("$SCRIPT_DIR/tmux-send.sh" --no-track --branch-mode off "$window" "$message" 2>&1)
    fi
    rc=$?
    # 清除 tmux-send 写的 manual-task 标记（这是 watchdog 自己发的，不是人工的）
    rm -f "${STATE_DIR}/manual-task-${safe_w}" 2>/dev/null
    if [ "$rc" -ne 0 ]; then
        output=$(echo "$output" | tr '\n' ' ' | tr -s ' ' | sed 's/^ *//; s/ *$//')
        log "❌ ${window}: ${action} send failed (rc=${rc}) — ${output:0:160}"
        return "$rc"
    fi

    # 保存最后成功发送的 nudge 内容（供 pre-compact 快照使用）
    echo "$message" > "${STATE_DIR}/last-nudge-msg-${safe_w}" 2>/dev/null || true

    return 0
}

extract_status_field() {
    local status_json="$1" field="$2" value
    value=$(echo "$status_json" | jq -r ".${field} // \"\"" 2>/dev/null || true)
    echo "$value"
}

extract_context_num_field() {
    local status_json="$1" ctx
    ctx=$(echo "$status_json" | jq -r '.context_num // -1' 2>/dev/null || echo "-1")
    if [[ "$ctx" =~ ^-?[0-9]+$ ]]; then
        echo "$ctx"
    else
        echo "-1"
    fi
}

get_window_status_json() {
    local window="$1" result
    # codex-status.sh exit codes: 0=working, 1=idle/permission, 2=shell, 3=absent
    # All are valid outputs; only capture stderr failures
    result=$("$SCRIPT_DIR/codex-status.sh" "$window" 2>/dev/null) || true
    if [ -z "$result" ] || ! echo "$result" | jq -e '.status' >/dev/null 2>&1; then
        echo "{\"status\":\"${CODEX_STATE_ABSENT}\",\"context_num\":-1}"
    else
        echo "$result"
    fi
}

extract_json_number() {
    local status_json="$1" field="$2" value
    value=$(echo "$status_json" | jq -r ".${field} // -1" 2>/dev/null || echo "-1")
    if ! [[ "$value" =~ ^-?[0-9]+$ ]]; then
        value=-1
    fi
    echo "$value"
}

sanitize_branch_for_key() {
    local branch="${1:-}"
    echo "$branch" | sed 's#[^a-zA-Z0-9_.-]#_#g'
}

extract_queue_meta_from_line() {
    local line="${1:-}" key="${2:-}"
    [ -n "$line" ] || return 1
    [ -n "$key" ] || return 1
    printf '%s\n' "$line" \
        | sed -n "s/^.* | ${key}: \\([^|]*\\).*$/\\1/p" \
        | sed 's/[[:space:]]*$//' \
        | head -n1
}

# 根据任务类型拼接队列任务前缀；兼容旧数据（空/type=task 均按 general 处理）。
build_task_prompt_by_type() {
    local task_type_raw="${1:-}"
    local task_desc="${2:-}"
    local task_type
    task_type=$(printf '%s\n' "$task_type_raw" | tr '[:upper:]' '[:lower:]')

    case "$task_type" in
        ""|general|task)
            printf '%s' "$task_desc"
            ;;
        bugfix|bug|fix)
            printf '任务类型: bugfix\n要求: 先复现并定位根因，再做最小修复；补充回归测试并自测通过。\n任务: %s' "$task_desc"
            ;;
        feature|feat)
            printf '任务类型: feature\n要求: 先给出最小可行实现方案（接口/数据/边界），再分步实现并补充测试。\n任务: %s' "$task_desc"
            ;;
        refactor)
            printf '任务类型: refactor\n要求: 不改变外部行为；重构后必须通过现有测试，并补充必要回归测试。\n任务: %s' "$task_desc"
            ;;
        review|review_fix)
            printf '任务类型: review\n要求: 优先修复高优先级问题（P1/P2），修改后说明验证方式并提交。\n任务: %s' "$task_desc"
            ;;
        frontend|ui|h5)
            printf '任务类型: frontend\n要求: 实现前端页面/组件/样式，确保响应式和交互状态覆盖（loading/empty/error/success），自查 Anti-AI-Slop 清单，design system 一致性。完成后自查：布局是否模板化？有没有通用渐变/3列grid？空状态有温度吗？间距有节奏感吗？\n任务: %s' "$task_desc"
            ;;
        *)
            printf '任务类型: %s\n任务: %s' "$task_type" "$task_desc"
            ;;
    esac
}

send_telegram_alert() {
    local window="$1" text="$2"
    send_telegram "🚨 ${window}: ${text}"
}

send_discord_to_target() {
    local target="$1" text="$2" context="$3"
    [ -n "$target" ] || return 1
    [ -n "$text" ] || return 0
    [ -x "${SCRIPT_DIR}/discord-notify.sh" ] || return 1

    (
        "${SCRIPT_DIR}/discord-notify.sh" "$target" "$text" >/dev/null 2>&1 \
            || log "⚠️ ${context}: discord notify failed (target=${target})"
    ) &
    return 0
}

send_discord_by_window() {
    local window="$1" text="$2"
    [ -n "$text" ] || return 0
    [ -x "${SCRIPT_DIR}/discord-notify.sh" ] || return 0

    local discord_channel
    discord_channel=$(get_discord_channel_for_window "$window" 2>/dev/null || true)
    [ -n "$discord_channel" ] || return 0

    send_discord_to_target "$discord_channel" "$text" "$window" || return 0
}

parse_iso_minute_to_ts() {
    local datetime="${1:-}"
    local ts=0
    [ -n "$datetime" ] || { echo 0; return 1; }

    if ts=$(date -j -f '%Y-%m-%d %H:%M' "$datetime" +%s 2>/dev/null); then
        echo "$ts"
        return 0
    fi
    if ts=$(date -d "$datetime" +%s 2>/dev/null); then
        echo "$ts"
        return 0
    fi

    echo 0
    return 1
}

recover_stale_queue_in_progress() {
    local window="$1" safe="$2"
    local queue_file="${HOME}/.autopilot/task-queue/${safe}.md"
    [ -f "$queue_file" ] || return 0

    local in_progress_line started_at started_ts now_val age
    in_progress_line=$(grep -m1 '^\- \[→\]' "$queue_file" 2>/dev/null || true)
    [ -n "$in_progress_line" ] || return 0

    started_at=$(printf '%s\n' "$in_progress_line" \
        | sed -n 's/^.* | started: \([0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\}\).*/\1/p' \
        | head -n1)
    [ -n "$started_at" ] || return 0

    started_ts=$(parse_iso_minute_to_ts "$started_at" 2>/dev/null || echo 0)
    started_ts=$(normalize_int "$started_ts")
    [ "$started_ts" -gt 0 ] || return 0

    now_val=$(now_ts)
    age=$((now_val - started_ts))
    if [ "$age" -lt "$QUEUE_IN_PROGRESS_TIMEOUT_SECONDS" ]; then
        return 0
    fi

    if "${SCRIPT_DIR}/task-queue.sh" fail "$safe" "in-progress-timeout-${age}s" >/dev/null 2>&1; then
        log "♻️ ${window}: queue in-progress stale (${age}s), auto requeued"
        send_telegram "♻️ ${window}: 队列任务超时 ${age}s，已自动重新入队。"
    fi
}

format_duration_short() {
    local seconds
    seconds=$(normalize_int "${1:-0}")

    if [ "$seconds" -ge 3600 ]; then
        local hours minutes
        hours=$((seconds / 3600))
        minutes=$(((seconds % 3600) / 60))
        if [ "$minutes" -gt 0 ]; then
            echo "${hours}h${minutes}m"
        else
            echo "${hours}h"
        fi
        return 0
    fi

    if [ "$seconds" -ge 60 ]; then
        echo "$((seconds / 60))m"
        return 0
    fi

    echo "${seconds}s"
}

is_idle_state_for_tracked_completion() {
    local state="${1:-}"
    [ "$state" = "$CODEX_STATE_IDLE" ] || [ "$state" = "$CODEX_STATE_IDLE_LOW_CONTEXT" ]
}

mark_tracked_task_timeout_notified() {
    local tracked_file="$1" now_val="$2"
    local tmp_file="${tracked_file}.tmp"

    if ! command -v jq >/dev/null 2>&1; then
        return 1
    fi

    jq --argjson now "$now_val" \
        '.stall_notified = true | .stall_notified_at = $now' \
        "$tracked_file" > "$tmp_file" 2>/dev/null \
        && mv -f "$tmp_file" "$tracked_file" \
        || rm -f "$tmp_file" 2>/dev/null || true
}

check_tracked_manual_task() {
    local window="$1" safe="$2" project_dir="$3" state="$4"
    local tracked_file="${STATE_DIR}/tracked-task-${safe}.json"
    [ -f "$tracked_file" ] || return 0

    if ! command -v jq >/dev/null 2>&1; then
        return 0
    fi
    if ! jq -e '.status' "$tracked_file" >/dev/null 2>&1; then
        log "⚠️ ${window}: tracked-task json 无法解析，已清理"
        rm -f "$tracked_file" 2>/dev/null || true
        return 0
    fi

    local status task source source_channel head_before started_at stall_notified
    status=$(jq -r '.status // ""' "$tracked_file" 2>/dev/null || echo "")
    [ "$status" = "in-progress" ] || return 0

    task=$(jq -r '.task // ""' "$tracked_file" 2>/dev/null || echo "")
    source=$(jq -r '.source // ""' "$tracked_file" 2>/dev/null || echo "")
    source_channel=$(jq -r '.source_channel // ""' "$tracked_file" 2>/dev/null || echo "")
    head_before=$(jq -r '.head_before // "none"' "$tracked_file" 2>/dev/null || echo "none")
    started_at=$(jq -r '.started_at // 0' "$tracked_file" 2>/dev/null || echo 0)
    stall_notified=$(jq -r '.stall_notified // false' "$tracked_file" 2>/dev/null || echo "false")

    started_at=$(normalize_int "$started_at")
    if [ "$started_at" -le 0 ]; then
        started_at=$(file_mtime "$tracked_file")
        started_at=$(normalize_int "$started_at")
    fi

    local now_val age
    now_val=$(now_ts)
    age=$((now_val - started_at))
    [ "$age" -ge 0 ] || age=0

    local current_head="none"
    current_head=$(run_with_timeout 10 git -C "$project_dir" rev-parse HEAD 2>/dev/null || echo "none")

    if [[ "$head_before" =~ ^[0-9a-f]{7,40}$ ]] \
        && [[ "$current_head" =~ ^[0-9a-f]{7,40}$ ]] \
        && [ "$current_head" != "$head_before" ] \
        && is_idle_state_for_tracked_completion "$state"; then
        local commit_msg elapsed_text done_msg
        commit_msg=$(run_with_timeout 10 git -C "$project_dir" log -1 --format="%s" "$current_head" 2>/dev/null || echo "")
        elapsed_text=$(format_duration_short "$age")
        done_msg=$(
            printf '✅ %s: 手动任务完成\n任务: %s\nCommit: %s — %s\n耗时: %s' \
                "$window" "${task:0:180}" "${current_head:0:7}" "${commit_msg:0:120}" "$elapsed_text"
        )

        if [ -n "$source_channel" ]; then
            send_discord_to_target "$source_channel" "$done_msg" "$window" || send_discord_by_window "$window" "$done_msg"
        else
            send_discord_by_window "$window" "$done_msg"
        fi

        log "✅ ${window}: tracked task completed (${current_head:0:7}, source=${source:-unknown})"
        rm -f "$tracked_file" "${STATE_DIR}/manual-task-${safe}" 2>/dev/null || true
        return 0
    fi

    if [ "$age" -ge "$TRACKED_TASK_TIMEOUT_SECONDS" ] && [ "$stall_notified" != "true" ] && [ "$stall_notified" != "1" ]; then
        local elapsed_text warn_msg
        elapsed_text=$(format_duration_short "$age")
        warn_msg=$(
            printf '⚠️ %s: 手动任务可能卡住\n任务: %s\n已运行: %s，尚未检测到新的 commit。' \
                "$window" "${task:0:180}" "$elapsed_text"
        )
        if [ -n "$source_channel" ]; then
            send_discord_to_target "$source_channel" "$warn_msg" "$window" || send_discord_by_window "$window" "$warn_msg"
        else
            send_discord_by_window "$window" "$warn_msg"
        fi
        mark_tracked_task_timeout_notified "$tracked_file" "$now_val"
        log "⚠️ ${window}: tracked task timeout (${elapsed_text}, source=${source:-unknown})"
    fi
}

maybe_trigger_test_agent_on_review_clean() {
    local window="$1" safe="$2" project_dir="$3" state="$4"
    [ "$TEST_AGENT_ENABLED" = "true" ] || return 0
    [ "$TEST_AGENT_TRIGGER_REVIEW_CLEAN" = "true" ] || return 0
    [ -x "$TEST_AGENT_SCRIPT" ] || return 0
    [ "$state" = "$CODEX_STATE_IDLE" ] || [ "$state" = "$CODEX_STATE_IDLE_LOW_CONTEXT" ] || return 0

    local review_file review_mtime stamp_file last_mtime
    review_file="${STATE_DIR}/layer2-review-${safe}.txt"
    [ -f "$review_file" ] || return 0
    # 严格匹配 CLEAN（避免 cleanup/not clean 误命中）
    grep -qiE '^\s*CLEAN\s*$|结论.*CLEAN|status.*CLEAN' "$review_file" 2>/dev/null || return 0

    review_mtime=$(file_mtime "$review_file")
    review_mtime=$(normalize_int "$review_mtime")
    [ "$review_mtime" -gt 0 ] || return 0

    stamp_file="${STATE_DIR}/test-agent-review-clean-${safe}.mtime"
    last_mtime=$(cat "$stamp_file" 2>/dev/null || echo 0)
    last_mtime=$(normalize_int "$last_mtime")
    [ "$review_mtime" -gt "$last_mtime" ] || return 0

    local trigger_lock="${LOCK_DIR}/test-agent-trigger-${safe}.lock.d"
    if [ -d "$trigger_lock" ]; then
        local lock_age
        lock_age=$(( $(now_ts) - $(file_mtime "$trigger_lock") ))
        if [ "$lock_age" -gt 900 ]; then
            rm -rf "$trigger_lock" 2>/dev/null || true
        fi
    fi
    mkdir "$trigger_lock" 2>/dev/null || return 0

    (
        trap 'rm -rf "'"$trigger_lock"'"' EXIT
        local out_file out_json
        out_file="${HOME}/.autopilot/logs/test-agent-${safe}.log"
        out_json=$("$TEST_AGENT_SCRIPT" enqueue "$project_dir" "$window" "review_clean" 2>>"$out_file" || true)

        if [ -n "$out_json" ] && echo "$out_json" | jq -e . >/dev/null 2>&1; then
            local enqueued
            enqueued=$(echo "$out_json" | jq -r '.enqueued // 0' 2>/dev/null || echo 0)
            enqueued=$(normalize_int "$enqueued")
            echo "$review_mtime" > "${stamp_file}.tmp" && mv -f "${stamp_file}.tmp" "$stamp_file"
            log "🧪 ${window}: test-agent enqueue triggered after review CLEAN (enqueued=${enqueued})"
        else
            log "⚠️ ${window}: test-agent enqueue failed after review CLEAN"
        fi
    ) &
}

maybe_trigger_test_agent_on_commit() {
    local window="$1" safe="$2" project_dir="$3" current_head="$4"
    [ "$TEST_AGENT_ENABLED" = "true" ] || return 0
    [ "$TEST_AGENT_TRIGGER_ON_COMMIT_EVALUATE" = "true" ] || return 0
    [ -x "$TEST_AGENT_SCRIPT" ] || return 0
    [ -n "$current_head" ] || return 0

    local stamp_file last_head trigger_lock
    stamp_file="${STATE_DIR}/test-agent-commit-${safe}.head"
    last_head=$(cat "$stamp_file" 2>/dev/null || echo "")
    [ "$current_head" != "$last_head" ] || return 0

    trigger_lock="${LOCK_DIR}/test-agent-commit-${safe}.lock.d"
    if [ -d "$trigger_lock" ]; then
        local lock_age
        lock_age=$(( $(now_ts) - $(file_mtime "$trigger_lock") ))
        if [ "$lock_age" -gt 900 ]; then
            rm -rf "$trigger_lock" 2>/dev/null || true
        fi
    fi
    mkdir "$trigger_lock" 2>/dev/null || return 0

    (
        trap 'rm -rf "'"$trigger_lock"'"' EXIT
        local out_file out_json
        out_file="${HOME}/.autopilot/logs/test-agent-${safe}.log"
        out_json=$("$TEST_AGENT_SCRIPT" evaluate "$project_dir" "$window" 2>>"$out_file" || true)

        if [ -n "$out_json" ] && echo "$out_json" | jq -e . >/dev/null 2>&1; then
            echo "$current_head" > "${stamp_file}.tmp" && mv -f "${stamp_file}.tmp" "$stamp_file"
            log "🧪 ${window}: test-agent evaluate triggered after commit (${current_head:0:7})"
        else
            log "⚠️ ${window}: test-agent evaluate failed after commit (${current_head:0:7})"
        fi
    ) &
}

start_nudge_ack_check() {
    local window="$1" safe="$2" project_dir="$3" before_head="$4" before_ctx="$5" reason="$6"
    local ack_lock="${LOCK_DIR}/ack-${safe}.lock.d"
    local active_ack_jobs

    active_ack_jobs=$(find "$LOCK_DIR" -maxdepth 1 -type d -name 'ack-*.lock.d' 2>/dev/null | wc -l | tr -d ' ')
    active_ack_jobs=$(normalize_int "$active_ack_jobs")
    if [ "$active_ack_jobs" -ge "$ACK_CHECK_MAX_JOBS" ]; then
        log "⏭ ${window}: skip ack check (active=${active_ack_jobs}, cap=${ACK_CHECK_MAX_JOBS})"
        return 0
    fi

    if [ -d "$ack_lock" ]; then
        local lock_age
        lock_age=$(( $(now_ts) - $(file_mtime "$ack_lock") ))
        if [ "$lock_age" -gt "$ACK_CHECK_LOCK_STALE_SECONDS" ]; then
            rm -rf "$ack_lock" 2>/dev/null || true
        fi
    fi

    mkdir "$ack_lock" 2>/dev/null || return 0
    echo "$$" > "${ack_lock}/parent_pid"
    (
        trap 'rm -rf "'"$ack_lock"'"' EXIT
        echo "$$" > "${ack_lock}/pid"
        local elapsed=0
        while [ "$elapsed" -lt 60 ]; do
            local cur_head cur_json cur_state cur_ctx
            cur_head=$(run_with_timeout 10 git -C "$project_dir" rev-parse HEAD 2>/dev/null || echo "none")
            if [ "$cur_head" != "none" ] && [ "$cur_head" != "$before_head" ]; then
                log "✅ ${window}: ${reason} ack by new commit (${before_head:0:7}→${cur_head:0:7})"
                return 0
            fi

            cur_json=$(get_window_status_json "$window")
            cur_state=$(extract_status_field "$cur_json" "status")
            cur_ctx=$(extract_context_num_field "$cur_json")

            if [ "$cur_state" = "$CODEX_STATE_WORKING" ]; then
                log "✅ ${window}: ${reason} ack by working state"
                return 0
            fi

            if [ "$before_ctx" -ge 0 ] && [ "$cur_ctx" -ge 0 ] && [ "$cur_ctx" != "$before_ctx" ]; then
                log "✅ ${window}: ${reason} ack by context change (${before_ctx}%→${cur_ctx}%)"
                return 0
            fi

            sleep 10
            elapsed=$((elapsed + 10))
        done

        log "⚠️ ${window}: ${reason} no-ack in 60s (head/context unchanged)"
    ) &
}

sync_project_status() {
    local project_dir="$1" event="$2"
    shift 2 || true
    if [ -x "$SCRIPT_DIR/status-sync.sh" ]; then
        "$SCRIPT_DIR/status-sync.sh" "$project_dir" "$event" "$@" >/dev/null 2>&1 || true
    fi
}

pid_start_signature() {
    local pid="$1"
    LC_ALL=C ps -p "$pid" -o lstart= 2>/dev/null | awk '{$1=$1; print}'
}

pid_is_same_process() {
    local pid="$1" expected_start="$2" current_start
    [ "$pid" -gt 0 ] || return 1
    kill -0 "$pid" 2>/dev/null || return 1
    [ -n "$expected_start" ] || return 1
    current_start=$(pid_start_signature "$pid")
    [ -n "$current_start" ] || return 1
    [ "$current_start" = "$expected_start" ]
}

pid_looks_like_watchdog() {
    local pid="$1" cmdline
    [ "$pid" -gt 0 ] || return 1
    cmdline=$(ps -p "$pid" -o command= 2>/dev/null || true)
    echo "$cmdline" | grep -q 'watchdog.sh'
}

rotate_log() {
    if [ -x "${SCRIPT_DIR}/rotate-logs.sh" ]; then
        "${SCRIPT_DIR}/rotate-logs.sh" >/dev/null 2>&1 || log "⚠️ rotate-logs.sh failed"
    fi

    local lines
    lines=$(wc -l < "$LOG" 2>/dev/null || echo 0)
    if [ "$lines" -gt 5000 ]; then
        tail -2000 "$LOG" > "${LOG}.tmp" && mv -f "${LOG}.tmp" "$LOG"
        log "📋 Log rotated (was ${lines} lines)"
    fi
    # 回收后台僵尸进程（wait -n 需要 bash 4.3+，macOS 默认 3.2）
    wait 2>/dev/null || true
    # 清理过期冷却/活动文件
    find "$COOLDOWN_DIR" -type f -mtime +1 -delete 2>/dev/null
    find "$ACTIVITY_DIR" -type f -mtime +1 -delete 2>/dev/null
}

# 冷却机制：检查某个 action 是否在冷却中
in_cooldown() {
    local key="$1" seconds="$2"
    local file="${COOLDOWN_DIR}/${key}"
    if [ -f "$file" ]; then
        local last=$(cat "$file" 2>/dev/null || echo 0)
        local now=$(now_ts)
        [ $((now - last)) -lt "$seconds" ] && return 0
    fi
    return 1
}

set_cooldown() {
    local key="$1"
    now_ts > "${COOLDOWN_DIR}/${key}"
}

nudge_pause_file() {
    local safe="$1"
    echo "${STATE_DIR}/nudge-paused-until-${safe}"
}

is_nudge_paused() {
    local safe="$1"
    local pause_file pause_until now
    pause_file=$(nudge_pause_file "$safe")
    [ -f "$pause_file" ] || return 1

    pause_until=$(cat "$pause_file" 2>/dev/null || echo 0)
    pause_until=$(normalize_int "$pause_until")
    now=$(now_ts)
    if [ "$pause_until" -gt "$now" ]; then
        return 0
    fi

    rm -f "$pause_file" 2>/dev/null || true
    return 1
}

pause_auto_nudge() {
    local window="$1" safe="$2" reason="$3"
    local now pause_until pause_file until_text pause_minutes
    now=$(now_ts)
    pause_until=$((now + NUDGE_PAUSE_SECONDS))
    pause_file=$(nudge_pause_file "$safe")
    echo "$pause_until" > "$pause_file"
    pause_minutes=$((NUDGE_PAUSE_SECONDS / 60))

    until_text=$(date -r "$pause_until" '+%H:%M:%S' 2>/dev/null || echo "${NUDGE_PAUSE_SECONDS}s 后")
    log "🚨 ${window}: ${reason}; pausing auto-nudge for ${NUDGE_PAUSE_SECONDS}s (until ${until_text})"
    send_telegram "🚨 ${window}: ${reason}。已暂停自动 nudge ${pause_minutes} 分钟（至 ${until_text}）。"
}

# 记录窗口最后一次有活动的时间
update_activity() {
    local safe="$1"
    now_ts > "${ACTIVITY_DIR}/${safe}"
}

get_idle_seconds() {
    local safe="$1"
    local file="${ACTIVITY_DIR}/${safe}"
    if [ -f "$file" ]; then
        local last=$(cat "$file" 2>/dev/null || echo 0)
        local now=$(now_ts)
        echo $((now - last))
    else
        # 首次运行没有记录，初始化为当前时间并返回 0
        # 下次如果还是 idle，就会开始累计
        update_activity "$safe"
        echo 0
    fi
}

reset_idle_probe() {
    local safe="$1"
    echo 0 > "${ACTIVITY_DIR}/idle-probe-${safe}-${CODEX_STATE_IDLE}"
    echo 0 > "${ACTIVITY_DIR}/idle-probe-${safe}-${CODEX_STATE_IDLE_LOW_CONTEXT}"
    rm -f "${ACTIVITY_DIR}/idle-probe-${safe}" 2>/dev/null || true
}

# 连续确认 + working 惯性，避免快照抖动误判 idle
idle_state_confirmed() {
    local safe="$1"
    local state_key="${2:-$CODEX_STATE_IDLE}"
    local probe_file="${ACTIVITY_DIR}/idle-probe-${safe}-${state_key}"
    local other_probe_file=""
    if [ "$state_key" = "$CODEX_STATE_IDLE" ]; then
        other_probe_file="${ACTIVITY_DIR}/idle-probe-${safe}-${CODEX_STATE_IDLE_LOW_CONTEXT}"
    elif [ "$state_key" = "$CODEX_STATE_IDLE_LOW_CONTEXT" ]; then
        other_probe_file="${ACTIVITY_DIR}/idle-probe-${safe}-${CODEX_STATE_IDLE}"
    fi
    local probe_count idle_secs

    idle_secs=$(get_idle_seconds "$safe")
    if [ "$idle_secs" -lt "$WORKING_INERTIA_SECONDS" ]; then
        echo 0 > "$probe_file"
        [ -n "$other_probe_file" ] && echo 0 > "$other_probe_file"
        return 1
    fi

    [ -n "$other_probe_file" ] && echo 0 > "$other_probe_file"
    probe_count=$(cat "$probe_file" 2>/dev/null || echo 0)
    probe_count=$(normalize_int "$probe_count")
    probe_count=$((probe_count + 1))
    echo "$probe_count" > "$probe_file"

    if [ "$probe_count" -lt "$IDLE_CONFIRM_PROBES" ]; then
        return 1
    fi

    return 0
}

# ---- 状态检测（统一来源 codex-status.sh）----
detect_state() {
    local window="$1"
    local safe="${2:-$(sanitize "$window")}" status_json state ctx_num

    status_json=$(get_window_status_json "$window")
    state=$(extract_status_field "$status_json" "status")
    [ -n "$state" ] || state="$CODEX_STATE_ABSENT"

    # 兼容 post-compact 恢复协议（基于统一状态输出的 context_num）
    ctx_num=$(extract_context_num_field "$status_json")
    if [ "$ctx_num" -ge 70 ]; then
        local compact_flag="${STATE_DIR}/post-compact-${safe}"
        if [ -f "${STATE_DIR}/was-low-context-${safe}" ]; then
            touch "$compact_flag"
            rm -f "${STATE_DIR}/was-low-context-${safe}"
        fi
    elif [ "$ctx_num" -ge 0 ] && [ "$ctx_num" -le "$LOW_CONTEXT_THRESHOLD" ]; then
        touch "${STATE_DIR}/was-low-context-${safe}"
    fi

    # Fix 5: compact 失败检测
    local compact_ts_file="${STATE_DIR}/compact-sent-ts-${safe}"
    if [ -f "$compact_ts_file" ] && [ "$ctx_num" -ge 0 ] && [ "$ctx_num" -le "$LOW_CONTEXT_THRESHOLD" ]; then
        local compact_sent_ts compact_elapsed compact_fail_file compact_fail_count
        compact_sent_ts=$(cat "$compact_ts_file" 2>/dev/null || echo 0)
        compact_sent_ts=$(normalize_int "$compact_sent_ts")
        compact_elapsed=$(( $(now_ts) - compact_sent_ts ))
        if [ "$compact_elapsed" -ge 180 ]; then
            # 3 分钟后 context 仍低 → compact 失败
            compact_fail_file="${STATE_DIR}/compact-fail-count-${safe}"
            compact_fail_count=$(cat "$compact_fail_file" 2>/dev/null || echo 0)
            compact_fail_count=$(normalize_int "$compact_fail_count")
            compact_fail_count=$((compact_fail_count + 1))
            echo "$compact_fail_count" > "$compact_fail_file"
            rm -f "$compact_ts_file"
            log "⚠️ ${window}: compact failure #${compact_fail_count} (context still ${ctx_num}% after ${compact_elapsed}s)"
            if [ "$compact_fail_count" -ge 3 ]; then
                send_telegram_alert "$window" "compact 连续 ${compact_fail_count} 次失败，context 仍 ${ctx_num}%"
                echo 0 > "$compact_fail_file"
            fi
        fi
    elif [ -f "$compact_ts_file" ] && [ "$ctx_num" -gt "$LOW_CONTEXT_THRESHOLD" ]; then
        # compact 成功，重置计数
        rm -f "$compact_ts_file"
        echo 0 > "${STATE_DIR}/compact-fail-count-${safe}" 2>/dev/null || true
    fi

    echo "$state"
}

# ---- 动作处理 ----
handle_permission() {
    local window="$1" safe="$2"
    local key="permission-${safe}"
    in_cooldown "$key" "$PERMISSION_COOLDOWN" && return

    acquire_lock "$safe" || { log "⏭ ${window}: permission locked"; return; }
    # 二次检查
    local recheck
    recheck=$($TMUX capture-pane -t "${SESSION}:${window}" -p 2>/dev/null | tail -8)
    if echo "$recheck" | grep -qiE "Yes, proceed|Press +enter +to +confirm|Allow once|Allow always|Esc to cancel"; then
        # 优先用 (p) permanently allow，其次 Enter 确认
        if echo "$recheck" | grep -qF "(p)"; then
            $TMUX send-keys -t "${SESSION}:${window}" "p" Enter
        else
            $TMUX send-keys -t "${SESSION}:${window}" Enter
        fi
        set_cooldown "$key"
        log "✅ ${window}: auto-approved permission"
    else
        log "⚠️ ${window}: permission detected but recheck didn't match"
    fi
    release_lock "$safe"
}

handle_idle() {
    local window="$1" safe="$2" project_dir="$3"
    local prd_done_logged_file="${STATE_DIR}/prd-done-logged-${safe}"
    local prd_skip_nudge=false

    # PRD 完成不代表没事做 — 还有 review fixes、autocheck issues、manual tasks
    # 只有当 PRD 完成 + 无 pending issues + 无 review issues 时才降低 nudge 频率
    local has_pending_work=false
    if [ -f "${STATE_DIR}/autocheck-issues-${safe}" ]; then
        has_pending_work=true
    fi
    if [ -f "${STATE_DIR}/prd-issues-${safe}" ]; then
        has_pending_work=true
    fi
    # 提前检查队列（用于后续绕过判断）
    local has_queue_task_early=false
    local queue_peek
    queue_peek=$("${SCRIPT_DIR}/task-queue.sh" next "$safe" 2>/dev/null || true)
    [ -n "$queue_peek" ] && has_queue_task_early=true

    if is_prd_todo_complete "$project_dir" && [ "$has_pending_work" = "false" ]; then
        local review_file="${STATE_DIR}/layer2-review-${safe}.txt"
        if [ -f "$review_file" ] && ! grep -qi "CLEAN" "$review_file" 2>/dev/null; then
            # review issues 退避计数
            local review_nudge_file="${STATE_DIR}/review-nudge-count-${safe}"
            local review_nudge_count
            review_nudge_count=$(cat "$review_nudge_file" 2>/dev/null || echo 0)
            review_nudge_count=$(normalize_int "$review_nudge_count")
            if [ "$review_nudge_count" -ge 5 ]; then
                # 连续 5 次 nudge review issues 都没新 commit → 停止 nudge
                if [ ! -f "${STATE_DIR}/review-issues-paused-${safe}" ]; then
                    log "⏸ ${window}: review issues nudge 已达 5 次无新 commit，暂停 nudge（等待手动安排或新 commit）"
                    touch "${STATE_DIR}/review-issues-paused-${safe}"
                fi
                prd_skip_nudge=true
            else
                echo $((review_nudge_count + 1)) > "$review_nudge_file"
                log "ℹ️ ${window}: PRD complete but review has issues, nudge #$((review_nudge_count + 1))/5"
            fi
        else
            if [ "$has_queue_task_early" = "true" ]; then
                # 队列有任务 → 绕过 prd-done 冷却
                log "📋 ${window}: PRD done but queue has tasks, bypassing prd-done cooldown"
            else
                # 真的没事做了 → 完全停止 nudge，不要干扰
                # 手动消息和队列任务会正常处理（由优先级 1/2 分支负责）
                prd_skip_nudge=true
            fi
        fi
    fi

    if [ "$prd_skip_nudge" = "true" ]; then
        if [ ! -f "$prd_done_logged_file" ]; then
            log "ℹ️ ${window}: PRD complete + review clean + no queue, skip nudge entirely"
            touch "$prd_done_logged_file"
        fi
        return
    fi
    rm -f "$prd_done_logged_file" 2>/dev/null || true

    # 检查是否有手动任务在 pending（手动消息 → 暂停 nudge 直到 Codex 开始工作）
    # 保护时间 300s (5分钟)：复杂任务 Codex 可能需要几分钟才开始 working
    local manual_task_file="${STATE_DIR}/manual-task-${safe}"
    if [ -f "$manual_task_file" ]; then
        local manual_ts
        manual_ts=$(cat "$manual_task_file" 2>/dev/null || echo 0)
        manual_ts=$(normalize_int "$manual_ts")
        local manual_age=$(( $(now_ts) - manual_ts ))
        if [ "$manual_age" -lt 300 ]; then
            log "⏭ ${window}: manual task sent ${manual_age}s ago, skipping nudge (protect 300s)"
            return
        else
            rm -f "$manual_task_file"
        fi
    fi

    # 复用之前的队列检查结果（避免重复调用 task-queue.sh）
    local has_queue_task="$has_queue_task_early"

    # 指数退避: nudge 次数越多，冷却越长 (300, 600, 1200, 2400, 4800, 9600)
    # 但队列任务绕过退避（用户主动提交 = 最高优先级）
    local key="nudge-${safe}"
    local nudge_count_file="${COOLDOWN_DIR}/nudge-count-${safe}"
    local nudge_count
    nudge_count=$(cat "$nudge_count_file" 2>/dev/null || echo 0)
    nudge_count=$(normalize_int "$nudge_count")

    if is_nudge_paused "$safe"; then
        return
    fi

    if [ "$has_queue_task" = "false" ]; then
        # 只有非队列任务才受退避限制
        # 连续 N 次无响应 → 暂停 30 分钟，避免无限 nudge
        if [ "$nudge_count" -ge "$NUDGE_MAX_RETRY" ]; then
            pause_auto_nudge "$window" "$safe" "已连续 ${nudge_count} 次 nudge 无响应"
            echo 0 > "$nudge_count_file"
            sync_project_status "$project_dir" "nudge_paused" "window=${window}" "state=idle" "reason=max_retry" "retry=${nudge_count}"
            return
        fi

        local effective_cooldown=$((NUDGE_COOLDOWN * (1 << (nudge_count > 5 ? 5 : nudge_count))))
        in_cooldown "$key" "$effective_cooldown" && return
    else
        log "📋 ${window}: queue task pending, bypassing backoff (nudge_count=${nudge_count})"
    fi

    local idle_secs
    idle_secs=$(get_idle_seconds "$safe")
    if [ "$idle_secs" -lt "$IDLE_THRESHOLD" ]; then
        return  # 还没 idle 够久
    fi

    # P0-1 兜底: 最近 5 分钟有 commit → 短暂休息，不 nudge
    local last_commit_ts
    last_commit_ts=$(run_with_timeout 10 git -C "$project_dir" log -1 --format="%ct" 2>/dev/null || echo 0)
    last_commit_ts=$(normalize_int "$last_commit_ts")
    local commit_age=$(( $(now_ts) - last_commit_ts ))
    if [ "$commit_age" -lt 300 ]; then
        return
    fi

    acquire_lock "$safe" || { log "⏭ ${window}: nudge locked"; return; }
    # 二次检查
    local state2
    state2=$(detect_state "$window" "$safe")
    if [ "$state2" = "$CODEX_STATE_IDLE" ] || [ "$state2" = "$CODEX_STATE_IDLE_LOW_CONTEXT" ]; then
        local nudge_msg before_head before_ctx before_status_json
        before_head=$(run_with_timeout 10 git -C "$project_dir" rev-parse HEAD 2>/dev/null || echo "none")
        before_status_json=$(get_window_status_json "$window")
        before_ctx=$(extract_context_num_field "$before_status_json")

        local manual_block_reason
        manual_block_reason=$(echo "$before_status_json" | jq -r '.manual_block_reason // ""' 2>/dev/null || echo "")
        if [ -n "$manual_block_reason" ]; then
            log "🛑 ${window}: manual block detected (${manual_block_reason}) — pausing nudges"
            pause_auto_nudge "$window" "$safe" "检测到人工阻塞（${manual_block_reason}）"
            echo 0 > "$nudge_count_file"
            sync_project_status "$project_dir" "nudge_blocked_manual" "window=${window}" "state=idle" "issue=${manual_block_reason}"
            release_lock "$safe"
            return
        fi

        local weekly_limit_pct
        weekly_limit_pct=$(extract_json_number "$before_status_json" "weekly_limit_pct")
        local weekly_limit_low=false
        local weekly_limit_exhausted=false
        if [ "$weekly_limit_pct" -ge 0 ] && [ "$weekly_limit_pct" -le 2 ]; then
            weekly_limit_exhausted=true
            weekly_limit_low=true
            log "🔴 ${window}: weekly limit exhausted (${weekly_limit_pct}%) — switching to Claude AgentTeam"
        elif [ "$weekly_limit_pct" -ge 0 ] && [ "$weekly_limit_pct" -lt 10 ]; then
            weekly_limit_low=true
            log "⚠️ ${window}: weekly limit low (${weekly_limit_pct}%) — will skip normal nudge (queue/compact still allowed)"
        fi

        # 优先级 1: post-compact 恢复协议（带上下文快照）
        local compact_flag="${STATE_DIR}/post-compact-${safe}"
        if [ -f "$compact_flag" ]; then
            # 从快照中恢复具体上下文
            local snapshot_file="${STATE_DIR}/pre-compact-snapshot-${safe}"
            local uncommitted="" recent_work="" queue_task="" last_nudge=""
            if [ -f "$snapshot_file" ]; then
                uncommitted=$(grep '^UNCOMMITTED_FILES:' "$snapshot_file" | sed 's/^UNCOMMITTED_FILES: //' || true)
                recent_work=$(grep '^RECENT_COMMITS:' "$snapshot_file" | sed 's/^RECENT_COMMITS: //' || true)
                queue_task=$(grep '^QUEUE_IN_PROGRESS:' "$snapshot_file" | sed 's/^QUEUE_IN_PROGRESS: //' || true)
                last_nudge=$(grep '^LAST_NUDGE:' "$snapshot_file" | sed 's/^LAST_NUDGE: //' || true)
            fi

            # 构造有针对性的恢复消息
            nudge_msg="compaction完成。先阅读 CONVENTIONS.md 与 prd-todo.md。"
            # 未提交改动 — 最高优先级
            if [ -n "$uncommitted" ]; then
                nudge_msg="${nudge_msg} 重要: 有未提交的改动(${uncommitted:0:100}),请先检查并commit。"
            fi
            # 恢复具体任务
            if [ -n "$queue_task" ]; then
                nudge_msg="${nudge_msg} 之前正在做: ${queue_task:0:100}。"
            elif [ -n "$last_nudge" ]; then
                nudge_msg="${nudge_msg} 之前的任务: ${last_nudge:0:120}。"
            elif [ -n "$recent_work" ]; then
                nudge_msg="${nudge_msg} 最近工作方向: ${recent_work:0:100}。"
            fi

            if send_tmux_message "$window" "$nudge_msg" "post-compact recovery nudge"; then
                rm -f "$compact_flag" "$snapshot_file"
                set_cooldown "$key"
                log "🔄 ${window}: post-compact recovery nudge sent (with snapshot)"
                start_nudge_ack_check "$window" "$safe" "$project_dir" "$before_head" "$before_ctx" "post-compact recovery nudge"
                sync_project_status "$project_dir" "nudge_sent" "window=${window}" "reason=post_compact" "state=idle"
            fi
            release_lock "$safe"
            return
        fi

        # 优先级 2: 任务队列（用户手动提交的 bug/需求）
        local queue_task
        queue_task=$("${SCRIPT_DIR}/task-queue.sh" next "$safe" 2>/dev/null || true)
        if [ -n "$queue_task" ]; then
            local queue_task_type queue_pending_line queue_file
            queue_task_type="general"
            queue_file="${HOME}/.autopilot/task-queue/${safe}.md"
            queue_pending_line=$(grep -m1 '^\- \[ \]' "$queue_file" 2>/dev/null || true)
            if [ -n "$queue_pending_line" ]; then
                queue_task_type=$(extract_queue_meta_from_line "$queue_pending_line" "type" 2>/dev/null || echo "general")
                [ -n "$queue_task_type" ] || queue_task_type="general"
            fi

            if [ "$weekly_limit_exhausted" = "true" ]; then
                # Codex 额度耗尽 → 用 Claude AgentTeam 替代
                "${SCRIPT_DIR}/task-queue.sh" start "$safe" 2>/dev/null || true
                log "🤖 ${window}: Codex limit exhausted, dispatching to Claude AgentTeam"
                ( "${SCRIPT_DIR}/claude-fallback.sh" "$safe" "$project_dir" "$queue_task" \
                    >> "${HOME}/.autopilot/logs/claude-fallback.log" 2>&1 ) &
                set_cooldown "$key"
                echo 0 > "$nudge_count_file"
                sync_project_status "$project_dir" "claude_fallback" "window=${window}" "state=idle"
            elif is_frontend_task "$queue_task_type"; then
                # 前端任务 → 路由到 Gemini tmux 窗口
                local gemini_win
                gemini_win=$(get_gemini_window "$safe" 2>/dev/null || true)
                nudge_msg=$(build_task_prompt_by_type "$queue_task_type" "${queue_task:0:280}")
                if [ -n "$gemini_win" ] && send_gemini_message "$gemini_win" "$nudge_msg"; then
                    "${SCRIPT_DIR}/task-queue.sh" start "$safe" 2>/dev/null || true
                    set_cooldown "$key"
                    echo 0 > "$nudge_count_file"
                    log "🎨 ${window}: frontend task routed to Gemini(${gemini_win}) — ${nudge_msg:0:80}"
                    sync_project_status "$project_dir" "gemini_task_sent" "window=${gemini_win}" "state=idle"
                    send_telegram "🎨 ${window}: 前端任务已发送到 Gemini(${gemini_win}) — ${nudge_msg:0:100}"
                else
                    # Gemini 不可用，降级到 Codex
                    log "⚠️ ${window}: Gemini unavailable, falling back to Codex for frontend task"
                    if send_tmux_message "$window" "$nudge_msg" "queue task (frontend→codex fallback)" "$queue_task_type" "auto"; then
                        "${SCRIPT_DIR}/task-queue.sh" start "$safe" 2>/dev/null || true
                        set_cooldown "$key"
                        echo 0 > "$nudge_count_file"
                        log "📋 ${window}: frontend task sent to Codex (Gemini fallback) — ${nudge_msg:0:80}"
                        start_nudge_ack_check "$window" "$safe" "$project_dir" "$before_head" "$before_ctx" "queue task"
                        sync_project_status "$project_dir" "queue_task_sent" "window=${window}" "state=idle"
                        send_telegram "📋 ${window}: 前端任务降级到 Codex — ${nudge_msg:0:100}"
                    fi
                fi
            else
                # 正常 Codex 派发
                nudge_msg=$(build_task_prompt_by_type "$queue_task_type" "${queue_task:0:280}")
                if send_tmux_message "$window" "$nudge_msg" "queue task" "$queue_task_type" "auto"; then
                    "${SCRIPT_DIR}/task-queue.sh" start "$safe" 2>/dev/null || true
                    set_cooldown "$key"
                    echo 0 > "$nudge_count_file"  # 队列任务重置退避计数
                    log "📋 ${window}: queue task sent(type=${queue_task_type}) — ${nudge_msg:0:80}"
                    start_nudge_ack_check "$window" "$safe" "$project_dir" "$before_head" "$before_ctx" "queue task"
                    sync_project_status "$project_dir" "queue_task_sent" "window=${window}" "state=idle"
                    send_telegram "📋 ${window}: 开始处理队列任务 — ${nudge_msg:0:100}"
                fi
            fi
            release_lock "$safe"
            return
        fi

        # weekly limit 低 → 跳过普通 nudge（queue/compact 已在上面处理）
        if [ "$weekly_limit_low" = "true" ]; then
            if [ "$weekly_limit_exhausted" = "true" ]; then
                # 额度耗尽但还有 autocheck/prd issues → 用 Claude 修
                local fallback_task=""
                if [ -f "${STATE_DIR}/autocheck-issues-${safe}" ]; then
                    fallback_task="修复以下自动检查问题: $(cat "${STATE_DIR}/autocheck-issues-${safe}" 2>/dev/null)"
                    rm -f "${STATE_DIR}/autocheck-issues-${safe}"
                elif [ -f "${STATE_DIR}/prd-issues-${safe}" ]; then
                    fallback_task="修复PRD验证失败项: $(cat "${STATE_DIR}/prd-issues-${safe}" 2>/dev/null)"
                    rm -f "${STATE_DIR}/prd-issues-${safe}"
                fi
                if [ -n "$fallback_task" ]; then
                    log "🤖 ${window}: Codex exhausted + pending issues → Claude fallback"
                    ( "${SCRIPT_DIR}/claude-fallback.sh" "$safe" "$project_dir" "$fallback_task" \
                        >> "${HOME}/.autopilot/logs/claude-fallback.log" 2>&1 ) &
                    set_cooldown "$key"
                    sync_project_status "$project_dir" "claude_fallback" "window=${window}" "reason=issues"
                fi
            else
                log "⚠️ ${window}: weekly limit low (${weekly_limit_pct}%) — skipping normal nudge"
                send_telegram_alert "$window" "weekly limit low (${weekly_limit_pct}%) — skipping normal nudge"
            fi
            sync_project_status "$project_dir" "nudge_skipped" "window=${window}" "state=idle" "reason=limit_low"
            release_lock "$safe"
            return
        fi

        # 优先级 3: Layer 1 自动检查发现的问题
        local issues_file="${STATE_DIR}/autocheck-issues-${safe}"
        local prd_issues_file="${STATE_DIR}/prd-issues-${safe}"
        local used_issues_file=false
        local used_prd_issues_file=false
        if [ -f "$issues_file" ]; then
            local issues
            issues=$(cat "$issues_file")
            nudge_msg="修复以下自动检查发现的问题，然后继续推进：${issues}"
            used_issues_file=true
        elif [ -f "$prd_issues_file" ]; then
            local prd_issues
            prd_issues=$(cat "$prd_issues_file")
            nudge_msg="PRD checker 未通过，先修复以下失败项：${prd_issues}"
            used_prd_issues_file=true
        else
            # 没有明确任务（无 queue、无 issues、无 PRD 问题）→ 不 nudge
            # 避免空转浪费 token。等手动安排任务或队列有新条目再 nudge
            log "💤 ${window}: idle 但无待办任务，跳过 nudge"
            release_lock "$safe"
            return
        fi

        local nudge_reason="idle"
        local git_dirty
        # 过滤运行时文件(status.json, prd-progress.json, .code-review/, locks/, logs/, state/)
        # 只关注有实质代码改动的 dirty
        git_dirty=$(git -C "$project_dir" status --porcelain 2>/dev/null \
            | grep -v 'status\.json' \
            | grep -v 'prd-progress\.json' \
            | grep -v '\.code-review/' \
            | grep -v '\.DS_Store$' \
            | grep -v '\.last-review-commit$' \
            | grep -v 'locks/' \
            | grep -v 'logs/' \
            | grep -v 'state/' \
            || true)
        if [ -n "$git_dirty" ]; then
            local dirty_summary
            dirty_summary=$(printf '%s' "$git_dirty" | head -n 5 | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g')
            [ -z "$dirty_summary" ] && dirty_summary="uncommitted changes"
            nudge_msg="当前仓库存在未提交改动（${dirty_summary:0:120}），请先提交/暂存再继续新任务。"
            nudge_reason="git_dirty"
            log "🛠 ${window}: dirty tree detected before idle nudge; nudging to commit"
        fi

        if send_tmux_message "$window" "$nudge_msg" "idle nudge"; then
            if [ "$nudge_reason" != "git_dirty" ]; then
                [ "$used_issues_file" = "true" ] && rm -f "$issues_file"
                [ "$used_prd_issues_file" = "true" ] && rm -f "$prd_issues_file"
            fi
            set_cooldown "$key"
            echo $((nudge_count + 1)) > "$nudge_count_file"
            log "📤 ${window}: auto-nudged #$((nudge_count+1)) (idle ${idle_secs}s) — ${nudge_msg:0:80}"
            start_nudge_ack_check "$window" "$safe" "$project_dir" "$before_head" "$before_ctx" "idle nudge"
            sync_project_status "$project_dir" "nudge_sent" "window=${window}" "reason=${nudge_reason}" "state=idle"
        else
            local failed_count=$((nudge_count + 1))
            echo "$failed_count" > "$nudge_count_file"
            set_cooldown "$key"
            log "❌ ${window}: idle nudge send failed (#${failed_count})"
            sync_project_status "$project_dir" "nudge_send_failed" "window=${window}" "reason=${nudge_reason}" "state=idle" "retry=${failed_count}"
            if [ "$failed_count" -ge "$NUDGE_MAX_RETRY" ]; then
                pause_auto_nudge "$window" "$safe" "idle nudge 连续发送失败 ${failed_count} 次"
                echo 0 > "$nudge_count_file"
                sync_project_status "$project_dir" "nudge_paused" "window=${window}" "state=idle" "reason=send_failed" "retry=${failed_count}"
            fi
        fi
    fi
    release_lock "$safe"
}

handle_low_context() {
    local window="$1" safe="$2" project_dir="$3"
    local key="compact-${safe}"
    in_cooldown "$key" "$COMPACT_COOLDOWN" && return

    acquire_lock "$safe" || { log "⏭ ${window}: compact locked"; return; }
    # 二次检查：必须仍在 idle 状态（› 提示符）且低上下文
    local state2
    state2=$(detect_state "$window" "$safe")
    if [ "$state2" = "$CODEX_STATE_IDLE_LOW_CONTEXT" ]; then
        # ★ compact 前保存上下文快照：未提交改动 + 最近任务 + 队列状态
        local snapshot_file="${STATE_DIR}/pre-compact-snapshot-${safe}"
        {
            echo "# Pre-compact snapshot $(date '+%Y-%m-%d %H:%M:%S')"
            # 未提交改动
            local dirty_files
            dirty_files=$(git -C "$project_dir" diff --name-only 2>/dev/null | head -10 || true)
            local staged_files
            staged_files=$(git -C "$project_dir" diff --cached --name-only 2>/dev/null | head -10 || true)
            if [ -n "$dirty_files" ] || [ -n "$staged_files" ]; then
                echo "UNCOMMITTED_FILES: ${dirty_files} ${staged_files}"
            fi
            # 最近 commit（反映当前工作方向）
            local recent
            recent=$(git -C "$project_dir" log --oneline -3 --format="%s" 2>/dev/null | tr '\n' '; ' || true)
            [ -n "$recent" ] && echo "RECENT_COMMITS: ${recent}"
            # 队列中进行中的任务
            local queue_task
            queue_task=$(grep -m1 '^\- \[→\]' "${HOME}/.autopilot/task-queue/${safe}.md" 2>/dev/null | sed 's/^- \[→\] //; s/ | added:.*$//' || true)
            [ -n "$queue_task" ] && echo "QUEUE_IN_PROGRESS: ${queue_task}"
            # 最后一次 nudge 内容
            local last_nudge_file="${STATE_DIR}/last-nudge-msg-${safe}"
            [ -f "$last_nudge_file" ] && echo "LAST_NUDGE: $(cat "$last_nudge_file")"
        } > "$snapshot_file"
        log "📸 ${window}: saved pre-compact snapshot"

        if send_tmux_message "$window" "/compact" "compact"; then
            set_cooldown "$key"
            # Fix 5: 记录 compact 发送时间
            now_ts > "${STATE_DIR}/compact-sent-ts-${safe}"
            log "🗜 ${window}: sent /compact"
            sync_project_status "$project_dir" "compact_sent" "window=${window}" "state=idle_low_context"
        fi
    fi
    release_lock "$safe"
}

handle_shell() {
    local window="$1" safe="$2" project_dir="$3"
    local key="shell-${safe}"
    in_cooldown "$key" "$SHELL_COOLDOWN" && return

    acquire_lock "$safe" || { log "⏭ ${window}: shell locked"; return; }
    # 二次检查：必须仍在 shell 状态
    local state2
    state2=$(detect_state "$window" "$safe")
    if [ "$state2" = "$CODEX_STATE_SHELL" ]; then
        $TMUX send-keys -t "${SESSION}:${window}" "cd '${project_dir}' && (${CODEX} resume --last 2>/dev/null || ${CODEX} --full-auto)" Enter
        set_cooldown "$key"
        log "🔄 ${window}: shell recovery"
        sync_project_status "$project_dir" "shell_recovery" "window=${window}" "state=shell"
    fi
    release_lock "$safe"
}

# ---- Layer 1: 自动检查 ----

# 获取当前 commit hash
get_head() {
    local dir="$1"
    git -C "$dir" rev-parse HEAD 2>/dev/null || echo "none"
}

attempt_branch_auto_merge_if_ready() {
    local window="$1" safe="$2" project_dir="$3" state="$4"
    local current_branch="$5" queue_task_branch="$6" queue_task_base="$7"
    local commit_msg="${8:-}" current_head="${9:-}"

    [ -n "$queue_task_branch" ] || return 1
    [[ "$queue_task_branch" == ap/* ]] || return 1
    [ "$current_branch" = "$queue_task_branch" ] || return 1
    is_idle_state_for_tracked_completion "$state" || return 1
    [ "$BRANCH_ISOLATION_ENABLED" = "true" ] || return 1
    [ "$BRANCH_AUTO_MERGE_ENABLED" = "true" ] || return 1
    [ -x "$BRANCH_MANAGER" ] || return 1

    local merge_base ahead_count
    merge_base="${queue_task_base:-$BRANCH_BASE_BRANCH}"
    ahead_count=$(run_with_timeout 10 git -C "$project_dir" rev-list "${merge_base}..${queue_task_branch}" --count 2>/dev/null || echo 0)
    ahead_count=$(normalize_int "$ahead_count")
    [ "$ahead_count" -gt 0 ] || return 1

    local merge_gate_ok=true gate_output gate_rc
    if [ "$BRANCH_REQUIRE_AUTO_CHECK" = "true" ]; then
        gate_output=$("${SCRIPT_DIR}/auto-check.sh" "$project_dir" --issues-only 2>&1)
        gate_rc=$?
        if [ "$gate_rc" -ne 0 ]; then
            merge_gate_ok=false
            if [ -n "$gate_output" ]; then
                echo "$gate_output" > "${STATE_DIR}/autocheck-issues-${safe}.tmp" \
                    && mv -f "${STATE_DIR}/autocheck-issues-${safe}.tmp" "${STATE_DIR}/autocheck-issues-${safe}"
            fi
            log "⏭ ${window}: branch merge gated by auto-check issues (${queue_task_branch})"
        fi
    fi
    if [ "$BRANCH_REQUIRE_TESTS" = "true" ]; then
        # Phase 1 暂不强制标准化测试门禁，仅记录配置告警，避免阻塞主流程。
        log "ℹ️ ${window}: require_tests=true（Phase 1 暂未接入统一测试门禁）"
    fi

    [ "$merge_gate_ok" = "true" ] || return 0

    local merge_json merge_status merge_head merge_reason
    merge_json=$("$BRANCH_MANAGER" auto-merge "$project_dir" "$safe" "$queue_task_branch" "$merge_base" 2>/dev/null || true)
    if command -v jq >/dev/null 2>&1; then
        merge_status=$(echo "$merge_json" | jq -r '.status // ""' 2>/dev/null || echo "")
        merge_head=$(echo "$merge_json" | jq -r '.head // ""' 2>/dev/null || echo "")
        merge_reason=$(echo "$merge_json" | jq -r '.reason // ""' 2>/dev/null || echo "")
    else
        merge_status=$(echo "$merge_json" | sed -n 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)
        merge_head=$(echo "$merge_json" | sed -n 's/.*"head"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)
        merge_reason=$(echo "$merge_json" | sed -n 's/.*"reason"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)
    fi

    case "$merge_status" in
        merged)
            [ -n "$merge_head" ] || merge_head=$(run_with_timeout 10 git -C "$project_dir" rev-parse HEAD 2>/dev/null || echo "$current_head")
            local queue_done_output queue_source remaining done_msg discord_done_msg display_msg
            queue_done_output=$("${SCRIPT_DIR}/task-queue.sh" done "$safe" "${merge_head:0:7}" 2>/dev/null || true)
            queue_source=$(printf '%s\n' "$queue_done_output" | sed -n 's/^SOURCE: //p' | head -n1 | tr -d '\r')
            remaining=$("${SCRIPT_DIR}/task-queue.sh" count "$safe" 2>/dev/null || echo 0)
            remaining=$(normalize_int "$remaining")
            display_msg="$commit_msg"
            [ -n "$display_msg" ] || display_msg=$(run_with_timeout 10 git -C "$project_dir" log -1 --format="%s" "$merge_head" 2>/dev/null || echo "")

            done_msg="✅ ${window}: 分支任务已合并 (${merge_head:0:7}) — ${display_msg:0:80}"
            [ "$remaining" -gt 0 ] && done_msg="${done_msg}\n📋 还剩 ${remaining} 个任务待处理"
            send_telegram "$done_msg"

            discord_done_msg="✅ ${window}: 分支任务已合并 (${merge_head:0:7}) — ${display_msg:0:80}"
            [ "$remaining" -gt 0 ] && discord_done_msg="${discord_done_msg} | 还剩 ${remaining} 个任务"
            [ -n "$queue_source" ] && discord_done_msg="${discord_done_msg} | source: ${queue_source}"
            send_discord_by_window "$window" "$discord_done_msg"
            log "🌿✅ ${window}: branch auto-merged (${queue_task_branch} -> ${merge_base})"
            return 0
            ;;
        conflict)
            "${SCRIPT_DIR}/task-queue.sh" fail "$safe" "branch-merge-conflict" >/dev/null 2>&1 || true
            "${SCRIPT_DIR}/task-queue.sh" add "$safe" \
                "解决分支冲突并完成合并：${queue_task_branch} -> ${merge_base}" \
                high --type review_fix >/dev/null 2>&1 || true
            send_telegram "⚠️ ${window}: 分支自动合并冲突，已入队冲突修复任务（${queue_task_branch}）"
            send_discord_by_window "$window" "⚠️ ${window}: 分支自动合并冲突，已入队冲突修复任务（${queue_task_branch}）"
            log "⚠️ ${window}: branch auto-merge conflict (${queue_task_branch}, reason=${merge_reason:-unknown})"
            return 0
            ;;
        *)
            log "⚠️ ${window}: branch auto-merge failed (${queue_task_branch}, status=${merge_status:-unknown}, reason=${merge_reason:-unknown})"
            return 1
            ;;
    esac
}

# 检测新 commit 并运行自动检查
check_new_commits() {
    local window="$1" safe="$2" project_dir="$3" state="${4:-$CODEX_STATE_IDLE}"
    local count_file="${COMMIT_COUNT_DIR}/${safe}-since-review"
    local legacy_head_file="${COMMIT_COUNT_DIR}/${safe}-head"

    local current_head current_branch branch_key head_file
    current_head=$(run_with_timeout 10 git -C "$project_dir" rev-parse HEAD 2>/dev/null || echo "none")
    [ "$current_head" = "none" ] && return
    current_branch=$(run_with_timeout 10 git -C "$project_dir" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
    branch_key=$(sanitize_branch_for_key "$current_branch")
    [ -n "$branch_key" ] || branch_key="detached"
    head_file="${COMMIT_COUNT_DIR}/${safe}-${branch_key}-head"

    local last_head
    last_head=$(cat "$head_file" 2>/dev/null || echo "none")
    if [ "$last_head" = "none" ]; then
        last_head=$(cat "$legacy_head_file" 2>/dev/null || echo "none")
    fi

    # 队列任务信息（包含 branch 隔离 metadata）
    local queue_file queue_in_progress queue_in_progress_line queue_task_branch queue_task_base queue_source
    queue_file="${HOME}/.autopilot/task-queue/${safe}.md"
    queue_in_progress_line=$(grep -m1 '^\- \[→\]' "$queue_file" 2>/dev/null || true)
    queue_in_progress=$(normalize_int "$(grep -c '^\- \[→\]' "$queue_file" 2>/dev/null || echo 0)")
    if [ "$queue_in_progress" -gt 0 ]; then
        queue_task_branch=$(extract_queue_meta_from_line "$queue_in_progress_line" "task_branch" 2>/dev/null || true)
        queue_task_base=$(extract_queue_meta_from_line "$queue_in_progress_line" "base_branch" 2>/dev/null || true)
        if [ -z "$queue_task_branch" ] && command -v jq >/dev/null 2>&1; then
            local branch_state_file branch_state
            branch_state_file="${STATE_DIR}/branches/${safe}.json"
            if [ -f "$branch_state_file" ] && jq -e . "$branch_state_file" >/dev/null 2>&1; then
                branch_state=$(jq -r '.state // ""' "$branch_state_file" 2>/dev/null || echo "")
                case "$branch_state" in
                    created|in_progress|ready_merge)
                        queue_task_branch=$(jq -r '.active_branch // ""' "$branch_state_file" 2>/dev/null || echo "")
                        queue_task_base=$(jq -r '.base_branch // ""' "$branch_state_file" 2>/dev/null || echo "")
                        ;;
                esac
            fi
        fi
    fi

    # 没有新 commit
    if [ "$current_head" = "$last_head" ]; then
        if [ "$queue_in_progress" -gt 0 ]; then
            attempt_branch_auto_merge_if_ready \
                "$window" "$safe" "$project_dir" "$state" \
                "$current_branch" "$queue_task_branch" "$queue_task_base" "" "$current_head" || true
        fi
        return
    fi

    # 记录新 head（分支维度 + 兼容旧路径）
    echo "$current_head" > "$head_file"
    echo "$current_head" > "$legacy_head_file"

    # P0-1 fix: 有新 commit 说明刚在工作，重置 activity 时间戳
    update_activity "$safe"
    # 重置 nudge 退避计数 + 清除暂停状态
    echo 0 > "${COOLDOWN_DIR}/nudge-count-${safe}"
    rm -f "$(nudge_pause_file "$safe")" "${STATE_DIR}/alert-stalled-${safe}"
    # Fix 4: 新 commit 重置 review 重试计数
    rm -f "${STATE_DIR}/review-retry-count-${safe}" "${STATE_DIR}/review-failed-${safe}"

    # 增加 commit 计数
    local count
    count=$(cat "$count_file" 2>/dev/null || echo 0)
    # 计算新增 commit 数
    local new_commits=1
    if [ "$last_head" != "none" ]; then
        new_commits=$(git -C "$project_dir" rev-list "${last_head}..${current_head}" --count 2>/dev/null || echo 1)
    fi
    count=$((count + new_commits))
    echo "$count" > "$count_file"

    # 获取最新 commit message
    local msg
    msg=$(git -C "$project_dir" log -1 --format="%s" 2>/dev/null || echo "")

    log "📝 ${window}: new commit on ${current_branch} (+${new_commits}, total since review: ${count}) — ${msg}"
    sync_project_status "$project_dir" "commit" "window=${window}" "head=${current_head}" "new_commits=${new_commits}" "since_review=${count}" "state=working"

    # 新 commit → 重置 review issues 退避计数
    rm -f "${STATE_DIR}/review-nudge-count-${safe}" "${STATE_DIR}/review-issues-paused-${safe}" 2>/dev/null || true

    # 队列任务完成检测：支持普通任务与 branch 隔离任务两种路径
    if [ "$queue_in_progress" -gt 0 ]; then
        if [ -n "$queue_task_branch" ] && [[ "$queue_task_branch" == ap/* ]]; then
            attempt_branch_auto_merge_if_ready \
                "$window" "$safe" "$project_dir" "$state" \
                "$current_branch" "$queue_task_branch" "$queue_task_base" "$msg" "$current_head" || true
        else
            # 普通任务：旧行为保持不变（检测到新 commit 即 done）。
            local queue_done_output
            queue_done_output=$("${SCRIPT_DIR}/task-queue.sh" done "$safe" "${current_head:0:7}" 2>/dev/null || true)
            queue_source=$(printf '%s\n' "$queue_done_output" | sed -n 's/^SOURCE: //p' | head -n1 | tr -d '\r')
            log "📋✅ ${window}: queue task completed (commit ${current_head:0:7})"
            local remaining
            remaining=$("${SCRIPT_DIR}/task-queue.sh" count "$safe" 2>/dev/null || echo 0)
            remaining=$(normalize_int "$remaining")
            if [ "$remaining" -gt 0 ]; then
                log "📋 ${window}: ${remaining} more tasks in queue"
            fi
            local done_msg="✅ ${window}: 队列任务完成 (${current_head:0:7}) — ${msg:0:80}"
            [ "$remaining" -gt 0 ] && done_msg="${done_msg}\n📋 还剩 ${remaining} 个任务待处理"
            send_telegram "$done_msg"

            local discord_done_msg="✅ ${window}: 队列任务完成 (${current_head:0:7}) — ${msg:0:80}"
            [ "$remaining" -gt 0 ] && discord_done_msg="${discord_done_msg} | 还剩 ${remaining} 个任务"
            [ -n "$queue_source" ] && discord_done_msg="${discord_done_msg} | source: ${queue_source}"
            send_discord_by_window "$window" "$discord_done_msg"
        fi
    fi

    # Layer 1 自动检查
    run_auto_checks "$window" "$safe" "$project_dir"
    maybe_trigger_test_agent_on_commit "$window" "$safe" "$project_dir" "$current_head"
    # PRD 引擎：按本次 commit 变更文件自动匹配并执行 checker
    run_prd_checks_for_commit "$window" "$safe" "$project_dir" "$last_head" "$current_head"

    # Layer 2 触发检查：commit 数达标且 idle 时，通知 cron 触发增量 review
    check_incremental_review_trigger "$window" "$safe" "$project_dir" "$count"
}

run_auto_checks() {
    local window="$1" safe="$2" project_dir="$3"
    local key="autocheck-${safe}"
    in_cooldown "$key" 120 && return  # 2 分钟内不重复跑
    set_cooldown "$key"

    # 后台异步执行，不阻塞主循环
    # 用 lockfile 防止同一项目同时跑多个 autocheck
    local check_lock="${LOCK_DIR}/autocheck-${safe}.lock.d"
    if ! mkdir "$check_lock" 2>/dev/null; then
        log "⏭ ${window}: autocheck already running, skip"
        return
    fi
    (
        trap 'rm -rf "'"$check_lock"'"' EXIT
        local check_output rc issues
        check_output=$("${SCRIPT_DIR}/auto-check.sh" "$project_dir" --issues-only 2>&1)
        rc=$?

        if [ "$rc" -eq 0 ]; then
            rm -f "${STATE_DIR}/autocheck-issues-${safe}" "${STATE_DIR}/autocheck-hash-${safe}" 2>/dev/null || true
            return 0
        fi

        issues=$(printf '%s\n' "$check_output" | sed '/^[[:space:]]*$/d')
        [ -n "$issues" ] || issues="auto-check failed (rc=${rc})"

        # P1-4: issue hash 去重，相同问题不重复 nudge
        local issues_hash
        issues_hash=$(hash_text "$issues")
        local prev_hash
        prev_hash=$(cat "${STATE_DIR}/autocheck-hash-${safe}" 2>/dev/null || echo "")
        if [ "$issues_hash" = "$prev_hash" ]; then
            log "⏭ ${window}: Layer 1 issues unchanged, skip re-nudge"
        else
            echo "$issues_hash" > "${STATE_DIR}/autocheck-hash-${safe}"
            log "⚠️ ${window}: Layer 1 issues — ${issues:0:200}"
            echo "$issues" > "${STATE_DIR}/autocheck-issues-${safe}.tmp" && mv -f "${STATE_DIR}/autocheck-issues-${safe}.tmp" "${STATE_DIR}/autocheck-issues-${safe}"
        fi
    ) &
}

run_prd_checks_for_commit() {
    local window="$1" safe="$2" project_dir="$3" last_head="$4" current_head="$5"
    local prd_items="${project_dir}/prd-items.yaml"
    local prd_verify="${SCRIPT_DIR}/prd-verify.sh"
    local prd_engine="${SCRIPT_DIR}/prd_verify_engine.py"
    local output_file="${project_dir}/prd-progress.json"
    local issues_file="${STATE_DIR}/prd-issues-${safe}"
    local -a verify_cmd

    [ -f "$prd_items" ] || return
    if [ -x "$prd_verify" ]; then
        verify_cmd=("$prd_verify" --project-dir "$project_dir")
    elif [ -f "$prd_engine" ]; then
        verify_cmd=("python3" "$prd_engine" --project-dir "$project_dir")
    else
        return
    fi

    local changed_files
    if [ "$last_head" != "none" ]; then
        changed_files=$(run_with_timeout 10 git -C "$project_dir" diff --name-only "${last_head}..${current_head}" --diff-filter=ACMR 2>/dev/null || true)
    else
        changed_files=$(run_with_timeout 10 git -C "$project_dir" show --pretty='' --name-only "${current_head}" --diff-filter=ACMR 2>/dev/null || true)
    fi
    changed_files=$(echo "$changed_files" | sed '/^$/d')
    [ -z "$changed_files" ] && return

    local check_lock="${LOCK_DIR}/prdcheck-${safe}.lock.d"
    if ! mkdir "$check_lock" 2>/dev/null; then
        log "⏭ ${window}: PRD check already running, skip ${current_head:0:7}"
        return
    fi

    (
        trap 'rm -rf "'"$check_lock"'"' EXIT
        local changed_files_json
        changed_files_json=$(printf '%s\n' "$changed_files" | python3 -c 'import json,sys; print(json.dumps([line.rstrip("\n") for line in sys.stdin if line.rstrip("\n")], ensure_ascii=False))' 2>/dev/null || echo "[]")
        local verify_output rc
        verify_output=$(run_with_timeout 45 "${verify_cmd[@]}" --changed-files "$changed_files_json" --output "$output_file" --sync-todo --print-failures-only 2>&1)
        rc=$?

        if [ "$rc" -eq 0 ]; then
            rm -f "$issues_file"
            log "✅ ${window}: PRD verify passed for ${current_head:0:7}"
            sync_project_status "$project_dir" "prd_verify_pass" "window=${window}" "state=working" "head=${current_head}"
            exit 0
        fi

        verify_output=$(echo "$verify_output" | tr '\n' ' ' | tr -s ' ' | sed 's/^ *//; s/ *$//')
        echo "$verify_output" > "${issues_file}.tmp" && mv -f "${issues_file}.tmp" "$issues_file"
        log "⚠️ ${window}: PRD verify failed — ${verify_output:0:200}"
        sync_project_status "$project_dir" "prd_verify_fail" "window=${window}" "state=working" "head=${current_head}" "issues=${verify_output:0:220}"
    ) &
}

# Layer 2 增量 review 触发
check_incremental_review_trigger() {
    local window="$1" safe="$2" project_dir="$3" count="$4"
    local key="review-${safe}"

    # 冷却检查
    in_cooldown "$key" "$REVIEW_COOLDOWN" && return

    # 条件1: commit 数 >= 阈值 OR 2 小时无 review
    local last_review_ts_file="${COMMIT_COUNT_DIR}/${safe}-last-review-ts"
    local last_review_ts
    last_review_ts=$(cat "$last_review_ts_file" 2>/dev/null || echo 0)
    local time_since_review=$(( $(now_ts) - last_review_ts ))

    local should_trigger=false
    if [ "$count" -ge "$COMMITS_FOR_REVIEW" ]; then
        should_trigger=true
    elif [ "$time_since_review" -ge "$REVIEW_COOLDOWN" ] && [ "$count" -gt 0 ]; then
        should_trigger=true
    fi
    # 快速 re-review：如果上次 review 有问题（issues 文件存在），降低触发门槛
    # 只需 3 个 fix commit + 30 分钟冷却
    local issues_file="${STATE_DIR}/autocheck-issues-${safe}"
    if [ -f "$issues_file" ] && [ "$count" -ge 3 ] && [ "$time_since_review" -ge 1800 ]; then
        should_trigger=true
        log "🔄 ${window}: fast re-review triggered (${count} fix commits, issues pending)"
    fi
    [ "$should_trigger" = "false" ] && return

    # 条件2: 当前是 idle 状态
    local state
    state=$(detect_state "$window" "$safe")
    [ "$state" != "$CODEX_STATE_IDLE" ] && return

    # 触发增量 review — 写 pending 标记，cron 执行成功后才重置计数（两阶段提交）
    local trigger_file="${STATE_DIR}/review-trigger-${safe}"
    local tmp_trigger="${trigger_file}.tmp"
    if command -v jq >/dev/null 2>&1; then
        jq -n --arg project_dir "$project_dir" --arg window "$window" '{project_dir:$project_dir,window:$window}' > "$tmp_trigger"
    else
        # 兼容无 jq 环境：退回旧格式（仅 project_dir）
        echo "${project_dir}" > "$tmp_trigger"
    fi
    mv -f "$tmp_trigger" "$trigger_file"
    set_cooldown "$key"
    sync_project_status "$project_dir" "review_triggered" "window=${window}" "since_review=${count}" "state=idle"

    # 注意：commit 计数不在这里重置！由 cron 端确认 review 成功后重置
    # cron 需要: echo 0 > ${COMMIT_COUNT_DIR}/${safe}-since-review && now_ts > ${last_review_ts_file}

    log "🔍 ${window}: incremental review triggered (${count} commits, ${time_since_review}s since last review)"
}

# 信号驱动 nudge 消息
get_smart_nudge() {
    local safe="$1" project_dir="$2"

    # 先检查 PRD 是否全部完成 — 如果全完成了，不要强制写测试
    local prd_todo="${project_dir}/prd-todo.md"
    if [ -f "$prd_todo" ]; then
        local remaining
        remaining=$(grep '^- ' "$prd_todo" | grep -vic "$PRD_DONE_FILTER_RE" || true)
        remaining=$(normalize_int "$remaining")
        if [ "$remaining" -eq 0 ]; then
            # PRD 完成 → 检查是否有 review issues 或 autocheck issues 需要修
            local issues_file="${STATE_DIR}/autocheck-issues-${safe}"
            local prd_issues_file="${STATE_DIR}/prd-issues-${safe}"
            if [ -f "$issues_file" ]; then
                local pending_issues
                pending_issues=$(cat "$issues_file" | head -c 200)
                echo "PRD 已完成，但仍有自动检查发现的问题待修复：${pending_issues}"
                return
            fi
            if [ -f "$prd_issues_file" ]; then
                local pending_prd
                pending_prd=$(cat "$prd_issues_file" | head -c 200)
                echo "PRD 已完成，但 PRD checker 仍有失败项：${pending_prd}"
                return
            fi
            # 检查是否有未处理的 review 结果
            local review_file="${STATE_DIR}/layer2-review-${safe}.txt"
            if [ -f "$review_file" ]; then
                local review_content
                review_content=$(cat "$review_file" 2>/dev/null | head -c 200)
                if ! echo "$review_content" | grep -qi "CLEAN"; then
                    echo "PRD 已完成，但上次 review 发现问题需要修复。读 ${review_file} 并修复所有 P1/P2 问题，然后 git commit。"
                    return
                fi
            fi
            echo "PRD 和 review 均已完成。运行测试确认无回归，检查是否有遗漏的优化项。"
            return
        fi
    fi

    # 检查连续 feat commit 无 test
    local recent_msgs
    recent_msgs=$(git -C "$project_dir" log -10 --format="%s" 2>/dev/null)

    local consecutive_feat=0
    while IFS= read -r msg; do
        if echo "$msg" | grep -qE '^(feat|feature)'; then
            consecutive_feat=$((consecutive_feat + 1))
        elif echo "$msg" | grep -qE '^test'; then
            break  # 遇到 test commit 就停，计数归零
        else
            break  # 遇到非 feat/非 test commit 就停（fix/chore/docs 不算连续 feat）
        fi
    done <<< "$recent_msgs"

    if [ "$consecutive_feat" -ge "$FEAT_WITHOUT_TEST_LIMIT" ]; then
        echo "为最近完成的功能写单元测试，确保包含 happy path + error path，断言要验证行为不是实现。写完后继续推进下一项任务。"
        return
    fi

    # 检查连续 checkpoint/空 commit
    local checkpoint_count=0
    while IFS= read -r msg; do
        if echo "$msg" | grep -qiE 'checkpoint|wip|fixup|squash'; then
            checkpoint_count=$((checkpoint_count + 1))
        else
            break
        fi
    done <<< "$recent_msgs"

    if [ "$checkpoint_count" -ge 3 ]; then
        echo "看起来进展受阻了。描述一下当前遇到的困难，然后换个思路解决。"
        return
    fi

    # 检查测试是否失败
    if [ -f "${project_dir}/package.json" ]; then
        local test_status="${COMMIT_COUNT_DIR}/${safe}-test-fail"
        if [ -f "$test_status" ]; then
            rm -f "$test_status"
            echo "修复失败的测试，优先级高于新功能开发。"
            return
        fi
    fi

    # PRD 驱动 nudge：从 prd-todo.md 读取下一个待办
    if [ -f "$prd_todo" ]; then
        local next_task
        next_task=$(grep '^- ' "$prd_todo" | grep -vi "$PRD_DONE_FILTER_RE" | head -1 | sed 's/^- //')
        if [ -n "$next_task" ]; then
            echo "实现以下 PRD 需求：${next_task}"
            return
        fi
    fi

    # 默认：带最近 commit 上下文
    local last_msg
    last_msg=$(git -C "$project_dir" log -1 --format="%s" 2>/dev/null || echo "")
    if [ -n "$last_msg" ]; then
        echo "上一个 commit: '${last_msg:0:80}'。基于此继续推进，或开始下一个 PRD 待办。"
    else
        echo "继续推进下一项任务"
    fi
}

# ---- 主循环 ----
# ---- 进程级互斥锁 ----
WATCHDOG_PIDFILE="${LOCK_DIR}/watchdog.pid"
if [ -f "$WATCHDOG_PIDFILE" ]; then
    existing_pid=$(cat "$WATCHDOG_PIDFILE" 2>/dev/null || echo 0)
    existing_pid=$(normalize_int "$existing_pid")
    if [ "$existing_pid" -gt 0 ] && kill -0 "$existing_pid" 2>/dev/null; then
        echo "watchdog already running (pid ${existing_pid})"
        exit 0
    fi
    rm -f "$WATCHDOG_PIDFILE" 2>/dev/null || true
fi

WATCHDOG_LOCK="${LOCK_DIR}/watchdog-main.lock.d"
if ! mkdir "$WATCHDOG_LOCK" 2>/dev/null; then
    # 通过 PID + 进程启动签名识别锁持有者，避免 PID 复用误判
    existing_pid=$(cat "${WATCHDOG_LOCK}/pid" 2>/dev/null || echo 0)
    existing_pid=$(normalize_int "$existing_pid")
    existing_start_sig=$(cat "${WATCHDOG_LOCK}/start_sig" 2>/dev/null || echo "")
    if pid_is_same_process "$existing_pid" "$existing_start_sig"; then
        echo "Another watchdog is running (pid ${existing_pid}). Exiting."
        exit 1
    elif [ -z "$existing_start_sig" ] && [ "$existing_pid" -gt 0 ] && kill -0 "$existing_pid" 2>/dev/null && pid_looks_like_watchdog "$existing_pid"; then
        # 兼容旧锁格式（仅有 pid）
        echo "Another watchdog is running (pid ${existing_pid}, legacy lock). Exiting."
        exit 1
    else
        log "🔓 Stale lock found (pid ${existing_pid} dead), reclaiming"
        rm -rf "$WATCHDOG_LOCK" 2>/dev/null
        mkdir "$WATCHDOG_LOCK" 2>/dev/null || { echo "Failed to reclaim lock. Exiting."; exit 1; }
    fi
fi
echo $$ > "${WATCHDOG_LOCK}/pid"
pid_start_signature "$$" > "${WATCHDOG_LOCK}/start_sig" 2>/dev/null || true
now_ts > "${WATCHDOG_LOCK}/started_at"
echo $$ > "$WATCHDOG_PIDFILE"
# ERR trap 仅用于诊断；不要与 set -e 组合
trap 'log "💥 ERR at line $LINENO (code=$?)"' ERR
# Graceful shutdown: kill background jobs, clean lock
cleanup_watchdog() {
    local pids
    pids=$(jobs -p 2>/dev/null || true)
    if [ -n "$pids" ]; then
        kill $pids 2>/dev/null || true
        # Give children 2s to clean up their own locks
        sleep 2
        kill -9 $pids 2>/dev/null || true
    fi
    rm -rf "$WATCHDOG_LOCK"
    rm -f "$WATCHDOG_PIDFILE"
}
trap cleanup_watchdog EXIT
trap 'log "🛑 Received SIGTERM, shutting down..."; exit 0' TERM INT

assert_runtime_ready
load_projects
load_branch_isolation_config
load_test_agent_config
log "🌿 branch isolation: enabled=${BRANCH_ISOLATION_ENABLED}, auto_merge=${BRANCH_AUTO_MERGE_ENABLED}, require_auto_check=${BRANCH_REQUIRE_AUTO_CHECK}, require_tests=${BRANCH_REQUIRE_TESTS}, base=${BRANCH_BASE_BRANCH}"
log "🧪 test-agent: enabled=${TEST_AGENT_ENABLED}, trigger_review_clean=${TEST_AGENT_TRIGGER_REVIEW_CLEAN}, trigger_on_commit=${TEST_AGENT_TRIGGER_ON_COMMIT_EVALUATE}"
log "🚀 Watchdog v4 started (tick=${TICK}s, idle_threshold=${IDLE_THRESHOLD}s, idle_confirm=${IDLE_CONFIRM_PROBES}, inertia=${WORKING_INERTIA_SECONDS}s, projects=${#PROJECTS[@]}, pid=$$)"

cycle=0
while true; do
    for entry in "${PROJECTS[@]}"; do
        window="${entry%%:*}"
        project_dir="${entry#*:}"
        safe=$(sanitize "$window")

        state=$(detect_state "$window" "$safe")

        # 队列保护：进行中任务超时自动回收，避免 [→] 长期僵死
        recover_stale_queue_in_progress "$window" "$safe"

        # 每 30 轮（~5 分钟）记录一次状态
        if [ $((cycle % 30)) -eq 0 ] && [ "$cycle" -gt 0 ]; then
            log "📊 ${window}: state=${state}"
        fi

        # Layer 1: 检测新 commit 并自动检查
        check_new_commits "$window" "$safe" "$project_dir" "$state"

        # 手动 tmux-send 任务追踪：检测完成与超时（不影响 queue 逻辑）
        check_tracked_manual_task "$window" "$safe" "$project_dir" "$state"

        # review CLEAN 后触发 Test Agent 任务生成（异步，不阻塞主循环）
        maybe_trigger_test_agent_on_review_clean "$window" "$safe" "$project_dir" "$state"

        # 检测 prd-todo.md 变化（新需求加入）→ 重置 nudge 计数，重新激活
        if detect_prd_todo_changes "$safe" "$project_dir"; then
            new_remaining=$(count_prd_todo_remaining "$project_dir")
            if [ "$new_remaining" -gt 0 ]; then
                log "📋 ${window}: prd-todo.md updated, ${new_remaining} items remaining — resetting nudge"
                echo 0 > "${COOLDOWN_DIR}/nudge-count-${safe}"
                rm -f "${STATE_DIR}/prd-done-logged-${safe}" 2>/dev/null || true
                rm -f "$(nudge_pause_file "$safe")" "${STATE_DIR}/alert-stalled-${safe}"
                send_telegram_alert "$window" "prd-todo.md 有新需求 (${new_remaining} 项待完成)，已重新激活 nudge"
            fi
        fi

        # Fix 6: 非 working 状态清除僵死追踪
        if [ "$state" != "$CODEX_STATE_WORKING" ]; then
            rm -f "${STATE_DIR}/working-since-${safe}" "${STATE_DIR}/working-head-${safe}" "${STATE_DIR}/working-ctx-${safe}" "${STATE_DIR}/working-pane-${safe}" "${STATE_DIR}/stall-alerted-${safe}" 2>/dev/null || true
        fi

        case "$state" in
            "$CODEX_STATE_WORKING")
                update_activity "$safe"
                reset_idle_probe "$safe"
                # Fix 6: TUI 僵死检测
                stall_head=$(cat "${COMMIT_COUNT_DIR}/${safe}-head" 2>/dev/null || echo "none")
                stall_json=$(get_window_status_json "$window")
                stall_ctx=$(extract_context_num_field "$stall_json")
                working_since_f="${STATE_DIR}/working-since-${safe}"
                working_head_f="${STATE_DIR}/working-head-${safe}"
                working_ctx_f="${STATE_DIR}/working-ctx-${safe}"
                prev_stall_head=$(cat "$working_head_f" 2>/dev/null || echo "")
                prev_stall_ctx=$(cat "$working_ctx_f" 2>/dev/null || echo "")
                # Fix 6.1: 增加 pane 内容 hash 检测 — TUI 输出变化说明确实在工作
                working_pane_f="${STATE_DIR}/working-pane-${safe}"
                pane_content=$($TMUX capture-pane -t "${SESSION}:${window}" -p 2>/dev/null | tail -30)
                pane_hash=$(hash_text "$pane_content")
                prev_pane_hash=$(cat "$working_pane_f" 2>/dev/null || echo "")
                pane_changed=false
                if [ "$pane_hash" != "$prev_pane_hash" ]; then
                    pane_changed=true
                    echo "$pane_hash" > "$working_pane_f"
                fi
                if [ "$stall_head" != "$prev_stall_head" ] || [ "$stall_ctx" != "$prev_stall_ctx" ]; then
                    # HEAD 或 context 变化 → 重置追踪
                    now_ts > "$working_since_f"
                    echo "$stall_head" > "$working_head_f"
                    echo "$stall_ctx" > "$working_ctx_f"
                    rm -f "${STATE_DIR}/stall-alerted-${safe}"
                elif [ "$pane_changed" = true ]; then
                    # HEAD/context 没变，但 pane 内容有变化 → TUI 活着，重置计时
                    now_ts > "$working_since_f"
                    rm -f "${STATE_DIR}/stall-alerted-${safe}"
                else
                    # HEAD/context/pane 全都没变 → 可能真的僵死
                    working_since_val=$(cat "$working_since_f" 2>/dev/null || echo 0)
                    working_since_val=$(normalize_int "$working_since_val")
                    stall_dur=$(( $(now_ts) - working_since_val ))
                    if [ "$stall_dur" -ge 1800 ]; then
                        # 30 分钟 → Telegram 告警
                        if [ ! -f "${STATE_DIR}/stall-alerted-${safe}" ]; then
                            send_telegram_alert "$window" "TUI 可能僵死（working ${stall_dur}s 但 HEAD/context/pane输出 均无变化）"
                            touch "${STATE_DIR}/stall-alerted-${safe}"
                            log "🚨 ${window}: possible TUI stall (${stall_dur}s, HEAD=${stall_head:0:7}, ctx=${stall_ctx}%, pane unchanged)"
                        fi
                    elif [ "$stall_dur" -ge 900 ]; then
                        # 15 分钟 → 日志 warn
                        log "⚠️ ${window}: working ${stall_dur}s with no HEAD/context/pane change (HEAD=${stall_head:0:7}, ctx=${stall_ctx}%)"
                    fi
                fi
                ;;
            "$CODEX_STATE_PERMISSION"|"${CODEX_STATE_PERMISSION_WITH_REMEMBER}")
                reset_idle_probe "$safe"
                handle_permission "$window" "$safe"
                ;;
            "$CODEX_STATE_IDLE")
                if idle_state_confirmed "$safe" "$CODEX_STATE_IDLE"; then
                    handle_idle "$window" "$safe" "$project_dir"
                fi
                ;;
            "$CODEX_STATE_IDLE_LOW_CONTEXT")
                if idle_state_confirmed "$safe" "$CODEX_STATE_IDLE_LOW_CONTEXT"; then
                    handle_low_context "$window" "$safe" "$project_dir"
                fi
                ;;
            "$CODEX_STATE_SHELL")
                reset_idle_probe "$safe"
                handle_shell "$window" "$safe" "$project_dir"
                ;;
            "$CODEX_STATE_ABSENT")
                # tmux window 不存在，跳过
                reset_idle_probe "$safe"
                ;;
        esac
    done

    cycle=$((cycle + 1))
    # 每 300 轮（~50 分钟）轮转日志
    if [ $((cycle % 300)) -eq 0 ]; then
        rotate_log
    fi

    sleep "$TICK"
done
