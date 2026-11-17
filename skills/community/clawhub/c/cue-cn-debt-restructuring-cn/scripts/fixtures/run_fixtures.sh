#!/usr/bin/env bash
# run_fixtures.sh — 债务重组逐条挂源稿的离线样例 runner
#
# 三档：① 机检自测 → ② 好样（--demo 产物自过机检）→ ③ 坏样（在好样副本上只破一处，须只点名 DR-LINE）。
# 零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp} 下自建目录，跑完即删。
# 退码：0 三档全合期望；1 有不合（逐档点名，附真实退码与真实码集）；
#       3 取值域故障（脚本取不到、或某支注入没落地——不读成「零违例」）。
#
# 本包不带夹具文件：好样由机检自己的 --demo 现出，坏样在好样临时副本上注入。
# 所以档② 顺带证了 --demo 与机检判据同源（同一份文本，一支零发条、一支发条）。
#
# 为什么每支注入都先断言「注入真的落地了」：注入片段对不上好样时，替换会静默产出原文，
# 于是「该红没红」会被读成「机检漏判」，实际是尺子没被放上去。所以注入前后都数片段出现次数
# （注入前原片段须在场、注入后须归零，新片段须恰一枚），不符即计取值域故障（unk），不并入「不合」。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_debt_restructuring.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-debt-restructuring-cn.XXXXXX")" || {
  echo "3 取值域故障：临时目录没建成（TMPDIR=${TMPDIR:-未设} 是否存在、可写？）"; exit 3; }
[ -d "$WORK" ] || { echo "3 取值域故障：临时目录不存在"; exit 3; }
trap 'rm -rf "$WORK"' EXIT

[ -f "$CK" ] || { echo "3 取值域故障：取不到 $CK（不读成「夹具全过」）"; exit 3; }

bad=0
unk=0
tiers=0

# 一支注入：mutate <源件> <目标件> <原文片段> <替换片段> <标签>
# 失败（注入前原片段不在场、替换后原片段未归零、或替换后与源件同字节）＝ 取值域故障，不计入「不合」。
mutate() {
  local src="$1" dst="$2" old="$3" new="$4" tag="$5"
  if ! python3 -B - "$src" "$dst" "$old" "$new" <<'PY'
import sys
from pathlib import Path
src, dst, old, new = sys.argv[1:5]
t = Path(src).read_text(encoding='utf-8')
if old not in t:
    sys.exit('注入点不在好样里（改前未命中，尺子没放上去）')
out = t.replace(old, new, 1)
if out == t:
    sys.exit('替换后与源件同字节')
if old in out:
    sys.exit('替换后原片段仍在场（注入没覆盖干净）')
if new not in out:
    sys.exit('替换后新片段不在场（注入没落地）')
Path(dst).write_text(out, encoding='utf-8')
PY
  then
    echo "  不可判 $tag：注入没落地（片段对不上好样，不读成「机检漏判」）"
    unk=$((unk + 1)); return 1
  fi
  return 0
}

# 跑一枚：run <标签> <期望退码> <文件> <期望码集（空＝不发码）|*＝不核码集>
# 码集从机检自己的输出里取（`DR-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(DR-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
# 五道全实装后 selftest 的正常退码是 0。若将来某道回退成未实装，末行不可判会>0——
# 那种「尺子没接线却报零发条」的状态必须由 runner 自己拦住，不能靠读的人看末行。
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ] && printf '%s\n' "$out" | tail -1 | grep -q '不合=0.*不可判=0'; then
  echo '  → 合'
else
  echo '  → 不合'; bad=$((bad + 1))
fi

echo '档② 好样：--demo 产物自过机检（零发条）'
tiers=$((tiers + 1))
GOOD="$WORK/good-dr.md"
if python3 -B "$CK" --demo > "$GOOD" 2>"$WORK/demo.err" && [ -s "$GOOD" ]; then
  echo "  ok   --demo 产出 $([ -s "$GOOD" ] && wc -c < "$GOOD" | tr -d ' ') 字节"
  run '好样 demo 稿（零发条）' 0 "$GOOD" ''
else
  echo "  不可判 --demo 没产出文本（取值域故障，不读成「好样零发条」）"
  sed 's/^/      /' "$WORK/demo.err" 2>/dev/null
  unk=$((unk + 1))
fi

echo '档③ 坏样：在好样临时副本上只破一处，须只发 DR-LINE'
tiers=$((tiers + 1))

# 破法：取 DEMO 第三节「以资产清偿债务」里那条资产账面价值行，在**登记值**里插一句处置主张，
# 行末的「原句」〔锚〕[S#] 三元组一字不动。
# 为什么这样只红一道：
#   DR-QUOTE 看三元组与 [S#] 登记，这里一个字没少，不红；
#   DR-STRUCT 看行形制，仍是合法 `- ` 发现行，不红；
#   DR-MODE 看重组路径词（以资产清偿／债转股／修改条款），插入句里一个路径词都没有，不红；
#   DR-GAP 看「未取到」两向对账，这一行本就不是缺口行，不红；
#   DR-LINE 洗掉「」原句与〔锚〕后判登记值，命中「建议处置」——只有这一道该红。
# 注入前断言原片段在场、注入后断言归零，否则计取值域故障。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-line.md" \
  '资产账面价值：9,800.00 万元「' \
  '资产账面价值：9,800.00 万元，建议处置该厂房及土地使用权「' '登记值里插入处置主张'; then
  run '登记值写「建议处置」→ 只红 DR-LINE' 1 "$WORK/bad-line.md" 'DR-LINE'
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
