---
name: build-protocol
description: "Rigorous workflow for producing long-form knowledge content (textbooks, knowledge bases, deep reports) with multi-agent collaboration. Use when the task requires >5,000 words, >2 parallel sub-agents, or >10 steps, or when the deliverable will be referenced long-term by the user. Enforces 8 iron rules (independent Audit unmissable / Plan before Execute / ≤2 parallel sub-agents for writing tasks / Why This Way reasoning / version + errata iteration / 3-layer consistency / anti-sycophancy content / independent review ≠ self-audit) and a 9-step standard workflow. Includes machine-verification scripts for PMID citations, red/green evaluation ratios, safety-keyword coverage, and H1-level checks. Triggers on explicit requests like 'build knowledge base / textbook / deep report' or implicitly on any long-form knowledge production."
version: 1.0.1
---

# Build Protocol

> Turn "write a knowledge product" into a rigorous 9-step workflow with machine-verifiable quality gates.
>
> Distilled from 4 battle-tested projects: a multi-chapter AI/ML textbook, a tactical gear knowledge base, a supplements knowledge base, and a product design doc series.

## When to Use

**Triggers** (any one):
- Task will produce > 5,000 words
- Requires > 2 sub-agents
- Requires > 10 steps
- User will reference the deliverable long-term (textbook / knowledge base / deep report)
- Explicit requests: "build knowledge base", "write textbook", "做知识库", "做教材"

**Don't use for**:
- One-off Q&A
- Simple documentation
- Engineering/code projects (use a separate build-protocol-engineering skill)
- Short reports (<5k words)

## The 8 Iron Rules

| # | Rule | Why |
|---|---|---|
| 1 | **Independent Audit unmissable** | LLM self-review has 30% lower accuracy (sycophancy) |
| 2 | **Plan before Execute** | Drift cost >> planning cost |
| 3 | **≤2 parallel sub-agents** | Conflict points grow as N(N-1)/2; 4+ concurrent = 75% failure |
| 4 | **Why This Way** | Force reasoning over authority ("best practice" = zero-cost lie) |
| 5 | **Version + Errata iteration** | Honest revision > pretending to get it right once |
| 6 | **3-layer consistency** | Naming ↔ Business ↔ Data |
| 7 | **Anti-Sycophancy content** | Must have 🔴 negatives; all-green = fake |
| 8 | **Independent review ≠ self-audit** | Writer and reviewer must be different agents |

## The 9-Step Workflow

```
1. Plan      → Outline + sub-agent allocation + time estimate
2. Prepare   → Extract content (≤3000 chars per sub-agent task)
3. Execute   → Dispatch sub-agents (≤2 parallel, jittered start)
4. Assemble  → Merge files, unify format
5. Review    → Lightweight review (format / dirty markers)
6. Audit     → Deep audit (L1 facts / L4 safety / L6 anti-sycophancy) ⚠️ unmissable
7. Fix       → Fix 🔴 > 🟡 > 🟢 in order
8. Publish   → Convert to docx + upload + VERIFY
9. Errata    → Subsequent issues → v1.x Changelog
```

**Each step has a completion checkpoint** — see `references/workflow-checkpoints.md`.

## Machine-Verified Quality Gates

Before **Step 8 (Publish)**, run `audit_check.sh` (see `references/audit-script-template.sh`) to verify:

- **L1.1 Citation count**: Each volume ≥ threshold (e.g., ≥5 PMIDs for medical)
- **L1.2 Citation duplicates**: Zero duplicates (`sort | uniq -c | awk '$1>1'` returns empty)
- **L3 Length**: Each volume ≥ 6,000 chars (for "full volume" style)
- **L3 Gender balance**: Male & female perspectives both present (if applicable)
- **L4 Safety coverage**: ≥3 safety keywords per volume (for health/medical content)
- **L5 H1 count**: Exactly 1 per file (no stray H1 from sub-agents' progress markers)
- **L6 Red count**: Each volume has ≥1 🔴 critical review; ideally 🔴 ≥ 20% of 🟢

**🔴 fails block publishing**. 🟡 can defer to next version.

## Audit Fallback (when Audit sub-agent fails)

| Scenario | Fallback |
|---|---|
| Single-model timeout | Retry with different model / region |
| 3+ models all timeout | Main agent audits manually (use Opus-tier model + grep scripts) |
| Time-pressed / context >85% | Reduce scope: L1 + L4 only, skip L5/L6 |
| Audit quality poor (<10 real issues) | Dispatch second audit agent for cross-validation |

Main-agent audit has advantages: stronger model, machine-scripted checks, no idle-timeout risk.

## Sub-agent Specification Template

Every sub-agent task must include:

```
1. Goal:        What to do (one sentence)
2. Output:      Which file, what format
3. Content:     Key info provided directly (don't make sub-agent hunt through large files)
4. Constraints: What NOT to do (as important as "what to do")
5. Acceptance:  Measurable completion criteria
```

Single-file content in task instructions: **≤3,000 chars** (just-in-time context principle).

## Version Numbering

- **+0.1** → minor revision (≤3 small fixes per ~5k words)
- **+1.0** → major version (≥50k words or ≥3 new chapters or architecture change)

Keep only latest version in the delivery folder; archive old versions to `HistoryBackup/`.

## Each Release Requires a Changelog

```markdown
## v1.1 · YYYY-MM-DD
- 🔴 Fixed: [blocker issue X]
- 🟡 Added: [improvement Y]
- 🟢 Deferred to v1.2: [minor issue Z]
```

## Anti-Patterns (DO NOT)

| ❌ Don't | Why |
|---|---|
| "I already reviewed it" | Implementer = LLM. Must independently verify. |
| "Time is tight, ship it" | Time tight = reduce scope, never reduce standards |
| Let writer sub-agent self-review | Sycophancy guarantees overestimation |
| Skip Audit because sub-agent failed | Use fallback path, don't skip |
| Version-bump without Changelog | Silent changes destroy trust |
| "Mostly correct, minor issues" | Details = professionalism; 🟡 issues are tracked |
| Copy existing review grades (all 🟢) | Real world has 🔴; all-green = fake |
| 4+ parallel sub-agents | 75% failure rate; use 2+2+1 batching instead |

## Gotchas

1. **Sub-agent progress markers leak to output** — check for `# progress: step X/N` in deliverables; grep and remove before Audit
2. **Same-region concurrent dispatch causes throttling** — jitter second sub-agent by 1-3s; use different Bedrock regions if available
3. **Fix step can introduce new duplicates** — always re-run `audit_check.sh` after Step 7; don't skip "verify after fix"
4. **`uniq -c` must reveal zero duplicates** — don't just count totals; count uniques and compare
5. **Upload/move can hit resource contention** — retry individually; don't parallelize moves >2 at once
6. **Single docx upload loses folder_token parameter** — use 3-step: upload (to root) → move (to folder) → verify

## References

- `references/workflow-checkpoints.md` — Detailed checkpoint for each of the 9 steps
- `references/audit-script-template.sh` — Bash template for machine-verified Audit
- `references/subagent-spec-examples.md` — Example sub-agent task specs for different domains
- `references/case-study-supplements.md` — Full case study: Supplements Knowledge Base v1.0 → v1.1 (includes the 5 blind spots found via dogfood)

## Related Skills

- `skill-distiller` — This skill was created by distilling `BUILD-PROTOCOL.md` (see that file in workspace)
- `pptx-presentation-builder` — For PPT-specific knowledge products
- Future: `build-protocol-engineering` — For software/design projects (separate rulebook)

## Why This Way (Meta)

**Why not just write a long prompt each time?**
LLM behavior degrades with context length and prompt complexity. A rules-as-file approach + machine verification scripts catches more issues than any one-shot prompt. Distilling this as a **skill** means: future-me gets automatic loading when the OpenClaw matcher sees trigger words, without having to re-invent the workflow.

**Why independent Audit is unmissable?**
Research: LLMs self-reviewing their own output show ~30% sycophantic bias. The writer agent cannot objectively grade itself. An Audit agent (or main-agent with different context) operating on the deliverable alone — without seeing original requirements — produces harder judgments.

**Why ≤2 parallel sub-agents (for writing tasks)?**
Multi-agent conflict points grow as N(N-1)/2. For long-form writing tasks specifically, where output coherence matters and sub-agents share file regions, 4+ concurrent sub-agents hit 75% failure (timeout / throttling / thundering herd on same API region). 2 parallel is the sweet spot; 2+2+1 batching for 5-agent workloads.

For non-writing agentic tasks (independent file outputs, less coherence-sensitive), the cap can be relaxed up to 4. See `trinity-harness` for the general-purpose ceiling.

**Why quantify anti-sycophancy?**
Soft rules ("have some negatives") get ignored. Hard quantitative rules ("🔴 count ≥ 20% of 🟢 count") can be machine-verified. `grep -c "🔴" file.md` enforces the rule; grep finds what opinions miss.

---

_Distilled: 2026-04-29 · Source: BUILD-PROTOCOL.md v1.1 (refined through dogfood)_
_Validated on: AI/ML textbook, tactical gear KB, supplements KB (v1.0 → v1.1 dogfood)_
