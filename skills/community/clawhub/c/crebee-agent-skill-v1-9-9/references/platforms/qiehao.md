# 企鹅号 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。`tasks[].taskId` 是批量发布的必填回调 ID；`params.taskId` 为兼容现有发布链路保留。可选字段无值时省略，不传 `null`。

### 视频 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | **是** | 视频标题，5-64 字 |
| `desc` | string | 否 | 视频描述，最多 200 字；平台发布页不展示该字段 |
| `videoPath` | string | **是** | 视频本地绝对路径 |
| `coverPath` | string | **是** | 封面路径 |
| `timing` | number | **是** | 秒级时间戳；`0` 立即发布 |
| `taskId` | string | 否 | 与 `tasks[].taskId` 保持一致 |
| `videoInfo` | object | 否 | `{ duration, width, height, size, thumbnail? }` |
| `category` | object | **是** | `{ value, children }`，`children` 为 string[]；通过 `qiehao/getCategoryList` 获取 |
| `topics` | string[] | **是** | 话题列表；真实表单要求至少 2 个 |
| `pubType` | number | 否 | `1` 立即发布，`0` 草稿 |

**最小参数校验示例：**

```json
{
  "title": "视频标题",
  "videoPath": "/tmp/video.mp4",
  "coverPath": "/tmp/cover.jpg",
  "timing": 0,
  "taskId": "task-1",
  "category": { "value": "娱乐", "children": ["影视"] },
  "topics": ["话题一", "话题二"]
}
```

## 接口调用

**端点前缀**: `/galic/v1/platform/qiehao/`

所有请求需要：

- `Authorization: Bearer <token>` 请求头
- `X-CreBee-Source: skill` 请求头（仅 Skill 直接调用）
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

### 发布辅助

#### getCategoryList

获取企鹅号分类列表。

```http
POST /galic/v1/platform/qiehao/getCategoryList
```

**请求体:**
```json
{
  "accountArgs": {}
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段

**响应:** 返回企鹅号分类列表，含主分类与子分类
---

### 数据分析

#### getDataOverviewGraph

获取企鹅号账号数据概览（趋势图）。

```http
POST /galic/v1/platform/qiehao/getDataOverviewGraph
```

**请求体:**
```json
{
  "accountArgs": {},
  "startDate": "2025-01-21",
  "endDate": "2025-01-21"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `startDate` (string) **必填** - 开始日期。传 Date 或 ISO 字符串，JSON 会转成字符串
- `endDate` (string) **必填** - 结束日期。传 Date 或 ISO 字符串，JSON 会转成字符串

**响应:** 返回企鹅号账号在指定日期范围内的视频数据概览，含播放量、点赞、评论、转发等趋势及表格统计
---

#### getSingleDataGraph

获取企鹅号单个内容数据概览统计。

```http
POST /galic/v1/platform/qiehao/getSingleDataGraph
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "startDate": "2025-01-21",
  "endDate": "2025-01-21"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `startDate` (string) - 开始日期。传 Date 或 ISO 字符串，JSON 会转成字符串
- `endDate` (string) - 结束日期。传 Date 或 ISO 字符串，JSON 会转成字符串

**响应:** 返回指定内容的数据统计图表，含播放量、点赞数、评论数、转发数等时间序列
---

#### getSingleDataOverview

获取企鹅号单个内容数据概览。

```http
POST /galic/v1/platform/qiehao/getSingleDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)

**响应:** 返回指定内容的数据概览，含播放量、互动数据、传播效果等
---

#### getSingleDataGraphLast24Hours

获取企鹅号单个内容最近24小时数据统计。

```http
POST /galic/v1/platform/qiehao/getSingleDataGraphLast24Hours
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)

**响应:** 返回指定内容最近24小时的实时数据统计
---

