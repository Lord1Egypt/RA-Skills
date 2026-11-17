# Figma Master — Agent 入口

> 本仓库是 skills-repo 组织下的 Figma 设计工具技能库。面向独立开发者和小团队，覆盖组件库生成、设计系统规范、线框图原型和 UI/UX 设计审查，帮你用 Figma 高效完成产品设计。采用 skills-repo 组织的 **superpower 架构**。

## 目录约定（superpower）

```
figma-master/
├── SKILL.md                       # L1 路由层：唯一入口，只做索引
├── references/                    # L2 深层 playbook
│   ├── design-token-strategy.md
│   ├── component-library-playbook.md
│   └── design-review-checklist.md
├── skills/                        # L3 细粒度子技能
│   ├── design-system-rules/SKILL.md
│   ├── figma-component-library/SKILL.md
│   ├── ui-ux-designer/SKILL.md
│   └── wireframe-prototyping/SKILL.md
├── scripts/                       # L4 确定性脚本：lint_design_tokens.py
├── assets/                        # L5 模板资源：token_rules.json 等
├── AGENTS.md / README.md / LICENSE / .gitignore
```

## 加载顺序（渐进式加载）

1. 先读 `SKILL.md` 路由表，判断任务属于哪一类。
2. **方法论决策**（Token 策略 / 组件库落地 / 设计评审）→ 读 `references/` 对应 playbook。
3. **落地具体动作**（建规范 / 生成组件 / 审查 / 线框）→ 调 `skills/<name>/SKILL.md`。
4. **确定性自检**（Token/变体命名）→ 跑 [scripts/lint_design_tokens.py](scripts/lint_design_tokens.py)。
5. 套用 `assets/` 模板，不重复造轮子。

## 技能清单

| 环节 | 技能 | 文件 | 用途 |
|------|------|------|------|
| 组件 | figma-component-library | [skills/figma-component-library/SKILL.md](skills/figma-component-library/SKILL.md) | 从 Figma 设计稿生成前端组件代码库 |
| 规范 | design-system-rules | [skills/design-system-rules/SKILL.md](skills/design-system-rules/SKILL.md) | 创建和维护设计系统的规则与规范 |
| 原型 | wireframe-prototyping | [skills/wireframe-prototyping/SKILL.md](skills/wireframe-prototyping/SKILL.md) | 快速线框图与交互原型设计 |
| 审查 | ui-ux-designer | [skills/ui-ux-designer/SKILL.md](skills/ui-ux-designer/SKILL.md) | UI/UX 设计审查与改进建议 |

## 使用场景

- 独立开发者快速将设计稿转化为前端代码
- 小团队建立和维护设计系统规范
- 产品早期阶段的线框图和原型验证
- 设计评审和 UI/UX 改进

## 相关仓库

- `design-studio` — UI/UX 设计原则（设计系统、UI审查、无障碍），本仓库聚焦 Figma 工具实操
- `visual-designer` — 视觉资产创作（排版、插画、海报、品牌），本仓库聚焦设计工具链
- `frontend-engineer` — 前端组件开发，本仓库产出设计稿到代码的桥梁

> 本仓库聚焦 **Figma 设计工具链的实操技能**，与 design-studio 的设计原则和 visual-designer 的视觉创作互补。
