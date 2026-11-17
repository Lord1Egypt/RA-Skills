#!/usr/bin/env bash
# run_fixtures.sh — 股东回报全景卡的离线样例 runner（零网络、零计费、30 秒内）。
#
# 三档：
#   ① 自测：--selftest 须全合（好样过、坏样五道齐发、对照样不误伤）
#   ② 样例：好样 rc=0 且 0 条发红；五枚坏样各自 rc=1 且各自那道码在场
#   ③ 边界：逐条插入边界形制，按期望退码判（不合即红）
#
# 退码：0＝三档全合；1＝有不合；3＝不可判（runner 自身故障）。
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="$HERE/../check_sh_return_card.py"
FIX="$HERE"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/sh-return-card.XXXXXX")" || exit 3
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

run_case "$FIX/good-sh-return-card.md" 0 ""
run_case "$FIX/bad-1-struct.md" 1 "SR-STRUCT"
run_case "$FIX/bad-2-quote.md"  1 "SR-QUOTE"
run_case "$FIX/bad-3-line.md"   1 "SR-LINE"
run_case "$FIX/bad-4-count.md"  1 "SR-COUNT"
run_case "$FIX/bad-5-value.md"  1 "SR-VALUE"

# ── 档③ 边界形制 ──
say "── 档③ 边界形制 ──"
GOOD="$FIX/good-sh-return-card.md"

# 边界形制按**替换**同名项行来造：插入会造成名目重复占行，测的就不是边界而是 SR-STRUCT。
# $1=标签 $2=替换后的整行（`- 名目：…`） $3=期望退码
edge() {
  local label="$1" line="$2" want_rc="$3" f="$WORK/edge.md" rc name
  name="${line#- }"; name="${name%%：*}"
  awk -v ins="$line" -v nm="$name" '
    index($0, "- " nm "：") == 1 { print ins; done = 1; next }
    { print }
  ' "$GOOD" > "$f"
  if ! grep -qF -- "$line" "$f"; then
    say "✗ $label 夹具未替换成功（名目「$name」不在好样里）"
    bad=$((bad + 1))
    return
  fi
  python3 -B "$CHECK" "$f" >/dev/null 2>&1; rc=$?
  if [ "$rc" -eq "$want_rc" ]; then
    say "✓ $label rc=$rc"
  else
    say "✗ $label rc=$rc，期望 $want_rc"
    bad=$((bad + 1))
  fi
}

# 分母不是值：`每 10 股派 3.50 元` 的 10 不得被当成派息值（掩分母后仍须结算 3.50）
edge "每N股分母掩码" '- 分红方案与每股派息：「每 10 股派发现金红利 3.50 元（含税）」 锚：公告 一' 0
# 简写形 `10 派 3.5 元`
edge "简写形分母掩码" '- 分红方案与每股派息：「10 派 3.5 元（含税）」 锚：公告 一' 0
# 比率不结算：`占归母净利润的 25%` 的 25% 不是分红总额
edge "比率不结算" '- 分红总额与分红率：「本次分红占归母净利润的 25%」 锚：公告 一' 1
# 参照数更近：净利润与派息值同短语，净利润更靠数即剔
edge "参照数更近即剔" '- 分红方案与每股派息：「2025 年归母净利润 7.00 亿元，每股派发现金红利 0.35 元」 锚：公告 一' 0
# 参照数族的**判别性**样本：本格名词在左、参照数更靠数。
# 撤掉参照数族后这条会假绿（误接「每股派发现金红利」），所以它才钉得住那一族。
edge "参照数族判别性样本" '- 分红方案与每股派息：「每股派发现金红利按公司总股本 5.00 亿股计算」 锚：公告 一' 1
# 日期不是值
edge "日期不是值" '- 股权登记日与除权除息日：「2026 年 6 月 12 日为股权登记日」 锚：公告 二' 0
# 空泛语：另行确定 → 该格无合格候选
edge "空泛语不结算" '- 回购方案与回购规模：「回购股份数量另行确定」 锚：公告 三' 1
# 待人工只登记自己那一分句，后半肯定预测照发
edge "待人工不豁免后半" '- 质押与解押情况：[待人工] 回报水平留人工；回购有望提振股价。' 1
# 免责句只登记自己那一分句
edge "免责不豁免后半" '- 质押与解押情况：本件不接代办；分红方案很合理。' 1
# 机构名里的「会」不误红
edge "机构名不误红" '- 质押与解押情况：「本次解押经董事会审议通过」 锚：公告 五' 0
# 锚是行尾标签，不是判据域终点：锚值之后的分句照扫
edge "锚后分句照扫" '- 质押与解押情况：「本次解押 1,200 万股」 锚：公告 五；建议增持，稳赚' 1

# ── 末行 ──
say "档数=3（由上面逐档现报）｜不合=$bad｜不可判=$unk"
[ "$bad" -eq 0 ] && exit 0
exit 1
