#!/usr/bin/env bash
#
# 内容工坊 前置依赖检查
# 用法: bash check-prereq.sh
#
set -e

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

ok()   { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
fail() { echo -e "${RED}❌ $1${NC}"; }

echo "内容工坊 环境检查"
echo "===================================="

# 1. Python
if command -v python3 >/dev/null 2>&1; then
  PYV=$(python3 --version | awk '{print $2}')
  ok "Python $PYV"
else
  fail "未找到 python3（需要 Python 3.9+）"
  exit 1
fi

# 2. Node（场景5 PPT 生成需要）
if command -v node >/dev/null 2>&1; then
  NODEV=$(node --version)
  ok "Node $NODEV"
else
  warn "未找到 node（场景5 html2pptx 需要 Node.js）"
fi

# 3. yt-dlp（视频下载）
if command -v yt-dlp >/dev/null 2>&1 || python3 -m yt_dlp --version >/dev/null 2>&1; then
  ok "yt-dlp 可用"
else
  warn "yt-dlp 未安装（场景5视频下载需要：pip3 install yt-dlp）"
fi

# 4. ffmpeg（音轨提取）
if command -v ffmpeg >/dev/null 2>&1; then
  ok "ffmpeg 可用"
else
  warn "ffmpeg 未安装（音轨提取需要）"
fi

# 5. 网络（按 Ctrl+C 跳过）
echo ""
echo "网络检查（5s 测一次，按 Ctrl+C 中途跳过）"
echo "------------------------------"
if curl -s -m 5 -o /dev/null -w "%{http_code}" https://www.google.com | grep -q "200\|301\|302"; then
  ok "Google 可达（NotebookLM 登录需要）"
else
  warn "Google 不可达 → 需配代理，见 references/china-network.md"
fi

if curl -s -m 5 -o /dev/null -w "%{http_code}" https://notebooklm.google.com | grep -q "200\|301\|302"; then
  ok "NotebookLM 可达"
else
  warn "NotebookLM 不可达（需海外代理，见 references/china-network.md）"
fi

if curl -s -m 5 -o /dev/null -w "%{http_code}" https://mp.weixin.qq.com | grep -q "200\|301\|302"; then
  ok "微信公众号可达"
else
  warn "微信公众号不可达（可能代理劫持了国内流量）"
fi

# 6. Playwright（场景5 html2pptx）
if node -e "require('playwright')" 2>/dev/null; then
  ok "Playwright（Node.js）可用"
else
  warn "Playwright（Node.js）未安装（场景5 html2pptx 需要）"
fi

if python3 -c "from playwright import sync_api" 2>/dev/null; then
  ok "Playwright（Python）可用"
else
  warn "Playwright（Python）未安装"
fi

# 7. 可选：Get笔记 API
if [[ -n "$GETNOTE_API_KEY" ]]; then
  ok "GETNOTE_API_KEY 已配置（播客/视频转写可用）"
else
  warn "GETNOTE_API_KEY 未设置（仅播客/视频转写需要，可选）"
fi

echo ""
echo "===================================="
echo "检查完成。⚠️ 提醒不影响使用，❌ 必须修复。"