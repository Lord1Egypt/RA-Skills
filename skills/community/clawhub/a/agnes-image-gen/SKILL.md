---
name: agnes-image-gen
description: 使用 Agnes AI 的图片生成模型生成图片，支持文生图（agnes-image-2.1-flash）和图生图（agnes-image-2.0-flash）。支持自定义 API Key，用户可使用自己的 Agnes Key。优化重点：降低AI生成图片的"AI感"，增强自然真实感；优化中文配文逻辑连贯性、字体排版精美度，避免文字重影重叠。当用户说「用 Agnes 生成图片」「用 Agnes 画一张」「Agnes 生成」或明确要求使用 Agnes API 进行文生图/图生图时，加载本 skill。不消耗 WorkBuddy 积分，仅消耗 Agnes API 额度。
agent_created: true
---

# Agnes Image Gen

## 概述

调用 Agnes AI 的图片生成模型，支持两种模式：
- **文生图**：使用 `agnes-image-2.1-flash` 模型，根据文本描述生成图片
- **图生图**：使用 `agnes-image-2.0-flash` 模型，基于现有图片进行编辑和风格转换

通过 curl 直接调用 HTTP API，不走 WorkBuddy 的对话模型机制，因此**不消耗对话积分**。

## API Key 配置

### 默认 API Key
技能内置了一个默认 API Key，可直接使用，无需额外配置。

### 自定义 API Key
用户可以使用自己的 Agnes API Key，优先级高于默认 Key。

**设置方式**：
1. **环境变量**（推荐）：设置环境变量 `AGNES_API_KEY`
   ```bash
   # Windows PowerShell
   $env:AGNES_API_KEY = "your-api-key-here"
   
   # Linux/macOS
   export AGNES_API_KEY="your-api-key-here"
   ```

2. **直接指定**：在调用时明确告知使用自己的 API Key
   - 用户说：「用我的 Agnes Key 生成图片，Key 是 sk-xxx」
   - AI 应使用用户提供的 Key

**API Key 优先级**：
1. 用户明确提供的 Key → 最高优先级
2. 环境变量 `AGNES_API_KEY` → 次优先级
3. 技能内置默认 Key → 最低优先级（兜底）

**API Key 格式**：
- 通常以 `sk-` 开头
- 长度约 48-64 个字符
- 示例：`sk-8Rzd2yCbFzOi1vxojseH8C5D8w3u4aMdNWsPNzxk0G7339Cz`

### 获取 API Key
访问 [Agnes AI 官网](https://agnes-ai.com) 注册账号后，在控制台获取 API Key。

## 触发条件

当用户提出以下请求时加载本 skill：
- 「用 Agnes 生成一张……的图片」
- 「用 Agnes 画……」
- 「Agnes 图片生成」
- 「用这张图片生成……」（图生图）
- 「把这张图片改成……风格」（图生图）
- 明确要求使用 Agnes API 进行文生图或图生图

## 模型选择指南

### agnes-image-2.1-flash（文生图）
- **用途**：根据文本描述生成全新图片
- **特点**：生成速度快，支持多种风格
- **适用场景**：海报设计、插画创作、概念图生成

### agnes-image-2.0-flash（图生图）
- **用途**：基于现有图片进行编辑、风格转换、元素修改
- **特点**：保持原图构图，支持局部修改和整体风格转换
- **适用场景**：图片风格化、背景替换、元素添加/删除

## 工作流程

### 推荐：使用封装脚本（一条命令搞定）

脚本路径: `scripts/agnes_gen.py`

**文生图**:
```bash
python scripts/agnes_gen.py text2img --prompt "图片描述" --size 1024x1024 --n 1
```

**图生图**:
```bash
python scripts/agnes_gen.py img2img --image ./input.jpg --prompt "编辑指令" --size 1024x1024
```

脚本自动处理：重试、友好错误提示、下载图片到本地。无需手动执行任何额外步骤。

### 备用：手动 curl（不推荐，缺少重试和自动下载）

### 1. 文生图（agnes-image-2.1-flash）

```bash
# AGNES_API_KEY 应替换为实际的 API Key（用户提供的、环境变量中的、或内置默认值）
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "<用户描述的图片内容>",
    "n": 1,
    "size": "1024x1024"
  }'
```

**支持参数说明：**
- `model`: 固定为 `agnes-image-2.1-flash`
- `prompt`: 图片描述（支持中英文，中文效果已优化）
- `n`: 生成张数，默认为 1，最多支持 4 张
- `size`: 图片尺寸，支持 `1024x1024`、`1024x768`、`768x1024`、`512x512`

### 2. 图生图（agnes-image-2.0-flash）

```bash
# AGNES_API_KEY 应替换为实际的 API Key
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/edits" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -d '{
    "model": "agnes-image-2.0-flash",
    "image": "<base64编码的图片数据或图片URL>",
    "prompt": "<编辑指令描述>",
    "n": 1,
    "size": "1024x1024"
  }'
```

**支持参数说明：**
- `model`: 固定为 `agnes-image-2.0-flash`
- `image`: 原始图片（支持 base64 编码或 URL）
- `prompt`: 编辑指令（支持中英文）
- `n`: 生成张数，默认为 1
- `size`: 输出图片尺寸

### 3. 响应处理

API 响应格式示例：
```json
{
  "created": 1780468823,
  "data": [{
    "url": "https://storage.googleapis.com/agnes-aigc-test/images/...",
    "revised_prompt": "优化后的提示词（如有）"
  }],
  "usage": {
    "total_tokens": 0
  }
}
```

从 `data[0].url` 提取图片 URL。

### 4. 下载图片到本地

**Windows 环境**使用 PowerShell 下载：

```powershell
Invoke-WebRequest -Uri "<图片URL>" -OutFile "<保存路径>/agnes_output.png"
```

或使用 Python（跨平台）：

```python
import urllib.request
import os
from datetime import datetime

# 生成带时间戳的文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_path = os.path.join("<当前workspace路径>", f"agnes_{timestamp}.png")
urllib.request.urlretrieve(url, save_path)
```

若下载失败，可改用 HTML 页面直接引用远程 URL（图片通过 `<img>` 加载），再叠加 CSS 文字制成海报。

### 5. 展示给用户

- 调用 `preview_url` 展示图片文件
- 调用 `deliver_attachments` 交付图片附件

## 调用示例

### 示例 1：生成产品海报（文生图）

**用户请求**：「用 Agnes 生成一张科技感十足的产品发布会海报，主题是AI助手」

**调用命令**：
```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "科技感产品发布会海报，主题是AI助手，未来主义风格，蓝色调， holographic效果，现代简约设计",
    "n": 1,
    "size": "1024x1024"
  }'
```

### 示例 2：生成多张不同风格（文生图）

**用户请求**：「生成3张不同风格的咖啡店logo」

**调用命令**：
```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "咖啡店logo设计，简约现代风格，咖啡杯元素，温暖色调",
    "n": 3,
    "size": "1024x1024"
  }'
```

### 示例 3：图片风格转换（图生图）

**用户请求**：「把这张照片改成赛博朋克风格」

**准备工作**：
```python
import base64
import urllib.request

# 读取本地图片并转换为 base64
with open("input_image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
```

**调用命令**：
```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/edits" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -d '{
    "model": "agnes-image-2.0-flash",
    "image": "data:image/jpeg;base64,<base64编码数据>",
    "prompt": "转换为赛博朋克风格，霓虹灯光效，未来科技感，暗色调，高对比度",
    "n": 1,
    "size": "1024x1024"
  }'
```

### 示例 4：图片元素修改（图生图）

**用户请求**：「把图片中的天空改成星空」

**调用命令**：
```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/edits" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -d '{
    "model": "agnes-image-2.0-flash",
    "image": "https://example.com/original_image.jpg",
    "prompt": "将天空替换为璀璨星空，银河清晰可见，深蓝色调",
    "n": 1,
    "size": "1024x1024"
  }'
```

### 示例 5：中文文本优化示例

**用户请求**：「生成一张带有"新年快乐"字样的贺卡」

**优化后的 prompt**：
```
精美新年贺卡设计，主视觉为"新年快乐"艺术字体，金色书法风格，红色背景，烟花装饰，喜庆氛围，中国传统元素，高清精致
```

**调用命令**：
```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "精美新年贺卡设计，主视觉为"新年快乐"艺术字体，金色书法风格，红色背景，烟花装饰，喜庆氛围，中国传统元素，高清精致",
    "n": 1,
    "size": "1024x1024"
  }'
```

## 中文文本生成优化

### 最佳实践

1. **详细描述**：提供尽可能详细的描述，包括风格、颜色、氛围、元素等
2. **关键词组合**：使用逗号分隔多个关键词，如「科技感, 蓝色调, 未来主义, 简约设计」
3. **风格指定**：明确指定艺术风格，如「水彩画风格」「像素艺术」「3D渲染」
4. **质量修饰词**：添加质量相关的描述，如「高清」「精致」「专业级」
5. **构图指导**：描述构图方式，如「居中构图」「对称设计」「留白艺术」

### 中文 Prompt 模板

**产品海报**：
```
[产品类型]海报设计，[主题描述]，[风格]，[色调]，[氛围]，[装饰元素]，[质量描述]
```

**插画创作**：
```
[场景描述]，[人物/物体]，[动作/状态]，[艺术风格]，[色彩搭配]，[光影效果]，[细节描述]
```

**Logo 设计**：
```
[品牌/公司]logo设计，[核心元素]，[设计风格]，[色彩方案]，[象征意义]，[应用场景]
```

### 常见问题解决

**问题1**：中文字符显示不清晰
**解决方案**：在 prompt 中强调「清晰中文字体」「可读性」「高对比度」

**问题2**：生成的图片不符合预期
**解决方案**：使用更具体的描述，避免模糊词汇，添加「精确」「准确」等修饰词

**问题3**：需要特定风格
**解决方案**：明确指定风格名称，如「中国风水彩」「日系动漫」「欧美卡通」

## 降低AI感与优化中文配文

### 核心目标
生成更自然、更少AI味的图片，同时确保中文配文逻辑连贯、字体排版精美、无重影重叠。

### 降低AI感的关键技巧

#### 1. 增加自然与真实感描述
在 prompt 中添加以下关键词，引导模型生成更自然、有纹理、不完美的图像：
- **自然元素**：自然光线、有机形态、不规则纹理、真实质感、生活气息
- **避免AI特征**：避免过度完美、过度对称、过度光滑、过度渲染
- **细节丰富**：添加微小瑕疵、自然磨损、环境痕迹、光影变化

**示例 prompt 优化**：
- 原始：`科技感产品海报，蓝色调，未来主义风格`
- 优化：`科技感产品海报，蓝色调，未来主义风格，自然光线下的真实质感，有机形态设计，避免过度光滑渲染，带有细微环境纹理`

#### 2. 指定真实世界参考
使用真实世界中的风格、材质、场景作为参考：
- `真实照片风格，非数字渲染`
- `手工绘制质感，带有笔触痕迹`
- `胶片摄影颗粒感，自然色彩还原`
- `实物拍摄，非3D建模`

#### 3. 避免典型AI生成模式
明确排除常见的AI生成特征：
- `避免过度完美对称`
- `避免不自然的光滑表面`
- `避免不真实的颜色饱和度`
- `避免机械感过强的几何形状`

### 优化中文配文的关键技巧

#### 1. 逻辑连贯性
确保配文内容逻辑清晰、语义连贯：
- **明确主题**：清晰定义图片要表达的核心信息
- **结构化描述**：使用主谓宾结构，避免碎片化关键词堆砌
- **上下文关联**：确保文字与图片内容紧密相关

**示例**：
- 原始：`新年快乐，红色背景，烟花`
- 优化：`一张温馨的新年贺卡，主视觉为手写体"新年快乐"，红色背景上绽放着金色烟花，整体传达喜庆与祝福的氛围`

#### 2. 字体排版精美
指定字体风格和排版要求，确保文字美观易读：
- **字体风格**：书法体、手写体、印刷体、艺术字
- **排版要求**：清晰可读、层次分明、布局合理
- **质量强调**：高清锐利、无模糊、无锯齿

**示例 prompt 添加**：
```
主视觉为"新年快乐"高清书法字体，笔触清晰锐利，无重影无重叠，字体边缘干净利落，专业排版设计
```

#### 3. 避免文字重影与重叠
明确要求文字清晰，避免常见问题：
- **清晰度要求**：字体清晰锐利，无模糊、无重影
- **布局要求**：文字位置合理，不与其他元素重叠
- **对比度要求**：文字与背景对比鲜明，易于阅读

**示例 prompt 添加**：
```
文字清晰锐利，无重影无重叠，字体边缘干净，与背景对比鲜明，专业排版无错位
```

### 综合优化 Prompt 模板

#### 带文字的图片生成模板：
```
[场景/主题描述]，[风格/艺术形式]，[色调/氛围]，[主要文字内容]使用[字体风格]清晰展示，字体高清锐利无重影无重叠，[自然/真实感描述]，[避免AI特征]，[质量描述]
```

#### 示例：优化后的新年贺卡 prompt
```
温馨的新年贺卡设计，手绘插画风格，暖色调，主视觉为"新年快乐"高清书法字体，笔触清晰锐利无重影无重叠，自然光线下带有纸张纹理质感，避免过度完美渲染，整体传达喜庆与祝福的氛围，专业排版设计，高清精致
```

### 测试与迭代建议

1. **对比测试**：生成多个版本，对比AI感与自然感
2. **文字检查**：重点检查文字是否清晰、有无重影重叠
3. **细节观察**：检查纹理、光影、瑕疵是否自然
4. **迭代优化**：根据结果调整prompt中的关键词权重

## 错误处理

### 推荐方式：使用封装脚本

优先使用 `scripts/agnes_gen.py` 调用 API，脚本已内置以下能力：
- **自动重试**：网络故障或服务端临时错误（429/5xx）最多自动重试 3 次，指数退避
- **友好错误提示**：技术性错误自动翻译成大白话 + 明确的操作步骤
- **自动下载到本地**：图片生成后立刻下载，不依赖临时 URL

```bash
python scripts/agnes_gen.py text2img --prompt "一只可爱的猫" --size 1024x1024
```

### 常见错误及大白话攻略

脚本会根据错误类型给出对应提示，这里列出完整映射供参考：

| 技术错误 | 大白话解释 | 怎么做 |
|---------|-----------|--------|
| `invalid_api_key` | API Key 无效 | 登录 agnes-ai.com 控制台重新复制 Key（sk-开头那种），或者直接用内置 Key |
| `authentication_error` | 身份验证失败 | Key 可能复制漏了字符或已过期，重新获取一个试试；也可能是账户欠费 |
| `rate_limit_exceeded` | 请求太频繁被限速了 | 等几十秒会自动重试，不用手动操作。下次可以把一次生成的张数设大一点 |
| `model_not_found` | 模型名称不对或暂时下线 | 确认用的是 `agnes-image-2.1-flash`（文生图）或 `agnes-image-2.0-flash`（图生图） |
| `invalid_image_format` | 图片格式有问题 | 只支持 JPG/PNG，检查文件是否损坏或链接能否正常打开 |
| `prompt_too_long` | 描述内容太长了 | 精简一下，只留关键信息，一般中文 200 字以内没问题 |
| `network_error` | 连不上服务器 | 检查自己网络，或者 Agnes 那边抽风了，脚本会自动重试 |
| `timeout` | 请求超时 | 图片尺寸太大生成慢，试试 512x512；网络不好换个环境 |

### 手动 curl 时的错误处理

如果直接使用 curl（不用封装脚本），错误响应格式为：

```json
{
  "error": {
    "message": "错误描述",
    "type": "错误类型",
    "code": "错误代码"
  }
}
```

自行处理时参考上方表格，将技术错误翻译成用户能听懂的话，并且给出下一步怎么做。**不要只丢一个错误码给用户**。

## 注意事项

### 调用方式
- **推荐使用封装脚本** `scripts/agnes_gen.py`，自带自动重试、友好错误提示、自动下载。比裸调 curl 省心很多
- 支持自定义 API Key，用户可通过环境变量 `AGNES_API_KEY`、`--key` 参数、或直接提供
- 默认使用内置 API Key，无需额外配置即可使用

### 图片保存（重要）
- ⚠️ **图片 URL 来自 Google Cloud Storage，有效期短（通常几小时到一天）**
- ✅ **封装脚本已自动下载**，生成后图片立刻保存到本地，无需担心过期
- ❌ 如果用裸 curl，必须在生成后立即用 PowerShell 或 Python 下载到本地

### 品质优化
- 中文 prompt 已优化，可直接使用中文描述，效果良好
- 保存路径使用当前 workspace 目录（Windows 下自动适配）
- 图生图功能需要先将图片转换为 base64 编码或提供可访问的 URL
- 生成的图片可能包含 AI 生成的伪影，必要时可进行后期处理
- **降低AI感**：在 prompt 中明确要求自然、真实、有纹理的特征，避免过度完美渲染
- **中文配文质量**：强调字体清晰无重影，逻辑连贯，排版精美
- **质量检查**：生成后务必检查文字清晰度和整体自然感，必要时调整 prompt 重新生成

### 错误处理
- **不要只丢技术错误码给用户**，翻译成大白话并给出解决步骤
- 网络/服务端临时错误会自动重试 3 次，用户无感
- 限速错误也会自动等待后重试

## 最佳实践

1. **明确需求**：在调用前明确是文生图还是图生图
2. **优化 Prompt**：使用详细、具体的描述，避免模糊词汇
3. **降低AI感**：在prompt中添加自然、真实、有纹理的描述，避免过度完美渲染
4. **优化中文配文**：确保文字逻辑连贯，指定字体风格，强调清晰无重影
5. **选择合适的尺寸**：根据用途选择合适的图片尺寸
6. **批量生成**：需要多种方案时，使用 `n` 参数生成多张
7. **及时保存**：生成后立即下载保存，避免 URL 过期
8. **错误重试**：遇到错误时，根据错误类型采取相应措施
9. **质量检查**：生成后重点检查文字清晰度和整体自然感
