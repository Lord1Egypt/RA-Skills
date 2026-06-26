# Mathematical Foundations

## Table of Contents

1. [Overview](#overview)
2. [Formal Axiomatic Systems](#formal-axiomatic-systems)
3. [Bayesian Assumption Networks](#bayesian-assumption-networks)
4. [Information-Theoretic Metrics](#information-theoretic-metrics)
5. [Consistency Verification Algorithms](#consistency-verification-algorithms)
6. [Quantitative Confidence Calibration](#quantitative-confidence-calibration)

---

## Overview

Qualitative first-principles reasoning is powerful, but mathematical formalization enables precision, automation, and quantifiable confidence.

This document provides the mathematical infrastructure for transforming the qualitative framework into a quantitative system.

**Principle**: Mathematics is the language of first principles. Where physics uses calculus, first-principles reasoning uses formal logic, probability theory, and information theory.

---

## Formal Axiomatic Systems

### Hilbert's Program for First Principles

A formal axiomatic system consists of:

1. **Alphabet**: Set of symbols (propositions, connectives, quantifiers)
2. **Formation rules**: Well-formed formula (WFF) construction
3. **Axiom schema**: Template for generating axioms
4. **Inference rules**: Rules for deriving theorems (e.g., modus ponens)

### First-Principles Axiom Schema

**Template 1: Universal Quantification**
```
∀x ∈ D: P(x) → Q(x)
```
Where D is the domain, P(x) is the antecedent, Q(x) is the consequent.

**Example**: ∀ closed systems S: energy_conserved(S)

**Template 2: Existential Quantification**
```
∃x ∈ D: P(x)
```
**Example**: ∃ failure modes F: unpredictable(F)

**Template 3: Conditional Axiom**
```
∀x ∈ D: P(x) → (Condition(x) → Q(x))
```
**Example**: ∀ products P: viable(P) → (market_size(P) > threshold → successful(P))

### Axiom Independence Test

Use linear algebra to test independence:

1. Represent each axiom as a vector in a high-dimensional space
2. Construct a matrix where rows are axiom vectors
3. Compute the rank of the matrix
4. If rank < number of axioms, some axioms are linearly dependent (not independent)

**Algorithm**:
```python
import numpy as np

def test_axiom_independence(axioms):
    # Convert axioms to feature vectors (embedding or logical representation)
    vectors = [axiom_to_vector(a) for a in axioms]
    matrix = np.array(vectors)
    rank = np.linalg.matrix_rank(matrix)
    return rank == len(axioms), rank
```

---

## Bayesian Assumption Networks

### Network Structure

Model assumptions as nodes in a Bayesian network:

```
A1 → A2 → A3
 ↓     ↓
A4 ← A5 → A6
```

Edges represent dependency: "A1 implies A2" or "A1 influences A2"

### Node Types

1. **Root nodes**: Assumptions with no parents (fundamental axioms)
2. **Intermediate nodes**: Assumptions derived from others
3. **Leaf nodes**: Final conclusions or observable claims

### Probability Distributions

Each node has a Conditional Probability Table (CPT):

**For root nodes**: P(Ai) (prior probability)
**For intermediate nodes**: P(Ai | parents(Ai))

**Example CPT for A2 given A1**:
```
P(A2 | A1=True) = 0.9
P(A2 | A1=False) = 0.1
```

### Inference

Use Bayes' theorem to update beliefs:

```
P(Ai | evidence) = P(evidence | Ai) × P(Ai) / P(evidence)
```

**Algorithm**: Use belief propagation (Pearl's algorithm) for exact inference in polytrees.

### Assumption Sensitivity Analysis

Compute the sensitivity of conclusions to each assumption:

```
Sensitivity(Conclusion, Assumption) = |∂P(Conclusion)/∂P(Assumption)|
```

High sensitivity = assumption is critical; verify carefully.

---

## Information-Theoretic Metrics

### Axiom Information Content

Use Shannon entropy to measure the information content of an axiom:

```
H(Axiom) = -Σ p(xi) × log₂ p(xi)
```

Where p(xi) is the probability of the axiom being in state xi.

**Interpretation**:
- High entropy = high uncertainty (less confidence)
- Low entropy = low uncertainty (more confidence)

**Example**:
- Axiom: "Energy is conserved"
  - P(True) = 0.9999, P(False) = 0.0001
  - H = -(0.9999 × log₂0.9999 + 0.0001 × log₂0.0001) ≈ 0.001 bits
  - Low entropy = high confidence

### Mutual Information Between Axioms

Measure how much one axiom tells us about another:

```
I(A, B) = H(A) - H(A | B)
```

**Interpretation**:
- High mutual information = axioms are tightly coupled
- Low mutual information = axioms are independent

**Use case**: Detect redundant axioms (if I(A, B) is very high, one may be unnecessary).

### Kullback-Leibler Divergence

Measure the "distance" between prior and posterior beliefs:

```
D_KL(P || Q) = Σ P(x) × log₂ (P(x) / Q(x))
```

Where P is the posterior distribution, Q is the prior.

**Use case**: Quantify how much evidence updates beliefs.

---

## Consistency Verification Algorithms

### Propositional Logic Consistency

Use SAT (Satisfiability) solvers to check for contradictions:

**Algorithm**:
1. Convert each assumption to a propositional formula
2. Negate the conclusion: ¬C
3. Check if {A1, A2, ..., An, ¬C} is satisfiable
4. If unsatisfiable, C is entailed by {A1, ..., An}
5. If satisfiable, find the satisfying assignment (counterexample)

**Example**:
```
A1: A → B
A2: B → C
Conclusion: A → C

Check {A1, A2, ¬(A → C)} = {A → B, B → C, A ∧ ¬C}
= {¬A ∨ B, ¬B ∨ C, A, ¬C}
Unsatisfiable → Conclusion is valid
```

### First-Order Logic Consistency

For quantified statements, use resolution or tableaux methods.

**Algorithm**:
1. Convert all statements to conjunctive normal form (CNF)
2. Apply resolution: resolve pairs of clauses with complementary literals
3. If the empty clause is derived, the set is inconsistent
4. If no more resolutions possible and no empty clause, consistent

### Probabilistic Consistency

Check if probability assignments are coherent:

**Constraints**:
1. P(A) ∈ [0, 1] for all A
2. P(True) = 1, P(False) = 0
3. P(A ∨ B) = P(A) + P(B) - P(A ∧ B)
4. P(A | B) = P(A ∧ B) / P(B) when P(B) > 0

**Algorithm**: Use linear programming to check feasibility.

---

## Quantitative Confidence Calibration

### Prior Confidence Assignment

Assign prior probabilities to assumptions based on evidence strength:

| Evidence Type | Prior Confidence |
|---------------|------------------|
| Mathematical proof | 0.9999 |
| Physical law (well-tested) | 0.99 |
| Strong empirical evidence | 0.9 |
| Weak empirical evidence | 0.7 |
| Expert consensus | 0.6 |
| Plausible but untested | 0.5 |
| Speculative | 0.3 |

### Bayesian Update with Evidence

**Evidence strength parameter (λ)**:
- Strong evidence: λ = 10 (10:1 likelihood ratio)
- Moderate evidence: λ = 3
- Weak evidence: λ = 1.5

**Update rule**:
```
P(A | evidence) = λ × P(A) / (λ × P(A) + (1 - P(A)))
```

**Example**:
- Prior: P(A) = 0.6
- Strong evidence for A (λ = 10)
- Posterior: P(A | E) = (10 × 0.6) / (10 × 0.6 + 0.4) = 6 / 6.4 ≈ 0.94

### Confidence Aggregation

Combine confidence from multiple sources:

**Product rule (independent sources)**:
```
P_conjunction = Π P_i
```

**Average rule (correlated sources)**:
```
P_aggregate = (Σ P_i) / n
```

**Log-odds aggregation (robust)**:
```
L = Σ log(P_i / (1 - P_i))
P_aggregate = 1 / (1 + e^(-L))
```

### Calibration Curve

Check if confidence predictions are well-calibrated:

1. Group predictions by confidence (0-0.1, 0.1-0.2, ..., 0.9-1.0)
2. For each group, compute the actual accuracy
3. Plot predicted confidence vs. actual accuracy
4. Perfect calibration: points lie on the diagonal

---

## When to Use This Reference

**Use during Phase 2 (Assumption Extraction) and Phase 3 (Verification)**.

**Apply to**:
- Building assumption networks with dependency structures
- Quantifying confidence in assumptions
- Checking logical consistency
- Measuring information content of axioms
- Performing sensitivity analysis

**Mathematical Tools Checklist**:
- [ ] Assumptions modeled as Bayesian network
- [ ] Prior probabilities assigned based on evidence
- [ ] Consistency verified with SAT solver or resolution
- [ ] Information entropy computed for each axiom
- [ ] Mutual information computed to detect redundancy
- [ ] Confidence calibrated with evidence
- [ ] Sensitivity analysis performed for critical assumptions
- [ ] Calibration curve generated (if historical data available)
