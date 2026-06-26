# 网易号 API

网易号是网易的内容创作平台。API 提供数据分析、分类管理、热门话题、活动列表等功能的访问。

## 发布参数

> `category` 和 `tags`（3-5个）均为必填，category 需通过辅助接口获取。

### 视频 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 视频标题（5-30字） |
| `desc` | string | 否 | - | 视频描述 |
| `videoPath` | string | **是** | - | 视频文件本地绝对路径 |
| `coverPath` | string | **是** | - | 封面路径 |
| `timing` | number | 否 | `0` | 定时时间戳，范围：5小时后~15天内 |
| `taskId` | string | **是** | - | 任务ID |
| `category` | object | **是** | - | 分类信息（**必填**），格式：`{ value: string, children: Array<{ value: string, children: string[] }> }`，通过 `wangyihao/getCategory` 获取 |
| `tags` | string[] | **是** | `[]` | 标签（**必填 3-5个**，每个≤12字） |
| `pubType` | number | 否 | `1` | 发布类型：1-立即发布，0-存草稿 |

**最小可用示例：**
```json
{ "title": "...(5-30字)", "desc": "", "videoPath": "...", "coverPath": "...", "timing": 0, "taskId": "...", "category": { "value": "...", "children": [] }, "tags": ["标签1", "标签2", "标签3"], "pubType": 1 }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/wangyihao/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

### 数据分析

#### getDataGraph

获取网易号数据图表。

```http
POST /galic/v1/platform/wangyihao/getDataGraph
```

**请求体:**
```json
{
  "accountArgs": {},
  "startDate": "2025-01-21",
  "endDate": "2025-01-21",
  "type": "video"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `startDate` (string) **必填** - 开始日期
- `endDate` (string) **必填** - 结束日期
- `type` (`video` \| `image`) - 内容类型：video | image，默认为 video

**响应:** 返回网易号账号在指定时间范围内的数据图表数据，包括阅读数、推荐数、评论数、分享数等指标的统计数据列表
---

#### getDataOverview

获取网易号数据概览。

```http
POST /galic/v1/platform/wangyihao/getDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "type": "video"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `type` (`video` \| `image`) - 内容类型：video | image，默认为 video

**响应:** 返回网易号账号的数据概览，包括总数量、昨日阅读数、推荐数等指标
---

#### getSingleDataOverview

获取网易号单个内容数据概览。

```http
POST /galic/v1/platform/wangyihao/getSingleDataOverview
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

**响应:** 返回网易号单个内容的详细数据概览，包括推荐数、阅读数、处理率、投票数、评论数、分享数等各项指标
---

#### getSingleDataGraph

获取网易号单个内容数据图表。

```http
POST /galic/v1/platform/wangyihao/getSingleDataGraph
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "contentType": 0,
  "startTime": "string",
  "endTime": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `contentType` (number) **必填** - 内容类型（必填，1-视频，2-图文等）
- `startTime` (string) **必填** - 开始时间（必填，格式：YYYY-MM-DD）
- `endTime` (string) **必填** - 结束时间（必填，格式：YYYY-MM-DD）

**响应:** 返回网易号单个内容在指定时间范围内的数据图表数据，包括播放数、展现量、评论数、分享数、点赞数等各项指标
---

### 发布辅助

#### getCategoryList

获取网易号分类列表。

```http
POST /galic/v1/platform/wangyihao/getCategoryList
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

**响应:** 返回网易号分类列表，含主分类与二级、三级分类
---

### 热门内容

#### getTopSubjects

获取网易号热门话题列表。

```http
POST /galic/v1/platform/wangyihao/getTopSubjects
```

**请求体:**
```json
{
  "accountArgs": {},
  "contentType": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `contentType` (number) - 内容类型：1-图文，2-视频

**响应:** 返回网易号热门话题列表，支持按内容类型筛选
---

#### getNoRepeatHotList

获取网易号不重复热门列表。

```http
POST /galic/v1/platform/wangyihao/getNoRepeatHotList
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

**响应:** 返回不重复热门内容列表，每条含类型（图文/视频）、标题、热度、来源、封面、摘要或视频信息等
---

### 活动任务

#### getActivityList

获取网易号活动列表。

```http
POST /galic/v1/platform/wangyihao/getActivityList
```

**请求体:**
```json
{
  "accountArgs": {},
  "state": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `state` (number) - 活动状态，默认 1

**响应:** 返回网易号活动列表，每条含标题、描述、时间范围、活动类型、领域、封面与链接等
---

### 其他

#### getHotDiscussionList

获取网易号易友热议列表。

```http
POST /galic/v1/platform/wangyihao/getHotDiscussionList
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

**响应:** 返回易友热议列表，data.cmtDocs 含文章标题、热评、热度值、回复数、来源等
---

