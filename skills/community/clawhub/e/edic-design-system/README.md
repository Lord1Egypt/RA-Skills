# EDIC Design System Skill Package v2.9.2
# EDIC 设计系统 Skill 技能包 v2.9.2

[![License: MIT-0](https://img.shields.io/badge/License-MIT%200-blue.svg)](https://spdx.org/licenses/MIT-0.html)
[![Version](https://img.shields.io/badge/Version-2.0.0-green.svg)](https://edic.cgartlab.com/)

---

## 适用场景 Scope

**✅ 适合以下场景：**

- 内容型网站、博客、文章排版
- 企业官网、品牌落地页
- 内部报告、多页文档
- 邮件模板、通讯设计
- 个人主页、作品集
- 需要精致 CJK（中日韩）排版的项目
- AI 辅助生成的界面原型

**❌ 目前不适合以下场景：**

- 游戏 UI（高对比/霓虹/像素风格）
- 重 Glassmorphism 风格
- 移动端原生应用（iOS/Android）
- 需要完全定制品牌色的项目（非橄榄绿体系）

> 以上不适用场景未来不排除支持，欢迎在 [GitHub Issues](https://github.com/cgartlab/edic-design-system/issues) 提需求。

---

## 快速上手 Quick Start

无论使用哪种 AI 工具，三步即可产出符合 EDIC 规范的界面：

**第一步：安装 Skill**（见下方各平台安装说明）

**第二步：用自然语言描述需求**

```
用 EDIC 设计系统，帮我做一个博客文章卡片列表，
包含封面图、标题、摘要、日期和「阅读全文」按钮。
```

**第三步：粘贴输出，即刻预览**

将 AI 返回的 HTML 片段粘贴进项目，确保已引入 `styles.css` 和 `scripts.js`，刷新即可预览 EDIC 样式。

> **Prompt 技巧：** 可以在描述需求时附加风格关键词，例如「偏杂志排版」「需要暗色模式」「CJK 中文优先」，Agent 会优先参考对应的组件和令牌。

---

## 安装 Installation

### Claude Code / Claude Code

```bash
# 项目级安装（推荐）
mkdir -p .claude/skills
# 解压本 ZIP，将 edic-design-system 目录内容放入 .claude/skills/edic-design-system/
# 或直接放置 SKILL.md 文件

# 全局安装
mkdir -p ~/.claude/skills/edic-design-system
cp SKILL.md ~/.claude/skills/edic-design-system/
```

> **验证安装成功**：将以下最小 demo 保存为 `test.html`，用浏览器打开——看到橄榄绿按钮即表示样式加载正常；
> 同时在 Claude Code 中发送「用 EDIC 设计系统设计一个按钮」，Claude 应使用 `ds-btn ds-btn--primary` 类名并遵循 `--ds-*` 令牌规范。

```html
<!doctype html>
<html lang="zh-CN" data-theme="">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDIC 安装验证</title>
    <link rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/cgartlab/edic-design-system@main/styles.css">
  </head>
  <body style="padding: 2rem">
    <button class="ds-btn ds-btn--primary">EDIC 安装成功 ✓</button>
    <script
      src="https://cdn.jsdelivr.net/gh/cgartlab/edic-design-system@main/scripts.js">
    </script>
  </body>
</html>
```

> **中文字体说明：** EDIC 使用系统字体栈（`"Noto Sans SC"`、`"Noto Serif SC"`），无需额外安装。
> 若目标环境未预装 Noto SC（如部分 Windows / Linux），可在 `<head>` 中补充以下代码确保稳定渲染：
>
> ```html
> <link rel="preconnect" href="https://fonts.googleapis.com">
> <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
> <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
> ```

### Cursor

```bash
# 方式一：写入项目级规则（推荐）
# 文件：.cursor/rules/edic-design-system.md
# 内容：复制 SKILL.md 的设计原则和组件规范部分

# 方式二：复制到全局 skills
mkdir -p ~/.cursor/skills/edic-design-system
cp SKILL.md ~/.cursor/skills/edic-design-system/
```

### Kiro

```bash
# 写入 steering 文件
mkdir -p .kiro/steering
# 复制 SKILL.md 设计规范到 .kiro/steering/edic-design-system.md
```

### GitHub Copilot

```bash
# 写入项目说明
# 文件：.github/copilot-instructions.md
# 内容：复制 SKILL.md 的设计原则、令牌和组件规范
```

### ChatGPT / Gemini / 其他 LLM

将 `SKILL.md` 的核心内容（设计原则 + 令牌速查 + 组件类名表）复制到：
- ChatGPT：Settings → Custom Instructions → "All conversations"
- Gemini：Gemini App Settings → AI Studio → System Instructions
- 其他：将规范作为每轮对话的首条系统消息

---

## 文件说明 Files

| 文件 | 用途 |
|------|------|
| `SKILL.md` | Agent 技能包 — 持久化遵循 EDIC 设计规范 |
| `README.md` | 安装指南 — 多平台 AI 工具接入说明 |
| `tokens.json` | 设计令牌 — 结构化 JSON 格式参考 |

---

## 设计原则 Design Principles

1. **OKLch Colors / OKLch 颜色** — 所有颜色使用 OKLch 色彩空间，绝不用 hex/rgb
2. **Token-Driven / 令牌驱动** — 使用 `--ds-*` CSS 变量，禁止硬编码魔法数字
3. **Dark Mode / 暗色模式** — 基底用暖灰 `oklch(17% 0.014 80)`，非纯黑
4. **Component System / 组件系统** — 基类 + 修饰符：`ds-btn` / `ds-btn--primary`
5. **Accessibility / 无障碍** — 图标按钮需 `aria-label`，装饰元素需 `aria-hidden`

---

## 核心令牌速查 Core Tokens

```css
/* Colors / 颜色 */
--ds-color-bg: oklch(97% 0.012 80)          /* Warm paper background */
--ds-color-fg: oklch(20% 0.02 60)           /* Body text */
--ds-accent: oklch(52% 0.08 115)           /* Olive green accent */

/* Typography / 字体 */
--ds-font-display: serif                   /* Headings */
--ds-font-body: sans-serif                 /* Body / UI */
--ds-font-mono: monospace                  /* Code */

/* Spacing / 间距 */
--ds-space-1..32                          /* 4px base ratio */

/* Radius / 圆角 */
--ds-radius-md: 4px

/* Motion / 动效 */
--ds-duration-150..500                    /* Duration scale */
--ds-ease-out: cubic-bezier(0.16, 1, 0.3, 1)
```

---

## 常用组件速查 Quick Component Reference

| 需求 | 组件类 |
|------|--------|
| Button / 按钮 | `ds-btn ds-btn--primary` |
| Card / 卡片 | `ds-card ds-card--hoverable` |
| Input / 输入框 | `ds-input ds-label` |
| Badge / 徽章 | `ds-badge ds-badge--accent` |
| Alert / 提示框 | `ds-alert ds-alert--info` |
| Navbar / 导航栏 | `ds-navbar ds-navbar-link--active` |
| Dark toggle / 暗色切换 | `ds-theme-toggle-btn` |
| Reveal animation / 揭示动效 | `ds-reveal` + `--d` stagger |
| Toast / 通知 | `ds-toast ds-toast-icon` |

完整组件契约（44 个核心组件家族）见 `SKILL.md`。

---

## 场景案例 Examples

以下均为官网真实页面，可直接查看源码作为参考：

| 场景 | 预览链接 | 核心组件 |
|------|----------|----------|
| 博客 / 文章页 | [blog.html](https://edic.cgartlab.com/blog.html) | `ds-prose` `ds-toc` `ds-badge` `ds-reveal` |
| 企业官网 | [company.html](https://edic.cgartlab.com/company.html) | `ds-hero-section` `ds-feature-card` `ds-footer-rich` |
| 个人简历 | [resume.html](https://edic.cgartlab.com/resume.html) | `ds-timeline` `ds-badge` `ds-grid-2` |
| 多页报告 | [report.html](https://edic.cgartlab.com/report.html) | `ds-docs` `ds-pagenav` `ds-table` |
| 设计系统主页 | [edic.cgartlab.com](https://edic.cgartlab.com/) | `ds-navbar` `ds-stat-grid` `ds-hero-section` |

---

## 常见问题 FAQ

**Q1：没有 `styles.css` 文件，示例代码能运行吗？**

不能。所有 `ds-*` 类名依赖 `styles.css` 中定义的 CSS 自定义属性。请先引入样式文件（本地路径或上方验证 demo 中的 jsDelivr CDN 链接），再运行示例代码。

---

**Q2：`tokens.json` 是做什么用的？怎么使用？**

`tokens.json` 是 EDIC 的结构化令牌导出：`tokens[]` 为当前机器入口，包含 `name`、`value`、`category`、`description`、`dark`、`aliases`、`status` 等元数据；`_legacyTokens` 保留 1.x 兼容读取。可用于 Figma Tokens 插件配置、Tailwind CSS 主题转换、AI 选择和批量生成。

---

**Q3：如何切换暗色模式？**

有两种方式：
- **手动**：在 `<html>` 标签上添加 `data-theme="dark"` 属性。
- **自动**：在页面中放置 `<button class="ds-theme-toggle-btn">` 按钮，引入 `scripts.js` 后会自动处理切换逻辑，用户选择通过 `localStorage`（key: `ds-theme-mode`）持久化。

若不引入 `scripts.js`，也可响应系统偏好：`styles.css` 内置了 `@media (prefers-color-scheme: dark)` 规则，无需 JavaScript。

---

**Q4：中文字体在某些环境下显示不对，怎么处理？**

EDIC 使用系统字体栈（`"Noto Sans SC"`、`"Noto Serif SC"`），在 macOS / 较新 Android 设备上通常已预装。若目标环境（如部分 Windows / Linux）未预装，建议在 `<head>` 中补充 Google Fonts 预加载（见上方「验证安装成功」下的字体说明代码块）。

---

**Q5：AI 生成的代码有 `ds-*` 类名，但样式完全不生效，怎么排查？**

按以下顺序检查：
1. 打开浏览器 DevTools → Network 面板，确认 `styles.css` 已加载且 HTTP 状态为 200。
2. 检查 `<link>` 标签的 `href` 路径是否正确（相对路径 vs 绝对路径）。
3. 确认 `<html>` 标签上没有被其他 CSS 框架覆盖 `--ds-*` 变量。

99% 的情况是第 1 步的路径问题。

---

**Q6：在 React / Vue / Svelte 等框架中怎么用？**

EDIC 是纯 CSS/JS，无需安装 npm 包。在框架的入口文件中引入 `styles.css` 即可：

```js
// React: src/index.js 或 src/main.jsx
import './path/to/styles.css';

// Vue: src/main.js
import './path/to/styles.css';
```

组件写法与普通 HTML 完全一致，直接在 JSX / 模板中使用 `className="ds-btn ds-btn--primary"`（React）或 `class="ds-btn ds-btn--primary"`（Vue/Svelte）。`scripts.js` 按需引入，或在 `index.html` 的 `<body>` 末尾用 `<script>` 标签引入。

---

## 参考资源

- **视觉手册**: https://edic.cgartlab.com/docs.html
- **下载页面**: https://edic.cgartlab.com/downloads.html
- **GitHub**: https://github.com/cgartlab/edic-design-system

---

## 更新日志 Changelog

### v1.9.2 (2026-06)
- 新增 `references/` 目录，包含三个按需加载的参考文件
- `references/EXAMPLES.md`：8 个高频复合组件（Glass Card、Docs 布局、Navbar、Toast、Accordion、Modal、Tabs、Dropdown）完整 HTML 结构示例
- `references/TOKENS.md`：间距 / 圆角 / 阴影 / 动效 / 排版令牌完整实际值速查表（含 px 换算）
- `references/ANTI-PATTERNS.md`：反模式 × 正确替代对照表，覆盖颜色、间距、Inline Style、BEM、无障碍、动效
- `SKILL.md` 末尾新增 Reference Files 章节，通过标准 Markdown 链接按需触发加载

### v2.9.2 (2026-09)
- 重构 tokens.json 为结构化数组，并保留 1.x 兼容读取层
- 添加统一构建工具链 `scripts/lint.py` 和 `scripts/build.py`
- 完善打印/PDF 输出样式，添加 `@page` 规则

### v1.5.1 (2026-06)
- 维护 44 个核心组件类与新增组件的样式契约
- 统一组件契约结构
- 添加双语 README 安装说明
