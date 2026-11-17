# AGENTS.md

## 仓库性质

`accessibility-engineer` 是一个 **单一、完整的无障碍工程技能包**，采用 Superpowers 架构（薄 SKILL.md + 按需加载的 references + 确定性 scripts + assets 模板）。

它把"让界面盲用也好用"做成可交付的工程标准，覆盖 WCAG 合规模型、语义标记、键盘焦点、读屏实测与审计修复。

## 目录约定

```
accessibility-engineer/
├── SKILL.md          # 入口：frontmatter(name/description/agent_created) + 路由与原则
├── README.md         # 人类可读的介绍与快速开始
├── AGENTS.md         # 本文件
├── references/       # 完整 playbook，按需由 SKILL.md 路由加载
│   └── <topic>.md
├── scripts/          # 确定性、可重复执行的脚本（纯 stdlib，无外部依赖）
│   └── *.py
├── skills/           # 可单独安装的细粒度子技能（每个含 source 字段）
│   └── <name>/SKILL.md
└── assets/           # 输出用模板与清单（不进上下文）
    └── *
```

## SKILL.md 格式

```markdown
---
name: accessibility-engineer
description: <第三人称触发描述，决定何时被调用>
agent_created: true
metadata:
  version: <语义化版本>
  category: 无障碍工程
  difficulty: 进阶
  architecture: superpower
---

# Accessibility Engineer
> <一句话简介>
## 何时使用
## 能力索引（路由到 references/ 与 skills/）
## 内置脚本
## 模板资源
## 核心原则
```

## 工作约定

- 所有内容用中文编写（技术术语保留英文）。
- SKILL.md 保持「薄」：只做路由与原则，详细流程放 `references/`。
- `references/` 中每个文件是**自包含 playbook**：能力、何时用、工作流、示例、限制。
- `scripts/` 只放确定性、可重复的任务脚本（纯标准库，必须支持 `--help`/`--json`/`--strict`）。
- `assets/` 放清单/模板，不依赖上下文加载。
- 新增主题：在 `references/` 加 `<topic>.md`，并在 SKILL.md 路由表与 README 同步登记（路由索引完整性）。

## 不做什么

- 不替代法律合规结论（只给技术对齐路径，法条以官方文本为准）。
- 不把"页面能通过自动化审计"等同于"盲用好用"——读屏实测是必需的人工层。
- 不维护与具体 SaaS 强绑定的私有工具链（保持框架中立）。
