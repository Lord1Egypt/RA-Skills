# 快手 API

快手是中国领先的短视频社交平台。API 提供数据分析、粉丝画像、话题活动、热点排名、创作灵感等功能的访问。

## 发布参数

> 可见性值与其他平台不同：**1**-公开，**2**-私密，**4**-好友可见。

### 视频 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 视频标题 |
| `desc` | string | 否 | - | 视频描述（≤500字） |
| `videoPath` | string | **是** | - | 视频文件本地绝对路径 |
| `coverPath` | string | **是** | - | 封面路径 |
| `timing` | number | **是** | `0` | 定时时间戳，0立即发布，范围：1小时后~14天内 |
| `taskId` | string | **是** | - | 任务ID |
| `visibilityType` | number | **是** | `1` | 可见性：**1**-公开，**2**-私密，**4**-好友可见 |
| `topics` | array | 否 | `[]` | 话题列表，格式：`[{ topic_name, topic_id, topic_view_count }]` |
| `mentions` | array | 否 | `[]` | @用户列表（≤10个） |
| `position` | object\|null | 否 | `null` | 位置信息 |
| `activities` | array | 否 | `[]` | 活动列表 |
| `allowSameFrame` | number | 否 | `1` | 允许同框：0-不允许，1-允许 |
| `allowDownload` | number | 否 | `1` | 允许下载：0-不允许，1-允许 |
| `nearbyShow` | number | 否 | `0` | 同城展示：0-不展示，1-展示 |
| `declareInfo` | object | 否 | - | 声明信息：`{ source: 1\|2\|3 }`（1-AI生成，2-演绎情节，3-个人观点） |

**最小可用示例：**
```json
{ "title": "...", "desc": "", "videoPath": "...", "coverPath": "...", "timing": 0, "taskId": "...", "visibilityType": 1, "topics": [], "mentions": [], "position": null, "activities": [], "allowSameFrame": 1, "allowDownload": 1, "nearbyShow": 0 }
```

### 图文 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `desc` | string | 否 | - | 描述（≤500字） |
| `images` | string[] | 否 | - | 图片路径列表 |
| `taskId` | string | **是** | - | 任务ID |
| `timing` | number | **是** | `0` | 定时时间戳，0立即发布，范围：1小时后~14天内 |
| `cover` | string | 否 | - | 封面路径 |
| `photoStatus` | number | 否 | `1` | 可见性：1-公开，2-私密，4-仅好友可见 |
| `topics` | array | 否 | `[]` | 话题列表 |
| `mentions` | array | 否 | `[]` | @用户列表 |
| `position` | object\|null | 否 | `null` | 位置信息 |
| `activities` | array | 否 | - | 活动列表 |
| `music` | object\|null | 否 | - | 背景音乐 |
| `declareInfo` | object | 否 | - | 声明信息 |

**最小可用示例：**
```json
{ "desc": "", "images": ["..."], "timing": 0, "taskId": "...", "photoStatus": 1, "topics": [], "mentions": [], "position": null, "activities": [] }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/kuaishou/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

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

### 粉丝画像

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

### 活动任务

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

### 热门内容

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

