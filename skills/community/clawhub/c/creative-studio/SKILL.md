---
name: creative-studio
description: >-
  Use when users ask to create or edit product images (background removal, OCR,
  resize/crop/convert), edit product videos (trim, concat, audio overlay),
  generate AI voiceovers (edge-tts, Chinese/English), build 3D product displays
  (Three.js), or create product detail pages (responsive HTML with bilingual
  support). All-in-one creative toolkit for 萤火虫空压机 (Firefly Air Compressor).
  Trigger keywords: 抠图, 去背景, 识别文字, OCR, 产品详情页, 3D展示, 配音,
  剪视频, 处理图片, 生成页面, remove background, product page, TTS.
version: 2.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python
    emoji: "🎨"
    homepage: http://www.fireflies.net.cn
    os:
      - darwin
      - linux
      - windows
    install:
      python:
        - Pillow
        - pyyaml
        - rembg
        - easyocr
        - edge-tts
user-invocable: true
disable-model-invocation: false
---

# 萤火虫创意工坊 / Firefly Creative Studio

All-in-one creative toolkit for 广州市萤火虫智能装备技术有限公司（萤火虫空压机）.

## 品牌身份 / Brand Identity

- **公司**：广州市萤火虫智能装备技术有限公司（萤火虫空压机）
- **网址**：http://www.fireflies.net.cn
- **热线**：13825202084（邹先生）| 邮箱：aifirefly@163.com | 地址：广州市
- **主营业务**：空压机、余热回收机、制氮机、激光/冷冻干燥机、精密过滤器、排水器、智能控制系统及成套设备
- **品牌理念**："节能自然萤火虫" — 为客户节资、为环境减排
- **品牌色**：绿 `#1B8C3A` | 蓝 `#1565C0` | 橙 `#F57C00`

## Installation

### Python 依赖（脚本模式）
```bash
pip install Pillow pyyaml rembg easyocr edge-tts
```

### 系统工具（可选）
- **FFmpeg** — 视频剪辑功能需要
  - macOS: `brew install ffmpeg`
  - Linux: `apt install ffmpeg` / `dnf install ffmpeg`
  - Windows: https://ffmpeg.org/download.html

### 环境检测
```bash
python scripts/install_deps.py --check-only
```

## 架构 / Architecture

```
SKILL.md                    # 核心指令集（本文件）
scripts/
  install_deps.py           # 环境检测 / 一键安装
  remove_background.py      # rembg AI 抠图
  ocr_image.py              # easyocr 文字识别
  text_to_speech.py         # edge-tts 语音合成
  video_edit.py             # FFmpeg 视频剪辑
  generate_detail_page.py   # YAML→HTML 详情页
references/                 # 按需读取的参考文档
  tools-reference.md        #   FFmpeg/Pillow 命令速查
  design-guidelines.md      #   品牌设计规范
  product-templates.md      #   产品 YAML schema
  video-specs.md            #   视频规格标准
assets/                     # 模板与资源
  detail-page-template.html #   详情页 HTML 模板
  3d-template.html          #   Three.js 3D 模板
  brand-logo.svg            #   公司 Logo
```

## 两种运行模式 / Dual Mode

### 模式 A：脚本模式（推荐）
有 Python 环境时使用。输出确定，可批量处理。
```bash
python scripts/install_deps.py --check-only  # 先检测环境
```

### 模式 B：Claude 原生模式（零依赖）
Python 不可用或需要高度定制时，Claude 直接读取模板生成产物：
- **详情页**：读取 `assets/detail-page-template.html` → 填充产品数据 → 输出 HTML
- **3D 展示**：读取 `assets/3d-template.html` → 建模 → 输出 HTML
- **product.yaml**：按 `references/product-templates.md` schema 编写

## 功能速查 / Quick Reference

### 图片工具
| 功能 | 脚本命令 (Mode A) | 原生模式 (Mode B) |
|-------|------------------|------------------|
| AI 抠图 | `python scripts/remove_background.py <图> -o <输出>` | 需 rembg |
| OCR 识别 | `python scripts/ocr_image.py <图> -o <输出> --format json` | 需 easyocr |
| 缩放/裁剪/格式转换 | Pillow one-liner | Claude 生成 Pillow 代码 |

**触发词**：抠图、去背景、移除背景、识别文字、铭牌、OCR、裁剪、缩放、格式转换

### 视频工具（需 FFmpeg）
```bash
python scripts/video_edit.py trim input.mp4 --start 0:30 --end 2:45 -o trimmed.mp4
python scripts/video_edit.py concat a.mp4 b.mp4 -o combined.mp4
python scripts/video_edit.py add-audio video.mp4 --audio narration.mp3 -o final.mp4
python scripts/video_edit.py screenshot input.mp4 --at 0:05 -o thumb.jpg
```

**触发词**：剪视频、拼接、配音合成、提取帧

### AI 语音配音
```bash
python scripts/text_to_speech.py --text "...文字..." -o output.mp3
python scripts/text_to_speech.py --file script.txt -o output.mp3
```
- 中文女声（默认）：zh-CN-XiaoxiaoNeural
- 中文男声：zh-CN-YunxiNeural
- 英文女声：en-US-JennyNeural
- `--rate -10` 减速 / `--rate +10` 加速

**触发词**：配音、旁白、语音合成、TTS、text to speech

### 3D 产品展示
1. 读取 `assets/3d-template.html` 获取 Three.js 框架
2. 用 `createCyl()` / `createBox()` 构建产品模型
3. 品牌主色 `#1B8C3A` 替换模板默认蓝色
4. 输出自包含 HTML

**触发词**：3D 展示、三维模型、3D 查看器、360度展示

### 产品详情页
**模式 A**：`python scripts/generate_detail_page.py -c product.yaml --lang zh -o detail.html`

**模式 B**：获取产品信息 → 读取模板 → 填充占位符 → 输出自包含 HTML

支持 `--lang zh|en|both`。结构：Hero 区 → 指标卡 → 技术参数表 → 特性卡片 → (可选)3D展示 → (可选)图库 → CTA → 页脚

**触发词**：生成详情页、产品页面、product page、产品介绍页

## 典型流程 / Workflows

1. **抠图+缩放**：`remove_background.py` → Pillow resize → 输出
2. **铭牌→详情页**：`ocr_image.py` 提取参数 → 按 schema 整理 → `generate_detail_page.py` 生成 HTML
3. **视频+配音**：`video_edit.py trim` → `text_to_speech.py` 配音 → `video_edit.py add-audio` 合成
4. **零依赖详情页**：直接读取模板 + 产品数据 → 输出 HTML

## 降级矩阵 / Degradation

| 缺失依赖 | 不可用功能 | 仍可用 |
|---------|-----------|-------|
| rembg | AI 抠图 | 全部其他 |
| easyocr | OCR 文字识别 | 全部其他 |
| edge-tts | AI 配音 | 全部其他 |
| FFmpeg | 视频处理 | 全部其他 |
| Python | 所有脚本 | 模式 B：详情页 + 3D + 基础图片编辑 |

## 关键规则 / Rules

### 必须遵守
- 操作前先 `check-only` 确认环境（模式 A），或告知用户以模式 B 运行
- 缺失可选依赖时清晰告知，给出具体安装命令
- 所有输出 HTML 必须自包含（CSS/JS 内联，无外部依赖）
- 生成内容使用品牌色：绿 `#1B8C3A`、蓝 `#1565C0`、橙 `#F57C00`

### 良好实践
- 批量处理报告进度（X/Y 完成）；大文件处理前告知预计时间
- 首次 easyocr 提醒模型下载（~200MB，仅一次）
- 生成 HTML 后提醒浏览器预览；技术参数标签中英双语

### 参考文件（按需读取）
- `references/tools-reference.md` — FFmpeg/Pillow 复杂命令速查
- `references/design-guidelines.md` — 品牌设计规范（配色、排版、间距）
- `references/product-templates.md` — 产品 YAML schema（各产品类型字段定义）
- `references/video-specs.md` — 视频分辨率/码率/格式标准

### 输出风格
- 中文环境中文输出；参数名中英双语；关键数据加粗
- 金额以"万元"为单位；百分比保留整数
