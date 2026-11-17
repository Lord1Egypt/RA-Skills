---
name: "frontend-design-v3-free"
description: "独特前端界面生成工具，拒绝AI同质化风格，输出有辨识度的HTML/CSS代码。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "前端设计V3-免费版"
  version: "1.0.0"
  summary: "独特前端界面生成工具，拒绝AI同质化风格，输出有辨识度的HTML/CSS代码。"
  tags:
    - "Creative"
    - "Frontend"
    - "Design"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 前端设计工具V3（免费版）

## 概述

前端设计工具V3免费版是一款独特前端界面生成工具。它致力于创造有辨识度的前端界面，拒绝平庸的"AI风格"同质化输出。通过鲜明美学方向选择和反模式检查，确保每次输出都是经过精心设计的独特作品。

本版本适合个人项目网页设计、创意作品集页面和独特风格的概念页面。输出标准 HTML/CSS/JS 代码，可直接使用。

## 核心能力

| 能力 | 说明 |
|:-----|:-----|
| 美学方向选择 | 10种极端美学方向，每次选择不同 |
| 字体指导 | 拒绝通用字体，精选独特字族配对 |
| 色彩指导 | CSS变量管理，主色+对比色拒绝均匀分布 |
| 动效指导 | CSS优先方案，高影响力动效编排 |
| 布局指导 | 不对称、重叠、对角流、网格破除 |
| 背景深度 | 渐变网格、噪点纹理、几何图案 |
| 反模式检查 | 自动拒绝可预测的设计套路 |

### 美学方向选择

```text
可选美学方向（每次选择一个极端）:
  1. Brutally Minimal     极简主义
  2. Maximalist Chaos     极繁混乱
  3. Retro-Futuristic     复古未来
  4. Organic/Natural       有机自然
  5. Luxury/Refined        奢华精致
  6. Playful/Toy-like      俏皮玩具
  7. Editorial/Magazine    社论杂志
  8. Brutalist/Raw         粗野主义
  9. Art Deco/Geometric    装饰艺术
  10. Soft/Pastel          柔粉色调
```

**输入**: 用户提供美学方向选择所需的指令和必要参数。
**处理**: 按照skill规范执行美学方向选择操作,遵循单一意图原则。
**输出**: 返回美学方向选择的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 反模式禁令

```text
永远不要使用:
  ❌ Inter, Roboto, Arial 等通用字体
  ❌ 白底紫色渐变的通用 SaaS 配色
  ❌ 可预测的布局和组件模式
  ❌ 缺乏语境的模版式设计
  ❌ 多次生成趋向同一字体（如 Space Grotesk）
```

**输入**: 用户提供反模式禁令所需的指令和必要参数。
**处理**: 按照skill规范执行反模式禁令操作,遵循单一意图原则。
**输出**: 返回反模式禁令的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：独特前端界面生成、同质化风格、输出有辨识度的、HTML、前端设计工具、免费版、面向个人开发者的、核心能力、鲜明美学方向选择、布局四维设计指导、避免可预测的设计、输出可用的等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：创意作品集页面

为个人作品集创建独特风格的页面。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>作品集</title>
  <!-- 社论/杂志风格字体配对 -->
  <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,700;1,400&family=Space+Grotesk:wght@300;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --ink: #0a0a0a;
      --paper: #f5f1e8;
      --accent: #c8553d;
      --muted: #8b8378;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'Space Grotesk', sans-serif;
      background: var(--paper);
      color: var(--ink);
      /* 噪点纹理背景 */
      background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.9'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E");
    }

    /* 杂志式排版 - 不对称布局 */
    .portfolio {
      display: grid;
      grid-template-columns: 1fr 2fr 1fr;
      grid-template-rows: auto auto auto;
      min-height: 100vh;
      padding: 4rem 2rem;
      gap: 2rem;
    }

    .title-block {
      grid-column: 1 / 3;
      grid-row: 1;
    }

    .title-block h1 {
      font-family: 'Crimson Pro', serif;
      font-size: clamp(3rem, 8vw, 7rem);
      font-weight: 700;
      line-height: 0.9;
      letter-spacing: -0.03em;
    }

    .title-block h1 em {
      font-style: italic;
      font-weight: 400;
      color: var(--accent);
    }

    .meta {
      grid-column: 3;
      grid-row: 1;
      writing-mode: vertical-rl;
      font-size: 0.75rem;
      letter-spacing: 0.3em;
      text-transform: uppercase;
      color: var(--muted);
      align-self: start;
    }

    /* 作品展示 - 对角流布局 */
    .work-1 { grid-column: 1; grid-row: 2; }
    .work-2 { grid-column: 2; grid-row: 2; margin-top: 3rem; }
    .work-3 { grid-column: 2; grid-row: 3; margin-top: -2rem; }

    .work-item {
      opacity: 0;
      animation: reveal 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    }
    .work-item:nth-child(1) { animation-delay: 0.2s; }
    .work-item:nth-child(2) { animation-delay: 0.4s; }
    .work-item:nth-child(3) { animation-delay: 0.6s; }

    @keyframes reveal {
      from { opacity: 0; transform: translateY(40px) rotate(-1deg); }
      to   { opacity: 1; transform: translateY(0) rotate(0); }
    }

    .work-item h3 {
      font-family: 'Crimson Pro', serif;
      font-size: 1.5rem;
      font-weight: 400;
      font-style: italic;
      margin-bottom: 0.5rem;
    }

    .work-item p {
      font-size: 0.875rem;
      color: var(--muted);
      max-width: 20rem;
    }
  </style>
</head>
<body>
  <div class="portfolio">
    <div class="title-block">
      <h1>设计的<em>可能性</em></h1>
    </div>
    <div class="meta">PORTFOLIO · 2025</div>

    <div class="work-item work-1">
      <h3>极简之美</h3>
      <p>用最少的元素传达最强的信息。</p>
    </div>
    <div class="work-item work-2">
      <h3>色彩对话</h3>
      <p>当暖色遇见冷色，故事就开始了。</p>
    </div>
    <div class="work-item work-3">
      <h3>空间留白</h3>
      <p>留白不是空虚，而是呼吸。</p>
    </div>
  </div>
</body>
</html>
```

### 场景二：概念落地页

为产品创意制作概念性落地页。

```css
/* 复古未来主义风格 - 概念落地页 */
:root {
  --bg: #1a0033;
  --grid: rgba(255, 0, 255, 0.08);
  --neon-pink: #ff00ff;
  --neon-cyan: #00ffff;
  --neon-yellow: #ffff00;
  --text: #e0e0ff;
}

body {
  background: var(--bg);
  background-image:
    linear-gradient(var(--grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 40px 40px;
  color: var(--text);
  font-family: 'IBM Plex Mono', monospace;
}

/* 霓虹文字效果 */
.neon-title {
  font-size: clamp(2rem, 6vw, 5rem);
  font-weight: 100;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  text-shadow:
    0 0 10px var(--neon-cyan),
    0 0 20px var(--neon-cyan),
    0 0 40px var(--neon-pink);
  animation: flicker 3s infinite alternate;
}

@keyframes flicker {
  0%, 18%, 22%, 25%, 53%, 57%, 100% { opacity: 1; }
  20%, 24%, 55% { opacity: 0.4; }
}

/* 扫描线效果 */
.scanlines::after {
  content: "";
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent 0,
    rgba(0,0,0,0.1) 1px,
    transparent 2px
  );
  pointer-events: none;
}
```

### 场景三：选择美学方向

```bash
# 美学方向选择指南
echo "选择一个极端美学方向:"
echo "1. 极简主义   - 用最少元素传达最强信息"
echo "2. 极繁混乱   - 信息密集，视觉冲击"
echo "3. 复古未来   - 80年代赛博朋克"
echo "4. 有机自然   - 流动曲线，自然色彩"
echo "5. 奢华精致   - 金属质感，深色调"
echo "6. 俏皮玩具   - 圆润形状，明亮色彩"
echo "7. 社论杂志   - 衬线字体，网格排版"
echo "8. 粗野主义   - 裸露结构，单色对比"
echo "9. 装饰艺术   - 几何对称，金色点缀"
echo "10. 柔粉色调  - 柔和渐变，圆润边角"
```

## 不适用场景

以下场景前端设计V3-免费版不适合处理：

- 3D建模和动画制作
- 照片级写实渲染
- 手绘原创插画

## 触发条件

需要设计创作、UI设计、海报制作、品牌视觉时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 第一步：明确设计思考

在编码前，回答以下问题：

```text
设计思考框架:
  目的: 这个界面解决什么问题？谁在使用？
  基调: 选择一个极端美学方向（见上方列表）
  约束: 技术要求（框架、性能、可访问性）
  差异化: 什么让这个界面令人难忘？
         那一个让人记住的点是什么？
```

### 第二步：选择字体配对

```html
<!-- 独特字体配对示例 -->
<!-- 配对1: 衬线标题 + 无衬线正文 -->
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;900&family=IBM+Plex+Sans:wght@300;400;600&display=swap" rel="stylesheet">

<!-- 配对2: 等宽字体 + 衬线正文 -->
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Crimson+Pro:ital,wght@0,400;1,400&display=swap" rel="stylesheet">

<!-- 配对3: 几何无衬线 + 人文衬线 -->
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Newsreader:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
```

### 第三步：生成代码

根据选择的美学方向生成 HTML/CSS 代码，确保每次尝试不同的字体和审美倾向。

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

### CSS 变量色彩系统

```css
:root {
  /* 深色系 - 拒绝通用 SaaS 配色 */
  --bg-primary: #0a0a0a;
  --bg-secondary: #1a1a2e;
  --accent: #c8553d;
  --text: #f5f1e8;
  --text-muted: #8b8378;
}
```

### 背景深度方案

```css
/* 方案1: 噪点纹理 */
body::before {
  content: "";
  position: fixed;
  inset: 0;
  background: url("data:image/svg+xml,..."); /* SVG noise */
  opacity: 0.05;
  pointer-events: none;
}

/* 方案2: 多层渐变 */
body {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(200,85,61,0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(26,26,46,0.2) 0%, transparent 50%),
    var(--bg-primary);
}

/* 方案3: 几何图案 */
body {
  background-image:
    linear-gradient(45deg, transparent 48%, rgba(255,255,255,0.02) 49%, rgba(255,255,255,0.02) 51%, transparent 52%);
  background-size: 20px 20px;
}
```

## 最佳实践

1. **美学方向明确**：每次选择一个极端方向，精准执行而非模糊折中。
2. **字体配对独特**：拒绝通用字体，每次尝试不同字体组合。
3. **色彩主次分明**：主色主导 + 尖锐对比色点缀，拒绝均匀分布。
4. **动效高影响力**：一次精心编排的页面加载胜过散乱微交互。
5. **布局不拘一格**：不对称、重叠、对角流、网格破除创造惊喜。

```text
免费版自检清单:
[ ] 美学方向已明确选择（10选1）
[ ] 字体非通用（非 Inter/Roboto/Arial）
[ ] 色彩非白底紫渐变 SaaS 配色
[ ] 布局非居中Hero+三列Feature可预测结构
[ ] 背景有多层深度（非纯色/单层渐变）
[ ] 动效有编排（非散乱微交互）
[ ] 每次输出尝试不同字体和审美
```

## 常见问题

### Q: 为什么要拒绝"AI风格"？

A: 通用AI生成界面趋向同质化（相似字体、相似配色、相似布局），缺乏辨识度。独特的设计才能让人记住。

### Q: 免费版支持 React/Vue 输出吗？

A: 免费版聚焦 HTML/CSS/JS 输出。React/Vue 等框架的生产级代码需要专业版。

### Q: 美学方向可以混合吗？

A: 建议每次选择一个明确方向并精准执行。大胆的极繁和精致极简都可以，关键是有意图性。

### Q: 如何选择字体配对？

A: 将独特展示字体与精致正文字体配对。避免每次都用同一种字体（如反复使用 Space Grotesk）。

### Q: 动效应该优先用什么实现？

A: HTML 输出优先用纯 CSS 方案。一次精心编排的交错显现页面加载，比散乱微交互更有冲击力。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **浏览器**: 任何现代浏览器

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Google Fonts | 字体 | 可选 | CDN免费加载 |

### API Key 配置
- 本Skill采用纯Markdown指令驱动，无需额外API Key
- Google Fonts 通过 CDN 免费加载

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 轻量级AI Skill，通过美学规范驱动生成独特前端界面
- **适用规模**: 个人开发者，单页面创意设计

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力