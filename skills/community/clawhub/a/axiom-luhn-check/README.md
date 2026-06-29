# axiom-luhn-check

> Luhn algorithm validator — credit cards, SIRET, IMEI, ISBN.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

L'algorithme de Luhn est utilisé partout : cartes de crédit (Visa, MC, Amex), SIRET/SIREN français, IMEI des téléphones, ISBN-10. Pas toujours facile de valider correctement avec détection de type.

**axiom-luhn-check** fait tout ça d'un coup.

## 🚀 Usage

```bash
# Carte Visa valide
python3 axiom_luhn_check.py "4532015112830366"
# ✅ credit_card_visa
#    Luhn check: OK
#    Length:     16 digits

# Avec espaces
python3 axiom_luhn_check.py "4532 0151 1283 0366"

# SIRET français
python3 axiom_luhn_check.py "73282932000074"

# IMEI
python3 axiom_luhn_check.py "490154203237518"

# JSON
python3 axiom_luhn_check.py "4532015112830366" --json
```

## 🧪 Tests

18 tests passent.

## ⚠️ Limitations

- Détection limitée du type (binaire)
- Pas de validation du préfixe IIN pour chaque réseau
- Pas de support des BIN ranges en temps réel

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.01/use |
