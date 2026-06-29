# axiom-phone-e164

> Phone number E.164 parser and normalizer.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

`(514) 555-1234` et `+1 555 123 4567` et `06 12 34 56 78` — 3 formats pour le même concept.

**axiom-phone-e164** normalise vers `+15551234567` (E.164 international).

Cas d'usage :
- Database dedup (reconnaître le même user)
- SMS gateways (besoin d'E.164)
- Form validation
- WhatsApp/Telegram integration

## 🚀 Usage

```bash
# France
python3 axiom_phone_e164.py "+33 6 12 34 56 78"
# ✅ E.164: +33612345678
#    Country: France (+33)

# Numéro français sans + (default country FR)
python3 axiom_phone_e164.py "06 12 34 56 78" --country 33

# US
python3 axiom_phone_e164.py "(514) 555-1234"

# JSON
python3 axiom_phone_e164.py "+44 20 7946 0958" --json
```

## 🧪 Tests

13 tests passent.

## ⚠️ Limitations

- ~200 pays (codes d'indicatif + longueur)
- Pas de validation en temps réel

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.01/use |
