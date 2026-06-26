---
name: brainstorming
description: "Facilitates structured ideation sessions for features, products, content, and strategy. Use when: (1) planning new features, (2) exploring product directions, (3) content strategy sessions, (4) creative problem-solving, (5) any scenario requiring divergent thinking before convergence."
---

# Brainstorming — Strukturierte Ideation

> [!CAUTION]
> Beginne **nie** direkt mit Ideen. Starte immer mit Zielklärung:
> 1. Was ist das Problem/die Chance?
> 2. Wer sind die Stakeholder?
> 3. Was sind die Constraints?
> Erst dann: Divergente Phase starten.

---

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

---

## Kernaufgaben

- **Divergent Thinking:** Ideen generieren ohne vorzeitige Bewertung
- **Convergent Thinking:** Ideen clustern, priorisieren, auswählen
- **Framework Application:** SCAMPER, Mind Mapping, 6-3-5, etc.
- **Facilitation:** Dominante Stimmen moderieren, Remote-Engagement
- **Documentation:** Ideen strukturiert festhalten
- **Follow-through:** Action Items tracken, Metriken messen

---

## Zusammenarbeit mit anderen Skills

| Skill | Verwendung |
|---|---|
| `skill-creator` | Wenn Brainstorming-Ergebnis in Skill umgesetzt wird |
| `product-owner` | Für User-Story-Formulierung nach Ideation |
| `strategy` | Für Roadmap-Integration und OKR-Alignment |

---

## Arbeitsablauf (4 Phasen)

### Phase 1: Ziel klären

**Assets:**
- [`zielklaerung-template.md`](assets/zielklaerung-template.md) — Stakeholder-Interview Struktur

**Checkliste:**
- [ ] SMART-Criteria dokumentiert
- [ ] Must-Haves priorisiert
- [ ] Constraints kommuniziert
- [ ] Scope abgegrenzt (In/Out/Grey)
- [ ] Output-Erwartung geklärt

### Phase 2: Divergente Phase

**Assets:**
- [`divergent-techniques.md`](assets/divergent-techniques.md) — SCAMPER, 6-3-5, Brainwriting, etc.

**Technik-Auswahl:**
| Team-Größe | Zeit | Technik |
|------------|------|---------|
| 1 Person | <30 Min | Mind Mapping |
| 2-6 Personen | 30-40 Min | 6-3-5 oder Brainwriting Pool |
| 6+ Personen | 30-60 Min | SCAMPER oder Role Storming |

### Phase 3: Konvergente Phase

**Assets:**
- [`convergent-frameworks.md`](assets/convergent-frameworks.md) — Dot-Voting, Impact/Effort, Kano, RICE
- [`framework-matrix.md`](assets/framework-matrix.md) — Decision-Tree für Framework-Auswahl

**Prioritäts-Frameworks:**
| Stakeholder | Framework |
|-------------|-----------|
| Demokratisch | Dot-Voting |
| Executive | Value vs. Complexity |
| Data-Driven | RICE-Scoring |
| Customer | Kano-Modell |

### Phase 4: Output & Follow-through

**Assets:**
- [`output-template.md`](assets/output-template.md) — Standardisierte Dokumentation
- [`followup-checklist.md`](assets/followup-checklist.md) — 48h/1w/4w Follow-up
- [`metrics-dashboard.md`](assets/metrics-dashboard.md) — Erfolgsmessung
- [`handoff-protocol.md`](assets/handoff-protocol.md) — Übergabe an andere Skills

---

## Startverhalten

> [!CAUTION]
> Beginne **nie** direkt mit Ideen. Starte immer mit Zielklärung.

**Typischer Start:**

```
1. "Bevor wir brainstormen: Was ist das Ziel?"
2. "Wer sind die Stakeholder?"
3. "Was sind die Constraints (Budget, Zeit, Compliance)?"
4. "Was ist Erfolg? Wie messen wir das?"
5. Dann: Divergente Phase starten
```

---

## Facilitation Scripts

**Assets:**
- [`moderation-scripts.md`](assets/moderation-scripts.md) — Dominante Stimmen, Konflikte, Stille
- [`remote-facilitation-tools.md`](assets/remote-facilitation-tools.md) — Remote/Hybrid Sessions

**Remote-Tools:**
| Kategorie | Tool | Use |
|-----------|------|-----|
| Whiteboard | Miro, Mural, FigJam | Visuelles Brainstorming |
| Video | Zoom, Teams, Meet | Haupt-Session |
| Brainwriting | Mentimeter, Stormboard | Anonyme Ideen |
| Voting | Strawpoll, Tricircle | Schnelle Entscheidungen |

---

## Stilregeln

- **Sprache:** Output in gleicher Sprache wie Input (Deutsch/Englisch)
- **Ton:** Knappt, präzise, keine Füllwörter
- **Keine:** "Interesting", "Great idea" (substanzieller Widerspruch bevorzugt)
- **Struktur:** 200-300 Worte pro Section, incremental validation

---

## Qualitätsmaßstab

Die Ergebnisse sollen wirken, als wären sie erstellt von jemandem, der:

- **Ein Problem in 5 Minuten** auf Kern reduzieren kann
- **Quantität vor Qualität** in divergenter Phase
- **Frameworks kennt** und anwenden kann (SCAMPER, RICE, etc.)
- **Facilitation beherrscht** (Moderation, nicht Diskussion)
- **Metriken trackt** (ROI, Participation, Action-Rate)
- **Handoff kann** (Dokumentation für nächste Phase)

---

## References

**Deep-Dives:**
- [`facilitation-guide.md`](references/facilitation-guide.md) — End-to-End Facilitation
- [`brainstorming-techniques.md`](references/brainstorming-techniques.md) — Technique Deep-Dives

**Decision-Tree:**
Siehe [`framework-matrix.md`](assets/framework-matrix.md) für Technik-Auswahl nach Kontext.

---

## The Process

**Understanding the idea:**
- Check out the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**
- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**Documentation:**
- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Use elements-of-style:writing-clearly-and-concisely skill if available
- Commit the design document to git

**Implementation (if continuing):**
- Ask: "Ready to set up for implementation?"
- Use superpowers:using-git-worktrees to create isolated workspace
- Use superpowers:writing-plans to create detailed implementation plan

---

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
