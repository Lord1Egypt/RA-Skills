---
name: ui-ux-designer
description: UI/UX 设计审查与改进建议，覆盖可用性、视觉一致性和交互流程
source:
  type: derived
  repo: skills-repo/figma-master
  path: skills/ui-ux-designer/SKILL.md
  url: https://skills.sh/sickn33/antigravity-awesome-skills/ui-ux-designer
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
  - ui-design
  - ux-design
  - design-review
  - usability
  - accessibility
---

# UI/UX Designer — 设计审查与改进

> 对产品界面进行系统化的 UI/UX 审查，发现可用性问题、视觉不一致和交互流程改进点，输出可执行的改进建议。

## 能力

- **可用性审查**：基于 Nielsen 十大可用性原则，评估界面易用性和用户效率
- **视觉一致性**：检查颜色、字体、间距、组件样式是否统一，识别设计债务
- **交互流程**：分析用户路径，发现流程断点、冗余步骤和认知负担
- **无障碍检查**：评估颜色对比度、焦点顺序、语义标签等无障碍要素
- **改进建议**：输出优先级排序的改进清单，包含具体方案和预期效果

## 使用方式

在 Claude Code 中使用 `/ui-ux-designer` 调用。

```
/ui-ux-designer 审查这个页面设计的可用性问题
/ui-ux-designer 检查整个产品的视觉一致性
/ui-ux-designer 分析用户注册流程，找出流失点
/ui-ux-designer 对这套设计做无障碍审查
```

## 工作流

1. **确定范围** — 明确审查的页面/流程范围和评估维度
2. **启发式评估** — 逐项检查可用性原则、视觉规范、交互逻辑
3. **问题记录** — 截图标注问题位置，描述严重程度和影响范围
4. **改进方案** — 为每个问题提供具体的设计建议和参考示例
5. **优先级排序** — 按影响×成本矩阵排列改进优先级

## 适用场景

- 产品上线前的设计质量把关
- 设计改版前后的对比审查
- 用户反馈问题后的设计诊断
- 独立开发者自查产品设计质量

## 限制

- 无法替代真实用户测试（可以补充但不能取代）
- 审查基于通用设计原则，具体行业规范需额外补充
- 复杂交互（如拖拽、手势）需实际操作验证
- 建议需要结合产品上下文和业务目标判断优先级

## 相关参考（Playbook）

- [references/design-review-checklist.md](../../references/design-review-checklist.md) — 把本子技能的启发式评估升级为可勾选 / 可量化 / 可复现的评审清单与对比度公式（本子技能"启发式评估"步骤的深度依据）
- [references/design-token-strategy.md](../../references/design-token-strategy.md) — 一致性 / 对比度问题常源于 Token 规范缺失，根治见三层 Token 化
- 路线：审查（本子技能）→ 量化评审清单（[design-review-checklist.md](../../references/design-review-checklist.md)）→ 规范修正（[design-system-rules](../design-system-rules/SKILL.md)）