#!/usr/bin/env bash
# run_fixtures.sh — 终止经营登记稿的离线样例 runner
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
CK="$ROOT/scripts/check_terminated_operations.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-terminated-operations-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`TO-XXX L12 …` 的行首码），不另跑一份统计。
# 注意：码里带连字符（TO-QUOTE／TO-PL／TO-CASH／TO-LINE），正则须写成 `TO-[A-Z-]*`——
# 写成 `TO-[A-Z]*` 会永远取不到 TO-QUOTE 这类，那条断言就成了永远为真的空断言。
# 机检的读数行与「—— 机检：…」汇总行**没有行号**，正则要求 `L数字` 才不会把它们当成发条。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(TO-[A-Z-]*\) L[0-9].*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
GOOD="$WORK/good-to.md"
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

# 注入一：删掉头部第三件自标。只该红 TO-STRUCT（形制三件自标逐字在位）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct-mark.md" \
  'AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议' \
  'AI 整理初稿 ｜ 请回原文核对' 0 '删掉头部第三件自标' ; then
  run '头部缺「不构成投资建议」→ 只红 TO-STRUCT' 1 "$WORK/bad-struct-mark.md" 'TO-STRUCT'
fi

# 注入二：拆掉「终止经营概况」里净利润那行的「」原句与〔锚〕，只留 [S1]。
# 只该红 TO-QUOTE。**改的是概况节的净利润行，金额不动**（TO-PL 仍拿到 34,600 与分项和相等），
# 所以不会顺带红 TO-PL——钉住「只红一道」。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '终止经营净利润〔口径：本期发生额〕34,600.00 万元「终止经营净利润为人民币 34,600.00 万元」〔锚：2025 年年报·第 251 页·终止经营〕[S1]' \
  '终止经营净利润〔口径：本期发生额〕34,600.00 万元 [S1]' 0 '拆掉原句与锚只留 [S1]' ; then
  run '拆掉原句与锚只留 [S1] → 只红 TO-QUOTE' 1 "$WORK/bad-quote.md" 'TO-QUOTE'
fi

# 注入三：把概况节的终止经营净利润改大（只改行首数，不改损益分项、不改引号内原句）。
# 只该红 TO-PL：分项和 34,600 仍在，披露净利润变 40,000。TO-QUOTE 不比对引号内的数与行首。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-pl.md" \
  '终止经营净利润〔口径：本期发生额〕34,600.00 万元' \
  '终止经营净利润〔口径：本期发生额〕40,000.00 万元' 0 '净利润改 40,000' ; then
  run '净利润 34,600→40,000（分项和对不上）→ 只红 TO-PL' 1 "$WORK/bad-pl.md" 'TO-PL'
fi

# 注入四：把现金流量节的合计改大（经营 15,200＋投资 21,800 仍是 37,000）。只该红 TO-CASH。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-cash.md" \
  '现金流量净额合计〔口径：本期发生额〕37,000.00 万元' \
  '现金流量净额合计〔口径：本期发生额〕40,000.00 万元' 0 '现金合计改 40,000' ; then
  run '现金合计 37,000→40,000（经营+投资对不上）→ 只红 TO-CASH' 1 "$WORK/bad-cash.md" 'TO-CASH'
fi

# 注入五：把投资活动改成净流出（21,800 → -21,800）。符号必须保住 ⇒ 15,200−21,800 与合计对不上。
# 只该红 TO-CASH。这一档钉住「负号不被吞」——若 _num 把负号吃掉，求和仍是 37,000，这一档就会假绿。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-cash-sign.md" \
  '投资活动现金流量净额〔口径：本期发生额〕21,800.00 万元' \
  '投资活动现金流量净额〔口径：本期发生额〕-21,800.00 万元' 0 '投资活动改净流出' ; then
  run '投资活动 21,800→-21,800（符号须保住）→ 只红 TO-CASH' 1 "$WORK/bad-cash-sign.md" 'TO-CASH'
fi

# 注入六：插一条带完整三元组的红线行（①类「处置划算」＋③类「将增厚业绩」）。
# 只该红 TO-LINE。插入型：新片段＝红线行 ＋ 节首空行后的原内容，旧片段（节标题＋空行）留着 ⇒ 残留 1。
# 锚在「节标题＋其后空行」（不是只锚节标题）：只锚标题的替换会把内容插进**上一节**，
# 红线行就落进了不该落的地方，测到的就不是 TO-LINE 判整行了。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line.md" \
  '## 处置损益与对价

' \
  '## 处置损益与对价

- 处置评价〔口径：本期末〕「本次处置划算，预计将增厚业绩」〔锚：2025 年年报·第 253 页·终止经营〕[S1]
' 1 '插一条处置评价红线行' ; then
  run '插「处置划算／将增厚业绩」行 → 只红 TO-LINE' 1 "$WORK/bad-line.md" 'TO-LINE'
fi

# 注入七：整节删掉「终止经营现金流量」。应**只红** TO-STRUCT（缺节），
# 而 TO-CASH **不该响**（任一侧缺失即跳过，缺节不归它管）。这一档钉住「跳过而不是猜 0」。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-nosec-cash.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
i = t.index('## 终止经营现金流量')
j = t.index('## 持有待售资产与负债')
out = t[:i] + t[j:]
if out == t:
    sys.exit('注入点不在好样里')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '整节删掉终止经营现金流量 → 只红 TO-STRUCT（TO-CASH 跳过不响）' 1 \
      "$WORK/bad-nosec-cash.md" 'TO-STRUCT'
  else
    echo '  不可判 删现金流量节注入没落地'; unk=$((unk + 1))
  fi
fi

# 注入八：只删掉现金流量节里的「投资活动」那一行，**节仍在、合计仍在**。
# 期望零发条（rc=0）：任一侧缺失即整条跳过。这一档专钉「跳过而不是补 0」——
# 若机检把缺失的那一项当 0（15,200 + 0 ≠ 37,000），它就会发一条 TO-CASH，本档即红。
# 整节删掉的那一档（上面注入七）测的是另一件事：节缺时 TO-CASH 不崩、TO-STRUCT 点名。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/ok-cash-oneside.md" \
  '- 投资活动现金流量净额〔口径：本期发生额〕21,800.00 万元「终止经营投资活动产生的现金流量净额为人民币 21,800.00 万元」〔锚：2025 年年报·第 252 页·终止经营〕[S1]
' '' 0 '删掉投资活动那一行（节与合计仍在）' ; then
  run '删掉投资活动行、合计仍在 → 跳过不补 0（零发条）' 0 "$WORK/ok-cash-oneside.md" ''
fi

# 反证档：把「口径与未取到」那行里的红线词再写一次，期望**零发条**。
# 口径节整节豁免：它按设计就要写「本件不判断处置是否划算……也不把处置损益当作可持续利润」，
# 而「可持续利润」正是 ②类红线词——好样能过全靠这一节豁免。这条反证把红线词在豁免节里
# **再加一处**，仍然期望零发条，钉住「豁免真的生效」而不是「好样恰好干净」。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/ok-gap-exempt.md" \
  '也不把处置损益当作可持续利润。' \
  '也不把处置损益当作可持续利润，更不当作可持续利润来源。' 0 '口径节再写一次红线词（应豁免）' ; then
  run '反证：口径节再写「可持续利润」→ 零发条（整节豁免）' 0 "$WORK/ok-gap-exempt.md" ''
fi

echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
