# WCAG 2.2 AA 速查清单

> 发布前逐条过一遍。目标等级：**AA**。打勾即达标。完整判据见 [references/wcag-playbook.md](../references/wcag-playbook.md)。

## P — 可感知（Perceivable）

- [ ] 1.1.1 所有信息性图片有 `alt`，装饰图 `alt=""`
- [ ] 1.3.1 结构用语义标签/正确 roles 表达（不靠颜色/位置）
- [ ] 1.4.3 正文对比度 ≥ 4.5:1，大字 ≥ 3:1（`contrast_check.py`）
- [ ] 1.4.11 组件边界与状态图标对比度 ≥ 3:1（`contrast_check.py`）
- [ ] 1.4.1 不用颜色作为唯一信息载体（加文字/图标）

## O — 可操作（Operable）

- [ ] 2.1.1 全部功能可用键盘
- [ ] 2.1.2 无键盘陷阱（模态可 Esc 退出）
- [ ] 2.4.2 每个页面有描述性 `<title>`
- [ ] 2.4.3 焦点顺序符合视觉/逻辑顺序
- [ ] 2.4.6 标题层级合理、表单标签清晰
- [ ] 2.4.7 焦点可见（不裸 `outline:none`）
- [ ] 2.5.3 标签（label）尺寸足够大、可点击区域充足

## U — 可理解（Understandable）

- [ ] 3.1.1 `<html lang>` 已声明
- [ ] 3.2.1/3.2.2 组件/页面行为可预期（不意外跳变）
- [ ] 3.3.1/3.3.2 输入错误有识别与文字说明

## R — 健壮（Robust）

- [ ] 4.1.2 自定义控件暴露 name/role/state（`aria_lint.py`）
- [ ] 4.1.3 动态提示用 `role="alert"` / `aria-live` 播报
- [ ] 4.1.1 解析无误（无重复 id、标签闭合正确）

## 静态自检命令

```bash
python3 scripts/a11y_audit.py page.html --strict
python3 scripts/aria_lint.py page.html --strict
python3 scripts/contrast_check.py "<前景>" "<背景>" --strict
```
