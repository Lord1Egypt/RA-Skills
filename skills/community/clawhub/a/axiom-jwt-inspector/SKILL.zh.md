---
name: axiom-jwt-inspector
description: JWT 检查器 — 解码 JSON Web Tokens 并检查 header、payload、claims、过期时间。在需要调试或审计 JWT 时使用。纯标准库,无需 LLM。**不验证签名** (请使用 JWT 库进行验证)。
version: 0.1.2
license: Apache-2.0
---

# axiom-jwt-inspector

**Version:** 0.1.2
**Axioma Tools**

解码 JWT 并公开其结构以供调试和审计。

## What this skill does

- 解码 header (alg、typ、kid 等)
- 解码 payload (claims)
- 显示过期状态 (exp/nbf/iat)
- 标记常见漏洞 (alg=none、弱密钥)
- **不验证签名** — 仅用于调试

## When to use this skill

- ✅ 调试你收到的 JWT
- ✅ 信任 token 之前审计其结构
- ✅ 检查过期/签发时间
- ❌ 用户身份验证 (使用带签名验证的 JWT 库)
- ❌ 替代 pyjwt (仅检查)

## Usage

```bash
python3 axiom_jwt_inspector.py "eyJhbGciOiJIUzI1NiIs..."
python3 axiom_jwt_inspector.py token.txt --json
```

```python
from axiom_jwt_inspector import inspect_jwt
info = inspect_jwt('eyJhbGciOiJIUzI1NiIs...')
# {'header': {...}, 'payload': {...}, 'expired': False, 'warnings': []}
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
