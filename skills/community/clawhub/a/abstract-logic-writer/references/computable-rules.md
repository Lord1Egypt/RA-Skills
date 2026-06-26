# Computable Rules for Abstract Construction

This file defines the abstract as a finite ordered structure that can be checked symbolically.

## 1. Symbols

Let the abstract be a sentence sequence

`S = <s1, s2, ..., sn>`.

Let the discourse-role set be

`R = {B, P, M, C, I, T, E}`

where:

- `B`: background
- `P`: present state or gap framing
- `M`: motivation
- `C`: challenge or obstacle
- `I`: idea or thesis move
- `T`: technique or mechanism
- `E`: evidence, outcome, or operational implication

Let `rho : S -> R` map each sentence to one primary role.

Let `tau : X -> U` map a lexical item or phrase to an upper-ontology type in

`U = {quantity, quality, process, artifact, capability, relation, task, constraint, metric}`.

Let the core semantic relations be:

- `motivates(x, y)`
- `addresses(x, y)`
- `enables(x, y)`
- `implemented_by(x, y)`
- `evaluated_by(x, y)`
- `for(x, y)` where `x` is an artifact or mechanism and `y` is a task or objective
- `to(v, y)` where `v` is an action or process and `y` is the intended objective

## 2. Well-formedness constraints

### 2.1 Mandatory roles

A valid short abstract must contain the image set `{M, C, I}`.

Formally:

`{M, C, I} subseteq Im(rho)`.

`B`, `P`, `T`, and `E` are optional, but `E` is strongly preferred for research papers that report experiments.

### 2.2 Global role order

Use the partial order

`B <= P <= M <= C <= I <= T <= E`.

If some roles are omitted, the remaining role subsequence must still respect this order.

Equivalent check:

`i < j  =>  ord(rho(si)) <= ord(rho(sj))`.

### 2.3 No orphan challenge

If a sentence is tagged as `C`, some later sentence must provide an idea or mechanism.

`rho(si) = C  =>  exists j > i : rho(sj) in {I, T}`.

### 2.4 No unsupported idea

If a sentence is tagged as `I`, the same sentence or the next sentence must state purpose, mechanism, or evidence.

`rho(si) = I  =>  exists j in {i, i+1} : purpose(si, sj) or rho(sj) in {T, E}`.

### 2.5 Terminal load constraint

The last sentence cannot be pure recap. It must carry mechanism, evidence, or operational implication.

`rho(sn) in {T, E}`.

## 3. Intra-sentence hierarchy

Represent each sentence as

`mu(si) = <g, d, o>`

where:

- `g`: governing claim with broader scope
- `d`: detail, explanation, or local asymmetry
- `o`: consequence, purpose, or operational effect

A sentence is well-formed when all three conditions hold:

1. `level(g) >= level(d)`
2. `instantiates(d, g) or explains(d, g)`
3. `causes(d, o) or enables(d, o) or constrains(d, o) or measures(o, d)`

This encodes the broad-to-narrow progression requested by the user. A local fact should not appear before the governing concept that licenses it.

## 4. Concept-introduction constraints

### 4.1 Motivation adjacency

When a new concept `x` is introduced, its motivation, purpose, or consequence must appear in the same sentence or an adjacent sentence.

`new(x, si)  =>  motive(x, si) or exists j in {i-1, i, i+1} : purpose(x, sj) or consequence(x, sj)`.

### 4.2 Explanation must terminate in purpose or relation

A concept explanation is incomplete if it only names the concept. It must terminate in purpose, relation, or operational effect.

`explain(x, si)  =>  purpose(x, si) or exists y : relation(x, y, si)`.

## 5. Summary-only prohibition

Define

`summary_only(si) := copular(si) and generic_head(si) and not cause(si) and not purpose(si) and not operational_term(si)`.

Typical invalid skeletons:

- `X is a challenge.`
- `Y is important.`
- `Z is a useful method.`

These can be repaired by appending cause, scope, or operational consequence.

## 6. Purpose and contribution relations

The user explicitly asked for computable handling of motivation, contribution, and `for` / `to` relations. Use the following schemas.

### 6.1 Artifact-purpose schema

`artifact(a) and task(t) and for(a, t)`

Example pattern:

`a lightweight parser for logical constraint extraction`

### 6.2 Action-purpose schema

`process(v) and objective(o) and to(v, o)`

Example pattern:

`translate mission goals to logical service chains`

### 6.3 Contribution schema

A research contribution should usually satisfy:

`introduces(a) and addresses(a, c) and implemented_by(a, m) and evaluated_by(a, e)`

where `a` is the proposed artifact, `c` is the challenge, `m` is the mechanism, and `e` is the evidence.

## 7. Lexical-selection interface

Selection mismatch is a type error.

Let `Sel(v)` be the set of upper-ontology types licensed by verb `v`.
A phrase is type-correct when:

`tau(noun_phrase) intersect Sel(v) != emptyset`.

Example:

- `tau(applications) = artifact`
- `Sel(grow) = {quantity}`
- therefore `grow(applications)` is rejected
- but `develop(applications)` is licensed because `artifact in Sel(develop)`

## 8. Scoring function and pairwise comparison

Use a bounded score in `[0, 100]` where a larger value indicates a better abstract fragment under this skill's logic.

`Score(F) = clip(100 - 20*M_core - 10*V_order - 8*V_summary - 6*V_marker - 4*V_select - 4*V_terminal + 5*Q_relation + 7*Q_evidence, 0, 100)`

where:

- `M_core`: number of missing core roles among `{M, C, I}`
- `V_order`: number of discourse-order violations
- `V_summary`: number of `summary_only` sentences
- `V_marker`: number of forbidden markers such as the em dash or `Unlike`
- `V_select`: number of verb-noun selection mismatches
- `V_terminal`: terminal-load violations where the last sentence is not mechanism or evidence bearing
- `Q_relation`: number of validated purpose or contribution links, capped per sentence
- `Q_evidence`: number of evidence-bearing sentences with metrics, outcomes, or measurable operational claims

For pairwise comparison between fragments `A` and `B`, define:

`Delta(B, A) = Score(B) - Score(A)`

Interpretation:

- `Delta(B, A) > 0`: `B` is better under the formal metric
- `Delta(B, A) = 0`: the two fragments are tied under the current rule set
- `Delta(B, A) < 0`: `A` is better

The machine-readable implementation lives in `assets/discourse_rules.json` and `scripts/abstract_score.py`.

## 9. Minimal valid plans

### 4-sentence plan

- `s1 = M`
- `s2 = C`
- `s3 = I + T`
- `s4 = E`

### 5-sentence plan

- `s1 = P`
- `s2 = M`
- `s3 = C`
- `s4 = I + T`
- `s5 = E`

If background is needed, prepend `B` without displacing the required order of `M`, `C`, and `I`.
