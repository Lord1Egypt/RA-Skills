---
name: bubble-plot
description: "在需要基于基因表达数据画气泡图（dot plot）时使用。适用于单细胞 RNA-seq、空间转录组等场景，按细胞类型 × 癌种展示基因表达比例和均值。"
metadata: { "openclaw": { "emoji": "🫧", "requires": { "bins": ["python3"] } } }
---

# Skill: 气泡图生成器 (bubble-plot)

基于基因表达矩阵数据，生成按**细胞类型 × 癌种**分组的气泡图（dot plot）。

## 何时使用

- 用户上传 TSV/CSV 表达数据文件，并要求画气泡图、dot plot、泡泡图
- 用户说"画气泡图"、"bubble plot"、"dot plot"并提供了数据文件
- 用户提供数据文件和基因列表，要求可视化表达模式

## 常见触发词

- 画气泡图
- bubble plot
- dot plot
- 泡泡图
- 气泡图可视化
- 表达气泡图

## 执行清单

### 1. 检查数据与环境

- 确认用户提供了数据文件（TSV/CSV）
- 确认文件已下载到工作目录
- 确认 Python 3 + pandas + matplotlib 已安装（缺失时 `pip3 install --break-system-packages pandas matplotlib`）

### 2. 了解数据结构

读取文件前几行，识别以下关键列：

| 角色 | 识别关键词 | 示例列名 |
|------|-----------|---------|
| 细胞类型 | `majorCluster`, `cell_type`, `cluster` | `majorCluster` |
| 组织类型 | `tissue`, `class`, `condition`, `group` | `tissue` |
| 癌种 | `cancerType`, `cancer_type`, `disease` | `cancerType` |
| 基因表达 | 所有数值型非元数据列 | `FOLR1`, `TACSTD2`, `MET` ... |

- 如果用户指定了基因列表，只画指定的
- 如果用户未指定，自动检测所有数值型非元数据列
- 将 `Adjacent` 等正常组织名称统一映射为 `Normal`

### 3. 运行脚本

```bash
# 基本用法 — 自动检测所有基因
python3 skills/bubble-plot/bubble_plot.py <data.tsv>

# 只画指定基因
python3 skills/bubble-plot/bubble_plot.py <data.tsv> --genes FOLR1 TACSTD2 MET

# 自定义列名（如果自动检测失败）
python3 skills/bubble-plot/bubble_plot.py <data.tsv> --genes FOLR1 MET --cell-col CellType --cancer-col Disease

# 不按组织类型拆分
python3 skills/bubble-plot/bubble_plot.py <data.tsv> --no-split-tissue

# 自定义输出目录和分辨率
python3 skills/bubble-plot/bubble_plot.py <data.tsv> -o my_plots --dpi 600
```

### 4. 输出文件

- 默认输出到 `bubble_plots/` 目录
- 每个基因 × 组织类型 = 1 个 PNG（300dpi）+ 1 个 PDF
- 文件命名：`{基因}_dotplot_{Normal|Tumor}.{png|pdf}`

### 5. 向用户报告结果

- 列出生成的文件清单和大小
- 如果有基因在数据中不存在，明确告知并跳过
- 展示 1-2 张关键图的预览

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `input` | 必填 | 输入 TSV 或 CSV 文件路径 |
| `--genes / -g` | 自动检测 | 要画的基因名列表 |
| `--cell-col` | 自动检测 | 细胞类型列名 |
| `--cancer-col` | 自动检测 | 癌种/疾病列名 |
| `--tissue-col` | 自动检测 | 组织类型列名 |
| `--split-tissue` | True | 按组织类型拆分画图 |
| `--no-split-tissue` | - | 不拆分，所有数据画一张 |
| `--outdir / -o` | `bubble_plots` | 输出目录 |
| `--dpi` | 300 | PNG 分辨率 |

## 图例说明

- **气泡颜色**：标准化平均表达量（0-1，红=高，蓝=低，RdBu_r 色谱）
- **气泡大小**：阳性细胞百分比（该细胞类型中表达量 > 0 的比例）

## 自检

- 数据文件是否已确认下载到本地
- 基因列名是否与数据中一致（区分大小写）
- `tissue` 列中 `Adjacent` 是否已映射为 `Normal`
- 输出是否包含 PNG 和 PDF 两种格式
- 缺失的基因是否已告知用户
