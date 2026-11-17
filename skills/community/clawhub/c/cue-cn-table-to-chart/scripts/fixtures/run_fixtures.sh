#!/usr/bin/env bash
# 离线样例 runner：30 秒内走完「机检自测 → 逐枚单跑 → 采集器出骨架且该红就红」三档。
# 用法：bash scripts/fixtures/run_fixtures.sh  （零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp}，跑完即删）
# 退码：0 三档全合期望；1 有不合（逐枚点名并附真实退码与真实码集）；3 取值域故障（脚本或夹具取不到，不读成「零违例」）。
# 档②除码集外另打「段」列＝该枚发条落在被检的哪一节——先证靶落在判据扫的那一段里，再谈「不判别」。
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-table-to-chart.XXXXXX")"
if [ -z "$WORK" ] || [ ! -d "$WORK" ]; then echo "3 取值域故障：临时目录没建成（TMPDIR=$TMPDIR 是否存在、可写？），不带空路径往下跑"; exit 3; fi
trap 'rm -rf "$WORK"' EXIT

bad=0
unk=0
for f in "$ROOT/scripts/check_chart.py" "$ROOT/scripts/collect_chart.py" "$FIX/good-chart.md" "$FIX/target-table.md" "$FIX/target-table-noted.md" "$FIX/target-table-merged.md"; do
  if [ ! -f "$f" ]; then echo "3 取值域故障：取不到 $f（不读成「夹具全过」）"; exit 3; fi
done
TBL="scripts/fixtures/target-table.md"

echo "档① 机检自测（好样须过、每枚坏样须各发它该发的那一道——枚数由脚本 CASES 自报，逐枚带原文比对）"
out=$(cd "$ROOT" && python3 -B scripts/check_chart.py --selftest 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | tail -1)"; echo "  实发退码=$rc｜期望=0"
if [ "$rc" -ne 0 ]; then echo "  → 不合"; bad=$((bad + 1)); else echo "  → 合"; fi

echo "档② 逐枚单跑（每枚只发它该发的那一道，且靶要落在那一道的判据段里；另跑一支不给表原文的，验「不可判」那条形制）"
pairfile="$WORK/pairs.txt"
cat > "$pairfile" <<'PAIRS'
good-chart.md|PASS||
good-quoted-note.md|PASS||target-table-noted.md
good-plain-quote.md|PASS||target-table-noted.md
good-third-party.md|PASS||target-table-noted.md
good-merged-order.md|PASS||target-table-merged.md
bad-spec.md|E-FORMAT|规格待核|
bad-no-anchor.md|E-ANCHOR|锚|
bad-invented-number.md|E-QUOTE|逐字回表（全篇）|
bad-unbound-quote.md|E-QUOTE|逐字回表（全篇）|
bad-cell-misplaced.md|E-QUOTE|格位·整行照序或配列头|
bad-no-header-pair.md|E-QUOTE|格位·数没配列头|
bad-cell-empty-zero.md|E-QUOTE|格位·列头配对不成立|
bad-merged-bind.md|E-QUOTE|格位·列头配对不成立|target-table-merged.md
bad-conclusion-crossline.md|E-ADVICE|投资断言|target-table-noted.md
bad-author-voice-verb.md|E-ADVICE|投资断言|target-table-noted.md
bad-quote-conclusion.md|E-ADVICE|投资断言|target-table-noted.md
bad-quote-source-only.md|E-ADVICE|投资断言|target-table-noted.md
bad-quote-third-party.md|E-ADVICE|投资断言|target-table-noted.md
bad-quote-bare.md|E-ADVICE|投资断言|target-table-noted.md
bad-missing-limit.md|E-COVERAGE|四类点名|
bad-advice.md|E-ADVICE|投资断言|
bad-bare-outcome.md|E-ADVICE|投资断言|
bad-superlative.md|E-ADVICE|结论式名次|
PAIRS
n=0
while IFS='|' read -r fx want wantseg fxTbl; do
  [ -n "$fx" ] || continue
  n=$((n + 1))
  if [ ! -f "$FIX/$fx" ]; then echo "  $fx｜→ 不可判：夹具不在场（不填 0）"; unk=$((unk + 1)); continue; fi
  tbl="$TBL"; [ -n "$fxTbl" ] && tbl="scripts/fixtures/$fxTbl"
  if [ -n "$fxTbl" ] && [ ! -f "$FIX/$fxTbl" ]; then echo "  $fx｜→ 不可判：这一枚要的表原文不在场 $fxTbl（不填 0）"; unk=$((unk + 1)); continue; fi
  out=$(cd "$ROOT" && python3 -B scripts/check_chart.py "scripts/fixtures/$fx" --table "$tbl" 2>&1); rc=$?
  detail=$(printf '%s\n' "$out" | grep '^\s*\[E-')
  codes=$(printf '%s\n' "$detail" | grep -o 'E-[A-Z]*' | sort -u | tr '\n' ',' | sed 's/,$//')
  hits=$(printf '%s\n' "$detail" | grep -c '^\s*\[E-')
  segs=$(printf '%s\n' "$detail" | sed -n 's/^\s*\[E-[A-Z]*\] \[\([^]]*\)\].*/\1/p' | sort -u | paste -sd '/' -)
  rows=$(printf '%s\n' "$detail" | grep -oE '第 [0-9]+ 行' | head -1)
  if [ "$want" = "PASS" ]; then
    echo "  $fx｜期望退码 0／实发 $rc｜期望码集=空／实发 ${codes:-空}｜表=${fxTbl:-默认合成表}"
    if [ "$rc" -eq 0 ] && [ -z "$codes" ]; then echo "    → 合（注入生效=不适用）"; else echo "    → 不合"; bad=$((bad + 1)); fi
  else
    echo "  $fx｜期望退码 1／实发 $rc｜期望只发 $want｜实发码 $codes｜发条 $hits 条｜靶位=$rows｜判据段=${segs:-无}｜表=${fxTbl:-默认合成表}"
    if [ "$rc" -eq 1 ] && [ "$codes" = "$want" ] && [ "$hits" -ge 1 ] && [[ "$segs" == *"$wantseg"* ]]; then
      echo "    → 合（注入生效=是：这一道确实发了条，且靶落在它扫的那一段里）"
    else
      echo "    → 不合（注入生效=$([ "$hits" -ge 1 ] && echo 是 || echo 否)；期望段名=${wantseg:-无}／实发段=${segs:-无}）"; bad=$((bad + 1))
    fi
  fi
done < "$pairfile"
echo "  逐枚枚数=$n（由上面逐行现数）｜不合=$bad"
out=$(cd "$ROOT" && python3 -B scripts/check_chart.py scripts/fixtures/good-chart.md 2>&1); rc=$?
det=$(printf '%s\n' "$out" | grep -c '\[不可判\]')
self=$(printf '%s\n' "$out" | grep -o '不可判 [0-9]* 项' | tail -1)
echo "  好样不给表原文这一支｜期望退码 0、明细行>0、末行自报「不可判 N 项」／实发退码 $rc、明细 $det 条、自报=${self:-未自报}"
if [ "$rc" -eq 0 ] && [ "$det" -gt 0 ] && [ -n "$self" ]; then
  echo "    → 合（没表就明写不可判，不并入通过、也不当违例）"
else
  echo "    → 不合（这一形变了就复读 check_chart 的道三出口与末行自报，别沿用本断言）"; bad=$((bad + 1))
fi

echo "档③ 采集器出骨架，骨架过机检——期望红在两道：第一节四件规格仍是待核位＋第三节四类限度仍是待核位"
out=$(cd "$ROOT" && python3 -B scripts/collect_chart.py --source "$TBL" --out "$WORK/skeleton.md" 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | head -1)"; echo "  实发退码=$rc｜期望=0"
if [ "$rc" -ne 0 ]; then
  if [ "$rc" -eq 3 ]; then echo "  → 不可判：采集器走到取值域出口（见上一行原文）"; unk=$((unk + 1));
  else echo "  → 不合：期望退码 0，实发 $rc"; bad=$((bad + 1)); fi
fi
if [ -f "$WORK/skeleton.md" ]; then
  out=$(cd "$ROOT" && python3 -B scripts/check_chart.py "$WORK/skeleton.md" --table "$TBL" 2>&1); rc=$?
  codes=$(printf '%s\n' "$out" | grep -o 'E-[A-Z]*' | sort -u | tr '\n' ',' | sed 's/,$//')
  hit=$(printf '%s\n' "$out" | grep -c '仍是待核位')
  kh=$(printf '%s\n' "$out" | grep -c '这一类仍是待核位')
  echo "  实发退码=$rc｜期望=1｜码集=$codes（期望 E-COVERAGE、E-FORMAT 两道齐发：四件规格没选、四类限度也没判）｜规格待核红命中=$hit｜限度待核红命中=$kh｜骨架行数=$(grep -c '^- ' "$WORK/skeleton.md")"
  if [ "$rc" -eq 1 ] && [ "$codes" = "E-COVERAGE,E-FORMAT" ] && [ "$hit" -ge 1 ] && [ "$kh" -ge 1 ]; then
    echo "    → 合（图型没人选、限度没判就红在这里，骨架不该被当成产物交付；两道齐发是实现加了道一判据后期望跟着走）"
  else
    echo "    → 不合：期望的红不再在场（退码 $rc／码集 $codes／命中 $hit）——这一形变了就复读 collect_chart 的待核句与 check_chart 的道一判据，别沿用本断言"
    bad=$((bad + 1))
  fi
else
  echo "  → 不可判：档③没出骨架，这一档无从跑"; unk=$((unk + 1))
fi

echo "----"
echo "档数=3（由上面逐档现报）｜合期望=$((3 - bad - unk))｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo "有档取值域故障，整趟按 3 读，不并入「不合」。"; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
