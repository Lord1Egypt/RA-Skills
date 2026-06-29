# axiom-markdown-link-auditor

> Markdown link checker — find all links and (optionally) check HTTP status.

**Axioma Tools for Capafy**
**Version:** 0.1.0

## 🎯 Problème résolu

Tes liens sont cassés ? Tu veux savoir lesquels avant publication ?

**axiom-markdown-link-auditor** :
- Extrait tous les liens d'un .md
- Catégorise (link, image, bare URL)
- Optionnel : HEAD request pour vérifier HTTP status
- Liste les liens cassés avec ligne

## 🚀 Usage

```bash
# Sans remote check (rapide)
python3 axiom_markdown_link_auditor.py README.md

# Avec remote check (lent, mais complet)
python3 axiom_markdown_link_auditor.py README.md --check-remote

# JSON
python3 axiom_markdown_link_auditor.py README.md --check-remote --json
```

## 🧪 Tests

11 tests passent.

## ⚠️ Limitations

- Pas de JS-rendered pages
- Pas d'ancres internes (#section)
- HEAD seulement, pas de GET fallback

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Pricing Capafy** | $0.02/use |
