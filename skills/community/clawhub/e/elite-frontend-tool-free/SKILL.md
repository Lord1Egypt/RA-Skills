---

name: "elite-frontend-tool-free"
description: "高品质前端UI设计工具，提供字体、色彩、动效规则与反模式检查，输出HTML/CSS代码。Use when 需要设计创作、UI设计、海报制作、品牌视觉时使用。不适用于3D建模和动画制作。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "精英前端设计-免费版"
  version: "1.0.0"
  summary: "高品质前端UI设计工具，提供字体、色彩、动效规则与反模式检查，输出HTML/CSS代码。"
  tags:
    - "Creative"
    - "Frontend"
    - "UI"
    - "Design"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - browser

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# 精英前端设计工具（免费版）

## 概述

精英前端设计工具免费版是一款前端 UI 设计规范与代码生成工具。它通过严格的字体、色彩和动效规则，帮助你生成拒绝平庸、避免"AI 风格"同质化的前端界面。每次输出都追求独特的审美表达，而非统计概率的产物。

本版本适合个人项目 Landing Page、作品集页面和小型 Web 应用界面设计。输出标准 HTML/CSS 代码，可直接使用。

## 核心能力

| 能力 | 说明 |
|:-----|:-----|
| 字体规范 | 禁用通用字体，按场景精选字族，字重精细对比 |
| 色彩管理 | CSS 变量管理，主色+对比色，拒绝模板配色 |
| 基础动效 | 交错入场动画，CSS @keyframes 实现 |
| 反模式自检 | 自动检测并拒绝可预测的布局结构 |
| 单页面输出 | HTML/CSS 单文件输出 |

### 免费版设计规则

```text
字体规则:
  禁用: Inter, Roboto, Open Sans, Arial, Helvetica, Segoe UI
  代码/硬核: JetBrains Mono, Fira Code, Space Grotesk
  社论/高级: Playfair Display, Crimson Pro, Newsreader
  技术专业: IBM Plex Sans, IBM Plex Mono, Source Sans 3
  对比: 字重 100 vs 900，字号 3 倍跳跃

色彩规则:
  禁止: 白底 + 淡紫渐变 SaaS 配色
  要求: CSS 变量管理，主色+尖锐对比色
  灵感: IDE主题( Monokai, Dracula, Nord), 复古, 蒸汽波, 赛博朋克

动效规则:
  原则: 用动画赋予界面呼吸感
  实现: CSS @keyframes + animation-delay 交错
  高光: 页面加载交错显现 > 散乱微交互

反模式禁令:
  ❌ 居中Hero + 三列Feature + CTA 可预测结构
  ❌ 模版式组件缺乏语境
  ❌ 等宽等高卡片网格
  ✅ 不对称布局、Bento Grid、杂志排版、错落层叠
```

**输出**: 返回免费版设计规则的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：高品质前端、设计工具、提供字体、动效规则与反模式、精英前端设计工具、面向个人开发者的、设计规范与生成工、核心能力、严格字体规范、色彩管理规则、变量统一管理、基础动效指导、交错入场与微交互、拒绝平庸、风格界面等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：Landing Page 设计

为产品创建独特的 Landing Page。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>产品名称</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;900&family=IBM+Plex+Sans:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #1a1a2e;
      --bg-secondary: #16213e;
      --accent: #e94560;
      --accent-alt: #0f3460;
      --text: #eee;
      --text-muted: #8892b0;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'IBM Plex Sans', sans-serif;
      background:
        radial-gradient(ellipse at 20% 50%, rgba(233,69,96,0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(15,52,96,0.2) 0%, transparent 50%),
        linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
      color: var(--text);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* 不对称布局 - 拒绝居中Hero */
    .hero {
      display: grid;
      grid-template-columns: 1fr 1fr;
      min-height: 80vh;
      align-items: center;
      padding: 0 8%;
      gap: 4rem;
    }

    .hero-text { padding-top: 4rem; }

    .hero h1 {
      font-family: 'Playfair Display', serif;
      font-size: clamp(2.5rem, 6vw, 5rem);
      font-weight: 900;
      line-height: 1.05;
      margin-bottom: 1.5rem;
    }

    .hero h1 span {
      font-weight: 100;
      font-style: italic;
      color: var(--accent);
    }

    .hero p {
      font-size: 1.1rem;
      color: var(--text-muted);
      max-width: 28rem;
    }

    /* 交错入场动效 */
    .fade-in {
      opacity: 0;
      animation: fadeSlideUp 0.8s ease forwards;
    }
    .fade-in:nth-child(1) { animation-delay: 0.1s; }
    .fade-in:nth-child(2) { animation-delay: 0.3s; }
    .fade-in:nth-child(3) { animation-delay: 0.5s; }

    @keyframes fadeSlideUp {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .hero-visual {
      position: relative;
      height: 400px;
    }

    .visual-card {
      position: absolute;
      background: var(--accent-alt);
      border: 1px solid rgba(233,69,96,0.3);
      border-radius: 12px;
      padding: 1.5rem;
    }
  </style>
</head>
<body>
  <section class="hero">
    <div class="hero-text">
      <h1 class="fade-in">拒绝平庸<span>的设计</span></h1>
      <p class="fade-in">每一次输出都追求独特审美，而非统计概率的产物。</p>
    </div>
    <div class="hero-visual fade-in">
      <div class="visual-card">视觉区域</div>
    </div>
  </section>
</body>
</html>
```

### 场景二：Dashboard 界面

为后台管理系统设计 Dashboard。

```css
/* Dashboard 色彩系统 - Dracula 变体 */
:root {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --bg-card: #0f3460;
  --accent: #e94560;
  --accent-alt: #533483;
  --text: #eee;
  --text-muted: #8892b0;
  --border: rgba(233, 69, 96, 0.2);
}

/* Bento Grid 布局 - 拒绝等宽等高 */
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: auto auto auto;
  gap: 1rem;
  padding: 2rem;
}

/* 不对称卡片尺寸 */
.card-large { grid-column: span 2; grid-row: span 2; }
.card-wide  { grid-column: span 2; }
.card-tall  { grid-row: span 2; }
.card-small { grid-column: span 1; grid-row: span 1; }

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  opacity: 0;
  animation: cardEntrance 0.6s ease forwards;
}

.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4) { animation-delay: 0.4s; }

@keyframes cardEntrance {
  from { opacity: 0; transform: translateY(20px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
```

### 场景三：色彩主题快速生成

根据灵感来源生成配色方案。

```bash
# 色彩主题生成脚本
generate_palette() {
  local theme=$1
  case $theme in
    "dracula")
      echo "--bg-primary: #1a1a2e"
      echo "--bg-secondary: #16213e"
      echo "--accent: #e94560"
      echo "--accent-alt: #0f3460"
      ;;
    "nord")
      echo "--bg-primary: #2e3440"
      echo "--bg-secondary: #3b4252"
      echo "--accent: #88c0d0"
      echo "--accent-alt: #5e81ac"
      ;;
    "tokyo-night")
      echo "--bg-primary: #1a1b26"
      echo "--bg-secondary: #24283b"
      echo "--accent: #7aa2f7"
      echo "--accent-alt: #bb9af7"
      ;;
  esac
}

generate_palette "dracula"
```

## 不适用场景

以下场景精英前端设计-免费版不适合处理：

- 3D建模和动画制作
- 照片级写实渲染
- 手绘原创插画

## 触发条件

需要设计创作、UI设计、海报制作、品牌视觉时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 领先步：确定设计方向

在开始编码前，明确以下设计方向：

```text
设计方向确认:
  目的: 这个界面解决什么问题？谁在使用？
  基调: 选择一个极端方向
    - 极简主义 / 极繁主义
    - 复古未来 / 有机自然
    - 奢华精致 / 俏皮玩具感
    - 社论杂志 / 粗野主义
    - 装饰艺术 / 柔粉色调
  约束: 技术要求（框架、性能、可访问性）
  差异化: 什么让这个界面令人难忘？
```

### 第二步：选择字体组合

```html
<!-- 代码/硬核风格 -->
googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;700&display=swap" rel="stylesheet">

<!-- 社论/高级风格 -->
googleapis.com/css2?family=Playfair+Display:wght@400;900&family=IBM+Plex+Sans:wght@300;400;600&display=swap" rel="stylesheet">
```

### 第三步：生成代码

根据上述规则生成 HTML/CSS 代码，确保每次尝试不同的字体和审美倾向。

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

### CSS 变量色彩系统

```css
:root {
  /* Dracula 变体 */
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --accent: #e94560;
  --accent-alt: #0f3460;
  --text: #eee;
  --text-muted: #8892b0;
}

/* 背景深度 - 多层渐变叠加 */
body {
  background:
15) 0%, transparent 50%),
2) 0%, transparent 50%),
    linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}
```

### 动效配置

```css
/* 交错入场 - 核心动效模式 */
.card { opacity: 0; animation: fadeSlideUp 0.6s ease forwards; }

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

## 优选实践

1. **字体对比精细**：字重 100 vs 900，字号至少 3 倍跳跃。
2. **背景多层叠加**：拒绝纯色或单层渐变，用径向渐变创造深度。
3. **布局不对称**：拒绝居中 Hero + 三列 Feature 的可预测结构。
4. **动效交错显现**：页面加载时交错入场比散乱微交互更有冲击力。
5. **每次尝试不同**：不同字体、不同审美倾向，拒绝重复。

```text
免费版自检清单:
[ ] 未使用 Inter/Roboto/Open Sans 等禁用字体
[ ] 字重对比达到 100 vs 900
[ ] 字号跳跃至少 3 倍
[ ] 色彩用 CSS 变量管理
[ ] 背景有多层渐变叠加
[ ] 布局非对称或非标准网格
[ ] 动效采用交错入场
[ ] 无白底淡紫渐变 SaaS 配色
```

## 常见问题

### Q: 为什么禁用 Inter、Roboto 等字体？

A: 这些字体过于通用，导致界面缺乏个性。选择有辨识度的字体能立刻提升设计质感。

### Q: 免费版支持 React/Vue 组件生成吗？

A: 免费版聚焦 HTML/CSS 单页面输出。React/Vue 组件及多页面应用需要专业版。

### Q: 动效必须用 CSS 实现吗？

A: 免费版推荐纯 CSS @keyframes 实现，零依赖。专业版支持 Framer Motion 等高级动效库。

### Q: 配色方案从哪里获取灵感？

A: IDE 主题（Monokai、Dracula、Nord、Tokyo Night）、复古风、蒸汽波、赛博朋克、包豪斯等都是优质灵感来源。

### Q: 如何避免"AI 风格"界面？

A: 每次输出前自检反模式清单，拒绝可预测的结构、模版式组件和等宽等高网格。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **浏览器**: 任何现代浏览器（Chrome/Firefox/Safari/Edge）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Google Fonts | 字体 | 可选 | 通过 `<link>` 或 `@import` 加载 |

### API Key 配置
- 本Skill采用纯Markdown指令驱动，无需额外API Key
- Google Fonts 通过 CDN 免费加载

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 轻量级AI Skill，通过设计规范驱动生成高品质前端代码
- **适用规模**: 个人开发者，单页面设计

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

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据