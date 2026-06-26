# Task Completion Verifier

## Problem

Agent 在复杂多步骤任务中"觉得做完了"就停止，但实际上 checklist 里还有未完成的项。Ralph 的迭代计数只能防止过早停止，无法验证任务语义完成度。需要一个确定性的完成度校验机制。

## Solution

Stop hook 读取 `.harness-tasks.json` checklist 文件，逐项检查完成状态。只要存在 `done: false` 的条目，就 block 停止并将未完成项注入 block reason，让 agent 知道还差什么。与 Ralph 互补：Ralph 管"别停"，Task Completion 管"为什么不能停"。

## Implementation

1. 任务启动时创建 `.harness-tasks.json`，格式为 `{tasks: [{name, done}]}`
2. Agent 完成子任务后通过 Bash 调用 `jq` 将对应条目设为 `done: true`
3. Stop hook 读取文件，过滤 `done == false` 的条目
4. 若存在未完成项，返回 `{"decision":"block","reason":"未完成：<具体条目>"}`
5. 所有条目 done 后，放行停止

```json
// .harness-tasks.json
{
  "tasks": [
    {"name": "修改 parser.ts 支持新语法", "done": true},
    {"name": "更新测试用例", "done": false},
    {"name": "更新 README 文档", "done": false}
  ]
}
```

```bash
# Stop hook 核心逻辑
TASK_FILE=".harness-tasks.json"
[ -f "$TASK_FILE" ] || exit 0  # 无 checklist 则放行

REMAINING=$(jq '[.tasks[] | select(.done == false)] | length' "$TASK_FILE")
if [ "$REMAINING" -gt 0 ]; then
  ITEMS=$(jq -r '[.tasks[] | select(.done == false) | .name] | join(", ")' "$TASK_FILE")
  echo "{\"decision\":\"block\",\"reason\":\"未完成项: ${ITEMS}\"}"
else
  echo '{"decision":"allow"}'
fi
```

## Tradeoffs

- **Pro**: 确定性校验，不依赖 LLM 判断，零 API 成本
- **Pro**: Agent 能看到具体缺失项，不会盲目"继续工作"
- **Con**: 需要预先定义 checklist，不适合探索性任务
- **Con**: Agent 可能只是把条目标记为完成但实际没做好（需配合 quality-verification 的 hook 做二次验证）

## Source

Claude Code Stop hook 机制 + OMC persistent-mode 的语义完成度检查思路。与 Pattern 1.1 (Ralph) 叠加使用。
