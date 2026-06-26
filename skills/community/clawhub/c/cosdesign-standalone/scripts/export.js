#!/usr/bin/env node
/**
 * CosDesign — Design Specification Export
 * PROMPT GENERATOR ONLY — outputs a structured agent prompt.
 *
 * Usage:
 *   node scripts/export.js <url> --format css-vars
 *   node scripts/export.js <url> --format tokens
 *   node scripts/export.js <url> --format tailwind
 *   node scripts/export.js <url> --format html-report
 */

const args = process.argv.slice(2);
const fmtIdx = args.indexOf('--format');
const format = fmtIdx !== -1 ? args[fmtIdx + 1] : 'css-vars';
const url = args.filter(a => !a.startsWith('--') && a !== format)[0];

if (!url) {
  console.error('Usage: node scripts/export.js <url> --format css-vars|tokens|tailwind|html-report');
  process.exit(1);
}

const FORMAT_TEMPLATES = {
  'css-vars': `
输出格式：CSS Custom Properties

将分析结果输出为一个完整的 CSS :root {} 块：

:root {
  /* Colors */
  --color-primary: #xxx;
  --color-secondary: #xxx;
  --color-bg: #xxx;
  --color-bg-secondary: #xxx;
  --color-text: #xxx;
  --color-text-muted: #xxx;
  --color-border: #xxx;
  --color-accent: #xxx;

  /* Typography */
  --font-heading: 'xxx', sans-serif;
  --font-body: 'xxx', sans-serif;
  --font-mono: 'xxx', monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 20px;
  --text-2xl: 24px;
  --text-3xl: 30px;
  --text-4xl: 36px;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* Layout */
  --container-max: 1200px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}

确保每个值都来自实际页面分析，不要使用默认值。`,

  'tokens': `
输出格式：Design Tokens (JSON)

将分析结果输出为 W3C Design Token 格式的 JSON：

{
  "color": {
    "primary": { "value": "#xxx", "type": "color" },
    "secondary": { "value": "#xxx", "type": "color" },
    ...
  },
  "font": {
    "family": {
      "heading": { "value": "'xxx', sans-serif", "type": "fontFamily" },
      "body": { "value": "'xxx', sans-serif", "type": "fontFamily" }
    },
    "size": {
      "xs": { "value": "12px", "type": "dimension" },
      "sm": { "value": "14px", "type": "dimension" },
      ...
    },
    "weight": {
      "regular": { "value": "400", "type": "fontWeight" },
      "medium": { "value": "500", "type": "fontWeight" },
      "bold": { "value": "700", "type": "fontWeight" }
    },
    "lineHeight": {
      "tight": { "value": "1.25", "type": "number" },
      "normal": { "value": "1.5", "type": "number" },
      "relaxed": { "value": "1.75", "type": "number" }
    }
  },
  "spacing": { ... },
  "borderRadius": { ... },
  "shadow": { ... }
}`,

  'tailwind': `
输出格式：Tailwind CSS Config

将分析结果输出为 tailwind.config.js 的 theme.extend 对象：

/** @type {import('tailwindcss').Config} */
export default {
  theme: {
    extend: {
      colors: {
        primary: '#xxx',
        secondary: '#xxx',
        accent: '#xxx',
        background: { DEFAULT: '#xxx', secondary: '#xxx' },
        foreground: { DEFAULT: '#xxx', muted: '#xxx' },
        border: '#xxx',
      },
      fontFamily: {
        heading: ['xxx', 'sans-serif'],
        body: ['xxx', 'sans-serif'],
      },
      fontSize: {
        // 从页面提取的实际 type scale
      },
      spacing: {
        // 从页面提取的实际 spacing scale
      },
      borderRadius: {
        // 从页面提取的实际 radius values
      },
      boxShadow: {
        // 从页面提取的实际 shadow values
      },
    },
  },
}`,

  'html-report': `
输出格式：完整 HTML 设计报告

生成一个自包含的 HTML 文件，包含：

1. 页面顶部：站点名称 + URL + 分析日期
2. 色卡区域：每个颜色一个矩形色块 + HEX + 名称
3. 字体样本：每个字号层级的实际渲染效果
4. 间距可视化：用灰色方块展示间距比例
5. 组件示例：按钮/卡片/输入框的 CSS 代码
6. 底部：Design Tokens JSON 的可复制代码块

HTML 页面必须：
- 使用从目标网站提取的实际字体和颜色
- 包含深色/浅色主题切换按钮
- 包含字体大小调节控件
- 默认浅色主题
- 自适应响应式布局
- 所有样式内联，不依赖外部资源`,
};

const formatTemplate = FORMAT_TEMPLATES[format] || FORMAT_TEMPLATES['css-vars'];

console.log(`=== COSDESIGN — 设计规范导出 ===
目标 URL：${url}
输出格式：${format}

你是一个专业的设计系统工程师。从目标 URL 提取视觉参数并转换为可执行的设计规范。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第一步 — 获取页面
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使用 WebFetch 获取 ${url}
提取所有 CSS 属性：颜色、字体、间距、阴影、圆角、布局。

如果 WebFetch 返回内容不足，补充使用：
  WebFetch URL: https://r.jina.ai/${url}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第二步 — 提取设计参数
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

完整提取以下维度：
- 色彩体系（所有 HEX 值 + 用途）
- 字体排版（family, size scale, weight, line-height）
- 间距系统（base unit, scale, padding/margin 规律）
- 圆角（border-radius 值集合）
- 阴影（box-shadow 值集合）
- 布局（container width, grid, breakpoints）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第三步 — 按指定格式输出
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${formatTemplate}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
重要提醒
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- 所有值必须来自实际页面分析，不得使用预设值
- 色彩值精确到 HEX 6 位
- 字号精确到 px
- 间距精确到 px
- 如果页面使用 rem，按 1rem=16px 换算后同时标注两种单位
`);
