#!/usr/bin/env bash
# cad-file-reader Linux 跨平台安装器（Debian/Ubuntu 优先，fedora/dnf 等价备注）。
# 用途：
#   1) 若缺系统依赖（python3-pip/libredwg/poppler-utils/tesseract-ocr/libreoffice），
#      用 apt 安装（需要 sudo/root；SKIP_APT=1 可跳过）。
#   2) 再调用 scripts/setup.py 安装/校验 package vendor。
# 零副作用默认：--dry-run 只打印检测与软件包清单，不做任何安装。
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DRY_RUN=0
SKIP_APT="${SKIP_APT:-0}"
ARGS=()
for a in "$@"; do
  case "${a}" in
    --dry-run) DRY_RUN=1 ;;
    *) ARGS+=("${a}") ;;
  esac
done

echo "== cad-file-reader Linux 安装器 =="
echo "平台      : $(uname -s) $(uname -m)"
echo "Python    : $(command -v python3 || echo '（未找到，需 Python 3.10+）')"

APT_PACKAGES=(python3-pip libredwg poppler-utils tesseract-ocr libreoffice)
echo "系统包(apt): ${APT_PACKAGES[*]}   # fedora/dnf 可用等价包：python3-pip libredwg poppler-utils tesseract libreoffice"

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "模式      : --dry-run（只打印，不执行安装）"
  PYTHON_BIN="$(command -v python3 || true)"
  if [[ -n "${PYTHON_BIN}" ]]; then "${PYTHON_BIN}" "${SKILL_DIR}/scripts/setup.py" --dry-run ${ARGS[@]+"${ARGS[@]}"}; fi
  exit 0
fi

if [[ "${SKIP_APT}" != "0" ]]; then
  echo "SKIP_APT=${SKIP_APT} → 跳过系统包安装"
elif command -v apt-get >/dev/null 2>&1; then
  echo "== 安装系统包（可能要求 sudo）=="
  sudo apt-get update -y
  sudo apt-get install -y "${APT_PACKAGES[@]}"
elif command -v dnf >/dev/null 2>&1; then
  echo "== dnf 发行版等价包 =="
  sudo dnf install -y python3-pip libredwg poppler-utils tesseract libreoffice
elif command -v yum >/dev/null 2>&1; then
  sudo yum install -y python3-pip libredwg poppler-utils tesseract libreoffice
else
  echo "⚠️ 未识别包管理器，跳过系统包安装；请按发行版文档安装后再继续。"
fi

PYTHON_BIN=""
for candidate in \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"; do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then PYTHON_BIN="${candidate}"; break; fi
done
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "❌ 未找到 python3，需要 Python 3.10+" >&2
  exit 1
fi

exec "${PYTHON_BIN}" "${SKILL_DIR}/scripts/setup.py" ${ARGS[@]+"${ARGS[@]}"}
