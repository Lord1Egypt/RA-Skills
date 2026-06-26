# B站 API

B站（哔哩哔哩）是中国领先的弹幕视频平台。API 提供数据分析、投稿管理、评论弹幕、收益中心、粉丝画像等功能的访问。

## 发布参数

### 视频 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | **是** | - | 视频标题（≤80字） |
| `desc` | string | **是** | - | 视频描述（≤2000字） |
| `videoPath` | string | **是** | - | 视频文件本地绝对路径 |
| `coverPath` | string | **是** | - | 封面路径 |
| `timing` | number | 否 | `0` | 定时时间戳，0立即发布，范围：2小时后~15天内 |
| `taskId` | string | **是** | - | 任务ID |
| `copyright` | number | **是** | `1` | 版权类型：1-自制，2-转载 |
| `tid` | object | **是** | - | 分区信息，格式：`{ fenqu_id: number, fenqu_name: string }`，通过 `bilibili/getVideoCategory` 获取 |
| `pubType` | number | **是** | `1` | 发布类型：1-立即发布，0-存草稿 |
| `tags` | string[] | 条件必填 | `[]` | 标签（copyright=1 且有 topic 时可不填，否则至少1个，≤10个，每个≤20字） |
| `source` | string | 条件必填 | - | 转载来源URL（copyright=2时必填） |
| `topic` | object | 否 | - | 活动话题（只能选一个） |
| `cover43` | string | 否 | - | 4:3封面路径（首页推荐） |
| `erchuang` | number | 否 | `0` | 允许转载：0-不允许，1-允许 |
| `danmu` | number | 否 | `1` | 弹幕：0-关闭，1-开启 |
| `comments` | number | 否 | `1` | 评论：0-关闭，1-开启 |
| `curated_comments` | number | 否 | `0` | 精选评论：0-关闭，1-开启 |
| `mentions` | array | 否 | `[]` | @好友列表（≤10个） |
| `self_captions` | number | 否 | `0` | 投稿字幕：0-不投，1-投稿 |
| `dolby_voice` | number | 否 | `0` | 杜比音效：0-关闭，1-开启 |
| `fans_desc` | string | 否 | - | 粉丝动态描述（≤200字） |

**最小可用示例（自制）：**
```json
{ "title": "...", "desc": "", "videoPath": "...", "coverPath": "...", "timing": 0, "taskId": "...", "copyright": 1, "tid": { "fenqu_id": 160, "fenqu_name": "生活" }, "pubType": 1, "tags": ["标签1"] }
```

**最小可用示例（转载）：**
```json
{ "title": "...", "desc": "", "videoPath": "...", "coverPath": "...", "timing": 0, "taskId": "...", "copyright": 2, "tid": { "fenqu_id": 160, "fenqu_name": "生活" }, "pubType": 1, "tags": ["标签1"], "source": "https://原始来源链接" }
```

### 文章 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 标题（≤80字） |
| `content` | string | 否 | - | 文章正文 |
| `covers` | string[] | 否 | - | 封面图路径列表 |
| `taskId` | string | **是** | - | 任务ID |
| `pubType` | number | 否 | `1` | 发布类型：1-立即发布，0-存草稿 |
| `original` | number | 否 | `1` | 原创标识：1-原创，0-转载 |
| `timing` | number | 否 | `0` | 定时时间戳 |

**最小可用示例：**
```json
{ "title": "...", "content": "<p>...</p>", "covers": [], "taskId": "...", "pubType": 1, "original": 1, "timing": 0 }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/bilibili/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

### 数据分析

#### getDataOverview

获取B站数据概览。

```http
POST /galic/v1/platform/bilibili/getDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "tab": 0,
  "period": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `tab` (number) - 标签页类型，0-视频，1-直播，默认为0
- `period` (number) - 时间类型 -1: 昨天 0: 近7天 1: 近30天 2: 近90天 3: 历史累积

**响应:** 返回B站账号在指定时间范围内的数据概览，包括播放量、访客数、粉丝数、点赞数、收藏数等指标
---

#### getSingleDataOverview

获取B站单个视频数据概览。

```http
POST /galic/v1/platform/bilibili/getSingleDataOverview
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

**响应:** 返回B站单个视频的详细数据概览，包括统计数据、播放平台占比、观众地区分布、性别分布、年龄分布等
---

#### getSingleDataTrend

获取B站单个视频数据趋势。

```http
POST /galic/v1/platform/bilibili/getSingleDataTrend
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "type": "coin"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `type` (`coin` \| `fav` \| `share` \| `comment` \| `dm` \| `like` \| `unfollow` \| `fan` \| `play`) **必填** - 统计类型

**响应:** 返回B站单个视频的数据趋势，包括趋势数据、近30天趋势数据、小时趋势数据等
---

#### getDataOverviewGraph

获取B站数据概览图表。

```http
POST /galic/v1/platform/bilibili/getDataOverviewGraph
```

**请求体:**
```json
{
  "accountArgs": {},
  "period": 0,
  "type": "coin"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `period` (number) **必填** - 时间类型 0: 近7天 1: 近30天 2: 近90天 3: 历史累积
- `type` (`coin` \| `fav` \| `share` \| `comment` \| `dm` \| `like` \| `unfollow` \| `fan` \| `play`) **必填** - 统计类型

**响应:** 返回B站账号在指定时间范围内的数据概览图表数据，用于绘制趋势图
---

#### getArticleThirty

获取B站稿件近30天数据。

```http
POST /galic/v1/platform/bilibili/getArticleThirty
```

**请求体:**
```json
{
  "accountArgs": {},
  "type": null
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `type` (any) **必填** - 指标类型

**响应:** 返回稿件近30天按日数据，指标类型为浏览量/评论量/分享数/硬币数/收藏数/点赞数之一
---

### 发布辅助

#### getVideoCategory

获取B站视频分区列表。

```http
POST /galic/v1/platform/bilibili/getVideoCategory
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

**响应:** 返回B站视频分区列表，用于发布时选择分区
---

#### getFriend

获取B站好友/用户列表。

```http
POST /galic/v1/platform/bilibili/getFriend
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

**响应:** 返回B站好友或用户列表，支持关键词搜索
---

#### getActivityTopicList

获取B站活动话题列表。

```http
POST /galic/v1/platform/bilibili/getActivityTopicList
```

**请求体:**
```json
{
  "accountArgs": {},
  "type_pid": 0,
  "keywords": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `type_pid` (number) **必填** - 话题类型ID，必传
- `keywords` (string) - 搜索关键词，有则搜索

**响应:** 返回B站活动话题列表，支持按类型获取或关键词搜索
---

#### getHotActivities

获取B站热门活动列表。

```http
POST /galic/v1/platform/bilibili/getHotActivities
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
- `pageNum` (number) - 页码，从 1 开始，默认 1
- `pageSize` (number) - 每页条数，默认 20

**响应:** 返回B站热门活动列表，支持分页
---

### 互动管理

#### getComments

获取B站 UP 主评论列表。

```http
POST /galic/v1/platform/bilibili/getComments
```

**请求体:**
```json
{
  "accountArgs": {},
  "order": 0,
  "filter": 0,
  "type": 0,
  "pageNum": 0,
  "pageSize": 0,
  "chargePlusFilter": true
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `order` (number) - 排序 1:最近发布 2:点赞最多 3:回复最多，默认 1
- `filter` (number) - 筛选，-1 为全部，默认 -1
- `type` (number) - 类型 1:视频评论 12:专栏评论 14:音频评论，默认 1
- `pageNum` (number) - 页码，从 1 开始，默认 1
- `pageSize` (number) - 每页条数，默认 10
- `chargePlusFilter` (boolean) - 充电筛选，默认 false

**响应:** 返回B站视频/专栏/音频的评论列表，支持排序与分页
---

#### getDanmuList

获取B站最近弹幕列表。

```http
POST /galic/v1/platform/bilibili/getDanmuList
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
- `pageNum` (number) - 页码，从 1 开始，默认 1
- `pageSize` (number) - 每页条数，默认 50

**响应:** 返回B站账号最近发送的弹幕列表，支持分页
---

#### searchDanmuList

搜索B站弹幕列表。

```http
POST /galic/v1/platform/bilibili/searchDanmuList
```

**请求体:**
```json
{
  "accountArgs": {},
  "oid": 0,
  "type": 0,
  "keyword": "string",
  "order": "string",
  "sort": "string",
  "pageNum": 0,
  "pageSize": 0,
  "cpFilter": true
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `oid` (number) **必填** - 作品 id（oid）从投稿列表接口获取，必填
- `type` (number) - 类型，默认 1
- `keyword` (string) - 关键词，空字符串表示不按关键词搜索，默认 ""
- `order` (string) - 排序字段，如 ctime，默认 ctime
- `sort` (string) - 排序方向 desc/asc，默认 desc
- `pageNum` (number) - 页码，从 1 开始，默认 1
- `pageSize` (number) - 每页条数，默认 50
- `cpFilter` (boolean) - 充电筛选，默认 false

**响应:** 按作品与关键词搜索弹幕，返回匹配的弹幕列表
---

### 投稿管理

#### getArchives

获取B站投稿列表。

```http
POST /galic/v1/platform/bilibili/getArchives
```

**请求体:**
```json
{
  "accountArgs": {},
  "keyword": "string",
  "status": "string",
  "pageNum": 0,
  "pageSize": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `keyword` (string) - 关键词，无则传空字符串
- `status` (string) - 状态筛选，如 pubed / is_pubing,pubed,not_pubed
- `pageNum` (number) - 页码，从 1 开始，默认 1
- `pageSize` (number) - 每页条数，默认 10

**响应:** 返回B站账号投稿列表，支持关键词、状态筛选与分页
---

### 收益中心

#### getEarningActivities

获取B站收益中心活动列表。

```http
POST /galic/v1/platform/bilibili/getEarningActivities
```

**请求体:**
```json
{
  "accountArgs": {},
  "sLocale": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `sLocale` (string) - 语言，默认 zh_CN

**响应:** 返回B站收益中心活动列表，含商业活动、有奖活动分类
---

#### getEarningIncomeOverview

获取B站收益中心收益概览。

```http
POST /galic/v1/platform/bilibili/getEarningIncomeOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "sLocale": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `sLocale` (string) - 语言，默认 zh_CN

**响应:** 返回B站收益中心收益概览，含日期范围、汇总金额及明细
---

#### getEarningIncomeTrend

获取B站收益中心收益趋势。

```http
POST /galic/v1/platform/bilibili/getEarningIncomeTrend
```

**请求体:**
```json
{
  "accountArgs": {},
  "days": 0,
  "sLocale": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `days` (integer) **必填** - 查询天数，1-30
- `sLocale` (string) - 语言，默认 zh_CN

**响应:** 返回B站收益中心按日的收益趋势数据
---

#### getEarningCollegeExperiment

获取B站收益中心创作学院实验。

```http
POST /galic/v1/platform/bilibili/getEarningCollegeExperiment
```

**请求体:**
```json
{
  "accountArgs": {},
  "sLocale": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `sLocale` (string) - 语言，默认 zh_CN

**响应:** 返回创作学院教程列表与优质案例列表
---

### 创作工具

#### getNotices

获取B站创作中心通知列表。

```http
POST /galic/v1/platform/bilibili/getNotices
```

**请求体:**
```json
{
  "accountArgs": {},
  "type": null,
  "from": 0,
  "limit": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `type` (any) **必填** - 1=激励月报 2=激励课堂 3=征稿活动 4=违规公告
- `from` (integer) - 分页游标，首次 0，第二页为上一页的 from+limit
- `limit` (integer) **必填** - 每页数量，如 7

**响应:** 返回创作中心通知列表，含激励月报、激励课堂、征稿活动、违规公告等类型
---

#### getHighQualityCreations

获取B站优质创作流。

```http
POST /galic/v1/platform/bilibili/getHighQualityCreations
```

**请求体:**
```json
{
  "accountArgs": {},
  "sLocale": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `sLocale` (string) - 语言，默认 zh_CN

**响应:** 返回创作成长优质创作流，含每周必看列表与精选推荐列表
---

### 粉丝画像

#### getFansList

获取B站粉丝列表。

```http
POST /galic/v1/platform/bilibili/getFansList
```

**请求体:**
```json
{
  "accountArgs": {},
  "pn": 0,
  "ps": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `pn` (integer) - 页码
- `ps` (integer) - 每页数量，最大 50

**响应:** 返回B站账号的粉丝列表
---

#### getFansOverview

获取B站粉丝数据概览。

```http
POST /galic/v1/platform/bilibili/getFansOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "period": null
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `period` (any) - 周期：-1 昨日，0 近7日，1 近30日，2 近90日

**响应:** 返回数据中心观众分析的粉丝数据概览，含指定时间范围内的粉丝与互动指标
---

#### getFansTrend

获取B站粉丝趋势。

```http
POST /galic/v1/platform/bilibili/getFansTrend
```

**请求体:**
```json
{
  "accountArgs": {},
  "type": "all_fans",
  "period": null
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `type` (`all_fans` \| `follow` \| `fan` \| `unfollow`) - 类型：all_fans 粉丝总数，follow 新增关注，fan 净增粉丝，unfollow 取消关注
- `period` (any) - 周期：0 最近7天，1 最近30天，2 最近90天

**响应:** 返回粉丝趋势图数据，含粉丝总数、新增关注、净增粉丝、取消关注等维度在指定时间范围内的趋势
---

#### getFanRank

获取B站粉丝排行。

```http
POST /galic/v1/platform/bilibili/getFanRank
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

**响应:** 返回近30天粉丝排行，含累计视频播放时长、视频互动指标、动态互动指标、粉丝勋章等维度排行
---

#### getFansStatSource

获取B站粉丝来源统计。

```http
POST /galic/v1/platform/bilibili/getFansStatSource
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

**响应:** 返回数据中心观众分析-粉丝来源统计，含视频、专栏、直播、空间、搜索、推荐、其他等各来源粉丝数
---

#### getDataTrend

获取B站数据趋势/观众画像。

```http
POST /galic/v1/platform/bilibili/getDataTrend
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

**响应:** 返回数据中心观众分析-兴趣分布，含粉丝与非粉丝的兴趣类型分布数据
---

#### getDataBase

获取B站数据中心观众基础数据。

```http
POST /galic/v1/platform/bilibili/getDataBase
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

**响应:** 返回观众地域分布（粉丝/非粉丝省份）与观众基础画像（性别/年龄/平台：粉丝/非粉丝）
---

#### getFansPortrayal

获取B站粉丝画像。

```http
POST /galic/v1/platform/bilibili/getFansPortrayal
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

**响应:** 返回粉丝画像数据：粉丝年龄/性别分布、24小时活跃时段、观众类型、观众地区、同领域粉丝活跃时段
---

