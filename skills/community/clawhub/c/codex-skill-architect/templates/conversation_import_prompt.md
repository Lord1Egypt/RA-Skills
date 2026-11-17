# 当前已开对话导入提示

## 用户

```text
把总结过的长对话导入当前对话，继续讨论 <问题>
```

## 执行规则

1. 运行 `scripts/find_conversation_handoff.py` 或 `scripts/import_conversation_handoff.py --topic <问题>`。
2. 读取最新 `conversation-snapshot.md` 和 `routing-index.md`。
3. 按路由索引只读取与 <问题> 匹配的技能包。
4. 不复制旧对话完整历史，只加载快照摘要和当前话题技能包。

## 注意

- 导入当前对话仍会消耗快照和技能包的 Token，但不是复制完整旧对话。
- 若没有指定话题，先只读快照和路由索引，再询问用户要处理哪个话题。
