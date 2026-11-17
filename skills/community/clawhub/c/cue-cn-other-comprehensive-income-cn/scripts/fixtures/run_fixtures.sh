#!/usr/bin/env bash
# run_fixtures.sh — 其他综合收益判断稿的离线样例 runner
#
# 三档：① 机检自测 → ② 好样（--demo 产物自过机检）→ ③ 坏样（在好样上只破一处，须点名）。
# 零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp} 下自建目录，跑完即删。
# 退码：0 三档全合期望；1 有不合（逐档点名，附真实退码与真实码集）；
#       3 取值域故障（脚本取不到、或某支注入没落地——不读成「零违例」）。
#
# 本包不带夹具文件：好样由机检自己的 --demo 现出，坏样在好样临时副本上注入。
# 所以档② 顺带证了 --demo 与机检判据同源（同一份文本，一支零发条）。
#
# 档③ 做五道已落字判据的坏样：OCI-STRUCT／OCI-QUOTE／OCI-TAX／OCI-RECLASS／OCI-LINE 各至少一支，
# 另加一支反证（口径节写轧账口径须零发条）。
# 五道全部落字之后，拿任何一道做坏样都不是「钉一个还没接线的靶」；反过来，若某道将来回退成
# 空壳，它那一支会因「实发退码/码集不符」变红，runner 自己会把回退拦住。
#
# 期望退码不写死：机检现有未落字判据时好样必退 3，全部落字后才退 0。
# 档①② 的期望退码由 --selftest 末行自报的「不可判=N」现算，不手改。
#
# 为什么每支注入都先断言「注入真的落地了」：注入字符串对不上好样时，替换会静默产出原文，
# 于是「该红没红」会被读成「机检漏判」，实际是尺子没被放上去。所以注入后一律数片段出现次数，
# 不一致即计取值域故障（unk），不并入「不合」。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_other_comprehensive_income.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-other-comprehensive-income-cn.XXXXXX")" || {
  echo "3 取值域故障：临时目录没建成（TMPDIR=${TMPDIR:-未设} 是否存在、可写？）"; exit 3; }
[ -d "$WORK" ] || { echo "3 取值域故障：临时目录不存在"; exit 3; }
trap 'rm -rf "$WORK"' EXIT

[ -f "$CK" ] || { echo "3 取值域故障：取不到 $CK（不读成「夹具全过」）"; exit 3; }

bad=0
unk=0
tiers=0

# 一支注入：mutate <源件> <目标件> <原文片段> <替换片段> <期望片段次数> <标签>
# 失败（片段不在源件里、替换后与源件同字节、或替换后片段次数不符）＝ 取值域故障，不计入「不合」。
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
# 码集从机检自己的输出里取（`OCI-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(OCI-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes:-*}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样零发条、逐枚坏样各只发自己那道码、覆盖自证不缺口）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
last="$(printf '%s\n' "$out" | tail -1)"
printf '%s\n' "$last"
# 期望退码由末行现报的「不可判=N」算出来：N>0 ⇒ 3（有判据未落字，rc=0 不发放），N=0 ⇒ 0。
# 不写死的好处：落字一道，这里自己跟着从 3 变 0，不用手改；也不可能把「尺子没接线」读成过。
unk_n="$(printf '%s\n' "$last" | sed -n 's/.*不可判=\([0-9][0-9]*\).*/\1/p')"
if [ -z "$unk_n" ]; then
  echo '  不可判：末行取不到「不可判=N」（取值域故障，不读成合）'
  unk=$((unk + 1)); unk_n=x; want=x
else
  [ "$unk_n" -gt 0 ] && want=3 || want=0
fi
echo "  实发退码=$rc｜期望=$want（未落字 $unk_n 道，由末行现算）"
if [ "$want" != x ] && [ "$rc" -eq "$want" ] && printf '%s\n' "$last" | grep -q '不合=0'; then
  echo '  → 合'
else
  echo '  → 不合'; bad=$((bad + 1))
fi

echo '档② 好样：--demo 产物自过机检（零发条；退码随未落字判据走）'
tiers=$((tiers + 1))
GOOD="$WORK/good-oci.md"
if python3 -B "$CK" --demo > "$GOOD" 2>"$WORK/demo.err" && [ -s "$GOOD" ]; then
  echo "  ok   --demo 产出 $([ -s "$GOOD" ] && wc -c < "$GOOD" | tr -d ' ') 字节"
  run '好样 demo 稿（零发条）' "$want" "$GOOD" ''
else
  echo "  不可判 --demo 没产出文本（取值域故障，不读成「好样零发条」）"
  sed 's/^/      /' "$WORK/demo.err" 2>/dev/null
  unk=$((unk + 1))
fi

echo '档③ 坏样：在好样临时副本上只破一处，须各只发自己那道码'
tiers=$((tiers + 1))

# 注入一：头部删掉「不构成投资建议」这一件自标。
# 只该红 OCI-STRUCT：其余六件自标仍在、七节没动、发现行没动，不连带别的码。
# 删完整行里该自标应出现 0 次：这是「注入真的落地了」的断言，不是装饰。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct-mark.md" \
  '不构成投资建议' '' 0 '头部删掉「不构成投资建议」'; then
  run '头部缺自标 → 只红 OCI-STRUCT' 1 "$WORK/bad-struct-mark.md" 'OCI-STRUCT'
fi

# 注入二：把「税后净额明细」的节标题写成认不出的样子（尾接字母数字才算认不出；
# 全角括号那种写法 _section_of 仍认得出，实测过，别用）。
# 只该红 OCI-STRUCT：该节进不了 sections，算缺节，标题本身也进 stray。
# 注入片段要连行尾换行一起换掉：新标题「## 税后净额明细旧」里仍含旧片段，
# 只换标题文字的话 count 是 1 不是 0——那支正确的注入会被误报成「没落地」。
# 带上换行，旧片段被整行吃掉，替换后才应出现 0 次：注入落地断言。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct-heading.md" \
  '## 税后净额明细
' '## 税后净额明细旧
' 0 '节标题写成认不出的样子'; then
  run '节标题认不出（进 stray＋缺节）→ 只红 OCI-STRUCT' 1 "$WORK/bad-struct-heading.md" 'OCI-STRUCT'
fi

# 注入三：拆掉「期末余额」那行尾的〔锚〕[S#]，只留「」原句。
# 只该红 OCI-QUOTE：原句仍在、行仍是合法 `- ` 行，所以不连带 OCI-STRUCT。
# 拆完整行里该锚块应出现 0 次：注入落地断言。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '「截至 2025 年 12 月 31 日，本集团其他综合收益余额为人民币 4,067.50 万元」〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]' \
  '「截至 2025 年 12 月 31 日，本集团其他综合收益余额为人民币 4,067.50 万元」' 0 '拆掉期末余额行的三元组'; then
  run '发现行缺〔锚〕[S#] → 只红 OCI-QUOTE' 1 "$WORK/bad-quote.md" 'OCI-QUOTE'
fi

# 注入四：把 S2 的检索日写成斜杠式，该行不合格式、S2 不再算登记。
# 只该红 OCI-QUOTE：行格式发一条；正文里引用 [S2] 的几行也会发「引用了未登记的 S2」，
# 但同一个 S 号只报一次，码集仍是 {OCI-QUOTE}，不连带别的码。
# 改完后旧检索日片段应出现 0 次：注入落地断言。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-source-fmt.md" \
  'https://example.invalid/600000_2025_notes.pdf | 检索日 2026-03-20' \
  'https://example.invalid/600000_2025_notes.pdf | 检索日 2026/03/20' 0 '来源行检索日写成斜杠式'; then
  run '来源行检索日不合格式 → 只红 OCI-QUOTE' 1 "$WORK/bad-source-fmt.md" 'OCI-QUOTE'
fi

# 注入五：把某行登记值的税后净额 900.00 改成 975.00，同行原句一字不动（原句仍是 900.00）。
# 只该红 OCI-TAX：税前 1,200.00 与所得税影响 300.00 仍能在原句里找到，缺的只有税后净额那个数。
# 三元组完整，OCI-QUOTE 不红；该行在「税后净额明细」节，OCI-RECLASS 只判重分类节、OCI-LINE 无红线词。
# 替换型注入把旧片段吃掉，改完后旧片段应出现 0 次：注入落地断言。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-tax.md" \
  '税后净额 900.00 万元「' \
  '税后净额 975.00 万元「' 0 '登记值税后净额 900.00 改成 975.00'; then
  run '登记值一个数在原句里找不到 → 只红 OCI-TAX' 1 "$WORK/bad-tax.md" 'OCI-TAX'
fi

# 注入六：在某行登记值里加一个原句没有的去向词（登记值写「转入营业成本」，原句是「转入投资收益」）。
# 只该红 OCI-RECLASS：金额 260.00 原句仍有，多出来的只有去向词。
# 三元组完整，OCI-QUOTE 不红；该行在「重分类调整」节，另两道不认这一行。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-reclass.md" \
  '本期重分类进损益 260.00 万元「' \
  '本期重分类进损益 260.00 万元 转入营业成本「' 0 '登记值加一个原句没有的去向词'; then
  run '登记值去向词与原句不符 → 只红 OCI-RECLASS' 1 "$WORK/bad-reclass.md" 'OCI-RECLASS'
fi

# 注入七：在某内容节插一条带完整三元组的发现行，登记值写「与净利润合计」。
# 只该红 OCI-LINE。必须挂完整「」+〔锚〕+[S#]——否则 OCI-QUOTE 会一起红，那一档就钉不住「只红 OCI-LINE」。
# 插在「口径与未取到」节标题之前，落点是最后一个内容节，不算口径节，不该被整节豁免放过。
# 插入型注入的落地断言与替换型不同：插入是在片段前面添一行、片段本身留在原处，
# 所以替换后该片段仍应出现恰好 1 次。写 0 会把正确的注入误报成「没落地」。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line.md" \
  '## 口径与未取到' \
  '- 合计影响 其他综合收益与净利润合计影响所有者权益 4,067.50 万元「截至 2025 年 12 月 31 日，本集团其他综合收益余额为人民币 4,067.50 万元」〔锚：2025 年年报·第 188 页·合并所有者权益变动表〕[S1]

## 口径与未取到' 1 '内容节插入一条自写「与净利润合计」的行'; then
  run '发现行自写轧账口径 → 只红 OCI-LINE' 1 "$WORK/bad-line.md" 'OCI-LINE'
fi

# 反证（替换型）：把口径行改写成带两个红线词（「与净利润合计」「合计影响所有者权益」）的形态。
# 期望**零发条、码集为空、退 0**：口径节整节豁免。这一档防的是「红线词把口径说明也判了」——
# 口径节按设计就要讲轧账口径，不豁免会自己咬自己。
# 它是全套里唯一期望「不发码」的注入档；若哪天豁免被误删，这一档会红。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/ok-gap.md" \
  '- 口径：税前金额、所得税影响、税后净额与重分类金额一律照抄附注原文，本件不按 25% 税率或上期比例反算；其他综合收益与净利润不轧账。' \
  '- 口径：税前金额、所得税影响、税后净额与重分类金额一律照抄附注原文，本件不按 25% 税率或上期比例反算；附注亦未列示「与净利润合计」或「合计影响所有者权益」的口径，本件同样不轧账。' 0 '口径节写轧账口径（反证）'; then
  run '口径节写轧账口径 → 不发码（整节豁免）' 0 "$WORK/ok-gap.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
