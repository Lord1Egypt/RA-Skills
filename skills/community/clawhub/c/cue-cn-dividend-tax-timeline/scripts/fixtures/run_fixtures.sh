#!/usr/bin/env bash
# run_fixtures.sh — 分红到账与扣税时间轴的离线样例 runner（零网络、零计费、30 秒内）。
#
# 三档：
#   ① 自测：--selftest 须全合（好样过、坏样五道齐发、对照样不误伤）
#   ② 样例：好样 rc=0 且 0 条发红；六枚坏样各自 rc=1 且各自那道码在场
#   ③ 边界：逐条替换同名行来造，按期望退码判（不合即红）
#
# 退码：0＝三档全合；1＝有不合；3＝不可判（runner 自身故障）。
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="$HERE/../check_dividend_tax_timeline.py"
FIX="$HERE"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/div-tax.XXXXXX")" || exit 3
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

run_case "$FIX/good-dividend-tax-timeline.md" 0 ""
run_case "$FIX/bad-1-struct.md"       1 "DT-STRUCT"
run_case "$FIX/bad-2-quote.md"        1 "DT-QUOTE"
run_case "$FIX/bad-3-line.md"         1 "DT-LINE"
run_case "$FIX/bad-4-gap.md"          1 "DT-GAP"
run_case "$FIX/bad-5-default-rate.md" 1 "DT-GAP"
run_case "$FIX/bad-6-bound.md"        1 "DT-BOUND"

# ── 档③ 边界形制 ──
say "── 档③ 边界形制 ──"
GOOD="$FIX/good-dividend-tax-timeline.md"

# 边界形制按**替换**同名行来造：插入会造成重复占行，测的就不是边界而是 DT-STRUCT。
# 每个替换实参写作 `目标子串|替换后的整行`——目标子串须在好样里**唯一**出现，
# 命中的那一整行被替换掉。替换后的整行可以换名（别名归位那两条就是靠这个把
# canonical 名换成别名），也可以换掉非项行（申报行没有「：」，只能按子串命中）。
# 用法：edge <标签> <期望退码> <替换1> [替换2 ...]
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

# 三节点同日：登记日 = 除权除息日 = 发放日，有序判据不得误红
edge "三节点同日不误红" 0 \
  '除权除息日|- 除权除息日：「除权除息日为 2026 年 6 月 12 日」 锚：公告 二'
# 节点次序错：除权除息日早于登记日
edge "节点次序错" 1 \
  '除权除息日|- 除权除息日：「除权除息日为 2026 年 6 月 10 日」 锚：公告 二'
# 日期写法变体：2026-06-15
edge "日期写法变体" 0 \
  '除权除息日|- 除权除息日：「除权除息日为 2026-06-15」 锚：公告 二'
# 股东别名归位：自然人股东 → 个人股东
edge "股东别名归位" 0 \
  '- 个人股东：|- 自然人股东：「对个人股东每股实际派发现金红利 0.28 元，按 20% 的税率代扣个人所得税，计税基数为每股派发现金红利 0.35 元」 锚：公告 四'
# 股东别名归位：QFII → 合格境外机构投资者
edge "QFII别名归位" 0 \
  '- 合格境外机构投资者：|- QFII：「对合格境外机构投资者按 10% 的税率代扣企业所得税，每股实际派发现金红利 0.315 元」 锚：公告 四'
# 税率不在原句里（套默认）
edge "税率不在原句" 1 \
  '- 香港投资者：|- 香港投资者：「对香港投资者代扣所得税」 按 10% 的税率，每股实际派发现金红利 0.315 元 锚：公告 四'
# 缺计税基数名词（原句只有税率与到手额，没有每股派息类税基名词）
edge "缺计税基数" 1 \
  '- 香港投资者：|- 香港投资者：「对香港投资者按 10% 的税率代扣所得税，每股实际到手 0.315 元」 锚：公告 四'
# 缺扣税后实得名词
edge "缺扣税后实得" 1 \
  '- 香港投资者：|- 香港投资者：「对香港投资者按 10% 的税率代扣所得税，计税基数为每股派发现金红利 0.35 元」 锚：公告 四'
# 待人工只登记自己那一分句，后半择时建议照发
edge "待人工不豁免后半" 1 \
  '- 其他法人股东：|- 其他法人股东：[待人工] 到手金额留人工；建议持有到登记日。'
# 免责句只登记自己那一分句
edge "免责不豁免后半" 1 \
  '- 其他法人股东：|- 其他法人股东：本件不接代办；税率很划算。'
# 机构名里的「会」不误红：董事会/股东大会的「会」不是判断语气。
# 该行三要素齐、申报同步改成 0 类，所以唯一可能发红的就是 DT-LINE 的「会」误判。
edge "机构名不误红" 0 \
  '- 其他法人股东：|- 其他法人股东：「对其他法人股东按 25% 的税率代扣企业所得税，计税基数为每股派发现金红利 0.35 元，每股实际派发现金红利 0.2625 元」 经董事会审议通过，股东名册以登记日为准 锚：公告 四' \
  '共五类股东·未取到 1 类|- 共五类股东·未取到 0 类' \
  '- 未取到 1 类：|- 本次五类股东扣税口径均已取到。'
# 锚是行尾标签，不是判据域终点
edge "锚后分句照扫" 1 \
  '- 其他法人股东：|- 其他法人股东：「本次分派经董事会审议通过」 锚：公告 四；建议持有到登记日，稳赚'
# 未取到写成「无需扣税」
edge "无需扣税即发" 1 \
  '- 其他法人股东：|- 其他法人股东：无需扣税'

# ── 末行 ──
say "档数=3（由上面逐档现报）｜不合=$bad｜不可判=$unk"
[ "$bad" -eq 0 ] && exit 0
exit 1
