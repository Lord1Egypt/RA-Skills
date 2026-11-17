# 抖音 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。可选字段无值时省略，不能传 `null`；示例保留实际发布需要的 `taskId`。

### 视频 params

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `title` | string | 是 | 视频标题 |
| `desc` | string | 是 | 视频描述 |
| `videoPath` | string | 是 | 本地视频路径 |
| `coverPath` | string | 是 | 本地封面路径 |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布，定时为 2 小时后至 14 天内 |
| `taskId` | string | 否（运行时必传） | 任务 ID |
| `videoInfo` | `{ duration: number; width: number; height: number; size: number; thumbnail?: string }` | 否 | 视频信息 |
| `horizontalCover` / `verticalCover` | string | 否 | 横版 / 竖版本地封面路径 |
| `allowDownload` | number | 否 | 是否允许下载 |
| `visibilityType` | `0 \| 1 \| 2` | 否 | 公开 / 私密 / 互相关注可见 |
| `music` | `{ music_cover: string; music_name: string; music_author: string; music_duration: number; user_count: number; play_url: string; music_id: string }` | 否 | 背景音乐；分类通过 `douyin/getMusicCategoryList` 获取，再调用 `douyin/getMusicListByCategory`，关键词搜索用 `douyin/getMusicListByKey` |
| `topics` | `{ topic_name: string; topic_id: string; topic_view_count: number }[]` | 否 | 话题，通过 `douyin/getTopics` 获取 |
| `activities` | `{ activity_name: string; activity_topics: string[]; activity_topic_ids: number[]; activity_hot_score: number; activity_start_time: string; activity_end_time: string; activity_cover_image: string }[]` | 否 | 活动，通过 `douyin/getActivityListInfo` 获取 |
| `mentions` | `{ friend_avatar: string; friend_follower_count: number; friend_uid: string; friend_name: string }[]` | 否 | 提及用户，通过 `douyin/getFriend` 获取 |
| `collection` | `{ collection_name: string; collection_id: string; collection_work_count: number; collection_cover_url: string }` | 否 | 合集，通过 `douyin/getCollection` 获取 |
| `position` | `{ position_id: string; position_name: string; position_address: string }` | 否 | 位置，通过 `douyin/getLocation` 获取 |
| `hotEvents` | `{ word: string; word_cover: string; hot_value: number }` | 否 | 热点事件，通过 `douyin/getHotEvents` 获取 |
| `declare` | `{ text: string; choose_value: string; source?: string }` | 否 | 自主声明 |

**最小参数校验示例：**

```json
{ "title": "示例视频", "desc": "", "videoPath": "/tmp/video.mp4", "coverPath": "/tmp/cover.jpg", "timing": 0, "taskId": "task-1" }
```

### 图文 params

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `desc` | string | 否 | 描述 |
| `images` | string[] | 否 | 本地图片路径 |
| `taskId` | string | 否（运行时必传） | 任务 ID |
| `title` / `cover` | string | 否 | 标题 / 本地封面路径 |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布 |
| `allowDownload` | number | 否 | 是否允许下载 |
| `visibilityType` | `0 \| 1 \| 2` | 否 | 公开 / 私密 / 互相关注可见 |
| `topics` / `mentions` / `activities` | 与视频同名字段类型相同 | 否 | 分别通过 `douyin/getTopics`、`douyin/getFriend`、`douyin/getActivityListInfo` 获取 |
| `collection` / `music` / `position` | 与视频同名字段类型相同 | 否 | 分别通过 `douyin/getCollection`、抖音音乐列表接口、`douyin/getLocation` 获取 |
| `hotEvent` | `{ word: string; word_cover: string; hot_value: number }` | 否 | 热点事件，通过 `douyin/getHotEvents` 获取；字段为单数 |
| `declare` | `{ text: string; choose_value: string; source?: string }` | 否 | 自主声明 |

**最小参数校验示例：**

```json
{ "desc": "示例图文", "images": ["/tmp/image.jpg"], "timing": 0, "taskId": "task-1" }
```

### 文章 params

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `title` / `content` | string | 否 | 标题 / 正文 |
| `covers` | string[] | 否 | 封面路径 |
| `taskId` | string | 否（运行时必传） | 任务 ID |
| `description` / `backgroundExtracted` | string | 否 | 摘要 / 正文背景色 |
| `headPoster` | `{ path: string; name: string; videoInfo?: unknown }` | 否 | 头图 |
| `topics` / `music` | 与视频同名字段类型相同 | 否 | 话题通过 `douyin/getTopics` 获取；音乐通过音乐列表接口获取 |
| `visibilityType` | `0 \| 1 \| 2` | 否 | 公开 / 私密 / 互相关注可见 |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布 |

**最小参数校验示例：**

```json
{ "title": "示例文章", "content": "<p>正文</p>", "timing": 0, "taskId": "task-1" }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/douyin/`

### 数据分析

#### getDataOverview

获取抖音帐号数据概览。

```http
POST /galic/v1/platform/douyin/getDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "recent_days": null
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `recent_days` (any) **必填** - 最近1，7，30天

**响应:** 返回抖音账号在指定时间范围内的数据概览，包括播放量、点赞数、评论数、分享数等指标及其趋势数据
---

#### getSingleDataOverview

获取抖音单个发布记录数据概览。

```http
POST /galic/v1/platform/douyin/getSingleDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "publishType": "video"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `publishType` (`video` \| `image` \| `article`) - 发布类型，默认为 video

**响应:** 返回抖音单个视频的详细数据概览，包括播放量、点赞量、评论量、分享量、完播率等各项指标
---

#### getSingleDataGraph

获取抖音单个发布记录数据图表。

```http
POST /galic/v1/platform/douyin/getSingleDataGraph
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "trendType": null,
  "timeUnit": null,
  "metrics": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `trendType` (any) **必填** - 趋势类型 2 累计 1 新增
- `timeUnit` (any) **必填** - 时间单位 2 每小时 1 每天
- `metrics` (string) **必填** - 指标

**响应:** 返回抖音单个视频的数据图表数据，用于绘制趋势图，支持累计和新增两种趋势类型，支持按小时或按天统计
---

#### getFansSummary

获取抖音粉丝画像数据。

```http
POST /galic/v1/platform/douyin/getFansSummary
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

**响应:** 调用帐号需具备查看粉丝画像权限，如果有权限则返回抖音账号的粉丝画像数据，包括粉丝分布、活跃度、年龄、性别、城市、设备品牌、兴趣分布等详细信息
---

#### getHotTopic

获取抖音相关热门话题榜单原始数据。

```http
POST /galic/v1/platform/douyin/getHotTopic
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

**响应:** 调用抖音创作者平台 hot_topic 接口，返回与创作内容相关的热门话题排行榜数据（平台维度，不局限于本账号），包括标题、热度分数、播放量、点赞量、评论量等原始指标
---

#### getCreativeInsightTags

获取抖音创意洞察标签原始数据。

```http
POST /galic/v1/platform/douyin/getCreativeInsightTags
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

**响应:** 调用抖音创作者平台 material/center/config 接口，返回创意洞察榜单可用的标签配置（包括城市、热点玩法、热词、内容垂类等）
---

#### getHotVideo

获取抖音相关热门视频榜单原始数据。

```http
POST /galic/v1/platform/douyin/getHotVideo
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

**响应:** 调用抖音创作者平台 hot_video 接口，返回与创作内容相关的热门视频排行榜数据（平台维度，不局限于本账号），包括标题、作者、热度分数、播放量、点赞量、分享量、评论量等原始指标
---

#### getCurrentHotTopic

获取抖音实时/飙升热点排行榜。

```http
POST /galic/v1/platform/douyin/getCurrentHotTopic
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

**响应:** 调用 get_current_hot_topic 接口，返回解密后的 data：current（实时热点）、rocketing（飙升热点）列表
---

#### getBrandHotVideosList

获取抖音指数-热门视频列表。

```http
POST /galic/v1/platform/douyin/getBrandHotVideosList
```

**请求体:**
```json
{
  "accountArgs": {},
  "tag_id": "string",
  "period": "string",
  "end_date": "string",
  "rank_type": "string",
  "category": "string",
  "sort_by": "string",
  "page_req": {},
  "week": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `tag_id` (string) **必填** - 标签/分类 ID，见 DOUYIN_BRAND_HOT_VIDEOS_TAG_LIST 映射（如 601-剧情）
- `period` (string) **必填** - 周期：1-日榜，7-周榜
- `end_date` (string) - 结束日期，如 20260225；不传时自动取 time_scope.latest_day（日榜）
- `rank_type` (string) - 排行类型，如 index
- `category` (string) - 分类，与 tag_id 同取 DOUYIN_BRAND_HOT_VIDEOS_TAG_LIST 的 tagId，不传时默认用 tag_id
- `sort_by` (string) - 排序字段，如 index
- `page_req` (object) **必填** - 分页
  - `current_page` (number) **必填** - 当前页
  - `page_size` (string) **必填** - 每页条数，如 50
- `week` (string) - 周榜（period=7）时传；不传时自动取 time_scope.end_week

**响应:** 先请求时间范围接口再请求热门视频列表。body 传 accountArgs、tag_id、period、page_req 等，end_date、week 可不传。period：1=日榜（接口返回的最新日），3=近三日（以最新日往前推），7=周榜（接口返回的最新周）。返回列表及可选 time_scope。
---

#### getCreativeInsightBillboard

获取抖音创意洞察内容榜单原始数据。

```http
POST /galic/v1/platform/douyin/getCreativeInsightBillboard
```

**请求体:**
```json
{
  "accountArgs": {},
  "billboard_type": 0,
  "billboard_tag": "string",
  "order_key": "string",
  "time_filter": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `billboard_type` (number) **必填** - 榜单类型：1热门视频 2创作热点 3热门话题 4热门道具 5热门音乐
- `billboard_tag` (string) - 创意洞察的标签
- `order_key` (string) - 排序字段
- `time_filter` (string) - 时间过滤参数

**响应:** 调用抖音创作者平台 material/center/billboard 接口，按类型、标签、排序和时间过滤返回创意洞察内容榜单（热门视频 / 创作热点 / 热门话题 / 热门道具 / 热门音乐），返回包括作者、播放量、点赞量、分享量、热度分数等原始指标
---

#### getItemSummary

获取抖音表现优异作品列表摘要。

```http
POST /galic/v1/platform/douyin/getItemSummary
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

**响应:** 调用抖音数据中心作品分析接口，返回投稿作品中表现优异作品的汇总信息，对应 item_summary 接口
---

#### getCreatorActivityList

获取抖音创作者活动列表原始数据。

```http
POST /galic/v1/platform/douyin/getCreatorActivityList
```

**请求体:**
```json
{
  "accountArgs": {},
  "start_time": "string",
  "end_time": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `start_time` (string) **必填** - 开始时间，通常为时间戳字符串
- `end_time` (string) **必填** - 结束时间，通常为时间戳字符串

**响应:** 调用抖音创作者平台 activity/pc/list 接口，按开始时间和结束时间返回创作者活动列表（原始数据，不做类型转换）
---

#### getCreatorActivityDetail

获取抖音创作者活动详情原始数据。

```http
POST /galic/v1/platform/douyin/getCreatorActivityDetail
```

**请求体:**
```json
{
  "accountArgs": {},
  "is_pc": true,
  "activity_id": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `is_pc` (boolean) **必填** - 是否为 PC 端请求，接口示例固定为 true
- `activity_id` (string) **必填** - 活动 ID

**响应:** 调用抖音创作者平台 activity/detail 接口，基于活动 ID 和 is_pc=true 返回单个创作者活动的详情数据（原始数据，不做类型转换）
---

#### creatorAttentionKeyword

关联视频搜索-搜索关联词。

```http
POST /galic/v1/platform/douyin/creatorAttentionKeyword
```

**请求体:**
```json
{}
```

**响应:** body.action：addKeyword / deleteKeyword / getKeywordList / getKeywordItemSearch。返回统一含 keyword_list 与 item_info_list（及 cursor、has_more）。必传 accountArgs。
---

#### getContentCreativeTopicWithValidDate

获取抖音创意洞察-热门话题列表。

```http
POST /galic/v1/platform/douyin/getContentCreativeTopicWithValidDate
```

**请求体:**
```json
{
  "accountArgs": {},
  "tag_id": "string",
  "period": "string",
  "end_date": "string",
  "rank_type": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `tag_id` (string) **必填** - 标签/分类 ID，如 601
- `period` (string) **必填** - 周期：1-日，7-周等
- `end_date` (string) - 结束日期，不传时可由 get_content_valid_date 的 day/week 填充
- `rank_type` (string) - 排行类型，如 index

**响应:** 先请求时间范围接口再请求热门话题列表。body 传 accountArgs、tag_id、period，end_date 可不传。period：1=日榜（接口返回的最新日），3=近三日（以最新日往前推），7=周榜（接口返回的最新周）。返回 topic_list 等
---

#### getContentCreativeKeywordsWithValidDate

获取抖音创意洞察-热门关键词列表。

```http
POST /galic/v1/platform/douyin/getContentCreativeKeywordsWithValidDate
```

**请求体:**
```json
{
  "accountArgs": {},
  "tag_id": "string",
  "period": "string",
  "end_date": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `tag_id` (string) **必填** - 标签/分类 ID，如 601
- `period` (string) **必填** - 周期：1-日，3-近三日，7-周
- `end_date` (string) - 结束日期，不传时由时间范围接口按 period 自动填充

**响应:** 先请求时间范围接口再请求热门关键词列表（时间范围与热门话题共用）。body 传 accountArgs、tag_id、period，end_date 可不传。period：1=日榜，3=近三日，7=周榜。返回 data.keyword_list（keyword、cnt、is_hot、index、search_index）
---

#### getContentPublishTrendWithValidDate

获取抖音创意洞察-内容生产分析（统一入口）。

```http
POST /galic/v1/platform/douyin/getContentPublishTrendWithValidDate
```

**请求体:**
```json
{
  "accountArgs": {},
  "tag_id": "string",
  "start_date": "string",
  "end_date": "string",
  "week": "string",
  "month": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `tag_id` (string) **必填** - 标签/分类 ID，如 601
- `start_date` (string) - 开始日期（趋势-按日），如 20260225；与 end_date 一起或不传时由时间范围接口取 latestDay
- `end_date` (string) - 结束日期（趋势-按日），如 20260226
- `week` (string) - 周标识（视频时长占比-按周），如 20260226 表示该周；与 month 二选一
- `month` (string) - 月份（内容生产者-按月），如 202602；与 week 二选一

**响应:** 根据传入时间类型自动路由：仅传 start_date/end_date（或其一）→ 按该日期推导周、月，同时返回 trend（按日）+ duration（按周）+ portrait（按月）；传 week → 仅视频时长占比（按周）；传 month → 仅内容生产者画像（按月）。body 必传 accountArgs、tag_id。日期超出有效范围时自动回退为最新。
---

#### getContentConsumeAnalysisWithValidDate

获取抖音创意洞察-内容消费分析（统一入口）。

```http
POST /galic/v1/platform/douyin/getContentConsumeAnalysisWithValidDate
```

**请求体:**
```json
{
  "accountArgs": {},
  "tag_id": "string",
  "start_date": "string",
  "end_date": "string",
  "week": "string",
  "month": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `tag_id` (string) **必填** - 标签/分类 ID，如 601
- `start_date` (string) - 开始日期（趋势-按日），如 20260225；与 end_date 一起或不传时由时间范围接口取 latestDay
- `end_date` (string) - 结束日期（趋势-按日），如 20260226
- `week` (string) - 周标识（视频时长占比-按周），如 20260226 表示该周；与 month 二选一
- `month` (string) - 月份（内容生产者-按月），如 202602；与 week 二选一

**响应:** 与内容生产分析结构一致。传 month → 仅内容消费者画像（按月）；传 week → 仅视频占比分布（按周）；仅传 start_date/end_date（或其一）→ 按该日期推导周、月，返回 supply_demand（内容供需）+ interaction（内容互动）+ duration（视频占比）+ portrait（消费者画像）；都不传则返回 supply_demand + interaction（latestDay）。时间范围与 get_content_valid_date 一致。
---

### 发布辅助

#### getTopics

获取抖音话题列表。

```http
POST /galic/v1/platform/douyin/getTopics
```

**请求体:**
```json
{
  "accountArgs": {},
  "searchKey": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `searchKey` (string) - 搜索关键词

**响应:** 根据关键词搜索抖音话题建议列表
---

#### getFriend

获取抖音好友/用户列表。

```http
POST /galic/v1/platform/douyin/getFriend
```

**请求体:**
```json
{
  "accountArgs": {},
  "searchKey": "string",
  "cursor": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `searchKey` (string) - 搜索关键词
- `cursor` (number) - 页码游标

**响应:** 获取抖音好友或用户列表，支持关键词搜索与游标分页
---

#### getActivityListInfo

获取抖音活动列表。

```http
POST /galic/v1/platform/douyin/getActivityListInfo
```

**请求体:**
```json
{
  "accountArgs": {},
  "queryTag": 0,
  "page": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `queryTag` (number) - 查询标签
- `page` (number) - 页码

**响应:** 获取抖音活动列表，支持查询标签与分页
---

#### getHotEvents

获取抖音热点事件列表。

```http
POST /galic/v1/platform/douyin/getHotEvents
```

**请求体:**
```json
{
  "accountArgs": {},
  "searchKey": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `searchKey` (string) - 搜索关键词

**响应:** 根据关键词搜索抖音热点事件列表
---

#### getCollection

获取抖音合集列表。

```http
POST /galic/v1/platform/douyin/getCollection
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

**响应:** 获取抖音视频合集列表
---

#### getLocation

获取抖音地点列表。

```http
POST /galic/v1/platform/douyin/getLocation
```

**请求体:**
```json
{
  "accountArgs": {},
  "locationSearchKey": "string",
  "type": 0,
  "cursor": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `locationSearchKey` (string) - 位置搜索关键词
- `type` (number) - 类型
- `cursor` (number) - 页码游标

**响应:** 根据关键词搜索抖音地点列表，支持类型与游标分页
---

#### getMusicCategoryList

获取抖音音乐分类列表。

```http
POST /galic/v1/platform/douyin/getMusicCategoryList
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

**响应:** 获取抖音音乐分类列表，含推荐、榜单、收藏、分类等类型
---

#### getMusicListByCategory

根据分类获取抖音音乐列表。

```http
POST /galic/v1/platform/douyin/getMusicListByCategory
```

**请求体:**
```json
{
  "accountArgs": {},
  "cursor": 0,
  "category_id": "string",
  "type": "rank"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `cursor` (number) - 游标
- `category_id` (string) - 分类ID
- `type` (`rank` \| `recommend` \| `fav` \| `category`) - 音乐类型：rank-榜单音乐（可能已不可用），recommend-推荐音乐（建议优先使用），fav-收藏音乐，category-分类音乐

**响应:** 根据分类、类型、游标获取抖音音乐列表
---

#### getMusicListByKey

根据关键词搜索抖音音乐列表。

```http
POST /galic/v1/platform/douyin/getMusicListByKey
```

**请求体:**
```json
{
  "accountArgs": {},
  "keyword": "string",
  "cursor": 0,
  "count": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `keyword` (string) **必填** - 搜索关键词
- `cursor` (number) - 游标，默认0
- `count` (number) - 数量，默认20

**响应:** 根据关键词搜索抖音音乐列表，支持游标与数量
---

