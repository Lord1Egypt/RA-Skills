#!/usr/bin/env bash
# run_fixtures.sh — 预期信用损失登记稿的离线样例 runner
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
# **期望退码不写死**：好样与自测那两档从自测末行的「不可判=N」现算（N>0 ⇒ 3，N=0 ⇒ 0），
# 与 KF／EQ／FV／OCI 那几份 runner 同形。写死某一个退码的形状是「今天对、判据补齐后就错」——
# 判据一补齐，runner 从该绿变常红，逼下一个人去改断言而不是改判据。这里让它自己跟着走。
# 坏样那几档期望恒为 1（有发条），反证档期望恒为 0（零发条）：这两条与「判据是否落字」无关，
# 发条就是 1、零发条就是 0，不会因为某道回退而变。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_expected_credit_loss.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-expected-credit-loss-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`ECL-XXX L12 …` 的行首码），不另跑一份统计。
# 注意：机检的读数行与「—— 机检：…」汇总行**没有行号**，正则要求 `L数字` 才不会把它们当成发条——
# 那是读数不是违例，混进码集会把「零发条」读成「发了某道码」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(ECL-[A-Z]*\) L[0-9].*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
GOOD="$WORK/good-ecl.md"
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

# 注入一：删掉头部第三件自标。只该红 ECL-STRUCT（形制三件自标逐字在位）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct-mark.md" \
  'AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议' \
  'AI 整理初稿 ｜ 请回原文核对' 0 '删掉头部第三件自标' ; then
  run '头部缺「不构成投资建议」→ 只红 ECL-STRUCT' 1 "$WORK/bad-struct-mark.md" 'ECL-STRUCT'
fi

# 注入二：整节删掉「前瞻性信息与账龄依据」（连标题与五行）。只该红 ECL-STRUCT（缺节）。
# 为什么删这一节而不是「单项计提」：ECL-LINE 按规格也判组合／单项两节缺失，
# 删单项计提会让那一档同时红两道，钉不住「只红形制」。缺单项计提另有注入九专钉双红。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-struct-sec.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
i = t.index('## 前瞻性信息与账龄依据')
j = t.index('## 口径与未取到')
out = t[:i] + t[j:]
if out == t:
    sys.exit('注入点不在好样里')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '整节删掉前瞻性信息与账龄依据 → 只红 ECL-STRUCT' 1 "$WORK/bad-struct-sec.md" 'ECL-STRUCT'
  else
    echo '  不可判 删节注入没落地'; unk=$((unk + 1))
  fi
fi

# 注入三：拆掉概况首行尾的「」原句与〔锚〕，只留 [S1]。只该红 ECL-QUOTE。
# 行仍是 `- ` 行、S1 仍被别的行引用（不致连带「来源行未被引用」）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '「本报告期末本集团预期信用损失准备的账面余额为人民币 3,456.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]' \
  '[S1]' 0 '拆掉原句与锚只留 [S1]' ; then
  run '数字行缺「」原句＋〔锚〕→ 只红 ECL-QUOTE' 1 "$WORK/bad-quote.md" 'ECL-QUOTE'
fi

# 注入四：来源行检索日写成斜杠式。该行不合格式、不再算登记，正文引 S2 的行随之发「未登记」。
# 两条都在 ECL-QUOTE 里，码集仍是 {ECL-QUOTE}。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-source.md" \
  '单项计提与前瞻性信息 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20' \
  '单项计提与前瞻性信息 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026/03/20' 0 '来源行检索日改斜杠式' ; then
  run '来源行检索日斜杠 → 只红 ECL-QUOTE' 1 "$WORK/bad-source.md" 'ECL-QUOTE'
fi

# 注入五：阶段行自写一个原句里没有的阶段词——行首标第三阶段，原句改成第一阶段。
# 三元组齐（ECL-QUOTE 不红），数没动（不触发同阶段两数）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-stage-word.md" \
  '「第三阶段（整个存续期预期信用损失，已发生信用减值）的损失准备为人民币 2,200.00 万元」' \
  '「第一阶段（整个存续期预期信用损失，已发生信用减值）的损失准备为人民币 2,200.00 万元」' 0 '行首第三阶段 vs 原句第一阶段' ; then
  run '行首阶段词与含该词的原句不符 → 只红 ECL-STAGE' 1 "$WORK/bad-stage-word.md" 'ECL-STAGE'
fi

# 注入六：同一阶段在一节里报两个不同的损失准备数（追加一行第一阶段 789.00，三元组齐）。
# 插入型：旧片段留在原处，残留次数应为 1。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-stage-two.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
anchor = ('- 损失准备〔阶段：第一阶段〕456.00 万元「第一阶段（未来 12 个月内预期信用损失）'
          '的损失准备为人民币 456.00 万元」〔锚：2025 年年报·第 206 页·三阶段划分〕[S1]\n')
if t.count(anchor) != 1:
    sys.exit('注入点出现 %d 次，期望 1 次' % t.count(anchor))
extra = ('- 损失准备〔阶段：第一阶段〕789.00 万元「第一阶段（未来 12 个月内预期信用损失）'
         '的损失准备为人民币 789.00 万元」〔锚：2025 年年报·第 206 页·三阶段划分〕[S1]\n')
out = t.replace(anchor, anchor + extra, 1)
if out == t:
    sys.exit('替换后与源件同字节')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '同一阶段报了两个不同损失准备数 → 只红 ECL-STAGE' 1 "$WORK/bad-stage-two.md" 'ECL-STAGE'
  else
    echo '  不可判 同阶段两数注入没落地'; unk=$((unk + 1))
  fi
fi

# 注入七：比率不符——账龄组合计提比例改成 20.00%，而 损失准备/账面余额 = 1,234/12,340 = 10.00%。
# 行首与引文同步改（否则会被读成「引文与行首不一致」，但本件没有那道判据；同步改是为了不留歧义）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-roll-pct.md" \
  '计提比例 10.00%「按账龄组合计提的预期信用损失计提比例为 10.00%」' \
  '计提比例 20.00%「按账龄组合计提的预期信用损失计提比例为 20.00%」' 0 '计提比例 10.00→20.00' ; then
  run '计提比例与 损失准备/账面余额 不符 → 只红 ECL-ROLL' 1 "$WORK/bad-roll-pct.md" 'ECL-ROLL'
fi

# 注入八：滚动不符——期末余额改成 1,500.00，而 期初 1,000 + 计提 334 - 转回 50 - 核销 50 = 1,234。
# 比率那一路不受影响（损失准备与账面余额没动，比例仍是 10.00%）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-roll-sum.md" \
  '期末余额 1,234.00 万元「账龄组合损失准备的期末余额为人民币 1,234.00 万元」' \
  '期末余额 1,500.00 万元「账龄组合损失准备的期末余额为人民币 1,500.00 万元」' 0 '期末余额 1,234→1,500' ; then
  run '滚动式与期末不符 → 只红 ECL-ROLL' 1 "$WORK/bad-roll-sum.md" 'ECL-ROLL'
fi

# 注入九：整节删掉「单项计提」。ECL-STRUCT 报缺节，ECL-LINE 按规格也报（两条计提路径缺一条）。
# 这一档专钉**双红**，不被并成单码——删节这种破坏确实同时违反两条判据，不是归属混了。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-nosec-single.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
i = t.index('## 单项计提')
j = t.index('## 前瞻性信息与账龄依据')
out = t[:i] + t[j:]
if out == t:
    sys.exit('注入点不在好样里')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '整节删掉单项计提 → 双红 ECL-STRUCT＋ECL-LINE' 1 "$WORK/bad-nosec-single.md" 'ECL-LINE,ECL-STRUCT'
  else
    echo '  不可判 删单项计提注入没落地'; unk=$((unk + 1))
  fi
fi

# 注入十~十三：四条红线各一支。都往「前瞻性信息与账龄依据」节末插一条**三元组齐**的行，
# 这样 ECL-QUOTE 不会连带红（原句够长、S 号已登记），只钉 ECL-LINE。
# 插入型：`## 口径与未取到` 留在原处，残留次数应为 1。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line-loss.md" \
  '## 口径与未取到' \
  '- 损失准备〔口径：本期末〕已确定收不回「本集团对甲客户的应收款项已确定收不回，全额计提损失准备」〔锚：2025 年年报·第 206 页·单项计提〕[S2]

## 口径与未取到' 1 '插入「已确定收不回」' ; then
  run '红线：把损失准备写成已确定收不回 → 只红 ECL-LINE' 1 "$WORK/bad-line-loss.md" 'ECL-LINE'
fi

if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line-enough.md" \
  '## 口径与未取到' \
  '- 计提结论〔口径：本期末〕计提充分「本集团预期信用损失计提充分，不存在进一步减值风险」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]

## 口径与未取到' 1 '插入「计提充分」' ; then
  run '红线：给「计提充分」的判断 → 只红 ECL-LINE' 1 "$WORK/bad-line-enough.md" 'ECL-LINE'
fi

if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line-net.md" \
  '## 口径与未取到' \
  '- 账面余额〔口径：本期末〕按净额列示 10,890.00 万元「按账龄组合计提的应收款项账面余额为人民币 12,340.00 万元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]

## 口径与未取到' 1 '插入「按净额列示」' ; then
  run '红线：用轧净额冒充账面余额 → 只红 ECL-LINE' 1 "$WORK/bad-line-net.md" 'ECL-LINE'
fi

if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line-rating.md" \
  '## 口径与未取到' \
  '- 结论〔口径：本期末〕给予增持评级「我们给予公司增持评级，目标价 12.00 元」〔锚：2025 年年报·第 205 页·预期信用损失〕[S1]

## 口径与未取到' 1 '插入「增持评级／目标价」' ; then
  run '红线：给评级与目标价 → 只红 ECL-LINE' 1 "$WORK/bad-line-rating.md" 'ECL-LINE'
fi

# 反证档：把「口径与未取到」那行口径说明改写成带红线词的形态，期望**零发条**。
# 口径节整节豁免：按设计它就要写「本件不判断计提是否充分」这类话，不豁免会自己咬自己。
# 这是全套里唯一期望 rc=0 的注入档——它证明「豁免真的生效」，而不是靠好样恰好不含红线词。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/ok-gap-exempt.md" \
  '本件不重算损失率、不拿期初期末轧本期计提、不判断计提是否充分；' \
  '本件不重算损失率、不拿期初期末轧本期计提；关于计提充分与计提不足的判断不在本件，附注亦未给出按净额列示的口径；' 0 '口径节写红线词（应豁免）' ; then
  run '反证：口径节写红线词 → 零发条（整节豁免）' 0 "$WORK/ok-gap-exempt.md" ''
fi

echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
