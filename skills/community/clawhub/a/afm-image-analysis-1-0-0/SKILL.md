# afm-image-analysis-1.0.0

> AFM图像分析工具 — 表面粗糙度、纳米颗粒统计、线轮廓、3D可视化、批量处理

## 快速使用

```bash
# 单文件
python ~/.openclaw/skills/afm-image-analysis-1.0.0/scripts/analyze_afm.py sample.afm -o ./output

# 批量目录
python ~/.openclaw/skills/afm-image-analysis-1.0.0/scripts/analyze_afm.py ./afm_data/ -o ./output -r

# 带线轮廓（px坐标）
python analyze_afm.py sample.npy --profile 100,50,400,250 -o ./out
```

## 输入格式

| 格式 | 说明 |
|------|------|
| `.npy/.npz` | NumPy 二进制数组（推荐） |
| `.txt/.csv/.asc/.dat` | 文本矩阵，空白分隔或CSV |
| `.jpg/.png/.tif` | 图像文件（灰度→高度映射） |

> ⚠️ 图像模式默认 1 gray level = 1 nm，用 `--scale` 调整。

## 功能模块

### 1. 表面粗糙度（自动平面校正）

```
Ra(nm)    — 算术平均粗糙度（最常用）
Rq(nm)    — 均方根粗糙度
Rpv(nm)   — 峰谷总值 (max−min)
Rsk       — 偏度（对称性）
Rku       — 峰度（分布锐度）
Ra_g(nm)  — 高斯滤波粗糙度
```

> 步骤：①一阶平面拟合去倾斜 ②计算粗糙度参数

### 2. 纳米颗粒/突起检测

- Otsu自动阈值分割
- OpenCV连通域分析
- 等效圆直径 (Ø_eq = 2√(area/π))
- 高度统计（mean/max/min）
- 批量CSV导出

### 3. 线轮廓截面

指定两个像素坐标，提取沿线的 높이变化曲线：

```bash
--profile x1,y1,x2,y2
```

### 4. 3D表面渲染

LightSource shading，颜色映射 terrain，垂直夸张 2×。

### 5. 批量处理

```bash
# 递归扫描
python analyze_afm.py ./afm_data/ -r -o ./afm_results/
```

## 输出文件

每个输入文件生成独立子目录（`{文件名}/`）：

| 文件 | 内容 |
|------|------|
| `afm_heatmap.png` | AFM高度热图 |
| `afm_3d.png` | 3D表面渲染图 |
| `roughness.png` | 粗糙度参数柱状图 |
| `roughness.csv` | 粗糙度数据表 |
| `particles_annotated.png` | 颗粒标注图 |
| `particle_hist.png` | 颗粒直径/高度分布直方图 |
| `particles.csv` | 颗粒详细数据 |
| `line_profile.png` | 线轮廓截面图 |
| `report.json` | 完整JSON报告 |

根目录额外输出：`summary.csv`（多文件汇总表）

## 常用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--threshold` | 颗粒检测阈值(%) | 20 |
| `--min-size` | 最小颗粒面积(px) | 10 |
| `--scale` | 灰度→nm比例 | auto/1.0 |
| `--no-3d` | 跳过3D渲染 | False |
| `-r` | 递归扫描子目录 | False |

## 典型分析场景

**催化剂薄膜粗糙度评估：**
```bash
python analyze_afm.py catalyst_film.npy -o ./results
# → 查看 Ra/Rq 判断表面平整度（Ra<5nm 很平整，Ra>30nm 较粗糙）
```

**纳米颗粒尺寸统计：**
```bash
python analyze_afm.py nano_particles.npy --threshold 25 --min-size 15 -o ./np_stats
```

**批量对比不同样品：**
```bash
python analyze_afm.py ./sample_series/ -r -o ./compare/
# → 对比 summary.csv 中 Ra/Rq 值
```

## 技术栈

- numpy — 数据处理
- opencv-python — 连通域/阈值分割
- scipy — 平面拟合/统计分析
- matplotlib — 全套绘图
- numpy/csv — 报告导出
