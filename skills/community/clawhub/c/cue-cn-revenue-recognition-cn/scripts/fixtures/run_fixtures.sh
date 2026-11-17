#!/usr/bin/env bash
# run_fixtures.sh — 收入确认稿的离线样例 runner
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
#   * 判「节在不在」的那道（RR-STRUCT）认的是**多出同名节**与**不认识节名**，不是「标题改名」：
#     改标题会让整节变 stray、节内发现行一并丢，连带别的注入测不到——所以这支注入插的是
#     重复节标题，正文一条不丢。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_revenue.py"
GOOD="$FIX/good-revenue.md"
BAD="$FIX/bad-revenue.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-revenue-recognition-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`  RR-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(RR-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样须过、坏样各支齐发、反证样不误伤、临时件自清）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
printf '%s\n' "$out" | tail -1
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ]; then echo '  → 合'; else echo '  → 不合'; bad=$((bad + 1)); fi

echo '档② 好样／坏样逐枚单跑'
tiers=$((tiers + 1))
run '好样 good-revenue（零发条）' 0 "$GOOD" ''
run '坏样 bad-revenue（RR-STRUCT·QUOTE·NOSELF·GAP·LINE 五道齐）' 1 "$BAD" \
  'RR-GAP,RR-LINE,RR-NOSELF,RR-QUOTE,RR-STRUCT'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 多出一节同名标题 → 该只红在 RR-STRUCT
#    不去改标题名：改名会让整节变 stray、节内发现行一并丢，连带下面几支注入测不到。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '## 时点与时段确认' '## 分摊至各履约义务

## 时点与时段确认' '多出同名节'; then
  run '多出一节同名「分摊至各履约义务」→ 只红 RR-STRUCT' 1 "$WORK/e-struct.md" 'RR-STRUCT'
fi

# ② 发现行丢原句与锚 → 该只红在 RR-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「设备销售分摊交易价格 90,000,000.00 元」〔锚：2025 年年报·第 91 页·附注三·收入〕[S1]' \
  '' '数字行丢原句与锚'; then
  run '分摊行丢了原句与锚 → 只红 RR-QUOTE' 1 "$WORK/e-quote.md" 'RR-QUOTE'
fi

# ③ 锚标签在而锚值为空 → 该只红在 RR-QUOTE
if mutate "$GOOD" "$WORK/e-anchor.md" \
  '〔锚：2025 年年报·第 90 页·附注三·收入〕' '〔锚：〕' '锚值为空'; then
  run '锚标签在而锚值为空 → 只红 RR-QUOTE' 1 "$WORK/e-anchor.md" 'RR-QUOTE'
fi

# ④ 比例自算只给分子没给分母 → 该只红在 RR-NOSELF
if mutate "$GOOD" "$WORK/e-self.md" \
  '分子＝设备销售单独售价 90,000,000.00 元 [S1]｜分母＝各履约义务单独售价合计 120,000,000.00 元 [S1]' \
  '分子＝设备销售单独售价 90,000,000.00 元 [S1]' '自算缺分母'; then
  run '自算只给分子不给分母 → 只红 RR-NOSELF' 1 "$WORK/e-self.md" 'RR-NOSELF'
fi

# ⑤ 自算出来的比例冒充披露值 → 该只红在 RR-NOSELF
#    （原句里没有 75.00%，去掉自算标记后没有人替这个数交代来路）
if mutate "$GOOD" "$WORK/e-bare.md" \
  '- 设备销售占比 75.00%〔自算〕分子＝设备销售单独售价 90,000,000.00 元 [S1]｜分母＝各履约义务单独售价合计 120,000,000.00 元 [S1]' \
  '- 设备销售占比 75.00%「设备销售分摊交易价格 90,000,000.00 元」〔锚：2025 年年报·第 91 页·附注三·收入〕[S1]' \
  '自算充披露值'; then
  run '自算出来的比例冒充披露值 → 只红 RR-NOSELF' 1 "$WORK/e-bare.md" 'RR-NOSELF'
fi

# ⑥ 原句没写时点／时段却自标「时段确认」→ 该只红在 RR-NOSELF（拆分与时点只认原句）
if mutate "$GOOD" "$WORK/e-timing.md" \
  '- 设备销售 时点确认「本集团在客户取得相关商品控制权时点确认收入」〔锚：2025 年年报·第 92 页·附注三·收入〕[S1]' \
  '- 设备销售 时段确认「设备销售于合同签订后交付并验收」〔锚：2025 年年报·第 92 页·附注三·收入〕[S1]' \
  '原句没写时段却自标'; then
  run '原句没写时点时段却自标时段确认 → 只红 RR-NOSELF' 1 "$WORK/e-timing.md" 'RR-NOSELF'
fi

# ⑦ 可变对价自算缺计入上限 → 该只红在 RR-NOSELF
if mutate "$GOOD" "$WORK/e-vc.md" \
  '- 可变对价 600.00 万元「合同约定按验收合格率浮动，可变对价估计为 6,000,000.00 元」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]' \
  '- 可变对价 600.00 万元〔自算〕按合同条款分档测算，估计方法取附注「按期望值确定」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]' \
  '可变对价自算缺上限'; then
  run '可变对价自算缺「计入上限／区间」→ 只红 RR-NOSELF' 1 "$WORK/e-vc.md" 'RR-NOSELF'
fi

# ⑧ 「未取到」写成「不适用」→ 该只红在 RR-GAP（正文那条未取到就没人点名了，两向各报一条）
if mutate "$GOOD" "$WORK/e-gap.md" \
  '- 未取到：合同变更' '- 未取到：不适用' '「不适用」搪塞'; then
  run '第六节写「不适用」→ 只红 RR-GAP' 1 "$WORK/e-gap.md" 'RR-GAP'
fi

# ⑨ 定式禁词 → 该只红在 RR-LINE
#    注入点选第六节的口径行：那一段本来就不要求三元组，插红线句不会连带 RR-QUOTE。
if mutate "$GOOD" "$WORK/e-fixed.md" \
  '- 口径：拆不拆、时点还是时段，一律照抄附注原句，不由本件按行业惯例推断。' \
  '- 口径：本集团收入真实可靠，无虚增收入。' '定式禁词自裁'; then
  run '「无虚增收入」落在非待人工行 → 只红 RR-LINE' 1 "$WORK/e-fixed.md" 'RR-LINE'
fi

# ⑩ 合同负债＝收入 → 该只红在 RR-LINE
if mutate "$GOOD" "$WORK/e-liab.md" \
  '- 口径：合同负债是已收对价而尚未履约的义务，与已确认收入不是同一个数，两者不得互相印证；收现口径见 cn-cash-flow-quality。' \
  '- 口径：合同负债即已确认收入，两者互相印证。' '合同负债＝收入'; then
  run '合同负债写成即已确认收入 → 只红 RR-LINE' 1 "$WORK/e-liab.md" 'RR-LINE'
fi

# ⑪ 对照样：[待人工] 整句成立 → 须零发条（判断位豁免只豁免它自己那一句）
if mutate "$GOOD" "$WORK/c-human.md" \
  '## 口径与未取到' '- 收入是否真实、有无虚构，交由人工判断 [待人工]

## 口径与未取到' '对照·[待人工] 整句'; then
  run '对照·[待人工] 整句成立不误伤（零发条）' 0 "$WORK/c-human.md" ''
fi

# ⑫ 对照样：引文里照抄的「虚构收入」不是本件断言 → 须零发条
if mutate "$GOOD" "$WORK/c-quoted.md" \
  '「对具有类似特征的合同，本集团采用组合方式确认收入」' \
  '「公司否认存在虚构收入，未发生舞弊」' '对照·引文不算本件断言'; then
  run '对照·引文里的「虚构收入」不误伤（零发条）' 0 "$WORK/c-quoted.md" ''
fi

# ⑬ 对照样：可变对价自算把方法与上限都写全 → 须零发条
if mutate "$GOOD" "$WORK/c-vc.md" \
  '- 可变对价 600.00 万元「合同约定按验收合格率浮动，可变对价估计为 6,000,000.00 元」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]' \
  '- 可变对价 600.00 万元〔自算〕按合同条款分档测算，估计方法取附注「按期望值确定」〔锚：2025 年年报·第 90 页·附注三·收入〕[S1]｜计入上限取附注「不超过 6,000,000.00 元」[S1]' \
  '对照·可变对价自算两项写全'; then
  run '对照·可变对价自算方法与上限写全不误伤（零发条）' 0 "$WORK/c-vc.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
