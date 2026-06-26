# DuIvyTools 命令参考文档

本文件包含所有命令的详细参数说明。关于核心概念和快速入门，请参考主 SKILL.md 文件。

> **重要说明**：不同命令支持的参数不同。以下列出的是所有可能的参数，具体某个命令支持哪些参数，请使用 `dit <command> -h` 查看。

## 目录

- [DuIvyTools 命令参考文档](#duivytools-命令参考文档)
  - [目录](#目录)
  - [通用参数说明](#通用参数说明)
    - [输入输出参数](#输入输出参数)
    - [数据选择参数](#数据选择参数)
    - [绘图标签参数](#绘图标签参数)
    - [数据范围参数](#数据范围参数)
    - [数据变换参数](#数据变换参数)
    - [绘图控制参数](#绘图控制参数)
    - [统计分析参数](#统计分析参数)
    - [插值参数](#插值参数)
    - [模式参数](#模式参数)
  - [XVG 命令](#xvg-命令)
    - [xvg\_show](#xvg_show)
    - [xvg\_compare](#xvg_compare)
    - [xvg\_ave](#xvg_ave)
    - [xvg\_show\_distribution](#xvg_show_distribution)
    - [xvg\_show\_stack](#xvg_show_stack)
    - [xvg\_show\_scatter](#xvg_show_scatter)
    - [xvg\_box\_compare](#xvg_box_compare)
    - [xvg\_combine](#xvg_combine)
    - [xvg\_ave\_bar](#xvg_ave_bar)
    - [xvg\_rama](#xvg_rama)
    - [xvg\_energy\_compute](#xvg_energy_compute)
  - [XPM 命令](#xpm-命令)
    - [xpm\_show](#xpm_show)
    - [xpm2csv](#xpm2csv)
    - [xpm2dat](#xpm2dat)
    - [xpm\_diff](#xpm_diff)
    - [xpm\_merge](#xpm_merge)
  - [NDX 命令](#ndx-命令)
    - [ndx\_add](#ndx_add)
    - [ndx\_split](#ndx_split)
    - [ndx\_show](#ndx_show)
    - [ndx\_rm\_dup](#ndx_rm_dup)
  - [其他命令](#其他命令)
    - [mdp\_gen](#mdp_gen)
    - [show\_style](#show_style)
    - [find\_center](#find_center)
    - [dccm\_ascii](#dccm_ascii)
    - [dssp](#dssp)
  - [常用 Colormap 参考](#常用-colormap-参考)

---

## 通用参数说明

以下是 DuIvyTools 各命令可能支持的参数。**不同命令支持的参数不同**，具体请查看 `dit <command> -h`。

### 输入输出参数

| 参数 | 说明 |
|------|------|
| `-f INPUT [INPUT ...]` | 输入文件（一个或多个） |
| `-o OUTPUT` | 输出文件名 |

### 数据选择参数

| 参数 | 说明 |
|------|------|
| `-c COLUMNS [COLUMNS ...]` | 选择数据列索引（0-based）。格式：`1-7,10` 表示第1到6列和第10列。多组文件：`1-7,10 0,1,4` |
| `-b BEGIN` | 起始行索引（包含） |
| `-e END` | 结束行索引（不包含） |
| `-dt DT` | 步长，默认为1 |

### 绘图标签参数

| 参数 | 说明 |
|------|------|
| `-l LEGENDS [LEGENDS ...]` | 图例标签。不显示：`-l "" "" ""`。支持 LaTeX：`-l "$\Delta G_{energy}$"` |
| `-x XLABEL` | X 轴标签 |
| `-y YLABEL` | Y 轴标签 |
| `-z ZLABEL` | Z 轴标签（用于颜色、3D图等） |
| `-t TITLE` | 图片标题。不显示：`-t ""` |

### 数据范围参数

| 参数 | 说明 |
|------|------|
| `-xmin XMIN` / `-xmax XMAX` | X 轴范围 |
| `-ymin YMIN` / `-ymax YMAX` | Y 轴范围 |
| `-zmin ZMIN` / `-zmax ZMAX` | Z 轴范围（某些情况下可能是颜色值） |

### 数据变换参数

| 参数 | 说明 |
|------|------|
| `-xs XSHRINK` / `-ys YSHRINK` / `-zs ZSHRINK` | 数据缩放因子，默认1.0 |
| `-xp XPLUS` / `-yp YPLUS` / `-zp ZPLUS` | 数据偏移量，默认0.0 |

**警告**：变换后必须更新对应的轴标签，不可以随意修改数据，除非用户明确要求！

### 绘图控制参数

| 参数 | 说明 |
|------|------|
| `-ns` | 不显示图形（用于批量处理） |
| `--alpha ALPHA` | 图形元素透明度 |
| `-csv CSV` | 将数据导出到 CSV 文件 |
| `-eg {matplotlib,plotly,gnuplot,plotext}` | 绘图引擎，默认 matplotlib |
| `-cmap COLORMAP` | 颜色映射（matplotlib 和 plotly） |
| `--colorbar_location {None,left,top,bottom,right}` | 颜色条位置 |
| `--legend_location {inside,outside}` | 图例位置 |
| `--legend_ncol LEGEND_NCOL` | 图例列数，默认1 |

### 统计分析参数

| 参数 | 说明 |
|------|------|
| `-smv [{,CI,origin}]` | 显示滑动平均值。`CI` 显示置信区间, `origin`显示原始数据作为背景 |
| `-ws WINDOWSIZE` | 滑动平均窗口大小，默认50 |
| `-cf CONFIDENCE` | 置信区间可信度，默认0.95 |

### 插值参数

| 参数 | 说明 |
|------|------|
| `-ip INTERPOLATION` | 插值方法（bilinear, bicubic, nearest, linear, cubic, quintic），需要根据程序输出进行调整，当使用imshow的时候，插值方法是matplotlib的插值方法，当使用其它mode的时候，使用的是scipy支持的插值方法 |
| `-ipf INTERPOLATION_FOLD` | 插值倍数，默认10 |

### 模式参数

| 参数 | 说明 |
|------|------|
| `-m MODE` | 模式选择：`pcolormesh`, `3d`, `contour`, `pdf`, `cdf` 等 |

---

## XVG 命令

### xvg_show

**功能**：快速显示一个或多个 XVG 文件中的所有数据。

**说明**：
- 默认第0列为 X 值，第1列及之后为 Y 值
- 自动解析图例、X/Y 轴标签

**参数**：标准参数（见全局参数）

**示例**：
```bash
# 显示单个文件
dit xvg_show -f rmsd.xvg

# 显示多个文件
dit xvg_show -f rmsd.xvg gyrate.xvg

# 选择特定列并设置标签
dit xvg_show -f rmsd.xvg -c 1 -x "Time (ns)" -y "RMSD (nm)" -t "RMSD Analysis"
```

---

### xvg_compare

**功能**：比较多个 XVG 文件中的数据，支持灵活的列选择和滑动平均。

**说明**：
- 比 xvg_show 更灵活，推荐使用
- 每个输入文件可以选择不同的列
- 支持滑动平均和置信区间显示

**示例**：
```bash
# 比较两个文件的不同列
dit xvg_compare -f rmsd.xvg gyrate.xvg -c 1 1,2

# 设置图例和轴标签
dit xvg_compare -f rmsd.xvg gyrate.xvg -c 1 1,2 -l RMSD gyrate gyrate_X -x "Time(ps)" -y "(nm)"

# 显示滑动平均值
dit xvg_compare -f energy.xvg -c 1,3 -l "LJ(SR)" "Coulomb(SR)" -smv

# 使用 plotly 引擎
dit xvg_compare -f energy.xvg -c 1,3 -l "LJ(SR)" "Coulomb(SR)" -smv -eg plotly

# 导出数据到 CSV
dit xvg_compare -f energy.xvg -c 1,3 -ns -csv data.csv
```

---

### xvg_ave

**功能**：计算 XVG 文件中每一列数据的平均值、标准偏差和标准误差。

**参数**：
- `-f`：输入 XVG 文件
- `-b`：起始行索引（包含）
- `-e`：结束行索引（不包含）

**示例**：
```bash
# 计算平均值
dit xvg_ave -f rmsd.xvg -b 1000 -e 2001

# 输出示例：
# >>>>>>>>>                    rmsd.xvg                    <<<<<<<<<<<<<<
# ----------------------------------------------------------------------------
# |                  |     Average      |     Std.Dev      |     Std.Err      |
# ----------------------------------------------------------------------------
# |    Time (ps)     |   15000.000000   |   2891.081113    |    91.378334     |
# ----------------------------------------------------------------------------
# |    RMSD (nm)     |     0.388980     |     0.038187     |     0.001207     |
# ----------------------------------------------------------------------------
```

---

### xvg_show_distribution

**功能**：显示数据的分布情况，支持直方图、PDF 和 CDF。

**参数**：
- `-m`：显示模式
  - 默认：直方图
  - `pdf`：概率密度函数
  - `cdf`：累积密度函数

**示例**：
```bash
# 显示分布
dit xvg_show_distribution -f gyrate.xvg -c 1,2

# 显示 PDF
dit xvg_show_distribution -f gyrate.xvg -c 1,2 -m pdf -eg plotly

# 显示 CDF
dit xvg_show_distribution -f gyrate.xvg -c 1,2 -m cdf
```

---

### xvg_show_stack

**功能**：绘制堆积折线图，适用于二级结构含量变化等场景。

**示例**：
```bash
# 绘制二级结构含量堆积图
dit xvg_show_stack -f dssp_sc.xvg -c 2-7 -x "Time (ns)"
```

---

### xvg_show_scatter

**功能**：绘制散点图，支持两列或三列数据。

**说明**：
- 两列：X-Y 散点图
- 三列：X-Y 散点图，第三列用于颜色映射

**示例**：
```bash
# 两列散点图
dit xvg_show_scatter -f gyrate.xvg -c 1,2

# 三列散点图（用第三列着色）
dit xvg_show_scatter -f gyrate.xvg -c 1,2,0 -z "Time(ps)" -eg plotly
```

---

### xvg_box_compare

**功能**：以小提琴图和散点图的形式比较数据列。

**参数**：
- `-m withoutScatter`：不显示散点图

**示例**：
```bash
# 显示小提琴图和散点图
dit xvg_box_compare -f gyrate.xvg -c 1,2,3,4 -l Gyrate Gx Gy Gz -z "Time(ps)"

# 仅显示小提琴图
dit xvg_box_compare -f gyrate.xvg -c 1,2,3,4 -l Gyrate Gx Gy Gz -m withoutScatter

# 使用 plotly 引擎
dit xvg_box_compare -f gyrate.xvg -c 1,2,3,4 -l Gyrate Gx Gy Gz -eg plotly
```

---

### xvg_combine

**功能**：从多个 XVG 文件中读取数据并组合成一个新的 XVG 文件。

**示例**：
```bash
# 组合两个文件的数据
dit xvg_combine -f RMSD.xvg Gyrate.xvg -c 0,1 1 -l RMSD Gyrate -x "Time(ps)"

# 组合并输出到新文件
dit xvg_combine -f f1.xvg f2.xvg -c 1,2 2,3 -o res.xvg
```

---

### xvg_ave_bar

**功能**：计算多组数据的平均值和误差，并绘制柱状图。

**说明**：适用于比较多个平行模拟的结果。

**参数**：
- `-al`：X 轴标签
- `-csv`：导出数据到 CSV

**示例**：
```bash
# 比较三个配体体系的氢键数量（逗号分隔表示平行实验）
dit xvg_ave_bar -f bar_0_0.xvg,bar_0_1.xvg bar_1_0.xvg,bar_1_1.xvg \
  -c 1,2 -l MD_0 MD_1 -al Hbond Pair -csv hhh.csv -y Number
```

---

### xvg_rama

**功能**：将 Ramachandran 数据（phi 和 psi 二面角）绘制成拉式图。

**示例**：
```bash
# 绘制拉式图
dit xvg_rama -f rama.xvg

# 保存为图片
dit xvg_rama -f rama.xvg -ns -o rama.png
```

---

### xvg_energy_compute

**功能**：计算蛋白质和配体之间的能量。

---

## XPM 命令

### xpm_show

**功能**：可视化 XPM 矩阵文件。

**支持的绘图模式**（`-m` 参数）：
| 模式 | 说明 | 支持引擎 |
|------|------|----------|
| `imshow` | 快速图像显示（默认） | matplotlib |
| `pcolormesh` | 网格可视化 | matplotlib, plotly, gnuplot |
| `3d` | 3D 表面图 | matplotlib, plotly, gnuplot |
| `contour` | 等高线图 | matplotlib, plotly, gnuplot |

**特有参数**：
| 参数 | 说明 |
|------|------|
| `-xmin/-xmax/-ymin/-ymax` | 图像切割（像素索引） |
| `--x_numticks/--y_numticks/--z_numticks` | 刻度数量 |

**示例**：
```bash
# 基本显示
dit xpm_show -f DSSP.xpm

# 不显示图形，保存到文件
dit xpm_show -f DSSP.xpm -ns -o dssp.png

# 3D 模式
dit xpm_show -f FEL.xpm -m 3d -x PC1 -y PC2 -z Energy -t FEL --alpha 0.5

# 等高线模式
dit xpm_show -f FEL.xpm -m contour -cmap jet -zmin 0 -zmax 20

# 图像切割（显示部分区域）
dit xpm_show -f DSSP.xpm -xmin 1000 -xmax 2001 -ymin 50 -ymax 101

# 使用 plotly 引擎
dit xpm_show -f FEL.xpm -eg plotly -m 3d -cmap spectral

# 使用 gnuplot 引擎
dit xpm_show -f FEL.xpm -eg gnuplot -m 3d -ip cubic
```

---

### xpm2csv

**功能**：将 XPM 文件转换为 CSV 格式（x, y, v 三列）。

**示例**：
```bash
dit xpm2csv -f test.xpm -o test.csv
```

---

### xpm2dat

**功能**：将 XPM 文件转换为 M×N 的 DAT 格式。

**输出格式**：
- 第一行：X 轴标题、Y 轴标题、矩阵标题
- 第二行：X 轴数据
- 第三行：Y 轴数据（从下到上）
- 后续：M×N 数据矩阵

**示例**：
```bash
dit xpm2dat -f test.xpm -o test.dat
```

---

### xpm_diff

**功能**：计算两个相同尺寸 XPM 文件的差值。

**说明**：
- 仅适用于 Continuous 类型（如 DCCM、FEL）
- 不适用于 Discrete 类型（如 DSSP）

**示例**：
```bash
dit xpm_diff -f DCCM0.xpm DCCM1.xpm -o DCCM0-1.xpm
```

---

### xpm_merge

**功能**：将两个相同尺寸的 XPM 文件沿对角线一半一半拼接。

**示例**：
```bash
dit xpm_merge -f DCCM0.xpm DCCM1.xpm -o DCCM0-1.xpm
```

---

## NDX 命令

### ndx_add

**功能**：向 NDX 索引文件添加新的索引组。

**参数**：
- `-al`：组名（可多个）
- `-c`：原子索引（从1开始，GROMACS 约定）

**示例**：
```bash
# 添加单个组
dit ndx_add -f index.ndx -o test.ndx -al lig -c 1-10

# 添加多个组
dit ndx_add -al lig mol -c 1-10-3,11-21 21-42
```

---

### ndx_split

**功能**：将一个索引组均匀切分成多个组。

**参数**：
- `-al`：组名或组索引 + 切分数量

**示例**：
```bash
# 按组索引切分
dit ndx_split -f index.ndx -al 1 2

# 按组名切分
dit ndx_split -f index.ndx -al Protein 2

# 切分并输出到新文件
dit ndx_split -f index.ndx -al Protein 2 -o test.ndx
```

---

### ndx_show

**功能**：显示 NDX 文件中所有索引组的名称。

**示例**：
```bash
dit ndx_show -f test.ndx
```

---

### ndx_rm_dup

**功能**：删除 NDX 文件中所有重复的索引组（名称和索引都相同）。

**示例**：
```bash
dit ndx_rm_dup -f test.ndx -o res.ndx
```

---

## 其他命令

### mdp_gen

**功能**：生成 GROMACS MDP 文件模板。

**说明**：生成的模板不一定适合您的体系，请根据实际情况调整参数。

**示例**：
```bash
# 生成默认模板
dit mdp_gen

# 生成指定文件名的模板
dit mdp_gen -o nvt.mdp
```

---

### show_style

**功能**：显示或生成不同绘图引擎的格式控制文件。

**说明**：生成的样式文件放在工作目录会自动被 DIT 加载。

**示例**：
```bash
# 显示默认 matplotlib 样式
dit show_style

# 显示 plotly 样式
dit show_style -eg plotly

# 显示 gnuplot 样式
dit show_style -eg gnuplot

# 生成样式文件
dit show_style -eg plotly -o DIT_plotly.json
```

---

### find_center

**功能**：寻找 GRO 文件中原子组的几何中心。

**参数**：
- `-m AllAtoms`：在所有原子中寻找指定原子组的几何中心

**示例**：
```bash
# 计算所有原子的几何中心
dit find_center -f test.gro

# 使用索引文件
dit find_center -f test.gro index.ndx

# 在所有原子中寻找指定组的几何中心
dit find_center -f test.gro index.ndx -m AllAtoms
```

---

### dccm_ascii

**功能**：将 GROMACS `covar` 命令的 ASCII 格式协方差矩阵转换为动态互相关矩阵（DCCM）XPM 文件。

**示例**：
```bash
dit dccm_ascii -f covar.dat -o dccm.xpm
```

---

### dssp

**功能**：处理 GROMACS 2023 的 `dssp` 命令生成的 DAT 文件，转换为 DSSP XPM 和 sc.xvg 文件。

**说明**：将 GROMACS 2023 格式转换为旧版本格式。

**参数**：
- `-c`：残基索引（用于时间序列生成）
- `-b/-e/-dt`：时间序列参数

**示例**：
```bash
# 基本转换
dit dssp -f dssp.dat -o dssp.xpm

# 生成时间序列
dit dssp -f dssp.dat -c 1-42,1-42,1-42 -b 1000 -e 2001 -dt 10 -x "Time (ps)"
```

---

## 常用 Colormap 参考

| 名称 | 适用场景 |
|------|----------|
| `coolwarm` | 对称数据（DCCM） |
| `jet` / `jet_r` `Blues_r` | 自由能景观 |
| `viridis` / `plasma` | 连续数据 |
| `Blues` / `Reds` / `Greys` | 单色调 |
| `tab10` | 离散数据 |

输入错误的 colormap 名称会显示所有可用选项。
