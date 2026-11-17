---
name: gen-hot-image
description: >-
  通过 Flyelep 爆款图片复刻 API，基于爆款图片风格生成产品复刻图。
  当用户要求复刻爆款图片、模仿参考图风格生成产品图时使用此技能。
---
# Flyelep 爆款图片复刻
通过 Flyelep AI Tool API 复刻爆款图片风格，将产品素材图融合到爆款参考图的视觉风格中。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**
**注意：此接口为异步接口，只返回任务ID，需要通过 queryTaskResult 接口获取最终结果。**

## API 接口信息

- **认证方式**: 在请求头中传入 `secretKey`（密钥需由用户在 Flyelep 开放平台申请：https://www.flyelep.cn/controlboard）
- **Content-Type**: `application/json`

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

### 创建任务

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotImage`
- **超时时间**: 建议 60-120 秒（获取任务结果需额外轮询）

### 查询结果

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult`
- **超时时间**: 建议 30 秒

## 请求 Body

创建任务：
```json
{
  "replaceUrl": "https://example.com/product1.png,https://example.com/product2.png",
  "sourceUrl": "https://example.com/hot_image1.png,https://example.com/hot_image2.png",
  "prompt": "突出产品卖点，增强视觉冲击力",
  "modelType": 9,
  "ratio": "1:1",
  "language": "中文简体"
}
```

查询结果：
```json
{
  "agentGenerateTaskId": "任务ID"
}
```

## 响应格式

创建任务（异步）：
```json
{
  "code": 200,
  "data": {
    "agentGenerateTaskId": "2072922328536604674"
  }
}
```

查询任务结果：
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
        "taskStatus": 2,
        "executeResult": "https://example.com/result2.png"
      }
    ]
  }
}
```

- `code=200` 表示调用成功
- `agentGenerateTaskId` 为异步任务ID，用于后续查询结果
- `taskStatus`: 0-待生成，1-生成中，2-生成成功，3-生成失败
- `executeResult` 为生成的图片URL
- 将结果图片逐个展示给用户，不要回读图片内容

## 参数说明

### 必传参数

> **重要**：以下必传参数必须通过询问用户获取，agent 不可自行填写。调用本技能时，应先向用户列出必传参数与可选参数表格，由用户确认或提供后再执行。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| replaceUrl | - | 产品素材图地址，多张用英文逗号分隔，总大小在10MB以内 |
| sourceUrl | - | 爆款参考图地址，最多10张，多张用英文逗号分隔 |
| prompt | - | 提示词，最多1000个字符长度 |
| modelType | - | 模型类型：`0`=gemini-2.5，`2`=Flyelep Nano 2（gemini-3.1），`3`=doubao-seedream，`9`=Flyelep Image 2 |
| ratio | - | 生图比例 |
| language | - | 生成语言 |

### 参数映射规则

**modelType**（模型类型）：
- `0`：gemini-2.5
- `2`：Flyelep Nano 2（gemini-3.1），按 30 算力/张计费
- `3`：doubao-seedream
- `9`：Flyelep Image 2，与 `0` 同属 10 算力/张计费档
- 只接受以上四个取值，传其它值接口直接拒绝

**ratio**（图片比例）：
- 支持：`1:1`、`3:2`、`2:3`、`3:4`、`4:3`、`4:5`、`5:4`、`16:9`、`9:16`、`21:9`
- 传其它比例接口报「生图比例不合法」

**language**（生成语言）：
- 中文简体、中文繁体、英文、俄语、日语、韩语、阿拉伯语、德语、西班牙语、法语、泰语、马来语、越南语、葡萄牙语、菲律宾语、印尼语、意大利语、荷兰语、波兰语、罗马尼亚语、匈牙利、保加利亚语
- 必须原样使用上面的中文标签（例如是 `英文` 而不是 `英语`），传其它写法会被拒绝

**replaceUrl**（产品素材）：
- 产品素材图地址，用于替换爆款图中的产品
- 多张图用英文逗号`,`分隔
- 总大小需在10MB以内
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

**sourceUrl**（爆款参考）：
- 爆款参考图片地址，用于提供风格参考
- 最多10张
- 多张图用英文逗号`,`分隔
- 如果用户提供本地文件路径，先按「本地文件上传」章节换取公网直链，再填入此参数

## 异步任务流程

> **重要**：本接口为异步接口，必须**先调用主接口获取 `agentGenerateTaskId`，然后调用 `queryTaskResult` 接口轮询任务结果**，不能省略轮询步骤。

1. 调用主接口（`generateHotImage`）提交任务，从响应中获取 `agentGenerateTaskId`
2. 使用 `agentGenerateTaskId` 调用 `queryTaskResult` 接口轮询任务结果（建议每5-10秒查询一次）
3. 当 `taskStatus=2` 时，表示生成成功，获取 `executeResult` 结果
4. 当 `taskStatus=3` 时，表示生成失败

> **轮询策略**：超时时间不超过5分钟

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

### 示例 1：完整流程 - 提交任务并查询结果

**前置步骤**：向用户索取产品素材图和爆款参考图的路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "replaceUrl": "https://example.com/product.png",
  "sourceUrl": "https://example.com/hot_image.png",
  "prompt": "突出产品卖点，增强视觉冲击力",
  "modelType": 9,
  "ratio": "1:1",
  "language": "中文简体"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"replaceUrl":"https://example.com/product.png","sourceUrl":"https://example.com/hot_image.png","prompt":"突出产品卖点，增强视觉冲击力","modelType":9,"ratio":"1:1","language":"中文简体"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行创建任务请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotImage" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

步骤 4：使用返回的 `agentGenerateTaskId` 创建查询请求 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "agentGenerateTaskId": "2072922328536604674"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"agentGenerateTaskId":"2072922328536604674"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 5：执行查询请求（每5-10秒轮询，直到 `taskStatus=2`）：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 30 --data-binary @payload_temp.json
```

步骤 6：清理临时文件：
```bash
rm payload_temp.json
```

**macOS/Linux**：

创建任务：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotImage" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"replaceUrl":"https://example.com/product.png","sourceUrl":"https://example.com/hot_image.png","prompt":"突出产品卖点，增强视觉冲击力","modelType":9,"ratio":"1:1","language":"中文简体"}'
```

查询结果（每5-10秒轮询，直到 `taskStatus=2`）：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 30 --data-binary '{"agentGenerateTaskId":"2072922328536604674"}'
```

### 示例 2：多张产品素材复刻

**前置步骤**：向用户索取产品素材图和爆款参考图的路径或 URL。如用户提供本地文件，先按「本地文件上传」章节换取公网直链。

**Windows/PowerShell**：

步骤 1：创建 `payload_temp.json`（两种方式任选其一）：

方式 A（使用 Write 工具）：
```json
{
  "replaceUrl": "https://example.com/product1.png,https://example.com/product2.png",
  "sourceUrl": "https://example.com/hot1.png,https://example.com/hot2.png",
  "prompt": "保持爆款图的配色和构图，将产品自然融入场景",
  "modelType": 2,
  "ratio": "3:4",
  "language": "英文"
}
```

方式 B（无 Write 工具，PowerShell 执行）：
```powershell
[System.IO.File]::WriteAllText("payload_temp.json", '{"replaceUrl":"https://example.com/product1.png,https://example.com/product2.png","sourceUrl":"https://example.com/hot1.png,https://example.com/hot2.png","prompt":"保持爆款图的配色和构图，将产品自然融入场景","modelType":2,"ratio":"3:4","language":"英文"}', [System.Text.UTF8Encoding]::new($false))
```

步骤 2：执行创建任务请求：
```bash
curl.exe --% -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotImage" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary @payload_temp.json
```

步骤 3：清理临时文件：
```bash
rm payload_temp.json
```

步骤 4：使用返回的 `agentGenerateTaskId` 查询结果（参考示例 1 步骤 4-6）

**macOS/Linux**：

创建任务：
```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/aiTool/generateHotImage" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 120 --data-binary '{"replaceUrl":"https://example.com/product1.png,https://example.com/product2.png","sourceUrl":"https://example.com/hot1.png,https://example.com/hot2.png","prompt":"保持爆款图的配色和构图，将产品自然融入场景","modelType":2,"ratio":"3:4","language":"英文"}'
```

查询结果（参考示例 1 的查询结果命令，替换 `agentGenerateTaskId`）

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| replaceUrl/sourceUrl 格式错误 | 多个URL用英文逗号分隔，不是JSON数组 |
| 素材图超过10MB | 压缩产品素材图大小 |
| 参考图超过10张 | 减少sourceUrl中的图片数量 |
| prompt 超过1000字符 | 缩短提示词内容 |
| 服务繁忙（9999错误码） | 稍后重试 |
| taskStatus=3 生成失败 | 检查素材图质量，尝试更换图片或调整prompt |

## 执行流程

1. **向用户询问 `secretKey`**（API 密钥必须由用户提供，agent 不可自行填写）
2. 收集产品素材图 URL 和爆款参考图 URL（如用户提供本地文件，先按「本地文件上传」章节换取公网直链）
3. 与用户确认复刻需求，构造 `prompt`，选择 `modelType`、`ratio`、`language`
4. 在请求头中传入 `secretKey`，调用创建任务接口，获取 `agentGenerateTaskId`
5. 使用 `agentGenerateTaskId` 轮询查询结果接口（每5-10秒一次），直到 `taskStatus=2`
6. 将返回的结果图片逐个展示给用户

复刻时，prompt 应指导AI：
- 保持爆款图的整体风格、配色和构图
- 将产品自然地融入到场景中
- 突出产品卖点和关键信息

**示例prompt：**
- "保持爆款图的配色和构图，将产品自然融入场景"
- "突出产品卖点，增强视觉冲击力"
- "延续原图的电商促销风格，产品主体突出"
- "保留原图的氛围感，让产品成为视觉焦点"
