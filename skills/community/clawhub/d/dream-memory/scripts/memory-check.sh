#!/bin/bash
# Dream Memory 自检脚本
# 用法: bash scripts/memory-check.sh

echo "=== Dream Memory 自检 ==="

# 1. 核心文件
WORKSPACE="${1:-$(pwd)}"
for f in MEMORY.md SOUL.md USER.md AGENTS.md WEEKLY-PROGRESS.md; do
  if [ -f "$WORKSPACE/$f" ]; then echo "[✅] $f"; else echo "[❌] $f 缺失"; fi
done

# 2. memory/ 目录
if [ -d "$WORKSPACE/memory" ]; then echo "[✅] memory/ 存在"; else echo "[❌] memory/ 缺失"; fi

# 3. OpenViking 服务
if curl -s http://127.0.0.1:1933/ 2>/dev/null | grep -q 'detail\|ok'; then
  echo "[✅] OpenViking 运行中 (1933)"
else
  echo "[⚠️] OpenViking 未运行"
fi

# 4. Ollama + bge-m3
if command -v ollama &>/dev/null && ollama list 2>/dev/null | grep -q bge-m3; then
  echo "[✅] bge-m3 已加载"
elif command -v ollama &>/dev/null; then
  echo "[⚠️] Ollama 运行但 bge-m3 未安装"
else
  echo "[❌] Ollama 未安装"
fi

# 5. 配置检查
CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
if [ -f "$CONFIG" ]; then
  count=$(grep -c 'memorySearch' "$CONFIG" 2>/dev/null || echo 0)
  echo "[ ] OpenClaw memorySearch: $count 处配置"
fi

echo "=== 检查完成 ==="
