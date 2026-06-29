# axiom-css-specificity

> CSS specificity calculator — compute (a, b, c) for any CSS selector.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

Pourquoi mon CSS ne s'applique pas ? Probablement un problème de spécificité.

**axiom-css-specificity** calcule la spécificité W3C de n'importe quel sélecteur :
- `a` = nombre d'IDs (`#foo`)
- `b` = nombre de classes, attributs, pseudo-classes (`.foo`, `[bar]`, `:hover`)
- `c` = nombre d'éléments, pseudo-éléments (`div`, `::before`)

Cas d'usage :
- Debugging CSS (pourquoi une règle est ignorée)
- Refactoring (équilibrer la spécificité)
- Audit (détecter les sélecteurs sur-spécifiques)
- Lint (éviter `!important`)

## 🚀 Usage

```bash
# Spec d'un sélecteur
python3 axiom_css_specificity.py "#header .nav a:hover"
# Selector:   #header .nav a:hover
# Specificity: (1, 2, 1)  (a=1, b=2, c=1)

# Comparer deux sélecteurs
python3 axiom_css_specificity.py "#header .nav a" --compare ".nav a"
# A: #header .nav a                    → (1, 1, 1)
# B: .nav a                             → (0, 1, 1)
# 🏆 Winner: a

# Examples builtin
python3 axiom_css_specificity.py --examples
```

## 🧪 Tests

18 tests passent (0.005s).

## ⚠️ Limitations

- `@scope` non supporté
- `:is()` / `:not()` simplifiés
- Pas de résolution `!important`

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.02/use |
