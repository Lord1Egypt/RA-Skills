#!/usr/bin/env bash
# T4 · 产物控件自动实测回归（V6 遗留 11 件 + V7 新增 OPS-5 三件 + 1 件负例）
# 退出码：0 = 全部符合预期；1 = 有不符合预期者
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(cd "$HERE/.." && pwd)"
HARNESS="$SKILL/assets/playwright-control-test-harness.js"
BASE_OUT="${V7_TEST_OUT:-$HERE/out}"
V7="$BASE_OUT/artifacts"      # 由 t4-build-ops5-artifacts.py 生成（含 3 件正例 + 1 件负例）
V6="${V6_ARTIFACTS:-}"        # 可选：V6.0 遗留产物目录；未设置则跳过该段
OUT="$BASE_OUT/harness-out"
rm -rf "$OUT"; mkdir -p "$OUT"

PASS=0; FAIL=0; FAILED=()
declare -a ROWS

run_one(){  # run_one <文件> <期望: pass|fail> <标签>
  local f="$1" expect="$2" tag="$3"
  local name; name=$(basename "$f" .html)
  local o="$OUT/$name"; mkdir -p "$o"
  local out; out=$(node "$HARNESS" "$f" --out "$o" 2>&1); local rc=$?
  local total pass fail cerr perr
  if [ -f "$o/control-test-report.json" ]; then
    total=$(jq -r '.summary.total // 0' "$o/control-test-report.json" 2>/dev/null)
    pass=$(jq -r '.summary.pass // 0'   "$o/control-test-report.json" 2>/dev/null)
    fail=$(jq -r '.summary.fail // 0'   "$o/control-test-report.json" 2>/dev/null)
    cerr=$(jq -r '.summary.consoleErrors // 0' "$o/control-test-report.json" 2>/dev/null)
    perr=$(jq -r '.summary.pageErrors // 0'   "$o/control-test-report.json" 2>/dev/null)
  else
    total=0; pass=0; fail=0; cerr=0; perr=0
  fi
  [ -z "$total" ] && total=0; [ -z "$pass" ] && pass=0; [ -z "$fail" ] && fail=0
  [ -z "$cerr" ] && cerr=0;  [ -z "$perr" ] && perr=0

  local verdict="?"
  if [ "$expect" = "pass" ]; then
    if [ "$rc" -eq 0 ] && [ "$fail" -eq 0 ]; then verdict="PASS"; else verdict="FAIL"; fi
  else
    # 负例：必须被门控拦下（exit 2 且存在未通过控件）
    if [ "$rc" -eq 2 ] && [ "$fail" -gt 0 ]; then verdict="PASS"; else verdict="FAIL"; fi
  fi

  if [ "$verdict" = "PASS" ]; then
    PASS=$((PASS+1)); printf '  ✅ %-26s %-5s 控件 %2s（过 %2s / 不过 %2s）控制台错 %s / 页面异常 %s\n' \
      "$name" "$tag" "$total" "$pass" "$fail" "$cerr" "$perr"
  else
    FAIL=$((FAIL+1)); FAILED+=("$name 期望=$expect 实际: exit=$rc total=$total pass=$pass fail=$fail")
    printf '  ❌ %-26s %-5s exit=%s 控件 %s（过 %s / 不过 %s）\n' "$name" "$tag" "$rc" "$total" "$pass" "$fail"
    printf '%s\n' "$out" | head -12 | sed 's/^/         /'
  fi
  ROWS+=("{\"file\":\"$name\",\"tag\":\"$tag\",\"expect\":\"$expect\",\"exit\":$rc,\"total\":$total,\"pass\":$pass,\"fail\":$fail,\"consoleErrors\":$cerr,\"pageErrors\":$perr,\"verdict\":\"$verdict\"}")
}

echo "=============================================================================="
echo "T4 · 产物控件自动实测回归（harness 门控）"
echo "=============================================================================="
echo ""
if [ -n "$V6" ] && [ -d "$V6" ]; then
  echo "[1] V6.0 遗留产物回归（11 件，期望全部通过）"
  for f in "$V6"/cap1-courseware-c1.html "$V6"/cap2-game-f4.html "$V6"/cap3-lesson.html \
           "$V6"/cap4-assessment.html "$V6"/cap5-recommend.html "$V6"/cap6-collab.html \
           "$V6"/mod-a2-courseware.html "$V6"/mod-d1-courseware.html "$V6"/mod-en-bnbu.html \
           "$V6"/mod-f1-game.html "$V6"/mod-g1-courseware.html; do
    [ -f "$f" ] && run_one "$f" pass "V6" || { echo "  ⚠️ 缺失: $f"; FAIL=$((FAIL+1)); }
  done
else
  echo "[1] V6.0 遗留产物回归 —— 跳过（未设置 V6_ARTIFACTS，该段为可选项）"
fi

echo ""
echo "[2] V7.0 新增 · OPS-5 轮转场景产物（3 件，期望全部通过）"
for f in "$V7"/ops5-B1-courseware.html "$V7"/ops5-G3-courseware.html "$V7"/ops5-G3-game.html; do
  [ -f "$f" ] && run_one "$f" pass "V7" || { echo "  ⚠️ 缺失: $f"; FAIL=$((FAIL+1)); }
done

echo ""
echo "[3] 负例（1 件，期望被门控拦下：exit=2 且存在未通过控件）"
run_one "$V7/neg-broken.html" fail "NEG"

echo ""
echo "=============================================================================="
echo "  T4 合计  $PASS/$((PASS+FAIL))   通过率 $(awk "BEGIN{printf \"%.1f\", $PASS/($PASS+FAIL)*100}")%"
echo "=============================================================================="
if [ ${#FAILED[@]} -gt 0 ]; then
  echo "❌ 失败明细："; for f in "${FAILED[@]}"; do echo "  - $f"; done
fi

# 汇总 JSON
{
  printf '{"total":%s,"passed":%s,"failed":%s,"rate":%s,"rows":[' \
    "$((PASS+FAIL))" "$PASS" "$FAIL" "$(awk "BEGIN{printf \"%.1f\", $PASS/($PASS+FAIL)*100}")"
  for i in "${!ROWS[@]}"; do
    [ "$i" -gt 0 ] && printf ','
    printf '%s' "${ROWS[$i]}"
  done
  printf ']}'
} > "$BASE_OUT/t4-results.json"

[ $FAIL -eq 0 ] || exit 1
exit 0
