# axiom-iban-validator

> IBAN validator with mod-97 algorithm (ISO 13616).

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

Valider un IBAN sans appel API bancaire. L'algorithme mod-97 est public (ISO 13616).

**axiom-iban-validator** :
- Valide format (longueur par pays, charset)
- Valide checksum (mod-97)
- Détecte pays + longueur attendue
- ~80 pays supportés

## 🚀 Usage

```bash
# France
python3 axiom_iban_validator.py "FR76 3000 6000 0112 3456 7890 189"
# ✅ Valid IBAN: FR76 3000 6000 0112 3456 7890 189
#    Country: FR

# Allemagne
python3 axiom_iban_validator.py "DE89370400440532013000"

# JSON
python3 axiom_iban_validator.py "BE68539007547034" --json
```

## 🧪 Tests

14 tests passent.

## ⚠️ Limitations

- ~80 pays principaux (pas la liste ISO 13616 complète)
- Pas de validation BIC/SWIFT
- Pas de conversion BBAN ↔ IBAN

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.02/use |
