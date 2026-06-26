---
name: crebee-social-media-gateway
description: |
  CreBee 社交媒体网关。当用户需要管理社交媒体账号、发布内容（视频/图文/文章）、获取数据分析、访问粉丝画像、搜索话题/活动/音乐、或与抖音、B站、小红书、快手等 12 个平台交互时触发此技能。适用于 AI Agent 自动化管理中国社交媒体平台运营。

  触发场景：
  - 发布内容到社交媒体平台
  - 获取账号列表或账号信息
  - 查询分析数据、数据概览、表现指标
  - 访问粉丝/观众画像
  - 搜索话题、标签、音乐、活动
  - 管理抖音、B站、小红书、快手等平台的内容
---

# [CreBee 社交媒体网关](https://www.crebee.cn)

统一 HTTP API 网关，让 AI Agent 自动化管理 12 个中国主流社交媒体平台。欢迎访问官网 https://www.crebee.cn 下载试用。

## 快速参考

| 属性         | 值                      |
| ------------ | ----------------------- |
| Base URL     | `http://127.0.0.1:3456` |
| API 前缀     | `/galic/v1`             |
| 认证方式     | Bearer Token (JWT)      |
| 请求方法     | 所有 API 使用 `POST`    |
| Content-Type | `application/json`      |

## 认证

所有 API 请求需要在 Authorization 头中携带 Bearer token。

**步骤 1：获取 Token**

```http
POST /galic/v1/auth/token
```

响应：

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2025-01-28T00:00:00.000Z",
  "createdAt": "2025-01-21T00:00:00.000Z"
}
```

> **提示**：Token 创建后可长期使用，无需在每次调用接口前都重新创建。仅在 token 过期（见响应中的 `expiresAt`）或返回 401 时再重新获取即可。

**步骤 2：在所有请求中使用 Token**

```http
POST /galic/v1/account/getAll
Authorization: Bearer <token>
Content-Type: application/json
```

## 通用约定

### 账号标识

大多数平台 API 需要指定操作哪个账号：

```json
{
  "accountArgs": {
    "accountID": "string",
    "appAlias": "string"
  }
}
```

- `accountID`：账号唯一标识（从 `account/getAll` 获取）
- `appAlias`：平台标识（如 `douyin`、`bilibili`、`xiaohongshu`）

**最佳实践**：先调用 `account/getAll` 获取可用账号列表及其 ID。

### 日期参数

当 API 需要日期范围时（如 `startDate`、`endDate`）：

- 使用 ISO 8601 日期字符串：`"2025-01-21"` 或 `"2025-01-21T00:00:00.000Z"`
- 时间间隔通常使用 Unix 时间戳(秒)

### 分页

许多列表 API 使用游标分页：

```json
{
  "cursor": "0",
  "count": 20
}
```

## 核心 API

### 账号管理

| 端点                            | 说明                         |
| ------------------------------- | ---------------------------- |
| `POST /galic/v1/account/getAll` | 获取所有已登录的社交媒体账号 |

### 内容发布

| 端点                                         | 说明                                     |
| -------------------------------------------- | ---------------------------------------- |
| `POST /galic/v1/platform/publish/batch`      | 批量发布内容（视频/图文/文章）到多个平台 |
| `POST /galic/v1/platform/publish/cancelTask` | 取消排队中的发布任务                     |

**支持的内容类型:**

- **视频 (video)**: 抖音、B站、快手、视频号、小红书、知乎、微博、百家号、头条号、企鹅号、网易号
- **图文 (image)**: 抖音、知乎、小红书、快手、头条号、视频号
- **文章 (article)**: 抖音、知乎、B站、百家号、头条号、公众号

> 发布支持实时进度追踪（WebSocket/SSE）、定时发布、平台特定参数配置。详见 `references/publishing.md`。

#### 批量发布请求结构

```json
{
  "contentType": "video | image | article",
  "commonForm": {
    /* 公共参数，见下方 */
  },
  "tasks": [
    {
      "taskId": "唯一任务ID（由调用方生成）",
      "accountId": "账号ID",
      "platform": "平台标识",
      "contentType": "video | image | article",
      "params": {
        /* 平台特定参数 */
      }
    }
  ]
}
```

#### 视频公共参数 (commonForm)

| 字段        | 类型   | 必填 | 说明                                 |
| ----------- | ------ | ---- | ------------------------------------ |
| `title`     | string | 是   | 视频标题                             |
| `desc`      | string | 是   | 视频描述                             |
| `videoPath` | string | 是   | 视频文件本地路径                     |
| `coverPath` | string | 是   | 封面图片本地路径                     |
| `timing`    | number | 否   | 定时发布时间戳（秒），0 表示立即发布 |

#### 图文公共参数 (commonForm)

| 字段     | 类型     | 必填 | 说明             |
| -------- | -------- | ---- | ---------------- |
| `desc`   | string   | 否   | 图文描述         |
| `images` | string[] | 否   | 图片本地路径列表 |

#### 文章公共参数 (commonForm)

| 字段      | 类型     | 必填 | 说明             |
| --------- | -------- | ---- | ---------------- |
| `title`   | string   | 否   | 文章标题         |
| `content` | string   | 否   | 文章内容（HTML） |
| `covers`  | string[] | 否   | 封面图片路径列表 |

#### 发布示例：批量发布视频到多个平台

```http
POST /galic/v1/platform/publish/batch
Authorization: Bearer <token>
Content-Type: application/json

{
  "contentType": "video",
  "commonForm": {
    "title": "我的第一个视频",
    "desc": "这是一个测试视频的描述",
    "videoPath": "/Users/demo/videos/test.mp4",
    "coverPath": "/Users/demo/videos/cover.jpg",
    "timing": 0
  },
  "tasks": [
    {
      "taskId": "douyin-1706044800-abc123",
      "accountId": "douyin_account_123",
      "platform": "douyin",
      "contentType": "video",
      "params": {
        "visibilityType": 0,
        "allowDownload": 1
      }
    },
    {
      "taskId": "bilibili-1706044800-def456",
      "accountId": "bilibili_account_456",
      "platform": "bilibili",
      "contentType": "video",
      "params": {
        "tid": { "fenqu_id": 160, "fenqu_name": "生活" },
        "copyright": 1,
        "tags": ["日常", "生活"],
        "pubType": 1
      }
    }
  ]
}
```

**响应:**

```json
{
  "total": 2,
  "success": 2,
  "failed": 0,
  "results": [
    { "accountId": "douyin_account_123", "platform": "douyin", "status": "success" },
    { "accountId": "bilibili_account_456", "platform": "bilibili", "status": "success" }
  ]
}
```

> **重要**: `taskId` 由调用方生成，用于关联 WebSocket/SSE 进度回调。建议格式：`{platform}-{timestamp}-{random}`。

#### 取消发布任务

```http
POST /galic/v1/platform/publish/cancelTask
Authorization: Bearer <token>
Content-Type: application/json

{
  "taskId": "douyin-1706044800-abc123"
}
```

### 发布记录

| 端点                                                      | 说明                               |
| --------------------------------------------------------- | ---------------------------------- |
| `POST /galic/v1/publish-record/get-global-publish-record` | 按账号和时间范围获取平台的发布记录 |

#### 请求参数

| 字段        | 类型   | 必填 | 说明             |
| ----------- | ------ | ---- | ---------------- |
| `account`   | object | 是   | 账号信息         |
| `startTime` | number | 是   | 开始时间戳（秒） |
| `endTime`   | number | 是   | 结束时间戳（秒） |

**account 结构:**

| 字段               | 类型   | 说明     |
| ------------------ | ------ | -------- |
| `account_id`       | string | 账户 ID  |
| `account_platform` | string | 平台类型 |

#### 请求示例

```http
POST /galic/v1/publish-record/get-global-publish-record
Authorization: Bearer <token>
Content-Type: application/json

{
  "account": {
    "account_id": "douyin_account_123",
    "account_platform": "douyin"
  },
  "startTime": 1705968000,
  "endTime": 1706227200
}
```

**响应:**

```json
[
  {
    "id": 1,
    "account_id": "douyin_account_123",
    "platform": "douyin",
    "content_type": "video",
    "title": "视频标题",
    "publish_status": "success",
    "publish_result_data": "{\"playCount\":1000,\"likeCount\":50,\"completePlayRate\":0.75}",
    "published_at": "2025-01-23T10:00:00.000Z",
    "account": {
      "account_id": "douyin_account_123",
      "account_platform": "douyin"
    }
  }
]
```

> **注意**: `publish_result_data` 是 JSON 字符串，包含平台特定指标（如完播率、2s 跳出率等），需解析后使用。

## 支持的平台

| 平台   | appAlias       | 主要能力                                                         |
| ------ | -------------- | ---------------------------------------------------------------- |
| 抖音   | `douyin`       | 数据分析、粉丝画像、话题、音乐、活动、热点、创意洞察、创作者活动 |
| B站    | `bilibili`     | 数据分析、投稿管理、评论、弹幕、收益、粉丝画像/趋势/排行         |
| 小红书 | `xiaohongshu`  | 数据分析、笔记、话题、位置、粉丝画像、观众来源/时段、活动中心    |
| 快手   | `kuaishou`     | 数据分析、粉丝画像、话题、活动、热点、音乐、创作灵感             |
| 微博   | `weibo`        | 数据分析、数据图表、话题、分类、素材中心                         |
| 公众号 | `gongzhonghao` | 数据分析、数据图表、单篇分析、用户画像                           |
| 百家号 | `baijiahao`    | 数据分析、话题、活动、分类、合集、热点、任务、投稿建议           |
| 头条号 | `toutiaohao`   | 数据分析、粉丝画像、话题、用户、位置、合集、活动                 |
| 企鹅号 | `qiehao`       | 数据分析、数据图表、单内容分析、分类                             |
| 网易号 | `wangyihao`    | 数据分析、数据图表、单内容分析、分类、热门话题、活动             |
| 视频号 | `shipinhao`    | 数据分析、粉丝画像、好友、位置、活动、合集、音乐                 |
| 知乎   | `zhihu`        | 数据分析、话题、分类、博主排行、优秀答主、问题推荐、热词热题     |

## 平台详细文档

各平台 API 的详细参数和响应说明，请阅读对应的参考文件：

- `references/platforms/douyin.md` - 抖音 API（29 个端点）
- `references/platforms/bilibili.md` - B站 API（27 个端点）
- `references/platforms/xiaohongshu.md` - 小红书 API（14 个端点）
- `references/platforms/kuaishou.md` - 快手 API（17 个端点）
- `references/platforms/weibo.md` - 微博 API（8 个端点）
- `references/platforms/gongzhonghao.md` - 公众号 API（4 个端点）
- `references/platforms/baijiahao.md` - 百家号 API（14 个端点）
- `references/platforms/toutiaohao.md` - 头条号 API（11 个端点）
- `references/platforms/qiehao.md` - 企鹅号 API（5 个端点）
- `references/platforms/wangyihao.md` - 网易号 API（8 个端点）
- `references/platforms/shipinhao.md` - 视频号 API（9 个端点）
- `references/platforms/zhihu.md` - 知乎 API（15 个端点）

## 典型工作流

1. **获取认证 Token**

   ```
   POST /galic/v1/auth/token
   ```

2. **获取可用账号**

   ```
   POST /galic/v1/account/getAll
   Authorization: Bearer <token>
   Body: {}
   ```

   > ⚠️ 注意：必须传递 body，即使没有参数也要传空对象 `{}`，否则请求可能失败。

3. **选择账号和平台**
   从账号列表中记录 `account_id` 和 `account_platform`

4. **调用平台 API**

   ```http
   POST /galic/v1/platform/douyin/getDataOverview
   Authorization: Bearer <token>
   Content-Type: application/json

   {
     "accountArgs": {
       "accountID": "<account_id>",
       "appAlias": "douyin"
     },
     "startDate": "2025-01-21",
     "endDate": "2025-01-28"
   }
   ```

## 错误处理

所有 API 返回标准 HTTP 状态码：

- `200` - 成功
- `400` - 请求参数错误
- `401` - 未授权（缺少或无效的 token）
- `500` - 服务器内部错误

错误响应格式：

```json
{
  "code": 400,
  "raw": null,
  "message": "详细错误信息"
}
```
