---
name: axiom-luhn-check
description: Luhn 算法验证器 — 信用卡 (Visa、MC、Amex、Discover)、SIRET/SIREN、IMEI、ISBN-10/13。在需要验证任何使用 Luhn 的数字时使用。纯标准库,无需 LLM。
version: 0.1.2
license: Apache-2.0
---

# axiom-luhn-check

**Version:** 0.1.2
**Axioma Tools**

使用 Luhn 算法验证数字,自动检测常见类型。

## What this skill does

- 对任何数字字符串进行 Luhn 检查
- 自动检测类型 (Visa/MC/Amex/Discover/SIRET/IMEI/ISBN-10/13)
- JSON 输出供脚本使用
- 处理输入中的空格和短横线

## When to use this skill

- ✅ 提交前验证信用卡
- ✅ 审计移动设备的 IMEI
- ✅ 编目前验证 ISBN
- ✅ 验证法国 SIRET/SIREN
- ❌ 需要完全 PCI 合规验证 (此工具仅校验和)

## Usage

```bash
python3 axiom_luhn_check.py "4532 0151 1283 0366"
python3 axiom_luhn_check.py "356938035643809" --json
```

```python
from axiom_luhn_check import validate, detect_type
validate('4532015112830366')  # True
detect_type('356938035643809')  # 'amex'
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 25+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
