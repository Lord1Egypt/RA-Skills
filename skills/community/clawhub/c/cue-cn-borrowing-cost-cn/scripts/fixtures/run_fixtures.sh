#!/usr/bin/env bash
# run_fixtures.sh — 借款费用资本化登记稿的离线样例 runner
#
# 三档：① 机检自测 → ② 好样／坏样逐枚单跑 → ③ 边界形逐枚单跑。
# 零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp} 下自建目录，跑完即删。
# 退码：0 三档全合期望；1 有不合（逐枚点名，附真实退码与真实码集）；3 取值域故障
#       （脚本或夹具取不到、或某支注入没落地——不读成「零违例」）。
#
# 为什么每支注入都先断言「注入真的落地了」：注入字符串对不上夹具时，替换会静默产出原文，
# 于是「边界形该红没红」会被读成「机检漏判」，实际是尺子没被放上去。这类假红比漏判更贵，
# 所以注入后一律比字节，不一致即 exit 3。
#
# 两条尺子的实话：
#   * 注入点不能用「会连带触发别道码」的行——那样测出来的红分不清是哪道判的。本档每支注入
#     都挑该项自己那句话，并在下面逐支注明「该只红在 X」，跑出来的码集不对即判不合。
#   * BC-CAP 与 BC-SPLIT 共用概况节的「其中资本化」：改那个数两道的会一起红，
#     所以凡是只想测两分的注入，改的是「其中费用化」；只想测恒等的，改的是资本化率或占用额。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_borrowing_cost.py"
GOOD="$FIX/good-borrowing.md"
BAD="$FIX/bad-borrowing.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-borrowing-cost-cn.XXXXXX")" || {
  echo "3 取值域故障：临时目录没建成（TMPDIR=${TMPDIR:-未设} 是否存在、可写？）"; exit 3; }
[ -d "$WORK" ] || { echo "3 取值域故障：临时目录不存在"; exit 3; }
trap 'rm -rf "$WORK"' EXIT

for f in "$CK" "$GOOD" "$BAD"; do
  [ -f "$f" ] || { echo "3 取值域故障：取不到 $f（不读成「夹具全过」）"; exit 3; }
done

bad=0
unk=0
tiers=0

# 一支注入：mutate <源件> <目标件> <原文片段> <替换片段> <标签>
# 失败（片段不在源件里、或替换后与源件同字节）＝ 取值域故障，不计入「不合」。
mutate() {
  local src="$1" dst="$2" old="$3" new="$4" tag="$5"
  if ! python3 -B - "$src" "$dst" "$old" "$new" <<'PY'
import sys
from pathlib import Path
src, dst, old, new = sys.argv[1:5]
t = Path(src).read_text(encoding='utf-8')
if old not in t:
    sys.exit('注入点不在源件里')
out = t.replace(old, new)
if out == t:
    sys.exit('替换后与源件同字节')
Path(dst).write_text(out, encoding='utf-8')
PY
  then
    echo "  不可判 $tag：注入没落地（片段对不上夹具，不读成「机检漏判」）"
    unk=$((unk + 1)); return 1
  fi
  return 0
}

# 跑一枚：run <标签> <期望退码> <文件> <期望码集（空＝不发码）|*＝不核码集>
# 码集从机检自己的输出里取（行首 BC-XXX），不另跑一份统计：
# 取的是「这枚稿实际发了哪几道」，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^\(BC-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样须过、坏样各支齐发、反证样不误伤）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
printf '%s\n' "$out" | tail -1
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ]; then echo '  → 合'; else echo '  → 不合'; bad=$((bad + 1)); fi

echo '档② 好样／坏样逐枚单跑'
tiers=$((tiers + 1))
run '好样 good-borrowing（零发条）' 0 "$GOOD" ''
run '坏样 bad-borrowing（BC-STRUCT·QUOTE·CAP·SPLIT·LINE 五道齐）' 1 "$BAD" \
  'BC-CAP,BC-LINE,BC-QUOTE,BC-SPLIT,BC-STRUCT'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 多出一节同名标题 → 该只红在 BC-STRUCT
if mutate "$GOOD" "$WORK/e-struct.md" \
  '## 专门借款' '## 概况补充

## 专门借款' '多出认不出的节标题'; then
  run '多出一节认不出的标题「概况补充」→ 只红 BC-STRUCT' 1 "$WORK/e-struct.md" 'BC-STRUCT'
fi

# ② 数字行丢原句 → 该只红在 BC-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「本集团本期借款费用利息支出合计为人民币 356.00 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]' \
  '' '数字行丢原句与锚'; then
  run '利息合计行丢了原句与锚 → 只红 BC-QUOTE' 1 "$WORK/e-quote.md" 'BC-QUOTE'
fi

# ③ 来源行检索日写成斜杠式 → 该只红在 BC-QUOTE
if mutate "$GOOD" "$WORK/e-date.md" \
  '检索日 2025-04-20' '检索日 2025/04/20' '检索日斜杠式'; then
  run '来源行检索日写成 2025/04/20 → 只红 BC-QUOTE' 1 "$WORK/e-date.md" 'BC-QUOTE'
fi

# ④ 正文引了未登记的 [S9] → 该只红在 BC-QUOTE
if mutate "$GOOD" "$WORK/e-cite.md" \
  '〔锚：2025 年年报·第 231 页·借款费用〕[S1]' '〔锚：2025 年年报·第 231 页·借款费用〕[S9]' \
  '引用未登记编号'; then
  run '正文引了 [S9] 但来源只登记 [S1] → 只红 BC-QUOTE' 1 "$WORK/e-cite.md" 'BC-QUOTE'
fi

# ⑤ 两分：只改「其中费用化」→ 该只红在 BC-SPLIT（另两道的数没动）
if mutate "$GOOD" "$WORK/e-split.md" \
  '- 其中费用化〔口径：本期发生额〕53.50 万元「其中计入当期损益的金额为人民币 53.50 万元」' \
  '- 其中费用化〔口径：本期发生额〕60.50 万元「其中计入当期损益的金额为人民币 60.50 万元」' \
  '两分加不回合计'; then
  run '其中费用化 53.50 → 60.50（两分加不回合计）→ 只红 BC-SPLIT' 1 "$WORK/e-split.md" 'BC-SPLIT'
fi

# ⑥ 恒等：只改资本化率 → 该只红在 BC-CAP（概况节的数一个没动）
if mutate "$GOOD" "$WORK/e-cap.md" \
  '- 一般借款资本化率〔口径：本期〕5.00%「一般借款资本化率为 5.00%」' \
  '- 一般借款资本化率〔口径：本期〕6.00%「一般借款资本化率为 6.00%」' \
  '资本化率失真'; then
  run '一般借款资本化率 5.00% → 6.00% → 只红 BC-CAP' 1 "$WORK/e-cap.md" 'BC-CAP'
fi

# ⑦ 恒等：删掉闲置资金收益整行 → BC-CAP 该报「整条跳过」并点名缺项（不按 0 算）
if mutate "$GOOD" "$WORK/e-idle.md" \
  '- 闲置资金收益〔口径：本期发生额〕12.50 万元「尚未动用的专门借款取得的利息收入为人民币 12.50 万元」〔锚：2025 年年报·第 231 页·借款费用〕[S1]
' '' '闲置资金收益整行删掉'; then
  run '删掉闲置资金收益整行 → BC-CAP 整条跳过并点名缺项' 1 "$WORK/e-idle.md" 'BC-CAP'
fi

# ⑧ 红线：正文写一句越界评价 → 该只红在 BC-LINE
if mutate "$GOOD" "$WORK/e-line.md" \
  '- 一般借款资本化金额〔口径：本期发生额〕97.50 万元' \
  '- 一般借款资本化金额 融资成本偏高〔口径：本期发生额〕97.50 万元' '红线评价词'; then
  run '正文写「融资成本偏高」→ 只红 BC-LINE' 1 "$WORK/e-line.md" 'BC-LINE'
fi

# ⑨ 对照样：引文里照抄的「预计」不是本件断言 → 须零发条
if mutate "$GOOD" "$WORK/c-quoted.md" \
  '「其中计入当期损益的金额为人民币 53.50 万元」' \
  '「公司预计其中计入当期损益的金额为人民币 53.50 万元」' '对照·引文不算断言'; then
  run '对照·引文里的「预计」不误伤（零发条）' 0 "$WORK/c-quoted.md" ''
fi

# ⑩ 对照样：锚指向「预计负债」科目名不是断言 → 须零发条
if mutate "$GOOD" "$WORK/c-anchor.md" \
  '第 231 页·借款费用' '第 231 页·预计负债' '对照·锚里的科目名'; then
  run '对照·锚指向「预计负债」科目名不误伤（零发条）' 0 "$WORK/c-anchor.md" ''
fi

# ⑪ 对照样：口径槽里的「预计」是标签不是断言 → 须零发条
if mutate "$GOOD" "$WORK/c-slot.md" \
  '〔口径：本期发生额〕97.50' '〔口径：预计下年〕97.50' '对照·口径槽标签'; then
  run '对照·口径槽写「预计」不误伤（零发条）' 0 "$WORK/c-slot.md" ''
fi

# ⑫ 对照样：缺口已在口径节声明 ⇒ 两道恒等静默跳过，不重复报缺失 → 须零发条
if mutate "$GOOD" "$WORK/c-gap.md" \
  '- 一般借款资本化率〔口径：本期〕5.00%「一般借款资本化率为 5.00%」〔锚：2025 年年报·第 231 页·借款费用〕[S1]' \
  '- 未取到：一般借款资本化率' '对照·缺口已声明'; then
  if mutate "$WORK/c-gap.md" "$WORK/c-gap2.md" \
    '- 未取到：无' '- 未取到：一般借款资本化率' '对照·缺口同步声明'; then
    run '对照·缺口两边都声明 ⇒ 零发条（不重复报缺失）' 0 "$WORK/c-gap2.md" ''
  fi
fi

# ⑬ 对照样：[待人工] 整句成立 → 须零发条（判断位不是断言）
if mutate "$GOOD" "$WORK/c-human.md" \
  '- 开始资本化时点〔口径：本期〕[待人工]' \
  '- 开始资本化时点 是否偏高〔口径：本期〕[待人工]' '对照·[待人工] 整句'; then
  run '对照·[待人工] 行里的评价词不误伤（零发条）' 0 "$WORK/c-human.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
