# Specialist Selection

Use this reference when the `ai-expert-team` skill needs more detail than the quick Specialist Selection Guide in `SKILL.md`.

The goal is to select a small roster of specialists whose scopes do not overlap, whose evidence requirements are explicit, and whose outputs can be verified before CEO synthesis.

## Core Idea

Specialists are not decorative job titles. Each specialist is a scoped capability with:

- A clear deliverable.
- A bounded responsibility.
- Required evidence.
- Explicit allowed tools and forbidden actions.
- A known reason for being on the team.
- A check against overlap with the rest of the roster.

Default roster size is 3-5 specialists. More than 7 specialists usually means the problem has not been decomposed well enough.

## Source Catalog

When a run needs grounded Agency Agents roles, use the local source asset:

- `assets/agency-agents`

If the directory does not exist, clone it first from:

- `https://github.com/msitarzewski/agency-agents.git`

Do not commit cloned source directories. `assets/.gitignore` ignores `agency-agents/`.

Use Agency Agents as a specialist catalog, not as prompt text to copy blindly. The role body can inspire identity and process, but the runtime handoff must still add current task scope, evidence requirements, tool boundaries, and output contract.

## Selection Pipeline

### 1. Convert the problem into expert needs

The CEO first writes expert needs, not role names.

Each expert need should include:

- `need_id`: short stable ID.
- `domain`: engineering, testing, product, design, security, marketing, operations, finance, academic, or specialized.
- `deliverable`: what the specialist must produce.
- `evidence_required`: source files, commands, docs, data, calculations, or reasoning checks.
- `risk_level`: high, medium, or low.
- `must_not_do`: forbidden actions.

Example:

```text
need_id: implementation-evidence
domain: testing
deliverable: verify whether the proposed code path exists and whether the test command supports the claim
evidence_required: source files + command output
risk_level: high
must_not_do: edit files, commit, push, deploy
```

### 2. Search for candidate specialists

Search the Agency catalog by:

- Division.
- Role name.
- Description.
- Body keywords.
- Deliverable type.
- Evidence type.
- Required tool or workflow hints.

Prefer candidates whose role naturally produces the needed deliverable. Do not pick a glamorous title when a narrower role fits better.

### 3. Inspect shortlisted roles

Inspect the top candidates before choosing final specialists. Do not select by name alone.

Look for:

- Actual mission and workflow.
- Critical rules.
- Deliverables.
- Success metrics.
- Tool assumptions.
- Any mismatch with the current task.

If the inspected role body conflicts with the current task, either normalize it heavily or reject it.

### 4. Score candidates

Use this scoring shape when the choice is non-obvious:

```text
candidate: <role name>
source_path: <agency path>
domain_fit: 0-3
deliverable_fit: 0-3
evidence_fit: 0-3
tool_fit: 0-3
overlap_penalty: 0-3
risk_coverage: 0-3
verification_value: 0-3
confidence: high | medium | low
selected: yes | no
reason: <why this candidate is or is not selected>
```

Guidelines:

- `domain_fit`: matches the problem domain.
- `deliverable_fit`: can produce the exact needed artifact.
- `evidence_fit`: can work with the required evidence type.
- `tool_fit`: can operate with available tools and permissions.
- `overlap_penalty`: subtract when another selected specialist covers the same work.
- `risk_coverage`: adds missing security, production, cost, user, or strategy risk coverage.
- `verification_value`: adds independent checking capability.

### 5. Normalize selected specialists

Every selected specialist becomes a runtime profile:

```text
name: <runtime specialist name>
source_path: <Agency source path or manual source>
division: <inferred division>
selected_for: <why this role is on this roster>
scope: <what this role owns>
out_of_scope: <what this role must not touch>
allowed_tools: <tools/actions allowed>
forbidden_actions: <edits, commits, pushes, sends, deploys, external mutation unless authorized>
evidence_required: <specific evidence>
output_contract: <required sections>
confidence: high | medium | low
limitations: <known blind spots>
```

Never dispatch a raw Agency role without this normalization.

### 6. Run roster coverage check

Before dispatch, check coverage:

- Does each specialist have a distinct deliverable?
- Is at least one specialist responsible for verification when claims matter?
- Are implementation, risk, user impact, and operational reality covered when relevant?
- Are there duplicate architects, duplicate reviewers, or duplicate strategists?
- Is any critical risk area missing?
- Are all forbidden actions explicit?

If coverage is weak, adjust the roster before dispatch.

## Common Role Patterns

### Technical architecture

Useful specialists:

- Multi-Agent Systems Architect.
- Backend Architect.
- SRE or DevOps Automator.
- Security Architect.
- Evidence Collector or Reality Checker.
- Technical Writer when the output is durable documentation.

Avoid picking several architecture specialists that all inspect the same thing.

### Codebase research

Useful specialists:

- Codebase Onboarding Engineer.
- Technical Writer.
- Code Reviewer.
- Evidence Collector.

Evidence should include file paths, symbol names, commands, or documented source references.

### Product strategy

Useful specialists:

- Product Manager.
- UX Researcher.
- Trend Researcher.
- Business Strategist.
- Risk or contrarian reviewer.

Evidence can include user constraints, market data, prior decisions, or explicitly labeled assumptions.

### Prompt and agent design

Useful specialists:

- Prompt Engineer.
- Multi-Agent Systems Architect.
- Agents Orchestrator.
- Reality Checker.
- Evidence Collector.

Check for prompt-boundary discipline, output contracts, tool boundaries, and helper-agent confidence calibration.

### Verification-heavy work

Useful specialists:

- Reality Checker.
- Evidence Collector.
- API Tester.
- Performance Benchmarker.
- Security Architect.

Verification roles should end with `VERDICT: PASS`, `VERDICT: FAIL`, or `VERDICT: PARTIAL`.

## Rejection Rules

Reject or replace a candidate when:

- The role title fits but the body describes unrelated work.
- The role duplicates another selected specialist.
- The role requires unavailable tools and no fallback exists.
- The role encourages mutation when the user asked only for inspection.
- The role cannot produce evidence for the claim it is asked to make.
- The role is primarily motivational or persona-flavored rather than operational.

## Example Roster

Problem: evaluate whether an AI agent plugin architecture should be rewritten.

Good roster:

- Multi-Agent Systems Architect: evaluates architecture boundaries, orchestration topology, failure modes, and least privilege.
- Codebase Onboarding Engineer: maps actual repo structure and implementation constraints.
- Security Architect: checks tool permissions, data exposure, and external mutation risks.
- Evidence Collector: verifies claims against source files and command output.
- Technical Writer: turns the result into a durable implementation record.

Weak roster:

- Software Architect.
- Backend Architect.
- Multi-Agent Architect.
- System Designer.

Why weak: too much architecture overlap, no verification owner, no security or documentation owner.

## Final Specialist Roster Format

Use this in the final team plan:

```text
Specialist roster:
1. <role> — selected for <reason>; owns <scope>; evidence <required evidence>.
2. <role> — selected for <reason>; owns <scope>; evidence <required evidence>.
3. <role> — selected for <reason>; owns <scope>; evidence <required evidence>.

Rejected candidates:
- <role> — rejected because <overlap / poor fit / unavailable tools / unsafe scope>.

Coverage check:
- implementation: covered | not needed | missing
- risk/security: covered | not needed | missing
- user/product impact: covered | not needed | missing
- verification: covered | missing
- documentation/handoff: covered | not needed | missing
```

## Pitfalls

- Selecting specialists by impressive names instead of deliverables.
- Dispatching raw catalog prompts without current task boundaries.
- Letting specialists decide their own verification standard.
- Treating a verifier as optional polish.
- Selecting too many specialists because the problem feels important.
- Allowing read-only requests to inherit edit, commit, push, or deploy behavior.
