# Evidence-gated intervention playbooks

## Contents

- [Common procedure](#common-procedure)
- [Dimension playbooks](#dimension-playbooks)
- [Repository selection rules](#repository-selection-rules)
- [Stop conditions](#stop-conditions)

Use these playbooks only after recording the current evidence and identifying a binding readiness
dimension. Select the smallest stack that can test or improve that bottleneck. Prefer a diagnostic
or evaluation repository when an effect is still unknown; do not treat installation as improvement.

The repository groups below refer to exact pinned entries in `repositories.json`.
Use only `default` entries without an additional source-selection condition. For a
`conditional` entry, satisfy and record its license, dependency, maturity, and
validation condition first. Treat `context_only` entries as explanatory evidence.

The `dimensions` field in `repositories.json` is a strict navigation association:
every value is backed by a matched span in the pinned repository README. A playbook
can also name a **support-only** repository for a prerequisite, diagnostic, evidence
route, or boundary control. Support-only placement does not add a dimension label,
does not establish an intervention effect, and must not be counted as improvement.

## Common procedure

1. State the target, scope, authority boundary, horizon, and rollback condition.
2. Attach direct observations to all affected dimensions; leave unobserved values `unknown`.
3. Choose one primary intervention for the binding dimension.
4. Add supporting components only for an unmet precondition.
5. Keep repositories from the same overlap group from contributing additive effect claims.
6. Estimate implementation, operation, verification, repair, and maintenance costs.
7. Compare against a matched baseline and validate using an independent check when possible.
8. Reassess all 13 dimensions, residual debt, resources, critical unknowns, and gate persistence.

## Dimension playbooks

### `provenance_integrity`

- **Diagnose:** `fost-agent-ledger`, `no-meta-standing-ledger`, `loscr`.
- **Intervene:** use `percolation-inversion-compiler` for evidence routing and residual records;
  `cait-certificate-schema` for typed certificate artifacts. Use `alt-foundry-kernel`
  as support-only certificate machinery and `future-claim-certifier` as a support-only
  temporal boundary when validity expires.
- **Verify:** replay the ledger, check hashes and authority, retain unresolved obligations.
- **Limit:** a complete, signed, or schema-valid record can still support a false claim.
- **Overlap:** `provenance_control`.

### `trust_quorum`

- **Diagnose:** `agent-trust-residual-benchmark`, `verification-ecology-kit`.
- **Intervene:** configure heterogeneous counter-checks with `verification-ecology-kit`, and route
  their evidence through the support-only routing layer in `percolation-inversion-compiler`.
- **Verify:** measure disagreement and error correlation; do not count duplicated verifiers as a
  larger quorum.
- **Limit:** verifier diversity by label is not effective independence.
- **Overlap:** `verification_core`.

### `temporal_integrity`

- **Diagnose/intervene:** `future-claim-certifier` for scoped future claims; use
  `certified-memory-governance-layer` for revocation and retrieval-time validity controls.
- **Verify:** replay at the relevant time, exercise expiry and authority-revocation cases.
- **Limit:** a passing certificate is scoped to its artifact, authority, policy, and time window.
- **Overlap:** `temporal_control`.

### `structural_reachability`

- **Diagnose:** `cgt-availability` and `cgt-ledgered-scientific-availability`.
  The latter is support-only for ledgered terminal-status transport.
- **Intervene:** `collective-capability-runtime` for task routing/recovery;
  `cgt-bandwidth-dynamics` for bounded constraint bandwidth.
- **Verify:** test dependency closure, continuation paths, rejected routes, and recovery.
- **Limit:** a reachable route does not establish substantive correctness.
- **Overlap:** `collective_coordination`, `cgt_availability`.

### `causal_formation`

- **Diagnose:** `cgt-availability`, `audit-closed-ai-scientist`, `loscr`.
- **Evaluate:** `agent-lifecycle-certification-poc`, `long-running-AI-agent-PoC`,
  `no-meta-observable-invention-poc`, or `pic-local-llm-phase-experiment` for matched,
  replayable comparisons.
- **Evidence boundary:** only records with explicit pinned causal-language evidence carry the
  `causal_formation` navigation label. All other repositories named here are support-only
  experimental or diagnostic comparators; they do not establish causal identification.
- **Verify:** predeclare the comparison, hold resources fixed, preserve null and adverse results,
  and separate association from causal identification.
- **Limit:** synthetic or local benchmark effects do not transport automatically to deployment.
- **Overlap:** `causal_evaluation`.

### `dimensional_consistency`

- **Diagnose:** `cgt-availability`.
- **Intervene:** `cgt-bandwidth-dynamics`, `semantic-translation-contracts-poc`, or
  the support-only `cimt-kernel` when typed cross-interface transformations are the bottleneck.
- **Verify:** run conformance, recoverability, composition, and round-trip checks.
- **Limit:** type or schema agreement does not guarantee semantic equivalence.
- **Overlap:** `cgt_availability`, `semantic_contracts`.

### `exact_self_maintenance`

- **Diagnose:** `memoryflow-agent-memory-auditor`, `search-stability-lab`.
- **Intervene:** `observable-agent-workflow-memory`, `certified-memory-governance-layer`, or `oasg`
  for evidence-bound procedure retention and replay; use `alt-foundry-kernel` only as
  support-only certified-abstraction machinery.
- **Verify:** reproduce behavior after restart, drift, revocation, and maintenance; account for
  ongoing costs.
- **Limit:** stored volume, cache hits, or workflow reuse is not certified self-maintenance.
- **Overlap:** `workflow_memory`, `memory_governance`, `reusable_capital`.

### `finite_horizon_resource_persistence`

- **Diagnose:** `asi-proxy-phase-growth-simulator`, `ai-real-economy-bottleneck-simulator`, and
  `bottleneck-audit-toolkit`.
- **Intervene:** reduce candidate or operating load before adding modules; use
  `certified-workflow-conversion` only after measuring the actual workflow bottleneck.
- **Verify:** include replenishment, implementation, maintenance, verification, and residual-repair
  costs over the complete horizon; exercise resource shocks.
- **Limit:** normalized resources need an independently justified mapping to real measurements.
- **Overlap:** `resource_analysis`.

### `target_bound_generative_catalysis`

- **Diagnose:** `problem-frame-gate`, `cimt-kernel`, and `certified-workflow-conversion`.
- **Target prerequisite:** `problem-frame-gate` is support-only target and authority framing,
  not evidence of generative catalysis.
- **Intervene:** admit candidate generation only against a declared target and acceptance evidence;
  use `no-meta-observable-invention-poc` to test replay-certified modification.
- **Verify:** distinguish gross output from verified reusable inflow and reject proxy-only gains.
- **Limit:** more candidates, benchmark score, or throughput is not capability capital.
- **Overlap:** `target_binding`.

### `verification_capacity`

- **Diagnose/intervene:** `percolation-inversion-compiler`, `verification-ecology-kit`,
  `bottleneck-audit-toolkit`; use `percolation-inversion-compiler-ts` only when a Node interface is
  required.
- **Verify:** measure verification throughput, coverage, false promotion, unresolved residuals,
  and receiver-side reuse.
- **Limit:** `accepted=true`, a passing schema, or verifier count alone does not certify capital.
- **Overlap:** `verification_core`.

### `effective_independence`

- **Diagnose:** `verification-ecology-kit`, `agent-trust-residual-benchmark`,
  `split-inference-bench`.
- **Intervene:** separate evidence routes, failure domains, models, and authorities; use
  `collective-capability-runtime` to enforce routing only after independence criteria are stated.
- **Verify:** perturb common dependencies and estimate correlated failure, not nominal agent count.
- **Limit:** multiple agents or models can share the same error mechanism.
- **Overlap:** `verification_core`, `collective_coordination`.

### `coordination_protocol_integrity`

- **Diagnose/intervene:** `collective-capability-runtime` and
  `collective-phase-control-fabric`; use `certified-local-participation-gate` or
  `no-meta-authority-runtime` for action and authority boundaries.
- **Verify:** test task ownership, recovery, refusal, revocation, release audit, and partial failure.
- **Limit:** orchestration success is not evidence of collective intelligence.
- **Overlap:** `collective_coordination`, `authority_control`.

### `perturbation_robustness`

- **Diagnose:** `agent-lifecycle-certification-poc`, `rsi-yardstick-drift-poc`,
  `search-stability-lab`, `memoryflow-agent-memory-auditor`,
  `Oversight-Centered-Metrology-PoC`.
- **Intervene:** use fail-closed gates from `problem-frame-gate`,
  `certified-local-participation-gate`, or `no-meta-authority-runtime`; preserve challenge and
  fork paths with `no-meta-standing-ledger` or `sovereign-epistemic-commons-poc`.
- **Evidence boundary:** gate, metrology, memory-audit, standing-ledger, and problem-frame
  repositories are support-only unless their own pinned routing evidence carries
  `perturbation_robustness`. Their presence is not a robustness result.
- **Verify:** run drift, expiry, revocation, contamination, monoculture, resource, and rollback
  tests.
- **Limit:** robustness to tested shocks does not cover hidden variables or regime changes.
- **Overlap:** `robustness_evaluation`, `authority_control`.

## Repository selection rules

- Prefer `core_intervention` repositories only when their preconditions match the workspace.
- Use `supporting_infrastructure` to satisfy a concrete dependency, not to inflate a stack.
- Use `evaluation_experiment` to produce evidence; do not assign it a direct growth effect.
- Use `research_source` for theory or provenance, not as an executable intervention.
- Do not select `historical_exploratory` repositories by default. They may provide context but have
  no effect mapping without new evidence.
- TypeScript and Python variants of PIC are interface alternatives, not additive interventions.
- Multiple memory tools share substantial mechanisms. Select one primary memory path and one
  independent audit path at most.
- CGT availability components share an overlap group; report joint adoption without summing
  assumed channel effects.
- Never infer effect magnitude from repository activity, language, stars, release labels, or
  documentation volume.

## Stop conditions

Stop the intervention and report the state when:

- a critical dimension remains `unknown`;
- the evidence does not support improvement;
- residual debt rises without a credible repair path;
- resource stock would cross its declared floor;
- verification or independence degrades;
- rollback cannot be exercised;
- required authority is absent; or
- completing the action would require push, release, external communication, destructive change,
  or another operation outside the declared authority boundary.
