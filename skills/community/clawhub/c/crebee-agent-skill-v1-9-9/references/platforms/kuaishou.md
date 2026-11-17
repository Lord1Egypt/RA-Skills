# 快手 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。可选字段无值时省略，不能传 `null`；示例保留实际发布需要的 `taskId`。

### 视频 params

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `title` | string | 否 | 视频标题 |
| `desc` | string | 是 | 视频描述 |
| `videoPath` / `coverPath` | string | 是 | 本地视频 / 封面路径 |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布，定时为 1 小时后至 14 天内 |
| `taskId` | string | 否（运行时必传） | 任务 ID |
| `videoInfo` | `{ duration: number; width: number; height: number; size: number; thumbnail?: string }` | 否 | 视频信息 |
| `allowSameFrame` / `allowDownload` / `nearbyShow` | number | 否 | 运行时使用 `0` 或 `1` |
| `visibilityType` | `1 \| 2 \| 4` | 否 | 公开 / 私密 / 好友可见 |
| `position` | `{ position_id: string; position_name: string; position_address: string; latitude: string; longitude: string }` | 否 | 位置，通过 `kuaishou/getLocation` 获取 |
| `topics` | `{ topic_name: string; topic_id: number; topic_view_count: number }[]` | 否 | 话题，通过 `kuaishou/getTopic` 获取 |
| `mentions` | `{ friend_name: string; friend_uid: string; friend_follower_count: number; friend_avatar: string }[]` | 否 | 提及用户，通过 `kuaishou/getFriend` 获取 |
| `activities` | `{ activity_detail_id: number; activity_source_id: number; activity_unclaimed: boolean; activity_name: string; activity_cover_image?: string; activity_custom_tag?: string; activity_tag_labels?: string[]; activity_brief?: string; activity_start_time?: number; activity_end_time?: number }[]` | 否 | 活动；先调用 `kuaishou/getActivityConfig` 获取筛选项，再调用 `kuaishou/getActivityList` 获取列表 |
| `declareInfo` | `{ source?: 1 \| 2 \| 3 }` | 否 | 内容声明 |
| `goods` | `{ title: string; url: string; price: number; promoterName: string \| null; associateTaskId: { taskId: number; bindId: string; entranceType: number; bindType: string; taskType: string } }[]` | 否 | 商品，通过 `kuaishou/getGoodsList` 获取 |

**最小参数校验示例：**

```json
{ "desc": "", "videoPath": "/tmp/video.mp4", "coverPath": "/tmp/cover.jpg", "timing": 0, "taskId": "task-1" }
```

### 图文 params

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `desc` | string | 否 | 描述 |
| `images` | string[] | 否 | 本地图片路径 |
| `taskId` | string | 否（运行时必传） | 任务 ID |
| `cover` | string | 否 | 本地封面路径 |
| `photoStatus` | `1 \| 2 \| 4` | 否 | 公开 / 私密 / 仅好友可见 |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布，定时为 1 小时后至 14 天内 |
| `position` / `topics` / `mentions` | 与视频同名字段类型相同 | 否 | 分别通过 `kuaishou/getLocation`、`kuaishou/getTopic`、`kuaishou/getFriend` 获取 |
| `activities` / `goods` | 与视频同名字段类型相同 | 否 | 活动通过 `kuaishou/getActivityConfig` + `kuaishou/getActivityList` 获取；商品通过 `kuaishou/getGoodsList` 获取 |
| `music` | `{ music_id: string; music_name: string; music_author: string; music_cover: string; music_duration: number; music_url: string }` | 否 | 背景音乐，通过 `kuaishou/getMusicList` 获取 |
| `declareInfo` | `{ source?: 1 \| 2 \| 3 }` | 否 | 内容声明 |

**最小参数校验示例：**

```json
{ "desc": "示例图文", "images": ["/tmp/image.jpg"], "timing": 0, "taskId": "task-1" }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/kuaishou/`

### 数据分析

#### getDataOverview

获取快手数据概览。

```http
POST /galic/v1/platform/kuaishou/getDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "timeType": 0,
  "startDate": 0,
  "endDate": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `timeType` (number) - 时间类型，1=最近7天，2=最近30天，3=最近90天，默认为2。与 startDate/endDate 二选一，startDate+endDate 优先
- `startDate` (number) - 开始日期，毫秒级时间戳
- `endDate` (number) - 结束日期，毫秒级时间戳

**响应:** 返回快手账号在指定时间范围内的数据概览，包括播放量、点赞数、评论数、分享数等指标及其趋势数据
---

#### getSingleDataOverview

获取快手单个视频数据概览。

```http
POST /galic/v1/platform/kuaishou/getSingleDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "timeGranularity": "string",
  "dataChangeType": "string",
  "tabType": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `timeGranularity` (string) **必填** - 时间粒度 1:每小时 2:每天
- `dataChangeType` (string) **必填** - 数据变化类型 1:新增 2:累计
- `tabType` (number) - 标签页类型 1:播放数据 2:互动效果

**响应:** 返回快手单个视频的详细数据概览，包括播放数据、互动效果等各项指标及其趋势数据
---

#### getFansPortrait

获取快手用户画像数据。

```http
POST /galic/v1/platform/kuaishou/getFansPortrait
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

**响应:** 返回快手账号的用户画像数据，包括设备系统分布、省份分布、城市分布、兴趣分布、性别分布、活跃度分布、年龄分布等
---

#### getInspirationMaterialList

获取快手创作灵感素材列表。

```http
POST /galic/v1/platform/kuaishou/getInspirationMaterialList
```

**请求体:**
```json
{
  "accountArgs": {},
  "pcursor": "string",
  "categoryId": 0,
  "displayType": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `pcursor` (string) - 分页游标，首次传空字符串，后续传上次返回的 pcursor
- `categoryId` (number) - 综合：传 -1，首次请求可不传（默认综合）
- `displayType` (number) - 粉丝爱看：传 2，与 categoryId 二选一

**响应:** 返回创作灵感页素材列表及分页游标，每条素材含封面、日期、作品数、标签、收藏状态等
---

#### getInspirationRankSearch

获取快手创作灵感榜单搜索。

```http
POST /galic/v1/platform/kuaishou/getInspirationRankSearch
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

**响应:** 返回创作灵感页热搜榜单列表，每条含关键词、分类与热度值
---

#### getActivityDetail

获取快手活动详情。

```http
POST /galic/v1/platform/kuaishou/getActivityDetail
```

**请求体:**
```json
{
  "accountArgs": {},
  "id": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `id` (number) **必填** - 活动详情 ID，来自活动列表的 activity_detail_id

**响应:** 返回单条活动详情，含标题、时间范围、规则说明、示例作品列表等；
---

#### getHotspotSearch

获取快手热点搜索。

```http
POST /galic/v1/platform/kuaishou/getHotspotSearch
```

**请求体:**
```json
{
  "accountArgs": {},
  "searchText": "string",
  "page": 0,
  "count": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `searchText` (string) **必填** - 搜索关键词
- `page` (number) - 页码
- `count` (number) - 每页条数

**响应:** 按关键词返回热点列表及总数，每条含描述、热度、封面、类型等
---

#### getHotspotListOptions

获取快手热点榜选项。

```http
POST /galic/v1/platform/kuaishou/getHotspotListOptions
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

**响应:** 返回热点分类列表（categoryId、categoryName）与榜单类型配置（trendingType、标题、图标等），供热点榜列表筛选与分页请求使用
---

#### getHotspotList

获取快手热点榜列表。

```http
POST /galic/v1/platform/kuaishou/getHotspotList
```

**请求体:**
```json
{
  "accountArgs": {},
  "trendingType": "string",
  "categoryId": "string",
  "pcursor": 0,
  "count": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `trendingType` (string) **必填** - 榜单类型，来自 getKuaishouHotspotListOptionsHandler 的 trendingListConfig[].trendingType
- `categoryId` (string) **必填** - 分类 ID，来自 getKuaishouHotspotListOptionsHandler 的 categoryListConfig[].categoryId
- `pcursor` (number) - 分页游标，首次传 1，后续传上次返回的 pcursor
- `count` (number) - 每页条数

**响应:** 返回当前页热点列表（词条 id、描述、热度值、观看数、封面图等）、总条数及是否有权限
---

### 发布辅助

#### getFriend

获取快手好友/用户列表。

```http
POST /galic/v1/platform/kuaishou/getFriend
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

**响应:** 返回快手好友或用户列表
---

#### getLocation

获取快手地点列表。

```http
POST /galic/v1/platform/kuaishou/getLocation
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

**响应:** 根据关键词搜索快手地点列表
---

#### getTopic

获取快手话题列表。

```http
POST /galic/v1/platform/kuaishou/getTopic
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

**响应:** 根据关键词搜索快手话题列表
---

#### getCategory

获取快手领域/分类列表。

```http
POST /galic/v1/platform/kuaishou/getCategory
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

**响应:** 返回快手领域分类列表
---

#### getMusicList

获取快手音乐列表。

```http
POST /galic/v1/platform/kuaishou/getMusicList
```

**请求体:**
```json
{
  "accountArgs": {},
  "keyword": "string",
  "page": 0,
  "count": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `keyword` (string) - 搜索关键词
- `page` (number) - 页码，从0开始
- `count` (number) - 每页数量

**响应:** 返回快手音乐列表，支持关键词搜索与分页
---

#### getActivityList

获取快手活动列表。

```http
POST /galic/v1/platform/kuaishou/getActivityList
```

**请求体:**
```json
{
  "accountArgs": {},
  "page": 0,
  "count": 0,
  "category": 0,
  "sortType": 0,
  "rewardType": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `page` (number) - 页码，默认为 1
- `count` (number) - 每页数量，默认为 20
- `category` (number) - 分类，默认为 0（综合）
- `sortType` (number) - 排序类型，默认为 0（默认排序）
- `rewardType` (number) - 收益类型，默认为 0（全部）

**响应:** 返回快手活动列表，支持分页与筛选（分类、排序、收益类型），pageSource 固定为创作者中心
---

#### getActivityConfig

获取快手活动配置。

```http
POST /galic/v1/platform/kuaishou/getActivityConfig
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

**响应:** 返回活动筛选条件配置：分类 Tab、收益类型、排序类型、标签类型等
---

#### sendActivityClaim

领取快手活动。

```http
POST /galic/v1/platform/kuaishou/sendActivityClaim
```

**请求体:**
```json
{
  "accountArgs": {},
  "activityId": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `activityId` (number) **必填** - 活动任务 ID（对应活动列表项的 sourceId）

**响应:** 根据活动任务 ID（sourceId）领取快手活动
---

#### getGoodsList

获取快手商品列表。

```http
POST /galic/v1/platform/kuaishou/getGoodsList
```

**请求体:**
```json
{
  "accountArgs": {},
  "type": null,
  "cursor": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `type` (any) **必填** - 商品类型：1=本店商品, 2=其他
- `cursor` (string) **必填** - 分页游标

**响应:** 按商品类型分页查询商品列表，返回商品名称、图片、价格、推广者及绑定信息
---

