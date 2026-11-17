#!/usr/bin/env bash
# run_fixtures.sh — 股权激励条款卡的离线样例 runner（M647）
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
# 两条尺子的实话（第一版在这两格上翻过车，记在 CHANGELOG 0.1.0 与 6.1 各轮修账里）：
#   * 注入点不能用「会连带触发别道码」的行——那样测出来的红分不清是哪道判的。本档每支注入
#     都挑该项自己那句话，并在下面逐支注明「该只红在 X」，跑出来的码集不对即判不合。
#   * 判「段在不在」的那道（EIP-STRUCT）按全文 re.search 判，只改标题而正文里还留着段名不算缺段，
#     所以「整节缺失」那支用的是全文替换、不是只换第一处。
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIX="$ROOT/scripts/fixtures"
CK="$ROOT/scripts/check_eip_card.py"
GOOD="$FIX/good-eip-card.md"
BAD="$FIX/bad-eip-card.md"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/equity-incentive-plan-cn.XXXXXX")" || {
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
# 全文替换、不是只换第一处：EIP-STRUCT 判「段在不在」用的是全文 re.search，
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
  codes="$(printf '%s\n' "$out" | grep -o '\[EIP-[A-Z]*\]' | sort -u | tr '\n' ',' | sed 's/,$//')"
  if [ "$rc" -eq "$want" ] && { [ "$wantcodes" = '*' ] || [ "$codes" = "$wantcodes" ]; }; then
    echo "  ok   $tag（退码 $rc｜码 ${codes:-无}）"
    return 0
  fi
  echo "  不合 $tag：期望退码 $want／码 ${wantcodes}，实发退码 $rc／码 ${codes:-无}"
  printf '%s\n' "$out" | sed 's/^/      /'
  bad=$((bad + 1)); return 1
}

echo '档① 机检自测（好样须过、坏样五道齐发、钉阈各钉一档、对照样不误伤、临时件自清）'
tiers=$((tiers + 1))
out="$(cd "$ROOT" && python3 -B "$CK" --selftest 2>&1)"; rc=$?
printf '%s\n' "$out" | tail -1
echo "  实发退码=$rc｜期望=0"
if [ "$rc" -eq 0 ]; then echo '  → 合'; else echo '  → 不合'; bad=$((bad + 1)); fi

echo '档② 好样／坏样逐枚单跑'
tiers=$((tiers + 1))
run '好样 good-eip-card（零发条）' 0 "$GOOD" ''
run '坏样 bad-eip-card（EIP-STRUCT·QUOTE·LINE·COUNT·PRICE 五道齐）' 1 "$BAD" \
  '[EIP-COUNT],[EIP-LINE],[EIP-PRICE],[EIP-QUOTE],[EIP-STRUCT]'

echo '档③ 边界形逐枚单跑（每支注入都先断言落地；每支只用该项自己那句话做替换点）'
tiers=$((tiers + 1))

# ① 齐缺申报改数 → 该只红在 EIP-COUNT
if mutate "$GOOD" "$WORK/e-count.md" \
  '- 共八项·缺 1 项' '- 共八项·缺 0 项' '齐缺申报对不上清单'; then
  run '申报缺 0 项但清单有 1 项 → 只红 EIP-COUNT' 1 "$WORK/e-count.md" '[EIP-COUNT]'
fi

# ② 「未检索到」写成同义词 → 该红在 EIP-COUNT（并连带 EIP-QUOTE：原句位也跟着空）
if mutate "$GOOD" "$WORK/e-syn.md" \
  '- 审议程序与披露义务：未检索到（缺数清单已点名）' \
  '- 审议程序与披露义务：无该项' '同义词顶替未检索到'; then
  run '「未检索到」写成「无该项」→ EIP-COUNT（连带 QUOTE）' 1 "$WORK/e-syn.md" '[EIP-COUNT],[EIP-QUOTE]'
fi

# ③ 五段齐里的第四节整节缺失 → 该只红在 EIP-STRUCT
#    判段按全文 re.search，所以必须把「缺数清单」每一处都换掉才算真的缺段。
if mutate "$GOOD" "$WORK/e-struct.md" \
  '缺数清单' '缺项记录' '五段齐里的第四节改名（全文替换，标题＋正文一并）'; then
  run '「缺数清单」一节整段缺失 → 只红 EIP-STRUCT' 1 "$WORK/e-struct.md" '[EIP-STRUCT]'
fi

# ④ 项行原句清空 → 该只红在 EIP-QUOTE
if mutate "$GOOD" "$WORK/e-quote.md" \
  '「本计划采取限制性股票与股票期权两种形式，标的股票来源为公司向激励对象定向发行的 A 股普通股」' \
  '「」' '原句清空'; then
  run '项行原句清空 → 只红 EIP-QUOTE' 1 "$WORK/e-quote.md" '[EIP-QUOTE]'
fi

# ⑤ 锚标签在而锚值为空 → 该只红在 EIP-QUOTE
if mutate "$GOOD" "$WORK/e-anchor.md" \
  '锚：草案 第一章 第二节' '锚：' '锚值为空'; then
  run '锚标签在而锚值为空 → 只红 EIP-QUOTE' 1 "$WORK/e-anchor.md" '[EIP-QUOTE]'
fi

# ⑥ 授予价格换成空泛语 → 该只红在 EIP-PRICE
if mutate "$GOOD" "$WORK/e-vague.md" \
  '「限制性股票授予价格为每股 12.60 元，不低于草案公告前 1 个交易日公司股票均价 25.20 元的 50%」' \
  '「授予价格由董事会确定」' '空泛语顶替授予价格'; then
  run '授予价格写「由董事会确定」→ 只红 EIP-PRICE' 1 "$WORK/e-vague.md" '[EIP-PRICE]'
fi

# ⑦ 市价冒充授予价 → 该只红在 EIP-PRICE
if mutate "$GOOD" "$WORK/e-mkt.md" \
  '「限制性股票授予价格为每股 12.60 元，不低于草案公告前 1 个交易日公司股票均价 25.20 元的 50%」' \
  '「授予价格参考市场价 30 元」' '市价冒充授予价'; then
  run '「参考市场价 30 元」→ 只红 EIP-PRICE（市价不是授予价）' 1 "$WORK/e-mkt.md" '[EIP-PRICE]'
fi

# ⑧ 定式禁词 → 该只红在 EIP-LINE（插一行，不动既有行，免得连带别道）
if mutate "$GOOD" "$WORK/e-fixed.md" \
  '## 三、口径对照' '- 说明：本计划建议参与，稳赚。

## 三、口径对照' '定式禁词自裁'; then
  run '「建议参与／稳赚」落在非待人工行 → 只红 EIP-LINE' 1 "$WORK/e-fixed.md" '[EIP-LINE]'
fi

# ⑨ 自裁效力判断 → 该只红在 EIP-LINE
if mutate "$GOOD" "$WORK/e-verdict.md" \
  '## 三、口径对照' '- 结论：本次审议程序违规。

## 三、口径对照' '自裁效力判断'; then
  run '「结论…违规」落在非待人工行 → 只红 EIP-LINE' 1 "$WORK/e-verdict.md" '[EIP-LINE]'
fi

# ⑩ 主题词＋判断语气同段 → 该只红在 EIP-LINE
if mutate "$GOOD" "$WORK/e-tone.md" \
  '## 三、口径对照' '- 说明：本次解锁条件会达成。

## 三、口径对照' '判断语气'; then
  run '「解锁…会达成」落在非待人工行 → 只红 EIP-LINE' 1 "$WORK/e-tone.md" '[EIP-LINE]'
fi

# ⑪ 对照样：「董事会拟定」是机构陈述，不是本件自裁 → 须零发条
if mutate "$GOOD" "$WORK/c-board.md" \
  '## 三、口径对照' '- 说明：授予价格由董事会拟定。

## 三、口径对照' '对照·董事会拟定不误伤'; then
  run '对照·「授予价格由董事会拟定」不误伤（零发条）' 0 "$WORK/c-board.md" ''
fi

echo '----'
echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then echo '有档取值域故障，整趟按 3 读，不并入「不合」。'; exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
