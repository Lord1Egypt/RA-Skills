# 公众号 API

## 发布参数

以下 JSON 是 batch 请求中的 `tasks[].params`。平台标识为 `gongzhonghao_official`。`tasks[].taskId` 是批量发布的必填回调 ID；`params.taskId` 为兼容现有发布链路保留。可选字段无值时省略，不传 `null`。

### 文章 params

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | **是** | 标题，不超过 32 字 |
| `content` | string | **是** | HTML 正文，少于 2 万字符；正文图片不超过 1 MB |
| `covers` | string[] | **是** | 封面本地路径；实际发布仅使用 1 张，比例为 2.35:1 或 1:1 |
| `taskId` | string | 否 | 与 `tasks[].taskId` 保持一致 |
| `author` | string | 否 | 作者，最多 16 字 |
| `digest` | string | 否 | 摘要，最多 128 字；省略时平台从正文提取 |
| `content_source_url` | string | 否 | 原文地址 |
| `need_open_comment` | `0 \| 1` | 否 | 是否开启评论 |
| `only_fans_can_comment` | `0 \| 1` | 否 | 是否仅粉丝可评论 |
| `pubType` | number | 否 | `1` 立即发布，`0` 仅创建草稿 |

**最小参数校验示例：**

```json
{
  "title": "文章标题",
  "content": "<p>正文</p>",
  "covers": ["/tmp/cover.jpg"],
  "taskId": "task-1"
}
```

## 接口调用

**端点前缀**: `/galic/v1/platform/gongzhonghao/`

所有请求需要：

- `Authorization: Bearer <token>` 请求头
- `X-CreBee-Source: skill` 请求头（仅 Skill 直接调用）
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

