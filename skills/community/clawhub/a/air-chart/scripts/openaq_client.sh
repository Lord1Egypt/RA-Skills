#!/usr/bin/env bash
# openaq_client.sh — OpenAQ API v3 轻量封装
# 职责: 鉴权、本地缓存(TTL)、429 限流退避、站点优选、时间序列拉取
# 依赖: curl / jq / awk(即本仓库零重型依赖主张)
set -euo pipefail

OPENAQ_API_BASE="${OPENAQ_API_BASE:-https://api.openaq.org/v3}"
AIR_CHART_CACHE_DIR="${AIR_CHART_CACHE_DIR:-$HOME/.cache/air-chart}"
AIR_CHART_TIMEOUT="${AIR_CHART_TIMEOUT:-20}"
AIR_CHART_MAX_RETRY="${AIR_CHART_MAX_RETRY:-4}"
AIR_CHART_UA="${AIR_CHART_UA:-x-cmd-air-chart/0.1.0}"

_OAC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARAMS_TSV="${AIR_CHART_PARAMS_TSV:-$_OAC_DIR/../data/parameters.tsv}"

air_chart_err() { printf '[air-chart] ERROR: %s\n' "$*" >&2; }

# 静态参数字典查询: param_field <slug> <列号>  列: 1slug 2id 3名称 4单位 5WHO基准 6物理上限 7色 8深色色
param_field() { awk -F'\t' -v s="$1" -v c="$2" '$1==s {print $c; exit}' "$PARAMS_TSV"; }
param_slugs() { awk -F'\t' 'NR>1 && $1 !~ /^#/ {print $1}' "$PARAMS_TSV" | tr '\n' ' ' | sed 's/ $//'; }

# 语言: 优先取 air_chart.sh 设置的 AIR_CHART_LANG, 否则按 locale 自动检测
_oac_lang() {
  local l="${AIR_CHART_LANG:-${LC_ALL:-${LC_MESSAGES:-${LANG:-}}}}"
  [[ "$l" == zh* ]] && printf 'zh' || printf 'en'
}

# ---------- 鉴权 (轻量化分层策略, 不依赖系统钥匙串) ----------
# 优先级: 1) 环境变量 OPENAQ_API_KEY  2) ~/.config/air-chart/config  3) ~/.air-chart.env
openaq_api_key() {
  if [[ -n "${OPENAQ_API_KEY:-}" ]]; then
    printf '%s' "$OPENAQ_API_KEY"; return 0
  fi
  local f
  for f in "${XDG_CONFIG_HOME:-$HOME/.config}/air-chart/config" "$HOME/.air-chart.env"; do
    if [[ -f "$f" ]]; then
      local k
      k="$(sed -n 's/^OPENAQ_API_KEY=//p' "$f" | tail -n1 | tr -d '"'"'"' \r')"
      if [[ -n "$k" ]]; then printf '%s' "$k"; return 0; fi
    fi
  done
  return 1
}

openaq_require_key() {
  if ! openaq_api_key >/dev/null; then
    if [[ "$(_oac_lang)" == "zh" ]]; then
      cat >&2 <<'EOF'
[Notice] 未检测到 OPENAQ_API_KEY，无法请求 OpenAQ API v3。
  首次使用请按以下步骤免费获取 Key（约 1 分钟）:
    1. 注册/登录: https://explore.openaq.org/register
       (已有账号直接登录: https://explore.openaq.org/login)
    2. 登录后打开账户页: https://explore.openaq.org/account
       页面下方即可看到并复制你的 API Key
    3. 配置（任选其一）:
       export OPENAQ_API_KEY="你的key"                              # 临时/CI
       echo 'OPENAQ_API_KEY=你的key' > ~/.config/air-chart/config   # 持久
  也可以先用 --demo 预览效果（无需 Key）。
EOF
    else
      cat >&2 <<'EOF'
[Notice] OPENAQ_API_KEY not found — the OpenAQ API v3 requires a key.
  First-time setup (free, ~1 minute):
    1. Register or log in: https://explore.openaq.org/register
       (existing account: https://explore.openaq.org/login)
    2. After logging in, open your account page:
       https://explore.openaq.org/account
       Your API key is shown near the bottom — copy it.
    3. Configure it (either one):
       export OPENAQ_API_KEY="your_key"                              # ephemeral/CI
       echo 'OPENAQ_API_KEY=your_key' > ~/.config/air-chart/config   # persistent
  Tip: use --demo to preview the charts without a key.
EOF
    fi
    exit 3
  fi
}

# ---------- 缓存 ----------
_cache_key() { printf '%s' "$1" | md5sum | awk '{print $1}'; }

_cache_get() { # _cache_get <key> <ttl_seconds>
  local f="$AIR_CHART_CACHE_DIR/$1"
  [[ -f "$f" ]] || return 1
  local now mtime
  now="$(date +%s)"
  mtime="$(date -r "$f" +%s 2>/dev/null || stat -c %Y "$f")"
  (( now - mtime <= $2 )) || return 1
  cat "$f"
}

_cache_put() { # _cache_put <key> <content>
  mkdir -p "$AIR_CHART_CACHE_DIR"
  printf '%s' "$2" > "$AIR_CHART_CACHE_DIR/$1"
}

# ---------- 带限流退避的请求 ----------
_openaq_get() { # _openaq_get <path-with-query> <ttl_seconds>
  local path="$1" ttl="${2:-1200}"
  local key; key="$(_cache_key "$path")"
  local cached
  if cached="$(_cache_get "$key" "$ttl")"; then
    printf '%s' "$cached"; return 0
  fi

  local api_key; api_key="$(openaq_api_key)" || exit 3
  local attempt=1 wait backoff=2
  local body http_code
  while (( attempt <= AIR_CHART_MAX_RETRY )); do
    body="$(curl -sS --max-time "$AIR_CHART_TIMEOUT" -w $'\n%{http_code}' \
      -H "X-API-Key: $api_key" -H 'Accept: application/json' \
      -H "User-Agent: $AIR_CHART_UA" \
      "${OPENAQ_API_BASE}${path}" 2>/dev/null)" || body=$'curl_failed\n000'
    http_code="$(printf '%s' "$body" | tail -n1)"
    body="$(printf '%s' "$body" | sed '$d')"

    case "$http_code" in
      200)
        _cache_put "$key" "$body"
        printf '%s' "$body"; return 0 ;;
      429)
        # 指数退避: 2s 起步倍增, 上限 30s
        wait=$backoff; (( backoff > 30 )) && wait=30
        sleep "$wait"; backoff=$(( backoff * 2 ))
        (( attempt++ )) ;;
      401|403)
        if [[ "$(_oac_lang)" == "zh" ]]; then
          air_chart_err "AUTH_ERROR: OPENAQ_API_KEY 无效或未配置 (HTTP $http_code)。"
        else
          air_chart_err "AUTH_ERROR: OPENAQ_API_KEY is invalid or missing (HTTP $http_code)."
        fi
        exit 4 ;;
      000)
        if [[ "$(_oac_lang)" == "zh" ]]; then
          air_chart_err "网络请求失败, 请检查网络连接。"
        else
          air_chart_err "Network request failed. Check your connection."
        fi
        exit 4 ;;
      *)
        air_chart_err "API_ERROR: OpenAQ request failed (HTTP $http_code): $(printf '%s' "$body" | head -c 200)"
        exit 4 ;;
    esac
  done
  if [[ "$(_oac_lang)" == "zh" ]]; then
    air_chart_err "RATE_LIMIT: OpenAQ API 请求频率超限, 已退避重试 $AIR_CHART_MAX_RETRY 次, 请稍后重试。"
  else
    air_chart_err "RATE_LIMIT: OpenAQ API rate limit hit after $AIR_CHART_MAX_RETRY retries. Please try again later."
  fi
  exit 4
}

# ---------- 站点检索与优选 ----------
openaq_find_locations() { # <lat> <lon> [radius_m] -> locations JSON
  local lat="$1" lon="$2" radius="${3:-25000}"
  _openaq_get "/locations?coordinates=${lat},${lon}&radius=${radius}&limit=100" 1800
}

# 从 locations JSON 中优选传感器; 输出: sensor_id \t units \t timezone \t location_name \t isMonitor
# 优先按参数固定 ID 匹配 (对齐 openaq-api 字典), 名称匹配兜底
_sensor_jq_filter='. as $loc
      | (.sensors // [])[] | select((.parameter.id // 0) == ($pid | tonumber)
          or (.parameter.name // "" | ascii_downcase) == $p
          or (.parameter.displayName // "" | ascii_downcase | gsub("[._]";"")) == ($p | gsub("[._]";"")))
      | { sensor_id: .id, units: (.parameter.units // ""),
          tz: ($loc.timezone // "UTC"), name: ($loc.name // $loc.locality // "unknown"),
          monitor: ($loc.isMonitor // false), last: ($loc.datetimeLast.utc // "") }'

openaq_pick_sensor() { # <locations_json> <param>
  local json="$1" param="$2" pid
  pid="$(param_field "$param" 2)"
  printf '%s' "$json" | jq -r --arg p "$param" --arg pid "${pid:-0}" "
    [ .results[]? | $_sensor_jq_filter ]
    | map(select(.last != \"\"))
    | sort_by(.monitor | not)          # 参考级监测站优先
    | .[0] // empty
    | [.sensor_id, .units, .tz, .name, (.monitor|tostring)] | @tsv"
}

openaq_pick_all_sensors() { # <locations_json> <param> — 快照模式: 输出全部活性站点的 sensor 行 (按站点去重, 参考级+最新优先)
  local json="$1" param="$2" pid
  pid="$(param_field "$param" 2)"
  printf '%s' "$json" | jq -r --arg p "$param" --arg pid "${pid:-0}" "
    [ .results[]? | $_sensor_jq_filter ]
    | map(select(.last != \"\"))
    | sort_by(.monitor | not)
    | .[] | [.sensor_id, .units, .tz, .name, (.monitor|tostring), .last] | @tsv" \
  | sort -t$'\t' -k4,4 -k6,6r | awk -F'\t' '!seen[$4]++'
}

# ---------- 活性过滤 ----------
openaq_filter_active() { # <locations_json> [max_age_hours] -> 过滤掉 datetimeLast 超龄站点的 JSON
  local json="$1" max_age="${2:-24}"
  local cutoff
  cutoff="$(date -u -d "-${max_age} hours" +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -u -v-"${max_age}"H +%Y-%m-%dT%H:%M:%S)"
  printf '%s' "$json" | jq --arg c "$cutoff" '
    .results = [ (.results // [])[] | select((.datetimeLast.utc // "") >= $c) ] | .'
}

# ---------- 时间序列 ----------
openaq_fetch_series() { # <sensor_id> <hours|days> <date_from> <date_to> -> TSV: utc \t local \t value
  local sensor_id="$1" gran="$2" from="$3" to="$4"
  local json range
  # 端点参数不对称: /hours 需要 datetime_from/to, /days 用 date_from/to
  if [[ "$gran" == hours ]]; then
    range="datetime_from=${from}&datetime_to=${to}"
  else
    range="date_from=${from}&date_to=${to}"
  fi
  json="$(_openaq_get "/sensors/${sensor_id}/${gran}?${range}&limit=1000" \
    "$( [[ "$gran" == hours ]] && echo 1200 || echo 7200 )")"
  printf '%s' "$json" | jq -r '
    (.results // [])
    | map(select(.value != null))
    | .[]
    | [ .period.datetimeFrom.utc,
        (.period.datetimeFrom.local // .period.datetimeFrom.utc),
        .value ] | @tsv'
}

openaq_fetch_latest() { # <sensor_id> -> TSV: utc \t local \t value (最新一条, 近 48h 内)
  local sensor_id="$1"
  local from
  from="$(date -u -d "-48 hours" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-48H +%Y-%m-%dT%H:%M:%SZ)"
  local json
  json="$(_openaq_get "/sensors/${sensor_id}/hours?datetime_from=${from}&limit=100" 600)"
  printf '%s' "$json" | jq -r '
    (.results // []) | sort_by(.period.datetimeFrom.utc) | last // empty
    | select(.value != null)
    | [ .period.datetimeFrom.utc, (.period.datetimeFrom.local // .period.datetimeFrom.utc), .value ] | @tsv'
}
