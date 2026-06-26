---
name: engineering-drawing-parser
description: |
  EN: Extract structured information from engineering drawings — mechanical 2D drafts, P&IDs, electrical schematics, construction architectural/structural drawings — into machine-readable BOM, dimension lists, tolerance tables, title-block metadata and symbol inventories. Supports DWG/DXF/PDF/image input. Use when the user provides a drawing and asks "解析图纸 / 抽 BOM / 读尺寸 / 出明细表 / parse drawing / extract BOM".
  中文：从工程图纸（机械二维图、P&ID 工艺管道仪表流程图、电气原理图、建筑结构施工图）中抽取结构化信息，输出 BOM 物料清单、尺寸表、公差表、标题栏元数据、符号清单。支持 DWG/DXF/PDF/图片输入。当用户提供图纸并要求"解析/抽 BOM/读尺寸/出明细"时触发。
version: 1.0.0
metadata:
  openclaw:
    emoji: "📐"
    homepage: https://github.com/openclaw-skills/engineering-drawing-parser
    requires:
      bins:
        - python3
    envVars:
      - name: DRAWING_DOMAIN
        required: false
        description: Drawing domain hint, one of `mechanical|piping|electrical|civil`. Auto-detected if unset.
      - name: DRAWING_STANDARD
        required: false
        description: Standard hint, one of `GB|ISO|ANSI|JIS|DIN`. Defaults to GB for Chinese drawings.
      - name: DRAWING_OCR_LANG
        required: false
        description: OCR language hint, e.g. `chi_sim+eng`. Defaults to auto.
---

# Engineering Drawing Parser · 工程图纸智能解析

> Turn a 1:50 scale engineering drawing into a clean structured dataset in under 2 minutes — BOM, dimensions, tolerances, title block, and every visible symbol — all linked back to coordinates on the source page.
>
> 2 分钟把工程图纸变成结构化数据：BOM、尺寸、公差、标题栏、符号清单，每一项都能定位回原图坐标。

---

## 🎯 When to Use · 何时使用

**Trigger keywords (中文):** 解析图纸、读图纸、抽 BOM、出明细表、尺寸清单、公差清单、标题栏、装配图、零件图、施工图、P&ID、电气原理图

**Trigger keywords (EN):** parse drawing, extract BOM, read dimensions, tolerance list, title block, drawing OCR, P&ID parsing, schematic extraction

**Supported drawing types:**

| 类别 / Type | 子类 / Subtype | 支持元素 |
|---|---|---|
| 机械 Mechanical | 零件图、装配图、爆炸图 | 尺寸、公差、表面粗糙度、几何公差、BOM、标题栏 |
| 管道工艺 P&ID | 工艺流程、PFD/PID | 设备、管线、阀门、仪表、tag 号、介质 |
| 电气 Electrical | 原理图、接线图、系统图 | 元器件、网络标号、回路、参数 |
| 建筑结构 Civil | 平面、立面、剖面、节点 | 轴网、构件、标高、配筋、说明 |

**Supported formats:** DWG, DXF, PDF (vector or scanned), PNG/JPG/TIFF (scanned)

**Do NOT use when:**
- Drawing is a freehand sketch with no standardized notation
- File is a 3D model (STEP/STL/IGES) — use a CAD-native tool instead
- User wants the parser to redesign or modify the drawing

---

## 📋 Parsing Pipeline · 解析流程

### Step 1: Format dispatch · 格式分发

```bash
python3 scripts/dispatch.py --input <file> --out /tmp/raw_geom.json
```

- DWG/DXF → vector geometry via `ezdxf` (bundled)
- Vector PDF → vector geometry via `pdfminer`
- Scanned PDF / image → raster pipeline (OCR + symbol detector)

### Step 2: Region segmentation · 区域分割

`scripts/segment_regions.py` partitions every drawing into 5 zones:
- Title block (右下角标题栏)
- BOM / parts list (明细栏)
- Main view region (主视区)
- Notes & legends (技术要求、图例)
- Border & frame (图框)

This dramatically improves downstream extraction precision.

### Step 3: Title block extraction · 标题栏抽取

Maps fields to standardized keys per `knowledge/title_block_<standard>.json`:
- 图号 drawing_no
- 图名 drawing_name
- 比例 scale
- 材料 material
- 设计/校对/审核/批准 (designer/checker/approver)
- 日期、版本、张次

### Step 4: BOM extraction · BOM 抽取

Table-aware extraction with column heuristics for serial/part-number/name/qty/material/remark columns. Handles merged cells, multi-row entries, and continuation pages.

### Step 5: Dimension & tolerance extraction · 尺寸与公差

`scripts/extract_dimensions.py` uses geometric reasoning:
- Detect dimension lines, arrows, extension lines
- Associate dimension text with feature (length / diameter / radius / angle)
- Parse tolerance notation (`±0.05`, `H7/g6`, `0/-0.02`, geometric tolerance frames per ISO 1101)
- Detect surface roughness symbols (Ra, Rz)

### Step 6: Symbol recognition · 符号识别

Domain-specific symbol libraries in `knowledge/symbols_<domain>.json`:
- Mechanical: welding symbols, datum symbols, surface finish
- P&ID: ISA-5.1 instrument symbols, valve types, equipment glyphs
- Electrical: IEC 60617 component symbols
- Civil: structural connection details, rebar callouts

### Step 7: Cross-reference resolution · 交叉引用解析

Resolve references like "see Detail A on sheet 3" or "(详 大样图 5)" by building an inter-sheet graph if multi-page input is provided.

### Step 8: Output assembly · 输出装配

```bash
python3 scripts/assemble_output.py --input parsed.json --format json|xlsx|csv
```

---

## 📤 Output Format · 输出格式

```json
{
  "document": { "title": "...", "drawing_no": "...", "scale": "1:50", "sheets": 4 },
  "title_block": { "designer": "李工", "approver": "王总", "date": "2024-03-15", ... },
  "bom": [
    { "no": 1, "part_no": "GB/T 70.1 M8x25", "name": "内六角螺栓", "qty": 4, "material": "8.8", "remark": "" }
  ],
  "dimensions": [
    { "value": "120", "tolerance": "±0.05", "feature": "总长", "page": 1, "bbox": [120,340,180,360] }
  ],
  "tolerances_geometric": [ { "symbol": "⏥", "value": "0.02", "datum": "A", ... } ],
  "symbols": [ { "type": "weld_fillet", "size": "5", "page": 1, "bbox": [...] } ],
  "notes": ["技术要求：1. 未注公差按 GB/T 1804-m；2. ..."],
  "cross_references": [ { "from": "p1@detail-A", "to": "p3@bbox=..." } ],
  "extraction_report": { "coverage_estimate": 0.92, "low_confidence_items": [...] }
}
```

For Excel export: BOM, dimension list, and symbol inventory are placed on separate sheets with hyperlinks back to a PDF preview annotated with extraction bounding boxes.

---

## ⚠️ Safety & Compliance · 安全合规

1. **Extraction only, no design judgment** — never infer whether a dimension is "correct" or suggest design changes.
2. **Confidence scores attached** — every item has a confidence score; items below threshold flagged for human review.
3. **No drawing redistribution** — the skill never uploads drawings anywhere; all processing local.
4. **IP protection** — title-block extraction excludes confidentiality notices verbatim; users responsible for downstream IP handling.
5. **Traceability** — every extracted value carries `{page, bbox}` for visual verification.

> 本技能仅做信息抽取，不做设计判断或修改建议；所有抽取项带置信度并支持人工复核；不向外部上传图纸；每项信息可定位回原图坐标用于核对。

---

## 🚀 Usage Examples · 使用示例

### Example 1: Single mechanical part drawing

```bash
python3 scripts/run_pipeline.py \
  --input bracket.dwg \
  --domain mechanical --standard GB \
  --output bracket_parsed.json
python3 scripts/render_preview.py --input bracket_parsed.json --pdf bracket_annotated.pdf
```

### Example 2: Multi-sheet assembly with BOM

```bash
python3 scripts/run_pipeline.py \
  --input assembly_4_sheets.pdf \
  --domain mechanical \
  --output assembly.json
python3 scripts/export_bom.py --input assembly.json --format xlsx > bom.xlsx
```

### Example 3: P&ID extraction

```bash
python3 scripts/run_pipeline.py \
  --input pid_unit_100.pdf \
  --domain piping \
  --output pid_extracted.json
python3 scripts/render_isa.py --input pid_extracted.json > pid_summary.md
```

### Example 4: Batch process drawing folder

```bash
python3 scripts/batch_parse.py \
  --input-dir ./project_drawings/ \
  --output-dir ./parsed/ \
  --workers 4 \
  --report summary.html
```

---

## 🧪 Testing · 测试

```bash
cd tests && python3 -m pytest -v
```

Fixtures cover:
- 8 mechanical drawings (GB/ISO/ANSI)
- 4 P&ID drawings (ISA-5.1)
- 3 electrical schematics (IEC 60617)
- 5 civil drawings (Chinese GB standard)
- Edge cases: rotated dimensions, stacked tolerance frames, hand-annotated revisions

---

## 📚 References · 参考资料

- GB/T 17450, GB/T 4458 机械制图国家标准
- ISO 128, ISO 1101, ISO 5459 Technical drawings
- ANSI Y14.5 Dimensioning and Tolerancing
- ISA-5.1 P&ID Instrumentation Symbols
- IEC 60617 Electrical Symbols

## 🏷️ Tags · 标签

`engineering` `CAD` `drawing-parsing` `BOM-extraction` `P&ID` `DWG` `DXF` `工程图` `图纸解析` `BOM` `工业`
