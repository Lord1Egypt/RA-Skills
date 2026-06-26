---
name: feeds-digest
description: Multi-Source-RSS-Digest (YouTube, MS Tech Community, GitHub) mit Datums- und Topic-Filter und optionaler LLM-Zusammenfassung.
version: 1.0.0
license: MIT
---

# feeds-digest

Sammelt Updates aus RSS/Atom-Feeds, filtert nach Zeitraum und Themen, gibt einen Markdown-Digest aus.

## Schnellstart

```bash
bash scripts/install.sh                     # einmalig
feeds-digest --since 7d                     # Standard-Digest
feeds-digest --since 3d --topics bc,fabric  # gefiltert
feeds-digest --llm                          # mit LLM-Summary
feeds-digest --output report.md             # in Datei
feeds-digest --test                         # Feed-Erreichbarkeit prüfen
```

## Quellen

- YouTube-Kanäle (RSS)
- Microsoft Tech Community (RSS)
- GitHub Releases (Atom)
- Generische RSS/Atom-Feeds

## Siehe

- `README.md` — ausführliche Doku
- `references/youtube-channel-discovery.md` — Channel-IDs finden
- `references/ms-tc-categories.md` — MS TC Kategorien
- `config/config.example.yaml` — Config-Vorlage
