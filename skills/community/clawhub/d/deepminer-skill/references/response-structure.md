# thread.result 返回结构解析

## 顶层结构

```json
{
  "status_code": 200,
  "message": "success",
  "data": {
    "state": "running | completed",
    "thread_id": "xxx",
    "last_messages": [...]
  }
}
```

**关键字段：**

- `state` — 任务状态，可能的值：
  - `running` — 任务进行中，继续轮询
  - `completed` — 任务完成，解析结果
  - `ask_human` — 需要用户确认，回复继续
  - `async_tag_task` — **异步任务已提交，需在 DM 平台 GUI 确认** ⚠️
- `last_messages` — 消息数组，按时间顺序排列（最后一条是最新的）

## last_messages 消息类型

### assistant 消息（文字回复）

```json
{
  "message_id": "uuid",
  "type": "assistant",
  "content": "{\"role\": \"assistant\", \"content\": \"文字内容...\", ...}",
  "created_at": "2026-04-03T07:38:21.843752+00:00",
  "metadata": "{\"worker_name\": \"supervisor\", \"worker_id\": \"xxx\", ...}"
}
```

**解析步骤：**

1. 找 `type: "assistant"` 的消息
2. `content` 是 JSON 字符串，需 parse
3. 取 parse 后的 `.content` 字段即为文字回复

**metadata 字段：**

- `worker_name` — 处理任务的 worker 类型（如 `supervisor`, `taobao_worker`）
- `observation_id`, `trace_id` — 追踪信息

### tool 消息（文件输出）

```json
{
  "message_id": "uuid",
  "type": "tool",
  "content": "{\"name\": \"final_files\", \"artifact\": {...}}",
  "status": "success"
}
```

**解析步骤：**

1. 找 `type: "tool"` 且 `name: "final_files"` 的消息
2. `content` 是 JSON 字符串，需 parse
3. 取 `artifact.attachments` 数组获取文件链接

**attachments 结构：**

```json
[
  {"type": "file", "data": "https://.../报告.html"},
  {"type": "file", "data": "https://.../数据.csv"}
]
```

每个 attachment 的 `data` 字段是可直接访问的文件 URL。

## 解析原则

⚠️ **必须遍历所有 `last_messages`，提取每条消息的内容！**

常见遗漏场景：
- tool 消息包含多个文件（如 HTML 报告 + CSV 原始数据）
- 多条 assistant 消息（如中间进度 + 最终回复）

**正确做法：遍历整个数组，逐一提取并汇总告知用户。**

```json
{
  "data": {
    "state": "completed",
    "last_messages": [
      {
        "type": "tool",
        "content": "{\"name\": \"final_files\", \"artifact\": {\"attachments\": [{\"type\": \"file\", \"data\": \"<endpoint>/files/.../报告.html\"}]}}"
      },
      {
        "type": "assistant",
        "content": "{\"content\": \"我已完成分析...\"}"
      }
    ]
  }
}
```

**正确提取逻辑（遍历所有消息）：**

```python
# 伪代码 - 必须遍历整个 last_messages 数组
files = []
text_replies = []

for msg in last_messages:
    content = json.loads(msg["content"])
    
    if msg["type"] == "tool":
        if content.get("name") == "final_files":
            attachments = content["artifact"]["attachments"]
            # 每个文件都要记录！
            for att in attachments:
                files.append(att["data"])
    
    if msg["type"] == "assistant":
        text_replies.append(content["content"])

# 汇总告知用户
print("文件输出:", files)  # ["https://.../报告.html", "https://.../数据.csv"]
print("文字回复:", text_replies)  # ["我已完成分析..."]
```

**错误示范（只取第一条）：**

❌ 只提取第一个文件，漏掉 CSV
❌ 只看最后一条消息，漏掉中间的进度信息

## worker_name 参考

| worker_name | 功能 |
|-------------|------|
| `supervisor` | 总控，协调任务 |
| `taobao_worker` | 淘宝数据查询 |
| 其他 worker | 按任务类型分配 |

通过 `metadata.worker_name` 可识别任务由哪个专业模块处理。

## async_tag_task 状态（异步任务）

⚠️ **当 `state: "async_tag_task"` 时，必须提示用户去 DM 平台 GUI 确认！**

异步任务已提交到后台队列，但不会自动开始执行，需要用户在 DM 平台进行 GUI 操作确认。

### 直接读取 status_info 字段

**不需要解析复杂的 messages！** 直接从 `data.status_info` 获取任务信息：

```json
{
  "data": {
    "state": "async_tag_task",
    "status_info": {
      "task_id": "5f56f532-f11f-4405-8a2c-9032fe8b059c",
      "task_name": "社媒内容品牌名称标注",
      "tool_name": "submit_async_task"
    }
  }
}
```

**关键字段：**

| 字段 | 说明 |
|------|------|
| `status_info.task_id` | 任务ID |
| `status_info.task_name` | 任务名称 |
| `status_info.tool_name` | `submit_async_task` 表示异步任务 |

### 提示用户的内容

检测到 `state: "async_tag_task"` 后，**必须告知用户：**

> ⚠️ **异步任务已提交（任务ID: {task_id}，任务名称: {task_name}）**
> 
> 请前往 **DM 平台** 进行 GUI 确认操作，任务才会开始执行。