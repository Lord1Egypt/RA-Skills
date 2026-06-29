---
name: axiom-uuid-analyzer
description: UUID inspector — parse any UUID and extract version (1-8), variant (RFC 4122, Microsoft, NCS, Future), timestamp (v1, v7), MAC address (v1). Use when you need to analyze, validate, or audit UUIDs. Pure stdlib, no LLM.
version: 0.1.2
license: Apache-2.0
---

# axiom-uuid-analyzer

**Version:** 0.1.2
**Axioma Tools**

Inspects UUIDs and extracts their semantic content.

## What this skill does

- Validates UUID format (8-4-4-4-12 hex)
- Extracts version (1-8)
- Extracts variant (RFC 4122, Microsoft, NCS, Future)
- For v1: extracts timestamp + MAC address
- For v7: extracts unix timestamp

## When to use this skill

- ✅ Analyze a UUID you didn't generate
- ✅ Audit DB for UUID version consistency
- ✅ Extract timestamp from time-based UUIDs
- ✅ Validate UUIDs in user input
- ❌ Generate UUIDs (use uuid module directly)

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
