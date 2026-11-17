#!/usr/bin/env bash
# run_fixtures.sh — 现金流质量稿离线自检（三档，零网络零计费）
#
# 档一 自测：check_cash_flow.py --selftest（12 条内置夹具，含反证）
# 档二 样例：good-cashflow.md 须零发条；每枚 bad-*.md 须只发它自己那道码
# 档三 边界：在好样上逐行替换，判「该红的红、该不红的不红」；empty/nofile 走 rc=3
#
# 末行形制：档数=N（由上面逐档现报）｜不合=M｜不可判=K
# 退码：0 全过 / 1 有不合法 / 3 有不可判
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/../check_cash_flow.py"
GOOD="$HERE/good-cashflow.md"
PY="${PYTHON:-python3}"
export PYTHONDONTWRITEBYTECODE=1

TMP="$(mktemp -d 2>/dev/null)" || { echo "3 取值域故障：临时目录没建成"; exit 3; }
[ -n "$TMP" ] && [ -d "$TMP" ] || { echo "3 取值域故障：临时目录没建成"; exit 3; }
trap 'rm -rf "$TMP"' EXIT INT TERM

bad=0; unk=0; tiers=0
say() { printf '%s\n' "$*"; }
ok()  { printf '过   %s\n' "$*"; }
no()  { printf '不合 %s\n' "$*"; bad=$((bad + 1)); }
cannot() { printf '不可判 %s\n' "$*"; unk=$((unk + 1)); }

run_check() { OUT="$("$PY" -B "$CHECK" "$1" 2>&1)"; RC=$?; }
codes_of() { printf '%s\n' "$1" | sed -n 's/^ *\(CF-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ' ' | sed 's/ $//'; }

for f in "$CHECK" "$GOOD"; do [ -f "$f" ] || cannot "取不到 $f"; done
[ "$unk" -eq 0 ] || { say "——"; say "档数=0｜不合=$bad｜不可判=$unk"; exit 3; }

# ---------------------------------------------------------------- 档一
tiers=$((tiers + 1))
say "—— 档一 自测（--selftest 内置夹具）——"
"$PY" -B "$CHECK" --selftest
rc=$?
if [ "$rc" -eq 0 ]; then ok "档一 自测 rc=0"
elif [ "$rc" -eq 1 ]; then no "档一 自测 rc=1（内置夹具有不合）"
else cannot "档一 自测 rc=$rc（跑不起来）"; fi

# ---------------------------------------------------------------- 档二
tiers=$((tiers + 1))
say "—— 档二 样例（1 好样 + 5 坏样，每枚只发自己那道码）——"
want_of() {
  case "$1" in
    bad-struct)  printf 'CF-STRUCT' ;;
    bad-quote)   printf 'CF-QUOTE' ;;
    bad-noself)  printf 'CF-NOSELF' ;;
    bad-gap)     printf 'CF-GAP' ;;
    bad-line)    printf 'CF-LINE' ;;
    *)           printf '?' ;;
  esac
}
for f in "$HERE"/bad-*.md; do
  [ -e "$f" ] || { cannot "档二 找不到任何 bad-*.md"; break; }
  base="$(basename "$f" .md)"; want="$(want_of "$base")"
  if [ "$want" = "?" ]; then cannot "档二 $base：不知道该发哪道码"; continue; fi
  run_check "$f"; got="$(codes_of "$OUT")"
  if [ "$RC" -ne 1 ]; then no "档二 $base rc=$RC（应 1）"
  elif [ "$got" != "$want" ]; then no "档二 $base 发条码为「${got:-无}」，应只发 $want"
  else ok "档二 $base rc=1 只发 $want"; fi
done

run_check "$GOOD"; got="$(codes_of "$OUT")"
if [ "$RC" -eq 0 ] && [ -z "$got" ]; then ok "档二 good-cashflow.md rc=0 零发条"
else no "档二 good-cashflow.md rc=$RC ｜ 发条「${got:-无}」"; fi

# ---------------------------------------------------------------- 档三
tiers=$((tiers + 1))
say "—— 档三 边界（好样逐行替换／插入删除，判该红的红、该不红的不红）——"

judge() {
  local name="$1" want_rc="$2" want_code="$3" f="$4" got
  run_check "$f"; got="$(codes_of "$OUT")"
  if [ "$RC" -ne "$want_rc" ]; then no "档三 $name：rc=$RC 应 $want_rc ｜ 发条「${got:-无}」"
  elif [ "$want_code" = "-" ]; then
    if [ -n "$got" ]; then no "档三 $name：应零发条，实得「$got」"; else ok "档三 $name rc=0 零发条"; fi
  elif printf '%s' "$got" | grep -qF "$want_code"; then ok "档三 $name rc=$RC 发 $got"
  else no "档三 $name：发条「${got:-无}」里没有 $want_code"; fi
}

edge() {
  local name="$1" want_rc="$2" want_code="$3" tgt="$4" rep="$5"
  local f="$TMP/edge-$name.md" n
  n="$(grep -cF -- "$tgt" "$GOOD")"
  if [ "$n" -ne 1 ]; then cannot "档三 $name：替换目标出现 $n 次（应唯一）"; return; fi
  awk -v t="$tgt" -v r="$rep" '{ if (index($0, t) > 0) print r; else print $0 }' "$GOOD" > "$f"
  judge "$name" "$want_rc" "$want_code" "$f"
}

ins() {
  local name="$1" want_rc="$2" want_code="$3" at="$4" new="$5"
  local f="$TMP/ins-$name.md" n
  n="$(grep -cF -- "$at" "$GOOD")"
  if [ "$n" -ne 1 ]; then cannot "档三 $name：锚点出现 $n 次（应唯一）"; return; fi
  awk -v t="$at" -v r="$new" '{ print; if (index($0, t) > 0) print r }' "$GOOD" > "$f"
  judge "$name" "$want_rc" "$want_code" "$f"
}

# —— 该红的红 ——
edge noself-no-flag 1 CF-NOSELF \
  '- 净现比为 1.21 倍〔自算〕分子＝经营活动产生的现金流量净额 123,400,000.00 元 [S1]｜分母＝归属于母公司所有者的净利润 102,000,000.00 元 [S2]' \
  '- 净现比为 1.21 倍「经营活动产生的现金流量净额 123,400,000.00 元」〔锚：2025 年年报·第 58 页·合并现金流量表〕[S1]'

edge noself-no-denom 1 CF-NOSELF \
  '- 收现比为 115.31%〔自算〕分子＝销售商品、提供劳务收到的现金 482,000,000.00 元 [S1]｜分母＝营业收入 418,000,000.00 元 [S2]' \
  '- 收现比为 115.31%〔自算〕分子＝销售商品、提供劳务收到的现金 482,000,000.00 元 [S1]'

edge indirect-abs 1 CF-NOSELF \
  '- 减：存货的减少 -1,200.00 万元「存货的减少 -12,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]' \
  '- 减：存货的减少 1,200.00 万元绝对值「存货的减少 -12,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]'

edge gap-excuse 1 CF-GAP \
  '- 未取到：无' \
  '- 未取到：不适用'

edge cash-equal 1 CF-LINE \
  '- 口径：期末现金及现金等价物余额取自现金流量表，与资产负债表的货币资金不以相等处理。' \
  '- 口径：期末现金及现金等价物余额等于货币资金，两者互相印证。'

edge source-no-url 1 CF-QUOTE \
  '- [S3] 示例科技 2025 年年度报告·现金流量表补充资料 | https://example.com/ann/S3 |' \
  '- [S3] 示例科技 2025 年年度报告·现金流量表补充资料 | 年报网页 | 检索日 2026-11-09 | 类型：公告'

edge undefined-ref 1 CF-QUOTE \
  '- 营业收入 41,800.00 万元「营业收入 418,000,000.00 元」〔锚：2025 年年报·第 46 页·合并利润表〕[S2]' \
  '- 营业收入 41,800.00 万元「营业收入 418,000,000.00 元」〔锚：2025 年年报·第 46 页·合并利润表〕[S8]'

# —— 该不红的不红 ——
edge fcf-declared 0 - \
  '- 自由现金流为 3,140.00 万元〔自算〕经营现金流取经营活动产生的现金流量净额 123,400,000.00 元 [S1]｜减项取购建固定资产、无形资产和其他长期资产支付的现金 92,000,000.00 元 [S1]，资本开支即该科目' \
  '- 自由现金流为 3,140.00 万元「自由现金流量 31,400,000.00 元」〔锚：2025 年年报·第 61 页·非财务信息披露〕[S3]'

ins human-exempt 0 - \
  '- 未取到：无' \
  '- 现金流质量是否优良，交由人工判断 [待人工]'

ins human-half 1 CF-LINE \
  '- 未取到：无' \
  '- 现金流质量交由人工判断 [待人工]，建议关注'

ins indirect-item 0 - \
  '- 减：存货的减少 -1,200.00 万元「存货的减少 -12,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]' \
  '- 经营性应收项目的减少 -3,400.00 万元「经营性应收项目的减少 -34,000,000.00 元」〔锚：2025 年年报·第 60 页·现金流量表补充资料〕[S3]'

: > "$TMP/empty.md"
run_check "$TMP/empty.md"
if [ "$RC" -eq 3 ]; then ok "档三 empty 空稿 rc=3"; else no "档三 empty 空稿 rc=$RC 应 3"; fi

run_check "$TMP/does-not-exist.md"
if [ "$RC" -eq 3 ]; then ok "档三 nofile 缺文件 rc=3"; else no "档三 nofile 缺文件 rc=$RC 应 3"; fi

# 零输入可跑：--demo 必须产出可判对错的成品，且该成品自己过机检
d="$TMP/demo.md"
"$PY" -B "$CHECK" --demo > "$d" 2>"$TMP/demo.err"
if [ ! -s "$d" ]; then
  no "档三 --demo 未产出内容（stderr: $(head -1 "$TMP/demo.err")）"
else
  run_check "$d"
  if [ "$RC" -eq 0 ]; then
    ok "档三 --demo 产出 $(wc -c < "$d") 字节且自过机检 rc=0"
  else
    no "档三 --demo 产物自身 rc=$RC ｜ $(codes_of "$OUT")"
  fi
fi

# ---------------------------------------------------------------- 末行
say "——"
say "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
