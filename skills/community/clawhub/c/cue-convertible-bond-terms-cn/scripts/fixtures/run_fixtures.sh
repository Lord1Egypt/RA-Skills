#!/usr/bin/env bash
# run_fixtures.sh — 可转债条款卡的离线样例 runner（M646）
#
# 三档：① 机检自测 → ② 好样／坏样逐枚单跑（各发它该发的那道，不并成一个总数）→ ③ 边界形逐枚单跑。
# 零网络、零计费、纯标准库；产物只落 ${TMPDIR:-/tmp} 下自建目录，跑完即删。
# 退码：0 三档全合期望；1 有不合（逐枚点名，附真实退码与真实码集）；3 取值域故障
#       （脚本或夹具取不到、或某支注入没落地——不读成「零违例」）。
#
# 为什么每支注入都先断言「注入真的落地了」：注入字符串对不上夹具时，sed 静默产出原文，
# 于是「边界形该红没红」会被读成「机检漏判」，实际是尺子没被放上去。这类假红比漏判更贵，
# 所以注入后一律比字节，不一致即 exit 3。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_cb_card.py"
GOOD="$FIX/good-cb-card.md"
BAD="$FIX/bad-cb-card.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/convertible-bond-terms-cn.XXXXXX")" || {
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
# 全文替换、不是只换第一处：机检判「段在不在」用的是全文 re.search，
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
  codes="$(printf '%s\n' "$out" | grep -o '\[CB-[A-Z]*\]' | sort -u | tr '\n' ',' | sed 's/,$//')"
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
run '好样 good-cb-card（零发条）' 0 "$GOOD" ''
run '坏样 bad-cb-card（CB-COUNT·CB-LINE·CB-QUOTE·CB-STRUCT·CB-TRIG 五道齐）' 1 "$BAD" '[CB-COUNT],[CB-LINE],[CB-QUOTE],[CB-STRUCT],[CB-TRIG]'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地）'
tiers=$((tiers + 1))

# ① 强赎触发线换成空泛语 → 该红在 CB-TRIG
if mutate "$GOOD" "$WORK/e-vague.md" \
  '「可转债转股日起二十个交易日后，若公司股票收盘价格不低于当期转股价格的 130%，发行人有权赎回」' \
  '「满足约定条件时，发行人有权赎回」' '空泛语顶替强赎触发线'; then
  run '强赎触发线写「满足约定条件」→ CB-TRIG' 1 "$WORK/e-vague.md" '[CB-TRIG]'
fi

# ② 别项的触发句塞进回售项 → 该红在 CB-TRIG（归属核验：窗口内出现别项触发语）
if mutate "$GOOD" "$WORK/e-cross.md" \
  '「最后两个计息年度，股票收盘价连续三十个交易日低于当期转股价格的 70% 时，持有人可回售」' \
  '「最后两个计息年度，若公司股票收盘价格不低于当期转股价格的 130%，发行人有权赎回」' '赎回触发句塞进回售项'; then
  run '赎回触发句塞进回售项→ CB-TRIG（归属不认）' 1 "$WORK/e-cross.md" '[CB-TRIG]'
fi

# ③ 价钱冒充触发线 → 该红在 CB-TRIG
if mutate "$GOOD" "$WORK/e-price.md" \
  '「最后两个计息年度，股票收盘价连续三十个交易日低于当期转股价格的 70% 时，持有人可回售」' \
  '「回售价格为面值的 100%」' '价钱冒充触发线'; then
  run '「回售价格为面值的 100%」→ CB-TRIG（价钱不是触发线）' 1 "$WORK/e-price.md" '[CB-TRIG]'
fi

# ④ 「未检索到」写成同义词 → 该红在 CB-COUNT（并连带 CB-QUOTE）
if mutate "$GOOD" "$WORK/e-syn.md" \
  '- 担保与评级：未检索到（缺数清单已点名）' \
  '- 担保与评级：无该项' '同义词顶替未检索到'; then
  run '「未检索到」写成「无该项」→ CB-COUNT' 1 "$WORK/e-syn.md" '[CB-COUNT],[CB-QUOTE]'
fi

# ⑤ 齐缺申报与清单不对账 → 该红在 CB-COUNT
if mutate "$GOOD" "$WORK/e-count.md" '共八项·缺 1 项' '共八项·缺 0 项' '齐缺申报对不上清单'; then
  run '申报缺 0 项但清单有 1 项 → CB-COUNT' 1 "$WORK/e-count.md" '[CB-COUNT]'
fi

# ⑥ 原句清空 → 该红在 CB-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「初始转股价格不低于募集说明书公告日前二十个交易日均价，且不高于前一个交易日均价」' '「」' '原句清空'; then
  run '项行原句清空 → CB-QUOTE' 1 "$WORK/e-quote.md" '[CB-QUOTE]'
fi

# ⑦ 锚值清空 → 该红在 CB-QUOTE
if mutate "$GOOD" "$WORK/e-anchor.md" '锚：募集说明书 第二节 修正条款' '锚：' '锚值为空'; then
  run '锚标签在而锚值为空 → CB-QUOTE' 1 "$WORK/e-anchor.md" '[CB-QUOTE]'
fi

# ⑧ 缺一节 → 该红在 CB-STRUCT
# 机检按「段名在全文出现过」判段在不在（re.search 全文，不锚标题），
# 所以只改标题不够——必须把「缺数清单」这个词的每一处都换掉，才真的算缺段。
if mutate "$GOOD" "$WORK/e-struct.md" '缺数清单' '缺项记录' '五段齐里的第四节改名（全文替换，标题＋正文一并）'; then
  run '「缺数清单」一节整段缺失 → CB-STRUCT' 1 "$WORK/e-struct.md" '[CB-STRUCT]'
fi

# ⑨ 自裁效力判断 → 该红在 CB-LINE（插一行，不替换既有行——否则连带 CB-COUNT／CB-QUOTE，测不出归属）
if mutate "$GOOD" "$WORK/e-judge.md" '## 三、口径对照' \
  '- 一句本件自己的话：综上，本次担保条款无效

## 三、口径对照' '自裁效力判断'; then
  run '「综上…无效」落在非待人工行 → CB-LINE（且只这一道）' 1 "$WORK/e-judge.md" '[CB-LINE]'
fi

# ⑩ 对照样：机构名里的「会」是名词后缀，不该被当判断语气 → 须零发条
if mutate "$GOOD" "$WORK/c-board.md" '## 三、口径对照' \
  '- 公告原文：「赎回价格由董事会拟定」 锚：募集说明书 第二节 赎回条款

## 三、口径对照' '对照·董事会不误伤'; then
  run '对照·「赎回价格由董事会拟定」不误伤（零发条）' 0 "$WORK/c-board.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
