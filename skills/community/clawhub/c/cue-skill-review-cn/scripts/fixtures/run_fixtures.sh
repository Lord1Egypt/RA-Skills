#!/usr/bin/env bash
# 离线样例 runner：30 秒内在临时目录里走完「机检自测 → 逐枚坏样单跑 → 采集器出骨架且该红就红」三档。
# 用法：bash scripts/fixtures/run_fixtures.sh   （零网络、零计费、零执行靶件代码、纯标准库；产物只落 ${TMPDIR:-/tmp}，跑完即删）
# 退码：0 三档全合期望；1 有不合（逐档点名并附那次真实退码与真实末行）；3 取值域故障（脚本或夹具取不到，不读成「零违例」）。
# 三档各自的期望都挂在两条分支都被读的断言上（通与不通读同一个数），不是只在失败分支里写死的死数。
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/skill-review-cn.XXXXXX")"
if [ -z "$WORK" ] || [ ! -d "$WORK" ]; then echo "3 取值域故障：临时目录没建成（TMPDIR=$TMPDIR 是否存在、可写？），不带空路径往下跑"; exit 3; fi
trap 'rm -rf "$WORK"' EXIT

bad=0
unk=0
for f in "$ROOT/scripts/check_review.py" "$ROOT/scripts/collect_review.py" "$FIX/good-review.md" "$FIX/target-demo/SKILL.md"; do
  if [ ! -f "$f" ]; then echo "3 取值域故障：取不到 $f（不读成「夹具全过」）"; exit 3; fi
done

echo "档① 机检自测（好样须过、五枚坏样须各发它该发的那一道）"
out=$(cd "$ROOT" && python3 -B scripts/check_review.py --selftest 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | tail -1)"; echo "  实发退码=$rc｜期望=0"
if [ "$rc" -ne 0 ]; then echo "  → 不合"; bad=$((bad + 1)); else echo "  → 合"; fi

echo "档② 逐枚坏样单跑（每枚只发它该发的那一道，所以逐枚报、不并成一个总数）"
pairfile="$WORK/pairs.txt"
cat > "$pairfile" <<'PAIRS'
bad-format.md|E-FORMAT
bad-no-anchor.md|E-ANCHOR
bad-unverified-claim.md|E-VERIFY
bad-safety-verdict.md|E-BANWORD
bad-missing-face.md|E-COVERAGE
PAIRS
n=0
while IFS='|' read -r fx want; do
  [ -n "$fx" ] || continue
  n=$((n + 1))
  if [ ! -f "$FIX/$fx" ]; then echo "  $fx｜→ 不可判：夹具不在场（不填 0）"; unk=$((unk + 1)); continue; fi
  out=$(cd "$ROOT" && python3 -B scripts/check_review.py "scripts/fixtures/$fx" 2>&1); rc=$?
  codes=$(printf '%s\n' "$out" | grep -o 'E-[A-Z]*' | sort -u | tr '\n' ',' | sed 's/,$//')
  echo "  $fx｜期望退码 1／实发 $rc｜期望只发 $want／实发码 $codes"
  if [ "$rc" -eq 1 ] && [ "$codes" = "$want" ]; then echo "    → 合"; else echo "    → 不合"; bad=$((bad + 1)); fi
done < "$pairfile"
echo "  逐枚枚数=$n（由上面逐行现数）｜不合=$bad"

echo "档③ 采集器出骨架，骨架过机检——期望红在「样例真跑」那一行"
out=$(cd "$ROOT" && python3 -B scripts/collect_review.py --target scripts/fixtures/target-demo --out "$WORK/skeleton.md" 2>&1); rc=$?
echo "$(printf '%s\n' "$out" | head -1)"; echo "  实发退码=$rc｜期望=0"
if [ "$rc" -ne 0 ]; then
  if [ "$rc" -eq 3 ]; then echo "  → 不可判：采集器走到取值域出口（见上一行原文）"; unk=$((unk + 1));
  else echo "  → 不合：期望退码 0，实发 $rc"; bad=$((bad + 1)); fi
fi
if [ -f "$WORK/skeleton.md" ]; then
  out=$(cd "$ROOT" && python3 -B scripts/check_review.py "$WORK/skeleton.md" 2>&1); rc=$?
  hit=$(printf '%s\n' "$out" | grep -c '写了真跑通却没附那条命令')
  echo "  实发退码=$rc｜期望=1｜「样例真跑待填」命中=$hit｜末行=$(printf '%s\n' "$out" | head -1)"
  if [ "$rc" -eq 1 ] && [ "$hit" -ge 1 ]; then
    echo "  → 合（没跑就不算跑过，红在这一行是设计：骨架不是交付）"
  else
    echo "  → 不合：期望的红不再在场（退码 $rc／命中 $hit）——这一形变了就复读 collect_review 的待填句与 check_review 的 RUNWORD 判据，别沿用本断言"
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
