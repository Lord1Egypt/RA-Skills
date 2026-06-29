---
name: axiom-regex-visualizer
description: 正则表达式可视化器 — 解析任何正则表达式并可视化其结构 (组、量词、锚定、字符类)。在需要理解或记录正则表达式时使用。纯标准库,无需 LLM。
version: 0.1.2
license: Apache-2.0
---

# axiom-regex-visualizer

**Version:** 0.1.2
**Axioma Tools**

解析正则表达式并直观显示其结构。

## What this skill does

- 正则组件的可视化树
- 各部分的简单英语解释
- 高亮组、量词、锚点
- 支持 Python re 语法 (基本 + 扩展)

## When to use this skill

- ✅ 理解不是你编写的正则表达式
- ✅ 记录复杂模式
- ✅ 调试正则匹配问题
- ❌ 测试正则是否匹配字符串 (使用 re.match)
- ❌ 支持 Perl/PCRE 独有功能

## Usage

```bash
python3 axiom_regex_visualizer.py "^(?:[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*)@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
```

```python
from axiom_regex_visualizer import parse, explain
tree = parse(r'\b\d{3}-\d{4}\b')
explain(tree)  # '词边界,正好 3 个数字,短横线,正好 4 个数字,词边界'
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 20+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
