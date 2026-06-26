#!/bin/bash
# ============================================================
# 公共函数库 —— 校验密钥、发送 AEP 同步请求
#
# 密钥来源：<skill_root>/.env 的 aim-secret-key（与数字人 skill 一致）
# ============================================================

_COMMON_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${_COMMON_DIR}/env_guard.sh"

require_env() {
    ensure_aep_env || exit 1
}

# 同步请求：直接发请求等结果返回
# 参数: $1=路径(以/开头)  $2=JSON body
run_skill_sync() {
    local path="$1"
    local body="$2"

    require_env

    local url="${AEP_BASE_URL}${path}"
    local timeout="${AEP_TIMEOUT:-600}"

    echo ">>> AEP sync request -> ${url}" >&2

    curl -s -N --noproxy '*' --max-time "${timeout}" -X POST "${url}" \
        -H "Content-Type: application/json" \
        -H "X-AEP-CONSUMER-SECRET: ${AEP_CONSUMER_SECRET}" \
        -d "${body}"
}
