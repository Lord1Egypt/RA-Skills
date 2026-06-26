# Review-Execution Separation

## Problem

同一个 agent 既写代码又 review 自己的代码，会有确认偏误——agent 倾向于认为自己写的代码是对的。特别是在长 session 中，agent 对自己前几轮的决策有"沉没成本"心理，不愿推翻。

## Solution

用两个独立 agent 分别负责 implementation 和 review。两者运行在完全隔离的 session 中——review agent 看到的是代码本身，不知道 implementation agent 的推理过程。这种"盲审"迫使 review agent 从第一性原理判断代码质量。

## Implementation

1. **Implementation agent**：带完整任务上下文，执行编码

```bash
claude -p --max-turns 60 \
  "$(cat task-description.md)" \
  > .coordination/impl-output.md
```

2. **Review agent**：只看代码和需求，不看 implementation agent 的推理

```bash
# 收集变更的 diff
git diff main > .coordination/changes.diff

# Review agent 独立 session
claude -p --max-turns 20 \
  "$(cat <<PROMPT
审查以下代码变更。对照原始需求检查：
1. 功能是否正确实现
2. 是否有遗漏的边界情况
3. 是否引入了 regression

需求：$(cat task-description.md)

变更：$(cat .coordination/changes.diff)

输出结构化 review 结果到 .coordination/review-result.json：
{"approved": bool, "issues": [...], "suggestions": [...]}
PROMPT
)"
```

3. **Coordinator 处理 review 结果**

```bash
APPROVED=$(jq -r '.approved' .coordination/review-result.json)
if [ "$APPROVED" = "false" ]; then
  ISSUES=$(jq -r '.issues | join("\n")' .coordination/review-result.json)
  # 将 review 问题反馈给 implementation agent（新 session）
  claude -p --max-turns 30 \
    "修复以下 review 问题：${ISSUES}"
fi
```

4. 可选的高级配置：两个 agent 使用不同模型（如 implementation 用 Claude，review 用 GPT）增加视角多样性

## Tradeoffs

- **Pro**: 消除确认偏误，review agent 没有"沉没成本"
- **Pro**: 可以用不同模型组合，互补盲区
- **Con**: 成本翻倍——每个任务至少两个 agent session
- **Con**: Review agent 缺乏实现上下文，可能提出不切实际的修改建议

## Source

本项目的蒸馏实践——Codex 做 review、Claude Code 做 execution 的双 agent 模式。经典的代码审查最佳实践在 agent 场景下的适配。
