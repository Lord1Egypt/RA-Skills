# Glossary

## Contents

- [Core model terms](#core-model-terms)
- [Evidence and agency terms](#evidence-and-agency-terms)
- [The 13 operational dimensions](#the-13-operational-dimensions)
- [Research-corpus terms](#research-corpus-terms)

Definitions in this file are operational conventions for the skill. They do not
create natural constants or scientific certifications.

## Core model terms

**Protocol-relative ASI-Proxy Capital (`A`)**
A model-internal quantity for capability that is both accumulated and phase-ready
under a declared protocol. The simulator defines `A = K × Phi`. It is not a measure
of real ASI or a prediction of ASI arrival.

**Gross certified reusable capability (`K`)**
The modeled stock of capability admitted through the current verification and reuse
gates before the readiness factor is applied. “Certified” means certified relative
to declared evidence and checks, not externally proven true.

**Phase readiness (`Phi`)**
A bottleneck-sensitive aggregation of 13 operational dimensions, multiplied by a
penalty for residual debt relative to capability. Low or unknown dimensions constrain
readiness.

**Candidate ASI-proxy growth regime**
A period in which all configured gates—readiness, capability reproduction, residual
ratio, verification coverage, resource floor, critical unknowns, and hold
duration—pass. It is a protocol-relative simulator status, not an ASI event.

**Capability reproduction number (`R_cap`)**
Certified inflow divided by modeled natural and monoculture-related losses, with a
small numerical stabilizer. Values above one mean modeled inflow exceeds modeled
losses; this condition is necessary but not sufficient for a candidate regime.

**Residual debt (`R`)**
Unresolved work, contradictions, defeaters, missing evidence, and unknowns that have
not passed the relevant repair or discharge process. Residual debt remains visible
rather than being counted as successful capability.

**Binding dimension**
The readiness dimension currently exerting the strongest bottleneck effect. It is a
diagnostic output relative to the current measurements and aggregation rule.

**Critical unknown**
An unknown whose resolution could change a gate, authorization decision, safety
boundary, or interpretation of the result. A candidate regime must not be asserted
while a configured critical-unknown gate fails.

## Evidence and agency terms

**Observable-only**
Reasoning and control based on declared, finite observations and artifacts. It does
not assume access to hidden internal truth. Observable evidence can still be
incomplete, manipulated, or causally insufficient.

**No-meta**
An operating condition without reliance on an infallible external meta-evaluator.
It does not mean “no governance,” “no human authority,” or “no independent review.”
The skill substitutes explicit protocols, evidence boundaries, plural verification,
and visible unknowns.

**Evidence gate**
A declared check that determines whether an artifact or claim may advance to a later
state. Passing a gate establishes only the conditions implemented by that gate.

**Certified reusable capability**
A procedure, artifact, or workflow that passes declared evidence, provenance,
validity, and reuse conditions for a specified receiver and scope. Reuse outside that
scope requires a new check.

**Observed / bounded / unknown**
Three evidence statuses used in phase assessment:

- `observed`: supported by a traceable measurement or artifact;
- `bounded`: only a justified interval or one-sided limit is available;
- `unknown`: available evidence does not support a value or bound.

**Intervention packet**
The machine-readable record of an objective, authority boundary, phase assessment,
sources, intervention mechanism, cost, rollback, validation, residuals, non-claims,
and outcome.

**Non-claim**
An explicit statement of what evidence or validation does not establish. Non-claims
prevent local checks from being promoted into stronger scientific or operational
conclusions.

## The 13 operational dimensions

**Provenance integrity (`provenance_integrity`)**
Quality and continuity of source, evidence, transformation, and authority lineage.

**Trust quorum (`trust_quorum`)**
Joint support from provenance and effectively independent checking; not reputation
or majority agreement alone.

**Temporal integrity (`temporal_integrity`)**
Whether evidence, authority, and claims remain valid at the relevant time and
horizon.

**Structural reachability (`structural_reachability`)**
Whether capability can traverse required interfaces, dependencies, and coordination
paths under current constraints.

**Causal formation (`causal_formation`)**
Strength of mechanistic, intervention, or comparison support for the claimed effect.
Correlation alone is insufficient.

**Dimensional consistency (`dimensional_consistency`)**
Compatibility of types, units, scopes, interfaces, and composition assumptions.

**Exact self-maintenance (`exact_self_maintenance`)**
Ability to retain verified procedures and operating conditions without silently
changing their meaning or requirements.

**Finite-horizon resource persistence (`finite_horizon_resource_persistence`)**
Adequacy of compute, energy, bandwidth, verification labor, and operational reserves
over the declared horizon.

**Target-bound generative catalysis (`target_bound_generative_catalysis`)**
Generation or improvement that is connected to the declared objective and admitted
as verified inflow, rather than raw output volume.

**Verification capacity (`verification_capacity`)**
Coverage and throughput of relevant checking relative to candidate generation.

**Effective independence (`effective_independence`)**
Independence remaining after shared data, models, prompts, institutions, or failure
modes are considered.

**Coordination protocol integrity (`coordination_protocol_integrity`)**
Reliability of task routing, ownership, handoffs, recovery, and multi-party
obligations.

**Perturbation robustness (`perturbation_robustness`)**
Ability to remain within declared operating bounds under drift, attack, shocks,
overload, and other perturbations.

## Research-corpus terms

**Canonical paper record (`canonical_paper`)**
One DOI-backed row from the released `papers` configuration of
`kadubon/paper-tex-corpus`.

**Archive-only provenance record (`archive_only_provenance`)**
A retained source archive without an asserted catalog DOI. It is useful for
provenance and historical completeness, not DOI-level bibliographic citation.

**Catalog summary**
The extractive first sentence from the catalog abstract used for quick routing. It
does not replace reading the source.

**Routing metadata**
Themes, method terms, and phase dimensions retained only with a versioned rule,
catalog field, matched span, confidence, and review status. They help source
selection and are not scientific evaluations.

**Selection eligibility (`default`, `conditional`, `context_only`)**
A source-use policy derived from pinned license, role, maturity, dependency, and
evidence observations. `default` means eligible for consideration, not automatically
correct. `conditional` requires the stated checks. `context_only` must not be chosen
as the default intervention.
