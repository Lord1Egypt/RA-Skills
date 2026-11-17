#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# inspect_pages.sh — 逐页版式体检（本技能入口，委托给 html-to-pdf-cdp 的实现）
#
# 用法：
#   bash inspect_pages.sh <in.html> [outDirForPng]
#
# 为什么是「委托」而不是自己实现：
#   把 Chrome 起在同一个前台进程里 + 端口自愈 + trap 收尾，这套逻辑
#   html-to-pdf-cdp 已经有（`measure_pages_selfhost.sh`）。本技能再抄一份只会漂移。
#   上游缺失时才报错退出，不复刻一份。
#
# 见 SKILL.md「步骤 2」，关键是看 over 列：A4 横向的溢出阈值是 794px（210mm）。
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

IN="${1:-}"
[ -n "$IN" ] || { sed -n '3,12p' "$0"; exit 2; }
[ -f "$IN" ] || { echo "[!] 找不到 HTML：$IN"; exit 1; }

UPSTREAM="$HOME/.workbuddy/skills/html-to-pdf-cdp/scripts/measure_pages_selfhost.sh"
if [ ! -f "$UPSTREAM" ]; then
  cat >&2 <<'MSG'
[!] 缺上游脚本：html-to-pdf-cdp/scripts/measure_pages_selfhost.sh

本技能的逐页体检依赖它（它负责在同一个前台进程里起 Chrome —— 受限沙箱里
后台常驻的 Chrome 会被回收，直接跑 measure_pages.js 会报 fetch failed）。

请先确认 html-to-pdf-cdp 技能已安装，或手工执行：
  bash ~/.workbuddy/skills/html-to-pdf-cdp/scripts/measure_pages_selfhost.sh <in.html> 1123 794
MSG
  exit 1
fi

exec bash "$UPSTREAM" "$IN" 1123 794 ${2:+"$2"}
