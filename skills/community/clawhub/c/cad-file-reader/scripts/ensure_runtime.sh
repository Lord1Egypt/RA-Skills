#!/usr/bin/env bash
# 运行时自举（幂等，缺依赖自动补齐）：
#   1) 先检查 vendor（ezdwg/ezdxf/fontTools）是否齐全
#   2) 齐全 -> 直接退出，不联网、不重复下载
#   3) 缺失 -> 默认自动调用 install_vendor.sh 从 GitHub Release 补齐（需联网）
#              设置 CAD_AUTO_SETUP=0 可关闭自动下载，进入明确报错
# 用法：scripts/ensure_runtime.sh [--quiet]
set -uo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# SkillHub 分发包（zip）会丢失可执行位：首次运行时幂等自愈，避免 permission denied
find "$SKILL_DIR/scripts" -maxdepth 1 -type f \( -name '*.sh' -o -name '*.py' \) ! -perm -u+x -exec chmod +x {} + 2>/dev/null || true
QUIET=0
if [ "${1:-}" = "--quiet" ]; then QUIET=1; fi

say() { [ "$QUIET" = 0 ] && echo "$*"; }

PYTHON_BIN=""
for candidate in \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"; do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then PYTHON_BIN="${candidate}"; break; fi
done
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "❌ 未找到 python3（需要 Python 3.10+），请先安装 Python 或设置 CODEX_PYTHON。" >&2
  exit 1
fi

_unpacked_ok() {
  [ -d "$SKILL_DIR/vendor/ezdwg" ] && \
  [ -d "$SKILL_DIR/vendor/ezdxf" ] && \
  [ -f "$SKILL_DIR/vendor/ezdxf/__init__.py" ] && \
  [ -d "$SKILL_DIR/vendor/fontTools" ]
}

if _unpacked_ok; then
  say "runtime: vendor 已存在，跳过（不联网）"
  exit 0
fi

# 跨 Agent 复用：本技能没有 vendor 时，先看其它 Agent 安装的同款技能是否已有 vendor。
# 命中则软链到本目录 vendor（幂等），避免重复下载 40MB+ 依赖。
_reuse_candidates() {
  [ -n "${CAD_SKILL_VENDOR:-}" ] && echo "$CAD_SKILL_VENDOR"
  for _d in "$SKILL_DIR"/../cad-file-reader/vendor \
            "$HOME"/.workbuddy/skills/*/cad-file-reader/vendor \
            "$HOME/.claude/skills/cad-file-reader/vendor" \
            "$HOME/.codex/skills/cad-file-reader/vendor"; do
    [ -d "$_d" ] && echo "$_d"
  done
}

if [ ! -e "$SKILL_DIR/vendor" ]; then
  while IFS= read -r _cand; do
    [ -d "$_cand/ezdxf" ] && [ -d "$_cand/fontTools" ] || continue
    if ln -sfn "$_cand" "$SKILL_DIR/vendor" 2>/dev/null; then
      say "runtime: 复用已有 vendor（不联网）：$_cand"
      exit 0
    fi
  done < <(_reuse_candidates)
fi

if [ "${CAD_AUTO_SETUP:-1}" != "1" ]; then
  echo "❌ cad-file-reader 缺少 vendor（ezdwg/ezdxf/fontTools）。" >&2
  echo "   已设 CAD_AUTO_SETUP=0 关闭自动下载。请手动运行：" >&2
  echo "   $SKILL_DIR/scripts/setup.sh" >&2
  echo "   或在联网环境运行：$SKILL_DIR/scripts/install_vendor.sh" >&2
  exit 3
fi

say "runtime: 检测到缺少 vendor，正在自动补齐（首次运行，需联网）……"
bash "$SKILL_DIR/scripts/install_vendor.sh" --quiet || rc=$?
rc=${rc:-0}
if [ "$rc" -ne 0 ]; then
  echo "❌ runtime: 自动补齐 vendor 失败（可重试或离线使用 setup.sh）。" >&2
  exit 3
fi

if _unpacked_ok; then
  say "runtime: vendor 已自动补齐 ✓"
  exit 0
fi
echo "❌ runtime: vendor 补齐后校验仍未通过，请手动运行 setup.sh 检查。" >&2
exit 3
