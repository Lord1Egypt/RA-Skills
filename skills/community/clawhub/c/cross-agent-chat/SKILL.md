# SKILL.md - 跨 Agent 通信技能

## 描述
用于在不同 agent 之间进行通信的标准化流程。当需要与其他 agent（机器人）聊天时，使用 `sessions_send` 工具。

## 使用场景

**需要和其他 agent 对话时**：
- 询问其他 agent 的能力或功能
- 请求其他 agent 执行任务
- 跨 agent 协作和沟通

## 工具使用

### sessions_send - 发送消息到其他 session

```json
{
  "sessionKey": "目标 session 的 key",
  "label": "目标 session 的 label",
  "message": "要发送的消息内容",
  "timeoutSeconds": 30
}
```

**参数说明**：
- `sessionKey` 或 `label`：必填其一，用于标识目标 session
- `message`：要发送的消息内容（必填）
- `timeoutSeconds`：超时时间（可选，默认 30 秒）

## 工作流程

### 1. 发现目标 session
使用 `sessions_list` 查找可用的 session：

```bash
sessions_list(activeMinutes=1440, limit=20, messageLimit=2)
```

返回结果包含：
- `key`: session 的唯一标识
- `displayName`: 显示名称
- `kind`: session 类型（group/other等）
- `channel`: 通信渠道

### 2. 发送消息
使用 `sessions_send` 发送消息：

```json
{
  "sessionKey": "agent:xxx:feishu:direct:ou_xxx",
  "message": "你好，请问你可以帮我做什么？"
}
```

### 3. 等待响应
对方 agent 会收到消息并回复，你可以在当前会话中继续对话。

## 重要规则

✅ **应该这样做**：
- 和其他 agent 对话时，统一使用 `sessions_send`
- 明确说明你的意图和需求
- 使用清晰、友好的语言
- 设置合理的超时时间

❌ **不要这样做**：
- 使用 `message` 工具给其他 agent 发送消息（这是给用户渠道用的）
- 直接猜测 sessionKey，先用 `sessions_list` 确认
- 发送模糊或无意义的信息

## 示例对话

### 场景 1：询问另一个 agent 的能力
```json
{
  "sessionKey": "agent:assistant:feishu:direct:ou_xxx",
  "message": "你好！我是玲子，听说你擅长数据分析，可以帮我分析一些测试数据吗？"
}
```

### 场景 2：请求执行任务
```json
{
  "label": "代码助手",
  "message": "请帮我写一个 Python 脚本，用于自动化测试用户登录功能。要求使用 pytest 框架。"
}
```

### 场景 3：跨 agent 协作
```json
{
  "sessionKey": "agent:developer:feishu:group:oc_xxx",
  "message": "我刚才发现了一个 P1 级别的 bug，已经整理好了复现步骤。需要你这边帮忙排查一下代码问题。"
}
```

## 注意事项

1. **权限问题**：确保你有权限访问目标 session
2. **超时处理**：如果目标 agent 没有响应，检查是否在线或超时时间设置是否合理
3. **消息格式**：发送的消息要清晰、简洁、明确
4. **上下文保持**：如果需要延续对话，记住目标 session 的标识

## 故障排查

### 问题：发送失败，提示找不到 session
**原因**：sessionKey 或 label 不正确
**解决**：使用 `sessions_list` 确认正确的 session 标识

### 问题：对方没有回应
**原因**：
- 目标 agent 不在线
- 超时时间太短
- 消息发送失败

**解决**：
- 延长 `timeoutSeconds`
- 检查目标 session 的 `updatedAt` 时间戳确认是否活跃
- 重新发送消息

### 问题：收到错误响应
**原因**：目标 agent 不理解你的请求
**解决**：
- 重新组织消息，更清楚地表达意图
- 提供更多上下文信息
- 简化请求内容

## 最佳实践

1. **先打招呼**：发送请求前，简单介绍自己和意图
2. **明确需求**：清楚说明你想要什么，避免歧义
3. **友好沟通**：使用礼貌、友好的语言
4. **保持简洁**：消息不要过长，突出重点
5. **及时反馈**：收到回复后，及时确认和反馈

---

_跨 agent 协作，让效率倍增_ 🤝