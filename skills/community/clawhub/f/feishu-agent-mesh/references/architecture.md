# Architecture Guide

## Core Components
1. **Feishu Bot Apps (existing identities)**
   - 每个机器人仍使用自己的飞书应用（例如 Coordinator Bot、Specialist Bot …）。
   - 事件订阅全部指向同一个 Relay 服务。
2. **Relay Service**
   - Web 服务（Node.js/Python 任一）负责：接收事件、写入上下文、调度任务、落日志、触发审批。
   - 暴露内部 API（HTTP/CLI）供机器人注册与心跳。
3. **Shared State Store**
   - 推荐：Postgres/MySQL (上下文 + 日志) + Redis (异步队列)。
   - MVP：飞书多维表格 / SQLite / JSON 文件。
4. **Worker Agents (OpenClaw instances)**
   - 各自暴露 `/tools/invoke`（或 CLI 接口）供 Relay 调用具体能力。
   - 定期向 Relay 报告可用能力、健康状态。

## Message Flow (Recommended)
```
User @Coordinator Bot --> Feishu Event --> Relay
   Relay writes context(chat_id) + logs entry
   Relay decides routing --> /tools/invoke Specialist Bot
Specialist Bot 处理后 --> 发言到群 + 回写 Relay
```

## Storage Considerations
| Layer | Option | Notes |
| --- | --- | --- |
| Context | Postgres table `contexts`（chat_id, thread_id, last_actor, payload） | 每条记录 <4 KB，轻量 |
| Logs | Postgres table `logs` 或对象存储 | 可按 chat_id + date 分区 |
| Queue | Redis list / Stream | 控制并行数、过期策略 |
| Archive | 对象存储 / 飞书文档 | 周期性迁出历史日志 |

## Multi-group Isolation
- 所有表都以 `chat_id` 为主键或前缀。
- 为每个 chat 维护配置（审批节点、限流、是否允许自动回应）。
- 当机器人收到来自未知 chat 的请求时，默认拒绝或降级为人工提醒。

## Fault Domains
- Relay 可部署成无状态服务，背后数据库做高可用；
- 机器人实例各自独立，任何一台宕机不会影响其它机器人，只需 Relay 标记其状态不可用。

## Scaling Tips
- 将 `routes` 和 `capabilities` 定义在配置文件（见 scripts/relay-config.example.json），方便新增机器人。
- 如果机器人越来越多，可把 Relay 拆成两个模块：事件入口（Feishu）和任务调度（队列消费者）。
- 对于跨租户需求，增加 `tenant_id` 维度即可。
