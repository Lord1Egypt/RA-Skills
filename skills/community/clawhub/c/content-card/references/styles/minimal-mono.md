# minimal-mono — 极简黑白

克制到极致的黑白灰。没有装饰，没有干扰，内容本身就是设计。

## CSS 变量

```css
:root {
  /* 背景 */
  --bg-primary: #FAFAFA;
  --bg-secondary: #F5F5F5;

  /* 文字 */
  --text-primary: #1a1a1a;
  --text-secondary: #666666;

  /* 强调 */
  --accent: #000000;
  --accent-light: #333333;

  /* 字体 */
  --font-heading: 'Geist', system-ui, -apple-system, sans-serif;
  --font-body: 'Geist', system-ui, -apple-system, sans-serif;
  --font-mono: 'Geist Mono', 'SF Mono', monospace;

  /* 圆角 */
  --radius: 0px;
  --radius-sm: 0px;
  --radius-lg: 0px;

  /* 阴影 */
  --shadow: none;
  --shadow-sm: none;
  --shadow-lg: none;

  /* 边框 */
  --border: 1px solid #E5E5E5;
}
```

## 适用场景

- 技术深度文章、架构分析
- 哲学思辨、本质追问
- 极客/开发者社区内容
- 任何希望"让内容说话"的场景

## 推荐布局搭配

| 布局 | 契合度 | 说明 |
|------|--------|------|
| `bento-grid` | ✓✓ | 直角网格 + 黑白色块，信息密度高 |
| `binary-comparison` | ✓✓ | 黑白对比天然适合二元对照 |
| `hierarchical-layers` | ✓✓ | 极简层级，每层用灰度区分 |
| `iceberg` | ✓✓ | 黑白分界线极有力量感 |
| `linear-progression` | ✓ | 简洁时间线 |
| `dense-modules` | ✓ | 高密度 + 极简 = 专业感 |

## 设计要点

- 分隔用细线（1px #E5E5E5），不用色块
- 强调用加粗或字号差异，不用颜色
- 留白是核心武器——宁可多留白，不堆装饰
- 标题与正文字号比至少 1.5:1
