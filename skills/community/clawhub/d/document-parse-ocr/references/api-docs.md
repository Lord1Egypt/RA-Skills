# Sugon-Scnet OCR 文档智能 API 文档摘要

## 概述
Scnet OCR 文档智能服务支持异步提交文档识别任务，适用于大批量文档处理。识别结果包含丰富的版面分析信息（文本、表格、图表、公式、页眉页脚、脚注、印章等）以及 Markdown 格式的全文。

## 接口地址
- **提交任务**: `POST https://api.scnet.cn/api/llm/v1/ocrdoc/submit`
- **查询结果**: `POST https://api.scnet.cn/api/llm/v1/ocrdoc/result`

## 请求头
- `Content-Type: application/json`
- `Authorization: Bearer <你的 API Key>`

## 任务提交接口

### 请求参数（Body JSON）

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| file_url | string | 是 | 公网可访问的文件下载地址 |
| ocr_type | string | 否 | 识别类别，目前仅支持 `DOC_PARSING` |

### 响应结构（成功）
```json
{
  "code": "200",
  "msg": "",
  "data": {
    "output": {
      "task_status": "pending",
      "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
  }
}
```
## 任务查询接口

### 请求参数（Body JSON）

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| task_ids | array | 是 | 任务 ID 列表，如 ["task_id_1", "task_id_2"] |


### 响应结构（任务成功）
```json
{
  "code": "0",
  "msg": "success",
  "data": [
    {
      "output": {
        "results": [
          "https://.../result.json?..."
        ],
        "task_id": "2056703208598626305",
        "task_status": "succeeded",
        "submit_time": "2026-05-19 19:47:11",
        "end_time": "2026-05-19 19:47:40"
      },
      "usage": {
        "image_count": 1
      },
      "request_id": "5e726f4f7d518259"
    }
  ]
}
```
### 任务进行中
```json
{
  "code": "200",
  "msg": "",
  "data": [
    {
      "request_id": "8ae698ba-df2d-966c-abcf-xxxxxx",
      "output": {
        "task_id": "e56d806f-76f9-4037-aefa-xxxxxx",
        "task_status": "running",
        "submit_time": "2026-04-20 19:33:50.425"
      }
    }
  ]
}
```
### 任务失败
```json
{
  "code": "200",
  "msg": "",
  "data": [
    {
      "request_id": "c61fe158-c0de-40f0-b4d9-964625119ba4",
      "output": {
        "task_id": "86ecf553-d340-4e21-xxxxxxxxx",
        "task_status": "failed",
        "submit_time": "2025-11-11 11:46:28.116",
        "end_time": "2025-11-11 11:46:28.255",
        "error_code": "limit_burst_rate",
        "error_message": "Burst rate limit exceeded for model xxx"
      }
    }
  ]
}
```
### 任务状态说明

| 状态 | 描述 |  |  |
|--------|------|------|----|
| pending | 任务已提交，等待处理 |  |  |
| running | 任务处理中 |  |  |
| succeeded | 任务处理成功 |  |  |
| failed | 任务处理失败 |  |  |
| unknown | 任务不存在或未知状态 |  |  |


### 错误码

| 错误码 | 描述 |  |  |
|--------|------|------|----|
| unknown_error | 未知错误 |  |  |
| modal_type_not_supported | 不支持的模态类型 |  |  |
| provider_not_supported | 不支持的提供商 |  |  |
| model_not_supported | 不支持的模型 |  |  |
| model_not_found | 模型不存在 |  |  |
| request_concurrency_conflict | 并发冲突，稍后重试 |  |  |
| provider_error | 提供商处理错误 |  |  |
| model_route_failed | 模型路由失败 |  |  |
| content_illegal | 内容违规 |  |  |
| limit_burst_rate | 突发速率限制超限 |  |  |
| task_not_found | 任务不存在 |  |  |
| InvalidParameter | 参数非法 |  |  |
| SystemError | 系统错误 |  |  |

## 识别结果文件结构
任务成功后会返回一个 JSON 格式的结果文件（下载地址由 results 数组提供）。该文件的详细字段说明请参阅 fields-summary.md。


## 注意事项
- `文件 URL 必须公网可访问，且服务端能直接下载`
- `结果文件下载地址有效期为 12 小时`
- `建议轮询间隔 ≥ 2 秒，避免过度请求`