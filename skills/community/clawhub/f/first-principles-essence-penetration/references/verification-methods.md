# Verification Methods

## Table of Contents

1. [Overview](#overview)
2. [Logical Verification](#logical-verification)
3. [Physical Verification](#physical-verification)
4. [Epistemic Verification](#epistemic-verification)
5. [Systemic Verification](#systemic-verification)
6. [Causal Verification](#causal-verification)
7. [Handling Verification Conflicts](#handling-verification-conflicts)

---

## Overview

After identifying assumptions, verify them through multiple lenses. No single verification method is sufficient; triangulation across methods increases confidence.

**Principle**: Every assumption must pass at least one verification test to be considered potentially true. Passing multiple tests increases confidence. Failing any test classifies the assumption as false or conditional.

---

## Logical Verification

### The Three Laws of Logic

#### 1. Law of Non-Contradiction
**Test**: Does the assumption contradict itself or other verified assumptions?

**Procedure**:
1. Formalize the assumption as a proposition P
2. Identify related propositions (Q, R, S...)
3. Check if P and ¬P are both asserted (direct contradiction)
4. Check if P and Q together imply ¬P (indirect contradiction)

**Example**:
- **Assumption**: "Our pricing strategy maximizes revenue"
- **Contradiction check**: "Lower prices increase volume" AND "Volume increase reduces per-unit margin" → if margin reduction > volume gain, revenue decreases. Contradiction with "maximizes revenue."

#### 2. Law of Excluded Middle
**Test**: Is the assumption falsifiable? Can we conceive of its negation?

**Procedure**:
1. Ask: "What would it mean for this to be false?"
2. If no coherent negation exists, the assumption is tautological or meaningless
3. If the negation is meaningful, design a test to distinguish between P and ¬P

**Example**:
- **Assumption**: "Our users love the product"
- **Negation**: "Our users do not love the product" (meaningful)
- **Test**: Measure NPS, churn, satisfaction → falsifiable
- **Tautology**: "What is, is" (no meaningful negation, not an assumption)

#### 3. Law of Sufficient Reason
**Test**: Does the assumption have a sufficient reason (cause, justification, basis)?

**Procedure**:
1. Ask: "Why should this be true?"
2. Trace to its basis: empirical evidence, logical deduction, or necessity
3. If no basis can be identified, the assumption is groundless

**Example**:
- **Assumption**: "Remote work reduces productivity"
- **Sufficient reason?**: "Distractions at home" OR "Lack of supervision" OR "Communication delays"
- **Evidence?**: Productivity data comparing remote vs. in-office
- **Without evidence**: Assumption fails sufficiency test

### Logical Consistency Check

**Procedure**:
1. List all assumptions and derived propositions
2. Create a consistency matrix: check each pair for contradiction
3. Resolve contradictions by rejecting one or both propositions

**Output**: A logically consistent set of propositions.

---

## Physical Verification

### Conservation Laws

**Test**: Does the assumption violate any conservation law?

**Procedure**:
1. Identify quantities in the assumption: energy, mass, momentum, charge, money, time
2. Check if these quantities are created or destroyed without transformation
3. Verify conservation in the proposed system

**Example**:
- **Assumption**: "Our business model generates money from nothing"
- **Conservation check**: Money is not conserved in economics, but value must be exchanged. If no value is provided, money cannot be sustainably generated. Assumption fails unless value exchange is demonstrated.

### Thermodynamic Constraints

**Test**: Does the assumption violate the laws of thermodynamics?

**Procedure**:
1. Check for perpetual motion or free energy claims
2. Verify entropy considerations: disorder tends to increase
3. Assess efficiency limits: no process is 100% efficient

**Example**:
- **Assumption**: "This AI system will be 100% accurate"
- **Thermodynamic check**: Complete accuracy requires infinite information (zero entropy). In practice, noise and uncertainty exist. 100% accuracy is thermodynamically implausible.

### Causality and Speed Limits

**Test**: Does the assumption respect causality and speed limits?

**Procedure**:
1. Verify temporal order: cause precedes effect
2. Check for action-at-a-distance without mediation
3. Assess if the proposed mechanism respects physical speed limits

**Example**:
- **Assumption**: "This strategy will show results instantly"
- **Causality check**: Effects require mechanisms (feedback loops, market adoption, learning). Instant results without mechanism violates causality.

### Scalability Laws

**Test**: Does the assumption respect scaling constraints?

**Procedure**:
1. Identify the scaling regime (linear, superlinear, sublinear)
2. Check for square-cube law, metabolic scaling, or other scaling constraints
3. Assess if the claimed scaling is physically plausible

**Example**:
- **Assumption**: "We can scale operations linearly with team size"
- **Scaling check**: Communication overhead grows quadratically (O(n²)) with team size. Linear scaling violates this constraint. Real scaling is sublinear or logarithmic.

---

## Epistemic Verification

### Falsifiability Test

**Test**: Can the assumption be proven false?

**Procedure**:
1. Ask: "What evidence would prove this assumption false?"
2. If no evidence could falsify it, it is not a scientific claim
3. If falsifiable, design the falsification experiment

**Example**:
- **Assumption**: "Our users are satisfied"
- **Falsification**: NPS < 4 OR churn rate > 5% OR satisfaction survey < 70%
- **Unfalsifiable**: "Users will be satisfied eventually" (no time bound, always deferrable)

### Repeatability Test

**Test**: Can the assumption be verified by independent observers?

**Procedure**:
1. Identify the evidence supporting the assumption
2. Check if the evidence is accessible to others
3. Verify if independent replication is possible

**Example**:
- **Assumption**: "Our methodology consistently produces results"
- **Repeatability**: Document the methodology, have independent teams apply it, compare results
- **Unrepeatable**: "Our CEO has a special ability" (inaccessible, unverifiable)

### Occam's Razor Test

**Test**: Is this the simplest explanation?

**Procedure**:
1. List alternative explanations for the same phenomenon
2. Count the entities and assumptions in each explanation
3. Prefer the explanation with fewer assumptions (higher parsimony)

**Example**:
- **Phenomenon**: Sales increased after marketing campaign
- **Explanation A**: Campaign caused sales increase (1 assumption)
- **Explanation B**: Campaign + favorable market conditions + competitor errors + seasonality caused increase (4 assumptions)
- **Occam's razor**: Prefer A unless evidence supports B

### Bayesian Updating

**Test**: Does the assumption properly incorporate new evidence?

**Procedure**:
1. State prior probability (initial belief strength)
2. Identify new evidence
3. Apply Bayes' theorem: P(assumption|evidence) = P(evidence|assumption) × P(assumption) / P(evidence)
4. Update belief based on likelihood of evidence

**Example**:
- **Assumption**: "This feature will drive adoption" (prior: 50% confidence)
- **Evidence**: Beta test shows 10% adoption (expected if true: 40%, if false: 5%)
- **Bayesian update**: P(true|evidence) = (0.4 × 0.5) / (0.4×0.5 + 0.05×0.5) = 0.2 / 0.225 = 89%
- **Result**: Update confidence from 50% to 89%

---

## Systemic Verification

### Emergence Test

**Test**: Does the assumption account for emergent properties?

**Procedure**:
1. Identify the system components and their interactions
2. Check if the whole equals the sum of parts
3. Look for unexpected properties arising from interactions

**Example**:
- **Assumption**: "Adding more engineers will linearly increase output"
- **Emergence check**: Coordination overhead, communication complexity, team dynamics → non-linear scaling. Emergent property: diminishing returns.

### Feedback Loop Test

**Test**: Does the assumption account for feedback loops?

**Procedure**:
1. Identify causal chains in the system
2. Check for loops: does output affect input?
3. Classify loops: positive (amplifying) or negative (stabilizing)
4. Assess loop strength and delay

**Example**:
- **Assumption**: "Lower prices will increase revenue"
- **Feedback check**: Lower prices → more customers → economies of scale → lower costs → can sustain lower prices (positive loop). BUT: Lower prices → perceived quality decline → fewer customers (negative loop). Net effect depends on loop strengths.

### Nonlinearity Test

**Test**: Does the assumption assume linear relationships?

**Procedure**:
1. Identify the variables in the assumption
2. Check if the relationship is assumed to be linear (proportional)
3. Test for thresholds, tipping points, saturation effects

**Example**:
- **Assumption**: "Doubling spend will double results"
- **Nonlinearity check**: Diminishing returns (market saturation), thresholds (minimum spend to be effective), saturation (full market penetration). Relationship is likely S-shaped, not linear.

### Dependency Test

**Test**: Does the assumption account for dependencies?

**Procedure**:
1. Identify variables in the assumption
2. Check for coupling: does one variable depend on another?
3. Assess independence: can variables vary independently?

**Example**:
- **Assumption**: "We can independently optimize each component"
- **Dependency check**: Components may share resources, have interfaces, affect each other. Optimizing one may degrade another. Assumption fails if dependencies exist.

---

## Causal Verification

### Counterfactual Test

**Test**: Would the effect have occurred without the cause?

**Procedure**:
1. Identify the claimed cause (C) and effect (E)
2. Ask: "If C had not happened, would E still have happened?"
3. If yes, C is not the cause (or not the sole cause)

**Example**:
- **Claim**: "The marketing campaign caused the sales increase"
- **Counterfactual**: If the campaign had not run, would sales still have increased? (check seasonality, market trends, competitor actions)
- **If yes**: Campaign is not the cause (or not the sole cause)

### Mechanism Test

**Test**: Is there a plausible mechanism connecting cause and effect?

**Procedure**:
1. Identify the proposed cause (C) and effect (E)
2. Describe the mechanism: how does C produce E?
3. Verify each step in the mechanism is plausible

**Example**:
- **Claim**: "Remote work causes productivity loss"
- **Mechanism**: Remote → less supervision → less motivation → less work → lower productivity
- **Verification**: Are there alternative mechanisms? (Remote → fewer interruptions → more focus → higher productivity). Which mechanism dominates?

### Temporal Precedence Test

**Test**: Does the cause precede the effect?

**Procedure**:
1. Identify the timeline of cause (C) and effect (E)
2. Verify that C occurs before E
3. Check for reverse causality: could E cause C?

**Example**:
- **Claim**: "Product features cause user satisfaction"
- **Temporal check**: Do features exist before satisfaction is measured? (yes). Could satisfied users request features? (reverse causality possible).

### Confounder Test

**Test**: Is there a third variable causing both cause and effect?

**Procedure**:
1. Identify the claimed cause (C) and effect (E)
2. Brainstorm potential confounders (Z) that affect both C and E
3. Test if C and E are correlated when Z is controlled for

**Example**:
- **Claim**: "Coffee consumption causes longevity"
- **Confounders**: Wealth (wealthy people drink more coffee and have better healthcare), lifestyle (coffee drinkers may exercise more), genetics.
- **Control**: Compare coffee drinkers vs. non-drinkers within same socioeconomic class.

---

## Handling Verification Conflicts

When different verification methods give conflicting results, use this framework:

### Step 1: Identify the Conflict
- Which methods support the assumption?
- Which methods contradict it?
- What is the strength of evidence for each?

### Step 2: Assess Method Reliability
- Logical verification is most reliable (cannot be false if sound)
- Physical verification is highly reliable (laws of nature)
- Epistemic verification is context-dependent (evidence quality matters)
- Systemic verification is often overlooked but critical for complex systems
- Causal verification is the hardest but most important for decision-making

### Step 3: Seek Resolution
1. **Check for errors**: Did we apply the test correctly?
2. **Refine the assumption**: Is it too broad or too narrow?
3. **Find boundary conditions**: When does the assumption hold? When does it fail?
4. **Collect more evidence**: Which method has the weakest evidence?

### Step 4: Classify the Assumption
- **Axiom** ✓: Passes all relevant verification tests
- **Conditional** ⚠: Passes some tests, fails others under specific conditions
- **False** ✗: Fails critical verification tests

### Conflict Resolution Example

**Assumption**: "Remote work reduces productivity"

- **Logical**: No contradiction ✓
- **Physical**: No violation ✓
- **Epistemic**: Mixed evidence (some studies show increase, some decrease) ⚠
- **Systemic**: Depends on communication, culture, tools ⚠
- **Causal**: Mechanism plausible but not unique ⚠

**Resolution**: The assumption is **conditional**. It holds when:
- Communication is inadequate
- Tools are insufficient
- Culture doesn't support autonomy
- Tasks require tight coordination

It fails when:
- Communication is effective
- Tools are adequate
- Culture supports autonomy
- Tasks can be done independently

---

## When to Use This Reference

**Use during Phase 3 (Verification)** to test each identified assumption.

**Apply to**:
- All assumptions from the taxonomy
- Each assumption should be tested by at least one method
- Critical assumptions should be tested by multiple methods

**Verification Checklist**:
- [ ] Logical consistency checked
- [ ] Physical laws respected
- [ ] Falsifiability confirmed
- [ ] Evidence evaluated
- [ ] Systemic effects considered
- [ ] Causal mechanism verified
- [ ] Conflicts resolved
- [ ] Assumption classified (Axiom / Conditional / False)
