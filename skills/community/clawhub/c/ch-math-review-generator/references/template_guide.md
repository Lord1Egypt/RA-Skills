# 初中数学章节复习资料 HTML 生成器

## 概述

本模板用于生成初中数学章节复习指南（HTML格式），包含：
- 完整的知识点总结（带判定定理、性质、口诀）
- SVG 精准绘制的几何图形或函数图象
- 5道选择题 + 5道填空题 + 3道大题（均附详解）
- 点击展开/收起的交互式设计

## HTML 文档结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>第X章 XXX 复习指南</title>
  <style>
    /* 核心样式 - 紧凑打印友好 */
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:"Microsoft YaHei",sans-serif; font-size:14px; line-height:1.8; color:#333; background:#f5f5f5; padding:20px; }
    .container { max-width:900px; margin:0 auto; background:#fff; padding:24px 32px; border-radius:12px; box-shadow:0 2px 12px rgba(0,0,0,.08); }
    h1 { text-align:center; color:#1565c0; font-size:1.6rem; margin-bottom:20px; padding-bottom:12px; border-bottom:2px solid #1565c0; }
    h2 { color:#2e7d32; font-size:1.15rem; margin:20px 0 10px; padding-left:10px; border-left:4px solid #2e7d32; }
    h3 { color:#1565c0; font-size:1rem; margin:12px 0 8px; }
    .card { background:#fafafa; border:1px solid #e0e0e0; border-radius:8px; padding:16px 20px; margin-bottom:16px; }
    .section-title { font-size:1.1rem; font-weight:bold; margin:24px 0 12px; padding:8px 12px; border-radius:6px; color:#fff; }
    .section-title.blue { background:linear-gradient(90deg,#1565c0,#1976d2); }
    .section-title.green { background:linear-gradient(90deg,#2e7d32,#388e3c); }
    .section-title.purple { background:linear-gradient(90deg,#6a1b9a,#7b1fa2); }
    .section-title.orange { background:linear-gradient(90deg,#e65100,#ef6c00); }
    .section-title.red { background:linear-gradient(90deg,#c62828,#d32f2f); }
    .icon { margin-right:6px; }
    ul { padding-left:20px; }
    li { margin:6px 0; }
    .prop-list { list-style:none; padding:0; }
    .prop-list li { display:flex; align-items:flex-start; gap:10px; padding:10px 0; border-bottom:1px dashed #e0e0e0; }
    .prop-list li:last-child { border-bottom:none; }
    .prop-no { display:inline-block; width:24px; height:24px; border-radius:50%; color:#fff; text-align:center; line-height:24px; font-size:.8rem; font-weight:bold; flex-shrink:0; }
    .bg-blue { background:#1565c0; }
    .bg-green { background:#2e7d32; }
    .bg-orange { background:#e65100; }
    .bg-purple { background:#6a1b9a; }
    .bg-red { background:#c62828; }
    .formula { background:#e3f2fd; color:#1565c0; padding:2px 8px; border-radius:4px; font-family:"Courier New",monospace; font-weight:bold; }
    /* 表格 */
    table { width:100%; border-collapse:collapse; margin:12px 0; font-size:.9rem; }
    th { background:#1565c0; color:#fff; padding:8px 12px; text-align:center; }
    td { padding:8px 12px; text-align:center; border:1px solid #ddd; }
    tr:nth-child(even) { background:#f5f5f5; }
    /* 图形网格 */
    .graphs-row { display:flex; flex-wrap:wrap; gap:16px; justify-content:center; margin:16px 0; }
    .graph-box { width:180px; text-align:center; background:#fff; border:1px solid #ddd; border-radius:8px; padding:8px; }
    .graph-box h3 { font-size:.9rem; margin:4px 0 2px; }
    .graph-box p { font-size:.8rem; color:#666; }
    /* 题目卡片 */
    .q-card { background:#fff; border-radius:8px; margin-bottom:12px; box-shadow:0 1px 4px rgba(0,0,0,.08); overflow:hidden; }
    .q-header { padding:12px 16px; font-size:.95rem; display:flex; align-items:flex-start; gap:10px; }
    .q-num { display:inline-block; width:26px; height:26px; border-radius:50%; color:#fff; text-align:center; line-height:26px; font-size:.85rem; font-weight:bold; flex-shrink:0; }
    .q-body { padding:12px 16px 16px; }
    .answer-btn { display:inline-block; padding:6px 18px; background:#1565c0; color:#fff; border-radius:20px; font-size:.85rem; cursor:pointer; transition:background .2s; }
    .answer-btn:hover { background:#0d47a1; }
    .orange-btn { background:#e65100; }
    .orange-btn:hover { background:#bf360c; }
    .green-btn { background:#2e7d32; }
    .green-btn:hover { background:#1b5e20; }
    .answer-box { display:none; margin-top:12px; padding:14px; background:#f5f5f5; border-radius:8px; border-left:4px solid #1565c0; font-size:.9rem; line-height:2; }
    .ans-label { color:#2e7d32; font-weight:bold; margin-bottom:8px; }
    .note { background:#fff3e0; border:1px solid #ffe0b2; border-radius:6px; padding:12px 16px; margin:12px 0; font-size:.9rem; }
    .warning { background:#ffebee; border:1px solid #ffcdd2; border-radius:6px; padding:12px 16px; margin:12px 0; font-size:.9rem; }
    /* 打印样式 */
    @media print { body{background:#fff;padding:0;} .container{max-width:100%;box-shadow:none;} .answer-box{display:block!important;} .answer-btn{display:none;} }
  </style>
</head>
<body>
<div class="container">
  <!-- 内容将根据具体章节生成 -->
</div>
<script>
function toggleAnswer(id){var el=document.getElementById(id);el.style.display=el.style.display==='block'?'none':'block';}
</script>
</body>
</html>
```

## 几何图形绘制规则（SVG）

### 坐标系规范
- viewBox="0 0 180 180"，原点 O 位于 (90, 90)
- **y轴向上为负**，y值越小图形越高
- x轴向右为正，y轴向上为正

### 顶点标注位置（8年级几何）
| 顶点 | 位置 | 颜色 |
|------|------|------|
| A | 左上 | #1565c0 |
| B | 右上 | #1565c0 |
| C | 右下 | #1565c0 |
| D | 左下 | #1565c0 |
| 对角线交点 O | 中心 | #666 |

### 平行四边形标准画法（顶点顺时针/逆时针）
```
A(40,40) → B(140,40) → C(150,110) → D(50,110) → A
```
- AB // CD（水平），AD // BC（倾斜）
- 标出平行符号（//）和相等边（等长刻度线）

### 矩形标准画法
```
A(40,50) → B(140,50) → C(140,120) → D(40,120) → A
```
- 四个角都标直角符号（┏ ┓ ┗ ┛）
- 对角线 AC、BD

### 菱形标准画法（等边四边形）
```
A(90,30) → B(140,70) → C(90,110) → D(40,70) → A
```
- 四条边都标等长刻度
- 对角线 AC（竖直）、BD（水平）交于中心

### 一次函数直线绘制规则
直线 y = kx + b 在SVG中：
- y轴截距：b > 0 → 截距点在 y轴上半轴（SVG y值 < 90）
- y轴截距：b < 0 → 截距点在 y轴下半轴（SVG y值 > 90）
- k > 0：直线从左下到右上
- k < 0：直线从左上到右下

计算公式（已知截距点(90, b_svg)，斜率k）：
- 左端 x=10：y_svg = b_svg + k*(90-10)
- 右端 x=165：y_svg = b_svg + k*(90-165)

## 题目设计规范

### 选择题（5道）
- 覆盖核心概念、判定定理、易错陷阱
- 每个选项都要有迷惑性（不是一眼能排除的）
- 正确答案位置随机分布

### 填空题（5道）
- 包含1-2道计算题（面积、边长、解析式）
- 包含1道多结论判断题
- 包含正比例/一次函数参数综合题

### 大题（3道）
- 第1题：基础证明或推导（直接用判定定理）
- 第2题：综合计算（面积+边长+参数）
- 第3题：实际应用或创新变形

## 校验优先级

⚠️ **必须在生成HTML后立即运行校验脚本，不允许跳过校验环节。**
