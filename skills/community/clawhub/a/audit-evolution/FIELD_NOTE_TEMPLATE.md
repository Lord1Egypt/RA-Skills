# Field Note 模板

在你用 Audit Evolution 测试自己的 Agent 后，用这个模板发社区反馈。

```text
Agent:
模型:
输入类型: benchmark 报告 | worklog | 任务输出 | 失败日志 | 用户反馈

Before:
- 原来哪里不清楚？
- 哪个能力维度最弱？
- Agent 容易重复什么错误？

Audit Evolution 输出:
- Snapshot:
- Evolution Card:
- Minimal Skill Patch:
- Field Note:

After:
- 哪些状态变清楚了？
- 下一步最小修复是什么？
- 晋升为长期 skill 前还要验证什么？

Shareable Claim:
一句别人也能测试的话。
```

示例：

```text
Before: 我的 Agent 答案还可以，但没有可复用的记忆更新模式。
After: Audit Evolution 判断 memory 是短板，并生成 trust-ledger patch，包含 verified_fact、stale_claim、confidence、expiry、retrieval_key。
Next test: 只添加这一处 patch 后，再跑一轮同类测试。
```
