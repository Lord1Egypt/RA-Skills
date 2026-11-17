#!/bin/bash
# Voice calibration for /aikey-mvp: print your own top-10 X posts by bookmark rate.
# Filters: canonical author + impressions >= 1000 (drop small-sample noise) + not a reply.
# CSV fields: role,bookmark_rate,bookmarks,impressions,url,text
#
# CSV 路径按这个顺序找，第一个存在的就用：
#   1. $ZMM_XPOSTS_CSV        （直接指定）
#   2. config.yaml 的 paths.vault_root 下 01-原始素材区/数据/候选池/*素材候选池.csv
#   3. 报错退出 —— 不猜路径
set -euo pipefail

CSV="${ZMM_XPOSTS_CSV:-}"

if [ -z "$CSV" ]; then
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
  VAULT="$(sed -n 's/^[[:space:]]*vault_root:[[:space:]]*//p' "$ROOT/config.yaml" 2>/dev/null | tr -d '"'"'"' ' | head -1)"
  VAULT="${VAULT/#\~/$HOME}"
  [ -n "$VAULT" ] && CSV="$(find "$VAULT/01-原始素材区/数据/候选池" -name '*素材候选池.csv' 2>/dev/null | head -1)"
fi

if [ -z "$CSV" ] || [ ! -f "$CSV" ]; then
  echo "找不到 X 帖子 CSV。用 ZMM_XPOSTS_CSV 指一个，或在 config.yaml 里设 paths.vault_root。" >&2
  exit 1
fi

awk -F, '$1=="本人(canonical)" && $4>=1000 && $6 !~ /^@/' "$CSV" | sort -t, -k2 -rn | head -10
