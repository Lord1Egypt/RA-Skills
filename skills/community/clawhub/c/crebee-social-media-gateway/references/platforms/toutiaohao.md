# 头条号 API

头条号是字节跳动的内容创作平台。API 提供数据分析、粉丝画像、话题搜索、活动任务等功能的访问。

## 发布参数

> 竖版视频不支持定时、描述（desc）、话题。

### 视频 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 视频标题（≤30字） |
| `desc` | string | 否 | - | 视频描述（横版≤400字；**竖版无效**） |
| `videoPath` | string | **是** | - | 视频文件本地绝对路径 |
| `coverPath` | string | **是** | - | 封面路径 |
| `timing` | number | **是** | `0` | 定时时间戳，0立即发布，横版可定时（2小时后~7天内）；**竖版不支持定时** |
| `taskId` | string | **是** | - | 任务ID |
| `videoType` | string | **是** | `"horizontal"` | 视频方向：`"horizontal"`（横版）或 `"vertical"`（竖版） |
| `visibilityType` | number | 否 | `0` | 可见性（仅横版）：0-公开，1-仅自己，2-互关可见 |
| `pubType` | number | 否 | `1` | 发布类型：1-立即发布，0-存草稿 |
| `topics` | array | 否 | `[]` | 话题列表（**仅横版有效**） |
| `collection` | object | 否 | - | 合集（仅横版） |
| `externalLink` | string | 否 | `""` | 外部链接（有效URL） |
| `generateImage` | object | 否 | - | 生成图文配置：`{ enable: boolean, publishType?: 1\|2 }` |
| `workStatement` | string | 否 | - | 作品声明 |

**最小可用示例（横版）：**
```json
{ "title": "...", "desc": "", "videoPath": "...", "coverPath": "...", "timing": 0, "taskId": "...", "videoType": "horizontal", "visibilityType": 0, "pubType": 1, "topics": [], "externalLink": "" }
```

**最小可用示例（竖版）：**
```json
{ "title": "...", "videoPath": "...", "coverPath": "...", "timing": 0, "taskId": "...", "videoType": "vertical" }
```

### 图文 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 标题 |
| `desc` | string | 否 | - | 描述（≤400字） |
| `images` | string[] | 否 | - | 图片路径列表 |
| `taskId` | string | **是** | - | 任务ID |

**最小可用示例：**
```json
{ "title": "...", "desc": "", "images": ["..."], "taskId": "..." }
```

### 文章 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 标题（≤30字） |
| `content` | string | 否 | - | 文章正文 |
| `covers` | string[] | 否 | - | 封面图路径列表 |
| `taskId` | string | **是** | - | 任务ID |
| `timing` | number | 否 | - | 定时时间戳 |

**最小可用示例：**
```json
{ "title": "...", "content": "<p>...</p>", "covers": [], "taskId": "...", "timing": 0 }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/toutiaohao/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
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

### 粉丝画像

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

### 活动任务

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

### 热门内容

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

