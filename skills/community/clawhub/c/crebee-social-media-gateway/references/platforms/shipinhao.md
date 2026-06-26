# 视频号 API

微信视频号是微信的短视频平台。API 提供数据分析、粉丝画像、社交功能、音乐管理等功能的访问。

## 发布参数

> `topics` 为**字符串数组**（如 `["旅行", "美食"]`），不是对象数组。

### 视频 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 视频标题 |
| `desc` | string | 否 | - | 视频描述（≤1000字） |
| `videoPath` | string | **是** | - | 视频文件本地绝对路径 |
| `coverPath` | string | **是** | - | 封面路径 |
| `timing` | number | 否 | `0` | 定时时间戳，0立即发布，范围：当前时间~1个月内 |
| `taskId` | string | **是** | - | 任务ID |
| `shortTitle` | string | 否 | `""` | 短标题（如填写需6-16字） |
| `topics` | string[] | 否 | `[]` | 话题列表（**字符串数组**，非对象） |
| `mentions` | array | 否 | `[]` | @视频号用户列表（≤10个） |
| `location` | object\|null | 否 | `null` | 位置信息 |
| `activity` | object\|null | 否 | `null` | 关联活动 |
| `collection` | object\|null | 否 | `null` | 合集信息 |
| `postFlag` | number | 否 | `0` | 原创标识：0-非原创，1-原创 |
| `pubType` | number | 否 | `1` | 发布类型：1-立即发布，0-存草稿 |
| `objectType` | number | 否 | `0` | 新闻动态（仅媒体认证账号有效）：0-不设置，1-设为新闻动态 |
| `cover43` | string | 否 | - | 4:3横版封面路径 |

**最小可用示例：**
```json
{ "title": "...", "desc": "", "videoPath": "...", "coverPath": "...", "timing": 0, "taskId": "...", "shortTitle": "", "topics": [], "mentions": [], "location": null, "activity": null, "collection": null, "postFlag": 0, "pubType": 1, "objectType": 0 }
```

### 图文 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 标题（1-22字） |
| `desc` | string | 否 | - | 描述（≤1000字） |
| `images` | string[] | 否 | - | 图片路径列表 |
| `taskId` | string | **是** | - | 任务ID |
| `timing` | number | 否 | `0` | 定时时间戳 |
| `topics` | string[] | 否 | `[]` | 话题列表（字符串数组） |
| `location` | object\|null | 否 | `null` | 位置信息 |
| `activity` | object\|null | 否 | `null` | 关联活动 |
| `collection` | object\|null | 否 | `null` | 合集信息 |
| `music` | object\|null | 否 | `null` | 背景音乐 |
| `pubType` | number | 否 | `1` | 发布类型：1-立即发布，0-存草稿 |
| `objectType` | number | 否 | `0` | 新闻动态标识 |

**最小可用示例：**
```json
{ "title": "...", "desc": "", "images": ["..."], "timing": 0, "taskId": "...", "topics": [], "location": null, "activity": null, "collection": null, "pubType": 1, "objectType": 0 }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/shipinhao/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
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

### 粉丝画像

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

### 投稿管理

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

### 其他

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

