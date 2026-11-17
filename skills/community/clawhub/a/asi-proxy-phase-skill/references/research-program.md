# Research Program Guide

## Contents

- [Purpose and evidential status](#purpose-and-evidential-status)
- [Seven connected themes](#seven-connected-themes)
- [How the themes map to phase diagnosis](#how-the-themes-map-to-phase-diagnosis)
- [Recommended reading workflow](#recommended-reading-workflow)
- [Corpus record policy](#corpus-record-policy)
- [Boundaries](#boundaries)

## Purpose and evidential status

This guide condenses the paper corpus into a navigation layer for an agent using the
ASI-Proxy Phase skill. It does not treat the papers as verified facts, an evaluation
benchmark, or evidence that artificial superintelligence exists. The corpus consists
primarily of preprints and formal proposals. Use each paper as a source of hypotheses,
definitions, failure modes, and candidate mechanisms; verify any claim against the
paper, executable evidence, and the current workspace before acting on it.
This synthesis is a navigation layer derived from catalog titles, abstracts, and
keywords. It does not assert that every paper endorses the synthesis or that a
catalog-level relation survives full-text review.

The unifying research question is:

> How can autonomous or collective intelligent systems improve while remaining
> observable, auditable, semantically persistent, resource-bounded, corrigible, and
> compatible with explicit governance and welfare constraints?

For this skill, that question is operationalized through a protocol-relative
candidate ASI-proxy growth regime. This is a modeling construct, not an ASI claim.
The skill uses the literature to locate a binding readiness dimension and to design
the smallest evidence-gated intervention that can be tested in the current workspace.

## Seven connected themes

### 1. Self-organization and self-improvement

The corpus develops architectures and formal proposals for autopoiesis, recursive
self-improvement, teleogenesis, autonomous poiesis, collective adaptation, and
capability accumulation. Later work increasingly distinguishes raw generation or
controller scale from reusable capability that survives verification, transfer,
maintenance, and drift.

Use this theme when the task concerns self-modification, capability growth,
autonomous research, emergence, or a transition from one-off outputs to durable
procedures. Do not infer improvement from output volume alone.

Representative catalog anchors: CAIT
(`10.5281/zenodo.20061296`) for certified capability reproduction and ECPT
(`10.5281/zenodo.20535654`) for execution-available capability propagation.
These are formal/navigation anchors, not evidence that recursive improvement occurs
in a deployed system.

### 2. Observable-only and no-meta assurance

This theme asks how an agent can operate without an assumed hidden, infallible
meta-judge. It develops typed claims, replayable artifacts, audit gates, certificate
algebras, provenance ledgers, verifier ecologies, claim-status semantics, and
authority protocols. A recurring principle is that finite validators check declared
records and recomputable conditions; they do not establish the truth or completeness
of external evidence.

Use this theme for verification bottlenecks, claim release, authority migration,
proof-carrying workflows, audit closure, or uncertainty that must remain visible.

Representative catalog anchors: typed autonomous research-claim certification
(`10.5281/zenodo.19427818`) and Verifier Ecology Theory
(`10.5281/zenodo.21147093`). Their finite validators remain scoped to declared
records and procedures.

### 3. Semantics, memory, and persistence

These papers study persistent meaning under limited observation, ontology drift,
coarse-graining, non-Markovian dynamics, memory truncation, representation changes,
and self-modification. They distinguish stored data from semantically or
procedurally valid memory and explore conditions under which an identity, law,
value, or workflow remains comparable over time.

Use this theme for memory promotion, stale evidence, semantic translation,
long-context search, continuity, or the risk that a changing evaluator invalidates
an apparent gain.

Representative catalog anchors: MemoryFlow
(`10.5281/zenodo.18136347`) and Sovereign Epistemic Commons
(`10.5281/zenodo.18997828`). Catalog summaries support this routing; persistent
semantic validity still requires task-specific evidence.

### 4. Thermodynamic and physical constraints

The corpus treats energy, exergy, compute, I/O, finite resources, physical ledgers,
and persistence horizons as constraints rather than metaphors. It includes
thermodynamic inequalities, resource-aware inference and training, availability
analysis, scaling bottlenecks, and links from AI capability to physical and
institutional production.

Use this theme when an intervention may improve a score while exhausting compute,
verification labor, energy, bandwidth, or operational reserves.

Representative catalog anchors: thermodynamic lower bounds for inference-memory
dynamics (`10.5281/zenodo.17946113`) and evidence-carrying physical ledgers
(`10.5281/zenodo.21531413`). Variational free-energy language alone is not routed as
physical resource accounting.

### 5. Mathematical structures

The mathematical program uses category theory, topoi, profunctors, Kan extensions,
homotopy, information geometry, optimal transport, gradient flows, formal concept
lattices, law spaces, holographic quotients, and dynamical systems. These structures
provide languages for composition, comparison, persistence, translation, and
multi-scale organization.

Use this theme to obtain a formal model or compositional interface. Do not substitute
formal elegance for empirical calibration or executable evidence.

Representative catalog anchors: the unified computational-autopoiesis/category
theory synthesis (`10.5281/zenodo.16420862`) and Fractal Category Theory
(`10.5281/zenodo.17292137`). Mathematical structure is not an implementation or
empirical-effect claim.

### 6. AI systems and operations

Operational papers address LLM routing, inference reuse, agent workflows, benchmark
decay, split inference, long-running search, training bottlenecks, telemetry,
deployment gates, and AI-scientist protocols. The focus is often on finite,
machine-readable artifacts and diagnostics that can be reproduced locally.

Use this theme when translating a theoretical construct into code, a test harness,
a schema, a runtime gate, or a resource-matched experiment.

Representative catalog anchors: certified workflow conversion
(`10.5281/zenodo.19994795`) and verification-limited intelligence acceleration
(`10.5281/zenodo.18436828`). Use their pinned companion repositories only after
checking license, dependencies, and local fit.

### 7. Governance, welfare, and coexistence

The governance strand examines authority, consent, non-capture, sovereignty,
participation, liberty, institutional identifiability, coexistence, suffering,
benevolent propagation, and human-AI welfare. It emphasizes declared boundaries,
rights, exit conditions, burden of proof, and limits on what observable data can
justify.

Use this theme when capability changes affect people, institutions, authorization,
or welfare. A technical gain does not override consent, authority, or external
governance requirements.

Representative catalog anchors: Consent-Bounded Contact Theory
(`10.5281/zenodo.20678428`) and Asymmetric Coexistence Theory
(`10.5281/zenodo.20694904`). They supply problem framings, not legal authority or
evidence of real-world welfare effects.

## How the themes map to phase diagnosis

The themes are broader than the simulator's 13 dimensions. Use the dimensions as a
diagnostic index, not as paper-quality scores:

| Research concern | Phase dimensions commonly implicated |
| --- | --- |
| Evidence lineage and claim release | provenance integrity, trust quorum, temporal integrity, verification capacity |
| Capability transport and reuse | structural reachability, dimensional consistency, exact self-maintenance |
| Mechanistic comparison | causal formation, effective independence |
| Sustained improvement | target-bound generative catalysis, finite-horizon resource persistence |
| Multi-agent operation | coordination protocol integrity, trust quorum |
| Drift, attack, and failure | perturbation robustness, temporal integrity |

The per-paper mappings in `papers.jsonl` are conservative keyword-derived routing
hints. They are not measurements and may be empty when the source does not clearly
support a mapping.

## Recommended reading workflow

1. Start with the current objective and observed evidence, not with a favored theory.
2. Identify the lowest or unknown phase dimension that could block the objective.
3. Query `papers.jsonl` by dimension, theme, title, DOI, or keyword.
4. Read the catalog summary and keywords to shortlist papers.
5. Follow the canonical DOI URL and inspect the source before relying on a formal
   condition, equation, or implementation detail.
6. Prefer an executable repository only where `related_repositories` records a
   traceable framework/title correspondence; otherwise consult `repository-map.md`.
7. Record unknowns, alternative explanations, resource costs, and non-claims in the
   intervention packet.

## Corpus record policy

- `canonical_paper` records are the 227 rows in the released `papers` Parquet
  configuration. Each retains its DOI and canonical catalog URL.
- `archive_only_provenance` records are the four rows in the released
  `archive_only` configuration. They retain archive hashes and have no asserted DOI
  or canonical URL.
- `summary` is an extract from the first sentence of the catalog abstract, shortened
  only when necessary. It is not an independent interpretation or validation.
- Theme, method, and phase-dimension labels are deterministic routing metadata based
  on titles, abstracts, and keywords. Agents must treat them as search aids.
- Repository links are included only for distinctive title or named-framework
  correspondences to public `kadubon` repositories.

See `source-state.json` for snapshot hashes, counts, exclusions, and derivation rules.

## Boundaries

- Do not use the corpus to certify ASI, consciousness, benevolence, safety, or a
  scientific phase transition.
- Do not convert missing evidence into a favorable score.
- Do not treat a DOI, formal theorem, schema-valid packet, or passing test as proof of
  real-world effectiveness.
- Do not infer a DOI for an archive-only record.
- Do not aggregate overlapping paper or repository effects as independent evidence.
- Preserve the distinction between a model-internal candidate regime and an observed
  external outcome.
