---
name: image-translate
description: >-
  通过 Flyelep AI 工具接口识别并翻译图片中的文字，返回翻译后的新图片地址。
  当用户要求翻译海报文字、翻译商品图文案、将图片文字改成目标语言时使用此技能。
---
# Flyelep 图片翻译

通过 Flyelep AI Tool API 对图片中的文字进行识别与翻译，并返回翻译后的新图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`（密钥需由用户在 Flyelep 开放平台申请：https://www.flyelep.cn/controlboard）
- **超时时间**: 建议 120-300 秒；多张图或多种目标语言时建议 600 秒（多种语言由服务端并行处理），服务端整批处理上限 20 分钟

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

## 请求 Body

```json
{
  "imageUrl": "https://example.com/poster_cn.jpg",
  "to": 1,
  "from": "auto"
}
```

## 响应格式

```json
{
  "code": 200,
  "msg": null,
  "data": "https://example.com/translated.jpg",
  "result": {
    "fileUrlList": ["https://example.com/translated.jpg"],
    "taskId": 1234567890
  }
}
```

- `code=200` 表示调用成功；失败时 `code` 非 200，原因在 `msg` 里
- `result.fileUrlList` 为翻译后的新图片 URL 数组（单张时也是数组）；**新接入请只读 `result`**
- `result.taskId` 为本次请求的主任务 ID，可用于查询任务明细（每个“图片 × 目标语言”组合对应一条明细）
- `result.taskId` 是 19 位长整数，用 JavaScript 等语言解析时按字符串处理，避免丢精度
- `data` 为同样的结果按英文逗号拼接成的字符串，为兼容老调用方保留
- 结果顺序：先按目标语言、再按图片，例如 2 张图 × 2 种语言为「图1-语言1, 图2-语言1, 图1-语言2, 图2-语言2」
- 批量时单个组合失败不影响其他组合，结果只含成功项，数量可能少于“图片数 × 语言数”；全部失败才返回错误
- 返回结果应直接展示给用户，不要回读图片内容

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| imageUrl | - | 待翻译的图片链接，多张时用英文逗号分隔 |
| to | - | 目标语言（单选），使用接口定义的整数枚举值；与 `toList` 二选一 |

### 可选参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| toList | - | 目标语言列表（多选），整数枚举数组；传了就优先于 `to` |
| from | `auto` | 原语言；当前服务端始终自动识别原语言，此字段不生效，可不传 |

### 参数映射规则

**imageUrl**：
- 传入待翻译图片的公网可访问 URL
- 必须是图片直链，不要传网页地址
- 支持批量：多张图片用英文逗号 `,` 拼接在同一个 `imageUrl` 字段里，返回结果同样按逗号分隔
- 图片数 × 目标语言数不能超过 20，超出报错「图片数×语言数不能超过20」，需分批调用
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**from（原语言）**：
- 服务端当前忽略该字段，始终自动识别原语言
- 可传 `"auto"` 或不传；用户指定了源语言也无需传入

**to / toList（目标语言）**：
- 传整数枚举值，而不是语言名称字符串
- 只要一种目标语言时传 `to`；要同时翻译成多种语言时传 `toList` 数组（如 `[15, 16]`），每张图会分别生成每种语言的结果
- 两者都传时以 `toList` 为准；两者都不传报错「目标语言不能为空」
- 目标语言枚举如下：

| `to` | 语言 |
|------|------|
| `0` | 中文 |
| `1` | 英文 |
| `2` | 俄语 |
| `3` | 西班牙语 |
| `4` | 法语 |
| `5` | 德语 |
| `6` | 意大利语 |
| `7` | 荷兰语 |
| `8` | 葡萄牙语 |
| `9` | 越南语 |
| `10` | 土耳其语 |
| `11` | 马来语 |
| `12` | 泰语 |
| `13` | 波兰语 |
| `14` | 印度尼西亚语 |
| `15` | 日语 |
| `16` | 韩语 |
| `17` | 繁体中文 |

- 当用户以自然语言表达目标语种时，按上表映射为对应整数后传入
- 如果用户请求的语言不在上述枚举表中，应明确告知接口当前不支持该目标语言
- 传入表外的整数不会得到明确提示，只会报「翻译异常,请稍后重试」或「翻译失败，请稍后重试」，因此调用前务必按表映射

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

### 示例 1：自动识别原语言，翻译成英文

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "imageUrl": "https://example.com/poster_cn.jpg",
  "to": 1,
  "from": "auto"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"imageUrl":"https://example.com/poster_cn.jpg","to":1,"from":"auto"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"imageUrl":"https://example.com/poster_cn.jpg","to":1,"from":"auto"}'
```

### 示例 2：两张图同时翻译成日语和韩语

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "imageUrl": "https://example.com/product-poster.jpg,https://example.com/product-detail.jpg",
  "toList": [15, 16]
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"imageUrl":"https://example.com/product-poster.jpg,https://example.com/product-detail.jpg","toList":[15,16]}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 600 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 600 --data-binary '{"imageUrl":"https://example.com/product-poster.jpg,https://example.com/product-detail.jpg","toList":[15,16]}'
```

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| `msg` 为 `密钥无效!` / `密钥格式错误!` / `密钥不能为空!` | `secretKey` 错误、被截断或已失效，向用户重新索取 |
| `code` 为 `9999`、`msg` 为 `服务繁忙，请稍后再试` | 最常见原因是漏传 `secretKey` 请求头，先自查请求头 |
| `点数不足` | 账户算力不足，让用户充值后再试，重试无效 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `imageUrl` 无法访问 | 图片 URL 不是公网直链、已过期，或源站限制访问 |
| `图片链接不能为空` | `imageUrl` 未传或为空 |
| `目标语言不能为空` | `to` 和 `toList` 都没传 |
| `图片数×语言数不能超过20` | 图片数乘以目标语言数超过 20，减少图片或语言后分批调用 |
| `翻译异常,请稍后重试` / `翻译失败，请稍后重试` | 目标语言用了枚举表外的整数（必须用表内值，例如英文=`1`、日语=`15`、韩语=`16`），或图片识别、翻译失败 |
| 返回数量少于“图片数 × 语言数” | 部分组合翻译失败，结果只含成功项；可凭 `result.taskId` 查明细后对失败项重试 |
| 翻译结果异常 | 原图文字过小、模糊或遮挡严重，可更换更清晰的源图后重试 |
| 请求超时 | 源图较大或识别耗时较长时，可适当增大超时时间 |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集图片 URL 写入 `imageUrl`，多张时用英文逗号拼接（如用户提供本地文件，先按「本地文件上传」章节换取公网直链）
3. 根据语言枚举表确定目标语言整数：一种语言传 `to`，多种语言传 `toList`
4. `from` 可不传，服务端自动识别原语言
5. 在请求头中传入 `secretKey`，调用接口
6. 返回 `result.fileUrlList` 中翻译后的图片 URL

该接口不接收自然语言提示词，不需要构造额外文案。如果用户只说“翻译成英文/日文/韩文”等常见语言，可直接按本技能内的枚举表映射为对应整数后调用；若用户要求的目标语言不在枚举表内，则不要硬猜，需明确告知暂不支持。
