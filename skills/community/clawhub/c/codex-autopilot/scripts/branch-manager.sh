#!/bin/bash
# branch-manager.sh — Branch 隔离模式管理器（Phase 1）
# 用法:
#   branch-manager.sh ensure <project_dir> <safe> <task_type> <base_branch>
#   branch-manager.sh mark-ready <project_dir> <safe> <branch> [reason]
#   branch-manager.sh auto-merge <project_dir> <safe> <branch> <base_branch>
#   branch-manager.sh cleanup <project_dir> <safe>
#
# 设计约束：
# - 仅操作 ap/ 前缀分支（可通过 config.yaml branch_isolation.naming.prefix 覆盖）
# - 状态文件原子写入（.tmp + mv）
# - set -euo pipefail，失败快速返回

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=autopilot-lib.sh
source "${SCRIPT_DIR}/autopilot-lib.sh"
if [ -f "${SCRIPT_DIR}/autopilot-constants.sh" ]; then
    # shellcheck disable=SC1091
    source "${SCRIPT_DIR}/autopilot-constants.sh"
fi

STATE_DIR="${STATE_DIR:-$HOME/.autopilot/state}"
BRANCH_STATE_DIR="${STATE_DIR}/branches"
CONFIG_FILE="${AUTOPILOT_CONFIG_FILE:-$HOME/.autopilot/config.yaml}"
mkdir -p "$BRANCH_STATE_DIR"

log_err() {
    echo "[branch-manager $(date '+%H:%M:%S')] $*" >&2
}

yaml_trim() {
    local v="${1:-}"
    v="${v%%#*}"
    v="$(echo "$v" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
    v="$(echo "$v" | sed 's/^"//; s/"$//; s/^'\''//; s/'\''$//')"
    echo "$v"
}

get_branch_block_value() {
    local key="$1" default_val="${2:-}"
    [ -f "$CONFIG_FILE" ] || { echo "$default_val"; return 0; }
    awk -v key="$key" -v def="$default_val" '
    function ltrim(s) { sub(/^[[:space:]]+/, "", s); return s }
    function rtrim(s) { sub(/[[:space:]]+$/, "", s); return s }
    function trim(s) { return rtrim(ltrim(s)) }
    function strip(s) {
        s = trim(s)
        sub(/[[:space:]]*#.*/, "", s)
        s = trim(s)
        if (s ~ /^".*"$/) return substr(s, 2, length(s) - 2)
        if (s ~ /^'\''.*'\''$/) return substr(s, 2, length(s) - 2)
        return s
    }
    BEGIN { in_branch = 0; branch_indent = -1; printed = 0 }
    {
        line = $0
        sub(/\r$/, "", line)
        match(line, /^[[:space:]]*/)
        indent = RLENGTH
        content = trim(substr(line, indent + 1))
        if (content == "" || content ~ /^#/) next

        if (in_branch == 0) {
            if (content ~ /^branch_isolation:[[:space:]]*($|#)/) {
                in_branch = 1
                branch_indent = indent
            }
            next
        }

        if (indent <= branch_indent) {
            in_branch = 0
            next
        }

        if (content ~ ("^" key ":[[:space:]]*")) {
            sub(("^" key ":[[:space:]]*"), "", content)
            print strip(content)
            printed = 1
            exit
        }
    }
    END {
        if (printed == 0) print def
    }
    ' "$CONFIG_FILE"
}

get_nested_branch_value() {
    local parent="$1" key="$2" default_val="${3:-}"
    [ -f "$CONFIG_FILE" ] || { echo "$default_val"; return 0; }
    awk -v parent="$parent" -v key="$key" -v def="$default_val" '
    function ltrim(s) { sub(/^[[:space:]]+/, "", s); return s }
    function rtrim(s) { sub(/[[:space:]]+$/, "", s); return s }
    function trim(s) { return rtrim(ltrim(s)) }
    function strip(s) {
        s = trim(s)
        sub(/[[:space:]]*#.*/, "", s)
        s = trim(s)
        if (s ~ /^".*"$/) return substr(s, 2, length(s) - 2)
        if (s ~ /^'\''.*'\''$/) return substr(s, 2, length(s) - 2)
        return s
    }
    BEGIN { in_branch = 0; in_parent = 0; branch_indent = -1; parent_indent = -1; printed = 0 }
    {
        line = $0
        sub(/\r$/, "", line)
        match(line, /^[[:space:]]*/)
        indent = RLENGTH
        content = trim(substr(line, indent + 1))
        if (content == "" || content ~ /^#/) next

        if (in_branch == 0) {
            if (content ~ /^branch_isolation:[[:space:]]*($|#)/) {
                in_branch = 1
                branch_indent = indent
            }
            next
        }

        if (indent <= branch_indent) {
            in_branch = 0
            in_parent = 0
            next
        }

        if (in_parent == 0) {
            if (content ~ ("^" parent ":[[:space:]]*($|#)")) {
                in_parent = 1
                parent_indent = indent
            }
            next
        }

        if (indent <= parent_indent) {
            in_parent = 0
            next
        }

        if (content ~ ("^" key ":[[:space:]]*")) {
            sub(("^" key ":[[:space:]]*"), "", content)
            print strip(content)
            printed = 1
            exit
        }
    }
    END {
        if (printed == 0) print def
    }
    ' "$CONFIG_FILE"
}

normalize_bool_text() {
    local raw
    raw=$(echo "${1:-}" | tr '[:upper:]' '[:lower:]')
    case "$raw" in
        1|true|yes|on) echo "true" ;;
        *) echo "false" ;;
    esac
}

branch_prefix() {
    local prefix
    prefix=$(get_nested_branch_value "naming" "prefix" "ap")
    prefix=$(sanitize "$prefix")
    # 安全约束：只允许 ap 前缀，避免误删/误合并业务分支。
    if [ "$prefix" != "ap" ]; then
        prefix="ap"
    fi
    echo "$prefix"
}

state_file_for_safe() {
    local safe="$1"
    echo "${BRANCH_STATE_DIR}/${safe}.json"
}

atomic_write_state() {
    local safe="$1" project_dir="$2" branch="$3" base_branch="$4" task_type="$5" state="$6" created="$7" stashed="$8" reason="$9"
    local state_file tmp_file now_val
    state_file=$(state_file_for_safe "$safe")
    tmp_file="${state_file}.tmp.$$"
    now_val=$(now_ts)

    jq -n \
        --arg safe "$safe" \
        --arg project_dir "$project_dir" \
        --arg active_branch "$branch" \
        --arg base_branch "$base_branch" \
        --arg task_type "$task_type" \
        --arg state "$state" \
        --arg reason "$reason" \
        --arg created "$created" \
        --arg stashed "$stashed" \
        --argjson now "$now_val" \
        '{
            safe: $safe,
            project_dir: $project_dir,
            active_branch: $active_branch,
            base_branch: $base_branch,
            task_type: $task_type,
            state: $state,
            reason: $reason,
            created: ($created == "true"),
            stashed: ($stashed == "true"),
            updated_at: $now
        } + (if $state == "in_progress" then {started_at: $now} else {} end)' > "$tmp_file"
    mv -f "$tmp_file" "$state_file"
}

update_state_fields() {
    local safe="$1"
    shift || true
    local state_file tmp_file
    state_file=$(state_file_for_safe "$safe")
    tmp_file="${state_file}.tmp.$$"

    if [ ! -f "$state_file" ] || ! jq -e . "$state_file" >/dev/null 2>&1; then
        jq -n '{}' > "$state_file"
    fi

    jq "$@" "$state_file" > "$tmp_file"
    mv -f "$tmp_file" "$state_file"
}

assert_git_repo() {
    local project_dir="$1"
    [ -d "$project_dir" ] || { log_err "project_dir 不存在: $project_dir"; return 1; }
    git -C "$project_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
        log_err "不是 git 仓库: $project_dir"
        return 1
    }
}

resolve_base_branch() {
    local project_dir="$1" requested="$2"
    local candidate="$requested"
    if [ -z "$candidate" ]; then
        candidate=$(get_branch_block_value "base_branch" "main")
    fi
    candidate=$(yaml_trim "$candidate")
    [ -n "$candidate" ] || candidate="main"

    if git -C "$project_dir" show-ref --verify --quiet "refs/heads/${candidate}"; then
        echo "$candidate"
        return 0
    fi
    if git -C "$project_dir" show-ref --verify --quiet "refs/remotes/origin/${candidate}"; then
        git -C "$project_dir" checkout -q -B "$candidate" "origin/${candidate}"
        echo "$candidate"
        return 0
    fi

    for fallback in main master; do
        if git -C "$project_dir" show-ref --verify --quiet "refs/heads/${fallback}"; then
            echo "$fallback"
            return 0
        fi
    done

    git -C "$project_dir" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main"
}

build_branch_name() {
    local project_dir="$1" prefix="$2" safe="$3" task_type="$4"
    local ts base_name candidate suffix=2
    ts=$(date '+%Y%m%d-%H%M%S')
    base_name="${prefix}/${safe}/${task_type}/${ts}"
    candidate="$base_name"

    while git -C "$project_dir" show-ref --verify --quiet "refs/heads/${candidate}"; do
        candidate="${base_name}-${suffix}"
        suffix=$((suffix + 1))
    done
    echo "$candidate"
}

branch_allowed() {
    local branch="$1" prefix="$2"
    [[ "$branch" == "${prefix}/"* ]]
}

branch_manager_ensure() {
    local project_dir="$1" safe="$2" task_type="${3:-task}" base_branch="${4:-}"
    assert_git_repo "$project_dir"

    safe=$(sanitize "$safe")
    [ -n "$safe" ] || safe="project"
    task_type=$(sanitize "$task_type")
    [ -n "$task_type" ] || task_type="task"

    local prefix state_file existing_branch existing_state
    prefix=$(branch_prefix)
    state_file=$(state_file_for_safe "$safe")

    local created="false" stashed="false"
    base_branch=$(resolve_base_branch "$project_dir" "$base_branch")

    # 已有进行中的任务分支，直接复用，避免重复分支泛滥。
    if [ -f "$state_file" ] && jq -e . "$state_file" >/dev/null 2>&1; then
        existing_branch=$(jq -r '.active_branch // ""' "$state_file" 2>/dev/null || echo "")
        existing_state=$(jq -r '.state // ""' "$state_file" 2>/dev/null || echo "")
        if [ -n "$existing_branch" ] \
            && branch_allowed "$existing_branch" "$prefix" \
            && [[ "$existing_state" =~ ^(created|in_progress|ready_merge)$ ]] \
            && git -C "$project_dir" show-ref --verify --quiet "refs/heads/${existing_branch}"; then
            git -C "$project_dir" checkout -q "$existing_branch"
            update_state_fields "$safe" \
                --arg now "$(now_ts)" \
                --arg base "$base_branch" \
                '.state="in_progress" | .base_branch=$base | .updated_at=($now|tonumber)'
            jq -n --arg branch "$existing_branch" --arg base "$base_branch" '{"branch":$branch,"base":$base,"created":false}'
            return 0
        fi
    fi

    local dirty current_branch
    dirty=$(git -C "$project_dir" status --porcelain 2>/dev/null || true)
    if [ -n "$dirty" ]; then
        # 工作树不干净时 fail-fast，不隐式 stash（避免丢失用户改动）
        log_err "工作树不干净，拒绝创建分支（请先 commit 或 stash）: $project_dir"
        jq -n --arg error "dirty_worktree" '{"error":$error}'
        return 3
    fi

    current_branch=$(git -C "$project_dir" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
    if [ "$current_branch" != "$base_branch" ]; then
        git -C "$project_dir" checkout -q "$base_branch"
    fi

    local branch_name
    branch_name=$(build_branch_name "$project_dir" "$prefix" "$safe" "$task_type")
    git -C "$project_dir" checkout -q -b "$branch_name"
    created="true"

    atomic_write_state "$safe" "$project_dir" "$branch_name" "$base_branch" "$task_type" "in_progress" "$created" "$stashed" ""
    jq -n --arg branch "$branch_name" --arg base "$base_branch" '{"branch":$branch,"base":$base,"created":true}'
}

branch_manager_mark_ready() {
    local project_dir="$1" safe="$2" branch="${3:-}" reason="${4:-manual-ready}"
    assert_git_repo "$project_dir"
    safe=$(sanitize "$safe")
    [ -n "$safe" ] || safe="project"

    local prefix
    prefix=$(branch_prefix)
    if [ -z "$branch" ]; then
        branch=$(jq -r '.active_branch // ""' "$(state_file_for_safe "$safe")" 2>/dev/null || echo "")
    fi
    [ -n "$branch" ] || { log_err "mark-ready 缺少 branch"; return 1; }
    branch_allowed "$branch" "$prefix" || { log_err "拒绝操作非 ${prefix}/ 前缀分支: $branch"; return 1; }

    update_state_fields "$safe" \
        --arg branch "$branch" \
        --arg reason "$reason" \
        --argjson now "$(now_ts)" \
        '.active_branch=$branch | .state="ready_merge" | .reason=$reason | .updated_at=$now'

    jq -n --arg branch "$branch" '{"status":"ready_merge","branch":$branch}'
}

branch_manager_auto_merge() {
    local project_dir="$1" safe="$2" branch="$3" base_branch="${4:-}"
    assert_git_repo "$project_dir"
    safe=$(sanitize "$safe")
    [ -n "$safe" ] || safe="project"
    [ -n "$branch" ] || { log_err "auto-merge 缺少 branch"; return 1; }

    local prefix
    prefix=$(branch_prefix)
    branch_allowed "$branch" "$prefix" || { log_err "拒绝操作非 ${prefix}/ 前缀分支: $branch"; return 1; }

    base_branch=$(resolve_base_branch "$project_dir" "$base_branch")
    if ! git -C "$project_dir" show-ref --verify --quiet "refs/heads/${branch}"; then
        log_err "分支不存在: $branch"
        update_state_fields "$safe" --argjson now "$(now_ts)" '.state="failed" | .reason="branch_missing" | .updated_at=$now'
        jq -n --arg status "failed" --arg reason "branch_missing" --arg branch "$branch" '{"status":$status,"reason":$reason,"branch":$branch}'
        return 1
    fi

    git -C "$project_dir" checkout -q "$branch"

    # 最多 1 次 rebase 尝试，失败直接 conflict。
    if ! git -C "$project_dir" rebase "$base_branch" >/dev/null 2>&1; then
        git -C "$project_dir" rebase --abort >/dev/null 2>&1 || true
        update_state_fields "$safe" --argjson now "$(now_ts)" '.state="conflict" | .reason="rebase_conflict" | .updated_at=$now'
        jq -n --arg status "conflict" --arg reason "rebase_conflict" --arg branch "$branch" --arg base "$base_branch" '{"status":$status,"reason":$reason,"branch":$branch,"base":$base}'
        return 2
    fi

    git -C "$project_dir" checkout -q "$base_branch"
    if ! git -C "$project_dir" merge --squash "$branch" >/dev/null 2>&1; then
        # squash merge 不写 MERGE_HEAD，merge --abort 无效，用 reset --hard 回滚
        git -C "$project_dir" reset --hard HEAD >/dev/null 2>&1 || true
        update_state_fields "$safe" --argjson now "$(now_ts)" '.state="conflict" | .reason="merge_conflict" | .updated_at=$now'
        jq -n --arg status "conflict" --arg reason "merge_conflict" --arg branch "$branch" --arg base "$base_branch" '{"status":$status,"reason":$reason,"branch":$branch,"base":$base}'
        return 2
    fi

    # squash 后无 staged 变化，视作已合并（例如 base 已包含同样改动）。
    if ! git -C "$project_dir" diff --cached --quiet; then
        git -C "$project_dir" commit -m "merge(${safe}): ${branch}" >/dev/null 2>&1 || {
            update_state_fields "$safe" --argjson now "$(now_ts)" '.state="failed" | .reason="commit_failed" | .updated_at=$now'
            jq -n --arg status "failed" --arg reason "commit_failed" --arg branch "$branch" '{"status":$status,"reason":$reason,"branch":$branch}'
            return 1
        }
    fi

    if branch_allowed "$branch" "$prefix"; then
        git -C "$project_dir" branch -D "$branch" >/dev/null 2>&1 || true
    fi

    local head
    head=$(git -C "$project_dir" rev-parse --short HEAD 2>/dev/null || echo "")
    update_state_fields "$safe" \
        --arg base "$base_branch" \
        --arg head "$head" \
        --argjson now "$(now_ts)" \
        '.state="merged" | .reason="auto_merge_success" | .active_branch="" | .base_branch=$base | .merged_head=$head | .updated_at=$now'
    jq -n --arg status "merged" --arg branch "$branch" --arg base "$base_branch" --arg head "$head" '{"status":$status,"branch":$branch,"base":$base,"head":$head}'
}

branch_manager_cleanup() {
    local project_dir="$1" safe="$2"
    assert_git_repo "$project_dir"
    safe=$(sanitize "$safe")
    [ -n "$safe" ] || safe="project"

    local prefix state_file state active_branch updated_at now_val age keep_failed ttl
    prefix=$(branch_prefix)
    state_file=$(state_file_for_safe "$safe")
    [ -f "$state_file" ] || { jq -n '{"status":"clean","cleaned":false}'; return 0; }

    state=$(jq -r '.state // ""' "$state_file" 2>/dev/null || echo "")
    active_branch=$(jq -r '.active_branch // ""' "$state_file" 2>/dev/null || echo "")
    updated_at=$(jq -r '.updated_at // 0' "$state_file" 2>/dev/null || echo 0)
    updated_at=$(normalize_int "$updated_at")
    if [ "$updated_at" -le 0 ]; then
        updated_at=$(file_mtime "$state_file")
        updated_at=$(normalize_int "$updated_at")
    fi
    now_val=$(now_ts)
    age=$((now_val - updated_at))
    [ "$age" -ge 0 ] || age=0

    ttl=$(get_nested_branch_value "cleanup" "ttl_hours" "72")
    keep_failed=$(get_nested_branch_value "cleanup" "keep_failed_hours" "168")
    ttl=$(normalize_int "$ttl")
    keep_failed=$(normalize_int "$keep_failed")
    [ "$ttl" -gt 0 ] || ttl=72
    [ "$keep_failed" -gt 0 ] || keep_failed=168

    local should_cleanup="false" reason=""
    case "$state" in
        merged)
            should_cleanup="true"
            reason="merged"
            ;;
        failed|conflict)
            if [ "$age" -ge $((keep_failed * 3600)) ]; then
                should_cleanup="true"
                reason="failed_expired"
            fi
            ;;
        abandoned)
            if [ "$age" -ge $((ttl * 3600)) ]; then
                should_cleanup="true"
                reason="abandoned_expired"
            fi
            ;;
    esac

    if [ "$should_cleanup" != "true" ]; then
        jq -n --arg status "kept" --arg state "$state" '{"status":$status,"state":$state,"cleaned":false}'
        return 0
    fi

    if [ -n "$active_branch" ] && branch_allowed "$active_branch" "$prefix"; then
        git -C "$project_dir" branch -D "$active_branch" >/dev/null 2>&1 || true
    fi
    rm -f "$state_file" 2>/dev/null || true
    jq -n --arg status "cleaned" --arg reason "$reason" --arg branch "$active_branch" '{"status":$status,"reason":$reason,"branch":$branch,"cleaned":true}'
}

usage() {
    cat <<'EOF'
用法:
  branch-manager.sh ensure <project_dir> <safe> <task_type> <base_branch>
  branch-manager.sh mark-ready <project_dir> <safe> <branch> [reason]
  branch-manager.sh auto-merge <project_dir> <safe> <branch> <base_branch>
  branch-manager.sh cleanup <project_dir> <safe>
EOF
}

cmd="${1:-}"
shift || true

case "$cmd" in
    ensure)
        branch_manager_ensure "$@"
        ;;
    mark-ready)
        branch_manager_mark_ready "$@"
        ;;
    auto-merge)
        branch_manager_auto_merge "$@"
        ;;
    cleanup)
        branch_manager_cleanup "$@"
        ;;
    *)
        usage
        exit 1
        ;;
esac
