# Anything to HTML · 视觉语言 Tokens

本文档定义所有 archetype 共用的视觉 token。颜色、字体、间距、圆角、阴影都只从这里取。**不要在 HTML 里随意配色**——看似无伤大雅的一次自由发挥，会让同一个用户多次生成的产物风格割裂，也会削弱"这是一套严肃交付物"的信任感。

## 设计哲学

交付物不是营销落地页。视觉语言要做到：

- **克制**：中性底色 + 小面积强调色，避免满屏彩虹
- **冷静**：偏灰调的蓝/青作为主色，不用高饱和度的玩具色
- **结构分明**：边框、分隔线、留白都用来服务"一眼扫清结构"
- **中文友好**：字号和行高按中文阅读习惯调整，不直接照搬英文排版

## 一、颜色

### 中性色（文字、背景、边框）

```css
:root {
  /* 文字 */
  --color-text-1: #0f172a;      /* 主文字：标题、正文 */
  --color-text-2: #334155;      /* 次要文字：次级标题、段落内强调 */
  --color-text-3: #64748b;      /* 辅助文字：时间、元信息 */
  --color-text-4: #94a3b8;      /* 禁用、占位 */

  /* 背景 */
  --color-bg-page:   #ffffff;    /* 页面底色 */
  --color-bg-soft:   #f8fafc;    /* 柔和区块、引用块 */
  --color-bg-card:   #ffffff;    /* 卡片底色 */
  --color-bg-muted:  #f1f5f9;    /* 代码块、标签底 */

  /* 边框 / 分隔线 */
  --color-border-1: #e2e8f0;    /* 一级分隔：主要边框 */
  --color-border-2: #f1f5f9;    /* 二级分隔：表格行线 */
}
```

### 主色（强调、链接、按钮）

主色走的是"深墨蓝"方向——冷静、专业，不抢戏：

```css
:root {
  --color-primary:        #2563eb; /* 主强调 */
  --color-primary-hover:  #1d4ed8;
  --color-primary-soft:   #dbeafe; /* 淡底，用于标签/强调背景 */
}
```

### 功能色（状态、标注）

```css
:root {
  /* 成功 */
  --color-success:      #10b981;
  --color-success-soft: #d1fae5;

  /* 警告 */
  --color-warning:      #f59e0b;
  --color-warning-soft: #fef3c7;

  /* 危险 */
  --color-danger:       #ef4444;
  --color-danger-soft:  #fee2e2;

  /* 信息/中性蓝 */
  --color-info:         #0ea5e9;
  --color-info-soft:    #e0f2fe;
}
```

### 数据可视化色板（图表专用）

仪表盘/图表里多序列数据用这组。顺序即优先级，两色场景用前两个，三色用前三个，以此类推，保证不同产物的图表观感一致：

```css
:root {
  --chart-1: #2563eb; /* 深蓝 */
  --chart-2: #10b981; /* 绿 */
  --chart-3: #f59e0b; /* 金黄 */
  --chart-4: #8b5cf6; /* 紫 */
  --chart-5: #ef4444; /* 红 */
  --chart-6: #0ea5e9; /* 浅蓝 */
  --chart-7: #ec4899; /* 品红 */
  --chart-8: #64748b; /* 灰 */
}
```

### 暗色主题（可选，海报 archetype 里偶尔用）

```css
@media (prefers-color-scheme: dark) {
  /* 仅当显式启用 .dark 类或产物本身是暗色海报时才用 */
}

.dark {
  --color-text-1: #f1f5f9;
  --color-text-2: #cbd5e1;
  --color-text-3: #94a3b8;
  --color-bg-page: #0f172a;
  --color-bg-card: #1e293b;
  --color-border-1: #334155;
}
```

**默认所有 archetype 使用亮色**。暗色是海报类产物的可选风格，不要无缘无故切暗。

## 二、字体

### 字体栈

```css
:root {
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont,
               "PingFang SC", "Microsoft YaHei", "Helvetica Neue",
               Arial, sans-serif;
  --font-mono: "JetBrains Mono", "Fira Code", "SF Mono",
               Menlo, Consolas, "Courier New", monospace;

  /* 海报/大标题专用：更有张力 */
  --font-display: "Inter", "PingFang SC", sans-serif;
}
```

### 字号阶梯

```css
:root {
  --fs-xs:    12px;  /* 元信息、标签 */
  --fs-sm:    14px;  /* 辅助文字、表格 */
  --fs-base:  16px;  /* 正文 */
  --fs-lg:    18px;  /* 重点正文、小标题 */
  --fs-xl:    20px;  /* H4 */
  --fs-2xl:   24px;  /* H3 */
  --fs-3xl:   30px;  /* H2 */
  --fs-4xl:   36px;  /* H1 */
  --fs-5xl:   48px;  /* 海报大标题 */
  --fs-6xl:   64px;  /* 海报超大数字 */
}
```

### 字重

```css
:root {
  --fw-regular: 400;
  --fw-medium:  500;
  --fw-semibold: 600;
  --fw-bold:     700;
}
```

### 行高

```css
:root {
  --lh-tight:  1.25;  /* 大标题、数字 */
  --lh-normal: 1.5;   /* 数据密集区、卡片 */
  --lh-relaxed: 1.7;  /* 中文长文阅读 */
  --lh-loose:   1.85; /* 引用、散文 */
}
```

**中文排版建议**：正文长文用 `1.7`，数据仪表盘用 `1.5`，海报大标题用 `1.25`。

## 三、间距

全部基于 4px 基准，避免出现奇数间距：

```css
:root {
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-8:  32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
}
```

### 常用组合

- 段落之间：`--space-6` (24px)
- 小节之间：`--space-10` (40px)
- 大节之间：`--space-16` (64px)
- 卡片内边距：`--space-6` (24px)
- 卡片之间：`--space-4` (16px) 或 `--space-6` (24px)

## 四、圆角

```css
:root {
  --radius-sm:  4px;    /* 标签、小按钮 */
  --radius-md:  8px;    /* 按钮、输入框 */
  --radius-lg:  12px;   /* 卡片、区块 */
  --radius-xl:  16px;   /* 大卡片、海报元素 */
  --radius-full: 9999px; /* 胶囊、头像 */
}
```

## 五、阴影

阴影克制使用，只在卡片 hover 或需要"浮起"的元素上用。长文类产物基本不用阴影，改用边框。

```css
:root {
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.06);
  --shadow-lg: 0 12px 32px rgba(15, 23, 42, 0.08);
  --shadow-xl: 0 24px 64px rgba(15, 23, 42, 0.12);
}
```

## 六、过渡动画

```css
:root {
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}
```

只在 hover、focus、折叠展开等真实交互上用，不做纯装饰动画。

## 七、断点

```css
/* 移动端 */
@media (max-width: 768px) { ... }

/* 平板 */
@media (max-width: 1024px) { ... }
```

只需覆盖这两档即可，不用更精细的断点。

## 八、容器最大宽度

不同 archetype 使用不同容器宽度：

| 场景 | max-width |
|---|---|
| 长文阅读 | 760px（中文最佳阅读宽度约 36-40 字/行） |
| 长文 + 侧栏 | 1080px |
| 仪表盘 | 1280px（1440px 更宽松） |
| 海报 | 1200px（居中放置在更大视口里） |

容器一律 `margin: 0 auto` 居中，两侧 padding 至少 `--space-6` (24px)。

## 九、基础 reset

所有产物的 `<style>` 开头都加这段：

```css
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--font-sans);
  font-size: var(--fs-base);
  line-height: var(--lh-relaxed);
  color: var(--color-text-1);
  background: var(--color-bg-page);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
img, svg { display: block; max-width: 100%; }
a { color: var(--color-primary); text-decoration: none; }
a:hover { color: var(--color-primary-hover); text-decoration: underline; }
```

## 十、完整 `:root` 模板（直接复制）

生成 HTML 时，把下面这段放进 `<style>`，后续只引用变量即可。不需要用到的 token 可以保留不删——保留 token 对下一轮 AI 读取和修改都更友好。

```css
:root {
  /* 颜色 - 文字 */
  --color-text-1: #0f172a;
  --color-text-2: #334155;
  --color-text-3: #64748b;
  --color-text-4: #94a3b8;

  /* 颜色 - 背景 */
  --color-bg-page: #ffffff;
  --color-bg-soft: #f8fafc;
  --color-bg-card: #ffffff;
  --color-bg-muted: #f1f5f9;

  /* 颜色 - 边框 */
  --color-border-1: #e2e8f0;
  --color-border-2: #f1f5f9;

  /* 颜色 - 主色 */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-primary-soft: #dbeafe;

  /* 颜色 - 功能色 */
  --color-success: #10b981;
  --color-success-soft: #d1fae5;
  --color-warning: #f59e0b;
  --color-warning-soft: #fef3c7;
  --color-danger: #ef4444;
  --color-danger-soft: #fee2e2;
  --color-info: #0ea5e9;
  --color-info-soft: #e0f2fe;

  /* 颜色 - 图表 */
  --chart-1: #2563eb;
  --chart-2: #10b981;
  --chart-3: #f59e0b;
  --chart-4: #8b5cf6;
  --chart-5: #ef4444;
  --chart-6: #0ea5e9;
  --chart-7: #ec4899;
  --chart-8: #64748b;

  /* 字体 */
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
  --font-mono: "JetBrains Mono", "Fira Code", "SF Mono", Menlo, Consolas, "Courier New", monospace;

  /* 字号 */
  --fs-xs: 12px;
  --fs-sm: 14px;
  --fs-base: 16px;
  --fs-lg: 18px;
  --fs-xl: 20px;
  --fs-2xl: 24px;
  --fs-3xl: 30px;
  --fs-4xl: 36px;
  --fs-5xl: 48px;
  --fs-6xl: 64px;

  /* 字重 */
  --fw-regular: 400;
  --fw-medium: 500;
  --fw-semibold: 600;
  --fw-bold: 700;

  /* 行高 */
  --lh-tight: 1.25;
  --lh-normal: 1.5;
  --lh-relaxed: 1.7;
  --lh-loose: 1.85;

  /* 间距 */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.06);
  --shadow-lg: 0 12px 32px rgba(15, 23, 42, 0.08);
  --shadow-xl: 0 24px 64px rgba(15, 23, 42, 0.12);

  /* 过渡 */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}
```
