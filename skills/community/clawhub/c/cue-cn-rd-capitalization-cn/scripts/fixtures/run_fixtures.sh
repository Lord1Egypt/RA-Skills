#!/usr/bin/env bash
# run_fixtures.sh — 研发支出资本化稿的离线样例 runner
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
#   * 判「节在不在」的那道（RD-STRUCT）认的是**多出同名节**与**不认识节名**，不是「节标题改名」：
#     改标题会让整节变 stray、节内发现行一并丢，连带别的注入测不到——所以这支注入插的是
#     重复节标题，正文一条不丢。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_rd_capitalization.py"
GOOD="$FIX/good-rd.md"
BAD="$FIX/bad-rd.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-rd-capitalization-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`  RD-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(RD-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
run '好样 good-rd（零发条）' 0 "$GOOD" ''
run '坏样 bad-rd（RD-STRUCT·QUOTE·NOSELF·GAP·LINE 五道齐）' 1 "$BAD" \
  'RD-GAP,RD-LINE,RD-NOSELF,RD-QUOTE,RD-STRUCT'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 多出一节同名标题 → 该只红在 RD-STRUCT
#    不去改节标题名：改名会让整节变 stray、节内发现行一并丢，连带下面几支注入测不到。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '## 开发支出明细' '## 研发投入与资本化概况

## 开发支出明细' '多出同名节'; then
  run '多出一节同名「研发投入与资本化概况」→ 只红 RD-STRUCT' 1 "$WORK/e-struct.md" 'RD-STRUCT'
fi

# ② 发现行丢原句与锚 → 该只红在 RD-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「本期研发投入合计 320,000,000.00 元」〔锚：2025 年年报·第 128 页·附注五·研发投入〕[S1]' \
  '320,000,000.00 元 [S1]' '数字行丢原句与锚'; then
  run '研发投入行丢了原句与锚 → 只红 RD-QUOTE' 1 "$WORK/e-quote.md" 'RD-QUOTE'
fi

# ③ 锚标签在而锚值为空 → 该只红在 RD-QUOTE
if mutate "$GOOD" "$WORK/e-anchor.md" \
  '〔锚：2025 年年报·第 129 页·附注五·开发支出〕' '〔锚：〕' '锚值为空'; then
  run '锚标签在而锚值为空 → 只红 RD-QUOTE' 1 "$WORK/e-anchor.md" 'RD-QUOTE'
fi

# ④ 比例自算只给分子没给分母 → 该只红在 RD-NOSELF
if mutate "$GOOD" "$WORK/e-self.md" \
  '｜分母＝本期研发投入合计 320,000,000.00 元 [S1]' \
  '' '自算缺分母'; then
  run '自算只给分子不给分母 → 只红 RD-NOSELF' 1 "$WORK/e-self.md" 'RD-NOSELF'
fi

# ⑤ 自算出来的比例冒充披露值 → 该只红在 RD-NOSELF
#    （原句里没有 25.00%，去掉自算标记后没有人替这个数交代来路）
if mutate "$GOOD" "$WORK/e-bare.md" \
  '- 资本化率 25.00%〔自算〕分子＝本期资本化研发投入 80,000,000.00 元 [S1]｜分母＝本期研发投入合计 320,000,000.00 元 [S1]' \
  '- 资本化率 25.00%「本期资本化研发投入 80,000,000.00 元」〔锚：2025 年年报·第 128 页·附注五·研发投入〕[S1]' \
  '自算充披露值'; then
  run '自算出来的比例冒充披露值 → 只红 RD-NOSELF' 1 "$WORK/e-bare.md" 'RD-NOSELF'
fi

# ⑥ 原句没写阶段划分却自标 → 该只红在 RD-NOSELF
#    注入点保留原句（去掉「研究阶段／开发阶段」），让正文的「开发阶段」成为原句之外的唯一词族
if mutate "$GOOD" "$WORK/e-stage.md" \
  '- 划分标准 照抄附注表述「研究阶段的支出于发生时计入当期损益，开发阶段的支出同时满足下列条件的予以资本化」' \
  '- 划分标准 开发阶段支出全部资本化「本公司的研发活动按项目立项管理，各项支出按项目归集」' \
  '原句没写阶段划分却自标'; then
  run '原句没写阶段划分却自标开发阶段 → 只红 RD-NOSELF' 1 "$WORK/e-stage.md" 'RD-NOSELF'
fi

# ⑦ 原句没写「满足资本化条件」却自标 → 该只红在 RD-NOSELF
#    注入点必须保留三元组：把「条件判断依据」那条未取到行整行换掉，会连带断掉两向对账（假 RD-GAP）
#    并让该行丢失原句与锚（假 RD-QUOTE），测出来的红就分不清是哪道判的。
#    所以改的是另一条**有完整三元组**的行，在值位里加一句原句之外的判断。
if mutate "$GOOD" "$WORK/e-cond.md" \
  '- 研究阶段支出 24,000.00 万元「本期研究阶段支出 240,000,000.00 元，全部计入当期损益」' \
  '- 研究阶段支出 24,000.00 万元，均满足资本化条件「本期研究阶段支出 240,000,000.00 元，全部计入当期损益」' \
  '原句没写资本化条件却自标'; then
  run '原句没写满足资本化条件却自标 → 只红 RD-NOSELF' 1 "$WORK/e-cond.md" 'RD-NOSELF'
fi

# ⑧ 三个数被拼成等式（自行轧差）→ 该只红在 RD-NOSELF
#    注入点选资本化金额那一行的值位：它自己那一句，不带别道的料
if mutate "$GOOD" "$WORK/e-jiazha.md" \
  '- 资本化金额 8,000.00 万元' \
  '- 资本化金额 即研发投入合计与费用化金额之差' '自行轧差'; then
  run '研发投入与资本化费用化拼成等式 → 只红 RD-NOSELF' 1 "$WORK/e-jiazha.md" 'RD-NOSELF'
fi

# ⑨ 自算差额缺分子来源 → 该只红在 RD-NOSELF
if mutate "$GOOD" "$WORK/e-nobasis.md" \
  '- 资本化率 25.00%〔自算〕分子＝本期资本化研发投入 80,000,000.00 元 [S1]｜分母＝本期研发投入合计 320,000,000.00 元 [S1]' \
  '- 资本化率 25.00%〔自算〕分母＝本期研发投入合计 320,000,000.00 元 [S1]' \
  '自算缺分子'; then
  run '比例自算缺分子来源 → 只红 RD-NOSELF' 1 "$WORK/e-nobasis.md" 'RD-NOSELF'
fi

# ⑩ 「未取到」写成「无此项」→ 该只红在 RD-GAP（正文那条未取到就没人点名了，两向各报一条）
if mutate "$GOOD" "$WORK/e-gap.md" \
  '- 未取到：资本化起始时点' '- 未取到：无此项' '「无此项」搪塞'; then
  run '第六节写「无此项」→ 只红 RD-GAP' 1 "$WORK/e-gap.md" 'RD-GAP'
fi

# ⑪ 正文写了未取到、第六节不点名 → 该只红在 RD-GAP
if mutate "$GOOD" "$WORK/e-gap2.md" \
  '- 未取到：条件判断依据
' '' '正文缺口未点名'; then
  run '正文未取到而第六节不点名 → 只红 RD-GAP' 1 "$WORK/e-gap2.md" 'RD-GAP'
fi

# ⑫ 定式禁词 → 该只红在 RD-LINE
#    注入点选第六节的口径行：那一段本来就不要求三元组，插红线句不会连带 RD-QUOTE。
if mutate "$GOOD" "$WORK/e-fixed.md" \
  '- 口径：研究阶段与开发阶段的划分、各项目所处阶段一律照抄附注原句，不由本件按项目进度推断。' \
  '- 口径：该项目是公司的核心竞争力，应当全部费用化。' '定式禁词自裁'; then
  run '「核心竞争力／应当全部费用化」落在非待人工行 → 只红 RD-LINE' 1 "$WORK/e-fixed.md" 'RD-LINE'
fi

# ⑬ 对照样：[待人工] 整句成立 → 须零发条（判断位豁免只豁免它自己那一句）
if mutate "$GOOD" "$WORK/c-human.md" \
  '## 口径与未取到' '- 该研发项目值不值钱 [待人工]
- 是否建议继续资本化 [待人工]
- 对利润的影响 [待人工]

## 口径与未取到' '对照·[待人工] 整句'; then
  run '对照·[待人工] 整句成立不误伤（零发条）' 0 "$WORK/c-human.md" ''
fi

# ⑭ 对照样：引文里照抄的「无风险」不是本件断言 → 须零发条
if mutate "$GOOD" "$WORK/c-quoted.md" \
  '「无形资产采用直线法按预计使用寿命摊销」' \
  '「公司称该项目无风险，研发成果可期」' '对照·引文不算本件断言'; then
  run '对照·引文里的「无风险」不误伤（零发条）' 0 "$WORK/c-quoted.md" ''
fi

# ⑮ 对照样：未取到行的项名里带「资本化条件」不算自推 → 须零发条
#     正文与第六节的项名要一起改，只改一处会断掉两向对账
if mutate "$GOOD" "$WORK/c-itemname.md" \
  '- 本期满足条件的项目数 未取到：附注未披露本期满足资本化条件的项目数量' \
  '- 本期满足资本化条件的项目数 未取到：附注未披露本期满足资本化条件的项目数量' '对照·项名带词族'; then
  mutate "$WORK/c-itemname.md" "$WORK/c-itemname2.md" \
    '- 未取到：本期满足条件的项目数' '- 未取到：本期满足资本化条件的项目数' '对照·项名带词族（第六节）' && \
  run '对照·未取到行的项名带词族不误伤（零发条）' 0 "$WORK/c-itemname2.md" ''
fi

# ⑯ 对照样：口径行里叙述「写未取到」不是缺口登记 → 须零发条
#     （判缺口只认带冒号的登记形，叙述形不许触发 RD-GAP）
if mutate "$GOOD" "$WORK/c-prose.md" \
  '- 口径：资本化率披露没给的，本件算出来才标〔自算〕，并在同一行给出分子与分母各自的来源。' \
  '- 口径：资本化率披露没给的写未取到，算出来的才标〔自算〕，并在同一行给出分子与分母各自的来源。' \
  '对照·口径行叙述未取到'; then
  run '对照·口径行叙述「写未取到」不误伤（零发条）' 0 "$WORK/c-prose.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
