---
name: image-enlarge
description: >-
  通过 Flyelep AI 工具接口对图片进行无损放大，支持单张或批量处理。
  当用户要求提升清晰度、放大图片尺寸、做超清增强、批量增强商品图时使用此技能。
---
# Flyelep 无损放大

通过 Flyelep AI Tool API 对图片进行无损放大处理，并返回增强后的图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`（密钥需由用户在 Flyelep 开放平台申请：https://www.flyelep.cn/controlboard）
- **超时时间**: 单张建议 120-300 秒；多张时服务端逐张并行处理（同时最多 10 张），超过 10 张或放大 8 倍时建议 600 秒；服务端整批处理上限 20 分钟

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
  ],
  "scalingRatio": 2
}
```

也可使用逗号分隔字符串形式（与 `imageUrlList` 二选一）：

```json
{
  "imgUrls": "https://example.com/img1.jpg,https://example.com/img2.jpg",
  "scalingRatio": 2
}
```

## 响应格式

```json
{
  "code": 200,
  "msg": null,
  "data": "https://example.com/enlarged1.jpg,https://example.com/enlarged2.jpg",
  "result": {
    "fileUrlList": [
      "https://example.com/enlarged1.jpg",
      "https://example.com/enlarged2.jpg"
    ],
    "taskId": 1234567890
  }
}
```

- `code=200` 表示调用成功；失败时 `code` 非 200，原因在 `msg` 里
- `result.fileUrlList` 为放大后的图片 URL 数组，按输入顺序排列；**新接入请只读 `result`**
- `result.taskId` 为本次请求的主任务 ID，可用于查询任务明细（每张输入图对应一条明细）
- `result.taskId` 是 19 位长整数，用 JavaScript 等语言解析时按字符串处理，避免丢精度
- `data` 为同样的结果按英文逗号 `,` 拼接成的字符串，为兼容老调用方保留
- 批量时单张失败不影响其他张，结果只含成功项，数量可能少于输入
- **全部失败时接口不报错**：`code` 仍为 200，但 `result.fileUrlList` 为空数组、`data` 为空字符串，必须据此判断失败并告知用户
- 返回结果应逐个展示给用户，不要回读图片内容

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| imageUrlList | array | - | 图片链接数组（推荐），与 `imgUrls` 二选一，最多 20 张，建议单张 10MB 以内 |
| imgUrls | String | - | 图片链接字符串，多张时使用英文逗号分隔，与 `imageUrlList` 二选一，最多 20 张 |
| scalingRatio | Integer | - | 放大倍率：`2`=2 倍，`4`=4 倍，`8`=8 倍 |

### 参数映射规则

**imageUrlList**（推荐）：
- JSON 数组，每个元素是一个图片直链
- 最多 20 张，超出报错「单次最多支持批量处理20张图片」；建议单张图片大小在 10MB 以内
- 与 `imgUrls` 二选一，两者传其一即可，优先使用本参数；同时传时以本参数为准

**imgUrls**（兼容写法）：
- 传字符串，不是数组
- 单张图片时直接传一个 URL 字符串
- 多张图片时，用英文逗号 `,` 按顺序拼接，最多 20 张
- 每个链接都应为公网可访问的图片直链，不要传网页地址
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**scalingRatio**：
- 含义是放大倍率，不是增强强度档位
- 只传 `2`、`4`、`8` 三个取值；`1`-`8` 之间的其他整数不报错，但按 2 倍处理
- 不传或超出 `1`-`8` 范围时接口直接报错「放大倍数必须是8倍以内」，因此该字段必须传
- 算力按倍率加倍：每张 2 倍计 1 份、4 倍计 2 份、8 倍计 3 份，只按成功张数扣除

推荐默认规则：

- 用户未指定倍数时，默认传 `2`
- 用户要求“放大 4 倍 / 更大尺寸”时，传 `4`
- 用户要求“尽可能放大”时，传 `8`

> **说明**：该接口按倍数放大原图，只做无损放大，不接收自然语言提示词。如果用户真正想要的是“提升清晰度、修复模糊”，应改用 AI 超清（image-clarity-enhance）技能，那里的 `enhanceStrength` 才是强度档位。

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

### 示例 1：单张图片 2 倍放大

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "imageUrlList": ["https://example.com/img1.jpg"],
  "scalingRatio": 2
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"imageUrlList":["https://example.com/img1.jpg"],"scalingRatio":2}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"imageUrlList":["https://example.com/img1.jpg"],"scalingRatio":2}'
```

### 示例 2：批量图片 4 倍放大

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "imageUrlList": [
    "https://example.com/img1.jpg",
    "https://example.com/img2.jpg"
  ],
  "scalingRatio": 4
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"imageUrlList":["https://example.com/img1.jpg","https://example.com/img2.jpg"],"scalingRatio":4}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"imageUrlList":["https://example.com/img1.jpg","https://example.com/img2.jpg"],"scalingRatio":4}'
```

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| `msg` 为 `密钥无效!` / `密钥格式错误!` / `密钥不能为空!` | `secretKey` 错误、被截断或已失效，向用户重新索取 |
| `code` 为 `9999`、`msg` 为 `服务繁忙，请稍后再试` | 最常见原因是漏传 `secretKey` 请求头，先自查请求头 |
| `点数不足` | 账户算力不足，让用户充值后再试，重试无效 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| 图片参数格式错误 | `imageUrlList` 必须是 JSON 数组，`imgUrls` 必须是逗号分隔字符串，两者只传一个 |
| `图片URL不能为空` | `imageUrlList` 和 `imgUrls` 都没传或都为空 |
| `单次最多支持批量处理20张图片` | 单次最多 20 张，超出需分批调用 |
| `code=200` 但 `result.fileUrlList` 为空 | 全部图片放大失败，接口不会报错；核对图片 URL 是否可访问、格式是否规范后重试 |
| 返回数量少于输入 | 部分图片放大失败，结果只含成功项；可凭 `result.taskId` 查明细后对失败图重试 |
| 图片 URL 无法访问 | 传入的链接不是公网直链、已过期，或源站限制访问 |
| `放大倍数必须是8倍以内` | `scalingRatio` 未传或不在 `1`-`8` 范围内，应传 `2`、`4` 或 `8` |
| 接口提示图片规格不符合要求 | 换用更规范的图片尺寸或格式后重试 |
| 请求超时 | 批量图片较多或放大倍数较高时，可适当增大超时时间 |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集一张或多张图片 URL（最多 20 张；如用户提供本地文件，先按「本地文件上传」章节换取公网直链）
3. 将 URL 组装为 `imageUrlList` 数组（推荐），或用英文逗号拼接为 `imgUrls`
4. 根据用户意图确定 `scalingRatio`（放大倍率，仅 `2`/`4`/`8`，未指定时用 `2`）
5. 在请求头中传入 `secretKey`，调用接口
6. 逐个展示 `result.fileUrlList` 中的图片 URL；数组为空时按失败处理并告知用户

该接口不接收自然语言提示词，不需要构造额外文案。如果用户只是说“帮我变清晰一点”而没有提尺寸，应改用 AI 超清（image-clarity-enhance）技能；只有明确要“放大、提尺寸、提分辨率”时才用本技能。
