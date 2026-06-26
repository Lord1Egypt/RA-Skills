# 千帆对话 API 文档

## 接口地址

```
POST https://qianfan.baidubce.com/v2/app/conversation/runs
```

## 接口描述

对话接口，用于与千帆AI应用进行对话交互。支持流式和非流式响应，支持文件上传、工具调用等功能。

---

## 请求说明

### 请求结构

```http
POST /v2/app/conversation/runs HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json

{
    "app_id": "85036d8f-239c-469c-b342-b62ca9d696f6",
    "query": "根据文件中的数据，统计这几所学校小学生有多少",
    "stream": true,
    "conversation_id": "355a4f4e-a6d8-4dec-b840-7075030c6d22",
    "file_ids": [
        "cdd1e194-cfb7-4173-a154-795fae8535d9"
    ]
}
```

### Headers 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| Authorization | string | 是 | API Key，格式：`Bearer <API Key>` |
| Content-Type | string | 是 | 固定值：`application/json` |

---

## 请求参数

### Body 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| app_id | string | 是 | 应用ID |
| query | string | 是 | 用户提问内容 |
| stream | boolean | 是 | 是否流式返回 |
| conversation_id | string | 否 | 会话ID。首次对话可不传，后续对话需传入上次返回的conversation_id |
| file_ids | array[string] | 否 | 文件ID列表 |
| tools | array[object] | 否 | 工具定义列表，用于Function Call本地函数调用 |
| tool_choice | object | 否 | 强制执行的工具选择 |
| tool_outputs | array[object] | 否 | 上报工具调用结果 |
| action | object | 否 | 动作配置，用于回复"信息收集节点"的消息 |
| end_user_id | string | 否 | 终端用户ID |

### action 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| action_type | string | 是 | 动作类型，可选值：`resume` |
| parameters | object | 是 | 动作参数 |

### action.parameters 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| interrupt_event | object | 是 | 要回复的"信息收集节点"中断事件的信息 |

### action.parameters.interrupt_event 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| id | string | 是 | 中断事件ID，为上次对话返回的 interrupt_event_id |
| type | string | 是 | 中断事件类型，当前仅支持 `chat` |

### tool_choice 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| type | string | 是 | 类型，固定值：`function` |
| function | object | 是 | 函数配置 |

### tool_choice.function 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| name | string | 是 | 函数名称 |
| input | object | 是 | 函数输入参数 |

### tools 参数（Function Call本地函数）

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| type | string | 是 | 类型，固定值：`function` |
| function | object | 是 | 函数定义 |

### tools.function 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| name | string | 是 | 函数名称 |
| description | string | 是 | 函数描述 |
| parameters | object | 是 | 函数参数定义（JSON Schema格式） |

### tool_outputs 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| tool_call_id | string | 是 | 工具调用ID |
| output | string | 是 | 工具调用结果 |

### metadata_filter 参数

元数据过滤条件，仅对自主规划agent生效。

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| filters | array[object] | 是 | 过滤条件 |
| tag_filters | array[object] | 否 | 文档标签过滤条件 |
| condition | string | 是 | 文档组合条件，可选值：`and`、`or` |

### metadata_filter.filters 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| operator | string | 是 | 操作符，可选值：`==`、`in`、`not_in` |
| field | string | 是 | 字段名（目前仅支持doc_id） |
| value | string/array | 是 | 文档ID或标签值 |

### custom_metadata 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| override_role_instruction | string | 否 | 自定义角色指令，适用于自主规划Agent |

---

## 示例代码

### 基础请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/app/conversation/runs' \
--header 'Authorization: Bearer <API Key>' \
--header 'Content-Type: application/json' \
--data '{
    "app_id": "85036d8f-239c-469c-b342-b62ca9d696f6",
    "query": "根据文件中的数据，统计这几所学校小学生有多少",
    "stream": true,
    "conversation_id": "355a4f4e-a6d8-4dec-b840-7075030c6d22",
    "file_ids": [
        "cdd1e194-cfb7-4173-a154-795fae8535d9"
    ]
}'
```

### 强制执行组件

```bash
curl --location --request POST 'https://qianfan.baidubce.com/v2/app/conversation/runs' \
--header 'Authorization: Bearer <API Key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "app_id": "b412f6b3-d9e9-4617-8be5-94df02b06bdf",
    "query": "你好",
    "stream": true,
    "conversation_id": "377208a9-2ec2-4ed3-bc1f-120d20d0018c",
    "tool_choice": {
        "type": "function",
        "function": {
            "name": "QueryFlights",
            "input": {
                "flight_number":"CZ8889"
            }
        }
    }
}'
```

### Function Call 本地函数

```bash
curl --location --request POST 'https://qianfan.baidubce.com/v2/app/conversation/runs' \
--header 'Authorization: Bearer <API Key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "app_id": "4d4b1b27-d607-4d2a-9002-206134217a9f",
    "query": "今天北京的天气怎么样",
    "stream": true,
    "conversation_id": "8c5928f7-a9e7-4826-a027-3eb1f97f6eab",
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "仅支持中国城市的天气查询，参数location为中国城市名称，其他国家城市不支持天气查询",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. Beijing"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location", "unit"]
                }
            }
        }
    ]
}'
```

### 上报工具调用结果

```bash
curl --location --request POST 'https://qianfan.baidubce.com/v2/app/conversation/runs' \
--header 'Authorization: Bearer <API Key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "app_id": "4d4b1b27-d607-4d2a-9002-206134217a9f",
    "stream": false,
    "conversation_id": "8c5928f7-a9e7-4826-a027-3eb1f97f6eab",
    "tool_outputs": [
        {
            "tool_call_id": "ba853313-cbf0-4ecc-8ae7-92b33f00509d",
            "output": "北京今天天气晴朗，温度32度"
        }
    ]
}'
```

### 回复"信息收集节点"的消息

```bash
# 首次请求，获取 interrupt_event_id
curl --location --request POST 'https://qianfan.baidubce.com/v2/app/conversation/runs' \
--header 'Authorization: Bearer <API Key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "app_id": "7439c98a-a96c-468a-8a94-97a61b4476bf",
    "query": "你好",
    "stream": true,
    "conversation_id": "f1e88920-6075-42e2-b6ce-fff44f2c3159"
}'

# 获取到 interrupt_event_id 后，通过 action 回复
curl --location --request POST 'https://qianfan.baidubce.com/v2/app/conversation/runs' \
--header 'Authorization: Bearer <API Key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "app_id": "7439c98a-a96c-468a-8a94-97a61b4476bf",
    "query": "这是回复信息收集节点的消息",
    "stream": true,
    "conversation_id": "f1e88920-6075-42e2-b6ce-fff44f2c3159",
    "action": {
        "action_type": "resume",
        "parameters": {
            "interrupt_event": {
                "id": "af01f7ee-0ba2-4208-ac3c-09dee43c9ba0",
                "type": "chat"
            }
        }
    }
}'
```

---

## 返回响应

### Headers 参数

除公共头域外，无其它特殊头域。

### 返回参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| date | string | 是 | 消息返回时间的时间戳，UTC时间格式 |
| answer | string | 是 | 文字答案。流式场景下是增量数据 |
| content | array[object] | 是 | 节点输出信息相关内容 |

### content.items 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| usage | object | 是 | 模型用量，仅Chat Agent和Function Call和FollowUpQuery有 |
| outputs | object | 是 | 每个事件个性化输出内容的汇总字段 |

### content.items.usage 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| name | string | 是 | 消耗tokens的模型名称 |
| total_tokens | integer | 是 | 总token数 |
| prompt_tokens | integer | 是 | 输入token数 |
| completion_tokens | integer | 是 | 输出token数 |

### content.items.outputs 参数

每个事件个性化输出内容的汇总字段，根据事件的类型不同，outputs下内容不同。

**event_type 为 rag 时：**
- `text`: string - 普通文本
- `references`: list[object] - 包含reference对象的数组

**event_type 为 function_call 时：**
- `text`: function_call的描述json

**event_type 为 Workflow 时：**
- `text`: string - 普通文本
- `meta`: json - 自定义组件的描述信息

**event_type 为 DataSheetAgent 时：**
- `text`: string - 普通文本
- `code`: string - 普通文本
- `references`: list[object] - 包含reference对象的数组

**event_type 为 DatabaseAgent 时：**
- `code`: string - 普通文本
- `text`: string - 普通文本或json结构
- `references`: list[object] - 包含reference对象的数组

**event_type 为 MemoryTableAgent 时：**
- `text`: string - 普通文本
- `code`: string - 普通文本

**event_type 为 thought 时：**
- `text`: string - 思考模型思维链内容

**event_type 为 chatflow，content_type 是 publish_message 时：**
- `message`: 消息内容
- `message_id`: 消息id

**event_type 为 chatflow，content_type 是 chatflow_interrupt 时：**
- `interrupt_event_id`: string - 信息收集节点返回的中断事件id
- `interrupt_event_type`: string - 信息收集节点返回的中断事件type

**event_type 为 FollowUpQuery，content_type 是 json 时：**
- `json`: 返回的追问信息，格式是dict，key为follow_up_querys

**event_type 为 chat_reasoning 时：**
- `text`: string - 问答模型思维链内容

**其他组件可能出现的字段：**
- `urls`: array - 外部链接
- `files`: array - 工具生成的文件链接
- `image`: string - 工具生成的图片url
- `audio`: string - 工具生成的语音url
- `video`: string - 工具生成的视频url

### outputs.meta 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| desc | string | 是 | 组件描述 |
| workflow_id | string | 是 | 组件id |
| workflow_code | string | 是 | 组件编码 |
| workflow_name | string | 是 | 组件名称 |

### outputs.text 参数（event_type 为 function_call）

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| arguments | string | 是 | 参数 |
| component_code | string | 是 | 组件编码 |
| component_name | string | 是 | 组件名称 |

### outputs.references 参数（rag的reference参考信息）

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| id | string | 是 | content信息的id |
| url | string | 否 | BaiduSearch的专用字段 |
| from | string | 是 | 信息来源 |
| meta | object | 否 | 切片的元数据信息 |
| coord | string | 否 | 命中的文字在切片中的位置 |
| score | float | 是 | 切片匹配分 |
| content | string | 是 | 切片内容 |
| row_line | array | 是 | 命中的表格型知识数据中的某行数据 |
| segment_id | string | 否 | 切片id，知识问答专有字段 |
| dataset_id | string | 否 | 数据集id，知识问答专有字段 |
| document_id | string | 否 | 文档id，知识问答专有字段 |
| child_chunks | array | 否 | 子切片 |

### outputs.references.meta 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| chart_img | array | 否 | para_type值为chart时存在，展示图表链接 |
| para_type | string | 否 | 当前切片正文的类型：`table`、`chart`、`text`、`code` |
| para_format | string | 否 | 当前切片正文的展示格式：`html`、`markdown`、`json`、`txt` |

### outputs.references.row_line.items 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| key | string | 是 | 列名 |
| index | string | 是 | 列顺序 |
| value | string | 是 | 列值 |
| enable_indexing | boolean | 是 | 是否参与索引 |
| enable_response | boolean | 是 | 是否参与问答 |

### outputs.references.child_chunks.items 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| meta | object | 否 | 切片的元数据信息 |
| coord | string | 否 | 命中的文字在切片中的位置 |
| score | float | 否 | 切片匹配分 |
| content | string | 否 | 切片内容 |
| chunk_id | string | 否 | 子切片id |
| position | integer | 否 | 切片位置 |
| dataset_id | string | 否 | 数据集id |
| segment_id | string | 否 | 切片id |
| document_id | string | 否 | 文档id |

### child_chunks.items.meta 参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| box | array | 否 | 命中的内容在图片中的位置 |
| url | string | 否 | 切片对应的原文档中的页形成的图片的url，有效期24h |
| page_num | integer | 否 | 当前切片在原文档中的页数 |

---

## 响应示例

### 流式响应示例（stream: true）

```
data: {"date": "2024-01-15T10:30:00Z", "answer": "根据", "content": [...]}

data: {"date": "2024-01-15T10:30:00Z", "answer": "文件", "content": [...]}

data: {"date": "2024-01-15T10:30:00Z", "answer": "中的", "content": [...]}

data: [DONE]
```

### 非流式响应示例（stream: false）

```json
{
    "date": "2024-01-15T10:30:00Z",
    "answer": "根据文件中的数据，统计结果如下...",
    "content": [
        {
            "usage": {
                "name": "ERNIE-Bot-4",
                "total_tokens": 150,
                "prompt_tokens": 100,
                "completion_tokens": 50
            },
            "outputs": {
                "text": "根据文件中的数据，统计结果如下..."
            }
        }
    ]
}
```

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 认证失败，API Key无效 |
| 403 | 无权限访问该应用 |
| 404 | 应用不存在 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

---

## 注意事项

1. **会话管理**：首次对话时`conversation_id`可不传，后续对话需传入上次返回的`conversation_id`以保持对话上下文。
2. **流式响应**：流式模式下，响应以`data: `开头，以`data: [DONE]`结束。
3. **文件上传**：`file_ids`需要先通过文件上传接口获取。
4. **工具调用**：Function Call需要先定义工具，然后上报工具调用结果。
5. **信息收集节点**：当工作流中包含信息收集节点时，会返回`interrupt_event_id`，需要通过`action`参数回复。

---

## 相关链接

- [千帆AI应用开发者中心](https://cloud.baidu.com/product/wenxinworkshop)
- [API参考文档](https://cloud.baidu.com/doc/qianfan-api/s/7m7wqq361)
- [SDK下载](https://cloud.baidu.com/doc/Developer/index.html)
