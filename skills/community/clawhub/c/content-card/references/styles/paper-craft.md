# paper-craft — 纸质手工

奶油纸底 + 虚线边框 + flat shadow。像手账本里撕下来的一页。

## CSS 变量

```css
:root {
  /* 背景 */
  --bg-primary: #FFF8F0;
  --bg-secondary: #FFF0E0;

  /* 文字 */
  --text-primary: #2C2420;
  --text-secondary: #6B5D52;

  /* 强调 */
  --accent: #E07A3A;
  --accent-light: #F09858;

  /* 字体 */
  --font-heading: 'LXGW WenKai', 'Ma Shan Zheng', cursive;
  --font-body: 'Noto Sans SC', 'PingFang SC', sans-serif;
  --font-mono: 'Fira Code', monospace;

  /* 圆角 */
  --radius: 16px;
  --radius-sm: 12px;
  --radius-lg: 20px;

  /* 阴影（flat shadow 风格） */
  --shadow: 0 3px 0 rgba(0, 0, 0, 0.08);
  --shadow-sm: 0 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 4px 0 rgba(0, 0, 0, 0.1);

  /* 边框 */
  --border: 1px dashed #D4C4B0;
  --border-solid: 2px solid #D4C4B0;
}
```

## 适用场景

- 教育类内容、轻松科普
- 手账风知识整理
- 亲子/育儿内容
- 生活小技巧、清单类
- 小红书干货贴

## 推荐布局搭配

| 布局 | 契合度 | 说明 |
|------|--------|------|
| `bento-grid` | ✓✓ | 虚线网格 = 手账分区感 |
| `linear-progression` | ✓✓ | 步骤教程的标配 |
| `winding-roadmap` | ✓ | 手绘路径感 |
| `hub-spoke` | ✓ | 中心概念 + 手工感标签 |
| `hierarchical-layers` | ✓ | 分层便签纸效果 |

## 设计要点

- 虚线边框（dashed）是核心视觉标志，不要换成实线
- flat shadow（纯 Y 轴偏移，无模糊）模拟纸片堆叠感
- 大圆角（16px+）保持柔和友好
- 标题用手写体/楷体，正文用常规无衬线——形成手写 vs 印刷的反差
- 可加轻微的纸纹背景纹理（`background-image` 叠加低透明度噪点）
- 橙红强调色用于标注、编号、重点标记
