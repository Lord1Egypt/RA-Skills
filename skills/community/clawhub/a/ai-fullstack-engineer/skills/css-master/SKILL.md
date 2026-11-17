---
name: css-master
description: Tailwind CSS 高级布局：Grid 模板、容器查询、Flexbox 模式、响应式方案
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/css-master/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/josiahsiegel/claude-plugin-marketplace/tailwindcss-advanced-layouts
metadata:
  category: CSS
  platform: Web
  difficulty: 入门
---

# Tailwind CSS 高级布局

> Tailwind CSS 高级布局技术：CSS Grid、Flexbox、容器查询、响应式模式。适用于复杂页面布局。

## 能力

- **CSS Grid 布局**：grid-template-areas、grid-cols 响应式、subgrid、minmax/auto-fit
- **Flexbox 模式**：flex-1/flex-grow/gap 空间分配、居中对齐方案
- **圣杯布局**：header + 多栏 + footer 经典布局的 Grid 和 Flexbox 实现
- **容器查询**：@container + Tailwind 插件实现组件级响应式
- **响应式模式**：移动优先断点策略、aspect-ratio 工具、多栏杂志布局

## 使用方式

```
/css-master 帮我实现一个响应式圣杯布局
/css-master 这个卡片网格需要自适应列数，帮我用 Grid 写
/css-master 把这个布局从 Flexbox 改成 CSS Grid
```

## 工作流

1. 描述页面布局需求（栏数、响应式断点、特殊区域）
2. AI 选择 Grid 或 Flexbox 方案
3. 实现核心布局结构
4. 添加响应式断点（移动优先）
5. 验证跨浏览器兼容性

## 适用场景

- 复杂多栏页面布局
- 响应式设计从零搭建
- 现有布局重构优化
- 学习 Tailwind CSS Grid/Flexbox 模式

## 限制

- 仅覆盖 Tailwind CSS 布局，不涉及原生 CSS
- 不涉及 CSS-in-JS 方案
- 不涉及 CSS 动画（归属 motion-design）
- 浏览器兼容性需用户自行测试

## 相关参考（Playbook）

本子技能落地"Tailwind / CSS 高级布局"，相关方法论见下列 `references/`（按需读取）：

- 前端深度 playbook（CSS / Grid / 响应式 / 踩坑）：[references/frontend-playbook.md](../../references/frontend-playbook.md)
- Tailwind CSS 审计 playbook（purge / 配置漂移 / 冲突类名 / v3→v4 迁移）：[references/tailwind-audit-playbook.md](../../references/tailwind-audit-playbook.md)