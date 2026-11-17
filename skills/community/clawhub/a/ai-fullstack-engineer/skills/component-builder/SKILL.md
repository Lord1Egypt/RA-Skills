---
name: component-builder
description: 现代 Web 开发最佳实践指南：HTML/CSS/JS 模式、API 使用、框架适配
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/component-builder/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/googlechrome/modern-web-guidance/modern-web-guidance
metadata:
  category: 综合
  platform: Web
  difficulty: 入门
---

# 现代 Web 开发指南

> 现代 Web 开发最佳实践搜索工具。Web API 快速演进，训练数据中的模式可能已过时——构建前先搜索最新实践。

## 能力

- **UI/布局**：Modal/Dialog/Popover 新模式、anchor positioning、container queries、`:has()` 选择器
- **滚动与动效**：View Transitions API、Scroll-driven animations、滚动视差
- **性能**：Core Web Vitals、content-visibility、Fetch Priority、图片优化
- **系统 API**：本地文件访问、WebUSB、WebSocket 同步、WebAssembly
- **框架适配**：React/Vue/Angular 中的布局和样式最佳实践
- **表单**：自动填充、高级输入类型、自定义滚动条、组件状态

## 使用方式

```
/component-builder 实现一个符合最新标准的 Modal 组件
/component-builder 这个表单的自动填充怎么处理？
/component-builder 在 React 中实现 View Transitions
```

## 工作流

1. 描述要实现的 Web 功能
2. 运行 `npx -y modern-web-guidance search "<query>"` 搜索最佳实践
3. 根据搜索结果选择标准化模式
4. 实现时优先使用原生 Web API，避免不必要的大依赖
5. 验证跨浏览器兼容性

## 适用场景

- 实现新 UI 组件前查找标准模式
- 学习现代 Web API 用法
- 避免使用过时或即将废弃的模式
- 框架中的 Web 平台特性适配

## 限制

- 不涉及后端开发
- 不涉及 CI/CD 和部署
- 搜索结果需要人工判断适用性

## 相关参考（Playbook）

本子技能落地"现代 Web 组件与模式"，前端方法论见下列 `references/`（按需读取）：

- 前端深度 playbook（组件 / 响应式 / 性能 / 踩坑速查）：[references/frontend-playbook.md](../../references/frontend-playbook.md)