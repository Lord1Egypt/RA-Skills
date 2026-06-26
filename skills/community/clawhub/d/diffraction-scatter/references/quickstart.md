# Quick Start / 快速开始

## When to Use / 适用场景

The user already has a `.poni` file and wants integration, not calibration.
你已经有 `.poni` 文件，现在要继续做积分，而不是重新校准。

## Three Steps / 三步流程

1. Inspect `.poni` and inputs / 检查 `.poni` 与输入：

```bash
python pyfaiskills/scripts/inspect_poni.py --poni geometry.poni sample.h5
```

2. Install pyFAI if needed / 如无环境，安装 pyFAI：

```bash
python pyfaiskills/scripts/install_pyfai_env.py --venv .venv-pyfai
```

3. Run integration / 运行积分：

```bash
python pyfaiskills/scripts/integrate_with_poni.py \
  --mode radial1d --poni geometry.poni -i "data/**/*.edf" -o output/radial
```

## Outputs / 输出说明

- 1D modes: `.csv` + `.h5` per frame / 每帧输出 `.csv` + `.h5`
- 2D modes: `.npz` + `.h5` per frame / 每帧输出 `.npz` + `.h5`
- Every run writes `manifest.jsonl` / 所有运行都会生成 `manifest.jsonl`
- Progress as JSONL on stdout / 进度以 JSONL 打到标准输出
