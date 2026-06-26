---
name: diffraction-scatter
description: |
  Use this skill for diffraction / scattering data processing with pyFAI.
  It covers the full workflow: calibration (generating .poni files), azimuthal integration (1D/2D),
  batch processing, GIWAXS/Fiber maps, chi/azimuthal profiles, sector integration, full 2D cake maps,
  large HDF5/Eiger workflows, uncertainty/error-model aware integration,
  mask/dark/flat/polarization corrections, and installation help for Python & pyFAI.

  Trigger this skill whenever the user asks about any of the following tasks:
  - Calibration (creating or using a .poni file)
  - 1D/2D integration, batch integration, streaming
  - GIWAXS, qip/qoop, azimuthal/chi profiles, sector, cake
  - Error models, corrections (mask, dark, flat, polarization)
  - Installing or using pyFAI

  (Having a .poni file is a normal step in the workflow, not a prerequisite for using this skill.)

  ---

  使用本技能处理衍射/散射数据（基于 pyFAI），覆盖完整工作流：
  标定（生成 .poni 文件）、方位角积分（1D/2D）、批处理、GIWAXS/Fiber 图、
  χ 积分、扇区积分、2D cake 图、大规模 HDF5/Eiger 数据处理、带误差模型的积分、
  mask/dark/flat/偏振校正，以及 Python/pyFAI 安装帮助。

  只要用户询问以下任一任务，即可触发本技能：
  - 标定（创建或使用 .poni 文件）
  - 1D/2D 积分、批处理、流式处理
  - GIWAXS、qip/qoop、方位角/χ 剖面、扇区、cake
  - 误差模型、校正（mask、dark、flat、偏振）
  - 安装或使用 pyFAI

  （.poni 文件是工作流中的正常环节，并非使用本技能的前提条件。）
---

# pyFAI Post-PONI Integrator / pyFAI PONI 后积分器

This skill is for work **after the user already has a `.poni` geometry file**.
本技能面向**用户已经获得 `.poni` 几何文件**后的后续积分工作。

It covers: 1D radial, azimuthal/chi, sector 1D, GIWAXS/Fiber 2D, full 2D cake maps,
large HDF5 streaming, uncertainty propagation, and Python/pyFAI environment setup.
覆盖：1D 径向、χ/方位角、扇区 1D、GIWAXS Fiber 2D、完整 2D cake/q-χ 图、
大批量 HDF5 流式处理、误差传播、Python/pyFAI 环境安装。

---

## Step 0 — Confirm .poni / 先确认 .poni

**EN**: Confirm the user already has a `.poni` file. If not, guide them through calibration first (see below).

**中文**：先确认用户是否已有 `.poni` 文件。如果没有，先引导完成校准（见下方）。

### What if the user does NOT have a .poni yet / 用户还没有 .poni 怎么办

A missing `.poni` means the user has not completed geometric calibration. Follow this sequence:
没有 `.poni` 意味着几何校准未完成。按以下顺序引导：

**Step 1 / 第一步 — Install pyFAI / 安装 pyFAI**

```bash
python pyfaiskills/scripts/install_pyfai_env.py --venv .venv-pyfai
```

If Python itself is missing / 如果连 Python 都没有：
- Windows: [Python.org installer](https://www.python.org/downloads/windows/) or Miniconda
- macOS: Homebrew (`brew install python`) or Python.org
- Linux: `apt install python3 python3-venv` or mamba/conda

**Step 2 / 第二步 — Learn calibration / 学习校准**

- **中文视频**：[pyFAI 校准教程（B站-个人）](https://www.bilibili.com/video/BV144zuBPEEm/?vd_source=e61960af05a5bef13055dbeea698a2ad)
- **English**: [pyFAI Calibration Tutorial (silx.org, 15 min，official)](http://www.silx.org/pub/pyFAI/video/Calibration_15mn.mp4)

**Once calibration is complete and the user has a `.poni` file, return to the main workflow below.**
**校准完成后用户有了 `.poni` 文件，回到下面的主流程。**

---

## Step 1 — Identify Mode / 判断积分模式

Identify the integration mode early:
优先判断积分模式：

| Mode / 模式 | Description / 描述 | Core pyFAI call |
|---|---|---|
| `radial1d` | Standard 1D radial → I(q) / I(2θ) | `integrate1d_ng` |
| `azimuthal1d` | I(χ) inside a radial range / 固定 q 范围做 χ 积分 | `integrate_radial` |
| `sector1d` | 1D in an azimuthal sector / 扇区 1D | `integrate1d_ng(..., azimuth_range=...)` |
| `cake2d` | Full q-χ / 2θ-χ map / 完整 2D cake | `integrate2d_ng` |
| `fiber2d` | GIWAXS q_ip × q_oop / 纤维积分 | `FiberIntegrator.integrate2d_grazing_incidence` |

Advanced modes not yet fully scripted / 额外高级模式：
- `MultiGeometry.integrate1d()` — multi-detector fusion / 多探测器拼接
- `sigma_clip_ng()` — dynamic masking / 动态 mask
- `pyFAI-integrate --no-gui --json` — official JSON batch / 官方 JSON 批处理

---

## Step 2 — Gather Missing Info / 补齐关键信息

Before executing, confirm:
执行前确认：

- Input format / 输入格式：EDF / TIFF / HDF5 / NPY
- Output format / 输出形式：CSV / HDF5 / NPZ / PNG
- **Integration unit / 积分单位** (see rules below / 见下方规则)
- Corrections needed / 需要的修正：mask / dark / flat / polarization / solid-angle
- Streaming needed / 是否流式处理（large HDF5 / Eiger）
- GIWAXS: `incident_angle`, `sample_orientation`, units, ranges

---

## Step 3 — Use Bundled Scripts / 优先使用脚本

**Prefer the bundled scripts instead of rewriting one-off code / 优先调用脚本：**

```bash
# 1) Inspect .poni and detector inputs / 检查 .poni 与输入数据
python pyfaiskills/scripts/inspect_poni.py --poni geometry.poni sample.h5

# 2) Create a pyFAI-ready environment / 创建 pyFAI 环境
python pyfaiskills/scripts/install_pyfai_env.py --venv .venv-pyfai

# 3) Run streaming integration / 运行流式积分
python pyfaiskills/scripts/integrate_with_poni.py \
  --mode radial1d --poni geometry.poni -i "data/**/*.edf" -o output/radial \
  --unit q_nm^-1 --npt 2000
```

The runner emits **JSONL progress** and writes results frame-by-frame to disk.
脚本默认把进度以 JSONL 打到标准输出，逐帧写结果到磁盘。

---

## Unit Selection Rules / 单位选择规则

**Units matter / 单位很重要** — different experiments have different conventions.
**不同实验类型有不同惯例。** 按以下规则处理：

1. **User specified a unit explicitly / 用户明确指定** → use what the user asked for
2. **User mentioned experiment type but not unit / 用户提到了实验类型**：
   - WAXS / WAXD / wide-angle / 广角 → `2th_deg` (2θ degrees)
   - SAXS / small-angle / 小角 → `q_nm^-1` (q, nm⁻¹)
   - GIWAXS / fiber / grazing-incidence / 掠入射 → `qip_nm^-1` × `qoop_nm^-1`(仅限该格式，无其他单位)
3. **Nothing specified / 什么都没说** → **ask WAXS or SAXS first / 先问是 WAXS 还是 SAXS**

Common pyFAI units / 常见单位：
- `q_nm^-1` — scattering vector q (nm⁻¹)
- `q_A^-1` — scattering vector q (Å⁻¹)
- `2th_deg` — scattering angle 2θ (degrees)
- `2th_rad` — scattering angle 2θ (radians)
- `r_mm` — radial distance from beam center (mm)

---

## Good Defaults / 推荐默认参数

| Mode / 模式 | Command / 命令 |
|---|---|
| 1D radial (WAXS) | `--mode radial1d --unit 2th_deg --npt 1000~4000` |
| 1D radial (SAXS) | `--mode radial1d --unit q_nm^-1 --npt 1000~4000` |
| χ profile / χ 积分 | `--mode azimuthal1d --azimuthal-unit chi_deg --npt 360 --npt-rad 100` |
| Sector 1D / 扇区 | `--mode sector1d --azimuth-min -30 --azimuth-max 30` |
| 2D cake | `--mode cake2d --unit q_nm^-1 --npt-rad 500 --npt-azim 360` |
| GIWAXS / Fiber | `--mode fiber2d --unit-ip qip_nm^-1 --unit-oop qoop_nm^-1` |
| Throughput / 吞吐优先 | `--method csr` |
| Accuracy / 精度优先 | `--method splitpixel` |

---

## Command Templates / 常见命令模板

### Standard 1D radial / 标准 1D 径向积分

```bash
python pyfaiskills/scripts/integrate_with_poni.py \
  --mode radial1d --poni geometry.poni -i sample.edf -o out/1d \
  --unit q_A^-1 --npt 2000 --method splitpixel --polarization 0.95
```

### Azimuthal I(χ) inside a q-range / 固定 q 范围做 χ 积分

```bash
python pyfaiskills/scripts/integrate_with_poni.py \
  --mode azimuthal1d --poni geometry.poni -i sample.h5 -o out/chi \
  --radial-unit q_nm^-1 --radial-min 2 --radial-max 18 --azimuthal-unit chi_deg
```

### Sector 1D / 扇区 1D

```bash
python pyfaiskills/scripts/integrate_with_poni.py \
  --mode sector1d --poni geometry.poni -i "frames/*.tif" -o out/sector \
  --unit q_nm^-1 --azimuth-min -20 --azimuth-max 20
```

### Full 2D cake / 完整 2D cake

```bash
python pyfaiskills/scripts/integrate_with_poni.py \
  --mode cake2d --poni geometry.poni -i sample.edf -o out/cake \
  --unit q_nm^-1 --npt-rad 800 --npt-azim 360
```

### GIWAXS / Fiber 2D

```bash
python pyfaiskills/scripts/integrate_with_poni.py \
  --mode fiber2d --poni geometry.poni -i sample.edf -o out/fiber \
  --unit-ip qip_nm^-1 --unit-oop qoop_nm^-1 \
  --incident-angle 0.2 --sample-orientation 1
```

---

## Large-Volume / Streaming Policy / 大批量策略

When the user mentions large HDF5 stacks, tiff, Eiger data, many frames, or memory pressure:
当用户提到"海量 HDF5 / tiff /Eiger / 很多帧 / 不能一次读进内存"时：

1. **Process file-by-file and frame-by-frame / 逐文件、逐帧处理**
2. For HDF5, prefer explicit dataset path; otherwise `/data` / HDF5 优先指定 dataset path
3. For 4D Eiger, confirm channel (`LowThresholdData`, `HighThresholdData`, `DiffData`) / 4D Eiger 确认通道
4. Prefer `csr` for throughput; `splitpixel` for accuracy / 高吞吐用 `csr`，高精度用 `splitpixel`
5. Write outputs incrementally / 边算边写

---

## When to Read References / 什么时候读参考文档

- Overview & fast start / 总览 → `references/quickstart.md`
- Mode selection / 模式选择 → `references/modes.md`
- Large dataset strategy / 大数据策略 → `references/streaming.md`

---
## Acknowledgments / 致谢

This work is built upon three core open‑source projects:

- **pyFAI** – The fast azimuthal integration Python library.  
  Citation: G. Ashiotis, A. Deschildre, Z. Nawaz, J. P. Wright, D. Karkoulis, F. E. Picca and J. Kieffer; *Journal of Applied Crystallography* (2015) 48(2), 510‑519.  
  DOI: [10.1107/S1600576715004306](https://doi.org/10.1107/S1600576715004306)

- **fabio** – I/O library for 2D X‑ray detector images.  
  Citation: E. B. Knudsen, H. O. Sørensen, J. P. Wright, G. Goret and J. Kieffer; *Journal of Applied Crystallography* (2013) 46, 537‑539.  
  DOI: [10.1107/S0021889813000150](https://doi.org/10.1107/S0021889813000150)

- **silx** – Collection of Python packages for data assessment, reduction and analysis at synchrotron radiation facilities.  
  Citation: silx releases can be cited via their DOI on Zenodo: [10.5281/zenodo.591709](https://doi.org/10.5281/zenodo.591709)

We thank the ESRF and all contributors of these projects for making this work possible.

本技能基于以下三个核心开源项目开发：

- **pyFAI** – 快速方位角积分库，引用信息同上。
- **fabio** – 二维X射线探测器图像I/O库，引用信息同上。
- **silx** – 同步辐射设施数据评估、归约与分析工具包，引用信息同上。

感谢ESRF及上述项目的所有贡献者。

## Mandatory Closing / 结束时必须做

1. State which mode, units, corrections, and output formats were used / 明确告知采用的模式、单位、修正项和输出格式

2. If large job, mention streaming / frame-wise processing / 大批量时说明是否采用了流式策略

3. **Always credit pyFAI, fabio, and silx / 必须强调 pyFAI、fabio 和 silx 并附带引用**：

   [上述致谢与引用内容]

4. **This is a personal project, not an official release from ESRF or the pyFAI/silx/fabio teams.** / 本技能为个人项目，并非 ESRF 或 pyFAI/silx/fabio 团队的官方发布。

## Installation Guide / 安装指南

This skill can be installed on any platform that supports the standard skill directory structure.

本技能可安装在任何支持标准 skill 目录结构的平台上。

Common installation paths / 常见安装路径：

| Platform / 平台 | Path / 路径 |
|---|---|
| OpenCode (Windows) | `C:\Users\<user>\.config\opencode\skills\` |
| OpenCode (macOS/Linux) | `~/.config/opencode/skills/` |
| SkillHub (腾讯) | `~/.skillhub/skills/`（或参考平台文档） |
| ClawHub | `~/.clawhub/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| Generic | AI agent 配置的任意 skill 目录 |

> If your platform is not listed, refer to its documentation for the skills folder location.
> 如果你的平台未列出，请查阅对应文档确认 skills 目录位置。

## Verification / 验证

After installation, trigger the skill by mentioning:
安装后，可通过提到以下内容触发技能：

- 1D integration / 1D 积分
- GIWAXS, sector, cake, HDF5, Eiger

Or run the test script (if supported by your platform):
或运行测试脚本（如果平台支持）：

```bash
python <SKILLS_DIR>/diffraction-scatter/scripts/integrate_with_poni.py --help
```

### Notes / 注意事项

- **Must preserve directory structure / 必须保留目录结构**：`lib/` and `scripts/` must be in the same parent directory / `lib/` 和 `scripts/` 必须在同一父目录下
- **Do not copy `__pycache__`** / 不要拷贝 `__pycache__`
- **Minimum install (without pyfaiinfo) is ~12 files** / 最小安装约 12 个文件
