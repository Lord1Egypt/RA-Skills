---
name: axiom-uuid-analyzer
description: UUID 检查器 — 解析任何 UUID 并提取版本 (1-8)、变体 (RFC 4122、Microsoft、NCS、Future)、时间戳 (v1、v7)、MAC 地址 (v1)。在需要分析、验证或审计 UUID 时使用。纯标准库,无需 LLM。
version: 0.1.2
license: Apache-2.0
---

# axiom-uuid-analyzer

**Version:** 0.1.2
**Axioma Tools**

检查 UUID 并提取其语义内容。

## What this skill does

- 验证 UUID 格式 (8-4-4-4-12 十六进制)
- 提取版本 (1-8)
- 提取变体 (RFC 4122、Microsoft、NCS、Future)
- 对于 v1:提取时间戳和 MAC 地址
- 对于 v7:提取 unix 时间戳

## When to use this skill

- ✅ 分析不是你生成的 UUID
- ✅ 审计数据库中 UUID 版本的一致性
- ✅ 从基于时间的 UUID 中提取时间戳
- ✅ 验证用户输入中的 UUID
- ❌ 生成 UUID (直接使用 uuid 模块)

## Usage

```bash
python3 axiom_uuid_analyzer.py "550e8400-e29b-41d4-a716-446655440000"
python3 axiom_uuid_analyzer.py uuid-list.txt --json
```

```python
from axiom_uuid_analyzer import analyze_uuid
info = analyze_uuid('550e8400-e29b-41d4-a716-446655440000')
# {'version': 4, 'variant': 'RFC 4122', 'timestamp': None, 'mac': None}
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 30+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
