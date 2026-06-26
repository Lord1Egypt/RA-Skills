# Collaboration Protocols

## Table of Contents

1. [Protocol 1: Parallel Fan-Out](#protocol-1-parallel-fan-out--synthesis)
2. [Protocol 2: Round-Robin Deliberation](#protocol-2-round-robin-deliberation)
3. [Protocol 3: Role-Specialized Council](#protocol-3-role-specialized-council-recommended)
4. [Protocol 4: Adversarial Debate](#protocol-4-adversarial-debate)
5. [Protocol 5: Sequential Pipeline](#protocol-5-sequential-pipeline)
6. [Protocol 6: DOVA Hybrid](#protocol-6-dova-hybrid-3-phase)
7. [Protocol 7: DCI Structured Deliberation](#protocol-7-dci-structured-deliberation)
8. [Decision Matrix](#decision-matrix)
9. [Cost Estimation](#cost-estimation)

---

## Protocol 1: Parallel Fan-Out → Synthesis

Send the same task to N agents in parallel, collect, synthesize. Fastest protocol.

```bash
# Setup
acpx claude sessions new --name fan-claude && acpx codex sessions new --name fan-codex && acpx gemini sessions new --name fan-gemini

# Fan-out in parallel
acpx --format quiet claude -s fan-claude "Task description here" > /tmp/fan1.txt &
acpx --format quiet codex -s fan-codex "Task description here" > /tmp/fan2.txt &
acpx --format quiet gemini -s fan-gemini "Task description here" > /tmp/fan3.txt &
wait

# Synthesize (orchestrator combines)
echo "[Claude]: $(cat /tmp/fan1.txt)\n\n[Codex]: $(cat /tmp/fan2.txt)\n\n[Gemini]: $(cat /tmp/fan3.txt)"

# Cleanup
acpx claude sessions close fan-claude && acpx codex sessions close fan-codex && acpx gemini sessions close fan-gemini
```

**When to use**: Quick multi-model opinion, getting diverse perspectives fast, any "get N opinions" task.

**Pros**: Fast (parallel), independent (no sycophancy), simple. **Cons**: No inter-agent learning, synthesis quality is the bottleneck.

---

## Protocol 2: Round-Robin Deliberation

Round 1: parallel independent analysis. Round 2: agents see all responses and revise.

```bash
# Setup
acpx claude sessions new --name r1c && acpx codex sessions new --name r1x && acpx gemini sessions new --name r1g

# Round 1: parallel
acpx --format quiet claude -s r1c "Analyze: <task>" > /tmp/rr1-c.txt &
acpx --format quiet codex -s r1x "Analyze: <task>" > /tmp/rr1-x.txt &
acpx --format quiet gemini -s r1g "Analyze: <task>" > /tmp/rr1-g.txt &
wait

# Build merged context
MERGED="[Claude]: $(cat /tmp/rr1-c.txt)\n\n[Codex]: $(cat /tmp/rr1-x.txt)\n\n[Gemini]: $(cat /tmp/rr1-g.txt)"

# Round 2: revise (same sessions preserve context)
acpx --format quiet claude -s r1c "Other reviewers:\n$MERGED\n\nRevise your assessment." > /tmp/rr2-c.txt &
acpx --format quiet codex -s r1x "Other reviewers:\n$MERGED\n\nRevise your assessment." > /tmp/rr2-x.txt &
acpx --format quiet gemini -s r1g "Other reviewers:\n$MERGED\n\nRevise your assessment." > /tmp/rr2-g.txt &
wait

# Final synthesis
echo "=== Round 2 Consensus ===\n\n[Claude]: $(cat /tmp/rr2-c.txt)\n\n[Codex]: $(cat /tmp/rr2-x.txt)\n\n[Gemini]: $(cat /tmp/rr2-g.txt)"
```

**When to use**: Design decisions, code review, architecture choices. The default deliberation protocol.

**Pros**: Agents learn from each other, session resume preserves context. **Cons**: 2× token cost, sycophancy risk (agents converge too fast).

---

## Protocol 3: Role-Specialized Council (Recommended)

Same as Protocol 2 but with role prefixes. See `references/roles.md` for role definitions and presets.

```bash
# Setup with team preset: code_review
acpx claude sessions new --name cr-claude && acpx codex sessions new --name cr-codex && acpx gemini sessions new --name cr-gemini

# Load role prefixes
SECURITY="[ROLE: Security Expert]\nAnalyze from a security perspective. Rate findings: CRITICAL/HIGH/MEDIUM/LOW."
PERF="[ROLE: Performance Expert]\nAnalyze from a performance perspective. Quantify where possible."
TESTING="[ROLE: Testing Expert]\nAnalyze from a testing perspective. List specific test cases needed."

# Round 1: role-specialized parallel analysis
acpx --format quiet claude -s cr-claude "$SECURITY\n\nReview src/auth.ts for vulnerabilities." > /tmp/cr1-c.txt &
acpx --format quiet codex -s cr-codex "$PERF\n\nReview src/auth.ts for performance issues." > /tmp/cr1-x.txt &
acpx --format quiet gemini -s cr-gemini "$TESTING\n\nReview src/auth.ts for test coverage gaps." > /tmp/cr1-g.txt &
wait

# Round 2: cross-review with role persistence
ALL="[Security (Claude)]: $(cat /tmp/cr1-c.txt)\n\n[Perf (Codex)]: $(cat /tmp/cr1-x.txt)\n\n[Testing (Gemini)]: $(cat /tmp/cr1-g.txt)"

acpx --format quiet claude -s cr-claude "Other experts:\n$ALL\n\n[ROLE: Security Expert — Deliberation] Maintain security perspective. Identify implications others missed." > /tmp/cr2-c.txt &
acpx --format quiet codex -s cr-codex "Other experts:\n$ALL\n\n[ROLE: Performance Expert — Deliberation] Check if proposals introduce performance regressions." > /tmp/cr2-x.txt &
acpx --format quiet gemini -s cr-gemini "Other experts:\n$ALL\n\n[ROLE: Testing Expert — Deliberation] Identify testing implications others missed." > /tmp/cr2-g.txt &
wait
```

**When to use**: Security audits, architecture reviews, PR reviews, any task where diverse expert perspectives improve quality. **The recommended default protocol.**

**Pros**: Prevents redundant analysis, matches model strengths to roles, composable. **Cons**: Overhead for simple tasks.

---

## Protocol 4: Adversarial Debate

Two agents argue opposing positions across rounds, then a judge synthesizes.

```bash
# Setup: advocate, critic, judge
acpx claude sessions new --name bull && acpx codex sessions new --name bear && acpx gemini sessions new --name judge

# Round 1: opening arguments
acpx --format quiet claude -s bull "Argue FOR adopting React Server Components in our project. Provide specific technical benefits." > /tmp/bull1.txt
acpx --format quiet codex -s bear "Argue AGAINST adopting React Server Components in our project. Provide specific technical risks." > /tmp/bear1.txt

# Round 2: cross-arguments (each sees opponent)
acpx --format quiet claude -s bull "The skeptic argues:\n$(cat /tmp/bear1.txt)\n\nCounter-argue. Address each concern." > /tmp/bull2.txt
acpx --format quiet codex -s bear "The advocate argues:\n$(cat /tmp/bull1.txt)\n\nCounter-argue. Address each claim." > /tmp/bear2.txt

# Judge synthesis
acpx --format quiet gemini -s judge "You are the judge. Synthesize this debate into a final recommendation.\n\n[FOR RSC]:\n$(cat /tmp/bull2.txt)\n\n[AGAINST RSC]:\n$(cat /tmp/bear2.txt)\n\nProvide:\n1. Summary of key arguments on each side\n2. Points of agreement\n3. Unresolved tensions\n4. Your final recommendation with confidence level (HIGH/MEDIUM/LOW)"
```

**When to use**: Go/no-go decisions, technology choices, "should we do X?" questions, high-stakes architectural decisions.

**Pros**: Forces engagement with counterarguments, reduces groupthink. **Cons**: Expensive, can produce false equivalence.

---

## Protocol 5: Sequential Pipeline

Chain agents in order — each sees prior agents' full output. Write → Review → Edit.

```bash
# Step 1: Write
acpx claude sessions new --name writer
acpx --format quiet claude -s writer "Implement user authentication with JWT. Include login, signup, and token refresh." > /tmp/pipe-write.txt

# Step 2: Review
acpx codex sessions new --name reviewer
acpx --format quiet codex -s reviewer "Review this implementation for bugs, security issues, and edge cases:\n$(cat /tmp/pipe-write.txt)\n\nRate: CRITICAL/HIGH/MEDIUM/LOW for each finding." > /tmp/pipe-review.txt

# Step 3: Edit (fix issues from review)
acpx claude -s writer "Fix the issues identified in this review:\n$(cat /tmp/pipe-review.txt)\n\nOriginal code:\n$(cat /tmp/pipe-write.txt)" > /tmp/pipe-final.txt
```

**When to use**: Write-review-edit cycles, implementation with quality gates, any ordered workflow.

**Pros**: Simplest to implement, clear audit trail, full context preserved. **Cons**: Sequential bottleneck, total latency = sum of all agents.

---

## Protocol 6: DOVA Hybrid (3-Phase)

Ensemble → Blackboard → Iterative Refinement. Research-backed (0.82 confidence vs 0.58 single agent).

```bash
# Phase 1: Ensemble (parallel independent solutions)
acpx claude sessions new --name dova-c && acpx codex sessions new --name dova-x && acpx gemini sessions new --name dova-g

acpx --format quiet claude -s dova-c "Solve: <task>. Provide your solution and rate your confidence (0-1)." > /tmp/do1.txt &
acpx --format quiet codex -s dova-x "Solve: <task>. Provide your solution and rate your confidence (0-1)." > /tmp/do2.txt &
acpx --format quiet gemini -s dova-g "Solve: <task>. Provide your solution and rate your confidence (0-1)." > /tmp/do3.txt &
wait

# Check agreement — if all confident and aligned, skip to synthesis
# (orchestrator evaluates)

# Phase 2: Blackboard (synthesize all solutions)
ALL="[Claude (conf: ?)]: $(cat /tmp/do1.txt)\n\n[Codex (conf: ?)]: $(cat /tmp/do2.txt)\n\n[Gemini (conf: ?)]: $(cat /tmp/do3.txt)"
acpx --format quiet claude -s dova-c "Synthesize these independent solutions into the best combined approach:\n$ALL\n\nRetain the strongest elements from each. Note any disagreements." > /tmp/board.txt

# Phase 3: Iterative refinement (2 rounds max)
acpx --format quiet claude -s dova-c "Critique and improve this synthesis:\n$(cat /tmp/board.txt)" > /tmp/ref1.txt
acpx --format quiet codex -s dova-x "Critique and improve this synthesis:\n$(cat /tmp/board.txt)" > /tmp/ref2.txt
# Optional second refinement round (diminishing returns beyond 2)
```

**When to use**: Complex analysis, research tasks, problems where quality justifies cost.

**Pros**: Highest quality (research-backed), adaptive (skip phases if high agreement). **Cons**: 3 phases = high token cost, complex orchestration.

---

## Protocol 7: DCI Structured Deliberation

Most rigorous protocol with typed epistemic acts, 5 phases, and guaranteed convergence. Research-backed but expensive (~62× single agent cost).

**5 Phases**: Arrival → Independent First Thought → Mutual Engagement → Collective Shaping → Closure

**14 Typed Acts** (use as structured instructions in prompts):

| Family | Acts | Purpose |
|---|---|---|
| Orienting | frame, clarify, reframe | Define the problem |
| Generative | propose, extend, spawn | Generate solutions |
| Critical | ask, challenge | Pressure-test |
| Integrative | bridge, synthesize, recall | Combine ideas |
| Epistemic | ground, update | Evidence management |
| Decisional | recommend | Final decision |

```bash
# Phase 1: Arrival — agents frame the problem
acpx claude sessions new --name dci1 && acpx codex sessions new --name dci2
acpx --format quiet claude -s dci1 "ACT: frame. Define the core problem with this task: <task>. What are we really trying to solve?" > /tmp/dci-f1.txt
acpx --format quiet codex -s dci2 "ACT: frame. Define the core problem with this task: <task>. What are we really trying to solve?" > /tmp/dci-f2.txt

# Phase 2: Independent First Thought — propose solutions without seeing others
acpx --format quiet claude -s dci1 "ACT: propose. Given your framing, propose a solution approach. Include rationale." > /tmp/dci-p1.txt &
acpx --format quiet codex -s dci2 "ACT: propose. Given your framing, propose a solution approach. Include rationale." > /tmp/dci-p2.txt &
wait

# Phase 3: Mutual Engagement — challenge and bridge
ALL="[Agent 1]: $(cat /tmp/dci-p1.txt)\n\n[Agent 2]: $(cat /tmp/dci-p2.txt)"
acpx --format quiet claude -s dci1 "ACT: challenge + bridge. Review proposals:\n$ALL\n\nChallenge weaknesses. Then bridge to create a combined approach." > /tmp/dci-c1.txt
acpx --format quiet codex -s dci2 "ACT: challenge + bridge. Review proposals:\n$ALL\n\nChallenge weaknesses. Then bridge to create a combined approach." > /tmp/dci-c2.txt

# Phase 4: Collective Shaping
ALL2="[A1 revised]: $(cat /tmp/dci-c1.txt)\n\n[A2 revised]: $(cat /tmp/dci-c2.txt)"
acpx --format quiet claude -s dci1 "ACT: synthesize. Combine into a unified recommendation:\n$ALL2\n\nIdentify: agreed points, tensions, and open questions." > /tmp/dci-final.txt

# Phase 5: Closure — always produces a decision packet
acpx --format quiet claude -s dci1 "ACT: recommend. Final decision packet:\n1. Selected option\n2. Residual objections (if any)\n3. Conditions to reopen discussion"
```

**When to use**: Consequential decisions, multi-stakeholder tradeoffs, architecture-level choices where process quality matters.

**Pros**: Most rigorous, guarantees convergence, preserves dissent. **Cons**: Very expensive (~62× cost), complex to implement, overkill for routine tasks.

---

## Decision Matrix

| Protocol | Speed | Quality | Cost | Complexity | Best For |
|---|:---:|:---:|:---:|:---:|---|
| 1. Fan-Out | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 💰 | Low | Quick multi-opinion |
| 2. Deliberation | ⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰 | Medium | Design decisions |
| 3. Role Council | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰 | Medium | Reviews, audits |
| 4. Adversarial | ⭐⭐ | ⭐⭐⭐⭐ | 💰💰💰 | High | Go/no-go choices |
| 5. Pipeline | ⭐⭐ | ⭐⭐⭐ | 💰 | Very Low | Write-review-edit |
| 6. DOVA Hybrid | ⭐ | ⭐⭐⭐⭐⭐ | 💰💰💰💰 | High | Complex analysis |
| 7. DCI Structured | ⭐ | ⭐⭐⭐⭐⭐ | 💰💰💰💰💰 | Very High | Critical decisions |

**Default recommendation**: Protocol 3 (Role Council) for most tasks. Protocol 1 (Fan-Out) for quick checks. Protocol 4 (Adversarial) for high-stakes decisions.

---

## Cost Estimation

Rough token cost multipliers relative to a single agent solving the task alone:

| Protocol | Agents | Rounds | Multiplier |
|---|:---:|:---:|:---:|
| Fan-Out | 3 | 1 | 3× |
| Deliberation | 3 | 2 | 6× |
| Role Council | 3 | 2 | 6× (+ role prefix overhead) |
| Adversarial | 3 | 2-3 | 6-9× |
| Pipeline | 3 | 1 each | 3× (but sequential) |
| DOVA Hybrid | 3 | 3-4 | 9-12× |
| DCI Structured | 2-3 | 5 | 10-15× |

**Cost-saving tips**:
- Use `--format quiet` to minimize token output
- Skip Round 2 if Round 1 responses already agree
- Use Protocol 1 for simple tasks, upgrade only when quality matters
- Limit to 3 agents — diminishing returns beyond 3 (research-backed)
