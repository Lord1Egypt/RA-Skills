#!/usr/bin/env bash
# geo_resolve.sh — 城市名 -> 经纬度/时区 解析模块
# 用法: geo_resolve.sh "Beijing"  ->  stdout: name \t country \t lat \t lon \t timezone
#        geo_resolve.sh "39.9,116.4" -> 直接按坐标解析(时区回落为 UTC)
set -euo pipefail

GEO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CITIES_TSV="${AIR_CHART_CITIES_TSV:-$GEO_DIR/../data/top_cities.tsv}"

die() { printf 'geo_resolve: %s\n' "$*" >&2; exit 1; }

_lang() { local l="${AIR_CHART_LANG:-${LC_ALL:-${LC_MESSAGES:-${LANG:-}}}}"; [[ "$l" == zh* ]] && printf 'zh' || printf 'en'; }

normalize() {
  # 小写、去首尾空白、压缩内部空白为单个空格（便于匹配）
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/[[:space:]]\+/ /g'
}

lookup_city() {
  local q; q="$(normalize "$1")"
  local hit
  # 精确匹配（规范名 或 中文名）
  hit="$(awk -F'\t' -v q="$q" '
    { n=$1; gsub(/^[ \t]+|[ \t]+$/,"",n); l=tolower(n); gsub(/ /,"_",l); gsub(/-/,"_",l);
      if (l == q || tolower(n) == q || $6 == q) { print; exit } }
  ' "$CITIES_TSV")"
  [[ -n "$hit" ]] && { printf '%s\n' "$hit"; return 0; }
  # 包含匹配（如 "delhi" -> "New Delhi", "中山" -> "中山市"）
  awk -F'\t' -v q="$q" '
    { n=$1; l=tolower(n); gsub(/ /,"_",l); gsub(/-/,"_",l);
      if (index(l, q) > 0 || index(tolower(n), q) > 0 || index($6, q) > 0) { print; exit } }
  ' "$CITIES_TSV"
}

main() {
  local input="${1:-}"
  [[ -z "$input" ]] && { if [[ "$(_lang)" == "zh" ]]; then printf 'geo_resolve: 城市名不能为空。\n' >&2; else printf 'geo_resolve: city name must not be empty.\n' >&2; fi; exit 2; }
  # 直接坐标输入: "lat,lon"
  if [[ "$input" =~ ^[[:space:]]*-?[0-9]+(\.[0-9]+)?[[:space:]]*,[[:space:]]*-?[0-9]+(\.[0-9]+)?[[:space:]]*$ ]]; then
    local lat lon
    lat="$(printf '%s' "$input" | cut -d, -f1 | tr -d ' ')"
    lon="$(printf '%s' "$input" | cut -d, -f2 | tr -d ' ')"
    printf 'custom\t--\t%s\t%s\tUTC\n' "$lat" "$lon"
    return 0
  fi

  local hit
  hit="$(lookup_city "$input")"
  if [[ -n "$hit" ]]; then
    printf '%s\n' "$hit"
    return 0
  fi

  # 未命中: 输出相近建议, 便于 Agent 纠错
  local q; q="$(normalize "$input")"
  if [[ "$(_lang)" == "zh" ]]; then
    printf 'geo_resolve: 城市 "%s" 不在内置坐标库中。\n相近候选:\n' "$input" >&2
    awk -F'\t' -v q="$q" 'tolower($1) ~ substr(q,1,3) { printf "  - %s (%s)\n", $1, $2 }' "$CITIES_TSV" | head -5 >&2
    printf '提示: 也可直接传入坐标, 如 "39.9,116.4"。\n' >&2
  else
    printf 'geo_resolve: city "%s" not in the built-in gazetteer.\nClose candidates:\n' "$input" >&2
    awk -F'\t' -v q="$q" 'tolower($1) ~ substr(q,1,3) { printf "  - %s (%s)\n", $1, $2 }' "$CITIES_TSV" | head -5 >&2
    printf 'Tip: you can also pass coordinates directly, e.g. "39.9,116.4".\n' >&2
  fi
  exit 2
}

main "$@"
