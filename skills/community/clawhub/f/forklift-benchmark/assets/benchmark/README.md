# FK-Bench v2 · 叉车具身智能 Benchmark

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](#-quickstart)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-success.svg)](.github/workflows/ci.yml)
[![Dataset](https://img.shields.io/badge/dataset-722_items-orange.svg)](data/v2.0/)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen.svg)](CHANGELOG.md)
[![Cite](https://img.shields.io/badge/cite-CITATION.cff-lightgrey.svg)](CITATION.cff)

> **FK-Bench v2**（Forklift Embodied Intelligence Benchmark v2）是一个面向
> 平衡重式叉车场景的 **多模态具身智能评测基准**，共 **722** 道题目，覆盖
> **6 个评估模块** 与 **7 个工业场景**，并附带 **3 层自动打分引擎** 与
> **物理 / 安全静态校验器**。

[English README](README.en.md) | [快速开始](docs/quickstart.md) |
[数据规范](docs/schema.md) | [打分公式](docs/scoring.md) | [模块说明](docs/modules.md)

---

## ✨ 核心特性

- **722 题三批构成** —— 500 基础题（组合式生成）+ 122 扩充题 A 批 +
  100 扩充题 B 批；统一 seed (`42`)，完全可复现，覆盖 MOD-1
  到 MOD-6 六大能力维度。
- **七种工业场景** —— `S1_HIGH_BAY` / `S2_BLOCK` / `S3_DOCK` /
  `S4_LINE_SIDE` / `S5_VNA` / `S6_OUTDOOR` / `S7_MIXED`。
- **三档难度** —— `basic` / `intermediate` / `edge`（285 / 300 / 137 题）。
- **15 个动作 DSL** —— `NAVIGATE`、`LIFT`、`LOWER`、`TILT_FORWARD`、
  `TILT_BACK`、`SIDESHIFT`、`CLAMP`、`RELEASE`、`ROTATE_CARGO`、
  `FORK_ADJUST`、`TRAVERSE`、`HORN`、`EMERGENCY_STOP`、`RAISE_ALARM`、
  `ASK_CLARIFICATION`。
- **静态校验器** —— 物理（超载、降额、载荷中心）+ 安全（GB/T 43756、
  ISO 3691-1、ISO 23308、TSG 11 红线）+ JSON Schema 校验。
- **三层打分引擎** —— 一票否决（红线）+ 动作序列 LCS（权重 0.4）+
  参数 IoU（权重 0.6），0–100 分。
- **完整知识库** —— 标准文档、物理参数、属具规格、场景拓扑、现场俚语、
  传感器异常模式、可访问参考文献（≥15 条 URL）。
- **端到端 Demo** —— `examples/run_demo.py`，无需联网即可跑通"生成 →
  预测 → 打分 → 报告"全流程。

## 📦 仓库结构

```
forklift-benchmark-v2/
├── README.md               # 中文主 README
├── README.en.md            # 完整英文 README
├── LICENSE                 # Apache-2.0
├── CONTRIBUTING.md         # 贡献指南
├── CHANGELOG.md            # 版本变更日志
├── CITATION.cff            # 学术引用信息
├── pyproject.toml          # 可 pip install -e .
├── requirements.txt        # 运行时依赖
├── requirements-dev.txt    # 开发依赖
├── .gitignore              # Python 通用
├── .github/
│   └── workflows/ci.yml    # GitHub Actions：lint + pytest + build
├── docs/
│   ├── quickstart.md       # 快速开始
│   ├── schema.md           # 数据规范
│   ├── scoring.md          # 打分公式
│   └── modules.md          # 模块说明
├── examples/
│   └── run_demo.py         # 端到端 demo（独立可运行）
├── forklift_benchmark/     # Python 顶层包（含 CLI）
│   ├── __init__.py
│   ├── cli.py
│   └── py.typed
├── dsl/                    # 动作 DSL 与 Pydantic schema
├── generator/              # 组合式生成器
├── validator/              # 物理/安全/Schema 校验器
├── scorer/                 # 三层打分引擎
├── tests/                  # pytest 测试
├── data/
│   └── v2.0/               # index.json（722 题全量汇总）
└── knowledge/              # 专业知识库（标准/物理/属具/场景/俚语/传感器/参考文献）
```

## 🚀 Quickstart

```bash
git clone https://github.com/forklift-benchmark/forklift-benchmark-v2.git
cd forklift-benchmark-v2
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"

# 跑一遍端到端 demo（无需联网，5 题 mini-benchmark）
python examples/run_demo.py

# 跑全部测试
pytest -v
```

完整说明请见 [`docs/quickstart.md`](docs/quickstart.md)。

## 📊 模块与场景分布

| 模块 | 名称                 | 题数 | basic | intermediate | edge |
|------|----------------------|------|-------|--------------|------|
| MOD-1 | 导航与路径规划       | 80   | 32    | 36           | 12   |
| MOD-2 | 载荷与货叉操作       | 100  | 40    | 45           | 15   |
| MOD-3 | 属具感知             | 100  | 40    | 45           | 15   |
| MOD-4 | 安全与红线合规       | 90   | 36    | 40           | 14   |
| MOD-5 | 现场拓扑推理         | 80   | 32    | 36           | 12   |
| MOD-6 | 传感器异常鲁棒性     | 50   | 20    | 22           | 8    |

场景分布：`S1=80 / S2=80 / S3=75 / S4=85 / S5=65 / S6=60 / S7=55`。

> **MOD-4 红线**：所有 90 道题**必须**触发 `SAFETY_ABORT`（`EMERGENCY_STOP`、
> `RAISE_ALARM` 或 `ASK_CLARIFICATION`）决策；任何未中止的方案在该题上
> 一律为 0 分。

## 🔬 打分公式

```
score = 100 · red_line · (0.4 · lcs + 0.6 · iou)
```

* `red_line ∈ {0, 1}`：MOD-4 红线或物理 / 法规硬性约束触发即一票否决。
* `lcs`：预测动作序列与 gold 序列的最长公共子序列相似度（带 Jaccard 微调）。
* `iou`：每个共享数值参数在 10% 容差内的对齐得分。

详见 [`docs/scoring.md`](docs/scoring.md)。

## 🤝 贡献

欢迎以 issue / PR / 数据集增补的方式参与。详细流程见
[`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 📚 引用

如果本 Benchmark 对你的研究有帮助，请按以下 BibTeX 引用：

```bibtex
@misc{fkbenchv2,
  title  = {FK-Bench v2: A 722-Item Multimodal Benchmark for Embodied Forklift Agents},
  year   = {2026},
  version = {2.1.0},
  url    = {https://github.com/forklift-benchmark/forklift-benchmark-v2},
  note   = {Apache-2.0 License}
}
```

或者直接使用仓库根目录下的 [`CITATION.cff`](CITATION.cff)。

## 📄 License

本仓库基于 [Apache License 2.0](LICENSE) 发布。 © 2026 Forklift
Embodied Intelligence Benchmark Authors.
