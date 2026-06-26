# Publication-Quality Visualization - 故障排查

## 常见错误及解决方案

### ERROR-001: 未检测到任何可视化工具

**症状:**
```
[ERROR] 未检测到任何可视化工具。请安装: PyMOL, VMD, 或 Python (matplotlib/seaborn)
```

**原因:**
- PyMOL、VMD、Python 可视化库均未安装

**解决方案:**

1. **安装 PyMOL (推荐用于分子结构):**
```bash
# Conda
conda install -c conda-forge pymol-open-source

# Ubuntu/Debian
sudo apt-get install pymol

# macOS
brew install pymol
```

2. **安装 Python 可视化库 (推荐用于数据图表):**
```bash
pip3 install matplotlib seaborn numpy scipy pandas
```

3. **安装 VMD (可选，用于高级渲染):**
```bash
# 从官网下载: https://www.ks.uiuc.edu/Research/vmd/
# 解压并添加到 PATH
export PATH="/path/to/vmd:$PATH"
```

---

### ERROR-002: PyMOL 执行失败

**症状:**
```
[ERROR] PyMOL 执行失败
```

**原因:**
- PyMOL 脚本语法错误
- 结构文件格式不支持
- PyMOL 版本不兼容

**解决方案:**

1. **检查 PyMOL 版本:**
```bash
pymol -c -Q -e "print(cmd.get_version())"
```

2. **手动测试 PyMOL 脚本:**
```bash
pymol -c publication-viz/pymol_script.pml
```

3. **转换结构文件格式:**
```bash
# GRO → PDB
gmx editconf -f structure.gro -o structure.pdb

# 清理 PDB (移除非标准残基)
grep "^ATOM" structure.pdb > structure_clean.pdb
```

4. **使用 Python API (如果命令行失败):**
```python
import pymol
pymol.cmd.load("structure.pdb")
pymol.cmd.show("cartoon")
pymol.cmd.png("output.png", dpi=300)
```

---

### ERROR-003: Python 绘图失败

**症状:**
```
[ERROR] Python 绘图失败
ERROR: 读取数据失败: ...
```

**原因:**
- 数据文件格式错误
- 缺少必需的 Python 库
- 数据维度不匹配

**解决方案:**

1. **检查数据文件格式:**
```bash
# XVG 文件应该是纯数值 (去除注释)
grep -v "^[@#]" data.xvg | head

# 检查列数
awk '{print NF}' data.xvg | sort -u
```

2. **手动清理 XVG 文件:**
```bash
grep -v "^[@#]" rmsd.xvg > rmsd_clean.dat
```

3. **检查 Python 库:**
```bash
python3 -c "import matplotlib, seaborn, numpy; print('OK')"
```

4. **测试简单绘图:**
```python
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('data.xvg', comments=['#', '@'])
plt.plot(data[:, 0], data[:, 1])
plt.savefig('test.png', dpi=300)
```

---

### ERROR-004: 轨迹可视化失败

**症状:**
```
ERROR: 投影数据不存在，请先运行 PCA 分析
```

**原因:**
- 未运行 PCA/聚类分析
- 投影文件命名不匹配

**解决方案:**

1. **先运行 PCA 分析:**
```bash
# 使用 trajectory-analysis skill
bash scripts/analysis/trajectory-analysis.sh \
  -s md.tpr -f md.xtc --mode pca

# 或手动运行
echo "C-alpha" | gmx covar -s md.tpr -f md.xtc -o eigenval.xvg -v eigenvec.trr
echo "C-alpha" | gmx anaeig -s md.tpr -f md.xtc -v eigenvec.trr \
  -2d projection_pca.xvg -first 1 -last 2
```

2. **检查投影文件:**
```bash
ls -lh projection_*.xvg
head projection_pca.xvg
```

3. **手动指定投影文件:**
```bash
# 修改脚本或创建符号链接
ln -s 2dproj.xvg projection_pca.xvg
```

---

### ERROR-005: 输出格式不支持

**症状:**
```
[ERROR] 未知输出格式: ...
```

**原因:**
- 指定的输出格式不被支持

**解决方案:**

1. **使用支持的格式:**
```bash
--format png   # 推荐，通用
--format svg   # 矢量图，可编辑
--format pdf   # 发表用，高质量
--format eps   # LaTeX 兼容
```

2. **格式转换 (如果需要):**
```bash
# PNG → PDF
convert -density 300 figure.png figure.pdf

# SVG → PDF
inkscape figure.svg --export-pdf=figure.pdf

# EPS → PDF
epstopdf figure.eps
```

---

### ERROR-006: DPI 设置无效

**症状:**
- 输出图像分辨率过低
- 文字模糊

**解决方案:**

1. **使用高 DPI (发表级):**
```bash
--dpi 300   # 标准发表质量
--dpi 600   # 高质量印刷
--dpi 150   # 预览用 (快速)
```

2. **检查实际 DPI:**
```bash
identify -verbose figure.png | grep Resolution
```

3. **矢量图优先 (无 DPI 限制):**
```bash
--format svg  # 或 pdf/eps
```

---

### ERROR-007: 内存不足

**症状:**
```
MemoryError: Unable to allocate array
```

**原因:**
- 轨迹文件过大
- 数据点过多

**解决方案:**

1. **减少轨迹帧数:**
```bash
# 跳帧处理
gmx trjconv -s md.tpr -f md.xtc -o md_skip10.xtc -skip 10
```

2. **降低分辨率 (临时):**
```bash
--dpi 150  # 预览用
```

3. **分段处理:**
```bash
# 只处理前 1000 帧
gmx trjconv -s md.tpr -f md.xtc -o md_first1000.xtc -e 1000
```

---

### ERROR-008: 期刊风格配置错误

**症状:**
- 图表风格不符合期刊要求
- 字体/线宽不正确

**解决方案:**

1. **使用预设期刊风格:**
```bash
--journal-style nature   # Nature 系列
--journal-style science  # Science
--journal-style cell     # Cell 系列
```

2. **手动调整 (修改脚本):**
```python
# Nature 风格
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.linewidth': 0.5,
    'figure.figsize': (3.5, 2.5)  # 单栏宽度
})

# Science 风格
plt.rcParams.update({
    'font.family': 'Helvetica',
    'font.size': 9,
    'axes.linewidth': 0.8,
    'figure.figsize': (3.3, 2.5)
})
```

3. **检查期刊要求:**
- Nature: Arial, 8pt, 单栏 89mm (3.5"), 双栏 183mm (7.2")
- Science: Helvetica, 9pt, 单栏 5.5cm, 双栏 12cm
- Cell: Arial, 7pt, 单栏 85mm, 双栏 180mm

---

### ERROR-009: 颜色方案不合适

**症状:**
- 颜色对比度不足
- 色盲不友好

**解决方案:**

1. **使用色盲友好配色:**
```python
# Seaborn 色盲友好调色板
sns.set_palette("colorblind")

# 或手动指定
colors = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC']
```

2. **PyMOL 配色方案:**
```pymol
color spectrum  # 彩虹色 (默认)
color chainbow  # 按链着色
color hydrophobicity  # 疏水性
color ss  # 二级结构
```

3. **在线工具检查:**
- ColorBrewer: https://colorbrewer2.org/
- Coblis (色盲模拟): https://www.color-blindness.com/coblis-color-blindness-simulator/

---

### ERROR-010: 多面板布局失败

**症状:**
- 子图重叠
- 布局不对齐

**解决方案:**

1. **使用 GridSpec:**
```python
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(7, 5))
gs = gridspec.GridSpec(2, 2, figure=fig)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])  # 跨列

plt.tight_layout()
```

2. **调整间距:**
```python
plt.subplots_adjust(hspace=0.3, wspace=0.3)
```

3. **使用 constrained_layout:**
```python
fig, axes = plt.subplots(2, 2, constrained_layout=True)
```

---

## 最佳实践

### 1. 分子结构可视化

**PyMOL 高质量渲染:**
```pymol
# 光线追踪
set ray_trace_mode, 1
set ray_shadows, 1
set antialias, 2
set ambient, 0.4

# 输出
ray 3000, 3000
png figure.png, dpi=300
```

**VMD 渲染:**
```tcl
# Tachyon 渲染器
render Tachyon figure.dat
tachyon figure.dat -o figure.tga -res 3000 3000
convert figure.tga figure.png
```

### 2. 数据图表

**时间序列 (RMSD/RMSF):**
```python
fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.plot(time, rmsd, linewidth=1.0, color='#0173B2')
ax.fill_between(time, rmsd-std, rmsd+std, alpha=0.3)
ax.set_xlabel('Time (ns)')
ax.set_ylabel('RMSD (nm)')
plt.tight_layout()
plt.savefig('rmsd.pdf', dpi=300, bbox_inches='tight')
```

**热图 (接触图):**
```python
sns.heatmap(contact_matrix, cmap='RdYlBu_r', 
            vmin=0, vmax=1, cbar_kws={'label': 'Contact Frequency'})
```

### 3. 轨迹可视化

**PCA 2D 投影:**
```python
scatter = ax.scatter(pc1, pc2, c=time, cmap='viridis', s=1, alpha=0.6)
ax.set_xlabel('PC1 (nm)')
ax.set_ylabel('PC2 (nm)')
plt.colorbar(scatter, label='Time (ns)')
```

**自由能景观:**
```python
from scipy.ndimage import gaussian_filter

# 计算自由能
hist, xedges, yedges = np.histogram2d(pc1, pc2, bins=50)
hist = gaussian_filter(hist, sigma=1.0)
free_energy = -0.008314 * 300 * np.log(hist + 1e-10)

# 绘制等高线
contour = ax.contourf(xedges[:-1], yedges[:-1], free_energy.T, 
                      levels=20, cmap='viridis')
plt.colorbar(contour, label='Free Energy (kJ/mol)')
```

---

## 工具对比

| 工具 | 优势 | 劣势 | 推荐场景 |
|------|------|------|----------|
| **PyMOL** | 易用、高质量渲染、脚本化 | 商业版收费 | 蛋白质结构、配体结合 |
| **VMD** | 免费、轨迹动画、插件丰富 | 学习曲线陡峭 | 轨迹可视化、密度图 |
| **Matplotlib** | 灵活、发表级图表、Python 生态 | 不支持 3D 分子 | 数据图表、统计分析 |
| **Seaborn** | 统计图表、美观 | 基于 Matplotlib | 分布图、热图 |

---

## 参考资源

- PyMOL Wiki: https://pymolwiki.org/
- VMD User Guide: https://www.ks.uiuc.edu/Research/vmd/current/ug/
- Matplotlib Gallery: https://matplotlib.org/stable/gallery/
- Seaborn Tutorial: https://seaborn.pydata.org/tutorial.html
- Nature Figure Guidelines: https://www.nature.com/nature/for-authors/final-submission
- Science Figure Guidelines: https://www.science.org/content/page/instructions-preparing-initial-manuscript
