#!/usr/bin/env bash
# 离线样例 runner：三档走完「机检自测 → 好样／坏样逐枚单跑 → 边界形逐枚单跑」。
# 用法：bash scripts/fixtures/run_fixtures.sh
# 零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp}，跑完即删。
# 退码：0 三档全合期望；1 有不合（逐枚点名，附真实退码与真实码集）；3 取值域故障（脚本或夹具取不到，不读成「零违例」）。
# 三档的期望都挂在「两侧都被读」的断言上：坏样逐枚单跑、各发该发那道，不并成一个总数；每支注入自报生效与否。
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_esop_card.py"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/employee-stock-ownership-cn.XXXXXX")"
if [ -z "$WORK" ] || [ ! -d "$WORK" ]; then
  echo "3 取值域故障：临时目录没建成（TMPDIR=${TMPDIR:-未设} 是否存在、可写？），不带空路径往下跑"; exit 3
fi
trap 'rm -rf "$WORK"' EXIT

bad=0
unk=0
for f in "$CK" "$FIX/good-esop-card.md" "$FIX/bad-esop-card.md"; do
  if [ ! -f "$f" ]; then echo "3 取值域故障：取不到 $f（不读成「夹具全过」）"; exit 3; fi
done

echo "档① 机检自测（好样须过、坏样须发五道码，两侧比对带原文）"
out=$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1); rc=$?
printf '%s\n' "$out" | tail -1
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ]; then echo "  → 合"; else echo "  → 不合"; bad=$((bad + 1)); fi

echo "档② 好样／坏样逐枚单跑（好样 rc=0 零发条；坏样 rc=1 且五道码齐）"
out=$(cd "$ROOT" && python3 -B "$CK" "$FIX/good-esop-card.md" 2>&1); rc=$?
hits=$(printf '%s\n' "$out" | grep -c '^FAIL')
echo "  good-esop-card.md｜期望退码 0／实发 $rc｜期望发条 0／实发 $hits"
if [ "$rc" -eq 0 ] && [ "$hits" -eq 0 ]; then echo "    → 合"; else echo "    → 不合"; bad=$((bad + 1)); fi

out=$(cd "$ROOT" && python3 -B "$CK" "$FIX/bad-esop-card.md" 2>&1); rc=$?
codes=$(printf '%s\n' "$out" | grep -o '\[ES-[A-Z]*\]' | sort -u | tr '\n' ',' | sed 's/,$//')
hits=$(printf '%s\n' "$out" | grep -c '^FAIL')
want="[ES-COUNT],[ES-LINE],[ES-QUOTE],[ES-STRUCT],[ES-VALUE]"
echo "  bad-esop-card.md｜期望退码 1／实发 $rc｜期望码集=$want｜实发码 ${codes:-空}｜发条 $hits 条"
if [ "$rc" -eq 1 ] && [ "$codes" = "$want" ] && [ "$hits" -ge 5 ]; then
  echo "    → 合（五道码齐，注入生效=是）"
else
  echo "    → 不合（注入生效=$([ "$hits" -ge 5 ] && echo 是 || echo 否)）"; bad=$((bad + 1))
fi

echo "档③ 边界形逐枚单跑（自称按前邻词性认：表内虚词前邻必红、复合词尾巴必绿、已知覆盖不到照绿；名目别名必绿）"
# 每行：标签|插入行|期望退码
cat > "$WORK/cases.txt" <<'CASES'
表内·据本件判断|- 草案原文：「据本件判断，本次受让价格公允」 锚：草案 第四章|1
表内·经本件判断|- 草案原文：「经本件判断本次受让价格公允」 锚：草案 第四章|1
表内·由本件判断|- 草案原文：「由本件判断本次受让价格公允」 锚：草案 第四章|1
表内·按本件结论|- 草案原文：「按本件结论，本次受让价格公允」 锚：草案 第四章|1
表内·对本件而言|- 草案原文：「对本件而言，本次受让价格公允」 锚：草案 第四章|1
表内·以本件为准|- 草案原文：「以本件为准，本次受让价格公允」 锚：草案 第四章|1
复合词·样本件|- 草案原文：「本次受让标的为样本件，受让价格按市场公允价格确定」 锚：草案 第四章|0
复合词·基本件|- 草案原文：「基本件受让价格按市场公允价格确定」 锚：草案 第四章|0
复合词·成本件|- 草案原文：「成本件与标准件的受让价格均为市场公允价格」 锚：草案 第四章|0
复合词·副本件|- 草案原文：「副本件与正本具有同等效力」 锚：草案 第四章|0
计划自称·本员工持股计划|- 草案原文：「本员工持股计划由公司自行管理」 锚：草案 第七章|0
计划自称·本计划|- 草案原文：「本计划的存续期不超过 36 个月」 锚：草案 第五章|0
已知覆盖不到·通过本件判断|- 草案原文：「通过本件判断本次受让价格公允」 锚：草案 第四章|0
已知覆盖不到·围绕本件|- 草案原文：「围绕本件判断本次受让价格公允」 锚：草案 第四章|0
已知覆盖不到·仍本件认为|- 草案原文：「仍本件认为本次受让价格公允」 锚：草案 第四章|0
CASES
n=0
while IFS='|' read -r tag line want; do
  [ -n "$tag" ] || continue
  n=$((n + 1))
  card="$WORK/case.md"
  # 把这一行插到好样卡的「## 三、口径对照」之前，落临时件
  python3 -B - "$FIX/good-esop-card.md" "$card" "$line" <<'PY'
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
  codes=$(printf '%s\n' "$out" | grep -o '\[ES-[A-Z]*\]' | sort -u | tr '\n' ',' | sed 's/,$//')
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
