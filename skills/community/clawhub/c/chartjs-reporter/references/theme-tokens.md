# 主题设计规范（Theme Tokens）

## 颜色系统

| 变量名         | 值        | 用途                     |
|--------------|----------|--------------------------|
| `--bg`       | `#0f172a` | 页面背景                  |
| `--card`     | `#1e293b` | 卡片/图表背景              |
| `--border`   | `#334155` | 分割线/边框               |
| `--accent`   | `#38bdf8` | 主色调（蓝色）KPI/标题     |
| `--accent2`  | `#818cf8` | 辅色调（紫色）             |
| `--green`    | `#34d399` | 正面指标（增长/完成）       |
| `--yellow`   | `#fbbf24` | 中性指标（警告/关注）       |
| `--red`      | `#f87171` | 负面指标（下降/风险）       |
| `--text`     | `#e2e8f0` | 正文文字                  |
| `--muted`    | `#94a3b8` | 次要文字/轴标签/标题       |

## 图表调色板（PALETTE，10色循环）

```
#38bdf8  蓝
#818cf8  紫
#34d399  绿
#fbbf24  黄
#fb923c  橙
#f472b6  粉
#a78bfa  淡紫
#4ade80  浅绿
#60a5fa  天蓝
#facc15  金黄
```

## 尺寸规范

| 元素         | 规格                              |
|------------|----------------------------------|
| 图表高度     | 固定 240px（`chart-wrap`）        |
| 卡片圆角     | 12px                             |
| 卡片内边距   | 20px 22px                        |
| 网格间距     | 20px（图表）/ 16px（KPI）         |
| KPI 数值字号 | 1.85rem, font-weight: 700        |
| 图表标题字号 | 0.85rem, uppercase, color: muted |

## 字体栈

```css
font-family: 'Segoe UI', system-ui, sans-serif;
```

## 图表坐标轴风格

```js
// X 轴
grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" }

// Y 轴
grid: { color: "#334155" }, ticks: { color: "#94a3b8" }
```

## 图例样式

```js
labels: { color: "#94a3b8", font: { size: 12 } }
```
