---
name: adversarial-review
description: "Run a structured adversarial multi-agent review loop on any significant document. Spawns parallel Opus reviewers with different critical lenses, collects structured redlines, then guides farsight through agree/disagree positioning and v2 production. SELF-TRIGGERING: load this skill and run the complexity self-assessment whenever you are about to produce or have just produced any substantial document — score it and offer the review loop if it qualifies. Also load when the user says things like: 'use the review team', 'get the review team on this', 'spin up the reviewers', 'have the team look at this', 'red-team this', 'redline this', 'challenge this', 'critique this', 'tear this apart', 'poke holes in this', 'stress test this', 'pressure test this', 'sanity check this', 'validate this', 'get a second opinion', 'before we build/implement/ship this'."
---

# Adversarial Review

Structured multi-agent review loop. Catches what a single agent misses.

**Session store:** `~/.openclaw/workspace/reviews/`  
**Process:** Init session → spawn Opus reviewers → collect redlines → position on each → produce v2 → deliver

---

## Complexity Self-Assessment

**Run this check whenever you produce a substantial document.** Score 1 point per signal present. If score ≥ 3, offer the review loop without being asked.

| # | Signal | Points |
|---|--------|--------|
| 1 | Has multiple interdependent components (failure in one affects others) | 1 |
| 2 | Involves schema changes, migrations, or index design | 1 |
| 3 | Irreversible or expensive to undo (data loss, structural rework) | 1 |
| 4 | Affects production systems, stored data, or external services | 1 |
| 5 | Introduces new abstractions, taxonomies, or data models | 1 |
| 6 | Has a defined sequence of steps where order matters | 1 |
| 7 | Contains security, access control, or permission logic | 1 |
| 8 | Will be acted on by code or agents without further human review | 1 |
| 9 | Document is longer than ~500 lines or covers 3+ distinct systems | 1 |
| 10 | Scott said "let's build this" or "implement this" at any point in the conversation | 1 |

**Score 0–2 → skip.** Simple doc, don't add noise.

**Score 3–6 → offer.** *"This scores [N]/10 on complexity. Want me to run the review team on it before we act?"*

**Score 7–10 → strongly recommend.** Don't just offer — make the case. *"This scores [N]/10 on complexity — multiple interdependent systems, production consequences, hard to reverse. I'd strongly recommend running the review team before we act on this. Today's taxonomy strategy was a 10/10 and the review caught 14 issues including multiple production-breaking bugs."*

---

## Quick Reference

| Step | Action |
|------|--------|
| 0. Init session | `scripts/new-review.sh <slug> <path-to-doc>` |
| 1. Choose reviewers | Read `references/review-types.md` for the right bundle |
| 2. Spawn reviewers | `sessions_spawn` with `model=anthropic/claude-opus-4-6`, `mode=run` — all in parallel |
| 3. Wait | Reviewers auto-announce. Do NOT poll. |
| 4. Save raw output | Write each reviewer result to `redlines/reviewer-{role}.md` |
| 5. Synthesize | `scripts/synthesize.sh <session-dir>` → writes `redlines/combined.md` |
| 6. Position | AGREE / DISAGREE / MODIFY on every redline → write `positions.md` |
| 7. Produce v2 | Write `output/{slug}-v2.md` incorporating accepted changes + rejected appendix |
| 8. Deliver | `scripts/cp-output.sh <session-name> <destination>` |

---

## Session Directory Structure

```
~/.openclaw/workspace/reviews/{YYYY-MM-DD}-{slug}/
├── input/
│   └── {original-filename}       ← copy of doc being reviewed
├── redlines/
│   ├── reviewer-{role}.md        ← raw output per reviewer
│   └── combined.md               ← synthesize.sh output (sorted by severity)
├── positions.md                  ← farsight agree/disagree log
└── output/
    └── {slug}-v2.md              ← final document
```

---

## Review Types

| Document Type | Reviewer A | Reviewer B |
|---------------|-----------|-----------|
| Architecture / strategy | Theory & data modeling | Implementation & systems |
| Pipeline / workflow | Sequencing & dependencies | Failure modes & ops |
| Schema / migration | SQL correctness & constraints | Performance & indexes |
| Security design | Threat modeling | Implementation gaps |
| Marketing / positioning | Message clarity & truth | Competitive exposure |
| API / interface design | Consistency & contracts | Consumer experience |

For full persona prompt templates → read `references/reviewer-personas.md`  
For pre-configured bundles → read `references/review-types.md`

---

## Spawning Reviewers

Spawn ALL reviewers simultaneously — parallel, not sequential. Independent reviewers find different issues.

### Model Selection

| Doc Score | Default Model | Rationale |
|-----------|--------------|-----------|
| 7–10 | `anthropic/claude-opus-4-6` | Deep reasoning required; subtle architectural flaws need Opus |
| 3–6 | `anthropic/claude-sonnet-4-6` | Worth trying; structured prompts may close the gap |

**A/B testing note:** If Sonnet misses a CRITICAL issue that Opus would have caught on a 3–6 doc, upgrade that doc type to Opus permanently. Track findings in `references/model-notes.md` as patterns emerge.

Key parameters for every reviewer spawn:
```
model: anthropic/claude-opus-4-6   ← or sonnet for 3-6 scored docs
mode: run
runTimeoutSeconds: 300
label: reviewer-{role}
```

The task field contains the full reviewer prompt from `references/reviewer-personas.md` plus the document content to review.

---

## Positioning Rules

For EVERY redline, take an explicit position. No skipping.

| Position | When | Requirement |
|----------|------|------------|
| **AGREE** | Critique is correct, change should be made | State what changes |
| **DISAGREE** | Original design is defensible | Must provide rationale — not just dismissal |
| **MODIFY** | Issue is real, suggested resolution is wrong | Propose your alternative |

All CRITICAL redlines default to AGREE unless strongly defensible.  
At least 1 DISAGREE expected — if zero, you may be rubber-stamping.

Write positions to `positions.md` in the session directory.

---

## v2 Requirements

- Revision table at the top (what changed and why)
- All AGREE + MODIFY changes incorporated
- Rejected redlines documented in an appendix ("considered and rejected")
- Version bumped, date updated
- Saved to `output/{slug}-v2.md`

---

## Quality Bar

A good review session produces:
- ≥2 CRITICAL issues (if zero, reviewers weren't adversarial enough — re-spawn with harder prompt)
- ≥1 DISAGREE from farsight (if zero, consider whether the doc was genuinely perfect or just unchallenged)
- A v2 meaningfully different from v1

---

## Redline Format

```
**[REDLINE-{TYPE}-{NNN}]** {Section reference}
**Claim:** What the document says
**Challenge:** The specific objection or gap
**Severity:** CRITICAL | MAJOR | MINOR
**Suggested Resolution:** What should change
```

Full spec → read `references/redline-format.md`
