# BusR 论文案例分析 — text-only 回退演示

> **论文**: *BusR is a Bifunctional Transcription Factor in S. mutans* (JMB 2026)
> **分析日期**: 2026-05-20
> **意义**: 展示当无法用 vision 时的完整纯文本分析流程（Stage 1 提取 + Stage 2 科学理解 + Kimi K2.6 补充视觉）

---

## PDF 提取步骤

### 1. 打开 PDF
```python
import fitz
doc = fitz.open("1-s2.0-S0022283626000136-main.pdf")
# 21 pages, 8 images extracted
```

### 2. 提取所有图片
```python
for page_num in range(doc.page_count):
    for img in page[page_num].get_images(full=True):
        base_image = doc.extract_image(img[0])
        # save base_image['image'] with base_image['ext']
```
结果: 8 images (1 graphical abstract + 7 figures)

### 3. 提取全文
```python
full_text = ''
for page_num in range(doc.page_count):
    full_text += page[page_num].get_text()
```

### 4. 提取嵌入文本块（含部分 caption）
```python
for block in page.get_text('blocks'):
    x0, y0, x1, y1, text = block[:5]
    # 按坐标排序，识别 page header、caption、body text
```

### 5. 定位 Figure captions
```python
import re
for match in re.finditer(r'Figure\s+\d+[^.]*\.', full_text):
    # 提取 caption 并在上下文中搜索实验方法
```

---

## 图片 ↔ Figure 映射

| 图片文件 | Page | 推断 Figure | 尺寸 |
|----------|------|-------------|------|
| page01_img00 | 1 | Graphical Abstract | 329×424 |
| page03_img00 | 3 | **Figure 1** (12 panels) | 1941×1989 |
| page06_img00 | 6 | **Figure 2** (12 panels) | 1748×2366 |
| page08_img00 | 8 | **Figure 3** (11 panels) | 1941×1948 |
| page09_img00 | 9 | **Figure 4** (7 panels) | 1742×1987 |
| page10_img00 | 10 | **Figure 5** (11 panels) | 1433×2366 |
| page13_img00 | 13 | **Figure 6** (7 panels) | 1468×2366 |
| page15_img00 | 15 | **Figure 7** (1 panel) | 1658×1262 |

---

## 纯文本可提取的定量数据（无需 vision）

### Figure 1
- SEC: BusR 14.02 mL, tetramer ~93.6 kDa
- SPR: Kd=196.4±14 nM
- FP: pAB1 apo=22.2, +c-di-AMP=11.5 nM; pAB2=28.8→12.2 nM

### Figure 2
- DEG: 69↑/3↓ (正常渗透)
- nagA: WT~50→ΔbusR~1500 TPM
- Table 1: 完整 fold change 数据

### Figure 3
- FP Kd: pA1 67→30; pA2 23→32; pA3 66→29; pB1 8→20; pB2 53→25; pB3 27→31 nM

### Figure 4
- FMC-GlcNAc: ΔbusR 早 30h 进入对数期
- ΔdacA 中速; ΔpdeA 严重延迟

### Figure 5
- 2.42Å SAD 结构
- RMSD A vs B=11.53Å; vs SaBusR=5.97/7.53Å
- 43% sequence identity

### Figure 6
- wHTH旋转117.8°/82.6°; RCK_C旋转157.4°/159.1°
- RMSF: apo > BusR-DNA > BusR-DNA-c-di-AMP

---

## Kimi K2.6 视觉补充的数据（纯文本无法获取）

| 数据类型 | 示例 |
|----------|------|
| 色谱图精确体积 | SEC 标准蛋白洗脱: G6pD 11.68, OxyR 12.57, PA2276 15.08 mL |
| DLS/SLS 面板数值 | Radius 5.72 nm, %PD 13.0, Mw-S 103.8±6.56 |
| 静电势色阶 | -77.792~+77.792 kT/e |
| EMSA 泳道设置 | 精确的 BusR 浓度梯度 (1-10 μM) |
| 结构域颜色编码 | wHTH=绿, Linker=红, RCK_C=黄 |
| 残基级别标注 | K36, R38, E50, R53, K54 (DNA互作) |
| 生长曲线 OD 值 | WT 延迟 ~40h, ΔbusR 峰值 ~0.53 |

---

## 方法论结论

1. **纯文本先行**: 先用 PyMuPDF 提取所有可读数据，构建 80% 的分析框架
2. **Vision 补充**: 仅在需要图上具体数值时才调用 Kimi K2.6
3. **交叉验证**: Kimi 提取的数值与正文描述交叉核对（全部一致，证明可靠性）
4. **成本优化**: 纯文本零成本，vision 按需使用
