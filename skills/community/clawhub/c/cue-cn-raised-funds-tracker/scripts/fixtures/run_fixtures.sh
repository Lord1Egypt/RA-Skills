#!/usr/bin/env bash
# run_fixtures.sh — 募集资金稿离线自检（三档，零网络零计费零凭据）
#
# 档一 自测：check_raised_funds.py --selftest（18 条内置夹具，含反证）
# 档二 样例：good-raised-funds.md 须零发条；每枚 bad-*.md 须发，且只发它自己那道码
# 档三 边界：在好样上逐行替换／删行做正反对照，判「该红的红、该不红的不红」；empty／nofile 走 rc=3
#
# 末行形制：档数=N（由上面逐档现报）｜不合=M｜不可判=K
# 退码：0 全过 / 1 有不合法 / 3 有不可判
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/../check_raised_funds.py"
GOOD="$HERE/good-raised-funds.md"
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

codes_of() { printf '%s\n' "$1" | grep -oE '^RF-[A-Z]+' | sort -u | tr '\n' ' ' | sed 's/ $//'; }

# ---------------------------------------------------------------- 档一 自测
tiers=$((tiers + 1))
printf '%s\n' "—— 档一 自测（--selftest 内置夹具）——"
"$PY" -B "$CHECK" --selftest > "$TMP/selftest.log" 2>&1
rc=$?
tail -1 "$TMP/selftest.log" | sed 's/^/     /'
if [ "$rc" -eq 0 ]; then ok "档一 自测 rc=0"
elif [ "$rc" -eq 1 ]; then no "档一 自测 rc=1（内置夹具有不合，详见 $TMP/selftest.log）"
else cannot "档一 自测 rc=$rc（跑不起来）"; fi

# ---------------------------------------------------------------- 档二 样例
tiers=$((tiers + 1))
printf '%s\n' "—— 档二 样例（1 好样＋6 坏样，每枚只发它自己那道码）——"

for f in "$HERE"/bad-*.md; do
  [ -e "$f" ] || { cannot "档二 找不到任何 bad-*.md"; break; }
  base="$(basename "$f" .md)"                     # bad-struct → struct
  lane="${base#bad-}"
  case "$lane" in
    struct|order) want="RF-STRUCT" ;;
    quote)        want="RF-QUOTE" ;;
    noself)       want="RF-NOSELF" ;;
    gap)          want="RF-GAP" ;;
    line|merge)   want="RF-LINE" ;;
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
  ok "档二 good-raised-funds.md rc=0 零发条"
else
  no "档二 good-raised-funds.md rc=$RC ｜ $(codes_of "$OUT")"
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

# sub <名> <期望rc> <期望必须出现的码或-> <行内唯一子串> <把该子串换成的文字>
# 与 edge 的区别：edge 换整行（用于「这一行该长成别的样子」），sub 只换行内一段
# （用于「同一行里换个词」）——引号内容替换必须走 sub，否则锚与 [S#] 跟着没了，
# 被 RF-QUOTE 拦下的会是夹具自己写残的行，不是被测的那条判据。
sub() {
  local name="$1" want_rc="$2" want_code="$3" tgt="$4" rep="$5"
  local f="$TMP/sub-$name.md"
  local n
  n="$(grep -oF -- "$tgt" "$GOOD" | wc -l)"
  if [ "$n" -ne 1 ]; then
    cannot "档三 $name：替换子串在好样里出现 $n 次（应唯一）"
    return
  fi
  awk -v t="$tgt" -v r="$rep" '{
    # 只替换第一处：替换文本里含目标子串时（`62.35%` → `62.35%（披露值）`），
    # while 循环会把刚写进去的那一段再匹配一次，永远停不下来。
    # 目标出现次数上面已断言为 1，所以替换一次就是全部。
    i = index($0, t)
    if (i > 0) $0 = substr($0, 1, i - 1) r substr($0, i + length(t))
    print
  }' "$GOOD" > "$f"
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

# 一、该不红的不红（反证三条）
sub disclosed-pct 0 - \
  '投入进度 62.35%' \
  '投入进度 62.35%（披露值）'

sub negated-no-change 0 - \
  '「本报告期内募投项目未发生变更」' \
  '「本报告期内募投项目未发生变更，不存在违规使用情形」'

sub selfcalc-shape-ok 0 - \
  '- 变更情况：「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页·募集资金投资项目变更情况〕[S2]' \
  '- 变更情况：投资完成度〔自算〕分子＝累计投入 12,800.00 万元 [S1]｜分母＝承诺投入 32,000.00 万元 [S2]「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页·募集资金投资项目变更情况〕[S2]'

# 二、该红的红（正证九条）
sub selfcalc-percent 1 RF-NOSELF \
  '- 募投项目一「智能制造产线建设项目」：' \
  '- 募投项目一「智能制造产线建设项目」投入进度 62.36%：'

sub selfcalc-no-denominator 1 RF-NOSELF \
  '- 变更情况：「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页·募集资金投资项目变更情况〕[S2]' \
  '- 变更情况：进度合计〔自算〕分子＝累计投入 12,800.00 万元 [S1]「本报告期内募投项目未发生变更」〔锚：专项报告·第 5 页·募集资金投资项目变更情况〕[S2]'

sub merge-total 1 RF-LINE \
  '- 专户二（中国银行深圳分行·末四位 4477）' \
  '- 专户合计：「余额合计 29,460.85 万元」'

sub redline-compliance 1 RF-LINE \
  '- 变更情况：' \
  '- 变更情况：公司存在违规使用募集资金情形。'

sub human-half 1 RF-LINE \
  '未取到：结项节余 [待人工]' \
  '未取到：结项节余 [待人工]，预计年内可达产'

edge gap-excuse 1 RF-GAP \
  '- 未取到：结项节余' \
  '- 未取到：结项节余（无需披露）'

edge caliber-wrong 1 RF-STRUCT \
  '数据口径：募集资金存放与实际使用情况（存续期台账）' \
  '数据口径：定增发行条款（发行方案十项）'

edge header-missing 1 RF-STRUCT \
  '判断位 [待人工]' \
  '判断位留白'

drop source-line 1 RF-QUOTE \
  '- [S3] 示例科技股份有限公司关于归还暂时补充流动资金的募集资金的公告'

drop unregistered 1 RF-QUOTE \
  '- [S1] 示例科技股份有限公司 2025 年半年度募集资金存放与实际使用情况的专项报告'


# 三、读不到 / 空稿
: > "$TMP/empty.md"
run_check "$TMP/empty.md"
if [ "$RC" -eq 3 ]; then ok "档三 empty 空稿 rc=3"; else no "档三 empty 空稿 rc=$RC 应 3"; fi

run_check "$TMP/does-not-exist.md"
if [ "$RC" -eq 3 ]; then ok "档三 nofile 缺文件 rc=3"; else no "档三 nofile 缺文件 rc=$RC 应 3"; fi

# 四、零输入可跑：--demo 必须产出可判对错的成品，且该成品自己过机检
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
printf '%s\n' "——"
printf '档数=%d（由上面逐档现报）｜不合=%d｜不可判=%d\n' "$tiers" "$bad" "$unk"
if [ "$unk" -gt 0 ]; then exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
