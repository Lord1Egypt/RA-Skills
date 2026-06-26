# 设计文档：ARCH-REVIEW H1–H5 修复方案

> 创建时间：2026-03-20
> 对应需求：docs/requirements/arch-review-fixes.md

## H1 — update-task-status.sh：flock race guard 修复

**根因：** `UTS_EC=${PIPESTATUS[0]:-$?}` 在 `set -euo pipefail` 下，
Python `sys.exit(2)` 会先触发 `-e` 终止子 shell，再被 `PIPESTATUS[0]` 捕获。
但 Python 代码是直接运行（不是管道），`PIPESTATUS` 不适用——应该用 `$?`。
实测 Python exit 2 时 `UTS_EC` 确实捕获到 2，所以当前逻辑偶然正确。
真正的风险是 `flock` 块内其他 bash 步骤失败会被 `-e` 静默终止，导致 Python 根本没跑到，
但 dispatch.sh 看到的 CLAIM_EC=1 而非 2，不走 skip 分支，双重 dispatch。

**修复方案：**
- `update-task-status.sh` 的 flock 块用 `( set +e; python3 -c "..." ; UTS_EC=$? )` 包裹，
  或对 flock 块内所有步骤用 `if cmd; then ...; fi` 显式处理，
  确保 Python exit code 始终被正确捕获并传出。
- 简洁方案：将 `set -euo pipefail` 改为只在 flock 块外生效，
  flock 块内用 `|| true` 或显式 `if` 保护每个步骤。

**具体改法：**
```bash
(
flock -x 200
python3 -c "..." 
UTS_EC=$?   # 直接用 $?，不用 PIPESTATUS
) 200>"$LOCK_FILE"
UTS_EC=${UTS_EC:-1}   # flock 子 shell 里的变量不传出——需要用 tmpfile 或其他方式传递
```
**注意：** flock 子 shell 的变量确实不传回父 shell，现有的 `PIPESTATUS[0]` 是唯一能拿到
子 shell 最后一个命令（python3）退出码的方式。真正的修复是：
把 `flock ... ( ... ) 200>lockfile` 改为 `flock 200; python3 ...; UTS_EC=$?; exec 200>&-`，
让 flock 和 python3 在同一 shell 层执行。

**最终方案：** 取消子 shell 包裹，改为：
```bash
exec 200>"$LOCK_FILE"
flock -x 200
python3 -c "..."
UTS_EC=$?
flock -u 200
exec 200>&-
```

---

## H2 — dispatch.sh：mark running 时写入 task.tmux 字段

**根因：** `update-task-status.sh` 只接受 `task_id status [commit] [tokens]` 四个参数，
没有 tmux session 参数。dispatch.sh 调用时没有传 session，导致 task.tmux 字段永远是
注册时写的初始值（可能是 null 或旧值），health-check 读不到正确 session。

**修复方案：** 在 `update-task-status.sh` 加第 5 个可选参数 `[tmux_session]`，
当 `new_status == 'running'` 且 tmux_session 非空时，同时更新 `task.tmux = tmux_session`。

dispatch.sh 调用时改为：
```bash
"$UPDATE_STATUS" "$TASK_ID" "running" "" "" "$SESSION"
```

---

## H3 — heartbeat：改为更新 active-tasks.json 的 task.updated_at

**根因：** dispatch.sh 的 heartbeat 每 5 分钟调用 `update-agent-status.sh` 更新
`agent-pool.json.agents[].last_seen`，但 health-check.sh 的 stuck 判断读的是
`active-tasks.json.tasks[].updated_at`——两个文件、两个字段，heartbeat 无效。

**修复方案：** heartbeat loop 改为调用 `update-task-status.sh "$TASK_ID" "running"` 
（保持 running 状态，但会刷新 updated_at），让 health-check 能感知到 agent 仍活跃。

```bash
# dispatch.sh heartbeat loop 改为：
while true; do
    sleep 300
    tmux has-session -t "$SESSION" 2>/dev/null || break
    "$SCRIPT_DIR/update-task-status.sh" "$TASK_ID" "running" 2>/dev/null || true
done
```

注意：`update-task-status.sh` 的 CAS guard 对 `running → running` 需要放行（当前只允许
`pending/failed → running`），需要在 Python 里加例外：
`running → running` 不是 claim，只是 heartbeat，直接更新 `updated_at` 即可。

---

## H4 — dispatch.sh force-commit：git add -A → git add -u

**根因：** `git add -A` 暂存所有文件（含未跟踪的新文件），可能把 `.env` 等敏感文件推上去。

**修复方案：** 改为 `git add -u`（只 stage 已跟踪文件的修改，不添加新文件）。
同时更新 commit message 标注这是 force-commit fallback。

```bash
# 修改前
git -C "${WORKDIR}" add -A \
  && git -C "${WORKDIR}" commit -m "feat: ${TASK_ID} auto-commit (agent forgot)" \
  && git -C "${WORKDIR}" push

# 修改后
git -C "${WORKDIR}" add -u \
  && git -C "${WORKDIR}" commit -m "chore(${TASK_ID}): force-commit fallback — agent did not commit" \
  && git -C "${WORKDIR}" push
```

此修复需要在 dispatch.sh 生成的两个 runner script 模板（CC JSON 模式和标准模式）里
各改一处。

---

## H5 — SKILL.md：修正自动化程度描述

**根因：** SKILL.md Phase 5 沿用了旧的 webhook 描述（`POST /hooks/agent`），
实际在 2026-03-19 的 v2.5 重构中已改为 `openclaw system event`，但文档没有同步。

**修复范围（SKILL.md 内）：**
1. Phase 5 描述里删除 `POST /hooks/agent` 相关内容，改为说明 `openclaw system event`
2. "Full Auto-Loop" 章节的描述调整为：
   - `on-complete.sh → openclaw system event → orchestrator 被唤醒`
   - `orchestrator（AI）负责：verify commit scope → dispatch review（full 级）→ dispatch next pending`
3. SKILL.md 里所有"自动"字眼加注：指 AI orchestrator 事件驱动响应，不是脚本无人值守
4. Hotfix Flow 里 "DEPLOY-XXX 自动解锁并 dispatch" 改为 "DEPLOY-XXX 自动解锁为 pending；
   orchestrator 被事件唤醒后 dispatch"

---

## 改动文件清单

| 文件 | 改动 | 对应 |
|------|------|------|
| `scripts/update-task-status.sh` | flock 块去子 shell + 加第 5 参数 tmux_session + running→running heartbeat 放行 | H1 + H2 + H3 |
| `scripts/dispatch.sh` | mark running 时传 SESSION 给 update-task-status；heartbeat 改为刷新 task.updated_at；force-commit 改 git add -u | H2 + H3 + H4（两处 runner 模板均需改） |
| `SKILL.md` | 修正 Phase 5 / Full Auto-Loop / Hotfix Flow 的自动化描述 | H5 |

## 任务拆分

- **FIX-H1H2H3**（codex-1）：update-task-status.sh + dispatch.sh 脚本修复（H1+H2+H3 一起改，因为都在同两个文件）
- **FIX-H4**（codex-1）：dispatch.sh force-commit git add -u（可与 H1H2H3 合并，单独拆开更安全）
- **FIX-H5**（codex-1）：SKILL.md 文档修正
- **FIX-REVIEW**（cc-review）：验收三个任务的修改
