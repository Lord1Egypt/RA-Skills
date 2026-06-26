# LLM-Summary Prompt für Feeds Digest

Du erhältst einen Roh-Digest mit Tech-Updates aus verschiedenen Quellen (YouTube, Microsoft Tech Community, GitHub Releases).

## Deine Aufgabe

Erstelle eine **Executive Summary** in deutscher Sprache (oder Englisch, falls Rohdaten englisch):

1. **Top 3-5 Highlights** (max. ein Bullet pro Highlight)
   - Was ist neu?
   - Warum relevant für ERP-/BC-/Power-BI-/AI-Consulting?
   - Link zum Original

2. **Breaking Changes** (falls vorhanden)
   - Was muss man sofort wissen / anpassen?

3. **Ignorieren**
   - Marketing-Floskeln
   - Wiederholungen / Duplikate
   - Triviale Bugfixes ohne Folgen

## Format

```markdown
## Highlights
- **[Datum]** [Titel](Link) — *Relevanz: ...*

## Breaking Changes
- **[Datum]** [Was bricht](Link) — *Aktion: ...*

## Beobachten
- [Thema]: 2-3 Sätze Kontext + Link
```

Halte dich kurz. Maximal 250 Wörter total. Keine Einleitung, keine Floskeln.
