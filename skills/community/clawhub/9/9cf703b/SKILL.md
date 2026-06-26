---
name: scientific-figure-analysis
description: |
  科学论文图表完整分析流水线 — PDF图表提取(PyMuPDF) + Kimi K2.6多模态视觉分析 + 科学理解 + 逆向工程。
  触发场景: (1) 分析论文PDF中的图表，(2) 逆向工程图表生成流水线，(3) 从文献中提取结构化知识，(4) 论文自动化文献挖掘。
  Do NOT call: 纯文本阅读、非科学类PDF、无图表的纯理论论文。
---

# 科学图表分析 — 完整流水线

> **PDF提取 → 视觉AI分析 → 科学理解 → 逆向工程**，一站式从论文到结构化知识。

## 四阶段流水线

```
 PDF论文
    │
    ├─ Stage 1: PyMuPDF 提取
    │   ├─ 所有嵌入图片 (.jpeg/.png)
    │   ├─ 全文文本 (captions + body)
    │   └─ 图片元数据 (尺寸、页码)
    │
    ├─ Stage 2: Kimi K2.6 视觉分析  ★核心★
    │   ├─ base64 编码图片
    │   ├─ OpenAI SDK 调用 api.moonshot.cn
    │   └─ 提取图表中所有可见数值/标签/趋势
    │
    ├─ Stage 3: 科学理解
    │   ├─ 图表类型识别（18种）
    │   ├─ 多模态推理（视觉+文本融合）
    │   └─ 保守置信度标注
    │
    └─ Stage 4: 逆向工程
        ├─ 软件推断（Prism/ggplot2/PyMOL...）
        └─ 流水线重建
```

---

### Stage 1 — 图表提取

#### 必需能力
- 解析科学PDF
- 检测所有图表
- 保留原始分辨率、颜色、轴标签、图例、比例尺、标注

#### 子图检测
准确检测并拆分 a/b/c/d 等子图面板。

**子图拆分要求**：
- 保留面板标签
- 避免裁剪
- 保留上下文
- 保留嵌入标注
- 不移除共享图例

**推理方式（组合使用，不单独依赖OCR）**：
- 布局边界分析
- 空白区域分割
- OCR文字识别
- 面板标签检测
- 标题对齐检测
- 视觉分组

#### 推荐工具

| 工具 | 用途 | 安装 |
|------|------|------|
| **PyMuPDF (fitz)** | PDF解析、图片提取、文本提取 | `pip install pymupdf` |
| pdfplumber | 表格/文本提取 | `pip install pdfplumber` |
| OpenCV | 图像处理/分割 | `pip install opencv-python` |
| LayoutParser | 布局检测 | `pip install layoutparser` |
| Tesseract OCR | 图片文字识别 | `sudo apt install tesseract-ocr` |
| YOLO | 布局检测（GPU加速） | — |

#### PyMuPDF 提取流水线（已验证）

```python
import fitz, os

doc = fitz.open("paper.pdf")
outdir = "figures_output"
os.makedirs(outdir, exist_ok=True)

# 1. 提取所有嵌入图片
for pn in range(doc.page_count):
    for i, img in enumerate(doc[pn].get_images(full=True)):
        base = doc.extract_image(img[0])
        fname = f"{outdir}/page{pn+1:02d}_img{i:02d}_{base['width']}x{base['height']}.{base['ext']}"
        with open(fname, 'wb') as f:
            f.write(base['image'])

# 2. 提取全文（含嵌入caption文本块）
with open(f"{outdir}/full_text.txt", 'w') as f:
    for pn in range(doc.page_count):
        for block in doc[pn].get_text('blocks'):
            x0, y0, x1, y1, text = block[:5]
            if text.strip():
                f.write(f"[p{pn+1},{x0:.0f},{y0:.0f}] {text.strip()}\n")

# 3. 提取 Figure caption
import re
full_text = '\n'.join([doc[p].get_text() for p in range(doc.page_count)])
for m in re.finditer(r'(Figure\s+\d+[^.]+\.)', full_text):
    print(m.group(1))
```

---

### Stage 2 — 科学理解

#### 图表类型识别

| 类型 | 特征 |
|------|------|
| 显微成像 | 灰度/荧光通道、比例尺 |
| 荧光成像 | 多通道伪彩、merge图 |
| 热图 | 色阶矩阵、行/列聚类树 |
| 火山图 | -log10(p) vs log2FC，阈值线 |
| PCA | 散点+椭圆、方差解释率 |
| UMAP/t-SNE | 点簇分布、perplexity标注 |
| 系统发育树 | 分支拓扑、bootstrap值 |
| Western Blot | 条带、分子量标记 |
| 通路图 | 箭头、节点、酶标注 |
| 工作流程图 | 步骤箭头、方法框 |
| 柱状图 | bar + error bar |
| 箱线图 | box + whisker |
| 小提琴图 | 密度轮廓 |
| 测序QC | FastQC曲线、duplication率 |
| 基因组浏览器 | tracks、reads堆积 |
| 微生物丰度图 | 堆叠柱状/热图+分类 |
| 空间转录组 | 组织切片+表达叠加 |
| 单细胞聚类 | UMAP+marker基因 |

#### 多模态推理
组合：图像内容 + 图表标题 + 邻近段落 + 科学术语 + 面板引用 + 视觉结构

#### 保守推理规则
- 绝不捏造不可读标签、基因名、分类单元、统计数据、方法、显著性、无依据的结论
- 不确定时明确标注不确定性 + 置信度等级
- 置信度：high / moderate / speculative

---

### Stage 2B: Kimi K2.6 视觉 AI 分析 ★核心增强★

> 用多模态 AI 直接"看图说话"，提取纯文本无法获取的数值。

**何时启用**: 当前模型不支持 vision 时**必须启用**；需要精确数值(Kd/RMSD/TPM)时**强烈推荐**。

**完整调用代码**: 见 `references/kimi-k2.6-vision-api.md`

```
核心参数:
  model: "kimi-k2.6"
  base_url: "https://api.moonshot.cn/v1"
  auth: MOONSHOT_API_KEY 环境变量
  图片: base64 data URI
  思考: extra_body={"thinking": {"type": "disabled"}}
```

**数据融合**:
```
Kimi 视觉输出 (数值、标签、趋势)  +  PyMuPDF 文本 (caption、正文、methods)
                    ↓
          结构化报告 (Markdown表格 + JSON)
```

---

### Stage 3 — 图表逆向工程

#### 软件推断

| 视觉特征 | 推断软件 |
|----------|---------|
| 粗边框、Helvetica字体、Prism配色 | GraphPad Prism |
| 灰色背景+白色网格、默认配色 | ggplot2 |
| 蓝/橙默认配色、sans-serif字体 | matplotlib/seaborn |
| UMAP灰色背景+离散色簇 | Seurat / Scanpy |
| 荧光merge图、比例尺标注风格 | ImageJ / Fiji |
| 扁平卡通风格箭头/细胞 | BioRender |
| 通路图+渐变箭头 | Illustrator |
| 细胞分割轮廓 | CellProfiler |

#### 流水线重建
- 归一化方法
- 聚类工作流
- 降维分析
- 差异表达分析
- 测序预处理
- 系统发育工作流
- 微生物分析流程
- 图像定量工作流
- 统计工作流
- 可视化工作流

#### 高级推断（如可行）
- 测序平台
- 染色方法
- 实验模态
- R vs Python 生态
- 出版装配工作流
- 可能的代码生态

---

## ⚠️ 模型能力适配

### Vision 不可用时的两条路径

| 路径 | 条件 | 效果 |
|------|------|------|
| **A: Kimi K2.6 (优先)** | 有 MOONSHOT_API_KEY | ★ 最佳 — 精确提取数值/标签/配色 |
| **B: 纯文本回退** | 无 API Key 或紧急 | 可接受 — 依赖 caption+正文+元数据 |

### 路径B: 纯文本回退流水线

```
1. PyMuPDF 提取嵌入文本 → page.get_text('blocks')
2. 全文正则搜索 → re.findall(r'Figure\s+\d+[^.]*\.', full_text)
3. 正文上下文 → caption 前后 500 字符
4. 图片元数据推断 → 宽高比、页码位置、图片数量
```

## 失败处理

| 情况 | 策略 |
|------|------|
| PDF 提取失败 | 解释原因 + 尝试替代解析器(pdfplumber) |
| 标签缺失 | 用布局和标题结构推断分组 |
| 图像质量差 | 说明限制条件，避免幻觉 |
| Vision 不可用 | **优先 Kimi K2.6** → 不行则走纯文本回退 → 绝不编造视觉内容 |
| Kimi API 401 | 检查 Key 格式(`sk-` vs `sk-kimi-`)、验证端点 |
| Kimi 输出截断 | 增大 `max_tokens`（4096-8192），或分 panel 请求 |

---

## 输出格式

支持两种输出格式：

### 格式A: JSON（机器可读，下游AI工作流）

```json
{
  "figure_id": "Figure 3",
  "caption": "...",
  "overall_summary": "...",
  "subfigures": [...]
}
```

### 格式B: Markdown表格（人类可读，直接交付Boss）

```markdown
## Figure X — 主题概括

| 属性 | 内容 |
|------|------|
| **Panel** | N个 (A–Z) |
| **类型** | xxx |
| **实验方法** | xxx |
| **关键发现** | xxx |

### 软件推断
| 推断 | 置信度 |
|------|--------|
| xxx | high/moderate |

### 逆推流水线
`step1 → step2 → ... → stepN`
```

**选择规则**: Boss 直接查看 → 格式B；下游自动化处理 → 格式A。

---

## 目标期刊覆盖

Nature / Cell / Science / bioRxiv / 密集多面板图 / 显微成像密集型 / 测序图表 / 微生物分析 / 单细胞 / 空间转录组

## 引用

这是小霉的 scientific-figure-analysis skill，整合了 PDF 提取 + Kimi K2.6 视觉 AI + 科学推理的完整流水线。

### 捆绑参考文件
- `references/kimi-k2.6-vision-api.md` — **Kimi K2.6 视觉 API 完整调用模式**（代码模板、参数、陷阱）
- `references/busr-paper-case-study.md` — BusR 论文完整案例（含视觉+文本双路径演示）
