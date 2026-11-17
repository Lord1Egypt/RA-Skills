#!/usr/bin/env bash
# run_fixtures.sh — 公告速览的离线样例 runner（M653）
#
# 三档：① 机检自测 → ② 好样／坏样逐枚单跑（各发它该发的那道，不并成一个总数）→ ③ 边界形逐枚单跑。
# 零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp} 下自建目录，跑完即删。
# 退码：0 三档全合期望；1 有不合（逐枚点名，附真实退码与真实码集）；3 取值域故障
#       （脚本或夹具取不到、或某支注入没落地——不读成「零违例」）。
#
# 为什么每支注入都先断言「注入真的落地了」：注入字符串对不上夹具时，替换会静默产出原文，
# 于是「边界形该红没红」会被读成「机检漏判」，实际是尺子没被放上去。这类假红比漏判更贵，
# 所以注入后一律比字节，不一致即 exit 3。
#
# 一处照实读：本件第五道码在 check_digest.py 里就是不带前缀的 `FILLER`（另四道是 `F-STRUCT`
# 等），所以下面的取码式两种形都认、期望值也照实发写 `[FILLER]`——不为了统一好看去改尺子，
# 也不把「码名对不上」读成「没发码」。
#
# 两条尺的实话（照姊妹件 equity-incentive-plan-cn 0.1.3 的同一套规矩）：
#   * 注入点不能用「会连带触发别道码」的行——那样测出来的红分不清是哪道判的。本档每支注入
#     都挑该项自己那句话，并在下面逐支注明「该只红在 X」，跑出来的码集不对即判不合。
#   * 判「段在不在」的那道（F-STRUCT）按全文 re.search 判，只改标题而正文里还留着段名不算缺段，
#     所以「整节缺失」那支用的是全文替换、不是只换第一处。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_digest.py"
GOOD="$FIX/good-digest.md"
BAD="$FIX/bad-digest.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/announcement-daily-cn.XXXXXX")" || {
  echo "3 取值域故障：临时目录没建成（TMPDIR=${TMPDIR:-未设} 是否存在、可写？）"; exit 3; }
[ -d "$WORK" ] || { echo "3 取值域故障：临时目录不存在"; exit 3; }
trap 'rm -rf "$WORK"' EXIT

for f in "$CK" "$GOOD" "$BAD"; do
  [ -f "$f" ] || { echo "3 取值域故障：取不到 $f（不读成「夹具全过」）"; exit 3; }
done

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
# 全文替换、不是只换第一处：F-STRUCT 判「段在不在」用的是全文 re.search，
# 只改标题而正文里还留着段名，这一段照样算在——那样测出来的「没红」是注入没落地，不是机检漏判。
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
  codes="$(printf '%s\n' "$out" | grep -o '\[F-[A-Z]*\]\|\[FILLER\]' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样须过、坏样五道齐发、钉阈各钉一档、临时件自清）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
printf '%s\n' "$out" | tail -1
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ]; then echo '  → 合'; else echo '  → 不合'; bad=$((bad + 1)); fi

echo '档② 好样／坏样逐枚单跑'
tiers=$((tiers + 1))
run '好样 good-digest（零发条）' 0 "$GOOD" ''
run '坏样 bad-digest（STRUCT·ANCHOR·LINE·COUNT·FILLER 五道齐）' 1 "$BAD" \
  '[F-ANCHOR],[F-COUNT],[FILLER],[F-LINE],[F-STRUCT]'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 头部申报的数字对不上要点行数 → 该只红在 F-COUNT
if mutate "$GOOD" "$WORK/e-count.md" \
  '- 共 3 条' '- 共 4 条' '申报条数对不上要点行'; then
  run '申报「共 4 条」而要点 3 行 → 只红 F-COUNT' 1 "$WORK/e-count.md" '[F-COUNT]'
fi

# ② 第四段整节改名 → 该只红在 F-STRUCT
#    判段按全文 re.search，所以「同类前后串」每一处都得换掉才算真的缺段。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '同类前后串' '类别对照' '四段齐里的第三段改名（全文替换，标题＋正文一并）'; then
  run '「同类前后串」一节整段缺失 → 只红 F-STRUCT' 1 "$WORK/e-struct.md" '[F-STRUCT]'
fi

# ③ 要点行去掉「锚：」→ 该只红在 F-ANCHOR
if mutate "$GOOD" "$WORK/e-anchor.md" \
  ' 锚：巨潮资讯网 公告编号 2026-087 第 1 页' '' '要点行缺来源锚'; then
  run '要点行去掉「锚：」→ 只红 F-ANCHOR' 1 "$WORK/e-anchor.md" '[F-ANCHOR]'
fi

# ④ 公告标题去掉书名号 → 该只红在 F-ANCHOR（标题须逐字，书名号是形制）
if mutate "$GOOD" "$WORK/e-title.md" \
  '「关于控股股东增持股份进展的公告」' '关于控股股东增持股份进展的公告' '标题去书名号'; then
  run '公告标题去书名号 → 只红 F-ANCHOR' 1 "$WORK/e-title.md" '[F-ANCHOR]'
fi

# ⑤ 红线断言词落在没有 [待人工] 的行 → 该只红在 F-LINE（插一行，不动既有行，免得连带别道）
if mutate "$GOOD" "$WORK/e-line.md" \
  '## 三、同类前后串' '- 结论：目标价 12 元。

## 三、同类前后串' '非待人工行写目标价'; then
  run '「目标价 12 元」落在非待人工行 → 只红 F-LINE' 1 "$WORK/e-line.md" '[F-LINE]'
fi

# ⑥ 「未检索到」写成「无公告」→ 该只红在 F-COUNT
if mutate "$GOOD" "$WORK/e-lie.md" \
  '未检索到：本窗内' '无公告：本窗内' '同义词顶替未检索到'; then
  run '「未检索到」写成「无公告」→ 只红 F-COUNT' 1 "$WORK/e-lie.md" '[F-COUNT]'
fi

# ⑦ 引号槽内只剩单字 → 该只红在 FILLER
if mutate "$GOOD" "$WORK/e-fill1.md" \
  '«人民币 1,850 万元»' '«略»' '引号槽内只剩单字'; then
  run '关键数写成 «略» → 只红 FILLER' 1 "$WORK/e-fill1.md" '[FILLER]'
fi

# ⑧ 引号槽内为空 → 该只红在 FILLER
if mutate "$GOOD" "$WORK/e-fill2.md" \
  '«人民币 1,850 万元»' '«»' '引号槽内为空'; then
  run '关键数写成 «» → 只红 FILLER' 1 "$WORK/e-fill2.md" '[FILLER]'
fi

# ⑨ 值位整体留空 → 该只红在 FILLER
if mutate "$GOOD" "$WORK/e-fill3.md" \
  '要点：增持 «2,100 万股»，占总股本 0.52% 锚' '要点： 锚' '值位整体留空'; then
  run '值位整体留空 → 只红 FILLER' 1 "$WORK/e-fill3.md" '[FILLER]'
fi

# ⑩ 对照样：带 [待人工] 的行里写评级与目标价 → 须零发条（红线只禁「没挂待人工」的行）
if mutate "$GOOD" "$WORK/c-pending.md" \
  '## 三、同类前后串' '- [待人工] 上调评级与目标价 12 元，需人工确认。

## 三、同类前后串' '对照·待人工行不误伤'; then
  run '对照·[待人工] 行写评级与目标价不误伤（零发条）' 0 "$WORK/c-pending.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
