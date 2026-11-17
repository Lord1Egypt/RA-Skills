#!/usr/bin/env bash
# run_fixtures.sh — 限售解禁压力稿离线自检（三档，零网络零计费）
#
# 档一 自测：check_lockup.py --selftest（内置夹具，含反证；档数以末行现报为准）
# 档二 样例：good-lockup.md 须零发条；每枚 bad-*.md 须发，且只发它自己那道码
# 档三 边界：在好样上逐行替换，判「该红的红、该不红的不红」
#
# 末行形制：档数=N（由上面逐档现报）｜不合=M｜不可判=K
# 退码：0 全过 / 1 有不合法 / 3 有不可判
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/../check_lockup.py"
GOOD="$HERE/good-lockup.md"
PY="${PYTHON:-python3}"
export PYTHONDONTWRITEBYTECODE=1

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT INT TERM

bad=0
unk=0
tiers=0

say() { printf '%s\n' "$*"; }
ok()  { printf '过   %s\n' "$*"; }
no()  { printf '不合 %s\n' "$*"; bad=$((bad + 1)); }
cannot() { printf '不可判 %s\n' "$*"; unk=$((unk + 1)); }

run_check() {  # $1=file  → 打印 rc，结果落在 $RC / $OUT
  OUT="$("$PY" -B "$CHECK" "$1" 2>&1)"
  RC=$?
}

codes_of() { printf '%s\n' "$1" | grep -oE '^LK-[A-Z]+' | sort -u | tr '\n' ' ' | sed 's/ $//'; }

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
say "—— 档二 样例（1 好样 + 6 坏样，每枚只发自己那道码）——"

wanth=""
for f in "$HERE"/bad-*.md; do
  [ -e "$f" ] || { cannot "档二 找不到任何 bad-*.md"; break; }
  base="$(basename "$f" .md)"                     # bad-struct → struct
  lane="${base#bad-}"
  case "$lane" in
    struct) want="LK-STRUCT" ;;
    anchor) want="LK-QUOTE" ;;
    redline) want="LK-LINE" ;;
    miss|pct) want="LK-GAP" ;;
    boundary) want="LK-BOUND" ;;
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
  ok "档二 good-lockup.md rc=0 零发条"
else
  no "档二 good-lockup.md rc=$RC ｜ $(codes_of "$OUT")"
fi

# ---------------------------------------------------------------- 档三 边界
tiers=$((tiers + 1))
say "—— 档三 边界（好样逐行替换，判该红的红、该不红的不红）——"

# edge <名> <期望rc> <期望必须出现的码或-> <行内唯一目标> <替换行> [第二组 目标 替换行]
edge() {
  local name="$1" want_rc="$2" want_code="$3" tgt="$4" rep="$5"
  local t2="${6:-}" r2="${7:-}"
  local f="$TMP/edge-$name.md"

  local n
  n="$(grep -cF -- "$tgt" "$GOOD")"
  if [ "$n" -ne 1 ]; then
    cannot "档三 $name：替换目标在好样里出现 $n 次（应唯一）"
    return
  fi
  awk -v t="$tgt" -v r="$rep" \
    '{ if (index($0, t) > 0) print r; else print $0 }' "$GOOD" > "$f"

  if [ -n "$t2" ]; then
    local n2
    n2="$(grep -cF -- "$t2" "$f")"
    if [ "$n2" -ne 1 ]; then
      cannot "档三 $name：第二个替换目标出现 $n2 次（应唯一）"
      return
    fi
    awk -v t="$t2" -v r="$r2" \
      '{ if (index($0, t) > 0) print r; else print $0 }' "$f" > "$f.2" && mv "$f.2" "$f"
  fi

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

# 1 自算但六节写明了口径 → 不红（备注：替换整行，不是行内片段）
edge selfcalc-declared 0 - \
  '占比出处：公告原文 [S1][S3]' \
  '- 第 1 轮 2026-12-20｜解禁 180,000,000 股／占总股本 4.50%（分母总股本 4,000,000,000 股）｜占比出处：自算 [S1][S3]' \
  '- 口径：占比取自解禁公告原句' \
  '- 口径：本轮占比为自算（解禁股数除以同锚总股本），分母总股本取自 2026 年三季报同一时点 [S3]'

# 2 [待人工] 只豁免它自己那一句，后半句照样红
edge human-mark-half 1 LK-LINE \
  '- 第 2 轮解锁条件是否全部达成，以公司后续公告为准 [待人工]' \
  '- 第 2 轮解锁条件是否全部达成 [待人工]，建议减持 [S1]'

# 3 分母总股本与二节总股本行不同数 → 分母拿错时点，整节占比全错
edge denom-mismatch 1 LK-GAP \
  '占比出处：公告原文 [S1][S3]' \
  '- 第 1 轮 2026-12-20｜解禁 180,000,000 股／占总股本 4.50%（分母总股本 3,800,000,000 股）｜占比出处：公告原文 [S1][S3]'

# 4 压力行两枚同号锚 → 分子分母没各挂一处
edge one-anchor 1 LK-QUOTE \
  '占比出处：公告原文 [S1][S3]' \
  '- 第 1 轮 2026-12-20｜解禁 180,000,000 股／占总股本 4.50%（分母总股本 4,000,000,000 股）｜占比出处：公告原文 [S1][S1]'

# 4b 引用来源节根本不存在的 S 号 → 凭空造出处；两枚不同号锚这条不响，响的是「未登记」
edge unknown-anchor 1 LK-QUOTE \
  '占比出处：公告原文 [S1][S3]' \
  '- 第 1 轮 2026-12-20｜解禁 180,000,000 股／占总股本 4.50%（分母总股本 4,000,000,000 股）｜占比出处：公告原文 [S1][S999]'

# 4c 反证：[S1][S2] 两枚都在册，只是分母挂在 S2 而非 S3 → 本拍只验存在性，不该发
edge anchor-exists-denom-elsewhere 0 - \
  '占比出处：公告原文 [S1][S3]' \
  '- 第 1 轮 2026-12-20｜解禁 180,000,000 股／占总股本 4.50%（分母总股本 4,000,000,000 股）｜占比出处：公告原文 [S1][S2]'

# 5 日历倒序 → 倒序的日历不是日历
edge calendar-desc 1 LK-STRUCT \
  '- 2027-06-18｜股权激励对象｜限制性股票第一期解锁 180,000,000 股 [S2]' \
  '- 2026-12-01｜股权激励对象｜限制性股票第一期解锁 180,000,000 股 [S2]'

# 6 日历行写解押 → 越界到质押那件
edge calendar-pledge 1 LK-BOUND \
  '- 2027-06-18｜股权激励对象｜限制性股票第一期解锁 180,000,000 股 [S2]' \
  '- 2027-06-18｜股权激励对象｜限制性股票第一期解押 180,000,000 股 [S2]'

# 7 日历只剩一行 → 本件不是单事件清单
drop calendar-one-row 1 LK-BOUND \
  '- 2027-06-18｜股权激励对象｜'

# 8 空稿 → 退码 3 不可判
: > "$TMP/empty.md"
run_check "$TMP/empty.md"
if [ "$RC" -eq 3 ]; then ok "档三 empty 空稿 rc=3"; else no "档三 empty 空稿 rc=$RC 应 3"; fi

# 9 读不到文件 → 退码 3 不可判
run_check "$TMP/does-not-exist.md"
if [ "$RC" -eq 3 ]; then ok "档三 nofile 缺文件 rc=3"; else no "档三 nofile 缺文件 rc=$RC 应 3"; fi

# ---------------------------------------------------------------- 末行
say "——"
say "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
