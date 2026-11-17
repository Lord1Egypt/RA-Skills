# Protocol-relative ASI-proxy phase model

## Contents

- [Scientific boundary](#scientific-boundary)
- [State and flow](#state-and-flow)
- [The 13 readiness dimensions](#the-13-readiness-dimensions)
- [Readiness, proxy capital, and reproduction](#readiness-proxy-capital-and-reproduction)
- [Candidate-regime gate](#candidate-regime-gate)
- [How an agent should use the model](#how-an-agent-should-use-the-model)
- [Required non-claims](#required-non-claims)

This reference condenses the operational model implemented by
[`kadubon/asi-proxy-phase-growth-simulator`](https://github.com/kadubon/asi-proxy-phase-growth-simulator).
Use the pinned simulator repository in `repositories.json` when exact equations, defaults, or code
behavior matter.

## Scientific boundary

The model is a finite, discrete-time scenario system for **operationally certified, reusable
capability capital**. It is not a model of real ASI, a forecast of superintelligence, a probability
of ASI, evidence for a physical phase transition, or an empirical causal estimate of repository
effects. All thresholds are protocol-relative choices and the default coefficients are synthetic
priors.

Agent outputs are candidate work. They become modeled capital only after verification, trust,
reuse, provenance, temporal, and resource constraints. Unresolved work remains visible as residual
debt.

## State and flow

The simulator tracks gross certified reusable capability `K`, residual debt `R`, resource stock
`B`, and bounded quality states for framing, availability, coordination, verification,
independence, provenance, memory, temporal validity, causal support, and hazard pressure.

Candidate flow `Q` depends on resources, existing capital, and the framing, availability,
coordination, and memory states. Candidate flow is never counted directly as capital.

```text
verification_coverage = min(1, verification_throughput / (Q + epsilon))

verified_yield =
    verification_coverage
    × trust
    × (1 - hazard_pressure)
    × bounded_yield_effect

reuse =
    reuse_base
    × geometric_mean(availability, memory, provenance, temporal_integrity)
    × bounded_reuse_effect

certified_inflow = Q × verified_yield × reuse
```

Both rates are clipped to `[0,1]`, so `certified_inflow <= Q`.

Residual generation includes unverified candidate work and an explicit unknown-work term:

```text
residual_generation = Q × (1 - verified_yield) + unknown_rate × Q
dR/dt = residual_generation - repair
```

Gross capital is updated by certified inflow minus natural decay, evidence expiry, memory
staleness, monoculture pressure, and incident losses. Resources are reduced by candidate
generation, residual repair, capital maintenance, module implementation, and module operation.

## The 13 readiness dimensions

Assess every dimension as `observed`, `bounded`, or `unknown`. Do not turn missing evidence into a
numeric zero or an inferred score.

| Identifier | Operational meaning | Simulator mapping |
|---|---|---|
| `provenance_integrity` | Source, evidence, transformation, and authority lineage remain traceable. | provenance state |
| `trust_quorum` | Trust is supported by provenance and genuinely independent checks. | geometric mean of provenance and independence |
| `temporal_integrity` | Evidence and authority remain current for the claim window. | temporal-integrity state |
| `structural_reachability` | Valid work can reach required participants and constrained execution paths. | geometric mean of coordination and availability |
| `causal_formation` | Mechanisms and comparisons support the claimed intervention effect. | causal-support state |
| `dimensional_consistency` | Artifacts, constraints, and interfaces remain compatible across transformations. | availability-bandwidth state |
| `exact_self_maintenance` | Certified procedures can be retained and maintained with available resources. | geometric mean of memory and resource adequacy |
| `finite_horizon_resource_persistence` | Resource stock persists over the declared finite horizon. | `B / (B + kappa_B)` |
| `target_bound_generative_catalysis` | Certified inflow is produced for the declared target, not merely more output. | `inflow / (inflow + inflow_scale)` |
| `verification_capacity` | Verification throughput keeps pace with candidate generation. | verification coverage |
| `effective_independence` | Checks remain useful after correlated-error and monoculture effects. | effective-independence state |
| `coordination_protocol_integrity` | Routing, recovery, responsibility, and release protocols remain coherent. | coordination-integrity state |
| `perturbation_robustness` | The system resists shocks, false promotion, and monoculture pressure. | `1 - hazard_pressure` |

This mapping is inspired by the Collective Phase Control Fabric. It is not CPCF certification.

## Readiness, proxy capital, and reproduction

The default dimension aggregate is a bottleneck-sensitive generalized mean:

```text
G_p(d) = [sum_j w_j × (d_j + epsilon)^p]^(1/p),  p = -4
```

Weights are normalized and non-negative. A weak dimension therefore constrains the aggregate more
than it would under an arithmetic mean. The simulator can also use minimum, harmonic, or geometric
aggregation.

```text
residual_factor = exp[-lambda_R × R / (K + epsilon)]
Phi = G_p(d) × residual_factor
A = K × Phi
```

- `Phi` is protocol-relative phase readiness.
- `A` is protocol-relative ASI-proxy capital.
- A high `K` with weak readiness or large residual debt can still produce low `A`.

The capability reproduction number is:

```text
R_cap = certified_inflow / (natural_loss + monoculture_loss + epsilon)
```

`R_cap > 1` means only that modeled inflow exceeds those modeled losses. It is necessary but never
sufficient for a candidate regime.

## Candidate-regime gate

The label `candidate ASI-proxy growth regime` is allowed only when all of these conditions pass for
the configured `hold_steps`:

1. readiness reaches the scenario threshold;
2. `R_cap > 1`;
3. residual debt divided by capital stays below its threshold;
4. verification coverage reaches its threshold;
5. resource stock stays above its floor;
6. no unresolved uncertain input or critical unknown remains; and
7. all conditions persist for the complete hold period.

A failed gate, a missing observation, or no-transition result is a valid outcome. Never relabel it
as partial ASI attainment.

## How an agent should use the model

1. Establish a concrete objective, finite scope, authority boundary, horizon, and evidence window.
2. Record evidence for each dimension and mark unmeasured dimensions `unknown`.
3. Identify the lowest supported dimension and any gate that already fails.
4. Choose the smallest non-overlapping intervention stack that addresses the binding evidence.
5. Price implementation, operating, verification, repair, and maintenance costs.
6. Run baseline and intervention scenarios from a matched resource envelope.
7. Test shocks, delayed adoption, expiry, rollback, correlated failures, and parameter uncertainty.
8. Report residuals, critical unknowns, no-transition frequency, and the next binding dimension.

Repository metadata, maturity labels, commits, stars, release tags, and documentation volume are
not effect sizes. Intervention effects remain assumptions unless independently measured for the
declared deployment.

## Required non-claims

Preserve these boundaries in every diagnosis and intervention packet:

- no prediction of ASI, time to ASI, or probability of superintelligence;
- no claim that `A`, `Phi`, or `R_cap` measures general intelligence;
- no inference that software availability equals adoption or operational effectiveness;
- no causal attribution from a scenario difference to a repository;
- no treatment of synthetic uncertainty bands as total real-world uncertainty;
- no claim that numerical convergence validates the equations or scientific interpretation;
- no claim that a complete ledger makes its contents true;
- no claim that verifier count implies independent verification;
- no claim that a phase profile creates or certifies a scientific phase transition; and
- no consequential deployment recommendation without independent empirical, security, domain,
  and governance review.
