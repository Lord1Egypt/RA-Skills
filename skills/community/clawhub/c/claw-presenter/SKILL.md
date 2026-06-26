---
name: claw-presenter
description: "准备PPT/PDF讲解稿。将幻灯片转为图片并生成逐页演讲词。触发词：准备PPT讲解稿、准备演讲稿、生成演讲词、prepare presentation narration."
user-invocable: true
metadata:
  openclaw:
    emoji: "🎤"
    setup: setup.sh
    requires:
      bins:
        - python3
---

# 🎤 Claw Presenter — Prepare Presentation Narration

Converts PPT/PPTX/PDF files into a ready-to-present package: per-slide images + narration scripts.

## What This Skill Does

Two jobs only:
1. **Split** — Convert each slide/page into a PNG image
2. **Script** — Generate a narration script for each slide

Output is a folder that **Claw Body** can load for presentation playback with digital avatar narration.

## Works With Claw Body

This skill is designed to pair with the **claw-body** skill (digital avatar). The workflow:

1. **Claw Presenter** (this skill) → parses PPT/PDF, generates slide images + narration scripts
2. **Claw Body** → loads the output folder, displays slides with the digital avatar narrating each page

Typical usage:
1. User: "帮我准备 xxx.pptx 的讲解稿" → triggers **claw-presenter**
2. After preparation is done, user: "讲解 presentations/xxx" → triggers **claw-body** presentation mode

> ⚠️ Make sure the **claw-body** skill is also installed if you want avatar-powered presentation playback.

## When To Use

When user says anything like:
- "帮我准备PPT讲解稿"
- "准备讲解 xxx.pptx"
- "帮我准备演讲稿"
- "生成PPT演讲词"
- "prepare presentation for xxx.pdf"
- "生成演讲词"
- "准备讲稿"

**Do NOT use this skill when user just says "讲PPT" without preparation** — that implies they want to present, and they should use Claw Body's presentation mode with an already-prepared folder.

## Step 0: Get the File

If user didn't provide a file path, ask:
> "请告诉我PPT/PDF文件的路径，例如 ~/Desktop/我的演讲.pptx"

Wait for user to provide the path before proceeding.

## Step 1: Parse the File

Run the parse script to extract slides and text:

```bash
python3 <skill-dir>/scripts/parse-presentation.py "<file-path>"
```

This creates:
```
<workspace>/presentations/<filename>/
  presentation.json    — metadata, per-slide text, notes
  slides/
    001.png, 002.png, ...
```

## Step 2: Generate Narration Scripts

After parsing, read `presentation.json`. For each slide:

- If `slide.script` is already filled (from speaker notes) → keep it, but optionally polish
- If `slide.script` is empty → generate natural narration based on `slide.title` and `slide.content`

### Style Guidelines

Ask the user (if not specified):
- **风格**: 正式汇报 / 轻松分享 / 教学讲解 / 幽默风趣
- **受众**: 老板/领导 / 同事 / 客户 / 学生
- **语言**: 中文 / English / 跟随原文
- **时长**: 简短（每页15-30秒）/ 标准（30-60秒）/ 详细（1-2分钟）

### Writing Good Narration

- Open naturally: "首先我们来看..." / "接下来..."
- Don't just read the slide — explain, add context, connect to previous slide
- Keep transitions smooth between slides
- Match the style throughout

## Step 3: Save the Scripts

After generating all scripts, update `presentation.json` — fill in the `script` field for each slide, then write back:

```python
# Read, update scripts, write back
import json
with open('<output-dir>/presentation.json', 'r') as f:
    data = json.load(f)
for slide in data['slides']:
    if not slide['script']:
        slide['script'] = '<your generated narration>'
with open('<output-dir>/presentation.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## Step 4: Confirm with User

Show a summary:
> 📊 演讲稿准备完成！
> - 文件: xxx.pptx
> - 共 12 页，其中 3 页使用了原始备注，9 页已生成演讲词
> - 风格: 轻松分享
> - 输出目录: presentations/xxx/
>
> 你可以：
> - 预览/修改某页的演讲词
> - 在 Claw Body 中说"讲解 presentations/xxx" 开始演讲
> - 或直接在这里文字预览

## Output Format

`presentation.json` structure:
```json
{
  "source": "filename.pptx",
  "total_pages": 12,
  "output_dir": "/path/to/presentations/filename",
  "slides": [
    {
      "page": 1,
      "title": "封面",
      "content": ["标题文字", "副标题"],
      "notes": "原始备注",
      "has_notes": true,
      "image": "slides/001.png",
      "script": "各位好，今天我来跟大家分享..."
    }
  ]
}
```

## Setup

Run the setup script to install all dependencies:

```bash
bash <skill-dir>/setup.sh
```

Or install manually:

### Python Packages

```bash
pip3 install python-pptx Pillow pdf2image pdfplumber
```

### System Dependencies

**poppler** (required — converts PDF to images):

| Platform | Command |
|----------|---------|
| macOS (Homebrew) | `brew install poppler` |
| Debian / Ubuntu | `sudo apt-get install -y poppler-utils` |
| Fedora / RHEL | `sudo dnf install -y poppler-utils` |
| Arch | `sudo pacman -S poppler` |

**LibreOffice** (optional — high-fidelity PPTX→image conversion):

| Platform | Command |
|----------|---------|
| macOS (Homebrew) | `brew install --cask libreoffice` |
| Debian / Ubuntu | `sudo apt-get install -y libreoffice` |
| Other | [libreoffice.org/download](https://www.libreoffice.org/download/) |

> Without LibreOffice, PPTX slides will fall back to simple text rendering (lower quality images).

### Verify Installation

```bash
python3 -c "import pptx; print('python-pptx ✅')"
python3 -c "from PIL import Image; print('Pillow ✅')"
python3 -c "from pdf2image import convert_from_path; print('pdf2image ✅')"
which pdftoppm && echo "poppler ✅"
which soffice && echo "LibreOffice ✅" || echo "LibreOffice ❌ (optional)"
```
