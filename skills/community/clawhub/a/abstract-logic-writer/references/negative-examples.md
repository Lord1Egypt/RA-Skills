# Negative Examples and Rule Tags

All rewrites in this file are intentionally bad. They are included as negative teaching material, not as templates.

## Example 1: Orbital service orchestration

### Negative rewrite

Satellite services are important. Existing orchestration is a challenge. Unlike prior work, we build a task-centric framework - it uses mission semantics and two stages. Simulations are good and show effectiveness.

### Violated predicates

- `summary_only(s1)`
- `summary_only(s2)`
- `forbidden_marker(unlike)`
- `forbidden_marker(em_dash)`
- `weak_evidence(s4)`
- `scope_inversion(s3)` because the framework appears before its operational purpose is grounded

## Example 2: Low-altitude foundation model

### Negative rewrite

Low-altitude missions change online and follow many rules. LaFo is a foundation model for better planning. With the growth of applications, the model develops state consistency and good success rates. It is useful in experiments.

### Violated predicates

- `selection_mismatch(growth, applications)`
- `unsupported_idea(s2)`
- `summary_only(s4)`
- `evidence_without_metric(s3)`

## Example 3: AERO ontology

### Negative rewrite

Low-altitude systems need physical, information, and legal reasoning. We provide AERO, which is an ontology suite. The ontology is for rules and constraints. This paper is important for reuse.

### Violated predicates

- `orphan_concept(s2)` because the purpose and operational interface remain weak
- `summary_only(s4)`
- `purpose_underdeveloped(s3)`
- `missing_evidence(E)`

## Example 4: LLM-collaborative TAMP

### Negative rewrite

Complex aerial operations are difficult. The problem is combinatorial and geometric. We therefore use an LLM system. It has cloud, edge, and terminal parts, and the success rate is high.

### Violated predicates

- `summary_only(s1)`
- `challenge_not_operationalized(s2)`
- `idea_not_grounded(s3)`
- `evidence_without_setup(s4)`

## Example 5: Lexical mismatch micro-case

### Negative rewrite

With the growth of applications, the ontology grows more practical.

### Violated predicates

- `selection_mismatch(growth, applications)`
- `selection_mismatch(grow, ontology)`
- `missing_relation_target` because the sentence does not state what practical change occurs or for which task

## How to use these negatives

1. Keep the core topic intact.
2. Break exactly one or several named predicates.
3. Label each broken predicate explicitly.
4. If the user asks for contrastive learning material, pair each negative rewrite with a repaired version and a terse explanation of the repair.
