#!/usr/bin/env bash
# run_fixtures.sh — 每股收益判断稿的离线样例 runner
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
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_eps.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-eps-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`EP-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(EP-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes:-*}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样零发条、逐枚坏样各只发自己那道码、反证样不误伤）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
printf '%s\n' "$out" | tail -1
# 五道全实装后 selftest 的正常退码是 0。若将来某道回退成未实装，这里会因末行不可判>0 而红——
# 那种「尺子没接线却报零发条」的状态必须由 runner 自己拦住，不能靠读的人看末行。
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ] && printf '%s\n' "$out" | tail -1 | grep -q '不合=0.*不可判=0'; then
  echo '  → 合'
else
  echo '  → 不合'; bad=$((bad + 1))
fi

echo '档② 好样：--demo 产物自过机检（零发条）'
tiers=$((tiers + 1))
GOOD="$WORK/good-eps.md"
if python3 -B "$CK" --demo > "$GOOD" 2>"$WORK/demo.err" && [ -s "$GOOD" ]; then
  echo "  ok   --demo 产出 $([ -s "$GOOD" ] && wc -c < "$GOOD" | tr -d ' ') 字节"
  run '好样 demo 稿（零发条）' 0 "$GOOD" ''
else
  echo "  不可判 --demo 没产出文本（取值域故障，不读成「好样零发条」）"
  sed 's/^/      /' "$WORK/demo.err" 2>/dev/null
  unk=$((unk + 1))
fi

echo '档③ 坏样：在好样临时副本上只破一处，须各只发自己那道码'
tiers=$((tiers + 1))

# 注入一：拆掉「列报位置」那条发现行尾的〔锚〕[S#]，只留「」原句。
# 只该红 EP-QUOTE：原句仍在、行仍是合法 `- ` 行，所以不连带 EP-STRUCT；
# 该项名不属于净利润／股数／基本每股收益三族，也不含潜在普通股与调整项词，
# 所以不连带 EP-CALC／EP-DILUTE；行内没有红线词，EP-LINE 不红。
# 拆完整行里该锚块应出现 0 次：这是「注入真的落地了」的断言，不是装饰。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '「每股收益在利润表内单独列示」〔锚：2025 年年报·第 78 页·附注九·每股收益〕[S1]' \
  '「每股收益在利润表内单独列示」' 0 '拆掉列报位置行的三元组'; then
  run '发现行缺〔锚〕[S#] → 只红 EP-QUOTE' 1 "$WORK/bad-quote.md" 'EP-QUOTE'
fi

# 注入二：把「基本每股收益」节里归属净利润的登记数改成 17,300.00 万元，原句一字不动。
# 只该红 EP-CALC：原句仍是 172,000,000.00 元，登记数与它对不上；
# 三元组完整，EP-QUOTE 不红；行形制没动，EP-STRUCT 不红；该项名不沾稀释调整项词。
# 改完后旧登记值片段应出现 0 次：注入落地断言。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-calc.md" \
  '- 归属于普通股股东的净利润：17,200.00 万元「' \
  '- 归属于普通股股东的净利润：17,300.00 万元「' 0 '把归属净利润登记数改成 17,300.00 万元'; then
  run '登记数与原句对不上 → 只红 EP-CALC' 1 "$WORK/bad-calc.md" 'EP-CALC'
fi

# 注入三：在「股数与调整」节里插一条带完整三元组的目标价行。
# 只该红 EP-LINE：三元组齐全，EP-QUOTE 不红；行形制没动，EP-STRUCT 不红；
# 项名「机构观点」不带净利润／股数／基本每股收益／调整项／潜在普通股词，
# EP-CALC 与 EP-DILUTE 都不认这一行。
# 插入型注入的落地断言与替换型不同：替换把原文片段吃掉（期望 0 次），插入是**在片段前面
# 添一行、片段本身留在原处**，所以替换后该片段仍应出现恰好 1 次。写 0 会把这支正确的注入
# 误报成「没落地」——断言得按注入的实际形状写，不能照抄替换型那一档。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line.md" \
  '- 报告期内股本变动：' \
  '- 机构观点：目标价 12.50 元「机构给出目标价 12.50 元」〔锚：2025 年年报·第 80 页〕[S1]
- 报告期内股本变动：' 1 '插入一条目标价行'; then
  run '正文写目标价 → 只红 EP-LINE' 1 "$WORK/bad-line.md" 'EP-LINE'
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
