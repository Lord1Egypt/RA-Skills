#!/usr/bin/env bash
# install.sh — 安装或升级 Claude Code CLI
#
# 功能:
#   - 检测当前是否已安装 claude 及其版本
#   - 版本低于 2.1.0 则升级,未安装则安装
#   - 已是最新版直接跳过,不浪费时间
#   - 确保 npm 全局路径在 PATH 中(沙箱重启不丢)
#
# 不涉及任何 Key 或 provider 的配置。

set -e

NPM_GLOBAL_BIN="$HOME/.npm-global/bin"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/helpers.sh"

# --- 1. 检查 npm ---
if ! command -v npm >/dev/null 2>&1; then
  cc_err "未检测到 npm。ArkClaw 沙箱默认自带 Node.js,若确实没有请先在沙箱中安装 Node.js。"
  exit 1
fi

# --- 2. 设置 npm 全局目录到用户家目录(避免权限问题,沙箱重启后依然存在)---
mkdir -p "$NPM_GLOBAL_BIN"
npm config set prefix "$HOME/.npm-global" >/dev/null 2>&1 || true

# 把全局 bin 目录加入 PATH(避免重复添加)
if ! grep -q '.npm-global/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> "$HOME/.bashrc"
  cc_log "已将 npm 全局 bin 目录添加到 ~/.bashrc 的 PATH 中"
fi
export PATH="$NPM_GLOBAL_BIN:$PATH"

# --- 3. 检查当前版本 ---
CURRENT_VERSION=""
if command -v claude >/dev/null 2>&1; then
  CURRENT_VERSION="$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "")"
fi

if [ -n "$CURRENT_VERSION" ] && cc_version_ge "$CURRENT_VERSION" "$CC_MIN_VERSION"; then
  cc_log "Claude Code CLI 已安装,版本 $CURRENT_VERSION(满足最低要求 $CC_MIN_VERSION),无需操作。"
  exit 0
fi

if [ -n "$CURRENT_VERSION" ]; then
  cc_warn "当前 Claude Code CLI 版本 $CURRENT_VERSION 低于最低要求 $CC_MIN_VERSION,准备升级..."
else
  cc_log "未检测到 Claude Code CLI,准备安装 $CC_NPM_PACKAGE..."
fi

# --- 4. 安装 / 升级 ---
npm install -g "${CC_NPM_PACKAGE}@latest"

NEW_VERSION="$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "?")"
cc_log "✅ Claude Code CLI 安装完成,版本 $NEW_VERSION"
cc_log "提示:新开终端或执行 source ~/.bashrc 即可生效。"
