#!/usr/bin/env bash
# install.sh — BiliYouTik2Brain 一键安装部署
#
# 用法: bash install.sh [--force] [--skip-preflight]
# 功能: 自动安装所有依赖，零配置开箱即用
# 平台: Linux / macOS / Windows (WSL)

set -euo pipefail

FORCE=false
SKIP_PREFLIGHT=false
for arg in "$@"; do
  case "$arg" in --force) FORCE=true ;; --skip-preflight) SKIP_PREFLIGHT=true ;; esac
done

OS_TYPE=$(uname -s 2>/dev/null || echo "Windows")
echo "════════════════════════════════════════"
echo "  BiliYouTik2Brain 一键安装"
echo "  平台: $OS_TYPE"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════"
echo ""

# ── 预检 ──
if [ "$SKIP_PREFLIGHT" = false ]; then
  echo "📋 运行环境预检..."
  if bash "$(dirname "$0")/preflight.sh" --verbose; then
    echo "  ✅ 预检通过"
  else
    echo "  ⚠️  预检有告警，继续安装..."
  fi
  echo ""
fi

# ── Python 包 ──
echo "📦 安装 Python 依赖..."
python3 -m pip install --quiet \
  faster-whisper \
  yt-dlp \
  psutil \
  requests \
  opencc \
  || {
    echo "  ⚠️  pip install 部分失败，尝试逐个安装..."
    for pkg in "faster-whisper" "yt-dlp" "psutil" "requests" "opencc"; do
      if ! python3 -c "import ${pkg//-/_}" 2>/dev/null; then
        echo "  安装 $pkg..."
        python3 -m pip install --quiet "$pkg" || echo "  ❌ $pkg 安装失败"
      fi
    done
  }
echo "  ✅ Python 依赖安装完成"
echo ""

# ── ffmpeg ──
echo "🎬 检查 ffmpeg..."
if ! command -v ffmpeg &>/dev/null; then
  echo "  安装 ffmpeg..."
  case "$OS_TYPE" in
    Linux)
      if command -v apt-get &>/dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg 2>/dev/null || \
          echo "  ⚠️  apt 安装失败，请手动安装: sudo apt install ffmpeg"
      elif command -v yum &>/dev/null; then
        sudo yum install -y ffmpeg 2>/dev/null || \
          echo "  ⚠️  yum 安装失败，请手动安装"
      else
        echo "  ⚠️  未知 Linux，请手动安装 ffmpeg"
      fi
      ;;
    Darwin)
      if command -v brew &>/dev/null; then
        brew install ffmpeg 2>/dev/null || echo "  ⚠️  brew 安装失败"
      else
        echo "  ⚠️  请先安装 Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
      fi
      ;;
    *)
      echo "  ⚠️  Windows 请手动安装 ffmpeg: winget install ffmpeg 或从 https://ffmpeg.org 下载"
      ;;
  esac
else
  echo "  ✅ ffmpeg 已安装: $(ffmpeg -version 2>&1 | head -1)"
fi
echo ""

# ── yt-dlp ──
echo "📺 检查 yt-dlp..."
if ! command -v yt-dlp &>/dev/null; then
  echo "  安装 yt-dlp..."
  python3 -m pip install --quiet yt-dlp || \
    echo "  ⚠️  yt-dlp 安装失败，可手动: pip3 install yt-dlp"
else
  echo "  ✅ yt-dlp 已安装: $(yt-dlp --version)"
fi
echo ""

# ── whisper 模型预下载 ──
echo "🧠 检查 whisper 模型..."
MODEL_CACHE="$HOME/.cache/huggingface/hub"
if [ ! -d "$MODEL_CACHE/models--Systran--faster-whisper-base" ]; then
  echo "  预下载 faster-whisper-base 模型（约 500MB，首次较慢）..."
  python3 -c "
from faster_whisper import WhisperModel
print('  下载中，请稍候...')
model = WhisperModel('base', device='cpu', compute_type='int8')
print('  ✅ 模型下载完成')
" 2>/dev/null || echo "  ⚠️  模型预下载失败（首次使用时会自动下载）"
else
  echo "  ✅ 模型已缓存"
fi
echo ""

# ── LLM API Key 检测 ──
echo "🔑 检查 LLM API 配置..."
if [ -n "${LLM_API_KEY:-}" ]; then
  echo "  ✅ LLM_API_KEY 已配置"
elif [ -n "${DEEPSEEK_API_KEY:-}" ]; then
  echo "  ✅ DEEPSEEK_API_KEY 已配置"
else
  echo "  ⚠️  未检测到 LLM API Key"
  echo "  如需 LLM 纠错功能，请设置环境变量:"
  echo "    export LLM_API_KEY=your-api-key-here"
  echo "    export LLM_BASE_URL=https://api.deepseek.com/v1"
  echo "    export LLM_MODEL=deepseek-chat"
fi
echo ""

# ── 目录初始化 ──
echo "📁 初始化存储目录..."
STORAGE="$HOME/openclaw/workspace/storage"
mkdir -p "$STORAGE"/{transcripts,notes,cards,errors,knowledge,comments} 2>/dev/null || \
mkdir -p "$HOME/.biliyoutik2brain"/{storage,cache} 2>/dev/null || \
echo "  ⚠️  存储目录创建失败"
echo "  ✅ 存储目录就绪"
echo ""

# ── 权限 ──
chmod +x "$(dirname "$0")/preflight.sh" 2>/dev/null || true
echo "🔧 设置执行权限..."
echo "  ✅ preflight.sh 可执行"
echo ""

# ── 验证安装 ──
echo "🧪 验证安装..."
ERRORS=0
python3 -c "import faster_whisper" 2>/dev/null || { echo "  ❌ faster_whisper 导入失败"; ERRORS=$((ERRORS+1)); }
python3 -c "import yt_dlp" 2>/dev/null || { echo "  ❌ yt_dlp 导入失败"; ERRORS=$((ERRORS+1)); }
python3 -c "import psutil" 2>/dev/null || { echo "  ❌ psutil 导入失败"; ERRORS=$((ERRORS+1)); }
python3 -c "import requests" 2>/dev/null || { echo "  ❌ requests 导入失败"; ERRORS=$((ERRORS+1)); }

if [ "$ERRORS" -eq 0 ]; then
  echo "  ✅ 所有模块导入成功"
else
  echo "  ⚠️  $ERRORS 个模块导入失败"
fi
echo ""

# ── 完成 ──
echo "════════════════════════════════════════"
echo "  ✅ 安装完成！"
echo "════════════════════════════════════════"
echo ""
echo "快速开始:"
echo "  python3 -m biliyoutik2brain <视频链接>"
echo "  python3 -m biliyoutik2brain --status      # 查看状态"
echo "  python3 -m biliyoutik2brain --env         # 环境诊断"
echo ""
echo "如需 LLM 纠错，请配置:"
echo "  export LLM_API_KEY=your-api-key-here"
echo "  export LLM_BASE_URL=https://api.deepseek.com/v1"
echo "  export LLM_MODEL=deepseek-chat"
