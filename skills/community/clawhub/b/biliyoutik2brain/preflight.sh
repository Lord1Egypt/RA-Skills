#!/usr/bin/env bash
# preflight.sh — BiliYouTik2Brain 安装前预检
#
# 用法: bash preflight.sh [--verbose]
# 功能: 检测运行环境是否满足最低要求，不自动安装
# 退出码: 0=全部通过  1=有阻断项  2=有告警但可通过

set -euo pipefail

VERBOSE=false
for arg in "$@"; do
  case "$arg" in --verbose|-v) VERBOSE=true ;; esac
done

PASS=0
WARN=0
FAIL=0

pass()  { PASS=$((PASS+1)); echo "  ✅ $1"; }
warn()  { WARN=$((WARN+1)); echo "  ⚠️  $1"; }
fail()  { FAIL=$((FAIL+1)); echo "  ❌ $1"; }

echo "════════════════════════════════════════"
echo "  BiliYouTik2Brain 环境预检"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════"
echo ""

# ── Python ──
echo "🔍 检查 Python..."
if command -v python3 &>/dev/null; then
  PY_VER=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
  PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
  PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
  if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 10 ]; then
    pass "Python $PY_VER (≥ 3.10)"
  else
    fail "Python $PY_VER (需要 ≥ 3.10)"
  fi
else
  fail "Python3 未安装"
fi

# ── pip ──
echo "🔍 检查 pip..."
if command -v pip3 &>/dev/null; then
  pass "pip3 可用"
else
  fail "pip3 未安装"
fi

# ── ffmpeg ──
echo "🔍 检查 ffmpeg..."
if command -v ffmpeg &>/dev/null; then
  FF_VER=$(ffmpeg -version 2>&1 | head -1 | grep -oP '\d+\.\d+' | head -1)
  pass "ffmpeg $FF_VER"
else
  fail "ffmpeg 未安装（转录必需）"
  echo "     安装: sudo apt install ffmpeg  |  brew install ffmpeg  |  winget install ffmpeg"
fi

# ── yt-dlp ──
echo "🔍 检查 yt-dlp..."
if command -v yt-dlp &>/dev/null; then
  YTDLP_VER=$(yt-dlp --version 2>/dev/null || echo "unknown")
  pass "yt-dlp $YTDLP_VER"
else
  warn "yt-dlp 未安装（YouTube/B站下载必需）"
  echo "     安装: pip3 install yt-dlp"
fi

# ── faster-whisper ──
echo "🔍 检查 faster-whisper..."
if python3 -c "import faster_whisper" 2>/dev/null; then
  pass "faster-whisper 已安装"
else
  warn "faster-whisper 未安装（本地转录必需）"
  echo "     安装: pip3 install faster-whisper"
fi

# ── whisper 模型 ──
echo "🔍 检查 whisper 模型缓存..."
MODEL_FOUND=false
for model_dir in \
  "$HOME/.cache/huggingface/hub/models--Systran--faster-whisper-base" \
  "$HOME/.cache/huggingface/hub/models--Systran--faster-whisper-tiny" \
  "$HOME/.cache/huggingface/hub/models--Systran--faster-whisper-small"; do
  if [ -d "$model_dir" ]; then
    pass "模型缓存: $(basename "$model_dir")"
    MODEL_FOUND=true
    break
  fi
done
if [ "$MODEL_FOUND" = false ]; then
  warn "whisper 模型未缓存（首次使用会自动下载，约 500MB）"
fi

# ── GPU ──
echo "🔍 检查 GPU..."
if command -v nvidia-smi &>/dev/null; then
  GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1 || echo "unknown")
  pass "NVIDIA GPU: $GPU_NAME"
else
  pass "无 GPU（CPU 模式可运行，速度较慢）"
fi

# ── 磁盘空间 ──
echo "🔍 检查磁盘空间..."
DISK_FREE=$(df -BG "$HOME" 2>/dev/null | tail -1 | awk '{print $4}' | tr -d 'G')
if [ -n "$DISK_FREE" ] && [ "$DISK_FREE" -gt 5 ]; then
  pass "磁盘可用: ${DISK_FREE}GB (> 5GB)"
elif [ -n "$DISK_FREE" ] && [ "$DISK_FREE" -gt 1 ]; then
  warn "磁盘可用: ${DISK_FREE}GB (> 1GB 但建议 > 5GB)"
else
  fail "磁盘空间不足: ${DISK_FREE:-未知}GB（至少需要 1GB）"
fi

# ── 内存 ──
echo "🔍 检查内存..."
if [ -f /proc/meminfo ]; then
  MEM_KB=$(grep MemAvailable /proc/meminfo 2>/dev/null | awk '{print $2}')
  if [ -z "$MEM_KB" ] || [ "$MEM_KB" = "0" ]; then
    MEM_KB=$(grep MemFree /proc/meminfo 2>/dev/null | awk '{print $2}')
  fi
  if [ -n "$MEM_KB" ] && [ "$MEM_KB" -gt 0 ]; then
    MEM_MB=$((MEM_KB / 1024))
    if [ "$MEM_MB" -ge 4096 ]; then
      pass "可用内存: $((MEM_MB/1024))GB (≥ 4GB)"
    elif [ "$MEM_MB" -ge 2048 ]; then
      pass "可用内存: $((MEM_MB/1024))GB (≥ 2GB)"
    elif [ "$MEM_MB" -ge 1024 ]; then
      warn "可用内存: $((MEM_MB/1024))GB (≥ 1GB，推荐 ≥ 2GB)"
    else
      fail "可用内存不足: ${MEM_MB}MB（至少需要 1GB）"
    fi
  else
    warn "无法读取内存信息"
  fi
else
  warn "无法检测内存（非 Linux 系统）"
fi

# ── LLM API Key ──
echo "🔍 检查 LLM API 配置..."
if [ -n "${LLM_API_KEY:-}" ]; then
  pass "LLM_API_KEY 已配置"
elif [ -n "${OPENAI_API_KEY:-}" ]; then
  pass "OPENAI_API_KEY 已配置"
elif [ -n "${DEEPSEEK_API_KEY:-}" ]; then
  pass "DEEPSEEK_API_KEY 已配置"
else
  warn "未检测到 LLM API Key（enhance 阶段将跳过）"
  echo "     设置: export LLM_API_KEY=your-api-key-here"
fi

# ── 代理连通性 ──
echo "🔍 检查网络..."
if curl -s --max-time 5 https://www.youtube.com -o /dev/null 2>/dev/null; then
  pass "YouTube 直连可达"
else
  # 检查代理
  PROXY_PORTS="7890 7897 9981 10809 1080"
  PROXY_OK=false
  for port in $PROXY_PORTS; do
    if curl -s --max-time 3 --proxy "http://127.0.0.1:$port" https://www.youtube.com -o /dev/null 2>/dev/null; then
      pass "YouTube 通过代理 (port $port) 可达"
      PROXY_OK=true
      break
    fi
  done
  if [ "$PROXY_OK" = false ]; then
    warn "YouTube 不可达（B站/抖音不影响，YouTube 下载需要代理）"
  fi
fi

# ── 总结 ──
echo ""
echo "════════════════════════════════════════"
echo "  结果: ✅ $PASS 通过  ⚠️  $WARN 告警  ❌ $FAIL 阻断"
echo "════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo "❌ 有 $FAIL 项阻断，请先解决后再安装"
  echo "   运行 bash install.sh 可自动修复部分问题"
  exit 1
elif [ "$WARN" -gt 0 ]; then
  echo ""
  echo "⚠️  有 $WARN 项告警，可以安装但部分功能可能受限"
  exit 2
else
  echo ""
  echo "✅ 环境检查全部通过，可以安装"
  exit 0
fi
