# async-command

**When to use async and how to stop long-running commands.**

## The Core Insight

Every long command is an opportunity to do something useful while waiting — or a trap that freezes you out.

**Blocking**: You run `make build`, wait 5 minutes, do nothing.
**Async**: You start `make build`, it runs in background, you do other things, check back later.

Rule of thumb: If a command takes longer than you want to wait, it should run async.

## When to Go Async

| Situation | Block or Async? |
|-----------|-----------------|
| Database migration (30s+) | **Async** |
| `pip install` 50 packages | **Async** |
| Build a Docker image | **Async** |
| `curl` a quick API | Block |
| Read a config file | Block |
| File search in small dir | Block |
| Compiling large project | **Async** |
| Running tests | **Async** |
| Watching logs | **Async** |

## The Pattern (Universal)

```python
# 1. Start in background, yield to not block
exec(command="...", yieldMs=30000)

# 2. While waiting, do other things
# (this is the key benefit - you're not frozen)

# 3. When ready, check result
process(action="poll", sessionId="<session_id>", timeout=60000)
```

## The Universal Steps

**Step 1: Start without blocking**
```python
exec(command="your command here", yieldMs=60000)
```
`yieldMs` = how long to wait before backgrounding. Longer = more output captured.

**Step 2: Manage the background job**
```python
# Check if done
process(action="poll", sessionId="<session_id>", timeout=0)

# Wait for completion
process(action="poll", sessionId="<session_id>", timeout=60000)

# Get partial output
process(action="log", sessionId="<session_id>")

# Stop it
process(action="kill", sessionId="<session_id>")
```

**Step 3: Done.**

## Common Mistakes

**Mistake 1**: Blocking a long command with a 5-minute timeout
```
# ❌ What most people do
exec(command="make build", timeout=300)
# Waits 5 minutes, then fails anyway

# ✅ Async approach
exec(command="make build", yieldMs=10000)
# Starts building, returns immediately, you decide when to check
```

**Mistake 2**: Not using process tool to check results
```
# ❌ Re-running to "check"
exec(command="make build", yieldMs=60000)
# ...then running it again with exec!
# This starts a SECOND build, wastes resources

# ✅ Use the process session
process(action="poll", sessionId="<session_id>", timeout=120000)
```

**Mistake 3**: Forgetting about background jobs
```
# Start something, then forget about it
exec(command="python train_model.py", yieldMs=10000)
# (goes on with other work, never checks back)

# ✅ Track it, check back periodically
exec(command="python train_model.py", yieldMs=10000)
# ...later:
process(action="poll", sessionId="<session_id>", timeout=60000)
```

## Emergency Stop: "Stop Now"

**Scenario**: You started a long operation, need to abort immediately.

**How it works**:
1. Run long commands with `yieldMs` (background mode) — the agent stays responsive
2. Ken says "stop" or runs `nek_stop`
3. Agent kills the background job immediately

**Why yieldMs matters**: Commands run in background (yieldMs > 0), agent can respond to messages and process actions even while command is running. Without yieldMs, the agent is blocked and cannot respond.

**To stop immediately**: Say "stop", "停止", or any clear stop signal. The agent checks for stop on every heartbeat and before any new command, and will immediately kill all background jobs.

**Key rule**: For any command that might need interruption, always use `yieldMs`. The agent stays alive and responsive.

## When NOT to Use

- Command is fast (< 5 seconds)
- You need the result before proceeding
- It's destructive and you want to confirm first

## Mental Model

Think of async like a餐厅点菜：

1. 你点了菜（exec → 开始运行）
2. 等着的时候可以做别的事（做其他任务）
3. 好了叫你来取（poll → 检查结果）
4. 可以中途退菜（kill → 停止进程）

不要站在厨房门口等菜做完了才去结账。
