# Crash Recovery

## Problem

Agent session 因断网、OOM、terminal 关闭等原因 crash 后，留下残留状态：半写的文件、未释放的 lock、处于 "active" 的 ralph.json。新 session 启动后如果不检测这些残留状态，要么从头开始（浪费已完成的工作），要么在残留状态上继续（基于损坏的中间状态工作）。

## Solution

新 session 启动时运行 crash recovery 脚本，扫描残留状态并分类处理：可恢复的状态（ralph.json、task checklist）从断点继续，损坏的状态（半写的文件）回滚到最近的 git checkpoint，过期的 lock 自动清理。

## Implementation

1. 在 UserPromptSubmit hook 中检测残留状态（session 首次触发）

```bash
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')
RECOVERY_FLAG="sessions/${SESSION_ID}/.recovery-checked"

# 只在首次 prompt 时检查
[ -f "$RECOVERY_FLAG" ] && exit 0

RECOVERY_ACTIONS=""

# 1. 检测残留的 ralph 状态
for STATE_FILE in sessions/*/ralph.json; do
  [ -f "$STATE_FILE" ] || continue
  ACTIVE=$(jq -r '.active // false' "$STATE_FILE")
  LAST=$(jq -r '.last_checked_at // ""' "$STATE_FILE")
  if [ "$ACTIVE" = "true" ]; then
    AGE=$(( $(date +%s) - $(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$LAST" +%s 2>/dev/null || echo 0) ))
    if [ "$AGE" -gt 7200 ]; then
      RECOVERY_ACTIONS="${RECOVERY_ACTIONS}发现 stale ralph 状态: ${STATE_FILE} (${AGE}s ago)\n"
      jq '.active = false | .deactivation_reason = "stale"' "$STATE_FILE" > "${STATE_FILE}.tmp" \
        && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    fi
  fi
done

# 2. 清理过期 lock
find .claims -name "*.lock" -mmin +15 -delete 2>/dev/null
STALE_LOCKS=$(find .claims -name "*.lock" -mmin +15 2>/dev/null | wc -l)
[ "$STALE_LOCKS" -gt 0 ] && RECOVERY_ACTIONS="${RECOVERY_ACTIONS}清理了 ${STALE_LOCKS} 个过期 lock\n"

# 3. 检测 .working-state/ 中的计划文件
if [ -f ".working-state/current-plan.md" ]; then
  RECOVERY_ACTIONS="${RECOVERY_ACTIONS}发现前次 session 的工作计划，建议先阅读 .working-state/current-plan.md\n"
fi

touch "$RECOVERY_FLAG"

if [ -n "$RECOVERY_ACTIONS" ]; then
  echo "{\"decision\":\"allow\",\"hookSpecificOutput\":{\"additionalContext\":\"[CRASH RECOVERY] 检测到前次 session 残留状态：\n${RECOVERY_ACTIONS}\"}}"
fi
```

2. 可选：检查 git 状态，提示未提交的变更

```bash
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$UNCOMMITTED" -gt 0 ]; then
  RECOVERY_ACTIONS="${RECOVERY_ACTIONS}发现 ${UNCOMMITTED} 个未提交文件变更\n"
fi
```

## Tradeoffs

- **Pro**: 从断点恢复而非从零开始，节省时间和 token
- **Pro**: 自动清理危险残留（过期 lock、stale ralph）
- **Con**: Recovery 逻辑本身可能误判（把有意保留的状态当残留清理）
- **Con**: 跨平台时间计算（macOS date vs GNU date）需要适配

## Claude Code 内部的 Crash Recovery 实现

Claude Code 源码中的 `conversationRecovery.ts` 提供了三层恢复：

1. **`detectTurnInterruption()`** — 分类 session 最后状态：正常结束、mid-turn 中断、tool call 未完成、parallel tool 部分完成。根据分类注入不同的 synthetic "Continue" 消息。

2. **`filterUnresolvedToolUses()`** — 清理残留的未完成 tool_use：找到没有对应 tool_result 的 tool_use block，移除或补上 placeholder result，防止 API 返回 400。

3. **`recoverOrphanedParallelToolResults()`** — 处理并行工具的残留：多个工具并行执行时如果中途 crash，部分 tool 有 result、部分没有。把有 result 的保留，没 result 的补 placeholder。

这些函数解决的核心问题是：**crash 后 session 的消息链不满足 API 不变量**（每个 tool_use 必须有对应 tool_result）。如果直接 resume，API 会拒绝。

### 对 hook 开发者的启示

如果你写了 crash recovery hook（Pattern 5.2），不需要重复 Claude Code 已有的消息链修复——它在 `--resume` 时自动做。你的 hook 应该聚焦在 Claude Code 管不到的东西：残留 ralph.json、过期 lock 文件、.working-state/ 中的中间产物。

## Source

Claude Code 源码 `conversationRecovery.ts`。OMC persistent-mode 的 stale state detection（`STALE_STATE_THRESHOLD_MS = 7200000`）。Ralph init 脚本的 crash resume 逻辑。
