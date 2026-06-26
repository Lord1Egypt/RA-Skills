# Agent Collaboration & Governance

> Distilled from real-world human-agent research collaboration practice

## Human-Agent Governance

**Human owns direction. Agent executes, organizes, critiques, proposes — but never decides.**

Agent CAN:
- Run experiments automatically
- Write drafts and proposals
- Fix engineering issues (encoding, format, API)
- Generate anomaly reports
- Update artifacts with evidence status tracking

Agent CANNOT:
- Change the research question or baseline definitions
- Promote candidate evidence to verified without human review
- Adopt core claims or make academic decisions
- Skip logs, checkpoints, or anomaly reports
- Change protected surfaces (rubric, metrics, schema) silently

## Evidence Status Grading

All evidence from LLM output, web search, or Deep Research starts as `candidate`.

| Status | Meaning | Who can promote |
|--------|---------|----------------|
| candidate | Useful clue, unverified | — (starting state) |
| needs-review | Organized, has specific verification task | Agent |
| verified | Can be used as research fact | Human or back-to-source verification |
| rejected | Disproven or inapplicable | Human or agent with evidence |

**Rule**: Never promote from candidate to verified based on AI/chat/Deep Research material alone. The LLM may be confident and wrong.

**The `rejected` state matters**: Keep rejected evidence in the registry. This prevents the agent from rediscovering and reusing bad candidates in future iterations.

## Priority System

| Level | Situation | Action |
|-------|-----------|-------- |
| P0 | Results severely conflict with research direction | Stop, write report, wait for human |
| P1 | Claim definition, innovation, methodology needs academic judgment | Stop, write report, wait for human |
| P1 | Scoring cannot distinguish groups after one autonomous fix | Stop, write report, wait for human |
| P1 | Major uncertainty in literature or data science correctness | Stop, write report, wait for human |
| P2 | Engineering issues (format, script, API, encoding) | Fix, record, continue |

**The P1 scoring trap**: If the scorer cannot distinguish baseline from treatment after one fix attempt, the problem is likely fundamental — wrong rubric, broken pipeline, or insufficient signal. Do not iterate blindly. Escalate.

## Phase Gate Self-Review

Before advancing to the next phase, the agent must answer:

1. Are exit conditions complete? Are incomplete items marked `[PARTIAL]`?
2. Are artifacts written to the repo with clear paths?
3. Are there unresolved P0/P1 anomalies?
4. Was AI output treated as verified fact?
5. Did `validate_repo_state.py` report 0 FAIL?

A "yes" to question 4 is an automatic stop. A "no" to question 5 is an automatic stop.

## Upstream Proposal Format

Any insight affecting the research direction must be a proposal first:

```markdown
# Proposal: <topic>

## Trigger
Why is this proposal needed? What experiment, anomaly, or finding triggered it?

## Proposed Target
Which file or decision should this affect?

## Proposed Change
Specific proposed content.

## Evidence
- Source file / run log / result table
- Evidence status: candidate / needs-review / verified

## Risk
What might break if this is adopted? What is lost if it is not?

## Human Decision Needed
Yes/no, with reasoning.
```

Save to `sync/upstream_proposals/YYYY-MM-DD-topic.md`.

## Agent Onboarding: Alignment Doc

**Never pass long chat history to the next agent.**

Instead, write a short alignment doc (~1 page) with:
- Current state (1 paragraph)
- Entry files (5-6 max)
- New/changed surfaces
- Preflight commands + expected output
- Completed work summary
- Next steps
- Protected surfaces (forbidden actions)
- Open notes

This is the single most effective way to reduce context cost and onboarding errors.

## Daily Work Discipline

1. Every substantial work ends in a file, not an impression
2. Every phase ends in a checkpoint
3. Every anomaly ends in an anomaly report
4. Every upstream writeback starts as a proposal
5. Research material goes through intake before becoming survey or claim

## Non-Negotiables

1. No unverified citation becomes a research fact
2. No debug result becomes a formal result
3. No agent changes baseline, rubric, or metric definitions without a proposal
4. No raw result is overwritten
5. No failed experiment is deleted
6. No phase gate passes before validators report zero FAIL
