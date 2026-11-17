---
name: semantic-markup
description: 为 UI 组件编写语义化 HTML 与正确的 ARIA（按钮/对话框/菜单/标签页等），避免无意义 role。
source:
  type: derived
  repo: skills-repo/accessibility-engineer
  path: skills/semantic-markup/SKILL.md
  version: 1.0.0
  updated: 2026-09-02
  url: https://skills.sh/jakubkrehel/skills/better-accessibility
metadata:
  category: 无障碍工程
  platform: Web
  difficulty: 进阶
---

# 语义化标记（Semantic Markup）

> 把"能显示"的组件变成"读屏能懂"的组件：优先原生标签，必要时用对的 ARIA。

## 能力

- 判断一个交互组件该用语义标签还是 ARIA
- 为对话框、菜单、标签页、下拉、列表框等编写合规 role/state
- 审查并去除冗余或错误 role（可用 `aria_lint.py` 辅助检查）
- 保证自定义控件暴露正确的 name / role / state

## 使用方式

```
/semantic-markup 把这段 div 弹窗改成合规 dialog
/semantic-markup 这个 tab 切换怎么写 ARIA 才对
```

## 工作流

1. 先看能否用原生元素（`<button>`/`<a>`/`<nav>`/`<main>`）表达，能则直接用。
2. 不能用时，从标准角色中选一个（参考 [references/semantic-html-aria.md](../../references/semantic-html-aria.md) 角色速查）。
3. 补齐必需子角色（如 `tablist` 下必须有 `tab`）。
4. 用 `aria-expanded` / `aria-selected` / `aria-pressed` 等暴露状态。
5. 用 `aria_lint.py` 静态校验 role 合法性与必需子角色。

## 适用场景

- 用 div/span 拼出来的"伪按钮""伪弹窗"
- 自定义组合组件（标签页、手风琴、树、列表框）
- Code Review 中满屏 `role=` 的标记

## 限制

- 只解决"标记语义"，键盘交互与焦点需配合 `keyboard-a11y` 子技能。
- ARIA 用法合法 ≠ 读屏体验好，最终需 `screen-reader-testing` 实测。
