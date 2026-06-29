# axiom-cron-whisperer

> Cron expression explainer — translate cron to human language.

**Axioma Tools for Capafy**
**Version:** 0.1.0

---

## 🎯 Problème résolu

Une expression cron comme `0 9 * * 1-5` est incompréhensible pour la plupart des gens.
**axiom-cron-whisperer** la traduit en langage humain :
- `0 9 * * 1-5` → *"At 09:00, every day of the month, every month, Monday through Friday"*
- `*/15 * * * *` → *"Every 15 minutes"*
- `0 0 1 1 *` → *"At 00:00, on day 1 of the month, in January, every day of the week"*

Cas d'usage :
- DevOps qui debug un cron qu'ils ont pas écrit
- No-code users qui veulent comprendre des schedules
- Documentation automatique de jobs cron
- Validation avant déploiement

---

## 🚀 Usage

### CLI

```bash
# English (default)
python3 axiom_cron_whisperer.py "0 9 * * 1-5"
# At 09:00, every day of the month, every month, Monday through Friday

# French
python3 axiom_cron_whisperer.py "0 9 * * 1-5" --lang fr
# À 09:00, tous les jours du mois, tous les mois, du lundi au vendredi

# Validate only
python3 axiom_cron_whisperer.py "0 9 * * 1-5" --validate
# ✅ Valid cron expression

# JSON output
python3 axiom_cron_whisperer.py "*/15 * * * *" --json
# {
#   "expression": "*/15 * * * *",
#   "parsed": {"minute": [0,15,30,45], ...},
#   "explanation": "Every 15 minutes, ...",
#   "valid": true
# }
```

### Python API

```python
from axiom_cron_whisperer import explain, is_valid, parse_cron

print(explain("0 9 * * 1-5"))  # "At 09:00, ..., Monday through Friday"
print(explain("*/15 * * * *", lang="fr"))  # "Toutes les 15 minutes"
is_valid("0 9 * * 1-5")  # True
parsed = parse_cron("0 9 * * 1-5")  # dict
```

---

## 🧪 Tests

```bash
cd axiom-cron-whisperer/
python3 -m unittest test_axiom_cron_whisperer.py -v
```

**17 tests couvrent :**
- Parsing de chaque type de champ (`*`, `N`, `N,M`, `N-M`, `*/N`)
- 5 fields obligatoire
- Valeurs hors limites rejetées
- Explication EN et FR
- Validation
- Déterminisme

---

## ⚠️ Limitations

- Pas de support des syntaxes étendues (`@yearly`, `@reboot`, `@hourly` Quartz)
- Pas de calcul des N prochaines occurrences
- Pas de gestion L/W/# (Quartz)
- Pas de support des secondes (cron 6-fields)
- Locale unique FR/EN (pas de DE, ES, etc.)

---

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Langage** | Python 3.11+ (pure stdlib) |
| **Dépendances** | 0 externe |
| **Lignes de code** | ~250 |
| **Pricing Capafy** | $0.01/use |

---

## 🤝 Crédits

- **Premier jet :** Axioma team
- **À valider :** Axioma team
- **Mission :** Kofna336 (Papa)
