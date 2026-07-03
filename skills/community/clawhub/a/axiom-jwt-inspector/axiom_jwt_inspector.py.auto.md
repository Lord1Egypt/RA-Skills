# 📄 `axiom_jwt_inspector.py`

**Path:** `/run/media/axioma/Merlin/axiom-skills-public/axiom-jwt-inspector/axiom_jwt_inspector.py`  
**Size:** 7,551 bytes / 228 lines  
**Hash:** `bf1bde35f9cc3310`  
**Generated:** 2026-06-15T03:00:47.167161+00:00

## 📝 Module Docstring

```
🛠️ axiom-jwt-inspector — JWT Decoder & Inspector
==================================================

⚠️ LIMITATIONS CONNUES :
- Vérif signature HS256/HS384/HS512 seulement (pas RS256/ES256)
- Pas de validation `aud`, `iss`, `nbf`, `exp` (parsing only)
- Pas de support JWE (encrypted JWT)

DÉCODE ET INSPECTE LES JSON WEB TOKENS
```

## 📦 Imports (8)

```python
import base64
import hashlib
import hmac
import json
import re
import sys
import time
import argparse
```

## ⚡ Functions (6)

### `def _b64url_decode(s):`
> Base64url decode with padding.

### `def _b64url_encode(b):`
> Base64url encode without padding.

### `def decode(jwt_token):`
> Decode a JWT (header + payload). Does NOT verify signature.

Returns dict with: header, payload, signature, valid_format, errors

### `def verify_hmac(jwt_token, secret):`
> Verify HMAC signature (HS256, HS384, HS512).

Returns dict with: signature_valid, algorithm_used

### `def create(payload, secret, alg):`
> Create a JWT with the given payload and HMAC signature.

Returns the JWT string.

### `def main():`
