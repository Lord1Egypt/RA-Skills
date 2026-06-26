---
name: coze-workflow
description: |
  在 OpenClaw 中调用 Coze Workflow API (stream_run)。
  
  **使用场景：**
  1. 用户需要调用 Coze workflow 执行特定任务
  2. 需要提供 workflow_id、parameters、PAT Key
  3. 处理流式响应结果
  
  **触发关键词：** coze workflow、调用 workflow、运行 workflow、coze 工作流
---

# Coze Workflow Skill

直接在 OpenClaw 中调用 Coze Workflow API。

## 前置配置

设置 **PAT Key** 环境变量：

```bash
export COZE_PAT_KEY="your_pat_token_here"
```

## 使用方法

### 直接使用 curl

```bash
curl -s --location --request POST 'https://api.coze.com/v1/workflow/stream_run' \
  --header "Authorization: Bearer $COZE_PAT_KEY" \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "workflow_id": "your_workflow_id",
    "parameters": {
      "key": "value"
    }
  }' \
  --max-time 120
```

### 保存结果到文件

```bash
curl -s --location --request POST 'https://api.coze.com/v1/workflow/stream_run' \
  --header "Authorization: Bearer $COZE_PAT_KEY" \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "workflow_id": "your_workflow_id",
    "parameters": {
      "key": "value"
    }
  }' \
  --max-time 120 > /tmp/coze_result.txt
```

## 参数说明

| 参数 | 位置 | 说明 |
|------|------|------|
| `workflow_id` | data-raw | Coze Workflow ID |
| `parameters` | data-raw | Workflow 输入参数 (JSON 对象) |
| `COZE_PAT_KEY` | header | PAT Token，通过环境变量传入 |

## 示例

### 示例: 分析创意素材风险

```bash
export COZE_PAT_KEY="your_pat_token_here"

curl -s --location --request POST 'https://api.coze.com/v1/workflow/stream_run' \
  --header "Authorization: Bearer $COZE_PAT_KEY" \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "workflow_id": "7566546276516642834",
    "parameters": {
      "id": "1859150663345201",
      "id_type": "creative"
    }
  }' \
  --max-time 120
```

## 响应格式

流式响应，每行一个事件：

```
id: 0
event: PING
data: {...}

id: 1
event: Message
data: {"content":"...","node_type":"End",...}

id: 2
event: Done
data: {"debug_url":"..."}
```

**关键字段：**
- `event: Message` - 包含 workflow 执行结果
- `event: Done` - 执行完成
- `node_type: End` - 结束节点

## 故障排查

### 超时 (28)
- 原因: API 响应较慢（通常 30-60 秒）
- 解决: 增加 `--max-time 120`

### HTTP 401
- 原因: PAT Key 无效
- 解决: 检查 PAT Key 是否正确

### HTTP 404
- 原因: Workflow ID 不存在
- 解决: 确认 workflow_id

### 连接失败
- 国内网络可能不稳定，重试即可
