#!/usr/bin/env bash
# 离线样例 runner（M588）：三档走完「机检自测 → 好样／坏样逐枚单跑 → 边界形逐枚单跑」。
# 用法：bash scripts/fixtures/run_fixtures.sh
# 零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp}，跑完即删。
# 退码：0 三档全合期望；1 有不合（逐枚点名，附真实退码与真实码集）；3 取值域故障（脚本或夹具取不到，不读成「零违例」）。
# 三档的期望都挂在「两侧都被读」的断言上：坏样逐枚单跑、各发该发那道，不并成一个总数；每支注入自报生效与否。
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_rpt_card.py"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/related-party-terms-cn.XXXXXX")"
if [ -z "$WORK" ] || [ ! -d "$WORK" ]; then
  echo "3 取值域故障：临时目录没建成（TMPDIR=${TMPDIR:-未设} 是否存在、可写？），不带空路径往下跑"; exit 3
fi
trap 'rm -rf "$WORK"' EXIT

bad=0
unk=0
for f in "$CK" "$FIX/good-rpt-card.md" "$FIX/bad-rpt-card.md"; do
  if [ ! -f "$f" ]; then echo "3 取值域故障：取不到 $f（不读成「夹具全过」）"; exit 3; fi
done

echo "档① 机检自测（好样须过、坏样须发五道码，两侧比对带原文）"
out=$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1); rc=$?
printf '%s\n' "$out" | tail -1
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ]; then echo "  → 合"; else echo "  → 不合"; bad=$((bad + 1)); fi

echo "档② 好样／坏样逐枚单跑（好样 rc=0 零发条；坏样 rc=1 且五道码齐）"
out=$(cd "$ROOT" && python3 -B "$CK" "$FIX/good-rpt-card.md" 2>&1); rc=$?
hits=$(printf '%s\n' "$out" | grep -c '^FAIL')
echo "  good-rpt-card.md｜期望退码 0／实发 $rc｜期望发条 0／实发 $hits"
if [ "$rc" -eq 0 ] && [ "$hits" -eq 0 ]; then echo "    → 合"; else echo "    → 不合"; bad=$((bad + 1)); fi

out=$(cd "$ROOT" && python3 -B "$CK" "$FIX/bad-rpt-card.md" 2>&1); rc=$?
codes=$(printf '%s\n' "$out" | grep -o '\[RP-[A-Z]*\]' | sort -u | tr '\n' ',' | sed 's/,$//')
hits=$(printf '%s\n' "$out" | grep -c '^FAIL')
want="[RP-COUNT],[RP-LINE],[RP-QUOTE],[RP-STRUCT],[RP-VALUE]"
echo "  bad-rpt-card.md｜期望退码 1／实发 $rc｜期望码集=$want｜实发码 ${codes:-空}｜发条 $hits 条"
if [ "$rc" -eq 1 ] && [ "$codes" = "$want" ] && [ "$hits" -ge 5 ]; then
  echo "    → 合（五道码齐，注入生效=是）"
else
  echo "    → 不合（注入生效=$([ "$hits" -ge 5 ] && echo 是 || echo 否)）"; bad=$((bad + 1))
fi

echo "档③ 边界形逐枚单跑（自称按前邻词性认：表内虚词前邻必红、复合词尾巴必绿、已知覆盖不到照绿）"
# 每行：标签|插入行|期望退码
cat > "$WORK/cases.txt" <<'CASES'
表内·据本件判断|- 公告原文：「据本件判断，本次关联交易定价公允」 锚：公告 第二节|1
表内·经本件判断|- 公告原文：「经本件判断本次交易定价公允」 锚：公告 第二节|1
表内·由本件判断|- 公告原文：「由本件判断本次交易定价公允」 锚：公告 第二节|1
表内·按本件结论|- 公告原文：「按本件结论，本次交易定价公允」 锚：公告 第二节|1
表内·对本件而言|- 公告原文：「对本件而言，本次关联交易定价公允」 锚：公告 第二节|1
表内·以本件为准|- 公告原文：「以本件为准，本次交易定价公允」 锚：公告 第二节|1
复合词·样本件|- 公告原文：「本次交易标的为样本件，交易价格按市场公允价格确定」 锚：公告 第三节|0
复合词·基本件|- 公告原文：「基本件采购价格按市场公允价格确定」 锚：公告 第三节|0
复合词·成本件|- 公告原文：「成本件与标准件的定价依据均为市场公允价格」 锚：公告 第三节|0
复合词·副本件|- 公告原文：「副本件与正本具有同等效力」 锚：公告 第三节|0
已知覆盖不到·通过本件判断|- 公告原文：「通过本件判断本次交易定价公允」 锚：公告 第二节|0
已知覆盖不到·围绕本件|- 公告原文：「围绕本件判断本次交易定价公允」 锚：公告 第二节|0
已知覆盖不到·仍本件认为|- 公告原文：「仍本件认为本次交易定价公允」 锚：公告 第二节|0
CASES
n=0
while IFS='|' read -r tag line want; do
  [ -n "$tag" ] || continue
  n=$((n + 1))
  card="$WORK/case.md"
  # 把这一行插到好样卡的「## 三、口径对照」之前，落临时件
  python3 -B - "$FIX/good-rpt-card.md" "$card" "$line" <<'PY'
import sys
from pathlib import Path
src, dst, line = sys.argv[1], sys.argv[2], sys.argv[3]
t = Path(src).read_text(encoding='utf-8')
HEAD = '## 三、口径对照'
if HEAD not in t:
    sys.exit('good 卡里找不到插入点')
Path(dst).write_text(t.replace(HEAD, line + '\n\n' + HEAD, 1), encoding='utf-8')
PY
  if [ $? -ne 0 ]; then echo "  $tag｜→ 不可判：临时件没建成"; unk=$((unk + 1)); continue; fi
  out=$(cd "$ROOT" && python3 -B "$CK" "$card" 2>&1); rc=$?
  codes=$(printf '%s\n' "$out" | grep -o '\[RP-[A-Z]*\]' | sort -u | tr '\n' ',' | sed 's/,$//')
  if [ "$rc" -eq "$want" ]; then
    echo "  $tag｜期望退码 $want／实发 $rc｜码 ${codes:-空} → 合"
  else
    echo "  $tag｜期望退码 $want／实发 $rc｜码 ${codes:-空} → 不合"; bad=$((bad + 1))
  fi
done < "$WORK/cases.txt"
echo "  逐枚枚数=$n（由上面逐行现数）"

echo "----"
echo "档数=3（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo "有档取值域故障，整趟按 3 读，不并入「不合」。"; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
