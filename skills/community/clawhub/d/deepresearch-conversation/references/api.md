# DeepResearch Agent API 接口文档

## 目录
1. [鉴权方式](#鉴权方式)
2. [创建会话接口](#创建会话接口)
3. [发起研究接口](#发起研究接口)
4. [请求参数详解](#请求参数详解)
5. [SSE 响应结构](#sse-响应结构)
6. [各阶段响应示例](#各阶段响应示例)

---

## 鉴权方式

所有接口使用 API Key 鉴权，在 HTTP Header 中传入：

```
Authorization: Bearer {api_key}
```

---

## 创建会话接口

**接口地址**: `POST /v2/agent/deepresearch/create`

**请求 Body 参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 否 | 深度研究 Agent ID。若与 `version` 同时提供，以 `agent_id` 为准 |
| `version` | string | 否 | 版本选择：`lite`（轻量版，默认）、`standard`（标准版）、`pro`（高级版）。都不提供时默认 `lite` |

**请求示例（使用 version）**:
```bash
curl -X POST "https://qianfan.baidubce.com/v2/agent/deepresearch/create" \
  -H "Authorization: Bearer {api_key}" \
  -H "Content-Type: application/json" \
  -d '{"version": "lite"}'
```

**请求示例（使用 agent_id）**:
```bash
curl -X POST "https://qianfan.baidubce.com/v2/agent/deepresearch/create" \
  -H "Authorization: Bearer {api_key}" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "xxx"}'
```

**响应示例**:
```json
{
  "request_id": "e84f1058-0b15-4983-ba18-ed140bd480aa",
  "result": {
    "conversation_id": "de65bd4c-f44f-4081-8435-9f99e671d18b"
  }
}
```

---

## 发起研究接口

**接口地址**: `POST /v2/agent/deepresearch/run`

响应为 **SSE 流式数据**，每行格式为 `data: {JSON}` 或 `data:{JSON}`。

---

## 请求参数详解

### 必填参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `query` | string | 用户输入。发起研究时填研究问题；回复澄清时填 `"跳过"`；确认大纲时填 `"确认"` |

### 可选参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `agent_id` | string | 深度研究 Agent ID，可选。若与 `version` 同时提供，以 `agent_id` 为准 |
| `version` | string | 版本选择：`lite`（轻量版，默认）、`standard`（标准版）、`pro`（高级版）。与 `agent_id` 都可选，都不提供时默认 `lite` |
| `conversation_id` | string | 会话 ID，首轮可不填，后续轮次必填 |
| `interrupt_id` | string | 中断 ID，在确认大纲时必填，从上一轮 SSE 响应中获取 |
| `structured_outline` | object | 确认大纲时携带，使用 Agent 生成的大纲原样传回 |
| `file_ids` | array | 文件 ID 列表（需先上传文件） |

### version 参数说明

| 值 | 说明 |
|------|------|
| `lite` | 轻量版（**默认**），速度快，适合快速调研 |
| `standard` | 标准版，均衡模式，深度与速度兼顾 |
| `pro` | 高级版，最详尽，适合深度研究报告 |

> **注意**: `agent_id` 和 `version` 都是可选参数。若同时提供，以 `agent_id` 为准；都不提供时默认使用 `version=lite`。

### structured_outline 结构

```json
{
  "locale": "简体中文",
  "title": "报告标题",
  "description": "报告摘要，指导全文写作",
  "sub_chapters": [
    {
      "title": "章节标题",
      "description": "章节写作指引",
      "sub_chapters": [
        {
          "title": "子章节标题",
          "description": "子章节写作指引",
          "sub_chapters": []
        }
      ]
    }
  ]
}
```

### 各阶段请求示例

**Step 2 - 发起初始查询（使用 version）**:
```json
{
  "query": "研究AI市场规模",
  "version": "lite",
  "conversation_id": "yyy"
}
```

**Step 2 - 发起初始查询（使用 agent_id）**:
```json
{
  "query": "研究AI市场规模",
  "agent_id": "xxx",
  "conversation_id": "yyy"
}
```

**Step 3 - 跳过澄清（自动）**:
```json
{
  "query": "跳过",
  "version": "lite",
  "conversation_id": "yyy"
}
```

**Step 5 - 自动确认大纲**:
```json
{
  "query": "确认",
  "version": "lite",
  "conversation_id": "yyy",
  "interrupt_id": "1b6696fd-1f68-4a3e-a3e3-a6d771504f08",
  "structured_outline": {
    "locale": "简体中文",
    "title": "全球人工智能市场研究与战略分析报告",
    "description": "本报告全面分析全球AI市场...",
    "sub_chapters": [...]
  }
}
```

---

## SSE 响应结构

每行 SSE 数据解析后得到：

```json
{
  "request_id": "string",
  "conversation_id": "string",
  "trace_id": "string",
  "role": "assistant | tool",
  "status": "running | done | interrupt",
  "content": [
    {
      "name": "/chat/chat_agent | /toolcall/interrupt | /toolcall/structured_outline | ...",
      "type": "text | json | files | references | plan",
      "text": {/* 内容，结构因 type 而异 */},
      "event": {
        "id": "string",
        "name": "string",
        "status": "running | done | interrupt",
        "is_end": false,
        "is_stop": false,
        "create": 1712345678000  // Unix 毫秒时间戳
      }
    }
  ]
}
```

### 特殊 type 说明

**type=json（中断/大纲数据）**:
```json
{
  "text": {
    "data": "<嵌套的JSON字符串，需二次解析>"
  }
}
```

**type=files（生成的文件）**:
```json
{
  "text": {
    "filename": "report_xxx.md",
    "url": "https://...",
    "download_url": "https://..."
  }
}
```

**type=references（搜索引用）**:
```json
{
  "text": {
    "title": "文章标题",
    "content": "文章摘要"
  }
}
```

---

## 各阶段响应示例

### 需求澄清阶段（event.name="/chat/chat_agent"，脚本自动跳过）

```
data: {"role":"assistant","status":"running","content":[{"name":"/chat/chat_agent","type":"text","text":{"info":"您希望侧重于技术发展趋势还是商业应用场景？"},"event":{"id":"msg-01","status":"running","name":"/chat/chat_agent"}}]}

data: {"role":"tool","status":"interrupt","content":[{"name":"/toolcall/interrupt","type":"json","text":{"data":"{\"interrupt_id\":\"1b6696fd-...\",\"interrupt_type\":\"deep_research_coordinator\",\"wait_for\":[\"query\"]}"},"event":{"id":"evt-int-01","status":"interrupt","name":"/toolcall/interrupt"}}]}
```

### 大纲生成阶段（event.name="/toolcall/structured_outline"，脚本自动确认）

```
data: {"role":"tool","status":"done","content":[{"name":"/toolcall/structured_outline","type":"json","text":{"data":"{\"title\":\"...\",\"description\":\"...\",\"sub_chapters\":[...]}"},"event":{"id":"xxx","status":"done","name":"/toolcall/structured_outline"}}]}

data: {"role":"tool","status":"interrupt","content":[{"name":"/toolcall/interrupt","type":"json","text":{"data":"{\"interrupt_id\":\"83e03dfa-...\",\"interrupt_type\":\"deep_research_outliner\",\"wait_for\":[\"structured_outline\",\"query\"]}"},"event":{"id":"xxx","status":"interrupt","name":"/toolcall/interrupt"}}]}
```

### 报告生成阶段（文件输出）

```
data: {"role":"tool","status":"done","content":[{"name":"","type":"files","text":{"filename":"report_xxx.md","url":"https://...","download_url":"https://..."},"event":{"id":"xxx","status":"done","name":"","is_end":false,"is_stop":false}}]}

data: {"role":"tool","status":"done","content":[{"name":"","type":"files","text":{"filename":"report_xxx.html","url":"https://...","download_url":"https://..."},"event":{"id":"xxx","status":"done","name":"","is_end":true,"is_stop":true}}]}
```
