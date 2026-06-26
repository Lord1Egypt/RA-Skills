---
name: ecommerce-image-suite
description: >
  电商套图生成助手。用户明确提出需要生成电商套图、商品主图、卖点图、场景图、模特图等图片内容时触发。
  支持国内平台（淘宝、京东、拼多多、抖音）与国际跨境平台（Amazon、独立站）的尺寸规范。
  触发示例：「帮我生成这件T恤的电商套图」「做一套淘宝主图」「生成亚马逊listing图片」。
  不应在用户仅上传图片但未明确提出图片生成需求时触发。
metadata: {"openclaw":{"emoji":"🛍️","requires":{"env":["DASHSCOPE_API_KEY"]},"primaryEnv":"DASHSCOPE_API_KEY","optionalEnv":["OPENAI_API_KEY","OPENAI_BASE_URL","OPENAI_MODEL","GEMINI_API_KEY","GEMINI_BASE_URL","GEMINI_MODEL","STABILITY_API_KEY","STABILITY_BASE_URL","STABILITY_MODEL","DASHSCOPE_BASE_URL","DASHSCOPE_MODEL","ARK_API_KEY","ARK_BASE_URL","ARK_MODEL"]}}
---

# 电商套图生成助手

## 概览

本 Skill 实现从「商品原始图片 + 卖点信息」到「完整电商套图」的一键生成流程：

```
① 上传商品图片（必须）+ 输入卖点信息（可选）
        ↓
② AI 视觉分析：提取商品主体，智能生成卖点文案（可编辑）
        ↓
③ 选择平台规范 + 套图类型（7种标准图）
        ↓
④ AI 生成每张图的详细 Prompt（可编辑）
        ↓
⑤ 调用图像生成 API，输出完整套图
```

---

## 第一步：收集输入信息

### 必须项
- **商品图片**：用户上传的原始商品图（平铺图/白底图/实物图均可）

### 可选项（若用户未提供，AI 将自动从图片中分析生成）
| 字段 | 说明 |
|------|------|
| 商品名称 | 如"卡通小狗印花宽松精梳棉短袖T恤" |
| 核心卖点 | 材质、版型、设计特点等 3-5 条 |
| 适用人群 | 如"追求舒适简约风的青少年" |
| 期望场景 | 如"校园日常、居家休闲、户外出游" |
| 规格参数 | 材质、颜色、版型、领型、袖长等 |

---

## 第二步：AI 分析与卖点生成

### 视觉分析步骤
1. 识别商品类型、颜色、款式、设计元素
2. 提取商品主体轮廓与关键视觉特征
3. 基于视觉特征推断材质、功能卖点
4. 生成结构化卖点（JSON格式，供后续图片生成使用）

### 卖点 JSON 结构
```json
{
  "product_name": "商品名称",
  "product_type": "服装/3C/家居/其他",
  "visual_features": ["白色", "圆领", "短袖", "卡通小狗印花"],
  "selling_points": [
    {"icon": "fabric", "en": "Combed Cotton", "zh": "精梳棉面料"},
    {"icon": "fit", "en": "Loose & Breathable", "zh": "宽松透气"},
    {"icon": "design", "en": "Cute Design", "zh": "萌趣设计"}
  ],
  "target_audience": "青少年、学生群体",
  "usage_scenes": ["校园", "居家", "户外"],
  "color": "白色",
  "material": "精梳棉"
}
```

> 📄 详细分析 Prompt 见 `references/analysis-prompts.md`

---

## 第三步：选择平台与套图配置

> 📄 各平台规范详见 `references/platforms.md`

### 平台选择
| 平台类型 | 平台 | 推荐尺寸 | 语言 |
|---------|------|---------|------|
| 国内 | 淘宝/天猫 | 800×800 (1:1) | 中文 |
| 国内 | 京东 | 800×800 (1:1) | 中文 |
| 国内 | 拼多多 | 750×750 (1:1) | 中文 |
| 国内 | 抖音/小红书 | 1080×1350 (4:5) 或 1:1 | 中文 |
| 国际 | Amazon | 2000×2000 (1:1) | 英文 |
| 国际 | 独立站/Shopify | 2000×2000 (1:1) 或 16:9 | 英文 |

### 标准套图（7种）
每种图的详细规格见 `references/image-types.md`

| # | 图片类型 | 核心目标 | 推荐位置 |
|---|---------|---------|---------|
| 1 | **白底主图** | 商品全貌展示，符合平台收录规则 | 第1张主图 |
| 2 | **核心卖点图** | 3大卖点图标化呈现 | 第2张 |
| 3 | **卖点图** | 单一核心卖点深度展示 | 第3张 |
| 4 | **材质图** | 面料/工艺特写，建立品质信任 | 第4张 |
| 5 | **场景展示图** | 生活方式场景，激发代入感 | 第5张 |
| 6 | **模特展示图** | 真人/AI模特穿搭，直观展示效果 | 第6张 |
| 7 | **多场景拼图** | 多场景适用性对比，提升决策 | 第7张 |

---

## 第四步：生成图片 Prompt

> 📄 各图类型的 Prompt 模板见 `references/image-types.md`

### Prompt 构建原则
1. **商品一致性**：所有图片必须保持商品颜色、结构、比例、细节不变
2. **背景差异化**：每张图背景/场景各不相同，形成完整故事线
3. **文字分离**：图片本身不含文字，文案通过后处理叠加（除非使用图像生成API支持文字）
4. **品质标准**：`photorealistic, high quality, studio lighting, 8K, commercial photography`

### Prompt 结构模板
```
[商品描述] + [版型/颜色/印花精确描述] + [场景/背景描述] + [光线/氛围] + [拍摄角度] + [品质词]
```

---

## 第五步：多供应商图像生成

> 📄 各供应商 API 接入详情见 `references/providers.md`

### 支持的图像生成供应商（5个）
| 供应商 | 默认模型 | 模型环境变量 | 国内可用 | 特点 |
|--------|---------|------------|---------|------|
| OpenAI | `dall-e-3` | `OPENAI_MODEL` | 需代理 | 高质量写实，细节清晰 |
| Google | `gemini-3.1-flash-image-preview` | `GEMINI_MODEL` | 需代理 | 原生图像生成，2K 输出 |
| Stability AI | `core` | `STABILITY_MODEL` | 需代理 | 精准控制构图 |
| 阿里云 | `qwen-image-2.0-pro` | `DASHSCOPE_MODEL` | ✅直连 | 同步接口，中文优化 |
| 字节跳动 | `doubao-seedream-5-0-260128` | `ARK_MODEL` | ✅直连 | 中文理解好，风格多样 |

> 模型名可通过 `--model` 参数、环境变量或默认值配置，优先级：`--model` > 环境变量 > 默认值。

### 供应商检测

```bash
python3 scripts/check_providers.py
```

输出 JSON 包含 `configured` 数组，显示哪些供应商已配置 API Key。

### 执行生图脚本

```bash
python3 scripts/generate.py \
  --product '{"product_description_for_prompt": "...", "selling_points": [...]}' \
  --provider tongyi \
  --types white_bg,key_features,selling_pt,material,lifestyle,model,multi_scene \
  --output-dir ./output/raw/
```

### generate.py 完整参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--product` | **必填**，商品 JSON 字符串 | — |
| `--provider` | **必填**，供应商：`openai` / `gemini` / `stability` / `tongyi` / `doubao` | — |
| `--api-key` | API Key，也可通过环境变量传入 | 环境变量 |
| `--base-url` | 自定义代理地址，也可通过 `*_BASE_URL` 环境变量传入 | 官方地址 |
| `--model` | 模型名称，也可通过 `*_MODEL` 环境变量传入 | 见供应商表 |
| `--types` | 逗号分隔的套图类型 | 全部 7 种 |
| `--output-dir` | 输出目录 | `./output/raw/` |

### 代理 API 使用示例

各供应商均支持通过 `--base-url` 或环境变量指定代理地址：

```bash
# Gemini 通过代理（代理使用 Bearer token 鉴权）
GEMINI_API_KEY="sk-proxy-key" \
GEMINI_BASE_URL="https://my-proxy.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  python3 scripts/generate.py --provider gemini --product '...'

# 通义通过代理
DASHSCOPE_API_KEY="sk-..." \
DASHSCOPE_BASE_URL="https://my-proxy.com/api/v1/services/aigc/multimodal-generation/generation" \
  python3 scripts/generate.py --provider tongyi --product '...'

# 切换模型版本
DASHSCOPE_MODEL="qwen-image-2.0" \
  python3 scripts/generate.py --provider tongyi --product '...'
```

## 第六步：文案叠加

使用 Pillow 将文案叠加到生成图片上：

```bash
python3 scripts/overlay.py \
  --input-dir ./output/raw/ \
  --product '{"selling_points": [...], "product_name_zh": "..."}' \
  --lang zh \
  --output-dir ./output/final/
```

### 叠加规范（各图类型）
- **白底主图 / 模特展示图**：无文案叠加
- **核心卖点图**：右侧区域，WHY CHOOSE US + 3个卖点标签，深色文字
- **卖点图**：左上主标题 + 左下两条副标题，深色文字
- **材质图**：右上主标题 + 右侧两条副标题，深色文字
- **场景展示图**：左上主标题 + 左下两条副标题，白色文字+阴影
- **多场景拼图**：顶部居中主标题 + 底部两侧场景标注，白色文字+阴影

> 📄 各图类型叠加坐标规范见 `references/providers.md`（Canvas规范部分）

---

## CLI 执行流程（Agent 调用）

Agent 或 CLI 环境下的完整流程：

```bash
# Step 1: 检测供应商配置
python3 scripts/check_providers.py

# Step 2: Agent 分析商品图片（Claude Vision），输出 product JSON

# Step 3: 执行生图
python3 scripts/generate.py \
  --product '{"product_description_for_prompt": "white T-shirt...", "selling_points": [...]}'  \
  --provider tongyi \
  --output-dir ./output/raw/

# Step 4: 文案叠加
python3 scripts/overlay.py \
  --input-dir ./output/raw/ \
  --product '{"product_description_for_prompt": "white T-shirt...", "selling_points": [...]}' \
  --lang zh \
  --output-dir ./output/final/
```

---

## 执行检查清单

- [ ] 商品图片已上传（必须）
- [ ] 商品卖点已生成或用户已填写
- [ ] 平台已选择（决定语言和尺寸）
- [ ] 套图类型已选择（至少1种）
- [ ] 所有 Prompt 已审核（可选）
- [ ] 图像生成 API 可用

---

## 参考文件索引

| 文件 | 内容 |
|------|------|
| `references/platforms.md` | 各平台尺寸规范、主图要求、文案风格指南 |
| `references/image-types.md` | 7种套图的详细视觉规格与 Prompt 模板 |
| `references/analysis-prompts.md` | AI商品分析与卖点提取的系统 Prompt |
| `references/providers.md` | 供应商 API 接入详情与文案叠加规范 |
| `scripts/check_providers.py` | 检测已配置供应商（读取环境变量） |
| `scripts/generate.py` | 调用图像生成 API（5个供应商，支持 `--model` / `--base-url` / `--api-key`） |
| `scripts/overlay.py` | Pillow 文案叠加（动态卖点 + 多语言） |

---

## API Key 配置

本 Skill 使用两类 API：

| 变量 | 用途 | 是否必需 |
|---|---|---|
| `DASHSCOPE_API_KEY` | 千问图像生成（国内直连） | ✅ 推荐 |
| `ARK_API_KEY` | 豆包 Seedream 图像生成（火山方舟，国内直连） | 可选 |
| `OPENAI_API_KEY` | DALL·E 3 图像生成（需代理） | 可选 |
| `GEMINI_API_KEY` | Gemini 原生图像生成（需代理） | 可选 |
| `STABILITY_API_KEY` | Stable Image Core（需代理） | 可选 |
| `*_BASE_URL` | 各供应商自定义代理地址（`OPENAI_BASE_URL` / `GEMINI_BASE_URL` 等） | 可选 |
| `*_MODEL` | 各供应商自定义模型名（`DASHSCOPE_MODEL` / `ARK_MODEL` / `GEMINI_MODEL` 等） | 可选 |

> **安全声明**：API Key 仅存于本地环境变量，直接调用各供应商官方 Endpoint，不经过任何第三方服务器中转。建议使用权限最小化的 Key，并定期轮换。

### 方式一：环境变量

```bash
# 至少配置一个图像供应商
export DASHSCOPE_API_KEY="sk-..."       # 阿里云 DashScope（国内直连，推荐）
export ARK_API_KEY="..."                # 字节跳动火山方舟（国内直连）
export OPENAI_API_KEY="sk-..."         # 需代理
export GEMINI_API_KEY="AIzaSy..."      # 需代理
export STABILITY_API_KEY="sk-..."      # 需代理

# 可选：自定义代理地址
export OPENAI_BASE_URL="https://my-proxy.com/v1"
export GEMINI_BASE_URL="https://my-proxy.com/gemini"
export DASHSCOPE_BASE_URL="https://my-proxy.com/dashscope"

# 可选：自定义模型名（不配置则使用默认值）
export DASHSCOPE_MODEL="qwen-image-2.0"       # 默认 qwen-image-2.0-pro
export ARK_MODEL="doubao-seedream-5-0-260128" # 默认 doubao-seedream-5-0-260128
export GEMINI_MODEL="gemini-3.1-flash-image-preview"  # 默认同此
```

加入 `~/.zshrc` 或 `~/.bashrc` 后永久生效。

### 方式二：OpenClaw 配置文件

在 `$OPENCLAW_CONFIG_PATH`（默认 `~/.openclaw/openclaw.json`）中配置 `apiKey`，对应 `primaryEnv`（即 `DASHSCOPE_API_KEY`）：

```json5
{
  skills: {
    entries: {
      "ecommerce-image-suite": {
        apiKey: "DASHSCOPE_API_KEY_HERE",
      },
    }
  },
}
```
