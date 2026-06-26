---
name: doc-scraper
description: Documentation extraction and indexing. Extracts information from markdown files and syncs to workspace-db. Works alongside workspace-db which handles synchronization and organization.
---

# Doc Scraper

Dokumentations-Extraktion und Indexierung - arbeitet mit workspace-db zusammen.

## Zusammenspiel mit workspace-db

| Skill | Aufgabe | Datenbank |
|-------|---------|-----------|
| **workspace-db** | Synchronisation & Organisation | docs.db |
| **doc-scraper** (dieser) | Informationsextraktion | Nutzt docs.db |

## Aufgaben

### 1. Markdown-Extraktion
```javascript
// Extrahiert aus SKILL.md:
// - Name, Version, Beschreibung
// - Nutzungsbeispiele
// - Konfigurationsoptionen

const docInfo = await docScraper.extractMarkdown({
  file: "skills/my-skill/SKILL.md",
  extract: ["title", "description", "usage", "config"]
});
```

### 2. Indexierung in docs.db
```javascript
// Speichert extrahierte Daten in docs.db
// (workspace-db verwaltet die DB)

await docScraper.index({
  source: "skills/my-skill/SKILL.md",
  data: docInfo,
  tags: ["skill", "api"]
});
```

### 3. Auto-Update bei Änderungen
```bash
# Überwacht .md Dateien
# Extrahiert bei Änderung neu
# Aktualisiert docs.db

doc-scraper watch --dir skills/ --ext .md
```

## Extraktions-Templates

### Skill-Dokumentation
```yaml
# Aus SKILL.md extrahiert:
name: "skill-name"
description: "Beschreibung"
version: "1.0.0"
category: "database"
usage_examples:
  - command: "openclaw skill"
    result: "..."
```

### API-Dokumentation
```yaml
# Aus API.md extrahiert:
endpoints:
  - path: "/api/v1/search"
    method: "GET"
    params:
      - query: string
    response: json
```

### System-Dokumentation
```yaml
# Aus SYSTEM.md extrahiert:
components:
  - databases:
      - docs.db
      - tree.db
cron_jobs:
  - db-maintainer: "*/30"
```

## Workflow

```
skill.md geändert
    ↓
doc-scraper erkennt Änderung
    ↓
Extrahiert: name, desc, usage, config
    ↓
Speichert in docs.db
    ↓
workspace-db synchronisiert
```

## Nutzung

### Einmalig
```bash
doc-scraper index --dir skills/ --recursive
doc-scraper index --dir docs/ --ext .md
```

### Watch-Modus
```bash
# Kontinuierlich überwachen
doc-scraper watch --dir workspace/

# Einzelne Datei
doc-scraper watch --file README.md
```

### Suche
```bash
# Direkt in extrahierten Daten suchen
doc-scraper search --query "database"
doc-scraper search --tag "api" --format json
```

## Integration mit workspace-db

```javascript
// doc-scraper extrahiert
// workspace-db speichert/organisiert

const extracted = await docScraper.extract('skills/my/SKILL.md');

// Übergabe an workspace-db
await workspaceDb.syncDocument({
  id: extracted.name,
  category: extracted.category,
  data: extracted,
  source_file: 'skills/my/SKILL.md'
});
```

## Konfiguration

```json
{
  "doc-scraper": {
    "watch_dirs": ["skills/", "docs/"],
    "extensions": [".md", ".mdx"],
    "extract_headers": ["##", "###"],
    "auto_index": true,
    "workspace_db_integration": true
  }
}
```

## Links

- [workspace-db Skill](https://clawhub.com/skills/workspace-db)
- [DATABASE_AND_TREE_TRACKING.md](../docs/reference/DATABASE_AND_TREE_TRACKING.md)
