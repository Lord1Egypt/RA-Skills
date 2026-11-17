#!/usr/bin/env bash
# 通用入口：run_cad.sh <cad_scan|read_cad|cad_interpret|...> [参数...]
# 输出选项（通用，所有脚本生效）：
#   --concise        精简输出（省 Token）：候选只保留主干字段
#   --full           完整输出（含 evidence/bbox 等全部字段，默认）
#   --with-evidence  同 --full
# 默认输出完整；环境变量 CAD_CONCISE=1 可全局改为精简默认。
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ==== 运行时自举：缺依赖自动补齐（可设 CAD_AUTO_SETUP=0 关闭） ====
if [ -f "$SKILL_DIR/scripts/ensure_runtime.sh" ]; then
  bash "$SKILL_DIR/scripts/ensure_runtime.sh" --quiet || exit $?
fi
PYTHON_BIN=""
for candidate in \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"
do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then
    PYTHON_BIN="${candidate}"
    break
  fi
done
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "Python 3 not found; cannot run CAD reader." >&2
  exit 1
fi
# 内存闸（2026-08-31）：macOS 无 RLIMIT_AS/ulimit -v，硬保护在 mem_guard.py 看门狗。
: "${CAD_MEM_LIMIT_MB:=4096}"
export CAD_MEM_LIMIT_MB
# 输出深度：默认完整；--concise 显式精简；--full/--with-evidence 显式完整。
: "${CAD_CONCISE:=0}"
forward_args=()
argc=0
for _arg in "$@"; do
  case "${_arg}" in
    --concise) export CAD_CONCISE=1 ;;
    --full|--with-evidence) export CAD_CONCISE=0 ;;
    *) forward_args+=("${_arg}"); argc=$((argc + 1)) ;;
  esac
done
export CAD_CONCISE
export PYTHONPATH="${SKILL_DIR}/vendor${PYTHONPATH:+:${PYTHONPATH}}"
# bash 3.2（macOS 自带）在 set -u 下对空数组取 ${#arr[@]} 会报 unbound variable，
# 改用标量 argc 计数，保证无参数时打印用法而不是中断。
if [ "$argc" -eq 0 ]; then
  echo "用法: run_cad.sh <cad_scan|read_cad|cad_interpret|...> [参数...] [--concise|--full|--with-evidence]" >&2
  exit 1
fi
SCRIPT_NAME="${forward_args[0]}"
unset 'forward_args[0]'
exec "${PYTHON_BIN}" "${SKILL_DIR}/scripts/${SCRIPT_NAME}.py" "${forward_args[@]}"
