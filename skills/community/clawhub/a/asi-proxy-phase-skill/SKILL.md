---
name: asi-proxy-phase-skill
description: Diagnose, explain, and improve an evidence-gated, protocol-relative ASI-proxy readiness regime using K. Takahashi's pinned papers and public repositories. Use for observable-only or no-meta agent improvement, verification bottlenecks, provenance and memory failures, certified reusable capability, finite-resource phase diagnostics, paper-to-implementation lineage, multi-repository intervention planning, or iterative implementation and evaluation. Do not use for unrelated generic coding or to claim that real ASI or a scientific phase transition has been achieved.
---

# ASI-Proxy Phase Orchestrator

Treat every output, including your own, as candidate work until evidence supports
admission and reuse. Optimize a declared operational proxy; never certify real ASI,
forecast a world event, or claim a scientific phase transition.

## Fast path

1. Run the offline installation check:

   ```text
   uv run --managed-python --python 3.11 --script scripts/doctor.py
   ```

2. Read [the phase model](references/phase-model.md).
3. Select one mode below from the user's objective.
4. Search before loading large references:

   ```text
   uv run --managed-python --python 3.11 --script scripts/query_sources.py --query "<problem>" --kind all --match auto --limit 8
   ```

5. Preserve DOI, catalog hash, repository URL, pinned HEAD SHA, evidence limits, and
   non-claims in every material recommendation.

## Select a mode

### Research

Use for explanation, literature navigation, or paper-to-repository lineage.

- Query exact DOI, repository name, and then problem terms.
- Read [the research program](references/research-program.md) for synthesis and
  [the repository map](references/repository-map.md) for implementation roles.
- Cite canonical DOI and pinned commit evidence.
- For lineage questions, name every observed edge as `implements`,
  `companion_software`, `cites`, or `lineage`; do not collapse these relations or
  infer an unstored edge.
- For ambiguous searches, report the requested and effective match policy, including
  any `auto` fallback, and retain the selected record's field/span routing evidence.
- Describe routing labels as catalog-based navigation, not peer review or validation.
- Do not create a packet or edit a workspace unless the user also requests an
  intervention.

### Diagnosis

Use when the user needs a readiness assessment without implementation.

- Establish the objective, workspace, authority, evidence boundary, resource envelope,
  and evaluation horizon.
- Assess every dimension from [the phase model](references/phase-model.md) as
  `observed`, `bounded`, or `unknown`.
- Record a value only for direct observation. Record explicit bounds only with cited
  evidence. Never convert an unknown into zero, a midpoint, or a prior.
- Identify the lowest supported dimension and any critical unknown that blocks a
  comparison.
- Report the next binding dimension without claiming improvement.

### Intervention

Use for a bounded implementation or experiment in the declared workspace.

An Intervention-mode request always requires an actual packet artifact. Create and
validate it before any workspace mutation; a prose assessment is not a substitute. If
no intervention can safely proceed, still preserve the valid fail-closed packet with
the blocking unknowns and outcome.

1. Create a fail-closed packet:

   ```text
   uv run --managed-python --python 3.11 --script scripts/init_packet.py intervention-packet.json --objective "<objective>"
   ```

2. Read [the intervention playbooks](references/intervention-playbooks.md).
3. Search candidate repositories with `--eligible-only`; use `context_only` sources for
   background, not default execution.
4. Choose the smallest coherent stack that targets one binding dimension. Do not add
   overlapping effect claims.
5. Record mechanism, cost, dependencies, evidence, rollback, and non-claims.
6. Validate before mutation:

   ```text
   uv run --managed-python --python 3.11 --script scripts/validate_packet.py intervention-packet.json
   ```

7. Inspect the selected repository's pinned evidence and current worktree, preserve
   unrelated changes, implement only within authority, and run repository-specific
   tests.
8. Revalidate and compare against the same starting conditions and resource budget.

### Iterative readiness loop

Use for repeated improvement over a declared hold period.

- Repeat diagnosis, one intervention, validation, and reassessment.
- Admit improvement only when evidence shows a targeted dimension improved without
  increasing an unbounded residual or violating the resource floor.
- Treat acceleration as faster removal of a verified bottleneck, reduced critical
  unknowns, higher verified reusable capability, or sustained readiness under finite
  resources. Do not equate acceleration with more output, commits, candidates, or
  unverified claims.
- Stop when evidence does not improve, residual debt grows, the resource floor fails,
  a critical unknown remains, or the next action exceeds authority.
- Record the next binding dimension; do not diffuse effort across all dimensions.

## Operating boundary

- Work autonomously only inside the workspace and authority placed in scope.
- Follow host approval rules for repository writes, network calls, messages,
  deployments, releases, and destructive actions.
- Do not push, publish, release, contact third parties, access credentials, or expand
  scope unless explicitly authorized.
- Do not infer a causal effect from a paper, repository, test pass, benchmark, model
  output, commit count, or simulation.
- Do not infer implementation readiness from a repository title. Check
  `selection_eligibility`, pinned license evidence, dependencies, maturity evidence,
  and interfaces.
- Prefer deterministic checks for mechanical claims and independently scoped evidence
  for admission decisions.
- Keep implementation cost and continuing operating cost separate.
- Preserve failed runs, expiry, residuals, and counterevidence in the audit trail.

## Candidate gate

Use all conditions from [the phase model](references/phase-model.md). Set
`candidate_regime: true` only when every gate passes, no critical unknown remains, and
the result holds for the declared period. Otherwise use `false` or `null`.

The public packet contract is
[the JSON Schema](assets/intervention-packet.schema.json). Structural validity makes a
packet reviewable; it does not make its claims true.

## Retrieve only what is needed

- Read [the glossary](references/glossary.md) for unfamiliar terms.
- Read [the research program](references/research-program.md) for thematic synthesis.
- Read [the repository map](references/repository-map.md) for role, license, maturity,
  dependencies, and selection policy.
- Read [the intervention playbooks](references/intervention-playbooks.md) after
  identifying a binding dimension.
- Use `query_sources.py --full` only for the few selected records.
- Treat the fixed [catalog snapshot](references/catalog-snapshot.json), routing rules,
  and stored evidence as provenance; do not load the whole catalog into context.

## Validate and report

Run repository tests and packet validation. Compare baseline and candidate over the
same horizon and resource envelope. Check targeted evidence, verification coverage,
new bottlenecks, residual debt, expiry, failure correlation, rollback, replay, and
reasonable perturbations.

Lead with the observed outcome. Report:

1. what changed or was analyzed;
2. exact tests and evidence;
3. dimensions affected and still binding;
4. residuals and critical unknowns;
5. rollback state;
6. non-claims; and
7. the next smallest evidence-supported intervention.

Distinguish `implemented`, `tested`, `observed`, `bounded`, `supported under declared
assumptions`, and `unknown`.

## Maintain sources

Keep normal use offline. Check public drift without writing:

```text
uv run --managed-python --python 3.11 --script scripts/refresh_sources.py --check
```

Verify deterministic paper reconstruction:

```text
uv run --managed-python --python 3.11 --script scripts/rebuild_indexes.py --check
```

Use write modes only during an explicit skill-maintenance task. Review changed semantic
claims, rerun all validators and evaluations, and publish a new version. Never include
private repository metadata, credentials, or local absolute paths.

## Required non-claims

- The ASI-proxy quantity is protocol-relative and model-dependent.
- A candidate regime is not ASI attainment.
- Repository availability or adoption is not a measured causal effect.
- Synthetic priors and simulation bands are not world forecasts.
- Verification supports only claims within the declared evidence and procedure.
- Unmodeled physical, social, economic, and institutional constraints remain possible.
