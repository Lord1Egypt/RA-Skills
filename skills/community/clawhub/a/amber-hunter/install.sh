#!/bin/bash
# amber-hunter 安装脚本（跨平台支持）
# 支持：macOS / Windows (PowerShell) / Linux
set -e

HUNTER_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.amber-hunter"
mkdir -p "$CONFIG_DIR"

echo "🌙 Amber-Hunter 安装脚本"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 检测操作系统 ────────────────────────────────────────
OS="$(uname -s)"
IS_MAC=false
IS_LINUX=false
IS_WINDOWS=false
if [[ "$OS" == "Darwin" ]]; then
  IS_MAC=true
  echo "  检测到: macOS"
elif [[ "$OS" == "Linux" ]]; then
  IS_LINUX=true
  echo "  检测到: Linux"
else
  IS_WINDOWS=true
  echo "  检测到: Windows (Git Bash / WSL)"
fi

# ── 1. 安装 Python 依赖 ────────────────────────────────
echo "[1/5] 安装 Python 依赖..."
echo "  ⚠️  首次安装包含语义搜索模型（sentence-transformers + all-MiniLM-L6-v2，约 90MB），请稍候..."
if command -v pip &> /dev/null; then
  pip install -r "$HUNTER_DIR/requirements.txt" || \
  pip3 install -r "$HUNTER_DIR/requirements.txt"
elif command -v conda &> /dev/null; then
  conda install -q -y pip 2>/dev/null && pip install -r "$HUNTER_DIR/requirements.txt"
else
  echo "  ⚠️  未找到 pip，请先安装 Python 3.10+"
  exit 1
fi
echo "  ✅ 依赖安装完成（含语义搜索支持）"

# ── 2. 配置 ─────────────────────────────────────────────
echo "[2/5] 初始化配置..."
CONFIG="$CONFIG_DIR/config.json"
if [ ! -f "$CONFIG" ]; then
  echo "{}" > "$CONFIG"
fi
echo "  → 配置文件: $CONFIG"

# ── 3. 系统密钥链 ─────────────────────────────────────
echo "[3/5] 配置系统密钥链..."

if $IS_MAC; then
  # macOS: 检查 security 命令
  if ! command -v security &> /dev/null; then
    echo "  ⚠️  security 命令不存在，请确保已安装 macOS Command Line Tools"
  fi
  echo "  → macOS Keychain（security 命令）"

elif $IS_LINUX; then
  # Linux: 检查 secret-tool
  if ! command -v secret-tool &> /dev/null; then
    echo "  ⚠️  secret-tool 未安装"
    echo "  → 安装方法（Ubuntu/Debian）: sudo apt install libsecret-tools"
    echo "  → 安装方法（Fedora）: sudo dnf install libsecret"
    echo "  → 安装方法（Arch）: sudo pacman -S libsecret"
  else
    echo "  → Linux GNOME Keyring（secret-tool）"
  fi

elif $IS_WINDOWS; then
  # Windows: cmdkey 内置
  echo "  → Windows 凭据管理器（cmdkey）"
fi

# ── 4. 开机自启 ───────────────────────────────────────
echo "[4/5] 配置开机自启..."
if $IS_MAC; then
  mkdir -p "$HOME/Library/LaunchAgents"
  # amber-hunter 主服务
  PLIST="$HOME/Library/LaunchAgents/com.huper.amber-hunter.plist"
  sed -e "s|AMBER_HUNTER_DIR|$HUNTER_DIR|g" \
      "$HUNTER_DIR/com.huper.amber-hunter.plist" > "$PLIST"
  chmod 644 "$PLIST"
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load "$PLIST" 2>/dev/null || true
  echo "  ✅ amber-hunter LaunchAgent 已安装"
  # proactive 自动巡逻（每 10 分钟）
  NODE_BIN=$(command -v node 2>/dev/null || echo "")
  if [ -n "$NODE_BIN" ]; then
    PROACTIVE_PLIST="$HOME/Library/LaunchAgents/com.huper.amber-proactive.plist"
    sed -e "s|AMBER_NODE_PATH|$NODE_BIN|g" \
        -e "s|AMBER_HUNTER_DIR|$HUNTER_DIR|g" \
        -e "s|AMBER_HOME|$HOME|g" \
        "$HUNTER_DIR/proactive/com.huper.amber-proactive.plist" > "$PROACTIVE_PLIST"
    chmod 644 "$PROACTIVE_PLIST"
    launchctl unload "$PROACTIVE_PLIST" 2>/dev/null || true
    launchctl load "$PROACTIVE_PLIST" 2>/dev/null || true
    echo "  ✅ amber-proactive LaunchAgent 已安装（每 10 分钟自动捕获记忆）"
  else
    echo "  ⚠️  未找到 node，跳过 proactive 安装（可后续运行: brew install node）"
  fi"

elif $IS_LINUX; then
  SERVICE_DIR="$HOME/.config/systemd/user"
  mkdir -p "$SERVICE_DIR"
  cat > "$SERVICE_DIR/amber-hunter.service" << SERVICE_EOF
[Unit]
Description=Amber Hunter - Local perception engine for Huper

[Service]
ExecStart=$(command -v python3) "$HUNTER_DIR/amber_hunter.py"
Restart=on-failure
RestartSec=10
WorkingDirectory=$HUNTER_DIR

[Install]
WantedBy=default.target
SERVICE_EOF
  systemctl --user daemon-reload 2>/dev/null || true
  systemctl --user enable amber-hunter 2>/dev/null || true
  systemctl --user start amber-hunter 2>/dev/null || true
  echo "  ✅ systemd 用户服务已安装"

elif $IS_WINDOWS; then
  # Windows: 任务计划程序
  SCRIPT="$CONFIG_DIR/amber-hunter.ps1"
  cat > "$SCRIPT" << 'PS_EOF'
$python = (Get-Command python -ErrorAction SilentlyContinue).Source
$script = "$PSScriptRoot\..\..\..\skills\amber-hunter\amber_hunter.py"
Start-Process $python -ArgumentList $script -WindowStyle Hidden
PS_EOF
  SCHTASKS=$(command -v schtasks 2>/dev/null || echo "")
  if [ -n "$SCHTASKS" ]; then
    schtasks /create /tn "Amber Hunter" /tr "powershell -WindowStyle Hidden -File $SCRIPT" \
      /sc onlogon /f 2>/dev/null || true
    echo "  ✅ Windows 任务计划已创建"
  else
    echo "  ⚠️  schtasks 不可用，请手动创建任务计划"
  fi
fi

# ── 5. 启动服务 ────────────────────────────────────────
echo "[5/5] 启动服务..."
if curl -s --max-time 1 http://localhost:18998/status > /dev/null 2>&1; then
  echo "  ✅ amber-hunter 已在运行"
else
  nohup python3 "$HUNTER_DIR/amber_hunter.py" >> "$CONFIG_DIR/amber-hunter.log" 2>&1 &
  sleep 2
  if curl -s --max-time 2 http://localhost:18998/status > /dev/null 2>&1; then
    echo "  ✅ amber-hunter 已启动"
  else
    echo "  ⚠️  启动失败，请查看 $CONFIG_DIR/amber-hunter.log"
  fi
fi

# ── 完成 ───────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 安装完成！无需账号，立即可用。"
echo ""
echo "🚀 立即查看本地记忆（无需注册）："
echo "   curl http://localhost:18998/memories"
echo ""
echo "📋 可选：注册 huper.org 解锁云端同步"
echo "   1. 打开 https://huper.org 注册账号"
echo "   2. 在 dashboard 获取 API Key，填入 ~/.amber-hunter/config.json"
echo "   3. 设置 master_password（本地加密密钥，不上传服务器）"
echo ""
echo "🔧 服务管理命令（$OS）："
if $IS_MAC; then
  echo "   状态: curl http://localhost:18998/status"
  echo "   日志: tail -f $CONFIG_DIR/amber-hunter.log"
  echo "   启动: launchctl load ~/Library/LaunchAgents/com.huper.amber-hunter.plist"
  echo "   停止: launchctl unload ~/Library/LaunchAgents/com.huper.amber-hunter.plist"
elif $IS_LINUX; then
  echo "   状态: curl http://localhost:18998/status"
  echo "   日志: tail -f $CONFIG_DIR/amber-hunter.log"
  echo "   启动: systemctl --user start amber-hunter"
  echo "   停止: systemctl --user stop amber-hunter"
elif $IS_WINDOWS; then
  echo "   状态: curl http://localhost:18998/status"
  echo "   日志: Get-Content $CONFIG_DIR\\amber-hunter.log -Tail 20"
  echo "   重启: Restart-Service amber-hunter 2>/dev/null || 手动重启"
fi
echo ""
echo "🔗 GitHub: https://github.com/ankechenlab-node/amber_hunter"
