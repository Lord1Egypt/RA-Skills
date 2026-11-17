#!/usr/bin/env bash
# 三链真跑：上游工件 → upstream_intake → build_memo → check_memo，逐链自报退码与出稿文件名。
# 用法：bash scripts/fixtures/run_upstream_chains.sh   （零网络；产物只落在 ${TMPDIR:-/tmp} 下一次性目录，跑完即删）
# 退码：0＝三条链的期望逐格合；1＝有不合（逐链点名，并吐那次真实退码与真实末行）；3＝取值域故障（件或脚本取不到，不当「不合」读）。
# 期望挂在两处（每条链各读自己那一支）：链 1／链 2 期望 check_memo 退 0；链 3（risk-fact-table 单源）期望**已知红**且红形逐字对上。
#   已知红的逐字形＝「事实与数字条数：正文列出 1，run.json 记 0」；
#   成因＝build_memo 在二节零事实且无合计时落一行「本次无可锚定的数值行」占位，而 check_memo 道四把占位行计入正文、run.json 记 0。
#   本 runner 不修这一形：任一改动让链 3 变绿或换形，本 runner 判「期望不再在场」，逼一次复读。
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
UP="$ROOT/scripts/fixtures/upstream"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/ic-memo-upchain.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
ASOF="2026-10-21 09:00"

for f in "$ROOT/scripts/upstream_intake.py" "$ROOT/scripts/build_memo.py" "$ROOT/scripts/check_memo.py"; do
  [ -f "$f" ] || { echo "3 取值域故障：取不到脚本 $f"; exit 3; }
done

bad=0
unk=0

chain() {  # chain <kind> <工件> <来源件|-> <人工看多件> <主体> <期望 green|known-red>
  local kind="$1" art="$2" src="$3" bull="$4" subj="$5" want="$6"
  local n="$kind" dir="$WORK/$kind" log="$WORK/$kind.log" p
  for p in "$art" "$bull"; do
    [ -f "$p" ] || { echo "链 $n｜UNK 3＝取值域故障：取不到 $p"; unk=$((unk + 1)); return; }
  done
  if [ "$src" != "-" ]; then
    [ -f "$src" ] || { echo "链 $n｜UNK 3＝取值域故障：取不到 $src"; unk=$((unk + 1)); return; }
    src_args=(--sources "$src")
  else
    src_args=()
  fi
  {
    echo "## intake"
    python3 -B "$ROOT/scripts/upstream_intake.py" --kind "$kind" \
      --artifact "$art" --out-dir "$dir" "${src_args[@]}" --manual-bull "$bull"; echo "rc_intake=$?"
    echo "## build"
    python3 -B "$ROOT/scripts/build_memo.py" --run-dir "$dir" --subject "$subj" --subject-name "合成示例主体" \
      --facts "$dir/facts.jsonl" --gaps "$dir/gaps.jsonl" --materials "$dir/materials.jsonl" \
      --asof "$ASOF"; echo "rc_build=$?"
    echo "## check"
    local memo
    memo="$(ls "$dir"/memo-"$subj"-*.md 2>/dev/null | head -1)"
    if [ -z "$memo" ]; then echo "no-memo"; echo "rc_check=3"; return; fi
    echo "出稿=$(basename "$memo")"
    python3 -B "$ROOT/scripts/check_memo.py" "$memo" --run "$dir/run.json"; echo "rc_check=$?"
  } > "$log" 2>&1

  local rc_i rc_b rc_c memo_line redline
  rc_i="$(sed -n 's/^rc_intake=//p' "$log")"
  rc_b="$(sed -n 's/^rc_build=//p' "$log")"
  rc_c="$(sed -n 's/^rc_check=//p' "$log")"
  memo_line="$(sed -n 's/^出稿=//p' "$log")"
  echo "链 $n｜kind=$kind｜主体=$subj｜intake rc=${rc_i:-无}｜build rc=${rc_b:-无}｜check rc=${rc_c:-无}｜出稿=${memo_line:-无}"

  if [ "$rc_i" != "0" ] || [ "$rc_b" != "0" ]; then
    echo "  → 不合：前置一环没绿（intake=${rc_i:-无}／build=${rc_b:-无}）"
    sed -n '1,20p' "$log" | sed 's/^/    │ /'
    bad=$((bad + 1)); return
  fi
  if [ "$want" = "green" ]; then
    if [ "$rc_c" = "0" ]; then
      echo "  → 合：机检过（期望 check rc=0）"
    else
      echo "  → 不合：期望 check rc=0，现读 rc=$rc_c"
      grep -E '^(\[E-|FAIL)' "$log" | head -6 | sed 's/^/    │ /'
      bad=$((bad + 1))
    fi
    return
  fi
  redline="$(grep -F '事实与数字条数：正文列出 1，run.json 记 0' "$log" | head -1)"
  if [ "$rc_c" = "1" ] && [ -n "$redline" ]; then
    echo "  → 合：已知红逐字在位（check rc=1）"
    echo "    ${redline# }"
    echo "    本 runner 不修这一形（成因见件首）；它变绿或换形都会被判不合。"
  else
    echo "  → 不合：已知红的期望不再在场（check rc=${rc_c:-无}，逐字命中=${redline:-无}）——这一链的形状变了，复读 build_memo 的占位行与 check_memo 道四，别沿用本断言"
    sed -n '1,24p' "$log" | sed 's/^/    │ /'
    bad=$((bad + 1))
  fi
}

chain tear-sheet-page "$UP/tear-sheet-page.md" "$UP/tear-sheet-sources.jsonl" \
  "$UP/manual-bull-tear-sheet.jsonl" 000333 green
chain structured-note "$UP/earnings-note.md" - \
  "$UP/manual-bull-note.jsonl" 600000 green
chain risk-fact-table "$UP/risk-report.md" "$UP/risk-sources.jsonl" \
  "$UP/manual-bull-risk-table.jsonl" 600001 known-red

echo "----"
echo "链数=3（由上面逐链现报）｜合期望=$(((3 - bad - unk)))｜不合=$bad｜不可判=$unk"
[ "$unk" -gt 0 ] && { echo "有链取值域故障，整趟按 3 读，不并入「不合」。"; exit 3; }
if [ "$bad" -gt 0 ]; then exit 1; fi
exit 0
