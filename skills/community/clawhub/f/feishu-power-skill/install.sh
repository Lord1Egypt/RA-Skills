#!/usr/bin/env bash
# Feishu Power Skill — 安装脚本
# 用法: bash install.sh [--openclaw | --claude-code | --standalone]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="feishu-power-skill"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ============================================================
# 1. 检查 Python
# ============================================================
check_python() {
    if command -v python3 &>/dev/null; then
        PY=$(python3 --version 2>&1 | awk '{print $2}')
        MAJOR=$(echo "$PY" | cut -d. -f1)
        MINOR=$(echo "$PY" | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 11 ]; then
            info "Python $PY"
        else
            warn "Python $PY 检测到，推荐 3.11+（可能仍可运行）"
        fi
    else
        error "未找到 python3，请先安装 Python 3.11+"
    fi
}

# ============================================================
# 2. 安装依赖
# ============================================================
install_deps() {
    info "安装 Python 依赖..."
    pip3 install --quiet requests pyyaml 2>/dev/null || pip install --quiet requests pyyaml
    info "依赖安装完成"
}

# ============================================================
# 3. 检查飞书凭证
# ============================================================
check_feishu_creds() {
    if [ -z "${FEISHU_APP_ID:-}" ] || [ -z "${FEISHU_APP_SECRET:-}" ]; then
        warn "未检测到飞书凭证环境变量"
        echo ""
        echo "  请在 shell 配置中添加："
        echo "    export FEISHU_APP_ID=cli_xxx"
        echo "    export FEISHU_APP_SECRET=xxx"
        echo ""
        echo "  或创建 .env 文件后 source 加载。"
        echo ""
    else
        info "飞书凭证已配置 (APP_ID: ${FEISHU_APP_ID:0:8}...)"
    fi
}

# ============================================================
# 4. 验证脚本可运行
# ============================================================
verify_scripts() {
    info "验证脚本..."
    local ok=true
    for script in feishu_api bitable_engine doc_workflow retail_audit report_generator; do
        if python3 -c "import sys; sys.path.insert(0,'${SCRIPT_DIR}/scripts'); __import__('${script}')" 2>/dev/null; then
            info "  ${script}.py ✓"
        else
            warn "  ${script}.py — import 失败（可能缺少飞书凭证，运行时再配置即可）"
            ok=false
        fi
    done
    if $ok; then
        info "所有模块验证通过"
    fi
}

# ============================================================
# 5. 平台安装
# ============================================================
install_openclaw() {
    local target="${HOME}/.openclaw/skills/${SKILL_NAME}"
    if [ "$SCRIPT_DIR" = "$target" ]; then
        info "已在 OpenClaw skills 目录中，无需链接"
        return
    fi
    if [ -e "$target" ]; then
        warn "${target} 已存在，跳过链接"
    else
        mkdir -p "${HOME}/.openclaw/skills"
        ln -s "$SCRIPT_DIR" "$target"
        info "已链接到 ${target}"
    fi
    info "OpenClaw 安装完成 — 重启 gateway 后自动加载 SKILL.md"
}

install_claude_code() {
    info "Claude Code 模式 — 将本目录放到项目中，Claude Code 会自动读取 CLAUDE.md"
    info "当前目录: ${SCRIPT_DIR}"
}

# ============================================================
# 6. 快速测试
# ============================================================
run_smoke_test() {
    info "运行冒烟测试（Demo 审计）..."
    if python3 "${SCRIPT_DIR}/scripts/retail_audit.py" demo --output /tmp/feishu-skill-test.md 2>/dev/null; then
        local lines
        lines=$(wc -l < /tmp/feishu-skill-test.md)
        info "Demo 审计通过 — 生成 ${lines} 行报告"
        rm -f /tmp/feishu-skill-test.md
    else
        warn "Demo 审计未通过（不影响安装，可能是环境问题）"
    fi
}

# ============================================================
# Main
# ============================================================
main() {
    echo ""
    echo "  ╔══════════════════════════════════════╗"
    echo "  ║   Feishu Power Skill — Installer     ║"
    echo "  ╚══════════════════════════════════════╝"
    echo ""

    local mode="${1:-auto}"

    check_python
    install_deps
    check_feishu_creds

    case "$mode" in
        --openclaw)
            install_openclaw
            ;;
        --claude-code)
            install_claude_code
            ;;
        --standalone)
            info "独立模式 — 直接通过 python3 scripts/xxx.py 调用"
            ;;
        auto|*)
            # 自动检测
            if [ -d "${HOME}/.openclaw" ]; then
                install_openclaw
            fi
            if command -v claude &>/dev/null; then
                install_claude_code
            fi
            if [ ! -d "${HOME}/.openclaw" ] && ! command -v claude &>/dev/null; then
                info "独立模式 — 直接通过 python3 scripts/xxx.py 调用"
            fi
            ;;
    esac

    verify_scripts
    run_smoke_test

    echo ""
    info "安装完成 🎉"
    echo ""
    echo "  快速体验："
    echo "    python3 ${SCRIPT_DIR}/scripts/retail_audit.py demo --output report.md"
    echo "    python3 ${SCRIPT_DIR}/scripts/bitable_engine.py stats --app <token> --table <id>"
    echo ""
}

main "$@"
