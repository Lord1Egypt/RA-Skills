---
name: aicraft-skill
description: >
    爱创AI平台（www.51aic.com）电商AI内容创作助手。当用户有以下任何需求时，**必须**使用此技能：

    - 电商作图、商品图生成、主图套图、详情图制作
    - AI生成图片、AI绘画、AI作图、Agent模式智能生成
    - AI试衣、AI试鞋、AI试戴、虚拟试穿
    - 商品精修、去水印、商品换色、服装去皱
    - 图片翻译、商品替换背景、商品平铺图
    - 换姿势、换表情、去牛皮癣/去除杂物
    - AI视频生成、商品讲解视频、带货视频、短视频制作
    - AI详情图生成、商品详情页、详情页规划
    - 风格复刻、风格迁移、参考图风格生成
    - 资产管理、素材管理、历史作品查看/下载/删除
    - 提到"爱创"、"51aic"、"aicraft"、"大泽AI"
    - 任何需要上传图片进行AI处理/编辑/生成的电商场景

    此技能帮助用户通过爱创AI平台的API完成图片生成、视频生成、图片编辑、详情图生成、风格复刻、资产管理等任务。
    支持18种图片生成模式、AI视频生成、AI详情图生成、风格复刻和资产管理。
---

# 爱创 AI 平台技能

## 概述

爱创 AI 平台（https://www.51aic.com?source=agents）是面向电商商家的AI内容创作平台，提供AI图片生成、AI视频生成、AI详情图生成、风格复刻、商品精修、虚拟试穿等全场景AI作图功能。

本技能允许用户在 AI 对话中直接调用爱创 AI 平台的服务，无需手动访问网页。

## 图片展示规则（重要）

**所有生成出来的图片，必须使用缩略图方式展示，不要直接展示原图。**

展示方式：
1. **缩略图 URL**：使用 API 返回的 `thumbnailUrl` 字段（自带 `?x-oss-process=image/resize,w_530` 缩放参数），或在原图 URL 后拼接 `?x-oss-process=image/resize,w_530`
2. **自定义缩略尺寸**：如需更小的缩略图，可调整 resize 宽度参数（如 `w_200`、`w_300`）
3. **多图展示**：生成多张图片时，用缩略图网格排列展示，每张图附带原图下载链接
4. **单图展示**：先展示缩略图，再提供原图 URL 供用户查看大图

示例：
- 原图：`https://oss.fzputi.com/xxx/result.png`
- 缩略图（530px）：`https://oss.fzputi.com/xxx/result.png?x-oss-process=image/resize,w_530`

## 认证流程

**所有 API 调用都需要用户的 token。**

如果用户没有提供过 token，按以下步骤引导用户获取：

1. 请用户打开浏览器访问 https://www.51aic.com/openclaw?source=agents
2. 点击右上角登录（支持手机号验证码或微信扫码）
3. 登录成功后，页面会自动显示当前 token
4. 点击「复制 token」按钮，将 token 复制到剪贴板
5. 将复制的 token 粘贴到对话中

> **安全提示**：token 是用户的登录凭证，请勿在公共对话中分享。对话中的 token 仅在当前会话有效。

获取到 token 后，保存到上下文中，后续所有 API 调用自动使用。

## API 基础配置

```
主 API 地址:    https://aicraft.51aic.com
文件上传地址:   https://api.fzputi.com/ossmanager/api/Oss/UploadFileV2
图片 CDN:      https://oss.fzputi.com/
```

所有请求需要在 HTTP Header 中携带：`Token: <用户token>`

## 核心能力

### 1. 图片上传

如果用户提供了本地图片文件，需要先上传到平台 OSS。

**上传逻辑：**

1. 读取图片文件，转为 base64 编码
2. 拼接成 `data:image/jpeg;base64,...` 格式
3. 生成 OSS 路径：`tools/aiCraft/1m/YYYYMMDD/<uuid>.<ext>`
4. POST 到上传接口

**macOS/Linux：**

```bash
FILE_PATH="<图片路径>"
B64=$(openssl base64 -in "$FILE_PATH" | tr -d '\n')
EXT="${FILE_PATH##*.}"
[ "$EXT" = "jpeg" ] && EXT="jpg"
UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '-')
DATE=$(date +%Y%m%d)
MIME="image/$EXT"
[ "$EXT" = "jpg" ] && MIME="image/jpeg"

curl -s -X POST "https://api.fzputi.com/ossmanager/api/Oss/UploadFileV2" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d "{\"ossFilePath\":\"tools/aiCraft/1m/$DATE/$UUID.$EXT\",\"fileBase64\":\"data:$MIME;base64,$B64\"}"
```

**Windows：**

```powershell
$FilePath = "<图片路径>"
$B64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($FilePath))
$Ext = [System.IO.Path]::GetExtension($FilePath).TrimStart('.')
if ($Ext -eq "jpeg") { $Ext = "jpg" }
$UUID = [Guid]::NewGuid().ToString().Replace("-", "").ToLower()
$Date = Get-Date -Format "yyyyMMdd"
$MIME = "image/$Ext"
if ($Ext -eq "jpg") { $MIME = "image/jpeg" }

$Body = @{
    ossFilePath = "tools/aiCraft/1m/$Date/$UUID.$Ext"
    fileBase64 = "data:$MIME;base64,$B64"
} | ConvertTo-Json
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://api.fzputi.com/ossmanager/api/Oss/UploadFileV2" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

上传成功后返回的可能是完整 URL（`https://oss.fzputi.com/...`）或相对路径（`tools/aiCraft/1m/...`）。如果是相对路径，需拼接 CDN 前缀：`https://oss.fzputi.com/` + 相对路径。

### 2. 图片生成（18 种模式）

支持 18 种图片生成模式，详见 [references/image-modes.md](references/image-modes.md)。

**Agent 模式**（首选推荐）：AI 智能体辅助生成，上传参考图后 AI 自主分析意图、制定方案并生成优化图片。这是平台前端的默认首屏模式，交互最自然、智能程度最高。

当用户没有明确指定具体功能模式时（如 AI 试衣、去水印等），**优先引导用户使用 Agent 模式**：上传参考图 → 描述需求 → AI 分析生成。

Agent 模式**只能**通过 SSE 流式接口 `Task/GenerateAgentImageStream` 调用，参数为 `conversationId`、`imageUrls`（参考图URL数组）、`des`（prompt）、`ratio`、`taskJobId`，流式返回思考过程（意图分析→方案制定→生成结果）。不支持 `Task/Publish`。

**Agent SSE 接口调用要点（重要）：**

1. **端点**：`POST https://aicraft.51aic.com/api/v1/Task/GenerateAgentImageStream`
2. **参数**：
   ```json
   {
       "conversationId": "<会话ID>",
       "imageUrls": ["https://oss.fzputi.com/..."],
       "des": "用户需求描述",
       "ratio": "16:9",
       "taskJobId": "<uuid>"
   }
   ```
3. **响应格式**：SSE `data:` 行，每行是嵌套 JSON：
   ```
   data:{"code":200,"result":{"reasoningContent":null,"content":"{\"msg_type\":\"...\",\"data\":...}"},"msg":"success"}
   ```
   需要双层解析：外层 `result.content` 是 JSON 字符串，内层 `msg_type` 标识事件类型：
   - `status_change`：状态更新（"正在不断思考中..." → "正在生成图像中..." → "图片生成成功！"）
   - `task_info`：生成信息（含 `image_length`）
   - `status_change_daze`：详细计划（含 `tasks` 数组，含 AI 生成的 prompt、intention、ratio）
   - `workflow_finish`：工作流完成结果（含 `downloadUrl` 等信息）
   - `asset_outputs`：**最终图片URL**（含 `assetId` 和 `url` 字段，**这是提取图片URL的关键事件**）
   - `task_error`：错误信息

4. **图片URL提取**：从 `workflow_finish` 事件的 `data` 中用正则提取 `"url":"https://oss.fzputi.com/..."` ；也可从 `asset_outputs` 事件的 `data` 数组中取 `type=="image"` 的 `url` 字段。**注意**：`task_info` 事件只返回 `image_length`，不包含图片URL。
5. **读取方式**：Python 推荐用 `http.client.HTTPSConnection` 的 `response.read()` 一次性读取完整响应体（约 6KB），然后按 `\n` 分行解析 `data:` 前缀。**不要用** `urllib.request` 逐字节读取 SSE 流——会因缓冲导致读不到内容。
6. **taskJobId**：自行生成 UUID（无后缀），返回的 `assetId` 会带 `_YYYYMM` 后缀（如 `d73e42fa11b74ffaa220efd31e214331_202606`），但 `taskJobId` 参数传无后缀的即可。
7. **Conversation/Search 返回格式**：返回的是 `result.list[].id`（不是 `result.items[].conversationId`），注意字段名差异。

**Agent 模式完整 Python 实现（推荐，Windows/通用）：**

由于 Agent 模式的 SSE 流式接口有嵌套 JSON 格式，Python `http.client` 是最可靠的实现方式。中文 prompt 必须用 `json.dumps(payload, ensure_ascii=False)` 编码，避免中文乱码。

```python
import http.client, urllib.request, json, uuid, time, base64, os, sys, io, re

# Windows GBK 编码修复
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

TOKEN = "<用户token>"
BASE_API = "aicraft.51aic.com"

def api_post(url, payload, token):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8", "Token": token}
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def upload_image(file_path, token):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(file_path)[1].lstrip(".").lower()
    if ext == "jpeg": ext = "jpg"
    mime = "image/jpeg" if ext == "jpg" else f"image/{ext}"
    file_uuid = uuid.uuid4().hex
    date_str = time.strftime("%Y%m%d")
    oss_path = f"tools/aiCraft/1m/{date_str}/{file_uuid}.{ext}"
    payload = {"ossFilePath": oss_path, "fileBase64": f"data:{mime};base64,{b64}"}
    result = api_post("https://api.fzputi.com/ossmanager/api/Oss/UploadFileV2", payload, token)
    if result.get("code") == 200:
        oss_url = result["result"]
        if not oss_url.startswith("http"):
            oss_url = "https://oss.fzputi.com/" + oss_url
        return oss_url
    raise Exception(f"上传失败: {result}")

def get_conversation_id(token):
    result = api_post(
        "https://aicraft.51aic.com/api/v1/Conversation/Search",
        {"projectType": "IMAGE", "pageIndex": 1, "pageSize": 1,
         "sortField": "lastMessageAt", "sortType": "desc"}, token)
    if result.get("code") == 200 and result.get("result", {}).get("list"):
        return result["result"]["list"][0]["id"]
    raise Exception(f"查询会话失败: {result}")

def agent_generate(conv_id, image_urls, des, ratio, token):
    """Agent模式SSE生成，返回图片URL"""
    task_job_id = uuid.uuid4().hex
    payload = json.dumps({
        "conversationId": conv_id, "imageUrls": image_urls,
        "des": des, "ratio": ratio, "taskJobId": task_job_id
    }, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Token": token, "Accept": "text/event-stream", "Cache-Control": "no-cache"
    }
    conn = http.client.HTTPSConnection(BASE_API, timeout=180)
    conn.request("POST", "/api/v1/Task/GenerateAgentImageStream", body=payload, headers=headers)
    response = conn.getresponse()
    body = response.read().decode("utf-8", errors="replace")
    conn.close()

    # 解析SSE，提取图片URL
    result_image_url = None
    for line in body.split("\n"):
        line = line.strip()
        if not line.startswith("data:"): continue
        try:
            outer = json.loads(line[5:].strip())
            content_str = outer.get("result", {}).get("content", "")
            if not content_str: continue
            content = json.loads(content_str)
            msg_type = content.get("msg_type", "")
            data_val = content.get("data", "")

            if msg_type == "workflow_finish":
                # 从 workflow_finish 中用正则提取图片URL
                raw = json.dumps(data_val, ensure_ascii=False)
                urls = re.findall(r'"url"\s*:\s*"(https?://[^"]+\.png[^"]*)"', raw)
                for u in urls:
                    if 'generate' in u or 'aiplatform' in u:
                        result_image_url = u
                        break
            elif msg_type == "asset_outputs":
                if isinstance(data_val, list):
                    for item in data_val:
                        if item.get("type") == "image" and item.get("url"):
                            result_image_url = item["url"]
                            break
        except (json.JSONDecodeError, KeyError):
            pass
    return result_image_url

# 使用示例
oss_url = upload_image("<图片路径>", TOKEN)
conv_id = get_conversation_id(TOKEN)
image_url = agent_generate(conv_id, [oss_url], "用户需求描述", "16:9", TOKEN)
if image_url:
    thumb = image_url + "?x-oss-process=image/resize,w_530"
    print(f"缩略图: {thumb}")
    print(f"原图: {image_url}")
```

其他常用模式：

-   **自由创作**：通用图片生成，上传参考图并描述需求即可

API 端点：`POST https://aicraft.51aic.com/api/v1/Task/Publish`

> **业务规则（重要）**：提交生成任务时，必须先查询并复用现有的 `conversationId`，**一律不创建新的 conversation（批次）**。这样能保证所有记录在同一个会话下，查询历史时不会断档。
>
> 查询方式：`POST /api/v1/Conversation/Search`（projectType: IMAGE/VIDEO，按 lastMessageAt 倒序取第一条）

> **prompt 字段规则（重要）**：
>
> -   **Agent 模式 / 自由创作**：prompt 由用户自定义，是核心必填参数，描述想要什么图片
> -   **其他 16 种模式**（如 AI 试衣、去水印等）：有**固定的默认 prompt**（详见 [references/image-modes.md](references/image-modes.md)），不可为空，否则任务发布会失败（code: 999）
> -   部分模式（如换色、翻译、换表情）的 prompt 包含动态参数（颜色、语言、表情等），需要根据用户选择填充

请求体示例（自由创作）：

```json
{
    "conversationId": "",
    "projectType": "IMAGE",
    "mode": 1,
    "type": 2,
    "payload": {
        "aspectRatio": "auto",
        "count": 1,
        "prompt": "一件红色连衣裙，白色背景，电商商品图",
        "sceneMode": "free_creation",
        "referenceImages": [{ "key": "images", "index": 0, "url": "https://oss.fzputi.com/...", "description": "" }]
    }
}
```

### 3. AI 详情图生成

上传产品图，AI 自动分析并生成完整的电商商品详情页（含多张详情图）。

**流程：**

1. 创建批次 → AI 分析产品并生成详情页规划方案
2. 用户确认/编辑规划方案（可选）
3. 生成详情图 → 按模块逐张生成
4. 查询结果和下载

**核心 API：**

-   `POST /api/v1/DetailImage/CreateBatch` — 创建详情图批次，AI 生成规划方案
-   `POST /api/v1/DetailImage/GenerateBatchImages` — 确认规划后，生成详情图
-   `POST /api/v1/DetailImage/GetBatchDetail` — 查询批次详情和规划方案
-   `POST /api/v1/DetailImage/GetBatchTaskResults` — 查询生成结果
-   `POST /api/v1/DetailImage/GetImageTasksProgress` — 查询任务进度
-   `POST /api/v1/DetailImage/RemakeImage` — 重新生成单张图

**CreateBatch 参数：**

```json
{
    "batchId": "", // 首次创建为空，复刻时传入旧batchId
    "productInfo": "无线智能洗地机，集吸尘拖地自清洁于一体...", // 产品信息描述
    "productImageUrls": ["https://oss.fzputi.com/..."], // 产品图，1-6张
    "language": "简体中文", // 语言：简体中文/繁体中文/英语/日语/韩语/德语/法语/阿拉伯语/俄语/泰语/印尼语/越南语/马来语/西班牙语/葡萄牙语/巴西葡萄牙语
    "aspectRatio": "3:4", // 尺寸比例
    "moduleKeys": ["header", "product_showcase", "selling_points"] // 选择的详情页模块
}
```

**可用尺寸比例：** `1:1`, `2:3`, `3:2`, `3:4`（默认）, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

**可用语言：** 简体中文、繁体中文、英语、日语、韩语、德语、法语、阿拉伯语、俄语、泰语、印尼语、越南语、马来语、西班牙语、葡萄牙语、巴西葡萄牙语

**模块列表**（通过 `GET /api/v1/Template/GetDetailImageModules` 获取，各模块有名称、描述、示例图）：

-   模块是详情页的标准组成部分（如首图、产品展示、卖点、参数、使用场景等）
-   每个模块有 `key`、`displayName`、`description`、`sampleImageUrls`
-   部分模块默认选中
-   用户多选，至少保留 1 个模块

**积分消耗：** 每张详情图 **15 积分**，总积分 = 选中模块数量 × 15

**状态流转：**

-   `plan_pending` → `planning`（AI 生成规划中） → `plan_completed`（规划完成，待生成） → `image_generating`（生成中） → `completed` / `failed` / `partial_completed`

### 4. 风格复刻

上传参考设计图和产品图，AI 学习参考图的风格并应用到产品上，生成风格一致的新图片。

**核心 API：**

-   `POST /api/v1/StyleReplication/CreateBatch` — 创建风格复刻批次
-   `POST /api/v1/StyleReplication/RetryImage` — 重新生成单张图
-   `POST /api/v1/DetailImage/GetBatchProgress` — 查询批次进度
-   `POST /api/v1/DetailImage/GetBatchTaskResults` — 查询批次结果
-   `POST /api/v1/DetailImage/GetImageTasksProgress` — 查询图片任务进度

**CreateBatch 参数：**

```json
{
    "batchId": "", // 首次创建为空
    "styleReferenceImageUrls": ["https://oss.fzputi.com/..."], // 参考设计图（风格来源），最多16张
    "productImageUrls": ["https://oss.fzputi.com/..."], // 产品素材图，最多6张
    "aspectRatio": "1:1", // 尺寸比例
    "generateCount": 1, // 生成组数：1-3
    "detailRequirements": "添加新品上市文字，使用金色渐变风格..." // 补充要求（prompt，可为null）
}
```

**可用尺寸比例：** `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

**积分消耗：** 每张图 **15 积分**，总积分 = 参考图数量 × 组数 × 15

**状态流转：**

-   `plan_pending` → `planning` → `plan_completed` → `image_generating` → `completed` / `failed` / `partial_completed`

### 5. 视频生成

支持商品讲解视频、带货视频、促销视频等多种类型。

API 端点：`POST https://aicraft.51aic.com/api/v1/Task/Publish`

配置参数详见 [references/video-config.md](references/video-config.md)。

请求体示例（新手模式）：

```json
{
    "conversationId": "",
    "projectType": "VIDEO",
    "mode": 1,
    "type": 1,
    "payload": {
        "prompt": "介绍这款红色连衣裙的优点",
        "duration": 10,
        "orientation": "9:16",
        "size": "large",
        "language": "0",
        "videoType": "2",
        "videoChannel": "stable",
        "images": ["https://oss.fzputi.com/..."]
    }
}
```

### 6. 资产管理

查询和管理用户的历史生成作品（图片、视频、详情图、风格复刻）。

**核心 API：**

-   `POST /api/v1/Asset/Search` — 查询资产列表
-   `POST /api/v1/Asset/BatchDelete` — 批量删除资产

**资产类型 (assetType)：**
| 类型值 | 说明 |
|--------|------|
| `IMAGE` | AI 作图（单图生成） |
| `VIDEO` | AI 视频 |
| `DETAILIMAGE` | AI 详情图 |
| `StyleReplication` | 风格复刻 |

**Search 参数：**

```json
{
    "pageIndex": 1,
    "pageSize": 40,
    "assetType": "IMAGE",
    "sortField": "createTime",
    "sortType": "desc",
    "startTime": "2024-01-01", // 可选
    "endTime": "2024-01-02" // 可选
}
```

**返回字段：**

```json
{
  "assetId": "xxx",
  "fileUrl": "https://oss.fzputi.com/...",
  "thumbnailUrl": "https://oss.fzputi.com/...?x-oss-process=image/resize,w_530",
  "width": 1024,
  "height": 1024,
  "createdAt": "2024-01-01T12:00:00",
  "extra": {
    "referenceImages": [...],
    "prompt": "...",
    "sceneMode": "...",
    "aspectRatio": "..."
  }
}
```

### 7. 查询任务状态

生成任务提交后，返回 `taskJobId` 和 `conversationId`。可通过以下接口查询任务进度：

-   **任务进度**: `POST /api/v1/Task/GetProgress`（支持批量查询，见下方 API 调用参考）
-   **详情图/风格复刻进度**: `POST /api/v1/DetailImage/GetImageTasksProgress`

### 8. 查询积分

积分查询需要**两步认证**：

1. **获取支付认证 token**：用用户 token 调用 `/api/v1/PayPackage/GetToken`（body: `{"appType": 6}`），返回 `authorization`
2. **查询积分**：用 `authorization` 作为 `Authorization` header，访问支付 API `https://api.fzputi.com/payment/api/v1/Vas/GetQuantityByPackageType`

返回用户的剩余积分（会员积分 + 套餐积分）。

> **authorization 缓存**：有效期约 2 小时。在同一次对话中获取后**可复用**，不需要每次查积分都重新调用 GetToken。如后续调用返回 401，再重新获取。
>
> 注意：支付 API 与主 API 使用不同的认证机制。如果用户未主动要求查积分，可跳过此步骤，直接引用下方的积分消耗参考表告知用户大致消耗。

## 使用流程

### 图片生成流程

1. 确认用户已提供 token（如未提供，引导获取）
2. **默认推荐 Agent 模式**：当用户有参考图并描述需求时，优先使用 Agent 模式
    - 如用户只是泛化描述（"帮我做张商品图"、"生成海报"），按 Agent 模式处理：上传参考图 + 原样传递用户需求描述 → AI 自主分析生成
    - **重要**：Agent 模式下，将用户的原始需求直接作为 `des` 参数传给 `GenerateAgentImageStream`，让爱创 AI 自主理解，不要自己改写或理解用户意图
    - 如用户明确指定了具体功能模式（如 AI 试衣、去水印、换色等），切换到对应模式并使用其默认 prompt
3. **确认 prompt**：
    - Agent 模式：**原样传递用户需求**，不做额外解读（用户说"帮我生成一个海报"就传"帮我生成一个海报"）
    - 自由创作：由用户描述需求生成 prompt（核心必填参数）
    - 其他 16 种模式：使用对应模式的**默认 prompt**（见 [references/image-modes.md](references/image-modes.md)），如用户有特殊需求可在此基础上调整
    - 部分模式（换色/翻译/换表情等）需要额外确认动态参数（颜色/语言/表情等）
4. 询问参考图片
5. 如有本地图片，先调用上传接口
6. **Agent 模式**：调用 `GenerateAgentImageStream`（SSE 流式）；**其他模式**：调用 `Task/Publish`
7. 解析响应，提取图片 URL，**使用缩略图展示**（原图 URL + `?x-oss-process=image/resize,w_530`）
8. 告知用户可在 https://www.51aic.com/image/history?source=agents 查看

### 视频生成流程

1. 确认用户已提供 token
2. 询问视频类型（商品讲解/带货/促销等）
3. 询问参考图片和提示词
4. 确认视频配置（通道/比例/清晰度/时长/语言）
5. 如有本地图片，先调用上传接口
6. 构建并发送 Publish 请求
7. 返回任务提交结果

### AI 详情图生成流程

1. 确认用户已提供 token
2. 请用户上传产品图（1-6 张）
3. 询问产品信息描述（可选，也可使用 AI 帮写自动生成）
4. 确认语言和尺寸比例（默认：简体中文 + 3:4）
5. 获取模块列表，让用户选择需要的详情页模块
6. 告知积分消耗：模块数量 × 15 积分
7. 调用 `DetailImage/CreateBatch` 创建批次
8. AI 生成规划方案（约需几十秒），轮询 `GetBatchDetail` 等待 `plan_completed`
9. 规划完成后，向用户展示方案（模块列表和整体设计规范）
10. 用户确认后，调用 `DetailImage/GenerateBatchImages` 生成详情图
11. 轮询 `GetImageTasksProgress` 查询进度，完成后展示结果

### 风格复刻流程

1. 确认用户已提供 token
2. 请用户上传参考设计图（风格来源，最多 16 张）
3. 请用户上传产品素材图（最多 6 张）
4. 确认尺寸比例和生成组数（1-3 组，默认 1 组）
5. 询问补充要求（prompt，可选）
6. 告知积分消耗：参考图数量 × 组数 × 15 积分
7. 调用 `StyleReplication/CreateBatch` 创建批次
8. 轮询 `DetailImage/GetBatchProgress` 查询进度
9. 完成后展示结果

### 资产管理流程

1. 确认用户已提供 token
2. 询问要查询的资产类型（图片/视频/详情图/风格复刻）
3. 可选：确认日期范围、排序方式
4. 调用 `Asset/Search` 查询
5. 展示资产列表，支持告知下载链接
6. 如用户要求删除，调用 `Asset/BatchDelete`

## 积分消耗参考

| 功能                             | 积分消耗                        |
| -------------------------------- | ------------------------------- |
| 图片生成（自由创作等大多数模式） | 5 积分/张                       |
| 主图套图                         | 25 积分/套（5 张）              |
| AI 详情图                        | 15 积分/张（按模块数量计）      |
| 风格复刻                         | 15 积分/张（参考图数量 × 组数） |
| 视频生成（stable 5 秒）          | 150 积分                        |
| 视频生成（stable 10 秒）         | 200 积分                        |
| 视频生成（stable 15 秒）         | 260 积分                        |
| 视频生成（fast 5 秒）            | 100 积分                        |
| 视频生成（fast 10 秒）           | 150 积分                        |
| 视频生成（fast 15 秒）           | 200 积分                        |
| AI 优质帮写视频脚本              | 2 积分                          |
| 产品分析（AI 帮写）              | 1 积分                          |

在提交生成任务前，可引用上表告知用户所需积分。如用户明确要求查当前余额，再执行积分查询（需要两步认证，见"查询积分"部分）。如积分不足，告知用户需要充值。

## 错误处理

常见错误及处理方式：

| 错误码   | 含义              | 处理方式                                                                                                                    |
| -------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 401      | Token 无效或过期  | 引导用户重新获取 token                                                                                                      |
| 999      | 任务发布失败      | 常见原因：① prompt 为空或不符合模式要求（非 Agent/自由创作模式必须使用默认 prompt）；② 参数格式错误。检查 prompt 和各字段值 |
| 积分不足 | 积分不够生成      | 告知用户当前积分和所需积分                                                                                                  |
| 上传失败 | 图片格式/大小不符 | 检查图片格式(jpg/png/webp)和大小(≤10MB)                                                                                     |

## API 调用参考

以下是用 exec 工具直接调用 API 的示例。**macOS/Linux 用 `curl`，Windows 用 PowerShell `Invoke-RestMethod`**。

调用前需确保已在 Header 中携带 `Token: <用户token>`。

### 查询积分（两步认证，authorization 可复用约 2 小时）

**Step 1 — 获取支付认证 token：**

**macOS/Linux：**

```bash
AUTH=$(curl -s -X POST "https://aicraft.51aic.com/api/v1/PayPackage/GetToken" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{"appType": 6}' | grep -o '"result":"[^"]*"' | sed 's/"result":"//;s/"$//')
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = '{"appType": 6}'
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
$AuthRes = Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/PayPackage/GetToken" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
$AUTH = $AuthRes.result
```

**Step 2 — 查询积分余额：**

**macOS/Linux：**

```bash
curl -s -X POST "https://api.fzputi.com/payment/api/v1/Vas/GetQuantityByPackageType" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Authorization: $AUTH" \
  -d '{"ValueAddedServicesType": 4}'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = '{"ValueAddedServicesType": 4}'
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://api.fzputi.com/payment/api/v1/Vas/GetQuantityByPackageType" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Authorization"=$AUTH} -Body $BodyBytes
```

### 查询会话 ID（复用现有批次）

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/Conversation/Search" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{"projectType": "IMAGE", "pageIndex": 1, "pageSize": 1, "sortField": "lastMessageAt", "sortType": "desc"}'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = '{"projectType": "IMAGE", "pageIndex": 1, "pageSize": 1, "sortField": "lastMessageAt", "sortType": "desc"}'
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/Conversation/Search" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### 发布图片生成任务

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/Task/Publish" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{
    "conversationId": "<会话ID>",
    "projectType": "IMAGE",
    "mode": 1,
    "type": 2,
    "payload": {
      "aspectRatio": "auto",
      "count": 1,
      "prompt": "一件红色连衣裙，白色背景，电商商品图",
      "sceneMode": "free_creation",
      "referenceImages": []
    }
  }'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = @{
    conversationId = "<会话ID>"
    projectType = "IMAGE"
    mode = 1
    type = 2
    payload = @{
        aspectRatio = "auto"
        count = 1
        prompt = "一件红色连衣裙，白色背景，电商商品图"
        sceneMode = "free_creation"
        referenceImages = @()
    }
} | ConvertTo-Json -Depth 5
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/Task/Publish" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### 发布视频生成任务

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/Task/Publish" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{
    "conversationId": "<会话ID>",
    "projectType": "VIDEO",
    "mode": 1,
    "type": 1,
    "payload": {
      "prompt": "介绍这款红色连衣裙的优点",
      "duration": 10,
      "orientation": "9:16",
      "size": "large",
      "language": "0",
      "videoType": "2",
      "videoChannel": "stable",
      "images": ["https://oss.fzputi.com/..."]
    }
  }'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = @{
    conversationId = "<会话ID>"
    projectType = "VIDEO"
    mode = 1
    type = 1
    payload = @{
        prompt = "介绍这款红色连衣裙的优点"
        duration = 10
        orientation = "9:16"
        size = "large"
        language = "0"
        videoType = "2"
        videoChannel = "stable"
        images = @("https://oss.fzputi.com/...")
    }
} | ConvertTo-Json -Depth 5
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/Task/Publish" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### 查询任务进度

提交任务后返回 `taskJobId`。可通过 `Task/GetProgress` 查询任务状态，支持一次查多个。

-   图片任务 `taskType`: `2`
-   视频任务 `taskType`: `1`

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/Task/GetProgress" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{"conditions":[{"taskJobId":"<任务ID>","taskType":2}]}'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = '{"conditions":[{"taskJobId":"<任务ID>","taskType":2}]}'
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/Task/GetProgress" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### AI 详情图 — 创建批次

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/DetailImage/CreateBatch" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{
    "batchId": "",
    "productInfo": "无线智能洗地机，集吸尘拖地自清洁于一体",
    "productImageUrls": ["https://oss.fzputi.com/..."],
    "language": "简体中文",
    "aspectRatio": "3:4",
    "moduleKeys": ["header", "product_showcase", "selling_points"]
  }'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = @{
    batchId = ""
    productInfo = "无线智能洗地机，集吸尘拖地自清洁于一体"
    productImageUrls = @("https://oss.fzputi.com/...")
    language = "简体中文"
    aspectRatio = "3:4"
    moduleKeys = @("header", "product_showcase", "selling_points")
} | ConvertTo-Json
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/DetailImage/CreateBatch" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### AI 详情图 — 生成图片

规划方案确认后调用：

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/DetailImage/GenerateBatchImages" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{"batchid": "<batchId>"}'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = '{"batchid": "<batchId>"}'
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/DetailImage/GenerateBatchImages" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### AI 详情图 — 查询批次详情

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/DetailImage/GetBatchDetail" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{"batchId": "<batchId>"}'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = '{"batchId": "<batchId>"}'
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/DetailImage/GetBatchDetail" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### AI 详情图 — 查询任务进度

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/DetailImage/GetImageTasksProgress" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{"type": 1, "taskIds": ["<taskId1>", "<taskId2>"]}'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = '{"type": 1, "taskIds": ["<taskId1>", "<taskId2>"]}'
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/DetailImage/GetImageTasksProgress" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### 风格复刻 — 创建批次

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/StyleReplication/CreateBatch" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{
    "batchId": "",
    "styleReferenceImageUrls": ["https://oss.fzputi.com/ref1.jpg"],
    "productImageUrls": ["https://oss.fzputi.com/prod1.jpg"],
    "aspectRatio": "1:1",
    "generateCount": 1,
    "detailRequirements": "使用金色渐变风格，添加促销标签"
  }'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = @{
    batchId = ""
    styleReferenceImageUrls = @("https://oss.fzputi.com/ref1.jpg")
    productImageUrls = @("https://oss.fzputi.com/prod1.jpg")
    aspectRatio = "1:1"
    generateCount = 1
    detailRequirements = "使用金色渐变风格，添加促销标签"
} | ConvertTo-Json
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/StyleReplication/CreateBatch" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### 风格复刻 — 查询批次进度

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/DetailImage/GetBatchProgress" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{"batchIds": ["<batchId>"]}'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = '{"batchIds": ["<batchId>"]}'
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/DetailImage/GetBatchProgress" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### 资产管理 — 查询资产

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/Asset/Search" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{
    "pageIndex": 1,
    "pageSize": 40,
    "assetType": "IMAGE",
    "sortField": "createTime",
    "sortType": "desc"
  }'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = @{
    pageIndex = 1
    pageSize = 40
    assetType = "IMAGE"
    sortField = "createTime"
    sortType = "desc"
} | ConvertTo-Json
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/Asset/Search" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```

### 资产管理 — 批量删除

**macOS/Linux：**

```bash
curl -s -X POST "https://aicraft.51aic.com/api/v1/Asset/BatchDelete" \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Token: <token>" \
  -d '{"assetIds": ["<assetId1>", "<assetId2>"]}'
```

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Body = '{"assetIds": ["<assetId1>", "<assetId2>"]}'
$BodyBytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
Invoke-RestMethod -Uri "https://aicraft.51aic.com/api/v1/Asset/BatchDelete" -Method POST -Headers @{"Content-Type"="application/json; charset=utf-8"; "Token"="<token>"} -Body $BodyBytes
```
