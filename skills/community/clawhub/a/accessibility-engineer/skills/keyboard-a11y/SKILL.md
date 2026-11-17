---
name: keyboard-a11y
description: 实现全键盘可达与焦点管理（模态陷阱/归还、roving tabindex、SPA 焦点转移、跳过链接）。
source:
  type: derived
  repo: skills-repo/accessibility-engineer
  path: skills/keyboard-a11y/SKILL.md
  version: 1.0.0
  updated: 2026-09-02
  url: https://skills.sh/ibelick/ui-skills/fixing-accessibility
metadata:
  category: 无障碍工程
  platform: Web
  difficulty: 进阶
---

# 键盘可达与焦点管理（Keyboard A11y）

> 让所有功能不靠鼠标也能完成，且焦点可见、有序、不丢失。

## 能力

- 为模态弹窗实现焦点陷阱与关闭后焦点归还
- 为组合 widget 实现 roving tabindex（方向键导航）
- SPA 路由切换后把焦点移到新页面主区
- 添加跳转主内容的 skip link，提供清晰的焦点指示

## 使用方式

```
/keyboard-a11y 这个弹窗打开后焦点丢了，帮我修
/keyboard-a11y 给标签页加键盘左右切换
```

## 工作流

1. 确认所有交互都能用 Tab / Enter / 方向键完成（SC 2.1.1）。
2. 模态：打开移焦点入、内部 Tab 循环、关闭归还触发元素、`Esc` 可关。
3. 组合 widget：容器 `tabindex=0`，子项 `tabindex=-1`，方向键移动焦点。
4. SPA：路由切换后 `.focus()` 到 `main`（带 `tabindex=-1`）。
5. 绝不用 `outline:none` 而不给 `:focus-visible` 替代。

## 适用场景

- 弹窗/抽屉打开后无法关闭或背景仍可 Tab
- Tab 顺序错乱、焦点看不见
- 自定义菜单、标签页、列表框的键盘操作

## 相关参考

- 方法论：[references/keyboard-focus.md](../../references/keyboard-focus.md)（焦点陷阱、roving tabindex、skip link）
- 实测确认：[references/screen-reader-testing.md](../../references/screen-reader-testing.md)（键盘可达性最终需读屏实测）
- 修复分级：[references/audit-remediation.md](../../references/audit-remediation.md)（焦点类缺陷整改）
- 语义基础：[skills/semantic-markup](../semantic-markup/SKILL.md)

## 限制

- 焦点管理需配合正确语义/ARIA（`semantic-markup`），否则读屏仍读错。
- 是否"好用"最终需 `screen-reader-testing` 实测确认。
