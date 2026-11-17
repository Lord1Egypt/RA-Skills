#!/usr/bin/env bash
# run_fixtures.sh — 投资性房地产稿的离线样例 runner（M656）
#
# 三档：① 机检自测 → ② 好样（--demo 产物）单跑 → ③ 坏样注入单跑。
# 零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp} 下自建目录，跑完即删。
# 退码：0 三档全合期望；1 有不合（逐枚点名，附真实退码与真实码集）；
#       3 取值域故障（脚本取不到、或注入没落地——不读成「零违例」）。
#
# 为什么每支注入都先断言「注入真的落地了」：注入片段对不上夹具时，替换会静默产出原文，
# 于是「该红没红」会被读成「机检漏判」，实际是尺子没被放上去。这类假红比漏判更贵，
# 所以注入后一律比字节，不一致即 exit 3。
#
# 两条尺子的实话：
#   * 码集必须从机检**自己的输出**里取（`  IP-XXX L12 …` 的行首码），不另跑一份统计——
#     取的是「这枚稿实际发了哪几道」。
#   * 本包的注入只破一处、且破在**三元组**上：把一条发现行的「原句」与〔锚：…〕一起去掉，
#     该条只少三元组，项名与数值都还在，所以只该红 IP-QUOTE，不连带别道。
#     注入点不选「未取到」行：整行换掉会同时打断 IP-GAP 的两向对账，红分不清归属。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CK="$ROOT/scripts/check_investment_property.py"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cn-investment-property-cn.XXXXXX")" || {
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
out = t.replace(old, new)
if out == t:
    sys.exit('替换后与源件同字节')
Path(dst).write_text(out, encoding='utf-8')
PY
  then
    echo "  不可判 $tag：注入没落地（片段对不上夹具，不读成「机检漏判」）"
    unk=$((unk + 1)); return 1
  fi
  return 0
}

# 跑一枚：run <标签> <期望退码> <文件> <期望码集（空＝不发码）|*＝不核码集>
run() {
  local tag="$1" want="$2" f="$3" wantcodes="${4:-*}" out rc codes
  out="$(python3 -B "$CK" "$f" 2>&1)"; rc=$?
  codes="$(printf '%s\n' "$out" | sed -n 's/^ *\(IP-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样须过、五道各一支坏样、反证样不误伤）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
printf '%s\n' "$out" | tail -1
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ]; then echo '  → 合'; else echo '  → 不合'; bad=$((bad + 1)); fi

echo '档② 好样（--demo 产物逐枚单跑）'
tiers=$((tiers + 1))
if python3 -B "$CK" --demo > "$WORK/good.md" 2>"$WORK/demo.err"; then
  [ -s "$WORK/good.md" ] || { echo '  不可判 好样：--demo 出的是空稿'; unk=$((unk + 1)); }
  run '好样 --demo 产物（零发条）' 0 "$WORK/good.md" ''
else
  echo "  不可判 好样：--demo 没跑成"; sed 's/^/      /' "$WORK/demo.err"
  unk=$((unk + 1))
fi

echo '档③ 坏样单跑（注入先断言落地；只破三元组一处）'
tiers=$((tiers + 1))

# ① 一条发现行丢原句与锚 → 该只红在 IP-QUOTE
if mutate "$WORK/good.md" "$WORK/e-quote.md" \
  '「投资性房地产原值 112,000,000.00 元」〔锚：2025 年年报·第 96 页·附注五·投资性房地产〕[S1]' \
  '' '发现行丢原句与锚'; then
  run '成本模式原值行丢了原句与锚 → 只红 IP-QUOTE' 1 "$WORK/e-quote.md" 'IP-QUOTE'
fi

# ② 对照样：三元组完好不动 → 须零发条（证明上面那支红是注入带来的，不是尺子恒真）
if cp "$WORK/good.md" "$WORK/c-intact.md"; then
  run '对照·好样原封不动（零发条）' 0 "$WORK/c-intact.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
