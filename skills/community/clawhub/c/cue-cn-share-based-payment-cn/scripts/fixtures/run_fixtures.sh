#!/usr/bin/env bash
# run_fixtures.sh — 股份支付登记稿的离线样例 runner
#
# 三档：① 机检自测 → ② 好样（--demo 产物自过机检）→ ③ 坏样／反证（在好样临时副本上只动一处）。
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
CK="$ROOT/scripts/check_share_based_payment.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-share-based-payment-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`SP-XXX L12 …` 的行首码），不另跑一份统计。
# 注意：码里带连字符（SP-STRUCT／SP-QUOTE／SP-SUM／SP-VEST／SP-LINE），正则须写成 `SP-[A-Z-]*`——
# 写成 `SP-[A-Z]*` 会永远取不到带连字符的那几道，那条断言就成了永远为真的空断言。
# 机检的读数行与「—— 机检：…」汇总行**没有行号**，正则要求 `L数字` 才不会把它们当成发条。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(SP-[A-Z-]*\) L[0-9].*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes:-*}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

# 数一条发条出现几次：count_lines <文件> <码> <期望条数> <标签>
# 专给「同一行同一组只报最长命中」那档用：要证的不是「红了」，而是「只红一条」。
count_lines() {
  local f="$1" code="$2" want="$3" tag="$4" got
  got="$(python3 -B "$CK" "$f" 2>&1 | grep -c "^${code} L[0-9]")"
  if [ "$got" = "$want" ]; then
    echo "  ok   $tag（${code} 发条 $got 条）"
  else
    echo "  不合 $tag：期望 ${code} 发条 $want 条，实发 $got 条"
    bad=$((bad + 1))
  fi
}

echo '档① 机检自测（好样零发条、逐枚坏样各只发自己那道码）'
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
GOOD="$WORK/good-sp.md"
if python3 -B "$CK" --demo > "$GOOD" 2>"$WORK/demo.err" && [ -s "$GOOD" ]; then
  echo "  ok   --demo 产出 $(wc -c < "$GOOD" | tr -d ' ') 字节"
  run "好样 demo 稿（零发条／不可判 $WANT_UNJUDGED 道）" "$WANT_RC" "$GOOD" ''
else
  echo "  不可判 --demo 没产出文本（取值域故障，不读成「好样零发条」）"
  sed 's/^/      /' "$WORK/demo.err" 2>/dev/null
  unk=$((unk + 1))
fi

echo '档③ 坏样／反证：在好样临时副本上只动一处'
tiers=$((tiers + 1))

# 注入一：删掉头部第三件自标。只该红 SP-STRUCT（形制三件自标逐字在位）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct-mark.md" \
  'AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议' \
  'AI 整理初稿 ｜ 请回原文核对' 0 '删掉头部第三件自标' ; then
  run '头部缺「不构成投资建议」→ 只红 SP-STRUCT' 1 "$WORK/bad-struct-mark.md" 'SP-STRUCT'
fi

# 注入二：拆掉权益结算「本期确认的费用」那行的「」原句与〔锚〕，只留 [S1]。
# 只该红 SP-QUOTE。**金额不动**（SP-SUM 仍拿到 15,600 与合计相等），钉住「只红一道」。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '- 本期确认的费用〔口径：本期发生额〕15,600.00 万元「以权益结算的股份支付本期确认费用人民币 15,600.00 万元」〔锚：2025 年年报·第 268 页·股份支付〕[S1]' \
  '- 本期确认的费用〔口径：本期发生额〕15,600.00 万元 [S1]' 0 '拆掉原句与锚只留 [S1]' ; then
  run '拆掉原句与锚只留 [S1] → 只红 SP-QUOTE' 1 "$WORK/bad-quote.md" 'SP-QUOTE'
fi

# 注入三：把概况的费用总额改大（只改行首数，不改引号内原句、不改两类费用）。只该红 SP-SUM。
# 这一档会同时踩到两条 SP-SUM（两类之和对不上 + 两处合计互不相等），但码集仍只有 SP-SUM。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-sum.md" \
  '本期确认的费用总额〔口径：本期发生额〕18,400.00 万元' \
  '本期确认的费用总额〔口径：本期发生额〕19,400.00 万元' 0 '概况总额改 19,400' ; then
  run '概况总额 18,400→19,400（两类之和与两处合计都对不上）→ 只红 SP-SUM' 1 \
    "$WORK/bad-sum.md" 'SP-SUM'
fi

# 注入四：把期末可行权数量改大（只动行首数与引号内的数）。只该红 SP-VEST。
# 若 _own_qty 取不到「万股」，这一档会假绿——所以它同时钉住「数量行按万股取数」。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-vest.md" \
  '1,300.00 万股「期末尚未解除限售的限制性股票为 1,300.00 万股」' \
  '1,400.00 万股「期末尚未解除限售的限制性股票为 1,400.00 万股」' 0 '期末数量改 1,400' ; then
  run '期末可行权 1,300→1,400（四数恒等不成立）→ 只红 SP-VEST' 1 "$WORK/bad-vest.md" 'SP-VEST'
fi

# 注入五：插一条带完整三元组的红线行（前瞻预测「预计」）。插入型 ⇒ 旧片段残留 1。
# 锚在「节标题＋其后空行」（不是只锚节标题）：只锚标题的替换会把内容插进**上一节**，
# 红线行就落进了不该落的地方，测到的就不是 SP-LINE 只在内容节扫。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line.md" \
  '## 等待期费用摊销

' \
  '## 等待期费用摊销

- 未来费用〔口径：本期发生额〕15,600.00 万元「预计明年股份支付费用将明显下降」〔锚：2025 年年报·第 269 页·股份支付〕[S1]
' 1 '插一条「预计」红线行' ; then
  run '插「预计明年…下降」行 → 只红 SP-LINE' 1 "$WORK/bad-line.md" 'SP-LINE'
fi

# 注入六：删掉现金结算「本期确认的费用」那一行，**且未在口径节声明未取到**。
# 只该红 SP-SUM（缺数），钉住「缺数要报、不是悄悄跳过」。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-sum-miss.md" \
  '- 本期确认的费用〔口径：本期发生额〕2,800.00 万元「以现金结算的股份支付本期确认费用人民币 2,800.00 万元」〔锚：2025 年年报·第 269 页·股份支付〕[S1]
' '' 0 '删掉现金结算费用行（未声明未取到）' ; then
  run '删现金结算费用行且未声明未取到 → 只红 SP-SUM（缺数）' 1 "$WORK/bad-sum-miss.md" 'SP-SUM'
fi

# 注入七：来源节多登记一条 [S2] 但正文从不引用。只该红 SP-QUOTE（反向对应）。
# 插入型（新行插在 [S1] 之前，[S1] 那行留在原处）⇒ 旧片段残留 1。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote-unused.md" \
  '- [S1] 示例材料 2025 年年度报告·附注·股份支付' \
  '- [S2] 未被引用的来源 | https://example.invalid/y.pdf | 检索日 2026-03-20
- [S1] 示例材料 2025 年年度报告·附注·股份支付' 1 '来源多登记一条 [S2]' ; then
  run '来源登记 [S2] 但正文未引用 → 只红 SP-QUOTE' 1 "$WORK/bad-quote-unused.md" 'SP-QUOTE'
fi

# 反证一：删掉现金结算费用行，但口径节写明「未取到」。期望**零发条**。
# 这一档专钉「跳过而不是补 0」：若机检把缺失项当 0，它会发一条 SP-SUM，本档即红。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/ok-sum-declared.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
row = ('- 本期确认的费用〔口径：本期发生额〕2,800.00 万元'
       '「以现金结算的股份支付本期确认费用人民币 2,800.00 万元」'
       '〔锚：2025 年年报·第 269 页·股份支付〕[S1]\n')
if row not in t:
    sys.exit('注入点不在好样里')
out = t.replace(row, '', 1).replace(
    '- 未取到：无', '- 未取到：现金结算的股份支付本期费用附注未单列', 1)
if out == t:
    sys.exit('替换后与源件同字节')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '删现金费用行但口径节声明未取到 → 跳过不补 0（零发条）' 0 "$WORK/ok-sum-declared.md" ''
  else
    echo '  不可判 删行+声明未取到 注入没落地'; unk=$((unk + 1))
  fi
fi

# 反证二：口径节整节豁免。在口径节里再写「买入」「目标价」，期望**零发条**。
# 好样能过靠的就是这一节豁免（口径节按设计要写「不判断…不合理…不预测…」），
# 这条反证把更多红线词在豁免节里再加一处，仍然期望零发条，钉住「豁免真生效」。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/ok-gap-exempt.md" \
  '也不把股份支付费用当作可比的经常性损益。' \
  '也不把股份支付费用当作可比的经常性损益；本件不给出买入或目标价一类的表述。' 0 \
  '口径节再写红线词（应豁免）' ; then
  run '反证：口径节再写「买入／目标价」→ 零发条（整节豁免）' 0 "$WORK/ok-gap-exempt.md" ''
fi

# 反证三：子串去重。插一行含「不合理」的完整数据行——它同时含「合理」。
# 期望 SP-LINE **只报 1 条**（报最长命中），而不是「合理」＋「不合理」两条。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/ok-line-dedup.md" \
  '## 等待期费用摊销

' \
  '## 等待期费用摊销

- 方案评价〔口径：本期〕15,600.00 万元「该激励方案的考核指标设置不合理」〔锚：2025 年年报·第 269 页·股份支付〕[S1]
' 1 '插一条含「不合理」的行' ; then
  run '插「不合理」行 → 只红 SP-LINE' 1 "$WORK/ok-line-dedup.md" 'SP-LINE'
  count_lines "$WORK/ok-line-dedup.md" 'SP-LINE' 1 '子串去重：「不合理」只记 1 条（不再额外记「合理」）'
fi

echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
