---
slug: "frontend-design-3-free"
name: "frontend-design-3-free"
version: "0.1.0"
displayName: "设计免费版"
summary: "基础版前端设计技能，创建独特界面并避免通用 AI 风格，支持 3 种美学方向。。frontend-design-3-free 是前端设计技能的基础版本，创建独特的生产级界面，避免通用"AI"
summary_zh: "基础版前端设计技能，创建独特界面并避免通用 AI 风格，支持 3 种美学方向。。frontend-design-3-free 是前端设计技能的基础版本，创建独特的生产级界面，避免通用"AI"
license: "MIT"
description: "|-. 适用于需要frontend design 3相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  frontend-design-3-free 是前端设计技能的基础版本，创建独特的生产级界面，避免通用"AI slop"美学.
  支持 3 种美学方向（brutally minimal、editorial/magazine、brutalist/raw）和基础字体、色彩、
  动效能力。不包含 8 种高级美学方向、Motion 库集成和背景视觉细节。适合快速创建独特界面，
  升级完整版获取全部 11 种美学方向和高级视觉技巧.
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 创意设计
  - frontend
  - design
  - automation
  - productivity
  - 设计
  - UI/UX
  - 创意
  - css-only
  - display
category: "Creative"
pricing_tier: free
---
# Frontend Design Free

frontend-design-3-free 创建独特的生产级前端界面，避免通用"AI slop"美学.
基础版支持 3 种美学方向和 CSS-only 动画方案.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Frontend Design Free处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

### 1. 设计思维与美学方向选择
在编码前理解上下文并承诺一个美学方向。分析四个维度：Purpose、Tone、Constraints、Differentiation.
基础版支持 3 种美学方向：brutally minimal（极简）、editorial/magazine（编辑杂志）、
brutalist/raw（粗野主义）。选择一种并优秀执行，不要混合多种方向。- 验证返回数据的完整性和格式正确性
- 参考`设计思维与美学方向选择`的配置文档进行参数调优
### 2. 字体策略（Display + Body 配对）
选择独特的字体，避免通用字体（Arial、Inter、Roboto、system fonts）。将 display 字体与
body 字体配对。基础版支持字体配对建议，但不包含跨美学方向的完整字体匹配策略.
禁止使用 Space Grotesk 等 AI 常见选择.

- 参考`字体策略（Display + Body 配对）`的配置文档进行参数调优
### 3. 色彩与主题系统
使用 CSS variables 建立色彩系统。主色配以锐利强调色优于均匀分布的调色板.
支持 light/dark 主题切换。基础版支持单色+一个强调色的配色策略，不包含高饱和度撞色、
霓虹色+暗色背景等高级配色方案.

- 参考`色彩与主题系统`的配置文档进行参数调优
### 4. CSS-only 动效
使用 CSS-only 方案实现动画（`@keyframes`、`transition`、`transform`）。聚焦高影响力时刻：
一次精心编排的页面加载配合 staggered reveals 比散落的微交互更有感染力。基础版不包含
Motion 库（React）集成.

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

1. 分析界面目的和目标用户
2. 从 3 种美学方向中选择一种（minimal、editorial、brutalist）
3. 确定 Differentiation：这个界面令人难忘的一个特征
4. 选择字体配对（display + body），避免通用字体
5. 建立色彩系统，使用 CSS variables
6. 实现 CSS-only 动效，聚焦页面加载的 staggered reveals
7. 检查反模式：确认无 Inter/Roboto/Arial、无紫色渐变白底
8. 输出生产级 HTML/CSS 代码

#
## 示例

### 示例1：Editorial 杂志风格落地页

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <style>
    :root {
      --display-font: 'Playfair Display', serif;
      --body-font: 'DM Sans', sans-serif;
      --ink: #1a1a1a;
      --paper: #f5f0e8;
      --accent: #c8102e;
    }
    body {
      font-family: var(--body-font);
      background: var(--paper);
      color: var(--ink);
      margin: 0;
    }
    .hero {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 48px;
      padding: 80px 64px;
    }
    .hero h1 {
      font-family: var(--display-font);
      font-size: 96px;
      font-weight: 900;
      line-height: 0.9;
      letter-spacing: -2px;
    }
    .hero h1 span {
      color: var(--accent);
      font-style: italic;
    }
    @keyframes reveal {
      from { opacity: 0; transform: translateY(24px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .hero h1 { animation: reveal 0.8s ease-out; }
    .hero p { animation: reveal 0.8s ease-out 0.2s both; }
  </style>
</head>
<body>
  <section class="hero">
    <h1>The Art of <span>Slow</span> Design</h1>
    <p>A quarterly journal on craft, intention, and the spaces between.</p>
  </section>
</body>
</html>
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 使用 Inter/Roboto/Arial 通用字体 | 默认使用系统字体或流行字体 | 选择 Distinctive 字体配对，如 Playfair Display + DM Sans |
| 白底紫色渐变老套配色 | AI 默认倾向常见的科技感配色 | 根据美学方向选择独特配色：editorial 用 ink+paper+accent |
| 可预测的居中三列卡片布局 | 默认使用对称网格 | 使用非对称 grid-template-columns（如 2fr 1fr） |
| 散落的微交互缺乏编排 | 每个元素独立动画 | 聚焦一次 staggered reveals 页面加载 |
| Minimalist 设计过度装饰 | 在需要克制的方向上添加过多元素 | minimalist 方向使用严格限制：单一字体、2-3 种颜色 |

## 常见问题

### Q1: 免费版支持哪些美学方向？
A: 免费版支持 3 种美学方向：brutally minimal、editorial/magazine、brutalist/raw.
完整版支持全部 11 种方向，包括 retro-futuristic、organic/natural、luxury/refined、
playful/toy-like、art deco/geometric、soft/pastel、industrial/utilitarian、maximalist chaos.
### Q2: 免费版可以使用 Motion 库吗？
A: 免费版仅支持 CSS-only 动画方案（`@keyframes`、`transition`、`transform`）.
完整版支持 React 环境下的 Motion 库集成（`motion.div`、`useScroll`、`useTransform`），
提供更强大的动画编排能力.
### Q3: 背景视觉细节在免费版中可用吗？
A: 免费版不包含 gradient meshes、noise textures、grain overlays 等高级背景视觉细节.
完整版支持全部 8 种背景创意形式，包括 SVG `feTurbulence` 滤镜、`backdrop-filter` 透明层叠等.
### Q4: 免费版支持 React/Vue 代码输出吗？
A: 免费版主要输出 HTML/CSS 代码。完整版支持 HTML/CSS/JS、React、Vue 等多种框架的
生产级代码输出，包含 Motion 库集成的 React 组件示例.
### Q5: 如何升级到完整版？
A: 将技能替换为完整版 frontend-design-3 即可。完整版包含 8 项核心能力、11 种美学方向、
Motion 库集成、8 种背景视觉细节和反模式完整规避策略.
## 已知限制

- 仅支持 3 种美学方向，不包含 retro-futuristic、organic/natural 等 8 种高级方向
- 不包含 Motion 库（React）集成，仅支持 CSS-only 动画
- 不包含 gradient meshes、noise textures、grain overlays 等背景视觉细节
- 不包含 custom cursors、decorative borders 等高级视觉技巧
- 不包含完整反模式规避清单（仅基础检查）

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "Frontend Design Free处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "frontend-design-3"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
