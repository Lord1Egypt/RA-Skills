#!/usr/bin/env node
/**
 * CosDesign — Single Page Design Analysis
 * PROMPT GENERATOR ONLY — outputs a structured agent prompt.
 *
 * Usage:
 *   node scripts/analyze.js <url>
 *   node scripts/analyze.js <url> --focus color
 *   node scripts/analyze.js <url> --focus typography
 *   node scripts/analyze.js <url> --focus layout
 *   node scripts/analyze.js <url> --focus components
 *   node scripts/analyze.js <url> --focus all        (default)
 */

const args = process.argv.slice(2);
const focusIdx = args.indexOf('--focus');
const focus = focusIdx !== -1 ? args[focusIdx + 1] : 'all';
const url = args.filter(a => !a.startsWith('--') && a !== focus)[0];

if (!url) {
  console.error('Usage: node scripts/analyze.js <url> [--focus color|typography|layout|components|all]');
  process.exit(1);
}

const FOCUS_SECTIONS = {
  color: `
COLOR ANALYSIS:
1. Use WebFetch to load the URL: ${url}
2. Extract ALL colors from the page:
   - Primary brand color (buttons, links, CTA)
   - Secondary colors (accents, highlights)
   - Background colors (page bg, card bg, section bg)
   - Text colors (heading, body, caption, muted)
   - Border/divider colors
   - Gradient definitions (if any)
   - Semantic colors (success, warning, error, info)
3. Output as structured palette with:
   - HEX value
   - RGB value
   - HSL value
   - Usage context (where on page)
   - CSS variable name suggestion (e.g. --color-primary)`,

  typography: `
TYPOGRAPHY ANALYSIS:
1. Use WebFetch to load the URL: ${url}
2. Extract the complete type system:
   - Font families used (heading, body, mono, display)
   - Font size scale (list every distinct size from largest to smallest)
   - Font weight scale (thin→black, which weights are used where)
   - Line height for each size
   - Letter spacing (tracking) values
   - Text transform usage (uppercase headings, etc.)
3. Map to a type scale:
   - Display / H1 / H2 / H3 / H4 / Body / Small / Caption / Overline
   - For each: font-family, size, weight, line-height, letter-spacing, color
4. Note any Google Fonts or @font-face declarations`,

  layout: `
LAYOUT ANALYSIS:
1. Use WebFetch to load the URL: ${url}
2. Extract the layout system:
   - Page max-width / container width
   - Grid system (columns, gutter, margin)
   - Flexbox usage patterns
   - Spacing scale (padding/margin values — find the base unit: 4px? 8px?)
   - Section padding (vertical rhythm between sections)
   - Responsive breakpoints (if visible from meta viewport or media queries)
   - Header height, footer height
   - Sidebar width (if applicable)
3. Output a spacing token scale:
   - xs / sm / md / lg / xl / 2xl → pixel values
4. Output grid specification:
   - columns, gutter, margin at each breakpoint`,

  components: `
COMPONENT STYLE ANALYSIS:
1. Use WebFetch to load the URL: ${url}
2. Identify and extract visual parameters for each common component:

   BUTTONS:
   - Primary / Secondary / Ghost / Outline variants
   - padding, border-radius, font-size, font-weight
   - hover/active state changes (color shift, shadow)
   - Icon button size

   CARDS:
   - border-radius, shadow, padding, background
   - hover state (lift? border change?)

   NAVIGATION:
   - Height, background, text style, active indicator style
   - Mobile nav pattern (hamburger? slide-out?)

   FORMS:
   - Input height, padding, border-radius, border-color
   - Focus ring style, placeholder color
   - Label style, error state style

   OTHER:
   - Badge / Tag / Chip styles
   - Avatar sizes
   - Tooltip / Popover styles
   - Divider / Border patterns`,
};

const focusSections = focus === 'all'
  ? Object.values(FOCUS_SECTIONS).join('\n')
  : FOCUS_SECTIONS[focus] || FOCUS_SECTIONS.color;

console.log(`=== COSDESIGN — 设计分析 ===
目标 URL：${url}
分析维度：${focus}

你是一个专业的设计系统分析师。你的任务是从目标 URL 中精准提取视觉设计规范。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第一步 — 获取页面内容
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使用 WebFetch 获取页面：
  URL: ${url}
  Prompt: "Extract all CSS styles, colors, fonts, spacing, and layout information from this page. Include inline styles, stylesheet links, and computed visual properties."

如果 WebFetch 失败，尝试 Jina Reader：
  URL: https://r.jina.ai/${url}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第二步 — 设计分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${focusSections}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第三步 — 输出格式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

将分析结果按以下格式输出：

## 🎨 ${url} — 设计规范

### 色彩体系
| 名称 | HEX | 用途 | CSS变量 |
|------|-----|------|---------|
| Primary | #xxx | 按钮/链接 | --color-primary |
...

### 字体排版
| 层级 | 字体 | 大小 | 行高 | 字重 | 颜色 |
|------|------|------|------|------|------|
| H1 | ... | ... | ... | ... | ... |
...

### 间距系统
| Token | 值 | 用途 |
|-------|-----|------|
| --space-xs | 4px | 内边距最小值 |
...

### 布局
- 容器宽度：...
- 栅格：...
- 断点：...

### 组件风格
- 按钮：...
- 卡片：...

### 设计总结
用 3-5 句话概括这个网站的视觉风格（如：极简主义、圆角风、高对比度等）。

请确保所有数值精确到像素/具体值，不要使用模糊描述。
`);
