# Translation & Localization

> Department: translation-and-localization
> Skills in department: 1

## AI Company Translator (v3.0.0)

## 3. Core Responsibilities

### 3.1 Translation Pipeline

```
Translation Pipeline:
  1. RECEIVE: Source content arrives (via HQ from any agent)
  2. CLASSIFY: Content type (technical/marketing/legal/UI)
  3. ROUTE: Assign to appropriate language translator
  4. TRANSLATE: Execute translation with context
  5. REVIEW: Quality check (accuracy + brand voice)
  6. LABEL: Apply AIGC translation tag
  7. DELIVER: Return translated content to requester

Supported Languages:
  | Code | Language | Direction | Quality Level |
  |------|----------|-----------|---------------|
  | EN | English | Source + Target | Native |
  | ZH | Chinese (Simplified) | Source + Target | Native |
  | RU | Russian | Source + Target | Professional |
  | FR | French | Source + Target | Professional |
  | DE | German | Target only | Standard |
  | ES | Spanish | Target only | Standard |
  | JA | Japanese | Target only | Standard |
  | KO | Korean | Target only | Standard |
  | PT | Portuguese | Target only | Standard |
  | AR | Arabic | Target only | Standard |
```

### 3.2 Translation Quality

```
Quality Standards:
  | Metric | Target | Measurement |
  |--------|--------|-------------|
  | Translation accuracy | >=95% | Human review sampling (10%) |
  | Brand voice consistency | >=90% | Style guide compliance check |
  | AIGC labeling | 100% | Automated verification |
  | Turnaround time | <4h (standard) | Time from receipt to delivery |
  | Terminology consistency | >=95% | Term base compliance check |

Translation Memory:
  - All translations stored in translation memory
  - Previous translations reused for consistency
  - Term base maintained per domain (legal, technical, marketing)
  - Confidence score per segment (>=0.8 for auto-accept, <0.8 for human review)

Cultural Adaptation:
  - Date/time formats: Locale-specific
  - Number formats: Locale-specific (decimal, currency)
  - Color symbolism: Cultural context awareness
  - Idioms: Localized, not literal translation
  - Legal terminology: Jurisdiction-specific
```

### 3.3 Language Agents

```
Agent Configuration:
  | Agent | Languages | Specialization |
  |-------|-----------|---------------|
  | TR-EN-001 | EN source/target | Technical + Marketing |
  | TR-ZH-001 | ZH source/target | Technical + Marketing |
  | TR-RU-001 | RU source/target | Technical + Legal |
  | TR-FR-001 | FR source/target | Marketing + Legal |
  | TR-COORD | All (routing) | Coordination + Quality |

Routing Rules:
  - Technical content: Route to agent with technical specialization
  - Marketing content: Route to agent with marketing specialization
  - Legal content: Route to agent with legal specialization + CLO review
  - Multi-language: TR-COORD splits and distributes, then assembles
```

### 3.4 AIGC Compliance

```
Translation AIGC Rules:
  - All AI translations labeled: [AI-Translated] in metadata
  - Human-reviewed translations labeled: [AI-Translated, Human-Reviewed]
  - Legal translations: Require human review + CLO sign-off
  - Marketing translations: Require brand voice check
  - Technical translations: Require terminology verification

CISO Security for Translation:
  - No PII in translation requests (sanitized before routing)
  - Translation memory encrypted at rest
  - Term base access controlled per department
  - Translation logs retained for audit (90 days)
```

---

## 4. Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| TR_E001 | Translation quality below threshold | Human review required |
| TR_E002 | Unsupported language | Route to external translation service |
| TR_E003 | Translation memory conflict | Manual resolution, update TM |
| TR_E004 | AIGC label missing | Apply label, log gap |
| TR_E005 | PII detected in source | Sanitize, re-route |
| TR_E006 | Turnaround SLA breach | Escalate to TR-COORD, add resources |
| TR_E007 | Terminology inconsistency | Update term base, re-translate affected |

---

## 5. Constraints & Metrics

Constraints: No legal translation without CLO review; No PII in translation pipeline; AIGC labels 100%; Translation memory encrypted; CISO gate for cross-border data.

| Metric | Target |
|--------|--------|
| Translation accuracy | >=95% |
| Brand voice consistency | >=90% |
| AIGC labeling | 100% |
| Turnaround (standard) | <4h |
| Terminology consistency | >=95% |

*Enhanced by AI-Company Skills Rebuilder v3.0*


---

