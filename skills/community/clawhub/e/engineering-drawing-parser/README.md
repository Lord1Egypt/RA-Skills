# Engineering Drawing Parser · 工程图纸智能解析

[English](#english) | [中文](#chinese)

---

## English

Extract structured info from engineering drawings (mechanical, P&ID, electrical, civil) into BOM, dimensions, tolerances, title block, symbol inventory.

### Quick Start

```bash
python3 scripts/run_pipeline.py \
  --input part.dwg --domain mechanical --standard GB \
  --output part_parsed.json
python3 scripts/render_preview.py --input part_parsed.json --pdf annotated.pdf
```

### Features

- 📐 4 domains: mechanical, piping (P&ID), electrical, civil
- 📁 Formats: DWG, DXF, PDF (vector or scanned), PNG/JPG
- 📋 BOM extraction with merged-cell support
- 🔢 Dimension + tolerance (ISO 1101 geometric tolerance)
- 🔍 Symbol recognition (ISA-5.1, IEC 60617, GB)
- 📍 Every output linked back to drawing coordinates

### License

MIT-0

---

## Chinese

从工程图纸（机械/管道/电气/建筑）抽取 BOM、尺寸、公差、标题栏、符号清单。

### 快速开始

```bash
python3 scripts/run_pipeline.py \
  --input 零件.dwg --domain mechanical --standard GB \
  --output 零件_解析.json
python3 scripts/render_preview.py --input 零件_解析.json --pdf 标注图.pdf
```

### 功能

- 📐 4 大类：机械、管道、电气、建筑
- 📁 格式：DWG / DXF / PDF / 图片
- 📋 BOM 抽取，支持合并单元格
- 🔢 尺寸 + 公差（ISO 1101 几何公差）
- 🔍 符号识别（ISA-5.1、IEC 60617、GB 标准）
- 📍 每项输出可定位回原图坐标

### 协议

MIT-0
