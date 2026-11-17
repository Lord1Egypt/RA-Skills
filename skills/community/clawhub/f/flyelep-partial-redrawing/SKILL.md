---
name: partial-redrawing
description: >-
  通过 Flyelep AI 工具接口对图片局部区域进行重绘，可结合文本提示词和参考替换图生成新图。
  当用户要求局部修改图片、替换背景、替换某个区域内容、保留主体仅改局部时使用此技能。
---
# Flyelep 局部重绘

通过 Flyelep AI Tool API 对图片指定区域进行局部重绘，并返回重绘后的新图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/partialRedrawing`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`（密钥需由用户在 Flyelep 开放平台申请：https://www.flyelep.cn/controlboard）
- **超时时间**: 建议 120-300 秒

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

## 请求 Body

```json
{
  "sourceUrl": "https://example.com/original.jpg",
  "textPrompt": "将背景替换为夏日海滩",
  "replaceImageUrl": "https://example.com/reference.jpg"
}
```

## 响应格式

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": "https://example.com/redrawn.jpg"
}
```

- `code=200` 表示调用成功
- `msg` 为接口返回说明
- `data` 为重绘后的图片 URL
- 返回结果应直接展示给用户，不要回读图片内容

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| sourceUrl | - | 原图链接 |
| textPrompt | - | 用户提示词，用于描述重绘内容 |

### 可选参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| replaceImageUrl | - | 参考替换图片链接 |
| maskDataUrl | - | 掩码图链接，用于限定重绘区域 |
| modelType | `"0"` | 模型类型，字符串：`"0"`=gemini-2.5，`"2"`=gemini-3.1，`"9"`=Flyelep Image 2 |
| languageType | - | 语言类型，用于约束重绘文案的语种 |

### 参数映射规则

**sourceUrl**：
- 传入待重绘原图的公网可访问 URL
- 必须是图片直链，不要传网页地址
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**textPrompt**：
- 直接描述要重绘的内容、目标风格和替换效果
- 应尽量明确“改哪里、改成什么、保留什么”
- 优先保留用户原始意图，不要无故扩写成完全不同的需求

推荐写法示例：

- `将背景替换为纯白背景，保留商品主体和阴影`
- `将杯子上的图案改为蓝色几何纹理，保留杯身材质`
- `把右上角的文字替换为英文促销文案，整体风格保持简洁`

**replaceImageUrl**：
- 当用户提供明确的参考替换图时再传入
- 适合用于“把某一区域替换成参考图风格或内容”的场景
- 用户未提供参考图时，不传此字段
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**maskDataUrl**：
- 掩码图链接，白色区域表示要重绘的部分
- 不传时由模型依据 `textPrompt` 自行判断重绘范围，因此提示词要写清"改哪里"
- 只有用户已经有现成掩码图时才需要传，agent 不要自己构造掩码

**modelType**：
- 该字段是**字符串**，不是数字，例如 `"0"`
- `"0"`：gemini-2.5（默认）
- `"2"`：gemini-3.1，按 3.1 档计费
- `"9"`：Flyelep Image 2，计费按 3.1 档处理，实际模型由工作流路由
- 不传时服务端按 `"0"` 处理；不要显式传 `null`，会导致解析失败

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

### 示例 1：仅通过文字提示进行局部重绘

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "sourceUrl": "https://example.com/original.jpg",
  "textPrompt": "将背景替换为夏日海滩"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"sourceUrl":"https://example.com/original.jpg","textPrompt":"将背景替换为夏日海滩"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/partialRedrawing" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/partialRedrawing" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"sourceUrl":"https://example.com/original.jpg","textPrompt":"将背景替换为夏日海滩"}'
```

### 示例 2：结合参考图进行局部替换

**前置步骤**：向用户索取原图路径或 URL，以及参考替换图路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "sourceUrl": "https://example.com/product.jpg",
  "textPrompt": "将背景更换为更高级的木质桌面场景，保留产品主体不变",
  "replaceImageUrl": "https://example.com/wood-scene.jpg"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"sourceUrl":"https://example.com/product.jpg","textPrompt":"将背景更换为更高级的木质桌面场景，保留产品主体不变","replaceImageUrl":"https://example.com/wood-scene.jpg"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/partialRedrawing" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/partialRedrawing" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"sourceUrl":"https://example.com/product.jpg","textPrompt":"将背景更换为更高级的木质桌面场景，保留产品主体不变","replaceImageUrl":"https://example.com/wood-scene.jpg"}'
```

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `sourceUrl` 无法访问 | 原图 URL 不是公网直链、已过期，或源站限制访问 |
| `textPrompt` 过于模糊 | 提示词没有说明要修改的区域或目标效果，应补充“改哪里、改成什么” |
| `replaceImageUrl` 无法访问 | 参考图 URL 无效或不可公开访问，去掉该字段或更换可访问链接 |
| 传 `"modelType": null` 后报错 | 该字段为字符串且不接受 null，要么不传，要么传 `"0"` |
| 重绘结果偏差较大 | 提示词不够具体，可补充材质、颜色、构图、保留元素等约束 |
| 请求超时 | 源图较大或处理复杂时，可适当增大超时时间 |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集原图 URL `sourceUrl`（如用户提供本地文件，先按「本地文件上传」章节换取公网直链）
3. 明确保留项：主体、品牌标识、材质、构图等不应被误改的内容
4. 明确修改项：背景、局部文案、某个物体、某种颜色或纹理，整理为 `textPrompt`
5. 有参考图时再传 `replaceImageUrl`（同样需为公网链接，本地文件先按「本地文件上传」章节换取公网直链）
6. 若用户只说"帮我改一下图"，应先补足最少必要信息，再调用接口
7. 在请求头中传入 `secretKey`，调用接口并返回重绘后的图片 URL

该接口接收自然语言提示词，`textPrompt` 的质量会直接影响结果。当用户目标是“小范围替换”时，提示词应避免写成整张图重做；当用户目标是“换背景”时，应在 `textPrompt` 中强调保留主体不变。
