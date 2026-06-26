# 百家号 API

百家号是百度的内容创作平台。API 提供数据分析、话题活动、分类管理、热点推荐、任务市场等功能的访问。

## 发布参数

> `verticalCoverPath`（竖版封面）为必填，无论横版还是竖版视频都需要提供。

### 视频 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 视频标题（≤30字） |
| `desc` | string | 否 | - | 视频描述（横版≤100字） |
| `videoPath` | string | **是** | - | 视频文件本地绝对路径 |
| `coverPath` | string | **是** | - | 封面路径 |
| `timing` | number | **是** | `0` | 定时时间戳，0立即发布，范围：1小时后~7天内 |
| `taskId` | string | **是** | - | 任务ID |
| `videoType` | string | **是** | `"horizontal"` | 视频方向：`"horizontal"`（横版）或 `"vertical"`（竖版） |
| `verticalCoverPath` | string | **是** | - | 竖版封面路径（**必填，即使是横版视频**） |
| `pubType` | number | 否 | `1` | 发布类型：1-立即发布，0-存草稿 |
| `isAigc` | boolean | 否 | `false` | 是否为AI生成内容 |
| `topic` | object | 否 | - | 话题 |
| `activityId` | object | 否 | - | 活动 |
| `category` | object | 否 | - | 分类信息，通过 `baijiahao/getCategory` 获取 |
| `collection` | object | 否 | - | 合集 |
| `tags` | string[] | 否 | `[]` | 标签（横版视频≤5个，每个≤20字） |

**最小可用示例：**
```json
{ "title": "...", "desc": "", "videoPath": "...", "coverPath": "...", "verticalCoverPath": "...", "timing": 0, "taskId": "...", "videoType": "horizontal", "pubType": 1, "isAigc": false, "tags": [] }
```

### 文章 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 标题（2-64字） |
| `content` | string | 否 | - | 文章正文 |
| `covers` | string[] | 否 | - | 封面图路径列表 |
| `taskId` | string | **是** | - | 任务ID |
| `category` | object | **是** | - | 分类信息（**必填**），通过 `baijiahao/getCategory` 获取 |
| `pubType` | number | 否 | `1` | 发布类型：1-立即发布，0-存草稿 |
| `summary` | string | 否 | - | 摘要（≤300字，不填则抓取正文前200字） |
| `timing` | number | 否 | `0` | 定时时间戳 |

**最小可用示例：**
```json
{ "title": "...(2-64字)", "content": "<p>...</p>", "covers": [], "taskId": "...", "category": { "通过baijiahao/getCategory获取": true }, "pubType": 1, "timing": 0 }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/baijiahao/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

### 数据分析

#### getDataOverview

获取百家号数据概览。

```http
POST /galic/v1/platform/baijiahao/getDataOverview
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
- `startDate` (string) - 开始日期。传 Date 或 ISO 字符串，JSON 会转成字符串
- `endDate` (string) - 结束日期。传 Date 或 ISO 字符串，JSON 会转成字符串

**响应:** 返回百家号账号在指定时间范围内的数据概览，包括视频数据统计、互动数据统计和时间范围数据
---

#### getSingleDataOverview

获取百家号单个内容数据概览。

```http
POST /galic/v1/platform/baijiahao/getSingleDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "startDate": "2025-01-21",
  "endDate": "2025-01-21",
  "dataType": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `startDate` (string) - 开始日期。传 Date 或 ISO 字符串，JSON 会转成字符串
- `endDate` (string) - 结束日期。传 Date 或 ISO 字符串，JSON 会转成字符串
- `dataType` (string) - 数据类型

**响应:** 返回百家号单个内容在指定时间范围内的详细数据概览，包括播放量统计、互动数据统计和时间趋势数据
---

#### getSingleDataOverviewStatistic

获取百家号单个内容数据概览统计。

```http
POST /galic/v1/platform/baijiahao/getSingleDataOverviewStatistic
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "timestamp": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `timestamp` (number) - 时间戳

**响应:** 返回百家号单个内容的详细统计数据，包括趋势分析数据、对比分析数据和性能指标数据
---

#### getSubmissionAnalysis

获取百家号投稿建议分析。

```http
POST /galic/v1/platform/baijiahao/getSubmissionAnalysis
```

**请求体:**
```json
{
  "accountArgs": {},
  "version": 0,
  "filterType": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `version` (integer) - 接口版本号，固定为 2
- `filterType` (string) - 排序或过滤类型，如 view_count（高播放量）、recommend_count（高推荐量）等

**响应:** 返回百家号数据分析-投稿建议，包含各分类投稿与播放表现排名、最佳分类的投稿建议与参考作者、投稿分析文案等，用于优化创作方向与垂类策略。
---

### 发布辅助

#### getTopicList

获取百家号话题列表。

```http
POST /galic/v1/platform/baijiahao/getTopicList
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

**响应:** 返回百家号推荐与热门话题列表，支持关键词搜索
---

#### getActivityList

获取百家号活动列表。

```http
POST /galic/v1/platform/baijiahao/getActivityList
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

**响应:** 返回百家号活动列表，包含活动ID、名称、封面、参与人数等
---

#### getCategoryList

获取百家号分类列表。

```http
POST /galic/v1/platform/baijiahao/getCategoryList
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

**响应:** 返回百家号分类列表，含主分类与子分类
---

#### getCollectionsList

获取百家号合集列表。

```http
POST /galic/v1/platform/baijiahao/getCollectionsList
```

**请求体:**
```json
{
  "accountArgs": {},
  "currentPage": 0,
  "pageSize": 0,
  "search": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `currentPage` (number) - 当前页码，默认1
- `pageSize` (number) - 每页数量，默认50
- `search` (string) - 搜索关键词

**响应:** 返回百家号合集列表，支持分页与搜索
---

### 活动任务

#### getRecommendTaskList

获取百家号推荐任务列表。

```http
POST /galic/v1/platform/baijiahao/getRecommendTaskList
```

**请求体:**
```json
{
  "accountArgs": {},
  "pageNo": 0,
  "pageSize": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `pageNo` (integer) - 页码，从 1 开始，默认 1
- `pageSize` (integer) - 每页数量，默认 18，最大 100

**响应:** 返回百家号作者首页的推荐任务列表，用于领取或参与创作任务（含话题、奖励、剩余时间等信息）
---

#### getAllTaskList

获取百家号全部任务列表。

```http
POST /galic/v1/platform/baijiahao/getAllTaskList
```

**请求体:**
```json
{
  "accountArgs": {},
  "pageNo": 0,
  "pageSize": 0,
  "taskType": 0,
  "taskOrigin": "string",
  "articleType": 0,
  "taskDomain": "string",
  "taskAttend": 0,
  "collectionFlag": null,
  "taskName": "string",
  "taskClassify": 0,
  "from": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `pageNo` (integer) - 页码，从 1 开始，默认 1
- `pageSize` (integer) - 每页数量，默认 20，最大 100
- `taskType` (integer) - 任务类型：-1 全部任务，0 挑战任务，1 征文活动，2 招募任务，6 在线任务
- `taskOrigin` (string) - 任务来源：all 全部；paid_column 付费专栏；online_retailers 电商；duxingxuan 度星选；vitality_cash 活力值变现
- `articleType` (integer) - 文章类型：-1 全部，1 图文，2 视频，3 动态，4 小视频，5 视频合集
- `taskDomain` (string) - 任务领域，不传或为空表示全部领域
- `taskAttend` (integer) - 任务参与状态，1 表示可参与
- `collectionFlag` (any) - 收藏标记，部分场景传 1
- `taskName` (string) - 任务名称搜索关键字
- `taskClassify` (integer) - 任务分类，1 表示全部
- `from` (string) - 来源标记，默认 pc_square

**响应:** 返回百家号任务广场的全部任务列表，可按任务来源、文章类型、任务领域等条件筛选，用于创作选题和活动参与。请求前可先调用「获取任务领域」接口得到 task_domain 可选值（如：军事、科技、历史、社会、影视、美食、游戏、旅游、汽车、教育、生活、健康养生、财经等），再传 taskDomain 进行筛选。
---

### 热门内容

#### getRealtimeHotList

获取百家号实时热点列表。

```http
POST /galic/v1/platform/baijiahao/getRealtimeHotList
```

**请求体:**
```json
{
  "accountArgs": {},
  "pageNum": 0,
  "pageSize": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `pageNum` (integer) - 页码，从 1 开始，对应 pn
- `pageSize` (integer) - 每页数量，对应 rn

**响应:** 返回百家号灵感中心的实时热点列表，包含热点标题、封面、标签等，按热度和时间实时更新，可用于选题参考。
---

#### getHotTopicList

获取百家号热门话题列表。

```http
POST /galic/v1/platform/baijiahao/getHotTopicList
```

**请求体:**
```json
{
  "accountArgs": {},
  "pageNum": 0,
  "pageSize": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `pageNum` (integer) - 页码，从 1 开始，对应 pn
- `pageSize` (integer) - 每页数量，对应 rn

**响应:** 返回百家号灵感中心的热门话题与近期热点事件列表，包含话题 ID、标题、封面、热度值与参与量等信息，可用于创作选题和挂话题。
---

#### getMainRankFlow

获取百家号主榜单/特色榜聚合数据。

```http
POST /galic/v1/platform/baijiahao/getMainRankFlow
```

**请求体:**
```json
{
  "accountArgs": {},
  "listType": "main",
  "rankValue": "string",
  "listName": "string",
  "listId": null,
  "pageNo": 0,
  "pageSize": 0,
  "needUserRank": true
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `listType` (`main` \| `other`) - 榜单类型：main 主榜单（baijiabang_main），other 特色榜（baijiabang_other）
- `rankValue` (string) - 子榜单 BID，用于切换子榜单（如万象、权威领航等），须为当前榜单 rank_list 中的 value；不传则使用列表首项
- `listName` (string) - 领域 list_name，用于领域达人榜下多领域时指定某一领域（如 bjh_baijiabang_crwsk 人文社科），须为 collection 返回的 data[].list_name；不传则使用首项
- `listId` (any) - 期次 ID，用于选择时间（如 2025年、2024年），须为 collection 返回的 periods[].list_id；不传则使用最新一期
- `pageNo` (integer) - 页码，从 1 开始，默认 1
- `pageSize` (integer) - 每页数量，默认 30，最大 100
- `needUserRank` (boolean) - 是否返回当前作者在该榜单中的排名

**响应:** 一次性返回榜单列表、时间范围（含 list_name 与各期 list_id）以及对应期次的榜单内容。通过 body.listType 区分：main 主榜单（baijiabang_main），other 特色榜（baijiabang_other）。
---

### 创作工具

#### getCoordinateTask

获取百家号质量与活跃建议任务。

```http
POST /galic/v1/platform/baijiahao/getCoordinateTask
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

**响应:** 返回百家号成长中心的质量与活跃建议任务，包括当前/前一日质量与活跃坐标、质量任务与活跃任务列表以及整改建议文案，用于指导创作者提升内容质量和账号活跃度。
---

