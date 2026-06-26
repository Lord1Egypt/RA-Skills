---
name: bitmap-vectorize
version: 1.0.0
description: 将位图图像（截图、手绘照片、示意图等）转换为精确的矢量图形代码（SVG或Canvas）。当用户提供一张图片并希望将其重新绘制成可缩放、可编辑的矢量图形时，应使用本技能。特别适合物理示意图、几何图形、电路图、标注图等需要精确还原的场景。
---

# 物理位图矢量化（Physics Animation Prep）

## 概述

将高中物理题的示意图（位图）转换为精确的矢量图形代码，全程分 6 步完成任务。本技能为物理动画制作提供前期准备工作。

## 工作流程

### 第 0 步：建立坐标系和比例尺（关键！）

根据图像内容建立坐标系，并记录关键参数：

- 确定画布尺寸（宽×高），通常选择 800×500 或 600×400
- 确定原点位置和比例尺（1 个单位 = 多少像素）
- **重要**：Canvas 坐标系 y 轴向下（y 增大 = 向下），与数学坐标系相反
- 对于物理图形，先用数学坐标系推导，再转换到 Canvas 坐标系

### 第 1 步：识别原图中的元素组件

读取并分析用户提供的图像，识别以下元素：

- **物品名称**：水平地面、竖直墙面、小球、物块、细绳、轻杆、弹簧、斜面、圆弧轨道、电场 E、磁场 B、带电粒子 q 等
- **位置布局**：各元素的相对位置
- **相互关系**：接触、连接、束缚等关系

完成后向用户描述识别到的内容。

### 第 2 步：用题目文字校对第 1 步

获取用户提供的物理题目文字，逐项核对：

- 检查是否有遗漏的组件
- 检查位置布局是否正确
- 检查相互关系是否准确

**此步不可跳过**，必须与用户交互完成。

### 第 3 步：生成矢量图形

根据校对后的元素列表，生成矢量图形代码：

- 默认使用 **HTML Canvas**（方便后续生成动画）
- 检查：物品 ✓、位置 ✓、关系 ✓ 三者与原图一致
- **注意事项**（务必遵守）：
  - Canvas y 轴向下，与数学/物理 y 轴相反
  - 圆弧角度：Canvas 中 0 = 3 点钟方向，顺时针为正
  - 对于复杂图形，先推导关键点坐标，再编码
- 如图像标注不清晰，可先描述识别到的结构，请用户确认后再绘制

### 第 4 步：校对矢量图

与用户交互，逐项检查：

- 背景是否正确
- 物体形状、大小是否一致
- 颜色是否正确
- 中英文标注是否准确

**此步必须与客户交互完成**。

### 第 5 步：按需导出

根据客户需求导出：

- **默认**：HTML Canvas（方便后续动画制作）
- **可选**：SVG 文件、PNG 图片

## Canvas 绘图要点

```javascript
// 坐标转换：数学坐标 → Canvas坐标
// 数学坐标 (mx, my) → Canvas坐标 (cx, cy)
// cx = originX + mx * scale
// cy = originY - my * scale  // 注意y轴方向反转

// 常用绘制方法
ctx.beginPath();
ctx.arc(cx, cy, radius, startAngle, endAngle);  // 圆弧
ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);          // 直线
ctx.strokeStyle = '#333'; ctx.lineWidth = 2;
ctx.stroke();

// 虚线
ctx.setLineDash([5, 5]);
ctx.stroke();
ctx.setLineDash([]);  // 恢复实线

// 箭头
function drawArrow(ctx, fromX, fromY, toX, toY) {
    const headLen = 10;
    const angle = Math.atan2(toY - fromY, toX - fromX);
    ctx.beginPath();
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.lineTo(toX - headLen * Math.cos(angle - Math.PI/6), toY - headLen * Math.sin(angle - Math.PI/6));
    ctx.moveTo(toX, toY);
    ctx.lineTo(toX - headLen * Math.cos(angle + Math.PI/6), toY - headLen * Math.sin(angle + Math.PI/6));
    ctx.stroke();
}
```

## 常见物理图形处理

### 圆弧槽（如半圆形轨道）

```javascript
// 半圆弧，圆心在 (cx, cy)，半径 R
// 在Canvas中：从 π 到 0（顺时针方向）
ctx.arc(cx, cy, R, Math.PI, 0, false);  // 下半圆（Canvas中y向下）
```

### 带箭头坐标轴

```javascript
// x轴
drawArrow(ctx, 30, originY, width-20, originY);
ctx.fillText('x', width-15, originY+5);
// y轴（物理向上，Canvas向下绘制）
drawArrow(ctx, originX, height-20, originX, 20);
ctx.fillText('y', originX-15, 25);
```

### 标注点和虚线辅助线

```javascript
// 虚线从点到坐标轴
ctx.setLineDash([4, 4]);
ctx.beginPath();
ctx.moveTo(px, py);
ctx.lineTo(px, originY);  // 垂直虚线到x轴
ctx.stroke();
ctx.setLineDash([]);

// 标注点（实心圆）
ctx.beginPath();
ctx.arc(px, py, 4, 0, 2 * Math.PI);
ctx.fillStyle = 'black';
ctx.fill();
```

## references/

- `physics_shapes.md`：常见物理图形的 Canvas/SVG 代码片段（圆弧、力箭头、弹簧等）

## 注意事项（极其重要！）

### 坐标系差异

| 坐标系 | Y轴方向 | 角度正方向 |
|--------|---------|-----------|
| Canvas | Y轴向下（y增大=向下） | 顺时针 |
| 数学/物理 | Y轴向上（y增大=向上） | 逆时针 |

### 圆弧绘制

- Canvas 中 **0° = 右侧 3 点钟方向**
- Canvas **角度正方向 = 顺时针**（与数学物理相反）
- 因此：Canvas 中画上半圆是 `arc(cx, cy, R, 0, Math.PI, true)`，下半圆是 `arc(cx, cy, R, Math.PI, 0, false)`

### 坐标转换公式

```
数学坐标 (mx, my) → Canvas坐标 (cx, cy)
cx = originX + mx * scale
cy = originY - my * scale  // 注意y轴方向反转
```

### 其他

- 对于复杂图形，先在纸上推导关键点坐标，再编码
- 如图像标注不清晰，可先描述识别到的结构，请用户确认后再绘制

---

# Physics Animation Prep (English)

## Overview

Transform bitmap images of high school physics problems into precise vector graphics code. This skill prepares diagrams for physics animation production through a 6-step workflow.

## 6-Step Workflow

### Step 0: Establish Coordinate System & Scale

- Determine canvas size (typically 800×500 or 600×400)
- Set origin position and scale (1 unit = X pixels)
- **Critical**: Canvas y-axis points DOWN (y increases = downward), opposite to math/physics

### Step 1: Identify Components

Recognize these elements from the image:

- **Objects**: ground, wall, ball, block, rope, rod, spring, slope, arc track, electric field E, magnetic field B, charged particle q, etc.
- **Positions**: relative locations of all elements
- **Relationships**: contact, connection, constraint

### Step 2: Verify with Problem Text

Cross-check Step 1 with the physics problem description:

- Any missing components?
- Are positions correct?
- Are relationships accurate?

**This step is mandatory** - must complete with user interaction.

### Step 3: Generate Vector Graphics

Create Canvas code based on verified elements:

- Default output: **HTML Canvas** (for easy animation)
- Verify: Objects ✓, Positions ✓, Relationships ✓
- **Critical Notes**:
  - Canvas y-axis is inverted
  - Arc angles: 0° = 3 o'clock, clockwise positive
  - Derive coordinates mathematically first, then convert to Canvas

### Step 4: Verify Vector Diagram

Interact with user to check:

- Background correct?
- Object shapes and sizes match?
- Colors correct?
- Labels accurate?

### Step 5: Export

Export based on user needs:

- **Default**: HTML Canvas
- **Optional**: SVG, PNG

## Key Canvas Differences

| System | Y-axis | Angle Direction |
|--------|--------|-----------------|
| Canvas | Downward | Clockwise |
| Math/Physics | Upward | Counter-clockwise |

## Coordinate Conversion

```
Math (mx, my) → Canvas (cx, cy)
cx = originX + mx * scale
cy = originY - my * scale  // Note: y-axis inverted
```
