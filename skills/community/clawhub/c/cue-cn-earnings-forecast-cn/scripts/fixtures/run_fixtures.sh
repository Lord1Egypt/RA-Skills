#!/usr/bin/env bash
# run_fixtures.sh — 业绩预告／快报稿离线自检（三档，零网络零计费）
#
# 档一 自测：check_forecast.py --selftest（11 条内置夹具，含反证）
# 档二 样例：good-forecast.md 须零发条；每枚 bad-*.md 须发，且只发它自己那道码
# 档三 边界：在好样上逐行替换／删行，判「该红的红、该不红的不红」；empty／nofile 走 rc=3
#
# 末行形制：档数=N（由上面逐档现报）｜不合=M｜不可判=K
# 退码：0 全过 / 1 有不合法 / 3 有不可判
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/../check_forecast.py"
GOOD="$HERE/good-forecast.md"
PY="${PYTHON:-python3}"
export PYTHONDONTWRITEBYTECODE=1

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT INT TERM

bad=0
unk=0
tiers=0

ok()  { printf '过   %s\n' "$*"; }
no()  { printf '不合 %s\n' "$*"; bad=$((bad + 1)); }
cannot() { printf '不可判 %s\n' "$*"; unk=$((unk + 1)); }

run_check() {  # $1=file  → 结果落在 $RC / $OUT
  OUT="$("$PY" -B "$CHECK" "$1" 2>&1)"
  RC=$?
}

codes_of() { printf '%s\n' "$1" | grep -oE '^FC-[A-Z]+' | sort -u | tr '\n' ' ' | sed 's/ $//'; }

# ---------------------------------------------------------------- 档一 自测
tiers=$((tiers + 1))
printf '%s\n' "—— 档一 自测（--selftest 内置夹具）——"
"$PY" -B "$CHECK" --selftest
rc=$?
if [ "$rc" -eq 0 ]; then ok "档一 自测 rc=0"
elif [ "$rc" -eq 1 ]; then no "档一 自测 rc=1（内置夹具有不合）"
else cannot "档一 自测 rc=$rc（跑不起来）"; fi

# ---------------------------------------------------------------- 档二 样例
tiers=$((tiers + 1))
printf '%s\n' "—— 档二 样例（1 好样＋5 坏样，每枚只发自己那道码）——"

for f in "$HERE"/bad-*.md; do
  [ -e "$f" ] || { cannot "档二 找不到任何 bad-*.md"; break; }
  base="$(basename "$f" .md)"                     # bad-struct → struct
  lane="${base#bad-}"
  case "$lane" in
    struct) want="FC-STRUCT" ;;
    quote) want="FC-QUOTE" ;;
    redline) want="FC-LINE" ;;
    calc)  want="FC-CALC" ;;
    boundary) want="FC-BOUND" ;;
    *) want="?" ;;
  esac
  run_check "$f"
  got="$(codes_of "$OUT")"
  if [ "$RC" -ne 1 ]; then
    no "档二 $(basename "$f") rc=$RC（应 1）"
  elif [ "$got" != "$want" ]; then
    no "档二 $(basename "$f") 发条码为「${got:-无}」，应只发 $want"
  else
    ok "档二 $(basename "$f") rc=1 只发 $want"
  fi
done

run_check "$GOOD"
if [ "$RC" -eq 0 ]; then
  ok "档二 good-forecast.md rc=0 零发条"
else
  no "档二 good-forecast.md rc=$RC ｜ $(codes_of "$OUT")"
fi

# ---------------------------------------------------------------- 档三 边界
tiers=$((tiers + 1))
printf '%s\n' "—— 档三 边界（好样逐行替换／删行，判该红的红、该不红的不红）——"

# edge <名> <期望rc> <期望必须出现的码或-> <行内唯一目标> <替换整行>
edge() {
  local name="$1" want_rc="$2" want_code="$3" tgt="$4" rep="$5"
  local f="$TMP/edge-$name.md"
  local n
  n="$(grep -cF -- "$tgt" "$GOOD")"
  if [ "$n" -ne 1 ]; then
    cannot "档三 $name：替换目标在好样里出现 $n 次（应唯一）"
    return
  fi
  awk -v t="$tgt" -v r="$rep" \
    '{ if (index($0, t) > 0) print r; else print $0 }' "$GOOD" > "$f"
  run_check "$f"
  local got
  got="$(codes_of "$OUT")"
  if [ "$RC" -ne "$want_rc" ]; then
    no "档三 $name：rc=$RC 应 $want_rc ｜ 发条「${got:-无}」"
  elif [ "$want_code" = "-" ]; then
    if [ -n "$got" ]; then
      no "档三 $name：应零发条，实得「$got」"
    else
      ok "档三 $name rc=0 零发条"
    fi
  elif printf '%s' "$got" | grep -qF "$want_code"; then
    ok "档三 $name rc=$RC 发 $got"
  else
    no "档三 $name：发条「${got:-无}」里没有 $want_code"
  fi
}

# drop <名> <期望rc> <期望码> <要删掉的行内唯一目标>
drop() {
  local name="$1" want_rc="$2" want_code="$3" tgt="$4"
  local f="$TMP/drop-$name.md"
  local n
  n="$(grep -cF -- "$tgt" "$GOOD")"
  if [ "$n" -ne 1 ]; then
    cannot "档三 $name：删除目标出现 $n 次（应唯一）"
    return
  fi
  awk -v t="$tgt" '{ if (index($0, t) > 0) next; print }' "$GOOD" > "$f"
  run_check "$f"
  local got
  got="$(codes_of "$OUT")"
  if [ "$RC" -ne "$want_rc" ]; then
    no "档三 $name：rc=$RC 应 $want_rc ｜ 发条「${got:-无}」"
  elif printf '%s' "$got" | grep -qF "$want_code"; then
    ok "档三 $name rc=$RC 发 $got"
  else
    no "档三 $name：发条「${got:-无}」里没有 $want_code"
  fi
}

# 反证 1：修正过且前后两值并列 → 不红
edge fixed-both 0 - \
  '- 修正情况：「本次业绩预告为首次披露，未发生修正」[S1]' \
  '- 修正前：「预计 20,000 万元至 24,000 万元」[S1]
- 修正后：「预计 32,000 万元至 38,000 万元」[S1]
- 修正说明：「本次业绩预告系对前次预告的更正」[S1]'

# 反证 2：口径里的「未取中值」是声明，不是自算 → 不红
edge caliber-negated 0 - \
  '- 口径：区间与同比幅度均直接引原文，未取中值，未做前后相减 [S1]' \
  '- 口径：区间与同比幅度均直接引原文，没有取中值，也没有拿前后相减 [S1]'

# 反证 3：[待人工] 独立成立的行 → 不红
edge human-mark-alone 0 - \
  '- 正式年度报告尚未披露，最终数据以经审计年报为准 [待人工]' \
  '- 是否超预期交由人工判断 [待人工]'

# 3 [待人工] 只豁免它自己那一句，后半句照样红
edge human-mark-half 1 FC-LINE \
  '- 正式年度报告尚未披露，最终数据以经审计年报为准 [待人工]' \
  '- 正式年度报告尚未披露 [待人工]，本次预告超预期 [S1]'

# 4 修正过但缺修正前 → 形制红
edge fixed-missing-pre 1 FC-STRUCT \
  '- 修正情况：「本次业绩预告为首次披露，未发生修正」[S1]' \
  '- 修正后：「预计 32,000 万元至 38,000 万元」[S1]
- 修正说明：「本次业绩预告系对前次预告的更正」[S1]'

# 5 中值单列一行 → 自算红
edge middle-value 1 FC-CALC \
  '- 修正情况：「本次业绩预告为首次披露，未发生修正」[S1]' \
  '- 修正情况：「本次业绩预告为首次披露，未发生修正」[S1]
- 区间中值：35,000 万元 [S1]'

# 6 区间下限大于上限 → 形制红（下限写成 39,000，上限仍是 38,000）
edge range-reversed 1 FC-STRUCT \
  '- 区间下限：「32,000 万元」[S1]' \
  '- 区间下限：「39,000 万元」[S1]'

# 7 预告类型不在册 → 形制红
edge type-unregistered 1 FC-STRUCT \
  '- 预告类型：「预增」[S1]' \
  '- 预告类型：「大幅增长」[S1]'

# 8 删掉变动原因整行 → 形制红（六项不全）
drop missing-element 1 FC-STRUCT \
  '- 变动原因：「主要产品销量增长及毛利率提升」[S1]'

# 9 删掉来源行 → 原句／锚红
drop missing-source 1 FC-QUOTE \
  '- [S1] 示例科技 2026 年年度业绩预告'

# 10 空稿 → rc=3
: > "$TMP/empty.md"
run_check "$TMP/empty.md"
if [ "$RC" -eq 3 ]; then ok "档三 empty 空稿 rc=3"; else no "档三 empty 空稿 rc=$RC 应 3"; fi

# 11 读不到文件 → rc=3
run_check "$TMP/does-not-exist.md"
if [ "$RC" -eq 3 ]; then ok "档三 nofile 缺文件 rc=3"; else no "档三 nofile 缺文件 rc=$RC 应 3"; fi

# ---------------------------------------------------------------- 末行
printf '%s\n' "——"
printf '档数=%d（由上面逐档现报）｜不合=%d｜不可判=%d\n' "$tiers" "$bad" "$unk"
if [ "$unk" -gt 0 ]; then exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
