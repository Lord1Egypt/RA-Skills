# Fix Review — 2026-03-22

审查对象：coding-swarm-agent security + reliability 修复批次（5 commits + 前置 H1H2H3）

---

## Review Result: Conditional Pass（已在本次 review 中修复遗漏项）

---

### FIX-A（81846ad + c3312de）

**注入修复**
- [PASS] `update-task-status.sh`：所有变量（TASK_ID、NEW_STATUS、COMMIT_HASH、TOKENS_JSON、TMUX_SESSION）通过 env 传入 Python，无拼接。
- [PASS] `on-complete.sh`：TASK_ID、SESSION、EXIT_CODE、COMMIT_HASH、TS 均改为 env var 传入；COMMIT_MSG 以 `sys.argv[1]` 传入，避免了 JSON 转义问题。
- [PASS] `dispatch.sh`：TASK_ID 用白名单 regex `^[A-Za-z0-9._-]+$` 严格校验；runner 脚本用 `<<'SCRIPT'`（无插值 heredoc），所有 dispatch-time 变量通过 `env ...` 注入，完全消除 heredoc 注入面。
- [PASS] `c3312de`：清除了 `<<'SCRIPT'` 内多余的 `$VAR` 反斜线转义——原来写成 `${COMMAND[@]}` / `${WORKDIR}` 的反斜线转义，在 no-interpolation heredoc 里会变成字面量传给 agent 端 bash，导致 `command not found`；修复后正确求值。

**mark-running 竞态**
- [PASS] `dispatch.sh:168-171`：`tmux has-session` 检查提前到 mark-running 之前；`cleanup_dispatch` trap 在 MARKED_RUNNING=true + DISPATCHED=false 时将任务回滚为 `failed`，覆盖了 tmux send-keys 失败或脚本中途 exit 的场景。

**task-not-found exit 2**
- [WARN] `update-task-status.sh` 对"竞态保护"（task already claimed, line 100）和"task not found"（line 126）统一返回 exit 2；而 `dispatch.sh:287-289` 将 exit 2 解释为"另一个 agent 已认领"并 `exit 0`。如果 task 因批次切换而真正不存在（task-not-found），错误仍被静默吞掉。
  **影响**：仅在旧 batch 任务晚到 completion 时触发，属已知边界情况，非 regression。建议后续将两者分为 exit 2 / exit 3。

**原子写入**
- [PASS] `update-task-status.sh:143-148`：tmpfile → fsync → `os.replace`，符合黄金标准。

**fire-and-forget**
- [PASS] `on-complete.sh:86`：`update-agent-status.sh` 改为同步执行，stderr 捕获到 `/tmp/update-agent-status-errors.log`。
- [PASS] `on-complete.sh:91`：`agent-manager.sh` 仍后台运行（`&`），但 stderr 捕获到 `/tmp/agent-manager-errors.log`。agent-manager 是 best-effort 扩缩容逻辑，后台执行合理。

---

### FIX-B（cc0f61a）

**generate-image.sh 路径穿越**
- [PASS] `ALLOWED_BACKENDS=("nano-banana" "openai" "stub")` + `validate_backend()` 在两处调用，backend_name 严格限制为 allowlist，拼出的路径 `$BACKENDS_DIR/${backend_name}.sh` 无法穿越。
- [PASS] 从 `source` 改为 `bash "$backend_script"` 子进程执行，消除了 source 引入的环境污染和注入放大面。

**假成功路径**
- [PASS] 移除了 `parse_args "$@" || return 0` 的假成功退出；在 `set -euo pipefail` 下，`parse_args` 返回 1 会触发脚本退出。
- [PASS] `main():178-183`：调用后验证输出文件存在，不存在则 `exit 1`，杜绝 backend/stub 静默失败仍报成功。

**WARN: OUTPUT 路径目录穿越**
- [WARN] `generate-image.sh:174`：`mkdir -p "$(dirname "$OUTPUT")"` 中 `$OUTPUT` 来自用户参数，无路径校验。攻击者可通过 `--output ../../../tmp/evil/img.png` 在任意位置创建目录（但不能写文件）。原始报告关注的是 backend source 执行，此处是遗留的低危 path traversal（目录创建）。建议后续增加 OUTPUT 路径 canonicalize + 限制在 allowed 目录内。

**swarm-config.sh 损坏失败**
- [PASS] `json_write` 遇到 JSON 损坏时 `sys.exit(1)`，不再静默清空。
- [PASS] flock + tmpfile + fsync + `os.replace` 完整实现原子写入。
- [PASS] 异常时清理 tmpfile，避免留下脏文件。
- 注：`json_read` 遇到损坏仍静默返回空字符串（line 38-40），属于读取侧的降级策略，与写入侧的 fail-fast 是合理的差异化处理。

---

### FIX-C（8cdca0e）

**agent-pool.json 并发写**
- [PASS] `update-agent-status.sh`：flock -x 9 + tmpfile + fsync + os.replace ✅
- [PASS] `spawn-agent.sh`：同上 ✅
- [PASS] `cleanup-agents.sh`：同上 ✅
- [PASS] `health-check.sh` 的 `mark_pool_session_dead` 和 `sync_pool_live_statuses`：同上 ✅
- 所有 agent-pool.json 写入路径统一加锁，覆盖完整。

**agent-manager 互斥锁**
- [PASS] `agent-manager.sh:27-31`：`flock -n 9` 非阻塞，另一个实例运行时静默退出。防止 on-complete.sh 并发触发导致的重复扩容碰撞。

**WARN: agent-manager.sh eval 注入模式未修复**
- [WARN] `agent-manager.sh:65-91`：仍使用 `eval "$(python3 -c "... json.load(open('$TASKS_FILE')) ...")"` 模式。
  - `$TASKS_FILE` / `$POOL_FILE` 是从 `$HOME` 派生的固定路径，实际注入面极窄（需要本地修改 HOME）。
  - `eval` 的输出仅为 `VAR=number` 赋值语句，Python 没有读取用户可控字段，实际风险低。
  - 但该模式与本次注入修复原则不一致，且一旦 Python 输出逻辑有变化就会引入新风险。
  **建议**：将 Python 输出改为 JSON，shell 侧用 `-c "import json; print(json.load(sys.stdin)['key'])"` 解析，或使用 env var 传参模式。此为 Medium 优先级，可在下一批次处理。

**health-check 标 failed 逻辑**
- [PASS] `mark_running_tasks_failed_for_session(session, reason)` 正确查找 status=running 且 tmux 匹配的任务，逐个调用 `update-task-status.sh failed`。
- [PASS] 三个触发场景均覆盖：tmux session 已死（line 172）、shell prompt 可见（line 190）、超时无进展（line 219）。
- [PASS] 使用 env var 传 DEAD_SESSION，无注入风险。
- 误标风险：shell prompt 检测基于 pane 末尾的 `$\s*$` 等 regex，如果 agent 输出中恰好以 shell 符号结尾（如代码 diff 中包含 `$ echo`），理论上会误判。属于已知局限性，在原始 review 中未作为 critical issue，可接受。

**直接修复（本 review 中已修）**
- [FIX] `health-check.sh:201-208`（原）：`'$UPDATED_AT'` 直接拼入 `python3 -c "..."` 字符串，若 `updated_at` 字段包含单引号+Python 代码即可注入执行。
  已改为 `UPDATED_AT_VAL="$UPDATED_AT" python3 - <<'PY' ... os.environ['UPDATED_AT_VAL'] ... PY` 模式，与其他脚本的修复方式一致。

---

### FIX-D（9963f2f + 24b409b）

**swarm-new-batch running 检查**
- [PASS] Python 读取 `active-tasks.json` 失败时 `print(0); sys.exit(0)` —— 异常不阻断（保持向后兼容），不放行 false-positive。
- [PASS] `RUNNING_COUNT -gt 0` 时拒绝执行并 `exit 1`，`--force` 可覆盖并给出明确警告。
- [PASS] 使用 `sys.argv[1]` 传路径，无注入。

**review-dashboard 精确匹配**
- [PASS] `find_review_for()` 优先检查 `depends_on` 列表精确匹配，其次用 `r"\b" + re.escape(task_id) + r"\b"` word boundary 匹配，彻底解决 T1 被 T10-REVIEW 误判问题。
- [PASS] 仅统计 `status == "done"` 的 review task，进行中的 review 不算通过。
- [PASS] `missing_full > 0` 时 `sys.exit(1)`，真正作为 release gate。

---

### H1H2H3（4d9afbe）

- [PASS] `update-task-status.sh`：`cleanup_lock` EXIT trap 保证同层加锁在异常退出时也能释放 FD，避免死锁。
- [PASS] `dispatch.sh` heartbeat 统一调用 `update-task-status.sh running`，刷新 `task.updated_at`，health-check 不再误判为"卡死"。
- [PASS] `update-task-status.sh:104-105`：status 切换为 running 时同时写入 `tmux` 字段，health-check 可凭此关联任务与会话。

---

### 综合结论

| Fix | 结论 | 关键问题 |
|-----|------|----------|
| FIX-A (81846ad+c3312de) | **Conditional Pass** | exit-2 语义歧义（WARN，非 regression） |
| FIX-B (cc0f61a) | **Conditional Pass** | OUTPUT 目录穿越遗留（WARN，低危） |
| FIX-C (8cdca0e) | **Conditional Pass** | eval+python3-c 模式未修（WARN，Medium）；health-check UPDATED_AT 注入已修复 |
| FIX-D (9963f2f) | **Pass** | 无 |
| H1H2H3 (4d9afbe) | **Pass** | 无 |

**本次 review 直接修复的问题：**
- `health-check.sh:201-208`：`$UPDATED_AT` 插值改为 env var 传入（commit 同此文档）

**遗留 WARN（建议下一批次处理）：**
1. `agent-manager.sh:65-91` eval + python3 -c 模式（Medium 优先级）
2. `generate-image.sh:174` OUTPUT 路径未做目录约束（Low 优先级）
3. `update-task-status.sh` exit-2 语义合并（task-not-found vs race-guard，Low 优先级）

整体评估：核心注入面已全部堵塞，原子写入和并发锁覆盖完整，健康检查错误传播路径已打通。遗留问题均为 Low-Medium 优先级，不影响当前 swarm 稳定运行。
