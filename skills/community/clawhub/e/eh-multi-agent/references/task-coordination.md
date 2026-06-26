# File-Based Task Coordination

## Problem

多个 agent 并行工作时需要知道：哪些任务已被领取、哪些正在进行、哪些已完成。没有中心化的任务状态，agent 会重复做同一件事或遗漏任务。MCP server 等进程内通信方案在跨 session 场景下不可用——agent 运行在不同 tmux pane、甚至不同机器上。

## Solution

用 JSON 文件作为共享任务板。每个任务有 `pending/claimed/done/failed` 四种状态，领取时写入 claim 者的 session-id。通过 lockfile 做并发控制，防止两个 agent 同时领取同一任务。

## Implementation

1. Coordinator 创建任务文件 `.coordination/tasks.json`

```json
{
  "tasks": [
    {"id": "t1", "description": "修改 parser.ts", "status": "pending", "claimed_by": null, "result": null},
    {"id": "t2", "description": "修改 visitor.ts", "status": "pending", "claimed_by": null, "result": null},
    {"id": "t3", "description": "写测试", "status": "pending", "claimed_by": null, "result": null}
  ],
  "updated_at": "2026-04-06T10:00:00Z"
}
```

2. Worker 领取任务（带锁）

```bash
LOCKFILE=".coordination/tasks.lock"
TASKFILE=".coordination/tasks.json"

# 获取锁（重试 10 次，指数退避 50-500ms）
for i in $(seq 1 10); do
  if mkdir "$LOCKFILE" 2>/dev/null; then
    # 找第一个 pending 任务并领取
    TASK_ID=$(jq -r '.tasks[] | select(.status == "pending") | .id' "$TASKFILE" | head -1)
    if [ -n "$TASK_ID" ]; then
      jq --arg id "$TASK_ID" --arg sid "$SESSION_ID" \
        '(.tasks[] | select(.id == $id)) |= (.status = "claimed" | .claimed_by = $sid)' \
        "$TASKFILE" > "${TASKFILE}.tmp" && mv "${TASKFILE}.tmp" "$TASKFILE"
    fi
    rmdir "$LOCKFILE"
    break
  fi
  sleep "0.$(( 50 * i ))"
done
```

3. Worker 完成后更新状态

```bash
# 标记完成（同样需要锁）
jq --arg id "$TASK_ID" --arg result "$RESULT_FILE" \
  '(.tasks[] | select(.id == $id)) |= (.status = "done" | .result = $result)' \
  "$TASKFILE" > "${TASKFILE}.tmp" && mv "${TASKFILE}.tmp" "$TASKFILE"
```

4. Coordinator 轮询任务状态，所有 done 后进入 synthesis 阶段

## Tradeoffs

- **Pro**: 零依赖——只需要文件系统，跨 session、跨机器可用
- **Pro**: 状态可审计——JSON 文件可以随时查看
- **Con**: Lockfile 竞争在高并发下效率低（>10 agent 可能需要更好的方案）
- **Con**: 没有 watch/notify 机制，只能轮询

## Claude Code Swarm 的邮箱 IPC 实现

Claude Code 的 Swarm 模式（~6,800 行，30 文件）使用 file-based mailbox：

- **路径**: `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`
- **并发控制**: lockfile + 指数退避（10 次重试，5-100ms）
- **消息类型**: 10 种，包括 `permission_request/response`、`shutdown_request`、`plan_approval_request`
- **后端检测优先级**: tmux > iTerm2 > in-process（`backends/registry.ts`）
- **tmux 实现**: PID-scoped sockets（`claude-swarm-{pid}`），每个 agent 一个 pane
- **in-process fallback**: 同一 Node.js 进程内跑多个 query loop

与本 Pattern 的关系：Claude Code 的实现和我们的 `tasks.json` + lockfile 方案思路一致。但它用了 per-agent inbox（每个 agent 一个 JSON 文件）而不是共享的 tasks.json。Per-agent inbox 在高并发下锁竞争更少——每个 agent 只写自己的 inbox，读别人的 inbox 不需要锁。

## Source

Claude Code 源码 swarm 模块。OMC Swarm 模式的 file-based mailbox 机制。
