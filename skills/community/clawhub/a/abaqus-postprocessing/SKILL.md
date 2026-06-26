---
name: abaqus-postprocessing
description: Abaqus后处理完整流程技能。覆盖结果可视化、输出数据类型、数据处理、图形显示、数据导出。
metadata:
  openclaw:
    emoji: 📊
  version: 1.1.0
  created: 2026-04-25
  updated: 2026-04-25
  domain: 有限元分析/结构工程
tags:
  - postprocessing
  - visualization
  - odb
---

# Abaqus后处理技能

> 官方文档: https://help.3ds.com → SIMULIA Established Products → Abaqus
> Abaqus/CAE后处理: 结果可视化模块 (Visualization Module)

## 技能描述
此技能涵盖了Abaqus中结果可视化和数据分析的完整流程。Abaqus/CAE提供全面的可视化选项，用于解释和传达任何Abaqus分析的结果。

## 核心组件

### 1. 结果可视化 (Results Visualization)
- **变形形状 (Deformed Shape)**：显示结构变形后的形状
  - 可叠加未变形轮廓进行对比
  - 支持变形缩放系数调整
- **等值线图 (Contour Plot)**：显示应力、应变、温度等场变量分布
  - Mises应力云图
  - 主应力分布
  - 等效塑性应变(PEEQ)
- **矢量图 (Vector Plot)**：显示位移、速度、力等矢量场
- **云纹图 (Fringe Plot)**：彩色显示场变量的数值分布
- **符号图 (Symbol Plot)**：显示反力、约束等符号

### 2. 输出数据类型 (Output Data Types)
- **场变量输出 (Field Output)**：
  - 空间分布的连续数据
  - 用于云图、等值线显示
  - 常用变量：
    | 变量 | 含义 | 用途 |
    |------|------|------|
    | S | 应力 | 查看应力分布（Mises、主应力） |
    | E | 应变 | 查看应变分布 |
    | U | 位移 | 查看变形情况 |
    | RF | 反力 | 查看支反力 |
    | CF | 接触力 | 查看接触力分布 |
    | PEEQ | 等效塑性应变 | 判断永久变形程度 |
    | LE | 对数应变 | 大变形分析 |
    | STH | 静水压力 | 流体/橡胶分析 |
- **历程输出 (History Output)**：
  - 特定位置随时间变化的数据
  - 用于XY曲线绘制
  - 能量输出（显式分析关键）：
    | 变量 | 含义 | 用途 |
    |------|------|------|
    | ALLKE | 总动能 | 观察速度衰减 |
    | ALLIE | 总内能 | 观察能量吸收 |
    | ALLAE | 伪应变能 | 沙漏控制指标 |
    | ETOTAL | 总能量 | 能量守恒验证 |
    | ALLFD | 摩擦耗散能 | 有摩擦接触时检查 |

### 3. 数据处理 (Data Processing)
- **结果提取**：从ODB文件中提取特定数据
- **数据过滤**：对输出数据进行筛选和处理
- **数学运算**：对原始结果进行数学处理得到衍生量
  - 创建场输出表达式 (Create Field Output → Expression)
  - 计算主应力、主应变等
- **XY数据操作**：
  - 从历程输出创建XY数据
  - 从场输出创建XY数据（沿路径）
  - XY数据运算（加减乘除）
  - 将XY数据保存为文本文件
- **报告生成**：创建分析结果报告
  - File → Report → Field/History/Free Body

### 4. 图形显示 (Graphics Display)
- **多窗口显示**：同时显示多个视图或结果
  - Viewport → Create 创建新视口
  - 不同视口显示不同结果
- **动画功能**：
  - 显示随时间变化的变形和响应
  - 支持多种动画模式：
    - Linear（线性播放）
    - Step（逐步播放）
    - Transient（瞬态播放）
  - 可导出为视频文件
- **截面显示 (Cutaway/Section)**：通过截面观察内部结果分布
- **路径显示 (Path)**：沿自定义路径显示变量分布
- **探针工具 (Probe Values)**：查询特定节点/单元的值

### 5. 数据导出 (Data Export)
- **图像导出**：将结果图形导出为图片文件
  ```python
  session.printToFile(fileName='result', format=PNG,
      canvasObjects=(viewport, ))
  ```
- **数据导出**：将数值结果导出为表格或其他格式
  - XY Data → Save As → .txt/.csv
  - Report → Field → .rpt
- **动画导出**：创建结果动画视频文件
  - Animation → Capture
- **ODB导出**：保存修改后的ODB文件

## 显式分析后处理要点

### 能量历史曲线检查
```python
# 在Abaqus/CAE中或通过Python脚本
from viewerModules import *
odb = session.openOdb(name='Job-1.odb')

# 创建能量曲线
xy_ke = session.XYDataFromHistory(name='ALLKE', odb=odb,
    outputVariableName='Kinetic Energy')
xy_ie = session.XYDataFromHistory(name='ALLIE', odb=odb,
    outputVariableName='Internal Energy')
xy_et = session.XYDataFromHistory(name='ETOTAL', odb=odb,
    outputVariableName='Total Energy')

# 创建XY图
session.XYPlot('Energy History')
session.curves['Energy History'].addData(xy_ke, xy_ie, xy_et)
```

### 判定标准
- ETOTAL 变化 < 5%：结果可信
- ETOTAL 变化 5~10%：可接受，需谨慎解读
- ETOTAL 变化 > 10%：结果不可信

### 接触穿透检查
在后处理中检查接触面是否有异常穿透。正常穿透量应 < 单元尺寸的 10%。

## 应用场景
- 结构变形分析结果查看
- 应力应变分布分析
- 模态振型显示
- 动力响应分析
- 热力分析结果可视化
- 跌落/冲击分析的能量验证

## 注意事项
- 结果的有效性依赖于分析的质量
- 需要选择合适的显示范围和颜色映射
- 动画播放可以帮助理解动态行为
- 导出结果时要注意单位和精度
- 大模型的ODB文件可能很大，注意磁盘空间
- 场输出频率影响ODB大小和后处理速度

## 与其它模块的关系
- 求解模块：后处理基于求解产生的结果文件(.odb)
- 载荷模块：可显示载荷和边界条件的施加情况
- 建模模块：可显示原始几何和变形后的几何对比
- 分析步模块：结果显示基于分析步定义的时间序列
