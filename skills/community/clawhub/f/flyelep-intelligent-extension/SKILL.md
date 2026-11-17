---
name: intelligent-extension
description: >-
  通过 Flyelep AI 工具接口对图片进行智能延展，支持批量处理并指定目标比例。
  当用户要求扩图、延展图片边缘、补全画布、适配 16:9/1:1 等比例时使用此技能。
---
# Flyelep 图片智能延展

通过 Flyelep AI Tool API 对一张或多张图片进行智能延展。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`（密钥需由用户在 Flyelep 开放平台申请：https://www.flyelep.cn/controlboard）
- **超时时间**: 单张建议 120-300 秒；多张时服务端逐张并行处理（同时最多 10 张），超过 10 张建议 600 秒；服务端整批处理上限 20 分钟

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

## 请求 Body

```json
{
  "imgUrlList": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
  ],
  "ratio": "16:9"
}
```

## 响应格式

```json
{
  "code": 200,
  "msg": null,
  "data": [
    "https://example.com/result1.jpg",
    "https://example.com/result2.jpg"
  ],
  "result": {
    "fileUrlList": [
      "https://example.com/result1.jpg",
      "https://example.com/result2.jpg"
    ],
    "taskId": 1234567890
  }
}
```

- `code=200` 表示调用成功；失败时 `code` 非 200，原因在 `msg` 里
- `result.fileUrlList` 为延展后的图片 URL 数组，按 `imgUrlList` 的输入顺序排列；**新接入请只读 `result`**
- `result.taskId` 为本次请求的主任务 ID，可用于查询任务明细（每张输入图对应一条明细）
- `result.taskId` 是 19 位长整数，用 JavaScript 等语言解析时按字符串处理，避免丢精度
- `data` 与 `result.fileUrlList` 内容相同，为兼容老调用方保留
- 批量时单张失败不影响其他张，结果只含成功项，数量可能少于输入；全部失败才返回错误
- 返回结果应逐个展示给用户，不要回读图片内容

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| imgUrlList | - | 源图片 URL 列表，支持批量传入多张图片，单次最多 20 张，单张不超过 10MB |
| ratio | - | 目标延展比例 |

### 可选参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| modelType | `"9"` | 模型类型，字符串：`"0"`=gemini-2.5，`"2"`=gemini-3.1，`"9"`=Flyelep Image 2 |

### 参数映射规则

**imgUrlList**：
- 接口要求传字符串数组，每个元素为一张图片 URL
- 单次最多 20 张，超出报错「单次最多支持批量处理20张图片」，需分批调用
- 单张图片不超过 10MB，超出报错「图片大小不能超过10MB，请压缩后重试」
- 每个链接都应为公网可访问的图片直链，不要传网页地址
- 保留用户原始图片顺序，不要擅自重排 `imgUrlList`
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**ratio（目标比例）**：
仅支持以下比例：

- `1:1`
- `2:3`
- `3:2`
- `3:4`
- `4:3`
- `9:16`
- `16:9`
- `21:9`

当用户明确指定目标比例时，原样传入 `ratio`。服务端不校验该字段，传入列表外的值不会报错，但出图比例不可控，因此只传上表中的值。

当用户仅表达“改成横版”或“适配视频封面”等模糊需求时，可按上下文推断最合理的比例：

- 横版内容优先考虑 `16:9`
- 方图内容优先考虑 `1:1`
- 竖版内容优先考虑 `9:16`

如果上下文不足以安全推断，先向用户确认目标比例。

**modelType**：
- 该字段是**字符串**，不是数字，例如 `"9"`
- 不传或传空串时服务端按 `"9"`（Flyelep Image 2）处理
- 智能延展按张固定计费，不随 `modelType` 变化；实际调用的模型由服务端路由
- 只能传上面列出的数字字符串，传非数字或未知编号会直接报错；用户没有指定模型时直接省略该字段

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

成功响应取 `data.fullPath` 作为公网直链（不带签名，按 24 小时限时链接对待，拿到后直接用于本次调用，不要长期保存）：

```json
{
  "code": 200,
  "msg": null,
  "data": {
    "relativePath": "oss_ai_agent_h_24/2026-11-12/3f2a9c1b7d84e6f5a0123b4c5d6e7f80.png",
    "fullPath": "https://oss-agent-7346.flyelep.cn/oss_ai_agent_h_24/2026-11-12/3f2a9c1b7d84e6f5a0123b4c5d6e7f80.png",
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

### 示例 1：单张图片延展为横版 16:9

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "imgUrlList": [
    "https://example.com/image1.jpg"
  ],
  "ratio": "16:9"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"imgUrlList":["https://example.com/image1.jpg"],"ratio":"16:9"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"imgUrlList":["https://example.com/image1.jpg"],"ratio":"16:9"}'
```

### 示例 2：批量图片延展为方图 1:1

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "imgUrlList": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
  ],
  "ratio": "1:1"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"imgUrlList":["https://example.com/image1.jpg","https://example.com/image2.jpg"],"ratio":"1:1"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"imgUrlList":["https://example.com/image1.jpg","https://example.com/image2.jpg"],"ratio":"1:1"}'
```

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| `msg` 为 `密钥无效!` / `密钥格式错误!` / `密钥不能为空!` | `secretKey` 错误、被截断或已失效，向用户重新索取 |
| `code` 为 `9999`、`msg` 为 `服务繁忙，请稍后再试` | 最常见原因是漏传 `secretKey` 请求头，先自查请求头 |
| `点数不足` | 账户算力不足，让用户充值后再试，重试无效 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `图片列表不能为空` | 至少传入一张待处理图片 URL |
| `单次最多支持批量处理20张图片` | 单次最多 20 张，超出需分批调用 |
| `图片大小不能超过10MB，请压缩后重试` | 源图超过 10MB，压缩后重新上传再调用 |
| 出图比例与预期不符 | `ratio` 传了列表外的值，服务端不报错但比例不可控，改用支持的固定枚举值 |
| 处理超时 | 批量图片较多或源图较大时可适当增大超时时间 |
| 返回数组数量少于输入 | 部分图片处理失败，结果只含成功项；可凭 `result.taskId` 查明细，核对源图 URL 是否可访问后对失败图重试 |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集用户提供的图片 URL 列表（如用户提供本地文件，先按「本地文件上传」章节换取公网直链）
3. 确定目标比例 `ratio`
4. 在请求头中传入 `secretKey`，调用接口
5. 按输入顺序展示 `result.fileUrlList` 中的图片 URL

该接口不接收自然语言提示词，不需要构造额外文案。保留用户原始图片顺序，不要擅自重排 `imgUrlList`。
