---
name: axiom-phone-e164
description: 电话号码规范化器 — 将任何电话号码转换为 E.164 国际格式。在需要用于存储或比较的规范电话表示时使用。纯标准库,无需 LLM。
version: 0.1.2
license: Apache-2.0
---

# axiom-phone-e164

**Version:** 0.1.2
**Axioma Tools**

将电话号码规范化为 E.164 标准 (例如:+14155552671)。

## What this skill does

- 解析本地和国际格式
- 检测国家代码 (默认:US/CA)
- 返回规范 E.164 字符串
- 验证长度和国家前缀

## When to use this skill

- ✅ 规范化用户输入的电话号码以供存储
- ✅ 联系人去重
- ✅ 为 SMS API 格式化 (Twilio 等)
- ❌ 验证号码是否可接通 (需要单独的 API)

## Usage

```bash
python3 axiom_phone_e164.py "(415) 555-2671"
python3 axiom_phone_e164.py "14155552671" --country US
```

```python
from axiom_phone_e164 import normalize
normalize('(415) 555-2671', default_country='US')  # '+14155552671'
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
