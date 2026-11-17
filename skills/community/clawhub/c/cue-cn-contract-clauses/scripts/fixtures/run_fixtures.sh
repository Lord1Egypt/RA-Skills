#!/usr/bin/env bash
# 离线样例 runner：30 秒内走完「机检自测 → 逐枚单跑 → 采集器出骨架且该红就红」三档。
# 用法：bash scripts/fixtures/run_fixtures.sh  （零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp}，跑完即删）
# 退码：0 三档全合期望；1 有不合（逐枚点名并附真实退码与真实码集）；3 取值域故障（脚本或夹具取不到，不读成「零违例」）。
# 三档的期望都挂在两条分支都被读的断言上；坏样逐枚单跑、各发该发那道，不并成一个总数；每支注入自报生效与否。
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-contract-clauses.XXXXXX")"
if [ -z "$WORK" ] || [ ! -d "$WORK" ]; then echo "3 取值域故障：临时目录没建成（TMPDIR=$TMPDIR 是否存在、可写？），不带空路径往下跑"; exit 3; fi
trap 'rm -rf "$WORK"' EXIT

bad=0
unk=0
for f in "$ROOT/scripts/check_clauses.py" "$ROOT/scripts/collect_clauses.py" "$FIX/good-clauses.md" "$FIX/target-contract.md"; do
  if [ ! -f "$f" ]; then echo "3 取值域故障：取不到 $f（不读成「夹具全过」）"; exit 3; fi
done
SRC="scripts/fixtures/target-contract.md"

echo "档① 机检自测（好样须过、七枚坏样须各发它该发的那一道，两侧比对带原文）"
out=$(cd "$ROOT" && python3 -B scripts/check_clauses.py --selftest 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | tail -1)"; echo "  实发退码=$rc｜期望=0"
if [ "$rc" -ne 0 ]; then echo "  → 不合"; bad=$((bad + 1)); else echo "  → 合"; fi

echo "档② 逐枚单跑（每枚只发它该发的那一道；好样另跑一支不给原文的，验「不可判」那条形制）"
pairfile="$WORK/pairs.txt"
cat > "$pairfile" <<'PAIRS'
good-clauses.md|PASS
bad-format.md|E-FORMAT
bad-no-anchor.md|E-ANCHOR
bad-invented-quote.md|E-QUOTE
bad-missing-type.md|E-COVERAGE
bad-legal-verdict.md|E-LAW
bad-outcome-bare.md|E-LAW
bad-outcome-split.md|E-LAW
PAIRS
n=0
while IFS='|' read -r fx want; do
  [ -n "$fx" ] || continue
  n=$((n + 1))
  if [ ! -f "$FIX/$fx" ]; then echo "  $fx｜→ 不可判：夹具不在场（不填 0）"; unk=$((unk + 1)); continue; fi
  out=$(cd "$ROOT" && python3 -B scripts/check_clauses.py "scripts/fixtures/$fx" --source "$SRC" 2>&1); rc=$?
  codes=$(printf '%s\n' "$out" | grep -o 'E-[A-Z]*' | sort -u | tr '\n' ',' | sed 's/,$//')
  hits=$(printf '%s\n' "$out" | grep -c '^\s*\[E-')
  if [ "$want" = "PASS" ]; then
    echo "  $fx｜期望退码 0／实发 $rc｜期望码集=空／实发 ${codes:-空}"
    if [ "$rc" -eq 0 ] && [ -z "$codes" ]; then echo "    → 合（注入生效=不适用）"; else echo "    → 不合"; bad=$((bad + 1)); fi
  else
    echo "  $fx｜期望退码 1／实发 $rc｜期望只发 $want｜实发码 $codes｜发条 $hits 条"
    if [ "$rc" -eq 1 ] && [ "$codes" = "$want" ] && [ "$hits" -ge 1 ]; then
      echo "    → 合（注入生效=是：这一道确实发了条）"
    else
      echo "    → 不合（注入生效=$([ "$hits" -ge 1 ] && echo 是 || echo 否)）"; bad=$((bad + 1))
    fi
  fi
done < "$pairfile"
echo "  逐枚枚数=$n（由上面逐行现数）｜不合=$bad"
out=$(cd "$ROOT" && python3 -B scripts/check_clauses.py scripts/fixtures/good-clauses.md 2>&1); rc=$?
det=$(printf '%s\n' "$out" | grep -c '\[不可判\]')
self=$(printf '%s\n' "$out" | grep -o '不可判 [0-9]* 项' | tail -1)
echo "  好样不给原文这一支｜期望退码 0、明细行>0、末行自报「不可判 N 项」／实发退码 $rc、明细 $det 条、自报=${self:-未自报}"
if [ "$rc" -eq 0 ] && [ "$det" -gt 0 ] && [ -n "$self" ]; then
  echo "    → 合（没原文就明写不可判，不并入通过、也不当违例）"
else
  echo "    → 不合（这一形变了就复读 check_clauses 的道三出口与末行自报，别沿用本断言）"; bad=$((bad + 1))
fi

echo "档③ 采集器出骨架，骨架过机检——期望红在七类需盯条款的待核位"
out=$(cd "$ROOT" && python3 -B scripts/collect_clauses.py --source "$SRC" --out "$WORK/skeleton.md" 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | head -1)"; echo "  实发退码=$rc｜期望=0"
if [ "$rc" -ne 0 ]; then
  if [ "$rc" -eq 3 ]; then echo "  → 不可判：采集器走到取值域出口（见上一行原文）"; unk=$((unk + 1));
  else echo "  → 不合：期望退码 0，实发 $rc"; bad=$((bad + 1)); fi
fi
if [ -f "$WORK/skeleton.md" ]; then
  out=$(cd "$ROOT" && python3 -B scripts/check_clauses.py "$WORK/skeleton.md" --source "$SRC" 2>&1); rc=$?
  codes=$(printf '%s\n' "$out" | grep -o 'E-[A-Z]*' | sort -u | tr '\n' ',' | sed 's/,$//')
  hit=$(printf '%s\n' "$out" | grep -c '仍是待核位')
  echo "  实发退码=$rc｜期望=1｜码集=$codes（期望只 E-COVERAGE）｜待核红命中=$hit｜骨架要点行=$(grep -c '^- 「' "$WORK/skeleton.md")"
  if [ "$rc" -eq 1 ] && [ "$codes" = "E-COVERAGE" ] && [ "$hit" -ge 1 ]; then
    echo "    → 合（哪一类要盯还没判就红在这里，骨架不该被当成清单交付）"
  else
    echo "    → 不合：期望的红不再在场（退码 $rc／码集 $codes／命中 $hit）——这一形变了就复读 collect_clauses 的待核句与 check_clauses 的道四判据，别沿用本断言"
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
