---
name: gsc-search
description: "Ruft Google Search Console Daten für akku-alle.de ab - Klicks, Impressionen, CTR, Rankings und Top-Keywords. Nutze das shell Tool um /root/.openclaw/skills/gsc-search/gsc-search auszuführen."
metadata: {"requires":{"env":["GOOGLE_APPLICATION_CREDENTIALS"]},"emoji":"🔍","always":true}
user-invocable: true
---

# Google Search Console Skill

Ruft Search Console Daten für akku-alle.de ab.

## Aufruf via Shell Tool

**WICHTIG**: Rufe dieses Skill mit dem `shell` Tool auf:

```bash
/root/.openclaw/skills/gsc-search/gsc-search
```

Für nur Keywords/Suchanfragen:

```bash
/root/.openclaw/skills/gsc-search/gsc-search "queries"
```

## Beispiel-Ausgabe

```
## 🔍 Search Console Übersicht (02.02 - 09.02.2026)
- **Klicks:** 106
- **Impressionen:** 10,661
- **CTR:** 0.99%
- **Ø Position:** 6.9

## 🔎 Top Suchanfragen
| Query | Klicks | Impressionen | CTR | Pos |
|-------|--------|--------------|-----|-----|
| e scooter versicherung 2026 | 2 | 138 | 1.4% | 2.8 |
```

## Wann verwenden

Nutze dieses Skill wenn der User fragt:
- "Zeige mir die Search Console Daten"
- "Für welche Keywords rankt akku-alle.de?"
- "Wie sind die Google Rankings?"
- "SEO Statistiken"
