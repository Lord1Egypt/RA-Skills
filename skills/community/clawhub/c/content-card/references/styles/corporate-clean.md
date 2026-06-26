# corporate-clean — 商务清爽

白底蓝色系，干净专业。适合给老板看的那种图。

## CSS 变量

```css
:root {
  /* 背景 */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F8FAFC;

  /* 文字 */
  --text-primary: #333333;
  --text-secondary: #6B7280;

  /* 强调 */
  --accent: #2563EB;
  --accent-light: #3B82F6;

  /* 字体 */
  --font-heading: 'Satoshi', 'Noto Sans SC', sans-serif;
  --font-body: 'Satoshi', 'Noto Sans SC', sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', monospace;

  /* 圆角 */
  --radius: 8px;
  --radius-sm: 4px;
  --radius-lg: 12px;

  /* 阴影 */
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.1);

  /* 边框 */
  --border: 1px solid #E5E7EB;
}
```

## 适用场景

- 商业分析、产品方案
- 项目报告、周报/月报
- 数据看板截图风
- 竞品分析、市场调研
- 内部汇报材料

## 推荐布局搭配

| 布局 | 契合度 | 说明 |
|------|--------|------|
| `dashboard` | ✓✓ | 白底蓝色看板 = 标准商务仪表盘 |
| `funnel` | ✓✓ | 转化漏斗的经典配色 |
| `comparison-matrix` | ✓✓ | 清爽的多因素对比表 |
| `bento-grid` | ✓ | 模块化总览，整洁专业 |
| `winding-roadmap` | ✓ | 项目路线图 |
| `linear-progression` | ✓ | 流程展示 |

## 设计要点

- 阴影克制（0.08 透明度），不要浮夸的投影
- 蓝色强调色用于数据高亮、按钮、链接——避免大面积蓝底
- 数据数字可以放大加粗，形成视觉锚点
- 保持网格对齐，间距统一——商务感来自秩序
- 白底 + 浅灰卡片交替，制造层次但不花哨
