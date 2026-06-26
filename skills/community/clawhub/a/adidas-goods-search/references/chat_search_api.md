# ChatSearch（对话搜索）接口整理

接口文档：<https://www.volcengine.com/docs/85296/1873492?lang=zh>

## Endpoint

- Method：POST
- Path：`/api/v1/application/{application_id}/chat_search`
- 华北：`https://aisearch.cn-beijing.volces.com`
- 柔佛：`https://aisearch.ap-southeast-1.volces.com`

## Auth

- Header：`Authorization: Bearer <API Key>`
- Header：`Content-Type: application/json`
- Header：`Accept: text/event-stream`

## 核心请求体

- `session_id`（必需）：会话唯一标识
- `input_message`（对话阶段必需）
  - `content[]`：元素列表
    - 文本：`{"type":"text","text":"..."}`
    - 图片：`{"type":"image_url","image_url":{"url":"data:<mime>;base64,<...>"}}`
- `user`（建议上传）：`{"_user_id":"...","nickname":"..."}`
- `enable_suggestions`（可选，默认 false）
- `search_param`（可选）：限制对话中触发搜索的数据集范围/过滤/返回字段
  - `page_size`：触发搜索时返回数量（默认 30）
  - `dataset_ids`：限定可搜索的数据集 ID 列表
  - `filters`：Map<dataset_id, filter object>，按数据集维度传过滤条件
  - `output_fields`：Map<data_source_id, fields[]>，控制返回字段（未指定则默认返回全部字段）
- `context`（可选）：地理位置等上下文
  - `location.longitude`：经度字符串，范围 [-180, 180]
  - `location.latitude`：纬度字符串，范围 [-90, 90]

## 流式返回要点

流式返回由多个 JSON chunk 组成，常见字段：

- 顶层：`request_id`
- `result.content`：增量文本
- `result.step_info`：过程步骤（analyze/tool call/get results/reply 等）
- `result.payload`：结构化内容（related_items、suggestions、search 等）
- `result.citation`：引用溯源（段落结束处可能出现）
- `result.stop_reason`：结束标记（如 "stop"）

## 注意事项

- 单次请求 HTTP Body 最大不超过 10MB
- 图片需使用 Data URI Scheme：`data:<MIME>;base64,<...>` 且 MIME 与真实格式一致
