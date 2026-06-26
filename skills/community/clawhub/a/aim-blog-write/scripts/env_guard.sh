#!/bin/bash
# ============================================================
# env_guard —— aim-secret-key 校验
#
# 与 digital-human-video skill 一致的策略：
#   - 密钥唯一来源：本 skill 根目录下的 .env 文件
#   - 键名规范：aim-secret-key（小写、连字符）
#   - 不读进程环境变量、不读家目录、不跨 agent 复用
#
#
# 使用方式:
#   - 作为库 source:           source env_guard.sh && ensure_aep_env
#   - 启动前自检 (JSON 输出):  bash env_guard.sh --check-config
# ============================================================

AIM_APPLY_URL="http://192.168.25.10:30775/aim-skills"
AEP_BASE_URL_FIXED="http://aep.vemic.com/aim_mentaassistant_2024"
SECRET_KEY_NAME="aim-secret-key"

# ---------- 定位 skill 根目录与 .env ----------
_guard_skill_root() {
    local here
    here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    (cd "${here}/.." && pwd)
}

_guard_env_file() {
    echo "$(_guard_skill_root)/.env"
}

# ---------- 从 <skill>/.env 解析 aim-secret-key ----------
# 输出: <value>\t<source>；未命中则空输出、退出码 1
_guard_resolve_secret() {
    local file
    file="$(_guard_env_file)"
    [ -f "${file}" ] || return 1

    local line key value
    while IFS= read -r line || [ -n "${line}" ]; do
        # 去掉首尾空白
        line="${line#"${line%%[![:space:]]*}"}"
        line="${line%"${line##*[![:space:]]}"}"
        [ -z "${line}" ] && continue
        case "${line}" in \#*) continue ;; esac
        [[ "${line}" == *=* ]] || continue

        key="${line%%=*}"
        value="${line#*=}"
        # 去掉包裹的引号
        case "${value}" in
            \"*\") value="${value%\"}"; value="${value#\"}" ;;
            \'*\') value="${value%\'}"; value="${value#\'}" ;;
        esac

        if [ "${key}" = "${SECRET_KEY_NAME}" ] && [ -n "${value}" ]; then
            printf '%s\t%s\n' "${value}" "file:${file}"
            return 0
        fi
    done < "${file}"
    return 1
}

# ---------- 加载到环境（供 curl 用）----------
_guard_load_secret() {
    local result value
    result="$(_guard_resolve_secret)" || return 1
    value="${result%%$'\t'*}"
    [ -z "${value}" ] && return 1
    export "AEP_CONSUMER_SECRET=${value}"
    return 0
}

_guard_load_base_url() {
    export "AEP_BASE_URL=${AEP_BASE_URL_FIXED}"
}

# ---------- 对外主入口 ----------
ensure_aep_env() {
    _guard_load_base_url
    if ! _guard_load_secret; then
        local env_file
        env_file="$(_guard_env_file)"
        {
            echo ""
            echo "=============================================="
            echo "  aim-secret-key 未配置"
            echo "  1. 到 ${AIM_APPLY_URL} 注册并拿到密钥"
            echo "  2. 把密钥粘给 agent，由它写入 ${env_file}"
            echo "     格式：一行 aim-secret-key=<你的密钥>"
            echo "=============================================="
            echo ""
        } >&2
        printf '{"success": false, "msg": "缺少 aim-secret-key，请先到 %s 申请后写入 %s"}\n' \
            "${AIM_APPLY_URL}" "${env_file}"
        return 1
    fi
    return 0
}

# ---------- 启动前自检 ----------
check_config_report() {
    local result value source env_file env_file_exists configured
    env_file="$(_guard_env_file)"
    env_file_exists="false"
    [ -f "${env_file}" ] && env_file_exists="true"

    result="$(_guard_resolve_secret || true)"
    value="${result%%$'\t'*}"
    source="${result#*$'\t'}"
    [ "${source}" = "${result}" ] && source=""
    if [ -n "${value}" ]; then
        configured="true"
    else
        configured="false"
        source=""
    fi

    python3 - "$configured" "$source" "$env_file" "$env_file_exists" "$AEP_BASE_URL_FIXED" "$SECRET_KEY_NAME" <<'PY'
import json, sys
configured = sys.argv[1] == "true"
source = sys.argv[2] or None
env_file = sys.argv[3]
env_file_exists = sys.argv[4] == "true"
base_url = sys.argv[5]
key_name = sys.argv[6]
report = {
    "aim_secret_key_configured": configured,
    "resolved_from": source,
    "env_file": env_file,
    "env_file_exists": env_file_exists,
    "key_name_in_env": key_name,
    "aep_base_url": base_url,
    "isolation_policy": "本脚本只读 skill 目录下的 .env，不看环境变量、不读家目录、不跨 agent 复用密钥",
    "next_action": (
        "ready" if configured
        else f"引导用户到 http://192.168.25.10:30775/aim-skills 注册取到密钥后，写入 {env_file} 的 {key_name} 字段"
    ),
}
print(json.dumps(report, ensure_ascii=False, indent=2))
PY
    if [ "${configured}" = "true" ]; then
        return 0
    else
        return 2
    fi
}

# ---------- 直接执行 ----------
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    case "${1:-}" in
        --check-config)
            check_config_report
            exit $?
            ;;
        *)
            ensure_aep_env
            exit $?
            ;;
    esac
fi
