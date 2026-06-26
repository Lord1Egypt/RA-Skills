#!/usr/bin/env bash
# browser-harness skill — single entry, dispatches subcommands to bhts.
#
# Usage:
#   scripts/run.sh setup
#   scripts/run.sh doctor
#   scripts/run.sh js   '<expr>'
#   scripts/run.sh exec '<bhts snippet>'
#   scripts/run.sh shot [--full] [path]
#   scripts/run.sh page
#   scripts/run.sh tabs
#   scripts/run.sh open '<url>'
#   scripts/run.sh switch '<keyword>'
#   scripts/run.sh upload '<selector>' '<abs-path>'
#   scripts/run.sh click  <x> <y>
#   scripts/run.sh type   '<text>'
#   scripts/run.sh key    '<Enter|Tab|...>'
#   scripts/run.sh scroll <dy>
#   scripts/run.sh helpers
#   scripts/run.sh raw    -c '<...>'
#   scripts/run.sh help

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RUNNER="$SCRIPT_DIR/lib/runner.mjs"

# Pinned upstream versions — keep in sync with config.json::capabilities.supplyChain
# and SKILL.md "上游版本钉死". Bumping these requires a new skill release with
# upstream diff audit (capabilities.supplyChain.policy.allowFloatingVersions=false).
BHTS_PKG_VERSION="0.1.1"
PYTHON_BH_PKG_VERSION="0.0.1"

blue()  { printf "\033[1;34m==>\033[0m %s\n" "$*"; }
green() { printf "\033[1;32m ok\033[0m %s\n" "$*"; }
warn()  { printf "\033[1;33m!!!\033[0m %s\n" "$*" >&2; }
fail()  { printf "\033[1;31mERR\033[0m %s\n" "$*" >&2; exit 1; }

show_help() {
  cat <<'EOF'
browser-harness skill v0.2.3
==> 让 LLM Agent 通过 CDP 接管用户已登录的真实 Chrome
==> 默认 sensitive-deny + 元数据审计日志 + 可选 BH_PUBLIC_ONLY 硬隔离

用法:
  scripts/run.sh <subcommand> [args] [--i-understand-sensitive]

子命令:
  setup                          一次性安装 + 引导接管 Chrome（钉死版本 + --ignore-scripts）
  doctor                         体检：依赖 / 守护进程 / 当前页
  stop                           停掉 browser-harness 守护进程（用完别让它常驻）

  js   '<expr>'                  在当前标签跑一段 JS，返回 JSON 结果
  exec '<snippet>'               跑任意 bhts -c snippet（bh / h 已就绪）
  raw  -c '<snippet>' ...        透传到 bhts；默认禁用，需 BH_RAW_OK=1 显式开启
                                 （绕过 sensitive-deny + in-snippet policy gate；
                                 仅记 metadata 审计，不做 URL 检查）

  page                           当前页 url/title/viewport/scroll/pageSize（只读，免检）
  tabs                           列出真实标签（只读，免检）
  open '<url>'                   新建标签 + waitForLoad（URL 过 sensitive-deny 检查）
  switch '<keyword>'             切到 url/title 含关键词的标签
  shot [--full] [path]           截图（默认 ./shot.png）

  click <x> <y>                  视口坐标点击（不推荐）
  type  '<text>'                 在焦点元素插入文本
  key   '<Enter|Tab|Esc|...>'    按下单键
  scroll <dy>                    滚动 dy 像素（负值向上）

  upload '<selector>' '<abs-path>'   给 input[type=file] 设文件
  helpers                            列已注册的自定义 helpers
  help                               本帮助

每命令开关:
  --i-understand-sensitive       本次允许操作匹配 alwaysSensitiveHostPatterns
                                 的页面（银行/邮箱/内网/admin 等）。
                                 等价于 BH_ALLOW_SENSITIVE=1 但只对当前命令生效。

环境变量:
  BU_NAME             守护进程命名空间，默认 default（多 Agent 并行用）
  BH_AGENT_WORKSPACE  agent-workspace 目录覆盖
  BH_ALLOW_SENSITIVE  =1 全局允许敏感站点（不推荐；优先用 --i-understand-sensitive）
  BH_PUBLIC_ONLY      =1 硬隔离模式：仅允许 publicSites allow-list 内域名
  BH_AUDIT_LOG        覆盖审计日志路径（默认 ~/.cache/browser-harness/skill-audit.log；
                      置空字符串可禁用）
  BH_RAW_OK           =1 启用 raw 子命令（默认禁用，避免后门）；raw 仍记 metadata
                      审计但绕过 URL 策略门，是用户接管全部责任的逃生口

依赖:
  node >= 20.6.0、python >= 3.10、uv、bhts、browser-harness（PATH）
  缺什么 `scripts/run.sh setup` 会指引安装

详细 API: ./reference.md   常见任务: ./examples.md   安装: ./setup.md
安全策略 / 审计 / 默认拒绝模式: ./SKILL.md 的"安全说明"节
EOF
}

# --- setup ---------------------------------------------------------------
do_setup() {
  blue "browser-harness skill setup"
  printf "\n"

  # 1. node
  if ! command -v node >/dev/null 2>&1; then
    warn "node 未安装。请先装 Node.js >= 20.6.0:"
    printf "    https://nodejs.org/  或  nvm install 20\n"
    fail "装好 node 后重跑: scripts/run.sh setup"
  fi
  NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
  NODE_MINOR="$(node -p 'process.versions.node.split(".")[1]')"
  if [ "$NODE_MAJOR" -lt 20 ] || { [ "$NODE_MAJOR" -eq 20 ] && [ "$NODE_MINOR" -lt 6 ]; }; then
    fail "node 版本太低（$(node --version)），需要 >= 20.6.0"
  fi
  green "node $(node --version)"

  # 2. uv
  if ! command -v uv >/dev/null 2>&1; then
    warn "uv 未安装。任选一种:"
    printf "    curl -LsSf https://astral.sh/uv/install.sh | sh\n"
    printf "    brew install uv\n"
    fail "装好 uv 后重跑: scripts/run.sh setup"
  fi
  green "uv $(uv --version | awk '{print $2}')"

  # 3. browser-harness-ts (npm global) — pinned + --ignore-scripts
  CURRENT_BHTS=""
  if command -v bhts >/dev/null 2>&1; then
    CURRENT_BHTS="$(bhts --version 2>/dev/null | awk '{print $2}' || echo '')"
  fi
  if [ "$CURRENT_BHTS" != "$BHTS_PKG_VERSION" ]; then
    blue "npm install -g browser-harness-ts@${BHTS_PKG_VERSION} --ignore-scripts"
    blue "  (--ignore-scripts: 拒绝包内 install/postinstall hook，降低供应链注入面)"
    npm install -g "browser-harness-ts@${BHTS_PKG_VERSION}" --ignore-scripts
  else
    green "bhts already at pinned version ${BHTS_PKG_VERSION}"
  fi
  if ! command -v bhts >/dev/null 2>&1; then
    warn "bhts 仍不在 PATH。把 npm 全局 bin 加进 PATH:"
    printf '    echo '\''export PATH="$(npm prefix -g)/bin:$PATH"'\'' >> ~/.zshrc && source ~/.zshrc\n'
    fail "PATH 修好后重跑"
  fi
  INSTALLED_BHTS="$(bhts --version 2>/dev/null | awk '{print $2}' || echo '?')"
  if [ "$INSTALLED_BHTS" != "$BHTS_PKG_VERSION" ]; then
    warn "bhts 安装版本 ${INSTALLED_BHTS} 不匹配钉死版本 ${BHTS_PKG_VERSION}"
    warn "请手动: npm install -g browser-harness-ts@${BHTS_PKG_VERSION} --ignore-scripts"
    fail "版本不匹配，setup 中止"
  fi
  green "bhts ${INSTALLED_BHTS} ($(command -v bhts))"

  # 4. browser-harness (Python via uv tool) — pinned
  CURRENT_PYBH=""
  if command -v browser-harness >/dev/null 2>&1; then
    CURRENT_PYBH="$(browser-harness --version 2>/dev/null || echo '')"
  fi
  if [ "$CURRENT_PYBH" != "$PYTHON_BH_PKG_VERSION" ]; then
    blue "uv tool install --force browser-harness==${PYTHON_BH_PKG_VERSION}"
    uv tool install --force "browser-harness==${PYTHON_BH_PKG_VERSION}"
  else
    green "browser-harness already at pinned version ${PYTHON_BH_PKG_VERSION}"
  fi
  if ! command -v browser-harness >/dev/null 2>&1; then
    warn "browser-harness 仍不在 PATH。把 uv tool bin 加进 PATH:"
    printf '    echo '\''export PATH="$HOME/.local/bin:$PATH"'\'' >> ~/.zshrc && source ~/.zshrc\n'
    fail "PATH 修好后重跑"
  fi
  INSTALLED_PYBH="$(browser-harness --version 2>/dev/null || echo '?')"
  if [ "$INSTALLED_PYBH" != "$PYTHON_BH_PKG_VERSION" ]; then
    warn "browser-harness 安装版本 ${INSTALLED_PYBH} 不匹配钉死版本 ${PYTHON_BH_PKG_VERSION}"
    warn "请手动: uv tool install --force browser-harness==${PYTHON_BH_PKG_VERSION}"
    fail "版本不匹配，setup 中止"
  fi
  green "browser-harness ${INSTALLED_PYBH}"

  printf "\n"
  blue "强烈建议：用一个独立的 Chrome profile（不要复用日常 profile）"
  printf "    macOS:  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\\\\n"
  printf "              --user-data-dir=\"\$HOME/.cache/chrome-bh-profile\" \\\\\n"
  printf "              --remote-debugging-port=9222\n"
  printf "    这样 Agent 接管的 Chrome 与你的银行/邮箱/日常账号完全隔离。\n"
  printf "\n"
  blue "下一步：把守护进程接到你正在用的 Chrome"
  printf "    browser-harness --setup\n"
  printf "\n"
  printf "接管完成后再跑:\n"
  printf "    scripts/run.sh doctor\n"
  printf "\n"
  printf "用完后停掉守护进程:\n"
  printf "    scripts/run.sh stop\n"
}

# --- doctor --------------------------------------------------------------
do_doctor() {
  EXIT=0

  if command -v node >/dev/null 2>&1; then
    green "node $(node --version)"
  else
    warn "node 缺失"; EXIT=1
  fi

  if command -v uv >/dev/null 2>&1; then
    green "uv $(uv --version | awk '{print $2}')"
  else
    warn "uv 缺失"; EXIT=1
  fi

  if command -v bhts >/dev/null 2>&1; then
    green "bhts $(bhts --version 2>/dev/null | awk '{print $2}' || echo '?') ($(command -v bhts))"
  else
    warn "bhts 缺失"; EXIT=1
  fi

  if command -v browser-harness >/dev/null 2>&1; then
    green "browser-harness $(browser-harness --version 2>/dev/null || echo '?') ($(command -v browser-harness))"
  else
    warn "browser-harness 缺失"; EXIT=1
  fi

  if [ "$EXIT" -ne 0 ]; then
    warn "依赖不完整。跑: scripts/run.sh setup"
    return $EXIT
  fi

  # 守护 + 当前标签
  blue "尝试连接守护进程并读取当前标签..."
  if bhts -c '
    try {
      const info = await bh.pageInfo();
      const tab = await bh.currentTab();
      console.log(JSON.stringify({
        ok: true,
        daemon: bh.name,
        log: bh.logPath,
        url: info.url || tab.url,
        title: info.title || tab.title,
        viewport: info.w ? `${info.w}x${info.h}` : null
      }, null, 2));
    } catch (e) {
      console.log(JSON.stringify({ ok: false, error: String(e.message || e) }, null, 2));
      process.exit(2);
    }
  '; then
    green "守护进程在跑且接管 Chrome 成功"
  else
    warn "守护进程没起或没接 Chrome——跑: browser-harness --setup"
    EXIT=1
  fi

  exit $EXIT
}

# --- stop ----------------------------------------------------------------
do_stop() {
  # ClawScan F3 (Rogue Agents, Note): the Python daemon is long-lived and
  # holds a CDP WebSocket to your real Chrome. Stop it when you're done so
  # an agent can't keep acting in the background.
  blue "停止 browser-harness 守护进程..."
  if ! command -v browser-harness >/dev/null 2>&1; then
    warn "browser-harness 不在 PATH，跳过（也可能本来就没起）"
    return 0
  fi
  # browser-harness ships its own --stop flag in upstream; if not, fall
  # back to a portable pgrep path. We try both, never escalate.
  if browser-harness --help 2>&1 | grep -q -- '--stop'; then
    browser-harness --stop || warn "browser-harness --stop 返回非零（可能本来就没起）"
  else
    # Match only browser-harness daemon processes started by the current uid.
    if pgrep -u "$(id -u)" -f 'browser-harness( |$)' >/dev/null 2>&1; then
      pkill -u "$(id -u)" -f 'browser-harness( |$)' || true
      green "已发送 SIGTERM 到守护进程"
    else
      green "未发现守护进程在跑"
    fi
  fi
  # Audit
  AUDIT_LOG="${BH_AUDIT_LOG:-$HOME/.cache/browser-harness/skill-audit.log}"
  if [ -n "$AUDIT_LOG" ]; then
    mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true
    printf 'ts=%s sub=stop host=- mode=daemon-stop denied=0 exit=0 argv_sha256=-\n' \
      "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$AUDIT_LOG" 2>/dev/null || true
    chmod 0600 "$AUDIT_LOG" 2>/dev/null || true
  fi
}

# --- 子命令分发 ----------------------------------------------------------
SUB="${1:-help}"
shift || true

case "$SUB" in
  -h|--help|help)   show_help ;;
  setup)            do_setup ;;
  doctor)           do_doctor ;;
  stop)             do_stop ;;

  # 其它子命令统一走 Node runner —— 拼 bhts -c 的逻辑放那里更易读
  js|exec|page|tabs|open|switch|shot|click|type|key|scroll|upload|helpers)
    exec node "$RUNNER" "$SUB" "$@"
    ;;

  raw)
    # ----------------------------------------------------------------------
    # raw — disabled by default since v0.2.3.
    #
    # Background: ClawScan flagged raw as a backdoor that bypasses the
    # sensitive-deny policy and the metadata audit log (Tool Misuse and
    # Exploitation, High/High concern). To use raw you must NOW:
    #   1. Set BH_RAW_OK=1 in your env (interactive opt-in, every session).
    #   2. Set BH_ALLOW_SENSITIVE=1 if the page is sensitive — raw does NOT
    #      run the in-snippet policy gate. You are accepting full
    #      responsibility for the bhts arguments you pass.
    # raw still emits a metadata audit log entry (sub=raw mode=raw-bypass)
    # so the action is at least observable.
    # ----------------------------------------------------------------------
    if [ "${BH_RAW_OK:-}" != "1" ]; then
      warn "raw is disabled by default (since v0.2.3)."
      warn "raw bypasses the sensitive-deny policy and the in-snippet"
      warn "policy gate, so the skill cannot protect you from accidentally"
      warn "running on bank/email/internal/admin pages."
      warn ""
      warn "To enable raw for THIS shell session ONLY:"
      warn "    export BH_RAW_OK=1"
      warn "    scripts/run.sh raw -c '...'"
      warn ""
      warn "Prefer scripts/run.sh exec '<snippet>' for normal use — it"
      warn "goes through sensitive-deny + audit log."
      exit 2
    fi
    if ! command -v bhts >/dev/null 2>&1; then
      fail "bhts 未安装。跑: scripts/run.sh setup"
    fi
    # Best-effort metadata audit entry for raw (cannot capture URL — that
    # would require launching bhts twice, defeating the "raw" semantic).
    AUDIT_LOG="${BH_AUDIT_LOG:-$HOME/.cache/browser-harness/skill-audit.log}"
    if [ -n "$AUDIT_LOG" ]; then
      mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true
      ARGV_SHA="$(printf '%s' "$*" | shasum -a 256 2>/dev/null | awk '{print substr($1,1,16)}')"
      printf 'ts=%s sub=raw host=unknown mode=raw-bypass denied=0 exit=- argv_sha256=%s\n' \
        "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$ARGV_SHA" >> "$AUDIT_LOG" 2>/dev/null || true
      chmod 0600 "$AUDIT_LOG" 2>/dev/null || true
    fi
    warn "raw: bypassing sensitive-deny + in-snippet policy gate (BH_RAW_OK=1)."
    exec bhts "$@"
    ;;

  *)
    warn "未知子命令: $SUB"
    show_help
    exit 2
    ;;
esac
