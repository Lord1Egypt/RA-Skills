#!/usr/bin/env bash
# 商誉减值风险台账·离线样例 runner（零网络、零计费、不碰真披露）
#
#   bash scripts/fixtures/run_fixtures.sh
#
# 三档：
#   档一 selftest  —— 机检自检：好样必过、坏样六枚各发其码
#   档二 好样直跑  —— 好样单独喂给 check_goodwill.py，必须 rc=0
#   档三 坏样逐枚  —— 每枚坏样退出码必须是 1（有发红），且必须点到它自己那道
#
# 退码：0＝三档全过；1＝有档未过；3＝取值域故障（好样缺失／脚本缺失）
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
CHECK="$ROOT/scripts/check_goodwill.py"
GOOD="$HERE/good-goodwill-ledger.md"

fail=0
say() { printf '%s\n' "$*"; }

[ -f "$CHECK" ] || { say "取值域故障：机检脚本不在 $CHECK"; exit 3; }
[ -f "$GOOD" ]  || { say "取值域故障：好样不在 $GOOD"; exit 3; }

say "=============================================="
say "档一：自检（好样必过｜坏样六枚各发其码）"
say "=============================================="
PYTHONDONTWRITEBYTECODE=1 python3 -B "$CHECK" --selftest
rc1=$?
if [ "$rc1" -eq 0 ]; then say "档一 rc=0 过"; else say "档一 rc=$rc1 未过"; fail=1; fi

say ""
say "=============================================="
say "档二：好样直跑（期望 rc=0，发红数必须为 0）"
say "=============================================="
out="$(PYTHONDONTWRITEBYTECODE=1 python3 -B "$CHECK" "$GOOD")"
rc2=$?
say "$out"
red="$(printf '%s\n' "$out" | sed -n 's/.*发红 \([0-9]\+\).*/\1/p' | tail -1)"
if [ "$rc2" -eq 0 ] && [ "${red:-x}" = "0" ]; then
  say "档二 rc=0 过（发红 0）"
else
  say "档二 未过：rc=$rc2 发红=${red:-未自报}"
  fail=1
fi

say ""
say "=============================================="
say "档三：坏样逐枚（期望 rc=1 且点到本枚那道）"
say "=============================================="
# 坏样 → 期望码
expect() {
  case "$(basename "$1")" in
    bad-1-struct.md)     echo "GW-STRUCT" ;;
    bad-2-quote.md)      echo "GW-QUOTE" ;;
    bad-3-line.md)       echo "GW-LINE" ;;
    bad-4-gap-count.md)  echo "GW-GAP" ;;
    bad-5-self-calc.md)  echo "GW-GAP" ;;
    bad-6-bound.md)      echo "GW-BOUND" ;;
    *)                   echo "" ;;
  esac
}
n=0; ok=0
for f in "$HERE"/bad-*.md; do
  [ -f "$f" ] || continue
  n=$((n+1))
  want="$(expect "$f")"
  o="$(PYTHONDONTWRITEBYTECODE=1 python3 -B "$CHECK" "$f")"
  r=$?
  if [ "$r" -eq 1 ] && printf '%s' "$o" | grep -q "$want"; then
    say "ok   $(basename "$f") rc=1 发 $want"
    ok=$((ok+1))
  else
    say "FAIL $(basename "$f") rc=$r 期望 rc=1 且发 $want"
    printf '%s\n' "$o" | sed 's/^/       /'
    fail=1
  fi
done
say "档三：$ok/$n 过"

say ""
say "=============================================="
if [ "$fail" -eq 0 ]; then
  say "三档全过：好样不发红｜坏样 $n 枚各发其码｜零网络"
  exit 0
fi
say "有档未过（见上）"
exit 1
