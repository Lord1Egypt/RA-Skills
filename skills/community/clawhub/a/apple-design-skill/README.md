# Apple Design Skill 🍎

[English](#english) | [中文](#中文)

---

## English

An open-source AI Skill that guides AI coding assistants to generate frontend UI code in Apple's iconic design style. Compatible with both **OpenClaw** and **Claude Code** ecosystems.

### Features

- **Design Token System** — Colors, spacing, font weights, shadows, gradients, and responsive breakpoints faithful to Apple's visual language
- **Typography Engine** — Multi-language font stacks (EN, zh-CN, zh-TW, JA, KO) with automatic fallback to Google Fonts
- **Copywriting Optimizer** — Transforms ordinary copy into Apple-style "crisp & punchy" headlines and descriptions
- **Image Curator** — Recommends high-quality free images from Unsplash/Pexels with CSS gradient fallbacks
- **Layout Patterns** — Hero sections, product grids, feature cards, and scroll-animated blocks

### Installation

#### OpenClaw (Recommended)

```bash
# Install via OpenClaw CLI
openclaw install apple-design-skill
```

Once installed, the Skill is automatically loaded by your AI coding assistant within the OpenClaw ecosystem.

#### Claude Code

Copy the `CLAUDE.md` file from this repository into your project root. Claude Code will automatically pick it up as a custom instruction file.

```bash
# Clone and copy
git clone https://github.com/user/apple-design-skill.git
cp apple-design-skill/CLAUDE.md /path/to/your/project/CLAUDE.md
```

### Usage Examples

After installing the Skill, simply ask your AI coding assistant to generate Apple-style pages:

**Example 1 — Product Landing Page**

```
Generate a product landing page for a wireless headphone in Apple style.
```

**Example 2 — Feature Showcase Page**

```
Create a feature showcase page highlighting 4 key features of a smartwatch, Apple style.
```

**Example 3 — Pricing Page**

```
Build a pricing comparison page with 3 tiers in Apple's clean design language.
```

See the `examples/` directory for full prompt-input / HTML-output pairs.

### Responsibility Boundaries

This project clearly separates what is implemented by the Skill itself, what relies on the OpenClaw platform, and what depends on third-party services.

| Capability | Implemented By |
|---|---|
| Design Token System (colors, spacing, shadows, etc.) | ✅ Skill itself |
| Typography Engine (font stacks, sizes, weights) | ✅ Skill itself |
| Copywriting Optimizer (copy rules & patterns) | ✅ Skill itself |
| Layout Patterns (Hero, grid, cards, scroll) | ✅ Skill itself |
| Image Curator — selection rules & CSS fallbacks | ✅ Skill itself |
| Image Curator — live API search (Unsplash/Pexels) | 🔌 Optional extension (third-party API) |
| Skill installation & distribution | 🏗️ OpenClaw platform |
| Version management | 🏗️ OpenClaw platform |
| Dependency resolution | 🏗️ OpenClaw platform |
| User ratings & reviews | 🏗️ OpenClaw platform |

### Project Structure

```
apple-design-skill/
├── README.md                   # This file
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guide
├── CHANGELOG.md                # Version history
├── manifest.json               # OpenClaw Skill metadata
├── CLAUDE.md                   # Claude Code compatible entry
├── prompts/
│   ├── main.md                 # Core entry prompt
│   ├── design-tokens.md        # Design token definitions
│   ├── typography.md           # Multi-language font system
│   ├── copywriting.md          # Copywriting optimization rules
│   ├── image-curation.md       # Image curation strategy
│   └── layout-patterns.md      # Layout pattern templates
└── examples/
    ├── product-landing/        # Product landing page example
    ├── feature-showcase/       # Feature showcase page example
    └── pricing-page/           # Pricing page example
```

### License

This project is licensed under the [MIT License](LICENSE).

---

## 中文

一个开源的 AI Skill 项目，指导 AI 编码助手生成具有苹果官网设计风格的前端 UI 代码。同时兼容 **OpenClaw** 和 **Claude Code** 生态。

### 功能特性

- **设计令牌系统** — 颜色、间距、字重、阴影、渐变、响应式断点，极致还原苹果视觉语言
- **排版引擎** — 多语言字体栈（英文、简中、繁中、日文、韩文），自动回退至 Google Fonts
- **文案优化器** — 将普通文案转化为苹果风格的"果味"文案，简洁有力
- **配图策略** — 从 Unsplash/Pexels 推荐高质量免费图片，并提供 CSS 渐变替代方案
- **布局模式** — Hero 区块、产品展示网格、特性对比卡片、滚动动效区块

### 安装方式

#### OpenClaw（推荐）

```bash
# 通过 OpenClaw CLI 安装
openclaw install apple-design-skill
```

安装后，Skill 会被 OpenClaw 生态中的 AI 编码助手自动加载。

#### Claude Code

将本仓库中的 `CLAUDE.md` 文件复制到你的项目根目录。Claude Code 会自动将其作为自定义指令文件加载。

```bash
# 克隆并复制
git clone https://github.com/user/apple-design-skill.git
cp apple-design-skill/CLAUDE.md /path/to/your/project/CLAUDE.md
```

### 使用示例

安装 Skill 后，直接向 AI 编码助手描述你的需求即可：

**示例 1 — 产品落地页**

```
生成一个无线耳机的产品落地页，使用苹果设计风格。
```

**示例 2 — 特性介绍页**

```
创建一个智能手表的特性介绍页，展示 4 个核心功能，苹果风格。
```

**示例 3 — 定价页**

```
构建一个包含 3 个套餐的定价对比页面，使用苹果简洁的设计语言。
```

完整的 prompt 输入和 HTML/CSS 输出示例请参见 `examples/` 目录。

### 职责边界说明

本项目明确区分了 Skill 自身实现的功能、依赖 OpenClaw 平台的功能，以及依赖第三方服务的功能。

| 能力 | 实现方 |
|---|---|
| 设计令牌系统（颜色、间距、阴影等） | ✅ Skill 自身 |
| 排版引擎（字体栈、字号、字重） | ✅ Skill 自身 |
| 文案优化器（文案规则与模式） | ✅ Skill 自身 |
| 布局模式（Hero、网格、卡片、滚动） | ✅ Skill 自身 |
| 配图策略 — 选图规则与 CSS 回退方案 | ✅ Skill 自身 |
| 配图策略 — 图片搜索 API 调用（Unsplash/Pexels） | 🔌 可选扩展（第三方 API） |
| Skill 安装与分发 | 🏗️ OpenClaw 平台 |
| 版本管理 | 🏗️ OpenClaw 平台 |
| 依赖解析 | 🏗️ OpenClaw 平台 |
| 用户评价系统 | 🏗️ OpenClaw 平台 |

### 项目结构

```
apple-design-skill/
├── README.md                   # 本文件
├── LICENSE                     # MIT 许可证
├── CONTRIBUTING.md             # 贡献指南
├── CHANGELOG.md                # 变更日志
├── manifest.json               # OpenClaw Skill 元数据
├── CLAUDE.md                   # Claude Code 兼容入口
├── prompts/
│   ├── main.md                 # 核心入口 prompt
│   ├── design-tokens.md        # 设计令牌定义
│   ├── typography.md           # 多语言字体系统
│   ├── copywriting.md          # 文案优化规则
│   ├── image-curation.md       # 配图策略
│   └── layout-patterns.md      # 布局模式模板
└── examples/
    ├── product-landing/        # 产品落地页示例
    ├── feature-showcase/       # 特性介绍页示例
    └── pricing-page/           # 定价页示例
```

### 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。
