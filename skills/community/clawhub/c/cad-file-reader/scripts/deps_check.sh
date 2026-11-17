#!/usr/bin/env bash
# 依赖/能力自检：一条命令看到哪些功能可用、哪些因缺依赖变复核。
# 用法：scripts/deps_check.sh [--minimal]
set -uo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MINIMAL="${1:-}"

PYTHON_BIN=""
for candidate in \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"; do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then PYTHON_BIN="${candidate}"; break; fi
done
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "❌ python3 缺失（需要 Python 3.10+）"; exit 1
fi
echo "python: $($PYTHON_BIN -V 2>&1)"

check() { # name expected_dir marker file
  local name="$1" dir="$2" marker="$3"
  if [ -d "$dir" ] && [ -e "$marker" ]; then echo "ok   $name"; else echo "缺   $name"; fi
}
check "vendor/ezdwg"  "$SKILL_DIR/vendor/ezdwg"  "$SKILL_DIR/vendor/ezdxf/__init__.py"
check "vendor/ezdxf"  "$SKILL_DIR/vendor/ezdxf"  "$SKILL_DIR/vendor/ezdxf/__init__.py"
check "vendor/fontTools" "$SKILL_DIR/vendor/fontTools" "$SKILL_DIR/vendor/fontTools/__init__.py"
check "vendor/typing_extensions" "$SKILL_DIR/vendor" "$SKILL_DIR/vendor/typing_extensions.py"
imported=$("$PYTHON_BIN" -c "import importlib.util as u; print('1' if u.find_spec('numpy') else '0')" 2>/dev/null || echo "0")
if [ "$imported" = 1 ]; then
  echo "numpy: ok"
else
  echo "numpy: 缺"
fi
if [ "$imported" != 1 ]; then echo "  （缺 numpy 只影响梁线几何估算；DWG/DXF 文字/图层/测量仍可用）"; fi
te_imported=$("$PYTHON_BIN" -c "import importlib.util as u; print('1' if u.find_spec('typing_extensions') else '0')" 2>/dev/null || echo "0")
if [ "$te_imported" = 1 ]; then
  echo "typing_extensions: ok"
else
  echo "typing_extensions: 缺（ezdxf 硬依赖，缺了 DXF 解析整条路会失败）"
fi

if [ "$MINIMAL" = "--minimal" ]; then
  echo "deps: $([ -d "$SKILL_DIR/vendor/ezdxf" ] && [ "$imported" = 1 ] && [ "$te_imported" = 1 ] && echo full || echo partial)  -> 缺依赖功能会降级为 review"
fi
