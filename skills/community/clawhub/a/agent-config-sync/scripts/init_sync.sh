#!/bin/bash
# init_sync.sh — One-command setup of all sync infrastructure (v1.5)
# Usage:
#   bash init_sync.sh [master_workspace] [--dry-run] [--lang en|zh] [--demo] [--auto]
#   bash init_sync.sh --help
#
# v1.5: --auto mode: auto-detects agent workspaces and generates registry
#       if agent-registry.json doesn't exist; enhanced SYNC.md template
# v1.4: atomic writes for all sentinel files; creates .agent_sync_version
#       for master and each agent for offline catch-up tracking
# v1.2: now reads agent list from agent-registry.json (single source of truth)
#       supports --dry-run, --lang, --demo, --help

set -e

# ── Atomic write (prevents partial/corrupt sentinel files) ─────
_atomic_write() {
  local file="$1" content="$2"
  local tmp_file="${file}.tmp.$$"
  echo "$content" > "$tmp_file" && sync "$tmp_file" && mv "$tmp_file" "$file"
}

# ── Resolve script directory and registry path ──────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REGISTRY_FILE="$SKILL_DIR/references/agent-registry.json"
MASTER_WS=""
DRY_RUN=false
LANG="zh"
DEMO_MODE=false
DEMO_DIR=""
CONFIRMED=false
AUTO_MODE=false

# ── Bilingual messages ─────────────────────────────────────────
msg() {
  local key="$1"; shift
  case "$LANG" in
    en)
      case "$key" in
        title)          echo "=== Agent Config Sync v1.5 — Initialization ===" ;;
        demo_title)     echo "=== Agent Config Sync v1.5 — DEMO MODE ===" ;;
        auto_mode)      echo "🤖 AUTO MODE — detecting workspaces and generating registry" ;;
        registry_auto)  echo "🔍 No registry found — auto-detecting agent workspaces..." ;;
        registry_generated) echo "✅ Auto-generated registry from $1 workspace(s)" ;;
        auto_detect_master) echo "🤖 Auto-detected master: $1" ;;
        auto_detect_fail) echo "❌ Could not auto-detect any agent workspaces" ;;
        auto_detect_hint) echo "   Ensure workspaces exist at: ~/.openclaw/workspace-*" ;;
        registry_err)   echo "❌ Registry not found: $REGISTRY_FILE" ;;
        registry_ok)    echo "✅ Loaded registry ($1 agents)" ;;
        master_ws)      echo "Master workspace: $1" ;;
        dry_run_warn)   echo "🔍 DRY-RUN MODE — no changes will be made" ;;
        demo_warn)      echo "🎭 DEMO MODE — using temporary directory: $1" ;;
        demo_done)      echo "" ; echo "Demo complete. To try for real: bash scripts/init_sync.sh" ;;
        demo_note1)     echo "ℹ️  In demo mode, all files are created in: $1" ;;
        demo_note2)     echo "   Real deployment would create files in your actual workspaces." ;;
        creating_dirs)  echo "📁 Creating memory directory..." ;;
        dirs_exist)     echo "ℹ️  Memory directory exists, skipping creation" ;;
        created_sentinels) echo "✅ Created version sentinel files" ;;
        skip_sentinels) echo "ℹ️  Version files exist, skipping creation" ;;
        created_changelog) echo "✅ Created structured CHANGELOG.md" ;;
        created_journal) echo "✅ Created .sync_journal.jsonl" ;;
        agent_skip)     echo "⚠️  Skipping $1 (workspace not found)" ;;
        agent_done)     echo "✅ Agent '$1' configured" ;;
        sync_created)   echo "✅ $1/SYNC.md created" ;;
        sync_updated)   echo "🔄 $1/SYNC.md updated (content changed)" ;;
        sync_ok)        echo "ℹ️  $1/SYNC.md up-to-date, skipping" ;;
        bootstrap_ok)   echo "✅ Updated $1/BOOTSTRAP.md" ;;
        bootstrap_skip) echo "ℹ️  $1/BOOTSTRAP.md already has sync check" ;;
        heartbeat_ok)   echo "✅ Updated $1/HEARTBEAT.md" ;;
        heartbeat_skip) echo "ℹ️  $1/HEARTBEAT.md already has sync check" ;;
        complete)       echo "=== Initialization complete ===" ;;
        next_heartbeat) echo "Next: Add HEARTBEAT item 12 to master agent's HEARTBEAT.md" ;;
        next_reference) echo "See references/sync-setup.md for details." ;;
        usage1)         echo "Usage: bash init_sync.sh [master_workspace] [--dry-run] [--confirm] [--lang en|zh] [--demo] [--auto]" ;;
        usage2)         echo "  master_workspace  Path to master agent workspace (optional, from registry if omitted)" ;;
        usage3)         echo "  --dry-run         Preview changes without making them" ;;
        usage3b)        echo "  --confirm         Required for real execution (skip with --dry-run or --auto)" ;;
        usage4)         echo "  --lang en|zh      Output language (default: zh)" ;;
        usage5)         echo "  --demo            Create demo deployment in /tmp for learning" ;;
        usage5b)        echo "  --auto            Auto-detect workspaces and generate registry" ;;
        usage6)         echo "  -h, --help        Show this help" ;;
      esac
      ;;
    zh|*)
      case "$key" in
        title)          echo "=== Agent Config Sync v1.5 — 初始化 ===" ;;
        demo_title)     echo "=== Agent Config Sync v1.5 — 演示模式 ===" ;;
        auto_mode)      echo "🤖 自动模式 — 正在检测工作空间并生成注册表" ;;
        registry_auto)  echo "🔍 未找到注册表 — 正在自动检测 Agent 工作空间..." ;;
        registry_generated) echo "✅ 已从 $1 个工作空间自动生成注册表" ;;
        auto_detect_master) echo "🤖 自动检测 Master: $1" ;;
        auto_detect_fail) echo "❌ 无法自动检测任何 Agent 工作空间" ;;
        auto_detect_hint) echo "   请确认工作空间路径: ~/.openclaw/workspace-*" ;;
        registry_err)   echo "❌ 未找到注册表: $REGISTRY_FILE" ;;
        registry_ok)    echo "✅ 已加载注册表 ($1 个 Agent)" ;;
        master_ws)      echo "Master 工作空间: $1" ;;
        dry_run_warn)   echo "🔍 预览模式 — 不会执行任何修改" ;;
        demo_warn)      echo "🎭 演示模式 — 使用临时目录: $1" ;;
        demo_done)      echo "" ; echo "演示完成。正式部署: bash scripts/init_sync.sh" ;;
        demo_note1)     echo "ℹ️  演示模式将所有文件创建在: $1" ;;
        demo_note2)     echo "    正式部署会在实际工作空间中创建文件。" ;;
        creating_dirs)  echo "📁 创建 memory 目录..." ;;
        dirs_exist)     echo "ℹ️  Memory 目录已存在，跳过创建" ;;
        created_sentinels) echo "✅ 已创建版本哨兵文件" ;;
        skip_sentinels) echo "ℹ️  版本文件已存在，跳过创建" ;;
        created_changelog) echo "✅ 已创建结构化 CHANGELOG.md" ;;
        created_journal) echo "✅ 已创建 .sync_journal.jsonl" ;;
        agent_skip)     echo "⚠️  跳过 $1 (工作空间不存在)" ;;
        agent_done)     echo "✅ Agent '$1' 已配置" ;;
        sync_created)   echo "✅ $1/SYNC.md 已创建" ;;
        sync_updated)   echo "🔄 $1/SYNC.md 已更新 (内容有变化)" ;;
        sync_ok)        echo "ℹ️  $1/SYNC.md 已是最新，跳过" ;;
        bootstrap_ok)   echo "✅ 已更新 $1/BOOTSTRAP.md" ;;
        bootstrap_skip) echo "ℹ️  $1/BOOTSTRAP.md 已有同步检查" ;;
        heartbeat_ok)   echo "✅ 已更新 $1/HEARTBEAT.md" ;;
        heartbeat_skip) echo "ℹ️  $1/HEARTBEAT.md 已有同步检查" ;;
        complete)       echo "=== 初始化完成 ===" ;;
        next_heartbeat) echo "下一步: 将 HEARTBEAT 第12项添加到 Master Agent 的 HEARTBEAT.md" ;;
        next_reference) echo "详见 references/sync-setup.md" ;;
        usage1)         echo "用法: bash init_sync.sh [master_workspace] [--dry-run] [--confirm] [--lang en|zh] [--demo] [--auto]" ;;
        usage2)         echo "  master_workspace  Master Agent 工作空间路径 (可选，默认从注册表读取)" ;;
        usage3)         echo "  --dry-run         预览模式，不执行修改" ;;
        usage3b)        echo "  --confirm         正式执行时必需 (--dry-run / --auto 模式下不需要)" ;;
        usage4)         echo "  --lang en|zh      输出语言 (默认: zh)" ;;
        usage5)         echo "  --demo            在 /tmp 创建演示部署" ;;
        usage5b)        echo "  --auto            自动检测 workspace 并生成注册表" ;;
        usage6)         echo "  -h, --help        显示帮助" ;;
      esac
      ;;
  esac
}

# ── Help ───────────────────────────────────────────────────────
show_help() {
  msg usage1
  echo ""
  msg usage2
  msg usage3
  msg usage3b
  msg usage4
  msg usage5
  msg usage5b
  msg usage6
  exit 0
}

# ── Parse arguments ───────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    -h|--help)   show_help ;;
    --dry-run)   DRY_RUN=true ;;
    --confirm)   CONFIRMED=true ;;
    --auto)      AUTO_MODE=true ;;
    --demo)      DEMO_MODE=true ;;
    --lang)      ;;  # value consumed by prev tracking below
    --lang=*)
      LANG="${arg#--lang=}"
      ;;
    *)
      if [ "$prev" = "--lang" ]; then
        LANG="$arg"
      elif [ -z "$MASTER_WS" ] && [ "${arg#--}" = "$arg" ]; then
        MASTER_WS="$arg"
      fi
      ;;
  esac
  prev="$arg"
done

# Validate language
case "$LANG" in
  en|zh) ;;
  *) LANG="zh" ;;
esac

# ── Auto-detection: extract agent info from workspace ──────────
auto_detect_agent_info() {
  local ws="$1"
  local agent_id=$(basename "$ws" | sed 's/workspace-//')
  local name="" role=""

  if [ -f "$ws/IDENTITY.md" ]; then
    name=$(grep -i '^\-\s*\*\*Name:\*\*' "$ws/IDENTITY.md" | head -1 | sed 's/.*Name:\*\*\s*//;s/\r//')
    role=$(grep -i '^\-\s*\*\*Creature:\*\*' "$ws/IDENTITY.md" | head -1 | sed 's/.*Creature:\*\*\s*//;s/\r//')
    [ -z "$role" ] && role=$(grep -i '^\-\s*\*\*Role:\*\*' "$ws/IDENTITY.md" | head -1 | sed 's/.*Role:\*\*\s*//;s/\r//')
  fi

  [ -z "$name" ] && name="$agent_id"
  [ -z "$role" ] && role="Agent"

  echo "$agent_id|$name|$role"
}

# Auto-detect master from workspace names
auto_detect_master() {
  for ws in "$HOME/.openclaw/workspace-"*; do
    [ -d "$ws" ] || continue
    local agent_id=$(basename "$ws" | sed 's/workspace-//')
    case "$agent_id" in
      amaster|AMaster|master|Master|main|Main) echo "$agent_id"; return ;;
    esac
  done

  # Check IDENTITY.md for master keywords
  for ws in "$HOME/.openclaw/workspace-"*; do
    [ -d "$ws" ] || continue
    if grep -qiE 'master|coordinator|主助手|协同|协调' "$ws/IDENTITY.md" "$ws/SOUL.md" 2>/dev/null; then
      basename "$ws" | sed 's/workspace-//'
      return
    fi
  done

  # Fallback: first workspace
  for ws in "$HOME/.openclaw/workspace-"*; do
    [ -d "$ws" ] || continue
    if [ -f "$ws/IDENTITY.md" ] || [ -f "$ws/SOUL.md" ]; then
      basename "$ws" | sed 's/workspace-//'
      return
    fi
  done
}

# Auto-generate agent-registry.json from workspace scan
auto_generate_registry() {
  local ws_count=0
  local detected_agents=""
  for ws in "$HOME/.openclaw/workspace-"*; do
    [ -d "$ws" ] || continue
    [ -f "$ws/IDENTITY.md" ] || [ -f "$ws/SOUL.md" ] || [ -f "$ws/BOOTSTRAP.md" ] || continue
    local info=$(auto_detect_agent_info "$ws")
    detected_agents="$detected_agents$info"$'\n'
    ws_count=$((ws_count + 1))
  done

  if [ "$ws_count" -eq 0 ]; then
    msg auto_detect_fail
    msg auto_detect_hint
    return 1
  fi

  local master_agent=$(auto_detect_master)
  [ -z "$master_agent" ] && master_agent="amaster"

  msg auto_detect_master "$master_agent"
  msg registry_generated "$ws_count"

  # Build registry JSON
  local first_agent=true
  local agents_json=""
  while IFS='|' read -r agent_id agent_name agent_role; do
    [ -z "$agent_id" ] && continue
    if [ "$first_agent" = true ]; then
      first_agent=false
    else
      agents_json="$agents_json,"$'\n'
    fi
    agents_json="${agents_json}    \"${agent_id}\": {
      \"name\": \"${agent_name}\",
      \"role\": \"${agent_role}\",
      \"workspace\": \"\${vars.workspace_root}/workspace-${agent_id}\"
    }"
  done <<< "$detected_agents"

  cat > "$REGISTRY_FILE" << REGEOF
{
  "version": "1.5.0",
  "comment": "Auto-generated by init_sync.sh --auto. Customize as needed.",
  "vars": {
    "workspace_root": "~/.openclaw",
    "master_agent": "${master_agent}",
    "master_memory": "\${vars.workspace_root}/workspace-\${vars.master_agent}/memory"
  },
  "agents": {
${agents_json}
  },
  "sync": {
    "sentinel_dir": "memory",
    "journal_file": ".sync_journal.jsonl",
    "changelog_file": "CHANGELOG.md",
    "pending_prefix": "pending_sync",
    "max_changelog_sections": 10,
    "ttl_hours": 24,
    "dispatch_timeout_sec": 120
  },
  "self_protect": {
    "enabled": true,
    "skip_agents": ["agent-config-sync"],
    "isolated_sync": true,
    "blacklist": [
      "HEARTBEAT.md",
      "BOOTSTRAP.md",
      "SKILL.md",
      "scripts/",
      "SECURITY.md",
      "references/",
      "agent-registry.json"
    ],
    "sync_own_version_file": "skills/agent-config-sync/.sync_own_version",
    "allow_bootstrap_only": true
  },
  "batch": {
    "mode": "auto",
    "window_sec": 300
  }
}
REGEOF

  return 0
}

# ── Load registry ─────────────────────────────────────────────
if [ ! -f "$REGISTRY_FILE" ]; then
  if [ "$AUTO_MODE" = true ]; then
    msg auto_mode
    msg registry_auto
    if ! auto_generate_registry; then
      echo "  Tip: create agent workspaces with IDENTITY.md, then re-run with --auto"
      exit 1
    fi
  else
    msg registry_err
    echo "  Looked in: $REGISTRY_FILE"
    echo "  Tip: run from the skill directory, or use --auto to auto-detect"
    exit 1
  fi
fi

# Simple JSON value extraction (no jq dependency)
json_val() {
  # Extract value for a given dotted path, e.g. "vars.workspace_root"
  # Very basic: handles top-level and one-level nesting
  local path="$1" file="$2" key
  key=$(echo "$path" | awk -F. '{print $NF}')
  if echo "$path" | grep -q '\.'; then
    local section=$(echo "$path" | awk -F. '{print $1}')
    grep -A 50 "\"$section\"" "$file" | grep "\"$key\"" | head -1 | sed 's/.*: *"//;s/".*//'
  else
    grep "\"$key\"" "$file" | head -1 | sed 's/.*: *"//;s/".*//'
  fi
}

# Resolve variables in a value string
resolve_vars() {
  local val="$1"
  local workspace_root=$(json_val "vars.workspace_root" "$REGISTRY_FILE")
  local master_agent=$(json_val "vars.master_agent" "$REGISTRY_FILE")
  val="${val//\$\{vars.workspace_root\}/$workspace_root}"
  val="${val//\$\{vars.master_agent\}/$master_agent}"
  echo "$val"
}

# Resolve path: expand ~ to $HOME
expand_path() {
  local p="$1"
  echo "${p/#\~/$HOME}"
}

# Read all agent IDs from registry
read_agent_ids() {
  # Extract only top-level agent keys (lines like "acode": { with 4-space indent)
  grep -E '^    "[a-z][a-z0-9_-]*" *: *\{' "$REGISTRY_FILE" \
    | sed 's/.*"\([^"]*\)".*/\1/' \
    | grep -v '^_comment'
}

# Read agent workspace from registry
read_agent_ws() {
  local agent_id="$1"
  local raw=$(grep -A 10 "\"$agent_id\":" "$REGISTRY_FILE" | grep '"workspace"' | head -1 | sed 's/.*: *"//;s/".*//')
  resolve_vars "$raw"
}

# Read agent display name
read_agent_name() {
  local agent_id="$1" lang="${2:-en}"
  local name_key="name"
  [ "$lang" = "zh" ] && name_key="name_zh"
  grep -A 10 "\"$agent_id\":" "$REGISTRY_FILE" | grep "\"$name_key\"" | head -1 | sed 's/.*: *"//;s/".*//'
}

# ── Demo mode setup ───────────────────────────────────────────
if [ "$DEMO_MODE" = true ]; then
  DEMO_DIR=$(mktemp -d /tmp/agent-config-sync-demo-XXXXXX)
  msg demo_title
  msg demo_warn "$DEMO_DIR"

  # Create fake agent workspaces in demo dir
  MASTER_AGENT=$(json_val "vars.master_agent" "$REGISTRY_FILE")
  mkdir -p "$DEMO_DIR/workspace-$MASTER_AGENT/memory"

  while IFS= read -r agent_id; do
    [ -z "$agent_id" ] && continue
    [ "$agent_id" = "$MASTER_AGENT" ] && continue
    local_ws="$DEMO_DIR/workspace-$agent_id"
    mkdir -p "$local_ws"
    touch "$local_ws/BOOTSTRAP.md" "$local_ws/HEARTBEAT.md"
  done <<< "$(read_agent_ids)"

  # Override workspace paths for demo
  DEMO_MASTER_WS="$DEMO_DIR/workspace-$MASTER_AGENT"
  DEMO_AGENT_WS_LIST=""
  while IFS= read -r agent_id; do
    [ -z "$agent_id" ] && continue
    [ "$agent_id" = "$MASTER_AGENT" ] && continue
    DEMO_AGENT_WS_LIST="$DEMO_AGENT_WS_LIST $DEMO_DIR/workspace-$agent_id"
  done <<< "$(read_agent_ids)"

  MASTER_WS="$DEMO_MASTER_WS"
  # We'll loop DEMO_AGENT_WS_LIST below
fi

# ── Determine master workspace ────────────────────────────────
if [ -z "$MASTER_WS" ]; then
  MASTER_AGENT=$(json_val "vars.master_agent" "$REGISTRY_FILE")
  if [ "$DEMO_MODE" = true ]; then
    MASTER_WS="$DEMO_MASTER_WS"
  else
    MASTER_WS_RAW=$(json_val "vars.master_memory" "$REGISTRY_FILE")
    MASTER_WS_RAW=$(resolve_vars "$MASTER_WS_RAW")
    # master_memory points to .../memory, strip /memory to get workspace
    MASTER_WS=$(dirname "$(expand_path "$MASTER_WS_RAW")")
  fi
fi

MASTER_WS=$(expand_path "$MASTER_WS")

if [ "$DRY_RUN" = true ]; then
  msg dry_run_warn
  echo ""
fi

msg title
msg master_ws "$MASTER_WS"
echo ""

# ── Confirm check (required for non-dry-run, non-auto execution) ──
if [ "$DRY_RUN" = false ] && [ "$AUTO_MODE" = false ] && [ "$CONFIRMED" = false ]; then
  echo ""
  echo "⚠️  安全确认未通过"
  echo "   首次运行请先使用 --dry-run 预览变更"
  echo "   确认无误后添加 --confirm 执行:"
  echo "     $0 $MASTER_WS --confirm ${LANG:+"--lang $LANG"}"
  echo "   或使用自动模式: $0 --auto ${LANG:+"--lang $LANG"}"
  echo ""
  exit 0
fi

# ── Dry-run helper ────────────────────────────────────────────
do_cmd() {
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY-RUN] $*"
  else
    eval "$@"
  fi
}

# ── 1. Initialize version files ───────────────────────────────
MEMORY_DIR="$MASTER_WS/memory"
msg creating_dirs
do_cmd "mkdir -p \"$MEMORY_DIR\""

START_VERSION="v1.0"

if [ ! -f "$MEMORY_DIR/.current_system_version" ]; then
  do_cmd "_atomic_write \"$MEMORY_DIR/.current_system_version\" '$START_VERSION'"
  do_cmd "_atomic_write \"$MEMORY_DIR/.last_sync_version\" '$START_VERSION'"
  msg created_sentinels
else
  START_VERSION=$(cat "$MEMORY_DIR/.current_system_version")
  msg skip_sentinels
fi

# ── Create .agent_sync_version for master ─────────────────────
if [ ! -f "$MEMORY_DIR/.agent_sync_version" ]; then
  do_cmd "_atomic_write \"$MEMORY_DIR/.agent_sync_version\" '$START_VERSION'"
  echo "✅ Master .agent_sync_version = $START_VERSION"
else
  echo "ℹ️  Master .agent_sync_version exists, skipping"
fi

# ── 2. Create CHANGELOG.md ───────────────────────────────────
if [ ! -f "$MEMORY_DIR/CHANGELOG.md" ]; then
  if [ "$LANG" = "en" ]; then
    do_cmd "cat > \"$MEMORY_DIR/CHANGELOG.md\" << 'CHG'
# System Change Log

## v1.0 (initial)
**Change Type**: ⚙️ OpenClaw Config / 🤖 Agent Config
**Author**: System
**Priority**: normal

### Added
- Initial deployment of config sync mechanism (agent-config-sync v1.0)
- Version sentinel files (.current_system_version, .last_sync_version)
- HEARTBEAT config change sync check

### Changed
- (none)

### Deprecated
- (none)
CHG"
  else
    do_cmd "cat > \"$MEMORY_DIR/CHANGELOG.md\" << 'CHG'
# 系统变更日志

## v1.0 (initial)
**变更类型**: ⚙️ OpenClaw 系统配置 / 🤖 Agent配置
**变更人**: System
**紧急程度**: normal

### 新增
- 首次部署配置同步机制 (agent-config-sync v1.0)
- 创建版本哨兵文件 (.current_system_version, .last_sync_version)
- HEARTBEAT 中配置变更强制同步检查

### 修改
- （暂无）

### 废弃
- （暂无）
CHG"
  fi
  msg created_changelog
fi

# ── 3. Initialize sync journal ───────────────────────────────
if [ ! -f "$MEMORY_DIR/.sync_journal.jsonl" ]; then
  do_cmd "touch \"$MEMORY_DIR/.sync_journal.jsonl\""
  msg created_journal
fi

# ── SYNC.md template (bilingual, v1.5 enhanced) ────────────────
if [ "$LANG" = "en" ]; then
  SYNC_TEMPLATE='# Config Sync — Automatic Change Notification (v1.5)

## 🆕 Quick Start (New User Guide)
> **Just installed?** Here is how sync works in 3 simple rules:

| Rule | What | How |
|:-----|:-----|:----|
| 1. **Check** | Look for `pending_sync_*.md` files on startup | Your BOOTSTRAP.md does this automatically |
| 2. **Apply** | Read the change summary, update your config | Follow instructions in the pending file |
| 3. **Delete** | Remove the file after applying changes | `rm pending_sync_v*.md` |

> ⚠️ **Important**: Never use shared/collaborative systems until all pending syncs are processed.

---

## 📋 Common Operations Cheat Sheet

| Task | Command |
|:-----|:--------|
| Check for pending syncs | `ls pending_sync_*.md revert_sync_*.md isolated_sync_*.md` |
| Check my version | `cat memory/.agent_sync_version` |
| Check system version | Ask Master agent: "What is the current system version?" |
| Request catch-up | Ask Master: "I am on v1.0, please send catch-up to latest" |
| Check if expired (TTL 24h) | Parse `**过期时间**` in the file header |
| Verify SHA256 signature | Compare filename SHA with `**签名**` field in file |
| View full change log | Ask Master to share `CHANGELOG.md` |

---

## 🔄 Sync Check Flow
```
Start/Activate → ls pending_sync_*.md revert_sync_*.md isolated_sync_*.md?
  ├─ ✅ Files exist → check for expired (TTL 24h) → delete expired
  ├─ ✅ Multiple non-expired → version collapse (fold to latest) → apply
  ├─ ✅ Single file → apply directly
  └─ ❌ No files → check .agent_sync_version vs system version
       ├─ Behind → request catch-up from Master
       └─ Up-to-date → no sync needed
```

## ⚡ Conflict Handling
- Expired files → delete, request latest from Master
- Multiple versions → version collapse (jump to latest if depends_on chain covers)
- Revert files → restore from memory/.sync_snapshots/
- Isolated sync → agent-config-sync self-upgrade (request from Master)

## 🔗 Sync Source
- Full log: <master_workspace>/memory/CHANGELOG.md
- Active query: send message to master agent

## 🔒 Important
- Check version before using coordinated systems
- If pending_sync_*.md exists but is unprocessed, do NOT use coordinated systems'
else
  SYNC_TEMPLATE='# 配置同步机制 — 自动获取变更通知 (v1.5)

## 🆕 新手上路指南
> **刚安装完？** 3 条规则即可上手：

| 规则 | 做什么 | 怎么做 |
|:-----|:-----|:-----|
| 1. **查** | 启动时检查有没有 `pending_sync_*.md` 文件 | BOOTSTRAP.md 已自动配置检查 |
| 2. **更** | 读取变更摘要，更新配置 | 按 pending 文件中的指令操作 |
| 3. **删** | 应用变更后删除文件 | `rm pending_sync_v*.md` |

> ⚠️ **重要提醒**：在未处理完所有 pending 同步文件之前，不要使用共享/协同系统功能。

---

## 📋 常用操作速查表

| 任务 | 命令/操作 |
|:-----|:--------|
| 检查待同步文件 | `ls pending_sync_*.md revert_sync_*.md isolated_sync_*.md` |
| 查看我的版本 | `cat memory/.agent_sync_version` |
| 查看系统版本 | 向 Master Agent 发送消息：当前系统版本是多少？ |
| 请求追赶包 | 向 Master 发送：我在 v1.0，请发送追赶包到最新版本 |
| 检查文件是否过期 | 解析文件头部的 `**过期时间**`（TTL 24h） |
| 验证 SHA256 签名 | 对比文件名 SHA 与文件内 `**签名**` 字段 |
| 查看完整变更日志 | 向 Master 请求 `CHANGELOG.md` |

---

## 🔄 同步检查流程
```
启动/激活 → ls pending_sync_*.md revert_sync_*.md isolated_sync_*.md?
  ├─ ✅ 有文件 → 检查是否过期 (TTL 24h) → 删除过期文件
  ├─ ✅ 多个未过期 → 版本折叠（跳到最新版本）→ 应用变更
  ├─ ✅ 单个文件 → 直接应用
  └─ ❌ 无文件 → 检查 .agent_sync_version 与系统版本对比
       ├─ 落后 → 向 Master 请求追赶包
       └─ 最新 → 无需同步
```

## ⚡ 冲突处理
- 过期文件 → 删除，向 Master 请求最新版本
- 多个版本 → 版本折叠（若 depends_on 链覆盖则直接跳到最新版）
- 回滚文件 → 从 memory/.sync_snapshots/ 恢复
- 隔离同步 → agent-config-sync 自身升级（向 Master 请求）

## 🔗 同步源
- 完整日志: <master_workspace>/memory/CHANGELOG.md
- 主动查询: 向 Master Agent 发送消息

## 🔒 重要
- 使用共享系统前，必须确认版本信息
- 如果有 pending_sync_*.md 但未处理，不要使用相关系统功能'
fi

# ── Bootstrap / Heartbeat content (bilingual) ─────────────────
if [ "$LANG" = "en" ]; then
  BOOTSTRAP_LINES=(
    ""
    "## Startup Check — Config Sync"
    "- [ ] Check for \`pending_sync_*.md\` files in workspace"
    "  - Files exist → read change summary, update MEMORY.md, delete files"
    "  - Expired files (生成时间 > 24h) → delete, request latest from Master"
    "  - Check \`memory/.agent_sync_version\` — if outdated, request catch-up"
    "  - ⚠️ agent-config-sync self-upgrade notices → request isolated sync from Master"
  )
  HEARTBEAT_LINES=(
    ""
    "<!-- agent-config-sync-check v1.4 -->"
    "## ⭐ Config Sync Check (run every heartbeat)"
    "- [ ] Check for \`pending_sync_*.md\` files in workspace"
    "  - Found and non-empty → read change summary, update MEMORY.md, delete files"
    "  - Not found → skip"
    "  - Verify SHA256 signature integrity"
    "  - Check \`memory/.agent_sync_version\` — if < system version, request catch-up from Master"
    "  - Delete expired pending_sync files (生成时间 > TTL 24h)"
  )
  HEARTBEAT_MARKER="agent-config-sync-check"
else
  BOOTSTRAP_LINES=(
    ""
    "## 启动检查 — 配置同步"
    "- [ ] 检查工作目录下是否存在 \`pending_sync_*.md\` 文件"
    "  - 存在 → 读取变更摘要，更新 MEMORY.md，删除文件"
    "  - 过期文件（生成时间 > 24h）→ 删除，向 Master 请求最新版本"
    "  - 检查 \`memory/.agent_sync_version\` — 若落后，请求追赶"
    "  - ⚠️ agent-config-sync 自身升级通知 → 向 Master 请求 isolated sync"
  )
  HEARTBEAT_LINES=(
    ""
    "<!-- agent-config-sync-check v1.4 -->"
    "## ⭐ 配置同步检查（每次 heartbeat 执行）"
    "- [ ] 检查工作目录下是否存在 \`pending_sync_*.md\` 文件"
    "  - 存在且非空 → 读取变更摘要，更新 MEMORY.md，删除文件"
    "  - 不存在 → 跳过"
    "  - 验证 SHA256 签名完整性"
    "  - 检查 \`memory/.agent_sync_version\` — 若落后于系统版本，向 Master 请求追赶"
    "  - 删除过期的 pending_sync 文件（生成时间 > TTL 24h）"
  )
  HEARTBEAT_MARKER="agent-config-sync-check"
fi

# ── 4. Setup each agent workspace ─────────────────────────────
# Collect agent workspaces to process
AGENT_WS_LIST=""
if [ "$DEMO_MODE" = true ]; then
  AGENT_WS_LIST="$DEMO_AGENT_WS_LIST"
else
  while IFS= read -r agent_id; do
    [ -z "$agent_id" ] && continue
    [ "$agent_id" = "$(json_val 'vars.master_agent' "$REGISTRY_FILE")" ] && continue
    agent_ws=$(expand_path "$(read_agent_ws "$agent_id")")
    AGENT_WS_LIST="$AGENT_WS_LIST $agent_ws"
  done <<< "$(read_agent_ids)"
fi

for agent_ws in $AGENT_WS_LIST; do
  agent_ws=$(echo "$agent_ws" | xargs)  # trim whitespace
  [ -z "$agent_ws" ] && continue

  # Path safety check — only allow ~/.openclaw/workspace-* paths
  case "$agent_ws" in
    $HOME/.openclaw/workspace-*)  # allowed
      ;;
    *)
      echo "❌ 拒绝: $agent_ws (不在 ~/.openclaw/workspace-* 范围内)"
      continue
      ;;
  esac

  if [ ! -d "$agent_ws" ]; then
    msg agent_skip "$agent_ws"
    continue
  fi

  agent_name=$(basename "$agent_ws" | sed 's/workspace-//')

  # SYNC.md
  if [ -f "$agent_ws/SYNC.md" ]; then
    existing_normalized=$(cat "$agent_ws/SYNC.md" 2>/dev/null | sed 's/[[:space:]]*$//')
    template_normalized=$(echo "$SYNC_TEMPLATE" | sed 's/[[:space:]]*$//')
    if [ "$existing_normalized" = "$template_normalized" ]; then
      msg sync_ok "$agent_ws"
    else
      do_cmd "echo \"\$SYNC_TEMPLATE\" > \"$agent_ws/SYNC.md\""
      msg sync_updated "$agent_ws"
    fi
  else
    do_cmd "echo \"\$SYNC_TEMPLATE\" > \"$agent_ws/SYNC.md\""
    msg sync_created "$agent_ws"
  fi

  # BOOTSTRAP.md
  if ! grep -q "pending_sync_" "$agent_ws/BOOTSTRAP.md" 2>/dev/null; then
    if [ "$DRY_RUN" = true ]; then
      echo "  [DRY-RUN] Would append to $agent_ws/BOOTSTRAP.md"
    else
      for line in "${BOOTSTRAP_LINES[@]}"; do
        echo "$line" >> "$agent_ws/BOOTSTRAP.md"
      done
    fi
    msg bootstrap_ok "$agent_ws"
  else
    msg bootstrap_skip "$agent_ws"
  fi

  # HEARTBEAT.md
  if ! grep -q "$HEARTBEAT_MARKER" "$agent_ws/HEARTBEAT.md" 2>/dev/null; then
    if [ "$DRY_RUN" = true ]; then
      echo "  [DRY-RUN] Would append to $agent_ws/HEARTBEAT.md"
    else
      for line in "${HEARTBEAT_LINES[@]}"; do
        echo "$line" >> "$agent_ws/HEARTBEAT.md"
      done
    fi
    msg heartbeat_ok "$agent_ws"
  else
    msg heartbeat_skip "$agent_ws"
  fi

  msg agent_done "$agent_name"

  # ── Create .agent_sync_version for this agent ──────────────
  local_agent_memory="$agent_ws/memory"
  do_cmd "mkdir -p \"$local_agent_memory\""
  if [ ! -f "$local_agent_memory/.agent_sync_version" ]; then
    do_cmd "_atomic_write \"$local_agent_memory/.agent_sync_version\" '$START_VERSION'"
    echo "  ✅ $agent_name memory/.agent_sync_version = $START_VERSION"
  else
    echo "  ℹ️  $agent_name memory/.agent_sync_version exists, skipping"
  fi

  # ── Create .sync_snapshots directory for rollback ──────────
  if [ ! -d "$local_agent_memory/.sync_snapshots" ]; then
    do_cmd "mkdir -p \"$local_agent_memory/.sync_snapshots\""
    echo "  ✅ $agent_name memory/.sync_snapshots/ created"
  fi

  echo ""
done

# ── Complete ──────────────────────────────────────────────────
if [ "$DEMO_MODE" = true ]; then
  echo ""
  echo "=== Demo Directory Structure ==="
  find "$DEMO_DIR" -type f | sort | sed "s|$DEMO_DIR|$DEMO_DIR|"
  echo ""
  msg demo_note1 "$DEMO_DIR"
  msg demo_note2
  msg demo_done
else
  msg complete
  echo ""
  msg next_heartbeat
  msg next_reference
fi
