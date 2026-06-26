# AutoMD-GROMACS

**English** | [中文](#中文说明)

---

## English

### Overview

**AutoMD-GROMACS** is an AI-friendly automation toolkit for GROMACS workflows. It now covers decision-layer routing, core MD execution, enhanced sampling, special-system simulation, advanced analysis, and publication-ready visualization as part of the **AutoMD** ecosystem.

**Author:** Guo Xuan 郭轩  
**Institution:** Hong Kong University of Science and Technology (Guangzhou)  
**Version:** v5.0.0  
**License:** MIT

### Highlights

- Decision-layer routing via `method-selector` before execution
- Core workflow automation for setup, equilibration, production, and preprocessing
- Enhanced sampling methods including umbrella, free energy, replica exchange, metadynamics, steered MD, and related protocols
- Special-system support for membrane, ligand, coarse-grained, electric-field, non-equilibrium, and QM/MM scenarios
- Validation and analysis modules for trajectory, binding, property, membrane, scattering, free-energy, and protein-focused studies
- Publication-ready visualization workflow for figures and reports
- Token-optimized, troubleshooting-first design for AI agents

### Repository Layout

```text
scripts/decision/       decision-layer routing
scripts/basic/          core workflow scripts
scripts/advanced/       sampling and special-system workflows
scripts/analysis/       validation and analysis modules
scripts/visualization/  publication-ready visualization
references/             indexes, target maps, and troubleshooting docs
examples/               example inputs and usage patterns
```

### Installation

```bash
# Via clawhub
clawhub install automd-gromacs

# Via GitHub
git clone https://github.com/Billwanttobetop/automd-gromacs.git
```

### Quick Start

```bash
# Decision-layer routing example
python3 scripts/decision/method-selector.py \
  --goal "binding free energy from a docked complex" \
  --system-type protein-ligand \
  --target-observable binding-free-energy \
  --pretty

# Core setup
bash scripts/basic/setup.sh --input protein.pdb

# Replica exchange example
bash scripts/advanced/replica-exchange.sh

# Validation example
bash scripts/analysis/trajectory-analysis.sh -s md.tpr -f md.xtc

# Publication-ready visualization example
bash scripts/visualization/publication-viz.sh --type plot --data rmsd.xvg
```

### Documentation

- `SKILL.md` - package entry and overview
- `method-selector-SKILL.md` - decision-layer entry
- `references/SKILLS_INDEX.yaml` - structured package index
- `references/METHOD_SELECTION_INDEX.yaml` - routing rules and canonical target map source
- `references/design/decision-target-map.md` - public target naming and layer model
- `references/troubleshoot/` - troubleshooting references

### Requirements

- GROMACS 2026.1+
- Python 3 with `PyYAML` for the decision layer (`pip install pyyaml`)
- Optional tools depending on workflow: PLUMED, acpype, martinize2, CP2K, ORCA, plotting utilities

### Contact

- **GitHub:** [@Billwanttobetop](https://github.com/Billwanttobetop)
- **Email:** xguo608@connect.hkust-gz.edu.cn

---

## 中文说明

### 概述

**AutoMD-GROMACS** 是面向 AI Agent 的 GROMACS 自动化工具包，现已覆盖 decision layer 路由、核心分子动力学流程、增强采样、特殊体系模拟、高级分析与论文级可视化，属于 **AutoMD** 系列生态的一部分。

**作者:** 郭轩 Guo Xuan  
**单位:** 香港科技大学（广州）  
**版本:** v5.0.0  
**许可证:** MIT

### 核心亮点

- 新增 `method-selector` decision layer，在执行前先做 method routing
- 覆盖系统准备、平衡、生产、预处理等核心流程
- 支持 umbrella、free energy、replica exchange、metadynamics、steered MD 等增强采样方法
- 支持膜体系、配体体系、粗粒化、电场、非平衡、QM/MM 等特殊场景
- 提供验证与分析模块，包括轨迹、结合、性质、膜、散射、自由能、蛋白专题等
- 提供论文级图形与结构/轨迹可视化能力
- 面向 AI 协作优化，默认强调低 token 和故障排查

### 目录结构

```text
scripts/decision/       决策层路由
scripts/basic/          核心流程脚本
scripts/advanced/       增强采样与特殊体系脚本
scripts/analysis/       验证与分析模块
scripts/visualization/  论文级可视化模块
references/             索引、target map 与故障排查文档
examples/               示例输入与使用模板
```

### 安装

```bash
# 通过 clawhub
clawhub install automd-gromacs

# 通过 GitHub
git clone https://github.com/Billwanttobetop/automd-gromacs.git
```

### 快速开始

```bash
# Decision layer 路由示例
python3 scripts/decision/method-selector.py \
  --goal "binding free energy from a docked complex" \
  --system-type protein-ligand \
  --target-observable binding-free-energy \
  --pretty

# 系统准备
bash scripts/basic/setup.sh --input protein.pdb

# 副本交换
bash scripts/advanced/replica-exchange.sh

# 高级轨迹分析
bash scripts/analysis/trajectory-analysis.sh -s md.tpr -f md.xtc

# 论文级可视化
bash scripts/visualization/publication-viz.sh --type plot --data rmsd.xvg
```

### 文档

- `SKILL.md` - 包入口与总览
- `method-selector-SKILL.md` - decision layer 入口
- `references/SKILLS_INDEX.yaml` - 结构化索引
- `references/METHOD_SELECTION_INDEX.yaml` - method routing 规则源
- `references/design/decision-target-map.md` - 公开 target 命名与层级说明
- `references/troubleshoot/` - 故障排查文档

### 依赖

- GROMACS 2026.1+
- 按具体工作流可选：PLUMED、acpype、martinize2、CP2K、ORCA、绘图工具等

### 联系方式

- **GitHub:** [@Billwanttobetop](https://github.com/Billwanttobetop)
- **邮箱:** xguo608@connect.hkust-gz.edu.cn
