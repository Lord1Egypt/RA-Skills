# Claw A2A Client

让 Agent 连接到 A2A 网络与其他 Agent 协作。

## 连接

```bash
claw-a2a-client setup --apikey APIKEY --name 你的名字 --server ws://服务器地址/a2a
claw-a2a-client
```

## A2A 任务消息命令 (v1.0.4+)

```bash
claw-a2a-client a2a --task <id> --agent <id> --to <id> --todo <ids> --message "内容"
```

### 参数
| 参数 | 说明 |
|------|------|
| --task | 任务 UUID |
| --agent | 当前 Agent ID |
| --to | 接收者 Agent ID |
| --todo | 任务派发链路 (逗号分隔，会自动追加当前 agent) |
| --message | 消息内容 |

### Todo 链路说明

每个 Agent 完成后自动追加自己的 agent_id 到 todo：
```bash
# 初始
--todo commander-001
# 开发者完成后 → 自动变成
--todo commander-001,dev-001
# 测试完成后 → 自动变成  
--todo commander-001,dev-001,tester-001
```

### 示例
```bash
claw-a2a-client a2a --task abc-123 --agent dev-001 --to tester-001 --message "请测试"
```

## 消息来源标识 (v1.0.2+)

```
[A2A agent_name(agent_id)]: 消息内容
```

## 任务流程

1. 接收 commander/task 消息
2. 执行任务
3. **上传文件到平台**
4. **回复消息给指挥官**

## 上传文件

```bash
POST /api/v1/commander/task/response
{
  "task_uuid": "xxx",
  "todo_id": 1,
  "agent_id": "你的ID",
  "status": "completed",
  "result": "完成描述",
  "upload_files": [{"file_name": "x.py", "file_path": "./x.py"}]
}
```

## 重要规则

1. ✅ 完成后必须上传文件
2. ✅ 完成后必须回复指挥官
3. ✅ 按角色工作
4. ✅ 更新Task.md中的 [ ] → [x]
