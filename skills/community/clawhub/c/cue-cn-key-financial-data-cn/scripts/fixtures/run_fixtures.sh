#!/usr/bin/env bash
# run_fixtures.sh — 主要会计数据与财务指标登记稿的离线样例 runner
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
# **期望退码不写死**：从自测末行的「不可判=N」现算（N>0 ⇒ 3，N=0 ⇒ 0），与 EQ／FV／OCI 那几份 runner 同形。
# 写死某一个退码的形状是「今天对、判据补齐后就错」——判据一补齐，runner 从该绿变常红，
# 逼下一个人去改断言而不是改判据。这里让它自己跟着走。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_key_financial_data.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-key-financial-data-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`KF-XXX L12 …` 的行首码），不另跑一份统计。
# 注意：机检的读数行与「—— 机检：…」汇总行**没有行号**，正则要求 `L数字` 才不会把它们当成发条——
# 那是读数不是违例，混进码集会把「零发条」读成「发了某道码」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(KF-[A-Z]*\) L[0-9].*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
GOOD="$WORK/good-kf.md"
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

# 注入一：删掉头部第三件自标。只该红 KF-STRUCT（形制三件自标逐字在位）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct.md" \
  'AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议' \
  'AI 整理初稿 ｜ 请回原文核对' 0 '删掉头部第三件自标' ; then
  run '头部缺「不构成投资建议」→ 只红 KF-STRUCT' 1 "$WORK/bad-struct.md" 'KF-STRUCT'
fi

# 注入二：摘掉某行的「」原句，只留数与〔锚〕。只该红 KF-QUOTE。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '「本集团本期实现营业收入人民币 1,234.00 亿元」' '' 0 '摘掉一个「」原句' ; then
  run '数字行缺「」原句 → 只红 KF-QUOTE' 1 "$WORK/bad-quote.md" 'KF-QUOTE'
fi

# 注入三：把本期比上年增减那一格的**行首与引文一起**改成 9.30%。
# 两处同步改，行首与引文才仍然一致（否则先撞 KF-LINK，测不出 CALC）；
# 重算 (1234-1150)/1150 = 7.3043%，与 9.30% 差 2 个百分点 ⇒ 只该红 KF-CALC。
# 这一支是**全局替换**而不是单点替换：7.30% 在好样里出现 2 次（行首一次、引文一次），
# 只改一处会同时触发 KF-LINK，归属就混了。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-calc.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
if t.count('7.30%') != 2:
    sys.exit('7.30%% 在好样里出现 %d 次，期望 2 次（行首与引文各一次）' % t.count('7.30%'))
out = t.replace('7.30%', '9.30%')
if out.count('7.30%') != 0:
    sys.exit('替换后仍有 7.30% 残留')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '增减披露值与重算不符（行首与引文同步改）→ 只红 KF-CALC' 1 "$WORK/bad-calc.md" 'KF-CALC'
  else
    echo '  不可判 增减注入没落地'; unk=$((unk + 1))
  fi
fi

# 注入四：把引文里的收入数改掉，行首不动。只该红 KF-LINK。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-link.md" \
  '「本集团本期实现营业收入人民币 1,234.00 亿元」' \
  '「本集团本期实现营业收入人民币 1,324.00 亿元」' 0 '引文收入数 1,234→1,324' ; then
  run '引文数与行首对不上 → 只红 KF-LINK' 1 "$WORK/bad-link.md" 'KF-LINK'
fi

# 注入五：删掉「经营活动产生的现金流量净额」那一整行。只该红 KF-LINE（该有的项少了）。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-line.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
target = '- 经营活动产生的现金流量净额〔口径：本期〕200.00 亿元'
lines = t.splitlines(keepends=True)
out = ''.join(l for l in lines if not l.startswith(target))
if out == t:
    sys.exit('注入点不在好样里（找不到经营现金流那一行）')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '删掉经营现金流净额一行 → 只红 KF-LINE' 1 "$WORK/bad-line.md" 'KF-LINE'
  else
    echo '  不可判 删行注入没落地'; unk=$((unk + 1))
  fi
fi

# 反证档：删掉整个「分季度主要会计数据」节 ⇒ KF-STRUCT 报缺节，KF-LINE 整节跳过。
# 这一档证明「缺节只红形制一道」——若 KF-LINE 也去报缺项，一支注入会红两道，归属就混了。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-nosec.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
i = t.index('## 分季度主要会计数据')
j = t.index('## 口径与未取到')
out = t[:i] + t[j:]
if out == t:
    sys.exit('注入点不在好样里')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '整节删掉分季度 → 只红 KF-STRUCT（KF-LINE 整节跳过）' 1 "$WORK/bad-nosec.md" 'KF-STRUCT'
  else
    echo '  不可判 删节注入没落地'; unk=$((unk + 1))
  fi
fi

echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
