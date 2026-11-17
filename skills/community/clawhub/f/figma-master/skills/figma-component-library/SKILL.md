---
name: figma-component-library
description: 从 Figma 设计稿生成前端组件代码库，支持 React/Vue 组件输出
source:
  type: derived
  repo: skills-repo/figma-master
  path: skills/figma-component-library/SKILL.md
  url: https://skills.sh/figma/mcp-server-guide/figma-generate-library
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
  - figma
  - component-library
  - design-to-code
  - react
  - vue
---

# Figma Component Library — 组件库生成

> 从 Figma 设计稿自动提取组件信息，生成结构化的前端组件代码库。覆盖组件识别、属性提取、代码生成和文档输出。

## 能力

- **组件识别**：自动解析 Figma 设计稿中的 Component 和 Instance，识别组件层级和变体
- **属性提取**：提取颜色、字体、间距、圆角等 Design Token，生成 CSS 变量或 Tailwind 配置
- **代码生成**：输出 React/Vue 组件骨架代码，包含 props 类型定义和基础样式
- **文档输出**：生成组件文档（Storybook 格式），包含使用示例和属性说明

## 使用方式

在 Claude Code 中使用 `/figma-component-library` 调用。

```
/figma-component-library 从这个 Figma 链接生成组件库
/figma-component-library 提取设计稿中的 Design Token
/figma-component-library 生成 Button 组件的 React 代码和 Storybook 文档
```

## 工作流

1. **连接设计稿** — 提供 Figma 文件链接或选中节点，读取组件结构
2. **提取 Token** — 解析颜色、字体、间距、阴影等设计变量，输出标准化 Token
3. **生成组件** — 为每个 Figma Component 生成对应的前端组件代码
4. **输出文档** — 生成组件使用说明和 Storybook stories

## 适用场景

- 设计稿交付后快速生成前端组件库
- 设计系统从 Figma 到代码的自动化同步
- 新项目启动时搭建组件基础设施
- 跨团队统一组件开发规范

## 限制

- 仅支持 Figma 中的 Component/ComponentSet，不支持 Group/Frame 自动转换
- 复杂交互逻辑（如动画、状态管理）需手动补充
- 代码生成基于模板，可能需要根据项目规范调整
- 需要 Figma 文件访问权限（个人/团队计划均可）

## 相关参考（Playbook）

- [references/component-library-playbook.md](../../references/component-library-playbook.md) — 生成前的组件边界 / 变体命名 / 属性映射决策与生成后去重验收（本子技能"生成组件"步骤的深度依据）
- [references/design-token-strategy.md](../../references/design-token-strategy.md) — 提取的 Token 必须符合三层命名规范，生成的样式不得出现裸 hex / 裸 px
- 路线：线框（[wireframe-prototyping](../wireframe-prototyping/SKILL.md)）→ 组件规划与生成（本子技能 + [component-library-playbook.md](../../references/component-library-playbook.md)）→ 评审（[ui-ux-designer](../ui-ux-designer/SKILL.md) + [design-review-checklist.md](../../references/design-review-checklist.md)）