---
name: axiom-cron-whisperer
description: Cron 表达式解释器 — 将 cron 语法翻译成人类语言 (英语或法语)。在需要理解、记录或验证 cron 表达式时使用。纯标准库,无需 LLM。
version: 0.1.2
license: Apache-2.0
---

# axiom-cron-whisperer

**Version:** 0.1.2
**Axioma Tools**

将 cron 表达式翻译成人类可读的说明。

## What this skill does

- 解析标准 cron 语法 (5 个字段)
- 用英语或法语解释
- 部署前验证
- 示例:`0 9 * * 1-5` → '在 09:00,周一至周五'

## When to use this skill

- ✅ 理解不是你编写的 cron 表达式
- ✅ 记录 cron 任务
- ✅ 部署前验证
- ❌ 计算接下来的 N 次发生时间 (使用 croniter)
- ❌ Quartz 语法 (@yearly, L, W, #) — 不支持

## Usage

```bash
python3 axiom_cron_whisperer.py "0 9 * * 1-5"
python3 axiom_cron_whisperer.py "*/15 * * * *" --lang fr
python3 axiom_cron_whisperer.py "0 9 * * 1-5" --validate
```

```python
from axiom_cron_whisperer import explain, validate
explain('0 9 * * 1-5')  # '在 09:00,周一至周五'
validate('not a cron')  # False
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 17 cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
