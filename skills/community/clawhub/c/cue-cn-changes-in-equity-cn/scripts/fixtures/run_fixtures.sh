#!/usr/bin/env bash
# run_fixtures.sh — 所有者权益变动表登记稿的离线样例 runner
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
# **期望退码不写死**：从自测末行的「不可判=N」现算（N>0 ⇒ 3，N=0 ⇒ 0），与 FV／OCI 那两份 runner 同形。
# 写死某一个退码的形状是「今天对、判据补齐后就错」——判据一补齐，runner 从该绿变常红，
# 逼下一个人去改断言而不是改判据。这里让它自己跟着走。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_equity_statement.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-changes-in-equity-cn.XXXXXX")" || {
  echo "3 取值域故障：临时目录没建成（TMPDIR=${TMPDIR:-未设} 是否存在、可写？）"; exit 3; }
[ -d "$WORK" ] || { echo "3 取值域故障：临时目录不存在"; exit 3; }
trap 'rm -rf "$WORK"' EXIT

[ -f "$CK" ] || { echo "3 取值域故障：取不到 $CK（不读成「样例全过」）"; exit 3; }

bad=0
unk=0
tiers=0

# 一支注入：mutate <源件> <目标件> <原文片段> <替换片段> <替换后原文片段残留次数> <标签>
# want 数的是**旧片段**在替换后的残留次数：换掉一处唯一片段 ⇒ 0；只从 N 处里抠掉一处 ⇒ N-1。
# 失败（片段不在源件里、替换后与源件同字节、或残留次数不符）＝ 取值域故障，不计入「不合」。
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
# 码集从机检自己的输出里取（`EQ-XXX L12 …` 的行首码），不另跑一份统计。
# 注意：`EQ-FOOT 已判：…` 那行**没有行号**，正则要求 `L数字` 才不会把它当成发条——
# 那是读数不是违例，混进码集会把「零发条」读成「发了 EQ-FOOT」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(EQ-[A-Z]*\) L[0-9].*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
GOOD="$WORK/good-eq.md"
if python3 -B "$CK" --demo > "$GOOD" 2>"$WORK/demo.err" && [ -s "$GOOD" ]; then
  echo "  ok   --demo 产出 $([ -s "$GOOD" ] && wc -c < "$GOOD" | tr -d ' ') 字节"
  run "好样 demo 稿（零发条／不可判 $WANT_UNJUDGED 道）" "$WANT_RC" "$GOOD" ''
else
  echo "  不可判 --demo 没产出文本（取值域故障，不读成「好样零发条」）"
  sed 's/^/      /' "$WORK/demo.err" 2>/dev/null
  unk=$((unk + 1))
fi

echo '档③ 坏样：在好样临时副本上只破一处，须各只发自己那道码'
tiers=$((tiers + 1))

# 注入一：删掉头部第三件自标。只该红 EQ-STRUCT（形制三件自标逐字在位）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct.md" \
  'AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议' \
  'AI 整理初稿 ｜ 请回原文核对' 0 '删掉头部第三件自标' ; then
  run '头部缺「不构成投资建议」→ 只红 EQ-STRUCT' 1 "$WORK/bad-struct.md" 'EQ-STRUCT'
fi

# 注入二：摘掉某发现行的〔锚〕（保留「」与 [S#]）。只该红 EQ-QUOTE。
# 好样里「第 181 页」这个锚出现 3 次（三行同页），抠掉一处 ⇒ 残留 2。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '〔锚：2025 年年报·第 181 页·合并所有者权益变动表〕' '' 2 '摘掉一个〔锚〕' ; then
  run '发现行缺〔锚〕→ 只红 EQ-QUOTE' 1 "$WORK/bad-quote.md" 'EQ-QUOTE'
fi

# 注入三：把「本期增减变动」列内破一格（实收资本期末 33→34）。
# 只该红 EQ-FOOT：期初 30 ＋ 增减 3 ＝ 33，改成 34 后列内不平；
# 合计列不动，于是期末行内也由平变不平（112 ≠ 113）。两条都是 EQ-FOOT，码集仍是一道。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-foot.md" \
  '期末余额〔列：实收资本〕33.00 亿元' '期末余额〔列：实收资本〕34.00 亿元' 0 '实收资本期末 33→34（列内破）'; then
  run '列内不平（期末≠期初＋增减）→ 只红 EQ-FOOT' 1 "$WORK/bad-foot.md" 'EQ-FOOT'
fi

# 注入四：勾稽①破，综合收益总额 10→11（净利润 8 ＋ 其他综合收益 2 ＝ 10）。
# 只该红 EQ-LINK：EQ-FOOT 只看列内的期初／增减／期末，不碰这个数。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-link.md" \
  '综合收益总额 10.00 亿元' '综合收益总额 11.00 亿元' 0 '综合收益总额 10→11（勾稽①破）'; then
  run '综合收益总额≠净利润＋其他综合收益 → 只红 EQ-LINK' 1 "$WORK/bad-link.md" 'EQ-LINK'
fi

# 注入五：红线词。在内容节里加一句替读者下结论的话。只该红 EQ-LINE。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line.md" \
  '- 综合收益总额 10.00 亿元' '- 公司股东回报丰厚，综合收益总额 10.00 亿元' 0 '加一句「股东回报丰厚」'; then
  run '正文自下判断 → 只红 EQ-LINE' 1 "$WORK/bad-line.md" 'EQ-LINE'
fi

# 注入六：把「未分配利润」改写成「可分现金」。只该红 EQ-LINE。
# 这一支是**追加**而非替换，旧片段仍在新行里 ⇒ 残留 1。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-cash.md" \
  '期末余额〔列：未分配利润〕59.00 亿元' '期末余额〔列：未分配利润〕59.00 亿元，为大额可分现金' 1 \
  '把未分配利润说成可分现金'; then
  run '账面数说成可分现金 → 只红 EQ-LINE' 1 "$WORK/bad-cash.md" 'EQ-LINE'
fi

# 注入七（读数档）：整稿摘掉全部〔列：…〕列标签 ⇒ EQ-FOOT 一项都判不了。
# 这一档专钉「读不到当成 0」：摘了标签之后必须**发条明说零校验**，而不是静默零发条。
# 期望码集恰为 EQ-FOOT（那一条「未判任何一项」的发条）。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/nocol.md" <<'PY'
import re, sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
out = re.sub(r"〔\s*列\s*[:：][^〕]*〕", "", t)
if out == t:
    sys.exit('注入点不在好样里（没有列标签可摘）')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '整稿摘掉列标签（零校验必须发条）→ 只红 EQ-FOOT' 1 "$WORK/nocol.md" 'EQ-FOOT'
  else
    echo '  不可判 摘列标签注入没落地'; unk=$((unk + 1))
  fi
fi

# 反证档：口径节按设计要写「不把未分配利润改写成可分现金」「不评价股东回报」这类说明，
# 该节整节豁免红线。这一档把红线词**搬进口径节**，期望零发条——
# 证明豁免是真生效，而不是靠「没测到」蒙过去的。
if [ -f "$GOOD" ]; then
  if mutate "$GOOD" "$WORK/ok-exempt.md" \
    '- 口径：七个节一律照抄合并所有者权益变动表原文；' \
    '- 口径：本件不评价股东回报是否丰厚，七个节一律照抄合并所有者权益变动表原文；' 0 \
    '红线词搬进口径节（该节整节豁免）'; then
    run '反证：口径节写红线词 → 零发条' 0 "$WORK/ok-exempt.md" ''
  fi
fi

echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
