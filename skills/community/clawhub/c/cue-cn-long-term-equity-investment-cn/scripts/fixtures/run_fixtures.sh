#!/usr/bin/env bash
# run_fixtures.sh — 长期股权投资稿的离线样例 runner
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
#   * 判「节在不在」的那道（LE-STRUCT）认的是**多出同名节**与**不认识节名**，不是「节标题改名」：
#     改标题会让整节变 stray、节内发现行一并丢，连带别的注入测不到——所以这支注入插的是
#     重复节标题，正文一条不丢。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_long_term_equity.py"
GOOD="$FIX/good-long-term-equity.md"
BAD="$FIX/bad-long-term-equity.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-long-term-equity-investment-cn.XXXXXX")" || {
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
# 失败（片段不在源件里、或片段不唯一、或替换后与源件同字节）＝ 取值域故障，不计入「不合」。
mutate() {
  local src="$1" dst="$2" old="$3" new="$4" tag="$5"
  if ! python3 -B - "$src" "$dst" "$old" "$new" "$tag" <<'PY'
import sys
from pathlib import Path
src, dst, old, new, tag = sys.argv[1:6]
t = Path(src).read_text(encoding='utf-8')
n = t.count(old)
if n != 1:
    sys.exit('%s：注入点在源件里出现 %d 次（应恰好 1 次）' % (tag, n))
out = t.replace(old, new)
if out == t:
    sys.exit('%s：替换后与源件同字节' % tag)
Path(dst).write_text(out, encoding='utf-8')
PY
  then
    echo "  不可判 $tag：注入没落地（片段对不上夹具，不读成「机检漏判」）"
    unk=$((unk + 1)); return 1
  fi
  return 0
}

# 跑一枚：run <标签> <期望退码> <文件> <期望码集（空＝不发码）|*＝不核码集>
# 码集从机检自己的输出里取（`  LE-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(LE-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
run '好样 good-long-term-equity（零发条）' 0 "$GOOD" ''
run '坏样 bad-long-term-equity（LE-STRUCT·QUOTE·NOSELF·GAP·LINE 五道齐）' 1 "$BAD" \
  'LE-GAP,LE-LINE,LE-NOSELF,LE-QUOTE,LE-STRUCT'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 多出一节同名标题 → 该只红在 LE-STRUCT
#    不去改节标题名：改名会让整节变 stray、节内发现行一并丢，连带下面几支注入测不到。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '## 核算方法与分类' '## 按被投资单位列的明细

## 核算方法与分类' '多出同名节'; then
  run '多出一节同名「按被投资单位列的明细」→ 只红 LE-STRUCT' 1 "$WORK/e-struct.md" 'LE-STRUCT'
fi

# ② 发现行丢原句与锚 → 该只红在 LE-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「乙公司期初余额 20,000,000.00 元」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕[S1]' \
  '20,000,000.00 元 [S1]' '数字行丢原句与锚'; then
  run '期初余额行丢了原句与锚 → 只红 LE-QUOTE' 1 "$WORK/e-quote.md" 'LE-QUOTE'
fi

# ③ 锚标签在而锚值为空 → 该只红在 LE-QUOTE
#    注入点带上引文，才在源件里唯一：同一个页锚在正文出现多次，只给锚块会判「出现 N 次」。
if mutate "$GOOD" "$WORK/e-anchor.md" \
  '「表决权比例 30.00%」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕' \
  '「表决权比例 30.00%」〔锚：〕' '锚值为空'; then
  run '锚标签在而锚值为空 → 只红 LE-QUOTE' 1 "$WORK/e-anchor.md" 'LE-QUOTE'
fi

# ④ 引用未登记编号 → 该只红在 LE-QUOTE
if mutate "$GOOD" "$WORK/e-undefined.md" \
  '「乙公司期末余额 32,000,000.00 元」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕[S1]' \
  '「乙公司期末余额 32,000,000.00 元」〔锚：2025 年年报·第 152 页·附注七·长期股权投资〕[S8]' \
  '引用未登记编号'; then
  run '引用 [S8] 而来源节没登记 → 只红 LE-QUOTE' 1 "$WORK/e-undefined.md" 'LE-QUOTE'
fi

# ⑤ 比例自算只给分子没给分母 → 该只红在 LE-NOSELF
if mutate "$GOOD" "$WORK/e-self.md" \
  '｜分母＝本期确认投资收益 12,000,000.00 元 [S1]' \
  '' '自算缺分母'; then
  run '自算只给分子不给分母 → 只红 LE-NOSELF' 1 "$WORK/e-self.md" 'LE-NOSELF'
fi

# ⑥ 自算出来的比例冒充披露值 → 该只红在 LE-NOSELF
#    （原句里没有 50.00%，去掉自算标记后没有人替这个数交代来路）
if mutate "$GOOD" "$WORK/e-bare.md" \
  '- 现金分红占本期确认投资收益比 50.00%〔自算〕分子＝本期收到现金分红 6,000,000.00 元 [S1]｜分母＝本期确认投资收益 12,000,000.00 元 [S1]' \
  '- 现金分红占本期确认投资收益比 50.00%「本期收到现金分红 6,000,000.00 元」〔锚：2025 年年报·第 154 页·附注七·长期股权投资〕[S1]' \
  '自算充披露值'; then
  run '自算出来的比例冒充披露值 → 只红 LE-NOSELF' 1 "$WORK/e-bare.md" 'LE-NOSELF'
fi

# ⑦ 原句没写权益法却按持股比例自标 → 该只红在 LE-NOSELF
#    这支是本件的专项反证：20%／50% 是常识门槛，但用哪种核算法只有披露知道。
#    注入点保留原句（换掉内容，让「权益法」成为原句之外唯一的词族）。
if mutate "$GOOD" "$WORK/e-method.md" \
  '- 对乙公司的核算方法 权益法「本公司对乙公司具有重大影响，采用权益法核算」' \
  '- 对乙公司的核算方法 持股 30.00%，故按权益法核算「本公司持有乙公司 30.00% 的股权」' \
  '按持股比例自推核算法'; then
  run '原句没写权益法却按持股比例自标 → 只红 LE-NOSELF' 1 "$WORK/e-method.md" 'LE-NOSELF'
fi

# ⑧ 原句没写「控制」却自标成本法 → 该只红在 LE-NOSELF
#    注入点选划分那一行的值位：原句保留，值位加一句原句之外的分类判断。
if mutate "$GOOD" "$WORK/e-class.md" \
  '- 合营企业与联营企业的划分 照抄附注表述「合营企业是指合营方仅对该安排的净资产享有权利的合营安排，联营企业是指投资方对被投资单位具有重大影响的权益性投资」' \
  '- 合营企业与联营企业的划分 该单位受本公司控制「合营企业是指合营方仅对该安排的净资产享有权利的合营安排，联营企业是指投资方对被投资单位具有重大影响的权益性投资」' \
  '原句没写控制却自标'; then
  run '原句没写「控制」却自标 → 只红 LE-NOSELF' 1 "$WORK/e-class.md" 'LE-NOSELF'
fi

# ⑨ 两个数被拼成等式（自行轧差）→ 该只红在 LE-NOSELF
#    注入点选「本期确认的投资收益」那一行的值位：它自己那一句，不带别道的料。
if mutate "$GOOD" "$WORK/e-jiazha.md" \
  '- 本期确认的投资收益 12,000,000.00 元' \
  '- 本期确认的投资收益 即本期收到现金分红与上期余额之差' '自行轧差'; then
  run '投资收益与现金分红拼成等式 → 只红 LE-NOSELF' 1 "$WORK/e-jiazha.md" 'LE-NOSELF'
fi

# ⑩ 三个数被拼成等式（净利润／投资收益／未实现损益）→ 该只红在 LE-NOSELF
if mutate "$GOOD" "$WORK/e-jiazha2.md" \
  '- 内部交易未实现损益抵消金额 1,500,000.00 元' \
  '- 内部交易未实现损益抵消金额 即被投资单位净利润与按比例确认投资收益之差' '三数轧差'; then
  run '净利润与投资收益拼成抵消额 → 只红 LE-NOSELF' 1 "$WORK/e-jiazha2.md" 'LE-NOSELF'
fi

# ⑪ 「未取到」写成「无此项」→ 该只红在 LE-GAP（正文那条未取到就没人点名了，两向各报一条）
if mutate "$GOOD" "$WORK/e-gap.md" \
  '- 未取到：各被投资单位的分类依据' '- 未取到：无此项' '「无此项」搪塞'; then
  run '第六节写「无此项」→ 只红 LE-GAP' 1 "$WORK/e-gap.md" 'LE-GAP'
fi

# ⑫ 正文写了未取到、第六节不点名 → 该只红在 LE-GAP
if mutate "$GOOD" "$WORK/e-gap2.md" \
  '- 未取到：对赌或业绩承诺的安排
' '' '正文缺口未点名'; then
  run '正文未取到而第六节不点名 → 只红 LE-GAP' 1 "$WORK/e-gap2.md" 'LE-GAP'
fi

# ⑬ 定式禁词 → 该只红在 LE-LINE
#    注入点选第六节的口径行：那一段本来就不要求三元组，插红线句不会连带 LE-QUOTE。
if mutate "$GOOD" "$WORK/e-fixed.md" \
  '- 口径：比例披露没给的，本件算出来才标〔自算〕，并在同一行给出分子与分母各自的来源。' \
  '- 口径：该投资具有投资价值，预计投资收益将增厚利润。' '定式禁词自裁'; then
  run '「具有投资价值／增厚利润」落在非待人工行 → 只红 LE-LINE' 1 "$WORK/e-fixed.md" 'LE-LINE'
fi

# ⑭ 越界件 → 该只红在 LE-STRUCT（边界列在第五节之外的行里）
if mutate "$GOOD" "$WORK/e-scope.md" \
  '- 减值准备期末余额 2,000,000.00 元「长期股权投资减值准备期末余额 2,000,000.00 元」〔锚：2025 年年报·第 154 页·附注七·长期股权投资〕[S1]' \
  '- 减值准备期末余额 2,000,000.00 元，减值测试的结论见另一件「长期股权投资减值准备期末余额 2,000,000.00 元」〔锚：2025 年年报·第 154 页·附注七·长期股权投资〕[S1]' \
  '越界到减值判定'; then
  run '正文越界到减值测试结论 → 只红 LE-STRUCT' 1 "$WORK/e-scope.md" 'LE-STRUCT'
fi

# ⑮ 对照样：[待人工] 整句成立 → 须零发条（判断位豁免只豁免它自己那一句）
if mutate "$GOOD" "$WORK/c-human.md" \
  '## 口径与未取到' '- 被投资单位值不值钱 [待人工]
- 本金能否收回 [待人工]
- 对 EPS 的影响 [待人工]

## 口径与未取到' '对照·[待人工] 整句'; then
  run '对照·[待人工] 整句成立不误伤（零发条）' 0 "$WORK/c-human.md" ''
fi

# ⑯ 对照样：引文里照抄的「无风险／业绩承诺可实现」不是本件断言 → 须零发条
#    注入点选减值准备那一行的引文：该行值位不含核算方法词族，换掉引文不会连带 LE-NOSELF。
if mutate "$GOOD" "$WORK/c-quoted.md" \
  '「长期股权投资减值准备期末余额 2,000,000.00 元」' \
  '「附注称该单位无风险，业绩承诺可实现」' '对照·引文不算本件断言'; then
  run '对照·引文里的「无风险」不误伤（零发条）' 0 "$WORK/c-quoted.md" ''
fi

# ⑰ 对照样：未取到行的项名里带「合营企业／联营企业」不算自推 → 须零发条
#     正文与第六节的项名要一起改，只改一处会断掉两向对账
if mutate "$GOOD" "$WORK/c-itemname.md" \
  '- 各被投资单位的分类依据 未取到：附注未说明划分为合营企业或联营企业的具体依据' \
  '- 合营企业与联营企业的分类依据 未取到：附注未说明划分为合营企业或联营企业的具体依据' '对照·项名带词族'; then
  mutate "$WORK/c-itemname.md" "$WORK/c-itemname2.md" \
    '- 未取到：各被投资单位的分类依据' '- 未取到：合营企业与联营企业的分类依据' '对照·项名带词族（第六节）' && \
  run '对照·未取到行的项名带词族不误伤（零发条）' 0 "$WORK/c-itemname2.md" ''
fi

# ⑱ 对照样：持股比例照抄披露原句 → 须零发条
#     （比例判据只要求「原句里也有这个数」，不要求它必须是自算）
if mutate "$GOOD" "$WORK/c-pct.md" \
  '- 乙公司持股比例 30.00%「本公司持有乙公司 30.00% 的股权」' \
  '- 乙公司持股比例 30.00%「本公司持有乙公司 30.00% 的股权，表决权比例相同」' '对照·比例照抄原句'; then
  run '对照·持股比例照抄原句不误伤（零发条）' 0 "$WORK/c-pct.md" ''
fi

# ⑲ 对照样：口径行里叙述「写未取到」不是缺口登记 → 须零发条
#     （判缺口只认带冒号的登记形，叙述形不许触发 LE-GAP）
if mutate "$GOOD" "$WORK/c-prose.md" \
  '- 口径：本期确认的投资收益与本期收到的现金分红是两个数，差额及其解释只认披露原句，没披露就写未取到。' \
  '- 口径：本期确认的投资收益与本期收到的现金分红是两个数，差额未取到就写未取到，不自己相减。' \
  '对照·口径行叙述未取到'; then
  run '对照·口径行叙述「写未取到」不误伤（零发条）' 0 "$WORK/c-prose.md" ''
fi

# ⑳ 对照样：〔自算〕行把两个数相减并交代了分子分母 → 须零发条
#     （轧差判据的例外形：自己算的差额标明来路就不是「替披露做减法」）
#     正文与第六节两处一起改：只把正文那条未取到换成自算行，第六节还在点名它，
#     两向对账就断了（假 LE-GAP）——测出来的红不是轧差那道。
if mutate "$GOOD" "$WORK/c-selfdiff.md" \
  '- 两者差额及其披露解释 未取到：附注未披露投资收益与现金分红差额的解释' \
  '- 两者差额〔自算〕分子＝本期确认投资收益 12,000,000.00 元 [S1]｜分母＝本期收到现金分红 6,000,000.00 元 [S1]' \
  '对照·自算差额交代来路'; then
  mutate "$WORK/c-selfdiff.md" "$WORK/c-selfdiff2.md" \
    '- 未取到：两者差额及其披露解释
' '' '对照·自算差额（第六节同步）' && \
  run '对照·〔自算〕差额交代分子分母不误伤（零发条）' 0 "$WORK/c-selfdiff2.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
