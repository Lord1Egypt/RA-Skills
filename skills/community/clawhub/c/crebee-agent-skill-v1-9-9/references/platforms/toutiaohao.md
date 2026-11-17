# 头条号 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。`tasks[].taskId` 是批量发布的必填回调 ID；`params.taskId` 为兼容现有发布链路保留。可选字段无值时省略，不传 `null`。

### 视频 params

> 竖版视频不支持定时、描述和话题；`visibilityType` 仅横版生效。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | **是** | 视频标题 |
| `desc` | string | 否 | 视频描述；竖版无效 |
| `videoPath` | string | **是** | 视频本地绝对路径 |
| `coverPath` | string | **是** | 封面路径 |
| `timing` | number | **是** | 秒级时间戳；`0` 立即发布；横版定时为 2 小时后至 7 天内 |
| `taskId` | string | 否 | 与 `tasks[].taskId` 保持一致 |
| `videoInfo` | object | 否 | `{ duration, width, height, size, thumbnail? }` |
| `videoType` | `"horizontal" \| "vertical"` | **是** | 视频方向 |
| `visibilityType` | `0 \| 1 \| 2` | 否 | 公开、仅自己、互相关注可见 |
| `pubType` | number | 否 | `1` 立即发布，`0` 草稿 |
| `externalLink` | string | 否 | 外部链接 |
| `generateImage` | object | 否 | `{ enable, publishType? }`；启用时真实表单要求 `publishType` 为 `1` 或 `2` |
| `workStatement` | `"from_external" \| "from_internal" \| "self_shot" \| "ai_generated" \| "fictional" \| "investment_advice" \| "health_medical"` | 否 | 作品声明 |
| `internalSourceAccount` | object | 否 | 站内引用账号，通过 `toutiaohao/getUserList` 获取：`{ user_id, user_name, user_avatar_url, user_followers_count }`；`workStatement` 为 `from_internal` 时真实表单必填 |
| `internalSourceTime` | string | 否 | 站内引用时间；JSON 使用可解析的日期时间字符串 |
| `internalSourceLocation` | object | 否 | `{ position_id, position_name, position_address, position_city, position_province, position_district?, position_latitude?, position_longitude?, position_type_code? }`，通过 `toutiaohao/getPositionsList` 获取 |
| `topics` | object[] | 否 | `[{ topic_name }]`，通过 `toutiaohao/getTopicList` 获取；仅横版有效 |
| `collection` | object | 否 | `{ collection_id, collection_title, collection_count, collection_cover_url }`，通过 `toutiaohao/getCollectionList` 获取；仅横版有效 |

**最小参数校验示例：**

```json
{
  "title": "视频标题",
  "videoPath": "/tmp/video.mp4",
  "coverPath": "/tmp/cover.jpg",
  "timing": 0,
  "taskId": "task-1",
  "videoType": "horizontal"
}
```

### 图文 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `desc` | string | 否 | 图文描述 |
| `images` | string[] | 否 | 图片本地路径列表 |
| `taskId` | string | 否 | 与 `tasks[].taskId` 保持一致 |

**最小参数校验示例：**

```json
{
  "desc": "图文描述",
  "images": ["/tmp/image.jpg"],
  "taskId": "task-1"
}
```

### 文章 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | 否 | 文章标题 |
| `content` | string | 否 | HTML 正文 |
| `covers` | string[] | 否 | 封面本地路径列表 |
| `taskId` | string | 否 | 与 `tasks[].taskId` 保持一致 |
| `timing` | number | 否 | 秒级时间戳；`0` 或省略立即发布 |
| `articleAdType` | `2 \| 3` | 否 | 广告投放类型 |
| `collection` | object | 否 | `{ collection_id, collection_title, collection_count, collection_cover_url }`，通过 `toutiaohao/getCollectionList` 获取；定时发布时运行时不会传给平台 |
| `city` | object | 否 | `{ city, city_code }`，通过 `toutiaohao/getArticleCityList` 获取 |
| `infoSourceType` | `-1 \| 1 \| 3 \| 4 \| 5 \| 6 \| 7 \| 8` | 否 | 作品声明类型 |

**最小参数校验示例：**

```json
{
  "taskId": "task-1"
}
```

## 接口调用

**端点前缀**: `/galic/v1/platform/toutiaohao/`

所有请求需要：

- `Authorization: Bearer <token>` 请求头
- `X-CreBee-Source: skill` 请求头（仅 Skill 直接调用）
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

### 数据分析

#### getDataOverview

获取头条号数据概览。

```http
POST /galic/v1/platform/toutiaohao/getDataOverview
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
- `startDate` (string) - 开始日期
- `endDate` (string) - 结束日期

**响应:** 返回头条号账号在指定时间范围内的数据概览，包括播放数、曝光数、互动数据等指标及其每日统计数据
---

#### getSingleDataOverview

获取头条号单个内容数据概览。

```http
POST /galic/v1/platform/toutiaohao/getSingleDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "startDate": "2025-01-21",
  "endDate": "2025-01-21",
  "dataType": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `startDate` (string) - 开始日期
- `endDate` (string) - 结束日期
- `dataType` (number) - 数据类型，默认为2

**响应:** 返回头条号单个内容的详细数据概览，包括播放数、曝光数、互动数据、消费详情等各项指标及其每日统计数据
---

#### getSingleDataOverviewStatistic

获取头条号单个内容数据概览统计。

```http
POST /galic/v1/platform/toutiaohao/getSingleDataOverviewStatistic
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "dataType": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `dataType` (number) - 数据类型，默认为2

**响应:** 返回头条号单个内容的详细统计数据，包括消费数据、粉丝数据、收入数据、互动数据、排名数据等
---

#### getFansPortrait

获取头条号用户画像数据。

```http
POST /galic/v1/platform/toutiaohao/getFansPortrait
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

**响应:** 返回头条号账号的用户画像数据，包括年龄分布、设备分布（价格区间）、性别分布、省份分布等
---

#### getActivityCategoryList

获取头条号活动任务分类列表。

```http
POST /galic/v1/platform/toutiaohao/getActivityCategoryList
```

**请求体:**
```json
{
  "accountArgs": {},
  "biz_id": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `biz_id` (number) - 体裁类型：1 文章类，2 视频类

**响应:** 返回活动任务页可用的分类名称列表（如全部、国际、军事、旅游等）
---

#### getActivityList

获取头条号活动任务列表。

```http
POST /galic/v1/platform/toutiaohao/getActivityList
```

**请求体:**
```json
{
  "accountArgs": {},
  "biz_id": 0,
  "limit": 0,
  "part_status": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `biz_id` (number) - 体裁类型：1 文章类，2 视频类
- `limit` (number) - 每页条数
- `part_status` (number) - 参加状态：0 全部 1 已参加 2 未参加

**响应:** 返回活动任务分页列表，含总数与活动明细（标题、时间、参与人数、奖励等）
---

#### getSuggestForum

获取头条号推荐话题/热点。

```http
POST /galic/v1/platform/toutiaohao/getSuggestForum
```

**请求体:**
```json
{
  "accountArgs": {},
  "offset": 0,
  "count": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `offset` (number) - 分页偏移
- `count` (number) - 每页条数（实际 hot 条数可能为 count-2）

**响应:** 返回推荐话题分页数据：最近使用列表、热门话题列表（含话题名、讨论数、阅读数等）、suggest_tips等
---

### 发布辅助

#### getTopicList

获取头条号话题列表。

```http
POST /galic/v1/platform/toutiaohao/getTopicList
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
- `keyword` (string) - 搜索关键词

**响应:** 根据关键词搜索头条号话题列表
---

#### getCollectionList

获取头条号视频合集列表。

```http
POST /galic/v1/platform/toutiaohao/getCollectionList
```

**请求体:**
```json
{
  "accountArgs": {},
  "offset": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `offset` (number) - 偏移量

**响应:** 返回头条号视频合集列表，支持偏移量分页
---

#### getArticleCityList

获取头条号文章城市列表。

```http
POST /galic/v1/platform/toutiaohao/getArticleCityList
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
- `keyword` (string) - 城市关键词

**响应:** 返回头条号文章发布可选城市，支持按城市名或行政区划编码过滤
---

#### getPositionsList

获取头条号位置列表。

```http
POST /galic/v1/platform/toutiaohao/getPositionsList
```

**请求体:**
```json
{
  "accountArgs": {},
  "keywords": "string",
  "offset": 0,
  "page": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `keywords` (string) - 搜索关键词
- `offset` (number) - 偏移量，默认0
- `page` (number) - 页码，默认1

**响应:** 根据关键词搜索头条号位置列表，支持分页
---

#### getUserList

获取头条号用户列表。

```http
POST /galic/v1/platform/toutiaohao/getUserList
```

**请求体:**
```json
{
  "accountArgs": {},
  "words": "string",
  "language": "string",
  "app_name": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `words` (string) - 搜索关键词
- `language` (string) - 语言，默认zh
- `app_name` (string) - 应用名称，默认toutiao_mp

**响应:** 根据关键词搜索头条号用户列表
---

