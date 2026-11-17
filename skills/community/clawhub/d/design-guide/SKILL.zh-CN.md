---
name: design-guide
description: 面向 Codex、Claude Code、Cursor、Qwen Code 等 AIDE 的前端设计与生产工程总控 skill。英文版 SKILL.md 是规范源文件；本文件提供中文操作入口。
---

# design-guide（中文操作入口）

`SKILL.md` 是规范源文件。本文件用于中文用户快速理解和使用；涉及规则细节时，以英文规范与 `references/` 为准，避免中英文行为分叉。

## 何时使用

当用户要求前端设计、页面开发、后台工作台、仪表盘、重设计、截图还原、响应式 UI、动效、3D、截图 QA，或评价已有页面的优缺点和改进方案时，使用 `design-guide`。

没有具体任务时进入导航模式：列出当前环境可执行的前端任务和可用辅助 skill，不写代码。

## 评审已有页面

用户只给 URL、图片或 HTML 并要求评估时，先执行 Scope Gate：

```text
Review scope: <用户明确要求的范围>
Not included by default: <未提及的移动端、无障碍、重设计、实现、发布等>
```

默认只评估单页桌面视图、视觉层级、基本任务流、完成度和明显可用性问题。除非用户明确要求，不继承历史对话中的移动端、公众号、发布或实现目标。

每个高优先级问题都要附带产物、视口、位置、观察、影响和置信度，并给出可落地改法、取舍、验收标准和验证步骤。

## 设计深度

- Level 0：孤立的小修复，沿用现有契约。
- Level 1：已有结构上的定向设计，先给简要设计说明。
- Level 2：新产品、主要流程变化或方向不确定时，先产出可查看的 HTML、截图或参考板。

Level 2 必须让用户立即看到产物，等待用户确认、选择方向或提出修改，再进入实现。确认后创建并校验设计契约，不得在等待确认时继续编码。

## 实现与验证

实现前读取项目情报、状态/数据契约和适用的框架适配。较大实现应覆盖加载、空、错误、权限、成功、回退和撤销状态。

交付前使用 HTTP 预览和 `verify-ui.py` 检查声明的流程、断点、控制台错误、水平溢出、可访问性、视觉差异和性能预算。

## CLI 语言

CLI 支持 `en` 与 `zh-CN`：

```bash
python3 scripts/present-design.py --locale zh-CN --help
F_DESIGN_LOCALE=zh-CN python3 scripts/design-guide-doctor.py
```

语言优先级为显式 `--locale`、`F_DESIGN_LOCALE`、`LC_ALL`、`LANG`、英文回退。JSON 字段和机器值始终保持英文稳定。

完整规则见：

- `SKILL.md`
- `references/internationalization.md`
- `references/product-design-review.md`
- `references/design-process.md`
- `references/artifact-presentation.md`
- `references/quality-gates.md`
