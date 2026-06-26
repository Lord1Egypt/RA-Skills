# DuIvyTools 使用示例

本文件包含真实使用场景的完整示例。关于核心概念和命令参数，请参考主 SKILL.md 文件和 commands-reference.md。

## 目录

- [分子动力学结果分析](#分子动力学结果分析)
- [能量分析](#能量分析)
- [氢键分析](#氢键分析)
- [二级结构分析](#二级结构分析)
- [RMSD/RMSF 分析](#rmsdrmsf-分析)
- [动态互相关矩阵 (DCCM)](#动态互相关矩阵-dccm)
- [自由能景观 (FEL)](#自由能景观-fel)
- [Ramachandran 图](#ramachandran-图)
- [蛋白质几何性质](#蛋白质几何性质)
- [批量处理和脚本生成](#批量处理和脚本生成)
- [高级技巧](#高级技巧)
- [常见问题](#常见问题)

---

## 分子动力学结果分析

### 场景1：比较不同模拟的 RMSD

**问题**：你有三个不同的模拟体系，每个体系进行了3次平行实验，需要比较它们的 RMSD 变化。

```bash
# 显示所有 RMSD 文件
dit xvg_compare -f md1_rep1_rmsd.xvg md1_rep2_rmsd.xvg md1_rep3_rmsd.xvg \
  md2_rep1_rmsd.xvg md2_rep2_rmsd.xvg md2_rep3_rmsd.xvg \
  md3_rep1_rmsd.xvg md3_rep2_rmsd.xvg md3_rep3_rmsd.xvg \
  -c 1 1 1 1 1 1 1 1 1 \
  -l "MD1-1" "MD1-2" "MD1-3" "MD2-1" "MD2-2" "MD2-3" "MD3-1" "MD3-2" "MD3-3" \
  -x "Time (ps)" -y "RMSD (nm)" -t "RMSD Comparison" -smv

# 保存为图片
dit xvg_compare -f md1_rep1_rmsd.xvg md2_rep1_rmsd.xvg md3_rep1_rmsd.xvg \
  -c 1 1 1 \
  -l "MD1" "MD2" "MD3" \
  -x "Time (ps)" -y "RMSD (nm)" \
  -ns -o rmsd_comparison.png
```

---

### 场景2：分析蛋白质回转半径（Gyrate）

**问题**：分析蛋白质在不同方向上的回转半径变化（Rg, RgX, RgY, RgZ）。

```bash
# 显示所有回转半径分量
dit xvg_compare -f gyrate.xvg -c 1,2,3,4 \
  -l Rg RgX RgY RgZ \
  -x "Time (ps)" -y "Rg (nm)" -t "Radius of Gyration"

# 使用小提琴图比较分布
dit xvg_box_compare -f gyrate.xvg -c 1,2,3,4 \
  -l Rg RgX RgY RgZ \
  -z "Time(ps)" \
  -t "Gyrate Distribution"

# 仅显示小提琴图
dit xvg_box_compare -f gyrate.xvg -c 1,2,3,4 \
  -l Rg RgX RgY RgZ \
  -z "Time(ps)" \
  -m withoutScatter
```

---

### 场景3：计算平衡时期的平均值

**问题**：模拟运行了 100 ns，前 20 ns 是平衡时期，需要计算后 80 ns 的平均值和标准误差。

```bash
# 假设 xvg 文件有 10000 行，前 2000 行是平衡时期
# 从第 2000 行开始计算到末尾
dit xvg_ave -f rmsd.xvg -b 2000

# 计算指定范围的平均值（2000-4000 行）
dit xvg_ave -f rmsd.xvg -b 2000 -e 4001
```

---

## 能量分析

### 场景4：分析蛋白质-配体相互作用能

**问题**：分析蛋白质和配体之间的 Lennard-Jones 和库仑相互作用能。

```bash
# 显示能量变化（带滑动平均）
dit xvg_compare -f energy.xvg -c 1,3 \
  -l "LJ(SR)" "Coulomb(SR)" \
  -x "Time (ps)" -y "Energy (kJ/mol)" \
  -t "Protein-Ligand Interaction Energy" \
  -smv -ws 100

# 使用 plotly 交互式图表
dit xvg_compare -f energy.xvg -c 1,3 \
  -l "LJ(SR)" "Coulomb(SR)" \
  -x "Time (ps)" -y "Energy (kJ/mol)" \
  -eg plotly -smv

# 导出数据到 CSV
dit xvg_compare -f energy.xvg -c 1,3 \
  -l "LJ(SR)" "Coulomb(SR)" \
  -ns -csv energy_data.csv
```

---

### 场景5：比较不同配体的结合能

**问题**：你有三个不同的配体，每个配体进行了3次平行实验，需要比较它们的平均结合能。

```bash
# 计算平均值并绘制柱状图
dit xvg_ave_bar \
  -f lig1_rep1_energy.xvg,lig1_rep2_energy.xvg,lig1_rep3_energy.xvg \
     lig2_rep1_energy.xvg,lig2_rep2_energy.xvg,lig2_rep3_energy.xvg \
     lig3_rep1_energy.xvg,lig3_rep2_energy.xvg,lig3_rep3_energy.xvg \
  -c 1 1 1 \
  -l Ligand1 Ligand2 Ligand3 \
  -al "Ligand" "Binding Energy" \
  -y "Energy (kJ/mol)" \
  -t "Binding Energy Comparison" \
  -csv binding_energy.csv
```

---

## 氢键分析

### 场景6：分析蛋白质-配体氢键数量

**问题**：分析蛋白质和配体之间的氢键数量变化，计算稳定时期的平均值。

```bash
# 显示氢键数量变化
dit xvg_show -f hbonds.xvg \
  -x "Time (ps)" -y "Number of H-bonds" \
  -t "Protein-Ligand Hydrogen Bonds"

# 计算稳定时期的平均值
dit xvg_ave -f hbonds.xvg -b 3000

# 显示分布
dit xvg_show_distribution -f hbonds.xvg -c 1 \
  -x "Number of H-bonds" -t "H-bond Distribution"
```

---

### 场景7：比较不同条件下的氢键

**问题**：比较野生型和突变体与配体的氢键数量。

```bash
# 比较氢键数量
dit xvg_compare -f wt_hbonds.xvg mutant_hbonds.xvg \
  -c 1 1 \
  -l "Wild-Type" "Mutant" \
  -x "Time (ps)" -y "Number of H-bonds" \
  -t "Hydrogen Bond Comparison"

# 使用小提琴图比较分布
dit xvg_box_compare -f wt_hbonds.xvg mutant_hbonds.xvg \
  -c 1 1 \
  -l "Wild-Type" "Mutant" \
  -z "Time(ps)" \
  -t "H-bond Distribution"
```

---

## 二级结构分析

### 场景8：可视化蛋白质二级结构随时间的变化

**问题**：使用 DSSP 分析蛋白质二级结构随时间的变化。

```bash
# 如果使用 GROMACS 2023+，需要先转换 DSSP 输出
dit dssp -f dssp.dat -o dssp.xpm

# 显示二级结构矩阵
dit xpm_show -f dssp.xpm \
  -x "Residue Index" -y "Time (ps)" \
  -t "Secondary Structure"

# 切割显示特定区域（残基 50-150，时间 1000-2000 ps）
dit xpm_show -f dssp.xpm \
  -xmin 50 -xmax 151 -ymin 1000 -ymax 2001 \
  -x "Residue Index" -y "Time (ps)" \
  -t "Secondary Structure (Residues 50-150)"

# 使用 plotly 交互式查看
dit xpm_show -f dssp.xpm -eg plotly \
  -x "Residue Index" -y "Time (ps)"
```

---

### 场景9：分析二级结构含量变化

**问题**：分析不同二级结构（α-helix, β-sheet, coil 等）的含量随时间的变化。

```bash
# 显示二级结构含量堆积图
dit xvg_show_stack -f dssp_sc.xvg -c 2-7 \
  -x "Time (ps)" -y "Amino Acids Count" \
  -t "Secondary Structure Content"
```

---

### 场景10：比较不同状态的动态互相关矩阵（DCCM）

**问题**：比较蛋白质在结合配体前后原子运动相关性的变化。

**注意**：DCCM 是 Continuous 类型，可以计算差值。DSSP 是 Discrete 类型，不能计算差值。

**方法1：计算差值矩阵**
```bash
# 计算 DCCM 差值（Holo - Apo）
dit xpm_diff -f apo_dccm.xpm holo_dccm.xpm -o dccm_diff.xpm

# 显示差值矩阵
dit xpm_show -f dccm_diff.xpm \
  -x "Residue Index" -y "Residue Index" \
  -t "DCCM Difference (Holo - Apo)" \
  -cmap coolwarm -zmin -2 -zmax 2

# 保存差值矩阵图片
dit xpm_show -f dccm_diff.xpm -ns -o dccm_diff.png
```

**方法2：合并显示两个矩阵**
```bash
# 合并显示（左上 Apo，右下 Holo）
dit xpm_merge -f apo_dccm.xpm holo_dccm.xpm -o dccm_merged.xpm
dit xpm_show -f dccm_merged.xpm \
  -x "Residue Index" -y "Residue Index" \
  -t "DCCM (Top-Left: Apo, Bottom-Right: Holo)"
```

**结果解读**（针对差值矩阵）：
- 正值（红色）：配体结合增强了这两个残基之间的正相关运动
- 负值（蓝色）：配体结合改变了运动方向，使原本正相关变为负相关
- 接近0：配体结合对这对残基的相关性影响较小

---

## RMSD/RMSF 分析

### 场景11：分析蛋白质骨架和重原子的 RMSD

**问题**：同时分析蛋白质骨架（backbone）和重原子（heavy atoms）的 RMSD。

```bash
# 同时显示两个 RMSD
dit xvg_compare -f rmsd_backbone.xvg rmsd_heavy.xvg \
  -c 1 1 \
  -l "Backbone" "Heavy Atoms" \
  -x "Time (ps)" -y "RMSD (nm)" \
  -t "RMSD Comparison"

# 使用滑动平均和置信区间
dit xvg_compare -f rmsd_backbone.xvg rmsd_heavy.xvg \
  -c 1 1 \
  -l "Backbone" "Heavy Atoms" \
  -x "Time (ps)" -y "RMSD (nm)" \
  -smv CI -ws 100 -cf 0.95
```

---

### 场景12：分析残基的 RMSF

**问题**：分析每个残基的均方根涨落（RMSF），识别柔性区域。

```bash
# 显示 RMSF
dit xvg_show -f rmsf.xvg \
  -x "Residue Index" -y "RMSF (nm)" \
  -t "Root Mean Square Fluctuation"

# 比较不同状态的 RMSF
dit xvg_compare -f apo_rmsf.xvg holo_rmsf.xvg \
  -c 1 1 \
  -l "Apo" "Holo" \
  -x "Residue Index" -y "RMSF (nm)" \
  -t "RMSF Comparison"
```

---

## 动态互相关矩阵 (DCCM)

### 场景13：生成和分析 DCCM

**问题**：分析蛋白质残基之间的动态相关性。

```bash
# 从协方差矩阵生成 DCCM
dit dccm_ascii -f covar.dat -o dccm.xpm

# 显示 DCCM
dit xpm_show -f dccm.xpm \
  -x "Residue Index" -y "Residue Index" \
  -z "Correlation" \
  -t "Dynamic Cross-Correlation Matrix" \
  -cmap coolwarm -zmin -1 -zmax 1

# 使用等高线显示
dit xpm_show -f dccm.xpm \
  -m contour -cmap coolwarm \
  -zmin -1 -zmax 1 \
  -x "Residue Index" -y "Residue Index"

# 保存为图片
dit xpm_show -f dccm.xpm -ns -o dccm.png
```

---

## 自由能景观 (FEL)

### 场景14：2D 自由能景观

**问题**：可视化二维自由能景观。

```bash
# 显示自由能景观
dit xpm_show -f fel.xpm \
  -x "PC1" -y "PC2" -z "Energy (kJ/mol)" \
  -t "Free Energy Landscape" \
  -cmap jet_r

# 使用 3D 模式
dit xpm_show -f fel.xpm \
  -m 3d \
  -x "PC1" -y "PC2" -z "Energy (kJ/mol)" \
  -t "Free Energy Landscape" \
  -cmap jet_r --alpha 0.8

# 使用等高线
dit xpm_show -f fel.xpm \
  -m contour -cmap jet_r \
  -x "PC1" -y "PC2" -z "Energy (kJ/mol)" \
  --colorbar_location bottom

# 插值平滑
dit xpm_show -f fel.xpm \
  -m pcolormesh -ip cubic -ipf 3 \
  -cmap jet_r
```

---

### 场景15：3D 自由能景观

**问题**：使用三个反应坐标构建三维自由能景观。

```bash
# 使用 3D 模式显示
dit xpm_show -f fel_3d.xpm \
  -m 3d \
  -x "PC1" -y "PC2" -z "Energy (kJ/mol)" \
  -t "3D Free Energy Landscape" \
  -cmap plasma --alpha 0.7

# 设置刻度数量
dit xpm_show -f fel.xpm \
  -m 3d \
  --x_numticks 5 --y_numticks 5 --z_numticks 5 \
  -x "PC1" -y "PC2" -z "Energy (kJ/mol)"
```

---

## Ramachandran 图

### 场景16：分析蛋白质主链二面角

**问题**：分析蛋白质的 phi 和 psi 二面角分布，识别二级结构区域。

```bash
# 绘制 Ramachandran 图
dit xvg_rama -f rama.xvg

# 保存为图片
dit xvg_rama -f rama.xvg -ns -o rama.png

# 比较不同残基类型
dit xvg_rama -f rama_gly.xvg
dit xvg_rama -f rama_ala.xvg
```

---

## 蛋白质几何性质

### 场景17：计算几何中心

**问题**：计算配体或残基的几何中心。

```bash
# 计算配体的几何中心
dit find_center -f complex.gro ligand.ndx

# 在所有原子中寻找配体的几何中心
dit find_center -f complex.gro ligand.ndx -m AllAtoms

# 计算蛋白质的几何中心
dit find_center -f protein.gro
```

---

### 场景18：分析残基间距离

**问题**：分析两个残基之间的距离随时间的变化。

```bash
# 显示距离变化
dit xvg_show -f distance.xvg \
  -x "Time (ps)" -y "Distance (nm)" \
  -t "Residue Distance"

# 计算平均距离
dit xvg_ave -f distance.xvg -b 2000

# 显示距离分布
dit xvg_show_distribution -f distance.xvg -c 1 \
  -x "Distance (nm)" -t "Distance Distribution"
```

---

## 批量处理和脚本生成

### 场景19：批量生成所有分析的图片

**Windows PowerShell 脚本**：
```powershell
# 定义文件列表
$files = @("md1_rmsd.xvg", "md2_rmsd.xvg", "md3_rmsd.xvg")

# 批量生成 RMSD 图片
foreach ($file in $files) {
    $output = $file -replace ".xvg", ".png"
    dit xvg_show -f $file -x "Time (ps)" -y "RMSD (nm)" -ns -o $output
}

# 批量生成能量图片
$energy_files = @("md1_energy.xvg", "md2_energy.xvg", "md3_energy.xvg")
foreach ($file in $energy_files) {
    $output = $file -replace ".xvg", ".png"
    dit xvg_compare -f $file -c 1,3 -l "LJ" "Coulomb" -ns -o $output
}
```

**Bash 脚本**：
```bash
#!/bin/bash

# 批量生成 RMSD 图片
for file in md*_rmsd.xvg; do
    output="${file%.xvg}.png"
    dit xvg_show -f "$file" -x "Time (ps)" -y "RMSD (nm)" -ns -o "$output"
done

# 批量生成能量图片
for file in md*_energy.xvg; do
    output="${file%.xvg}.png"
    dit xvg_compare -f "$file" -c 1,3 -l "LJ" "Coulomb" -ns -o "$output"
done
```

---

### 场景20：使用 gnuplot 生成高质量图片

**问题**：使用 gnuplot 引擎生成高质量、可定制的图片。

```bash
# 生成 gnuplot 脚本（不显示图片）
dit xvg_show -f rmsd.xvg -eg gnuplot -ns -o rmsd.png

# 这会生成一个 gnuplot 脚本文件
# 可以手动编辑脚本进行进一步定制

# 使用 gnuplot 生成 3D 图
dit xpm_show -f fel.xpm -m 3d -eg gnuplot -ns -o fel_3d.png
```

---

### 场景21：自定义绘图样式

**问题**：自定义 matplotlib 绘图样式以满足特定要求。

**创建样式文件 `dit_mplstyle.mplstyle`**：
```python
## 自定义 matplotlib 样式
axes.labelsize:     14
axes.linewidth:     1.5
xtick.labelsize:    12
ytick.labelsize:    12
lines.linewidth:    2.5
legend.fontsize:    12
font.family:        Arial
font.size:          12
image.cmap:         viridis
figure.dpi:         100
savefig.dpi:        600
```

**使用自定义样式**：
```bash
# 将样式文件放在工作目录，DIT 会自动加载
dit xvg_show -f rmsd.xvg
```

---

## 高级技巧

### 技巧1：组合多种分析

```bash
# 组合 RMSD、Rg 和能量
dit xvg_compare -f rmsd.xvg gyrate.xvg energy.xvg \
  -c 1 1 1 \
  -l RMSD Rg Energy \
  -x "Time (ps)" \
  -t "Multiple Properties"

# 使用散点图显示相关性
dit xvg_show_scatter -f rmsd.xvg -c 0,1 \
  -x "Time (ps)" -y "RMSD (nm)" -t "RMSD vs Time"
```

---

### 技巧2：导出数据用于其他软件

```bash
# 导出 XVG 数据
dit xvg_compare -f rmsd.xvg -c 1 -ns -csv rmsd_data.csv

# 导出 XPM 数据
dit xpm2csv -f fel.xpm -o fel_data.csv

# 导出 XPM 为矩阵格式
dit xpm2dat -f fel.xpm -o fel_data.dat
```

---

### 技巧3：处理大型数据集

```bash
# 只读取部分行（1000-2000 行）
dit xvg_show -f large_rmsd.xvg -b 1000 -e 2001

# 只显示 XPM 的部分区域
dit xpm_show -f large_dssp.xpm -xmin 0 -xmax 100 -ymin 0 -ymax 1000

# 使用步长减少数据点
dit xvg_show -f large_rmsd.xvg -dt 10
```

---

### 技巧4：使用不同的 colormap 突出显示特征

```bash
# 显示对称数据（如 DCCM）
dit xpm_show -f dccm.xpm -cmap coolwarm -zmin -1 -zmax 1

# 显示自由能（高能量红色，低能量蓝色）
dit xpm_show -f fel.xpm -cmap jet_r

# 显示离散数据（如 DSSP）
dit xpm_show -f dssp.xpm -cmap tab10

# 使用渐变 colormap
dit xpm_show -f fel.xpm -cmap viridis
```

---

### 技巧5：生成出版级图片

```bash
# 使用 matplotlib 引擎，调整分辨率
# 编辑 dit_mplstyle.mplstyle，设置 savefig.dpi: 600
# 然后
dit xvg_show -f rmsd.xvg -ns -o rmsd_publication.png

# 使用 gnuplot 生成矢量图
dit xvg_show -f rmsd.xvg -eg gnuplot -ns -o rmsd.eps

# 使用 plotly 生成交互式网页
dit xvg_show -f rmsd.xvg -eg plotly -ns -o rmsd.html
```

---

## 常见问题

### Q1: 如何处理中文路径或文件名？

DuIvyTools 支持中文路径和文件名，但建议使用英文路径以避免编码问题。

```bash
dit xvg_show -f "路径/中文文件名.xvg"
```

---

### Q2: 如何调整图例位置？

使用 `--legend_location` 参数：

```bash
# 图例在图外
dit xvg_show -f rmsd.xvg --legend_location outside

# 图例在图内（默认）
dit xvg_show -f rmsd.xvg --legend_location inside
```

---

### Q3: 如何处理时间单位？

**默认保持原始单位（通常是 ps）**，仅在用户明确要求时转换：

```bash
# 保持原始单位（推荐）
dit xvg_show -f rmsd.xvg -x "Time (ps)"

# 用户明确要求转换为 ns 时
dit xvg_show -f rmsd.xvg -xs 0.001 -x "Time (ns)"
```

**警告**：单位转换时必须同时更新轴标签。

---

### Q4: 如何处理能量单位？

**默认保持原始单位（通常是 kJ/mol）**，仅在用户明确要求时转换：

```bash
# 保持原始单位（推荐）
dit xvg_show -f energy.xvg -c 1 -y "Energy (kJ/mol)"

# 用户明确要求转换为 kcal/mol 时（乘以 0.239）
dit xvg_show -f energy.xvg -c 1 -ys 0.239 -y "Energy (kcal/mol)"
```

---

### Q5: xpm_diff 可以用于 DSSP 吗？

**不可以**。DSSP 是 Discrete 类型（离散），每个像素代表一个状态，不能计算差值。xpm_diff 仅适用于 Continuous 类型（如 DCCM、FEL）。

对于 DSSP 比较，建议使用：
- `xpm_merge` 合并显示两个矩阵
- 分析二级结构含量变化（xvg_show_stack）