---
name: ai-writing-assist
description: >-
  通过 Flyelep AI 帮写 API 辅助生成创意文案，可用于优化用户提示词。
  当用户要求生成文案、优化提示词、获取创意灵感时使用此技能。
---
# Flyelep AI帮写
通过 Flyelep AI Tool API 辅助生成创意文案，可用于优化用户提示词或获取创意灵感。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/assistedGeneration`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`（密钥需由用户在 Flyelep 开放平台申请：https://www.flyelep.cn/controlboard）
- **超时时间**: 建议 60-120 秒

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：`secretKey` 必须放在请求头中，这是 AI 工具接口的统一鉴权要求。不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

## 请求 Body

```json
{
  "query": "用户需求描述，最多1000个字符",
  "fileUrlList": ["https://example.com/img1.png", "https://example.com/img2.png"],
  "generateType": "image"
}
```

## 响应格式

成功：
```json
{
  "code": 200,
  "data": {
    "options": [
      "创意文案选项1",
      "创意文案选项2",
      "创意文案选项3",
      "创意文案选项4"
    ]
  }
}
```
- `code=200` 表示调用成功
- `data.options` 为 AI 生成的多个创意文案选项数组
- 将所有选项展示给用户供其选择

失败：
```json
{
  "code": 500,
  "msg": "错误信息"
}
```

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| query | - | 用户需求描述，最多1000个字符长度 |

### 可选参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| fileUrlList | - | 文件URL地址数组，最多上传6张，建议单张图片大小在10MB以内 |
| generateType | - | 生成类型：`image`或空表示图片生成，`video`表示视频生成 |

### 参数映射规则

#### generateType（生成类型）
- `image` 或不传：图片生成场景
- `video`：视频生成场景

#### fileUrlList（参考文件）
- 数组格式，支持多个URL
- 最多6个文件
- 用于提供参考图片帮助AI生成更精准的文案
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

#### 结果处理
- `data.options` 是一个数组，包含多个备选文案
- 每个选项是一个完整的创意文案，通常包含产品卖点、使用场景、用户群体、背景风格等信息
- 将所有选项展示给用户，让用户选择或作为创作参考

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

### 示例 1：基础文案生成

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "query": "钓鱼竿"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"query":"钓鱼竿"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/assistedGeneration" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/assistedGeneration" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"query":"钓鱼竿"}'
```

### 示例 2：带参考图的文案优化（图片场景）

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "query": "为这款蓝牙耳机生成电商文案",
  "fileUrlList": ["https://example.com/product1.png", "https://example.com/product2.png"],
  "generateType": "image"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"query":"为这款蓝牙耳机生成电商文案","fileUrlList":["https://example.com/product1.png","https://example.com/product2.png"],"generateType":"image"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/assistedGeneration" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/assistedGeneration" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"query":"为这款蓝牙耳机生成电商文案","fileUrlList":["https://example.com/product1.png","https://example.com/product2.png"],"generateType":"image"}'
```

### 示例 3：视频场景文案生成

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "query": "为这款智能手表生成短视频脚本文案",
  "generateType": "video"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"query":"为这款智能手表生成短视频脚本文案","generateType":"video"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/assistedGeneration" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/assistedGeneration" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"query":"为这款智能手表生成短视频脚本文案","generateType":"video"}'
```

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| query 超过1000字符 | 缩短 query 内容 |
| 服务繁忙（9999错误码） | 稍后重试 |
| fileUrlList 文件过多 | 最多上传6个文件 |
| 单张图片超过10MB | 压缩图片大小 |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集用户的基础描述并写入 `query`
3. 如有参考图片，收集图片 URL 写入 `fileUrlList`（本地文件先按「本地文件上传」章节换取公网直链）
4. 根据场景选择 `generateType`：`image`（图片场景）或 `video`（视频场景）
5. 在请求头中传入 `secretKey`，调用接口
6. 将返回的 `data.options` 中所有创意文案选项展示给用户

**提示词处理：**
当用户需要：
- 优化产品描述、生成电商文案
- 获取创意灵感、润色提示词
- 为海报或视频生成配套文案

收集用户的基础描述，如有参考图片则一并上传，调用此接口获取多个创意选项展示给用户。

**AI帮写结果通常包含以下结构：**
- 产品卖点
- 使用场景
- 用户群体
- 背景风格建议

这些信息可直接用于后续的图片或视频生成任务。
