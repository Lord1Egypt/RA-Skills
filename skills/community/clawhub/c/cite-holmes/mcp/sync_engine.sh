#!/bin/bash
# mcp 嵌入式引擎同步+一致性门禁（v6.0.0 模块化版：同步壳+全部 ch_* 层）
# 用法: bash mcp/sync_engine.sh   (在 skill 根目录执行)
# 发布链必跑:pkg/pyproject 分发只含 mcp/,引擎以副本形态进包——
# trunk scripts/ 的壳与 ch_* 层和 mcp/ 副本逐字节一致才许发。
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LAYERS="ch_text ch_netio ch_registry ch_semantic ch_verify ch_reports ch_cli"
FAIL=0
for f in verify_refs.py ch_text.py ch_netio.py ch_registry.py ch_semantic.py ch_verify.py ch_reports.py ch_cli.py; do
  SRC="$ROOT/scripts/$f"
  DST="$ROOT/mcp/$f"
  [ -f "$SRC" ] || { echo "[sync_engine] FAIL: 缺 $SRC"; FAIL=1; continue; }
  cp "$SRC" "$DST"
  A=$(sha256sum "$SRC" | cut -d' ' -f1)
  B=$(sha256sum "$DST" | cut -d' ' -f1)
  if [ "$A" != "$B" ]; then
    echo "[sync_engine] FAIL: $f sha 不一致($A vs $B)"; FAIL=1
  fi
done
[ "$FAIL" = 0 ] || exit 1
V1=$(grep -m1 '^VERSION' "$ROOT/scripts/ch_text.py" | sed 's/.*"\(.*\)".*/\1/')
V2=$(grep -m1 '^VERSION' "$ROOT/mcp/ch_text.py" | sed 's/.*"\(.*\)".*/\1/')
[ "$V1" = "$V2" ] || { echo "[sync_engine] FAIL: VERSION 不一致($V1 vs $V2)"; exit 1; }
# mcp 壳自检:动态加载在 mcp/ 目录下应解析 mcp_ 前缀（双壳隔离）
_PROBE_DIR=$(mktemp -d)
python3 - "$ROOT" "$_PROBE_DIR" <<'PYEOF'
import os, sys
root = sys.argv[1]
import tempfile as _t
_probe_dir = sys.argv[2] if len(sys.argv) > 2 else _t.mkdtemp()
sys.path.insert(0, os.path.join(root, "mcp"))
import verify_refs as vr
assert vr.VERSION, "mcp 副本 VERSION 缺失"
rc = vr.main_with_args(["--demo", "--offline", "--out", os.path.join(_probe_dir, "probe.md")])  # CLI 探针（审计 P1）；--out 指向 tmp 防 cwd 污染（目录由外层 shell 注入）
assert rc in (0, 1), f"mcp 副本 CLI 探针 rc={rc}"
mods = [n for n in ("ch_text", "ch_netio", "ch_registry") if hasattr(vr, n)]
assert len(mods) == 3, f"mcp 壳重导出缺层: {mods}"
print("[sync_engine] mcp 副本独立加载自检 PASS (VERSION %s)" % vr.VERSION)
PYEOF
# F54 wheel 清单门：pyproject include ⊇ mcp/ 全部 py 文件（防新模块漏打包）
python3 - "$ROOT" <<'PYEOF2'
import glob, os, sys, tomllib
root = sys.argv[1]
d = tomllib.load(open(os.path.join(root, "mcp", "pyproject.toml"), "rb"))
inc = set(d["tool"]["hatch"]["build"]["targets"]["wheel"]["include"])
actual = {os.path.basename(p) for p in glob.glob(os.path.join(root, "mcp", "*.py"))}
missing = actual - inc
assert not missing, f"pyproject wheel include 缺 {sorted(missing)}——uvx/pip 安装将崩（F54 教训）"
print("[sync_engine] wheel 清单门 PASS（include ⊇ %d 个 mcp py 文件）" % len(actual))
PYEOF2
echo "[sync_engine] PASS: 壳+7 层全部同步（8 文件逐字节一致, VERSION $V1）"
