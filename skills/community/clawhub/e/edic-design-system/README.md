# EDIC Design System Skill Package v1.9.1
# EDIC 设计系统 Skill 技能包 v1.9.1

[![License: MIT-0](https://img.shields.io/badge/License-MIT%200-blue.svg)](https://spdx.org/licenses/MIT-0.html)
[![Version](https://img.shields.io/badge/Version-1.9.1-green.svg)](https://edic.cgartlab.com/)

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

> **验证安装成功**：在任意项目中发送「用 EDIC 设计系统设计一个按钮」，Claude 应理解 `--ds-*` 令牌规范并使用 `ds-btn` `ds-btn--primary` 类名。

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
3. **Dark Mode / 暗色模式** — 基底用暖灰 `oklch(15% 0.008 75)`，非纯黑
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

完整组件目录（280+）见 `SKILL.md`。

---

## 参考资源

- **视觉手册**: https://edic.cgartlab.com/docs.html
- **下载页面**: https://edic.cgartlab.com/downloads.html
- **GitHub**: https://github.com/cgartlab/edic-design-system

---

## 更新日志 Changelog

### v1.9.1 (2026-06)
- 重构 tokens.json 为 flat 结构，与 CSS `--ds-*` 变量名一一对应
- 添加统一构建工具链 `scripts/lint.py` 和 `scripts/build.py`
- 完善打印/PDF 输出样式，添加 `@page` 规则

### v1.5.1 (2026-06)
- 补全 280+ 遗漏的组件类
- 统一组件目录结构
- 添加双语 README 安装说明
