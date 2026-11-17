# 小红书 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。可选字段无值时省略；仅 `collection` 明确支持 `null`。示例保留实际发布需要的 `taskId`。

标题按平台规则限制为 20 字；中文、`^` 和编码大于 127 的字符按两个半角字符计数后向上取整。

### 视频 params

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `title` / `desc` | string | 是 | 视频标题 / 描述 |
| `videoPath` / `coverPath` | string | 是 | 本地视频 / 封面路径 |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布，定时为 1 小时后至 14 天内 |
| `taskId` | string | 否（运行时必传） | 任务 ID |
| `videoInfo` | `{ duration: number; width: number; height: number; size: number; thumbnail?: string }` | 否 | 视频信息 |
| `visibilityType` | `0 \| 1 \| 4` | 否 | 公开 / 私密 / 仅互关好友可见 |
| `topics` | `{ topic_id: string; topic_name: string; topic_link: string; topic_view_count: number }[]` | 否 | 话题，通过 `xiaohongshu/getTopic` 获取 |
| `mentions` | `{ friend_uid: string; friend_name: string; friend_avatar: string }[]` | 否 | 提及用户，通过 `xiaohongshu/getFriend` 获取 |
| `location` | `{ position_id: string; position_name: string; position_address: string; position_source?: number }` | 否 | 位置，通过 `xiaohongshu/getLocation` 获取 |
| `userDeclarationBind` | `{ origin: 1 \| 2 \| 3 \| 4 \| 5; photoInfo?: { photoPlace?: { position_id: string; position_name: string; position_address: string; position_source?: number }; photoTime?: string }; repostInfo?: { source: string } }` | 否 | 声明；`origin: 5` 时 `repostInfo.source` 必填 |
| `originalStatement` | `"ORIGINAL_STATEMENT"` | 否 | 原创声明；仅可与 `userDeclarationBind.origin: 4` 一起使用 |
| `goods` | `{ goods_id: string; name: string; purchase_price: number; purchase_price_range: string; image: string; inventory: number; goods_seller_type: string }[]` | 否 | 商品；先调用 `xiaohongshu/getGoodsPermission` 获取账号权限与分类，再调用 `xiaohongshu/getGoodsList` 选择商品 |
| `goodsEntranceType` | `"GOODS_SELLER_V2" \| "RELATED_GOODS" \| "LIFE_SERVICE_KOL"` | 否 | 商品入口，取 `xiaohongshu/getGoodsPermission` 返回项的 `note_flag` |
| `collection` | `{ id: string; name: string; type: number; paid: number; total_episodes: number; note_num: number } \| null` | 否 | 合集，通过 `xiaohongshu/getCollectionList` 获取 |

**最小参数校验示例：**

```json
{ "title": "示例视频", "desc": "", "videoPath": "/tmp/video.mp4", "coverPath": "/tmp/cover.jpg", "timing": 0, "taskId": "task-1" }
```

### 图文 params

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `desc` / `title` | string | 否 | 描述 / 图文标题 |
| `images` | string[] | 否 | 本地图片路径 |
| `taskId` | string | 否（运行时必传） | 任务 ID |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布 |
| `visibilityType` | `0 \| 1 \| 4` | 否 | 公开 / 私密 / 仅互关好友可见 |
| `topics` / `mentions` / `location` | 与视频同名字段类型相同 | 否 | 分别通过 `xiaohongshu/getTopic`、`xiaohongshu/getFriend`、`xiaohongshu/getLocation` 获取 |
| `userDeclarationBind` / `originalStatement` | 与视频同名字段类型相同 | 否 | 内容声明 / 原创声明，约束相同 |
| `goods` / `goodsEntranceType` / `collection` | 与视频同名字段类型相同 | 否 | 商品先调用 `xiaohongshu/getGoodsPermission`、再调用 `xiaohongshu/getGoodsList`；合集通过 `xiaohongshu/getCollectionList` 获取；仅 `collection` 可为 `null` |

**最小参数校验示例：**

```json
{ "desc": "示例图文", "images": ["/tmp/image.jpg"], "timing": 0, "taskId": "task-1" }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/xiaohongshu/`

### 数据分析

#### getDataOverview

获取小红书数据概览。

```http
POST /galic/v1/platform/xiaohongshu/getDataOverview
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

**响应:** 返回小红书账号的数据概览，包含7天和30天的数据统计，包括浏览量、点赞数、评论数、分享数、收藏数、弹幕数、新增粉丝数等各项指标，以及按时间序列的数据列表和分析信息
---

#### getSingleDataOverview

获取小红书单个作品数据概览。

```http
POST /galic/v1/platform/xiaohongshu/getSingleDataOverview
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

**响应:** 返回小红书单个作品的详细数据概览，包括笔记基本信息、数据统计（浏览量、点赞数、评论数、分享数、收藏数等）、按天/小时统计的各项数据趋势和分析信息
---

#### getFansPortrait

获取小红书用户画像。

```http
POST /galic/v1/platform/xiaohongshu/getFansPortrait
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

**响应:** 返回小红书账号的用户画像数据，包括性别分布、年龄分布、城市分布和兴趣分布等维度数据
---

#### getClassicTopics

获取小红书经典话题。

```http
POST /galic/v1/platform/xiaohongshu/getClassicTopics
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

**响应:** 返回经典话题列表，按分类（如美食、美妆、时尚）展示，含话题标题、参与数、浏览量及关联笔记、用户等
---

#### getCreateGuidance

获取小红书官方课程列表。

```http
POST /galic/v1/platform/xiaohongshu/getCreateGuidance
```

**请求体:**
```json
{
  "accountArgs": {},
  "page": 0,
  "page_size": 0,
  "type": null
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `page` (number) - 页码，默认 1
- `page_size` (number) - 每页条数，默认 6
- `type` (any) - 分类：1 官方课程 2 新手入门 3 账号运营 4 内容创作 5 变现指南

**响应:** 返回创作学院官方课程列表，每条含 note_id、标题、封面图、链接、作者头像与昵称、学习人数（view_count/display_count_text）等；支持按分类与分页请求
---

#### getNoteAnalyzeList

获取小红书笔记分析列表数据。

```http
POST /galic/v1/platform/xiaohongshu/getNoteAnalyzeList
```

**请求体:**
```json
{
  "accountArgs": {},
  "type": null,
  "page_size": 0,
  "page_num": 0,
  "post_begin_time": 0,
  "post_end_time": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `type` (any) - 类型：0 全部 1 图文 2 视频
- `page_size` (number) - 每页条数
- `page_num` (number) - 页码，从 1 开始
- `post_begin_time` (number) - 发布开始时间（毫秒时间戳）
- `post_end_time` (number) - 发布结束时间（毫秒时间戳）

**响应:** 返回数据中心笔记分析列表与总数，每条笔记含阅读、点赞、评论、分享、收藏、曝光、涨粉、发布时间、审核状态等指标
---

#### getAudienceSourceAccount

获取小红书观众来源。

```http
POST /galic/v1/platform/xiaohongshu/getAudienceSourceAccount
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

**响应:** 返回近 7 天与近 30 天的观众来源分布列表及对应时间范围，每条为来源名称与占比
---

#### getAudienceViewPeriods

获取小红书观众观看时段。

```http
POST /galic/v1/platform/xiaohongshu/getAudienceViewPeriods
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

**响应:** 返回近 7 天与近 30 天的观众查看时段分布，每套为各时段的观看人数统计
---

#### getActivityCenterList

获取小红书活动中心列表。

```http
POST /galic/v1/platform/xiaohongshu/getActivityCenterList
```

**请求体:**
```json
{
  "accountArgs": {},
  "sort": null,
  "type": null,
  "source": 0,
  "topic_activity": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `sort` (any) - sort：1 默认排序 2 最新排序
- `type` (any) - type：1 全部活动 2 我的收藏
- `source` (number) - source
- `topic_activity` (number) - topic_activity

**响应:** 返回可参与的活动列表及收藏总数，每条活动包含名称、关联话题、时间范围、封面与链接等
---

#### getLeaderboardRecommend

获取小红书成长榜样榜单。

```http
POST /galic/v1/platform/xiaohongshu/getLeaderboardRecommend
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

**响应:** 返回同领域创作者推荐榜单，每条含创作者信息及其代表笔记的简要数据
---

### 发布辅助

#### getFriend

获取小红书好友列表。

```http
POST /galic/v1/platform/xiaohongshu/getFriend
```

**请求体:**
```json
{
  "accountArgs": {},
  "keyword": "string",
  "page": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `keyword` (string) - 搜索关键词
- `page` (number) - 页码

**响应:** 返回小红书好友列表，支持关键词搜索与分页
---

#### getLocation

获取小红书位置列表。

```http
POST /galic/v1/platform/xiaohongshu/getLocation
```

**请求体:**
```json
{
  "accountArgs": {},
  "keyword": "string",
  "page": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `keyword` (string) - 搜索关键词
- `page` (number) - 页码

**响应:** 根据关键词搜索小红书位置列表
---

#### getTopic

获取小红书话题列表。

```http
POST /galic/v1/platform/xiaohongshu/getTopic
```

**请求体:**
```json
{
  "accountArgs": {},
  "keyword": "string",
  "page": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `keyword` (string) - 搜索关键词
- `page` (number) - 页码

**响应:** 根据关键词搜索小红书话题列表
---

#### getNoteList

获取小红书笔记列表。

```http
POST /galic/v1/platform/xiaohongshu/getNoteList
```

**请求体:**
```json
{
  "accountArgs": {},
  "tab": "string",
  "page": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `tab` (string) - 标签ID，默认1
- `page` (number) - 页码，从0开始

**响应:** 返回小红书笔记列表，支持标签与分页
---

#### getGoodsPermission

获取小红书商品挂车权限。

```http
POST /galic/v1/platform/xiaohongshu/getGoodsPermission
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

**响应:** 返回账号可用的商品挂车权限列表，包含入口编号、发布类型标识、最大可绑定商品数、商品子类型等
---

#### getGoodsList

获取小红书商品列表/搜索。

```http
POST /galic/v1/platform/xiaohongshu/getGoodsList
```

**请求体:**
```json
{
  "accountArgs": {},
  "goods_option_type": "goods_seller",
  "keyword": "string",
  "page_num": 0,
  "tab_type": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `goods_option_type` (`goods_seller` \| `buyable_note_goods`) **必填** - 商品来源类型
- `keyword` (string) **必填** - 搜索关键词
- `page_num` (number) **必填** - 页码，从1开始
- `tab_type` (number) **必填** - Tab 类型

**响应:** 根据商品来源类型和关键词搜索商品列表，返回商品ID、名称、价格、主图、库存等信息
---

#### getCollectionList

获取小红书合集列表。

```http
POST /galic/v1/platform/xiaohongshu/getCollectionList
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

**响应:** 返回当前账号发布时可选择的小红书合集列表，包含合集 ID、名称、类型和笔记数量等信息
---

