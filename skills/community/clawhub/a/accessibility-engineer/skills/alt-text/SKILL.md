---
name: alt-text
description: 为图片/SVG/图表/图标按钮撰写有意义的替代文本或标记为装饰，配合对比度校验。
source:
  type: derived
  repo: skills-repo/accessibility-engineer
  path: skills/alt-text/SKILL.md
  version: 1.0.0
  updated: 2026-09-02
  url: https://skills.sh/addyosmani/web-quality-skills/accessibility
metadata:
  category: 无障碍工程
  platform: Web
  difficulty: 入门
---

# 替代文本（Alt Text）

> 让非文本内容包括读屏用户：该描述的描述，该装饰的装饰。

## 能力

- 判断图片是"信息性"还是"装饰性"
- 为信息性图片撰写简洁、等价的 alt
- 为图标按钮、SVG、图表提供可读名称
- 配合 `contrast_check.py` 校验文本/图标与背景对比度

## 使用方式

```
/alt-text 给这张产品图写 alt
/alt-text 这几个图标按钮没有名称，帮我补
```

## 工作流

1. 问"去掉这张图，信息是否缺失？"——缺失 → 写 alt；不缺失 → `alt=""`。
2. 信息性 alt：传达图片的**目的**，而非"图片显示…"。图表给结论，细节放长描述。
3. 图标按钮：用 `aria-label` 或包裹 `<button aria-label>`；纯装饰图标 `aria-hidden`。
4. 复杂图（图、示意图）：`alt` 给一句话，详细用 `<figure><figcaption>` 或 `aria-describedby`。
5. 文本与图标对比度用 `contrast_check.py` 复核（正文 ≥4.5:1，组件 ≥3:1）。

## 适用场景

- CMS / 富文本里成批图片缺 alt
- 用图标当按钮却无名称
- 数据图表需要无障碍替代

## 相关参考

- 判据来源：[references/wcag-playbook.md](../../references/wcag-playbook.md)（SC 1.1.1 非文本内容）
- 修复分级：[references/audit-remediation.md](../../references/audit-remediation.md)（alt 缺失/不当的整改）
- 整页静态审计：配合 [skills/a11y-audit](../a11y-audit/SKILL.md)
- 对比度复核：[scripts/contrast_check.py](../../scripts/contrast_check.py)

## 限制

- 只处理"非文本内容"维度；结构、键盘、读屏流程见其它子技能。
- 对比度计算见 `contrast_check.py`，本技能不重复实现公式。
