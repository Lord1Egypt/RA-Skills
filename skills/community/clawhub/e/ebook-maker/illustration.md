# 插图规范

本文件定义电子书插图的生成参数、风格模板和嵌入规则。修改此文件即可调整插图风格，无需改动主 Skill。

---

## 生成工具（三选一）

在 Stage 1 需求确认时，选择使用哪个生图工具。默认即梦 CLI。

| 工具 | 适合场景 | 前置条件 |
|------|--------|---------|
| **即梦 CLI**（默认） | 最方便，本地 CLI 直接调用 | `dreamina` 已登录 |
| **SeedDream API** | 质量最高（Seedream 5.0），稳定 | 需要 `ARK_API_KEY` |
| **Nano Banana** | 免费额度大，支持 4K | 需要 `GEMINI_API_KEY` |

---

### 选项 A：即梦 CLI（默认）

```
工具：dreamina CLI
模型：5.0
分辨率：2k（可选 4k）
```

**调用规则**：
- **必须串行调用**，不支持并发（并发会 EOF 失败）
- 每次生成前检查余额：`dreamina user_credit`
- 生成失败自动重试 1 次，仍失败则跳过并记录

**生成命令**：
```bash
dreamina text2image \
  --prompt="[STYLE_PREFIX], [内容描述]" \
  --ratio=3:2 \
  --model_version=5.0 \
  --resolution_type=2k \
  --poll=60
```

**结果提取**：从 JSON 响应的 `result_json.images[0].image_url` 获取图片 URL。

---

### 选项 B：SeedDream API（火山引擎方舟）

```
工具：HTTP API（curl 或 Python SDK）
模型：seedream-5-0-260128（最新）/ doubao-seedream-4-5-251128（稳定）
端点：https://ark.cn-beijing.volces.com/api/v3/images/generations
认证：ARK_API_KEY 环境变量
```

**调用前检查**：
```bash
echo $ARK_API_KEY  # 确认 API Key 已配置
```

**curl 调用**：
```bash
curl -s "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  --max-time 120 \
  -d '{
    "model": "seedream-5-0-260128",
    "prompt": "[STYLE_PREFIX], [内容描述]",
    "size": "2K",
    "response_format": "url",
    "watermark": false
  }'
```

**Python SDK 调用**：
```python
# pip install --upgrade "volcengine-python-sdk[ark]"
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ["ARK_API_KEY"]
)
response = client.images.generate(
    model="seedream-5-0-260128",
    prompt="[STYLE_PREFIX], [内容描述]",
    size="2K",
    response_format="url"
)
image_url = response.data[0].url
```

**结果提取**：`data[0].url`（链接约 24 小时过期，需及时下载）

**注意事项**：
- 支持 1-4 张图同时生成（`num_images` 参数）
- 可选尺寸：`1K` / `2K` / `4K` 或自定义 WxH（如 `1920x1080`）
- 生成失败不扣费
- 限速约 100 RPM

---

### 选项 C：Nano Banana（Google Gemini 图像生成）

```
工具：Gemini API（curl 或 Python SDK）
模型：gemini-3.1-flash-image-preview（Nano Banana 2，推荐）
      gemini-3-pro-image-preview（Nano Banana Pro，最高质量）
端点：https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent
认证：GEMINI_API_KEY 环境变量
```

**禁止使用 Nano Banana 1**（`gemini-2.5-flash-image`）。只能用 v2 或 Pro。如果过载，等待或切换即梦/SeedDream，绝不降级到 v1。

**调用前检查**：
```bash
echo $GEMINI_API_KEY  # 确认 API Key 已配置
```

**curl 调用**：
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 120 \
  -d '{
    "contents": [{"parts": [{"text": "Generate an image in 3:2 landscape aspect ratio: [STYLE_PREFIX], [内容描述]"}]}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {
        "aspectRatio": "3:2",
        "imageSize": "2K"
      }
    }
  }'
```

**Python SDK 调用**：
```python
# pip install google-genai
from google import genai
from google.genai import types
import base64

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="Generate an image in 3:2 landscape aspect ratio: [STYLE_PREFIX], [内容描述]",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="3:2", image_size="2K"),
    ),
)
# 提取图片
for part in response.candidates[0].content.parts:
    if hasattr(part, "inline_data"):
        with open("output.png", "wb") as f:
            f.write(base64.b64decode(part.inline_data.data))
```

**结果提取**：图片以 base64 内嵌在响应中（`candidates[0].content.parts[].inline_data.data`），需解码保存。

**注意事项**：
- 免费额度：60 RPM，500 张/天
- 可选尺寸：`512` / `1K` / `2K` / `4K`（4K 仅 Nano Banana 2）
- 比例写在 prompt 文本中更可靠（API 参数偶尔不生效）
- 图片保存到 `~/Downloads/NanoBanana生成图片/`（本地 Skill 默认路径）

---

## 通用调用规则

- 单次电子书最多生成 12 张插图
- 生成失败自动重试 1 次，仍失败则跳过并记录
- 不同工具之间可以混用（如即梦生成大部分，SeedDream 补几张高质量的）
- 所有工具生成的图片统一走后续的下载、压缩、嵌入流程

---

## 插图数量规划

| 书的篇幅 | 建议插图数 | 分布策略 |
|---------|----------|---------|
| 8-10 章 | 5-6 张 | 每 2 章之间 1 张 |
| 11-15 章 | 7-9 张 | 关键章节衔接处各 1 张 |
| 16+ 章 | 10-12 张 | 每 1-2 章之间 1 张 |

### 位置选择优先级

1. 章节之间的自然断点（最优）
2. 章节内较长的空白区域
3. 封面（可选）
4. 末尾引导页前（可选）

### 不放插图的位置

- 表格正上方或正下方（视觉冲突）
- 代码块中间
- 提示框紧邻处

---

## 比例选择

| 插图位置 | 推荐比例 | 效果说明 |
|---------|---------|---------|
| 章节间隔（横幅式） | 21:9 | 宽幅条状，像视觉分隔符，不占纵向空间 |
| 章节间隔（标准） | 16:9 | 略高于 21:9，信息量更大 |
| 正文配图 | 3:2 | 经典横向比例，适合叙事性插图 |
| 封面主图 | 1:1 | 居中展示，稳重 |
| 封面主图（竖向） | 3:4 | 适合人物或纵向构图 |
| 末尾引导页 | 1:1 | 配合居中排版 |

**用户指定比例时，以用户为准。**

---

## 风格模板系统

### 模板结构

每张插图的 prompt = `STYLE_PREFIX` + `内容描述` + `补充修饰词`

```
STYLE_PREFIX + ", " + CONTENT + ", " + MODIFIERS
```

### STYLE_PREFIX（风格前缀）

默认风格前缀：

```
Flat vector illustration, soft pastel purple and blue color palette, white background, no text, minimal clean style, friendly and approachable vibe
```

### 主色调方案

根据书的主题自动选择（或由用户指定）：

| 主题类型 | 主色 + 辅色 | 适合场景 |
|---------|-----------|---------|
| 技术/编程 | purple and blue | 代码、开发、AI |
| 设计/创意 | pink and coral | 设计、美学、品牌 |
| 商业/增长 | blue and green | 创业、营销、数据 |
| 教育/学习 | orange and teal | 教程、课程、知识 |
| 健康/生活 | green and warm yellow | 健康、生活方式 |
| 通用 | purple and teal | 不确定时的安全选择 |

### MODIFIERS（补充修饰词库）

按需求选用，不要全部堆叠：

| 感觉 | 关键词 |
|------|--------|
| 亲和力 | kawaii, cute, friendly, warm, cozy |
| 专业感 | geometric, structured, organized, precise |
| 科技感 | digital, futuristic, glowing, tech |
| 简约感 | minimalist, flat, clean, simple, sparse |
| 自然感 | organic, soft, natural, gentle |

### 禁用关键词

以下关键词会导致风格不一致或过于复杂，**不要使用**：

```
photorealistic, gradients, soft shadows, 3D, detailed,
complex, realistic, textured, ornate, busy, cluttered,
heavy, dark, moody, dramatic
```

---

## 风格锚定流程

### Step 1：生成风格前缀

根据书的主题，组装 STYLE_PREFIX：

```python
STYLE_PREFIX = f"Flat vector illustration, soft pastel {主色} and {辅色} color palette, white background, no text, minimal clean style, {亲和力/专业感修饰词}"
```

### Step 2：生成锚定图

用第一张插图的内容 + STYLE_PREFIX 生成锚定图：

```bash
dreamina text2image \
  --prompt="{STYLE_PREFIX}, {第一张图内容描述}" \
  --ratio=3:2 \
  --model_version=5.0 \
  --resolution_type=2k \
  --poll=60
```

### Step 3：用户确认

展示锚定图给用户，确认风格满意后继续。

如果用户要求调整，修改 STYLE_PREFIX 后重新生成锚定图。

常见调整方向：
- "更卡通" → 加 kawaii, cute
- "更专业" → 去掉 kawaii, 加 geometric, structured
- "换配色" → 修改主色辅色
- "更简单" → 加 sparse, minimal, fewer elements
- "更丰富" → 加 detailed scene, multiple elements

### Step 4：批量生成

锚定图确认后，用同一个 STYLE_PREFIX 逐个生成其余插图。

---

## 图片处理

### 下载

```bash
curl -sL --max-time 30 --retry 3 \
  -o "/tmp/ebook-imgs/img${i}.png" "${image_url}"
```

注意：字节跳动 CDN 偶发 SSL 错误（LibreSSL 兼容问题）。
失败 3 次后跳过，不阻塞流程。

### 压缩

```bash
sips --resampleWidth ${WIDTH} "input.png" \
  --out "output.jpg" \
  -s format jpeg \
  -s formatOptions ${QUALITY}
```

| 比例 | 缩小宽度 | JPEG 质量 | 目标大小 |
|------|---------|----------|---------|
| 21:9 / 16:9 | 800px | 80 | ≤ 60KB |
| 3:2 / 4:3 | 800px | 80 | ≤ 80KB |
| 1:1 | 600px | 80 | ≤ 50KB |
| 3:4 / 9:16 | 500px | 80 | ≤ 60KB |

### 文件组织

```
插图文件放在 HTML 同目录，用相对路径引用。
命名：img1.jpg, img2.jpg, ...（按插入顺序编号）
```

---

## 嵌入规则

### HTML 标签

```html
<!-- 标准配图 -->
<img class="ebook-img" src="img1.jpg" alt="描述文字">

<!-- 横幅图 -->
<img class="ebook-img banner" src="img2.jpg" alt="描述文字">
```

### 插入位置

插在章节 `</div>` 闭合标签之后、下一个 `<div class="chapter">` 之前：

```html
</div>  <!-- 上一章结束 -->

<img class="ebook-img" src="img3.jpg" alt="描述">

<!-- ========== 下一章 ========== -->
<div class="chapter">
```

### alt 文字

每张图都要有简短的 alt 描述，用于：
- 无障碍（屏幕阅读器）
- 图片加载失败时的回退文字
- 格式：动词 + 名词，如"人与 AI 协作编程"、"火箭发射代表部署上线"

---

## 记录模板

每次生成插图后，在工作报告中记录：

```markdown
| # | submit_id | prompt 摘要 | 比例 | 状态 | 用于位置 |
|---|-----------|-----------|------|------|---------|
| 1 | xxxx | 人与AI协作 | 3:2 | 成功 ✅ | Ch01→Ch02 |
| 2 | xxxx | 积木搭建 | 21:9 | 成功 ✅ | Ch03→Ch04 |
| 3 | xxxx | 数据传递 | 3:2 | 下载失败 ❌ | 跳过 |
```
