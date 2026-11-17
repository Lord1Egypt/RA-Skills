---
name: agnes-image-gen
description: 使用 Agnes AI 升级版图像生成模型 agnes-image-2.1-flash 生成图片。同时支持文生图（text-to-image）与图生图（image-to-image）。当用户说「用 Agnes 生成图片」「用 Agnes 画一张」「Agnes 生成」「用这张图生成/改成……」或明确要求使用 Agnes API 进行文生图/图生图时，加载本 skill。不消耗 WorkBuddy 积分，仅消耗 Agnes API 额度（当前图像生成免费）。
agent_created: true
---

# Agnes Image Gen

## 概述

调用 Agnes AI 的升级版图像生成模型 **`agnes-image-2.1-flash`**（Sapiens AI 出品）。该模型同时支持：

- **文生图（Text-to-Image）**：根据文本提示词生成全新图像
- **图生图（Image-to-Image）**：基于输入图像进行转换、重绘、风格化编辑，并尽量保留原始构图

通过 curl 直接调用 HTTP API，不走 WorkBuddy 的对话模型机制，因此**不消耗对话积分**。当前图像生成定价为 **$0 / 张**。

## 触发条件

当用户提出以下请求时加载本 skill：
- 「用 Agnes 生成一张……的图片」
- 「用 Agnes 画……」
- 「Agnes 图片生成」
- 「用这张图片生成……」「把这张图片改成……风格」「给这张图换个背景」（图生图）
- 明确要求使用 Agnes API 进行文生图或图生图

## 核心能力

- **高信息密度图像**：适合复杂场景、丰富构图、多层视觉元素（精细场景、复杂环境、丰富构图）
- **构图保留**：图生图编辑时尽量保留原始构图与主体布局
- **灵活尺寸控制**：使用 `1K` / `2K` / `3K` / `4K` 档位，配合宽高比
- **URL / Base64 输出**：支持图像 URL 或 Base64 数据返回
- **适用场景**：创意设计、营销内容、产品可视化、社交媒体素材、图像转换（风格迁移 / 场景重打光 / 背景变换）

## API Reference

### Endpoint（双端点容灾）

脚本自动按以下顺序尝试，前一个访问不了就切到下一个，**无需手动干预**：

| 优先级 | Endpoint | 说明 |
|--------|----------|------|
| 1（主） | `https://apihub.agnes-ai.com/v1/images/generations` | 国际主端点 |
| 2（容灾） | `https://apihub.agnes-ai.cn/v1/images/generations` | **国内容灾端点**：主端点 TCP 不可达时自动切换（国内网络访问 Agnes 更稳） |

- 调用前会做轻量连通性探测（TCP 层，8s 超时），主端点不可达时**立即跳过**而非空等，再尝试国内网关。
- 端点可达但请求失败（限速/5xx）会在该端点内重试，耗尽后才跳到下一端点。
- 运行结束会打印「本次使用: <实际端点>」，方便确认走的是哪个。

> 注意：文生图与图生图**共用同一端点** `/v1/images/generations`，不再使用 `/v1/images/edits`。

### 请求头

```
-H "Authorization: Bearer YOUR_API_KEY"
-H "Content-Type: application/json"
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称，固定为 `agnes-image-2.1-flash` |
| `prompt` | string | 是 | 图像生成或图像编辑的文本指令 |
| `size` | string | 是 | 输出尺寸档位，推荐 `1K` / `2K` / `3K` / `4K`；兼容 `1024x768` 这类历史精确写法（不支持的尺寸可能被标准化） |
| `ratio` | string | 否 | 与档位式 `size` 配合的宽高比，支持 `1:1`、`3:4`、`4:3`、`16:9`、`9:16`、`2:3`、`3:2`、`21:9`，默认 `1:1` |
| `image` | string[] | 图生图必填 | 输入图像数组（**注意：放在 `extra_body.image` 中**，见下方图生图示例） |
| `return_base64` | boolean | 否 | 文生图需要以 Base64 返回时设为 `true` |
| `extra_body` | object | 否 | 高级工作流附加参数（见下） |
| `extra_body.response_format` | string | 否 | 输出格式：`url` 或 `b64_json` |
| `extra_body.image` | string[] | 图生图必填 | 输入图像数组，支持公共图像 URL 或 `data:image/...;base64,...` Data URI |

### 尺寸与宽高比（输出尺寸参考）

为获得可预期的输出尺寸，建议将 `size` 与 `ratio` 配合使用：

| Ratio | 1K | 2K | 3K | 4K |
|-------|-----|-----|-----|-----|
| `1:1` | 1024x1024 | 2048x2048 | 3072x3072 | 4096x4096 |
| `3:4` | 864x1152 | 1728x2304 | 2592x3456 | 3456x4608 |
| `4:3` | 1152x864 | 2304x1728 | 3456x2592 | 4608x3456 |
| `16:9` | 1312x736 | 2624x1472 | 3936x2208 | 5248x2944 |
| `9:16` | 736x1312 | 1472x2624 | 2208x3936 | 2944x5248 |
| `2:3` | 832x1248 | 1664x2496 | 2496x3744 | 3328x4992 |
| `3:2` | 1248x832 | 2496x1664 | 3744x2496 | 4992x3328 |
| `21:9` | 1568x672 | 3136x1344 | 4704x2016 | 6272x2688 |

> 若请求 `1920x1080` / `2560x1440` 这类非原生精确尺寸，服务会自动映射到最接近的档位与宽高比（如 16:9 的 `1K` 输出为 `1312x736`）。需要标准显示器素材时建议请求 `size:"2K"` + `ratio:"16:9"`，再下游裁剪。

## 工作流程

### 1. 文生图（Text-to-Image）

```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer REDACTED-SECRET" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "<用户描述的图片内容>",
    "size": "2K",
    "ratio": "1:1",
    "extra_body": {
      "response_format": "url"
    }
  }'
```

- `size` 支持档位式（`1K`/`2K`/`3K`/`4K`）或兼容精确写法（`1024x1024` 等）
- 需要 Base64 时把 `extra_body.response_format` 改为 `b64_json`，或用顶层 `return_base64: true`

### 2. 图生图（Image-to-Image）

图生图**同样调用 `/v1/images/generations`**，输入图像通过 `extra_body.image` 传入（数组，支持 URL 或 Data URI）：

```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer REDACTED-SECRET" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "将白天街道场景改为电影级赛博朋克夜景，添加霓虹招牌和湿滑路面倒影，保留原始街道布局与建筑形状",
    "size": "2K",
    "extra_body": {
      "image": ["https://example.com/input-image.png"],
      "response_format": "url"
    }
  }'
```

- 输入图像为数组，可放多个（多图合成），每个元素为公共 HTTPS URL 或 `data:image/png;base64,...`
- 输入图像 URL 必须可公开访问（无需登录/cookie）；不可公开时改用 Data URI Base64
- **不需要**传递 `tags: ["img2img"]`

### 3. 响应处理

URL 输出：
```json
{
  "created": 1780000000,
  "data": [{
    "url": "https://storage.googleapis.com/agnes-aigc/xxx.png",
    "b64_json": null,
    "revised_prompt": null
  }]
}
```

Base64 输出：
```json
{
  "created": 1780000000,
  "data": [{
    "url": null,
    "b64_json": "iVBORw0KGgoAAAANSUhEUgAA...",
    "revised_prompt": null
  }]
}
```

- URL 输出：从 `data[0].url` 提取
- Base64 输出：从 `data[0].b64_json` 解码保存

### 4. 下载图片到本地

**URL 输出**（PowerShell）：
```powershell
Invoke-WebRequest -Uri "<图片URL>" -OutFile "<保存路径>/agnes_output.png"
```

**URL 输出**（Python，跨平台，带时间戳）：
```python
import urllib.request, os
from datetime import datetime
url = "<图片URL>"
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
save_path = os.path.join("<workspace路径>", f"agnes_{ts}.png")
urllib.request.urlretrieve(url, save_path)
```

**Base64 输出**（Python）：
```python
import base64, os
from datetime import datetime
b64 = "<data[0].b64_json>"
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
save_path = os.path.join("<workspace路径>", f"agnes_{ts}.png")
with open(save_path, "wb") as f:
    f.write(base64.b64decode(b64))
```

> 图片 URL 来自 Google Cloud Storage，有访问时效，应尽快下载到本地。若下载失败，可改用 HTML 页面直接引用远程 URL（`<img>` 加载）再叠加 CSS 文字制成海报。

### 5. 展示给用户

- 调用 `preview_url` 展示图片文件
- 调用 `deliver_attachments` 交付图片附件

## 调用示例

### 示例 1：软件宣传海报（文生图，档位+宽高比）

**用户请求**：「用 Agnes 生成一张科技感产品发布会海报，主题 AI 助手」

```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer REDACTED-SECRET" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "科技感产品发布会海报，主题是AI助手，未来主义风格，蓝色调，holographic效果，现代简约设计",
    "size": "2K",
    "ratio": "1:1",
    "extra_body": { "response_format": "url" }
  }'
```

### 示例 2：多张不同风格（文生图，n 参数）

```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer REDACTED-SECRET" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "咖啡店logo设计，简约现代风格，咖啡杯元素，温暖色调",
    "size": "1K",
    "extra_body": { "response_format": "url" }
  }'
```

> 需要多张时，部分场景可用 `n` 参数（旧写法）；当前档位式请求建议单张循环获取多种方案。

### 示例 3：图片风格转换（图生图，URL 输入）

**用户请求**：「把这张照片改成赛博朋克风格」

```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer REDACTED-SECRET" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "转换为赛博朋克风格，霓虹灯光效，未来科技感，暗色调，高对比度，保留原构图",
    "size": "2K",
    "extra_body": {
      "image": ["https://example.com/photo.jpg"],
      "response_format": "url"
    }
  }'
```

### 示例 4：图片元素修改（图生图，Base64 Data URI 输入）

**用户请求**：「把图片中的天空改成星空」

```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer REDACTED-SECRET" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "将天空替换为璀璨星空，银河清晰可见，深蓝色调，保留原主体与构图",
    "size": "2K",
    "extra_body": {
      "image": ["data:image/png;base64,<BASE64_HERE>"],
      "response_format": "b64_json"
    }
  }'
```

### 示例 5：中文文本优化示例（含中文字样）

**用户请求**：「生成一张带『新年快乐』字样的贺卡」

**优化后的 prompt**：
```
精美新年贺卡设计，主视觉为"新年快乐"艺术字体，金色书法风格，红色背景，烟花装饰，喜庆氛围，中国传统元素，高清精致
```

```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer REDACTED-SECRET" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "精美新年贺卡设计，主视觉为'新年快乐'艺术字体，金色书法风格，红色背景，烟花装饰，喜庆氛围，中国传统元素，高清精致",
    "size": "1K",
    "extra_body": { "response_format": "url" }
  }'
```

## 中文文本生成优化

### 官方推荐提示词结构

**文生图**：`[主体] + [场景/环境] + [风格] + [光照] + [构图] + [质量要求]`
```
日出时分薄雾峡谷上方的发光浮空城市，电影级写实风格，广角构图，丰富的建筑细节，柔和的金色光线，高视觉密度
```

**图生图**：`[改变要求] + [新风格/场景] + [添加或移除的元素] + [需要保留的元素]`
```
将白天街道场景改为电影级赛博朋克夜景，添加霓虹招牌和湿滑路面倒影，同时保留原始街道布局、相机角度和主要建筑形状。
```

**高信息密度图像**：清晰描述视觉层次结构（主要主体、背景环境、重要次要细节、风格、光照、构图约束）
```
建在悬崖上的大型奇幻港口城市，数百艘小船，层叠的石桥，发光的窗户，远山，多云的日落天空，电影级奇幻写实风格，广角构图，丰富的建筑细节，高视觉密度
```

### 最佳实践

1. **详细描述**：风格、颜色、氛围、元素、光照、构图尽量写全
2. **关键词组合**：逗号分隔多个关键词，如「科技感, 蓝色调, 未来主义, 简约设计」
3. **风格指定**：明确风格名称，如「水彩画风格」「像素艺术」「3D渲染」「电影级写实」
4. **质量修饰词**：「高清」「精致」「专业级」「高视觉密度」
5. **构图指导**：「居中构图」「对称设计」「留白艺术」「广角构图」
6. **尺寸策略**：标准方图用 `size:"1K"`+`ratio:"1:1"`；横幅/封面用 `size:"2K"`+`ratio:"16:9"`；手机壁纸用 `9:16`

### 常见问题解决

- **中文字符显示不清晰**：prompt 中强调「清晰中文字体」「可读性」「高对比度」
- **图片不符合预期**：使用更具体描述，避免模糊词汇，加「精确」「准确」
- **需要特定风格**：明确风格名称，如「中国风水彩」「日系动漫」「欧美卡通」
- **需要精确显示器分辨率**（如 1920x1080）：用 `size:"2K"`+`ratio:"16:9"`，下游裁剪

## 错误与故障排除

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `model_not_found` | 模型名错误 | 确认使用 `agnes-image-2.1-flash` |
| `rate_limit_exceeded` | 调用频率过高 | 等待后重试，降低并发 |
| `invalid_image_format` | 图片格式/编码错误 | 确保 JPEG/PNG，Base64 编码正确 |
| `prompt_too_long` | 提示词过长 | 精简，保留关键描述 |
| 请求超时 | 生成耗时数秒到数十秒 | 客户端超时设为 `60s-360s` |
| 输入图像 URL 无法访问 | 私有/需登录 | 改用 Data URI Base64 |

### 高频坑（官方强调）

1. **不要顶层放 `response_format`**：应放在 `extra_body.response_format`
   - ❌ `{"model":..., "response_format": "url"}`
   - ✅ `{"model":..., "extra_body": {"response_format": "url"}}`
2. **图生图不要传 `tags: ["img2img"]`**：只需在 `extra_body.image` 提供输入图像
3. **图生图缺少 image**：`extra_body.image` 为必填数组
4. **文生图三必填**：`model` + `prompt` + `size`

### 错误响应格式

```json
{
  "error": {
    "message": "错误描述",
    "type": "错误类型",
    "code": "错误代码"
  }
}
```

## 注意事项

- API Key 已在请求中硬编码，无需用户额外提供（如需自定义，替换 `Authorization` 中的 Bearer 值）
- 图片 URL 来自 Google Cloud Storage，有访问时效，应尽快下载到本地
- 若 API 返回错误，如实报告给用户，不做猜测
- 中文 prompt 已优化，可直接用中文描述，效果良好
- 图生图统一走 `/v1/images/generations`，输入图像放 `extra_body.image`
- 生成的图片可能含 AI 伪影，必要时可后期处理
- 标准价格 `$0.003/张`，**当前免费 `$0/张`**

## 最佳实践

1. **明确需求**：调用前明确文生图还是图生图
2. **优化 Prompt**：用详细、具体描述，遵循官方提示词结构
3. **选尺寸档位**：用 `1K/2K/3K/4K` + `ratio` 获得可预期输出
4. **及时保存**：生成后立即下载，避免 URL 过期
5. **错误重试**：按错误类型对应处理；超时调大客户端超时时间
6. **图生图保留构图**：prompt 中显式写「保留原始构图/主体布局」
