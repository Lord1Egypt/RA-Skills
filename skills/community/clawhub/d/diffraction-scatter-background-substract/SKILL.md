---
name: bgsub
description: |
  BGsub — X-ray diffraction (SAXS/WAXS/XRD) background subtraction toolkit for 2D images and 1D curves.
  X射线衍射(SAXS/WAXS/XRD)数据背景扣除工具，覆盖2D图像处理和1D曲线处理。

  Use this skill whenever the user's task involves ANY of the following, even if they don't explicitly mention "BGsub" or "background subtraction":
  请在以下场景触发此 skill，即使用户未明确提及 "BGsub" 或 "背景扣除"：

  - "背景扣除", "background subtraction", "扣除背景", "去掉背景", "减背景"
  - "基线校正", "基线扣除", "基线拟合", "baseline correction", "baseline subtraction", "subtract background", "background estimation"
  - "SAXS", "WAXS", "XRD", "GIWAXS", "散射", "衍射", "小角散射背景扣除", "small-angle scattering background subtraction", "diffraction pattern"
  - "SSRF电离室", "电离室", "ionchamber", "ion chamber", "ionchamber file", "透射率校正", "透射率修正", "transmission correction", "transmission", "透过率", "T-背景", "T-background", "T修正", "T-correction"
  - "批量处理TIFF/EDF/H5文件", "batch process images", "batch background subtraction", "批量背景扣除", "格式转换", "图像格式转换", "file format conversion", "convert TIFF to EDF"
  - "PBS数据", "生物SAS", "biological SAS", "蛋白散射", "protein scattering", "生物样品散射"
  - "1D曲线处理", "1D curve processing", "曲线背景扣除", "XY曲线", "XY data", "积分曲线", "integrated curve", "curve smoothing", "基线拟合"
  - "形态学背景", "morphological background", "形态学", "多项式拟合", "polynomial fit", "滚球算法", "rolling ball"
  - User uploaded .Ionchamber files and needs X-ray data processing
  - User wants to subtract a known background image from signal images
  - User wants to estimate and subtract background from 1D diffraction curves
  - User mentions "T-背景", "T-background", "透射率修正", or asks how to correct for transmission in XRD data

compatibility: opencode
---

# BGsub Skill — 2D Image & 1D Curve Background Subtraction / 2D图像与1D曲线背景扣除

BGsub is a **self-contained** CLI toolkit for background subtraction of X-ray diffraction data. It covers **2D detector image processing** (TIFF/EDF/H5) and **1D curve processing** (XY/DAT/CSV), with SSRF ionchamber transmission auto-correction. **No external BGsub package installation is required** — all dependencies are bundled in `lib/`, though standard scientific Python dependencies are still needed.
BGsub 是一套**自包含**的 X 射线衍射数据背景扣除 CLI 工具集，覆盖**2D探测器图像处理**(TIFF/EDF/H5)和**1D曲线处理**(XY/DAT/CSV)，集成 SSRF 电离室透射率自动校正。**无需安装外部 BGsub 包**——所有依赖已打包在 `lib/` 中，但仍需标准科学计算 Python 依赖。

Latest 1D highlights / 最新 1D 特性：
- **T-背景扣除** 为首要模式 / **T-background subtraction** is the primary mode
- 支持多列文本结构 `single / xyxy / xyyy`
- 支持 **逐一文件** 与 **合并单文件** 导出
- 合并导出支持文本/CSV/HDF5；多列模式下暂不支持电离室自动 T

---

## Core Capabilities / 核心能力

| # | Capability / 能力 | Domain / 领域 | Script / 脚本 |
|---|---|---|---|
| 1 | Reference-based 2D background subtraction / 有参考2D背景扣除 | 2D Image | `bg_subtract.py` |
| 2 | Batch 2D processing with ionchamber / 批量2D处理+电离室 | 2D Image | `bg_batch.py` |
| 3 | Ionchamber stats + sample/background transmission / 电离室统计与样品/背景透过率 | Shared | `ionchamber.py` |
| 4 | 1D curve background estimation & T-corrected reference subtraction / 1D曲线算法背景估计与T修正参考扣除 | 1D Curve | `curve_process_1d.py` |
| 5 | Batch 1D curve processing with unified / per-file / ionchamber T / 批量1D曲线处理（统一T/分别设置/电离室） | 1D Curve | `curve_batch_1d.py` |
| 6 | Format conversion (TIFF/EDF/H5) / 格式转换 | 2D Image | `format_convert.py` |
| 7 | silx image comparison popup / silx图像对比弹窗 | 2D Image | `compare_images.py` |

---

## Processing Flow / 处理流程

### 2D Image Background Subtraction / 2D图像背景扣除

```
Sample image + Ionchamber file / 样品图像 + 电离室文件
         ↓
    Calculate T = I_sample / I_background / 计算透射率
         ↓
result = sample / T - background
         ↓
    Save result image / 保存结果图像
```

### 1D Curve Background Estimation / 1D曲线背景估计

```
Load 1D curve file (XY/DAT/CSV) / 加载1D曲线文件
         ↓
Choose column layout: single / xyxy / xyyy / 选择列结构
         ↓
    Estimate background using algorithm / 使用算法估计背景
    (Morphological / Polynomial / Rolling Ball)
         ↓
    Subtract: result = curve - background / 扣除背景
         ↓
    Save raw, background, subtracted / 保存原始、背景、扣除结果
```

### 1D Reference Background Subtraction / 1D参考背景扣除

```
Sample curve + background curve / 样品曲线 + 背景曲线
         ↓
Transmission source / 透过率来源
  - manual unified / 手动统一值
  - manual per-file / 手动分别设置
  - ionchamber auto / 电离室自动计算
         ↓
result = sample / (T/100) - background
         ↓
Save raw, background, subtracted / 保存原始、背景、扣除结果
```

---

## Quick Usage / 快速使用

### Run Scripts Directly / 直接运行脚本

Scripts are **self-contained** — they import from the bundled `lib/` package instead of requiring the BGsub package to be installed. Run from the project root directory. Only standard scientific dependencies are needed: `numpy`, `scipy`, `fabio`, `h5py`, `pandas`.
脚本为**自包含可执行文件**——从内含的 `lib/` 包导入，无需安装 BGsub 包。在项目根目录下运行。仅需标准科学计算依赖：`numpy`、`scipy`、`fabio`、`h5py`、`pandas`。

```bash
# 2D: Single file background subtraction / 单文件背景扣除
python BGsub_skills/scripts/bg_subtract.py sample.tif background.tif --ion-dir ./ionchamber -o result.tif

# 2D: Batch processing / 批量处理
python BGsub_skills/scripts/bg_batch.py ./data background.tif --ion-dir ./ionchamber -o ./results

# 2D/1D: Ionchamber analysis / 电离室数据分析
python BGsub_skills/scripts/ionchamber.py sample.Ionchamber

# 2D/1D: Sample-vs-background transmission / 样品-背景透过率
python BGsub_skills/scripts/ionchamber.py sample.Ionchamber --background-ion background.Ionchamber

# 2D: Format conversion / 格式转换
python BGsub_skills/scripts/format_convert.py input.tif -o output.edf --format edf

# 2D: Image comparison (silx popup) / 图像对比(silx弹窗)
python BGsub_skills/scripts/compare_images.py image1.tif image2.tif

# 1D: Single curve processing / 单曲线处理
python BGsub_skills/scripts/curve_process_1d.py curve.xy --method morph --radius 50 -o result.xy

# 1D: Multi-column XYYY merged export / 多列 XYYY 合并导出
python BGsub_skills/scripts/curve_process_1d.py curve.txt --parse-mode xyyy --output-mode merged -o merged_curves.h5

# 1D: Reference background + manual T / 参考背景 + 手动T
python BGsub_skills/scripts/curve_process_1d.py curve.xy --background bg.xy --transmission 87.5 -o result.xy

# 1D: Reference background + ionchamber / 参考背景 + 电离室
python BGsub_skills/scripts/curve_process_1d.py curve.xy --background bg.xy --ion-dir ./ionchamber -o result.xy

# 1D: Batch curve processing / 批量曲线处理
python BGsub_skills/scripts/curve_batch_1d.py ./curves --method morph --radius 50 -o ./output

# 1D: Batch reference background + per-file T / 批量参考背景 + 分别设置T
python BGsub_skills/scripts/curve_batch_1d.py ./curves --background bg.xy --transmission-map transmissions.csv -o ./output
```

---

## SSRF Ionchamber File Format / SSRF电离室文件格式

Plain text format (extension `.Ionchamber` or `.txt`) / 纯文本格式：

```
# Time  Ionchamber0  Ionchamber1  Ionchamber2
2026-01-19 12:34:34.130671238  2.807135e-7  2.388761e-8  9.71103e-10
```

| Channel / 通道 | Description / 说明 |
|---|---|
| Ionchamber0 | Incident beam intensity / 入射光强度 |
| Ionchamber1 | Transmitted beam (intermediate) / 透射光(中间) |
| Ionchamber2 | Transmitted beam (primary measurement) / 透射光(主测量) |

**Transmission / 透射率**: `T = I_sample / I_background × 100%`

Where `I_sample` and `I_background` are user-selectable channel statistics (mean / median / trimmed_mean).
其中 `I_sample` 与 `I_background` 由用户选择通道和统计方式（mean / median / trimmed_mean）。

### File Matching Rules / 文件匹配规则

Ionchamber files auto-match with images by number / 电离室文件通过编号自动匹配：

```
PBS-sd1-1s_00046.tif  ←→  PBS-sd1-1s_046.Ionchamber
   (auto-match _00046.tif → _046.Ionchamber)
```

---

## 1D Curve Processing Details / 1D曲线处理详情

### Supported Input Formats / 支持的输入格式

| Format / 格式 | Extensions / 扩展名 |
|---|---|
| XY / DAT / TXT | `.xy`, `.dat`, `.txt` (single XY / xyxy / xyyy) |
| CSV | `.csv` (single XY / xyyy) |
| GR | `.gr` |

### Background Estimation Methods / 背景估计方法

| Method / 方法 | Key Parameter / 关键参数 | Use Case / 适用场景 |
|---|---|---|
| `morph` (Morphological) / 形态学 | `--radius` (default: 50) | Broad features, smooth background / 宽衍射峰, 平滑背景 |
| `poly` (Polynomial) / 多项式 | `--degree` (default: 4), `--quantile` | Amorphous halo fitting / 非晶晕拟合 |
| `rolling_ball` / 滚球 | `--radius` (default: 50) | Complex baseline / 复杂基线 |

### 1D Output Format / 1D输出格式

Default batch output is per-file split export. Merged single-file output is also supported / 默认批处理为逐文件拆分导出，也支持合并单文件导出：
```
原始: sample_001.xy
→ sample_001_raw.xy   (raw data / 原始数据)
→ sample_001_bg.xy    (estimated background / 估计背景, optional / 可选)
→ sample_001_sub.xy   (subtracted result / 扣除结果, optional / 可选)
```

### 1D Transmission Sources / 1D透过率来源

- `--transmission 85` → unified manual transmission / 手动统一透过率
- `--transmission-map transmissions.csv` → per-file transmission / 分别设置透过率
- `--ion-dir ./ionchamber` → auto-match ionchamber files and calculate T / 自动匹配电离室并计算逐文件 T

### Multi-column Constraints / 多列约束

- `--parse-mode xyxy`：按 `(x1,y1)(x2,y2)...` 展开多条曲线
- `--parse-mode xyyy`：按 `x,y1,y2,...` 展开多条曲线
- 多列模式下若使用 `--background`，当前**不支持** `--ion-dir` 自动电离室 T

When `--background` is provided, BGsub uses the traditional reference formula:
当提供 `--background` 时，BGsub 使用传统参考扣除公式：

```text
result = sample / (T/100) - background
```

---

## Reference Documents / 参考文档

When the user's request goes beyond the quick usage examples above, read the appropriate reference file for detailed guidance. Each file serves a specific purpose — only read what you need.
当用户的需求超出上方快速使用示例时，请阅读对应的参考文档获取详细指引。每个文件有特定用途——只读你需要的。

| When to read / 何时阅读 | File / 文件 | Content / 内容 |
|---|---|---|
| User is new to BGsub or needs step-by-step walkthrough / 新手入门或需要分步引导 | `references/quickstart.md` | 5-minute quick start with 4 real scenarios / 5分钟快速入门，含4个实际场景 |
| User asks about specific CLI flags, parameters, or default values / 用户询问具体 CLI 参数或默认值 | `references/cli_commands.md` | Full CLI command reference for all 7 scripts / 全部 7 个脚本的 CLI 命令参考 |
| User provides real data and wants end-to-end processing guidance / 用户提供真实数据需要端到端处理指引 | `references/examples.md` | 9 real-world SSRF PBS processing examples / 9 个 SSRF PBS 实际处理示例 |

---

## Script Reference / 脚本参考

### Directory Structure / 目录结构

```
BGsub_skills/
├── SKILL.md           # This file / 本文件
├── lib/               # Self-contained library (no external BGsub needed) / 自包含库（无需外部BGsub）
│   ├── __init__.py
│   ├── image_io.py    # Image I/O (TIFF/EDF/H5) / 图像读写
│   ├── common.py      # Ionchamber & transmission utilities / 电离室与透射率工具
│   ├── curve_data.py  # 1D curve data model / 1D曲线数据模型
│   ├── curve_io.py    # 1D curve I/O / 1D曲线读写
│   ├── curve_processor.py  # Background estimation algorithms / 背景估计算法
│   └── task_pipeline.py    # Batch pipeline engine / 批处理管线引擎
├── scripts/           # CLI scripts (import from lib/) / CLI脚本（从lib/导入）
└── references/        # Detailed docs / 详细文档
```

### Scripts / 脚本

| Script / 脚本 | Function / 功能 |
|---|---|
| `scripts/bg_subtract.py` | Single 2D image background subtraction / 单文件2D背景扣除 |
| `scripts/bg_batch.py` | Batch 2D image processing / 批量2D处理 |
| `scripts/ionchamber.py` | Ionchamber data analysis / 电离室数据分析 |
| `scripts/curve_process_1d.py` | Single 1D curve processing / 单曲线1D处理 |
| `scripts/curve_batch_1d.py` | Batch 1D curve processing / 批量1D曲线处理 |
| `scripts/format_convert.py` | TIFF/EDF/H5 format conversion / 格式转换 |
| `scripts/compare_images.py` | silx CompareImages popup / silx图像对比弹窗 |

Usage / 使用方法: `python BGsub_skills/scripts/<script>.py --help`
