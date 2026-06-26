# Redline Format Specification

---

## Standard Format

Every redline must use this exact structure:

```
**[REDLINE-{TYPE}-{NNN}]** {Section reference}
**Claim:** What the document says (quote or close paraphrase)
**Challenge:** The specific objection or identified gap
**Severity:** CRITICAL | MAJOR | MINOR
**Suggested Resolution:** What should change
```

---

## ID Scheme

`REDLINE-{TYPE}-{NNN}`

**TYPE** — reviewer role tag (one per reviewer):
| Tag | Role |
|-----|------|
| `T` | Theory & Data Modeling |
| `I` | Implementation & Systems |
| `P` | Pipeline & Sequencing |
| `X` | Performance & Indexes |
| `S` | Security & Access |
| `M` | Positioning & Message |

**NNN** — sequential number within that reviewer's output (001, 002, etc.)

Examples: `REDLINE-T-001`, `REDLINE-I-007`, `REDLINE-P-003`

---

## Severity Definitions

### CRITICAL
The document is materially wrong in a way that will cause production failures, data loss, security breaches, or fundamental architectural breakdown if implemented as written.

Examples:
- SQL that will silently fail or produce wrong results
- A claim of atomicity that is architecturally impossible
- A safety gate that is bypassed by its own default values
- An index type that doesn't support the query operators used

### MAJOR
A significant design flaw that will cause problems at scale, create operational pain, or require expensive rework. Won't necessarily cause immediate failure but will cause regret.

Examples:
- Wrong data type for a use case (JSONB for boolean flags)
- Missing failure handling for a non-trivial failure mode
- Axis definitions that are correlated but treated as independent
- A state machine with unreachable or unexitable states

### MINOR
A correctness or clarity issue that should be fixed but won't cause serious harm. Polish.

Examples:
- A naming inconsistency between sections
- A default value that's technically correct but semantically confusing
- A missing edge case in documentation
- An example that uses deprecated syntax

---

## Deduplication Rules

When synthesizing multiple reviewer outputs, two redlines are the same issue if:
- They identify the same flaw in the same section
- Even if the framing or suggested resolution differs

**Resolution:** Keep the higher-severity version. Note in parentheses: `(also raised by REDLINE-I-003)`

---

## Linking Related Redlines

If two redlines are about the same root cause but different symptoms, link them:

```
**Suggested Resolution:** Fix X. Note: this is the root cause of REDLINE-T-002.
```

---

## Positions Format

In `positions.md`, document each position in this format:

```markdown
## [REDLINE-{TYPE}-{NNN}] — {AGREE | DISAGREE | MODIFY}

**Original claim:** {one sentence}
**Redline summary:** {one sentence}
**Position:** AGREE | DISAGREE | MODIFY
**Rationale:** {Why this position. Required for DISAGREE and MODIFY.}
**Change in v2:** {What specifically changes, or "No change — rejected."}
```

---

## Rejected Redlines Appendix

At the end of the v2 document, include:

```markdown
## Appendix: Considered and Rejected

The following redlines were reviewed and rejected. Documented here to prevent
re-raising in future review cycles.

### [REDLINE-T-002] — REJECTED
**Critique:** {summary}
**Reason for rejection:** {explanation}
```
