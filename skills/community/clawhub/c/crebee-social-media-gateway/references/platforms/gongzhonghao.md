# 公众号 API

微信公众号是腾讯的内容创作平台。API 提供数据分析、用户画像、图文发布等功能的访问。

## 发布参数

> platform 标识为 `gongzhonghao_official`（含下划线）。

### 文章 params

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `title` | string | 否 | - | 标题（≤32字） |
| `content` | string | 否 | - | 正文（≤20000字） |
| `covers` | string[] | 否 | - | 封面图路径列表（仅1张） |
| `taskId` | string | **是** | - | 任务ID |
| `pubType` | number | 否 | `1` | 发布类型：1-立即发布，0-存草稿 |
| `author` | string | 否 | - | 作者（≤16字） |
| `digest` | string | 否 | - | 摘要（≤128字） |
| `content_source_url` | string | 否 | - | 原文链接（有效URL） |
| `need_open_comment` | number | 否 | `0` | 是否开启评论：0-不开启，1-开启 |
| `only_fans_can_comment` | number | 否 | `0` | 是否仅粉丝可评论：0-所有人，1-仅粉丝 |

**最小可用示例：**
```json
{ "title": "...", "content": "<p>...</p>", "covers": [], "taskId": "...", "pubType": 1, "author": "", "digest": "", "need_open_comment": 0, "only_fans_can_comment": 0 }
```

## 接口调用

**端点前缀**: `/galic/v1/platform/gongzhonghao/`

所有请求需要：
- `Authorization: Bearer <token>` 请求头
- `Content-Type: application/json`
- 请求体中的 `accountArgs`

### 数据分析

#### getGongzhonghaoDataOverview

获取公众号数据概览。

```http
POST /galic/v1/platform/gongzhonghao/getGongzhonghaoDataOverview
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

**响应:** 返回公众号账号的数据概览，包括阅读量、分享、点赞、收藏（在看）、评论等各项指标的统计，支持当日、近7天、近30天三个时间范围的数据
---

#### getGongzhonghaoDataGraph

获取公众号数据图表。

```http
POST /galic/v1/platform/gongzhonghao/getGongzhonghaoDataGraph
```

**请求体:**
```json
{
  "accountArgs": {},
  "beginTimestamp": 0,
  "endTimestamp": 0
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `beginTimestamp` (number) **必填** - 开始时间戳（秒级）
- `endTimestamp` (number) **必填** - 结束时间戳（秒级）

**响应:** 返回公众号账号在指定时间范围内的数据图表数据，包括文章趋势统计和文章来源统计，支持按场景（服务号消息、聊天、朋友圈、搜一搜等）分类查看
---

#### getGongzhonghaoSingleDataOverview

获取公众号单个发布记录数据概览。

```http
POST /galic/v1/platform/gongzhonghao/getGongzhonghaoSingleDataOverview
```

**请求体:**
```json
{
  "accountArgs": {},
  "msgid": "string",
  "publish_date": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `msgid` (string) **必填** - 消息ID
- `publish_date` (string) **必填** - 发布日期（格式：YYYY-MM-DD）

**响应:** 返回公众号单个发布记录的详细数据概览，包括文章数据（标题、阅读时长、完读率等）、文章摘要数据（阅读趋势）、详细数据（用户画像：年龄、性别、地域分布）
---

### 粉丝画像

#### getUserPortrait

获取公众号用户画像。

```http
POST /galic/v1/platform/gongzhonghao/getUserPortrait
```

**请求体:**
```json
{
  "accountArgs": {},
  "beginDate": "string",
  "endDate": "string"
}
```

**参数说明:**
- `accountArgs` (object) **必填** - 账号参数
  - `appAlias` (string) **必填** - 平台标识 对应平台表的account_platform字段 如douyin等
  - `accountID` (string) **必填** - 账号ID 对应账号表的account_id字段
- `beginDate` (string) **必填** - 开始日期（格式：YYYY-MM-DD）
- `endDate` (string) **必填** - 结束日期（格式：YYYY-MM-DD）

**响应:** 返回公众号账号在指定时间范围内的用户画像数据，包括性别分布、语言分布、地区分布、平台分布、设备分布、年龄分布等维度数据
---

