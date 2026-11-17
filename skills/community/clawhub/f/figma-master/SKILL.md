---
name: figma-master
description: >-
  把 AI 变成 Figma 设计搭档：从设计系统规范、组件库生成到 UI/UX 审查与线框原型。
  覆盖 Design Token 三层策略、组件变体命名 lint、设计评审检查清单。
  触发词："Figma 设计系统"、"Design Token"、"组件库生成"、"设计评审"、"线框图"、"变体命名"。
agent_created: true
metadata:
  version: 1.0.0
  category: Figma 设计
  difficulty: 进阶
  architecture: superpower
---

# Figma 设计大师

> 让 AI 帮你把 Figma 设计稿变成有规范、可维护、能落地代码的设计资产。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放 `references/` 按需加载，
细粒度能力放 `skills/` 子技能，确定性 lint 交给 `scripts/`，规范模板放 `assets/`。

## 何时使用

- 要建立或清理一套 Design Token / 设计系统规范
- 从 Figma 设计稿生成前端组件代码库，需要命名与属性规范
- 做 UI/UX 设计评审，需要可量化、可复现的检查清单
- 需要快速产出线框图或可点击原型
- 要校验 Token 命名、组件变体命名是否合规

## 能力索引（超级技能路由）

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| Design Token 三层策略、命名分类、暗色主题 | [references/design-token-strategy.md](references/design-token-strategy.md) | design token 命名 分层 primitive semantic 暗色 分类 |
| 组件库落地：规划/变体命名/属性映射/去重 | [references/component-library-playbook.md](references/component-library-playbook.md) | 组件库 变体 1:1 映射 props Token 去重 |
| 设计评审检查清单（对比度/一致性/a11y） | [references/design-review-checklist.md](references/design-review-checklist.md) | 设计评审 Nielsen 对比度 一致性 无障碍 a11y 检查 |
| 设计系统规则与 Token 文档编写 | [skills/design-system-rules/SKILL.md](skills/design-system-rules/SKILL.md) | design system token 规范 样式指南 组件文档 |
| Figma 设计稿 → 前端组件代码库 | [skills/figma-component-library/SKILL.md](skills/figma-component-library/SKILL.md) | figma 组件库 设计到代码 React Vue storybook |
| UI/UX 设计审查与改进建议 | [skills/ui-ux-designer/SKILL.md](skills/ui-ux-designer/SKILL.md) | UI UX 审查 可用性 视觉一致性 无障碍 |
| 线框图与可点击原型设计 | [skills/wireframe-prototyping/SKILL.md](skills/wireframe-prototyping/SKILL.md) | 线框图 原型 信息架构 用户流程 测试 |

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，把设计系统规范变成可复现的机器检查：

- `scripts/lint_design_tokens.py tokens --file <tokens.json>` — 校验 Token 命名/分类/$type
- `scripts/lint_design_tokens.py variants --file <variants.txt>` — 校验组件变体命名
- `scripts/lint_design_tokens.py selfcheck` — 校验内置资产（规则+示例）0 ERROR

运行示例：

```bash
python3 scripts/lint_design_tokens.py tokens --file tokens.json
```

## 模板资源

`assets/` 提供可直接套用的规范与模板：

- [assets/token_rules.json](assets/token_rules.json) — 命名/分类规则（脚本 `tokens`/`variants` 的规则来源，可自定义）
- [assets/design_tokens.example.json](assets/design_tokens.example.json) — 合规 Token 示例（脚本 selfcheck 回检 0 ERROR）
- [assets/design-system-spec-template.md](assets/design-system-spec-template.md) — 设计系统规范文档模板

## 核心原则（始终遵循）

1. **三层 Token 解耦**：组件只引用 Semantic 层，暗色主题只覆盖 Semantic 绑定。
2. **命名即契约**：Token/变体命名走受控分类与 kebab，用脚本 lint 而非凭记忆。
3. **不为 1:1 买单**：先抽原子组件再组合，避免整页成组件、重复生成。
4. **渐进式加载**：先读路由表与对应 `references/`，再动手。
5. **明确边界**：脚本只做规范自检、出报告，不替你拍板设计决策、不改你的源文件。
6. **证据驱动评审**：对比度用公式算，一致性用扫描命令查，不靠肉眼。

## 与其他技能协作

- 组件代码落库后的工程化 → `skills-repo/frontend-engineer`
- 视觉资产与品牌创作 → `skills-repo/visual-designer`
- 设计原则与 UI 审查理论 → `skills-repo/design-studio`
