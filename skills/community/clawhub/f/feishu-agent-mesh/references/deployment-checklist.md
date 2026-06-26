# Deployment Checklist

## Phase 0 — MVP (≤ 1 hour)
- [ ] 选择共享存储（飞书多维表格 / SQLite / JSON）。
- [ ] 若使用飞书多维表格，创建字段：chat_id、task_id、actor、target、action、content、timestamp、status。
- [ ] 为每个机器人添加轮询任务（≤60s），读取“待处理”记录。
- [ ] 定义记录字段：`chat_id`, `thread_id`, `message`, `actor`, `assignee`, `state`。
- [ ] 机器人发言后写回记录，标记 `handled_by`。
- [ ] 手动约定审批字段，例如 `state=\"needs_approval\"` 时在群里 @ 人类。

## Phase 1 — Recommended Architecture
- [ ] 搭建 Relay Web 服务（Node.js/Python）。
- [ ] 如需先捕获 open_id，部署 `scripts/feishu-callback-server.js` 并接管所有 message.receive 事件。
- [ ] 为每个飞书机器人配置事件订阅 → Relay/回调服务。（校验签名、重试策略）。
- [ ] 创建数据库：
  - [ ] `contexts` 表：chat_id, thread_id, last_actor, summary, payload。
  - [ ] `logs` 表：log_id, chat_id, actor, target, action, content, timestamp。
- [ ] （可选）部署 Redis / MQ 作为 `task_queue`。
- [ ] 机器人注册：
  - [ ] 填写 `scripts/relay-config.example.json` 并改名为 `relay-config.json`。
  - [ ] 包含 `bot_id`, `feishu_open_id`, `capabilities`, `invoke`（HTTP URL 或 CLI）。
- [ ] 在 Relay 中实现：
  - [ ] 消息路由（rules + fallback）。
  - [ ] 日志写入。
  - [ ] 审批 hook（配置 `approval_points`，超时策略）。

## Phase 2 — Advanced Features
- [ ] 意图识别升级（LLM 分类或 DSL）。
- [ ] 无领导讨论流程（参见 workflow-templates）。
- [ ] 异步任务：
  - [ ] Redis stream / 队列消费者。
  - [ ] 超时 / 重试 / 死信队列策略。
- [ ] 多群策略：
  - [ ] chat 白/黑名单。
  - [ ] 每群的限流（每分钟响应次数）与审批规则。
- [ ] 日志归档：定期导出到对象存储或飞书文档。
- [ ] 健康监控：
  - [ ] Relay 心跳。
  - [ ] 机器人状态心跳。
  - [ ] 告警（消息堆积、审批超时、机器人无响应）。
