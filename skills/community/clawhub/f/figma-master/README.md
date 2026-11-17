# Figma Master — Figma 设计工具技能库

> 面向独立开发者和小团队的 Figma 设计工具技能集合。覆盖组件库生成、设计系统规范、线框图原型和 UI/UX 设计审查。

## 架构说明（superpower）

本仓库采用 skills-repo 组织的 **superpower 架构**：

- `SKILL.md` — 唯一入口，只做能力路由（本文件）
- `references/` — 深层 playbook：Design Token 策略、组件库落地、设计评审检查清单
- `skills/` — 4 个细粒度子技能，可单独安装
- `scripts/` — `lint_design_tokens.py` 设计系统规范自检（纯标准库、可复现）
- `assets/` — 命名规则配置、合规 Token 示例、设计系统规范模板

渐进式加载：Agent 先读路由表，按需读取 `references/` 或 `skills/`，重复任务交给脚本。

## 技能清单

| 技能 | 描述 | 安装量 | 来源 |
|------|------|--------|------|
| figma-component-library | 从 Figma 设计稿生成前端组件代码库，支持 React/Vue 组件输出 | 2.8K | [skills.sh](https://skills.sh/figma/mcp-server-guide/figma-generate-library) |
| design-system-rules | 创建和维护设计系统的规则与规范，包含 Design Token 和组件文档 | 1.7K | [skills.sh](https://skills.sh/figma/mcp-server-guide/figma-create-design-system-rules) |
| wireframe-prototyping | 快速线框图与交互原型设计，从草图到可点击原型 | 1.3K | [skills.sh](https://skills.sh/aj-geddes/useful-ai-prompts/wireframe-prototyping) |
| ui-ux-designer | UI/UX 设计审查与改进建议，覆盖可用性、视觉一致性和交互流程 | 2.5K | [skills.sh](https://skills.sh/sickn33/antigravity-awesome-skills/ui-ux-designer) |

## 工作流

```
设计系统规范 ──→ 组件库生成
(design-system-rules)   (figma-component-library)
        │
        ├──→ 线框图原型
        │    (wireframe-prototyping)
        │
        └──→ UI/UX 审查
             (ui-ux-designer)
```

## 安装

```bash
# 安装全部 Figma 设计技能
npx skills add skills-repo/figma-master -g -y

# 或按需安装单个技能
npx skills add skills-repo/figma-master@figma-component-library -g -y
npx skills add skills-repo/figma-master@design-system-rules -g -y
npx skills add skills-repo/figma-master@wireframe-prototyping -g -y
npx skills add skills-repo/figma-master@ui-ux-designer -g -y
```

## 与本组织其他仓库的关系

- **design-studio** — UI/UX 设计原则，本仓库聚焦 Figma 工具实操
- **visual-designer** — 视觉资产创作，本仓库聚焦设计工具链
- **frontend-engineer** — 前端组件开发，本仓库产出设计到代码的桥梁
