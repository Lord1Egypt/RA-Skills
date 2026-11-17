---
name: design-system-rules
description: 创建和维护设计系统的规则与规范，包含 Design Token 和组件文档
source:
  type: derived
  repo: skills-repo/figma-master
  path: skills/design-system-rules/SKILL.md
  url: https://skills.sh/figma/mcp-server-guide/figma-create-design-system-rules
  version: 1.0.0
  updated: 2026-07-31
metadata:
  author: hope
  category: Figma 设计
  platform: Web
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-31
tags:
  - design-system
  - figma
  - design-tokens
  - component-documentation
  - style-guide
---

# Design System Rules — 设计系统规范

> 为产品建立和维护设计系统规则，覆盖 Design Token 定义、组件规范编写、样式指南生成和团队协作流程。

## 能力

- **Design Token 体系**：定义颜色、字体、间距、圆角、阴影等基础 Token，支持多主题（亮色/暗色）
- **组件规范**：为每个组件编写使用规则、变体说明、状态定义和代码示例
- **样式指南**：生成品牌色彩板、字体层级、间距系统和图标库的完整文档
- **团队协作**：设计评审清单、版本管理策略和设计-开发交接规范

## 使用方式

在 Claude Code 中使用 `/design-system-rules` 调用。

```
/design-system-rules 帮我建立一套 Design Token 体系
/design-system-rules 为这个组件库编写使用规范
/design-system-rules 生成一份设计系统样式指南
/design-system-rules 审查当前设计系统的完整性
```

## 工作流

1. **审计现状** — 扫描现有产品的颜色、字体、组件使用情况，识别不一致
2. **定义 Token** — 建立基础 Token（色彩、字体、间距）和语义 Token（primary、danger、success）
3. **编写规范** — 为每个组件编写使用规则，包含 Do/Don't 示例
4. **输出指南** — 生成可分享的设计系统文档，支持 Markdown 或 Storybook 格式

## 适用场景

- 新项目启动前建立设计基础
- 现有产品设计债务清理和规范化
- 设计师与开发者之间的协作规范建立
- 开源项目的设计系统文档化

## 限制

- 不替代 Figma Libraries 或 Style Dictionary 等专业工具
- Token 命名规范需要团队协商确认，不能自动决策
- 大型设计系统的迁移需要分阶段进行
- 适合 1-10 人的小团队，企业级设计系统需额外工具支持

## 相关参考（Playbook）

- [references/design-token-strategy.md](../../references/design-token-strategy.md) — 三层 Token 模型、命名分类法、暗色主题与迁移的架构决策（本子技能"定义 Token"步骤的深度依据）
- [references/design-review-checklist.md](../../references/design-review-checklist.md) — 一致性扫描命令可直接核查本子技能产出的 Token 是否被正确引用（无硬编码色值）
- 路线：规范定义（本子技能）→ Token 架构决策（[design-token-strategy.md](../../references/design-token-strategy.md)）→ 组件生成（[figma-component-library](../figma-component-library/SKILL.md)）