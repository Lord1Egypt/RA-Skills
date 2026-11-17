#!/usr/bin/env bash
# run_fixtures.sh — 个股深度研究稿离线自检（三档，零网络零计费）
#
# 档一 自测：check_note.py --selftest（10 条内置夹具，含反证）
# 档二 样例：good-note.md 须零发条；每枚 bad-*.md 须发，且只发它自己那道码；
#           反证组（ok-human-exempt / bad-human-half）判「不该红的红没红、该红的红了」
# 档三 边界：在好样上逐行替换，判「该红的红、该不红的不红」；empty/nofile 走 rc=3
#
# 末行形制：档数=N（由上面逐档现报）｜不合=M｜不可判=K
# 退码：0 全过 / 1 有不合法 / 3 有不可判
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/../check_note.py"
GOOD="$HERE/good-note.md"
PY="${PYTHON:-python3}"
export PYTHONDONTWRITEBYTECODE=1

TMP="$(mktemp -d 2>/dev/null)" || { echo "3 取值域故障：临时目录没建成（TMPDIR 是否存在、可写？）"; exit 3; }
[ -n "$TMP" ] && [ -d "$TMP" ] || { echo "3 取值域故障：临时目录没建成"; exit 3; }
trap 'rm -rf "$TMP"' EXIT INT TERM

bad=0
unk=0
tiers=0

say() { printf '%s\n' "$*"; }
ok()  { printf '过   %s\n' "$*"; }
no()  { printf '不合 %s\n' "$*"; bad=$((bad + 1)); }
cannot() { printf '不可判 %s\n' "$*"; unk=$((unk + 1)); }

run_check() {  # $1=file  → rc 落在 $RC，输出落在 $OUT
  OUT="$("$PY" -B "$CHECK" "$1" 2>&1)"
  RC=$?
}

# 码集只从「  ER-XXX Lnn …」这种发条行取，避开报告末行的「发条码：…」汇总行
codes_of() { printf '%s\n' "$1" | sed -n 's/^ *\(ER-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ' ' | sed 's/ $//'; }

# 夹具与机检若缺位，一律不可判，不读成「零违例」
for f in "$CHECK" "$GOOD"; do
  [ -f "$f" ] || cannot "取不到 $f"
done
[ "$unk" -eq 0 ] || { say "——"; say "档数=0（由上面逐档现报）｜不合=$bad｜不可判=$unk"; exit 3; }

# ---------------------------------------------------------------- 档一 自测
tiers=$((tiers + 1))
say "—— 档一 自测（--selftest 内置夹具）——"
"$PY" -B "$CHECK" --selftest
rc=$?
if [ "$rc" -eq 0 ]; then ok "档一 自测 rc=0"
elif [ "$rc" -eq 1 ]; then no "档一 自测 rc=1（内置夹具有不合）"
else cannot "档一 自测 rc=$rc（跑不起来）"; fi

# ---------------------------------------------------------------- 档二 样例
tiers=$((tiers + 1))
say "—— 档二 样例（1 好样 + 6 坏样 + 2 枚反证，每枚只发自己那道码）——"

want_of() {  # 夹具名 → 它该发的那一道码（五道码名以 check_note.py 现值为准）
  case "$1" in
    bad-form)    printf 'ER-FORM' ;;
    bad-empty)   printf 'ER-FORM' ;;
    bad-anchor)  printf 'ER-ANCHOR' ;;
    bad-redline) printf 'ER-REDLINE' ;;
    bad-noself)  printf 'ER-NOSELF' ;;
    bad-scope)   printf 'ER-SCOPE' ;;
    bad-self-borrow) printf 'ER-ANCHOR' ;;
    *)           printf '?' ;;
  esac
}

for f in "$HERE"/bad-*.md; do
  [ -e "$f" ] || { cannot "档二 找不到任何 bad-*.md"; break; }
  base="$(basename "$f" .md)"
  case "$base" in bad-human-half) continue ;; esac   # 反证组另判
  want="$(want_of "$base")"
  if [ "$want" = "?" ]; then cannot "档二 $base：不知道该发哪道码"; continue; fi
  run_check "$f"
  got="$(codes_of "$OUT")"
  if [ "$RC" -ne 1 ]; then
    no "档二 $base rc=$RC（应 1）"
  elif [ "$got" != "$want" ]; then
    no "档二 $base 发条码为「${got:-无}」，应只发 $want"
  else
    ok "档二 $base rc=1 只发 $want"
  fi
done

# 好样与两枚反证：该零发条的必须零发条，该只发一道的只发一道
expect_zero() {  # $1=文件名
  run_check "$HERE/$1"
  local got; got="$(codes_of "$OUT")"
  if [ "$RC" -eq 0 ] && [ -z "$got" ]; then ok "档二 $1 rc=0 零发条"
  else no "档二 $1 rc=$RC ｜ 发条「${got:-无}」（应零）"; fi
}
expect_one() {  # $1=文件名 $2=该发的那道码
  run_check "$HERE/$1"
  local got; got="$(codes_of "$OUT")"
  if [ "$RC" -eq 1 ] && [ "$got" = "$2" ]; then ok "档二 $1 rc=1 只发 $2"
  else no "档二 $1 rc=$RC ｜ 发条「${got:-无}」（应只发 $2）"; fi
}
expect_zero "good-note.md"
expect_zero "ok-human-exempt.md"
expect_one  "bad-human-half.md" "ER-REDLINE"

# ---------------------------------------------------------------- 档三 边界
tiers=$((tiers + 1))
say "—— 档三 边界（好样逐行替换／增删，判该红的红、该不红的不红）——"

# edge <名> <期望rc> <期望必现的码或-> <目标行内唯一片段> <替换整行> [第二组 目标 替换行]
edge() {
  local name="$1" want_rc="$2" want_code="$3" tgt="$4" rep="$5"
  local t2="${6:-}" r2="${7:-}"
  local f="$TMP/edge-$name.md"
  local n

  n="$(grep -cF -- "$tgt" "$GOOD")"
  if [ "$n" -ne 1 ]; then cannot "档三 $name：替换目标在好样里出现 $n 次（应唯一）"; return; fi
  awk -v t="$tgt" -v r="$rep" '{ if (index($0, t) > 0) print r; else print $0 }' "$GOOD" > "$f"

  if [ -n "$t2" ]; then
    local n2
    n2="$(grep -cF -- "$t2" "$f")"
    if [ "$n2" -ne 1 ]; then cannot "档三 $name：第二个替换目标出现 $n2 次（应唯一）"; return; fi
    awk -v t="$t2" -v r="$r2" '{ if (index($0, t) > 0) print r; else print $0 }' "$f" > "$f.2" && mv "$f.2" "$f"
  fi

  judge "$name" "$want_rc" "$want_code" "$f"
}

# ins <名> <期望rc> <期望码> <锚点行内唯一片段> <要插入的整行>
ins() {
  local name="$1" want_rc="$2" want_code="$3" at="$4" new="$5"
  local f="$TMP/ins-$name.md" n
  n="$(grep -cF -- "$at" "$GOOD")"
  if [ "$n" -ne 1 ]; then cannot "档三 $name：插入锚点在好样里出现 $n 次（应唯一）"; return; fi
  awk -v t="$at" -v r="$new" '{ print; if (index($0, t) > 0) print r }' "$GOOD" > "$f"
  judge "$name" "$want_rc" "$want_code" "$f"
}

# drop <名> <期望rc> <期望码> <要删掉的行内唯一片段>...
drop() {
  local name="$1" want_rc="$2" want_code="$3"; shift 3
  local f="$TMP/drop-$name.md" t n
  cp "$GOOD" "$f"
  for t in "$@"; do
    n="$(grep -cF -- "$t" "$GOOD")"
    if [ "$n" -ne 1 ]; then cannot "档三 $name：删除目标出现 $n 次（应唯一）"; return; fi
    awk -v t="$t" '{ if (index($0, t) > 0) next; print }' "$f" > "$f.2" && mv "$f.2" "$f"
  done
  judge "$name" "$want_rc" "$want_code" "$f"
}

judge() {  # $1=名 $2=期望rc $3=期望码（- 表示应零发条） $4=文件
  local name="$1" want_rc="$2" want_code="$3" f="$4" got
  run_check "$f"
  got="$(codes_of "$OUT")"
  if [ "$RC" -ne "$want_rc" ]; then
    no "档三 $name：rc=$RC 应 $want_rc ｜ 发条「${got:-无}」"
  elif [ "$want_code" = "-" ]; then
    if [ -n "$got" ]; then no "档三 $name：应零发条，实得「$got」"; else ok "档三 $name rc=0 零发条"; fi
  elif printf '%s' "$got" | grep -qF "$want_code"; then
    ok "档三 $name rc=$RC 发 $got"
  else
    no "档三 $name：发条「${got:-无}」里没有 $want_code"
  fi
}

# —— 该红的红 ——
# 1 比率原句里找不到、又没标〔自算〕
edge pct-not-in-quote 1 ER-NOSELF \
  '数控机床 2025 年实现营业收入 42.6 亿元，占主营业务收入 68.30%' \
  '- 数控机床 2025 年实现营业收入 42.6 亿元，占主营业务收入 71.50%「数控机床产品实现营业收入 426,000.00 万元，占主营业务收入的 68.30%」〔锚：2025 年年报·第 46 页·营业收入构成表〕[S1]'

# 2 标了〔自算〕但分母没挂源 —— 自算不是免责，分子分母各要出处
edge selfcalc-no-denom 1 ER-NOSELF \
  '数控机床 2025 年实现营业收入 42.6 亿元，占主营业务收入 68.30%' \
  '- 数控机床 2025 年实现营业收入 42.6 亿元，占主营业务收入 68.30%（同比 +12.40%〔自算〕分子＝本期 426,000.00 万元 [S1]｜分母＝上期 379,000.00 万元）「数控机床产品实现营业收入 426,000.00 万元，占主营业务收入的 68.30%」〔锚：2025 年年报·第 46 页·营业收入构成表〕[S1]'

# 3 [待人工] 只豁免它自己那一句，同行后半句的评级照样红
edge human-half 1 ER-REDLINE \
  '- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]' \
  '- 未取到 客户集中度的具体数值 [待人工]，建议买入 [S1]'

# 4 来源行缺可点 URL
edge source-no-url 1 ER-ANCHOR \
  '- [S3] 示例科技首次公开发行招股说明书 | https://example.com/ann/S3 |' \
  '- [S3] 示例科技首次公开发行招股说明书 | 招股说明书网页 | 检索日 2026-11-09 | 类型：公告'

# 5 正文引用了来源节没登记的行
edge undefined-ref 1 ER-ANCHOR \
  '未取到 公司在细分型号上的份额：行业资料只给前五名合计，未按型号拆分 [S2]' \
  '- 未取到 公司在细分型号上的份额：行业资料只给前五名合计，未按型号拆分 [S9]'

# 6 三元组不在行末（后面又跟了一句没挂源的话）
edge triple-not-tail 1 ER-ANCHOR \
  '- 已披露的同行业可比公司名单见招股说明书' \
  '- 已披露的同行业可比公司名单见招股说明书「同行业可比公司包括华中数控、海天精工等」〔锚：招股说明书·第 88 页·同行业可比公司〕[S3] 以上由我们整理'

# 7 空节：风险清单一条不剩（空节不是研究稿）
drop empty-section 1 ER-FORM \
  '- 风险为原材料价格上行' '- 已披露的应对为集中采购' '- 未取到 客户集中度的具体数值'

# 8 边界：写成已出财报的四期差异
ins scope-earnings 1 ER-SCOPE \
  '- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]' \
  '- 本稿同时覆盖已出财报的四期差异与科目勾稽「公司主营业务收入主要来自数控机床及功能部件两大板块」〔锚：2025 年年报·第 46 页〕[S1]'

# 9 边界：写成问题驱动的逐问作答
ins scope-question 1 ER-SCOPE \
  '- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]' \
  '- 本稿按问题清单逐问作答「公司主营业务收入主要来自数控机床及功能部件两大板块」〔锚：2025 年年报·第 46 页〕[S1]'

# —— 该不红的不红 ——
# 10 〔自算〕且分子分母各挂源 → 不红
edge selfcalc-declared 0 - \
  '数控机床 2025 年实现营业收入 42.6 亿元，占主营业务收入 68.30%' \
  '- 数控机床 2025 年实现营业收入 42.6 亿元，占主营业务收入 68.30%（同比 +12.40%〔自算〕分子＝本期 426,000.00 万元 [S1]｜分母＝上期 379,000.00 万元 [S1]）「数控机床产品实现营业收入 426,000.00 万元，占主营业务收入的 68.30%」〔锚：2025 年年报·第 46 页·营业收入构成表〕[S1]'

# 11 [待人工] 整句成立 → 不红
ins human-exempt 0 - \
  '- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]' \
  '- 是否形成壁垒、竞争位怎么排，交由人工判断 [待人工]'

# 12 未取到行本来就无原句可挂，只要求 [S#] 指向查过的那一处 → 不红
ins miss-no-quote 0 - \
  '- 未取到 客户集中度的具体数值：公告未披露前五大客户占比 [S1]' \
  '- 未取到 公司在细分型号上的毛利结构：行业资料未按型号披露 [S2]'

# 13 空稿 → 退码 3 不可判
: > "$TMP/empty.md"
run_check "$TMP/empty.md"
if [ "$RC" -eq 3 ]; then ok "档三 empty 空稿 rc=3"; else no "档三 empty 空稿 rc=$RC 应 3"; fi

# 14 读不到文件 → 退码 3 不可判
run_check "$TMP/does-not-exist.md"
if [ "$RC" -eq 3 ]; then ok "档三 nofile 缺文件 rc=3"; else no "档三 nofile 缺文件 rc=$RC 应 3"; fi

# ---------------------------------------------------------------- 末行
say "——"
say "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
