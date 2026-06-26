---
name: doc2slides
version: 3.8.2
description: "One-click PDF/Word/Markdown to designer-grade PPT. AI auto-layout + 18 slide types + built-in charts. Local-first, free. Use when: user wants to create slides from a document or convert content to PPT."
license: MIT-0
author: lifei68801
metadata:
  openclaw:
    requires:
      bins: ["python3", "pip3"]
      env:
        optional:
          - OPENAI_API_KEY
          - ZHIPU_API_KEY
          - DEEPSEEK_API_KEY
    permissions:
      - "file:read"
      - "file:write"
    behavior:
      modifiesLocalFiles: true
      network: optional
      telemetry: none
      credentials: optional
---

# Doc2Slides

> 把 PDF、Word、Markdown 一键变成设计师级 PPT。10 秒出稿，无需设计能力。

📄 论文答辩 / 📊 周报月报 / 📋 技术文档培训 / 💡 创业路演

```bash
# Install & setup
clawhub install doc2slides
bash ~/.openclaw/workspace/skills/doc2slides/setup.sh

# Go
python3 workflow.py --input report.pdf --output report.pptx
```

Done. 一行命令，PPT 生成在本地。

## Why doc2slides?

| | doc2slides | 模板方案 | AI 在线服务 |
|--|-----------|---------|-----------|
| 排版 | 18 种布局 AI 自动匹配 | 固定 2-3 种 | 有限 |
| 图表 | 内置 SVG 饼图/柱状/进度环 | 手动插入 | 依赖模板 |
| 隐私 | 默认本地，可选 LLM | 本地 | 上传云端 |
| 费用 | 免费 | 免费 | 按次收费 |
| 画质 | 3x 高清 (3840×2160) | 标清 | 取决于套餐 |
| AI | GPT-4o / 智谱 / DeepSeek 可选 | 无 | 固定模型 |

## Use Cases

- **论文答辩** — 把论文 PDF 变成答辩 PPT，自动提炼要点
- **周报月报** — Markdown 周报一键幻灯片，数据自动配图表
- **技术分享** — 技术文档转培训材料，代码块自动排版
- **创业路演** — 商业计划书变路演 PPT，金字塔/矩阵布局
- **读书笔记** — 长文拆解成结构化幻灯片

## Agent Trigger

User says any of → activate:

- "把这个文档做成PPT" / "做个演示文稿"
- "Convert this PDF to slides"
- "Generate a presentation from..."

**Workflow:**

1. First time? `bash setup.sh --verify`
2. Missing deps? tell user `bash setup.sh`
3. Ask: "有特殊要求吗？页数、风格、重点？没有我按默认来。"
4. Locate input (path or URL)
5. Generate:
   ```bash
   cd ~/.openclaw/workspace/skills/doc2slides/scripts
   python3 workflow.py --input <file> --output <file.pptx> [options]
   ```
6. Verify output, send to user

## CLI Options

| Flag | Example |
|------|---------|
| `--input` | Required. PDF / DOCX / MD path |
| `--output` | Required. Output .pptx path |
| `--pages N` | Limit slide count |
| `--instruction "..."` | Custom guidance |
| `--style corporate` | Color: corporate / tech / nature / warm / minimal / dark_purple / finance |
| `--theme AI` | Auto color by topic |
| `--model gpt-4o` | LLM for analysis |
| `--preview` | Also generate PNG screenshots |

```bash
# Example: business style, 8 pages, data focused
python3 workflow.py --input report.pdf --output report.pptx \
  --instruction "商务风格，重点突出数据，控制在8页，每页配图表"
```

## Layouts (18+)

| Category | Layouts |
|----------|---------|
| Data | Dashboard, Big Number, KPI Cards, Chart |
| Structure | Pyramid, Comparison, 2x2 Matrix, Flow |
| Narrative | Timeline, Action Plan, Quote, Full-image |
| Content | Two-column, Three-column, Icon Grid, Vertical List |
| Visual | Progress Ring, Horizontal Bar, Stacked Cards |

Each section of your document gets auto-matched to the best layout.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: pptx` | `pip3 install python-pptx` |
| No browser for screenshots | `playwright install chromium` |
| Chromium download timeout | `apt install google-chrome-stable` |
| Output blank/broken | Add `--preview` to debug HTML |
| Too slow for long docs | `--pages N` to limit |

## Pipeline

```
Document → Analyze → Match Layouts → Build HTML → Render (3x) → PPTX
```

Default mode runs fully local — no CDN, no cloud. Optionally connect LLM providers (GPT-4o / 智谱 / DeepSeek) for smarter analysis when you configure API keys.

MIT-0 license.
