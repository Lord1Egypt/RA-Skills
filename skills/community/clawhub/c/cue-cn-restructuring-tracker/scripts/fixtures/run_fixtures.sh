#!/usr/bin/env bash
# run_fixtures.sh — 本包离线自检（30 秒内跑完，零网络、零计费、零凭据）。
#
# 五档，逐档现报，不并成一个数：
#   ① check_tracker.py --selftest        五道判据的钉阈与反证（含临时根自清）
#   ② 好样 1 枚 + 坏样 5 枚逐枚单跑      每枚报自己的退码与实发码，不合并
#   ③ make_outline.py 排骨架             零通道降级：只排形状，不产内容
#   ④ 骨架过 check_tracker.py            必须红在占位行上（红是设计，不是故障）
#   ⑤ 边界五形                           跟踪口径写成单份／时间轴不足两行／节点不在册／
#                                        终止不在末行／变化行只挂一枚锚
#
# 退码：0 全过；1 有档不合；3 有档取值域故障（脚本或夹具不在场、骨架没写出来）——3 不并入 1。

set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG="$(cd "$HERE/../.." && pwd)"
FX="$HERE"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-restructuring-tracker.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

bad=0
unk=0

# 预检：缺件按取值域故障读，不当「零违例」
for f in "$PKG/scripts/check_tracker.py" "$PKG/scripts/make_outline.py" \
         "$FX/good-tracker.md" "$FX/bad-no-anchor.md" "$FX/bad-missing-section.md" \
         "$FX/bad-rating-word.md" "$FX/bad-gap-unlisted.md" "$FX/bad-single-doc.md" \
         "$FX/sources.jsonl"; do
  if [ ! -f "$f" ]; then
    echo "取值域故障：缺件 $f"
    unk=$((unk + 1))
  fi
done
if [ "$unk" -gt 0 ]; then
  echo "档数=0（预检未过）｜不合=0｜不可判=$unk"
  exit 3
fi

run_one() {   # run_one <文件> <期望退码> <期望码或 ->
  local f="$1" want="$2" code="$3" out rc
  out="$(python3 -B "$PKG/scripts/check_tracker.py" "$f" 2>&1)"
  rc=$?
  if [ "$rc" -ne "$want" ]; then
    echo "  不合 $(basename "$f")：期望退码 $want，实发 $rc"
    echo "$out" | sed 's/^/      /'
    bad=$((bad + 1))
    return
  fi
  if [ "$code" != "-" ] && ! printf '%s' "$out" | grep -q "$code"; then
    echo "  不合 $(basename "$f")：期望发码 $code，实发详行不含它"
    echo "$out" | sed 's/^/      /'
    bad=$((bad + 1))
    return
  fi
  echo "  ok   $(basename "$f")（退码 $rc${code:+·实发 $code}）"
}

echo "① check_tracker.py --selftest"
if python3 -B "$PKG/scripts/check_tracker.py" --selftest > "$WORK/selftest.log" 2>&1; then
  echo "  ok   selftest 全绿（$(grep -c '^  ok' "$WORK/selftest.log") 档）"
else
  echo "  不合 selftest"
  sed 's/^/      /' "$WORK/selftest.log"
  bad=$((bad + 1))
fi

echo "② 好样 1 枚 + 坏样 5 枚逐枚单跑"
run_one "$FX/good-tracker.md"        0 -
run_one "$FX/bad-no-anchor.md"       1 E-ANCHOR
run_one "$FX/bad-missing-section.md" 1 E-FORMAT
run_one "$FX/bad-rating-word.md"     1 E-BANWORD
run_one "$FX/bad-gap-unlisted.md"    1 E-COVERAGE
run_one "$FX/bad-single-doc.md"      1 E-SCOPE

echo "③ make_outline.py 排骨架（零通道降级）"
if python3 -B "$PKG/scripts/make_outline.py" "$FX/sources.jsonl" --out "$WORK/skeleton.md" > "$WORK/outline.log" 2>&1; then
  tl=$(grep -c '^- 20' "$WORK/skeleton.md" || true)
  echo "  ok   骨架已写出（时间轴 $tl 行）"
else
  echo "  不合 make_outline.py"
  sed 's/^/      /' "$WORK/outline.log"
  bad=$((bad + 1))
fi

echo "④ 骨架过 check_tracker.py（必须红在占位行上）"
if [ -f "$WORK/skeleton.md" ]; then
  out="$(python3 -B "$PKG/scripts/check_tracker.py" "$WORK/skeleton.md" 2>&1)"
  rc=$?
  if [ "$rc" -eq 1 ] && printf '%s' "$out" | grep -q '占位'; then
    echo "  ok   骨架按设计判红（退码 1·红在占位行）"
  else
    echo "  不合 骨架：期望退码 1 且红在占位行，实发 $rc"
    echo "$out" | sed 's/^/      /'
    bad=$((bad + 1))
  fi
else
  echo "  不可判 骨架没写出来，本档跳过"
  unk=$((unk + 1))
fi

echo "⑤ 边界五形"
edge() {   # edge <名> <python 改写表达式> <期望退码> <期望码>
  local name="$1" expr="$2" want="$3" code="$4" f="$WORK/edge.md" out rc
  python3 -B -c "
import pathlib
t = pathlib.Path('$FX/good-tracker.md').read_text(encoding='utf-8')
$expr
pathlib.Path('$f').write_text(t, encoding='utf-8')
" || { echo "  不可判 $name：改写脚本失败"; unk=$((unk + 1)); return; }
  out="$(python3 -B "$PKG/scripts/check_tracker.py" "$f" 2>&1)"
  rc=$?
  if [ "$rc" -ne "$want" ] || ! printf '%s' "$out" | grep -q "$code"; then
    echo "  不合 $name：期望退码 $want 且发 $code，实发 $rc"
    echo "$out" | sed 's/^/      /'
    bad=$((bad + 1))
    return
  fi
  echo "  ok   $name（退码 $rc·实发 $code）"
}

edge "跟踪口径写成单份" \
  "t = t.replace('跟踪口径：跨期（同一笔交易的多份公告按时间轴串起来，标进度节点与每步变化）', '跟踪口径：单份（只读一份重组报告书草案，做条款速读）')" \
  1 E-SCOPE
edge "时间轴只剩一行" \
  "import re
t = re.sub(r'^- 2025-11-10｜.*\n', '', t, flags=re.M)
t = re.sub(r'^- 2025-11-24｜.*\n', '', t, flags=re.M)
t = re.sub(r'^- 2026-01-15｜.*\n', '', t, flags=re.M)
t = re.sub(r'^- 2026-02-10｜.*\n', '', t, flags=re.M)
t = re.sub(r'^- 2026-02-27｜.*\n', '', t, flags=re.M)
t = re.sub(r'^- 2026-04-18｜.*\n', '', t, flags=re.M)
t = re.sub(r'^- 2026-05-22｜.*\n', '', t, flags=re.M)" \
  1 E-SCOPE
edge "节点不在册" \
  "t = t.replace('- 2026-04-18｜过会｜并购重组委审核通过 [S6]', '- 2026-04-18｜上会｜并购重组委审核通过 [S6]')" \
  1 E-FORMAT
edge "终止不在末行" \
  "t = t.replace('- 2026-07-03｜实施｜标的资产完成过户，新增股份尚未上市 [S8]', '- 2026-07-03｜终止｜交易终止 [S8]\n- 2026-08-01｜实施｜标的资产完成过户 [S8]')" \
  1 E-FORMAT
edge "变化行只挂一枚锚" \
  "t = t.replace('- 交易对价：8.6 亿元 → 9.2 亿元（草案相对预案上调 0.6 亿元） [S2][S3]', '- 交易对价：8.6 亿元 → 9.2 亿元（草案相对预案上调 0.6 亿元） [S3]')" \
  1 E-ANCHOR

echo "档数=5（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then
  echo "有档取值域故障，整趟按 3 读，不并入「不合」。"
  exit 3
fi
if [ "$bad" -gt 0 ]; then
  exit 1
fi
exit 0
