# Logging & Approval Schema

本阶段默认将日志写入飞书多维表格（Bitable）。建议字段：`序号`（自动）、`chat_id`、`task_id`、`actor`、`target`、`action`、`content`、`timestamp`、`status`。也可同步写数据库，但必须保证飞书表格能实时查看。

## Log Table (Recommended)
| Field | Type | Description |
| --- | --- | --- |
| `log_id` | UUID | 唯一 ID |
| `timestamp` | ISO8601 | 事件时间 |
| `chat_id` | string | 飞书群 ID |
| `thread_id` | string/null | 引用消息 ID（可空） |
| `task_id` | string | chat_id + logical task identifier |
| `actor` | string | 发起机器人或用户（open_id） |
| `target` | string | 被调用机器人/用户 |
| `action` | enum | e.g. `message`, `assignment`, `queue_enqueue`, `approval_request`, `approval_result` |
| `content` | jsonb | 主要 payload（文本摘要、路径、文件链接） |
| `status` | enum | `success`, `failed`, `retrying` |
| `latency_ms` | int | 可选，用于性能监控 |

## Approval Hooks
Configure per chat_id:
```json
{
  "chat_id": "oc_xxx",
  "approval_points": [
    {
      "name": "plan_signoff",
      "trigger": "state == 'ready_for_plan_approval'",
      "summary_fields": ["task_id", "owner", "next_steps"],
      "timeout_minutes": 10,
      "on_timeout": "notify-human"
    }
  ]
}
```
- 当触发条件为真，Relay 自动从上下文抽取字段→在群里 @ 人类。
- 人类回复 `同意/拒绝` 或点击互动按钮，Relay 将结果写入 `logs` 并继续后续流程。

## Storage Rotation
- **Hot data**：最近 7-30 天保留在主库，供排查。
- **Warm data**：定期导出为 CSV/Parquet 上传对象存储。
- **Cold data**：可选地同步到飞书文档、Notion 等供产品/运营查看。

## Audit Tips
- 所有跨机器人调用都必须在日志中留下双向记录（A 调用 B、B 返回结果）。
- 关联 `task_id` 方便还原整个任务链；`chat_id` + `task_id` 能唯一定位某次协作。
- 为审批相关的 log 加上 `approval_id`，方便独立审计。
