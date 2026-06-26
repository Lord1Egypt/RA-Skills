#!/usr/bin/env bash
# ClawdHub 一键发布脚本
# 用法: bash scripts/publish-clawdhub.sh
# 前置: 没有任何前置 — 脚本会自动安装 CLI、注册 Agent、发布技能

set -e

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "========================================"
echo "  ClawdHub publish — beautsgo-booking"
echo "========================================"
echo ""

# Step 1: 装 CLI(如果没装)
if ! command -v claw >/dev/null 2>&1; then
  echo "[1/3] 安装 @openclaw-cn/cli ..."
  npm install -g @openclaw-cn/cli
else
  echo "[1/3] CLI 已安装,跳过。版本: $(claw --version)"
fi
echo ""

# Step 2: 注册 Agent(如果未登录)
if claw whoami 2>/dev/null | grep -qv "未登录"; then
  echo "[2/3] 已登录: $(claw whoami)"
else
  echo "[2/3] 注册 Agent..."
  claw register \
    -i beautsgo \
    -n BeautsGO \
    -d "韩国医美预约" \
    -b "BeautsGO 出品 - 一键预约韩国 1300+ 顶级医美机构" \
    -a "$ROOT/.claw-agent/avatar.svg"

  echo ""
  echo "⚠️  请记下上面输出里的 Access Token,以后换机器用 claw login -t <token> 重新登录"
fi
echo ""

# Step 3: 发布技能
echo "[3/3] 发布 beautsgo-booking@$(grep '"version"' skill.json | head -1 | sed 's/.*: "\(.*\)".*/\1/') 到 ClawdHub..."
claw skill publish

echo ""
echo "✅ 完成。等审核(通常 24h 内)。"
echo "   验证: https://clawd.org.cn/market/ 搜 beautsgo"
