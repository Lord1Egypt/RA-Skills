#!/usr/bin/env bash
# run_fixtures.sh — 或有事项与承诺事项稿的离线样例 runner
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
#   * 判「节在不在」的那道（CC-STRUCT）认的是**多出同名节**与**不认识节名**，不是「节标题改名」：
#     改标题会让整节变 stray、节内发现行一并丢，连带别的注入测不到——所以这支注入插的是
#     重复节标题，正文一条不丢。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_contingency.py"
GOOD="$FIX/good-contingency.md"
BAD="$FIX/bad-contingency.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-contingency-commitment-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`  CC-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(CC-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
run '好样 good-contingency（零发条）' 0 "$GOOD" ''
run '坏样 bad-contingency（CC-STRUCT·QUOTE·NOSELF·GAP·LINE 五道齐）' 1 "$BAD" \
  'CC-GAP,CC-LINE,CC-NOSELF,CC-QUOTE,CC-STRUCT'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 多出一节同名标题 → 该只红在 CC-STRUCT
#    不去改节标题名：改名会让整节变 stray、节内发现行一并丢，连带下面几支注入测不到。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '## 预计负债与或有负债的区分' '## 承诺事项

## 预计负债与或有负债的区分' '多出同名节'; then
  run '多出一节同名「承诺事项」→ 只红 CC-STRUCT' 1 "$WORK/e-struct.md" 'CC-STRUCT'
fi

# ② 发现行丢原句与锚 → 该只红在 CC-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]' \
  '30,000,000.00 元 [S1]' '数字行丢原句与锚'; then
  run '担保行丢了原句与锚 → 只红 CC-QUOTE' 1 "$WORK/e-quote.md" 'CC-QUOTE'
fi

# ③ 锚标签在而锚值为空 → 该只红在 CC-QUOTE
if mutate "$GOOD" "$WORK/e-anchor.md" \
  '〔锚：2025 年年报·第 132 页·附注三·承诺事项〕' '〔锚：〕' '锚值为空'; then
  run '锚标签在而锚值为空 → 只红 CC-QUOTE' 1 "$WORK/e-anchor.md" 'CC-QUOTE'
fi

# ④ 担保占比自算只给分子没给分母 → 该只红在 CC-NOSELF
if mutate "$GOOD" "$WORK/e-self.md" \
  '｜分母＝归属于母公司所有者权益 1,000,000,000.00 元 [S1]' \
  '' '自算缺分母'; then
  run '自算只给分子不给分母 → 只红 CC-NOSELF' 1 "$WORK/e-self.md" 'CC-NOSELF'
fi

# ⑤ 自算出来的比例冒充披露值 → 该只红在 CC-NOSELF
#    （原句里没有 3.00%，去掉自算标记后没有人替这个数交代来路）
if mutate "$GOOD" "$WORK/e-bare.md" \
  '- 担保余额占净资产比例 3.00%〔自算〕金额取附注「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]｜分子＝担保余额 30,000,000.00 元 [S1]｜分母＝归属于母公司所有者权益 1,000,000,000.00 元 [S1]' \
  '- 担保余额占净资产比例 3.00%「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]' \
  '自算充披露值'; then
  run '自算出来的比例冒充披露值 → 只红 CC-NOSELF' 1 "$WORK/e-bare.md" 'CC-NOSELF'
fi

# ⑥ 原句没写诉讼阶段却自标「一审已判决」→ 该只红在 CC-NOSELF（诉讼阶段只认原句）
if mutate "$GOOD" "$WORK/e-stage.md" \
  '- 诉讼阶段 一审已判决「本案一审已判决，本公司已提起上诉」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]' \
  '- 诉讼阶段 一审已判决「原告请求本公司赔偿 12,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]' \
  '原句没写诉讼阶段却自标'; then
  run '原句没写诉讼阶段却自标一审已判决 → 只红 CC-NOSELF' 1 "$WORK/e-stage.md" 'CC-NOSELF'
fi

# ⑦ 原句没写「未终止确认」却自标 → 该只红在 CC-NOSELF（终止确认只认原句）
if mutate "$GOOD" "$WORK/e-derecog.md" \
  '- 已贴现商业承兑票据 500.00 万元「已贴现未到期的商业承兑票据 5,000,000.00 元，附追索权，本公司未终止确认」〔锚：2025 年年报·第 131 页·附注三·或有事项〕[S1]' \
  '- 已贴现商业承兑票据 未终止确认「已贴现未到期的商业承兑票据 5,000,000.00 元，附追索权」〔锚：2025 年年报·第 131 页·附注三·或有事项〕[S1]' \
  '原句没写终止确认却自标'; then
  run '原句没写「未终止确认」却自标 → 只红 CC-NOSELF' 1 "$WORK/e-derecog.md" 'CC-NOSELF'
fi

# ⑧ 或有金额自算缺金额出处 → 该只红在 CC-NOSELF
if mutate "$GOOD" "$WORK/e-prov.md" \
  '金额取附注「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]｜' \
  '' '或有金额自算缺金额出处'; then
  run '或有金额自算缺「金额取哪一句」→ 只红 CC-NOSELF' 1 "$WORK/e-prov.md" 'CC-NOSELF'
fi

# ⑨ 「未取到」写成「不适用」→ 该只红在 CC-GAP（正文那条未取到就没人点名了，两向各报一条）
if mutate "$GOOD" "$WORK/e-gap.md" \
  '- 未取到：投资承诺' '- 未取到：不适用' '「不适用」搪塞'; then
  run '第六节写「不适用」→ 只红 CC-GAP' 1 "$WORK/e-gap.md" 'CC-GAP'
fi

# ⑩ 定式禁词 → 该只红在 CC-LINE
#    注入点选第六节的口径行：那一段本来就不要求三元组，插红线句不会连带 CC-QUOTE。
if mutate "$GOOD" "$WORK/e-fixed.md" \
  '- 口径：或有事项的性质、金额与不确定性一律照抄附注原句，不由本件按事项类型或金额大小推断。' \
  '- 口径：本案胜诉概率较高，不会败诉，风险可控。' '定式禁词自裁'; then
  run '「胜诉概率／不会败诉」落在非待人工行 → 只红 CC-LINE' 1 "$WORK/e-fixed.md" 'CC-LINE'
fi

# ⑪ 预计负债＝或有负债 → 该只红在 CC-LINE
if mutate "$GOOD" "$WORK/e-mix.md" \
  '- 口径：确认预计负债还是仅作或有负债披露，只照抄附注那一句；两者是不同的处理，不得写成相等或互相替代。' \
  '- 口径：预计负债视同或有负债，两者按同一种方式处理。' '两类负债混写'; then
  run '预计负债视同或有负债 → 只红 CC-LINE' 1 "$WORK/e-mix.md" 'CC-LINE'
fi

# ⑫ 对照样：[待人工] 整句成立 → 须零发条（判断位豁免只豁免它自己那一句）
if mutate "$GOOD" "$WORK/c-human.md" \
  '## 口径与未取到' '- 是否很可能败诉 [待人工]
- 赔偿金额估计 [待人工]
- 是否影响偿债能力 [待人工]

## 口径与未取到' '对照·[待人工] 整句'; then
  run '对照·[待人工] 整句成立不误伤（零发条）' 0 "$WORK/c-human.md" ''
fi

# ⑬ 对照样：引文里照抄的「不会败诉」不是本件断言 → 须零发条
if mutate "$GOOD" "$WORK/c-quoted.md" \
  '「对关联方担保已在关联方交易附注中单独披露」' \
  '「公司称该诉讼不会败诉，不存在败诉风险」' '对照·引文不算本件断言'; then
  run '对照·引文里的「不会败诉」不误伤（零发条）' 0 "$WORK/c-quoted.md" ''
fi

# ⑭ 对照样：或有金额自算把金额出处与分子分母都写全 → 须零发条
if mutate "$GOOD" "$WORK/c-prov.md" \
  '- 对外担保 担保余额 3,000.00 万元「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]' \
  '- 对外担保 担保余额 3,000.00 万元〔自算〕金额取附注「本公司为子公司提供担保 30,000,000.00 元」〔锚：2025 年年报·第 130 页·附注三·或有事项〕[S1]｜分子＝担保余额 30,000,000.00 元 [S1]｜分母＝归属于母公司所有者权益 1,000,000,000.00 元 [S1]' \
  '对照·或有金额自算写全'; then
  run '对照·或有金额自算出处与分子分母写全不误伤（零发条）' 0 "$WORK/c-prov.md" ''
fi

# ⑮ 对照样：项名里带「或有事项」不算自推 → 须零发条
if mutate "$GOOD" "$WORK/c-itemname.md" \
  '- 对外担保 担保余额 3,000.00 万元「本公司为子公司提供担保 30,000,000.00 元」' \
  '- 或有事项·对外担保：担保余额 3,000.00 万元「本公司为子公司提供担保 30,000,000.00 元」' \
  '对照·项名带词族'; then
  run '对照·项名里带「或有事项」不误伤（零发条）' 0 "$WORK/c-itemname.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
