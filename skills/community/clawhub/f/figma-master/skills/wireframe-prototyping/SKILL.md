---
name: wireframe-prototyping
description: 快速线框图与交互原型设计，从草图到可点击原型
source:
  type: derived
  repo: skills-repo/figma-master
  path: skills/wireframe-prototyping/SKILL.md
  url: https://skills.sh/aj-geddes/useful-ai-prompts/wireframe-prototyping
  version: 1.0.0
  updated: 2026-07-31
metadata:
  author: hope
  category: Figma 设计
  platform: Web
  difficulty: 入门
  version: 1.0.0
  created: 2026-07-31
tags:
  - wireframe
  - prototyping
  - figma
  - ux-design
  - rapid-prototyping
---

# Wireframe Prototyping — 线框图与原型设计

> 从想法到可交互原型的快速通道。覆盖低保真线框图、中保真原型、交互流程设计和用户测试准备。

## 能力

- **快速线框图**：将文字需求转化为结构化页面线框图，定义信息架构和布局骨架
- **交互原型**：添加页面跳转、hover 状态、弹窗等交互，生成可点击原型
- **用户流程**：梳理关键用户路径，绘制流程图和页面流转关系
- **测试准备**：为可用性测试准备原型任务和观察要点

## 使用方式

在 Claude Code 中使用 `/wireframe-prototyping` 调用。

```
/wireframe-prototyping 为这个 SaaS 产品的注册流程设计线框图
/wireframe-prototyping 把登录流程做成可点击原型
/wireframe-prototyping 梳理电商购物车到支付完成的用户流程
```

## 工作流

1. **需求分析** — 明确页面目标、目标用户和核心任务
2. **信息架构** — 确定页面元素优先级和布局骨架
3. **线框图绘制** — 输出低保真线框图，聚焦结构和流程而非视觉
4. **交互设计** — 添加页面跳转和微交互，生成可点击原型
5. **测试迭代** — 准备可用性测试脚本，根据反馈迭代

## 适用场景

- 产品早期阶段的功能验证和方向探索
- 与利益相关者沟通产品方案时快速可视化
- 可用性测试前的原型准备
- 独立开发者验证产品想法

## 限制

- 不产出高保真视觉设计（需要后续由视觉设计师完成）
- 原型交互逻辑为演示级别，不包含真实数据处理
- 复杂动画和微交互需额外工具支持
- 适合快速验证而非像素级交付

## 相关参考（Playbook）

- [references/component-library-playbook.md](../../references/component-library-playbook.md) — 线框确定后，从设计稿到组件库的边界 / 变体命名 / 属性映射决策（下游落地依据）
- [references/design-review-checklist.md](../../references/design-review-checklist.md) — 进入高保真前的可量化评审清单，提前暴露可用性与一致性问题
- 路线：线框与原型（本子技能）→ 组件生成（[figma-component-library](../figma-component-library/SKILL.md) + [component-library-playbook.md](../../references/component-library-playbook.md)）→ 评审（[ui-ux-designer](../ui-ux-designer/SKILL.md) + [design-review-checklist.md](../../references/design-review-checklist.md)）