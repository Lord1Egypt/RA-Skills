# morandi-warm — 莫兰迪暖色

低饱和暖色调，像旧书页、像午后的光。安静但有温度。

## CSS 变量

```css
:root {
  /* 背景 */
  --bg-primary: #F5F0E6;
  --bg-secondary: #EDE4D3;

  /* 文字 */
  --text-primary: #3D3832;
  --text-secondary: #7A6F63;

  /* 强调 */
  --accent: #B5836C;
  --accent-light: #D4A68C;

  /* 字体 */
  --font-heading: 'Noto Serif SC', 'Source Han Serif SC', serif;
  --font-body: 'Noto Serif SC', 'Source Han Serif SC', serif;
  --font-mono: 'SF Mono', 'Fira Code', monospace;

  /* 圆角 */
  --radius: 12px;
  --radius-sm: 8px;
  --radius-lg: 16px;

  /* 阴影 */
  --shadow: 0 2px 8px rgba(181, 131, 108, 0.12);
  --shadow-sm: 0 1px 4px rgba(181, 131, 108, 0.08);
  --shadow-lg: 0 4px 16px rgba(181, 131, 108, 0.16);

  /* 边框 */
  --border: 1px solid rgba(181, 131, 108, 0.2);
}
```

## 适用场景

- 文学叙事、散文随笔
- 生活方式、人文类内容
- 读书笔记、书评
- 个人成长、心理类内容
- 小红书生活类卡片

## 推荐布局搭配

| 布局 | 契合度 | 说明 |
|------|--------|------|
| `linear-progression` | ✓✓ | 叙事流天然适合线性推进 |
| `winding-roadmap` | ✓✓ | 旅程/成长叙事的最佳载体 |
| `iceberg` | ✓✓ | 暖色水面线 + 深浅分层，温柔的洞察 |
| `hub-spoke` | ✓ | 中心概念辐射，适合读书笔记 |
| `bento-grid` | ✓ | 暖色网格用于知识合集 |

## 设计要点

- 阴影必须染色（赭石色系），不用灰色默认阴影
- 字体用衬线体，增强文学气质
- 分隔用色块渐变或留白，不用硬线
- 强调色点到即止——小面积用于标题下划线、引号、标注
