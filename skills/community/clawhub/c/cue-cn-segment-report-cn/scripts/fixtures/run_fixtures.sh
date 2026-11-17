#!/usr/bin/env bash
# run_fixtures.sh — 分部报告稿的离线样例 runner
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
#   * 判「节在不在」的那道（SG-STRUCT）认的是**多出同名节**与**不认识节名**，不是「节标题改名」：
#     改标题会让整节变 stray、节内发现行一并丢，连带别的注入测不到——所以这支注入插的是
#     重复节标题，正文一条不丢。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_segment.py"
GOOD="$FIX/good-segment.md"
BAD="$FIX/bad-segment.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-segment-report-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`  SG-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(SG-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
run '好样 good-segment（零发条）' 0 "$GOOD" ''
run '坏样 bad-segment（SG-STRUCT·QUOTE·NOSELF·GAP·LINE 五道齐）' 1 "$BAD" \
  'SG-GAP,SG-LINE,SG-NOSELF,SG-QUOTE,SG-STRUCT'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 多出一节同名标题 → 该只红在 SG-STRUCT
#    不去改节标题名：改名会让整节变 stray、节内发现行一并丢，连带下面几支注入测不到。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '## 分部资产与负债' '## 分部收入与利润

## 分部资产与负债' '多出同名节'; then
  run '多出一节同名「分部收入与利润」→ 只红 SG-STRUCT' 1 "$WORK/e-struct.md" 'SG-STRUCT'
fi

# ② 发现行丢原句与锚 → 该只红在 SG-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「制造业分部对外交易收入 820,000,000.00 元」〔锚：2025 年年报·第 157 页·附注六·分部报告〕[S1]' \
  '820,000,000.00 元 [S1]' '数字行丢原句与锚'; then
  run '分部收入行丢了原句与锚 → 只红 SG-QUOTE' 1 "$WORK/e-quote.md" 'SG-QUOTE'
fi

# ③ 锚标签在而锚值为空 → 该只红在 SG-QUOTE
if mutate "$GOOD" "$WORK/e-anchor.md" \
  '〔锚：2025 年年报·第 159 页·附注六·分部报告〕' '〔锚：〕' '锚值为空'; then
  run '锚标签在而锚值为空 → 只红 SG-QUOTE' 1 "$WORK/e-anchor.md" 'SG-QUOTE'
fi

# ④ 比例自算只给分子没给分母 → 该只红在 SG-NOSELF
if mutate "$GOOD" "$WORK/e-self.md" \
  '｜分母＝三个分部对外交易收入合计 1,350,000,000.00 元 [S1]' \
  '' '自算缺分母'; then
  run '自算只给分子不给分母 → 只红 SG-NOSELF' 1 "$WORK/e-self.md" 'SG-NOSELF'
fi

# ⑤ 自算出来的比例冒充披露值 → 该只红在 SG-NOSELF
#    （原句里没有 8.67%，去掉自算标记后没有人替这个数交代来路）
if mutate "$GOOD" "$WORK/e-bare.md" \
  '- 分部利润合计占对外收入比 8.67%〔自算〕分子＝制造业分部利润 110,000,000.00 元 [S1]｜分母＝三个分部对外交易收入合计 1,350,000,000.00 元 [S1]' \
  '- 分部利润合计占对外收入比 8.67%「制造业分部利润 110,000,000.00 元」〔锚：2025 年年报·第 157 页·附注六·分部报告〕[S1]' \
  '自算充披露值'; then
  run '自算出来的比例冒充披露值 → 只红 SG-NOSELF' 1 "$WORK/e-bare.md" 'SG-NOSELF'
fi

# ⑥ 原句没写分部个数却自标「经营分部三个」→ 该只红在 SG-NOSELF（分部识别只认原句）
if mutate "$GOOD" "$WORK/e-segnum.md" \
  '- 报告分部个数 三个「本公司划分为三个报告分部」〔锚：2025 年年报·第 156 页·附注六·分部报告〕[S1]' \
  '- 报告分部个数 经营分部三个「本公司按产品线组织生产经营」〔锚：2025 年年报·第 156 页·附注六·分部报告〕[S1]' \
  '原句没写分部个数却自标'; then
  run '原句没写分部个数却自标经营分部三个 → 只红 SG-NOSELF' 1 "$WORK/e-segnum.md" 'SG-NOSELF'
fi

# ⑦ 原句没写「主要报告分部」却自标 → 该只红在 SG-NOSELF（主次要之分只认原句）
if mutate "$GOOD" "$WORK/e-mainsec.md" \
  '- 是否合并列报 三个分部均不合并「上述三个经营分部均符合报告分部条件，分别列报」〔锚：2025 年年报·第 156 页·附注六·分部报告〕[S1]' \
  '- 主次要分部 制造业分部为主要报告分部「上述三个经营分部均符合报告分部条件，分别列报」〔锚：2025 年年报·第 156 页·附注六·分部报告〕[S1]' \
  '原句没写主次要却自标'; then
  run '原句没写主要报告分部却自标 → 只红 SG-NOSELF' 1 "$WORK/e-mainsec.md" 'SG-NOSELF'
fi

# ⑧ 勾稽差额自算缺分子来源 → 该只红在 SG-NOSELF
if mutate "$GOOD" "$WORK/e-recon.md" \
  '分子＝分部对外收入合计 1,350,000,000.00 元 [S1]｜' \
  '' '勾稽自算缺分子'; then
  run '勾稽差额自算缺分子来源 → 只红 SG-NOSELF' 1 "$WORK/e-recon.md" 'SG-NOSELF'
fi

# ⑨ 「未取到」写成「无此项」→ 该只红在 SG-GAP（正文那条未取到就没人点名了，两向各报一条）
if mutate "$GOOD" "$WORK/e-gap.md" \
  '- 未取到：服务业分部·分部利润' '- 未取到：无此项' '「无此项」搪塞'; then
  run '第六节写「无此项」→ 只红 SG-GAP' 1 "$WORK/e-gap.md" 'SG-GAP'
fi

# ⑩ 定式禁词 → 该只红在 SG-LINE
#    注入点选第六节的口径行：那一段本来就不要求三元组，插红线句不会连带 SG-QUOTE。
if mutate "$GOOD" "$WORK/e-fixed.md" \
  '- 口径：分部个数、分部名称与主次要之分一律照抄附注原句，不由本件按业务板块或收入规模推断。' \
  '- 口径：制造业分部是最有价值的业务，该公司应优先发展该分部。' '定式禁词自裁'; then
  run '「最有价值的业务／应优先发展」落在非待人工行 → 只红 SG-LINE' 1 "$WORK/e-fixed.md" 'SG-LINE'
fi

# ⑪ 分部利润＝合并净利润 → 该只红在 SG-LINE
if mutate "$GOOD" "$WORK/e-profit.md" \
  '- 口径：分部利润与合并净利润是两个口径，本件不把两者写成相等，也不替披露补差额。' \
  '- 口径：分部利润即合并净利润，两者等同处理。' '两个口径混写'; then
  run '分部利润即合并净利润 → 只红 SG-LINE' 1 "$WORK/e-profit.md" 'SG-LINE'
fi

# ⑫ 对照样：[待人工] 整句成立 → 须零发条（判断位豁免只豁免它自己那一句）
if mutate "$GOOD" "$WORK/c-human.md" \
  '## 口径与未取到' '- 哪块业务更值钱 [待人工]
- 是否建议分拆 [待人工]
- 对股价的影响 [待人工]

## 口径与未取到' '对照·[待人工] 整句'; then
  run '对照·[待人工] 整句成立不误伤（零发条）' 0 "$WORK/c-human.md" ''
fi

# ⑬ 对照样：引文里照抄的「无风险」不是本件断言 → 须零发条
if mutate "$GOOD" "$WORK/c-quoted.md" \
  '「分部信息中的对外交易收入与合并利润表营业收入一致」' \
  '「公司称该分部无风险，分部前景确定」' '对照·引文不算本件断言'; then
  run '对照·引文里的「无风险」不误伤（零发条）' 0 "$WORK/c-quoted.md" ''
fi

# ⑭ 对照样：勾稽差额自算把分子分母都写全 → 须零发条
if mutate "$GOOD" "$WORK/c-recon.md" \
  '- 收入勾稽差额 0.00 万元〔自算〕分子＝分部对外收入合计 1,350,000,000.00 元 [S1]｜分母＝合并营业收入 1,350,000,000.00 元 [S2]' \
  '- 收入勾稽差额 0.00 万元〔自算〕分子＝分部对外收入合计 1,350,000,000.00 元 [S1]｜分母＝合并营业收入 1,350,000,000.00 元 [S2]｜口径＝取合并利润表营业收入原句' \
  '对照·勾稽自算写全'; then
  run '对照·勾稽差额自算分子分母写全不误伤（零发条）' 0 "$WORK/c-recon.md" ''
fi

# ⑮ 对照样：未取到行的项名里带「报告分部」不算自推 → 须零发条
#     正文与第六节的项名要一起改，只改一处会断掉两向对账
if mutate "$GOOD" "$WORK/c-itemname.md" \
  '- 未达量化门槛的分部处理 未取到：附注未披露未达 10% 门槛的分部如何归并' \
  '- 未达报告分部量化门槛的分部处理 未取到：附注未披露未达 10% 门槛的分部如何归并' '对照·项名带词族'; then
  mutate "$WORK/c-itemname.md" "$WORK/c-itemname2.md" \
    '- 未取到：未达量化门槛的分部处理' '- 未取到：未达报告分部量化门槛的分部处理' '对照·项名带词族（第六节）' && \
  run '对照·未取到行的项名带词族不误伤（零发条）' 0 "$WORK/c-itemname2.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
