---
name: creator-collection
description: |
  批量达人数据采集与导出能力，支持 TikTok、YouTube、Instagram、Twitter 四平台。支持链接批量、用户名批量、关键词采集三种模式。异步任务机制，含提交、轮询、取数、导出完整生命周期。
  Use when: 批量采集, 数据导出, 离线采集, batch collection, data export, keyword collection
compatibility: Node.js 20.6+
metadata:
  layer: collection
  parent: creator-scraper-cv
---

## 概述

批量达人数据采集与导出能力。支持通过链接、用户名或关键词提交异步采集任务，自动轮询任务状态，完成后导出为 xlsx/csv/html 文件并提供下载链接。

支持平台：TikTok、YouTube、Instagram、Twitter。

> **Twitter 平台限制**：仅支持 `LINK_BATCH`（链接采集）和 `FILE_UPLOAD`（用户名采集），不支持视频采集（`CREATOR_VIDEO`、`POST_VIDEO`）。

## 脚本引用

| # | 脚本 | 路径 | 状态 |
|---|------|------|------|
| 1 | submit_collection_task.mjs | `../../scripts/submit_collection_task.mjs` | ✅ |
| 2 | submit_keyword_task.mjs | `../../scripts/submit_keyword_task.mjs` | ✅ |
| 3 | poll_task_status.mjs | `../../scripts/poll_task_status.mjs` | ✅ |
| 4 | get_task_status.mjs | `../../scripts/get_task_status.mjs` | ✅ |
| 5 | get_task_data.mjs | `../../scripts/get_task_data.mjs` | ✅ |
| 6 | export_task_data.mjs | `../../scripts/export_task_data.mjs` | ✅ |
| 7 | export_to_csv.mjs | `../../scripts/export_to_csv.mjs` | ✅ |
| 8 | get_download_url.mjs | `../../scripts/get_download_url.mjs` | ✅ |

## 异步任务生命周期

采集任务为异步操作（耗时 5~30 分钟），遵循四阶段流程：

```
提交(submit) → 轮询(poll) → 取数(get data) → 导出(export)
```

| 阶段 | 脚本 | 说明 |
|------|------|------|
| 1. 提交 | `submit_collection_task.mjs` / `submit_keyword_task.mjs` | 返回 task_id |
| 2. 轮询 | `poll_task_status.mjs` | 每 60s 自动轮询直到终态 |
| 3. 取数 | `get_task_data.mjs` | 分页获取原始 JSON 数据（仅在用户明确要求时使用） |
| 4. 导出 | `export_task_data.mjs` | 生成文件并返回下载链接 |

### 任务状态与终态判断

| 状态 | 含义 | 是否终态 |
|------|------|---------|
| `processing` | 处理中（爬取中或数据入库中） | ❌ 继续轮询 |
| `completed` | 已完成 | ✅ 可取数/导出 |
| `failed` | 失败 | ✅ 报告错误 |
| `timeout` | 超时 | ✅ 报告超时 |

> **[禁止] 在 `status: "processing"` 时提前报告结果。**
> 即使 `progress: 100%`，只要 `status` 仍为 `processing`，说明数据仍在入库处理中，**不能**判定为"0 条数据"或"无匹配结果"。
> 必须等到 `status` 变为 `completed` / `failed` / `timeout` 之一后，才能向用户报告最终结果。
>
> **典型场景**：`progress: 100%, completed: 0, status: processing` — 爬取已完成但数据尚未入库，继续轮询等待 `completed` 状态。

> **规则**：采集完成后（`status: completed`），**必须**先调用 `export_task_data.mjs` 生成可下载文件并展示链接给用户。不要直接调用 `get_task_data.mjs` 输出原始 JSON。

> **积分提醒规则**：仅当接口明确返回错误码 `40201` 时提示积分不足。`meta.quota_remaining` 是当天剩余 API 请求次数，不是积分余额；采集、轮询或导出成功后，禁止根据该字段生成“剩余积分不足”提醒。

辅助脚本：
- `get_task_status.mjs` — 单次查询任务状态（不轮询）
- `export_to_csv.mjs` — 管道式本地 CSV 导出（接收 stdin JSON）
- `get_download_url.mjs` — 获取已生成文件的下载链接

## 采集类型

| 类型 | task_type 值 | 触发场景 | 提交脚本 |
|------|-------------|----------|----------|
| 链接批量 | `LINK_BATCH` | 用户提供达人主页链接列表 | `submit_collection_task.mjs` |
| 用户名批量 | `FILE_UPLOAD` | 用户提供用户名列表 | `submit_collection_task.mjs` |
| 关键词采集 | — | 用户提供关键词，按关键词批量采集 | `submit_keyword_task.mjs` |

**使用示例**：

```bash
# 链接批量采集
node ../../scripts/submit_collection_task.mjs '{"task_type":"LINK_BATCH","platform":"tiktok","values":["https://www.tiktok.com/@creator1","https://www.tiktok.com/@creator2"],"task_name":"Q1 collection"}'

# 用户名批量采集
node ../../scripts/submit_collection_task.mjs '{"task_type":"FILE_UPLOAD","platform":"tiktok","values":["creator1","creator2"],"task_name":"username batch"}'

# 关键词采集
node ../../scripts/submit_keyword_task.mjs '{"platform":"tiktok","keywords":["beauty tips","skincare routine"]}'

# Twitter 链接批量采集
node ../../scripts/submit_collection_task.mjs '{"task_type":"LINK_BATCH","platform":"twitter","values":["https://x.com/creator1","https://x.com/creator2"],"task_name":"Twitter collection"}'
```

## 平台支持矩阵

| 平台 | `LINK_BATCH` | `FILE_UPLOAD` | `CREATOR_VIDEO` | `POST_VIDEO` | 关键词采集 |
|------|:---:|:---:|:---:|:---:|:---:|
| TikTok | ✅ | ✅ | ✅ | ✅ | ✅ |
| YouTube | ✅ | ✅ | ✅ | ✅ | ✅ |
| Instagram | ✅ | ✅ | ✅ | ✅ | ✅ |
| Twitter | ✅ | ✅ | ❌ | ❌ | ✅ |

> **Twitter 限制**：仅支持链接采集和用户名采集，不支持视频采集（`CREATOR_VIDEO`、`POST_VIDEO`）。

## 参数说明

### submit_collection_task.mjs

| 参数 | 类型 | 说明 |
|------|------|------|
| `task_type` | string | **必填**。`LINK_BATCH`（链接）/ `FILE_UPLOAD`（用户名） |
| `platform` | string | **必填**。`tiktok` / `youtube` / `instagram` / `twitter` |
| `values` | string[] | **必填**。链接或用户名数组，最多 200 条 |
| `task_name` | string | 任务名称 |
| `webhook_url` | string | 完成回调 URL（HTTPS） |

### submit_keyword_task.mjs

| 参数 | 类型 | 说明 |
|------|------|------|
| `platform` | string | **必填**。`tiktok` / `youtube` / `instagram` / `twitter` |
| `keywords` | string[] | **必填**。关键词列表，最多 10 个 |
| `task_name` | string | 任务名称 |
| `webhook_url` | string | 完成回调 URL（HTTPS） |

### poll_task_status.mjs

| 参数 | 类型 | 说明 |
|------|------|------|
| `task_id` | string | **必填**。任务 ID |
| `interval` | integer | 轮询间隔秒数，默认 60 |
| `max_attempts` | integer | 最大轮询次数，默认 45（约 45 分钟） |

### get_task_data.mjs

| 参数 | 类型 | 说明 |
|------|------|------|
| `task_id` | string | **必填**。任务 ID |
| `page` | integer | 页码，默认 1 |
| `size` | integer | 每页条数，默认 20，最大 100 |

### export_task_data.mjs

| 参数 | 类型 | 说明 |
|------|------|------|
| `task_id` | string | **必填**。任务 ID（必须已完成） |
| `format` | string | **必填**。`xlsx` / `csv` / `html` |

> 重复调用相同 task_id + format 会返回缓存文件，不会重复生成。

## 输出格式

### 导出格式

| 格式 | 说明 |
|------|------|
| `xlsx` | Excel 格式（默认推荐） |
| `csv` | CSV 格式 |
| `html` | HTML 表格格式 |

### 下载链接

`export_task_data.mjs` 返回 `file_url` 字段，为 OSS 签名下载链接。如需重新获取链接，使用 `get_download_url.mjs`：

```bash
node ../../scripts/get_download_url.mjs '{"file_id":"xxx"}'
# 或
node ../../scripts/get_download_url.mjs '{"file_name":"task_xxx.xlsx"}'
```

`export_to_csv.mjs` 为本地管道导出，通过 stdin 接收 JSON 数据：

```bash
node ../../scripts/get_task_data.mjs '{"task_id":"xxx","size":100}' | node ../../scripts/export_to_csv.mjs '{"output":"creators.csv"}'
```
