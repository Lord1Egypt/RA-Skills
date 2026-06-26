#!/bin/bash
# wizard.sh — Interactive Setup Wizard for agent-config-sync (v1.5)
# Usage:
#   bash wizard.sh                    # Interactive mode (default)
#   bash wizard.sh --auto             # Non-interactive auto-detection
#   bash wizard.sh --lang en|zh       # Language selection
#   bash wizard.sh --help             # Show help
#
# Guides new users through 5-step initialization:
#   1. Detect environment (OpenClaw, workspaces, agents, master)
#   2. Configure agent registry
#   3. Run init_sync.sh
#   4. Integrate HEARTBEAT item 12
#   5. Completion report

set -e

# ═══════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REGISTRY_FILE="$SKILL_DIR/references/agent-registry.json"
OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_PREFIX="${OPENCLAW_DIR}/workspace-"
INIT_SCRIPT="$SCRIPT_DIR/init_sync.sh"

LANG="zh"
AUTO_MODE=false
SKIP_STEPS=""  # comma-separated steps to skip (--skip 1,2,4 etc.)

# ── Colors ────────────────────────────────────────────────────
if [ -t 1 ]; then
  BOLD='\033[1m'
  RED='\033[31m'
  GREEN='\033[32m'
  YELLOW='\033[33m'
  BLUE='\033[34m'
  CYAN='\033[36m'
  MAGENTA='\033[35m'
  RESET='\033[0m'
else
  BOLD='' RED='' GREEN='' YELLOW='' BLUE='' CYAN='' MAGENTA='' RESET=''
fi

# ═══════════════════════════════════════════════════════════════
# Bilingual Messages
# ═══════════════════════════════════════════════════════════════
msg() {
  local key="$1"; shift
  case "$LANG" in
    en) _msg_en "$key" "$@";;
    zh) _msg_zh "$key" "$@";;
    *) _msg_zh "$key" "$@";;
  esac
}

_msg_en() {
  local key="$1"; shift
  case "$key" in
    # Banner
    banner)       echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════╗${RESET}"
                  echo -e "${BOLD}${CYAN}║     agent-config-sync v1.5 — Setup Wizard           ║${RESET}"
                  echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════╝${RESET}" ;;
    auto_banner)  echo -e "${BOLD}${CYAN}== agent-config-sync v1.5 — Auto Setup ==${RESET}" ;;
    welcome)      echo ""
                  echo -e "${BOLD}Welcome!${RESET} This wizard will set up config sync across your agents."
                  echo "It takes ~2 minutes and requires no manual file editing."
                  echo ""
                  echo "  Step 1: Detect environment"
                  echo "  Step 2: Configure agent registry"
                  echo "  Step 3: Initialize sync infrastructure"
                  echo "  Step 4: Integrate HEARTBEAT check"
                  echo "  Step 5: Completion report"
                  echo ""
                  echo -e "${CYAN}Tip:${RESET} Use ${BOLD}--auto${RESET} for non-interactive setup (auto-detect everything)."
                  echo "" ;;

    # Step 1
    s1_title)     echo ""
                  echo -e "${BOLD}${BLUE}── Step 1/5: Detect Environment${RESET}" ;;
    s1_check_oc)  echo -n "  Checking OpenClaw installation... " ;;
    s1_oc_ok)     echo -e "${GREEN}✅ Found${RESET}" ;;
    s1_oc_fail)   echo -e "${RED}❌ Not found${RESET}"
                  echo ""
                  echo "  ${RED}Error:${RESET} openclaw command not available."
                  echo "  This skill requires OpenClaw to be installed."
                  echo "  Install from: https://docs.openclaw.ai/install"
                  echo ""
                  echo "  ${YELLOW}Workaround:${RESET} re-run with --skip 1 to skip environment check" ;;
    s1_scan_ws)   echo "  Scanning agent workspaces..." ;;
    s1_ws_found)  echo -e "  ${GREEN}Found $1 agent workspace(s):${RESET}" ;;
    s1_ws_none)   echo -e "  ${YELLOW}No agent workspaces found in ${OPENCLAW_DIR}${RESET}"
                  echo "  Expected pattern: ${WORKSPACE_PREFIX}<agent-id>/"
                  echo ""
                  echo "  ${CYAN}Skip this step?${RESET} You can create workspaces later and re-run."
                  echo "  Or: create them now in another terminal and press Enter to retry." ;;
    s1_ws_item)   echo -e "    ${GREEN}$1${RESET} — $2 ($3)" ;;
    s1_master_auto) echo -e "  Auto-detected master: ${BOLD}${GREEN}$1${RESET}" ;;
    s1_master_ask) echo ""
                  echo "  ${CYAN}Which agent is your master/coordinator?${RESET}"
                  echo "  (Master agent manages sync dispatch to other agents)" ;;

    # Step 2
    s2_title)     echo ""
                  echo -e "${BOLD}${BLUE}── Step 2/5: Configure Agent Registry${RESET}" ;;
    s2_reg_exists) echo -e "  ${GREEN}✅ Registry file exists${RESET}" ;;
    s2_reg_create) echo -e "  ${YELLOW}Registry file will be created:${RESET}" ;;
    s2_reg_show)  echo ""; echo -e "  ${BOLD}Agent list:${RESET}" ;;
    s2_reg_item)  echo -e "    ${CYAN}$1${RESET} — $2 ($3)";;
    s2_reg_path)  echo "    Workspace: $1" ;;
    s2_reg_master) echo -e "    ${BOLD}Master:${RESET} $1" ;;
    s2_reg_confirm) echo ""; echo -e "  ${YELLOW}Confirm this configuration?${RESET} [Y/n]" ;;
    s2_reg_saved) echo -e "  ${GREEN}✅ Registry saved ($1 agents)${RESET}" ;;
    s2_edit_opt)  echo "  ${CYAN}Options:${RESET} [e] edit  [Y] confirm  [n] skip" ;;

    # Step 3
    s3_title)     echo ""
                  echo -e "${BOLD}${BLUE}── Step 3/5: Initialize Sync Infrastructure${RESET}" ;;
    s3_running)   echo "  Running init_sync.sh --confirm --auto..." ;;
    s3_ok)        echo -e "  ${GREEN}✅ Initialization complete${RESET}" ;;
    s3_fail)      echo -e "  ${RED}❌ Initialization failed (exit code: $1)${RESET}"
                  echo "  Check error output above. Common fixes:"
                  echo "  - Verify agent workspace paths exist"
                  echo "  - Run with --dry-run first to preview changes"
                  echo "  ${CYAN}Retry?${RESET} [Y/n] (or skip and initialize manually later)" ;;

    # Step 4
    s4_title)     echo ""
                  echo -e "${BOLD}${BLUE}── Step 4/5: Integrate HEARTBEAT${RESET}" ;;
    s4_already)   echo -e "  ${GREEN}✅ HEARTBEAT item 12 already present${RESET}" ;;
    s4_adding)    echo "  Adding HEARTBEAT item 12 to master agent ($1)..." ;;
    s4_added)     echo -e "  ${GREEN}✅ HEARTBEAT item 12 added to $1/HEARTBEAT.md${RESET}" ;;
    s4_no_master) echo -e "  ${YELLOW}⚠️  Master agent workspace not found, skipping${RESET}"
                  echo "  Add manually later: see references/sync-setup.md" ;;
    s4_note)      echo ""
                  echo -e "  ${CYAN}Note:${RESET} This adds a sync check to the master's heartbeat."
                  echo "  The item number may need manual adjustment if HEARTBEAT.md"
                  echo "  already has 12+ items." ;;

    # Step 5
    s5_title)     echo ""
                  echo -e "${BOLD}${BLUE}── Step 5/5: Completion Report${RESET}" ;;
    s5_summary)   echo ""
                  echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════════════╗${RESET}"
                  echo -e "${BOLD}${GREEN}║          Setup Complete! 🎉                          ║${RESET}"
                  echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════════════════╝${RESET}" ;;
    s5_vers)      echo ""
                  echo -e "  ${BOLD}Version Sentinel Status:${RESET}" ;;
    s5_vers_ok)   echo -e "    ${GREEN}✅${RESET} $1: current=$2  last_sync=$2" ;;
    s5_vers_miss) echo -e "    ${YELLOW}○${RESET} $1: no version files yet" ;;
    s5_agent)     echo ""
                  echo -e "  ${BOLD}Agent Sync Readiness:${RESET}" ;;
    s5_agent_ok)  echo -e "    ${GREEN}✅${RESET} $1 ($2): SYNC.md + BOOTSTRAP + HEARTBEAT ready" ;;
    s5_agent_part) echo -e "    ${YELLOW}⚠️${RESET} $1 ($2): some files missing" ;;
    s5_agent_miss) echo -e "    ${RED}❌${RESET} $1 ($2): workspace not found" ;;
    s5_files)     echo ""
                  echo -e "  ${BOLD}Files Created:${RESET}" ;;

    # Next steps
    s5_next)      echo ""
                  echo -e "${BOLD}${CYAN}Next Steps:${RESET}"
                  echo ""
                  echo "  1. ${BOLD}Daily use:${RESET} Make changes → update CHANGELOG.md"
                  echo "     → bump .current_system_version → HEARTBEAT auto-dispatches"
                  echo ""
                  echo "  2. ${BOLD}Force sync:${RESET} bash scripts/force_sync.sh --confirm \\"
                  echo "        ~/.openclaw/workspace-$1/memory v1.0 v1.1"
                  echo ""
                  echo "  3. ${BOLD}Rollback:${RESET} bash scripts/revert_sync.sh --confirm \\"
                  echo "        ~/.openclaw/workspace-$1/memory v1.0"
                  echo ""
                  echo "  4. ${BOLD}Check status:${RESET}"
                  echo "     cat ~/.openclaw/workspace-$1/memory/.current_system_version"
                  echo "     cat ~/.openclaw/workspace-$1/memory/.last_sync_version"
                  echo ""
                  echo -e "  ${CYAN}Full docs:${RESET} ${SKILL_DIR}/SKILL.md"
                  echo -e "  ${CYAN}Quickstart:${RESET} ${SKILL_DIR}/references/quickstart.md"
                  echo "" ;;

    # Skip prompt
    skip_prompt)  echo -e "  ${CYAN}Skip this step?${RESET} [y/N]" ;;
    skip_ok)      echo -e "  ${YELLOW}⏭️  Step skipped${RESET}" ;;

    # Errors
    err_reg_parse) echo -e "  ${RED}❌ Failed to parse registry${RESET}" ;;

    # Help
    help_title)   echo "agent-config-sync Setup Wizard v1.5"
                  echo ""
                  echo "Interactive wizard to set up config sync across OpenClaw agents." ;;
    help_usage)   echo "Usage: bash wizard.sh [OPTIONS]" ;;
    help_opts)    echo ""
                  echo "Options:"
                  echo "  --auto          Non-interactive: auto-detect everything (no prompts)"
                  echo "  --lang en|zh    Language selection (default: zh)"
                  echo "  --skip N[,N]    Skip specific steps (e.g., --skip 4)"
                  echo "  -h, --help      Show this help" ;;

    # Misc
    abort)        echo ""; echo -e "  ${YELLOW}Aborted by user${RESET}";;
    press_enter)  echo ""; echo -n "Press Enter to continue...";;
    yn_default_y) echo -n " [Y/n]: ";;
    yn_default_n) echo -n " [y/N]: ";;
  esac
}

_msg_zh() {
  local key="$1"; shift
  case "$key" in
    # Banner
    banner)       echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════╗${RESET}"
                  echo -e "${BOLD}${CYAN}║     agent-config-sync v1.5 — 安装向导               ║${RESET}"
                  echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════╝${RESET}" ;;
    auto_banner)  echo -e "${BOLD}${CYAN}== agent-config-sync v1.5 — 自动安装 ==${RESET}" ;;
    welcome)      echo ""
                  echo -e "${BOLD}欢迎！${RESET} 本向导将帮您配置跨 Agent 配置同步系统。"
                  echo "耗时约 2 分钟，无需手动编辑任何文件。"
                  echo ""
                  echo "  第1步: 检测环境"
                  echo "  第2步: 配置 Agent 注册表"
                  echo "  第3步: 初始化同步基础设施"
                  echo "  第4步: 集成 HEARTBEAT 检查"
                  echo "  第5步: 完成报告"
                  echo ""
                  echo -e "${CYAN}提示:${RESET} 使用 ${BOLD}--auto${RESET} 可跳过所有交互，自动完成安装。"
                  echo "" ;;

    # Step 1
    s1_title)     echo ""
                  echo -e "${BOLD}${BLUE}── 第 1/5 步: 检测环境${RESET}" ;;
    s1_check_oc)  echo -n "  检查 OpenClaw 安装... " ;;
    s1_oc_ok)     echo -e "${GREEN}✅ 已找到${RESET}" ;;
    s1_oc_fail)   echo -e "${RED}❌ 未找到${RESET}"
                  echo ""
                  echo "  ${RED}错误:${RESET} openclaw 命令不可用。"
                  echo "  本 skill 需要 OpenClaw 环境。"
                  echo "  安装指引: https://docs.openclaw.ai/install"
                  echo ""
                  echo "  ${YELLOW}跳过:${RESET} 使用 --skip 1 跳过环境检查" ;;
    s1_scan_ws)   echo "  正在扫描 Agent 工作空间..." ;;
    s1_ws_found)  echo -e "  ${GREEN}找到 $1 个 Agent 工作空间:${RESET}" ;;
    s1_ws_none)   echo -e "  ${YELLOW}在 ${OPENCLAW_DIR} 下未找到 Agent 工作空间${RESET}"
                  echo "  预期格式: ${WORKSPACE_PREFIX}<agent-id>/"
                  echo ""
                  echo "  ${CYAN}跳过此步骤?${RESET} 您可以在创建好工作空间后重新运行。"
                  echo "  或者: 在另一个终端创建好工作空间后，按 Enter 重试。" ;;
    s1_ws_item)   echo -e "    ${GREEN}$1${RESET} — $2 ($3)" ;;
    s1_master_auto) echo -e "  自动识别 Master: ${BOLD}${GREEN}$1${RESET}" ;;
    s1_master_ask) echo ""
                  echo "  ${CYAN}哪个 Agent 是您的 Master/协调者?${RESET}"
                  echo "  (Master Agent 负责向其他 Agent 分发同步配置)" ;;

    # Step 2
    s2_title)     echo ""
                  echo -e "${BOLD}${BLUE}── 第 2/5 步: 配置 Agent 注册表${RESET}" ;;
    s2_reg_exists) echo -e "  ${GREEN}✅ 注册表文件已存在${RESET}" ;;
    s2_reg_create) echo -e "  ${YELLOW}将创建注册表文件:${RESET}" ;;
    s2_reg_show)  echo ""; echo -e "  ${BOLD}Agent 列表:${RESET}" ;;
    s2_reg_item)  echo -e "    ${CYAN}$1${RESET} — $2 ($3)";;
    s2_reg_path)  echo "    工作空间: $1" ;;
    s2_reg_master) echo -e "    ${BOLD}Master:${RESET} $1" ;;
    s2_reg_confirm) echo ""; echo -e "  ${YELLOW}确认此配置?${RESET} [Y/n]" ;;
    s2_reg_saved) echo -e "  ${GREEN}✅ 注册表已保存 ($1 个 Agent)${RESET}" ;;
    s2_edit_opt)  echo "  ${CYAN}选项:${RESET} [e] 编辑  [Y] 确认  [n] 跳过" ;;

    # Step 3
    s3_title)     echo ""
                  echo -e "${BOLD}${BLUE}── 第 3/5 步: 初始化同步基础设施${RESET}" ;;
    s3_running)   echo "  正在运行 init_sync.sh --confirm --auto..." ;;
    s3_ok)        echo -e "  ${GREEN}✅ 初始化完成${RESET}" ;;
    s3_fail)      echo -e "  ${RED}❌ 初始化失败 (退出码: $1)${RESET}"
                  echo "  请检查上方错误输出。常见修复:"
                  echo "  - 确认 Agent 工作空间路径正确"
                  echo "  - 先用 --dry-run 预览变更"
                  echo "  ${CYAN}重试?${RESET} [Y/n] (或跳过后手动初始化)" ;;

    # Step 4
    s4_title)     echo ""
                  echo -e "${BOLD}${BLUE}── 第 4/5 步: 集成 HEARTBEAT${RESET}" ;;
    s4_already)   echo -e "  ${GREEN}✅ HEARTBEAT 第12项已存在${RESET}" ;;
    s4_adding)    echo "  正在将 HEARTBEAT 第12项添加到 Master Agent ($1)..." ;;
    s4_added)     echo -e "  ${GREEN}✅ HEARTBEAT 第12项已添加到 $1/HEARTBEAT.md${RESET}" ;;
    s4_no_master) echo -e "  ${YELLOW}⚠️  Master Agent 工作空间不存在，跳过${RESET}"
                  echo "  请稍后手动添加: 参考 references/sync-setup.md" ;;
    s4_note)      echo ""
                  echo -e "  ${CYAN}注意:${RESET} 此操作将同步检查添加到 Master 的心跳中。"
                  echo "  如果 HEARTBEAT.md 已有 12 个以上的项目，编号可能需要手动调整。" ;;

    # Step 5
    s5_title)     echo ""
                  echo -e "${BOLD}${BLUE}── 第 5/5 步: 完成报告${RESET}" ;;
    s5_summary)   echo ""
                  echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════════════╗${RESET}"
                  echo -e "${BOLD}${GREEN}║              安装完成！🎉                            ║${RESET}"
                  echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════════════════╝${RESET}" ;;
    s5_vers)      echo ""
                  echo -e "  ${BOLD}版本哨兵状态:${RESET}" ;;
    s5_vers_ok)   echo -e "    ${GREEN}✅${RESET} $1: current=$2  last_sync=$2" ;;
    s5_vers_miss) echo -e "    ${YELLOW}○${RESET} $1: 尚无版本文件" ;;
    s5_agent)     echo ""
                  echo -e "  ${BOLD}Agent 同步就绪状态:${RESET}" ;;
    s5_agent_ok)  echo -e "    ${GREEN}✅${RESET} $1 ($2): SYNC.md + BOOTSTRAP + HEARTBEAT 就绪" ;;
    s5_agent_part) echo -e "    ${YELLOW}⚠️${RESET} $1 ($2): 部分文件缺失" ;;
    s5_agent_miss) echo -e "    ${RED}❌${RESET} $1 ($2): 工作空间不存在" ;;
    s5_files)     echo ""
                  echo -e "  ${BOLD}已创建文件:${RESET}" ;;

    # Next steps
    s5_next)      echo ""
                  echo -e "${BOLD}${CYAN}下一步:${RESET}"
                  echo ""
                  echo "  1. ${BOLD}日常使用:${RESET} 修改配置 → 更新 CHANGELOG.md"
                  echo "     → 修改 .current_system_version → HEARTBEAT 自动分发"
                  echo ""
                  echo "  2. ${BOLD}强制同步:${RESET} bash scripts/force_sync.sh --confirm \\"
                  echo "        ~/.openclaw/workspace-$1/memory v1.0 v1.1"
                  echo ""
                  echo "  3. ${BOLD}版本回滚:${RESET} bash scripts/revert_sync.sh --confirm \\"
                  echo "        ~/.openclaw/workspace-$1/memory v1.0"
                  echo ""
                  echo "  4. ${BOLD}检查状态:${RESET}"
                  echo "     cat ~/.openclaw/workspace-$1/memory/.current_system_version"
                  echo "     cat ~/.openclaw/workspace-$1/memory/.last_sync_version"
                  echo ""
                  echo -e "  ${CYAN}完整文档:${RESET} ${SKILL_DIR}/SKILL.md"
                  echo -e "  ${CYAN}快速上手:${RESET} ${SKILL_DIR}/references/quickstart.md"
                  echo "" ;;

    # Skip prompt
    skip_prompt)  echo -e "  ${CYAN}跳过此步骤?${RESET} [y/N]" ;;
    skip_ok)      echo -e "  ${YELLOW}⏭️  已跳过${RESET}" ;;

    # Errors
    err_reg_parse) echo -e "  ${RED}❌ 注册表解析失败${RESET}" ;;

    # Help
    help_title)   echo "agent-config-sync 安装向导 v1.5"
                  echo ""
                  echo "交互式向导，帮您配置 OpenClaw 跨 Agent 配置同步。" ;;
    help_usage)   echo "用法: bash wizard.sh [选项]" ;;
    help_opts)    echo ""
                  echo "选项:"
                  echo "  --auto          非交互模式: 自动检测所有内容 (无提示)"
                  echo "  --lang en|zh    语言选择 (默认: zh)"
                  echo "  --skip N[,N]    跳过指定步骤 (如 --skip 4)"
                  echo "  -h, --help      显示帮助" ;;

    # Misc
    abort)        echo ""; echo -e "  ${YELLOW}用户取消${RESET}";;
    press_enter)  echo ""; echo -n "按 Enter 继续...";;
    yn_default_y) echo -n " [Y/n]: ";;
    yn_default_n) echo -n " [y/N]: ";;
  esac
}

# ═══════════════════════════════════════════════════════════════
# Utility Functions
# ═══════════════════════════════════════════════════════════════

# Prompt user for Y/n (default yes)
ask_yn_default_y() {
  if [ "$AUTO_MODE" = true ]; then return 0; fi
  msg yn_default_y >&2
  echo -n "" >&2
  read -r answer
  case "$answer" in
    [Nn]|[Nn][Oo]) return 1 ;;
    *) return 0 ;;
  esac
}

# Prompt user for y/N (default no)
ask_yn_default_n() {
  if [ "$AUTO_MODE" = true ]; then return 1; fi
  msg yn_default_n >&2
  echo -n "" >&2
  read -r answer
  case "$answer" in
    [Yy]|[Yy][Ee][Ss]) return 0 ;;
    *) return 1 ;;
  esac
}

# Prompt user for number selection (1-based)
ask_number() {
  local max="$1" default="${2:-1}"
  if [ "$AUTO_MODE" = true ]; then echo "$default"; return 0; fi
  echo -n "  选择 [1-$max, 默认 $default]: " >&2
  read -r num
  if [ -z "$num" ]; then echo "$default"; return 0; fi
  if echo "$num" | grep -qE '^[0-9]+$' && [ "$num" -ge 1 ] && [ "$num" -le "$max" ]; then
    echo "$num"
  else
    echo "$default"
  fi
}

# Check if a step should be skipped
is_skipped() {
  local step="$1"
  echo "$SKIP_STEPS" | grep -qE "(^|,)$step(,|$)"
}

# Ask user to skip current step; returns 0 if skip
ask_skip() {
  local step="$1"
  if is_skipped "$step"; then
    msg skip_ok
    return 0
  fi
  if [ "$AUTO_MODE" = true ]; then return 1; fi
  msg skip_prompt
  if ask_yn_default_n; then
    msg skip_ok
    return 0
  fi
  return 1  # continue with step
}

# Simple JSON value extraction (no jq dependency)
json_val() {
  local path="$1" file="$2" key
  key=$(echo "$path" | awk -F. '{print $NF}')
  if echo "$path" | grep -q '\.'; then
    local section=$(echo "$path" | awk -F. '{print $1}')
    grep -A 50 "\"$section\"" "$file" 2>/dev/null | grep "\"$key\"" | head -1 | sed 's/.*: *"//;s/".*//'
  else
    grep "\"$key\"" "$file" 2>/dev/null | head -1 | sed 's/.*: *"//;s/".*//'
  fi
}

# Extract agent name from IDENTITY.md or SOUL.md
extract_agent_info() {
  local ws="$1"
  local agent_id=$(basename "$ws" | sed 's/workspace-//')
  local name="" role="" creature=""

  # Try IDENTITY.md first
  if [ -f "$ws/IDENTITY.md" ]; then
    name=$(grep -i '^\-\s*\*\*Name:\*\*' "$ws/IDENTITY.md" | head -1 | sed 's/.*Name:\*\*\s*//;s/\r//')
    role=$(grep -i '^\-\s*\*\*Role:\*\*' "$ws/IDENTITY.md" | head -1 | sed 's/.*Role:\*\*\s*//;s/\r//')
    creature=$(grep -i '^\-\s*\*\*Creature:\*\*' "$ws/IDENTITY.md" | head -1 | sed 's/.*Creature:\*\*\s*//;s/\r//')
  fi

  # Fallback to SOUL.md
  if [ -z "$name" ] && [ -f "$ws/SOUL.md" ]; then
    name=$(head -5 "$ws/SOUL.md" | grep -E "你是|You are" | head -1 | sed 's/.*你是[「「]//;s/[」」].*//;s/.*You are[「「]//;s/[」」].*//')
  fi

  # Fallback to directory name
  [ -z "$name" ] && name="$agent_id"
  [ -z "$role" ] && role="$creature"
  [ -z "$role" ] && role="Agent"

  echo "$agent_id|$name|$role"
}

# Detect all agent workspaces
detect_workspaces() {
  local ws_list=""
  for ws in "$WORKSPACE_PREFIX"*; do
    [ -d "$ws" ] || continue
    # Skip if no IDENTITY.md or SOUL.md (not a proper agent)
    if [ ! -f "$ws/IDENTITY.md" ] && [ ! -f "$ws/SOUL.md" ]; then
      # Still include if directory exists for OpenClaw
      [ -f "$ws/BOOTSTRAP.md" ] || [ -f "$ws/HEARTBEAT.md" ] || continue
    fi
    ws_list="$ws_list $ws"
  done
  echo "$ws_list" | xargs
}

# Detect master agent from workspaces
detect_master() {
  local ws_list="$1"

  # Priority detection: check for "amaster" or "AMaster" keyword
  for ws in $ws_list; do
    local agent_id=$(basename "$ws" | sed 's/workspace-//')
    case "$agent_id" in
      amaster|AMaster|master|Master|main|Main) echo "$agent_id"; return ;;
    esac
  done

  # Check SOUL.md / IDENTITY.md for master/主/coordinator keywords
  for ws in $ws_list; do
    local agent_id=$(basename "$ws" | sed 's/workspace-//')
    if grep -qiE 'master|coordinator|主助手|协同|协调' "$ws/IDENTITY.md" "$ws/SOUL.md" 2>/dev/null; then
      echo "$agent_id"; return
    fi
  done

  # Default: first workspace
  local first=$(echo "$ws_list" | awk '{print $1}')
  [ -n "$first" ] && basename "$first" | sed 's/workspace-//'
}

# ═══════════════════════════════════════════════════════════════
# Step 1: Detect Environment
# Outputs: agent data lines to stdout; all display messages to stderr
# Returns: data in $WIZARD_DATA_FILE
# ═══════════════════════════════════════════════════════════════
step1_detect_environment() {
  msg s1_title >&2

  # 1a. Check OpenClaw
  msg s1_check_oc >&2
  if command -v openclaw >/dev/null 2>&1 || [ -f "$OPENCLAW_DIR/openclaw.json" ] || [ -d "/usr/lib/node_modules/openclaw" ]; then
    msg s1_oc_ok >&2
  else
    msg s1_oc_fail >&2
    if ask_skip "1-oc"; then
      return 1
    fi
    return 1
  fi

  # 1b. Scan workspaces
  msg s1_scan_ws >&2
  local ws_list=$(detect_workspaces)

  if [ -z "$ws_list" ]; then
    msg s1_ws_none >&2
    if ask_skip "1-ws"; then
      return 1
    fi
    return 1
  fi

  # Count and display workspaces
  local ws_count=0
  for ws in $ws_list; do ws_count=$((ws_count + 1)); done
  msg s1_ws_found "$ws_count" >&2

  local agents_info=""
  local idx=0
  for ws in $ws_list; do
    idx=$((idx + 1))
    local info=$(extract_agent_info "$ws")
    local agent_id=$(echo "$info" | cut -d'|' -f1)
    local agent_name=$(echo "$info" | cut -d'|' -f2)
    local agent_role=$(echo "$info" | cut -d'|' -f3)
    msg s1_ws_item "$agent_id" "$agent_name" "$agent_role" >&2
    agents_info="${agents_info}${info}\n"
  done
  agents_info=$(echo -e "$agents_info" | grep -v '^$')

  # 1c. Detect master
  local master_agent=$(detect_master "$ws_list")
  msg s1_master_auto "$master_agent" >&2

  if [ "$AUTO_MODE" = false ]; then
    msg s1_master_ask >&2
    idx=0
    local master_opts=""
    for ws in $ws_list; do
      idx=$((idx + 1))
      local agent_id=$(basename "$ws" | sed 's/workspace-//')
      local name=$(echo "$agents_info" | grep "^$agent_id|" | head -1 | cut -d'|' -f2)
      echo "  [$idx] $agent_id ($name)" >&2
      master_opts="$master_opts $agent_id"
    done
    local choice=$(ask_number "$ws_count" 1)
    master_agent=$(echo "$master_opts" | cut -d' ' -f$((choice + 1)))
    [ -z "$master_agent" ] && master_agent=$(detect_master "$ws_list")
  fi

  # Set global data
  WIZARD_MASTER_AGENT="$master_agent"
  WIZARD_AGENTS_DATA="$agents_info"
  return 0
}

# ═══════════════════════════════════════════════════════════════
# Step 2: Configure Agent Registry
# ═══════════════════════════════════════════════════════════════
step2_configure_registry() {
  local master_agent="$1" agents_info="$2"
  msg s2_title

  # Check existing registry
  if [ -f "$REGISTRY_FILE" ] && [ -s "$REGISTRY_FILE" ]; then
    msg s2_reg_exists
    if [ "$AUTO_MODE" = true ]; then
      echo "  Using existing registry. To regenerate, delete it first:"
      echo "    rm $REGISTRY_FILE"
      echo "$REGISTRY_FILE"
      return 0
    fi

    # Show existing registry summary
    local existing_master=$(json_val "vars.master_agent" "$REGISTRY_FILE")
    local existing_count=$(grep -cE '^    "[a-z]' "$REGISTRY_FILE" 2>/dev/null || echo 0)
    echo "  Master: $existing_master  |  Agents: $existing_count"
    echo ""
    if ask_yn_default_n "  Override with auto-detected config?"; then
      # proceed to create
      :
    else
      echo "  Keeping existing registry."
      echo "$REGISTRY_FILE"
      return 0
    fi
  fi

  msg s2_reg_create

  # Build agent list
  local agent_count=0
  local agent_ids=""
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    local agent_id=$(echo "$line" | cut -d'|' -f1)
    local agent_name=$(echo "$line" | cut -d'|' -f2)
    local agent_role=$(echo "$line" | cut -d'|' -f3)
    agent_ids="$agent_ids $agent_id"

    # Workspace path
    local ws="${WORKSPACE_PREFIX}${agent_id}"
    msg s2_reg_item "$agent_id" "$agent_name" "$agent_role"
    msg s2_reg_path "$ws"
    echo ""

    agent_count=$((agent_count + 1))
  done <<< "$agents_info"

  msg s2_reg_master "$master_agent"

  if [ "$AUTO_MODE" = false ]; then
    msg s2_edit_opt
    local answer
    echo -n "  选择: "
    read -r answer
    case "$answer" in
      e|E)
        echo ""; echo "  Opening for manual edit..."
        # Generate a temp registry, let user edit, then save
        # For now, just inform
        echo "  Edit ${REGISTRY_FILE} and re-run wizard when ready."
        return 1
        ;;
      n|N)
        msg skip_ok
        return 1
        ;;
      *)
        # Y or anything else → confirm
        ;;
    esac
  fi

  # Generate agent-registry.json
  local reg_content=$(cat <<REGHDR
{
  "version": "1.5.0",
  "comment": "Auto-generated by setup wizard v1.5. Customize as needed.",
  "vars": {
    "workspace_root": "~/.openclaw",
    "master_agent": "${master_agent}",
    "master_memory": "\${vars.workspace_root}/workspace-\${vars.master_agent}/memory"
  },
  "agents": {
REGHDR
)

  local first_agent=true
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    local agent_id=$(echo "$line" | cut -d'|' -f1)
    local agent_name=$(echo "$line" | cut -d'|' -f2)
    local agent_role=$(echo "$line" | cut -d'|' -f3)

    if [ "$first_agent" = true ]; then
      first_agent=false
    else
      reg_content="$reg_content,"$'\n'
    fi

    reg_content="${reg_content}    \"${agent_id}\": {
      \"name\": \"${agent_name}\",
      \"role\": \"${agent_role}\",
      \"workspace\": \"\${vars.workspace_root}/workspace-${agent_id}\"
    }"
  done <<< "$agents_info"

  reg_content="${reg_content}"$'\n'"  },
  \"sync\": {
    \"sentinel_dir\": \"memory\",
    \"journal_file\": \".sync_journal.jsonl\",
    \"changelog_file\": \"CHANGELOG.md\",
    \"pending_prefix\": \"pending_sync\",
    \"max_changelog_sections\": 10,
    \"ttl_hours\": 24,
    \"dispatch_timeout_sec\": 120
  },
  \"self_protect\": {
    \"enabled\": true,
    \"skip_agents\": [\"agent-config-sync\"],
    \"isolated_sync\": true,
    \"blacklist\": [
      \"HEARTBEAT.md\",
      \"BOOTSTRAP.md\",
      \"SKILL.md\",
      \"scripts/\",
      \"SECURITY.md\",
      \"references/\",
      \"agent-registry.json\"
    ],
    \"sync_own_version_file\": \"skills/agent-config-sync/.sync_own_version\",
    \"allow_bootstrap_only\": true
  },
  \"batch\": {
    \"mode\": \"auto\",
    \"window_sec\": 300
  }
}
"

  echo "$reg_content" > "$REGISTRY_FILE"
  msg s2_reg_saved "$agent_count"
  echo "$REGISTRY_FILE"
}

# ═══════════════════════════════════════════════════════════════
# Step 3: Initialize Sync Infrastructure
# ═══════════════════════════════════════════════════════════════
step3_run_init() {
  msg s3_title

  msg s3_running
  if [ ! -x "$INIT_SCRIPT" ]; then
    echo "  ${RED}❌ init_sync.sh not found at: $INIT_SCRIPT${RESET}"
    return 1
  fi

  local exit_code=0
  if [ "$DRY_RUN_STEP3" = true ]; then
    bash "$INIT_SCRIPT" --confirm --lang "$LANG" --dry-run 2>&1 || exit_code=$?
  else
    bash "$INIT_SCRIPT" --confirm --lang "$LANG" 2>&1 || exit_code=$?
  fi

  case $exit_code in
    0) msg s3_ok; return 0 ;;
    *)
      msg s3_fail "$exit_code"
      if ask_yn_default_y "  Retry?"; then
        step3_run_init
      else
        return 1
      fi
      ;;
  esac
}

# ═══════════════════════════════════════════════════════════════
# Step 4: Integrate HEARTBEAT
# ═══════════════════════════════════════════════════════════════
step4_heartbeat_integration() {
  local master_agent="$1"
  msg s4_title

  local master_ws="${WORKSPACE_PREFIX}${master_agent}"
  if [ ! -d "$master_ws" ]; then
    msg s4_no_master
    return 1
  fi

  local hb_file="$master_ws/HEARTBEAT.md"

  # Check if already present
  if [ -f "$hb_file" ] && grep -q "agent-config-sync-check" "$hb_file" 2>/dev/null; then
    msg s4_already
    return 0
  fi

  msg s4_adding "$master_agent"

  # Determine item number: count existing numbered items
  local item_num=12
  if [ -f "$hb_file" ]; then
    local last_num=$(grep -oE '^[0-9]+\.' "$hb_file" | tail -1 | tr -d '.')
    if [ -n "$last_num" ] && [ "$last_num" -ge 0 ] 2>/dev/null; then
      item_num=$((last_num + 1))
    fi
  else
    touch "$hb_file"
  fi

  if [ "$LANG" = "en" ]; then
    cat >> "$hb_file" << 'HBEOF'

<!-- agent-config-sync-check v1.4 -->
## ⭐ Config Sync Check (run every heartbeat)
- [ ] Check for `pending_sync_*.md` files in workspace
  - Found and non-empty → read change summary, update MEMORY.md, delete files
  - Not found → skip
  - Verify SHA256 signature integrity
  - Check `memory/.agent_sync_version` — if < system version, request catch-up from Master
  - Delete expired pending_sync files (生成时间 > TTL 24h)
HBEOF
  else
    cat >> "$hb_file" << 'HBEOF'

<!-- agent-config-sync-check v1.4 -->
## ⭐ 配置同步检查（每次 heartbeat 执行）
- [ ] 检查工作目录下是否存在 `pending_sync_*.md` 文件
  - 存在且非空 → 读取变更摘要，更新 MEMORY.md，删除文件
  - 不存在 → 跳过
  - 验证 SHA256 签名完整性
  - 检查 `memory/.agent_sync_version` — 若落后于系统版本，向 Master 请求追赶
  - 删除过期的 pending_sync 文件（生成时间 > TTL 24h）
HBEOF
  fi

  msg s4_added "$master_ws"
  msg s4_note
  return 0
}

# ═══════════════════════════════════════════════════════════════
# Step 5: Completion Report
# ═══════════════════════════════════════════════════════════════
step5_completion_report() {
  local master_agent="$1" agents_info="$2"
  msg s5_title
  msg s5_summary

  local master_ws="${WORKSPACE_PREFIX}${master_agent}"

  # Version sentinel status
  msg s5_vers
  local current_file="$master_ws/memory/.current_system_version"
  if [ -f "$current_file" ]; then
    local current_ver=$(cat "$current_file" | tr -d '[:space:]')
    msg s5_vers_ok "Master ($master_agent)" "$current_ver"
  else
    msg s5_vers_miss "Master ($master_agent)"
  fi

  # Agent sync readiness
  msg s5_agent
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    local agent_id=$(echo "$line" | cut -d'|' -f1)
    local agent_name=$(echo "$line" | cut -d'|' -f2)

    local ws="${WORKSPACE_PREFIX}${agent_id}"

    if [ ! -d "$ws" ]; then
      msg s5_agent_miss "$agent_id" "$agent_name"
      continue
    fi

    # Check for files
    local ready_count=0
    [ -f "$ws/SYNC.md" ] && ready_count=$((ready_count + 1))
    [ -f "$ws/BOOTSTRAP.md" ] && grep -q "pending_sync_" "$ws/BOOTSTRAP.md" 2>/dev/null && ready_count=$((ready_count + 1))
    [ -f "$ws/HEARTBEAT.md" ] && grep -q "agent-config-sync" "$ws/HEARTBEAT.md" 2>/dev/null && ready_count=$((ready_count + 1))

    case $ready_count in
      3) msg s5_agent_ok "$agent_id" "$agent_name" ;;
      1|2) msg s5_agent_part "$agent_id" "$agent_name" ;;
      *) msg s5_agent_part "$agent_id" "$agent_name" ;;
    esac
  done <<< "$agents_info"

  # Files created summary
  msg s5_files
  echo "    ${SKILL_DIR}/references/agent-registry.json"
  echo "    ${master_ws}/memory/.current_system_version"
  echo "    ${master_ws}/memory/.last_sync_version"
  echo "    ${master_ws}/memory/.agent_sync_version"
  echo "    ${master_ws}/memory/CHANGELOG.md"
  echo "    ${master_ws}/memory/.sync_journal.jsonl"
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    local agent_id=$(echo "$line" | cut -d'|' -f1)
    local ws="${WORKSPACE_PREFIX}${agent_id}"
    [ -d "$ws" ] && echo "    ${ws}/SYNC.md"
    [ -d "$ws" ] && echo "    ${ws}/memory/.agent_sync_version"
    [ -d "$ws" ] && echo "    ${ws}/memory/.sync_snapshots/"
  done <<< "$agents_info"

  msg s5_next "$master_agent"
}

# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

# ── Parse arguments ───────────────────────────────────────────
show_help() {
  echo ""
  msg help_title
  echo ""
  msg help_usage
  msg help_opts
  echo ""
  echo "Examples:"
  echo "  bash wizard.sh                 # Interactive setup"
  echo "  bash wizard.sh --auto          # Auto-detect & run everything"
  echo "  bash wizard.sh --lang en       # English output"
  echo "  bash wizard.sh --skip 4        # Skip HEARTBEAT integration"
  echo "  bash wizard.sh --skip 1,4      # Skip environment check + HEARTBEAT"
  exit 0
}

for arg in "$@"; do
  case "$arg" in
    -h|--help) show_help ;;
    --auto)    AUTO_MODE=true ;;
    --lang)    ;;  # consumed below
    --lang=*)
      LANG="${arg#--lang=}"
      ;;
    --skip)
      ;;  # consumed below
    --skip=*)
      SKIP_STEPS="${arg#--skip=}"
      ;;
    --dry-run-step3)
      DRY_RUN_STEP3=true
      ;;
    *)
      if [ "$prev" = "--lang" ]; then
        LANG="$arg"
      elif [ "$prev" = "--skip" ]; then
        SKIP_STEPS="$arg"
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

# ── Main execution ────────────────────────────────────────────
if [ "$AUTO_MODE" = true ]; then
  msg auto_banner
  echo ""
else
  msg banner
  msg welcome
fi

# Global data holders (not captured from stdout)
WIZARD_MASTER_AGENT=""
WIZARD_AGENTS_DATA=""

# Step 1: Detect Environment
if is_skipped "1"; then
  msg skip_ok
else
  if ! step1_detect_environment; then
    echo ""; msg abort; exit 1
  fi
fi

# master_agent and agents_info are set globally by step1
master_agent="$WIZARD_MASTER_AGENT"
agents_info="$WIZARD_AGENTS_DATA"
[ -z "$master_agent" ] && { msg abort; exit 1; }

# Step 2: Configure Registry
if is_skipped "2"; then
  msg skip_ok
else
  if ! step2_configure_registry "$master_agent" "$agents_info"; then
    echo "  Using existing registry if available..." >&2
    [ ! -f "$REGISTRY_FILE" ] && { msg abort; exit 1; }
  fi
fi

# Step 3: Initialize
if is_skipped "3"; then
  msg skip_ok
else
  if ! step3_run_init; then
    echo ""
    echo "  ${YELLOW}Initialization incomplete. You can run it later:${RESET}"
    echo "    bash $INIT_SCRIPT --confirm --lang $LANG"
    if ask_yn_default_n "  Continue to next step anyway?"; then
      msg abort; exit 1
    fi
  fi
fi

# Step 4: HEARTBEAT Integration
if is_skipped "4"; then
  msg skip_ok
else
  step4_heartbeat_integration "$master_agent" || true
fi

# Step 5: Completion Report
if is_skipped "5"; then
  msg skip_ok
else
  step5_completion_report "$master_agent" "$agents_info"
fi

exit 0
