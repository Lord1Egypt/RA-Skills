# Output-Template — Standardisierte Ideendokumentation

**Use:** Nach Brainstorming-Session. Dokumentation für Handoff + Follow-up.

---

## 1. Meta-Informationen

```markdown
**Session-ID:** [YYYYMMDD-Topic-#]
**Datum:** [YYYY-MM-DD]
**Zeit:** [HH:MM - HH:MM]
**Facilitator:** [Name]
**Teilnehmer:** [Liste]
**Location:** [In-Person / Remote (Tool)]
```

---

## 2. Session-Ziel (aus Zielklärung)

```markdown
**Ausgangssituation:**
[1-2 Sätze: Welches Problem/Chance?]

**Success-Criteria:**
- Must-Haves: [1, 2, 3]
- Should-Haves: [1, 2]
- Nice-to-Haves: [1]

**Constraints:**
- Budget: [X]
- Zeit: [Deadline]
- Compliance: [Anforderungen]
```

---

## 3. Divergente Phase — Ergebnis

### 3.1 Technik eingesetzt

```
Technik: [SCAMPER / 6-3-5 / Mind Mapping / etc.]
Dauer: [X Minuten]
Teilnehmer: [X Personen]
```

### 3.2 Ideen gesamt

```
**Quantität:** [X Ideen]
**Qualitätsschnitt:** [Top 10 identifiziert]
**Wild-Card:** [Überraschendste Idee]
```

### 3.3 Top-Ideen (Rohliste)

| ID | Idee | Kategorie | Autor |
|----|------|-----------|-------|
| D1 | [Beschreibung] | [Cat] | [Name] |
| D2 | [Beschreibung] | [Cat] | [Name] |
| D3 | [Beschreibung] | [Cat] | [Name] |
| ... | ... | ... | ... |

---

## 4. Konvergente Phase — Ergebnis

### 4.1 Technik eingesetzt

```
Technik: [Dot-Voting / Impact-Effort / RICE / etc.]
Dauer: [X Minuten]
Kriterien: [Falls Weighted]
```

### 4.2 Priorisierte Top 5

| Rank | ID | Idee | Score/Votes | Next |
|------|----|------|-------------|------|
| 1 | D7 | [Beschreibung] | [Score] | Action |
| 2 | D3 | [Beschreibung] | [Score] | Action |
| 3 | D12 | [Beschreibung] | [Score] | Action |
| 4 | D5 | [Beschreibung] | [Score] | Action |
| 5 | D9 | [Beschreibung] | [Score] | Action |

### 4.3 Begründung Top 3

```
**#1 (D7):**
- Warum Top: [Business Value, Feasibility, Strategic Fit]
- Owner: [Name]
- Deadline: [Datum]

**#2 (D3):**
- Warum Top: [Gründe]
- Owner: [Name]
- Deadline: [Datum]

**#3 (D12):**
- Warum Top: [Gründe]
- Owner: [Name]
- Deadline: [Datum]
```

---

## 5. Decision-Log

### 5.1 Entscheidungen

| Decision | Option A | Option B | Gewählt | Warum |
|----------|----------|----------|---------|-------|
| [Thema] | [Option] | [Option] | [A/B] | [Begruendung] |

### 5.2 Offene Fragen

| Question | Owner | Due Date | Status |
|----------|-------|----------|--------|
| [Frage] | [Name] | [Datum] | Open |

### 5.3 Eskalationen

| Topic | Escalated To | Reason | Expected By |
|-------|--------------|--------|-------------|
| [Thema] | [Person/Role] | [Grund] | [Datum] |

---

## 6. Action-Items

### 6.1 Immediate (This Week)

| ID | Action | Owner | Due | Status |
|----|--------|-------|-----|--------|
| A1 | [Beschreibung] | [Name] | [Date] | Todo |
| A2 | [Beschreibung] | [Name] | [Date] | Todo |

### 6.2 Short-Term (This Month)

| ID | Action | Owner | Due | Status |
|----|--------|-------|-----|--------|
| A3 | [Beschreibung] | [Name] | [Date] | Todo |
| A4 | [Beschreibung] | [Name] | [Date] | Todo |

### 6.3 Backlog (Later)

| ID | Action | Owner | Review Date |
|----|--------|-------|-------------|
| A5 | [Beschreibung] | [Name] | [Date] |

---

## 7. Metriken

### 7.1 Session-Metriken

| Metrik | Wert | Target | Status |
|--------|------|--------|--------|
| Ideen gesamt | [X] | 50+ | ✅/⚠️/❌ |
| Teilnehmer | [X] | 4-8 | ✅/⚠️/❌ |
| Divergent-Zeit | [X Min] | 30-40 | ✅/⚠️/❌ |
| Convergent-Zeit | [X Min] | 20-30 | ✅/⚠️/❌ |
| Top 3 klar | [Ja/Nein] | Ja | ✅/❌ |

### 7.2 Business-Metriken (erwartet)

| Metrik | Baseline | Target | Uplift |
|--------|----------|--------|--------|
| Conversion | [X%] | [Y%] | [+Z%] |
| NPS | [X] | [Y] | [+Z] |
| Revenue | [X€] | [Y€] | [+Z€] |
| Cost | [X€] | [Y€] | [-Z€] |

---

## 8. Follow-up-Plan

### 8.1 Cadence

```
**48h:**
- [ ] Action-Items gestartet
- [ ] Offene Fragen geklärt
- [ ] Stakeholder update

**1 Woche:**
- [ ] Top 3 im Fortschritt
- [ ] Eskalationen resolved
- [ ] Next Sprint geplant

**4 Wochen:**
- [ ] Ergebnisse messbar
- [ ] ROI check
- [ ] Retrospective
```

### 8.2 Next Session (if needed)

```
**Datum:** [YYYY-MM-DD]
**Topic:** [Folge-Brainstorming]
**Open Points:** [Aus dieser Session]
**Participants:** [Same / Extended]
```

---

## 9. Handoff

### 9.1 Empfänger

| Role | Name |交付物 | Deadline |
|------|------|--------|----------|
| Product-Owner | [Name] | Top 3 Ideen | [Date] |
| Tech-Lead | [Name] | Feasibility-Check | [Date] |
| Design | [Name] | Wireframes | [Date] |
| Stakeholder | [Name] | Decision-Log | [Date] |

### 9.2 Format

- [ ] **Slack-Update** (Summary in Channel)
- [ ] **Email** (Full Output an Stakeholder)
- [ ] **Jira-Tickets** (Action-Items erstellt)
- [ ] **Confluence** (Dokumentation gepublished)
- [ ] **Meeting** (Handoff-Call angesetzt)

---

## 10. Appendix

### 10.1 Rohe Ideenliste (vollständig)

```
[Alle X Ideen aus divergenter Phase, unsortiert]
```

### 10.2 Voting-Rohdaten

```
[Alle Votes/Scores aus konvergenter Phase]
```

### 10.3 Fotos/Whiteboards

```
[Links zu Photos, Miro-Boards, FigJam-Files]
```

### 10.4 Tools verwendet

```
- [Tool 1] (URL)
- [Tool 2] (URL)
```

---

## Template-Checkliste vor Publish

- [ ] Meta-Infos vollständig
- [ ] Ziel dokumentiert (aus Zielklärung)
- [ ] Top 5 priorisiert
- [ ] Top 3 begründet
- [ ] Action-Items mit Ownern
- [ ] Follow-up-Dates gesetzt
- [ ] Handoff-Empfänger identifiziert
- [ ] Rohdaten im Appendix

---

**Source:** Brainstorming-Skill P0-Assets  
**Integration:** Nach jeder Session ausfüllen → Handoff an Product/Strategy/Engineering
