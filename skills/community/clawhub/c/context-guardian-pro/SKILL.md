# context-guardian Skill

## Description
该技能用于自动化监控对话上下文压力。当检测到当前会话消息量或 Token 占用达到阈值时，自动触发“总结历史 -> 写入长期记忆 -> 发送 QQ 告警”的闭环流程，以防止 `Context limit exceeded` 错误。

## Usage
用户无需直接调用，该技能通过 `taskflow` 或 `cron` 周期性运行。

## Features
- **Pressure Monitoring**: 监控 Session 消息长度或字符数。
- **Auto-Summarization**: 集成 `summarize` 技能提取核心信息。
- **Memory Persistence**: 自动将摘要追加到 `memory/YYYY-MM-DD.md`。
- **Proactive Alerting**: 通过 `qqbot-channel` 接口向用户发送重启会话的提醒。

## Inputs
- `threshold`: 触发阈值 (默认 80% 字符占用或消息数)。

## Outputs
- `status`: 任务执行结果 (SUCCESS/FAILED)。
- `action_taken`: 采取的操作 (NONE/SUMMARIZED_AND_NOTIFIED)。
