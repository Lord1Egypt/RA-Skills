---
name: duivytools-skills
description: "DuIvyTools (dit) 命令行工具使用指南。当 Agent 需要使用 DuIvyTools 但不清楚命令用法时调用。功能覆盖：(1) XVG 数据可视化 - RMSD、RMSF、能量、氢键、回转半径等；(2) XPM 矩阵可视化 - DCCM、FEL、DSSP 二级结构热图；(3) NDX 索引文件操作 - 查看、合并、提取原子组；(4) 统计分析 - 平均值、标准差、分布、相关性；(5) 拉马钱德兰图绘制；(6) 数据格式转换 - 导出为 CSV/DAT。支持 matplotlib、plotly、gnuplot、plotext 四种绘图引擎。"
---

# DuIvyTools (DIT)

> **重要：使用前务必查看命令帮助**
>
> DuIvyTools 持续开发中。**务必**先运行 `dit <command> -h` 获取该命令最准确、最新的参数信息。

DuIvyTools 是一个命令行工具，用于分析和可视化 GROMACS 分子动力学模拟结果。它提供约 30 个命令，用于处理 XVG、XPM、NDX 等常见的 GROMACS 输出文件。

## 快速入门

### 安装

```bash
pip install DuIvyTools
```

或使用清华镜像（国内更快）：
```bash
pip install DuIvyTools -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 验证安装

```bash
dit
```

### 获取帮助

```bash
dit                    # 所有可用命令
dit -h                 # 全局参数
dit xvg_show -h        # 特定命令帮助（务必先执行此操作！）
```

## 核心概念

### 单位与数据转换

- **GROMACS 默认单位**：时间 = ps，距离 = nm，能量 = kJ/mol
- **默认不转换单位**：除非用户明确要求，否则保留原始单位
- **转换时**：必须同时更新数据和坐标轴标签

### 列与行索引

- **列索引**：从 0 开始（0 = 第一列）
- **行索引**：从 0 开始（0 = 第一行）
- **原子索引（NDX）**：从 1 开始（GROMACS 惯例）
- **范围**：左闭右开（如 `1-7` 表示第 1 至第 6 列）

### XPM 数据类型

- **离散型（Discrete）**：如 DSSP，每个像素代表一个离散状态
- **连续型（Continuous）**：如 DCCM、FEL，每个像素代表一个连续值
- **xpm_diff**：仅适用于连续型，不适用于 DSSP 等离散型

## 命令列表

### XVG 命令（数据可视化）

| 命令 | 功能说明 |
|------|----------|
| `xvg_show` | 显示 XVG 数据，自动解析图例和坐标轴 |
| `xvg_compare` | 比较多个 XVG 文件，支持灵活的列选择 |
| `xvg_ave` | 计算每列的平均值、标准差、标准误 |
| `xvg_show_distribution` | 显示数据分布（直方图/PDF/CDF） |
| `xvg_show_stack` | 绘制堆积面积图 |
| `xvg_show_scatter` | 绘制 2D 或 3D 散点图 |
| `xvg_box_compare` | 使用小提琴图和散点图比较分布 |
| `xvg_combine` | 将多个 XVG 文件的数据合并为一个 |
| `xvg_ave_bar` | 计算并显示平行实验的平均值 |
| `xvg_rama` | 根据 phi/psi 二面角绘制拉式图（Ramachandran plot） |
| `xvg_energy_compute` | 计算蛋白质-配体相互作用能 |

### XPM 命令（矩阵可视化）

| 命令 | 功能说明 |
|------|----------|
| `xpm_show` | 使用 4 种绘图引擎可视化 XPM 矩阵 |
| `xpm2csv` | 将 XPM 转换为 CSV 格式（x, y, value） |
| `xpm2dat` | 将 XPM 转换为 M×N 矩阵格式 |
| `xpm_diff` | 计算两个 XPM 文件的差值（仅连续型） |
| `xpm_merge` | 将两个 XPM 文件沿对角线合并 |

### NDX 命令（索引文件）

| 命令 | 功能说明 |
|------|----------|
| `ndx_add` | 向 NDX 文件添加新的索引组 |
| `ndx_split` | 将一个索引组切分为多个 |
| `ndx_show` | 显示所有索引组名称 |
| `ndx_rm_dup` | 删除重复的索引组 |

### 工具命令

| 命令 | 功能说明 |
|------|----------|
| `mdp_gen` | 生成 GROMACS MDP 文件模板 |
| `show_style` | 显示/生成绘图样式配置文件 |
| `find_center` | 查找原子组的几何中心 |
| `dccm_ascii` | 将 ASCII 协方差矩阵转换为 DCCM XPM |
| `dssp` | 将 GROMACS 2023 DSSP 格式转换为 XPM/XVG |

完整参数说明请参阅 [commands-reference.md](references/commands-reference.md)。

## 绘图引擎

| 引擎 | 适用场景 |
|------|----------|
| `matplotlib`（默认） | 功能最全面，支持所有模式 |
| `plotly` | 交互式图表，适合网页展示 |
| `gnuplot` | 高质量输出，需单独安装 |
| `plotext` | 终端显示，快速预览 |

使用 `-eg` 参数指定引擎：`dit xvg_show -f data.xvg -eg plotly`

## 常用工作流

### 可视化 XVG 数据

```bash
# 基本显示
dit xvg_show -f rmsd.xvg

# 比较多个文件
dit xvg_compare -f rmsd.xvg gyrate.xvg -c 1 1,2 -l RMSD Gyrate

# 计算平均值（从第 2000 行到末尾）
dit xvg_ave -f rmsd.xvg -b 2000

# 显示分布
dit xvg_show_distribution -f gyrate.xvg -c 1
```

### 显示 XPM 矩阵

```bash
# 基本显示
dit xpm_show -f dccm.xpm -cmap coolwarm -zmin -1 -zmax 1

# 3D 模式
dit xpm_show -f fel.xpm -m 3d -x PC1 -y PC2 -z Energy

# 等高线图
dit xpm_show -f dccm.xpm -m contour -cmap coolwarm

# 交互式 plotly
dit xpm_show -f fel.xpm -eg plotly -m 3d
```

更多实际场景请参阅 [examples.md](references/examples.md)。

## 参考文档

- **[commands-reference.md](references/commands-reference.md)** - 完整命令参数说明
- **[examples.md](references/examples.md)** - 实际使用场景示例

## 相关资源

- GitHub: https://github.com/CharlesHahn/DuIvyTools
- 文档: https://duivytools.readthedocs.io/
- 引用: https://doi.org/10.5281/zenodo.6339993