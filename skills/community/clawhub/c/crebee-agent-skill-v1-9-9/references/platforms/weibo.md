# 微博 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。`params.taskId` 虽是 Zod 可选字段，仍应传入以支持发布状态回调。

### 视频 params

| 字段 | 类型 | Zod 必填 | 说明 |
|------|------|----------|------|
| `title` | string | 是 | 标题 |
| `desc` | string | 否 | 描述，可为空字符串 |
| `videoPath` | string | 是 | 本地视频路径 |
| `coverPath` | string | 是 | 封面路径 |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布，定时发布在当前时间至 7 天内且为 VIP 功能 |
| `taskId` | string | 否 | 发布状态回调任务 ID |
| `videoInfo` | `{ duration, width, height, size, thumbnail? }` | 否 | 视频校验信息 |
| `createType` | number | 否 | 业务约定：`0` 原创、`1` 转载、`2` 二创 |
| `mblogStatement` | `0` \| `4` \| `3` \| `1` \| `2` | 否 | `0` 无、`4` 自主创作、`3` 转载、`1` AI 生成、`2` 虚构演绎 |
| `topics` | string[] | 否 | 话题数组，通过 `weibo/getTopicList` 获取后取 `topic_name` |
| `location` | string | 否 | 位置信息 |
| `visibleType` | `0` \| `10` \| `6` \| `1` \| `5` | 否 | `0` 公开、`10` 粉丝、`6` 好友圈、`1` 仅自己、`5` 群可见 |
| `category` | `{ value: string, label: string, children: { value: string, label: string }[] }` | 否 | 分类信息，通过 `weibo/getCategoryList` 获取 |

**最小参数校验示例：**
```json
{
  "title": "微博视频示例",
  "videoPath": "/tmp/video.mp4",
  "coverPath": "/tmp/cover.jpg",
  "timing": 0,
  "taskId": "task-1"
}
```

## 接口调用

**端点前缀**: `/galic/v1/platform/weibo/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
- `X-CreBee-Source: skill` 请求头（仅 Skill 直接调用）
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

### 数据分析

#### getDataGraph

获取微博数据图表。

```http
POST /galic/v1/platform/weibo/getDataGraph
```

**请求体:**
```json
{
  "accountArgs": {},
  "period": null,
  "item_subtype": "upload_count"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `period` (any) **必填** - 周期：近7日或近30日
- `item_subtype` (`upload_count` \| `play_count` \| `play_dura_count` \| `reposts_count` \| `comments_count` \| `attitudes_count`) **必填** - 数据子类型

**响应:** 返回微博账号在指定周期内的数据图表数据，支持多种数据子类型（发布量、播放量、播放时长、转发数、评论数、点赞数）
---

#### getDataOverview

获取微博账号数据概览。

```http
POST /galic/v1/platform/weibo/getDataOverview
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

**响应:** 返回微博账号的数据概览，包含近7日和近30日两个周期的各项指标数据
---

#### getSingleDataOverview

获取微博单个内容数据概览。

```http
POST /galic/v1/platform/weibo/getSingleDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "type": "play"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 内容ID
- `type` (`play` \| `interaction`) **必填** - 数据类型：播放数据或互动数据

**响应:** 返回微博单个内容的详细数据概览，支持播放数据和互动数据两种类型。播放数据包括总播放量、播放时长、完播率等；互动数据包括转发数、评论数、点赞数等
---

#### getSingleDataGraph

获取微博单个内容数据图表。

```http
POST /galic/v1/platform/weibo/getSingleDataGraph
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
- `postId` (string) **必填** - 内容ID

**响应:** 返回微博单个内容发布后7天的数据图表数据，包括播放量、转发数、评论数、点赞数等各项指标
---

#### getSingleDataCompletion

获取微博单个内容播放留存率。

```http
POST /galic/v1/platform/weibo/getSingleDataCompletion
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
- `postId` (string) **必填** - 内容ID

**响应:** 返回微博单个内容的播放留存率数据，包括自己的留存率数据和同类平均留存率数据
---

### 发布辅助

#### getTopicList

获取微博话题列表。

```http
POST /galic/v1/platform/weibo/getTopicList
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

**响应:** 根据关键词搜索微博话题列表
---

#### getCategoryList

获取微博分类列表。

```http
POST /galic/v1/platform/weibo/getCategoryList
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

**响应:** 返回微博分类列表，含主分类与子分类
---

#### getMaterialLabelsThenList

获取微博素材中心（先拉类别再拉素材列表）。

```http
POST /galic/v1/platform/weibo/getMaterialLabelsThenList
```

**请求体:**
```json
{
  "accountArgs": {},
  "labelId": "string",
  "cursor": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `labelId` (string) - 素材类别 id，不传则用首个类别
- `cursor` (string) - 游标，首次不传或 "0"

**响应:** 先拉取素材类别 id，再拉取该类别下的素材视频列表
---

