# Handoff Protocol — Ideen-Übergabe an andere Skills

**Use:** Nach Brainstorming: strukturierte Übergabe an Product-Owner, Engineering, Strategy.

---

## 1. Handoff-Übersicht

### 1.1 Wann handoff?

```
Nach Session: Top 3 Ideen → Product/Engineering
Nach Strategy-Session: Empfehlungen → Leadership
Nach Research-Session: Findings → Product Team
```

### 1.2 Handoff-Formate

| Format | Für | Inhalt |
|--------|-----|--------|
| **Brief** | Product-Owner | 1-Pager mit Idea + Rationale |
| **Spec** | Engineering | Detaillierte Anforderungen |
| **Executive Summary** | Leadership | ROI + Strategic Fit |
| **Research Report** | Research Team | Findings + Methodology |

---

## 2. Idea-to-Product Handoff

### 2.1 Standard Template

```markdown
# Idea Brief: [Name]

## 1-Pager (max 1 Seite)

**Submitted by:** [Name]  
**Date:** [YYYY-MM-DD]  
**Source Session:** [Session-ID]  
**Priority:** [P0/P1/P2]

---

### Problem/Opportunity
[2-3 Sätze: Was ist das Problem oder die Chance?]

### Solution Concept
[3-5 Sätze: Wie lösen wir das?]

### Target User
[Wer profitiert davon?]

### Expected Impact
- Revenue: €[X]/Monat oder +[Y]%
- Engagement: +[Z]% Retention
- Cost: -€[W]/Monat
- Sonstiges: [Qualitative Benefits]

### Effort Estimate
- Design: [X] Days
- Engineering: [Y] Sprints
- QA: [Z] Days

### Success Metrics
- Primary: [Metric]
- Secondary: [Metric]
- North Star: [Metric]

### Risks
- [Risk 1]
- [Risk 2]

### Dependencies
- [Dependency 1]
- [Dependency 2]

### Alternatives Considered
- [Alternative 1] — warum nicht gewählt
- [Alternative 2] — warum nicht gewählt

---

**Next Steps:**
- [ ] PO Review: [Datum]
- [ ] Design Sprint: [Datum]
- [ ] Engineering: [Datum]
```

### 2.2 PO Conversation Guide

```
SCRIPT für Übergabe-Gespräch mit PO:

"Vorab: Ich schicke dir den Idea-Brief.
Wir hatten gestern eine Brainstorming-Session zu [Topic].

Die Top-Idee ist [Name].
Kurz: [1-Satz-Erklärung]

Impact-Schätzung: [X] (Revenue/Engagement/Cost)
Effort: [Y] (Sprints/Days)

Ich würde gerne wissen:
1. Passt das zu unserer Roadmap?
2. Welche Infos fehlen noch?
3. Wann können wir weitermachen?"

Expected Response:
- "Ja, passt" → Backlog-Item erstellen
- "Ja, aber später" → Roadmap-Diskussion
- "Nein, passt nicht" → Rationale verstehen, ggf. andere Ideen
```

---

## 3. Idea-to-Engineering Handoff

### 3.1 Engineering Spec Template

```markdown
# Technical Spec: [Feature-Name]

## Context

**Problem:** [Link zu Problem Statement]  
**Solution:** [Link zu Idea Brief]  
**Stakeholder:** [PO Name]

## Goals

- [Goal 1]
- [Goal 2]

## Non-Goals (Out of Scope)

- [Item 1]
- [Item 2]

## User Stories

```
AS A [User Type]
I WANT [Action]
SO THAT [Benefit]

ACCEPTANCE CRITERIA:
- [ ] [Criteria 1]
- [ ] [Criteria 2]
```

## Technical Approach

### Architecture
[Diagramm oder Erklärung]

### API Design

```
POST /api/v1/[endpoint]
Request:
{
  "field": "value"
}

Response:
{
  "result": "success",
  "data": {}
}
```

### Data Model

```
Table: [Name]
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| ... | ... | ... |

```

### Dependencies

| Dependency | Version | Notes |
|-----------|---------|-------|
| [Library] | [Ver] | [Notes] |

### Security

- [Security Consideration 1]
- [Security Consideration 2]

## Testing Strategy

- Unit Tests: [Coverage Target]
- Integration Tests: [Scope]
- E2E Tests: [User Flows]

## Milestones

| Milestone | Date | Deliverables |
|-----------|------|--------------|
| M1: Design Done | [Date] | Figma Specs |
| M2: MVP Ready | [Date] | Working MVP |
| M3: GA | [Date] | Production |

## Open Questions

- [Question 1]
- [Question 2]
```

---

## 4. Strategy-to-Leadership Handoff

### 4.1 Executive Summary Template

```markdown
# Executive Summary: [Topic]

**Date:** [YYYY-MM-DD]  
**Prepared by:** [Names]  
**For:** [Leadership Team]

---

## Recommendation

**[Clear Statement of Recommendation]**

## Strategic Rationale

[3-4 Sätze: Warum ist das strategisch wichtig?]

## Market Opportunity

[TAM/SAM/SOM Analysis wenn relevant]

## Financial Impact

| Scenario | Year 1 | Year 2 | Year 3 |
|----------|--------|--------|--------|
| Conservative | €X | €Y | €Z |
| Base | €X | €Y | €Z |
| Optimistic | €X | €Y | €Z |

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk] | High | Medium | [Mitigation] |

## Required Decisions

- [Decision 1]
- [Decision 2]

## Required Resources

- Budget: €[X]
- Headcount: [X] FTE
- Timeline: [X] Months

## Next Steps

| Action | Owner | Due Date |
|--------|-------|----------|
| [Action] | [Name] | [Date] |

---

**Appendix A:** Detailed Analysis  
**Appendix B:** Supporting Data  
**Appendix C:** Alternative Options Considered
```

---

## 5. Research-to-Product Handoff

### 5.1 Research Report Template

```markdown
# Research Report: [Topic]

**Research Date:** [YYYY-MM-DD]  
**Methodology:** [User Interviews / A/B Test / Survey / etc.]  
**Participants:** [N=XX]

---

## Key Findings

### Finding 1: [Headline]
[2-3 sentences explaining the finding]

**Evidence:**
- [Quote / Data Point]
- [Quote / Data Point]

**Implication for Product:**
[What this means for product decisions]

### Finding 2: [Headline]
...

## User Quotes (Verbatim)

> "[Interesting quote 1]"

> "[Interesting quote 2]"

## Behavioral Patterns

1. [Pattern 1]
2. [Pattern 2]

## Opportunities

| Opportunity | Impact | Effort | Priority |
|-------------|--------|--------|----------|
| [Opportunity] | High | Medium | P1 |

## Recommendations

1. [Recommendation with rationale]
2. ...

## Limitations

- [Limitation 1]
- [Limitation 2]

## Appendix

- Full interview notes (link)
- Raw data (link)
- Survey instrument (link)
```

---

## 6. Handoff-Checkliste

### 6.1 Vor dem Handoff

```
□ Idee validiert (Kunden-Feedback?)
□ Impact geschätzt (Revenue/Engagement/Cost)
□ Effort geschätzt (Design/Engineering)
□ Risiken identifiziert
□ Konkurrenz-Analyse gemacht
□ Abhängigkeiten dokumentiert
□ Stakeholder-Alignment (intern)
```

### 6.2 Während Handoff

```
□ Brief/Spec verschickt (vor Meeting)
□ Meeting mit Empfänger (30 Min)
□ Q&A beantwortet
□ Nächste Schritte vereinbart
□ Timeline bestätigt
□ Owner zugewiesen
```

### 6.3 Nach dem Handoff

```
□ Follow-Up-Email verschickt
□ Action Items in Jira/Tool erstellt
□ Dokumentation in Wiki/Confluence
□ Feedback eingeholt (Handoff-Qualität)
□ Timeline überprüfen (48h, 1 Woche)
```

---

## 7. Handoff-Qualität

### 7.1 Quality Gates

| Gate | Kriterium | Wer prüft |
|------|----------|-----------|
| **G1: Completeness** | Alle Sections ausgefüllt? | Sender |
| **G2: Clarity** | Verständlich für Empfänger? | Empfänger-Feedback |
| **G3: Feasibility** | Effort realistisch? | Engineering |
| **G4: Alignment** | Passt zu Roadmap/Strategy? | PO/Leadership |
| **G5: Priority** | Korrekt priorisiert? | PO |

### 7.2 Feedback Loop

```
Nach Handoff (1 Woche später):
□ Empfänger gefragt: "War der Handoff hilfreich?"
□ Was fehlte?
□ Was war zu viel?
□ Wie können wir verbessern?

Feedback aggregieren und Prozess anpassen
```

---

## 8. Skill-Integration

### 8.1 Welche Skill für was?

| Skill | Output | Input für |
|-------|--------|-----------|
| **brainstorming** | Ideen, Prioritäten | product-owner, strategy |
| **product-owner** | User Stories, Backlog | engineering, design |
| **strategy** | Roadmap, OKRs | leadership, finance |
| **engineering** | Tech Specs, Code | qa, devops |
| **design** | Wireframes, Prototypes | user-research |

### 8.2 Handoff-Protokoll zwischen Skills

```
Brainstorming → Product-Owner:
  Input: Idea Brief (1-Pager)
  Output: User Stories, Acceptance Criteria, Priority
  Tool: [Jira/Linear/Asana]

Product-Owner → Engineering:
  Input: User Stories + Tech Spec
  Output: Sprint Tasks, Implementation
  Tool: [Jira/GitHub Projects]

Engineering → QA:
  Input: Test Cases, Spec
  Output: Test Results, Bugs
  Tool: [TestRail/Jira]

[Return Path:]
QA → Engineering → Product-Owner → Brainstorming: Retrospective/Learnings
```

---

## 9. Fehlervermeidung

### 9.1 Typische Fehler

| Fehler | Warum schlecht | Lösung |
|--------|---------------|--------|
| **Kein ROI** | Leadership kauft nicht | Impact immer quantifizieren |
| **Vage Idee** | Kann nicht umgesetzt werden | Konkretisieren vor Handoff |
| **Zu viel Content** | Overload, nichts gelesen | Max 1-Pager für Execs |
| **Kein Owner** | Verpufft | Immer Owner zuweisen |
| **Kein Follow-Up** | Keine Action | 48h Follow-Up erzwingen |
| **Wrong Audience** | Verpufft | Richtigen Empfänger wählen |

### 9.2 Best Practices

```
✅ Immer Impact quantifizieren (auch Schätzung)
✅ Max 1-Page für Leadership
✅ Nächste Schritte mit Deadlines
✅ Owner für jede Action
✅ Follow-Up nach 48h
✅ Feedback-Loop etablieren
✅ Skill-Integration nutzen
```

---

## 10. Handoff-Skills (Übergabe-Toolkit)

### 10.1 Slack/Teams Templates

```
/idea-brief:
[Automatischer Bot für Idea-Brief Template]

/handoff-check:
[Automatischer Check für Handoff-Qualität]

/feedback-loop:
[Automatische Follow-Up Erinnerung]
```

### 10.2 Jira/Linear Integration

```
Issue Type: Idea
Fields:
- Source Session: [Link]
- Impact: [€X oder %Y]
- Effort: [X Days]
- Priority: [P0-P4]
- Handoff Status: [Draft → Sent → Accepted → In Progress]
```

### 10.3 Notion/Confluence Template

```
Template: Idea Brief
- Copy link für jede neue Idee
- Review-Workflow automatisch
- Status-Tracking sichtbar
```

---

**Source:** Brainstorming-Skill P0-Assets  
**Integration:** Nach jeder Session für Top-Ideen
