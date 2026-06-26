---
name: ga4-analytics
description: "Ruft Google Analytics 4 Daten für akku-alle.de ab - Seitenaufrufe, Nutzer, Sessions, Top-Seiten und Traffic-Quellen. Nutze das shell Tool um /root/.openclaw/skills/ga4-analytics/ga4-analytics auszuführen."
metadata: {"requires":{"env":["GOOGLE_APPLICATION_CREDENTIALS","GA4_PROPERTY_ID"]},"emoji":"📊","always":true}
user-invocable: true
---

# GA4 Analytics Skill

Ruft Google Analytics 4 Daten für akku-alle.de ab.

## Aufruf via Shell Tool

**WICHTIG**: Rufe dieses Skill mit dem `shell` Tool auf:

```bash
/root/.openclaw/skills/ga4-analytics/ga4-analytics
```

Für nur Top-Seiten:

```bash
/root/.openclaw/skills/ga4-analytics/ga4-analytics "top seiten"
```

## Beispiel-Ausgabe

```
## 📊 Traffic-Übersicht (7 Tage)
- **Sessions:** 41
- **Nutzer:** 23
- **Pageviews:** 126
- **Bounce Rate:** 31.7%

## 📄 Top Seiten
| Seite | Views | Users |
|-------|-------|-------|
| / | 65 | 7 |
| /ratgeber/e-scooter-versicherung | 24 | 6 |
```

## Wann verwenden

Nutze dieses Skill wenn der User fragt:
- "Zeige mir die GA4 Statistiken"
- "Wie viele Besucher hat akku-alle.de?"
- "Welche Seiten werden am meisten besucht?"
- "Analytics Daten"
