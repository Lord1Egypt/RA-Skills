# CLI 命令参考 / CLI Commands Reference

## Table of Contents / 目录

- [通用约定 / General Conventions](#通用约定--general-conventions)
- [bg_subtract.py — 单文件 2D 背景扣除](#bg_subtractpy--单文件-2d-背景扣除--single-2d-background-subtraction)
- [bg_batch.py — 批量 2D 处理](#bg_batchpy--批量-2d-处理--batch-2d-processing)
- [ionchamber.py — 电离室分析](#ionchamberpy--电离室分析--ionchamber-analysis)
- [curve_process_1d.py — 单曲线 1D 处理](#curve_process_1dpy--单曲线-1d-处理--single-1d-curve-processing)
- [curve_batch_1d.py — 批量 1D 处理](#curve_batch_1dpy--批量-1d-处理--batch-1d-curve-processing)
- [format_convert.py — 格式转换](#format_convertpy--格式转换--format-conversion)
- [compare_images.py — 图像对比](#compare_imagespy--图像对比--image-comparison)

---

## 通用约定 / General Conventions

- 所有脚本从项目根目录运行 / All scripts run from project root
- 脚本路径前缀: `BGsub_skills/scripts/` / Script path prefix: `BGsub_skills/scripts/`
- 查看帮助: `python <script>.py --help` / View help: `python <script>.py --help`

---

## bg_subtract.py — 单文件 2D 背景扣除 / Single 2D Background Subtraction

```bash
python BGsub_skills/scripts/bg_subtract.py SAMPLE BACKGROUND [OPTIONS]
```

### 参数 / Arguments

| 参数 / Arg | 必需 / Required | 说明 / Description |
|---|---|---|
| SAMPLE | 是 / Yes | 样品图像路径 / Sample image path |
| BACKGROUND | 是 / Yes | 背景图像路径 / Background image path |

### 选项 / Options

| 选项 / Option | 类型 / Type | 默认值 / Default | 说明 / Description |
|---|---|---|---|
| `-o, --output` | PATH | — | 输出文件路径 / Output file path |
| `-t, --transmission` | FLOAT | None | 透射率 (0-1)，覆盖电离室计算 / Transmission (0-1), override ionchamber |
| `--ion-dir` | PATH | None | 电离室文件目录 / Ionchamber file directory |

### 示例 / Examples

```bash
# 基本扣除 / Basic subtraction (T=1.0)
python BGsub_skills/scripts/bg_subtract.py sample.tif background.tif -o result.tif

# 带电离室校正 / With ionchamber correction
python BGsub_skills/scripts/bg_subtract.py sample.tif background.tif --ion-dir ./ionchamber -o result.tif

# 手动透射率 / Manual transmission
python BGsub_skills/scripts/bg_subtract.py sample.tif background.tif -t 0.99 -o result.tif
```

---

## bg_batch.py — 批量 2D 处理 / Batch 2D Processing

```bash
python BGsub_skills/scripts/bg_batch.py SAMPLE_DIR BACKGROUND [OPTIONS]
```

### 参数 / Arguments

| 参数 / Arg | 必需 / Required | 说明 / Description |
|---|---|---|
| SAMPLE_DIR | 是 / Yes | 样品图像目录 / Sample image directory |
| BACKGROUND | 是 / Yes | 背景图像路径 / Background image path |

### 选项 / Options

| 选项 / Option | 类型 / Type | 默认值 / Default | 说明 / Description |
|---|---|---|---|
| `-o, --output-dir` | PATH | `./output` | 输出目录 / Output directory |
| `--pattern` | STRING | `*.tif` | 文件匹配模式 / File glob pattern |
| `--ion-dir` | PATH | SAMPLE_DIR | 电离室文件目录 / Ionchamber directory |
| `-t, --transmission` | FLOAT | None | 统一透射率 / Uniform transmission override |

### 示例 / Examples

```bash
# 批量处理所有 TIFF / Batch all TIFFs
python BGsub_skills/scripts/bg_batch.py ./samples background.tif -o ./results

# 指定模式匹配 / Specify pattern
python BGsub_skills/scripts/bg_batch.py ./samples background.tif --pattern "*.edf" -o ./results

# 带电离室 / With ionchamber
python BGsub_skills/scripts/bg_batch.py ./samples background.tif --ion-dir ./ionchamber -o ./results
```

---

## ionchamber.py — 电离室分析 / Ionchamber Analysis

```bash
python BGsub_skills/scripts/ionchamber.py IONCHAMBER_FILE [OPTIONS]
```

### 参数 / Arguments

| 参数 / Arg | 必需 / Required | 说明 / Description |
|---|---|---|
| IONCHAMBER_FILE | 是 / Yes | 电离室文件路径 / Ionchamber file path |

### 选项 / Options

| 选项 / Option | 类型 / Type | 默认值 / Default | 说明 / Description |
|---|---|---|---|
| `--background-ion` | PATH | None | 背景电离室文件，用于计算样品/背景透过率 / Background ionchamber file |
| `-c, --channel` | CHOICE | `Ionchamber2` | 显示通道 / Channel to display |
| `--method` | CHOICE | `median` | 单文件摘要统计方法 / Single-file summary method |
| `--sample-channel` | CHOICE | `Ionchamber1` | 样品透过率通道 / Sample transmission channel |
| `--background-channel` | CHOICE | `Ionchamber1` | 背景透过率通道 / Background transmission channel |
| `--sample-method` | CHOICE | `median` | 样品统计方法 / Sample summary method |
| `--background-method` | CHOICE | `median` | 背景统计方法 / Background summary method |

### 示例 / Examples

```bash
# Ionchamber2 统计（默认）/ Ionchamber2 stats (default)
python BGsub_skills/scripts/ionchamber.py sample.Ionchamber

# 所有通道 / All channels
python BGsub_skills/scripts/ionchamber.py sample.Ionchamber --channel all

# 样品/背景透过率 / Sample-vs-background transmission
python BGsub_skills/scripts/ionchamber.py sample.Ionchamber --background-ion background.Ionchamber
```

---

## curve_process_1d.py — 单曲线 1D 处理 / Single 1D Curve Processing

```bash
python BGsub_skills/scripts/curve_process_1d.py INPUT [OPTIONS]
```

### 参数 / Arguments

| 参数 / Arg | 必需 / Required | 说明 / Description |
|---|---|---|
| INPUT | 是 / Yes | 输入曲线文件路径 / Input curve file path |

### 选项 / Options

| 选项 / Option | 类型 / Type | 默认值 / Default | 说明 / Description |
|---|---|---|---|
| `--background` | PATH | None | 参考背景曲线；提供后进入 T 修正参考扣除模式 / Reference background curve |
| `--parse-mode` | CHOICE | `single` | 列结构: single/xyxy/xyyy / Column layout |
| `--skip-header` | INT | `0` | 跳过头部行数 / Skip header rows |
| `--delimiter` | CHOICE | `auto` | 分隔符: auto/comma/tab/space / Delimiter |
| `--method` | CHOICE | `morph` | 算法背景估计方法: morph/poly/rolling_ball / Algorithmic method |
| `--radius` | INT | 50 | 形态学/滚球半径 / Morph/RB radius |
| `--iterations` | INT | 1 | 形态学迭代次数 / Morph iterations |
| `--degree` | INT | 4 | 多项式阶数 / Polynomial degree |
| `--quantile` | FLOAT | `0.3` | 多项式分位数 / Polynomial quantile |
| `-o, --output` | PATH | — | 输出文件路径 / Output path |
| `--format` | CHOICE | `auto` | 输出格式: xy/csv/txt/gr/npy/h5 / Output format |
| `--output-mode` | CHOICE | `merged` | 输出模式: merged/per-file / Output mode |
| `--preview` | FLAG | False | 显示 matplotlib 预览 / Show matplotlib preview |
| `-t, --transmission` | FLOAT | None | 手动透过率(%) / Manual transmission percent |
| `--ion-dir` | PATH | None | 电离室目录，自动匹配样品/背景 / Ionchamber directory |
| `--sample-ion` | PATH | None | 显式样品电离室文件 / Explicit sample ionchamber file |
| `--background-ion` | PATH | None | 显式背景电离室文件 / Explicit background ionchamber file |
| `--sample-channel` | CHOICE | `Ionchamber1` | 样品通道 / Sample channel |
| `--background-channel` | CHOICE | `Ionchamber1` | 背景通道 / Background channel |
| `--sample-method` | CHOICE | `median` | 样品统计方法 / Sample summary method |
| `--background-method` | CHOICE | `median` | 背景统计方法 / Background summary method |
| `--match-regex` | STRING | `""` | 自定义匹配正则 / Custom matching regex |

### 示例 / Examples

```bash
# 形态学 / Morphological
python BGsub_skills/scripts/curve_process_1d.py curve.xy --method morph --radius 50 -o result.xy

# 多项式 / Polynomial
python BGsub_skills/scripts/curve_process_1d.py curve.xy --method poly --degree 4 --quantile 0.3 -o result.xy

# 滚球 + 预览 / Rolling ball + preview
python BGsub_skills/scripts/curve_process_1d.py curve.xy --method rolling_ball --radius 80 --preview

# CSV 输入 / CSV input
python BGsub_skills/scripts/curve_process_1d.py curve.csv -o result.xy

# 多列 XYYY 合并 HDF5 / Multi-column XYYY merged HDF5
python BGsub_skills/scripts/curve_process_1d.py curve.txt --parse-mode xyyy --format h5 --output-mode merged -o merged_curves.h5

# 参考背景 + 手动 T / Reference background + manual T
python BGsub_skills/scripts/curve_process_1d.py curve.xy --background bg.xy --transmission 87.5 -o result.xy

# 参考背景 + 电离室 / Reference background + ionchamber
python BGsub_skills/scripts/curve_process_1d.py curve.xy --background bg.xy --ion-dir ./ionchamber -o result.xy
```

---

## curve_batch_1d.py — 批量 1D 处理 / Batch 1D Curve Processing

```bash
python BGsub_skills/scripts/curve_batch_1d.py INPUT_DIR [OPTIONS]
```

### 参数 / Arguments

| 参数 / Arg | 必需 / Required | 说明 / Description |
|---|---|---|
| INPUT_DIR | 是 / Yes | 曲线文件目录 / Curve file directory |

### 选项 / Options

| 选项 / Option | 类型 / Type | 默认值 / Default | 说明 / Description |
|---|---|---|---|
| `--background` | PATH | None | 参考背景曲线 / Reference background curve |
| `--parse-mode` | CHOICE | `single` | 列结构: single/xyxy/xyyy / Column layout |
| `--skip-header` | INT | `0` | 跳过头部行数 / Skip header rows |
| `--delimiter` | CHOICE | `auto` | 分隔符: auto/comma/tab/space / Delimiter |
| `--method` | CHOICE | `morph` | 背景估计方法 / Background estimation method |
| `--radius` | INT | 50 | 半径参数 / Radius parameter |
| `--iterations` | INT | 1 | 形态学迭代次数 / Morph iterations |
| `--degree` | INT | 4 | 多项式阶数 / Polynomial degree |
| `--quantile` | FLOAT | None | 多项式分位数 / Polynomial quantile |
| `-o, --output-dir` | PATH | `./output` | 输出目录 / Output directory |
| `--pattern` | STRING | `*.xy` | 文件匹配模式 / File glob pattern |
| `--format` | CHOICE | `xy` | 输出格式: xy/csv/txt/gr/npy/h5 / Output format |
| `--output-mode` | CHOICE | `per-file` | 输出模式: per-file/merged / Output mode |
| `--merged-output` | STRING | `merged_curves.h5` | 合并输出文件名 / Merged output filename |
| `--save-bg` | FLAG | False | 保存背景 / Save background |
| `--save-sub` | FLAG | True | 保存扣除结果 / Save subtracted |
| `-t, --transmission` | FLOAT | None | 手动统一透过率(%) / Manual unified transmission percent |
| `--transmission-map` | PATH | None | 分别设置透过率 CSV/JSON / Per-file transmission CSV/JSON |
| `--ion-dir` | PATH | None | 电离室目录，自动计算逐文件 T / Ionchamber directory |
| `--sample-channel` | CHOICE | `Ionchamber1` | 样品通道 / Sample channel |
| `--background-channel` | CHOICE | `Ionchamber1` | 背景通道 / Background channel |
| `--sample-method` | CHOICE | `median` | 样品统计方法 / Sample summary method |
| `--background-method` | CHOICE | `median` | 背景统计方法 / Background summary method |
| `--match-regex` | STRING | `""` | 自定义匹配正则 / Custom matching regex |

### 示例 / Examples

```bash
# 批量形态学 / Batch morphological
python BGsub_skills/scripts/curve_batch_1d.py ./curves --method morph --radius 50 -o ./output

# 批量多项式 + 保存背景 / Batch polynomial + save background
python BGsub_skills/scripts/curve_batch_1d.py ./curves --method poly --degree 4 --save-bg -o ./output

# CSV 批量 / CSV batch
python BGsub_skills/scripts/curve_batch_1d.py ./csv_data --pattern "*.csv" -o ./output

# 多列 XYXY + 合并输出 / Multi-column XYXY + merged output
python BGsub_skills/scripts/curve_batch_1d.py ./curves --parse-mode xyxy --output-mode merged --merged-output merged_xyxy.h5 --pattern "*.txt" -o ./output

# 参考背景 + 分别设置 T / Reference background + per-file T
python BGsub_skills/scripts/curve_batch_1d.py ./curves --background bg.xy --transmission-map transmissions.csv -o ./output

# 参考背景 + 电离室 / Reference background + ionchamber
python BGsub_skills/scripts/curve_batch_1d.py ./curves --background bg.xy --ion-dir ./ionchamber -o ./output
```

多列说明 / Multi-column note:
- `single`: 默认两列 XY
- `xyxy`: `(x1,y1)(x2,y2)...`
- `xyyy`: `x,y1,y2,...`
- 多列模式下当前不支持 `--ion-dir` 自动电离室 T

---

## format_convert.py — 格式转换 / Format Conversion

```bash
python BGsub_skills/scripts/format_convert.py INPUT -o OUTPUT [OPTIONS]
```

### 参数 / Arguments

| 参数 / Arg | 必需 / Required | 说明 / Description |
|---|---|---|
| INPUT | 是 / Yes | 输入文件路径 / Input file path |

### 选项 / Options

| 选项 / Option | 类型 / Type | 默认值 / Default | 说明 / Description |
|---|---|---|---|
| `-o, --output` | PATH | 必需 / Required | 输出文件路径 / Output file path |
| `--format` | CHOICE | auto-detect | 输出格式: edf/tif/tiff / Output format |
| `--frame` | INT | 0 | H5 帧索引 / H5 frame index |

### 示例 / Examples

```bash
# TIFF → EDF
python BGsub_skills/scripts/format_convert.py input.tif -o output.edf --format edf

# EDF → TIFF
python BGsub_skills/scripts/format_convert.py input.edf -o output.tif

# H5 → TIFF（提取第3帧 / Extract frame 3）
python BGsub_skills/scripts/format_convert.py stack.h5 -o frame3.tif --frame 3
```

---

## compare_images.py — 图像对比 / Image Comparison

```bash
python BGsub_skills/scripts/compare_images.py IMAGE1 IMAGE2
```

### 参数 / Arguments

| 参数 / Arg | 必需 / Required | 说明 / Description |
|---|---|---|
| IMAGE1 | 是 / Yes | 第一张图像 / First image |
| IMAGE2 | 是 / Yes | 第二张图像 / Second image |

### 依赖 / Dependencies

需要 silx (含 GUI 支持) / Requires silx (with GUI support)

### 示例 / Examples

```bash
python BGsub_skills/scripts/compare_images.py sample.tif background.tif
python BGsub_skills/scripts/compare_images.py result.tif sample.tif
```
