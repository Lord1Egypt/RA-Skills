# Quality Checklist (Layer 5)

> **Role**: Final quality gate
> **Load Time**: Pipeline final step (Step 4)

---

## Check Sequence

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4
                              │
                              ▼
                         Load QUALITY
                              │
                              ▼
                    Check if output qualifies
                              │
                    ┌─────────┴─────────┐
                    │                   │
                  Pass              Fail
                    │                   │
                    ▼                   ▼
                Task Complete      Return to correct
```

---

## Generic Check Items

### Completeness
- [ ] All required sections completed
- [ ] No empty placeholders
- [ ] Logical coherence between steps

### Format Consistency
- [ ] Meets template requirements
- [ ] Consistent terminology
- [ ] Clear structure

### Content Quality
- [ ] Has substantial content (not placeholder fill)
- [ ] Logically coherent
- [ ] Conclusions have basis

---

## Checks by Combination

### Pipeline + research
- [ ] Executive summary complete (3-5 sentences)
- [ ] Each finding has source
- [ ] Confidence annotated
- [ ] Knowledge gaps identified

### Pipeline + subagent
- [ ] Task decomposition reasonable
- [ ] Sub-tasks independent
- [ ] Result merging complete

### Pipeline + context
- [ ] Snapshot records complete
- [ ] Key information preserved
- [ ] Task coherence verified

### Pipeline + analysis
- [ ] Scoring matrix complete
- [ ] Conclusions supported by data
- [ ] Suggestions actionable

---

## Output Format

```markdown
## Quality Check Report

### Passed Items
- [ ] {Passed 1}
- [ ] {Passed 2}

### Failed Items
- [ ] {Failed 1}
  - Problem: {Description}
  - Fix: {Suggestion}

### Final Verdict
✅ Pass / ❌ Needs Correction
```

---

_Last updated: 2026-04-07 by neltharion11 | https://github.com/neltharion11/skill-agent-harness_
