---
name: axiom-css-specificity
description: CSS 特异性计算器 — 计算任何 CSS 选择器的 (a, b, c) 特异性。处理 :is()、:not()、:where()、组合符、属性选择器。在需要调试 CSS 冲突时使用。纯标准库,无需 LLM。
version: 0.1.2
license: Apache-2.0
---

# axiom-css-specificity

**Version:** 0.1.2
**Axioma Tools**

根据 W3C Selectors Level 4 计算 CSS 特异性。

## What this skill does

- 根据 W3C 规范计算 (a, b, c) 元组
- 处理 :is()、:not()、:where() (where() = 0)
- 处理属性选择器、伪类
- 支持组合符 (>, +, ~, 后代)
- 带细分的 JSON 输出

## When to use this skill

- ✅ 调试 CSS 特异性冲突
- ✅ 审计 CSS 中过于宽泛的选择器
- ✅ 比较两条规则的特异性
- ❌ 渲染 CSS (使用浏览器)
- ❌ 支持 CSS 预处理器语法 (SCSS/Less)

## Usage

```bash
python3 axiom_css_specificity.py "body div#main .item:first-child"
python3 axiom_css_specificity.py --compare "a" "div.menu a"
```

```python
from axiom_css_specificity import compute_specificity
compute_specificity('div#main a:hover')  # (0, 2, 2)
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 18 cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
