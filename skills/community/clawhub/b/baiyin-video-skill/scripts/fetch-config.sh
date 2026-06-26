#!/usr/bin/env bash
# 获取视频配置（带缓存）
# 用法: bash fetch-config.sh
# 输出: 缓存文件路径
# 环境变量: BAIYIN_API_KEY
# 可选: BAIYIN_CACHE_FILE（自定义缓存路径）, BAIYIN_SKIP_CACHE=1（强制刷新）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

check_env

CACHE_FILE="$(get_cache_file)"
CACHE_MAX_AGE=3600

need_fetch=true
if [[ "${BAIYIN_SKIP_CACHE:-}" != "1" ]] && [[ -f "$CACHE_FILE" ]]; then
  # 验证缓存文件有效性
  if ! head -c 1 "$CACHE_FILE" | grep -q '{'; then
    need_fetch=true
  else
    if [[ "$(uname)" == "Darwin" ]]; then
      file_age=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE") ))
    else
      file_age=$(( $(date +%s) - $(stat -c %Y "$CACHE_FILE") ))
    fi
    if (( file_age < CACHE_MAX_AGE )); then
      need_fetch=false
    fi
  fi
fi

if $need_fetch; then
  http_code=$(curl_auth -w "%{http_code}" -o "$CACHE_FILE" \
    "${BASE_URL}/api/open/v1/video/config")

  if [[ "$http_code" != "200" ]]; then
    rm -f "$CACHE_FILE"
    echo "ERROR: /video/config 返回 HTTP $http_code" >&2
    exit 1
  fi

  if ! head -c 1 "$CACHE_FILE" | grep -q '{'; then
    rm -f "$CACHE_FILE"
    echo "ERROR: 响应不是有效 JSON" >&2
    exit 1
  fi
fi

echo "$CACHE_FILE"
