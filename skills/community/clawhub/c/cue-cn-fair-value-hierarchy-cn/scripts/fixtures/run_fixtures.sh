#!/usr/bin/env bash
# run_fixtures.sh — 公允价值层次登记稿的离线样例 runner
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
# **期望退码不写死**：从自测末行的「不可判=N」现算（N>0 ⇒ 3，N=0 ⇒ 0），与 OCI 那份 runner 同形。
# 写死 WANT_UNJUDGED=3 的形状是「今天对、三道落字后就错」——判据一补齐，runner 从该绿变常红，
# 逼下一个人去改断言而不是改判据。这里让它自己跟着走。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_fair_value.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-fair-value-hierarchy-cn.XXXXXX")" || {
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
# 码集从机检自己的输出里取（`FV-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
# 「不可判 FV-LEVEL（…）」那几行行首是「不可判」不是码，不会混进码集——这点是故意的：
# 未落字的道不该出现在「发了哪几道」里。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(FV-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
# 期望退码按末行现算：不可判=0 ⇒ 0（五道全落字），否则 ⇒ 3。这不放宽标准——末行仍要求 不合=0。
# 同时把「不可判=N」里的 N 取出来，档② 用同一个值，两份读数是同一次运行算出来的。
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
GOOD="$WORK/good-fv.md"
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

# 注入一：把「层次间转换」的节标题改成「层次间转换表」。
# 只该红 FV-STRUCT：该节既进不了 sections（算缺节），标题本身进 stray。
# 行形制没动、三元组齐全，FV-QUOTE 不红；未落字的三道本来就不判，不会因此冒出来。
# 替换型注入把原文片段吃掉，改完后旧标题片段应出现 0 次：这是「注入真的落地了」的断言，不是装饰。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-struct.md" \
  '## 层次间转换
' '## 层次间转换表
' 0 '把「层次间转换」节标题改成认不出的样子'; then
  run '节标题改字（缺节＋stray）→ 只红 FV-STRUCT' 1 "$WORK/bad-struct.md" 'FV-STRUCT'
fi

# 注入二：把「估值技术与输入值」节第一行的整段「」+〔锚〕摘掉，只留收尾 [S1]。
# 只该红 FV-QUOTE：原句与锚都没了，行形制仍合规（仍是 `- ` 行、该节仍有发现行）。
# 该行在「估值技术与输入值」节，不碰节标题也不碰来源节，FV-STRUCT 不红。
# 摘完该锚块片段应出现 0 次：注入落地断言。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-quote.md" \
  '「上市公司股票采用市场法估值，以活跃市场报价作为输入值」〔锚：2025 年年报·第 242 页·附注十·公允价值的披露〕[S1]' \
  '[S1]' 0 '摘掉估值技术行的「」+〔锚〕'; then
  run '发现行缺「」与〔锚〕→ 只红 FV-QUOTE' 1 "$WORK/bad-quote.md" 'FV-QUOTE'
fi

# 注入三：层次归属节里把登记值改成别的层次，原句仍写第三层次。
# 只该红 FV-LEVEL：形制完好、三元组完好、原句在场上只是与登记值不符。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-level.md" \
  '- 非上市股权 第三层次 5.00 亿元「' \
  '- 非上市股权 第一层次 5.00 亿元「' 0 '把登记值的层次改成第一层次（原句仍写第三层次）'; then
  run '登记值层次与原句不符 → 只红 FV-LEVEL' 1 "$WORK/bad-level.md" 'FV-LEVEL'
fi

# 注入四：估值技术节里登记值写收益法，原句写市场法。
# 只该红 FV-TECH：形状同注入三，动的是另一道的靶。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-tech.md" \
  '- 上市公司股票 市场法「上市公司股票采用市场法估值' \
  '- 上市公司股票 收益法「上市公司股票采用市场法估值' 0 '把登记值的估值技术改成收益法（原句仍写市场法）'; then
  run '登记值估值技术与原句不符 → 只红 FV-TECH' 1 "$WORK/bad-tech.md" 'FV-TECH'
fi

# 注入五：第三层次变动节里给发现行加一句「估值偏高」。
# 只该红 FV-LINE：发现行原句与锚都还在，只多了一个判断词。
# 该行不在「口径与未取到」节，所以不走整节豁免——豁免只保护那节的口径说明。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line.md" \
  '- 期初余额 6.00 亿元「第三层次公允价值计量项目的期初余额' \
  '- 期初余额 6.00 亿元 估值偏高「第三层次公允价值计量项目的期初余额' 0 '给发现行加一句「估值偏高」'; then
  run '正文自己下估值判断 → 只红 FV-LINE' 1 "$WORK/bad-line.md" 'FV-LINE'
fi

# 反证档：口径节里写「不轧净额」「不相抵」是这件的合法口径说明，整节豁免，必须零发条。
# 这一档不挂 mutate 的「片段次数」断言（它是插入型，原片段留在原处），
# 直接写好样副本再跑，期望零发条且码集为空。
if [ -f "$GOOD" ]; then
  python3 -B - "$GOOD" "$WORK/ok-gap.md" <<'PY'
import sys
from pathlib import Path
src, dst = sys.argv[1:3]
t = Path(src).read_text(encoding='utf-8')
old = '- 未取到：无'
if old not in t:
    sys.exit('注入点不在好样里')
Path(dst).write_text(t.replace(old, old + '\n- 口径补充：利息与股息不轧净额、数值不相抵，各占各行。', 1),
                     encoding='utf-8')
PY
  run '反证：口径节写「不轧净额」→ 零发条' 0 "$WORK/ok-gap.md" ''
fi
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
