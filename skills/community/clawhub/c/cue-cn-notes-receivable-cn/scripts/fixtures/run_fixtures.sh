#!/usr/bin/env bash
# run_fixtures.sh — 应收应付票据稿的离线样例 runner（M649）
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
# 两条尺子的实话（都在这枚件上现试出来过）：
#   * 注入点不能用「会连带触发别道码」的行——那样测出来的红分不清是哪道判的。本档每支注入
#     都挑该项自己那句话，并在下面逐支注明「该只红在 X」，跑出来的码集不对即判不合。
#   * 判「节在不在」的那道（NR-STRUCT）认的是**多出同名节**与**不认识节名**，不是「标题改名」：
#     改标题会让整节变 stray、节内发现行一并丢，连带别的注入测不到——所以这支注入插的是
#     重复节标题，正文一条不丢。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_notes.py"
GOOD="$FIX/good-notes.md"
BAD="$FIX/bad-notes.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-notes-receivable-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`  NR-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(NR-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样须过、坏样五道齐发、反证样不误伤、临时件自清）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
printf '%s\n' "$out" | tail -1
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ]; then echo '  → 合'; else echo '  → 不合'; bad=$((bad + 1)); fi

echo '档② 好样／坏样逐枚单跑'
tiers=$((tiers + 1))
run '好样 good-notes（零发条）' 0 "$GOOD" ''
run '坏样 bad-notes（NR-STRUCT·QUOTE·NOSELF·GAP·LINE 五道齐）' 1 "$BAD" \
  'NR-GAP,NR-LINE,NR-NOSELF,NR-QUOTE,NR-STRUCT'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 多出一节同名标题 → 该只红在 NR-STRUCT
#    不去改标题名：改名会让整节变 stray、节内发现行一并丢，连带下面几支注入测不到。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '## 期末余额与坏账准备' '## 票据分类

## 期末余额与坏账准备' '多出同名节'; then
  run '多出一节同名「票据分类」→ 只红 NR-STRUCT' 1 "$WORK/e-struct.md" 'NR-STRUCT'
fi

# ② 发现行丢原句与锚 → 该只红在 NR-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「本期到期托收的应收票据 46,000,000.00 元」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]' \
  '' '数字行丢原句与锚'; then
  run '托收行丢了原句与锚 → 只红 NR-QUOTE' 1 "$WORK/e-quote.md" 'NR-QUOTE'
fi

# ③ 锚标签在而锚值为空 → 该只红在 NR-QUOTE
if mutate "$GOOD" "$WORK/e-anchor.md" \
  '〔锚：2025 年年报·第 118 页·附注五·应付票据〕' '〔锚：〕' '锚值为空'; then
  run '锚标签在而锚值为空 → 只红 NR-QUOTE' 1 "$WORK/e-anchor.md" 'NR-QUOTE'
fi

# ④ 比例自算只给分子没给分母 → 该只红在 NR-NOSELF
if mutate "$GOOD" "$WORK/e-self.md" \
  '分子＝坏账准备 1,500,000.00 元 [S1]｜分母＝应收票据期末余额 100,000,000.00 元 [S1]' \
  '分子＝坏账准备 1,500,000.00 元 [S1]' '自算缺分母'; then
  run '自算只给分子不给分母 → 只红 NR-NOSELF' 1 "$WORK/e-self.md" 'NR-NOSELF'
fi

# ⑤ 比例原句有而漏标自算不误伤：把〔自算〕连同分子分母一起去掉、只留原句值 → 该只红在 NR-NOSELF
#    （原句里没有 1.50%，去掉自算标记后没有人替这个数交代来路）
if mutate "$GOOD" "$WORK/e-bare.md" \
  '- 坏账准备计提比例为 1.50%〔自算〕分子＝坏账准备 1,500,000.00 元 [S1]｜分母＝应收票据期末余额 100,000,000.00 元 [S1]' \
  '- 坏账准备计提比例为 1.50%「坏账准备 1,500,000.00 元」〔锚：2025 年年报·第 96 页·附注五·应收票据〕[S1]' \
  '自算充披露值'; then
  run '自算出来的比例冒充披露值 → 只红 NR-NOSELF' 1 "$WORK/e-bare.md" 'NR-NOSELF'
fi

# ⑥ 原句没分类却自己写「商业承兑」→ 该只红在 NR-NOSELF（分类只认原句）
if mutate "$GOOD" "$WORK/e-class.md" \
  '- 应付票据·商业承兑 未取到：附注只按银行承兑列示' \
  '- 应付票据·商业承兑 0.00 万元「应付票据期末余额合计 32,000,000.00 元」〔锚：2025 年年报·第 118 页·附注五·应付票据〕[S2]' \
  '原句没分类却自推'; then
  run '原句只写应收票据却自标商业承兑 → 只红 NR-NOSELF' 1 "$WORK/e-class.md" 'NR-GAP,NR-NOSELF'
fi

# ⑦ 贴现利息自算缺天数折算 → 该只红在 NR-NOSELF（连带 NR-GAP：原句被换走，正文明写未取到的项也没了）
if mutate "$GOOD" "$WORK/e-disc.md" \
  '- 贴现利息 18.00 万元「本期贴现利息支出 180,000.00 元」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]' \
  '- 贴现利息 18.00 万元〔自算〕票面 8,000,000.00 元 [S1]｜利率取附注「年贴现率 3.60%」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]｜期间 76 天 [S1]' \
  '贴现自算缺天数口径'; then
  run '贴现利息自算缺「按 360／365 天折算」→ 只红 NR-NOSELF' 1 "$WORK/e-disc.md" 'NR-NOSELF'
fi

# ⑧ 「未取到」写成「不适用」→ 该只红在 NR-GAP（正文那条未取到就没人点名了，两向各报一条）
if mutate "$GOOD" "$WORK/e-gap.md" \
  '- 未取到：应付票据·商业承兑' '- 未取到：不适用' '「不适用」搪塞'; then
  run '第五节写「不适用」→ 只红 NR-GAP' 1 "$WORK/e-gap.md" 'NR-GAP'
fi

# ⑨ 定式禁词 → 该只红在 NR-LINE
#    注入点选第五节的口径行：那一段本来就不要求三元组，插红线句不会连带 NR-QUOTE。
#    （先前插在正文节里，一条 `- 说明：…` 同时触发「发现行缺三元组」，测出来的红分不清是哪道判的。）
if mutate "$GOOD" "$WORK/e-fixed.md" \
  '- 口径：分类取附注列示的银行承兑与商业承兑两栏，不按出票人名称自推。' \
  '- 口径：本公司所持票据兑付风险低，稳赚。' '定式禁词自裁'; then
  run '「兑付风险低／稳赚」落在非待人工行 → 只红 NR-LINE' 1 "$WORK/e-fixed.md" 'NR-LINE'
fi

# ⑩ 票据保证金＝货币资金 → 该只红在 NR-LINE
if mutate "$GOOD" "$WORK/e-mgn.md" \
  '- 口径：票据保证金属受限资金，与货币资金口径不同，不得互相印证；贴现收到的现金见 cn-cash-flow-quality。' \
  '- 口径：票据保证金即货币资金，两者互相印证。' '保证金＝货币资金'; then
  run '票据保证金写成即货币资金 → 只红 NR-LINE' 1 "$WORK/e-mgn.md" 'NR-LINE'
fi

# ⑪ 对照样：[待人工] 整句成立 → 须零发条（判断位豁免只豁免它自己那一句）
if mutate "$GOOD" "$WORK/c-human.md" \
  '## 口径与未取到' '- 票据到期能否足额兑付，交由人工判断 [待人工]

## 口径与未取到' '对照·[待人工] 整句'; then
  run '对照·[待人工] 整句成立不误伤（零发条）' 0 "$WORK/c-human.md" ''
fi

# ⑫ 对照样：引文里照抄的「承兑人信用」不是本件断言 → 须零发条
if mutate "$GOOD" "$WORK/c-quoted.md" \
  '「本期到期的应收票据均已收回」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]
- 托收是否按期到账' \
  '「公司称承兑人信用良好，未发生拒付」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]
- 托收是否按期到账' '对照·引文不算本件断言'; then
  run '对照·引文里的「承兑人信用」不误伤（零发条）' 0 "$WORK/c-quoted.md" ''
fi

# ⑬ 对照样：贴现利息自算把利率／期间／天数三项写全 → 须零发条
if mutate "$GOOD" "$WORK/c-disc.md" \
  '- 贴现利息 18.00 万元「本期贴现利息支出 180,000.00 元」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]' \
  '- 贴现利息 18.00 万元〔自算〕票面 8,000,000.00 元 [S1]｜利率取附注「年贴现率 3.60%」〔锚：2025 年年报·第 98 页·附注五·应收票据〕[S1]｜期间 76 天、按 360 天折算 [S1]' \
  '对照·贴现自算三项写全'; then
  run '对照·贴现自算三项口径写全不误伤（零发条）' 0 "$WORK/c-disc.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
