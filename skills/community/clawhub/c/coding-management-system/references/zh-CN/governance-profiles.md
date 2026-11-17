# 治理级别与文件 2.1

选择足以控制实际风险的最轻治理级别。文件数量不代表严谨。

## Lite

用于 Small、本地、可逆且不需要独立 QA 的工作。

必要文件：

- `Docs/ACTIVE_PACKET.md`
- `Docs/LOOP_RUNS.jsonl`

只有在 `qa_required: false`、自动与功能证据均通过、没有受保护边界或重大风险时才可自验收。不要建立 Program、逐阶段派工、Handoff 或 QA 文件。

## Standard

用于 Medium、重要用户流程、中等不确定性或需要独立评估的工作。

必要文件：

- `Docs/ACTIVE_PACKET.md`
- `Docs/LOOP_RUNS.jsonl`
- 一份最终 `Docs/QA_DECISION_{ID}.md`

只有当 Work Order 能承载稳定范围或责任时才建立一份合并工单。执行终态为 `Ready for Independent Acceptance`；执行 Agent 不能签署最终验收。

## Full

用于 Large、多 Agent、架构、迁移、生产、安全、数据完整性或发布工作。

按需使用这些持久材料：

- `Docs/TARGET.md` 与 `Docs/ACCEPTANCE.md`
- `Docs/ACTIVE_PACKET.md`
- 在责任边界不同时使用一个 Program 和有界 Work Order
- `Docs/LOOP_RUNS.jsonl`
- 独立最终 QA 决策
- 用于 Owner 决策和风险债务的 `Docs/DECISIONS.md`

只在真正的权限边界建立独立 Handoff 或重基线文件。

## 新建文件测试

只有当文件独立承载以下至少一项时才创建：

- 新权限或责任边界；
- 独立最终 QA 决策；
- 改变授权的 Owner 决策；
- Packet 无法承载的跨团队交接；
- 已批准的目标重基线；
- 归档边界。

否则更新规范 Packet，或追加一条 Loop 记录。

## 防文档膨胀规则

- 新 Active Packet 原则上不超过约 120 行。
- 只保留一个立即行动。
- 阶段不是 Milestone、Work Order、Handoff 或文件。
- QA 失败在同一 Packet、同一 Work Order 返修。
- 迁移后停止扩张重复的 STATUS、NEXT、PENDING、COMPLETED、EVALUATION 和逐阶段 Handoff。
- 链接原始证据，只保留精简命令摘要。
- 归档旧材料，不批量重写历史。

## 旧项目采用

只运行一次 Legacy Bootstrap。先索引名称、时间与大小，再选择性读取当前文件。无冲突时建立一个 Active Packet，并把新执行证据写入 `LOOP_RUNS.jsonl`；有冲突时零写入，只提出一个合并后的 Owner 决策请求。
