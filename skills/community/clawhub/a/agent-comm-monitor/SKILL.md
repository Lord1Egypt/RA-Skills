# Agent 通信监控 Skill

## 简介

此 Skill 用于监控牧者（muzhe）与其他 Agent（司辰、采诗、格物、计相、蒙正）之间的通信状态，确保跨 Agent 消息传递正常，并定期向用户报告通信情况。

## 触发条件

当用户要求以下情况时使用：
- "检查 Agent 通信状态"
- "验证与 XX 的通信"
- "Agent 通信报告"
- "监控通信状态"

## 通信测试流程

### 1. 单向通信测试

使用 `sessions_send` 工具向目标 Agent 发送测试消息：

```
sessions_send(sessionKey="agent:{agent_name}:main", message="【牧者通信测试】这是一条验证消息，请回复确认。测试时间：{current_time}")
```

### 2. 响应判断

| 状态 | 含义 |
|------|------|
| `status: "ok"` + 有 `reply` | ✅ 双向通信正常 |
| `status: "ok"` + 无 `reply` | ⚠️ 单向通信正常，回复可能延迟 |
| `status: "timeout"` | ❌ 通信异常 |

### 3. 备用验证

如果 `sessions_send` 返回超时，使用 `sessions_history` 检查目标 Agent 的会话历史，确认消息是否已送达。

## Agent 列表

| Agent | Session Key | 主要职责 |
|-------|-------------|----------|
| 司辰 | agent:sichen:main | 日历日程管理 |
| 采诗 | agent:caishi:main | 前沿资讯追踪 |
| 格物 | agent:gewu:main | Agent 进化管理 |
| 计相 | agent:jixiang:main | 学习管理 |
| 蒙正 | agent:mengzheng:main | 孩子教育 |

## 报告格式

向用户报告时使用以下精简格式：

```
📊 Agent 通信状态报告

| Agent | 状态 | 响应时间 |
|-------|------|----------|
| 司辰 | ✅ 正常 | <1s |
| 采诗 | ✅ 正常 | <1s |
| 格物 | ✅ 正常 | <1s |
| 计相 | ⚠️ 待测 | - |
| 蒙正 | ✅ 正常 | <1s |

🕐 检测时间：12:24
```

## 注意事项

1. **异步延迟**：跨 Agent 消息可能存在 1-3 秒的异步延迟
2. **超时容忍**：如果 `sessions_send` 超时，等待 5 秒后重新检查会话历史
3. **精简报告**：向用户报告时使用表格形式，保持简洁
4. **异常记录**：如果发现异常，记录到 MEMORY.md 中

## 紧急异常处理

如果某个 Agent 连续 3 次通信失败：
1. 记录到 HEARTBEAT.md 的异常日志中
2. 在下次 heartbeat 时提醒用户
3. 建议用户检查该 Agent 的运行状态
