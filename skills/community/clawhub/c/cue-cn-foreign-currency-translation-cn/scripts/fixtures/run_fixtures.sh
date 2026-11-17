#!/usr/bin/env bash
# run_fixtures.sh — 外币折算稿的离线样例 runner
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
# 于是「该红没红」会被读成「机检漏判」，实际是尺子没被放上去。所以注入后一律比字节，
# 不一致即计取值域故障（unk），不并入「不合」。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_foreign_currency.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-foreign-currency-translation-cn.XXXXXX")" || {
  echo "3 取值域故障：临时目录没建成（TMPDIR=${TMPDIR:-未设} 是否存在、可写？）"; exit 3; }
[ -d "$WORK" ] || { echo "3 取值域故障：临时目录不存在"; exit 3; }
trap 'rm -rf "$WORK"' EXIT

[ -f "$CK" ] || { echo "3 取值域故障：取不到 $CK（不读成「夹具全过」）"; exit 3; }

bad=0
unk=0
tiers=0

# 一支注入：mutate <源件> <目标件> <原文片段> <替换片段> <标签>
# 失败（片段不在源件里、或替换后与源件同字节）＝ 取值域故障，不计入「不合」。
mutate() {
  local src="$1" dst="$2" old="$3" new="$4" tag="$5"
  if ! python3 -B - "$src" "$dst" "$old" "$new" <<'PY'
import sys
from pathlib import Path
src, dst, old, new = sys.argv[1:5]
t = Path(src).read_text(encoding='utf-8')
if old not in t:
    sys.exit('注入点不在源件里')
out = t.replace(old, new, 1)
if out == t:
    sys.exit('替换后与源件同字节')
Path(dst).write_text(out, encoding='utf-8')
PY
  then
    echo "  不可判 $tag：注入没落地（片段对不上好样，不读成「机检漏判」）"
    unk=$((unk + 1)); return 1
  fi
  return 0
}

# 跑一枚：run <标签> <期望退码> <文件> <期望码集（空＝不发码）|*＝不核码集>
# 码集从机检自己的输出里取（`  FX-XXX L12 …` 的行首码），不另跑一份统计：
# 取的是**这枚稿实际发了哪几道**，不是「我以为它发了哪几道」。
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(FX-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
GOOD="$WORK/good-fx.md"
if python3 -B "$CK" --demo > "$GOOD" 2>"$WORK/demo.err" && [ -s "$GOOD" ]; then
  echo "  ok   --demo 产出 $([ -s "$GOOD" ] && wc -c < "$GOOD" | tr -d ' ') 字节"
  run '好样 demo 稿（零发条）' 0 "$GOOD" ''
else
  echo "  不可判 --demo 没产出文本（取值域故障，不读成「好样零发条」）"
  sed 's/^/      /' "$WORK/demo.err" 2>/dev/null
  unk=$((unk + 1))
fi

echo '档③ 坏样：在好样临时副本上只破一处，须只发 FX-NOSELF'
tiers=$((tiers + 1))

# 注入点选一条**已有完整三元组**的发现行之后追加一行：正文断言「公允价值模式」，
# 而它引的原句写的是「成本模式」——计量模式只认原句，这行属自推。
# 追加行自带三元组与 [S2]（S2 已在来源节登记），所以只该红 FX-NOSELF：
# 不连带 FX-QUOTE（三元组齐）、不连带 FX-STRUCT（节内仍全是 `- ` 发现行、无新增节）。
if [ -f "$GOOD" ] && mutate "$GOOD" "$WORK/bad-noself.md" \
  '- 境外子公司记账本位币 美元「乙公司以美元为记账本位币」〔锚：2025 年年报·第 159 页·附注七·境外经营〕[S2]' \
  '- 境外子公司记账本位币 美元「乙公司以美元为记账本位币」〔锚：2025 年年报·第 159 页·附注七·境外经营〕[S2]
- 投资性房地产后续计量 公允价值模式「投资性房地产按成本模式进行后续计量」〔锚：2025 年年报·第 159 页·附注七·投资性房地产〕[S2]' \
  '计量模式自推'; then
  run '正文断「公允价值模式」而原句写「成本模式」→ 只红 FX-NOSELF' 1 "$WORK/bad-noself.md" 'FX-NOSELF'
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
