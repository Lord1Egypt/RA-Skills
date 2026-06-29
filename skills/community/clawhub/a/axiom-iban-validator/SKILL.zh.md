---
name: axiom-iban-validator
description: IBAN 验证器 — 检查 100+ 个国家的 IBAN 格式和 mod-97 校验和。在需要验证国际银行账号时使用。纯标准库,无需 LLM。
version: 0.1.2
license: Apache-2.0
---

# axiom-iban-validator

**Version:** 0.1.2
**Axioma Tools**

使用 mod-97 算法验证 IBAN,带特定国家长度检查。

## What this skill does

- mod-97 校验和验证
- 特定国家长度检查 (FR=27, DE=22, GB=22 等)
- 去除输入中的空格和短横线
- 返回 BBAN 细分

## When to use this skill

- ✅ 付款提交前验证 IBAN
- ✅ 审计客户银行数据
- ✅ 在付款表单中预验证
- ❌ 验证账户是否真实存在 (需要单独的 API)

## Usage

```bash
python3 axiom_iban_validator.py "FR76 3000 6000 0112 3456 7890 189"
python3 axiom_iban_validator.py --country FR --number "3000600011234567890189"
```

```python
from axiom_iban_validator import validate_iban
validate_iban('FR7630006000011234567890189')  # True
# 返回: {valid, country, bban, checksum_ok, length_ok}
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
