# Scientific Figure Analysis Pipeline

A complete scientific paper figure analysis workflow: **PDF extraction (PyMuPDF) → Kimi K2.6 multimodal vision → scientific reasoning → reverse engineering**.

## Overview

```
PDF Paper
   │
   ├─ Stage 1: PyMuPDF Extraction
   │   ├─ All embedded images (.jpeg/.png)
   │   ├─ Full text (captions + body)
   │   └─ Image metadata (dimensions, page number)
   │
   ├─ Stage 2: Kimi K2.6 Vision Analysis ★ Core
   │   ├─ base64 encoded images
   │   ├─ OpenAI SDK → api.moonshot.cn
   │   └─ Extract all visible values/labels/trends
   │
   ├─ Stage 3: Scientific Understanding
   │   ├─ Figure type recognition (18 types)
   │   ├─ Multimodal reasoning (vision + text)
   │   └─ Conservative confidence labeling
   │
   └─ Stage 4: Reverse Engineering
       ├─ Software inference (Prism/ggplot2/PyMOL...)
       └─ Pipeline reconstruction
```

## Features

- **Multi-panel figure detection** — accurately splits a/b/c/d sub-panels while preserving labels and legends
- **Kimi K2.6 vision AI** — extracts exact values (Kd, RMSD, fold change, OD values) not readable from text
- **18 scientific figure types** — microscopy, fluorescence, heatmaps, volcano plots, PCA, phylogeny, Western Blot, pathways, and more
- **Software fingerprinting** — GraphPad Prism, ggplot2, matplotlib, ImageJ, BioRender, Illustrator
- **Pipeline reconstruction** — infers normalization, clustering, differential expression, sequencing preprocessing workflows
- **Confidence-aware** — never hallucinate; uncertain findings are flagged as speculative

## Installation

```bash
pip install pymupdf opencv-python pdfplumber openai
```

Optional (OCR):
```bash
sudo apt install tesseract-ocr
```

## Quick Start

```python
import fitz, os
from openai import OpenAI
import base64, os

# 1. Extract figures from PDF
doc = fitz.open("paper.pdf")
os.makedirs("figures_output", exist_ok=True)

for pn in range(doc.page_count):
    for i, img in enumerate(doc[pn].get_images(full=True)):
        base = doc.extract_image(img[0])
        fname = f"figures_output/page{pn+1:02d}_img{i:02d}.{base['ext']}"
        with open(fname, 'wb') as f:
            f.write(base['image'])

# 2. Vision analysis with Kimi K2.6
client = OpenAI(
    api_key=os.environ.get("MOONSHOT_API_KEY"),
    base_url="https://api.moonshot.cn/v1",
)

with open("figures_output/page03_img00.jpeg", "rb") as f:
    image_data = f.read()

ext = "jpeg"
image_url = f"data:image/{ext};base64,{base64.b64encode(image_data).decode('utf-8')}"

completion = client.chat.completions.create(
    model="kimi-k2.6",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": "请描述这张科学图表的内容，包括所有可见的数值、标签和趋势。"},
        ],
    }],
    extra_body={"thinking": {"type": "disabled"}},
    max_tokens=4096,
)

print(completion.choices[0].message.content)
```

Set your API key:
```bash
export MOONSHOT_API_KEY="sk-..."   # from https://platform.kimi.com
```

## Figure Types Supported

| Type | Features |
|------|----------|
| Microscopy / Fluorescence | Grayscale/fluorescence channels, scale bars |
| Heatmap | Color scale matrix, row/column clustering |
| Volcano Plot | -log10(p) vs log2FC, threshold lines |
| PCA | Scatter + ellipse, variance explained |
| UMAP / t-SNE | Cluster distribution, perplexity annotation |
| Phylogenetic Tree | Branch topology, bootstrap values |
| Western Blot | Bands, molecular weight markers |
| Pathway Diagram | Arrows, nodes, enzyme labels |
| Workflow Chart | Step arrows, method boxes |
| Bar/Box/Violin Plot | Error bars, density contours |
| Sequencing QC | FastQC curves, duplication rates |
| Genome Browser | Tracks, read piles |
| Spatial Transcriptomics | Tissue section + expression overlay |
| Single-cell Clustering | UMAP + marker genes |

## File Structure

```
scientific-figure-analysis/
├── SKILL.md                                    # Main skill documentation
└── references/
    ├── kimi-k2.6-vision-api.md                 # Kimi K2.6 API reference
    └── busr-paper-case-study.md                 # Full case study (text-only fallback)
```

## License

MIT

## Contact & Citation

Designed and published by Huang Kai (huangjk8023@yeah.net).
