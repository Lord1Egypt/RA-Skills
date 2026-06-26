# Pattern 19: Git Checkpoint + Auto Rollback（快照与回滚）

## 问题

Agent 执行 Bash 命令可能造成不可逆的破坏——`rm -rf`、`git reset --hard`、`docker rm`。Claude Code 内置的 checkpoint 只追踪 Write/Edit 工具的文件变更，不覆盖 Bash 的副作用。

来源：Claude Code 官方文档 Checkpointing + PostToolUseFailure hook

## 原理

在 Bash 执行破坏性命令前，PreToolUse hook 创建 git 快照。如果命令失败（PostToolUseFailure），自动回滚到快照。

## 实现

### PreToolUse hook（Bash 命令快照）

```bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
[ "$TOOL" = "Bash" ] || exit 0

CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
# 检测破坏性命令
if echo "$CMD" | grep -qE 'rm -rf|git reset --hard|git checkout --|docker rm|kubectl delete'; then
  # 创建快照（先 git add -A 让 untracked 文件进入 index，再 stash create）
  # 注意：git stash create 不支持 --include-untracked，只有 push/save 支持
  git add -A 2>/dev/null
  CHECKPOINT=$(git stash create 2>/dev/null)
  git reset HEAD 2>/dev/null  # 恢复 index 到原始状态
  if [ -n "$CHECKPOINT" ]; then
    echo "$CHECKPOINT" > "sessions/${SESSION_ID}/checkpoint"
    # PreToolUse 不支持 additionalContext，只能用 permissionDecision
    # 这里只记录 checkpoint，不修改工具行为
  fi
fi
# 允许工具执行（不输出任何 JSON = 默认允许）
```

### PostToolUseFailure hook（自动回滚）

```bash
INPUT=$(cat)
CHECKPOINT_FILE="sessions/${SESSION_ID}/checkpoint"
[ -f "$CHECKPOINT_FILE" ] || exit 0

CHECKPOINT=$(cat "$CHECKPOINT_FILE")
git stash apply "$CHECKPOINT" 2>/dev/null
rm -f "$CHECKPOINT_FILE"
echo '{"hookSpecificOutput":{"additionalContext":"Auto-rolled back to checkpoint after tool failure."}}'
```

## 与 Claude Code 内置 checkpoint 的区别

| | 内置 Checkpoint | 本 Pattern |
|---|---|---|
| 覆盖范围 | Write/Edit 工具 | Bash 破坏性命令 |
| 恢复方式 | Esc+Esc 或 /rewind（用户手动） | PostToolUseFailure hook（自动） |
| 存储方式 | Claude Code 内部 | git stash |

## Tradeoff

- 通过先 `git add -A` 可以捕获 untracked 文件，但会短暂改变 index 状态
- 每个破坏性命令前都 stash 会有 I/O 开销
- 命令匹配是 regex——可能误判（`rm -rf` 在代码注释里也会触发）
