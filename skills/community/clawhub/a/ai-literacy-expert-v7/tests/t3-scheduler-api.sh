#!/usr/bin/env bash
# T3 · 真实调度 API 校验（只读操作 + 非法参数拦截）
# ---------------------------------------------------------------
# 安全边界（严格遵守 automation-task-manager《操作确认协议》）：
#   · 只执行「只读」或「必然在 HTTP 请求之前失败」的命令
#   · 绝不执行任何可能成功落库的 create / update / delete
#   · 脚本内置护栏：任一 create 类用例若意外返回 success → 立即告警并中止
# 经源码核实：scheduler-api.sh 的必填校验 / frequency-type 校验 / cron 秒位校验
# 全部位于 do_request() 之前，非法参数必然 exit 1，不会发出 HTTP 请求。
set -u
API_DIR="$HOME/.codebuddy/skills/automation-task-manager"
SH="$API_DIR/scripts/scheduler-api.sh"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(cd "$HERE/.." && pwd)"
OUT="${V7_TEST_OUT:-$HERE/out}"
mkdir -p "$OUT"
LOG="$OUT/t3-raw.log"
: > "$LOG"

PASS=0; FAIL=0; FAILED=()
G=""

note(){ printf '%s\n' "$*" >> "$LOG"; }
ok(){  # ok <名称> <条件退出码> <详情>
  local name="$1" cond="$2" detail="${3:-}"
  if [ "$cond" = "0" ]; then
    PASS=$((PASS+1)); printf '  ✅ [%s] %s\n' "$G" "$name"
  else
    FAIL=$((FAIL+1)); FAILED+=("[$G] $name | $detail")
    printf '  ❌ [%s] %s\n         %s\n' "$G" "$name" "$detail"
  fi
  note "[$G] $name => $([ "$cond" = 0 ] && echo PASS || echo FAIL) $detail"
}
sec(){ G="$1"; printf '\n[%s] %s\n' "$G" "$2"; note "=== $G ==="; }

cd "$API_DIR" || exit 9

echo "=============================================================================="
echo "T3 · 真实调度 API 校验（只读 + 非法参数拦截）"
echo "=============================================================================="

# =============================================== A. 只读操作（无需确认）
sec "A.只读" "list / get 只读调用"

L1=$(./scripts/scheduler-api.sh list 2>&1); R1=$?
note "list => exit=$R1 out=$L1"
TOTAL=$(printf '%s' "$L1" | jq -r '.data.total // empty' 2>/dev/null)
ok "list 调用成功（退出码 0）" "$([ $R1 -eq 0 ] && echo 0 || echo 1)" "exit=$R1"
ok "list 返回合法 JSON 且 success=true" \
   "$(printf '%s' "$L1" | jq -e '.success == true' >/dev/null 2>&1 && echo 0 || echo 1)" \
   "$(printf '%s' "$L1" | head -c 200)"
[ -n "$TOTAL" ] && ok "list 可解析 data.total（当前 = $TOTAL）" 0 "total=$TOTAL" \
                || ok "list 可解析 data.total" 1 "无法解析 total"

L2=$(./scripts/scheduler-api.sh list --keyword "AI教学" 2>&1); R2=$?
note "list --keyword => exit=$R2 out=$L2"
ok "list --keyword 'AI教学' 可用（过滤查询）" "$([ $R2 -eq 0 ] && echo 0 || echo 1)" "exit=$R2"

G_404=$(./scripts/scheduler-api.sh get --id 99999999 2>&1); R_404=$?
note "get 99999999 => exit=$R_404 out=$G_404"
# 期望：非 0 退出 + 结构化 TASK_NOT_FOUND（优雅报错，非崩溃/非堆栈）
ok "get 不存在 id 优雅报错（exit≠0 且有结构化错误）" \
   "$([ $R_404 -ne 0 ] && printf '%s' "$G_404" | grep -q 'TASK_NOT_FOUND' && echo 0 || echo 1)" \
   "exit=$R_404 out=$(printf '%s' "$G_404" | head -c 200)"
ok "get 不存在 id 返回标准错误码 TASK_NOT_FOUND（与文档错误码表一致）" \
   "$(printf '%s' "$G_404" | grep -q '"code": *"TASK_NOT_FOUND"' && echo 0 || echo 1)" \
   "$(printf '%s' "$G_404" | grep -o '"code": *"[A-Z_]*"' | head -1)"
ok "get 不存在 id 返回 success=false" \
   "$(printf '%s' "$G_404" | grep -q '"success": *false' && echo 0 || echo 1)" "—"
ok "get 不存在 id 不产生异常堆栈（无 Traceback/Segmentation）" \
   "$(printf '%s' "$G_404" | grep -qE 'Traceback|Segmentation|panic' && echo 1 || echo 0)" "—"

G_NOID=$(./scripts/scheduler-api.sh get 2>&1); R_NOID=$?
note "get (no id) => exit=$R_NOID out=$G_NOID"
ok "get 缺 --id 被拦截" "$([ $R_NOID -ne 0 ] && echo 0 || echo 1)" "exit=$R_NOID"

L3=$(./scripts/scheduler-api.sh list --bogus-flag x 2>&1); R3=$?
ok "list 未知参数被拦截" "$([ $R3 -ne 0 ] && echo 0 || echo 1)" "exit=$R3"

HELP=$(./scripts/scheduler-api.sh help 2>&1)
ok "help 列出四大必填参数" \
   "$(printf '%s' "$HELP" | grep -q -- '--frequency-type' && echo 0 || echo 1)" \
   "$(printf '%s' "$HELP" | grep -c -- '--' ) 个参数"

# =============================================== B. 非法参数拦截
sec "B.拦截" "create 非法参数必须在 HTTP 前被拦截"

run_bad(){  # run_bad <名称> <期望错误关键词> <args...>（前 2 个为元信息，切片后传给 create）
  local name="$1" kw="$2"; shift 2
  local out; out=$(./scripts/scheduler-api.sh create "$@" 2>&1); local rc=$?
  note "CREATE-BAD [$name] args=$* => exit=$rc out=$out"
  ok "$name → 被拦截（exit≠0）" "$([ $rc -ne 0 ] && echo 0 || echo 1)" "exit=$rc out=$(printf '%s' "$out"|head -c 160)"
  ok "$name → 错误信息含『$kw』" \
     "$(printf '%s' "$out" | grep -qF -- "$kw" && echo 0 || echo 1)" \
     "got=$(printf '%s' "$out" | head -c 160)"
  # 护栏（真正的底线）：绝不允许成功创建任务
  ok "$name → 未成功创建任务（无 success:true）" \
     "$(printf '%s' "$out" | grep -q '"success": *true' && echo 1 || echo 0)" \
     "out=$(printf '%s' "$out" | head -c 160)"
}

BASE_CRON="0 0 8 * * 1"
run_bad "缺 --name"          "--name"          --cron "$BASE_CRON" --prompt "p" --frequency-type daily
run_bad "缺 --cron"          "--cron"          --name "t" --prompt "p" --frequency-type daily
run_bad "缺 --prompt"        "--prompt"        --name "t" --cron "$BASE_CRON" --frequency-type daily
run_bad "缺 --frequency-type" "--frequency-type" --name "t" --cron "$BASE_CRON" --prompt "p"
run_bad "frequency-type 非法值(weekly)" "frequency-type" --name "t" --cron "$BASE_CRON" --prompt "p" --frequency-type weekly
run_bad "frequency-type 非法值(monthly)" "frequency-type" --name "t" --cron "$BASE_CRON" --prompt "p" --frequency-type monthly
run_bad "cron 秒位非 0"      "秒位必须为 0"    --name "t" --cron "30 0 8 * * 1" --prompt "p" --frequency-type daily
run_bad "cron 秒位为 */5"    "秒位必须为 0"    --name "t" --cron "*/5 0 8 * * 1" --prompt "p" --frequency-type daily

# ⚠️ 已知行为：5 位 cron 的 awk $1="0" 能骗过客户端秒位校验 → 由服务端兜底拒绝
FIVE=$(./scripts/scheduler-api.sh create --name "t" --cron "0 8 * * 1" --prompt "p" --frequency-type daily 2>&1); R5=$?
note "CREATE-BAD [cron 5位] => exit=$R5 out=$FIVE"
ok "cron 仅 5 位 → 最终被拒绝（exit≠0）" "$([ $R5 -ne 0 ] && echo 0 || echo 1)" "exit=$R5"
ok "cron 仅 5 位 → 服务端返回 INVALID_CRON_EXPR（纵深防御兜底）" \
   "$(printf '%s' "$FIVE" | grep -q 'INVALID_CRON_EXPR' && echo 0 || echo 1)" \
   "got=$(printf '%s' "$FIVE" | grep -o '"code": *"[A-Z_]*"' | head -1)"
ok "cron 仅 5 位 → 未成功创建任务" \
   "$(printf '%s' "$FIVE" | grep -q '"success": *true' && echo 1 || echo 0)" "—"

# =============================================== C. 用真实校验器验证 6 条 OPS cron
sec "C.cron" "用脚本内真实 validate_cron_seconds 校验 6 条 OPS 的 cron"

# 从真实脚本中抽取函数源码（不执行 main），保证测的是真代码
python3 - "$SH" <<'PY' > /tmp/cronfn.sh
import sys, re
src = open(sys.argv[1], encoding='utf-8').read()
m = re.search(r'^validate_cron_seconds\(\)\s*\{.*?^\}', src, re.S | re.M)
sys.stdout.write(m.group(0) if m else "")
PY
ok "成功抽取真实校验函数 validate_cron_seconds" \
   "$(grep -q 'validate_cron_seconds' /tmp/cronfn.sh && echo 0 || echo 1)" \
   "size=$(wc -c < /tmp/cronfn.sh)"
# shellcheck source=/dev/null
. /tmp/cronfn.sh 2>/dev/null
# ⚠️ 真实函数内部用的是 exit 1（非 return 1），直接调用会杀死宿主脚本 → 必须子 shell 隔离
vcron(){ ( validate_cron_seconds "$1" ) >/dev/null 2>&1; }
ok "[发现3] validate_cron_seconds 内部用 exit（非 return），须子 shell 隔离复用" \
   "$(grep -q 'exit 1' /tmp/cronfn.sh && echo 0 || echo 1)" \
   "函数体含 exit 1"

declare -A OPS_CRON=(
  [OPS-1]="0 0 8 * * 1"
  [OPS-2]="0 30 8 * * 1-5"
  [OPS-3]="0 0 19 14 1 *"
  [OPS-4]="0 0 17 * * 5"
  [OPS-5]="0 0 10 * * 3"
  [OPS-6]="0 0 20 * * 0"
)
for t in OPS-1 OPS-2 OPS-3 OPS-4 OPS-5 OPS-6; do
  c="${OPS_CRON[$t]}"
  vcron "$c"; rc=$?
  ok "$t cron '$c' 通过真实秒位校验" "$rc" "exit=$rc cron=$c"
done
# 反向用例
for bad in "1 0 8 * * 1" "59 0 8 * * 1" "*/10 0 8 * * 1" "5 30 8 * * 1-5"; do
  vcron "$bad"; rc=$?
  ok "非法 cron '$bad' 被真实校验器拒绝" "$([ $rc -ne 0 ] && echo 0 || echo 1)" "exit=$rc"
done

# =============================================== D. 零副作用护栏
sec "D.护栏" "确认所有测试零副作用（未建出任何任务）"

L_END=$(./scripts/scheduler-api.sh list 2>&1)
T_END=$(printf '%s' "$L_END" | jq -r '.data.total // empty' 2>/dev/null)
note "list(final) => total=$T_END"
ok "测试后 list 仍可用" "$([ $? -eq 0 ] && echo 0 || echo 1)" "out=$(printf '%s' "$L_END"|head -c 160)"
if [ -n "$TOTAL" ] && [ -n "$T_END" ]; then
  ok "任务总数未变化（$TOTAL → $T_END，零副作用）" \
     "$([ "$TOTAL" = "$T_END" ] && echo 0 || echo 1)" "before=$TOTAL after=$T_END"
else
  ok "任务总数可对比" 1 "before=$TOTAL after=$T_END"
fi
if [ -n "$T_END" ] && [ "$T_END" != "0" ]; then
  echo ""
  echo "  ⚠️⚠️ 护栏触发：检测到 $T_END 个任务！T3 设计上不应创建任何任务。"
  printf '%s' "$L_END" | jq '.' 2>/dev/null | head -40
fi

# =============================================== E2. 缺陷登记（真实发现）
sec "E2.发现" "文档承诺 vs 实际实现的偏差登记"
SRC_TXT=$(cat "$SH")

# 发现 1：客户端不校验 cron 字段数，仅服务端校验
vcron "0 8 * * 1"; CLIENT_PASSES=$?
ok "[发现1] 客户端 validate_cron_seconds 不校验字段数（5 位 cron 客户端放行）" \
   "$([ $CLIENT_PASSES -eq 0 ] && echo 0 || echo 1)" \
   "client_exit=$CLIENT_PASSES（0=放行 → 说明位数校验在服务端）"
ok "[发现1] 该偏差已被服务端 INVALID_CRON_EXPR 兜底（风险可控）" \
   "$(printf '%s' "$FIVE" | grep -q 'expected exactly 6 fields' && echo 0 || echo 1)" \
   "server_msg=$(printf '%s' "$FIVE" | grep -o 'expected exactly 6 fields[^"]*' | head -1)"

# 发现 2：客户端不校验 timeout / retry-count 范围（文档声称 10-1800 / ≤10）
ok "[发现2] 客户端无 timeout 范围校验（文档称 10-1800，实为服务端校验）" \
   "$(printf '%s' "$SRC_TXT" | grep -qE 'timeout_sec.*-lt 10|-gt 1800' && echo 1 || echo 0)" \
   "未在 create() 中发现 10~1800 范围判断"
ok "[发现2] 客户端无 retry-count 上限校验（文档称 ≤10，实为服务端校验）" \
   "$(printf '%s' "$SRC_TXT" | grep -qE 'retry_count.*-gt 10' && echo 1 || echo 0)" \
   "未在 create() 中发现 ≤10 判断"
cat > /tmp/chk_reg.py <<PY
import json, sys
reg = json.load(open('$SKILL/assets/automation-registry.json'))
tasks = reg if isinstance(reg, list) else reg.get('tasks', [])
bad = [t.get('key') or t.get('id') for t in tasks
       if not (10 <= t.get('timeoutSec', 0) <= 1800 and 0 <= t.get('retryCount', 0) <= 10)]
print(("OK" if not bad else "BAD:" + ",".join(map(str, bad))), len(tasks))
sys.exit(0 if not bad else 1)
PY
REGCHK=$(python3 /tmp/chk_reg.py 2>&1); REG_RC=$?
ok "[发现2] 偏差不影响 L4 安全：6 条 OPS 的 timeout/retry 均在文档范围内" \
   "$REG_RC" "check=$REGCHK（需 timeout 10~1800、retry ≤10）"

# =============================================== E. 文档-实现一致性
sec "E.一致性" "文档承诺 vs 脚本实现"
SRC=$(cat "$SH")
ok "脚本实现 daily/interval/once 三值（与文档一致）" \
   "$(printf '%s' "$SRC" | grep -q 'daily|interval|once' && echo 0 || echo 1)" "—"
ok "脚本强制秒位为 0（与文档『严禁秒级』一致）" \
   "$(printf '%s' "$SRC" | grep -q '不允许秒级定时任务' && echo 0 || echo 1)" "—"
ok "脚本默认时区 Asia/Shanghai（与文档一致）" \
   "$(printf '%s' "$SRC" | grep -q 'Asia/Shanghai' && echo 0 || echo 1)" "—"
ok "脚本使用 agentConfig.prompt 结构（与 L4 文档一致）" \
   "$(printf '%s' "$SRC" | grep -q 'agentConfig' && echo 0 || echo 1)" "—"
ok "脚本含 timeoutSec / retryCount 字段（与文档一致）" \
   "$(printf '%s' "$SRC" | grep -q 'timeoutSec' && printf '%s' "$SRC" | grep -q 'retryCount' && echo 0 || echo 1)" "—"

# =============================================== 汇总
echo ""
echo "=============================================================================="
echo "  T3 合计  $PASS/$((PASS+FAIL))   通过率 $(awk "BEGIN{printf \"%.1f\", $PASS/($PASS+FAIL)*100}")%"
echo "=============================================================================="
if [ ${#FAILED[@]} -gt 0 ]; then
  echo "❌ 失败明细："; for f in "${FAILED[@]}"; do echo "  - $f"; done
fi

cat > "$OUT/t3-results.json" <<JSON
{"total":$((PASS+FAIL)),"passed":$PASS,"failed":$FAIL,
 "rate":$(awk "BEGIN{printf \"%.1f\", $PASS/($PASS+FAIL)*100}"),
 "tasksTotalBefore":"${TOTAL:-unknown}","tasksTotalAfter":"${T_END:-unknown}",
 "failedItems":$(python3 -c 'import json,sys;print(json.dumps(sys.argv[1:],ensure_ascii=False))' "${FAILED[@]+"${FAILED[@]}"}")}
JSON

[ $FAIL -eq 0 ] || exit 1
exit 0
