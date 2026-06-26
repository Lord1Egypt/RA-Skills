#!/bin/bash

# Event Planning Skill — 环境配置脚本
# 全自动、非交互式，适合 Agent 直接调用
# 职责：安装工具 + 检测状态 → 输出结构化摘要供 Agent 判断后续动作
#
# xhs-cli 依赖：Python >= 3.10 + uv/pipx（但已安装的可独立运行，不依赖系统 Python）
# flyai-cli 依赖：Node.js >= 16 + npm

# ── 颜色 ─────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }
err()  { echo -e "${RED}✗ $1${NC}"; }
info() { echo -e "${CYAN}→ $1${NC}"; }

# ── 状态标记 ─────────────────────────────────────────────────────────
XHS_INSTALLED="no"
XHS_AUTH="no"
FLYAI_INSTALLED="no"
FLYAI_API_KEY_STATUS="no"
ERRORS=""
GUIDES=""  # 配置引导提示

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   活动演出出行规划技能 — 环境配置            ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# ══════════════════════════════════════════════════════════════════════
# 阶段 1/3：检测已安装的工具（优先检查，跳过依赖检查）
# ══════════════════════════════════════════════════════════════════════
echo "── 阶段 1/3：检测已安装的工具 ──"

# ── xhs-cli ──
info "检查 xhs-cli..."
if command -v xhs &>/dev/null; then
  ok "xhs-cli 已安装：$(xhs --version 2>/dev/null || echo '版本未知')"
  XHS_INSTALLED="yes"
else
  info "xhs-cli 未安装，将在阶段 2 尝试安装"
fi

# ── flyai-cli ──
info "检查 flyai-cli..."
if command -v flyai &>/dev/null; then
  ok "flyai-cli 已安装"
  FLYAI_INSTALLED="yes"
else
  info "flyai-cli 未安装，将在阶段 2 尝试安装"
fi

echo ""

# ══════════════════════════════════════════════════════════════════════
# 阶段 2/3：安装缺失的工具
# ══════════════════════════════════════════════════════════════════════
echo "── 阶段 2/3：安装缺失的工具 ──"

# ── 安装 xhs-cli（如果未安装）──
if [ "${XHS_INSTALLED}" = "no" ]; then
  info "准备安装 xhs-cli..."

  # 检查 Python
  PYTHON_OK="no"
  if command -v python3 &>/dev/null; then
    PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PY_MAJOR=$(echo "${PY_VER}" | cut -d. -f1)
    PY_MINOR=$(echo "${PY_VER}" | cut -d. -f2)
    if [ "${PY_MAJOR}" -ge 3 ] && [ "${PY_MINOR}" -ge 10 ]; then
      ok "Python ${PY_VER} 满足要求"
      PYTHON_OK="yes"
    else
      err "Python ${PY_VER}（需要 >= 3.10）"
      ERRORS="${ERRORS}\n- [xhs-cli] Python 版本过低（当前 ${PY_VER}，需要 >= 3.10），请升级：https://www.python.org/downloads/"
    fi
  else
    err "未找到 Python3"
    ERRORS="${ERRORS}\n- [xhs-cli] 未安装 Python3（需要 >= 3.10），请安装：https://www.python.org/downloads/"
  fi

  # 检查 uv / pipx
  HAS_UV="no"
  HAS_PIPX="no"
  if [ "${PYTHON_OK}" = "yes" ]; then
    if command -v uv &>/dev/null; then
      ok "uv $(uv --version 2>/dev/null | head -1)"
      HAS_UV="yes"
    elif command -v pipx &>/dev/null; then
      ok "pipx $(pipx --version 2>/dev/null)"
      HAS_PIPX="yes"
    else
      warn "未找到 uv 或 pipx，将尝试自动安装 uv..."
      if curl -LsSf https://astral.sh/uv/install.sh 2>/dev/null | sh 2>/dev/null; then
        export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
        if command -v uv &>/dev/null; then
          ok "uv 已自动安装：$(uv --version 2>/dev/null | head -1)"
          HAS_UV="yes"
        else
          err "uv 自动安装后仍不可用"
          ERRORS="${ERRORS}\n- [xhs-cli] uv 安装失败，请手动执行：curl -LsSf https://astral.sh/uv/install.sh | sh"
        fi
      else
        err "uv 自动安装失败"
        ERRORS="${ERRORS}\n- [xhs-cli] uv 安装失败，请手动执行：curl -LsSf https://astral.sh/uv/install.sh | sh"
      fi
    fi
  fi

  # 执行安装
  if [ "${HAS_UV}" = "yes" ]; then
    if uv tool install xiaohongshu-cli 2>/dev/null; then
      ok "xhs-cli 安装成功（via uv）"
      XHS_INSTALLED="yes"
    else
      if uv tool upgrade xiaohongshu-cli 2>/dev/null; then
        ok "xhs-cli 已升级到最新版（via uv）"
        XHS_INSTALLED="yes"
      else
        err "xhs-cli 安装失败"
        ERRORS="${ERRORS}\n- [xhs-cli] 安装失败，请手动执行：uv tool install xiaohongshu-cli"
      fi
    fi
  elif [ "${HAS_PIPX}" = "yes" ]; then
    if pipx install xiaohongshu-cli 2>/dev/null; then
      ok "xhs-cli 安装成功（via pipx）"
      XHS_INSTALLED="yes"
    else
      if pipx upgrade xiaohongshu-cli 2>/dev/null; then
        ok "xhs-cli 已升级到最新版（via pipx）"
        XHS_INSTALLED="yes"
      else
        err "xhs-cli 安装失败"
        ERRORS="${ERRORS}\n- [xhs-cli] 安装失败，请手动执行：pipx install xiaohongshu-cli"
      fi
    fi
  fi
else
  info "xhs-cli 已安装，跳过安装步骤"
fi

# ── 安装 flyai-cli（如果未安装）──
if [ "${FLYAI_INSTALLED}" = "no" ]; then
  info "准备安装 flyai-cli..."

  # 检查 Node.js
  NODE_OK="no"
  if command -v node &>/dev/null; then
    NODE_VER=$(node -v | sed 's/v//')
    NODE_MAJOR=$(echo "${NODE_VER}" | cut -d. -f1)
    if [ "${NODE_MAJOR}" -ge 16 ]; then
      ok "Node.js v${NODE_VER} 满足要求"
      NODE_OK="yes"
    else
      err "Node.js v${NODE_VER}（需要 >= 16）"
      ERRORS="${ERRORS}\n- [flyai-cli] Node.js 版本过低（当前 v${NODE_VER}，需要 >= 16），请升级：https://nodejs.org/"
    fi
  else
    err "未找到 Node.js"
    ERRORS="${ERRORS}\n- [flyai-cli] 未安装 Node.js（需要 >= 16），请安装：https://nodejs.org/"
  fi

  # 检查 npm
  if [ "${NODE_OK}" = "yes" ]; then
    if command -v npm &>/dev/null; then
      ok "npm $(npm -v)"
    else
      err "未找到 npm"
      ERRORS="${ERRORS}\n- [flyai-cli] 未安装 npm，通常随 Node.js 一起安装"
      NODE_OK="no"
    fi
  fi

  # 执行安装
  if [ "${NODE_OK}" = "yes" ]; then
    if npm install -g @fly-ai/flyai-cli 2>/dev/null; then
      ok "flyai-cli 安装成功"
      FLYAI_INSTALLED="yes"
    else
      err "flyai-cli 安装失败"
      ERRORS="${ERRORS}\n- [flyai-cli] 安装失败，请手动执行：npm i -g @fly-ai/flyai-cli"
    fi
  fi
else
  info "flyai-cli 已安装，跳过安装步骤"
fi

echo ""

# ══════════════════════════════════════════════════════════════════════
# 阶段 3/3：配置状态检测
# ══════════════════════════════════════════════════════════════════════
echo "── 阶段 3/3：配置状态检测 ──"

# ── xhs-cli 认证状态 ──
if [ "${XHS_INSTALLED}" = "yes" ]; then
  info "检查 xhs-cli 认证状态..."
  if xhs status --yaml 2>/dev/null | grep -q "authenticated: true" 2>/dev/null; then
    XHS_AUTH="yes"
    XHS_USER=$(xhs whoami --yaml 2>/dev/null | grep "nickname:" | head -1 | sed 's/.*nickname: *//' || echo "未知")
    ok "xhs-cli 已认证（用户：${XHS_USER}）"
  else
    warn "xhs-cli 未认证"
    GUIDES="${GUIDES}\n\n【xhs-cli 认证配置】\n小红书 Cookie 未配置，需要引导用户完成认证。\n\n方式 A：浏览器 Cookie 提取（推荐）\n  1. 请用户确认已在浏览器中登录 https://www.xiaohongshu.com\n  2. 执行：xhs login\n  3. 验证：xhs status\n\n方式 B：二维码扫码登录\n  1. 执行：xhs login --qrcode\n  2. 终端显示二维码，请用户用小红书 App 扫码\n  3. 验证：xhs status\n\n详细说明见：references/xhs_cli.md 认证章节"
  fi
else
  warn "xhs-cli 未安装，跳过认证检查"
fi

# ── flyai-cli 功能验证 & API Key 检测 ──
if [ "${FLYAI_INSTALLED}" = "yes" ]; then
  info "验证 flyai-cli..."
  if flyai --help &>/dev/null; then
    ok "flyai-cli 功能正常"

    # 检测是否配置了 API Key
    info "检测 flyai API Key 配置..."
    FLYAI_API_KEY_CONFIGURED="no"

    # 检查配置文件 ~/.flyai/config.json
    if [ -f "$HOME/.flyai/config.json" ]; then
      # 使用 grep 简单检查是否包含 FLYAI_API_KEY 字段且值不为空
      if grep -q '"FLYAI_API_KEY"' "$HOME/.flyai/config.json" 2>/dev/null; then
        # 进一步检查值是否为空（简单提取值并检查长度）
        API_KEY_VALUE=$(grep '"FLYAI_API_KEY"' "$HOME/.flyai/config.json" 2>/dev/null | sed 's/.*"FLYAI_API_KEY".*:.*"\([^"]*\)".*/\1/')
        if [ -n "${API_KEY_VALUE}" ] && [ "${API_KEY_VALUE}" != "null" ]; then
          FLYAI_API_KEY_CONFIGURED="yes"
        fi
      fi
    fi

    # 也检查环境变量（作为备选配置方式）
    if [ "${FLYAI_API_KEY_CONFIGURED}" = "no" ] && [ -n "${FLYAI_API_KEY:-}" ]; then
      FLYAI_API_KEY_CONFIGURED="yes"
    fi

    # 根据检测结果给出不同的提示
    if [ "${FLYAI_API_KEY_CONFIGURED}" = "yes" ]; then
      ok "flyai API Key 已配置"
    else
      # 未检测到 API Key，给出配置提示
      GUIDES="${GUIDES}\n\n【flyai-cli API Key 配置（可选）】\nflyai-cli 无需 API Key 即可使用，但配置后可获得增强搜索结果。\n\n获取 API Key：\n  1. 访问 https://flyai.open.fliggy.com/console\n  2. 登录后获取 API Key\n\n配置命令：\n  flyai config set FLYAI_API_KEY \"your-api-key\"\n\n没有 API Key 不影响正常使用，可以跳过此步骤。\n\n详细说明见：references/flyai_cli.md 配置章节"
    fi
  else
    warn "flyai-cli 命令异常，可能需要重新安装"
  fi
else
  warn "flyai-cli 未安装，跳过功能验证"
fi

# ══════════════════════════════════════════════════════════════════════
# 最终摘要
# ══════════════════════════════════════════════════════════════════════
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║              配置结果摘要                    ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# 状态表
printf "  %-18s %-10s %-10s\n" "工具" "安装" "认证/配置"
printf "  %-18s %-10s %-10s\n" "──────────────────" "──────────" "──────────"

if [ "${XHS_INSTALLED}" = "yes" ]; then
  XHS_INSTALL_STATUS="${GREEN}已安装${NC}"
else
  XHS_INSTALL_STATUS="${RED}未安装${NC}"
fi
if [ "${XHS_AUTH}" = "yes" ]; then
  XHS_AUTH_STATUS="${GREEN}已认证${NC}"
elif [ "${XHS_INSTALLED}" = "yes" ]; then
  XHS_AUTH_STATUS="${YELLOW}未认证${NC}"
else
  XHS_AUTH_STATUS="${RED}不可用${NC}"
fi
printf "  %-18s %-22b %-22b\n" "xhs-cli" "${XHS_INSTALL_STATUS}" "${XHS_AUTH_STATUS}"

if [ "${FLYAI_INSTALLED}" = "yes" ]; then
  FLYAI_INSTALL_STATUS="${GREEN}已安装${NC}"
  FLYAI_READY_STATUS="${GREEN}可用${NC}"
else
  FLYAI_INSTALL_STATUS="${RED}未安装${NC}"
  FLYAI_READY_STATUS="${RED}不可用${NC}"
fi
printf "  %-18s %-22b %-22b\n" "flyai-cli" "${FLYAI_INSTALL_STATUS}" "${FLYAI_READY_STATUS}"

# 错误详情
if [ -n "${ERRORS}" ]; then
  echo ""
  echo -e "${RED}待解决问题：${NC}"
  echo -e "${ERRORS}"
fi

# 配置引导
if [ -n "${GUIDES}" ]; then
  echo ""
  echo -e "${YELLOW}配置引导：${NC}"
  echo -e "${GUIDES}"
fi

echo ""

# ── 下一步指引（结构化输出，供 Agent 解析） ──
echo "── NEXT_STEPS ──"

# 工具安装状态
if [ "${XHS_INSTALLED}" = "yes" ]; then
  echo "XHS_INSTALLED=yes"
  if [ "${XHS_AUTH}" = "yes" ]; then
    echo "XHS_AUTH=yes"
  else
    echo "XHS_AUTH_NEEDED=yes"
    echo "XHS_AUTH_GUIDE=执行 'xhs login' 或在浏览器中完成验证码后重试"
  fi
else
  echo "XHS_INSTALLED=no"
fi

if [ "${FLYAI_INSTALLED}" = "yes" ]; then
  echo "FLYAI_INSTALLED=yes"
  echo "FLYAI_API_KEY_OPTIONAL=yes"
else
  echo "FLYAI_INSTALLED=no"
fi

# 综合状态
if [ "${XHS_INSTALLED}" = "yes" ] && [ "${XHS_AUTH}" = "yes" ] && [ "${FLYAI_INSTALLED}" = "yes" ]; then
  echo "STATUS=ALL_READY"
  echo "提示：所有工具已就绪，可以开始使用。"
elif [ "${XHS_INSTALLED}" = "no" ] && [ "${FLYAI_INSTALLED}" = "no" ]; then
  echo "STATUS=NONE_READY"
  echo "提示：所有工具都未安装，请解决上述依赖问题后重新运行脚本。"
elif [ "${XHS_INSTALLED}" = "yes" ] && [ "${XHS_AUTH}" = "no" ]; then
  echo "STATUS=XHS_AUTH_NEEDED"
  echo "提示：xhs-cli 已安装但未认证，请按上述【xhs-cli 认证配置】引导完成认证。"
else
  echo "STATUS=PARTIAL"
  echo "提示：部分工具未就绪，请查看上述状态和配置引导。"
fi

echo "── END ──"
echo ""
