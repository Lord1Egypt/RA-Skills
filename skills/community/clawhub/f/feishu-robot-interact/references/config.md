# 飞书机器人通信配置指南

## 环境变量配置

在运行环境中设置以下环境变量：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `FEISHU_ROBOT_ID` | 本机器人的 open_id | `ou_xxxxx` |
| `FEISHU_ROBOT_NAME` | 机器人名称 | `小龙虾` |
| `FEISHU_DEVELOPER_ID` | 开发者 open_id，用于发送确认请求 | `ou_xxxxx` |
| `MEMORY_PATH` | 偏好记忆存储路径 | `~/.openclaw/workspace/memory/robot_confirm.json` |

## 飞书机器人配置

### 1. 创建机器人

1. 打开飞书开放平台 → 创建企业自建应用
2. 添加机器人能力：消息订阅、群聊权限

### 2. 配置回调事件

需要订阅以下事件：
- `im.message.message_created` - 消息创建事件

### 3. 获取 ID

- **机器人 ID**: 应用凭证 → App ID
- **开发者 ID**: 在飞书中查看自己 → 复制用户 ID

## 使用流程

### 场景：机器人A和机器人B协作

**机器人B** 在群里@**机器人A**：

```
@小龙虾 请帮我查询今天的销售数据
```

### 机器人A 处理流程

1. **接收消息** → 解析出@了自己的机器人ID
2. **提取任务** → "请帮我查询今天的销售数据"
3. **检查记忆** → 首次任务，需要确认
4. **发送确认请求** 给开发者：

```
🤖 收到新任务请求
📋 任务内容：请帮我查询今天的销售数据

请回复：
- "确认" 执行任务
- "确认+不再询问" 执行任务并记住偏好
- "拒绝" 不执行
```

5. **开发者回复** → "确认"
6. **执行任务** → 调用数据查询服务
7. **群内回复结果**：

```
✅ 任务已完成
📋 任务内容：请帮我查询今天的销售数据
🔧 执行结果：今日销售额 12,345 元
```

### 第二次相同任务

如果开发者之前回复"确认+不再询问"，则直接执行，不再询问。

## 记忆文件格式

`~/.openclaw/workspace/memory/robot_confirm.json`:

```json
{
  "请帮我查询今天的销售数据": {
    "status": "confirmed",
    "confirmed_at": "2026-03-27T10:30:00",
    "ask_again": false
  },
  "请同步库存数据": {
    "status": "rejected",
    "confirmed_at": "2026-03-27T11:00:00",
    "ask_again": true
  }
}
```

## 集成到 OpenClaw

1. 将 `feishu-robot-interact` skill 放入 `~/.openclaw/workspace/skills/`
2. 配置环境变量
3. 飞书消息事件通过 OpenClaw 的飞书插件接收
4. 在 Agent 中调用 `robot_interact.py` 处理消息