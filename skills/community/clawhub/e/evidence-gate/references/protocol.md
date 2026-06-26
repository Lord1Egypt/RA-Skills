# Evidence Gate Protocol

Use this protocol when embedding Evidence Gate inside another agent, workflow, or skill.

## Goal

Keep the original workflow in control while inserting one bounded step:

1. Turn the current claim or action into a tentative candidate.
2. Generate the minimum evidence obligations for that candidate.
3. Check whether explicit evidence satisfies them.
4. Return a verdict plus the safest next move.

Assume the skill itself has no durable state.

## Candidate schema

Use this normalized shape when possible:

See `input-template.md` for the canonical input template.

```json
{
  "claim": "The likely root cause is a nil dereference in request parsing.",
  "claim_type": "diagnosis",
  "domain": "coding",
  "risk_level": "medium",
  "execution_mode": "advisory",
  "target_strength": "definitive",
  "known_evidence": [],
  "alternatives_checked": [],
  "available_tools": ["rg", "tests", "logs"],
  "policy_overrides": []
}
```

### Field notes

- `claim`: Keep it specific and testable. Avoid vague goals such as "make this safer".
- `claim_type`: Use `fact`, `diagnosis`, `recommendation`, `action`, or `safety`.
- `domain`: Keep it coarse. Domain-specific details belong in evidence items and requirements.
- `risk_level`: Drive how hard the gate should push back.
- `execution_mode`:
  - `informational`: the caller only wants to communicate
  - `advisory`: the caller is recommending but not executing
  - `auto`: the caller may execute directly
- `target_strength`:
  - `exploratory`: open possibility
  - `provisional`: likely but not settled
  - `definitive`: strong conclusion
  - `execute`: proceed with action
- `alternatives_checked`: Record competing explanations or actions already considered.
- `policy_overrides`: Add any stricter local rules, such as "security actions require human approval".

## Evidence item schema

Model each explicit evidence item with a compact record:

```json
{
  "id": "ev-1",
  "summary": "Regression test reproduces the crash when request.user is missing.",
  "kind": "test",
  "source": "local test suite",
  "artifact_ref": "tests/auth_test.rb:42",
  "reliability": "high",
  "supports": ["req-repro"],
  "contradicts": []
}
```

### Recommended evidence kinds

- `observation`
- `measurement`
- `log`
- `trace`
- `test`
- `reproduction`
- `code_path`
- `policy`
- `external_source`
- `human_confirmation`
- `counterevidence`

## Requirement schema

Generate only the minimum obligations needed to justify the current claim/action.
Each requirement should be concrete enough for the caller to satisfy with a real check.

```json
{
  "id": "req-repro",
  "description": "Show a reliable reproduction path for the claimed failure mode.",
  "mandatory": true,
  "acceptable_kinds": ["test", "reproduction", "log"],
  "status": "missing",
  "evidence_refs": [],
  "notes": "Without reproduction, the diagnosis should remain provisional."
}
```

### Status values

- `satisfied`
- `missing`
- `conflicting`
- `not_applicable`

### Evidence evaluation pitfalls

When deciding whether an evidence item satisfies a requirement, watch for these common errors:

- **Temporal correlation ≠ causation.** "X happened after Y" does not satisfy a causation requirement. Require an isolation test, controlled experiment, or at least elimination of confounders.
- **Single-source confirmation.** One log line, one metric, or one person's claim should not satisfy a requirement that asks for reliable confirmation. Look for corroboration from an independent source or method.
- **Scope mismatch.** Evidence from a different environment (dev vs prod), a different time window, or a different population does not automatically transfer. Note the gap explicitly.
- **Absence of counterevidence ≠ evidence of absence.** "No one reported problems" does not satisfy a safety requirement. Require an active check, not a passive lack of complaints.

If any of these pitfalls apply, mark the requirement `missing` or `conflicting`, not `satisfied`.

## Operating loop

Use this exact control shape unless local policy requires something stricter:

1. Build a candidate from the caller's tentative conclusion or action.
2. Decide whether a gate is required.
3. If no gate is required, return `PASS` with a short rationale.
4. If a gate is required, generate `2-5` evidence requirements.
5. Map only the currently provided evidence against those requirements.
6. Return one final verdict for the current invocation.
7. If the verdict is weaker than desired:
   - downgrade the claim/action immediately
   - and optionally return a bounded next-evidence plan
8. Exit.

## Stateless defaults

These defaults are the main reason this skill can stay portable:

- Do not assume any memory of prior gate outputs
- Do not require writing intermediate state files
- Do not require the caller to come back for a second pass
- If evidence is insufficient, return a bounded next-evidence plan instead of looping
- Low-risk informational outputs may continue with `SOFT_PASS`
- High-risk auto actions should require `PASS` or human approval
- Unresolved contradiction on a central requirement should become `CONFLICT`, not `PASS`

If a future caller wants multi-step orchestration, implement that outside this base skill by explicitly passing prior outputs back in.

## Verdict interpretation

- `PASS`: Enough evidence exists for the intended claim or action strength.
- `SOFT_PASS`: The evidence supports a weaker statement, advisory output, or reversible continuation.
- `BLOCK`: The intended strength or action is not justified yet.
- `CONFLICT`: The evidence materially points in different directions or leaves a central dispute unresolved.

## Canonical output template

Return JSON matching `output-template.md`.
Keep all top-level keys present on every invocation.
Use empty arrays instead of omitting fields.
Keep `gate_required` even on explicit invocation.
If `gate_required` is `false`, treat it as a fast exit and return `verdict = PASS`.

## Minimal examples

### Coding diagnosis

Candidate claim:

```json
{
  "claim": "The bug is caused by an empty user object during request parsing.",
  "claim_type": "diagnosis",
  "domain": "coding",
  "risk_level": "medium",
  "execution_mode": "advisory",
  "target_strength": "definitive"
}
```

Good requirements:

- reproduce the failure mode
- match the failing path to the claimed code path
- check at least one competing explanation

Possible downgrade:

- from "the root cause is X" to "X is the leading hypothesis"

### High-impact action

Candidate claim:

```json
{
  "claim": "Disable the worker queue in production.",
  "claim_type": "action",
  "domain": "sre",
  "risk_level": "high",
  "execution_mode": "auto",
  "target_strength": "execute"
}
```

Good requirements:

- confirm the queue is the actual failure source
- verify blast radius and rollback path
- confirm policy or operator approval for the action

Possible downgrade:

- from automatic execution to an advisory recommendation with human approval required
