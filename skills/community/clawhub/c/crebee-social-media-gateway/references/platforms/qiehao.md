# 企鹅号 API

企鹅号是腾讯的内容创作平台。API 提供数据分析和分类管理功能的访问。

## 发布参数

> `category` 和 `topics`（至少2个）均为必填，需通过辅助接口获取。

### 视频 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 视频标题（5-64字） |
| `desc` | string | 否 | - | 视频描述（≤200字） |
| `videoPath` | string | **是** | - | 视频文件本地绝对路径 |
| `coverPath` | string | **是** | - | 封面路径 |
| `timing` | number | 否 | `0` | 定时时间戳 |
| `taskId` | string | **是** | - | 任务ID |
| `category` | object | **是** | - | 分类信息（**必填**），格式：`{ value: string, children: string[] }`，通过 `qiehao/getCategory` 获取 |
| `topics` | string[] | **是** | `[]` | 话题列表（**至少2个**，字符串数组） |
| `pubType` | number | 否 | `1` | 发布类型：1-立即发布，0-存草稿 |

**最小可用示例：**
```json
{ "title": "...(5-64字)", "desc": "", "videoPath": "...", "coverPath": "...", "timing": 0, "taskId": "...", "category": { "value": "...", "children": ["子分类"] }, "topics": ["话题1", "话题2"], "pubType": 1 }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/qiehao/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
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

