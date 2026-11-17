# AI-native SDLC Practice Layer

Use this reference when the problem is not merely how to write code, but how to move a software change from intent to production with evidence, control, and feedback. It is an original operational synthesis derived from Anthropic's official [The AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), published 2026-08-21. Verify current Claude product commands in official documentation.

## The delivery loop

`intent → spec → plan → code/tests → review → deploy → incident → intent`

Each transition produces a versioned artifact readable by both people and agents. The artifact is evidence of what was requested, decided, built, checked, and approved. Human attention moves to judgment gates; deterministic controls enforce rules that must never be optional.

## Stage guide

| Stage | Use when | Minimum artifact | Human judgment | Useful measure | Common failure |
|---|---|---|---|---|---|
| Plan | an idea, ticket, or alert is ambiguous | `intent.md`: problem, outcome, affected users/systems, constraints, open questions | product owner accepts the intent | time to accepted intent; acceptance rate | automating an unclear request |
| Design | an accepted intent needs requirements and constraints | `spec.md`: behavior, design, risks, unresolved policy conflicts | product owner and named policy owners resolve concerns | intent-to-spec time; late requirement rework | hiding contradictions behind generated prose |
| Build | implementation could diverge from intent | `plan.md`: files, sequence, risks, proof | engineer approves the plan; lead reviews high-risk work | first-pass merge; rework cycles | coding before the plan is decision-complete |
| Test | output needs machine-verifiable evidence | test/build/lint output and, for UI, visual comparison | reviewer judges intent and residual risk | first-pass CI; review time; eval pass rate | allowing the fix agent to weaken its own test |
| Deploy | autonomy must stop at explicit boundaries | PR findings, approvals, pipeline and release records | code owner or release owner authorizes critical gates | time to first review; DORA measures | granting production credentials to an unrestricted agent |
| Maintain | operational signals should re-enter delivery | incident record and a new `intent.md` | service owner triages act, schedule, or dismiss | detection-to-triage; incidents converted to evals | letting a probabilistic model define the alert threshold |

## Operating patterns

### Artifact Gate

Use when a handoff is slow, lossy, or unauditable. Define the minimum artifact and acceptance owner for each transition. The next stage starts from the accepted artifact, not from chat history. Keep the chain linked by commit, ticket ID, or both.

### One Source of Truth

Use when repository files coexist with Jira, ServiceNow, Figma, or another system. Declare one authoritative home per artifact. Other systems hold a link or synchronized copy. During transition, record both the external ID and commit SHA.

### Skill plus deterministic guardrail

Use a Skill for policy the agent should apply consistently while working. Back any non-negotiable rule with a deterministic check such as a hook, CI gate, branch protection, permission rule, or sandbox. Advisory guidance reduces mistakes; enforcement establishes the boundary.

### Verification Evidence

Make “done” observable. Give the agent one-command build, test, and lint paths plus a quantifiable target. Require literal tool output or visual evidence. For bug fixes, establish a failing regression test before the fix and prevent the implementation pass from weakening that test.

### Autonomy Tiers

Increase autonomy by environment and blast radius, not by enthusiasm:

1. **Suggest:** diagnose and draft; no writes.
2. **Propose:** write only through a reviewed PR.
3. **Act in development:** execute with scoped tools and no production credentials.
4. **Prepare production:** complete all work up to a named human release gate.
5. **Pre-approved response:** trigger only rehearsed runbooks such as rollback under deterministic conditions.

Do not advance a tier until tests, permissions, logging, review, and rollback for the current tier are reliable.

### Incident-to-Eval

Turn every meaningful production escape into a permanent evaluation or regression test. Run the suite when agent instructions, Skills, hooks, prompts, or models change. Treat agent configuration as code: version it, review it, and block regressions.

### Production Control Band Loop

Keep detection deterministic. A versioned monitor evaluates stable metrics and selects a response tier. Low severity logs; medium severity invokes read-only diagnosis; high severity may open a PR or invoke a pre-approved runbook. The agent writes evidence and a new `intent.md`; a responsible human triages it.

## Fast adoption order

1. Make build, test, and lint runnable and require verification evidence.
2. Add `intent.md`, `spec.md`, and approved `plan.md` only where they reduce ambiguity.
3. Capture repeated repository mistakes in concise project instructions.
4. Encode recurring institutional policy as Skills; enforce hard requirements deterministically.
5. Add continuous evals and agent-assisted review.
6. Add environment-specific autonomy and production approval gates.
7. Close the maintenance loop only after rollback and audit paths are proven.

## Decision rules and anti-patterns

- If a change is small, reversible, and already test-covered, combine spec and plan instead of manufacturing paperwork.
- If a decision requires business, safety, compliance, or release judgment, name the accountable human; do not delegate accountability to the agent.
- If the agent repeats a repository-specific mistake, improve shared project context; if the rule is organizational and reusable, make it a Skill.
- If a policy must always hold, prose alone is insufficient; add deterministic enforcement.
- If generated output cannot be checked cheaply, reduce scope or build the check before increasing autonomy.
- Avoid copying every legacy ceremony into markdown. Preserve control objectives, remove redundant handoffs.
- Avoid one giant context file. Keep stable project facts concise and load specialized policy only when relevant.
- Avoid autonomous production actions through general shell access. Expose narrow, auditable tools and rehearsed runbooks.
