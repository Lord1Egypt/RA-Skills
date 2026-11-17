# Dog Slide

> AI 驱动的多格式 SVG 演示文稿生成系统 — 将源文档转换为高质量 SVG 页面，通过多角色协作生成，并导出为 PPTX。

## 项目简介

Dog Slide 是一个完整的 AI 演示文稿生成流水线。它可以将 PDF、DOCX、PPTX、Excel、网页等多种格式的源文档转换为结构化的 Markdown，然后通过策略师（Strategist）、图片生成器（Image Generator）、执行器（Executor）等多角色协作，逐页生成高质量 SVG 演示页面，最终导出为可编辑的 PowerPoint 文件。

**核心能力：**
- 多格式源文档导入（PDF / DOCX / PPTX / Excel / 网页 / Markdown）
- 多角色协作生成（策略规划 → 图片生成 → 页面执行 → 质量检查）
- 15 种 AI 图片生成后端支持
- 4 种网络图片搜索源
- 71 个图表模板 + 7,980 个 SVG 图标库
- SVG 实时预览编辑器
- PPTX 导出（含动画）+ TTS 语音旁白

## 核心流程

```
源文档 → 创建项目 → [模板] → 策略师 → [图片生成] → 执行器实时预览 → 质量检查 → 后处理 → 导出 PPTX
```

**8 步流水线：**

| 步骤 | 阶段 | 说明 |
|------|------|------|
| 1 | 源文档转换 | 将 PDF/DOCX/PPTX/Excel/网页转为 Markdown |
| 2 | 创建项目 | 初始化项目目录结构 |
| 3 | 模板选择 | 选择布局模板或自由设计（可选） |
| 4 | 策略规划 | 策略师生成大纲、设计规范（颜色/字体/图标/图片） |
| 5 | 图片获取 | AI 生成或网络搜索配图（可选） |
| 6 | 页面执行 | 逐页生成 SVG 页面，支持实时预览 |
| 7 | 质量检查 | 自动 SVG 质量验证 + 视觉自查 |
| 8 | 导出 | SVG → PPTX（含动画），可选 TTS 旁白 |

## 安装前提

### Python 环境

- **Python 3.10+**（推荐 3.13）

### 安装依赖

```bash
cd <skill-dir>
pip install -r requirements.txt
```

主要依赖包括：

| 依赖 | 用途 |
|------|------|
| `python-pptx` | SVG 转 PPTX 导出 |
| `edge-tts` | 默认 TTS 语音旁白（免费，无需 API Key） |
| `svglib` + `reportlab` | SVG 转 PNG（Office 兼容模式） |
| `PyMuPDF` | PDF 转 Markdown |
| `mammoth` | DOCX 转 Markdown |
| `openpyxl` | Excel 转 Markdown |
| `Pillow` + `numpy` | 图片处理 |
| `requests` + `beautifulsoup4` | 网页抓取 |
| `google-genai` | Gemini 图片生成后端 |
| `openai` | OpenAI 兼容图片生成后端 |
| `flask` | SVG 实时预览编辑器 |

**可选系统依赖：**
- `cairo`（macOS: `brew install cairo`）— 用于 CairoSVG，完整的渐变/滤镜支持
- `pandoc`（macOS: `brew install pandoc`）— 用于 .doc/.odt/.rtf 等小众格式转换

## 配置说明

### 配置文件

Dog Slide 的图片生成、图片搜索和 TTS 功能需要配置 API 密钥。配置方式有三种（按优先级读取第一个存在的文件）：

1. 当前工作目录下的 `.env`
2. 技能根目录下的 `.env`
3. `~/.dog-slide/.env`（用户级配置）

**快速开始：**

```bash
cp .env.example .env
# 编辑 .env，填入你的 API 密钥
```

### 图片生成后端

通过 `IMAGE_BACKEND` 变量切换后端，只需配置你使用的那个：

| 后端 | 变量 | 说明 |
|------|------|------|
| `openai` | `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL` | OpenAI / OpenAI 兼容 API（推荐） |
| `gemini` | `GEMINI_API_KEY`, `GEMINI_MODEL` | Google Gemini |
| `qwen` | `QWEN_API_KEY`, `QWEN_MODEL` | 阿里通义万相 |
| `zhipu` | `ZHIPU_API_KEY`, `ZHIPU_MODEL` | 智谱 GLM-Image |
| `volcengine` | `VOLCENGINE_API_KEY`, `VOLCENGINE_MODEL` | 火山引擎豆包 Seedream |
| `minimax` | `MINIMAX_API_KEY`, `MINIMAX_MODEL` | MiniMax |
| `stability` | `STABILITY_API_KEY` | Stability AI |
| `bfl` | `BFL_API_KEY` | Black Forest Labs (FLUX) |
| `ideogram` | `IDEOGRAM_API_KEY` | Ideogram |
| `siliconflow` | `SILICONFLOW_API_KEY` | SiliconFlow |
| `fal` | `FAL_KEY` | fal.ai |
| `replicate` | `REPLICATE_API_TOKEN` | Replicate |
| `openrouter` | `OPENROUTER_API_KEY` | OpenRouter |
| `modelscope` | `MODELSCOPE_API_KEY` | ModelScope |
| `apimart` | 使用 OPENAI_* 变量 | APIMart (OpenAI 兼容) |

**示例配置（OpenAI）：**

```env
IMAGE_BACKEND=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-image-2
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 网络图片搜索

| 来源 | 变量 | 说明 |
|------|------|------|
| Openverse | 无需 Key | 免费，质量不稳定 |
| Wikimedia | 无需 Key | 免费 |
| Pexels | `PEXELS_API_KEY` | 商业图库风格，推荐 |
| Pixabay | `PIXABAY_API_KEY` | 商业图库风格，推荐 |

### TTS 语音旁白

`edge-tts` 为默认后端，**无需 API Key**。如需更高质量的云端旁白：

| 后端 | 变量 | 说明 |
|------|------|------|
| ElevenLabs | `ELEVENLABS_API_KEY` | 高质量语音合成 |
| MiniMax | `MINIMAX_API_KEY` | 支持音色复刻 |
| Qwen | `QWEN_API_KEY` | 通义语音合成 |
| CosyVoice | `COSYVOICE_API_KEY` | 支持音色复刻 |

## 使用方式

### 触发词

在 AI 助手中使用以下触发词激活技能：

- "做PPT" / "生成PPT" / "制作演示文稿"
- "create PPT" / "make presentation"
- "dog-slide"

### 基本用法

1. **准备源文档**：提供 PDF、DOCX、PPTX、Excel 文件或网页 URL
2. **启动流水线**：告诉 AI "用这个文档做一份PPT"
3. **按步骤确认**：在策略规划、大纲审核、页面审核等关键节点确认
4. **导出 PPTX**：最终生成可编辑的 PowerPoint 文件

### 脚本工具

所有脚本位于 `scripts/` 目录，也可独立使用：

```bash
# PDF 转 Markdown
python scripts/source_to_md/pdf_to_md.py input.pdf -o output.md

# 项目管理
python scripts/project_manager.py init my-project

# 图片生成
python scripts/image_gen.py --prompt "a tech background" --output bg.png

# SVG 转 PPTX
python scripts/svg_to_pptx.py project_dir/ -o output.pptx

# SVG 实时预览编辑器
python scripts/svg_editor/server.py
```

## 文件结构

```
dog-slide/
├── SKILL.md                 # 主技能定义（8步流水线）
├── README.md                # 本文件
├── .env.example             # 配置模板（复制为 .env 使用）
├── requirements.txt         # Python 依赖
│
├── scripts/                 # Python 脚本工具
│   ├── source_to_md/        # 源文档转 Markdown
│   ├── image_backends/      # 15 个图片生成后端
│   ├── image_sources/       # 4 个图片搜索源
│   ├── tts_backends/        # TTS 语音后端
│   ├── svg_finalize/        # SVG 后处理
│   ├── svg_to_pptx/         # SVG 转 PPTX
│   ├── pptx_to_svg/         # PPTX 转 SVG
│   ├── svg_editor/          # SVG 实时预览编辑器
│   ├── config.py            # 统一配置模块
│   └── ...                  # 其他工具脚本
│
├── references/              # 参考文档
│   ├── *.md                 # 角色定义、技术标准、布局规范
│   ├── image-palettes/      # 14 种配色方案
│   ├── image-renderings/    # 19 种渲染风格
│   ├── image-type-templates/ # 15 种图片类型模板
│   └── ai-image-comparison/ # 49 张参考图片
│
├── templates/               # 模板资源
│   ├── icons/               # 7,980 个 SVG 图标（Tabler + Phosphor + Chunk）
│   ├── charts/              # 71 个图表模板
│   ├── brands/              # 品牌预设 (Anthropic, Google)
│   └── layouts/             # 10 个通用布局模板
│
└── workflows/               # 10 个独立工作流定义
```

## 注意事项

1. **API 密钥安全**：请勿将 `.env` 文件提交到版本控制或分享给他人。`.env.example` 仅包含占位符，可安全分享。

2. **品牌模板**：本发布版本已排除企业专属品牌模板（中国电信、中国电建、中汽研、招商银行、重庆大学等）和品牌 Logo 图标集（Simple Icons），仅保留通用布局模板和通用图标。SKILL.md 中对品牌模板的引用仅作为示例说明，不影响核心功能。如需品牌 Logo，可通过 AI 图片生成功能获取。

3. **图标库**：包含 7,980 个 SVG 图标，来自 Tabler（填充/描边）、Phosphor（双色）、Chunk（填充）等开源图标集，涵盖通用 UI、商务、科技等场景。

4. **Office 兼容性**：PPTX 导出默认使用 PNG + SVG 双格式，确保所有 Office 版本正常显示。安装 `cairosvg` 可获得更好的渐变/滤镜渲染效果。

5. **性能建议**：处理大型文档（100+ 页）时，建议分批执行并在每个 BLOCKING 节点仔细确认，避免上下文压缩导致的风格漂移。

## 许可证

本技能遵循 MIT-0 许可证。图标库来自各自的开源许可证（Tabler MIT、Phosphor MIT、Chunk MIT 等）。
