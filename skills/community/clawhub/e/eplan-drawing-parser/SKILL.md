---
name: eplan-drawing-parser
description: |
  EN: Extract structured data from EPLAN/CAD vector PDF electrical drawings — component list (位号/型号/数量), wire/pin topology (导线连接、串并联、电能流向), terminal table, and title-block metadata. Uses PDF vector geometry (100% accurate, no OCR) instead of visual models. Use when the user provides an EPLAN or vector PDF electrical schematic and asks "解析EPLAN图 / 抽元件清单 / 看导线怎么连 / 提取位号型号 / parse EPLAN drawing / extract components / wire topology".
  中文：从 EPLAN / CAD 矢量 PDF 电气图纸中抽取结构化数据 —— 元件清单（位号/型号/数量）、导线连接拓扑（串并联、电能流向）、端子表、标题栏。基于 PDF 矢量几何直接提取（100%准确，无OCR误差），不依赖视觉模型。当用户提供 EPLAN 或矢量 PDF 电气原理图并要求"解析EPLAN图/抽元件清单/看导线怎么连/提取位号型号"时触发。
version: 1.1.0
metadata:
  openclaw:
    emoji: "⚡"
    homepage: https://github.com/openclaw-skills/eplan-drawing-parser
    requires:
      bins:
        - python3
      pip:
        - pymupdf
        - openpyxl
    envVars: []
---

# EPLAN Drawing Parser · EPLAN电气图纸智能解析

> Turn an EPLAN vector PDF into structured component + wiring topology data in seconds — with 100% accuracy on text and wire geometry, no OCR, no vision-model hallucination.
>
> 秒级把 EPLAN 矢量 PDF 变成结构化数据：元件清单 + 导线连接拓扑，文本和导线几何 100% 精确，无 OCR、无视觉模型幻觉。

---

## 🎯 When to Use · 何时使用

**Trigger keywords (中文):** 解析EPLAN图、解析电气图、抽元件清单、提取位号型号、看导线怎么连、连接拓扑、端子表、出BOM、元件明细、图纸和清单核对、UL证书核对、位号型号数量核对

**Trigger keywords (EN):** parse EPLAN, parse electrical drawing, extract components, extract reference designators, wire topology, connection diagram, terminal table, extract BOM, cross-check drawing vs BOM, verify BOM, UL cert check

**Supported input:** EPLAN 导出的矢量 PDF、CAD 矢量 PDF（必须带文本层 + 矢量线，非扫描件）

**Do NOT use when:**
- 扫描件/图片型 PDF（无文本层）→ 需先转 OCR 或用其他流程
- 用户只想读纯文字，不关心连线 → 用简单文本提取即可

---

## 📋 Pipeline · 解析流程

### Step 1: Extract geometry · 提取几何（权威层）

```bash
python3 scripts/extract_geom.py --input drawing.pdf --output parsed.json
```

逐页提取两部分，**均来自 PDF 矢量对象，机器直读，零误差**：
- **导线 (wires)**: 每条线的精确起止坐标 (x1,y1,x2,y2)
- **文本 (texts)**: 型号/位号/数值 + 每个字的中心坐标

### Step 2: Count wire connections · 统计导线连接数

每个元件附近(radius像素)的导线端点数量 → 判断元件是否在电路、主/辅助性质。

### Step 3: Build topology · 重建连接拓扑

通过"导线端点 ↔ 元件端子坐标"匹配，重建元件间连接关系、串并联结构、电能流向、垂直层级。

---

## 🧾 BOM Cross-Check · 图纸 ↔ 清单核对（v1.1 新增）

将 EPLAN 图纸与 Excel 物料清单(UL证书汇总)交叉核对，一次性完成四件事：

```bash
python3 scripts/check_bom.py --pdf drawing.pdf --xlsx bom.xlsx
# 指定 sheet / 自定义导出路径:
python3 scripts/check_bom.py --pdf drawing.pdf --xlsx bom.xlsx --sheet "UL证书汇总" --out 核对结果.xlsx
```

核对内容：
1. **位号核对** —— 清单每个位号是否在图纸出现（自动去掉 EPLAN 前导 `-`，如 `-FU1001`→`FU1001`）
2. **型号核对** —— 基于图纸矢量文本（100%准）比对清单型号
3. **数量核对** —— 清单数量 vs 图纸出现频次
4. **UL归口检查** —— 找出清单中 型号↔UL档案号↔供应商 缺档条目（缺 UL 档案号等）

默认自动识别含 `UL` 的 sheet；导出 xlsx 含「位号核对 / 无UL档案号」两个表。

**用法示例：**
```bash
python3 scripts/check_bom.py --pdf 燃料电池直流输出柜0821.pdf --xlsx 清能3mw项目清单-08-21.xlsx --sheet "UL证书汇总"
```

---

## 📤 Output Format · 输出格式

```json
{
  "file": "燃料电池直流输出柜8-20.pdf",
  "num_pages": 18,
  "pages": [
    {
      "page": 3,
      "num_wires": 1006,
      "num_texts": 454,
      "topology_nodes": 1007,
      "components": ["FCM1-", "FCM1+", "QF1001触点反馈", "..."]
    }
  ]
}
```

用 `--full` 参数可输出完整 texts（含所有文字坐标）。

---

## 🚀 Usage Examples · 使用示例

### Example 1: 全部页解析（精简）

```bash
python3 scripts/extract_geom.py --input 燃料电池直流输出柜8-20.pdf --output out.json
```

### Example 2: 完整输出（含全部文字坐标）

```bash
python3 scripts/extract_geom.py --input drawing.pdf --output full.json --full
```

---

## 🧠 Design Philosophy · 设计理念

**为什么不用视觉模型？** 实测 agnes-2.5-flash 视觉识别会把 `3VA5450-7GV41-0AA0` 读成 `3VA5450-7GJ41-0AL0`、把 SPD 串联顺序说反、甚至编造不存在的标注。而 **PDF 矢量对象本身携带精确的导线坐标和文本**，机器直接读取即可 100% 还原，彻底消除视觉模型的"看图幻觉"。

**优势对比：**

| 信息维度 | 本Skill (矢量直读) | 视觉模型 |
|---------|------------------|---------|
| 文字/型号/位号/数值 | ✅ **100%** | ⚠️ 60-90%（字母数字误读） |
| 导线连接/串并联/流向 | ✅ **~100%**（几何重建） | ⚠️ 常把并联说成串联 |
| 是否编造标注 | ❌ 从不（只读真实对象） | ⚠️ 可能幻觉 |
| 速度 | 毫秒~秒级 | 秒~分钟级 |

---

## ⚠️ Safety & Compliance · 安全合规

1. **纯本地处理** — 图纸从不上传任何外部服务，所有解析在本机完成。
2. **提取不判断** — 只抽取信息，不做"尺寸对不对""设计改不改"的判断。
3. **可追溯** — 每页输出带页码与坐标，可回原图核对。

---

## 📚 References · 参考资料

- PyMuPDF (fitz) 矢量 PDF 提取: https://pymupdf.readthedocs.io/
- EPLAN 导出 PDF 规范（矢量+文本层）

## 🏷️ Tags · 标签

`EPLAN` `electrical` `schematic` `CAD` `PDF` `topology` `wiring` `BOM` `UL` `电气图` `导线拓扑` `元件清单` `图纸清单核对`
