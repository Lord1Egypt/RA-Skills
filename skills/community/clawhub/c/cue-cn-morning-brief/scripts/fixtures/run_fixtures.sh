#!/usr/bin/env bash
# run_fixtures.sh — 晨会纪要（数据槽与覆盖率申报）的离线样例 runner（零网络、零计费、30 秒内）。
#
# 三档：
#   ① 自测：--selftest 须全合（好样过、坏样五枚各只发自己那道码、对照样不误伤）
#   ② 样例：好样 rc=0 且 0 条发红；五枚坏样各自 rc=1 且**只**含自己那道码
#   ③ 边界：逐条替换同名行来造，按期望退码判（不合即红）
#
# 退码：0＝三档全合；1＝有不合；3＝不可判（runner 自身故障）。
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="$HERE/../check_morning.py"
FIX="$HERE"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/morning.XXXXXX")" || exit 3
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
# $1=文件 $2=期望退码 $3=期望在场的码（空=不要求）——要求码时另判「只含这一道」。
run_case() {
  local f="$1" want_rc="$2" want_code="${3:-}" rc out codes
  out="$(python3 -B "$CHECK" "$f" 2>&1)"; rc=$?
  if [ "$rc" -ne "$want_rc" ]; then
    say "✗ $(basename "$f") 退码 $rc，期望 $want_rc"
    printf '%s\n' "$out" | sed 's/^/    /'
    bad=$((bad + 1))
    return
  fi
  if [ -n "$want_code" ]; then
    if ! printf '%s\n' "$out" | grep -q "^$want_code "; then
      say "✗ $(basename "$f") 未发 $want_code"
      printf '%s\n' "$out" | sed 's/^/    /'
      bad=$((bad + 1))
      return
    fi
    codes="$(printf '%s\n' "$out" | grep -oE '^MB-[A-Z]+' | sort -u | tr '\n' ' ')"
    if [ "$codes" != "$want_code " ]; then
      say "✗ $(basename "$f") 应只发 $want_code，实发 $codes"
      printf '%s\n' "$out" | sed 's/^/    /'
      bad=$((bad + 1))
      return
    fi
  fi
  say "✓ $(basename "$f") rc=$rc${want_code:+ 只发 $want_code}"
}

run_case "$FIX/good-morning-brief.md" 0 ""
run_case "$FIX/bad-1-struct.md" 1 "MB-STRUCT"
run_case "$FIX/bad-2-cover.md"  1 "MB-COVER"
run_case "$FIX/bad-3-anchor.md" 1 "MB-ANCHOR"
run_case "$FIX/bad-4-gap.md"    1 "MB-GAP"
run_case "$FIX/bad-5-line.md"   1 "MB-LINE"

# ── 档③ 边界形制 ──
say "── 档③ 边界形制 ──"
GOOD="$FIX/good-morning-brief.md"

# 边界形制按**替换**同名行来造：插入会造成重复占行，测的就不是边界而是 MB-STRUCT。
# 每个替换实参写作 `目标子串@@替换后的整行`——分隔符用 @@ 而不是 |，因为槽表行本身就带竖线。
# 目标子串须在好样里**唯一**出现，命中的那一整行被替换掉。
# 用法：edge <标签> <期望退码> <替换1> [替换2 ...]
edge() {
  local label="$1" want_rc="$2" f="$WORK/edge.md" rc spec target line hits
  shift 2
  cp "$GOOD" "$f"
  for spec in "$@"; do
    target="${spec%%@@*}"
    line="${spec#*@@}"
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

# 检索日写成中文日期形（合法，不误红）——替换的是整行，不是行内片段
edge "检索日中文写法" 0 \
  '| 交易所收盘页 | 2026-11-09 |@@| ① | 隔夜外盘 | 市场层 | 已填 | 道琼斯 -0.42%、纳斯达克 +0.31% | 交易所收盘页 | 2026 年 11 月 9 日 |'
# 八槽全填：两槽补上、覆盖率与缺口申报同步跟上，须仍全绿
edge "八槽全填即百分百" 0 \
  '| ③ | 利率与流动性 | 市场层 | 未取到 | — | — | 2026-11-09 |@@| ③ | 利率与流动性 | 市场层 | 已填 | DR007 1.82% | 银行间质押式回购行情页 | 2026-11-09 |' \
  '| ⑤ | 两融余额 | 市场层 | 未取到 | — | — | 2026-11-09 |@@| ⑤ | 两融余额 | 市场层 | 已填 | 两融余额 1.62 万亿元 | 交易所融资融券汇总页 | 2026-11-09 |' \
  '- 已填槽/总槽 = 6/8（75%）@@- 已填槽/总槽 = 8/8（100%）' \
  '- 未取到槽：利率与流动性、两融余额@@- 未取到槽：无'
# 零缺口写「无」，而槽表仍标 2 槽缺 —— 漏报方向
edge "零缺口即漏报" 1 \
  '- 未取到槽：利率与流动性、两融余额@@- 未取到槽：无'
# 已填槽数与槽表不符（申报 7 而表里只有 6 行已填）
edge "已填数与表不符" 1 \
  '- 已填槽/总槽 = 6/8（75%）@@- 已填槽/总槽 = 7/8（88%）'
# 覆盖率申报写两处（同一份纪要两个数，读者无从取信）
edge "覆盖率两处即发" 1 \
  '- 文件：2026-11-09 隔夜｜覆盖标的：2 只｜来路：用户直供@@- 已填槽/总槽 = 6/8（75%）'
# 槽名被改名（契约名不许动）
edge "槽名改名即发" 1 \
  '| ⑥ | 标的隔夜公告标题 |@@| ⑥ | 隔夜公告 |'
# 「未取到」写成「不适用」
edge "不适用即发" 1 \
  '| ③ | 利率与流动性 | 市场层 | 未取到 | — | — | 2026-11-09 |@@| ③ | 利率与流动性 | 市场层 | 未取到 | 不适用 | — | 2026-11-09 |'
# 判断段整段不写 [待人工]（一字不代填那条兜底）
edge "判断段缺待人工" 1 \
  '- [待人工] 风险大小、是否需回避，本件不判、不给方向。@@- 风险大小见各槽申报。'
# 公告正文精读越界（本件只到标题级）
edge "越界精读即发" 1 \
  '- 示例科技（300002）｜「2026 年第三季度报告」 锚：披露平台标题列表｜检索日 2026-11-09@@- 示例科技（300002）｜「2026 年第三季度报告」 公告称营业收入同比增长 12% 锚：披露平台标题列表｜检索日 2026-11-09'
# 事实行缺锚（市场综述里夹一条无出处的事实）
edge "事实行缺锚即发" 1 \
  '- 汇率与商品：「美元兑人民币 7.1180」 锚：官方中间价｜检索日 2026-11-09@@- 汇率与商品：「美元兑人民币 7.1180」'

# ── 末行 ──
say "档数=3（由上面逐档现报）｜不合=$bad｜不可判=$unk"
[ "$bad" -eq 0 ] && exit 0
exit 1
