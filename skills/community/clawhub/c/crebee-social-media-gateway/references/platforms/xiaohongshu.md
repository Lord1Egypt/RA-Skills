# 小红书 API

小红书是中国领先的生活方式分享平台。API 提供数据分析、笔记管理、话题搜索、粉丝画像、活动中心等功能的访问。

## 发布参数

> 标题限制：小红书视频和图文的标题均限制在 **20字** 以内。

### 视频 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 视频标题（**≤20字**） |
| `desc` | string | 否 | - | 视频描述（≤1000字） |
| `videoPath` | string | **是** | - | 视频文件本地绝对路径 |
| `coverPath` | string | **是** | - | 封面路径 |
| `timing` | number | **是** | `0` | 定时时间戳，0立即发布，范围：1小时后~14天内 |
| `taskId` | string | **是** | - | 任务ID |
| `visibilityType` | number | 否 | `0` | 可见性：0-公开，1-私密，4-仅互关好友可见 |
| `topics` | array | 否 | `[]` | 话题列表，通过 `xiaohongshu/getTopic` 获取，格式：`[{ topic_id, topic_name, topic_link, topic_view_count }]` |
| `mentions` | array | 否 | `[]` | @用户列表（≤20个），通过 `xiaohongshu/getFriend` 获取 |
| `location` | object\|null | 否 | `null` | 位置信息，通过 `xiaohongshu/getLocation` 获取 |

**最小可用示例：**
```json
{ "title": "...(≤20字)", "desc": "", "videoPath": "...", "coverPath": "...", "timing": 0, "taskId": "...", "visibilityType": 0, "topics": [], "mentions": [], "location": null }
```

### 图文 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 图文标题（**≤20字**） |
| `desc` | string | 否 | - | 描述（≤1000字） |
| `images` | string[] | 否 | - | 图片路径列表（至少1张） |
| `taskId` | string | **是** | - | 任务ID |
| `visibilityType` | number | 否 | `0` | 可见性：0-公开，1-私密，4-仅互关好友可见 |
| `timing` | number | 否 | `0` | 定时时间戳，0立即发布，范围：1小时后~14天内 |
| `topics` | array | 否 | `[]` | 话题列表 |
| `mentions` | array | 否 | `[]` | @用户列表（≤20个） |
| `location` | object\|null | 否 | `null` | 位置信息 |
| `userDeclarationBind` | object | 否 | - | 内容声明：`{ origin: 1\|2\|3 }`（1-虚构演绎，2-AI合成，3-已自主标记） |

**最小可用示例：**
```json
{ "title": "...(≤20字)", "desc": "", "images": ["..."], "timing": 0, "taskId": "...", "visibilityType": 0, "topics": [], "mentions": [], "location": null }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/xiaohongshu/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

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

### 粉丝画像

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

### 投稿管理

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

### 热门内容

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

### 创作工具

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

### 活动任务

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

