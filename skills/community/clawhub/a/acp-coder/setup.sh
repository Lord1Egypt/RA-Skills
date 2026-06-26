#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# acp-coder — 一键安装脚本
# 配置 OpenClaw ACP（acpx 已内置于 openclaw）
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ----------------------------------------------------------
# 0. 前置检查
# ----------------------------------------------------------
if ! command -v openclaw &>/dev/null; then
  fail "未找到 openclaw 命令。请先安装 OpenClaw 再运行此脚本。"
fi
if ! command -v node &>/dev/null; then
  fail "未找到 node 命令。请先安装 Node.js。"
fi

# ----------------------------------------------------------
# 1. 检测已安装的 coding agent
# ----------------------------------------------------------
info "检测已安装的 coding agent..."

AGENTS=()

check_agent() {
  local name=$1 cmd=$2 label=$3
  if command -v "$cmd" &>/dev/null; then
    AGENTS+=("$name")
    ok "$name ($label)"
  fi
}

check_agent "claude"   "claude"   "Claude Code"
check_agent "codex"    "codex"    "Codex CLI"

# codex-acp 平台二进制（optional dep，npx 默认跳过，需手动补装）
for agent in "${AGENTS[@]}"; do
  if [ "$agent" = "codex" ]; then
    PLATFORM="$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m | sed 's/x86_64/x64/;s/aarch64/arm64/')"
    PKG="@zed-industries/codex-acp-${PLATFORM}"
    if ! npm list -g "$PKG" --depth=0 2>/dev/null | grep -q "$PKG"; then
      info "安装 codex-acp 平台二进制 ($PKG)..."
      npm install -g "$PKG" --registry=https://registry.npmmirror.com \
        && ok "已安装 $PKG" \
        || warn "安装失败，codex 可能无法通过 ACP 启动，请手动执行: npm install -g $PKG"
    else
      ok "codex-acp 平台二进制已就绪 ($PKG)"
    fi
  fi
done
check_agent "gemini"   "gemini"   "Gemini CLI"
check_agent "opencode" "opencode" "OpenCode"
check_agent "kimi"     "kimi"     "Kimi CLI"
check_agent "aider"    "aider"    "Aider"

if [ ${#AGENTS[@]} -eq 0 ]; then
  fail "未检测到任何 coding agent。请至少安装一个，如:\n  npm install -g @anthropic-ai/claude-code"
fi

# 构建白名单 JSON（纯 bash，不依赖 jq）
ALLOW_JSON="["
for i in "${!AGENTS[@]}"; do
  [ "$i" -gt 0 ] && ALLOW_JSON+=","
  ALLOW_JSON+="\"${AGENTS[$i]}\""
done
ALLOW_JSON+="]"

DEFAULT_AGENT="${AGENTS[0]}"

info "可用 agent: ${AGENTS[*]}  (默认: $DEFAULT_AGENT)"

# ----------------------------------------------------------
# 2. 配置 OpenClaw
# ----------------------------------------------------------
info "配置 OpenClaw..."

# acpx 插件（使用 openclaw 内置 acpx）
openclaw config set plugins.entries.acpx.enabled true
openclaw config set plugins.entries.acpx.config.permissionMode approve-all

# ACP
openclaw config set acp.enabled true
openclaw config set acp.backend acpx
openclaw config set acp.defaultAgent "$DEFAULT_AGENT"

# 合并 allowedAgents：读取已有值，追加新检测到的 agent，不覆盖用户手动配置
MERGED_JSON=$(node -e "
  const { execSync } = require('child_process');
  let existing = [];
  try {
    const out = execSync('openclaw config get acp.allowedAgents', { encoding: 'utf8' }).trim();
    existing = JSON.parse(out);
  } catch {}
  const incoming = $ALLOW_JSON;
  const merged = [...new Set([...existing, ...incoming])];
  console.log(JSON.stringify(merged));
" 2>/dev/null || echo "$ALLOW_JSON")
openclaw config set acp.allowedAgents "$MERGED_JSON"

# 跨 session 访问
openclaw config set tools.sessions.visibility all
openclaw config set tools.agentToAgent.enabled true

ok "OpenClaw 配置完成"

# ----------------------------------------------------------
# 3. 配置 heartbeat（streamTo 自动回调必需）
# ----------------------------------------------------------
# sessions_spawn streamTo:"parent" + sessions_yield 实现子 agent 完成后自动唤醒父 session。
# 前提：父 session 所属的 agent 必须在 agents.list 里配置 heartbeat.target = "last"。
# 若无此配置，回调通知会被丢弃，需用户手动发消息才能继续。
info "配置 heartbeat（子 agent 完成自动回调）..."

OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

if [ ! -f "$OPENCLAW_CONFIG" ]; then
  warn "未找到 $OPENCLAW_CONFIG，跳过 heartbeat 配置（可在 openclaw 初始化后重新运行此脚本）"
else
  node -e "
    const fs = require('fs');
    const cfg = JSON.parse(fs.readFileSync('$OPENCLAW_CONFIG', 'utf8'));
    const list = cfg.agents?.list ?? [];
    let changed = 0;
    for (const entry of list) {
      if (!entry.heartbeat) {
        entry.heartbeat = { every: '30m', target: 'last' };
        changed++;
      } else if (!entry.heartbeat.target) {
        entry.heartbeat.target = 'last';
        changed++;
      }
    }
    if (changed > 0) {
      fs.writeFileSync('$OPENCLAW_CONFIG', JSON.stringify(cfg, null, 2) + '\n');
      console.log('已为 ' + changed + ' 个 agent 添加 heartbeat 配置');
    } else {
      console.log('heartbeat 已配置，跳过');
    }
  " && ok "heartbeat 配置完成" || warn "heartbeat 配置失败，请手动在 openclaw.json 的 agents.list 每个 agent 下添加: { \"heartbeat\": { \"every\": \"30m\", \"target\": \"last\" } }"
fi

# ----------------------------------------------------------
# 4. 重启 daemon
# ----------------------------------------------------------
info "重启 OpenClaw daemon..."

if openclaw daemon restart 2>/dev/null; then
  ok "daemon 已重启"
else
  warn "daemon 重启失败（可能未在运行），请手动执行: openclaw daemon restart"
fi

# ----------------------------------------------------------
# 5. 验证
# ----------------------------------------------------------
info "配置校验（仅验证配置已写入，不验证 ACP runtime 连通性）..."

sleep 2

# 注意：这里只检查配置是否正确写入 openclaw.json，不代表 ACP runtime 能成功拉起 agent。
# 连通性验证需要在 openclaw web UI 或聊天中实际 spawn 一个 agent 才能确认。
if openclaw config get acp.enabled 2>/dev/null | grep -q "true" && \
   openclaw config get acp.backend 2>/dev/null | grep -q "acpx"; then
  ok "配置已写入：acp.enabled=true, acp.backend=acpx, allowedAgents=$(openclaw config get acp.allowedAgents 2>/dev/null)"
else
  warn "配置校验失败，请手动检查:\n  openclaw config get acp.enabled\n  openclaw config get acp.backend"
fi

# ----------------------------------------------------------
# 完成
# ----------------------------------------------------------
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  acp-coder 安装完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "  可用 agent:  ${AGENTS[*]}"
echo "  默认 agent:  $DEFAULT_AGENT"
echo "  Workspace:   ~/.openclaw/workspace"
echo ""
echo "  使用方式："
echo "    - 通过 Web UI / Telegram 发送代码任务，自动触发"
echo "    - 或手动发送 /acp-coder <任务描述>"
echo ""
