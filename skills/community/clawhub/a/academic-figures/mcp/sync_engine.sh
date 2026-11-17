#!/bin/bash
# mcp 引擎镜像同步+一致性门禁（v4.0.0 模块化形态：多文件+期刊预设+changelog）
# 用法: bash mcp/sync_engine.sh   (在 skill 根目录执行)
# 发布链必跑: mcp/ 分发只含 af_engine/ 嵌入副本——trunk scripts/ 与副本
# 逐字节一致才许发（防错配：两副本 sha 漂移=用户拿到旧引擎）。
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/scripts"
DST="$ROOT/mcp/af_engine"
mkdir -p "$DST/journal"

FILES="gen_figure.py af_draw.py af_shared.py af_v23_stats.py af_v23_charts.py af_wizard.py af_diagnostics.py af_resilience.py detect_cjk_font.py check_consistency.py banned_af.txt"
for f in $FILES; do
  cp "$SRC/$f" "$DST/$f"
done
cp "$SRC"/journal/*.json "$DST/journal/"
cp "$ROOT/references/changelog.md" "$DST/changelog.md"
touch "$DST/__init__.py"

FAIL=0
check() { # check <源路径> <副本路径> <名称>
  A=$(sha256sum "$1" | cut -d' ' -f1)
  B=$(sha256sum "$2" | cut -d' ' -f1)
  if [ "$A" != "$B" ]; then echo "[sync_engine] FAIL: $3 sha 不一致"; FAIL=1; fi
}
for f in $FILES; do
  check "$SRC/$f" "$DST/$f" "$f"
done
for j in "$DST"/journal/*.json; do
  b=$(basename "$j")
  check "$SRC/journal/$b" "$DST/journal/$b" "journal/$b"
done
check "$ROOT/references/changelog.md" "$DST/changelog.md" "changelog.md"
for f in "$DST"/*.py; do
  b=$(basename "$f")
  [ "$b" = "__init__.py" ] && continue
  case " $FILES " in *" $b "*) ;; *) echo "[sync_engine] FAIL: 清单外文件 $b"; FAIL=1;; esac
done
[ "$FAIL" = 0 ] && echo "[sync_engine] PASS: 引擎镜像一致（$FILES + journal/*.json + changelog.md）" || exit 1
