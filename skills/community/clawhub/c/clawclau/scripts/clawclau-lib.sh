#!/usr/bin/env bash
# clawclau-lib.sh — 乌萨奇任务调度系统共享库
# 用法: source "$(dirname "${BASH_SOURCE[0]}")/clawclau-lib.sh"

# ── 路径配置 ───────────────────────────────────────────────────────────────
CC_HOME="${CC_HOME:-$HOME/.clawclau}"
CC_REGISTRY="$CC_HOME/active-tasks.json"
CC_LOG_DIR="$CC_HOME/logs"
CC_PROMPT_DIR="$CC_HOME/prompts"

# openclaw 工具链路径，提前导出确保所有函数均可调用 openclaw
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.openclaw/bin:$PATH"

# ── 初始化 ─────────────────────────────────────────────────────────────────
# @description 初始化日志目录、Prompt 目录和注册表文件
# @returns 无
# @example cc_init
cc_init() {
    mkdir -p "$CC_LOG_DIR" "$CC_PROMPT_DIR"
    [[ -f "$CC_REGISTRY" ]] || echo '[]' > "$CC_REGISTRY"
}

# ── 依赖检查 ───────────────────────────────────────────────────────────────
# @description 检查所有必要命令是否已安装，缺失则输出错误并退出
# @param $@ 要检查的命令名称（可多个）
# @returns 无（缺失命令时 exit 1）
# @example cc_require tmux jq claude
cc_require() {
    for cmd in "$@"; do
        command -v "$cmd" >/dev/null 2>&1 || {
            echo "ERROR: '$cmd' 未安装，请先安装。" >&2
            exit 1
        }
    done
}

# ── 注册表操作 ─────────────────────────────────────────────────────────────

# @description 从注册表读取指定任务的字段值
# @param $1 id    任务 ID
# @param $2 field 字段名称
# @returns 字段值字符串；字段不存在时输出空字符串
# @example cc_task_get my-task status
cc_task_get() {
    local id="$1" field="$2"
    jq -r --arg id "$id" --arg f "$field" \
        '.[] | select(.id == $id) | .[$f] // ""' \
        "$CC_REGISTRY" 2>/dev/null
}

# @description 检查任务是否已存在于注册表
# @param $1 id 任务 ID
# @returns 0=存在，1=不存在
# @example cc_task_exists my-task && echo "已注册"
cc_task_exists() {
    local id="$1"
    local count
    count=$(jq --arg id "$id" '[.[] | select(.id == $id)] | length' "$CC_REGISTRY" 2>/dev/null || echo 0)
    [[ "$count" -gt 0 ]]
}

# @description 向注册表追加一个新任务
# @param $1 task_json 合法的 JSON 对象字符串（由调用方通过 jq -n 构造）
# @returns 0=成功，1=JSON 格式无效
# @example cc_task_register '{"id":"my-task","status":"running"}'
cc_task_register() {
    local task_json="$1"
    if ! jq -e . <<< "$task_json" >/dev/null 2>&1; then
        echo "ERROR: cc_task_register 收到无效 JSON" >&2
        return 1
    fi
    jq --argjson t "$task_json" '. += [$t]' \
        "$CC_REGISTRY" > "$CC_REGISTRY.tmp" \
        && mv "$CC_REGISTRY.tmp" "$CC_REGISTRY"
}

# @description 用 JSON 补丁更新注册表中指定任务的字段
# @param $1 id    任务 ID
# @param $2 patch 合法的 JSON 对象补丁（如 '{"status":"done"}'）
# @returns 0=成功，1=JSON 格式无效
# @example cc_task_update my-task '{"status":"done","completedAt":1700000000000}'
cc_task_update() {
    local id="$1" patch="$2"
    if ! jq -e . <<< "$patch" >/dev/null 2>&1; then
        echo "ERROR: cc_task_update 收到无效 JSON patch" >&2
        return 1
    fi
    jq --arg id "$id" --argjson p "$patch" \
        '(.[] | select(.id == $id)) |= . + $p' \
        "$CC_REGISTRY" > "$CC_REGISTRY.tmp" \
        && mv "$CC_REGISTRY.tmp" "$CC_REGISTRY"
}

# @description 向任务的 steerLog 数组追加一条引导记录
# @param $1 id      任务 ID
# @param $2 message 记录内容（任意文本，jq --arg 自动转义，无注入风险）
# @returns 无
# @example cc_task_steer_log my-task "调整方向：专注登录模块"
cc_task_steer_log() {
    local id="$1" message="$2"
    local ts
    ts=$(date +%s000)
    jq --arg id "$id" --arg msg "$message" --argjson ts "$ts" \
        '(.[] | select(.id == $id)) |= . + {steerLog: ((.steerLog // []) + [{at: $ts, message: $msg}])}' \
        "$CC_REGISTRY" > "$CC_REGISTRY.tmp" \
        && mv "$CC_REGISTRY.tmp" "$CC_REGISTRY"
}

# ── tmux 助手 ──────────────────────────────────────────────────────────────

# @description 根据任务 ID 生成规范的 tmux session 名称
# @param $1 id 任务 ID
# @returns "cc-<id>" 格式的 session 名
# @example cc_tmux_session my-task  # → "cc-my-task"
cc_tmux_session() {
    echo "cc-${1}"
}

# @deprecated 请直接使用 `tmux has-session -t "$(cc_tmux_session <id>)"` 代替
# @description 检查任务对应的 tmux session 是否存活
# @param $1 id 任务 ID
# @returns 0=session 存活，非0=不存在
cc_tmux_alive() {
    tmux has-session -t "$(cc_tmux_session "$1")" 2>/dev/null
}

# ── 日志文本提取 ───────────────────────────────────────────────────────────

# @description 从 stream-json 日志或纯文本日志中提取可读文本摘要
# @param $1 log_file  日志文件路径
# @param $2 max_chars 最大字符数（默认: 500）
# @returns 提取到的文本摘要；文件不存在或为空时输出空字符串
# @example cc_extract_text ~/.clawclau/logs/my-task.json 300
cc_extract_text() {
    local log_file="$1"
    local max_chars="${2:-500}"

    [[ -f "$log_file" ]] || { echo ""; return; }
    [[ -s "$log_file" ]] || { echo ""; return; }

    # 检测格式：stream-json 以 '{' 开头
    local first_char
    first_char=$(head -c1 "$log_file" 2>/dev/null)

    if [[ "$first_char" == "{" ]]; then
        # Claude stream-json 格式
        # 优先级：result > assistant message > text_delta 片段
        # 使用逐行 fromjson 容忍截断/非 JSON 行
        local text
        text=$(jq -Rs '
          [split("\n")[] | select(length > 0) | (try fromjson catch null) | select(. != null)] |
          ([ .[] | select(.type == "result") | (.result // "") ] | last // "") as $result |
          ([ .[] | select(.type == "assistant") |
             ((.message.content // []) | map(select(.type == "text") | .text) | join(""))
          ] | last // "") as $assistant |
          ([ .[] |
             select(.type == "stream_event") |
             select(.event.type == "content_block_delta") |
             select(.event.delta.type == "text_delta") |
             .event.delta.text
          ] | join("")) as $delta |
          if $result != "" then $result
          elif $assistant != "" then $assistant
          elif $delta != "" then $delta
          else ""
          end
        ' "$log_file" 2>/dev/null)
        if [[ "${#text}" -le "$max_chars" ]]; then
            echo "$text"
        else
            echo "${text: -$max_chars}"
        fi
    else
        # 纯文本（steerable 模式），剥离 ANSI 转义码
        tail -200 "$log_file" 2>/dev/null \
            | perl -pe 's/\x1b\[[0-9;]*[mGKHF]//g' \
            | tr -d '\r' \
            | grep -v '^$' \
            | tail -c "$max_chars"
    fi
}

# ── 通知 ───────────────────────────────────────────────────────────────────

# @description 发送通知；优先飞书群（CC_NOTIFY_CHAT 环境变量或 config 的 notify_chat），
#              回退到 openclaw system event
# @param $1 text 通知文本内容
# @returns 无（静默失败）
# @example cc_notify "任务 my-task 已完成"
cc_notify() {
    local text="$1"
    local chat="${CC_NOTIFY_CHAT:-}"
    # 如果没设环境变量，从配置文件读默认值
    if [[ -z "$chat" && -f "$CC_HOME/config" ]]; then
        chat=$(awk -F'[:=]' '/notify_chat/{gsub(/[ \t"]/,"",$2); print $2}' "$CC_HOME/config" 2>/dev/null || true)
    fi
    if [[ -n "$chat" ]]; then
        openclaw message send --channel feishu --target "$chat" \
            --message "$text" 2>/dev/null || true
    else
        openclaw system event --text "$text" --mode now 2>/dev/null || true
    fi
}

# ── 时间助手 ───────────────────────────────────────────────────────────────

# @description 返回当前时间的毫秒级 Unix 时间戳
# @returns 13 位毫秒时间戳字符串（如 "1700000000000"）
# @example ts=$(cc_now_ms)
cc_now_ms() { date +%s000; }

# @description 将毫秒级起始时间戳转换为人类可读的经过时长
# @param $1 start_ms 开始时刻的毫秒时间戳
# @returns "N秒" 或 "N分钟" 格式的字符串
# @example cc_elapsed_human "$START_MS"  # → "3分钟"
cc_elapsed_human() {
    local start_ms="$1"
    local now_ms
    now_ms=$(cc_now_ms)
    local elapsed=$(( (now_ms - start_ms) / 1000 ))
    if [[ $elapsed -lt 60 ]]; then
        echo "${elapsed}秒"
    else
        echo "$((elapsed / 60))分钟"
    fi
}

# ── 验证 ───────────────────────────────────────────────────────────────────

# @description 验证任务 ID 格式合法性，非法时打印错误并退出
# @param $1 id 待验证的任务 ID（仅允许 a-z/A-Z/0-9/-/_）
# @returns 无（非法时 exit 1）
# @example cc_validate_task_id "my-task-01"
cc_validate_task_id() {
    local id="$1"
    if ! [[ "$id" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "ERROR: task-id 只能包含 a-z/A-Z/0-9/-/_，收到: '$id'" >&2
        exit 1
    fi
}
