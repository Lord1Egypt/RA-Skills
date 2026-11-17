#!/usr/bin/env bash
# run_fixtures.sh — 金融工具风险敞口登记稿的离线样例 runner
#
# 三档：① 机检自测 → ② 好样（--demo 产物自过机检）→ ③ 坏样（在好样上只破一处，须点名）。
# 零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp} 下自建目录，跑完即删。
# 退码：0 三档全合期望；1 有不合（逐档点名，附真实退码与真实码集）；
#       3 取值域故障（脚本取不到、或某支注入没落地——不读成「零违例」）。
#
# 本包不带夹具文件：好样由机检自己的 --demo 现出，坏样在好样临时副本上注入。
# 所以档② 顺带证了 --demo 与机检判据同源（同一份文本，一支零发条、一支发条）。
#
# 为什么每支注入都先断言「注入真的落地了」：注入字符串对不上好样时，替换会静默产出原文，
# 于是「该红没红」会被读成「机检漏判」，实际是尺子没被放上去。所以注入后一律数片段出现次数，
# 不一致即计取值域故障（unk），不并入「不合」。
#
# **期望退码不写死**：好样与自测那两档从自测末行的「不可判=N」现算（N>0 ⇒ 3，N=0 ⇒ 0）。
# 写死退码的形状是「今天对、判据补齐后就错」——判据一补齐，runner 从该绿变常红，
# 逼下一个人去改断言而不是改判据。这里让它自己跟着走。
# 坏样那几档期望恒为 1（有发条），反证档期望恒为 0（零发条）：这两条与「判据是否落字」无关。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_financial_instruments_risk.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-financial-instruments-risk-cn.XXXXXX")" || {
  echo "3 取值域故障：临时目录没建成（TMPDIR=${TMPDIR:-未设} 是否存在、可写？）"; exit 3; }
[ -d "$WORK" ] || { echo "3 取值域故障：临时目录不存在"; exit 3; }
trap 'rm -rf "$WORK"' EXIT

[ -f "$CK" ] || { echo "3 取值域故障：取不到 $CK（不读成「样例全过」）"; exit 3; }

bad=0
unk=0
tiers=0

# 一支注入：mutate <源件> <目标件> <原文片段> <替换片段> <替换后原文片段残留次数> <标签>
# want 数的是**旧片段**在替换后的残留次数：换掉一处唯一片段 ⇒ 0；插入型（旧片段留在原处）⇒ 1。
# 失败（片段不在源件里、替换后与源件同字节、或残留次数不符）＝取值域故障，不计入「不合」。
mutate() {
  local src="$1" dst="$2" old="$3" new="$4" want="$5" tag="$6"
  if ! python3 -B - "$src" "$dst" "$old" "$new" "$want" <<'PY'
import sys
from pathlib import Path
src, dst, old, new, want = sys.argv[1:6]
t = Path(src).read_text(encoding='utf-8')
if old not in t:
    sys.exit('注入点不在源件里')
out = t.replace(old, new, 1)
if out == t:
    sys.exit('替换后与源件同字节')
got = out.count(old)
if got != int(want):
    sys.exit('替换后片段次数 %d ≠ 期望 %s' % (got, want))
Path(dst).write_text(out, encoding='utf-8')
PY
  then
    echo "  不可判 $tag：注入没落地（片段对不上好样，不读成「机检漏判」）"
    unk=$((unk + 1)); return 1
  fi
  return 0
}

# 跑一枚：run <标签> <期望退码> <文件> <期望码集（空＝不发码）|*＝不核码集>
# 码集从机检自己的输出里取（`FR-XXX L12 …` 的行首码），不另跑一份统计。
# 注意：码里带连字符（FR-QUOTE／FR-BUCKET／FR-SENS／FR-LINE），正则须写成 `FR-[A-Z-]*`——
# 写成 `FR-[A-Z]*` 会永远取不到 FR-QUOTE 这类，那条断言就成了永远为真的空断言。
# 机检的读数行与「—— 机检：…」汇总行**没有行号**，正则要求 `L数字` 才不会把它们当成发条。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(FR-[A-Z-]*\) L[0-9].*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes:-*}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样零发条、逐枚坏样各只发自己那道码、未落字各计一档不可判）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
last="$(printf '%s\n' "$out" | tail -1)"
printf '%s\n' "$last"
WANT_UNJUDGED="$(printf '%s\n' "$last" | sed -n 's/.*不可判=\([0-9]\+\).*/\1/p')"
if [ -z "$WANT_UNJUDGED" ]; then
  echo '  不可判 → 自测末行取不到「不可判=N」（取值域故障，不读成「五道全过」）'
  unk=$((unk + 1)); WANT_UNJUDGED=3
fi
if [ "$WANT_UNJUDGED" -eq 0 ]; then WANT_RC=0; else WANT_RC=3; fi
echo "  实发退码=$rc｜期望=$WANT_RC（由末行 不可判=$WANT_UNJUDGED 现算）"
if [ "$rc" -eq "$WANT_RC" ] && printf '%s\n' "$last" | grep -q '不合=0'; then
  echo '  → 合'
else
  echo '  → 不合'; bad=$((bad + 1))
fi

echo '档② 好样：--demo 产物自过机检（零发条；退码随未落字判据走）'
tiers=$((tiers + 1))
GOOD="$WORK/good-fr.md"
if python3 -B "$CK" --demo > "$GOOD" 2>"$WORK/demo.err" && [ -s "$GOOD" ]; then
  echo "  ok   --demo 产出 $(wc -c < "$GOOD" | tr -d ' ') 字节"
  run "好样 demo 稿（零发条／不可判 $WANT_UNJUDGED 道）" "$WANT_RC" "$GOOD" ''
else
  echo "  不可判 --demo 没产出文本（取值域故障，不读成「好样零发条」）"
  sed 's/^/      /' "$WORK/demo.err" 2>/dev/null
  unk=$((unk + 1))
fi

echo '档③ 坏样：在好样临时副本上只破一处，须各只发自己那道码'
tiers=$((tiers + 1))

# 注入一：删掉头部第三件自标。只该红 FR-STRUCT（形制三件自标逐字在位）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct-mark.md" \
  'AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议' \
  'AI 整理初稿 ｜ 请回原文核对' 0 '删掉头部第三件自标' ; then
  run '头部缺「不构成投资建议」→ 只红 FR-STRUCT' 1 "$WORK/bad-struct-mark.md" 'FR-STRUCT'
fi

# 注入二：拆掉「风险敞口概况」里某数字行的「」原句与〔锚〕，只留 [S1]。
# 只该红 FR-QUOTE。**不选流动性风险节的那几行**：那些行的金额会进 FR-BUCKET 的求和，
# 动它们会让一支注入同时红两道，钉不住「只红一道」。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '182,400.00 万元「本集团金融资产账面余额合计为人民币 182,400.00 万元」〔锚：2025 年年报·第 232 页·金融工具及风险〕[S1]' \
  '182,400.00 万元 [S1]' 0 '拆掉原句与锚只留 [S1]' ; then
  run '拆掉原句与锚只留 [S1] → 只红 FR-QUOTE' 1 "$WORK/bad-quote.md" 'FR-QUOTE'
fi

# 注入三：把流动性风险节的合计改大，让分档和对不上。只该红 FR-BUCKET。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-bucket-sum.md" \
  '流动性风险合计〔口径：合同未折现现金流〕125,400.00 万元' \
  '流动性风险合计〔口径：合同未折现现金流〕130,000.00 万元' 0 '合计改大 4,600' ; then
  run '合计 125,400→130,000（分档和对不上）→ 只红 FR-BUCKET' 1 "$WORK/bad-bucket-sum.md" 'FR-BUCKET'
fi

# 注入四：把某个档名改成认不出的样子。只该红 FR-BUCKET（档名认不出）。
# 注意换的只是档名，金额不动 ⇒ 求和仍对得上，不会顺带红求和那一条。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-bucket-name.md" \
  '- 1 年以内〔口径：合同未折现现金流〕71,800.00 万元' \
  '- 一年以内〔口径：合同未折现现金流〕71,800.00 万元' 0 '档名写成「一年以内」' ; then
  run '档名「1 年以内」→「一年以内」→ 只红 FR-BUCKET' 1 "$WORK/bad-bucket-name.md" 'FR-BUCKET'
fi

# 注入五：把利率敏感性的影响金额从 240 改成 300（48,000×50/10000=240）。只该红 FR-SENS。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-sens.md" \
  '敞口 48,000.00 万元 变动 50 个基点 影响 240.00 万元' \
  '敞口 48,000.00 万元 变动 50 个基点 影响 300.00 万元' 0 '影响金额改 300' ; then
  run '影响 240→300（算式对不上）→ 只红 FR-SENS' 1 "$WORK/bad-sens.md" 'FR-SENS'
fi

# 注入六：把敞口写成 0。应发「此项无从重算」而**不是崩掉**——这一档同时证了不除零。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-sens-zero.md" \
  '敞口 48,000.00 万元 变动 50 个基点 影响 240.00 万元' \
  '敞口 0.00 万元 变动 50 个基点 影响 240.00 万元' 0 '敞口写 0' ; then
  run '敞口写 0.00 → 发「无从重算」且不崩 → 只红 FR-SENS' 1 "$WORK/bad-sens-zero.md" 'FR-SENS'
fi

# 注入七：插一条带完整三元组的红线行（评级／目标价类）。只该红 FR-LINE。
# 插入型：新片段＝红线行 ＋ 原行，原行留着 ⇒ 旧片段残留 1。
# 锚在原行（不是节标题"## 市场风险—利率"）：只锚节标题的替换会把内容插进**上一节**，
# 红线行就落进了不该落的地方，测到的就不是 FR-LINE 判整行了。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line-rating.md" \
  '- 浮动利率借款〔口径：本期末〕48,000.00 万元' \
  '- 投资建议〔待人工〕我们给予公司增持评级，目标价 12.00 元「我们给予公司增持评级，目标价 12.00 元」〔锚：2025 年年报·第 234 页·利率风险〕[S1]
- 浮动利率借款〔口径：本期末〕48,000.00 万元' 1 '插一条评级红线行' ; then
  run '插评级／目标价行 → 只红 FR-LINE' 1 "$WORK/bad-line-rating.md" 'FR-LINE'
fi

# 注入八：整节删掉「流动性风险」。应**双红** FR-STRUCT（缺节）＋ FR-LINE（结构判据），
# 而 FR-BUCKET **不该响**（缺一侧即跳过，节缺不归它管）。这一档钉住「各判各的」。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-nosec-liq.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
i = t.index('## 流动性风险')
j = t.index('## 市场风险—利率')
out = t[:i] + t[j:]
if out == t:
    sys.exit('注入点不在好样里')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '整节删掉流动性风险 → 双红 FR-LINE＋FR-STRUCT（FR-BUCKET 不响）' 1 \
      "$WORK/bad-nosec-liq.md" 'FR-LINE,FR-STRUCT'
  else
    echo '  不可判 删流动性风险注入没落地'; unk=$((unk + 1))
  fi
fi

# 反证档：把「口径与未取到」那行口径说明改写成带红线词的形态，期望**零发条**。
# 口径节整节豁免：按设计它就要写「本件不判断流动性是否充裕、不判断偿债能力强弱」这类话，
# 不豁免会自己咬自己。这是全套里唯一期望 rc=0 的注入档——它证明「豁免真的生效」，
# 而不是靠好样恰好不含红线词。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/ok-gap-exempt.md" \
  '本件不判断流动性是否充裕、不判断偿债能力强弱，也不把敞口金额当作已发生损失或可用资金。' \
  '本件不判断流动性是否充裕、不判断偿债能力强弱，也不把敞口金额当作已损失、已减值或可动用资金。' 0 '口径节写红线词（应豁免）' ; then
  run '反证：口径节写红线词 → 零发条（整节豁免）' 0 "$WORK/ok-gap-exempt.md" ''
fi

echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
