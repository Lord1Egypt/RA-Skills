#!/usr/bin/env bash
# cron-edit-safe.sh - 安全编辑 cron 任务（备份 + dry-run + edit + 验证 + rollback）
# 作者: 码虫 🐛 (v1.0.0 - 2026-06-28)
# 用途: 包装 openclaw cron edit，自动处理 Refine 揪出的 3 个真问题
#       1. 缺备份机制 → 自动备份原 JSON
#       2. 缺 dry-run → edit 前先验证命令可跑通
#       3. 缺 rollback → 失败时自动恢复
#
# 用法:
#   cron-edit-safe.sh <cron-id> [options]
#
# 示例:
#   cron-edit-safe.sh d21a3540-... \
#     --name "Foo" \
#     --command "python3 /path/to/script.py" \
#     --command-cwd "/path/to/workdir" \
#     --session isolated
#
# 控制选项:
#   --no-backup       跳过备份（默认开启）
#   --no-dry-run      跳过 dry-run（默认开启）
#   --no-rollback     失败时不自动 rollback（默认开启）
#   --dry-run-only    只跑 dry-run，不 edit
#   --backup-dir DIR  自定义备份目录
#   --quiet           减少输出

set -euo pipefail

# ─── 全局变量 ───────────────────────────────────────────
SCRIPT_NAME="$(basename "$0")"
BACKUP_DIR_DEFAULT="$HOME/.openclaw/backups/cron-$(date +%Y%m%d)"
BACKUP_DIR="$BACKUP_DIR_DEFAULT"
DO_BACKUP=1
DO_DRY_RUN=1
DO_ROLLBACK=1
DRY_RUN_ONLY=0
QUIET=0
CRON_ID=""
EDIT_ARGS=()  # 透传给 openclaw cron edit 的参数

# ─── 工具函数 ───────────────────────────────────────────
log() { [[ $QUIET -eq 0 ]] && echo -e "$@"; }
err() { echo -e "❌ $*" >&2; }
ok()  { log "✅ $*"; }
warn() { log "⚠️  $*"; }

usage() {
  cat <<EOF
Usage: $SCRIPT_NAME <cron-id> [options]

Options:
  --name <string>
  --description <string>
  --command <shell>
  --command-argv <json>
  --command-cwd <path>
  --session <main|isolated>
  --announce
  --channel <id>
  --to <dest>
  --failure-alert-after <n>
  --failure-alert-channel <id>
  --failure-alert-to <dest>
  --failure-alert-cooldown <duration>

Control:
  --no-backup       跳过备份（默认开启）
  --no-dry-run      跳过 dry-run（默认开启）
  --no-rollback     失败时不自动 rollback（默认开启）
  --dry-run-only    只跑 dry-run，不 edit
  --backup-dir DIR  自定义备份目录
  --quiet           减少输出
  -h, --help        显示帮助

Example:
  $SCRIPT_NAME d21a3540-... --name "Foo [v2.0 command]" \\
    --command "python3 /path/script.py" \\
    --command-cwd "/path" --session isolated
EOF
  exit 0
}

# ─── 参数解析 ───────────────────────────────────────────
if [[ $# -lt 1 ]]; then usage; fi

CRON_ID="$1"
shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-backup)     DO_BACKUP=0; shift ;;
    --no-dry-run)    DO_DRY_RUN=0; shift ;;
    --no-rollback)   DO_ROLLBACK=0; shift ;;
    --dry-run-only)  DRY_RUN_ONLY=1; shift ;;
    --backup-dir)    BACKUP_DIR="$2"; shift 2 ;;
    --quiet|-q)      QUIET=1; shift ;;
    -h|--help)       usage ;;
    *)
      EDIT_ARGS+=("$1")
      shift
      ;;
  esac
done

# ─── 前置检查 ───────────────────────────────────────────
command -v jq >/dev/null 2>&1 || { err "jq 未安装，请先: sudo apt install jq"; exit 1; }
command -v openclaw >/dev/null 2>&1 || { err "openclaw 未安装"; exit 1; }

# 校验 cron-id 存在
if ! openclaw cron get "$CRON_ID" >/dev/null 2>&1; then
  err "Cron 任务不存在: $CRON_ID"
  exit 1
fi

# ─── Step 1: BACKUP ─────────────────────────────────────
BACKUP_FILE=""
if [[ $DO_BACKUP -eq 1 ]]; then
  log ""
  log "📦 Step 1/5: BACKUP"
  mkdir -p "$BACKUP_DIR"
  BACKUP_FILE="$BACKUP_DIR/${CRON_ID}.bak.json"
  if openclaw cron get "$CRON_ID" > "$BACKUP_FILE" 2>/dev/null; then
    local_size=$(wc -c < "$BACKUP_FILE")
    if [[ $local_size -lt 100 ]]; then
      err "Backup 文件过小 ($local_size bytes)，疑似空文件"
      exit 1
    fi
    ok "Backup OK: $BACKUP_FILE ($local_size bytes)"
  else
    err "Backup 失败: 无法 export cron JSON"
    exit 1
  fi
fi

# ─── Step 2: DRY-RUN ────────────────────────────────────
DRY_RUN_CMD=""
DRY_RUN_CWD=""
if [[ $DO_DRY_RUN -eq 1 ]]; then
  log ""
  log "🧪 Step 2/5: DRY-RUN"

  # 提取 --command 参数
  for ((i=0; i<${#EDIT_ARGS[@]}; i++)); do
    if [[ "${EDIT_ARGS[$i]}" == "--command" ]]; then
      DRY_RUN_CMD="${EDIT_ARGS[$((i+1))]:-}"
    fi
    if [[ "${EDIT_ARGS[$i]}" == "--command-cwd" ]]; then
      DRY_RUN_CWD="${EDIT_ARGS[$((i+1))]:-}"
    fi
  done

  if [[ -z "$DRY_RUN_CMD" ]]; then
    warn "未指定 --command，跳过 dry-run"
  else
    warn "dry-run 副作用：可能发飞书 / 写文件 / 调外部 API"
    warn "执行命令: $DRY_RUN_CMD"
    if [[ -n "$DRY_RUN_CWD" ]]; then
      warn "cwd: $DRY_RUN_CWD"
    fi

    # 真正跑一次（带 timeout 60s）
    if [[ -n "$DRY_RUN_CWD" ]]; then
      (cd "$DRY_RUN_CWD" && timeout 60 bash -c "$DRY_RUN_CMD") >/tmp/cron-dry-run.out 2>&1 && DRY_RUN_OK=1 || DRY_RUN_OK=0
    else
      timeout 60 bash -c "$DRY_RUN_CMD" >/tmp/cron-dry-run.out 2>&1 && DRY_RUN_OK=1 || DRY_RUN_OK=0
    fi

    if [[ $DRY_RUN_OK -eq 1 ]]; then
      ok "Dry-run OK (exit 0)"
      log "  摘要: $(head -3 /tmp/cron-dry-run.out | tr '\n' ' ')"
    else
      err "Dry-run FAILED (exit non-zero)"
      log "  完整输出: /tmp/cron-dry-run.out"
      log "  前 5 行:"
      head -5 /tmp/cron-dry-run.out | sed 's/^/    /'
      err "默认不继续 edit。如确认要继续，请用 --no-dry-run 重跑"
      exit 1
    fi
  fi
fi

# ─── 仅 dry-run 模式 ───────────────────────────────────
if [[ $DRY_RUN_ONLY -eq 1 ]]; then
  log ""
  ok "✅ dry-run-only 模式完成，未做 edit"
  exit 0
fi

# ─── Step 3: EDIT ───────────────────────────────────────
log ""
log "✏️  Step 3/5: EDIT"
if openclaw cron edit "$CRON_ID" "${EDIT_ARGS[@]}" >/tmp/cron-edit.out 2>&1; then
  ok "Edit OK"
else
  err "Edit FAILED"
  log "  输出: /tmp/cron-edit.out"
  EDIT_FAILED=1
fi

# ─── Step 4: VERIFY ─────────────────────────────────────
VERIFY_OK=0
if [[ -z "${EDIT_FAILED:-}" ]]; then
  log ""
  log "🔍 Step 4/5: VERIFY"
  if openclaw cron get "$CRON_ID" >/tmp/cron-after.json 2>&1; then
    # openclaw cron get 输出顶部有 plugin warnings，跳过非 JSON 行
    python3 -c "
import json
with open('/tmp/cron-after.json', 'r') as f:
    content = f.read()
idx = content.find('{')
if idx < 0:
    print('NO_JSON')
else:
    d = json.loads(content[idx:])
    print(f'payload.kind={d[\"payload\"][\"kind\"]}')
    argv = d['payload'].get('argv', [])
    if argv:
        print(f'argv=[\"{\" \".join(argv)}]')
    else:
        print('argv=[]')
    print(f'name={d[\"name\"]}')
    print(f'enabled={d.get(\"enabled\", \"?\")}')
" > /tmp/cron-after-extract.txt 2>&1

    # 读取提取结果
    CHANGES_STR=$(cat /tmp/cron-after-extract.txt | grep -v "NO_JSON" | tr '\n' ' ')
    if grep -q "NO_JSON" /tmp/cron-after-extract.txt; then
      err "Verify FAILED: 输出无可用 JSON"
    else
      ok "Verify OK"
      log "  变更:"
      sed 's/^/    /' /tmp/cron-after-extract.txt
      VERIFY_OK=1
    fi
  else
    err "Verify FAILED: 无法重新 get cron"
  fi
fi

# ─── Step 5: ROLLBACK（失败时）──────────────────────────
if [[ -z "${EDIT_FAILED:-}" && $VERIFY_OK -eq 1 ]]; then
  log ""
  ok "🎉 全部 5 步成功: $CRON_ID"
  if [[ -n "$BACKUP_FILE" ]]; then
    log "  备份保留在: $BACKUP_FILE"
  fi
  exit 0
fi

# 失败路径
if [[ $DO_ROLLBACK -eq 1 && -n "$BACKUP_FILE" && -f "$BACKUP_FILE" ]]; then
  err ""
  err "⚠️  触发自动 ROLLBACK"
  log "  从 $BACKUP_FILE 恢复..."

  # 从 backup JSON 提取关键字段
  ORIG_NAME=$(jq -r '.name' "$BACKUP_FILE")
  ORIG_DESC=$(jq -r '.description' "$BACKUP_FILE")
  ORIG_KIND=$(jq -r '.payload.kind' "$BACKUP_FILE")
  ORIG_CWD=$(jq -r '.payload.cwd // ""' "$BACKUP_FILE")
  ORIG_ARGV=$(jq -r '.payload.argv | join(" ")' "$BACKUP_FILE")

  # 构造 rollback 命令
  ROLLBACK_ARGS=(
    --name "$ORIG_NAME"
    --description "$ORIG_DESC"
  )

  if [[ "$ORIG_KIND" == "command" ]]; then
    ROLLBACK_ARGS+=(--command "$ORIG_ARGV")
    [[ -n "$ORIG_CWD" ]] && ROLLBACK_ARGS+=(--command-cwd "$ORIG_CWD")
  elif [[ "$ORIG_KIND" == "agentTurn" ]]; then
    ORIG_MSG=$(jq -r '.payload.message' "$BACKUP_FILE")
    ROLLBACK_ARGS+=(--message "$ORIG_MSG")
  fi

  if openclaw cron edit "$CRON_ID" "${ROLLBACK_ARGS[@]}" >/tmp/cron-rollback.out 2>&1; then
    ok "Rollback OK: 已恢复 $CRON_ID 到原始状态"
  else
    err "Rollback FAILED"
    err "  手动恢复命令: openclaw cron edit $CRON_ID \\"
    err "    --name \"\$ORIG_NAME\" --description \"\$ORIG_DESC\" ..."
    err "  或读 backup: $BACKUP_FILE"
    exit 2
  fi
else
  err "未启用 rollback 或无 backup，cron 状态可能不一致"
  err "  请手动检查: openclaw cron get $CRON_ID"
  exit 2
fi