#!/usr/bin/env bash
# fw-trade-skill 组合技能一键安装（Mac/Linux）
#
# 模拟盘、实盘、fosun-env-setup 共用本脚本与同一份 venv（默认落在 skill 根目录 .venv）。
# 符合 Agent Skills 约定：依赖与脚本相对 skill 根目录管理，避免写入 Agent 工作区外路径。
#
# 设计思路（不假设用户机器已装 Python）：
#   1. 检测 uv；没有则从官方安装到 ~/.local/bin
#   2. 在 $FW_TRADE_VENV（默认 $SKILL_ROOT/.venv）创建环境，Python 由 uv 自动下载
#   3. 下载 fsopenapi SDK 源码并 editable 安装（含 setup.py 声明的 PyPI 依赖）
#   4. 自检 import fsopenapi
#
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_FOSUN_ENV_PATH="${SKILL_ROOT}/fosun.env"
FOSUN_ENV_PATH="${FOSUN_ENV_PATH:-${DEFAULT_FOSUN_ENV_PATH}}"
export FOSUN_ENV_PATH

VENV_DIR="${FW_TRADE_VENV:-${FOSUN_VENV:-${MONI_VENV:-${SKILL_ROOT}/.venv}}}"
PIN_PYTHON_VERSION="${FW_TRADE_PYTHON_VERSION:-${MONI_PYTHON_VERSION:-3.13}}"
SDK_VERSION="${FW_TRADE_SDK_VERSION:-${MONI_SDK_VERSION:-v1.2.0}}"
SDK_ZIP_URL_PRIMARY="${FW_TRADE_SDK_URL:-${MONI_SDK_URL:-https://hk.gh-proxy.org/https://github.com/fosunwealth/openapi-python-sdk/archive/refs/tags/v1.2.0.zip}}"
SDK_ZIP_URL="${SDK_ZIP_URL_PRIMARY}"
SDK_CACHE_ROOT="${FW_TRADE_CACHE_DIR:-${MONI_CACHE_DIR:-${SKILL_ROOT}/.cache}}"
SDK_CACHE_DIR="${SDK_CACHE_ROOT}/openapi-python-sdk-${SDK_VERSION}"
PYPI_MIRROR="${FW_TRADE_PYPI_MIRROR:-${MONI_PYPI_MIRROR:-https://pypi.tuna.tsinghua.edu.cn/simple}}"

log() { printf "\033[1;36m[fw-trade]\033[0m %s\n" "$*"; }
err() { printf "\033[1;31m[fw-trade ERROR]\033[0m %s\n" "$*" >&2; }

resolve_sdk_fallback_url() {
  if [ -n "${FW_TRADE_SDK_FALLBACK_URL:-${MONI_SDK_FALLBACK_URL:-}}" ]; then
    printf '%s\n' "${FW_TRADE_SDK_FALLBACK_URL:-${MONI_SDK_FALLBACK_URL}}"
    return 0
  fi
  local ensure_py="${SKILL_ROOT}/fosun-env-setup/code/ensure_fosun_env.py"
  if [ -f "${ensure_py}" ]; then
    grep -E '^DEFAULT_SDK_ZIP_FALLBACK_URL[[:space:]]*=' "${ensure_py}" \
      | sed -n 's/.*"\([^"]*\)".*/\1/p' \
      | head -1
  fi
}

# ---- 1. 确保 uv 可用 -------------------------------------------------------
ensure_uv() {
  export PATH="${HOME}/.local/bin:${HOME}/.cargo/bin:${PATH}"
  if command -v uv >/dev/null 2>&1; then
    log "检测到 uv：$(command -v uv)"
    return 0
  fi
  log "未检测到 uv，自动从官方源安装（一次性，安装到 ~/.local/bin）..."
  if command -v curl >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- https://astral.sh/uv/install.sh | sh
  else
    err "未找到 curl 或 wget，无法自动安装 uv。请手动安装：https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
  fi
  export PATH="${HOME}/.local/bin:${HOME}/.cargo/bin:${PATH}"
  if ! command -v uv >/dev/null 2>&1; then
    err "uv 自动安装失败，请手动安装后重试。"
    exit 1
  fi
  log "uv 安装完成：$(command -v uv)"
}

ensure_uv

SDK_ZIP_URL_FALLBACK="$(resolve_sdk_fallback_url || true)"

# ---- 2. 创建或复用共享 venv ------------------------------------------------
VENV_PY="${VENV_DIR}/bin/python"

if [ ! -x "${VENV_PY}" ]; then
  log "创建共享环境（uv 会按需下载 Python ${PIN_PYTHON_VERSION}）：${VENV_DIR}"
  mkdir -p "$(dirname "${VENV_DIR}")"
  uv venv --python "${PIN_PYTHON_VERSION}" "${VENV_DIR}"
else
  log "复用已有共享环境：${VENV_DIR}"
fi

if [ ! -x "${VENV_PY}" ]; then
  err "共享环境创建失败，未找到解释器：${VENV_PY}"
  exit 1
fi

# ---- 3. 下载并解压 SDK 源码 -------------------------------------------------
TMP_BUILD_DIR="$(mktemp -d "${TMPDIR:-/tmp}/fw-trade-build.XXXXXX")"
trap 'rm -rf "${TMP_BUILD_DIR}"' EXIT
SDK_ZIP_PATH="${TMP_BUILD_DIR}/openapi-python-sdk.zip"
SDK_EXTRACT_DIR="${TMP_BUILD_DIR}/src"

download_sdk_zip() {
  local url="$1"
  if command -v curl >/dev/null 2>&1; then
    curl -fL --connect-timeout 30 --max-time 600 "${url}" -o "${SDK_ZIP_PATH}"
    return 0
  fi
  if command -v wget >/dev/null 2>&1; then
    wget -O "${SDK_ZIP_PATH}" "${url}"
    return 0
  fi
  err "未找到 curl 或 wget，无法下载 SDK 压缩包：${url}"
  exit 1
}

log "下载官方 SDK 源码（主源）：${SDK_ZIP_URL_PRIMARY}"
if download_sdk_zip "${SDK_ZIP_URL_PRIMARY}"; then
  SDK_ZIP_URL="${SDK_ZIP_URL_PRIMARY}"
elif [ -n "${SDK_ZIP_URL_FALLBACK}" ] && [ "${SDK_ZIP_URL_FALLBACK}" != "${SDK_ZIP_URL_PRIMARY}" ]; then
  log "主源下载失败，尝试备用源：${SDK_ZIP_URL_FALLBACK}"
  if download_sdk_zip "${SDK_ZIP_URL_FALLBACK}"; then
    SDK_ZIP_URL="${SDK_ZIP_URL_FALLBACK}"
  else
    err "主源与备用源都下载失败。可设置 FW_TRADE_SDK_URL / FW_TRADE_SDK_FALLBACK_URL 后重试。"
    exit 1
  fi
else
  err "主源下载失败，且未解析到可用备用源。可设置 FW_TRADE_SDK_URL / FW_TRADE_SDK_FALLBACK_URL 后重试。"
  exit 1
fi

log "解压 SDK 源码包"
SDK_EXTRACTED_DIR="$("${VENV_PY}" - "${SDK_ZIP_PATH}" "${SDK_EXTRACT_DIR}" <<'PY'
import sys
import zipfile
from pathlib import Path

zip_path = Path(sys.argv[1])
extract_root = Path(sys.argv[2])
extract_root.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(zip_path, "r") as zf:
    zf.extractall(extract_root)

root_dirs = [p for p in extract_root.iterdir() if p.is_dir()]
if len(root_dirs) == 1:
    candidate = root_dirs[0]
else:
    candidates = []
    for marker in ("setup.py", "pyproject.toml"):
        for file in extract_root.rglob(marker):
            candidates.append(file.parent)
    if not candidates:
        raise SystemExit("无法在解压目录中找到 setup.py / pyproject.toml")
    candidate = sorted(candidates, key=lambda p: len(str(p)))[0]

print(candidate.resolve())
PY
)"
mkdir -p "${SDK_CACHE_ROOT}"
rm -rf "${SDK_CACHE_DIR}"
cp -R "${SDK_EXTRACTED_DIR}" "${SDK_CACHE_DIR}"
SDK_SRC_DIR="${SDK_CACHE_DIR}"
log "SDK 持久缓存目录：${SDK_SRC_DIR}"

if [ ! -f "${SDK_SRC_DIR}/setup.py" ] && [ ! -f "${SDK_SRC_DIR}/pyproject.toml" ]; then
  err "SDK 目录异常，未找到 setup.py / pyproject.toml：${SDK_SRC_DIR}"
  exit 1
fi

# ---- 4. 可编辑安装 SDK 到共享环境 -------------------------------------------
log "安装 fsopenapi SDK（editable 模式，默认 PyPI 官方源）"
if ! uv pip install --python "${VENV_PY}" --reinstall --editable "${SDK_SRC_DIR}"; then
  log "默认 PyPI 源不可用，改用清华大学 PyPI 镜像重试：${PYPI_MIRROR}"
  uv pip install --python "${VENV_PY}" --reinstall --editable \
    --default-index "${PYPI_MIRROR}" \
    "${SDK_SRC_DIR}"
fi

# ---- 5. 开通页二维码依赖 ---------------------------------------------------
log "安装开通页二维码依赖（qrcode + Pillow）"
if ! uv pip install --python "${VENV_PY}" "qrcode[pil]>=7.4"; then
  log "默认 PyPI 源不可用，改用清华大学 PyPI 镜像重试：${PYPI_MIRROR}"
  uv pip install --python "${VENV_PY}" \
    --default-index "${PYPI_MIRROR}" \
    "qrcode[pil]>=7.4"
fi

# ---- 6. 自检 ---------------------------------------------------------------
log "自检 import fsopenapi"
"${VENV_PY}" -c "import fsopenapi; print('  fsopenapi @', fsopenapi.__file__)"
log "自检 import qrcode / PIL"
"${VENV_PY}" -c "import qrcode; from PIL import Image; print('  qrcode + Pillow OK')"

cat <<EOF

✅ 安装完成（模拟盘 / 实盘 / env-setup 共用）。

🐍 Python 解释器：${VENV_PY}（锁定 ${PIN_PYTHON_VERSION}）
📁 Skill 根目录：${SKILL_ROOT}
📦 虚拟环境：${VENV_DIR}
🔐 共享凭证路径：${FOSUN_ENV_PATH}
📦 SDK 来源：${SDK_ZIP_URL}
📂 SDK 缓存：${SDK_SRC_DIR}

——— 起手式（每个新会话 export 一次）———
  export FOSUN_SKILL_ROOT="${SKILL_ROOT}"
  export FOSUN_PY="${VENV_PY}"
  export FOSUN_ENV_PATH="${FOSUN_ENV_PATH}"
  # 兼容旧速抄表变量名
  export MONI_PY="\${FOSUN_PY}"
  export REAL_PY="\${FOSUN_PY}"

——— 共享凭证（优先于业务脚本）———
  \$FOSUN_PY \$FOSUN_SKILL_ROOT/fosun-env-setup/code/ensure_fosun_env.py

——— 模拟盘示例（\$SKILL=moni-trade-skill 绝对路径）———
  export SKILL="\${FOSUN_SKILL_ROOT}/moni-trade-skill"
  \$FOSUN_PY \$SKILL/code/check_shared_env.py

——— 实盘示例（\$SKILL=real-trade-skill 绝对路径）———
  export SKILL="\${FOSUN_SKILL_ROOT}/real-trade-skill"
  \$FOSUN_PY \$SKILL/code/check_shared_env.py

完整说明见各子 skill 的 SKILL.md。

EOF
