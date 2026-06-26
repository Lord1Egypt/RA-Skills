# 快速入门 / Quick Start

## 5分钟上手 BGsub / 5-Minute BGsub Guide

### 场景 A: 2D 图像背景扣除 / Scenario A: 2D Image Background Subtraction

你有一批 PBS 样品的 SAXS 数据，需要用 69 号背景图像扣除背景，并用电离室文件进行透射率校正。
You have PBS sample SAXS data and need to subtract background using image #69, with ionchamber transmission correction.

#### 数据结构 / Data Structure

```
test/
├── PBS-BG-sd1-20s_00069.tif      # 背景图像 / Background image (20s exposure)
├── PBS-BG-sd1-20s_069.Ionchamber # 背景电离室 / Background ionchamber
├── PBS-sd1-1s_00046.tif          # 样品 46 / Sample #46
├── PBS-sd1-1s_046.Ionchamber     # 样品电离室 / Sample ionchamber
└── ...更多样品 / more samples
```

#### 单文件处理 / Single File Processing

```bash
python BGsub_skills/scripts/bg_subtract.py \
    test/PBS-sd1-1s_00046.tif \
    test/PBS-BG-sd1-20s_00069.tif \
    --ion-dir test/ \
    -o test/output/PBS-sd1-1s_00046_bgsub.tif
```

#### 批量处理 / Batch Processing

```bash
python BGsub_skills/scripts/bg_batch.py \
    test/ \
    test/PBS-BG-sd1-20s_00069.tif \
    --ion-dir test/ \
    --pattern "PBS-sd1-1s_*.tif" \
    -o test/output
```

#### 预期输出 / Expected Output

```
test/output/
├── PBS-sd1-1s_00046_bgsub.tif
├── PBS-sd1-1s_00047_bgsub.tif
└── ...
```

正常透射率应在 **99% ~ 101%** 范围内。
Normal transmission should be in the **99% ~ 101%** range.

---

### 场景 B: 1D 曲线背景扣除 / Scenario B: 1D Curve Background Subtraction

你有多个 1D 衍射曲线文件（XY 格式），需要用形态学方法估计并扣除背景。
You have 1D diffraction curve files (XY format) and need to estimate and subtract background using morphological method.

#### 数据结构 / Data Structure

```
curves/
├── sample_001.xy    # q-I 两列 / two-column q-I
├── sample_002.xy
└── ...
```

#### 单曲线处理 / Single Curve Processing

```bash
# 形态学方法 / Morphological method
python BGsub_skills/scripts/curve_process_1d.py \
    curves/sample_001.xy \
    --method morph --radius 50 \
    -o output/sample_001_processed.xy

# 多项式拟合 / Polynomial fitting
python BGsub_skills/scripts/curve_process_1d.py \
    curves/sample_001.xy \
    --method poly --degree 4 --quantile 0.3 \
    -o output/sample_001_sub.xy

# 滚球算法 / Rolling ball
python BGsub_skills/scripts/curve_process_1d.py \
    curves/sample_001.xy \
    --method rolling_ball --radius 80 \
    -o output/sample_001_sub.xy

# 多列 XYYY 合并导出 / Multi-column XYYY merged export
python BGsub_skills/scripts/curve_process_1d.py \
    curves/multi_curve.txt \
    --parse-mode xyyy \
    --output-mode merged \
    -o output/multi_curve_merged.h5
```

#### 批量曲线处理 / Batch Curve Processing

```bash
python BGsub_skills/scripts/curve_batch_1d.py \
    curves/ \
    --method morph --radius 50 \
    --pattern "*.xy" \
    -o output/

# 批量多列 XYXY，逐文件导出 / Batch XYXY, per-file export
python BGsub_skills/scripts/curve_batch_1d.py \
    curves/ \
    --parse-mode xyxy \
    --output-mode per-file \
    --pattern "*.txt" \
    -o output/
```

#### 参考背景 + 手动统一 T / Reference Background + Manual Unified T

```bash
python BGsub_skills/scripts/curve_process_1d.py \
    curves/sample_001.xy \
    --background curves/background.xy \
    --transmission 88.5 \
    -o output/sample_001_tsub.xy
```

#### 参考背景 + 电离室自动 T / Reference Background + Ionchamber T

```bash
python BGsub_skills/scripts/curve_process_1d.py \
    curves/sample_001.xy \
    --background curves/background.xy \
    --ion-dir ionchamber/ \
    --sample-channel Ionchamber1 \
    --background-channel Ionchamber1 \
    -o output/sample_001_tsub.xy
```

#### 批量参考背景 + 分别设置 T / Batch Reference Background + Per-file T

```bash
python BGsub_skills/scripts/curve_batch_1d.py \
    curves/ \
    --background curves/background.xy \
    --transmission-map transmissions.csv \
    --pattern "*.xy" \
    -o output/
```

其中 `transmissions.csv` 示例 / Example `transmissions.csv`:

```csv
file,transmission
sample_001.xy,88.5
sample_002.xy,91.2
```

#### 预期输出 / Expected Output

```
output/
├── sample_001_processed.xy   # 单文件脚本输出：多列(raw/bg/sub) / Single-file output: multi-column raw/bg/sub
├── sample_001_raw.xy         # 批处理原始数据 / Batch raw data
├── sample_001_bg.xy          # 批处理背景 / Batch background (if --save-bg)
├── sample_001_sub.xy         # 批处理扣除结果 / Batch subtracted result
├── multi_curve_merged.h5     # 多曲线合并输出 / Merged multi-curve output
└── ...
```

说明 / Notes:
- `--parse-mode single`：默认两列 XY
- `--parse-mode xyxy`：按 `(x1,y1)(x2,y2)...` 拆分
- `--parse-mode xyyy`：按 `x,y1,y2,...` 拆分
- 多列模式下暂不支持 `--ion-dir` 自动电离室 T

---

### 场景 C: 格式转换 / Scenario C: Format Conversion

```bash
# TIFF → EDF
python BGsub_skills/scripts/format_convert.py input.tif -o output.edf --format edf

# EDF → TIFF
python BGsub_skills/scripts/format_convert.py input.edf -o output.tif --format tif

# H5 → TIFF (提取第一帧 / Extract first frame)
python BGsub_skills/scripts/format_convert.py stack.h5 -o frame0.tif --frame 0
```

---

### 场景 D: 图像对比 / Scenario D: Image Comparison

```bash
# 使用 silx CompareImages 弹窗对比 / Compare with silx popup
python BGsub_skills/scripts/compare_images.py sample.tif background.tif
```

---

## 透射率计算公式 / Transmission Formula

```text
T(%) = I_sample / I_background × 100
result = sample / (T/100) - background
```

其中 `I` 可由 `Ionchamber0/1/2` 任一通道的 `mean / median / trimmed_mean` 给出。
Here `I` can come from any `Ionchamber0/1/2` channel using `mean / median / trimmed_mean`.

## 常见问题 / FAQ

**Q: 电离室文件不在同一目录？ / Ionchamber files in different directory?**
```bash
--ion-dir /path/to/ionchamber/files
```

**Q: 不想用电离室校正？ / Skip ionchamber correction?**
```bash
python BGsub_skills/scripts/bg_subtract.py sample.tif background.tif -o result.tif
# 使用 T=1.0 / Uses T=1.0
```

**Q: 1D 曲线格式是 CSV？ / 1D curve is CSV format?**
```bash
python BGsub_skills/scripts/curve_process_1d.py curve.csv -o result.xy
# 自动识别 CSV / CSV is auto-detected
```

**Q: 我想给每条 1D 曲线分别设置 T？ / I need per-file T for 1D curves?**
```bash
python BGsub_skills/scripts/curve_batch_1d.py ./curves \
    --background ./bg.xy \
    --transmission-map transmissions.csv \
    -o ./output
```
