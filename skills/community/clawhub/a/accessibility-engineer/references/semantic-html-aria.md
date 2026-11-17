# 语义化 HTML 与 ARIA（Playbook）

> 适用技能：[skills/semantic-markup](../skills/semantic-markup/SKILL.md)（语义标签选择、ARIA 用法与反模式修复）。

> 决定"什么时候用原生标签、什么时候上 ARIA、怎么上才不会更糟"。本篇是组件级可访问性的方法论核心。

## 何时用本篇

- 写一个交互组件（弹窗、菜单、标签页、下拉、树）不确定该用语义标签还是 ARIA
- Code Review 看到满屏 `role=` 想判断是否过度
- 排查"读屏读不出来/读错"的控件问题

## 第一原则：语义 HTML 优先

原生元素自带正确的 name / role / state / 键盘行为。**能用 `<button>` 就别用 `<div onclick>`。**

| 意图 | 用原生 | 不要用 |
|------|--------|--------|
| 可点击动作 | `<button>` | `<div role="button">` |
| 导航链接 | `<a href>` | `<span onclick>` |
| 文本输入 | `<input>`/`<textarea>` | `contenteditable` 裸 div |
| 列表 | `<ul>/<ol>/<li>` | 一堆 `<div>` |
| 标题 | `<h1>–<h6>` | 加粗的 `<div>` |
| 地标 | `<header>/<nav>/<main>/<footer>` | 无语义 `<div>` |

## ARIA 决策树

```
需求是一个交互控件或状态？
├─ 原生元素能表达？ → 直接用原生，结束。
└─ 不能（需复合 widget，如 tablist/combobox）→
    ├─ 选用标准 role（见下方清单）
    ├─ 配合必需子角色（listbox→option, tablist→tab, radiogroup→radio）
    ├─ 用 aria-* 暴露状态（expanded/selected/pressed/checked）
    └─ 自己补齐键盘交互（见 keyboard-focus.md）
```

## ARIA 五铁律（必背）

1. **不用 ARIA 好过用错的 ARIA**（No ARIA is better than bad ARIA）。
2. **不要改原生语义**：`<button role="heading">` 是错误，破坏按钮行为。
3. **所有交互 ARIA 控件必须可用键盘**（role + 键盘缺一不可，否则更糟）。
4. **`aria-hidden="true"` 的元素内不能有可聚焦元素**（否则读屏与 Tab 错位）。
5. **可见文字优先于 `aria-label`**：若 `aria-label` 与可见文本冲突，读屏播报 aria-label，易造成不一致。

## 角色速查

- **地标（landmark）**：`banner`(header) `navigation`(nav) `main` `contentinfo`(footer) `complementary`(aside) `search` `form` `region`
- **组合 widget**：`listbox` `menu`/`menubar` `radiogroup` `tablist` `tree` `grid` `table` `combobox`
- **原子 widget**：`button` `checkbox` `link` `option` `radio` `slider` `spinbutton` `switch` `tab` `textbox` `progressbar`
- **实时区域**：`alert` `status` `log` `marquee` `timer`

> 完整角色与必需子角色校验见 `aria_lint.py`；它会直接报错"listbox 缺 option"。

## 高频反模式

| 反模式 | 后果 | 正确做法 |
|--------|------|----------|
| 所有 div 都加 `role` | 噪音、读屏卡顿 | 首选语义标签 |
| `<a>` 无 href 当按钮 | 不聚焦、不触发 | 用 `<button>` |
| `aria-label` 覆盖可见文本 | 视障/明眼信息不一致 | 让可见文本即名称 |
| `aria-hidden` 包住 `tabindex=0` 元素 | Tab 能进、读屏不读 | 移除其一 |
| `role="list"` 给 `<ul>` | 冗余（见 `aria_lint.py` redundant-role） | 删掉即可 |

## 限制

- ARIA 不能修复对比度、不能替代键盘支持——这些是其它维度的要求（见 `wcag-playbook.md`、`keyboard-focus.md`）。
- 读屏实际表现仍需 `screen-reader-testing.md` 验证；静态 lint 只查"用法合法"。
