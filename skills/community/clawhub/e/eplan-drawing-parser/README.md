# EPLAN Drawing Parser ⚡

[English](#english) | [中文](#chinese)

---

## English

**Parse EPLAN / CAD vector PDF electrical drawings into structured component lists and wire connection topology — seconds, 100% accurate on text & wire geometry, no OCR, no vision-model hallucination.**

Unlike vision-based parsers that "guess" wire connections (and often get series/parallel wrong or hallucinate labels), this skill reads the **vector geometry directly from the PDF** — every wire's exact coordinates and every text label — then rebuilds the true circuit topology by matching wire endpoints to component terminals.

### Why this is different

- ✅ **100% accurate text** — model numbers, reference designators (位号), quantities read from PDF vector text layer
- ✅ **~100% accurate wire topology** — series/parallel, energy flow direction rebuilt from vector line geometry (not "guessed" by a vision model)
- 🚫 **No fabrication** — never invents labels; only reads objects that actually exist in the PDF
- ⚡ **Fast & local** — milliseconds, fully offline, drawings never uploaded

### Quick Start

```bash
# Basic parse (all pages) -> components + wire counts
python3 scripts/parse_eplan.py --input drawing.pdf --out-dir ./out

# Specific pages + annotated preview PNGs
python3 scripts/parse_eplan.py --input drawing.pdf --pages 3,5 --preview --out-dir ./out
```

### Output

```
drawing.json          # structured: per-page wires, components (designator/type/wires/coords)
drawing_page3.png     # annotated preview (with --preview): component boxes overlaid
```

Console summary shows per-page component count, wire count, and total.

### Requirements

- Python 3 + PyMuPDF (`pip install pymupdf`)
- Input: EPLAN / CAD **vector** PDF (text layer + vector lines). Scanned/image PDFs are NOT supported (no text layer).

### Supported reference designators

`QF`/`Q`（断路器）, `FU`/`F`（熔断器）, `SPD`（浪涌）, `KM`（接触器）, `KA`/`K`（继电器）, `TA`（电流互感器）, `X`（端子排）, `H`/`HL`（指示灯）, `S`（按钮）, `TC`（温控）, `FAN`（风扇）, PLC modules (`CPU`/`HMI`/`IM`/`ET`), `AGH`/`CHA`（绝缘监测）, and more.

### License

MIT-0

---

## 中文

**秒级解析 EPLAN / CAD 矢量 PDF 电气图纸，输出元件清单 + 导线连接拓扑。文本与导线几何 100% 精确，无 OCR、无视觉模型幻觉。**

与依赖视觉模型"猜"导线连接的解析器不同（它们常把串并联搞错、甚至凭空编造标注），本技能**直接从 PDF 读取矢量几何** —— 每条导线的精确坐标、每个文字标注，再通过"导线端点 ↔ 元件端子"匹配，重建真实电路拓扑。

### 优势对比

- ✅ **文字 100% 精确** — 型号、位号、数量直接从 PDF 矢量文本层读取
- ✅ **导线拓扑 ~100% 精确** — 串/并联、电能流向由矢量线几何重建（非视觉模型猜测）
- 🚫 **不编造** — 只读 PDF 里真实存在的对象，绝不幻觉标注
- ⚡ **快且本地化** — 毫秒级、完全离线、图纸绝不上传

### 快速开始

```bash
# 基本解析（全部页）-> 元件 + 导线统计
python3 scripts/parse_eplan.py --input 图纸.pdf --out-dir ./out

# 指定页 + 生成标注预览PNG
python3 scripts/parse_eplan.py --input 图纸.pdf --pages 3,5 --preview --out-dir ./out
```

### 输出

```
图纸.json          # 结构化：每页导线数、元件列表(位号/类型/导线数/坐标)
图纸_page3.png     # 标注预览(需 --preview)：元件坐标框叠加图
```

控制台会输出每页元件数、导线数、总数汇总。

### 依赖

- Python 3 + PyMuPDF（`pip install pymupdf`）
- 输入：EPLAN / CAD **矢量** PDF（文本层 + 矢量线）。扫描件/图片 PDF 不支持（无文本层）。

### 支持位号

`QF`/`Q`（断路器）、`FU`/`F`（熔断器）、`SPD`（浪涌）、`KM`（接触器）、`KA`/`K`（继电器）、`TA`（电流互感器）、`X`（端子排）、`H`/`HL`（指示灯）、`S`（按钮）、`TC`（温控）、`FAN`（风扇）、PLC 模块（`CPU`/`HMI`/`IM`/`ET`）、`AGH`/`CHA`（绝缘监测）等。

### 协议

MIT-0
