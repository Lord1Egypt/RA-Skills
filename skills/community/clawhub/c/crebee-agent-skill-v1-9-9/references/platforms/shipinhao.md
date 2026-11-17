# 视频号 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。`params.taskId` 虽是 Zod 可选字段，仍应传入以支持发布状态回调。

### 视频 params

| 字段 | 类型 | Zod 必填 | 说明 |
|------|------|----------|------|
| `title` | string | 是 | 视频标题 |
| `desc` | string | 是 | 视频描述 |
| `videoPath` | string | 是 | 本地视频路径 |
| `coverPath` | string | 是 | 封面路径 |
| `timing` | number | 是 | 秒级时间戳；`0` 为立即发布，定时发布在当前时间至 1 个月内 |
| `taskId` | string | 否 | 发布状态回调任务 ID |
| `videoInfo` | `{ duration, width, height, size, thumbnail? }` | 否 | 视频校验信息 |
| `cover43` | string | 否 | 4:3 封面路径 |
| `mentions` | `{ friend_id, friend_avatar, friend_name }[]` | 否 | 提及用户，通过 `shipinhao/getFriend` 获取 |
| `location` | `{ position_id, position_name, position_address, position_city? } \| null` | 否 | 位置信息，通过 `shipinhao/getLocation` 获取 |
| `collection` | `{ collection_id, collection_name } \| null` | 否 | 合集信息，通过 `shipinhao/getCollection` 获取 |
| `activity` | `{ activity_id, activity_name, activity_creator? } \| null` | 否 | 关联活动，通过 `shipinhao/getActivity` 获取 |
| `topics` | string[] | 否 | 话题列表 |
| `link` | `{ url: string, title: string }` | 否 | 扩展链接 |
| `shortTitle` | string | 否 | 短标题 |
| `postFlag` | number | 否 | 业务约定：`0` 非原创、`1` 原创 |
| `pubType` | number | 否 | 业务约定：`1` 立即发布、`0` 草稿 |
| `objectType` | number | 是 | 业务约定：`0` 不设置、`1` 设为新闻动态 |

**最小参数校验示例：**
```json
{
  "title": "视频号示例",
  "desc": "示例描述",
  "videoPath": "/tmp/video.mp4",
  "coverPath": "/tmp/cover.jpg",
  "timing": 0,
  "taskId": "task-1",
  "objectType": 0
}
```

### 图文 params

| 字段 | 类型 | Zod 必填 | 说明 |
|------|------|----------|------|
| `desc` | string | 否 | 描述 |
| `images` | string[] | 否 | 图片路径；运行时至少需要一张 |
| `taskId` | string | 否 | 发布状态回调任务 ID |
| `title` | string | 否 | 图文标题 |
| `location` | `{ position_id, position_name, position_address, position_city? } \| null` | 否 | 位置信息，通过 `shipinhao/getLocation` 获取 |
| `collection` | `{ collection_id, collection_name } \| null` | 否 | 合集信息，通过 `shipinhao/getCollection` 获取 |
| `activity` | `{ activity_id, activity_name, activity_creator? } \| null` | 否 | 关联活动，通过 `shipinhao/getActivity` 获取 |
| `topics` | string[] | 否 | 话题列表 |
| `timing` | number | 否 | 秒级时间戳；`0` 为立即发布 |
| `pubType` | number | 否 | 业务约定：`1` 立即发布、`0` 草稿 |
| `objectType` | number | 否 | 业务约定：`0` 不设置、`1` 设为新闻动态 |

`music` 不在 `ShipinhaoPublishImageParamsSchema` 中，不能传入。

**最小参数校验示例：**
```json
{
  "images": ["/tmp/image.jpg"],
  "taskId": "task-1"
}
```

## 接口调用

**端点前缀**: `/galic/v1/platform/shipinhao/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
- `X-CreBee-Source: skill` 请求头（仅 Skill 直接调用）
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

### 数据分析

#### getDataOverview

获取视频号数据概览。

```http
POST /galic/v1/platform/shipinhao/getDataOverview
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
- `startDate` (string) **必填** - 开始日期
- `endDate` (string) **必填** - 结束日期

**响应:** 返回视频号账号在指定时间范围内的数据概览，包括浏览、点赞、评论、转发、收藏等指标及其趋势数据
---

#### getSingleDataOverview

获取视频号单个视频数据概览。

```http
POST /galic/v1/platform/shipinhao/getSingleDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "postId": "string",
  "startDate": "2025-01-21",
  "endDate": "2025-01-21"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `postId` (string) **必填** - 平台作品ID (publish_platform_post_id)
- `startDate` (string) **必填** - 开始日期
- `endDate` (string) **必填** - 结束日期

**响应:** 返回视频号单个视频的详细数据概览，包括播放、点赞、评论、转发、收藏等各项指标及其趋势数据
---

#### getFansPortrait

获取视频号用户画像数据。

```http
POST /galic/v1/platform/shipinhao/getFansPortrait
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

**响应:** 返回视频号账号的用户画像数据，包括年龄分布、性别分布、省份分布、城市分布、设备分布等
---

### 发布辅助

#### getFriend

获取视频号好友列表。

```http
POST /galic/v1/platform/shipinhao/getFriend
```

**请求体:**
```json
{
  "accountArgs": {},
  "key": "string",
  "cursor": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `key` (string) - 搜索关键词
- `cursor` (number) - 分页游标

**响应:** 返回视频号好友列表，支持关键词搜索与游标分页
---

#### getLocation

获取视频号位置列表。

```http
POST /galic/v1/platform/shipinhao/getLocation
```

**请求体:**
```json
{
  "accountArgs": {},
  "locationKey": "string",
  "cursor": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `locationKey` (string) - 位置搜索关键词
- `cursor` (number) - 分页游标

**响应:** 根据关键词搜索视频号位置列表
---

#### getActivity

获取视频号活动列表。

```http
POST /galic/v1/platform/shipinhao/getActivity
```

**请求体:**
```json
{
  "accountArgs": {},
  "query": "string",
  "cursor": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `query` (string) - 搜索关键词
- `cursor` (number) - 分页游标

**响应:** 返回视频号活动列表，支持搜索与游标分页
---

#### getCollection

获取视频号合集列表。

```http
POST /galic/v1/platform/shipinhao/getCollection
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

**响应:** 返回视频号合集列表
---

#### getMusicList

获取视频号音乐列表。

```http
POST /galic/v1/platform/shipinhao/getMusicList
```

**请求体:**
```json
{
  "accountArgs": {},
  "type": null,
  "query": "string",
  "pageSize": 0,
  "currentPage": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `type` (any) **必填** - 列表类型：103-推荐，3-收藏，104-搜索
- `query` (string) - 搜索关键词（type 为 104 时使用）
- `pageSize` (number) - 每页数量
- `currentPage` (number) - 当前页码，从 1 开始

**响应:** 返回视频号音乐列表，支持推荐(103)、收藏(3)、搜索(104),支持分页
---

#### getContentList

获取视频号内容列表。

```http
POST /galic/v1/platform/shipinhao/getContentList
```

**请求体:**
```json
{
  "accountArgs": {},
  "page": 0,
  "pageSize": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `page` (number) - 页码，从1开始
- `pageSize` (number) - 每页数量，默认20

**响应:** 返回视频号内容列表，支持分页
---

#### getNotificationList

获取视频号通知中心列表。

```http
POST /galic/v1/platform/shipinhao/getNotificationList
```

**请求体:**
```json
{
  "accountArgs": {},
  "pageSize": 0,
  "currentPage": 0,
  "reqType": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `pageSize` (number) - 每页数量，默认20
- `currentPage` (number) - 当前页，从1开始，默认1
- `reqType` (number) - 请求类型，默认1

**响应:** 返回视频号通知中心列表，包括作品优化建议、反馈进度、实名提醒等系统通知，支持分页
---

