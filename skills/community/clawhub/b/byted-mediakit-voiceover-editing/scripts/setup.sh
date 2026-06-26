#!/usr/bin/env bash
set -euo pipefail

# Step 1 环境检查与依赖安装（与 SKILL.md 一致）：
# - 若不存在 .env：从 templates/env.md 复制生成骨架文件（不写入任何云厂商密钥）。
# - 校验必填变量：优先读**当前进程环境**（与容器注入一致），否则读 `.env`（与 python load_dotenv override=False 一致）。
# - 不执行「自动化填入密钥」；用户须在本地编辑 .env 或通过宿主/容器注入环境变量。
#
# - SCRIPT_DIR: 当前脚本所在目录（.../<SKILL_DIR>/scripts）
# - 默认产物目录：<工程根>/output/（见 scripts/project_paths.py：get_project_root）
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

SKILL_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${SKILL_DIR}/.env"
ENV_TEMPLATE="${SKILL_DIR}/templates/env.md"
SCRIPT_FOLDER="${SKILL_DIR}/scripts"

echo "[1/2] 环境检查"

read_env_value() {
  local k="$1"
  if [[ ! -f "${ENV_FILE}" ]]; then
    echo ""
    return
  fi
  if ! grep -Eq "^[[:space:]]*${k}[[:space:]]*=" "${ENV_FILE}"; then
    echo ""
    return
  fi
  local raw_line
  raw_line="$(grep -E "^[[:space:]]*${k}[[:space:]]*=" "${ENV_FILE}" | sed -n '1p')"
  local raw_value="${raw_line#*=}"
  local value
  value="$(printf '%s' "${raw_value}" | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"
  if [[ "${value}" =~ ^\".*\"$ ]]; then
    value="${value:1:${#value}-2}"
  elif [[ "${value}" =~ ^\'.*\'$ ]]; then
    value="${value:1:${#value}-2}"
  fi
  printf '%s' "${value}"
}

# 与 Python load_dotenv(..., override=False) 一致：进程环境优先，再读 .env
read_effective_value() {
  local k="$1"
  local v
  v="${!k:-}"
  v="${v#"${v%%[![:space:]]*}"}"
  v="${v%"${v##*[![:space:]]}"}"
  if [[ -n "$v" ]]; then
    printf '%s' "$v"
    return
  fi
  read_env_value "$k"
}

# ─── 检测执行模式 ───
# 优先级（v1.0.9 修正）:
#   1. 进程环境 export EXECUTION_MODE=xxx  → **绝对锁定**，包括 local
#   2. .env 中 EXECUTION_MODE=xxx          → 尊重用户显式选择
#   3. 自动检测: apig(ARK_SKILL_API_*) > cloud(VOLC_*+ASR_*) > local
# 用户显式指定 local 时，即使存在 APIG 环境变量也不做"自动升级"。
_ORIG_PROC_MODE="${EXECUTION_MODE:-}"
_FILE_EXEC_MODE="$(read_env_value EXECUTION_MODE)"
IS_LOCAL_MODE=0

# ── 1. 用户显式指定 → 绝对锁定 ──
_explicit_mode=""
if [[ -n "$_ORIG_PROC_MODE" ]]; then
  _explicit_mode="$_ORIG_PROC_MODE"
elif [[ -n "$_FILE_EXEC_MODE" ]]; then
  _explicit_mode="$_FILE_EXEC_MODE"
fi

if [[ -n "$_explicit_mode" ]]; then
  EXECUTION_MODE="$_explicit_mode"
  case "$_explicit_mode" in
    local)
      IS_LOCAL_MODE=1
      echo "[信息] 执行模式: local（用户显式指定）"
      echo "  - 跳过云端环境变量校验"
      ;;
    cloud)
      echo "[信息] 执行模式: cloud（用户显式指定，直连火山 OpenAPI）"
      ;;
    apig)
      echo "[信息] 执行模式: apig（用户显式指定）"
      ;;
    *)
      echo "[信息] 执行模式: ${_explicit_mode}（用户显式指定）"
      ;;
  esac
else
  # ── 2. 无显式指定 → 自动检测 ──
  _det_ark_base="$(read_effective_value ARK_SKILL_API_BASE)"
  _det_ark_key="$(read_effective_value ARK_SKILL_API_KEY)"
  if [[ -n "$_det_ark_base" && -n "$_det_ark_key" ]]; then
    EXECUTION_MODE="apig"
    echo "[信息] 自动检测到 APIG 环境变量，使用 apig 模式"
  else
    # 无 APIG 凭据，暂不确定是 cloud 还是 local，留空后续校验
    EXECUTION_MODE=""
  fi
fi

# 导出 EXECUTION_MODE 使子进程（Python 脚本等）继承
if [[ -n "${EXECUTION_MODE}" ]]; then
  export EXECUTION_MODE
fi

# 记录模式是否由用户显式指定（影响缺变量时的行为：显式→exit，自动→有限降级）
IS_EXPLICIT_MODE=0
if [[ -n "$_explicit_mode" ]]; then
  IS_EXPLICIT_MODE=1
fi

if [[ ! -f "${ENV_FILE}" ]]; then
  if [[ -f "${ENV_TEMPLATE}" ]]; then
    cp "${ENV_TEMPLATE}" "${ENV_FILE}"
    echo "已根据模板创建 ${ENV_FILE}（来源：${ENV_TEMPLATE}）"
    if [[ "${IS_LOCAL_MODE}" -eq 0 ]]; then
      echo "请编辑 .env 并填入必需的环境变量后重新运行。"
    fi
  else
    if [[ "${IS_LOCAL_MODE}" -eq 0 ]]; then
      echo "ERROR: 未找到 ${ENV_FILE}，且模板 ${ENV_TEMPLATE} 不存在，无法自动创建。"
      exit 1
    else
      echo "[信息] local 模式无需 .env 文件"
    fi
  fi
fi


# ─── 辅助：将 KEY=VALUE 写入 .env（存在则替换，否则追加） ───
_write_env_var() {
  local key="$1" value="$2"
  if [[ -f "${ENV_FILE}" ]] && grep -Eq "^[[:space:]]*${key}[[:space:]]*=" "${ENV_FILE}"; then
    sed -i.bak "s|^[[:space:]]*${key}[[:space:]]*=.*|${key}=${value}|" "${ENV_FILE}"
    rm -f "${ENV_FILE}.bak"
  else
    if [[ -f "${ENV_FILE}" ]]; then
      echo "${key}=${value}" >> "${ENV_FILE}"
    else
      echo "${key}=${value}" > "${ENV_FILE}"
    fi
  fi
  export "${key}=${value}"
}

# ─── 非交互式：缺失变量报告 ───
# 策略（v1.0.9）:
#   显式指定 → 提示缺失变量 + exit 1（不降级，不改 .env）
#   自动检测 apig 缺补充变量 → 降级到 cloud；cloud 也缺 → 提示 + exit 1
#   cloud 缺变量 → 提示 + exit 1（不降到 local，local 只能显式选择）
_report_missing_vars() {
  local current_mode="$1"
  local is_explicit="$2"  # 1=用户显式指定, 0=自动检测
  shift 2
  local all_missing=("$@")

  echo
  echo "============================================================"
  echo "⚠️  当前 ${current_mode} 模式缺少以下环境变量:"
  echo "   ${all_missing[*]}"
  echo
  echo "请在以下位置补全后重新运行:"
  echo "  文件: ${ENV_FILE}"
  echo
  echo "缺失变量说明:"
  for k in "${all_missing[@]}"; do
    case "${k}" in
      ARK_SKILL_API_BASE) echo "  ${k}: SkillHub 网关 OpenAPI 根 URL（通常容器注入）" ;;
      ARK_SKILL_API_KEY) echo "  ${k}: SkillHub 网关 Bearer Token（通常容器注入）" ;;
      VOLC_ACCESS_KEY_ID) echo "  ${k}: 火山引擎 Access Key ID  →  https://console.volcengine.com/iam/keymanage" ;;
      VOLC_ACCESS_KEY_SECRET) echo "  ${k}: 火山引擎 Access Key Secret  →  同上" ;;
      VOLC_SPACE_NAME) echo "  ${k}: 火山引擎 VOD 点播空间名称  →  https://console.volcengine.com/vod" ;;
      ASR_API_KEY) echo "  ${k}: 豆包语音转写 API Key  →  https://console.volcengine.com/speech/new/experience/asr" ;;
      ASR_BASE_URL) echo "  ${k}: 豆包语音转写 Base URL（默认 https://openspeech.bytedance.com/api/v3/auc/bigmodel）" ;;
      *)                      echo "  ${k}" ;;
    esac
  done
  echo "============================================================"
  echo

  # ── 显式指定 → 不降级，直接退出 ──
  if [[ "${is_explicit}" -eq 1 ]]; then
    echo "[错误] 您显式指定了 ${current_mode} 模式，但所需环境变量不全。"
    echo "  请在 ${ENV_FILE} 中补全上述变量后重新运行。"
    exit 1
  fi

  # ── 自动检测 → 有限降级（到 cloud 为止，不降到 local） ──
  if [[ "${current_mode}" == "apig" ]]; then
    echo "[信息] apig 模式补充变量不全，尝试降级到 cloud 模式..."
    local _can_cloud=true
    local cloud_keys=("VOLC_ACCESS_KEY_ID" "VOLC_ACCESS_KEY_SECRET" "VOLC_SPACE_NAME" "ASR_API_KEY" "ASR_BASE_URL")
    for ck in "${cloud_keys[@]}"; do
      local cv
      cv="$(read_effective_value "$ck")"
      if [[ -z "$cv" ]]; then
        _can_cloud=false
        break
      fi
    done

    if [[ "$_can_cloud" == "true" ]]; then
      EXECUTION_MODE="cloud"
      _write_env_var "EXECUTION_MODE" "cloud"
      export EXECUTION_MODE
      echo "[信息] 已自动降级到 cloud 模式（火山 OpenAPI 直连）"
      echo "  → 已写入 EXECUTION_MODE=cloud 到 ${ENV_FILE}"
    else
      echo "[错误] apig 补充变量不全，cloud 变量也不全。"
      echo
      echo "您有两个选择:"
      echo "  ① 补全变量 → 在 ${ENV_FILE} 中填写所需项，然后重新运行"
      echo "  ② 切换到 local 模式（本地 ASR + ffmpeg，无需云端密钥）:"
      echo "      在 ${ENV_FILE} 中设置:  EXECUTION_MODE=local"
      echo "      或启动时指定:           --mode local"
      exit 1
    fi
  else
    # cloud 缺参 → 不降到 local，直接退出
    echo "[错误] cloud 模式所需环境变量不全。"
    echo
    echo "您有两个选择:"
    echo "  ① 补全变量 → 在 ${ENV_FILE} 中填写上述缺失项，然后重新运行"
    echo "  ② 切换到 local 模式（本地 ASR + ffmpeg，无需云端密钥）:"
    echo "      在 ${ENV_FILE} 中设置:  EXECUTION_MODE=local"
    echo "      或启动时指定:           --mode local"
    exit 1
  fi
  echo
}


# local 模式跳过云端环境变量校验
if [[ "${IS_LOCAL_MODE}" -eq 0 ]]; then

IS_APIG_TRANSPORT=0
ark_base="$(read_effective_value ARK_SKILL_API_BASE)"
ark_key="$(read_effective_value ARK_SKILL_API_KEY)"
_setup_mode="$(read_effective_value EXECUTION_MODE)"

if [[ "${_setup_mode}" == "cloud" ]]; then
  IS_APIG_TRANSPORT=0
  echo "[信息] VOD 接入：cloud（火山 OpenAPI，AK/SK 签算）"
  echo "  - 以下变量须在「进程环境或 ${ENV_FILE}」中非空："
  required_keys=(
    "VOLC_ACCESS_KEY_ID"
    "VOLC_ACCESS_KEY_SECRET"
    "VOLC_SPACE_NAME"
    "ASR_API_KEY"
    "ASR_BASE_URL"
  )
elif [[ -n "${ark_base}" && -n "${ark_key}" ]]; then
  IS_APIG_TRANSPORT=1
  echo "[信息] VOD 接入：APIG（SkillHub 网关）"
  echo "  - 已从进程环境或 .env 检测到 ARK_SKILL_API_BASE / ARK_SKILL_API_KEY（部署侧通常由容器注入，不必写入 .env）。"
  echo "  - 可不填 VOLC_ACCESS_KEY_ID / VOLC_ACCESS_KEY_SECRET。"
  echo "  - 以下变量须在「进程环境或 ${ENV_FILE}」中非空："
  echo "      VOLC_SPACE_NAME — 点播空间名称（用于 ListSpace / 上传 / 导出等 OpenAPI）"
  echo "      ASR_API_KEY       — 豆包语音转写"
  echo "      ASR_BASE_URL      — 转写服务 Base URL"
  required_keys=(
    "VOLC_SPACE_NAME"
    "ASR_API_KEY"
    "ASR_BASE_URL"
  )
else
  required_keys=(
    "VOLC_ACCESS_KEY_ID"
    "VOLC_ACCESS_KEY_SECRET"
    "VOLC_SPACE_NAME"
    "ASR_API_KEY"
    "ASR_BASE_URL"
  )
fi

all_problematic=()
for k in "${required_keys[@]}"; do
  value="$(read_effective_value "$k")"
  if [[ -z "${value}" ]]; then
    all_problematic+=("${k}")
  fi
done

if (( ${#all_problematic[@]} > 0 )); then
  if [[ "${IS_APIG_TRANSPORT}" -eq 1 ]]; then
    _report_missing_vars "apig" "${IS_EXPLICIT_MODE}" "${all_problematic[@]}"
  else
    _report_missing_vars "cloud" "${IS_EXPLICIT_MODE}" "${all_problematic[@]}"
  fi
fi

fi  # END: IS_LOCAL_MODE == 0

py_bin=""
if command -v python >/dev/null 2>&1; then
  py_bin="python"
elif command -v python3 >/dev/null 2>&1; then
  py_bin="python3"
else
  echo "ERROR: 未找到 python/python3，可执行文件不存在。"
  exit 1
fi

py_ver="$("${py_bin}" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')"
py_ok="$("${py_bin}" -c 'import sys; print(int((sys.version_info.major,sys.version_info.minor) >= (3,11)))')"

echo "Python: ${py_bin} (${py_ver})"
if [[ "${py_ok}" != "1" ]]; then
  echo "ERROR: Python 版本不满足要求：需要 >=3.11"
  echo "当前版本：${py_ver}"
  exit 1
fi

echo "[CHECKPOINT] 环境检查完成"

echo
echo "[2/2] 依赖安装"

if [[ ! -d "${SCRIPT_FOLDER}" ]]; then
  echo "ERROR: 未找到目录 ${SCRIPT_FOLDER}"
  exit 1
fi

cd "${SCRIPT_FOLDER}"

VENV_DIR=".venv"
MARKER_BASE="${VENV_DIR}/.deps_installed"
MARKER_LOCAL="${VENV_DIR}/.deps_local_installed"

_needs_install() {
  local marker="$1" req_file="$2"
  [[ ! -f "${marker}" ]] && return 0
  [[ ! -f "${req_file}" ]] && return 1
  if [[ "${req_file}" -nt "${marker}" ]]; then
    return 0
  fi
  return 1
}

if [[ -f "${VENV_DIR}/bin/activate" ]]; then
  echo "[信息] 已检测到 ${VENV_DIR}，复用现有虚拟环境"
  # shellcheck disable=SC1091
  source "${VENV_DIR}/bin/activate"
else
  echo "[信息] 创建虚拟环境 ${VENV_DIR} ..."
  "${py_bin}" -m venv "${VENV_DIR}"
  if [[ -f "${VENV_DIR}/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "${VENV_DIR}/bin/activate"
  else
    echo "ERROR: 未找到 ${VENV_DIR}/bin/activate，请检查 python -m venv 是否成功。"
    exit 1
  fi
fi

if _needs_install "${MARKER_BASE}" "requirements.txt"; then
  echo "[信息] 安装基础依赖 (requirements.txt) ..."
  python -m pip install --upgrade pip -q
  python -m pip install -r requirements.txt -q
  touch "${MARKER_BASE}"
  echo "[信息] 基础依赖安装完成"
else
  echo "[信息] 基础依赖已安装，跳过 (requirements.txt 未变更)"
fi

if [[ "${IS_LOCAL_MODE}" -eq 1 ]]; then
  if [[ -f "requirements-local.txt" ]]; then
    if _needs_install "${MARKER_LOCAL}" "requirements-local.txt"; then
      echo "[local] 安装本地模式额外依赖 (requirements-local.txt) ..."
      python -m pip install -r requirements-local.txt -q
      touch "${MARKER_LOCAL}"
      echo "[local] 本地依赖安装完成"
    else
      echo "[local] 本地依赖已安装，跳过 (requirements-local.txt 未变更)"
    fi
  fi
fi

echo "[CHECKPOINT] 依赖安装完成"
