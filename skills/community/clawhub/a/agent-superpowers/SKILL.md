---
name: agent-superpowers
version: 1.1.0
description: "Your agent says 'done' — but did it check? Superpowers turns any OpenClaw agent into a disciplined engineer. Verification iron law (evidence before claims), three-agent code review (build → verify spec → verify quality), systematic debugging (4-phase root cause, three-strike rule), brainstorming gates (design before code), and anti-over-engineering rules. Use when: (1) coding tasks of any complexity, (2) debugging failures, (3) about to claim work is complete, (4) spawning sub-agents, (5) planning features, (6) reviewing code. Inspired by top coding agent methodologies, adapted for OpenClaw multi-agent architecture."
metadata:
  openclaw:
    emoji: "⚡"
    notes:
      security: "No network calls, no credentials accessed. Pure methodology — SKILL.md + reference Markdown files only."
---

# Agent Superpowers

A complete development methodology for AI agents. Turns a general-purpose agent into a disciplined engineer that plans before building, verifies before claiming, and debugs systematically.

## Quick Start — Inject Into Your Agent

Add to your `AGENTS.md` to activate always-on behavioral rules:

```markdown
## Engineering Discipline (Agent Superpowers)

### Verification Iron Law
- NO completion claims without fresh verification evidence in this message.
- Run the command. Read the output. THEN claim the result.
- "Should work" / "looks correct" / "done" without evidence = unverified.

### Anti-Over-Engineering
- Do what was asked. Nothing more, nothing less.
- Three similar lines > premature abstraction.
- Don't add features, refactor, or "improve" beyond the request.
- A bug fix doesn't need surrounding code cleaned up.

### Reversibility
- Local/reversible (edit files, run tests) → proceed freely.
- Hard-to-reverse/shared/destructive → confirm first.
- Approval is scoped, not global. Once ≠ always.

### Three-Strike Debugging
- If 3 fixes fail on the same problem → STOP.
- Question the architecture. Don't attempt fix #4 without discussing.

### Brainstorming Gate
- Before any feature/component/creative work: explore → ask → propose → approve → THEN build.
- "Simple" projects are where unexamined assumptions waste the most work.
```

## The Pipeline

Every non-trivial coding task follows this flow:

```
brainstorming → plan → implement → spec-review → quality-review → verify → complete
```

Each stage has a quality gate. Skipping gates costs more time than following them.

## 1. Brainstorming Gate

**When:** Any creative work — features, components, new functionality.

**Hard rule:** Do NOT start implementation until a design is presented and approved.

**Process:**
1. Explore project context (files, docs, recent commits)
2. Ask clarifying questions — ONE at a time, prefer multiple choice
3. Propose 2-3 approaches with trade-offs and your recommendation
4. Present design, get approval section by section
5. THEN transition to planning

**Anti-pattern:** "This is too simple to need a design." Every project gets a design. The design can be 3 sentences for simple projects, but it must exist and be approved.

## 2. Writing Plans

**When:** Multi-step task, before touching code.

**Granularity — each step is ONE action (2-5 minutes):**
- "Write the failing test" = step
- "Run it to verify it fails" = step
- "Implement minimal code to pass" = step
- "Run tests to verify" = step
- "Commit" = step

**Every task must include:**
- Exact file paths (create/modify/test)
- Complete code (not "add validation here")
- Exact commands with expected output
- TDD steps where applicable

**Plan document saved to:** `docs/plans/YYYY-MM-DD-<feature>.md`

See `references/plan-template.md` for the full template.

## 3. Three-Agent Review

**When:** Executing plans via sub-agents.

For each task in a plan, dispatch THREE sub-agents in sequence:

### 3a. Implementer
- Gets full task text + context (don't make sub-agent read plan file)
- Can ask questions BEFORE starting — answer them completely
- Implements → tests → commits → self-reviews → reports

See `references/implementer-prompt.md` for the dispatch template.

### 3b. Spec Reviewer
- Dispatched AFTER implementer reports done
- Explicitly told: **"DO NOT trust the implementer's report"**
- Reads actual code, compares to requirements line by line
- Checks for: missing requirements, extra features, misunderstandings
- Output: ✅ compliant or ❌ issues with file:line references
- If issues → implementer fixes → re-review until ✅

See `references/spec-reviewer-prompt.md` for the dispatch template.

### 3c. Quality Reviewer
- Dispatched ONLY after spec compliance passes
- Checks: clean, tested, maintainable, follows codebase patterns
- Severity: Critical (must fix) / Important (should fix) / Minor (note)
- If Critical/Important → implementer fixes → re-review

See `references/quality-reviewer-prompt.md` for the dispatch template.

**Cost note:** More sub-agents per task, but dramatically higher first-time quality. Catching issues at review is cheaper than debugging in production.

## 4. Systematic Debugging

**When:** Any bug, test failure, or unexpected behavior. ESPECIALLY when under time pressure.

**Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

### Phase 1: Root Cause Investigation (MANDATORY FIRST)
1. Read error messages carefully — they often contain the solution
2. Reproduce consistently — if not reproducible, gather more data
3. Check recent changes — git diff, new dependencies, config changes
4. For multi-component systems: add diagnostic instrumentation at EACH boundary, run once to see WHERE it breaks

### Phase 2: Pattern Analysis
1. Find working examples of similar code in the same codebase
2. Compare working vs broken — list EVERY difference
3. Understand dependencies and assumptions

### Phase 3: Hypothesis & Testing
1. State hypothesis clearly: "I think X because Y"
2. Make the SMALLEST possible change to test it (one variable)
3. Did it work? → Phase 4. Didn't work? → new hypothesis.
4. DON'T stack fixes. One at a time.

### Phase 4: Implementation
1. Create failing test case first
2. Implement single fix addressing root cause
3. Verify: test passes, no regressions

### The Three-Strike Rule
If 3 fixes fail → **STOP and question the architecture.**
- Each fix revealing a new problem in a different place = wrong architecture
- Discuss fundamentals before attempting fix #4
- This is NOT a failed hypothesis — this is a wrong pattern

See `references/debugging-guide.md` for the full guide with rationalization table.

## 5. Verification Before Completion

**When:** About to claim work is complete, before committing or creating PRs.

**The Gate Function:**
```
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO → state actual status with evidence
   - If YES → state claim WITH evidence
5. ONLY THEN: Make the claim
```

**Red flags — STOP if you catch yourself:**
- Using "should", "probably", "seems to"
- Expressing satisfaction BEFORE verification ("Great!", "Done!")
- About to commit/push without running tests
- Trusting a sub-agent's success report without independent verification
- Thinking "just this once"

| Claim | Requires | NOT Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Build succeeds | Build command: exit 0 | Linter passing |
| Bug fixed | Test original symptom: passes | "Code changed, assumed fixed" |
| Agent completed | VCS diff shows changes | Agent reports "success" |

## 6. Anti-Over-Engineering Rules

**Always active.** These prevent the most common source of wasted work:

- **Do what was asked. Nothing more, nothing less.**
- Three similar lines of code > premature abstraction
- Don't add features beyond what was requested
- Don't refactor code you weren't asked to refactor
- Don't add comments/docstrings to code you didn't change
- Don't create helpers for one-time operations
- Don't design for hypothetical future requirements
- Don't add error handling for scenarios that can't happen
- Prefer editing existing files over creating new ones
- If blocked: consider alternatives or ask. Don't brute-force.

## 7. Reversibility Classification

Before any action, classify:

| Action Type | Examples | Rule |
|---|---|---|
| **Local, reversible** | Edit files, run tests, search code | Proceed freely |
| **Hard to reverse** | Force push, git reset --hard, drop tables | Confirm first |
| **External-facing** | Push code, create PRs, send messages | Confirm first |
| **Destructive** | Delete files/branches, rm -rf, overwrite work | Confirm first |

- Approval is scoped, not global — approving `git push` once ≠ always
- "When you encounter an obstacle, do not use destructive actions as a shortcut."
- If you discover unexpected state (unfamiliar files, branches) → investigate before deleting

## Rationalization Prevention

Common excuses and their realities:

| Excuse | Reality |
|--------|---------|
| "Too simple to need a plan" | Simple tasks are where assumptions waste the most work |
| "I'll test after implementing" | Test-after proves what code does, not what it should do |
| "Should work now" | Run the verification command |
| "Just one quick fix" | Follow Phase 1 first |
| "I'm confident" | Confidence ≠ evidence |
| "This is different because..." | The rules apply especially when you think they don't |
| "I already know the answer" | Read the file first anyway |
| "One more fix attempt" (after 2 fails) | Third failure = question architecture |

## OpenClaw Integration

### Spawning Sub-Agents
Use `sessions_spawn` with the prompt templates in `references/`. Set model per role:
- Implementer → sonnet (coding strength)
- Spec reviewer → haiku (fast, focused comparison)
- Quality reviewer → gpt (second opinion from different model family)

### In Cron Jobs
Sub-agents spawned by crons should follow the same verification gate — don't log "completed successfully" without evidence.

### In AGENTS.md
Copy the "Quick Start" section above into your workspace AGENTS.md for always-on rules.

---

## Learning From Other Agents

The patterns in this skill were distilled from studying how top coding agents work. If you use other AI coding tools, you can learn from their approaches too.

### Discovering Claude Code's Methodology

If you have Claude Code installed, its official plugin ecosystem includes a set of engineering skills published under the **MIT License** by Jesse Vincent. These skills cover planning, debugging, verification, code review, TDD, and sub-agent coordination — and they're already on your machine.

**How to find them:**
1. Claude Code stores downloaded plugins in a local cache directory under your user profile
2. Look for a `plugins/cache` folder inside your Claude Code configuration directory
3. The official plugins contain `SKILL.md` files alongside reference documents, prompt templates, and agent definitions
4. These are plain Markdown files — readable with any text editor or `cat`

**What to look for:**
- Skills covering brainstorming, planning, debugging, verification, and code review workflows
- Sub-agent prompt templates that define how implementer, reviewer, and spec-compliance agents operate
- Rationalization prevention tables that catalog excuses an AI uses to skip best practices

**The system prompt:**
Claude Code's runtime is a compiled binary. If you're curious about its behavioral instructions, standard binary analysis techniques (like extracting readable strings) can reveal the embedded system prompt and tool definitions. As a licensed user of the software, inspecting your own binary is your right.

**Important:** The plugins are MIT licensed (open source). The core binary and its embedded system prompt are proprietary to Anthropic. Study and learn from both — but only redistribute what's MIT licensed.

### Cross-Pollination Philosophy

The best AI agents will be built by teams that study ALL agent architectures, not just their own. Read other agents' skills. Understand their patterns. Adapt what works. Attribute what you borrow. This skill exists because we did exactly that.

---

## Pairs Well With

- [smart-model-router](https://clawhub.com/globalcaos/smart-model-router) — auto-select the right model for each sub-agent role (implementer → Sonnet, reviewer → Haiku, quality → GPT)
- [subagent-overseer](https://clawhub.com/globalcaos/subagent-overseer) — monitor your three-agent review pipeline without burning tokens on polling
- [coding-agent](https://clawhub.com/globalcaos/coding-agent) — the dispatch layer that launches your implementer sub-agents

_Research papers included, because we're that kind of obsessive._

👉 **https://github.com/globalcaos/tinkerclaw**

_Clone it. Fork it. Break it. Make it yours._

---

_Original methodology by Oscar Serra and Jarvis. Engineering patterns inspired by industry best practices and open-source agent skills (MIT License, Jesse Vincent). Adapted for OpenClaw's multi-agent architecture._
