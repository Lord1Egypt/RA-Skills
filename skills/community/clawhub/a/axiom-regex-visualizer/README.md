# axiom-regex-visualizer

> Regex pattern visualizer — tokenize and explain any regex.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

`(?:https?://)?(?:www\.)?[\w-]+\.[a-z]{2,}` — qu'est-ce que ça matche ?

**axiom-regex-visualizer** :
- Tokenize la regex en composants
- Visualise en arbre lisible
- Explique en anglais plain

## 🚀 Usage

```bash
# Visualize
python3 axiom_regex_visualizer.py "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Plain English
python3 axiom_regex_visualizer.py --explain "(\d{3})-(\d{3})-(\d{4})"

# Just tokens
python3 axiom_regex_visualizer.py --tokens "https?://[^\s]+"
```

## 🧪 Tests

17 tests passent.

## ⚠️ Limitations

- Pas de lookbehind complexes
- Pas de backref visualization

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.02/use |
