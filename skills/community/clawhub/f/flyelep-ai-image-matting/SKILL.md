---
name: ai-image-matting
description: >-
  通过 Flyelep AI 工具接口自动去除图片背景，支持单张或批量处理。
  当用户要求抠图、去背景、提取商品主体、生成透明底素材时使用此技能。
---
# Flyelep AI抠图

通过 Flyelep AI Tool API 自动去除图片背景，并返回抠图后的新图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting`
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
  "imageUrlList": [
    "https://example.com/img1.jpg",
    "https://example.com/img2.jpg"
  ]
}
```

也可使用逗号分隔字符串形式（与 `imageUrlList` 二选一）：

```json
{
  "imgUrls": "https://example.com/img1.jpg,https://example.com/img2.jpg"
}
```

## 响应格式

```json
{
  "code": 200,
  "msg": null,
  "data": "https://example.com/matted1.png,https://example.com/matted2.png",
  "result": {
    "fileUrlList": [
      "https://example.com/matted1.png",
      "https://example.com/matted2.png"
    ],
    "taskId": 1234567890
  }
}
```

- `code=200` 表示调用成功；失败时 `code` 非 200，原因在 `msg` 里
- `result.fileUrlList` 为抠图后的图片 URL 数组，按输入顺序排列；**新接入请只读 `result`**
- `result.taskId` 为本次请求的主任务 ID，可用于查询任务明细（每张输入图对应一条明细）
- `result.taskId` 是 19 位长整数，用 JavaScript 等语言解析时按字符串处理，避免丢精度
- `data` 为同样的结果按英文逗号 `,` 拼接成的字符串，为兼容老调用方保留
- 批量时单张失败不影响其他张，结果只含成功项，数量可能少于输入；全部失败才返回错误
- 返回结果应逐个展示给用户，不要回读图片内容

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| imageUrlList | - | 图片链接数组（推荐），与 `imgUrls` 二选一，最多 20 张 |
| imgUrls | - | 图片链接字符串，多张时使用英文逗号分隔，与 `imageUrlList` 二选一，最多 20 张 |

### 参数映射规则

**imageUrlList**（推荐）：
- JSON 数组，每个元素是一个图片直链
- 单次最多 20 张，超出报错「单次最多支持批量处理20张图片」，需分批调用

**imgUrls**（兼容写法）：
- 传字符串，不是数组
- 单张图片直接传 URL 字符串；多张图片用英文逗号 `,` 拼接
- 也可以改用 `imageUrl` 字段传单张图片；三者同时传时优先级为 `imageUrlList` > `imgUrls` > `imageUrl`
- 每个链接都应为公网可访问的图片直链
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**结果格式**：
- 抠图结果通常为透明背景的 `.png` 图片
- 若接口实际返回其他格式，按接口返回值原样展示即可

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

### 示例 1：单张图片抠图

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "imgUrls": "https://example.com/img1.jpg"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"imgUrls":"https://example.com/img1.jpg"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"imgUrls":"https://example.com/img1.jpg"}'
```

### 示例 2：批量图片抠图

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "imgUrls": "https://example.com/img1.jpg,https://example.com/img2.jpg"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"imgUrls":"https://example.com/img1.jpg,https://example.com/img2.jpg"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"imgUrls":"https://example.com/img1.jpg,https://example.com/img2.jpg"}'
```

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| `msg` 为 `密钥无效!` / `密钥格式错误!` / `密钥不能为空!` | `secretKey` 错误、被截断或已失效，向用户重新索取 |
| `code` 为 `9999`、`msg` 为 `服务繁忙，请稍后再试` | 最常见原因是漏传 `secretKey` 请求头，先自查请求头 |
| `点数不足` | 账户算力不足，让用户充值后再试，重试无效 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| 图片参数格式错误 | `imageUrlList` 必须是 JSON 数组，`imgUrls` 必须是逗号分隔字符串，两者只传一个 |
| `图片URL不能为空` | 没有传入任何图片链接 |
| `单次最多支持批量处理20张图片` | 单次最多 20 张，超出需分批调用 |
| `抠图服务异常，请重试` | 全部图片抠图失败，核对图片 URL 是否可访问后重试 |
| 返回数量少于输入 | 部分图片抠图失败，结果只含成功项；可凭 `result.taskId` 查明细后对失败图重试 |
| 图片 URL 无法访问 | 传入的链接不是公网直链、已过期，或源站限制访问 |
| 抠图边缘效果不理想 | 原图主体与背景对比不足、边缘过于复杂，可换更清晰或背景更干净的源图 |
| 请求超时 | 批量图片较多或源图较大时，可适当增大超时时间 |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集一张或多张图片 URL（最多 20 张；如用户提供本地文件，先按「本地文件上传」章节换取公网直链）
3. 将 URL 组装为 `imageUrlList` 数组（推荐），或用英文逗号拼接为 `imgUrls`
4. 在请求头中传入 `secretKey`，调用接口
5. 逐个展示 `result.fileUrlList` 中的图片 URL

> 当用户明确要求"透明底""抠出主体""去掉背景"时，优先使用此技能；如果用户真正想要的是"换背景"而不是"去背景"，则更适合使用场景替换或局部重绘类技能。
