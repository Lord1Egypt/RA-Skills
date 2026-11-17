#!/usr/bin/env bash
# run_fixtures.sh — 存货与应收质量卡的离线样例 runner（零网络、零计费、30 秒内）。
#
# 三档：
#   ① 自测：--selftest 须全合（好样过、坏样五枚各只发自己那道码）
#   ② 样例：好样 rc=0 且 0 条发红；五枚坏样各自 rc=1 且**只**含自己那道码
#   ③ 边界：在好样上**逐行替换**造形，正反对照——该红的红、该不红的不红；empty/nofile 走 rc=3
#
# 退码：0＝三档全合；1＝有不合；3＝不可判（runner 自身故障）。
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="$HERE/../check_working_capital.py"
FIX="$HERE"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/wc.XXXXXX")" || exit 3
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
    codes="$(printf '%s\n' "$out" | grep -oE '^WC-[A-Z]+' | sort -u | tr '\n' ' ')"
    if [ "$codes" != "$want_code " ]; then
      say "✗ $(basename "$f") 应只发 $want_code，实发 $codes"
      printf '%s\n' "$out" | sed 's/^/    /'
      bad=$((bad + 1))
      return
    fi
  fi
  say "✓ $(basename "$f") rc=$rc${want_code:+ 只发 $want_code}"
}

run_case "$FIX/good-working-capital.md" 0 ""
run_case "$FIX/bad-1-struct.md" 1 "WC-STRUCT"
run_case "$FIX/bad-2-anchor.md" 1 "WC-ANCHOR"
run_case "$FIX/bad-3-noself.md" 1 "WC-NOSELF"
run_case "$FIX/bad-4-gap.md"    1 "WC-GAP"
run_case "$FIX/bad-5-line.md"   1 "WC-LINE"

# ── 档③ 边界形制（正反对照）──
say "── 档③ 边界形制 ──"
GOOD="$FIX/good-working-capital.md"

# 边界形制按**替换**同名行来造：插入会造成重复占位，测的就不是边界而是计数。
# 每个替换实参写作 `目标子串@@替换后的整行`——分隔符用 @@ 而不是 |，因为项行里没有 @@ 但常带竖线。
# 目标子串须在好样里**唯一**出现，命中的那一整行被替换掉。
# 替换串里的 \n 是真换行：整块写进临时文件，由 awk 逐行吐出。
# 不能用 `awk -v ins="$line"`——-v 会把 \n 解释成换行，于是「一行换一行」变成「一行变两行」，
# 行位全错，测的就不是边界而是占位（cn-controlling-shareholder-change-cn 一轮实测过）。
# 用法：edge <标签> <期望退码> <替换1> [替换2 ...]
edge() {
  local label="$1" want_rc="$2" f="$WORK/edge.md" rc spec target line first hits
  shift 2
  cp "$GOOD" "$f"
  for spec in "$@"; do
    target="${spec%%@@*}"
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
# 自算比例却不标〔自算〕
edge "自算周转不标即发" 1 \
  '- 存货周转天数：「存货周转天数 168.42 天」 锚：管理层讨论与分析 二  [S1]@@- 存货周转天数：182.50 天'
# 〔自算〕标了但只交代分子、没交代分母
edge "自算缺分母即发" 1 \
  '- 存货周转天数：「存货周转天数 168.42 天」 锚：管理层讨论与分析 二  [S1]@@- 存货周转天数：〔自算〕 182.50 天\n  分子：营业成本「本期营业成本 1,825,000,000 元」 [S1]｜口径：360 天基准'
# 账面价值自己拿余额减准备
edge "余额减准备即发" 1 \
  '- 合同资产账面价值：「合同资产账面价值 154,200,000.00 元」 锚：附注 五、14  [S2]@@- 合同资产账面价值：账面余额 158,826,000.00 元 − 减值准备 4,626,000.00 元'
# 锚只剩来源编号
edge "锚只剩编号即发" 1 \
  '- 存货账面余额：「存货账面余额 1,024,500,000.00 元」 锚：合并财务报表附注 五、6  [S1]@@- 存货账面余额：「存货账面余额 1,024,500,000.00 元」 锚：  [S1]'
# 来源编号悬空
edge "来源编号悬空即发" 1 \
  '- [S2] 示例股份有限公司 2025 年年度报告@@- [S3] 示例股份有限公司 2025 年年度报告'
# 零缺口靠留空表示
edge "零缺口留空即发" 1 \
  '- 共 15 项·未取到 1 项@@- 共 15 项·未取到 0 项' \
  '- 未取到 1 项：合同资产周转天数——附注未披露该指标，需回年报「管理层讨论与分析」核对是否另有表述。@@- 未取到 0 项：' \
  '- 合同资产周转天数：未取到（未取到清单已点名）@@- 合同资产周转天数：「合同资产周转天数 41.20 天」 锚：附注 五、14  [S2]'
# 申报项数漏报
edge "申报漏报即发" 1 \
  '- 共 15 项·未取到 1 项@@- 共 14 项·未取到 1 项'

# ── 正面（该不红） ──
# 自算但分子分母与口径都交代了
edge "自算交代清楚不红" 0 \
  '- 存货周转天数：「存货周转天数 168.42 天」 锚：管理层讨论与分析 二  [S1]@@- 存货周转天数：〔自算〕 182.50 天\n  分子：营业成本「本期营业成本 1,825,000,000 元」 [S1]｜分母：平均存货「期末存货 1,024,500,000 元、期初 850,000,000 元」 [S1]｜口径：360 天基准，本件自算未经验证'
# 账面价值写在原句里（报表自己写的，不是本件减的）
edge "原句含账面价值不红" 0 \
  '- 合同资产账面价值：「合同资产账面价值 154,200,000.00 元」 锚：附注 五、14  [S2]@@- 合同资产账面价值：「合同资产账面价值 154,200,000.00 元（账面余额 158,826,000.00 元减减值准备 4,626,000.00 元）」 锚：附注 五、14  [S2]'
# 账龄结构原句同时给了金额与占比
edge "账龄含占比不红" 0 \
  '- 账龄结构（1 年以内）：「1 年以内 702,400,000.00 元，占 89.33%」 锚：附注 五、10  [S2]@@- 账龄结构（1 年以内）：「1 年以内 702,400,000.00 元，占 89.33%；1 至 2 年 61,200,000.00 元，占 7.78%」 锚：附注 五、10  [S2]'
# 免责句里的「投资建议」不误红
edge "免责句不误红" 0 \
  '# 存货与应收质量卡·2026-11-09（样例·好样）@@# 存货与应收质量卡·2026-11-09\n\nAI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]'
# 事实句写「较上年同期」不误红
edge "事实句不误红" 0 \
  '- 存货同比增速：「存货较上年同期增长 9.35%」 锚：管理层讨论与分析 二  [S1]@@- 存货同比增速：「存货较上年同期增长 9.35%，主要系原材料备货增加」 锚：管理层讨论与分析 二  [S1]'
# 零缺口显式写「无」不红
edge "零缺口写无不红" 0 \
  '- 共 15 项·未取到 1 项@@- 共 15 项·未取到 0 项' \
  '- 未取到 1 项：合同资产周转天数——附注未披露该指标，需回年报「管理层讨论与分析」核对是否另有表述。@@- 未取到 0 项：无。' \
  '- 合同资产周转天数：未取到（未取到清单已点名）@@- 合同资产周转天数：「合同资产周转天数 41.20 天」 锚：附注 五、14  [S2]'

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
