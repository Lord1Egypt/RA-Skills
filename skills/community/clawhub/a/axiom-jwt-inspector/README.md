# axiom-jwt-inspector

> JWT decoder + HMAC signature verifier (HS256/384/512) + creator.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

Debug JWT en local sans jwt.io. Décoder le header, payload, vérifier la signature, créer un JWT de test.

**axiom-jwt-inspector** :
- Decode any JWT
- Show header + payload
- Verify HMAC signature (HS256/384/512)
- Show expiration status
- Create new JWTs

## 🚀 Usage

```bash
# Decode
python3 axiom_jwt_inspector.py "eyJhbGciOiJIUzI1NiIs..."

# Decode + verify HMAC
python3 axiom_jwt_inspector.py "..." --secret mysecret

# Create JWT
python3 axiom_jwt_inspector.py --create '{"sub":"123","exp":1234567890}' --secret-create mysecret

# JSON
python3 axiom_jwt_inspector.py "..." --json
```

## 🧪 Tests

13 tests passent.

## ⚠️ Limitations

- HMAC only (HS256/HS384/HS512)
- No RS256/ES256 (asymmetric)
- No exp/aud/iss/nbf enforcement

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.03/use (security tier) |
