# Memory Ledger Entry 示例

Audit Evolution 的记忆层不是把所有日志都塞进长期记忆，而是只保存下一轮真的会用到的少量事实、反馈、决策和检索 key。

## 候选记忆

```yaml
memory_type: skill_patch
source_evidence:
  - "latest benchmark receipt"
  - "local dry-run receipt"
confidence: medium
expiry: "next benchmark or when contradicted"
retrieval_key: "act_direct_execution"
owner_or_role: "agent"
write_target: "proposed_only"
content: "Act 类任务优先输出：目标/边界 -> 最小工具链 -> action map -> idempotency -> evidence receipt -> stop condition。"
```

## 写入判断

```text
可以保存:
- 有明确证据来源。
- 能帮助下一轮恢复状态或选择行动。
- 有 confidence 和 expiry。
- 不含 API key、credentials、cookies、客户数据或私有路径。

不要保存:
- 整段脏日志。
- 模型猜测。
- 已经过期的 claim。
- 没有证据的 completed 声明。
```

## 推荐落点

```text
已有 worklog -> 写入 worklog 的 Memory Ledger 段。
已有 handoff -> 写入 handoff 的 Next-Run Bootstrap 段。
已有 dashboard -> 写入 dashboard 的最近决策/检索 key。
没有持久层 -> 先保持 proposed_only，等待人类指定位置。
```
