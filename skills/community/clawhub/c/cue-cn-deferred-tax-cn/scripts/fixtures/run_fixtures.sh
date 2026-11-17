#!/usr/bin/env bash
# run_fixtures.sh — 递延所得税稿的离线样例 runner
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
# 三条尺子的实话：
#   * 注入点不能用「会连带触发别道码」的行——那样测出来的红分不清是哪道判的。本档每支注入
#     都挑该项自己那句话，并在下面逐支注明「该只红在 X」，跑出来的码集不对即判不合。
#   * 判「节在不在」的那道（DT-STRUCT）认的是**多出同名节**与**不认识节名**，不是「节标题改名」：
#     改标题会让整节变 stray、节内发现行一并丢，连带别的注入测不到——所以这支注入插的是
#     重复节标题，正文一条不丢。
#   * 本件的「未取到」有两处会被误当成登记行：第六节的 `口径：…` 行里本身就有「写未取到」这句
#     话。所以注入一律避开口径行里的「未取到」三字，且机检侧只认 `未取到` 开头或 `项名：未取到`
#     两种登记形——否则每支注入都会顺带多出一条假 DT-GAP，码集永远对不上。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_deferred_tax.py"
GOOD="$FIX/good-deferred-tax.md"
BAD="$FIX/bad-deferred-tax.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-deferred-tax-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`  DT-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(DT-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
run '好样 good-deferred-tax（零发条）' 0 "$GOOD" ''
run '坏样 bad-deferred-tax（DT-STRUCT·QUOTE·NOSELF·GAP·LINE 五道齐）' 1 "$BAD" \
  'DT-GAP,DT-LINE,DT-NOSELF,DT-QUOTE,DT-STRUCT'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 多出一节同名标题 → 该只红在 DT-STRUCT
#    不去改节标题名：改名会让整节变 stray、节内发现行一并丢，连带下面几支注入测不到。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '## 未经抵销的递延所得税资产与负债' '## 递延所得税资产与负债明细

## 未经抵销的递延所得税资产与负债' '多出同名节'; then
  run '多出一节同名「递延所得税资产与负债明细」→ 只红 DT-STRUCT' 1 "$WORK/e-struct.md" 'DT-STRUCT'
fi

# ② 发现行丢原句与锚 → 该只红在 DT-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「期末递延所得税资产余额 1,500,000.00 元」〔锚：2025 年年报·第 140 页·附注三·递延所得税〕[S1]' \
  '1,500,000.00 元 [S1]' '数字行丢原句与锚'; then
  run '资产减值准备期末丢了原句与锚 → 只红 DT-QUOTE' 1 "$WORK/e-quote.md" 'DT-QUOTE'
fi

# ③ 锚标签在而锚值为空 → 该只红在 DT-QUOTE
if mutate "$GOOD" "$WORK/e-anchor.md" \
  '〔锚：2025 年年报·第 142 页·附注三·递延所得税〕' '〔锚：〕' '锚值为空'; then
  run '锚标签在而锚值为空 → 只红 DT-QUOTE' 1 "$WORK/e-anchor.md" 'DT-QUOTE'
fi

# ④ 自算只给分子没给分母 → 该只红在 DT-NOSELF
if mutate "$GOOD" "$WORK/e-self.md" \
  '｜分母＝可抵扣亏损总额 20,000,000.00 元 [S1]' '' '自算缺分母'; then
  run '未确认亏损占比自算只给分子不给分母 → 只红 DT-NOSELF' 1 "$WORK/e-self.md" 'DT-NOSELF'
fi

# ⑤ 自算出来的比例冒充披露值 → 该只红在 DT-NOSELF
#    （原句里没有 40.00%，去掉〔自算〕后没有人替这个数交代来路）
if mutate "$GOOD" "$WORK/e-bare.md" \
  '- 未确认亏损占比：40.00%〔自算〕分子＝未确认的可抵扣亏损 8,000,000.00 元 [S1]｜分母＝可抵扣亏损总额 20,000,000.00 元 [S1]' \
  '- 未确认亏损占比：40.00%「未确认递延所得税资产的可抵扣亏损 8,000,000.00 元」〔锚：2025 年年报·第 142 页·附注三·递延所得税〕[S1]' \
  '自算充披露值'; then
  run '自算出来的比例冒充披露值 → 只红 DT-NOSELF' 1 "$WORK/e-bare.md" 'DT-NOSELF'
fi

# ⑥ 拿「未经抵销」那两句顶「互抵金额」→ 该只红在 DT-NOSELF（互抵额只认抵销额写法）
#    「抵销」是「未经抵销」的子串，所以判据不能只认「抵销」二字——那正是轧差最想蒙混的写法。
if mutate "$GOOD" "$WORK/e-offset.md" \
  '- 互抵金额：200.00 万元「上述递延所得税资产与负债以 2,000,000.00 元为限相互抵销」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]' \
  '- 互抵金额：200.00 万元「未经抵销的递延所得税资产 19,000,000.00 元，未经抵销的递延所得税负债 3,000,000.00 元」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]' \
  '互抵额拿未经抵销顶'; then
  run '互抵金额拿「未经抵销」两句顶上 → 只红 DT-NOSELF' 1 "$WORK/e-offset.md" 'DT-NOSELF'
fi

# ⑦ 拿「未经抵销的资产」顶「抵销后净额」→ 该只红在 DT-NOSELF（净额取自披露，不由本件做减法）
if mutate "$GOOD" "$WORK/e-net.md" \
  '- 抵销后净额·资产：1,700.00 万元「抵销后列示的递延所得税资产净额 17,000,000.00 元」' \
  '- 抵销后净额·资产：1,700.00 万元「未经抵销的递延所得税资产 19,000,000.00 元」' \
  '净额拿未经抵销顶'; then
  run '抵销后净额拿「未经抵销」顶上 → 只红 DT-NOSELF' 1 "$WORK/e-net.md" 'DT-NOSELF'
fi

# ⑧ 第二节少一行「互抵金额」→ 该只红在 DT-STRUCT（四个数各占一行，没披露也要留它的未取到）
if mutate "$GOOD" "$WORK/e-missing.md" \
  '- 互抵金额：200.00 万元「上述递延所得税资产与负债以 2,000,000.00 元为限相互抵销」〔锚：2025 年年报·第 141 页·附注三·递延所得税〕[S1]
' '' '互抵四数少一行'; then
  run '第二节少了「互抵金额」这一行 → 只红 DT-STRUCT' 1 "$WORK/e-missing.md" 'DT-STRUCT'
fi

# ⑨ 税率落默认值 → 该只红在 DT-NOSELF
#    （法定税率 25% 是常识，但披露没写就只能写未取到。注入把引文里的 25% 拿掉，
#      项名「法定税率」仍在，机检按「谈税率而原句无数」判，即便标〔自算〕也不放过）
if mutate "$GOOD" "$WORK/e-rate.md" \
  '- 法定税率：25%「本公司适用的企业所得税法定税率为 25%」〔锚：2025 年年报·第 144 页·附注三·所得税费用〕[S1]' \
  '- 法定税率：按 25% 计算〔自算〕「本公司适用的企业所得税税率见附注三」〔锚：2025 年年报·第 144 页·附注三·所得税费用〕[S1]｜分子＝1 [S1]｜分母＝1 [S1]' \
  '税率落默认值'; then
  run '税率按 25% 默认值补（标了自算也发）→ 只红 DT-NOSELF' 1 "$WORK/e-rate.md" 'DT-NOSELF'
fi

# ⑩ 「未取到」写成「不适用」→ 该只红在 DT-GAP（正文那条未取到就没人点名了，两向各报一条）
if mutate "$GOOD" "$WORK/e-gap.md" \
  '- 未取到：调节表差异项' '- 未取到：不适用' '「不适用」搪塞'; then
  run '第六节写「不适用」→ 只红 DT-GAP' 1 "$WORK/e-gap.md" 'DT-GAP'
fi

# ⑪ 定式禁词 → 该只红在 DT-LINE
#    注入点选第六节的口径行：那一段本来就不要求三元组，插红线句不会连带 DT-QUOTE。
if mutate "$GOOD" "$WORK/e-fixed.md" \
  '- 口径：递延所得税资产与负债逐项照抄期初、本期增减、期末，未列的项目不补。' \
  '- 口径：递延所得税资产未来能够转回，税务风险可控。' '定式禁词自裁'; then
  run '「能够转回／税务风险可控」落在非待人工行 → 只红 DT-LINE' 1 "$WORK/e-fixed.md" 'DT-LINE'
fi

# ⑫ 抵销后净额＝未经抵销 → 该只红在 DT-LINE（把抵销这一层抹掉）
if mutate "$GOOD" "$WORK/e-mix.md" \
  '- 口径：未经抵销的资产、未经抵销的负债、互抵金额、抵销后净额是四个独立数，各占一行；抵销额取自披露，不由本件做减法。' \
  '- 口径：抵销后净额即未经抵销的递延所得税资产，两者相等。' '互抵四数混写'; then
  run '抵销后净额即未经抵销金额 → 只红 DT-LINE' 1 "$WORK/e-mix.md" 'DT-LINE'
fi

# ⑬ 对照样：[待人工] 整句成立 → 须零发条（判断位豁免只豁免它自己那一句）
if mutate "$GOOD" "$WORK/c-human.md" \
  '## 口径与未取到' '- 递延所得税资产能否转回 [待人工]
- 未来盈利能否覆盖可抵扣亏损 [待人工]
- 税务风险高低 [待人工]

## 口径与未取到' '对照·[待人工] 整句'; then
  run '对照·[待人工] 整句成立不误伤（零发条）' 0 "$WORK/c-human.md" ''
fi

# ⑭ 对照样：引文里照抄的「能够转回」不是本件断言 → 须零发条
if mutate "$GOOD" "$WORK/c-quoted.md" \
  '「合并报表按各纳税主体适用税率分别计算后合并」' \
  '「公司称该递延所得税资产能够转回，税务风险可控」' '对照·引文不算本件断言'; then
  run '对照·引文里的「能够转回」不误伤（零发条）' 0 "$WORK/c-quoted.md" ''
fi

# ⑮ 对照样：项名里带「互抵·抵销」不算自推 → 须零发条
if mutate "$GOOD" "$WORK/c-itemname.md" \
  '- 互抵金额：200.00 万元「上述递延所得税资产与负债以 2,000,000.00 元为限相互抵销」' \
  '- 互抵·抵销金额 200.00 万元「上述递延所得税资产与负债以 2,000,000.00 元为限相互抵销」' \
  '对照·项名带词族'; then
  run '对照·项名里带「互抵·抵销」不误伤（零发条）' 0 "$WORK/c-itemname.md" ''
fi

# ⑯ 对照样：未取到行里的百分比整行豁免比值判定 → 须零发条
#    （那一行的百分比是在标「没取到的是哪一项」，不是本件算的）
if mutate "$GOOD" "$WORK/c-gappct.md" \
  '- 未确认暂时性差异：未取到：附注未列示未确认的可抵扣暂时性差异' \
  '- 未确认暂时性差异：未取到：附注未按 25% 分解列示未确认的可抵扣暂时性差异' \
  '对照·未取到行带百分比'; then
  run '对照·未取到行里的百分比整行豁免（零发条）' 0 "$WORK/c-gappct.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
