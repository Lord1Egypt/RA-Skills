---
name: accessibility-engineer
description: >-
  无障碍工程技能库：让 AI 编程助手交付可达的 Web 界面——覆盖 WCAG 2.2 合规模型、语义化
  HTML 与 ARIA、键盘可达与焦点管理、读屏器实测、静态审计与修复工作流，并内置对比度计算、
  HTML 静态审计、ARIA 校验三套确定性脚本。尤其针对 AI 生成代码最常见的盲区（缺 alt、缺
  label、缺语义、对比度不达标）。触发词："无障碍"、"可访问性"、"a11y"、"WCAG"、"对比度"、
  "ARIA"、"读屏"、"alt 文本"、"键盘可达"、"焦点管理"、"无障碍审计"、"EAA"、"ADA"。
agent_created: true
metadata:
  version: 1.0.0
  category: 无障碍工程
  difficulty: 进阶
  architecture: superpower
---

# 无障碍工程师 (Accessibility Engineer)

> 把 AI 编程助手变成一名能让界面"盲用也好用"的无障碍工程搭档：从合规判据、语义标记、键盘焦点，到读屏实测与审计修复，把可达性做成可交付的工程标准。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

- 需要让页面/组件**符合 WCAG 2.2 AA**（或应对 EAA / ADA 合规要求）
- 写交互组件不确定该用**语义标签还是 ARIA**
- 自定义弹窗/菜单/标签页**键盘进不去或焦点丢失**
- 图片、图标按钮、图表**缺替代文本**
- 需要**静态审计**一处页面并产出分级修复报告
- 要把无障碍检查**固化进 CI** 做门禁
- 需要**读屏实测**（NVDA / VoiceOver）发现自动化抓不到的问题

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| WCAG 2.2 合规模型与 SC 判据 | [references/wcag-playbook.md](references/wcag-playbook.md) | wcag, 2.2, AA, AAA, POUR, 合规, EAA, ADA, 成功准则 |
| 语义化 HTML 与 ARIA 决策 | [references/semantic-html-aria.md](references/semantic-html-aria.md) | 语义, aria, role, 决策树, 反模式, 五铁律 |
| 键盘可达与焦点管理 | [references/keyboard-focus.md](references/keyboard-focus.md) | 键盘, 焦点, focus, 陷阱, roving, tabindex, skip link |
| 读屏器实测方法 | [references/screen-reader-testing.md](references/screen-reader-testing.md) | 读屏, nvda, voiceover, 实测, live region, 测试脚本 |
| 审计与修复工作流 | [references/audit-remediation.md](references/audit-remediation.md) | 审计, 修复, 严重度, 报告, CI, 门禁, 流水线 |
| 语义标记（细粒度调用） | [skills/semantic-markup/SKILL.md](skills/semantic-markup/SKILL.md) | semantic-markup, 语义标签, dialog, 菜单, 标签页 |
| 键盘可达（细粒度调用） | [skills/keyboard-a11y/SKILL.md](skills/keyboard-a11y/SKILL.md) | keyboard-a11y, 模态, 焦点归还, 方向键 |
| 替代文本（细粒度调用） | [skills/alt-text/SKILL.md](skills/alt-text/SKILL.md) | alt-text, alt, 图标按钮, svg, 图表 |
| 无障碍审计（细粒度调用） | [skills/a11y-audit/SKILL.md](skills/a11y-audit/SKILL.md) | a11y-audit, 审计, 报告, 分级, 排期 |

> 路由规则：先判断任务属于「合规判据 / 语义标记 / 键盘焦点 / 读屏实测 / 审计修复」哪一类；做方法论决策读 `references/`，要落地某个具体能力直接调 `skills/`。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本处理重复/确定性任务，而非每次重写代码：

- `scripts/contrast_check.py <前景> <背景>` — 计算 WCAG 对比度并判定 AA/AAA（支持 `--json`/`--strict`）
- `scripts/a11y_audit.py <page.html|->` — 静态 HTML 审计：缺 lang/title/alt、无名链接按钮、表单无 label、跳级标题等
- `scripts/aria_lint.py <page.html|->` — 校验 ARIA 用法：角色合法、必需子角色、冗余 role、未知 aria 属性

运行示例：

```bash
python3 scripts/contrast_check.py "#777777" "#ffffff" --strict
python3 scripts/a11y_audit.py page.html --strict
python3 scripts/aria_lint.py page.html --strict
```

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- [assets/wcag-checklist.md](assets/wcag-checklist.md) — WCAG 2.2 AA 速查清单（按 POUR 组织）
- [assets/a11y-audit-report-template.md](assets/a11y-audit-report-template.md) — 审计报告模板（含严重度分级）
- [assets/component-a11y-acceptance.md](assets/component-a11y-acceptance.md) — 组件无障碍验收标准模板

## 核心原则（始终遵循）

1. **语义优先**：能用原生标签就别上 ARIA，错误 ARIA 比没有更糟。
2. **键盘是底线**：所有功能必须不用鼠标也能完成，焦点可见且不丢失。
3. **对比度算出来**：用 `contrast_check.py` 判定，不靠"看起来还行"。
4. **自动化只覆盖三成**：读屏实测与焦点实际表现必须人工验证。
5. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜 ARIA 角色。
6. **明确边界**：本技能给技术对齐路径，法律结论以官方文本为准；不替团队做合规拍板。

## 与其他技能协作

- 需要**测试**（单测 / E2E 含 a11y 断言）→ 调用 `software-tester`
- 需要**安全审计**（XSS 也可能破坏可访问性）→ 调用 `security-guardian`
- 需要**前端组件 / CSS 布局**落地 → 调用 `ai-fullstack-engineer`
- 需要**文档**（可访问性说明、合规文档）→ 调用 `docs-writer`
