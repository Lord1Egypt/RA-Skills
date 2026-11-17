#!/usr/bin/env bash
# run_fixtures.sh — 股权质押与解押跟踪的离线样例 runner（零网络、零计费、30 秒内）。
#
# 三档：
#   ① 自测：--selftest 须全合（好样过、坏样六枚各发其码、对照样不误伤）
#   ② 样例：好样 rc=0 且 0 条发红；六枚坏样各自 rc=1 且各自那道码在场
#   ③ 边界：逐条替换同名行来造，按期望退码判（不合即红）
#
# 退码：0＝三档全合；1＝有不合；3＝不可判（runner 自身故障）。
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="$HERE/../check_pledge_tracker.py"
FIX="$HERE"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/pledge.XXXXXX")" || exit 3
trap 'rm -rf "$WORK"' EXIT

bad=0
unk=0
say() { printf '%s\n' "$*"; }

# ── 档① 自测 ──
say "── 档① 自测 ──"
if out="$(python3 -B "$CHECK" --selftest 2>&1)"; then
  say "✓ 自测全合"
else
  say "✗ 自测不合"
  printf '%s\n' "$out" | sed 's/^/    /'
  bad=$((bad + 1))
fi

# ── 档② 样例 ──
say "── 档② 样例 ──"
run_case() {   # $1=文件 $2=期望退码 $3=期望在场的码（空=不要求）
  local f="$1" want_rc="$2" want_code="${3:-}" rc out
  out="$(python3 -B "$CHECK" "$f" 2>&1)"; rc=$?
  if [ "$rc" -ne "$want_rc" ]; then
    say "✗ $(basename "$f") 退码 $rc，期望 $want_rc"
    printf '%s\n' "$out" | sed 's/^/    /'
    bad=$((bad + 1))
    return
  fi
  if [ -n "$want_code" ] && ! printf '%s\n' "$out" | grep -q "$want_code"; then
    say "✗ $(basename "$f") 未发 $want_code"
    printf '%s\n' "$out" | sed 's/^/    /'
    bad=$((bad + 1))
    return
  fi
  say "✓ $(basename "$f") rc=$rc${want_code:+ 含 $want_code}"
}

run_case "$FIX/good-pledge-tracker.md" 0 ""
run_case "$FIX/bad-1-struct.md"      1 "SP-STRUCT"
run_case "$FIX/bad-2-quote.md"       1 "SP-QUOTE"
run_case "$FIX/bad-3-line.md"        1 "SP-LINE"
run_case "$FIX/bad-4-gap.md"         1 "SP-GAP"
run_case "$FIX/bad-5-self-pct.md"    1 "SP-GAP"
run_case "$FIX/bad-6-bound.md"       1 "SP-BOUND"

# ── 档③ 边界形制 ──
say "── 档③ 边界形制 ──"
GOOD="$FIX/good-pledge-tracker.md"

# 边界形制按**替换**同名行来造：插入会造成重复占行，测的就不是边界而是 SP-STRUCT。
# 每个替换实参写作 `目标子串|替换后的整行`——目标子串须在好样里**唯一**出现，
# 命中的那一整行被替换掉。用法：edge <标签> <期望退码> <替换1> [替换2 ...]
edge() {
  local label="$1" want_rc="$2" f="$WORK/edge.md" rc spec target line hits
  shift 2
  cp "$GOOD" "$f"
  for spec in "$@"; do
    target="${spec%%|*}"
    line="${spec#*|}"
    hits="$(grep -cF -- "$target" "$f")"
    if [ "$hits" -ne 1 ]; then
      say "✗ $label 目标子串「$target」在好样里出现 $hits 次（须恰 1 次）"
      bad=$((bad + 1))
      return
    fi
    awk -v ins="$line" -v nm="$target" '
      index($0, nm) > 0 { print ins; next }
      { print }
    ' "$f" > "$f.new" && mv "$f.new" "$f"
    if ! grep -qF -- "$line" "$f"; then
      say "✗ $label 夹具未替换成功（目标名目「$target」不在好样里）"
      bad=$((bad + 1))
      return
    fi
  done
  python3 -B "$CHECK" "$f" >/dev/null 2>&1; rc=$?
  if [ "$rc" -eq "$want_rc" ]; then
    say "✓ $label rc=$rc"
  else
    say "✗ $label rc=$rc，期望 $want_rc"
    bad=$((bad + 1))
  fi
}

# 日期写法变体：2026-08-20 合法
edge "日期写法变体" 0 \
  '解除质押登记日为 2026 年 8 月 20 日|- 解押：「出质人示例控股集团有限公司，本次解除质押股份数量 500 万股，解除质押登记日为 2026-08-20」 锚：公告 三、本次解除质押情况'
# 自算比例：公告原句只写股数，卡面把百分比放在书名号外
edge "自算比例即发" 1 \
  '本次质押股份数量 1,200 万股|- 质押：「出质人示例控股集团有限公司，质权人中国工商银行股份有限公司，本次质押股份数量 1,200 万股，占其所持公司股份的比例未披露，占公司总股本的比例未披露，质押期限自 2026 年 6 月 12 日至 2027 年 6 月 11 日」 占其所持公司股份的 8.00%，占公司总股本的 2.40% 锚：公告 二、本次质押情况'
# 锚是行尾标签，不是判据域终点
edge "锚后分句照扫" 1 \
  '锚：公告 三、本次解除质押情况|- 解押：「出质人示例控股集团有限公司，本次解除质押股份数量 500 万股，解除质押登记日为 2026 年 8 月 20 日」 锚：公告 三、本次解除质押情况；该股质押比例偏高'
# 机构名「股东大会」里的「会」不误红
edge "机构名不误红" 0 \
  '锚：公告 三、本次解除质押情况|- 解押：「出质人示例控股集团有限公司，本次解除质押股份数量 500 万股，解除质押登记日为 2026 年 8 月 20 日」 经股东大会审议通过 锚：公告 三、本次解除质押情况'
# 未取到写成「不适用」
edge "不适用即发" 1 \
  '- 质押：未取到（未取到清单已点名）|- 质押：不适用'
# 单份公告速读的单选行
edge "事件类型单选行" 1 \
  '- 质押：未取到（未取到清单已点名）|- 事件类型：股份质押公告' \
  '- 共 4 笔质押变动·未取到 1 笔|- 共 3 笔质押变动·未取到 0 笔'
# 待人工只豁免自己那一分句
edge "待人工不豁免后半" 1 \
  '- [待人工] 质押比例是否偏高、是否存在平仓风险、对股价的影响，全部留人工；本件不接代办，也不给风险判断。|- [待人工] 质押比例留人工；该股质押比例偏高'
# 累计行只有一处（看不出变化）
edge "累计只有一处" 1 \
  '- 示例控股集团有限公司：累计质押 4,500 万股 → 累计质押 6,000 万股|- 示例控股集团有限公司：累计质押 6,000 万股'
# 股东回报速读的项行
edge "股东回报项行" 1 \
  '本次质押股份数量 1,200 万股|- 分红方案与每股派息：「每 10 股派发现金红利 3.50 元（含税）」 锚：公告 一、重要内容提示' \
  '- 共 4 笔质押变动·未取到 1 笔|- 共 3 笔质押变动·未取到 1 笔'

# ── 末行 ──
say "档数=3（由上面逐档现报）｜不合=$bad｜不可判=$unk"
[ "$bad" -eq 0 ] && exit 0
exit 1
