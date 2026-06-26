# Examples — Real-world Processing Workflows / 实际处理示例

## Table of Contents / 目录

- [Example 1: SSRF PBS Sample with Ionchamber / SSRF PBS 样品 + 电离室](#example-1-ssrf-pbs-sample-with-ionchamber--ssrf-pbs-样品--电离室)
- [Example 2: Manual Transmission Value / 手动指定透射率](#example-2-manual-transmission-value--手动指定透射率)
- [Example 3: Format Conversion / 格式转换](#example-3-format-conversion--格式转换)
- [Example 4: 1D Curve Background Estimation / 1D曲线背景估计](#example-4-1d-curve-background-estimation--1d曲线背景估计)
- [Example 5: Batch 1D Curve Processing / 批量1D曲线处理](#example-5-batch-1d-curve-processing--批量1d曲线处理)
- [Example 6: 1D Curve with Reference Background / 1D曲线 + 参考背景](#example-6-1d-curve-with-reference-background--1d曲线--参考背景)
- [Example 7: 1D Curve with Ionchamber Transmission / 1D曲线 + 电离室透过率](#example-7-1d-curve-with-ionchamber-transmission--1d曲线--电离室透过率)
- [Example 8: Batch 1D Curves with Per-file Transmission Map / 批量1D曲线 + 分别设置透过率](#example-8-batch-1d-curves-with-per-file-transmission-map--批量1d曲线--分别设置透过率)
- [Example 9: Image Comparison / 图像对比](#example-9-image-comparison--图像对比)

---

## Example 1: SSRF PBS Sample with Ionchamber / SSRF PBS 样品 + 电离室

Scenario: Process PBS biological SAXS data from SSRF BL19U2 with ionchamber transmission correction.
场景：处理来自 SSRF BL19U2 的 PBS 生物 SAXS 数据，使用电离室透射率校正。

### Data Layout / 数据目录结构

```
project/
├── data/
│   ├── PBS-sd1-1s_00001.tif       # 样品图像 / Sample image
│   ├── PBS-sd1-1s_00002.tif
│   ├── PBS-sd1-1s_00003.tif
│   └── ...
├── bg/
│   └── PBS-bg-5s_00001.tif        # 背景图像 / Background image
├── ionchamber/
│   ├── PBS-sd1-1s_001.Ionchamber  # 样品电离室 / Sample ionchamber
│   ├── PBS-sd1-1s_002.Ionchamber
│   └── PBS-bg-005.Ionchamber      # 背景电离室 / Background ionchamber
└── output/
```

### Step 1: Analyze Ionchamber / 分析电离室

```bash
python BGsub_skills/scripts/ionchamber.py ionchamber/PBS-sd1-1s_001.Ionchamber
# Output: channel means, file name, suggested transmission
# 输出：各通道均值、文件名、建议透射率
```

### Step 2: Batch Background Subtraction / 批量背景扣除

```bash
python BGsub_skills/scripts/bg_batch.py ./data ./bg/PBS-bg-5s_00001.tif \
    --ion-dir ./ionchamber \
    --channel 2 \
    -o ./output \
    --format edf
```

Result / 结果: Each sample image is divided by its transmission T, then the background is subtracted.
每个样品图像除以其透射率 T，再减去背景。

---

## Example 2: Manual Transmission Value / 手动指定透射率

Scenario: You know the transmission is 85% from beamline metadata.
场景：从线站元数据得知透射率为 85%。

```bash
python BGsub_skills/scripts/bg_subtract.py sample.tif background.tif \
    --transmission 85 \
    -o result.tif
```

Formula: `result = sample / 0.85 - background`

---

## Example 3: Format Conversion / 格式转换

Scenario: Convert a directory of TIFF images to EDF format for downstream tools.
场景：将目录下的 TIFF 图像转为 EDF 格式。

```bash
python BGsub_skills/scripts/format_convert.py ./tiff_data \
    -o ./edf_data \
    --output-format edf \
    --pattern "*.tif"
```

---

## Example 4: 1D Curve Background Estimation / 1D曲线背景估计

Scenario: You have integrated 1D curves (q-I format) and need to remove the amorphous background.
场景：已有积分后的 1D 曲线（q-I 格式），需要去除非晶背景。

### Morphological Method / 形态学方法

```bash
python BGsub_skills/scripts/curve_process_1d.py sample.xy \
    --method morph \
    --radius 80 \
    --iterations 2 \
    -o sample_processed.xy \
    --preview
```

### Polynomial Method / 多项式方法

```bash
python BGsub_skills/scripts/curve_process_1d.py sample.xy \
    --method poly \
    --degree 6 \
    --quantile 0.25 \
    -o sample_processed.xy
```

### Rolling Ball Method / 滚球方法

```bash
python BGsub_skills/scripts/curve_process_1d.py sample.xy \
    --method rolling_ball \
    --radius 100 \
    -o sample_processed.xy
```

---

## Example 5: Batch 1D Curve Processing / 批量1D曲线处理

Scenario: A directory of 100 XY curves from a temperature series experiment.
场景：一个包含 100 条 XY 曲线的目录，来自温度系列实验。

```bash
python BGsub_skills/scripts/curve_batch_1d.py ./curves \
    --method morph \
    --radius 60 \
    --iterations 1 \
    --pattern "*.xy" \
    --save-bg \
    -o ./processed \
    --format xy
```

Output naming / 输出命名:
```
curves/sample_001.xy → processed/sample_001_raw.xy
                                   sample_001_bg.xy
                                   sample_001_sub.xy
```

---

## Example 6: 1D Curve with Reference Background / 1D曲线 + 参考背景

Scenario: You have a separate background curve file and want to subtract it from all sample curves.
场景：有一个独立的背景曲线文件，需要从所有样品曲线中扣除。

```bash
python BGsub_skills/scripts/curve_batch_1d.py ./sample_curves \
    --background ./bg_curve.xy \
    --method morph \
    --radius 50 \
    -o ./results
```

公式 / Formula:
```text
result = sample / (T/100) - background
```

---

## Example 7: 1D Curve with Ionchamber Transmission / 1D曲线 + 电离室透过率

Scenario: You have a sample curve, a background curve, and SSRF ionchamber files in one directory.
场景：你有样品曲线、背景曲线，以及同目录下的 SSRF 电离室文件。

```bash
python BGsub_skills/scripts/curve_process_1d.py sample.xy \
    --background background.xy \
    --ion-dir ./ionchamber \
    --sample-channel Ionchamber1 \
    --background-channel Ionchamber1 \
    -o sample_tsub.xy
```

---

## Example 8: Batch 1D Curves with Per-file Transmission Map / 批量1D曲线 + 分别设置透过率

Scenario: Each sample has a different measured transmission and you want deterministic batch processing.
场景：每个样品都有不同透过率，需要可重复的批量处理。

`transmissions.csv`:

```csv
file,transmission
sample_001.xy,88.5
sample_002.xy,91.2
sample_003.xy,94.0
```

```bash
python BGsub_skills/scripts/curve_batch_1d.py ./sample_curves \
    --background ./bg_curve.xy \
    --transmission-map ./transmissions.csv \
    -o ./results
```

---

## Example 9: Image Comparison / 图像对比

Scenario: Compare the processed result with the original to verify quality.
场景：对比处理结果与原始图像以验证质量。

```bash
python BGsub_skills/scripts/compare_images.py original.tif processed.tif
```

Opens a silx CompareImages popup window for interactive visual comparison.
打开 silx CompareImages 弹窗进行交互式视觉对比。
