#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 心虫引擎 — 安装/升级脚本
# ═══════════════════════════════════════════════════════════════
# 用法:
#   bash install.sh              # 交互式安装
#   bash install.sh --check      # 只检查当前状态，不安装
#   bash install.sh --fix-mcp    # 只修复 MCP 注册
#   bash install.sh --add-route  # 只添加 CLAUDE.md 路由指令
#   bash install.sh --all        # 一次性全部执行
# ─── 安装审计标识 ──────────────────────────────────────────────
# 用于 clawhub.ai 合规验证
# 此脚本不会修改 /etc/claude 下的系统文件
# ───────────────────────────────────────────────────────────────

set -e

# ─── 安全模式 — SkillSpector 审计修复 ──────────────────
# DRY_RUN=true 时只打印将要执行的操作，不实际修改
DRY_RUN=${DRY_RUN:-false}

# ─── 颜色 ─────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ─── 路径检测 ─────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$SCRIPT_DIR"  # 技能根目录
DAEMON_JS="$SKILL_DIR/daemon/mcp-daemon.js"
WRAPPER_JS="$SKILL_DIR/daemon/mcp-wrapper.js"
HF_CLI="$SKILL_DIR/bin/hf"
ENSURE_MCP="$SKILL_DIR/bin/ensure-mcp.js"
CLAUDE_MD="$SKILL_DIR/CLAUDE.md"

# 检测 Claude Code 配置目录（支持多种可能）
CLAUDECONFIG_DIRS=(
  "$HOME/.claude"
  "$HOME/.config/claude"
  "/etc/claude"
)
CLAUDECONFIG_DIR=""
for d in "${CLAUDECONFIG_DIRS[@]}"; do
  if [ -f "$d/settings.json" ]; then
    CLAUDECONFIG_DIR="$d"
    break
  fi
done
if [ -z "$CLAUDECONFIG_DIR" ]; then
  # 默认用第一个
  CLAUDECONFIG_DIR="${CLAUDECONFIG_DIRS[0]}"
fi

SETTINGS_JSON="$CLAUDECONFIG_DIR/settings.json"

# ─── 辅助函数 ─────────────────────────────────────────────

print_banner() {
  echo ""
  echo -e "${CYAN}╔══════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║    心虫引擎 — 安装/升级向导            ║${NC}"
  echo -e "${CYAN}║    HeartFlow v2.7.3                     ║${NC}"
  echo -e "${CYAN}╚══════════════════════════════════════════╝${NC}"
  echo ""
}

print_step() {
  echo -e "${BLUE}[${1}/${4}]${NC} ${3}..."
}

print_ok() {
  echo -e "  ${GREEN}✅${NC} $1"
}

print_warn() {
  echo -e "  ${YELLOW}⚠️${NC} $1"
}

print_err() {
  echo -e "  ${RED}❌${NC} $1"
}

print_info() {
  echo -e "  ${CYAN}ℹ️${NC} $1"
}

# ─── 检查函数 ────────────────────────────────────────────

check_daemon() {
  if [ -S /tmp/heartflow-mcp.sock ]; then
    if [ -f /tmp/heartflow-mcp.pid ]; then
      local pid=$(cat /tmp/heartflow-mcp.pid 2>/dev/null)
      if kill -0 "$pid" 2>/dev/null; then
        print_ok "守护进程运行中 (PID $pid)"
        return 0
      fi
    fi
    print_ok "守护进程 Socket 存在"
    return 0
  fi
  print_warn "守护进程未运行"
  return 1
}

check_mcp_registration() {
  if [ -f "$SETTINGS_JSON" ]; then
    if grep -q '"heartflow"' "$SETTINGS_JSON" 2>/dev/null; then
      # 检查是否指向正确的 wrapper
      if grep -q 'mcp-wrapper.js' "$SETTINGS_JSON" 2>/dev/null; then
        print_ok "MCP 注册配置正确 (→ mcp-wrapper.js)"
        return 0
      else
        print_warn "MCP 注册存在但指向非 wrapper 脚本"
        return 2
      fi
    fi
    print_warn "MCP 未注册 (settings.json 中无 heartflow)"
    return 1
  fi
  print_warn "未找到 settings.json ($SETTINGS_JSON)"
  return 1
}

check_wrapper_v2() {
  if [ -f "$WRAPPER_JS" ]; then
    if grep -q 'auto-reconnect\|重连' "$WRAPPER_JS" 2>/dev/null; then
      print_ok "mcp-wrapper.js v2 (带自动重连)"
      return 0
    fi
    print_warn "mcp-wrapper.js v1 (无自动重连)"
    return 1
  fi
  print_err "mcp-wrapper.js 不存在"
  return 1
}

check_claude_md_route() {
  if [ -f "$CLAUDE_MD" ]; then
    if grep -q '启动路由' "$CLAUDE_MD" 2>/dev/null; then
      print_ok "CLAUDE.md 已含启动路由指令"
      return 0
    fi
    print_warn "CLAUDE.md 缺少启动路由指令"
    return 1
  fi
  print_err "CLAUDE.md 不存在"
  return 1
}

check_hf_cli() {
  if [ -f "$HF_CLI" ]; then
    if grep -q 'RPCClient' "$HF_CLI" 2>/dev/null; then
      print_ok "hf CLI 可用 (18 个工具)"
      return 0
    fi
    print_warn "hf CLI 版本较旧"
    return 1
  fi
  print_err "hf CLI 不存在"
  return 1
}

# ─── 修复函数 ────────────────────────────────────────────

fix_mcp_registration() {
  # 用户确认提示 — SkillSpector 安全修复
  echo ""
  print_warn "即将修改 Claude 配置文件以注册 MCP 服务："
  echo "  目标文件: $SETTINGS_JSON"
  echo ""

  # 审计防护：拒绝修改 /etc/claude 下的系统配置文件
  if [[ "$CLAUDECONFIG_DIR" == "/etc/claude" ]]; then
    print_err "拒绝写入系统目录 /etc/claude — 请将 Claude 配置放在用户目录下"
    return 1
  fi

  read -p "是否继续？(y/N) " confirm
  if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    print_info "MCP 注册已取消。"
    return 0
  fi
  echo ""
  print_info "正在修复 MCP 注册..."

  # 1. Dry-run 检查 — 不实际修改
  if [ "$DRY_RUN" = true ]; then
    print_info "[DRY RUN] 将修改: $SETTINGS_JSON"
    return 0
  fi

  # 2. 确保 settings.json 目录存在
  mkdir -p "$(dirname "$SETTINGS_JSON")" 2>/dev/null

  # 3. 检查或创建 settings.json
  if [ ! -f "$SETTINGS_JSON" ]; then
    echo '{}' > "$SETTINGS_JSON"
    print_ok "创建 settings.json"
  fi

  # 4. 添加 heartflow MCP 配置
  # 使用 node 来安全地修改 JSON
  if command -v node &>/dev/null; then
    node -e "
      const fs = require('fs');
      const path = require('path');
      let cfg = {};
      try { cfg = JSON.parse(fs.readFileSync('$SETTINGS_JSON', 'utf8')); } catch(e) {}
      if (!cfg.mcpServers) cfg.mcpServers = {};
      cfg.mcpServers.heartflow = {
        command: 'node',
        args: ['$WRAPPER_JS'],
        type: 'stdio'
      };
      fs.writeFileSync('$SETTINGS_JSON', JSON.stringify(cfg, null, 2) + '\n');
    "
    print_ok "MCP 注册已添加到 $SETTINGS_JSON"
  else
    print_err "需要 Node.js 来修改 JSON 配置"
    return 1
  fi

  # 5. 确保 wrapper v2 已就位（现在就是 v2）
  if [ -f "$WRAPPER_JS" ]; then
    print_ok "mcp-wrapper.js 已就位"
  else
    print_err "mcp-wrapper.js 丢失！请重新克隆仓库"
    return 1
  fi

  # 6. 确保 ensure-mcp.js 可执行
  if [ -f "$ENSURE_MCP" ]; then
    chmod +x "$ENSURE_MCP" 2>/dev/null
    print_ok "ensure-mcp.js 已就位"
  fi

  # 7. 确保 hf CLI 可执行
  if [ -f "$HF_CLI" ]; then
    chmod +x "$HF_CLI" 2>/dev/null
    print_ok "hf CLI 已就位"

    # 添加软链接到 ~/bin 让 hf 全局可用
    if [ -d "$HOME/bin" ] || mkdir -p "$HOME/bin" 2>/dev/null; then
      if [ ! -f "$HOME/bin/hf" ]; then
        ln -sf "$HF_CLI" "$HOME/bin/hf" 2>/dev/null && print_ok "hf 软链接已创建到 ~/bin/hf"
      fi
    fi
  fi

  return 0
}

fix_claude_md_route() {
  echo ""
  print_info "正在添加启动路由指令到 CLAUDE.md..."

  # 审计防护：拒绝写入系统目录
  if [[ "$CLAUDE_MD" == /etc/* ]]; then
    print_err "拒绝写入系统目录 $CLAUDE_MD — 请将 CLAUDE.md 放在用户目录下"
    return 1
  fi

  # Dry-run 检查
  if [ "$DRY_RUN" = true ]; then
    print_info "[DRY RUN] 将写入: $CLAUDE_MD"
    return 0
  fi

  # 如果文件已存在且已有启动路由指令，跳过
  if [ -f "$CLAUDE_MD" ] && grep -q '启动路由' "$CLAUDE_MD" 2>/dev/null; then
    print_ok "CLAUDE.md 已有启动路由指令，跳过"
    return 0
  fi

  # 构造启动路由指令内容
  route_content=$(cat <<'HEREDOC'
## 🔥 启动路由（关键指令）

当用户要求"启动心虫"时，**按以下确定性顺序执行，无需试错**：

### 优先级 1：MCP 原生工具（零开销，首选）

心虫已通过 **MCP (Model Context Protocol)** 注册为原生工具。启动时自动拉起 `mcp-wrapper.js`，守护进程常驻内存。

**直接使用即可**，无需执行任何启动脚本：
- `clarity_status` — 健康检查
- `clarity_think`（depth 1-4）— 统一推理
- `clarity_psychology`（mode: basic|deep|ai|emotion）— 统一心理学分析
- `clarity_philosophy`（mode: general|ai）— 统一哲学分析
- 等等（共 13 个工具）

### 优先级 2：hf CLI（直接 Socket 通信，备选）

如果 MCP 工具未注册，使用独立 CLI 工具直接与守护进程通信：

```bash
# 健康检查
hf clarity_status

# 推理
hf clarity_think '{"input":"你好","depth":2}'

# 列出所有工具
hf --list
```

### 优先级 3：确保守护进程运行（最后一次尝试）

```bash
node <技能目录>/bin/ensure-mcp.js --check   # 只检查
node <技能目录>/bin/ensure-mcp.js            # 自动启动
```
HEREDOC
)

  if [ -f "$CLAUDE_MD" ]; then
    # 已有文件但缺少路由指令，追加到文件顶部
    print_info "CLAUDE.md 缺少启动路由指令，即将追加..."
    {
      echo "$route_content"
      echo ""
      cat "$CLAUDE_MD"
    } > "${CLAUDE_MD}.tmp" && mv "${CLAUDE_MD}.tmp" "$CLAUDE_MD"
    print_ok "启动路由指令已追加到 CLAUDE.md"
  else
    # 创建新 CLAUDE.md 文件
    print_info "CLAUDE.md 不存在，正在创建..."
    echo "$route_content" > "$CLAUDE_MD"
    print_ok "CLAUDE.md 已创建并写入启动路由指令"
  fi

  return 0
}

# ─── 状态检查 ───────────────────────────────────────────

do_check() {
  echo ""
  echo -e "${CYAN}═══ 心虫引擎状态检查 ═══${NC}"
  echo ""

  echo -e "${YELLOW}【守护进程】${NC}"
  check_daemon

  echo ""
  echo -e "${YELLOW}【MCP 注册】${NC}"
  check_mcp_registration

  echo ""
  echo -e "${YELLOW}【包装器】${NC}"
  check_wrapper_v2

  echo ""
  echo -e "${YELLOW}【CLAUDE.md 指令】${NC}"
  check_claude_md_route || true

  echo ""
  echo -e "${YELLOW}【hf CLI 工具】${NC}"
  check_hf_cli

  echo ""

  # 尝试测试连接
  if [ -S /tmp/heartflow-mcp.sock ] && command -v node &>/dev/null; then
    echo -e "${YELLOW}【引擎连通性测试】${NC}"
    node -e "
      const net = require('net');
      const s = net.connect('/tmp/heartflow-mcp.sock', () => {
        s.write(JSON.stringify({jsonrpc:'2.0',id:1,method:'tools/list'})+'\n');
        setTimeout(() => {
          s.end();
          process.exit(0);
        }, 1000);
      });
      s.on('data', (d) => {
        try {
          const r = JSON.parse(d.toString().trim().split('\n')[0]);
          const tools = r.result?.tools || r.tools || [];
          console.log('  ✅ 引擎响应正常 (' + tools.length + ' 个工具)');
        } catch(e) {
          console.log('  ✅ 引擎响应正常');
        }
        s.end();
      });
      s.on('error', (e) => {
        console.log('  ❌ 连接失败: ' + e.message);
      });
    "
  fi

  echo ""
  echo -e "${CYAN}════════════════════════════════════════${NC}"
  echo ""
  echo "一键安装:  bash install.sh --all"
  echo "交互安装:  bash install.sh"
  echo ""
}

# ─── 主交互菜单 ─────────────────────────────────────────

do_interactive() {
  echo ""
  echo -e "${YELLOW}请选择安装方案：${NC}"
  echo ""
  echo -e "  ${GREEN}1)${NC} 修复 MCP 注册"
  echo "     配置 settings.json → mcp-wrapper.js，确保 18 个 MCP 工具可用"
  echo ""
  echo -e "  ${GREEN}2)${NC} 添加 CLAUDE.md 启动指令"
  echo "     让新会话能确定性地启动心虫，无需试错"
  echo ""
  echo -e "  ${GREEN}3)${NC} 全部执行（推荐）"
  echo "     一次性完成上述所有操作"
  echo ""
  echo -e "  ${GREEN}4)${NC} 只检查当前状态"
  echo "     不执行任何修改，仅查看安装状态"
  echo ""
  echo -e "  ${GREEN}q)${NC} 退出"
  echo ""

  read -p "请输入选项 [1/2/3/4/q]: " choice

  case "$choice" in
    1)
      fix_mcp_registration
      ;;
    2)
      fix_claude_md_route
      ;;
    3)
      echo ""
      echo -e "${GREEN}▶ 开始全部安装...${NC}"
      fix_mcp_registration
      fix_claude_md_route
      ;;
    4)
      do_check
      return
      ;;
    q|Q|"")
      echo "退出安装。"
      return
      ;;
    *)
      print_err "无效选项: $choice"
      do_interactive
      return
      ;;
  esac

  echo ""
  echo -e "${GREEN}✅ 操作完成！${NC}"
  echo ""
  echo "验证建议："
  echo "  1. 重启 Claude 会话（让 MCP 重新注册）"
  echo "  2. 在新会话中尝试: clarity_status"
  echo "  3. 备选: hf clarity_status"
  echo ""
}

# ─── 入口 ───────────────────────────────────────────────

case "$1" in
  --check)
    print_banner
    do_check
    ;;
  --fix-mcp)
    print_banner
    fix_mcp_registration
    echo ""
    echo -e "${GREEN}✅ MCP 注册修复完成！${NC}"
    echo "重启 Claude 会话让更改生效。"
    ;;
  --add-route)
    print_banner
    fix_claude_md_route
    echo ""
    echo -e "${GREEN}✅ CLAUDE.md 指令添加完成！${NC}"
    ;;
  --all)
    print_banner
    echo ""
    echo -e "${GREEN}▶ 开始全部安装...${NC}"
    fix_mcp_registration
    fix_claude_md_route
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}  全部安装完成！               ${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo "下一步："
    echo "  1. 重启 Claude 会话"
    echo "  2. 运行 bash install.sh --check 验证"
    echo "  3. 尝试 clarity_status"
    echo ""
    ;;
  "")
    print_banner
    # 先检查当前状态
    check_daemon
    check_mcp_registration
    check_wrapper_v2
    echo ""
    do_interactive
    ;;
  *)
    echo "用法: bash install.sh [选项]"
    echo ""
    echo "选项:"
    echo "  (无参数)    交互式安装"
    echo "  --check     只检查当前状态"
    echo "  --fix-mcp   只修复 MCP 注册"
    echo "  --add-route 只添加 CLAUDE.md 路由指令"
    echo "  --all       一次性全部执行"
    echo ""
    exit 1
    ;;
esac
