# 简化续接提示

## 老对话

```text
帮我总结这个长对话，生成 conversation-snapshot.md、技能包和 routing-index.md，完成后告诉我输出路径。
```

## 新对话

```text
继续讨论 <问题>。先读取 conversation-output/conversation-snapshot.md 和 conversation-output/routing-index.md，按需加载对应技能包。
```

## 继续规则

- 先展示 `conversation-snapshot.md` 中的“老对话最后一段回答”。
- 不自动执行老对话中的瘦身、修改、蒸馏等任务。
- 停止并让用户决定下一步操作。
