#!/usr/bin/env bash
# 离线样例 runner：30 秒内在临时目录里走完「机检自测 → 逐枚单跑（含不给原文那支）」三档。
# 用法：bash scripts/fixtures/run_fixtures.sh   （零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp}，跑完即删）
# 退码：0 三档全合期望；1 有不合（逐枚点名并附那次真实退码与真实码集）；3 取值域故障（脚本或夹具取不到，不读成「零违例」）。
# 三档各自的期望都挂在两条分支都被读的断言上（通与不通读同一个数）；坏样逐枚单跑、各发该发那道，不并成一个总数。
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-link-to-note.XXXXXX")"
if [ -z "$WORK" ] || [ ! -d "$WORK" ]; then echo "3 取值域故障：临时目录没建成（TMPDIR=$TMPDIR 是否存在、可写？），不带空路径往下跑"; exit 3; fi
trap 'rm -rf "$WORK"' EXIT

bad=0
unk=0
for f in "$ROOT/scripts/check_note.py" "$ROOT/scripts/make_note.py" "$FIX/good-note.md" "$FIX/source-article.md"; do
  if [ ! -f "$f" ]; then echo "3 取值域故障：取不到 $f（不读成「夹具全过」）"; exit 3; fi
done

echo "档① 机检自测（好样须过、四枚坏样须各发它该发的那一道，道三带原文真跑）"
out=$(cd "$ROOT" && python3 -B scripts/check_note.py --selftest 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | tail -1)"; echo "  实发退码=$rc｜期望=0"
if [ "$rc" -ne 0 ]; then echo "  → 不合"; bad=$((bad + 1)); else echo "  → 合"; fi

echo "档② 逐枚单跑（每枚只发它该发的那一道；好样另跑一支不给原文的，验「不可判」那条形制）"
pairfile="$WORK/pairs.txt"
cat > "$pairfile" <<'PAIRS'
good-note.md|PASS
bad-format.md|E-FORMAT
bad-no-anchor.md|E-ANCHOR
bad-quote.md|E-QUOTE
bad-unnamed-gap.md|E-COVERAGE
PAIRS
n=0
while IFS='|' read -r fx want; do
  [ -n "$fx" ] || continue
  n=$((n + 1))
  if [ ! -f "$FIX/$fx" ]; then echo "  $fx｜→ 不可判：夹具不在场（不填 0）"; unk=$((unk + 1)); continue; fi
  out=$(cd "$ROOT" && python3 -B scripts/check_note.py "scripts/fixtures/$fx" --source scripts/fixtures/source-article.md 2>&1); rc=$?
  codes=$(printf '%s\n' "$out" | grep -o 'E-[A-Z]*' | sort -u | tr '\n' ',' | sed 's/,$//')
  if [ "$want" = "PASS" ]; then
    echo "  $fx｜期望退码 0／实发 $rc｜期望码集=空／实发 ${codes:-空}"
    if [ "$rc" -eq 0 ] && [ -z "$codes" ]; then echo "    → 合"; else echo "    → 不合"; bad=$((bad + 1)); fi
  else
    echo "  $fx｜期望退码 1／实发 $rc｜期望只发 $want／实发码 $codes"
    if [ "$rc" -eq 1 ] && [ "$codes" = "$want" ]; then echo "    → 合"; else echo "    → 不合"; bad=$((bad + 1)); fi
  fi
done < "$pairfile"
echo "  逐枚枚数=$n（由上面逐行现数）｜不合=$bad"
out=$(cd "$ROOT" && python3 -B scripts/check_note.py scripts/fixtures/good-note.md 2>&1); rc=$?
det=$(printf '%s\n' "$out" | grep -c '\[不可判\]')
self=$(printf '%s\n' "$out" | grep -o '不可判 [0-9]* 项' | head -1)
echo "  好样不给原文这一支｜期望退码 0、明细行 1 条、末行自报「不可判 1 项」／实发退码 $rc、明细 $det 条、自报=${self:-未自报}"
if [ "$rc" -eq 0 ] && [ "$det" -eq 1 ] && [ "$self" = "不可判 1 项" ]; then echo "    → 合（不可判不并入通过，也不当违例）"; else echo "    → 不合（这一形变了就复读 check_note 的道三出口与末行自报，别沿用本断言）"; bad=$((bad + 1)); fi

echo "档③ 生成器出骨架，骨架过机检——期望红在「要点没挂锚」那三条"
out=$(cd "$ROOT" && python3 -B scripts/make_note.py --source scripts/fixtures/source-article.md --url https://example.org/article --out "$WORK/skeleton.md" 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | head -1)"; echo "  实发退码=$rc｜期望=0"
if [ "$rc" -ne 0 ]; then
  if [ "$rc" -eq 3 ]; then echo "  → 不可判：生成器走到取值域出口（见上一行原文）"; unk=$((unk + 1));
  else echo "  → 不合：期望退码 0，实发 $rc"; bad=$((bad + 1)); fi
fi
if [ -f "$WORK/skeleton.md" ]; then
  out=$(cd "$ROOT" && python3 -B scripts/check_note.py "$WORK/skeleton.md" --source scripts/fixtures/source-article.md 2>&1); rc=$?
  codes=$(printf '%s\n' "$out" | grep -o 'E-[A-Z]*' | sort -u | tr '\n' ',' | sed 's/,$//')
  hit=$(printf '%s\n' "$out" | grep -c '要点行行末没有')
  echo "  实发退码=$rc｜期望=1｜码集=$codes（期望 E-ANCHOR）｜「要点没挂锚」命中=$hit（期望 3）｜引用行由件内逐字摘出=$(grep -c '^> 「' "$WORK/skeleton.md")"
  if [ "$rc" -eq 1 ] && [ "$codes" = "E-ANCHOR" ] && [ "$hit" -eq 3 ]; then
    echo "    → 合（没挂锚的发现不进笔记，红在这三条是设计：骨架不是交付）"
  else
    echo "    → 不合：期望的红不再在场（退码 $rc／码集 $codes／命中 $hit）——这一形变了就复读 make_note 的待填句与 check_note 的锚判据，别沿用本断言"
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
