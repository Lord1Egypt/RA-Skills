# BGsub Skills — 2D / 1D Background Subtraction Toolkit

BGsub Skills is the self-contained CLI layer of BGsub for X-ray diffraction data processing.
BGsub Skills 是 BGsub 的自包含命令行工具层，用于 X 射线衍射数据处理。

It covers 2D detector images (TIFF / EDF / H5) and 1D curves (XY / DAT / CSV / GR), and includes SSRF ionchamber-based transmission correction.
它覆盖 2D 探测器图像（TIFF / EDF / H5）和 1D 曲线（XY / DAT / CSV / GR），并集成基于 SSRF 电离室的透射率校正。

All scripts run directly from this bundle and import from `lib/`; no external BGsub package installation is required.
所有脚本都可直接运行并从 `lib/` 导入；无需额外安装外部 BGsub 包。

Standard scientific Python dependencies are still required, such as `numpy`, `scipy`, `fabio`, `h5py`, and `pandas`.
仍然需要标准科学计算 Python 依赖，例如 `numpy`、`scipy`、`fabio`、`h5py`、`pandas`。

---

## When to Use / 适用场景

Use BGsub Skills when you need any of the following:
当你有以下需求时，可使用 BGsub Skills：

- 2D image background subtraction / 2D 图像背景扣除
- 1D curve background estimation and subtraction / 1D 曲线背景估计与扣除
- T-corrected reference subtraction / T 修正参考背景扣除
- SSRF ionchamber parsing and transmission calculation / SSRF 电离室解析与透射率计算
- Batch processing for TIFF / EDF / H5 or XY / DAT / CSV files / TIFF / EDF / H5 或 XY / DAT / CSV 文件的批量处理
- Format conversion among TIFF / EDF / H5 / TIFF / EDF / H5 格式互转
- Quick visual comparison of two diffraction images / 两张衍射图像的快速可视化对比

Typical trigger phrases include:
常见触发词包括：

- 背景扣除 / background subtraction
- 基线校正 / baseline correction
- SAXS/WAXS/XRD 背景相关处理 / SAXS/WAXS/XRD background-related processing
- 电离室 / ion chamber / ionchamber
- 透射率修正 / transmission correction / transmission
- 基线扣除 / baseline subtraction
- 批量背景扣除 / batch background subtraction
- 图像格式转换 / file format conversion
- TIFF 转 EDF / convert TIFF to EDF

---

## Core Capabilities / 核心能力

| Script / 脚本 | Purpose / 功能 |
|---|---|
| `scripts/bg_subtract.py` | Single 2D image background subtraction / 单文件 2D 背景扣除 |
| `scripts/bg_batch.py` | Batch 2D image processing / 批量 2D 背景扣除 |
| `scripts/ionchamber.py` | Ionchamber statistics and transmission calculation / 电离室统计与透射率计算 |
| `scripts/curve_process_1d.py` | Single 1D curve processing / 单条 1D 曲线处理 |
| `scripts/curve_batch_1d.py` | Batch 1D curve processing / 批量 1D 曲线处理 |
| `scripts/format_convert.py` | TIFF / EDF / H5 format conversion / TIFF / EDF / H5 格式转换 |
| `scripts/compare_images.py` | silx popup-based image comparison / 基于 silx 弹窗的图像对比 |

---

## Quick Start / 快速开始

Run from the project root directory.
请在项目根目录下运行。

```bash
# 2D: single image subtraction / 单张图像背景扣除
python BGsub_skills/scripts/bg_subtract.py sample.tif background.tif --ion-dir ./ionchamber -o result.tif

# 2D: batch subtraction / 批量图像背景扣除
python BGsub_skills/scripts/bg_batch.py ./data background.tif --ion-dir ./ionchamber -o ./output

# 1D: morphological subtraction / 1D 形态学背景扣除
python BGsub_skills/scripts/curve_process_1d.py curve.xy --method morph --radius 50 -o result.xy

# 1D: reference background + manual transmission / 1D 参考背景 + 手动透射率
python BGsub_skills/scripts/curve_process_1d.py curve.xy --background bg.xy --transmission 87.5 -o result.xy

# 1D: batch processing with transmission map / 带透射率映射的 1D 批量处理
python BGsub_skills/scripts/curve_batch_1d.py ./curves --background bg.xy --transmission-map transmissions.csv -o ./output
```

For full CLI options, use:
完整命令行参数请使用：

```bash
python BGsub_skills/scripts/<script>.py --help
```

---

## Key Processing Notes / 关键处理说明

### 2D Reference Subtraction / 2D 参考背景扣除

```text
result = sample / T - background
```

### 1D Reference Subtraction / 1D 参考背景扣除

```text
result = sample / (T/100) - background
```

### Ionchamber Transmission / 电离室透射率

```text
T(%) = I_sample / I_background × 100
```

Files are matched by numeric suffix when possible.
在可自动匹配时，文件通过编号后缀进行关联。

```text
PBS-sd1-1s_00046.tif  ←→  PBS-sd1-1s_046.Ionchamber
```

---

## Important Constraints / 重要约束

- Multi-column 1D layouts (`xyxy` / `xyyy`) are supported.
  支持多列 1D 结构（`xyxy` / `xyyy`）。
- When `--background` is used in multi-column mode, `--ion-dir` auto ionchamber T is currently not supported.
  多列模式下若同时使用 `--background`，当前不支持 `--ion-dir` 自动电离室 T。
- Merged export is supported for text / CSV / HDF5, but exact workflow details should be checked in the reference docs.
  支持文本 / CSV / HDF5 合并导出，具体工作流请查看参考文档。
- `compare_images.py` depends on a GUI-capable environment because it opens a silx popup.
  `compare_images.py` 需要可用的图形界面环境，因为它会打开 silx 弹窗。

---

## Reference Documents / 参考文档

Read the detailed docs in `references/` when the quick commands above are not enough.
如果上方快速命令不够，请阅读 `references/` 中的详细文档。

| File / 文件 | Purpose / 用途 |
|---|---|
| `references/quickstart.md` | 5-minute onboarding with real scenarios / 5 分钟入门与真实场景 |
| `references/cli_commands.md` | Full CLI reference for all scripts / 全部脚本的完整 CLI 参数参考 |
| `references/examples.md` | End-to-end SSRF PBS examples / SSRF PBS 端到端处理示例 |

---

## Directory Layout / 目录结构

```text
BGsub_skills/
├── README.md
├── SKILL.md
├── lib/
├── scripts/
└── references/
```

---

## Acknowledgements / 致谢

We sincerely thank the **fabio** project for providing the reliable image I/O foundation used throughout BGsub Skills.
我们真诚感谢 **fabio** 项目，它为 BGsub Skills 提供了稳定可靠的图像读写基础。

Fabio makes it practical to handle key diffraction image formats such as EDF and TIFF in a unified workflow, which is essential for these 2D workflows.
Fabio 让 EDF、TIFF 等关键衍射图像格式能够在统一工作流中处理，这对这里的 2D 工作流非常关键。

Recommended citation / 推荐引用：

> Knudsen, E. B., Sørensen, H. O., Wright, J. P., Goret, G. & Kieffer, J. (2013). **fabio: Processing of 2D X-ray diffraction data**. *J. Appl. Cryst.* 46, 537–539. http://dx.doi.org/10.1107/S0021889813000150
