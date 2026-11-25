#!/usr/bin/env bash
# run_fixtures.sh — 应付职工薪酬登记稿的离线样例 runner
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
CK="$ROOT/scripts/check_employee_benefits.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-employee-benefits-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`EB-XXX L12 …` 的行首码），不另跑一份统计。
# 注意：码里带连字符（EB-STRUCT／EB-QUOTE／EB-ROLL／EB-PLAN／EB-LINE），正则须写成 `EB-[A-Z-]*`——
# 写成 `EB-[A-Z]*` 会永远取不到带连字符的那几道，那条断言就成了永远为真的空断言。
# 机检的读数行与「—— 机检：…」汇总行**没有行号**，正则要求 `L数字` 才不会把它们当成发条。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(EB-[A-Z-]*\) L[0-9].*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
GOOD="$WORK/good-eb.md"
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

# 注入一：删掉头部第三件自标。只该红 EB-STRUCT（形制三件自标逐字在位）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct-mark.md" \
  'AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议' \
  'AI 整理初稿 ｜ 请回原文核对' 0 '删掉头部第三件自标' ; then
  run '头部缺「不构成投资建议」→ 只红 EB-STRUCT' 1 "$WORK/bad-struct-mark.md" 'EB-STRUCT'
fi

# 注入二：拆掉期初余额那行的「」原句与〔锚〕，只留 [S1]。
# 只该红 EB-QUOTE。**金额不动**（EB-ROLL 仍拿到 12,400 与四数相等），钉住「只红一道」。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '- 期初余额〔口径：本期末〕12,400.00 万元「本集团应付职工薪酬年初余额为人民币 12,400.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]' \
  '- 期初余额〔口径：本期末〕12,400.00 万元 [S1]' 0 '拆掉原句与锚只留 [S1]' ; then
  run '拆掉原句与锚只留 [S1] → 只红 EB-QUOTE' 1 "$WORK/bad-quote.md" 'EB-QUOTE'
fi

# 注入三：把期末余额改大 100（只改行首数，不改引号内原句）。只该红 EB-ROLL。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-roll.md" \
  '13,800.00 万元「本集团应付职工薪酬期末余额' \
  '13,900.00 万元「本集团应付职工薪酬期末余额' 0 '期末余额改 13,900' ; then
  run '期末 13,800→13,900（12,400＋8,600−7,200 对不上）→ 只红 EB-ROLL' 1 \
    "$WORK/bad-roll.md" 'EB-ROLL'
fi

# 注入四：删掉设定提存计划那一行。只该红 EB-PLAN（两类计划必须分列）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-plan.md" \
  '- 设定提存计划〔口径：本期发生额〕960.00 万元「本集团按既定比例向基本养老保险及企业年金缴存，设定提存计划本期缴费金额为人民币 960.00 万元」〔锚：2025 年年报·第 259 页·离职后福利〕[S1]
' '' 0 '删掉设定提存计划行' ; then
  run '删掉设定提存计划行 → 只红 EB-PLAN' 1 "$WORK/bad-plan.md" 'EB-PLAN'
fi

# 注入五：插一条带完整三元组的红线行（前瞻预测「预计」）。插入型 ⇒ 旧片段残留 1。
# 锚在「节标题＋其后空行」（不是只锚节标题）：只锚标题的替换会把内容插进**上一节**，
# 红线行就落进了不该落的地方，测到的就不是 EB-LINE 只在内容节扫。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line.md" \
  '## 短期薪酬

' \
  '## 短期薪酬

- 明年福利〔口径：本期发生额〕420.00 万元「预计明年职工福利费将上升」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]
' 1 '插一条「预计」红线行' ; then
  run '插「预计明年…上升」行 → 只红 EB-LINE' 1 "$WORK/bad-line.md" 'EB-LINE'
fi

# 注入六：删掉「本期减少」那一行，**且口径节仍是「未取到：无」**。
# 只该红 EB-ROLL（缺数），钉住「未取到：无 不算已声明缺数」——这是我在 /tmp 里亲手撞过的坑。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-roll-miss.md" \
  '- 本期减少〔口径：本期发生额〕7,200.00 万元「本集团本期应付职工薪酬减少额为人民币 7,200.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]
' '' 0 '删掉本期减少行（口径节仍写未取到：无）' ; then
  run '删本期减少行且口径节仍写「未取到：无」→ 只红 EB-ROLL（缺数）' 1 "$WORK/bad-roll-miss.md" 'EB-ROLL'
fi

# 注入七：来源节多登记一条 [S2] 但正文从不引用。只该红 EB-QUOTE（反向对应）。
# 插入型（新行插在 [S1] 之前，[S1] 那行留在原处）⇒ 旧片段残留 1。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote-unused.md" \
  '- [S1] 示例材料 2025 年年度报告·附注·应付职工薪酬' \
  '- [S2] 未被引用的来源 | https://example.invalid/y.pdf | 检索日 2026-03-20
- [S1] 示例材料 2025 年年度报告·附注·应付职工薪酬' 1 '来源多登记一条 [S2]' ; then
  run '来源登记 [S2] 但正文未引用 → 只红 EB-QUOTE' 1 "$WORK/bad-quote-unused.md" 'EB-QUOTE'
fi

# 反证一：删掉「本期减少」那一行，但口径节写明「未取到：本期减少额」。期望**零发条**。
# 这一档专钉「跳过而不是补 0」：若机检把缺失项当 0，它会发一条 EB-ROLL，本档即红。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/ok-roll-declared.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
row = ('- 本期减少〔口径：本期发生额〕7,200.00 万元'
       '「本集团本期应付职工薪酬减少额为人民币 7,200.00 万元」'
       '〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]\n')
if row not in t:
    sys.exit('反证注入点不在源件里')
t2 = t.replace(row, '', 1)
old = '- 未取到：无'
if old not in t2:
    sys.exit('口径节「未取到：无」不在源件里')
t2 = t2.replace(old, '- 未取到：本期减少额', 1)
Path(dst).write_text(t2, encoding='utf-8')
PY
  if [ -f "$WORK/ok-roll-declared.md" ]; then
    run '删本期减少＋口径节声明「未取到：本期减少额」→ 零发条（豁免生效）' 0 "$WORK/ok-roll-declared.md" ''
  else
    echo "  不可判 反证注入没落地（不读成「豁免生效」）"; unk=$((unk + 1))
  fi
fi

# 反证二：口径节里写一句含「预计」的话。期望**零发条**（整节豁免）。
# 钉住「EB-LINE 只在四个内容节扫」：若豁免失效，这句会红。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/ok-line-exempt.md" \
  '也不把应付职工薪酬当作可支配资金。' \
  '也不把应付职工薪酬当作可支配资金，不预计以后期间。' 0 '口径节插一句含「预计」' ; then
  run '口径节写「不预计以后期间」→ 零发条（整节豁免）' 0 "$WORK/ok-line-exempt.md" ''
fi

# 去重档：一行同时含「不合理」与「显著偏低」⇒ 恰好 2 条，不是 3 条也不是 1 条。
# 这一档证的不是「红了」而是「只报不被包含的那些」：偏低被显著偏低吸收，合理被不合理吸收。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/line-dedup.md" \
  '- 职工福利费〔口径：本期发生额〕420.00 万元「短期薪酬中职工福利费本期发生额为人民币 420.00 万元」〔锚：2025 年年报·第 258 页·应付职工薪酬〕[S1]' \
  '- 薪酬结构不合理且显著偏低〔口径：本期发生额〕420.00 万元「x」〔锚：y〕[S1]' 0 '插一行含「不合理」「显著偏低」' ; then
  count_lines "$WORK/line-dedup.md" 'EB-LINE' 2 '一行含「不合理」与「显著偏低」→ 恰好 2 条'
fi

echo '——'
echo "档数=$tiers｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then
  echo "3 取值域故障：有 $unk 支注入没落地，结果不可判（不读成「零违例」）"; exit 3
fi
if [ "$bad" -gt 0 ]; then
  echo "1 有不合：$bad 档"; exit 1
fi
echo "0 三档全合期望"
exit 0
