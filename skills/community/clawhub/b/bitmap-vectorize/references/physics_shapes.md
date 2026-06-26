# 常见物理图形 Canvas 代码片段

## 坐标系设置

```javascript
const width = 600, height = 400;
const originX = 80;   // 原点x（Canvas坐标）
const originY = 300;  // 原点y（Canvas坐标）
const scale = 80;     // 1单位 = 80px

// 数学坐标 → Canvas坐标
function toCanvas(mx, my) {
    return { x: originX + mx * scale, y: originY - my * scale };
}
```

## 带箭头坐标轴

```javascript
function drawAxes(ctx) {
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1.5;
    // x轴
    drawArrow(ctx, 30, originY, width - 20, originY);
    ctx.fillText('x', width - 12, originY + 5);
    // y轴
    drawArrow(ctx, originX, height - 20, originX, 20);
    ctx.fillText('y', originX - 15, 18);
}
```

## 半圆弧（槽/轨道）

```javascript
// 下半圆（开口向上，常见物理槽形状）
// 圆心在 Canvas (cx, cy)，半径 R（像素）
ctx.beginPath();
ctx.arc(cx, cy, R, Math.PI, 0, false);  // 从左到右，下半圆
ctx.strokeStyle = '#2196F3';
ctx.lineWidth = 3;
ctx.stroke();

// 上半圆（开口向下）
ctx.arc(cx, cy, R, 0, Math.PI, false);
```

## 圆弧（任意角度）

```javascript
// 从角度 startAngle 到 endAngle（Canvas弧度，顺时针）
// Canvas角度：0=右，π/2=下，π=左，3π/2=上
ctx.beginPath();
ctx.arc(cx, cy, R, startAngle, endAngle, false);
ctx.stroke();
```

## 标注点

```javascript
function drawPoint(ctx, x, y, label, offsetX=8, offsetY=-8) {
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, 2 * Math.PI);
    ctx.fillStyle = '#e74c3c';
    ctx.fill();
    ctx.fillStyle = '#333';
    ctx.font = 'bold 14px serif';
    ctx.fillText(label, x + offsetX, y + offsetY);
}
```

## 虚线辅助线

```javascript
function drawDashLine(ctx, x1, y1, x2, y2) {
    ctx.save();
    ctx.setLineDash([5, 5]);
    ctx.strokeStyle = '#999';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.restore();
}
```

## 箭头（力、速度方向）

```javascript
function drawArrow(ctx, fromX, fromY, toX, toY, color='#e74c3c') {
    const headLen = 12;
    const angle = Math.atan2(toY - fromY, toX - fromX);
    ctx.save();
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.stroke();
    // 箭头头部
    ctx.beginPath();
    ctx.moveTo(toX, toY);
    ctx.lineTo(toX - headLen * Math.cos(angle - Math.PI/6),
               toY - headLen * Math.sin(angle - Math.PI/6));
    ctx.lineTo(toX - headLen * Math.cos(angle + Math.PI/6),
               toY - headLen * Math.sin(angle + Math.PI/6));
    ctx.closePath();
    ctx.fill();
    ctx.restore();
}
```

## 实心球（运动的小球）

```javascript
function drawBall(ctx, x, y, r=10, color='#e74c3c') {
    const grad = ctx.createRadialGradient(x-r*0.3, y-r*0.3, r*0.1, x, y, r);
    grad.addColorStop(0, '#ff8a80');
    grad.addColorStop(1, color);
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.fillStyle = grad;
    ctx.fill();
}
```

## 弹簧

```javascript
function drawSpring(ctx, x1, y1, x2, y2, coils=6) {
    const dx = (x2 - x1) / (coils * 2 + 2);
    const dy = (y2 - y1) / (coils * 2 + 2);
    const perpX = -(y2 - y1) / Math.sqrt((x2-x1)**2 + (y2-y1)**2) * 8;
    const perpY = (x2 - x1) / Math.sqrt((x2-x1)**2 + (y2-y1)**2) * 8;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    for (let i = 0; i < coils * 2; i++) {
        const t = (i + 1) / (coils * 2 + 2);
        const mx = x1 + (x2 - x1) * t;
        const my = y1 + (y2 - y1) * t;
        const sign = i % 2 === 0 ? 1 : -1;
        ctx.lineTo(mx + perpX * sign, my + perpY * sign);
    }
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = '#555';
    ctx.lineWidth = 1.5;
    ctx.stroke();
}
```

## 角度标注（弧线+数字）

```javascript
function drawAngle(ctx, cx, cy, r, startAngle, endAngle, label) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, startAngle, endAngle);
    ctx.strokeStyle = '#666';
    ctx.lineWidth = 1;
    ctx.stroke();
    const midAngle = (startAngle + endAngle) / 2;
    ctx.fillStyle = '#333';
    ctx.font = '13px serif';
    ctx.fillText(label, cx + (r+8)*Math.cos(midAngle), cy + (r+8)*Math.sin(midAngle));
}
```
