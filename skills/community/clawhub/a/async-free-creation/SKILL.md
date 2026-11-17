---
name: async-free-creation
description: >-
  通过 Flyelep 异步自由创作接口调用 Image-2 模型生成产品图或创意图。
  当用户要求异步自由创作、自由创作、Image-2 自由创作、根据提示词和参考图生成多张图片时使用此技能。
---
# Flyelep 异步自由创作

通过 Flyelep Image-2 自由创作 API 异步生成图片。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息

### 创建任务

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/allAroundCreationAsync`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`（密钥需由用户在 Flyelep 开放平台申请：https://www.flyelep.cn/controlboard）
- **超时时间**: 建议 120-300 秒

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：`secretKey` 必须放在请求头中，不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

### 查询结果

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult`
- **Content-Type**: `application/json`
- **认证方式**: 在请求 Header 中传入 `secretKey`
- **说明**: 该接口是新版任务查询接口，优先使用；旧接口 `queryResult` 仍可作为兼容备选。

## 请求 Body

创建任务：
```json
{
  "query": "生成钢笔的产品图",
  "apiImgUrlList": [
    "https://example.com/product.png"
  ],
  "detailPictureNumber": 4,
  "aspectRatio": "1:1",
  "channel": "promotion"
}
```

查询结果：
```json
{
  "agentGenerateTaskId": "创建任务返回的任务ID"
}
```

## 响应格式

### 创建任务响应

```json
{
  "code": 200,
  "data": {
    "agentGenerateTaskId": "2054467932287070209"
  }
}
```

- `code=200` 表示创建任务成功
- `data.agentGenerateTaskId` 为异步任务 ID
- 创建任务后必须继续调用查询结果接口获取最终图片 URL

### 查询结果响应

```json
{
  "code": 200,
  "data": {
    "taskList": [
      {
        "taskStatus": 2,
        "executeResult": "https://example.com/result1.png"
      },
      {
        "taskStatus": 1
      }
    ]
  }
}
```

#### taskStatus 状态

| 值 | 含义 |
|----|------|
| `0` | 待生成 |
| `1` | 生成中 |
| `2` | 生成成功 |
| `3` | 生成失败 |

当 `taskStatus=2` 时，读取对应项的 `executeResult` 图片 URL 并展示给用户。若仍有 `0` 或 `1`，等待后继续轮询；若出现 `3`，告知用户该任务项生成失败。

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| query | - | 用户生成图片的具体需求描述，最多 1000 个字符 |
| detailPictureNumber | - | 需要生成的图片数量，支持 `1` 到 `4` |
| aspectRatio | 随机 | 图片比例；文档标注为必需，但为空时默认随机比例 |

### 可选参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| apiImgUrlList | - | 参考图片 URL 数组，最多 6 张，建议单张图片小于 10MB |
| channel | `promotion` | 特惠通道（`promotion`，默认，未指定时显式传该值）/尊享通道（`premium`） |

### 参数映射规则

#### query
- 直接传入用户对图片的生成需求
- 保留用户原始创意意图，不要无故扩写成另一种产品或场景
- 如果用户只给产品名，可补充为简洁的产品图生成需求，例如：`生成钢笔的产品图`
- 最多 1000 个字符，超出时需要压缩描述

#### apiImgUrlList
- 传入公网可访问的图片直链数组
- 最多 6 张
- 字段名是 `apiImgUrlList`，不是 `fileUrlList` 或 `imgUrlList`
- 用户未提供参考图时，不传此字段
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

#### detailPictureNumber
- 支持 `1`、`2`、`3`、`4`
- 用户未指定数量时，默认传 `4`
- 用户要求超过 4 张时，告知该接口单次最多生成 4 张，可分多次调用

#### aspectRatio
支持以下比例：
- `1:1`
- `3:2`
- `2:3`
- `3:4`
- `4:3`
- `4:5`
- `5:4`
- `9:16`
- `16:9`
- `21:9`

API 文档标注此参数为必需，但默认为空时接口随机选择比例。

默认规则：
- 用户明确指定比例时，原样传入
- 用户未指定比例时，可传空字符串或不传，让接口随机选择
- 横版优先推断为 `16:9`
- 方图优先推断为 `1:1`
- 竖版优先推断为 `9:16`

#### channel（通道）
- `promotion`：特惠通道，**本技能的默认通道**，线路更经济
- `premium`：尊享通道，官方专线，支持全部模型

**默认规则：用户没有指定通道时，一律显式传 `"channel": "promotion"`。** 只在用户明确要求尊享通道，或本次要用的模型不在特惠通道支持范围内时，才传 `premium`。

特惠通道只开放 `modelEdition` 为 `3`（Flyelep Nano 2）和 `9`（Flyelep Image 2）这两个模型，默认模型 `9` 本身就在范围内。**显式传 `promotion` 又搭配特惠通道不支持的模型（如 `modelEdition=2`）时，接口会直接报错拒绝，不会自动降级**，此时通道要跟着改成 `premium`。

> 完全不传 `channel` 时，服务端也是按特惠通道处理，并在模型不支持特惠时自动回落尊享。但显式传值能让通道和计费可预期，因此按上面的规则明确传入，不要依赖服务端兜底。

## 异步任务流程

> **重要**：本接口为异步接口，必须**先调用主接口获取 `agentGenerateTaskId`，然后调用 `queryTaskResult` 接口轮询任务结果**，不能省略轮询步骤。

1. 调用主接口（`allAroundCreationAsync`）提交任务，从响应中获取 `agentGenerateTaskId`
2. 使用 `agentGenerateTaskId` 调用 `queryTaskResult` 接口轮询任务结果（建议每 5-10 秒查询一次）
3. 当 `taskStatus=2` 时，表示生成成功，获取 `executeResult` 结果
4. 当 `taskStatus=3` 时，表示生成失败

## 本地文件上传

用户提供的是本地文件路径而不是公网直链时，先把文件上传换取直链，再调用本接口。已安装 `file-upload` 技能时以该技能为准；未安装时按下面的说明直接调用上传接口。

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload`
- **请求方式**: `multipart/form-data`，文件字段名固定为 `file`，单次只能上传一个文件，多个文件并发调用多次
- **认证方式**: 请求头传 `secretKey`，与本技能使用同一个密钥
- **超时时间**: 图片建议 60-120 秒
- **不要手动设置 `Content-Type` 请求头**，让 HTTP 客户端自动生成带 boundary 的值，手写会导致服务端解析失败
- 图片仅支持 `bmp`、`gif`、`jpg`、`jpeg`、`png`，`webp` 需先转成 `png` 或 `jpg`；文件名必须带正确后缀，服务端靠它判断格式
- 原文件名不会出现在 URL 里，中文名、空格、特殊字符都能直接上传，不需要提前改名
- 上传不消耗算力，但服务端不做去重：同一个文件在一次任务里只上传一次，记下 `fullPath` 复用

成功响应取 `data.fullPath` 作为公网直链，永久有效、不带签名：

```json
{
  "code": 200,
  "msg": null,
  "data": {
    "relativePath": "cos_ai_agent/2026-08-11/3f2a9c1b7d84e6f5a012.png",
    "fullPath": "https://agent-1404002717.cos.ap-guangzhou.myqcloud.com/cos_ai_agent/2026-08-11/3f2a9c1b7d84e6f5a012.png",
    "serviceProvider": null
  }
}
```

判断成功只看 `code`，业务失败时 HTTP 状态码仍是 200，`code` 为 500 或 9999，原因在 `msg` 里。

```bash
# Windows/PowerShell（用 curl.exe，PowerShell 里的 curl 是 Invoke-WebRequest 的别名）
curl.exe -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload" -H "secretKey: 你的密钥" --max-time 120 -F "file=@C:/path/to/product.png"

# macOS/Linux
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload" -H "secretKey: 你的密钥" --max-time 120 -F "file=@./product.png"
```

图片入桶前会先过内容审核，审核不通过整个请求失败，需换图重试。拿到 `code=9999`、`msg` 为 `服务繁忙，请稍后再试` 时，先自查三项：是否漏了 `secretKey` 请求头、表单字段名是否为 `file`、文件是否超出服务端体积上限。密钥、格式、审核、体积类错误重试无效，只有网络超时、5xx 和存储类异常值得重试。

## 调用示例

> **跨平台调用说明**：
> - 请求头必须包含 `Content-Type: application/json; charset=utf-8` 和 `secretKey`
> - **Windows/PowerShell**：因 GBK 编码问题，必须先将 JSON 写入临时文件 `payload_temp.json`（UTF-8 无 BOM），再用 `curl.exe --% --data-binary @payload_temp.json` 发送请求。使用 Write 工具创建文件，或用 .NET API `[System.IO.File]::WriteAllText("payload_temp.json", $json, [System.Text.UTF8Encoding]::new($false))`。调用后用 `rm payload_temp.json` 清理。
> - **macOS/Linux**：bash/zsh 默认 UTF-8，可直接内联 JSON：`curl -X POST URL -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --data-binary 'JSON单行内容'`

### 示例 1：创建异步自由创作任务

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "aspectRatio": "1:1",
  "query": "生成钢笔的产品图",
  "detailPictureNumber": 4,
  "channel": "promotion",
  "apiImgUrlList": [
    "https://example.com/product.png"
  ]
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"aspectRatio":"1:1","query":"生成钢笔的产品图","detailPictureNumber":4,"channel":"promotion","apiImgUrlList":["https://example.com/product.png"]}', [System.Text.UTF8Encoding]::new($false))
```

执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/allAroundCreationAsync" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/allAroundCreationAsync" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"aspectRatio":"1:1","query":"生成钢笔的产品图","detailPictureNumber":4,"channel":"promotion","apiImgUrlList":["https://example.com/product.png"]}'
```

### 示例 2：查询任务结果

**Windows/PowerShell**：

创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "agentGenerateTaskId": "2054467932287070209"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"agentGenerateTaskId":"2054467932287070209"}', [System.Text.UTF8Encoding]::new($false))
```

执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"agentGenerateTaskId":"2054467932287070209"}'
```

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `agentGenerateTaskId` 为空 | 创建任务失败或响应结构异常，检查创建任务接口返回 |
| 查询结果一直是 `0` 或 `1` | 图片仍在排队或生成中，等待后继续轮询 |
| `taskStatus=3` | 对应图片生成失败，可简化提示词、减少参考图或重试 |
| `detailPictureNumber` 超出范围 | 该接口仅支持单次生成 `1-4` 张 |
| `apiImgUrlList` 无法访问 | 参考图 URL 不是公网直链、已过期，或源站限制访问 |
| 比例不支持 | `aspectRatio` 必须使用文档规定的比例枚举 |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集用户的生成需求并写入 `query`
3. 收集可选参考图并写入 `apiImgUrlList`（本地文件先按「本地文件上传」章节换取公网直链）
4. 确定 `detailPictureNumber`，未指定时默认 `4`
5. 确定 `aspectRatio`，未指定时可为空或不传
6. 在请求头中传入 `secretKey`
7. 调用创建任务接口，从响应中读取 `data.agentGenerateTaskId`
8. 轮询调用查询结果接口，将 `taskStatus=2` 的 `executeResult` 图片 URL 逐个展示给用户

**提示词处理：**
该接口适合宽泛的创意图片生成，但仍应把提示词写得明确、短而有约束。

推荐提示词包含：
- 产品或主体
- 使用场景
- 风格与氛围
- 构图或比例要求
- 需要保留的参考图特征

不要在提示词中承诺接口不支持的细粒度编辑能力。若用户明确要求局部重绘、商品换色、商品替换、场景替换、图片翻译、抠图、放大或超清增强，应优先使用对应的专用 skill。
