# tech-dark — 深色技术

深色背景 + 青色高亮。终端既视感，给开发者的视觉语言。

## CSS 变量

```css
:root {
  /* 背景 */
  --bg-primary: #1A1B1E;
  --bg-secondary: #25262B;

  /* 文字 */
  --text-primary: #C1C2C5;
  --text-secondary: #909296;

  /* 强调 */
  --accent: #00D9FF;
  --accent-light: #33E1FF;

  /* 字体 */
  --font-heading: 'JetBrains Mono', 'Fira Code', monospace;
  --font-body: 'Inter', 'Noto Sans SC', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* 圆角 */
  --radius: 8px;
  --radius-sm: 4px;
  --radius-lg: 12px;

  /* 阴影 */
  --shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  --shadow-sm: 0 2px 6px rgba(0, 0, 0, 0.2);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.4);

  /* 边框 */
  --border: 1px solid #373A40;
}
```

## 适用场景

- 开发者工具介绍、技术架构解析
- 代码相关内容、CLI 工具
- 技术选型对比
- 开源项目展示
- 极客社区分享

## 推荐布局搭配

| 布局 | 契合度 | 说明 |
|------|--------|------|
| `bento-grid` | ✓✓ | 深色网格 = 仪表盘既视感 |
| `dashboard` | ✓✓ | 深色看板是天然搭配 |
| `comparison-matrix` | ✓✓ | 深底 + 青色高亮行列 |
| `binary-comparison` | ✓✓ | 技术选型对比的标准画面 |
| `hub-spoke` | ✓ | 架构图中心辐射 |
| `circular-flow` | ✓ | 系统循环流，科技感 |
| `dense-modules` | ✓ | 高密度 + 深色 = 数据手册 |

## 设计要点

- 代码块/数据用等宽字体，与正文形成层次
- 强调色（青色）仅用于关键数据、标题装饰、边框高亮——不要大面积填充
- 文字避免纯白 #FFF，用 #C1C2C5 降低对比刺激
- 卡片间用 border 分隔而非阴影（深色背景下阴影不明显）
- 可在代码区块加微弱的青色 glow：`0 0 8px rgba(0, 217, 255, 0.1)`
