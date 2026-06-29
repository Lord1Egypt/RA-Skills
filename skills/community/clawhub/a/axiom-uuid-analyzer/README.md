# axiom-uuid-analyzer

> UUID inspector — parse any UUID and extract version, variant, timestamp, MAC.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

Un UUID c'est opaque : `550e8400-e29b-41d4-a716-446655440000` — qu'est-ce que ça veut dire ?

**axiom-uuid-analyzer** vous dit :
- Version (1, 2, 3, 4, 5, 6, 7, 8)
- Variante (NCS, RFC 4122, Microsoft, Future)
- Timestamp (si v1 ou v7)
- Adresse MAC (si v1)
- Type (time-based / random / hash-based)

Cas d'usage :
- Forensics (UUID v1 = timestamp + MAC de la machine qui l'a généré)
- Debug (vérifier qu'un UUID v4 est bien random)
- Audit (logger les types d'UUID dans un système)

## 🚀 Usage

```bash
# Analyse complète
python3 axiom_uuid_analyzer.py "550e8400-e29b-41d4-a716-446655440000"
# UUID:        550e8400-e29b-41d4-a716-446655440000
# Version:     4 (v4 (random))
# Variant:     RFC 4122 (rfc4122)
# Type:        random

# JSON
python3 axiom_uuid_analyzer.py "550e8400-e29b-41d4-a716-446655440000" --json

# Validate only
python3 axiom_uuid_analyzer.py "..." --validate

# Batch (un UUID par ligne)
python3 axiom_uuid_analyzer.py --batch uuids.txt
```

## 🧪 Tests

17 tests passent (0.005s).

## ⚠️ Limitations

- v6, v7, v8 partiellement supportés
- Pas de validation stricte variante Microsoft
- Pas de génération de UUID (analyse seulement)

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.01/use |
