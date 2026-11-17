#!/usr/bin/env bash
# run_fixtures.sh — 债券条款卡的离线样例 runner（M653）
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
# 两条尺的实话：
#   * 注入点不能用「会连带触发别道码」的行——那样测出来的红分不清是哪道判的。本档每支注入
#     都挑该项自己那句话，并在下面逐支注明「该只红在 X」，跑出来的码集不对即判不合。
#     实测踩到过：好样里「锚：第二节 发行条款」出现 4 次，拿它做「删锚」的替换点会一次红 4 行，
#     分不清是「这一行的锚没了」还是「整段锚都洗掉了」——所以删锚那支改用只出现 1 次的
#     「锚：第四节 增信机制」。
#   * 判「段在不在」的那道（B-STRUCT）按全文 re.search 判，只改标题而正文里还留着段名不算缺段，
#     所以「整节缺失」那支用的是全文替换、不是只换第一处。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_bond_card.py"
GOOD="$FIX/good-bond-card.md"
BAD="$FIX/bad-bond-card.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/bond-terms-cn.XXXXXX")" || {
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
# 全文替换、不是只换第一处：B-STRUCT 判「段在不在」用的是全文 re.search，
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
  codes="$(printf '%s\n' "$out" | grep -o '\[B-[A-Z]*\]' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样须过、坏样六道齐发、钉阈各钉一档、临时件自清）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
printf '%s\n' "$out" | tail -1
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ]; then echo '  → 合'; else echo '  → 不合'; bad=$((bad + 1)); fi

echo '档② 好样／坏样逐枚单跑'
tiers=$((tiers + 1))
run '好样 good-bond-card（零发条）' 0 "$GOOD" ''
run '坏样 bad-bond-card（STRUCT·QUOTE·LINE·COUNT·VALUE·RATING 六道齐）' 1 "$BAD" \
  '[B-COUNT],[B-LINE],[B-QUOTE],[B-RATING],[B-STRUCT],[B-VALUE]'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 齐缺申报改数 → 该只红在 B-COUNT
if mutate "$GOOD" "$WORK/e-count.md" \
  '- 共八项·缺 1 项' '- 共八项·缺 0 项' '齐缺申报对不上清单'; then
  run '申报缺 0 项但速读段有 1 行未检索到 → 只红 B-COUNT' 1 "$WORK/e-count.md" '[B-COUNT]'
fi

# ② 「口径对照」整节改名 → 该只红在 B-STRUCT
#    判段按全文 re.search，所以必须每一处都换掉才算真的缺段。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '口径对照' '口径比对' '五段齐里的第三段改名（全文替换，标题＋正文一并）'; then
  run '「口径对照」一节整段缺失 → 只红 B-STRUCT' 1 "$WORK/e-struct.md" '[B-STRUCT]'
fi

# ③ 八项名目之一改名（不再以「- 名目：」起头）→ 该只红在 B-STRUCT（名目行级在场）
if mutate "$GOOD" "$WORK/e-item.md" \
  '- 发行价格与计息方式：' '- 发行价格计息方式：' '名目行改名后不在场'; then
  run '名目「发行价格与计息方式」行级不在场 → 只红 B-STRUCT' 1 "$WORK/e-item.md" '[B-STRUCT]'
fi

# ④ 锚值清空 → 该只红在 B-QUOTE
#    替换点选全文只出现 1 次的锚（「锚：第二节 发行条款」出现 4 次，用它会让 4 行一起红，分不清归属）。
if mutate "$GOOD" "$WORK/e-anchor.md" \
  ' 锚：第四节 增信机制' ' 锚：' '锚标签在而锚值为空'; then
  run '锚标签在而锚值为空 → 只红 B-QUOTE' 1 "$WORK/e-anchor.md" '[B-QUOTE]'
fi

# ⑤ 项行书名号内只剩单字 → 该只红在 B-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「按面值平价发行，采用单利按年计息」' '「略」' '原句占位只剩单字'; then
  run '原句写成「略」→ 只红 B-QUOTE' 1 "$WORK/e-quote.md" '[B-QUOTE]'
fi

# ⑥ 发行规模写成推定语 → 该只红在 B-VALUE
if mutate "$GOOD" "$WORK/e-v1.md" \
  '「本期债券发行规模为人民币 10 亿元，期限 5 年」' '「待定」' '规模写「待定」'; then
  run '发行规模写「待定」→ 只红 B-VALUE' 1 "$WORK/e-v1.md" '[B-VALUE]'
fi

# ⑦ 票面利率写成推定语 → 该只红在 B-VALUE
if mutate "$GOOD" "$WORK/e-v2.md" \
  '「票面利率 3.20%，按年付息」' '「询价」' '利率写「询价」'; then
  run '票面利率写「询价」→ 只红 B-VALUE' 1 "$WORK/e-v2.md" '[B-VALUE]'
fi

# ⑧ 评级符号 AAA 裸奔（同句无锚、非 [待人工]）→ 该只红在 B-RATING
if mutate "$GOOD" "$WORK/e-r1.md" \
  '## 四、缺数清单' '- 主体评级 AAA，展望稳定。

## 四、缺数清单' '评级符号 AAA 裸奔'; then
  run '主体评级 AAA 同句无锚 → 只红 B-RATING' 1 "$WORK/e-r1.md" '[B-RATING]'
fi

# ⑨ 评级符号 AA+ 裸奔（走另一条正则分支，单钉一档）→ 该只红在 B-RATING
if mutate "$GOOD" "$WORK/e-r2.md" \
  '## 四、缺数清单' '- 债项评级 AA+。

## 四、缺数清单' '评级符号 AA+ 裸奔'; then
  run '债项评级 AA+ 同句无锚 → 只红 B-RATING' 1 "$WORK/e-r2.md" '[B-RATING]'
fi

# ⑩ 红线定式词落在非待人工行 → 该只红在 B-LINE（插一行，不动既有行，免得连带别道）
if mutate "$GOOD" "$WORK/e-l1.md" \
  '## 四、缺数清单' '- 说明：建议买入。

## 四、缺数清单' '非待人工行写建议买入'; then
  run '「建议买入」落在非待人工行 → 只红 B-LINE' 1 "$WORK/e-l1.md" '[B-LINE]'
fi

# ⑪ 目标价位落在非待人工行 → 该只红在 B-LINE
if mutate "$GOOD" "$WORK/e-l2.md" \
  '## 四、缺数清单' '- 说明：目标价 110 元。

## 四、缺数清单' '非待人工行写目标价'; then
  run '「目标价 110 元」落在非待人工行 → 只红 B-LINE' 1 "$WORK/e-l2.md" '[B-LINE]'
fi

# ⑫ 「未检索到」写成「无该项」→ 该只红在 B-COUNT
if mutate "$GOOD" "$WORK/e-lie.md" \
  '## 四、缺数清单' '## 四、缺数清单
- 违约与交叉违约：无该项内容。' '同义词顶替未检索到'; then
  run '「未检索到」写成「无该项」→ 只红 B-COUNT' 1 "$WORK/e-lie.md" '[B-COUNT]'
fi

# ⑬ 对照样：带 [待人工] 的行里写估值与建议买入 → 须零发条
if mutate "$GOOD" "$WORK/c-pending.md" \
  '## 四、缺数清单' '- [待人工] 债项估值与建议买入留人工。

## 四、缺数清单' '对照·待人工行不误伤'; then
  run '对照·[待人工] 行写债项估值与建议买入不误伤（零发条）' 0 "$WORK/c-pending.md" ''
fi

# ⑭ 对照样：评级符号同句带锚 → 须零发条（B-RATING 只禁「同句无锚」）
if mutate "$GOOD" "$WORK/c-rating.md" \
  '## 四、缺数清单' '- 主体评级 AAA 锚：评级报告 第 1 页

## 四、缺数清单' '对照·评级符号带锚不误伤'; then
  run '对照·评级符号同句带锚不误伤（零发条）' 0 "$WORK/c-rating.md" ''
fi

# ⑮ 对照样：发行价格带数字原值 → 须零发条（B-VALUE 只钉规模与利率两项，不误伤其它项的数）
if mutate "$GOOD" "$WORK/c-price.md" \
  '「按面值平价发行，采用单利按年计息」' '「按面值 100 元平价发行，采用单利按年计息」' '对照·发行价格带数不误伤'; then
  run '对照·发行价格写「按面值 100 元」不误伤（零发条）' 0 "$WORK/c-price.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
