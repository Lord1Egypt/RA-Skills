#!/usr/bin/env bash
# run_fixtures.sh — 受限资产登记稿的离线样例 runner
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
# 与 KF／EQ／ECL 那几份 runner 同形。写死某一个退码的形状是「今天对、判据补齐后就错」——
# 判据一补齐，runner 从该绿变常红，逼下一个人去改断言而不是改判据。这里让它自己跟着走。
# 坏样那几档期望恒为 1（有发条），反证档期望恒为 0（零发条）：这两条与「判据是否落字」无关，
# 发条就是 1、零发条就是 0，不会因为某道回退而变。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_restricted_assets.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-restricted-assets-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`RA-XXX L12 …` 的行首码），不另跑一份统计。
# 注意：码里带连字符（RA-SUM／RA-RATIO），正则须写成 `RA-[A-Z-]*`——
# 写成 `RA-[A-Z]*` 会永远取不到 RA-RATIO，那条断言就成了永远为真的空断言。
# 机检的读数行与「—— 机检：…」汇总行**没有行号**，正则要求 `L数字` 才不会把它们当成发条。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(RA-[A-Z-]*\) L[0-9].*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
GOOD="$WORK/good-ra.md"
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

# 注入一：删掉头部第三件自标。只该红 RA-STRUCT（形制三件自标逐字在位）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct-mark.md" \
  'AI 整理初稿 ｜ 请回原文核对 ｜ 不构成投资建议' \
  'AI 整理初稿 ｜ 请回原文核对' 0 '删掉头部第三件自标' ; then
  run '头部缺「不构成投资建议」→ 只红 RA-STRUCT' 1 "$WORK/bad-struct-mark.md" 'RA-STRUCT'
fi

# 注入二：整节删掉「受限原因与期限」（连标题与三行）。只该红 RA-STRUCT（缺节）。
# 为什么删这一节而不是「货币资金受限」：RA-LINE 按规格也判货币资金受限缺节，
# 删那一节会让这一档同时红两道，钉不住「只红形制」。缺货币资金受限另有注入十三专钉双红。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-struct-sec.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
i = t.index('## 受限原因与期限')
j = t.index('## 与负债的对应')
out = t[:i] + t[j:]
if out == t:
    sys.exit('注入点不在好样里')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '整节删掉受限原因与期限 → 只红 RA-STRUCT' 1 "$WORK/bad-struct-sec.md" 'RA-STRUCT'
  else
    echo '  不可判 删节注入没落地'; unk=$((unk + 1))
  fi
fi

# 注入三：拆掉概况首行尾的「」原句与〔锚〕，只留 [S1]。只该红 RA-QUOTE。
# 行仍是 `- ` 行、S1 仍被别的行引用（不致连带「来源行未被引用」）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '「本集团所有权或使用权受到限制的资产账面价值合计为人民币 6,600.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]' \
  '[S1]' 0 '拆掉原句与锚只留 [S1]' ; then
  run '数字行缺「」原句＋〔锚〕→ 只红 RA-QUOTE' 1 "$WORK/bad-quote.md" 'RA-QUOTE'
fi

# 注入四：来源行检索日写成斜杠式。该行不合格式、不再算登记，正文引 S1 的行随之发「未登记」。
# 两条都在 RA-QUOTE 里，码集仍是 {RA-QUOTE}。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-source.md" \
  '所有权或使用权受到限制的资产 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20' \
  '所有权或使用权受到限制的资产 | https://example.invalid/600000_2025_notes.pdf | 检索日 2026/03/20' 0 '来源行检索日改斜杠式' ; then
  run '来源行检索日斜杠 → 只红 RA-QUOTE' 1 "$WORK/bad-source.md" 'RA-QUOTE'
fi

# 注入五：合计与分项和对不上——合计 6,600→9,900，分项一律不动（分项和仍是 6,600）。
# 行首与引文同步改（三元组仍齐 ⇒ RA-QUOTE 不红）；比例行不动 ⇒ RA-RATIO 不红。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-sum-total.md" \
  '受限资产合计〔口径：本期末〕6,600.00 万元「本集团所有权或使用权受到限制的资产账面价值合计为人民币 6,600.00 万元」' \
  '受限资产合计〔口径：本期末〕9,900.00 万元「本集团所有权或使用权受到限制的资产账面价值合计为人民币 9,900.00 万元」' 0 '合计 6,600→9,900' ; then
  run '合计与分项和不符 → 只红 RA-SUM' 1 "$WORK/bad-sum-total.md" 'RA-SUM'
fi

# 注入六：某类受限金额大于该类资产账面总额（同一行内才判）。
# 插在「受限原因与期限」节末（该节不参与分项求和 ⇒ 不惊动 RA-SUM 分支①；行内无比例 ⇒ 不惊动 RA-RATIO）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-sum-over.md" \
  '## 与负债的对应' \
  '- 存货受限〔类别：存货〕1,200.00 万元／账面总额 1,000.00 万元「期末用于质押借款的存货账面价值为人民币 1,200.00 万元，该类存货账面总额为人民币 1,000.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 与负债的对应' 1 '插入受限 1,200 > 账面总额 1,000' ; then
  run '受限金额 > 该类资产账面总额 → 只红 RA-SUM' 1 "$WORK/bad-sum-over.md" 'RA-SUM'
fi

# 注入七：比例重算对不上——披露比例 3.20%→5.20%（分子分母不动，仍 6,600/206,250=3.2%）。
# 整行替换，行首与引文同步改；只动这一行 ⇒ 别道不受影响。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-ratio.md" \
  '- 占总资产比例〔口径：本期末〕受限金额 6,600.00 万元／资产总额 206,250.00 万元 → 3.20%「上述受限资产账面价值为人民币 6,600.00 万元，占本集团资产总额人民币 206,250.00 万元的比例为 3.20%」〔锚：2025 年年报·第 210 页·受限资产〕[S1]' \
  '- 占总资产比例〔口径：本期末〕受限金额 6,600.00 万元／资产总额 206,250.00 万元 → 5.20%「上述受限资产账面价值为人民币 6,600.00 万元，占本集团资产总额人民币 206,250.00 万元的比例为 5.20%」〔锚：2025 年年报·第 210 页·受限资产〕[S1]' 0 '披露比例 3.20→5.20' ; then
  run '比例与重算不符 → 只红 RA-RATIO' 1 "$WORK/bad-ratio.md" 'RA-RATIO'
fi

# 注入八：重算比例 > 100%（分子分母取错行）。
# 分母刻意写「总资产」而不是「资产总额」——后者会连 RA-SUM 分支②一起点亮，归属就混了。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-ratio-over.md" \
  '## 与负债的对应' \
  '- 受限比例〔口径：本期末〕受限金额 6,600.00 万元／总资产 5,000.00 万元 → 132.00%「上述受限资产占本集团总资产的比例为 132.00%」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 与负债的对应' 1 '插入 6,600/5,000=132%' ; then
  run '重算比例 > 100% → 只红 RA-RATIO' 1 "$WORK/bad-ratio-over.md" 'RA-RATIO'
fi

# 注入九~十二：四条红线各一支。都往「受限原因与期限」节末插一条**三元组齐**的行，
# 这样 RA-QUOTE 不会连带红（原句够长、S1 已登记），只钉 RA-LINE。
# 插入型：`## 与负债的对应` 留在原处，残留次数应为 1。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line-quality.md" \
  '## 与负债的对应' \
  '- 结论〔口径：本期末〕偿债能力充足「本集团资产质量好，偿债能力充足」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 与负债的对应' 1 '插入「资产质量好／偿债能力充足」' ; then
  run '红线①：给资产质量与偿债能力判断 → 只红 RA-LINE' 1 "$WORK/bad-line-quality.md" 'RA-LINE'
fi

if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line-loss.md" \
  '## 与负债的对应' \
  '- 受限资产〔口径：本期末〕已减值「上述受限资产已减值，预计无法收回」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 与负债的对应' 1 '插入「已减值」' ; then
  run '红线②：把受限资产说成已减值 → 只红 RA-LINE' 1 "$WORK/bad-line-loss.md" 'RA-LINE'
fi

if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line-spend.md" \
  '## 与负债的对应' \
  '- 可动用资金〔口径：本期末〕8,600.00 万元「本集团可自由支配的货币资金为人民币 8,600.00 万元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 与负债的对应' 1 '插入「可自由支配」' ; then
  run '红线③：拿受限金额当可动用金额 → 只红 RA-LINE' 1 "$WORK/bad-line-spend.md" 'RA-LINE'
fi

if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line-rating.md" \
  '## 与负债的对应' \
  '- 结论〔口径：本期末〕增持「我们给予公司增持评级，目标价 12.00 元」〔锚：2025 年年报·第 210 页·受限资产〕[S1]

## 与负债的对应' 1 '插入「增持评级／目标价」' ; then
  run '红线④：给评级与目标价 → 只红 RA-LINE' 1 "$WORK/bad-line-rating.md" 'RA-LINE'
fi

# 注入十三：整节删掉「货币资金受限」。RA-STRUCT 报缺节，RA-LINE 按规格也报（这一节是本件存在的理由）。
# 这一档专钉**双红**，不被并成单码——删节这种破坏确实同时违反两条判据，不是归属混了。
# RA-SUM 在这一档**必须不响**：缺节时它整条跳过（那是 STRUCT／LINE 的活），否则三红。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/bad-nosec-cash.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
i = t.index('## 货币资金受限')
j = t.index('## 非货币资产受限')
out = t[:i] + t[j:]
if out == t:
    sys.exit('注入点不在好样里')
Path(dst).write_text(out, encoding='utf-8')
PY
  if [ $? -eq 0 ]; then
    run '整节删掉货币资金受限 → 双红 RA-STRUCT＋RA-LINE（RA-SUM 不响）' 1 "$WORK/bad-nosec-cash.md" 'RA-LINE,RA-STRUCT'
  else
    echo '  不可判 删货币资金受限注入没落地'; unk=$((unk + 1))
  fi
fi

# 反证档：把「口径与未取到」那行口径说明改写成带红线词的形态，期望**零发条**。
# 口径节整节豁免：按设计它就要写「本件不判断资产质量与偿债能力、不把受限金额当作可动用金额」
# 这类话，不豁免会自己咬自己。这是全套里唯一期望 rc=0 的注入档——它证明「豁免真的生效」，
# 而不是靠好样恰好不含红线词。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/ok-gap-exempt.md" \
  '本件不重算可动用资金、不判断资产质量与偿债能力，也不把受限金额当作可动用金额。' \
  '本件不重算可动用资金、不判断资产质量好坏与偿债能力是否充足，也不把受限金额当作可动用金额或实际可用额度。' 0 '口径节写红线词（应豁免）' ; then
  run '反证：口径节写红线词 → 零发条（整节豁免）' 0 "$WORK/ok-gap-exempt.md" ''
fi

echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
