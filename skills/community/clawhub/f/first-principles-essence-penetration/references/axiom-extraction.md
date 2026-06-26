# Axiom Extraction

## Table of Contents

1. [Overview](#overview)
2. [The Five Axiom Principles](#the-five-axiom-principles)
3. [Axiom vs. Non-Axiom](#axiom-vs-non-axiom)
4. [Axiom Formulation](#axiom-formulation)
5. [Axiom Set Verification](#axiom-set-verification)
6. [Common Mistakes](#common-mistakes)

---

## Overview

After verification, extract true axioms from the surviving assumptions. Axioms are the irreducible, universal, independent foundations of your reasoning.

**Principle**: Axioms must be exceptionally stringent. Many things that seem "true" are not axioms. Distinguish between axioms (first principles) and well-supported beliefs (derived truths).

---

## The Five Axiom Principles

### 1. Irreducibility

**Definition**: An axiom cannot be broken down into simpler components without losing its meaning or truth.

**Test**: Ask "Why is this true?" repeatedly. If you can give a reason (other than "because it's self-evident"), it is not an axiom.

**Procedure**:
1. State the proposition P
2. Ask: "Why is P true?"
3. If an answer exists, go deeper
4. Stop when the only answer is "It cannot be otherwise" or "To ask why is nonsensical"

**Examples**:

| Proposition | Why? | Is it an axiom? |
|-------------|------|-----------------|
| "Energy is conserved" | No simpler explanation; physics law | ✓ Yes |
| "Users want value" | Because value = benefit - cost; because... | ✗ No (reducible) |
| "A ≠ ¬A" | Logical law; cannot be otherwise | ✓ Yes |
| "This market will grow" | Because of trends, demand, competition... | ✗ No (reducible) |

**Irreducible axioms**:
- Logical laws (non-contradiction, excluded middle)
- Physical laws (conservation, causality)
- Mathematical definitions (set theory, arithmetic)

### 2. Universality

**Definition**: An axiom holds across its entire domain of applicability. No exceptions within the domain.

**Test**: Can you conceive of a case within the domain where the axiom would be false?

**Procedure**:
1. Define the domain of applicability (e.g., "all physical systems", "all logical propositions")
2. Search for edge cases or exceptions
3. If an exception exists within the domain, it's not an axiom

**Examples**:

| Proposition | Domain | Exceptions? | Is it an axiom? |
|-------------|--------|-------------|-----------------|
| "Energy is conserved" | All physical systems | No (in closed systems) | ✓ Yes |
| "Customers prefer lower prices" | All customers | Yes (quality-sensitive customers) | ✗ No |
| "A = A" | All logical propositions | No | ✓ Yes |
| "Past predicts future" | All domains | Yes (regime changes, chaos) | ✗ No |

**Note**: Universality is domain-relative. An axiom in one domain may not be an axiom in another. For example, "Euclidean geometry" has axioms that don't hold in "non-Euclidean geometry."

### 3. Independence

**Definition**: An axiom does not depend on other propositions. It cannot be derived from other axioms.

**Test**: Can this proposition be derived from other axioms?

**Procedure**:
1. Identify the candidate axioms set
2. For each proposition, ask: "Can I derive this from the others?"
3. If yes, remove it (it's a theorem, not an axiom)
4. If no, it's an axiom

**Examples**:

**Set A**: {A1: Energy conserved, A2: Momentum conserved, A3: Energy + momentum conserved}

- A3 can be derived from A1 + A2 → A3 is not an axiom
- A1 and A2 are independent (neither can derive the other)

**Result**: True axiom set = {A1, A2}

**Set B**: {B1: All humans are mortal, B2: Socrates is human, B3: Socrates is mortal}

- B3 can be derived from B1 + B2 (syllogism)
- B3 is a theorem, not an axiom

**Result**: True axiom set = {B1, B2} (if we accept them as axioms)

### 4. Verifiability

**Definition**: An axiom must be verifiable (or falsifiable), even if only in principle.

**Test**: Is there a way to verify or falsify this proposition?

**Procedure**:
1. Ask: "What evidence would confirm this?"
2. Ask: "What evidence would falsify this?"
3. If neither exists, the proposition is meaningless or tautological

**Examples**:

| Proposition | Verifiable? | Falsifiable? | Is it an axiom? |
|-------------|-------------|--------------|-----------------|
| "Energy is conserved" | Yes (measure) | Yes (find violation) | ✓ Yes |
| "This product will succeed" | Yes (observe) | Yes (observe failure) | ✗ No (not universal) |
| "God exists" | No (unfalsifiable) | No (unfalsifiable) | ✗ No (not verifiable) |
| "Everything is either P or not P" | No (tautology) | No (tautology) | ✗ No (tautology, not axiom) |

**Note**: Tautologies (e.g., "A = A") are not axioms—they're logical truths with no empirical content. Axioms can be empirical (e.g., conservation laws) or logical (e.g., non-contradiction).

### 5. Necessity

**Definition**: An axiom is necessarily true. It could not be otherwise without contradiction or physical impossibility.

**Test**: Can you conceive of a possible world where this is false?

**Procedure**:
1. Ask: "Imagine a world where this is false. Is that world logically/physically coherent?"
2. If the world is coherent, the proposition is contingent, not necessary
3. If the world is incoherent, the proposition is necessary

**Examples**:

| Proposition | Could it be false? | Is it necessary? | Is it an axiom? |
|-------------|--------------------|------------------|-----------------|
| "2 + 2 = 4" | No (contradiction) | Yes (logical necessity) | ✓ Yes |
| "Water boils at 100°C" | Yes (different pressure) | No (physical contingent) | ✗ No |
| "Energy is conserved" | No (physical impossibility) | Yes (physical necessity) | ✓ Yes |
| "Remote work is productive" | Yes (different culture/tools) | No (contingent) | ✗ No |

**Types of necessity**:
- **Logical necessity**: True in all possible worlds (e.g., A = A, 2 + 2 = 4)
- **Physical necessity**: True in all physically possible worlds (e.g., conservation laws)
- **Contingent truths**: True in some worlds, false in others (not axioms)

---

## Axiom vs. Non-Axiom

### Common Non-Axioms (Disguised as Truths)

| Type | Example | Why not an axiom? |
|------|---------|-------------------|
| **Correlation** | "More features = more value" | Not causal; can reverse; context-dependent |
| **Convention** | "Sprints are 2 weeks" | Arbitrary; could be 1 week, 3 weeks, etc. |
| **Authority** | "Experts say X" | Expert opinion ≠ truth; needs verification |
| **Heuristic** | "Premature optimization is evil" | Rule of thumb; exceptions exist |
| **Observation** | "Users click more on blue buttons" | Empirical regularity; not universal |
| **Preference** | "Minimal design is better" | Axiological; not universally true |
| **Trend** | "AI will replace programmers" | Extrapolation; not guaranteed |
| **Belief** | "Culture is critical" | Plausible but not irreducible |

### True Axioms (Examples)

**Logical Axioms**:
- Law of non-contradiction: A ≠ ¬A
- Law of excluded middle: A ∨ ¬A
- Law of identity: A = A

**Mathematical Axioms**:
- Peano axioms (arithmetic)
- Zermelo-Fraenkel axioms (set theory)

**Physical Axioms**:
- Conservation of energy (closed systems)
- Causality (cause precedes effect)
- Second law of thermodynamics (entropy increases)

**Epistemic Axioms**:
- Falsifiability criterion (scientific claims must be falsifiable)
- Occam's razor (simpler explanations are preferred)

**Systemic Axioms**:
- Complexity arises from interactions (not just parts)
- Feedback loops produce stability or amplification

---

## Axiom Formulation

### Guidelines

1. **Use falsifiable statements**: "X increases Y" is better than "X affects Y"
2. **Be precise**: Avoid vague terms (e.g., "better", "good", "effective")
3. **Specify domain**: "In competitive markets..." or "For biological systems..."
4. **Avoid hidden assumptions**: Each statement should stand alone
5. **Use quantification when possible**: "All users..." or "More than 50% of cases..."

### Reformulation Examples

| Vague | Precise | Axiom? |
|-------|---------|--------|
| "Users want value" | "Users exchange resources for benefits they perceive as greater than cost" | ✗ No (definition) |
| "Energy is conserved" | "In closed physical systems, total energy remains constant over time" | ✓ Yes |
| "Culture matters" | "Shared norms and beliefs influence group behavior" | ✗ No (definition) |
| "Complex systems exhibit emergent properties" | "Systems with interacting components produce behaviors not predictable from component properties alone" | ✓ Yes |

### Axiom Statement Template

```
In the domain of [domain], [statement] under conditions [conditions].

Example: "In the domain of closed thermodynamic systems, total energy
remains constant over time."
```

---

## Axiom Set Verification

After extracting individual axioms, verify the set as a whole.

### 1. Consistency Check

**Test**: Are any axioms contradictory?

**Procedure**:
1. Create a pairwise matrix of all axioms
2. Check each pair for contradiction
3. Resolve contradictions by rejecting one or both axioms

**Example**:
- A1: "All actions have costs"
- A2: "Some actions are free"
- **Contradiction**: A1 and A2 cannot both be true
- **Resolution**: Reject A2 (violates conservation of resources) or refine A1 to "Most actions have costs"

### 2. Independence Check

**Test**: Are any axioms derivable from others?

**Procedure**:
1. For each axiom, attempt to derive it from the others
2. If derivable, remove it (it's a theorem)
3. Repeat until no axiom can be removed

**Example**:
- A1: "Energy is conserved"
- A2: "Momentum is conserved"
- A3: "Energy + momentum is conserved"
- **Derivation**: A3 follows from A1 + A2
- **Resolution**: Remove A3

### 3. Completeness Check

**Test**: Do the axioms cover all necessary aspects of the domain?

**Procedure**:
1. Identify the key aspects of the domain (variables, constraints, relationships)
2. Check if each aspect is addressed by at least one axiom
3. If aspects are missing, ask: "Is this aspect fundamental or derived?"

**Example (Business)**:
- Aspects: Value exchange, resource constraints, market dynamics
- Axioms:
  - A1: "Value exchange requires benefit > cost"
  - A2: "Resources are finite and allocate to highest-value uses"
  - A3: "Market prices equilibrate supply and demand"
- **Coverage**: All aspects covered ✓

### 4. Minimality Check

**Test**: Is the axiom set minimal (no redundant axioms)?

**Procedure**:
1. Temporarily remove each axiom
2. Check if the remaining axioms can still support the domain
3. If yes, the removed axiom is redundant

**Example**:
- A1: "Value exchange requires benefit > cost"
- A2: "Users maximize perceived benefit"
- A3: "Users minimize perceived cost"
- **Redundancy**: A2 + A3 together imply A1
- **Resolution**: Remove A1 (or A2 + A3) — choose minimal set

---

## Common Mistakes

### Mistake 1: Confusing Axioms with Well-Supported Beliefs

**Example**: "Remote work reduces productivity"

- **Why it's not an axiom**: It's an empirical claim, supported by some evidence, contradicted by other evidence. It depends on context (culture, tools, tasks).
- **What to do**: Verify it, then treat it as a contingent belief, not an axiom.

### Mistake 2: Extracting Definitions as Axioms

**Example**: "Product-market fit occurs when demand exceeds supply"

- **Why it's not an axiom**: This is a definition, not a first principle. It's tautological.
- **What to do**: Use it as a definition, then extract the underlying axioms (e.g., "Supply and demand equilibrate in markets").

### Mistake 3: Ignoring Domain Boundaries

**Example**: "Users always prefer simpler products"

- **Why it's not an axiom**: It's not universal. Power users prefer complexity (if it provides value).
- **What to do**: Specify domain: "In consumer markets, users prefer simplicity for initial adoption."

### Mistake 4: Including Contingent Truths

**Example**: "Startups need to pivot"

- **Why it's not an axiom**: It's contingent on uncertainty, market feedback, initial assumptions. Some startups succeed without pivoting.
- **What to do**: Extract the underlying axiom: "Under uncertainty, feedback improves decision quality."

### Mistake 5: Over-Abstracting

**Example**: "Everything is connected"

- **Why it's not an axiom**: It's too vague. It doesn't provide falsifiable content.
- **What to do**: Make it precise: "In complex systems, component interactions produce system-level behavior."

### Mistake 6: Mixing Axioms with Theorems

**Example**: "Profit = Revenue - Cost"

- **Why it's not an axiom**: It's a definition (theorem). The axioms are: "Revenue is value received", "Cost is value expended", "Profit is net value."
- **What to do**: Treat it as a definition derived from axioms.

---

## When to Use This Reference

**Use during Phase 3 (Axiom Extraction)** after verification.

**Apply to**:
- All assumptions that passed verification tests
- Select candidates for axioms
- Test each candidate against the five principles
- Formulate axioms precisely
- Verify the axiom set as a whole

**Extraction Checklist**:
- [ ] Irreducibility tested (cannot decompose further)
- [ ] Universality confirmed (no exceptions in domain)
- [ ] Independence verified (not derivable from others)
- [ ] Verifiability confirmed (falsifiable in principle)
- [ ] Necessity established (logically or physically necessary)
- [ ] Formulated precisely (falsifiable, quantified)
- [ ] Set consistency checked (no contradictions)
- [ ] Set independence verified (minimal set)
- [ ] Set completeness assessed (covers domain)
