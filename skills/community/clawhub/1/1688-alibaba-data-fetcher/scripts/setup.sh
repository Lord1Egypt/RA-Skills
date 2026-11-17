# ============================================================
# 1688 Data Claw - Linux 一键初始化
# 安装 skill 时立即执行一次
# ============================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/env.sh"

echo "=== 1688 Data Claw - Linux 初始化 ==="

# 1. 安装系统依赖
echo ">>> 安装系统依赖..."
apt-get update -qq
apt-get install -y -qq xvfb fonts-wqy-zenhei fonts-noto-cjk

# 2. 安装 lark-cli
echo ">>> 安装 lark-cli..."
npm install -g @larksuite/lark-cli 2>&1 | tail -1

# 3. 下载 Chromium 便携版（从 npmmirror，国内最快）
CHROMIUM_ZIP="$SKILL_DIR/chromium/chrome-linux64.zip"
if [ ! -f "$CHROME" ]; then
  echo ">>> 获取最新 Chromium 版本..."
  
  # 从 npmmirror 获取最新稳定版号
  version=$(curl -s "https://registry.npmmirror.com/-/binary/chrome-for-testing/last-known-good-versions.json" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['channels']['Stable']['version'])" 2>/dev/null)
  echo "  最新稳定版: $version"
  
  # 下载 zip（npmmirror CDN，国内 ~4.5MB/s）
  echo ">>> 下载 Chromium（~150MB，约需 30s）..."
  download_url="https://registry.npmmirror.com/-/binary/chrome-for-testing/$version/linux64/chrome-linux64.zip"
  
  if ! curl -L -o "$CHROMIUM_ZIP" "$download_url" --connect-timeout 15 --max-time 300; then
    echo "  npmmirror 下载失败，尝试 Google 官方源..."
    download_url="https://storage.googleapis.com/chrome-for-testing-public/$version/linux64/chrome-linux64.zip"
    curl -L -o "$CHROMIUM_ZIP" "$download_url" --connect-timeout 15 --max-time 300
  fi
  
  echo ">>> 解压 Chromium..."
  unzip -o "$CHROMIUM_ZIP" -d "$SKILL_DIR/chromium/" > /dev/null
  rm -f "$CHROMIUM_ZIP"
  echo "✅ Chromium 就位: $CHROME"
else
  echo "✅ Chromium 已就位: $CHROME"
fi

# 4. 创建必要目录
mkdir -p "$OUTPUT_DIR"
echo "输出目录: $OUTPUT_DIR"

# 5. 验证插件已存在
if [ -f "$EXT_DIR/manifest.json" ]; then
  echo "✅ 插件已就位: $EXT_DIR"
else
  echo "❌ 插件缺失: $EXT_DIR/manifest.json"
  exit 1
fi

echo ""
echo "=== ✨ 初始化完成 ==="
echo "运行 ./scripts/start-browser.sh 启动浏览器"
echo "扩展 ID: ekmgnempbbamlmaolijdfjakeopniion"