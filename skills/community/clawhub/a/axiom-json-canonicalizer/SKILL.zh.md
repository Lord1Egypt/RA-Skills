---
name: axiom-json-canonicalizer
description: JCS RFC 8785 — 规范化 JSON。将任何 JSON 转换为确定性的、字节到字节相同的规范化形式。在需要对 JSON 进行签名、哈希或比较时使用。纯标准库,无需 LLM,无云。
version: 1.0.1
license: Apache-2.0
---

# axiom-json-canonicalizer

**Version:** 1.0.1
**Axioma Tools**

根据 RFC 8785 (JCS) 将任何 JSON 转换为规范化形式。

## What this skill does

- 对象的键按字典序排序 (NFC 之后)
- 无多余空白
- 数字:ECMAScript 最短往返格式
- 字符串:NFC 规范化,代理对安全
- 输出:UTF-8 字节 (字节到字节稳定)

## When to use this skill

- ✅ 签名 OAuth/JWT 负载 (签名前规范化)
- ✅ 对 JSON 哈希以验证完整性
- ✅ 比较语义等价的 JSON
- ✅ 构建防篡改审计日志
- ❌ 需要美化输出 (使用 json.dumps indent)
- ❌ 需要 JSON5/JSONL/JSONC (不同规范)

## Usage

```bash
python3 axiom_json_canonicalizer.py input.json > canonical.json
python3 axiom_json_canonicalizer.py input.json --verify canonical.json
```

```python
from axiom_json_canonicalizer import canonicalize
canon_bytes = canonicalize(json_obj)  # UTF-8 字节
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 81 cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
