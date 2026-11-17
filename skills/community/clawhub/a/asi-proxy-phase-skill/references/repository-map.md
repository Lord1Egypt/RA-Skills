# Public repository map

## Contents

- [Scope and provenance](#scope-and-provenance)
- [Start here](#start-here)
- [Role classification](#role-classification)
- [Dimension-to-repository routing](#dimension-to-repository-routing)
- [Overlap and substitution](#overlap-and-substitution)
- [Selection checklist](#selection-checklist)

This map helps a first-time agent choose evidence and tools without reading all 53 repositories.
The machine-readable source of truth is [`repositories.json`](repositories.json).

## Scope and provenance

- Owner: `kadubon`
- Inventory endpoint:
  `https://api.github.com/users/kadubon/repos?per_page=100&type=public&sort=full_name`
- Observation: 54 public repositories were listed on 2026-07-30.
- Included: 53 upstream research and implementation repositories.
- Explicitly excluded: `asi-proxy-phase-skill`, because it is this derived index rather
  than an upstream source.
- Also excluded: every private repository and every local unpublished source.
- Pin: each entry records the full 40-character default-branch HEAD SHA and commit date.
- License: each entry separates the GitHub API SPDX observation from the pinned root
  license file path, SHA-256, and detected SPDX text. `NOASSERTION` is not permission
  to copy code.

Descriptions, topics, public artifacts, activity, and release labels can support navigation and a
maturity observation. They do not measure scientific validity, security, adoption, or effect size.

## Start here

For a new workspace:

1. Use `problem-frame-gate` to define the task, authority, and risk boundary.
2. Use `percolation-inversion-compiler` and `verification-ecology-kit` to inspect verification,
   provenance, residuals, and independence.
3. Use `fost-agent-ledger` or `no-meta-standing-ledger` when claims and unresolved obligations
   need durable lineage.
4. Use `collective-capability-runtime` only when coordination is the measured bottleneck.
5. Use one memory path—normally `observable-agent-workflow-memory` or
   `certified-memory-governance-layer`—plus an independent audit path such as
   `memoryflow-agent-memory-auditor`.
6. Use `asi-proxy-phase-growth-simulator` for transparent counterfactual analysis after evidence,
   costs, and unknowns are stated. Never use its synthetic defaults as observations.

Choose by the binding dimension, not by repository popularity or apparent sophistication.

## Role classification

### Core interventions — 20

These repositories expose an executable gate, ledger, runtime, workflow, memory, verification, or
constraint mechanism. Their inclusion does not assert a positive effect.

`alt-foundry-kernel`, `certified-local-participation-gate`,
`certified-memory-governance-layer`, `certified-workflow-conversion`, `cgt-availability`,
`cgt-bandwidth-dynamics`, `cimt-kernel`, `collective-capability-runtime`,
`collective-phase-control-fabric`, `fost-agent-ledger`, `future-claim-certifier`, `loscr`,
`no-meta-authority-runtime`, `no-meta-standing-ledger`, `oasg`,
`observable-agent-workflow-memory`, `percolation-inversion-compiler`, `problem-frame-gate`,
`Proof-Carrying-Skills--PCS-Core-`, `verification-ecology-kit`

### Supporting infrastructure — 7

These repositories supply schemas, checkers, telemetry, language adapters, transfer checks, or an
agent integration. Add one only to satisfy a stated precondition.

`bottleneck-audit-toolkit`, `cait-certificate-schema`,
`cgt-ledgered-scientific-availability`, `cgt-marker`, `frontier-transfer-certifier`,
`percolation-inversion-compiler-ts`, `pic-openclaw-skill`

### Evaluation and experiments — 17

These repositories produce bounded evidence or scenario diagnostics. They do not have a direct
growth effect merely because an experiment can be run.

`agent-lifecycle-certification-poc`, `agent-trust-residual-benchmark`,
`ai-real-economy-bottleneck-simulator`, `asi-proxy-phase-growth-simulator`,
`audit-closed-ai-scientist`, `long-running-AI-agent-PoC`,
`memoryflow-agent-memory-auditor`, `no-meta-observable-invention-poc`,
`observable-replay-lab`, `Oversight-Centered-Metrology-PoC`,
`pic-local-llm-phase-experiment`, `record-absence-poc`, `rsi-yardstick-drift-poc`,
`search-stability-lab`, `semantic-translation-contracts-poc`,
`sovereign-epistemic-commons-poc`, `split-inference-bench`

### Research sources — 3

Use these for the research lineage and primary text, not as executable interventions.

`github.io`, `no-meta-drift-papers`, `paper-tex-backup`

### Historical and exploratory — 6

These are indexed for completeness but have no default intervention mapping. A fresh code,
evidence, license, and safety review is required before use.

`AIconsciousness`, `ASI`, `Benevolent-Propagation-spec`, `GEAR`, `UniverseModel`,
`WisdomWeaver`

## Dimension-to-repository routing

| Binding dimension | Primary evidence or intervention choices | Independent or supporting checks |
|---|---|---|
| `provenance_integrity` | `fost-agent-ledger`, `no-meta-standing-ledger`, `percolation-inversion-compiler` | `loscr`, `cait-certificate-schema` |
| `trust_quorum` | `verification-ecology-kit`, `percolation-inversion-compiler` | `agent-trust-residual-benchmark` |
| `temporal_integrity` | `future-claim-certifier`, `certified-memory-governance-layer` | `cgt-ledgered-scientific-availability` |
| `structural_reachability` | `collective-capability-runtime`, `cgt-bandwidth-dynamics` | `cgt-availability` |
| `causal_formation` | `loscr`, `cgt-availability` | `audit-closed-ai-scientist`, bounded PoCs |
| `dimensional_consistency` | `cgt-bandwidth-dynamics`, `cimt-kernel` | `semantic-translation-contracts-poc` |
| `exact_self_maintenance` | `observable-agent-workflow-memory`, `certified-memory-governance-layer`, `alt-foundry-kernel` | `memoryflow-agent-memory-auditor`, `search-stability-lab` |
| `finite_horizon_resource_persistence` | load reduction, then `certified-workflow-conversion` if supported | `asi-proxy-phase-growth-simulator`, `bottleneck-audit-toolkit` |
| `target_bound_generative_catalysis` | `problem-frame-gate`, `cimt-kernel`, `oasg` | `no-meta-observable-invention-poc` |
| `verification_capacity` | `percolation-inversion-compiler`, `verification-ecology-kit` | `bottleneck-audit-toolkit`, `agent-trust-residual-benchmark` |
| `effective_independence` | `verification-ecology-kit`, explicit failure-domain separation | `split-inference-bench`, `agent-trust-residual-benchmark` |
| `coordination_protocol_integrity` | `collective-capability-runtime`, `collective-phase-control-fabric` | `certified-local-participation-gate`, `no-meta-authority-runtime` |
| `perturbation_robustness` | fail-closed gates and challenge/fork paths | drift, lifecycle, memory, and oversight PoCs |

Read [`intervention-playbooks.md`](intervention-playbooks.md) before composing a stack.

## Overlap and substitution

- `percolation-inversion-compiler` and `percolation-inversion-compiler-ts` are language/interface
  alternatives. Do not count both as independent effects.
- `percolation-inversion-compiler` and `verification-ecology-kit` overlap in verification-core
  functions. Use one primary routing path and state the independent checks explicitly.
- `cgt-availability`, `cgt-bandwidth-dynamics`, and
  `cgt-ledgered-scientific-availability` share availability and constraint mechanisms.
- `observable-agent-workflow-memory`, `certified-memory-governance-layer`, `oasg`, and
  `alt-foundry-kernel` overlap in retention or reuse. Do not add assumed effects mechanically.
- `fost-agent-ledger`, `no-meta-standing-ledger`, `loscr`, and PIC ledgers overlap in provenance
  recording. Choose the ledger whose claim and authority model fits the task.
- `problem-frame-gate`, `certified-local-participation-gate`, and
  `no-meta-authority-runtime` overlap in action or authority control.
- Benchmarks, PoCs, and simulators provide evidence or falsification opportunities. They are not
  direct capability interventions.

## Selection checklist

Before selecting a repository, confirm:

- the repository is pinned to the exact SHA in `repositories.json`;
- its `selection_eligibility` is `default` or the stated condition for `conditional`
  use has been satisfied;
- its role is not `historical_exploratory` or `research_source` for a default
  intervention;
- any `NOASSERTION` license remains context-only until permission is established;
- the workspace can satisfy its stated dependencies and interfaces;
- the mechanism addresses the observed binding dimension;
- an independent validation and rollback path exist;
- implementation and operating costs fit the resource floor; and
- the intervention packet repeats the repository-specific limit and the global ASI non-claims.
