#!/usr/bin/env bash
# Career Compass 安装脚本
# by Barry
# 功能：安装 boss-cli + 检测 PDF 工具链
# 注意：运行一次即可，无需每次使用

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${YELLOW}[INFO]${NC}  $1"; }
ok()    { echo -e "${GREEN}[OK]${NC}  $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; }

echo ""
echo -e "${BOLD}============================================${NC}"
echo -e "${BOLD}  Career Compass 安装向导 (by Barry)${NC}"
echo -e "${BOLD}============================================${NC}"

# ─────────────────────────────────────────────
# Step 1: boss-cli 安装
# ─────────────────────────────────────────────
echo ""
echo -e "${CYAN}▶ Step 1 — 安装 boss-cli${NC}"

if command -v boss &>/dev/null; then
    ok "boss-cli 已安装 ($(boss --version 2>/dev/null || echo '已安装'))"
else
    warn "boss-cli 未安装，正在安装..."
    echo ""

    if command -v uv &>/dev/null; then
        info "使用 uv 安装（推荐）..."
        if uv tool install kabi-boss-cli 2>/dev/null; then
            ok "boss-cli 安装成功"
        else
            pip install kabi-boss-cli --user 2>/dev/null && ok "boss-cli 安装成功 (pip)" || fail "boss-cli 安装失败，请手动运行: pip install kabi-boss-cli --user"
        fi
    elif command -v pipx &>/dev/null; then
        info "使用 pipx 安装..."
        pipx install kabi-boss-cli 2>/dev/null && ok "boss-cli 安装成功" || fail "安装失败"
    else
        info "使用 pip 安装..."
        pip install kabi-boss-cli --user 2>/dev/null && ok "boss-cli 安装成功" || fail "安装失败，请手动运行: pip install kabi-boss-cli --user"
    fi
fi

# ─────────────────────────────────────────────
# Step 2: PDF 工具链检测
# ─────────────────────────────────────────────
echo ""
echo -e "${CYAN}▶ Step 2 — 检测 PDF 工具链${NC}"
echo ""

MISSING_TOOLS=""
for tool in pdftotext tesseract ghostscript; do
    if command -v $tool &>/dev/null; then
        ok "$tool 已安装"
    else
        warn "$tool 未安装"
        MISSING_TOOLS=1
    fi
done

if [ -n "$MISSING_TOOLS" ]; then
    echo ""
    echo "  PDF 工具链（pdftotext / tesseract / ghostscript）用于解析简历 PDF。"
    echo "  不安装也可以使用，直接复制简历内容粘贴给 AI 即可。"
    echo ""
    echo "  macOS 安装:  brew install poppler tesseract ghostscript"
    echo "  Ubuntu 安装: sudo apt install poppler-utils tesseract-ocr ghostscript"
    echo "  Windows 安装:"
    echo "    - poppler:  https://github.com/oschwartz10612/poppler-windows/releases"
    echo "    - tesseract: https://github.com/UB-Mannheim/tesseract/wiki"
    echo "    - ghostscript: https://ghostscript.com/releases/gsdnld.html"
fi

# ─────────────────────────────────────────────
# Step 3: BOSS 登录检测
# ─────────────────────────────────────────────
echo ""
echo -e "${CYAN}▶ Step 3 — BOSS 直聘登录状态${NC}"
echo ""

BOSS_READY=""
if command -v boss &>/dev/null; then
    AUTH=$(boss status --json 2>/dev/null || echo "")
    if echo "$AUTH" | grep -q '"authenticated": true'; then
        ok "BOSS 直聘已登录！"
        boss me --json 2>/dev/null | grep -o '"name":"[^"]*"' | head -1 || true
        BOSS_READY=1
    else
        warn "未检测到登录态，需要绑定 BOSS 账号"
        echo ""
        echo "  请按以下步骤操作："
        echo ""
        echo "  1. 确认浏览器已登录 https://www.zhipin.com"
        echo "  2. 运行: boss login"
        echo "  3. 验证: boss status"
        echo ""
        echo "  如自动提取失败: boss login --qrcode"
    fi
else
    warn "boss-cli 未安装，无法检测登录状态"
fi

# ─────────────────────────────────────────────
# 完成
# ─────────────────────────────────────────────
echo ""
echo "============================================"
echo -e "${BOLD}  安装完成！${NC}"
echo "============================================"
echo ""
echo "  在 AI 对话中说以下任意一句即可激活："
echo ""
echo -e "  ${CYAN}帮我全面准备面试${NC}"
echo -e "  ${CYAN}我要去XX公司面试，帮我模拟一下${NC}"
echo -e "  ${CYAN}帮我看看简历有哪些可以优化的地方${NC}"
echo -e "  ${CYAN}分析一下XX公司${NC}"
echo -e "  ${CYAN}帮我搜索同城类似职位${NC}"
echo ""
echo "============================================"
echo ""
