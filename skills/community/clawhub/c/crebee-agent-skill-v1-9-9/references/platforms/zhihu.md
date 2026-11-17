# 知乎 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。`params.taskId` 虽是 Zod 可选字段，知乎运行时仍要求传入。

### 视频 params

| 字段 | 类型 | Zod 必填 | 说明 |
|------|------|----------|------|
| `title` | string | 是 | 5-50 个字符 |
| `desc` | string | 是 | 最多 300 个字符 |
| `videoPath` | string | 是 | 本地视频路径 |
| `coverPath` | string | 是 | 封面路径 |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布，定时发布需在半小时后 |
| `taskId` | string | 否 | 发布状态回调任务 ID；运行时必传 |
| `videoInfo` | `{ duration, width, height, size, thumbnail? }` | 否 | 视频校验信息 |
| `isOriginal` | number | 否 | 业务约定：`1` 原创、`0` 转载 |
| `topics` | `{ topic_id, topic_name, topic_avatar? }[]` | 否 | 最多 5 个话题，通过 `zhihu/getTopic` 获取 |
| `category` | `{ id: number, name: string, children: { id: number, name: string }[] }` | 否 | 分类信息，通过 `zhihu/getCategory` 获取 |

**最小参数校验示例：**
```json
{
  "title": "知乎视频示例",
  "desc": "示例描述",
  "videoPath": "/tmp/video.mp4",
  "coverPath": "/tmp/cover.jpg",
  "timing": 0,
  "taskId": "task-1"
}
```

### 图文 params

| 字段 | 类型 | Zod 必填 | 说明 |
|------|------|----------|------|
| `desc` | string | 否 | 描述 |
| `images` | string[] | 否 | 图片路径 |
| `taskId` | string | 否 | 发布状态回调任务 ID；运行时必传 |
| `title` | string | 否 | 标题 |
| `commentPermission` | `all` \| `follower_n_days` \| `followee` \| `censor` \| `nobody` | 否 | 评论权限 |

**最小参数校验示例：**
```json
{
  "images": ["/tmp/image.jpg"],
  "taskId": "task-1"
}
```

### 文章 params

| 字段 | 类型 | Zod 必填 | 说明 |
|------|------|----------|------|
| `title` | string | 否 | 标题 |
| `content` | string | 否 | HTML 正文；不支持 `<video>` |
| `covers` | string[] | 否 | 封面路径 |
| `taskId` | string | 否 | 发布状态回调任务 ID；运行时必传 |

**最小参数校验示例：**
```json
{
  "title": "知乎文章示例",
  "content": "<p>示例正文</p>",
  "taskId": "task-1"
}
```

## 接口调用

**端点前缀**: `/galic/v1/platform/zhihu/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
- `X-CreBee-Source: skill` 请求头（仅 Skill 直接调用）
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

### 数据分析

#### getDataOverview

获取知乎数据概览。

```http
POST /galic/v1/platform/zhihu/getDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "startDate": "2025-01-21",
  "endDate": "2025-01-21",
  "contentType": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `startDate` (string) - 开始日期，默认为当前时间前7天
- `endDate` (string) - 结束日期，默认为当前时间，不能大于当前时间
- `contentType` (string) - 内容类型，默认为"all"

**响应:** 返回知乎账号在指定时间范围内的数据概览，包括页面浏览量、播放量、展示量、赞同数、评论数、喜欢数、收藏数、分享数等各项指标的时间序列数据
---

#### getDataOverviewStatistic

获取知乎数据概览统计。

```http
POST /galic/v1/platform/zhihu/getDataOverviewStatistic
```

**请求体:**
```json
{
  "accountArgs": {},
  "contentType": "string",
  "startDate": "2025-01-21",
  "endDate": "2025-01-21"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `contentType` (string) - 内容类型，默认为"all"
- `startDate` (string) - 开始日期，默认为当前时间前7天
- `endDate` (string) **必填** - 结束日期，默认为当前时间，不能大于当前时间

**响应:** 返回知乎账号的数据概览统计数据，包括总体数据、昨日数据和今日数据的详细统计，以及各项指标的增量变化
---

#### getSingleDataOverview

获取知乎单个内容数据概览。

```http
POST /galic/v1/platform/zhihu/getSingleDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "publishType": "video",
  "startDate": "2025-01-21",
  "endDate": "2025-01-21"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `publishType` (`video` \| `image` \| `article`) - 发布类型，用于区分视频、文章、图片
- `startDate` (string) - 开始日期，默认为当前时间前7天
- `endDate` (string) - 结束日期，默认为当前时间，不能大于当前时间

**响应:** 返回知乎单个内容在指定时间范围内的数据概览，包括页面浏览量、播放量、展示量、赞同数、评论数、喜欢数、收藏数、分享数等各项指标的时间序列数据
---

#### getSingleDataOverviewStatistic

获取知乎单个内容数据概览统计。

```http
POST /galic/v1/platform/zhihu/getSingleDataOverviewStatistic
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "publishType": "video",
  "startDate": "2025-01-21",
  "endDate": "2025-01-21"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `publishType` (`video` \| `image` \| `article`) - 发布类型，用于区分视频、文章、图片
- `startDate` (string) - 开始日期，7天、14天、30天时使用，累计模式不传
- `endDate` (string) - 结束日期，默认为当前时间，不能大于当前时间

**响应:** 返回知乎单个内容的详细统计数据，包括总体数据、昨日数据和今日数据的详细统计，以及完读率、正面互动率、粉丝转化等高级指标
---

### 发布辅助

#### getTopic

获取知乎话题列表。

```http
POST /galic/v1/platform/zhihu/getTopic
```

**请求体:**
```json
{
  "accountArgs": {},
  "keyword": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `keyword` (string) **必填** - 搜索关键词

**响应:** 根据关键词搜索知乎话题列表
---

#### getCategory

获取知乎分类列表。

```http
POST /galic/v1/platform/zhihu/getCategory
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

**响应:** 返回知乎分类列表，含主分类与子分类
---

#### getRankDomainTagsThenMemberInfo

获取知乎博主排行榜。

```http
POST /galic/v1/platform/zhihu/getRankDomainTagsThenMemberInfo
```

**请求体:**
```json
{
  "accountArgs": {},
  "batchNumber": "string",
  "rankType": "string",
  "domainType": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `batchNumber` (string) **必填** - 批次号，由用户输入时间戳/批次，如 2026_02
- `rankType` (string) - 榜单类型，如「影响力榜」
- `domainType` (string) - 领域类型，如「科学工程」

**响应:** 先拉取博主排行榜标签（榜单类型与领域），再拉取该榜单下的博主排名列表
---

#### getBestAnswererHomeThenMemberInfo

获取知乎优秀答主排行榜。

```http
POST /galic/v1/platform/zhihu/getBestAnswererHomeThenMemberInfo
```

**请求体:**
```json
{
  "accountArgs": {},
  "domain": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `domain` (string) - 优秀答主领域，如「汽车」；不传则用 home 返回的首个领域

**响应:** 先获取优秀答主排行榜的领域和时间，再拉取该领域下的成员列表；domain 不传则用首个领域
---

#### getPinTopicRecommend

获取想法话题推荐。

```http
POST /galic/v1/platform/zhihu/getPinTopicRecommend
```

**请求体:**
```json
{
  "accountArgs": {},
  "offset": 0,
  "limit": 0,
  "scene": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `offset` (number) - 分页偏移，默认 0
- `limit` (number) - 每页条数，默认 12
- `scene` (string) - 场景，默认 mine_topic_card

**响应:** 发想法时的推荐话题列表，支持分页（offset、limit），默认 scene 为 mine_topic_card
---

#### getQuestionInvite

获取邀请回答问题时间线。

```http
POST /galic/v1/platform/zhihu/getQuestionInvite
```

**请求体:**
```json
{
  "accountArgs": {},
  "offset": 0,
  "limit": 0,
  "invite_with_time_slice": 0,
  "invite_domain_score_ab": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `offset` (number) - 分页偏移，默认 0
- `limit` (number) - 每页条数，默认 20
- `invite_with_time_slice` (number) - 默认 1
- `invite_domain_score_ab` (number) - 默认 1

**响应:** 创作者-精选问题-邀请回答页的时间线，支持分页（offset、limit）
---

#### getQuestionRecommend

获取推荐问题。

```http
POST /galic/v1/platform/zhihu/getQuestionRecommend
```

**请求体:**
```json
{
  "accountArgs": {},
  "offset": 0,
  "limit": 0,
  "page_source": "string",
  "recom_domain_score_ab": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `offset` (number) - 分页偏移，默认 0
- `limit` (number) - 每页条数，默认 20
- `page_source` (string) - 页面来源，默认 web_author_recommend
- `recom_domain_score_ab` (number) - 默认 1

**响应:** 创作者-精选问题-推荐页的推荐问题列表，支持分页（offset、limit）
---

#### getSearchEvent

获取问题搜索-全网热点榜单。

```http
POST /galic/v1/platform/zhihu/getSearchEvent
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

**响应:** 创作者-问题搜索页的全网热点榜单列表
---

#### getTopSearch

获取问题搜索-知乎热词。

```http
POST /galic/v1/platform/zhihu/getTopSearch
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

**响应:** 问题搜索-全网热点榜单中的热词/热搜列表（top_search.words）
---

#### getRankHot

获取问题搜索-知乎热题。

```http
POST /galic/v1/platform/zhihu/getRankHot
```

**请求体:**
```json
{
  "accountArgs": {},
  "domain": 0,
  "period": "string",
  "limit": 0,
  "offset": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `domain` (number) - 领域，0 表示全领域，默认 0
- `period` (string) - 周期，如 hour，默认 hour
- `limit` (number) - 每页条数，默认 20
- `offset` (number) - 分页偏移，默认 0

**响应:** 问题搜索-全网热点榜单中的热题榜单，支持 domain、period、limit、offset
---

#### getSearchQuery

问题搜索。

```http
POST /galic/v1/platform/zhihu/getSearchQuery
```

**请求体:**
```json
{
  "accountArgs": {},
  "query": "string",
  "sort_type": "string",
  "time_after": "string",
  "limit": 0,
  "offset": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `query` (string) **必填** - 搜索关键词，必填
- `sort_type` (string) - 排序：day 24 小时，total 累积热度；不传默认
- `time_after` (string) - 时间范围，如 quarter；不传默认
- `limit` (number) - 每页条数，默认 20
- `offset` (number) - 分页偏移，默认 0

**响应:** 问题搜索-全网热点榜单中按关键词搜索问题，支持 sort_type（day/total）、time_after、分页
---

