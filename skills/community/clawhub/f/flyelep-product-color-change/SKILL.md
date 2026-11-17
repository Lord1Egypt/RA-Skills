---
name: product-color-change
description: >-
  通过 Flyelep AI 工具接口智能识别图片中的商品并进行换色处理。
  当用户要求修改商品颜色、保持商品不变只换配色、生成同款不同颜色展示图时使用此技能。
---
# Flyelep 商品换色
通过 Flyelep AI Tool API 对图片中的商品进行换色处理，并返回换色后的新图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange`
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
  "sourceUrl": "https://example.com/product_red.jpg",
  "textPrompt": "将商品颜色改为深蓝色",
  "modelType": 9
}
```

## 响应格式

```json
{
  "code": 200,
  "msg": null,
  "data": "https://example.com/product_blue.jpg",
  "result": {
    "fileUrlList": ["https://example.com/product_blue.jpg"],
    "taskId": 2118243882832912400
  }
}
```

- `code=200` 表示调用成功；**判断成功只看 `code`**，业务失败时 HTTP 状态码仍是 200，`code` 为 500 或 9999，原因在 `msg` 里，且不带 `result`
- `msg` 成功时为 `null`
- `data` 为换色后的图片 URL（为兼容已接入的调用方保留）
- `result.fileUrlList` 为结果图片 URL 数组，新接入优先读这个字段
- `result.taskId` 为本次生图主任务 ID，可凭它调用 `/api/v1/poster/queryTaskResult` 复查明细；它是 19 位长整数，用 JavaScript 等解析时按字符串处理，避免丢精度

返回结果应直接展示给用户，不要回读图片内容。

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| sourceUrl | - | 原图链接，只支持 1 张 |
| textPrompt | - | 换色提示词，如"将商品颜色改为深蓝色" |
| modelType | 9 | 模型类型：当前仅支持传 `9`（Flyelep Image 2） |

### 可选参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| prompt | - | 补充提示词，用于描述换色位置、不换色区域等，会与 `textPrompt` 拼接后一起下发 |
| additionalPrompt | - | `prompt` 的兼容字段，仅在 `prompt` 为空时生效，新接入直接用 `prompt` |
| replaceImageUrl | - | 颜色参考图，最多 1 张 |

### 参数映射规则

**sourceUrl**：
- 传入待换色商品的原图公网 URL
- 必须是图片直链，不要传网页地址
- 原图应尽量清晰展示商品主体和原始颜色
- 只传 1 张，不要用逗号拼接多张；多张原图需要逐张调用
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**textPrompt**：
- 文档将其标为必需；与场景替换、商品替换不同，本接口没有默认提示词，`textPrompt` 和 `prompt` 都不传时模型拿不到任何换色指令
- 直接描述目标颜色及必要约束
- 应尽量明确"将什么改成什么颜色"

推荐写法示例：

- `将商品颜色改为深蓝色`
- `把包包主体颜色改为奶油白，保留金属扣件颜色不变`
- `将耳机外壳换成哑光黑色，保持材质质感与光影不变`
- `把杯身改为浅绿色，保留品牌标识和背景不变`

**提示词边界**：
- 优先描述颜色，不要把换色需求扩写成换材质或换商品
- 如果用户只是想"更换商品"，应改用商品替换 skill
- 如果用户想"换背景"，应改用场景替换 skill

**prompt**：
- 与 `textPrompt` 是两个独立字段，服务端会把两者用中文逗号拼接后再下发
- 适合承载"只改哪个部位、哪些区域不要动"这类补充约束
- 只传 `prompt` 不传 `textPrompt` 时也能生效

**modelType**：
- 当前接口仅支持 `9`（Flyelep Image 2），必传
- 不传或传其他值会报「modelType 传入非法值，当前接口仅支持 9(Flyelep Image 2)」

**replaceImageUrl**：
- 可选，用于提供颜色参考图
- 只支持 1 张，传多张会被接口拒绝，报「该操作类型最多只能上传1张图片」

> **说明**：场景替换、商品替换、商品换色三个接口共用同一 DTO，由接口内部自动设置 `type` 字段，调用方无需传入 `type`。

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

### 示例 1：基础商品换色

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "sourceUrl": "https://example.com/product_red.jpg",
  "textPrompt": "将商品颜色改为深蓝色",
  "modelType": 9
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"sourceUrl":"https://example.com/product_red.jpg","textPrompt":"将商品颜色改为深蓝色","modelType":9}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"sourceUrl":"https://example.com/product_red.jpg","textPrompt":"将商品颜色改为深蓝色","modelType":9}'
```

### 示例 2：强调保留材质与光影的换色

**前置步骤**：向用户索取图片路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "sourceUrl": "https://example.com/product_watch.jpg",
  "textPrompt": "将表带改为深棕色皮革观感，保留金属表盘和整体光影不变",
  "modelType": 9
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"sourceUrl":"https://example.com/product_watch.jpg","textPrompt":"将表带改为深棕色皮革观感，保留金属表盘和整体光影不变","modelType":9}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"sourceUrl":"https://example.com/product_watch.jpg","textPrompt":"将表带改为深棕色皮革观感，保留金属表盘和整体光影不变","modelType":9}'
```

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| `msg` 为 `密钥无效!` / `密钥格式错误!` | `secretKey` 错误、被截断或已失效，向用户重新索取 |
| `code` 为 `9999`、`msg` 为 `服务繁忙，请稍后再试` | 最常见原因是漏传 `secretKey` 请求头，先自查请求头 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `原图URL不能为空` | 没传 `sourceUrl` |
| `sourceUrl` 无法访问 | 原图 URL 不是公网直链、已过期，或源站限制访问 |
| `modelType 传入非法值，当前接口仅支持 9(Flyelep Image 2)` | `modelType` 未传或不在支持范围，当前仅支持 `9` |
| `该操作类型最多只能上传1张图片` | `replaceImageUrl` 传了多张，商品换色只接受 1 张 |
| `点数不足` | 账户算力不足，让用户充值后再试，重试无效 |
| `msg` 以 `处理失败` 结尾 | 生成环节失败（原图无法下载、模型出错等），失败不扣算力，可稍后重试或换图 |
| 换色结果偏差较大 | `textPrompt` 过于模糊，可补充目标颜色、材质观感和保留项 |
| 局部也被错误换色 | 原图主体边界不清晰，可换更干净的源图或在提示词里强调保留范围 |
| 请求超时 | 图片较大或处理复杂时，可适当增大超时时间 |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集原图 URL（如用户提供本地文件，先按「本地文件上传」章节换取公网直链）
3. 与用户确认换色需求，构造 `textPrompt`，`modelType` 固定填 `9`
4. 在请求头中传入 `secretKey`，调用接口
5. 将返回的换色结果图片 URL 直接展示给用户

该接口支持 `textPrompt`，商品换色的结果高度依赖提示词描述质量。执行时应遵循：

1. 明确目标颜色
2. 明确保留项：材质、品牌标识、背景、光影、构图
3. 避免把"换色"写成"换商品"或"换背景"
4. 对多部件商品可明确指定仅修改哪个部位

当用户要求"同款不同色""把红色改成蓝色"时，优先使用此技能；如果用户想替换为完全不同的商品，应改用商品替换 skill。
