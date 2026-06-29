---
name: design-systems-index
description: >-
  External-link index of major companies' design systems (Material, Fluent, Carbon, Polaris, Atlassian, Lightning), design-token tools and specs, pattern-library tooling, and React/React Native design-system component libraries. Use this skill whenever the user wants to reference or adopt an existing design system, study a company's DS, look up design-token tooling, or evaluate React/RN component libraries — consult this before web-searching. Token-architecture methodology lives in the separate design-system skill; this is the link index only.
---

# 设计系统外部链接索引

各公司 / 社区公开设计系统的外部链接导航索引，用于参考现成 DS 的设计令牌、组件与规范。

> ⚠️ 本 skill 是**资源索引层**：只收录链接与一句简介，不展开方法论。Token 架构、命名分层、跨平台落地的方法论见本地 `design-system` skill——两个 skill 各司其职，此处不重复。

## 如何使用（progressive disclosure）

本 SKILL.md 是**调度索引层**：5 个分类各列 2-3 条最经典条目，附"是什么 / 何时去读"。需要更长清单时，按指引读取对应 `references/<category>.md`（一层深，不再嵌套）。

先根据下方分类判断你要的是哪一类，再按需读对应 reference，避免一次性加载全部。

数据来源：[klaufel/awesome-design-systems](https://github.com/klaufel/awesome-design-systems) + [jbranchaud/awesome-react-design-systems](https://github.com/jbranchaud/awesome-react-design-systems)。

触发示例：`参考各大公司设计系统` / `找一份 React 组件库选型` / `design tokens 工具和规范` / `挑一个 pattern library 工具`。

## 分类速查（先定位再下钻）

判断不清晰时先查这张表，再去对应文件下钻，避免把 5 份全读一遍：

| 你的诉求 | 去读 |
|---|---|
| 参考某家大公司的成熟 DS | `references/major-company-systems.md` |
| 选 design tokens 工具链 / 对齐 W3C 规范 | `references/design-tokens.md` |
| 搭组件开发环境、文档站、pattern library | `references/pattern-libraries.md` |
| 为 React Web 项目选可采用的组件库 | `references/react-ds-libraries.md` |
| 为 React Native 项目选 UI 工具包 | `references/react-native-ds-libraries.md` |

> 边界提示：想"怎么设计 token 架构"不在本索引，去本地 `design-system` skill；想"怎么用 React 写组件"去 `react-best-practices`，本索引只回答"有哪些现成 DS/库可参考或采用"。

## 路由示例（progressive disclosure 怎么走）

> 用户："帮我给企业后台选个 React 组件库"
> 1. 定位分类 → 这是"React 设计系统库"类，不是 tokens / pattern library。
> 2. 先看下文该类精选（Ant Design / MUI / Blueprint），多数情况已够回答。
> 3. 要更多候选 → 读 `references/react-ds-libraries.md`；仍不够 → 跳 awesome 原目录。
> 4. 选定后，落地实现细节交给 `react-best-practices` / `frontend-design`，不在本索引展开。

---

## 主要公司设计系统

**是什么**：各大公司公开的完整设计系统（令牌 + 组件 + 规范 + 文档）。
**何时去读**：要参考某家公司的 DS、挑选可借鉴的成熟体系、做设计语言竞品调研时。

精选（最经典）：
- [Google Material Design](https://material.io/design) - Google's design system for intuitive, beautiful products.
- [Microsoft Fluent UI](https://fluentui.microsoft.com/) - Microsoft's open-source cross-platform design system (web/Apple/Android).
- [IBM Carbon](https://www.carbondesignsystem.com/) - IBM's open-source design system for products and experiences.

→ 完整列表见 `references/major-company-systems.md`（Polaris、Atlassian、Lightning、Primer、Pajamas、Photon、Atlaskit + 通用 DS 资源）。

## 设计 tokens 资源

**是什么**：design tokens 的规范、生成、转换与跨平台同步工具。
**何时去读**：要选 token 工具链、对齐 W3C 规范、从 Figma 抽取 token、做多端 token 分发时。

精选：
- [Design Tokens W3C Community Group](https://www.w3.org/community/design-tokens/) - W3C community group defining a design tokens format spec.
- [Style Dictionary](https://github.com/amzn/style-dictionary) - Amazon's build system to define styles once and use them on any platform.
- [Theo](https://github.com/salesforce-ux/theo) - Salesforce's abstraction for transforming and formatting design tokens.

→ 完整列表见 `references/design-tokens.md`（DesignTokens.dev、Diez、Figmagic、Superposition、Validator、Awesome Design Tokens、Abstract Connect、Zeplin export 等）。

## pattern library 资源

**是什么**：组件隔离开发环境与模式库编排工具（Storybook 类）。
**何时去读**：要搭组件开发环境 / 文档站 / 原子设计工作流、选文档协作平台时。

精选：
- [Storybook](https://storybook.js.org/) - Build UI components in isolation for React, Vue, Angular and more.
- [Pattern Lab](https://patternlab.io/) - Build pattern-driven UIs using atomic design principles.
- [React Styleguidist](https://react-styleguidist.js.org/) - Isolated React component dev environment with a living style guide.

→ 完整列表见 `references/pattern-libraries.md`（Styled System、Stencil、Zeroheight、Backlight、Storybook DS、addons 清单等）。

## React 设计系统库

**是什么**：可直接采用的 React 组件库 / 企业级设计系统，开箱即用。
**何时去读**：为 SaaS / 后台 / dashboard 选 React 组件库、评估企业级 DS 采用方案时。

精选：
- [Ant Design](https://ant.design/) - Ant Financial - design system for enterprise applications (Nature & Determinacy).
- [Material UI](https://mui.com/) - React components that implement Google's Material Design.
- [Blueprint](http://blueprintjs.com/) - Palantir - React-based UI toolkit for the web.

→ 完整列表见 `references/react-ds-libraries.md`（Grommet、Garden、Backpack、Ring UI、Canvas、Atlaskit、cf-ui、Mineral UI、Spark、Swarm、Uniform、Lightning React 等 20+）。

## React Native 设计系统库

**是什么**：React Native 跨平台开箱即用 UI 工具包。
**何时去读**：为 RN App 选成型组件库、避免从零搭 UI 时。

精选：
- [React Native Elements](https://reactnativeelements.com/) - Cross-platform React Native UI toolkit.
- [React Native Paper](https://reactnativepaper.com/) - Material Design-compliant React Native components.
- [NativeBase](https://nativebase.io/) - GeekyAnts - essential cross-platform UI components for React Native & Vue Native.

→ 完整列表见 `references/react-native-ds-libraries.md`（Shoutem UI、Teaset 等）。

---

## awesome 总目录指针

更全的 awesome 设计相关总目录见 [sindresorhus/awesome](https://github.com/sindresorhus/awesome)。本 skill 主要从以下两份精炼：

- [klaufel/awesome-design-systems](https://github.com/klaufel/awesome-design-systems) — 主要公司 DS / tokens / pattern library 的母目录。
- [jbranchaud/awesome-react-design-systems](https://github.com/jbranchaud/awesome-react-design-systems) — React / RN DS 库的母目录。

## 相关本地 skill

本索引只负责"有哪些现成 DS 可参考 / 采用"，方法论与实现细节交给下列本地 skill：

- `design-system` — token 架构、命名分层、跨平台落地方法论（本索引的方法论后端）。
- `react-native-skills` — React Native 组件与样式模式。
- `react-best-practices` / `frontend-design` — React 与前端实现、设计落地细节。
- `design-assets-index` — 设计资源（图标、字体、插画等）索引。
