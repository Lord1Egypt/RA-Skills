#!/usr/bin/env bash
# 公共函数：缓存路径、环境变量校验、curl 认证头

# 固定 BASE_URL，不从环境变量读取
BASE_URL="https://ai.hikoon.com"

# 缓存文件路径（可通过 BAIYIN_CACHE_FILE 覆盖）
get_cache_file() {
  if [[ -n "${BAIYIN_CACHE_FILE:-}" ]]; then
    echo "$BAIYIN_CACHE_FILE"
  elif [[ "$(uname)" == "MINGW"* ]] || [[ "$(uname)" == "CYGWIN"* ]]; then
    echo "${TEMP:-${TMP:-C:/Temp}}/baiyin_config.json"
  else
    echo "/tmp/baiyin_config.json"
  fi
}

# 校验必需的环境变量
check_env() {
  if [[ -z "${BAIYIN_API_KEY:-}" ]]; then
    echo "ERROR: 环境变量 BAIYIN_API_KEY 未设置" >&2
    exit 1
  fi
}

# 带认证的 curl（附加超时）
curl_auth() {
  curl -s --connect-timeout 10 --max-time 30 \
    -H "Authorization: Bearer ${BAIYIN_API_KEY}" \
    -H "Content-Type: application/json" \
    "$@"
}
