---
name: architecture-critic
version: 1.1.0
requires:
  - python3
  - bash
credentials:
  - ANTHROPIC_API_KEY
description: >
  Adversarial pre-build architecture review. Spawns a structurally independent agent
  that reviews proposed builds, features, or operational decisions BEFORE any code is
  written. The critic sees only the task spec and codebase state — never conversation
  history, enthusiasm, or the proposer's reasoning. Returns APPROVE, REVISE, or REJECT
  with specific, itemized findings. Use when: starting any new feature, endpoint, schema
  change, payment/auth touch, or any decision being recommended with confidence.
  Skip only for: copy/style-only changes under 3 files with no logic, or isolated bug
  fixes that don't touch payment or auth.
---

# Architecture Critic

An adversarial pre-build agent. Its job is to find what's wrong with a proposed build before a single line of code is written.

This is not a collaborator. It does not refine the plan or suggest alternatives. It reads the proposal and returns a verdict with specific, itemized findings. No stake in the outcome. No relationship to protect.

**Cost to run: ~$0.05. Cost of skipping: a rework cycle.**

---

## When to Run

| Condition | Action |
|---|---|
| New API endpoint or route | Run |
| Schema change (DB table, migration) | Run |
| Payment or charge flow touched | Run |
| Auth logic touched | Run |
| Feature touching >3 files | Run |
| New external API integration | Run |
| Any decision being pitched with confidence | Run |
| Copy/style-only change, <3 files, no logic | Skip |
| Isolated bug fix, no payment/auth touch | Skip |

**When in doubt: run it.** The gate costs a fraction of a rework cycle.

---

## How to Run

```bash
# Write a DONE_WHEN brief to a temp file first
cat > /tmp/brief.md << 'EOF'
Goal: <what this build accomplishes>
Scope: <what files/systems are touched>
Done when: <specific acceptance criteria>
EOF

bash /path/to/skills/architecture-critic/scripts/run-critic.sh \
  --project <project-name> \
  --task "<short task description>" \
  --done-when /tmp/brief.md
```

**Exit codes:** `0` = APPROVE · `1` = REVISE · `2` = REJECT · `3` = ERROR

Verdict is saved to `specialists/critic-verdicts/YYYY-MM-DD-<slug>.md`.

---

## Critic System Prompt — v1.0 (LOCKED — never modify per task)

```
You are an adversarial architecture reviewer.
Your job is to find what is wrong with a proposed build before any code is written.

You have no knowledge of how the plan was developed, who proposed it, or why they think it will work.
You see only the task brief and the current state of the codebase.

Your mandate:
- Find scope violations: does this touch more than it should?
- Find missing pieces: what's not in the plan that will be needed?
- Find integration risks: what existing systems could this break?
- Find security gaps: what data, auth, or payment flows are at risk?
- Find token/cost waste: is this approach more expensive than necessary?
- Find sacred file risks: does this approach put protected files at risk?
- Find architectural drift: does this duplicate logic that already exists?
- Find deployment risks: what could break in production that won't show in dev?

Return one of three verdicts:

APPROVE — the plan is sound. List any minor WARNs.
REVISE — specific correctable problems. List each with exact fix required. Build does not start until addressed.
REJECT — fundamental problems requiring redesign. Do not patch — redesign.

Be specific. Be uncharitable. Do not validate effort or intent.
Temperature: 0.
```

This prompt is versioned and frozen. It never changes per task. The critic's structural independence is the point.

---

## Verdict Protocol

**APPROVE** → Build proceeds. Log any WARNs to specialist log before starting.

**REVISE** → Build does NOT start. Address every listed item. Update the brief. Re-run critic. Max 2 REVISE cycles before escalating to a human.

**REJECT** → Build STOPS. Notify immediately. No build proceeds until a human approves a redesigned approach.

---

## Verdict File Format

Saved to `specialists/critic-verdicts/YYYY-MM-DD-<task-slug>.md`:

```markdown
# Critic Verdict — <task-slug>
Date: YYYY-MM-DD
Project: <project>
Task: <description>
Spec version: v1.0
Verdict: APPROVE | REVISE | REJECT

## Findings
[itemized — empty if APPROVE with no WARNs]

## WARNs (non-blocking)
[itemized]

## Decision
[one paragraph — what the critic concluded and why]
```

---

## Domain Checklists

For web/API projects, load `references/checklist-web.md` and pass it to the critic.
For general/non-web projects, use `references/checklist-general.md`.

The run script handles this automatically when `--checklist` is passed.

---

## Independence Rules

1. Critic agent spawned fresh for every review — no accumulated context
2. Receives ONLY: task brief, codebase state, system prompt, optional checklist
3. System prompt never modified per task
4. Verdict written to file BEFORE any build agent starts
5. Critic infrastructure down → build is BLOCKED (no pass-through)
