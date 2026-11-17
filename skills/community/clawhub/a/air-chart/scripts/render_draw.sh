#!/usr/bin/env bash
# render_draw.sh — x-cmd Draw URL 构造器 (URL-as-Data)
# 不自行渲染图表: 数据编码进 https://x-cmd.com/draw URL, 由 x-cmd Draw 服务渲染。
# 默认仅输出 URL; 指定 --out file.svg|file.png 时下载对应格式。
#
#   render_draw.sh line --title T --subtitle S --unit U \
#       --series "名称1:文件1" ["名称2:文件2" ...] [--who 数值] [--who-label 文本] \
#       [--theme light|dark] [--out out.svg|out.png]
#   render_draw.sh bar --title T --subtitle S --unit U \
#       --items "名称1:数值1" ["名称2:数值2" ...] \
#       [--theme light|dark] [--out out.svg|out.png]
set -euo pipefail
MODE=""; TITLE=""; SUBTITLE=""; UNIT=""; WHO=""; WHO_LABEL="WHO 24h"
THEME="light"; STYLE="opendata"; OUT=""
declare -a SPECS=()

while (( $# )); do
  case "$1" in
    line|bar) MODE="$1"; shift ;;
    --title) TITLE="$2"; shift 2 ;;
    --subtitle) SUBTITLE="$2"; shift 2 ;;
    --unit) UNIT="$2"; shift 2 ;;
    --series|--items) shift; while (( $# )) && [[ "$1" != --* ]]; do SPECS+=("$1"); shift; done ;;
    --who) WHO="$2"; shift 2 ;;
    --who-label) WHO_LABEL="$2"; shift 2 ;;
    --theme) THEME="$2"; shift 2 ;;
    --style) STYLE="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    *) printf 'render_draw: unknown option %s\n' "$1" >&2; exit 1 ;;
  esac
done
[[ -n "$MODE" && ${#SPECS[@]} -gt 0 ]] || { printf 'render_draw: mode and series/items are required\n' >&2; exit 1; }

# ---------- URL 编码 (保留分隔符 , : 由调用方拼接, 此处编码最小单元) ----------
if jq -rn '""|@uri' >/dev/null 2>&1; then
  enc() { jq -rn --arg s "$1" '$s|@uri'; }
else
  enc() { python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=""))' "$1"; }
fi

DRAW_BASE="https://x-cmd.com/draw"
title_enc="$(enc "${SUBTITLE:+${TITLE} · ${SUBTITLE}}")"
[[ -z "$title_enc" ]] && title_enc="$(enc "$TITLE")"
unit_enc="$(enc "$UNIT")"
scheme=""; [[ "$THEME" == "dark" ]] && scheme="&scheme=dark"
# opendata 主题在 hbar 模式下会丢标题(x-cmd Draw 布局问题), 柱状图默认改用 evil-glow
bar_style="$STYLE"; [[ "$MODE" == "bar" && "$bar_style" == "opendata" ]] && bar_style="evil-glow"
style_enc=""; [[ -n "$bar_style" && "$bar_style" != "shadcn" ]] && style_enc="&t=$(enc "$bar_style")"

if [[ "$MODE" == "line" ]]; then
  # 读取各序列, 对齐到序列 1 的时间槽; 任意序列缺失的槽位整槽丢弃 (严禁零填充)
  declare -a LAB=() NAMES=() keep=()
  declare -A SV   # SV[$si,$j] = 数值 或 __GAP__
  ns=0
  for s in "${SPECS[@]}"; do
    name="${s%%:*}"; file="${s#*:}"
    if (( ns == 0 )); then
      mapfile -t LAB < <(cut -f1 "$file")
    fi
    j=0
    while IFS=$'\t' read -r _ v; do
      SV[$ns,$j]="$v"
      j=$((j + 1))
    done < "$file"
    NAMES+=("$name")
    ns=$((ns + 1))
  done
  labels_csv=""
  for j in "${!LAB[@]}"; do
    gap=0
    for ((si = 0; si < ns; si++)); do
      if [[ "${SV[$si,$j]:-__GAP__}" == "__GAP__" ]]; then gap=1; fi
    done
    if (( gap )); then continue; fi
    keep+=("$j")
    labels_csv+="${labels_csv:+,}$(enc "${LAB[$j]}")"
  done
  query="$DRAW_BASE?type=line&title=$title_enc"
  [[ -n "$unit_enc" ]] && query+="&unit=$unit_enc"
  query+="&labels=$labels_csv"
  for ((si = 0; si < ns; si++)); do
    csv=""
    for j in "${keep[@]}"; do csv+="${csv:+,}${SV[$si,$j]}"; done
    query+="&series=$(enc "${NAMES[$si]}"):$csv"
  done
  # WHO 基准线: 以常量序列形式注入 ("URL 即数据"的体现)
  if [[ -n "$WHO" ]]; then
    who_csv=""
    for _ in "${keep[@]}"; do who_csv+="${who_csv:+,}$WHO"; done
    query+="&series=$(enc "$WHO_LABEL"):$who_csv"
  fi
  query+="&w=960&h=500${scheme}${style_enc}"
else
  names_csv=""; vals_csv=""
  for s in "${SPECS[@]}"; do
    names_csv+="${names_csv:+,}$(enc "${s%%:*}")"
    vals_csv+="${vals_csv:+,}${s#*:}"
  done
  query="$DRAW_BASE?type=hbar&title=$title_enc"
  [[ -n "$unit_enc" ]] && query+="&unit=$unit_enc"
  query+="&labels=$names_csv&values=$vals_csv&num=all&w=960&h=$((120 + 60 * ${#SPECS[@]}))${scheme}${style_enc}"
fi

printf '%s\n' "$query"

# ---------- 可选: 下载 SVG/PNG ----------
if [[ -n "$OUT" ]]; then
  case "$OUT" in
    *.svg) dl="$query" ;;
    *.png) dl="${query}&format=png" ;;
    *) printf 'render_draw: --out must end in .svg or .png\n' >&2; exit 1 ;;
  esac
  case "$dl" in
    "$DRAW_BASE"|"$DRAW_BASE?"*|"$DRAW_BASE/"*) ;;
    *) printf 'render_draw: refuse non-x-cmd draw URL\n' >&2; exit 1 ;;
  esac
  tmp="$OUT.part.$$"
  if curl -sL -A 'x-cmd-air-chart/0.1.0 (+https://x-cmd.com/draw)' --max-time 40 -o "$tmp" "$dl"; then
    if [[ "$OUT" == *.png ]]; then
      ok=$(od -An -tx1 -N4 "$tmp" 2>/dev/null | tr -d ' \n'); ok="${ok:0:8}"
      [[ "$ok" == "89504e47" ]] || { rm -f "$tmp"; printf 'render_draw: PNG validation failed\n' >&2; exit 4; }
    else
      head -c 1 "$tmp" | grep -q '<' || { rm -f "$tmp"; printf 'render_draw: SVG validation failed\n' >&2; exit 4; }
    fi
    mv "$tmp" "$OUT"
    printf 'saved: %s (%s bytes)\n' "$OUT" "$(wc -c < "$OUT" | tr -d ' ')" >&2
  else
    rm -f "$tmp"
    printf 'render_draw: download failed (network?). Open the URL above in a browser instead.\n' >&2
    exit 4
  fi
fi
