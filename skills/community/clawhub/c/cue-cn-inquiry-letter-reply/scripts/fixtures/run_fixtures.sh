#!/usr/bin/env bash
# run_fixtures.sh — 问询函答复核对稿离线自检（三档，零网络零计费）
#
# 档一 自测：check_inquiry_letter.py --selftest（10 条内置夹具，含六道反证与三条不红）
# 档二 样例：good-inquiry.md 须零发条；每枚 bad-*.md 须只发它自己那道码
# 档三 边界：在好样上逐行替换／插入，判「该红的红、该不红的不红」；empty/nofile 走 rc=3
#
# 末行形制：档数=N（由上面逐档现报）｜不合=M｜不可判=K
# 退码：0 全过 / 1 有不合法 / 3 有不可判
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HERE/../check_inquiry_letter.py"
GOOD="$HERE/good-inquiry.md"
PY="${PYTHON:-python3}"
export PYTHONDONTWRITEBYTECODE=1

TMP="$(mktemp -d 2>/dev/null)" || { echo "3 取值域故障：临时目录没建成"; exit 3; }
[ -n "$TMP" ] && [ -d "$TMP" ] || { echo "3 取值域故障：临时目录没建成"; exit 3; }
trap 'rm -rf "$TMP"' EXIT INT TERM

bad=0; unk=0; tiers=0
say() { printf '%s\n' "$*"; }
ok()  { printf '过   %s\n' "$*"; }
no()  { printf '不合 %s\n' "$*"; bad=$((bad + 1)); }
cannot() { printf '不可判 %s\n' "$*"; unk=$((unk + 1)); }

run_check() { OUT="$("$PY" -B "$CHECK" "$1" 2>&1)"; RC=$?; }
codes_of() { printf '%s\n' "$1" | sed -n 's/^ *\(IL-[A-Z]*\).*/\1/p' | sort -u | tr '\n' ' ' | sed 's/ $//'; }

for f in "$CHECK" "$GOOD"; do [ -f "$f" ] || cannot "取不到 $f"; done
[ "$unk" -eq 0 ] || { say "——"; say "档数=0｜不合=$bad｜不可判=$unk"; exit 3; }

# ---------------------------------------------------------------- 档一
tiers=$((tiers + 1))
say "—— 档一 自测（--selftest 内置夹具）——"
"$PY" -B "$CHECK" --selftest
rc=$?
if [ "$rc" -eq 0 ]; then ok "档一 自测 rc=0"
elif [ "$rc" -eq 1 ]; then no "档一 自测 rc=1（内置夹具有不合）"
else cannot "档一 自测 rc=$rc（跑不起来）"; fi

# ---------------------------------------------------------------- 档二
tiers=$((tiers + 1))
say "—— 档二 样例（1 好样 + 6 坏样，每枚只发自己那道码）——"
want_of() {
  case "$1" in
    bad-struct) printf 'IL-STRUCT' ;;
    bad-quote)  printf 'IL-QUOTE' ;;
    bad-pair)   printf 'IL-PAIR' ;;
    bad-gap)    printf 'IL-GAP' ;;
    bad-media)  printf 'IL-MEDIA' ;;
    bad-line)   printf 'IL-LINE' ;;
    *)          printf '?' ;;
  esac
}
for f in "$HERE"/bad-*.md; do
  [ -e "$f" ] || { cannot "档二 找不到任何 bad-*.md"; break; }
  base="$(basename "$f" .md)"; want="$(want_of "$base")"
  if [ "$want" = "?" ]; then cannot "档二 $base：不知道该发哪道码"; continue; fi
  run_check "$f"; got="$(codes_of "$OUT")"
  if [ "$RC" -ne 1 ]; then no "档二 $base rc=$RC（应 1）"
  elif [ "$got" != "$want" ]; then no "档二 $base 发条码为「${got:-无}」，应只发 $want"
  else ok "档二 $base rc=1 只发 $want"; fi
done

run_check "$GOOD"; got="$(codes_of "$OUT")"
if [ "$RC" -eq 0 ] && [ -z "$got" ]; then ok "档二 good-inquiry.md rc=0 零发条"
else no "档二 good-inquiry.md rc=$RC ｜ 发条「${got:-无}」"; fi

# ---------------------------------------------------------------- 档三
tiers=$((tiers + 1))
say "—— 档三 边界（好样逐行替换／插入删除，判该红的红、该不红的不红）——"

judge() {
  local name="$1" want_rc="$2" want_code="$3" f="$4" got
  run_check "$f"; got="$(codes_of "$OUT")"
  if [ "$RC" -ne "$want_rc" ]; then no "档三 $name：rc=$RC 应 $want_rc ｜ 发条「${got:-无}」"
  elif [ "$want_code" = "-" ]; then
    if [ -n "$got" ]; then no "档三 $name：应零发条，实得「$got」"; else ok "档三 $name rc=0 零发条"; fi
  elif printf '%s' "$got" | grep -qF "$want_code"; then ok "档三 $name rc=$RC 发 $got"
  else no "档三 $name：发条「${got:-无}」里没有 $want_code"; fi
}

edge() {
  local name="$1" want_rc="$2" want_code="$3" tgt="$4" rep="$5"
  local f="$TMP/edge-$name.md" n
  n="$(grep -cF -- "$tgt" "$GOOD")"
  if [ "$n" -ne 1 ]; then cannot "档三 $name：替换目标出现 $n 次（应唯一）"; return; fi
  awk -v t="$tgt" -v r="$rep" '{ if (index($0, t) > 0) print r; else print $0 }' "$GOOD" > "$f"
  judge "$name" "$want_rc" "$want_code" "$f"
}

ins() {
  local name="$1" want_rc="$2" want_code="$3" at="$4" new="$5"
  local f="$TMP/ins-$name.md" n
  n="$(grep -cF -- "$at" "$GOOD")"
  if [ "$n" -ne 1 ]; then cannot "档三 $name：锚点出现 $n 次（应唯一）"; return; fi
  awk -v t="$at" -v r="$new" '{ print; if (index($0, t) > 0) print r }' "$GOOD" > "$f"
  judge "$name" "$want_rc" "$want_code" "$f"
}

# —— 该红的红 ——
edge gap-excuse 1 IL-GAP \
  '- 未取到：前次募集资金使用明细' \
  '- 未取到：不适用'

edge gap-both-none 1 IL-GAP \
  '- 未取到：前次募集资金使用明细' \
  '- 未取到：无
- 未取到：前次募集资金使用明细'

# 来源行去掉 URL：该行不再被登记 ⇒ 正文引用它的 [S3] 变成未登记，两向都该发。
# （替换是整行替换，所以目标与替换都写整行；只改 URL 那一段，其余逐字保留）
edge source-no-url 1 IL-QUOTE \
  '- [S1] 示例科技 向特定对象发行股票审核问询函（用户直供原件） | https://example.com/q1 | 检索日 2026-11-10' \
  '- [S1] 示例科技 向特定对象发行股票审核问询函（用户直供原件） | 问询函原件 | 检索日 2026-11-10'

# 正文引用一个没登记的编号：同样整行替换，只把行末的 [S1] 改成 [S9]
edge undefined-ref 1 IL-QUOTE \
  '- 问题2 前次募集资金使用「请说明前次募集资金的使用进度及是否存在用途变更」〔锚：问询函·第 2 页·问题 2〕[S1]' \
  '- 问题2 前次募集资金使用「请说明前次募集资金的使用进度及是否存在用途变更」〔锚：问询函·第 2 页·问题 2〕[S9]'

edge letter-date-shape 1 IL-STRUCT \
  '收函日：2026-03-12' \
  '收函日：2026 年 3 月 12 日'

edge media-undefined 1 IL-MEDIA \
  '- 主体：会计师事务所｜[S3]' \
  '- 主体：会计师事务所｜[S7]'

# —— 该不红的不红 ——
ins human-exempt 0 - \
  '- 问题2 未取到：前次募集资金使用明细' \
  '- 问题2 未取到：前次募集资金使用明细｜是否构成审核障碍交人工判断 [待人工]'

edge quote-conclusion-ok 0 - \
  '- 问题1 回复要点：披露在手订单覆盖率' \
  '- 问题1 回复要点：抄录公司答复原文「经核查，本次募投项目产能消化措施充分，不存在重大问题」〔锚：回复公告·第 5 页·问题 1〕[S2]'

ins media-lawyer 0 - \
  '- 主体：会计师事务所｜[S3]' \
  '- 主体：发行人律师｜[S3]'

: > "$TMP/empty.md"
run_check "$TMP/empty.md"
if [ "$RC" -eq 3 ]; then ok "档三 empty 空稿 rc=3"; else no "档三 empty 空稿 rc=$RC 应 3"; fi

run_check "$TMP/does-not-exist.md"
if [ "$RC" -eq 3 ]; then ok "档三 nofile 缺文件 rc=3"; else no "档三 nofile 缺文件 rc=$RC 应 3"; fi

# 零输入可跑：--demo 必须产出可判对错的成品，且该成品自己过机检
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
say "——"
say "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
if [ "$unk" -gt 0 ]; then exit 3; fi
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
