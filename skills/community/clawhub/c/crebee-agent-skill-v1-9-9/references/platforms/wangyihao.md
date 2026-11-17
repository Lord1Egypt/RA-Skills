# 网易号 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。`tasks[].taskId` 是批量发布的必填回调 ID；`params.taskId` 为兼容现有发布链路保留。可选字段无值时省略，不传 `null`。

### 视频 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | **是** | 视频标题，5-30 字 |
| `desc` | string | 否 | 兼容字段；平台视频不使用该描述 |
| `videoPath` | string | **是** | 视频本地绝对路径 |
| `coverPath` | string | **是** | 封面路径 |
| `timing` | number | **是** | 秒级时间戳；`0` 立即发布，定时为 5 小时后至 15 天内 |
| `taskId` | string | 否 | 与 `tasks[].taskId` 保持一致 |
| `videoInfo` | object | 否 | `{ duration, width, height, size, thumbnail? }` |
| `pubType` | number | 否 | `1` 立即发布，`0` 草稿 |
| `category` | object | **是** | `{ value, children }`；`children` 为 `[{ value, children }]`，子级 `children` 为 string[]；通过 `wangyihao/getCategoryList` 获取，主分类必填，子分类可选 |
| `tags` | string[] | **是** | 标签列表；真实表单要求 3-5 个，每个最多 12 字 |

**最小参数校验示例：**

```json
{
  "title": "视频标题",
  "videoPath": "/tmp/video.mp4",
  "coverPath": "/tmp/cover.jpg",
  "timing": 0,
  "taskId": "task-1",
  "category": { "value": "娱乐", "children": [] },
  "tags": ["标签一", "标签二", "标签三"]
}
```

## 接口调用

**端点前缀**: `/galic/v1/platform/wangyihao/`

所有请求需要：

- `Authorization: Bearer <token>` 请求头
- `X-CreBee-Source: skill` 请求头（仅 Skill 直接调用）
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

