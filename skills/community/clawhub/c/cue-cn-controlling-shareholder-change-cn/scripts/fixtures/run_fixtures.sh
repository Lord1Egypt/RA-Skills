#!/usr/bin/env bash
# run_fixtures.sh — 实控人变更与要约收购卡的离线样例 runner（零网络、零计费、30 秒内）。
#
# 三档：
#   ① 自测：--selftest 须全合（好样过、坏样五枚各只发自己那道码、对照样不误伤）
#   ② 样例：好样 rc=0 且 0 条发红；五枚坏样各自 rc=1 且**只**含自己那道码
#   ③ 边界：在好样上**逐行替换**造形，正反对照——该红的红、该不红的不红；empty/nofile 走 rc=3
#
# 退码：0＝三档全合；1＝有不合；3＝不可判（runner 自身故障）。
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="$HERE/../check_control_change.py"
FIX="$HERE"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/cc.XXXXXX")" || exit 3
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
    codes="$(printf '%s\n' "$out" | grep -oE '^CC-[A-Z]+' | sort -u | tr '\n' ' ')"
    if [ "$codes" != "$want_code " ]; then
      say "✗ $(basename "$f") 应只发 $want_code，实发 $codes"
      printf '%s\n' "$out" | sed 's/^/    /'
      bad=$((bad + 1))
      return
    fi
  fi
  say "✓ $(basename "$f") rc=$rc${want_code:+ 只发 $want_code}"
}

run_case "$FIX/good-control-change.md" 0 ""
run_case "$FIX/bad-1-struct.md" 1 "CC-STRUCT"
run_case "$FIX/bad-2-quote.md"  1 "CC-QUOTE"
run_case "$FIX/bad-3-calc.md"   1 "CC-CALC"
run_case "$FIX/bad-4-line.md"   1 "CC-LINE"
run_case "$FIX/bad-5-bound.md"  1 "CC-BOUND"

# ── 档③ 边界形制（正反对照）──
say "── 档③ 边界形制 ──"
GOOD="$FIX/good-control-change.md"

# 边界形制按**替换**同名行来造：插入会造成重复占行，测的就不是边界而是 CC-STRUCT。
# 每个替换实参写作 `目标子串@@替换后的整行`——分隔符用 @@ 而不是 |，因为要素行里没有 @@ 但常带竖线与空格。
# 目标子串须在好样里**唯一**出现，命中的那一整行被替换掉。
# 用法：edge <标签> <期望退码> <替换1> [替换2 ...]
edge() {
  local label="$1" want_rc="$2" f="$WORK/edge.md" rc spec target line first hits
  shift 2
  cp "$GOOD" "$f"
  for spec in "$@"; do
    target="${spec%%@@*}"
    # 替换串里的 \n 是真换行：整块（可能多行）写进临时文件，由 awk 逐行吐出。
    # 不能用 `awk -v ins="$line"`——-v 会把 \n 解释成换行，于是「一行换一行」变成「一行变两行」，
    # 行的位次全错，测的就不是边界而是占位。
    line="$(printf '%b' "${spec#*@@}")"
    printf '%s\n' "$line" > "$WORK/ins.txt"
    hits="$(grep -cF -- "$target" "$f")"
    if [ "$hits" -ne 1 ]; then
      say "✗ $label 目标子串「$target」在好样里出现 $hits 次（须恰 1 次）"
      bad=$((bad + 1))
      return
    fi
    awk -v nm="$target" -v rf="$WORK/ins.txt" '
      index($0, nm) > 0 { while ((getline l < rf) > 0) print l; close(rf); next }
      { print }
    ' "$f" > "$f.new" && mv "$f.new" "$f"
    first="${line%%$'\n'*}"
    if grep -qF -- "$target" "$f" || ! grep -qF -- "$first" "$f"; then
      say "✗ $label 夹具未替换成功（目标子串「$target」仍在或被替换行「$first」没落上）"
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

# ── 反面（该红） ──
# 自算对价：公告没写金额，卡面自己拿股数乘价格
edge "自算对价即发" 1 \
  '- 交易对价：未取到（未取到清单已点名）@@- 交易对价：「本次转让股份数量 120,000,000 股」 按每股 8.00 元计合计 9.6亿元 锚：报告书 第二节 三  [S1]' \
  '- 共 8 项要素·未取到 1 项@@- 共 8 项要素·未取到 0 项' \
  '- 未取到 1 项：交易对价——报告书写「转让价格由双方另行协商确定」，需回补充协议核对。@@- 未取到 0 项：无。'
# 要约价与溢价率写在同一行
edge "要约价溢价率同行即发" 1 \
  '- 本笔不涉及要约收购，无要约价与溢价率。@@- 要约价：「本次要约价格为每股 12.00 元」 溢价率：「较前 30 个交易日均价溢价 21.40%」 锚：报告书 第四节  [S1]'
# 溢价率百分比不在原句里（卡面自己减出来的）
edge "自算溢价率即发" 1 \
  '- 本笔不涉及要约收购，无要约价与溢价率。@@- 要约价：「本次要约价格为每股 12.00 元」 锚：报告书 第四节  [S1]\n- 溢价率：「较前 30 个交易日均价溢价」 21.40% 锚：报告书 第四节  [S1]'
# 溢价率原句没写基准口径（无法判断它减的是哪个基准）
edge "溢价率缺基准即发" 1 \
  '- 本笔不涉及要约收购，无要约价与溢价率。@@- 要约价：「本次要约价格为每股 12.00 元」 锚：报告书 第四节  [S1]\n- 溢价率：「本次要约溢价率为 21.40%」 锚：报告书 第四节  [S1]'
# 来源编号在索引里找不到
edge "来源编号悬空即发" 1 \
  '- [S1] 示例股份有限公司详式权益变动报告书@@- [S2] 示例股份有限公司详式权益变动报告书'
# 「未取到」写成「不适用」
edge "不适用即发" 1 \
  '- 交易对价：未取到（未取到清单已点名）@@- 交易对价：不适用'
# 申报数比明细少报一项（漏报方向）
edge "申报漏报即发" 1 \
  '- 共 8 项要素·未取到 1 项@@- 共 8 项要素·未取到 0 项'

# ── 正面（该不红） ──
# 真要约收购、三样齐（要约价一行、溢价率一行带基准价）
edge "真要约三样齐不红" 0 \
  '- 本笔不涉及要约收购，无要约价与溢价率。@@- 要约价：「本次要约价格为每股 12.00 元」 锚：报告书 第四节 一  [S1]\n- 溢价率：「较前 30 个交易日均价 9.88 元溢价 21.40%」 锚：报告书 第四节 二  [S1]'
# 金额写在原句里（不是自算的）
edge "原句含金额不红" 0 \
  '- 交易对价：未取到（未取到清单已点名）@@- 交易对价：「本次股份转让价款合计人民币 960,000,000 元」 锚：报告书 第二节 四  [S1]' \
  '- 共 8 项要素·未取到 1 项@@- 共 8 项要素·未取到 0 项' \
  '- 未取到 1 项：交易对价——报告书写「转让价格由双方另行协商确定」，需回补充协议核对。@@- 未取到 0 项：无。'
# 机构名「股东大会」「委员会」里的会不误红（红线判据域的词形）
edge "机构名不误红" 0 \
  '- 变更方式：「本次权益变动方式为协议转让」 锚：报告书 第二节 一  [S1]@@- 变更方式：「本次权益变动方式为协议转让，已经股东大会审议通过」 锚：报告书 第二节 一  [S1]'
# 待人工只豁免自己那一分句的正面形：整行都在 [待人工] 后且只写疑问
edge "待人工整行留白不红" 0 \
  '- [待人工] 对控制权稳定性、新实控人后续动作、股价影响的判断，全部留人工；本件不接代办，也不给方向。@@- [待人工] 控制权稳定性、新实控人后续动作、股价影响，全部留人工。'

# ── 不可判（rc=3）──
say "── 档③附 不可判 ──"
: > "$WORK/empty.md"
python3 -B "$CHECK" "$WORK/empty.md" >/dev/null 2>&1; rc=$?
if [ "$rc" -eq 3 ]; then say "✓ empty 空稿 rc=3"; else say "✗ empty 空稿 rc=$rc，应 3"; bad=$((bad + 1)); fi
python3 -B "$CHECK" "$WORK/nofile-不存在.md" >/dev/null 2>&1; rc=$?
if [ "$rc" -eq 3 ]; then say "✓ nofile 缺文件 rc=3"; else say "✗ nofile 缺文件 rc=$rc，应 3"; bad=$((bad + 1)); fi

# ── 末行 ──
say "档数=3（由上面逐档现报）｜不合=$bad｜不可判=$unk"
[ "$bad" -eq 0 ] && exit 0
exit 1
