# Mode Advisor — Unified Cross-Skill Decision Tree

## Purpose

Helps users (and the pipeline orchestrator) select the right skill and mode for their current situation. Eliminates the most common routing mistakes by mapping user intent to the optimal entry point.

---

## Quick Decision Matrix

| What do you want? | How far along? | Time? | Skill + Mode |
|-------------------|---------------|-------|--------------|
| Explore a topic | Starting fresh | 30 min | ars-deep-research quick |
| Explore a topic | Starting fresh | 2+ hr | ars-deep-research full |
| Think through a research idea | Have vague idea | Any | ars-deep-research socratic |
| Systematic review | Have clear PICO | 3+ hr | ars-deep-research systematic-review |
| Verify claims | Have specific claims | 30 min | ars-deep-research fact-check |
| Write a paper | Have research done | 2+ hr | ars-academic-paper full |
| Plan a paper step by step | Have RQ, need structure | 1+ hr | ars-academic-paper plan |
| Fix citations | Have draft | 30 min | ars-academic-paper citation-check |
| Convert format | Have final draft | 15 min | ars-academic-paper format-convert |
| Review a paper | Have paper to evaluate | 1 hr | ars-academic-reviewer full |
| Check revision quality | Have revised draft | 30 min | ars-academic-reviewer re-review |
| Full pipeline (zero to publication) | Starting fresh | 5+ hr | ars-pipeline-orchestrator |
| Handle real reviewer feedback | Have review comments | 1+ hr | ars-pipeline-orchestrator (Stage 4 entry) |

---

## Common Misconceptions

| User Says | They Probably Need | Why |
|-----------|-------------------|-----|
| "Write me a paper on X" | ars-deep-research first, THEN ars-academic-paper | Writing without research produces shallow papers with unsupported claims |
| "Review my paper" (but no draft exists) | ars-academic-paper plan mode | They need to write first, not review |
| "Check my citations" (but paper isn't done) | ars-academic-paper full mode | Finish writing first, then check citations as a separate pass |
| "I need a systematic review" | ars-deep-research systematic-review mode | NOT ars-academic-paper lit-review structure (different methodology: PRISMA vs narrative) |
| "Just give me a quick paper" | ars-deep-research quick + ars-academic-paper full | Quick research is fine, but paper writing still needs the full mode for quality |
| "Format my paper as APA" | ars-academic-paper format-convert mode | Not a rewrite; purely formatting transformation |
| "I got reviewer comments" | ars-pipeline-orchestrator Stage 4 entry (External Review) | Needs structured intake + strategic coaching, not just "fix what they said" |

---

## User Archetype Recommendations

| Archetype | Recommended Workflow | Rationale |
|-----------|---------------------|-----------|
| Graduate student (first paper) | ars-deep-research socratic -> ars-academic-paper plan -> full pipeline | Socratic mode builds research thinking; plan mode structures the paper incrementally; pipeline ensures quality gates |
| Experienced researcher (submission prep) | ars-pipeline-orchestrator (full, from Stage 1 or mid-entry) | Knows what they want; benefits from the automated quality assurance and integrity checks |
| Advisor reviewing student work | ars-academic-reviewer full | Provides structured multi-perspective feedback the advisor can use in mentoring |
| Quick literature scan | ars-deep-research quick or lit-review | Fast turnaround; no need for full pipeline overhead |
| Journal revision response | ars-pipeline-orchestrator (Stage 4 entry with review comments) | External Review Protocol handles real reviewer feedback with strategic coaching |
| Conference paper (short deadline) | ars-deep-research quick -> ars-academic-paper full (conference type) | Compressed timeline; quick research + full writing with conference structure |
| Thesis chapter | ars-deep-research full -> ars-academic-paper full | Each chapter treated as a standalone paper; full depth needed |
| Policy brief | ars-deep-research quick -> ars-academic-paper full (policy_brief type) | Evidence-based but concise; quick research sufficient for policy scope |

---

## Skill Capability Boundaries

Understanding what each skill can and cannot do prevents misrouting:

| Skill | Can Do | Cannot Do |
|-------|--------|-----------|
| ars-deep-research | Literature search, synthesis, RQ refinement, fact-checking | Write papers, review papers, format documents |
| ars-academic-paper | Write papers, revise papers, format documents, check citations | Conduct original research, review papers (as reviewer), verify integrity |
| ars-academic-reviewer | Review papers (5-person panel), re-review revisions | Write papers, conduct research, fix issues (only identifies them) |
| ars-pipeline-orchestrator | Orchestrate all stages, manage transitions, track state | Perform any substantive work (purely dispatching and coordinating) |
| integrity_verification_agent | Verify references, citations, data, originality | Fix issues (only identifies them), review paper quality |

---

## Decision Flowchart

```
START: What does the user want?
  |
  +--> "I want to research/explore/investigate"
  |      |
  |      +--> Have specific claims to verify? --> ars-deep-research fact-check
  |      +--> Have clear PICO/systematic question? --> ars-deep-research systematic-review
  |      +--> Want guided exploration? --> ars-deep-research socratic
  |      +--> Want direct results, have time? --> ars-deep-research full
  |      +--> Want direct results, short on time? --> ars-deep-research quick
  |
  +--> "I want to write a paper"
  |      |
  |      +--> Have research/literature ready? --> ars-academic-paper (plan or full)
  |      +--> No research done yet? --> ars-deep-research FIRST, then ars-academic-paper
  |      +--> Want full quality assurance? --> ars-pipeline-orchestrator (from Stage 1)
  |
  +--> "I want someone to review my paper"
  |      |
  |      +--> Have a complete draft? --> ars-academic-reviewer full
  |      +--> Want integrity check + review? --> ars-pipeline-orchestrator (Stage 2.5 entry)
  |      +--> No draft yet? --> ars-academic-paper first
  |
  +--> "I need to revise based on feedback"
  |      |
  |      +--> From AI reviewers (pipeline)? --> Continue pipeline (Stage 4)
  |      +--> From real journal reviewers? --> ars-pipeline-orchestrator Stage 4 entry (External Review)
  |
  +--> "I want the full treatment (research to publication)"
         |
         +--> ars-pipeline-orchestrator (Stage 1 entry)
```

---

## Pipeline Stage Entry Points

For users entering the pipeline mid-stream, this table clarifies what materials are needed:

| Entry Point | Required Materials | What Gets Skipped | Integrity Implications |
|------------|-------------------|-------------------|----------------------|
| Stage 1 (RESEARCH) | None | Nothing | Full pipeline |
| Stage 2 (WRITE) | RQ Brief + Bibliography | Stage 1 | Full pipeline from Stage 2 |
| Stage 2.5 (INTEGRITY) | Paper draft | Stages 1-2 | Integrity check runs on provided draft |
| Stage 3 (REVIEW) | Verified paper + integrity report | Stages 1-2.5 | User must provide integrity evidence |
| Stage 4 (REVISE) | Paper + review comments | Stages 1-3 | Pipeline runs Stage 4 -> 3' -> 4' -> 4.5 -> 5 |
| Stage 5 (FINALIZE) | Paper + integrity pass report | Stages 1-4.5 | Must show Stage 4.5 passed |

---

## Anti-Patterns

These are common workflow mistakes to avoid:

| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|-----------------|
| Skipping research | Paper lacks evidence depth | Always do at least ars-deep-research quick |
| Writing then researching | Confirmation bias in source selection | Research first, write second |
| Reviewing before integrity check | Wasted review effort on fabricated citations | Always Stage 2.5 before Stage 3 |
| Accepting all reviewer comments blindly | May introduce inconsistencies or weaken valid arguments | Use External Review Protocol's strategic coaching |
| Running pipeline for a 1-page abstract | Overhead far exceeds benefit | Use ars-academic-paper full directly |
| Using fact-check mode for literature review | Different purpose and methodology | Use ars-deep-research full or systematic-review |
