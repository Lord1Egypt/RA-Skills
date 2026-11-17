# 内容发布指南

## 概述

CreBee 支持将内容（视频/图文/文章）批量发布到多个社交媒体平台。

**端点:**

- `POST /galic/v1/platform/publish/batch` - 批量发布内容
- `POST /galic/v1/platform/publish/cancelTask` - 取消队列中的任务

**各平台详细参数：** [抖音](./platforms/douyin.md) · [B站](./platforms/bilibili.md) · [小红书](./platforms/xiaohongshu.md) · [快手](./platforms/kuaishou.md) · [视频号](./platforms/shipinhao.md) · [知乎](./platforms/zhihu.md) · [微博](./platforms/weibo.md) · [百家号](./platforms/baijiahao.md) · [头条号](./platforms/toutiaohao.md) · [企鹅号](./platforms/qiehao.md) · [网易号](./platforms/wangyihao.md) · [公众号](./platforms/gongzhonghao.md) · [大鱼号](./platforms/dayuhao.md) · [搜狐号](./platforms/souhuhao.md) · [简书](./platforms/jianshu.md) · [CSDN](./platforms/csdn.md)

---

## 内容类型

| 类型 | contentType | 支持平台                                                                    |
| ---- | ----------- | --------------------------------------------------------------------------- |
| 视频 | `video`     | 抖音、B站、快手、视频号、小红书、知乎、微博、百家号、头条号、企鹅号、网易号、大鱼号 |
| 图文 | `image`     | 抖音、知乎、小红书、快手、头条号、视频号、百家号、搜狐号                          |
| 文章 | `article`   | 抖音、知乎、B站、百家号、头条号、公众号、简书、CSDN、搜狐号、大鱼号                 |

---

## 请求结构

接口在任务记录创建并入队后立即返回。响应中的 `success` / `failed` 仅表示任务创建状态，不会等待各平台实际发布完成。

```json
{
  "contentType": "video | image | article",
  "commonForm": {
    /* 公共基础信息，供参考 */
  },
  "tasks": [
    {
      "taskId": "唯一任务ID（调用方生成）",
      "accountId": "账号ID（从 account/getAll 获取）",
      "platform": "平台标识",
      "contentType": "video | image | article",
      "params": {
        /* 该平台完整发布参数 */
      }
    }
  ]
}
```

**核心设计：**

- `commonForm` 是公共模板/基础信息，供参考用
- `params` 是实际发送给平台的完整参数，不会自动合并 `commonForm`；具体必填项以“平台 + contentType”参数表为准
- 每个平台的 `params` 中各字段值可与 `commonForm` 不同，按该平台的约束独立填写（例如小红书标题限20字，需在其 params.title 中单独传截短后的标题）

---

## 公共字段

`commonForm` 中填写公共基础信息（不含 taskId），各平台 `params` 中需包含这些字段 + 平台特有字段 + `taskId`。

### 视频（commonForm）

| 字段        | 类型   | 必填   | 说明                             |
| ----------- | ------ | ------ | -------------------------------- |
| `title`     | string | **是** | 视频标题                         |
| `desc`      | string | **是** | 视频描述（可为空字符串）         |
| `videoPath` | string | **是** | 视频文件本地绝对路径             |
| `coverPath` | string | **是** | 封面图片本地绝对路径             |
| `timing`    | number | 否     | 定时秒级时间戳，`0` 表示立即发布 |

### 图文（commonForm）

| 字段     | 类型     | 必填 | 说明                             |
| -------- | -------- | ---- | -------------------------------- |
| `desc`   | string   | 否   | 图文描述                         |
| `images` | string[] | 否   | 图片本地路径列表                 |

### 文章（commonForm）

| 字段      | 类型     | 必填 | 说明                 |
| --------- | -------- | ---- | -------------------- |
| `title`   | string   | 否   | 文章标题             |
| `content` | string   | 否   | 文章正文（HTML格式） |
| `covers`  | string[] | 否   | 封面图片本地路径列表 |

---

## 各平台最小传参速查

> 以下 params 是可通过 batch 接口 Zod 校验的最小参数集合，`"..."` 处填入实际内容。真实发布还会受账号状态和平台运行时规则约束，需通过辅助接口获取的字段已注明。
>
> 可选字段没有值时直接省略，不要用 `null` 或 `undefined` 占位；只有平台参数表明确标注可空的字段才接受 `null`。

### 视频发布

**抖音 `douyin`**

```json
{
  "title": "...",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "..."
}
```

**B站 `bilibili`** — `tid` 通过 `bilibili/getVideoCategory` 获取；有 topic 时 tags 可为空

```json
{
  "title": "...",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "copyright": 1,
  "tid": { "fenqu_id": 160, "fenqu_name": "生活" },
  "source": "",
  "pubType": 1,
  "tags": ["标签1"]
}
```

**快手 `kuaishou`** — `visibilityType` 值：1公开 / 2私密 / 4好友

```json
{
  "title": "...",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "visibilityType": 1,
  "topics": [],
  "mentions": [],
  "activities": [],
  "allowSameFrame": 1,
  "allowDownload": 1,
  "nearbyShow": 0
}
```

**视频号 `shipinhao`** — `topics` 为字符串数组

```json
{
  "title": "...",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "shortTitle": "",
  "topics": [],
  "mentions": [],
  "location": null,
  "activity": null,
  "collection": null,
  "postFlag": 0,
  "pubType": 1,
  "objectType": 0
}
```

**小红书 `xiaohongshu`** — 标题限20字

```json
{
  "title": "...(≤20字)",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "visibilityType": 0,
  "topics": [],
  "mentions": []
}
```

**知乎 `zhihu`** — `topics` 通过 `zhihu/getTopic` 获取，`category` 通过 `zhihu/getCategory` 获取

```json
{
  "title": "...(5-50字)",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "isOriginal": 1,
  "topics": [{ "topic_id": "...", "topic_name": "..." }],
  "category": { "id": 1, "name": "...", "children": [] }
}
```

**微博 `weibo`**

```json
{
  "title": "...",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "createType": 0,
  "visibleType": 0,
  "topics": [],
  "location": ""
}
```

**百家号 `baijiahao`** — 当前只有作品描述，没有独立标题；手动封面可不传

```json
{
  "desc": "",
  "videoPath": "...",
  "coverPath": "",
  "timing": 0,
  "taskId": "...",
  "videoType": "horizontal",
  "pubType": 1,
  "publishStatement": 1,
  "publishStatementSub": 0
}
```

**头条号 `toutiaohao`** — 竖版不支持 desc/topics/timing

```json
{
  "title": "...",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "videoType": "horizontal",
  "visibilityType": 0,
  "pubType": 1,
  "topics": [],
  "externalLink": ""
}
```

**企鹅号 `qiehao`** — `category` 通过 `qiehao/getCategoryList` 获取；`topics` 至少2个

```json
{
  "title": "...(5-64字)",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "category": { "value": "...", "children": ["子分类"] },
  "topics": ["话题1", "话题2"],
  "pubType": 1
}
```

**网易号 `wangyihao`** — `category` 通过 `wangyihao/getCategoryList` 获取；`tags` 必须3-5个

```json
{
  "title": "...(5-30字)",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "category": { "value": "...", "children": [] },
  "tags": ["标签1", "标签2", "标签3"],
  "pubType": 1
}
```

**大鱼号 `dayuhao`**

```json
{
  "title": "...",
  "desc": "",
  "videoPath": "...",
  "coverPath": "...",
  "timing": 0,
  "taskId": "...",
  "category": "科技"
}
```

---

### 图文发布

**抖音 `douyin`**

```json
{
  "images": ["..."],
  "timing": 0,
  "taskId": "..."
}
```

**快手 `kuaishou`**

```json
{
  "desc": "",
  "images": ["..."],
  "timing": 0,
  "taskId": "...",
  "photoStatus": 1,
  "topics": [],
  "mentions": [],
  "activities": []
}
```

**视频号 `shipinhao`**

```json
{
  "title": "...",
  "desc": "",
  "images": ["..."],
  "timing": 0,
  "taskId": "...",
  "topics": [],
  "location": null,
  "activity": null,
  "collection": null,
  "pubType": 1,
  "objectType": 0
}
```

**小红书 `xiaohongshu`** — 标题限20字

```json
{
  "title": "...(≤20字)",
  "desc": "",
  "images": ["..."],
  "timing": 0,
  "taskId": "...",
  "visibilityType": 0,
  "topics": [],
  "mentions": []
}
```

**知乎 `zhihu`**

```json
{ "title": "...", "desc": "", "images": ["..."], "taskId": "...", "commentPermission": "all" }
```

**头条号 `toutiaohao`**

```json
{ "desc": "", "images": ["..."], "taskId": "..." }
```

**百家号 `baijiahao`**

```json
{ "desc": "...", "images": ["..."], "taskId": "...", "timing": 0 }
```

**搜狐号 `souhuhao`**

```json
{ "title": "...", "desc": "...", "images": ["..."], "taskId": "..." }
```

---

### 文章发布

**抖音 `douyin`**

```json
{
  "title": "...",
  "content": "<p>...</p>",
  "taskId": "...",
  "timing": 0
}
```

**B站 `bilibili`**

```json
{ "title": "...", "content": "<p>...</p>", "covers": [], "taskId": "...", "pubType": 1, "original": 1, "timing": 0 }
```

**知乎 `zhihu`**

```json
{ "title": "...(5-50字)", "content": "<p>...</p>", "covers": [], "taskId": "..." }
```

**百家号 `baijiahao`**

```json
{
  "title": "...(2-64字)",
  "content": "<p>...</p>",
  "covers": ["/absolute/path/to/cover.jpg"],
  "taskId": "...",
  "pubType": 1,
  "timing": 0
}
```

**头条号 `toutiaohao`**

```json
{ "title": "...", "content": "<p>...</p>", "covers": [], "taskId": "...", "timing": 0, "articleAdType": 2, "infoSourceType": -1, "city": { "city": "武汉", "city_code": "420100" }, "collection": { "collection_id": "...", "collection_title": "...", "collection_count": 0, "collection_cover_url": "..." } }
```

**公众号 `gongzhonghao_official`**

```json
{
  "title": "...",
  "content": "<p>...</p>",
  "covers": [],
  "taskId": "...",
  "pubType": 1,
  "author": "",
  "digest": "",
  "need_open_comment": 0,
  "only_fans_can_comment": 0
}
```

**简书 `jianshu`**

```json
{ "title": "...", "content": "<p>...</p>", "covers": [], "taskId": "..." }
```

**CSDN `csdn`**

```json
{ "title": "...", "content": "<p>...</p>", "covers": [], "taskId": "...", "tags": "标签1,标签2" }
```

**搜狐号 `souhuhao`**

```json
{ "title": "搜狐号文章标题", "content": "<p>...</p>", "covers": [], "taskId": "..." }
```

**大鱼号 `dayuhao`**

```json
{ "title": "...", "content": "<p>...</p>", "covers": [], "taskId": "...", "timing": 0 }
```

---

## 任务ID规范

- 任务ID由**调用方生成**，服务端不生成
- 每个任务ID必须**全局唯一**
- 任务ID需同时出现在 `tasks[].taskId` 和 `tasks[].params.taskId` 中
- 建议使用 `nanoid()` 或 `crypto.randomUUID()` 生成

---

## 完整示例

### 批量发布视频到多个平台

```json
{
  "contentType": "video",
  "commonForm": {
    "title": "我的旅行日记",
    "desc": "记录美好的旅行时光",
    "videoPath": "/Users/demo/videos/travel.mp4",
    "coverPath": "/Users/demo/videos/cover.jpg",
    "timing": 0
  },
  "tasks": [
    {
      "taskId": "lPzbyXN7f0Rwnc3671CjZ",
      "accountId": "a3e3098b7be0c97071914e23c0a865d8",
      "platform": "shipinhao",
      "contentType": "video",
      "params": {
        "title": "我的旅行日记",
        "desc": "记录美好的旅行时光",
        "videoPath": "/Users/demo/videos/travel.mp4",
        "coverPath": "/Users/demo/videos/cover.jpg",
        "timing": 0,
        "taskId": "lPzbyXN7f0Rwnc3671CjZ",
        "shortTitle": "",
        "topics": [],
        "mentions": [],
        "location": null,
        "activity": null,
        "collection": null,
        "postFlag": 0,
        "pubType": 1,
        "objectType": 0
      }
    },
    {
      "taskId": "tri0n703DVT7icv9gpJC9",
      "accountId": "a29912e9585709d397b1e1ef650b96f7",
      "platform": "xiaohongshu",
      "contentType": "video",
      "params": {
        "title": "我的旅行日",
        "desc": "记录美好的旅行时光",
        "videoPath": "/Users/demo/videos/travel.mp4",
        "coverPath": "/Users/demo/videos/cover.jpg",
        "timing": 0,
        "taskId": "tri0n703DVT7icv9gpJC9",
        "visibilityType": 0,
        "topics": [],
        "mentions": []
      }
    },
    {
      "taskId": "DKD2t5DNaqAW7lic9fvJY",
      "accountId": "6e2c1fc802f358a8c2360cf7c6e6a7b1",
      "platform": "douyin",
      "contentType": "video",
      "params": {
        "title": "我的旅行日记",
        "desc": "记录美好的旅行时光",
        "videoPath": "/Users/demo/videos/travel.mp4",
        "coverPath": "/Users/demo/videos/cover.jpg",
        "timing": 0,
        "taskId": "DKD2t5DNaqAW7lic9fvJY"
      }
    }
  ]
}
```

---

## 进度追踪

发布是**异步任务**，通过 WebSocket 或 SSE 实时接收进度（二选一）。

### WebSocket

```
ws://127.0.0.1:3456/galic/v1/ws
```

连接时请求头携带 `Authorization: Bearer <token>`，下行消息格式：`{ "channel": "string", "data": unknown }`

### SSE

```http
GET /galic/v1/sse
Authorization: Bearer <token>
Accept: text/event-stream
```

连接成功后先收到 `connected` 事件，event 为 channel，data 为载荷。

### 进度事件

channel：`platform/publish/progress`

```json
{
  "taskId": "lPzbyXN7f0Rwnc3671CjZ",
  "type": "publishing",
  "progress": 50,
  "message": "正在上传视频...",
  "timestamp": 1706000000000
}
```

| type            | 说明       |
| --------------- | ---------- |
| `taskQueued`    | 任务已入队 |
| `publishing`    | 发布进行中 |
| `taskRetrying`  | 重试中     |
| `taskCancelled` | 已取消     |
| `success`       | 发布成功   |
| `error`         | 发布失败   |

---

## 取消任务

```http
POST /galic/v1/platform/publish/cancelTask
Authorization: Bearer <token>
X-CreBee-Source: skill
Content-Type: application/json

{ "taskId": "lPzbyXN7f0Rwnc3671CjZ" }
```

响应：`{ "success": true, "message": "任务已取消" }`

---

## 批量发布响应

```json
{
  "code": 0,
  "raw": {
    "total": 3,
    "success": 2,
    "failed": 1,
    "results": [
      { "accountId": "...", "platform": "shipinhao", "status": "success" },
      { "accountId": "...", "platform": "xiaohongshu", "status": "success" },
      { "accountId": "...", "platform": "douyin", "status": "failed", "error": "账号已失效，请重新绑定" }
    ]
  },
  "message": "success"
}
```

> HTTP `code: 0` 表示 batch handler 已正常返回，单个任务仍可能创建失败。`raw.success` 表示任务已成功创建并入队，`raw.failed` 表示创建任务时失败。接口不会等待实际发布完成，最终结果需通过进度事件判断。
