#!/usr/bin/env bash
# run_fixtures.sh — 前期会计差错更正稿的离线样例 runner
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
#   * 判「节在不在」的那道（EC-STRUCT）认的是**多出同名节**与**不认识节名**，不是「节标题改名」：
#     改标题会让整节变 stray、节内发现行一并丢，连带别的注入测不到——所以这支注入插的是
#     重复节标题，正文一条不丢。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_correction.py"
GOOD="$FIX/good-correction.md"
BAD="$FIX/bad-correction.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-accounting-error-correction-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`  EC-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(EC-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
run '好样 good-correction（零发条）' 0 "$GOOD" ''
run '坏样 bad-correction（EC-STRUCT·QUOTE·NOSELF·GAP·LINE 五道齐）' 1 "$BAD" \
  'EC-GAP,EC-LINE,EC-NOSELF,EC-QUOTE,EC-STRUCT'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 多出一节同名标题 → 该只红在 EC-STRUCT
#    不去改节标题名：改名会让整节变 stray、节内发现行一并丢，连带下面几支注入测不到。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '## 受影响的报表科目与各期重述金额' '## 更正方法与判据

## 受影响的报表科目与各期重述金额' '多出同名节'; then
  run '多出一节同名「更正方法与判据」→ 只红 EC-STRUCT' 1 "$WORK/e-struct.md" 'EC-STRUCT'
fi

# ② 发现行丢原句与锚 → 该只红在 EC-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「调减 2024 年度营业收入 12,000,000.00 元」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]' \
  '12,000,000.00 元 [S1]' '数字行丢原句与锚'; then
  run '重述行丢了原句与锚 → 只红 EC-QUOTE' 1 "$WORK/e-quote.md" 'EC-QUOTE'
fi

# ③ 锚标签在而锚值为空 → 该只红在 EC-QUOTE
if mutate "$GOOD" "$WORK/e-anchor.md" \
  '〔锚：差错更正公告·第 3 页·二、更正方法〕' '〔锚：〕' '锚值为空'; then
  run '锚标签在而锚值为空 → 只红 EC-QUOTE' 1 "$WORK/e-anchor.md" 'EC-QUOTE'
fi

# ④ 重述比例自算只给分子没给分母 → 该只红在 EC-NOSELF
if mutate "$GOOD" "$WORK/e-self.md" \
  '｜分母＝2024 年度原披露营业收入 400,000,000.00 元 [S1]' \
  '' '自算缺分母'; then
  run '自算只给分子不给分母 → 只红 EC-NOSELF' 1 "$WORK/e-self.md" 'EC-NOSELF'
fi

# ⑤ 自算出来的比例冒充披露值 → 该只红在 EC-NOSELF
#    （原句里没有 3.00%，去掉自算标记后没有人替这个数交代来路）
if mutate "$GOOD" "$WORK/e-bare.md" \
  '- 重述金额较原披露数变动 3.00%〔自算〕累积影响取附注「上述差错累积影响数为 3,200,000.00 元」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]｜分子＝2024 年度营业收入调减 12,000,000.00 元 [S1]｜分母＝2024 年度原披露营业收入 400,000,000.00 元 [S1]' \
  '- 重述金额较原披露数变动 3.00%「调减 2024 年度营业收入 12,000,000.00 元」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]' \
  '自算充披露值'; then
  run '自算出来的比例冒充披露值 → 只红 EC-NOSELF' 1 "$WORK/e-bare.md" 'EC-NOSELF'
fi

# ⑥ 原句没写更正方法却自标「追溯重述法」→ 该只红在 EC-NOSELF（更正方法只认原句）
if mutate "$GOOD" "$WORK/e-method.md" \
  '- 更正方法 追溯重述法「本公司采用追溯重述法对该项前期差错进行更正」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]' \
  '- 更正方法 追溯重述法「该差错影响金额较大，属于重大前期差错」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]' \
  '原句没写更正方法却自标'; then
  run '原句没写更正方法却自标追溯重述法 → 只红 EC-NOSELF' 1 "$WORK/e-method.md" 'EC-NOSELF'
fi

# ⑦ 原句没写「会计政策变更」却自标三类界线 → 该只红在 EC-NOSELF（三类界线只认原句）
if mutate "$GOOD" "$WORK/e-change.md" \
  '- 三类界线 本次属前期差错更正「本公司认为该事项属于前期差错更正，不属于会计政策变更，也不属于会计估计变更」〔锚：2025 年年报·第 122 页·附注二·前期差错更正〕[S1]' \
  '- 三类界线 本次属前期差错更正且不属于会计政策变更「本公司认为该事项属于前期差错更正，不属于会计估计变更」〔锚：2025 年年报·第 122 页·附注二·前期差错更正〕[S1]' \
  '原句没写政策变更却自标'; then
  run '原句没写「会计政策变更」却自标 → 只红 EC-NOSELF' 1 "$WORK/e-change.md" 'EC-NOSELF'
fi

# ⑧ 重述金额自算缺累积影响出处 → 该只红在 EC-NOSELF
if mutate "$GOOD" "$WORK/e-restate.md" \
  '累积影响取附注「上述差错累积影响数为 3,200,000.00 元」〔锚：2025 年年报·第 120 页·附注二·前期差错更正〕[S1]｜' \
  '' '重述自算缺累积影响出处'; then
  run '重述金额自算缺「累积影响取哪一句」→ 只红 EC-NOSELF' 1 "$WORK/e-restate.md" 'EC-NOSELF'
fi

# ⑨ 「未取到」写成「不适用」→ 该只红在 EC-GAP（正文那条未取到就没人点名了，两向各报一条）
if mutate "$GOOD" "$WORK/e-gap.md" \
  '- 未取到：政策变更判据' '- 未取到：不适用' '「不适用」搪塞'; then
  run '第六节写「不适用」→ 只红 EC-GAP' 1 "$WORK/e-gap.md" 'EC-GAP'
fi

# ⑩ 定式禁词 → 该只红在 EC-LINE
#    注入点选第六节的口径行：那一段本来就不要求三元组，插红线句不会连带 EC-QUOTE。
if mutate "$GOOD" "$WORK/e-fixed.md" \
  '- 口径：差错性质与更正方法一律照抄更正公告与附注原句，不由本件按金额大小或科目类型推断。' \
  '- 口径：本次更正不存在舞弊，更正后报表可信。' '定式禁词自裁'; then
  run '「不存在舞弊／更正后报表可信」落在非待人工行 → 只红 EC-LINE' 1 "$WORK/e-fixed.md" 'EC-LINE'
fi

# ⑪ 会计政策变更＝前期差错 → 该只红在 EC-LINE
if mutate "$GOOD" "$WORK/e-mix.md" \
  '- 口径：会计政策变更、会计估计变更、前期差错更正三者是不同的东西，界线只照抄披露自己的表述。' \
  '- 口径：会计政策变更视同前期差错更正，两者按同一方法处理。' '三类变更混写'; then
  run '会计政策变更视同前期差错更正 → 只红 EC-LINE' 1 "$WORK/e-mix.md" 'EC-LINE'
fi

# ⑫ 对照样：[待人工] 整句成立 → 须零发条（判断位豁免只豁免它自己那一句）
if mutate "$GOOD" "$WORK/c-human.md" \
  '## 口径与未取到' '- 差错是否属于舞弊 [待人工]
- 差错是否为管理层故意 [待人工]
- 更正后报表是否可信 [待人工]

## 口径与未取到' '对照·[待人工] 整句'; then
  run '对照·[待人工] 整句成立不误伤（零发条）' 0 "$WORK/c-human.md" ''
fi

# ⑬ 对照样：引文里照抄的「舞弊」不是本件断言 → 须零发条
if mutate "$GOOD" "$WORK/c-quoted.md" \
  '「本财务报表已对 2024 年度比较数据进行了重述」' \
  '「公司否认存在舞弊，未发生人为调节」' '对照·引文不算本件断言'; then
  run '对照·引文里的「舞弊」不误伤（零发条）' 0 "$WORK/c-quoted.md" ''
fi

# ⑭ 对照样：重述金额自算把累积影响出处与分子分母都写全 → 须零发条
if mutate "$GOOD" "$WORK/c-restate.md" \
  '- 期初未分配利润 调减 320.00 万元「调减 2024 年 1 月 1 日未分配利润 3,200,000.00 元」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]' \
  '- 期初未分配利润 调减 320.00 万元〔自算〕累积影响取附注「调减 2024 年 1 月 1 日未分配利润 3,200,000.00 元」〔锚：2025 年年报·第 121 页·附注二·前期差错更正〕[S1]｜分子＝调减金额 3,200,000.00 元 [S1]｜分母＝原披露期初未分配利润 60,000,000.00 元 [S1]' \
  '对照·重述自算写全'; then
  run '对照·重述金额自算出处与分子分母写全不误伤（零发条）' 0 "$WORK/c-restate.md" ''
fi

# ⑮ 对照样：未取到行的项名里带「会计政策变更」不算自推 → 须零发条
if mutate "$GOOD" "$WORK/c-itemname.md" \
  '- 政策变更判据 未取到：附注未列示会计政策变更的判据' \
  '- 会计政策变更判据 未取到：附注未列示会计政策变更的判据' '对照·项名带词族'; then
  # 正文与第六节的项名要一起改，只改一处会断掉两向对账
  mutate "$WORK/c-itemname.md" "$WORK/c-itemname2.md" \
    '- 未取到：政策变更判据' '- 未取到：会计政策变更判据' '对照·项名带词族（第六节）' && \
  run '对照·未取到行的项名带词族不误伤（零发条）' 0 "$WORK/c-itemname2.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
