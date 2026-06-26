# Practice Loop

## Table of Contents

1. [Overview](#overview)
2. [Feedback Learning](#feedback-learning)
3. [Failure Mode Analysis](#failure-mode-analysis)
4. [Success Pattern Extraction](#success-pattern-extraction)
5. [Case Management System](#case-management-system)
6. [Performance Metrics](#performance-metrics)

---

## Overview

First-principles reasoning is not just a thinking exercise—it must be validated through action. This document closes the loop between reasoning and results.

**Principle**: The value of first-principles analysis is measured by the quality of decisions and outcomes it produces. Continuous learning from practice refines the framework.

---

## Feedback Learning

### The Learning Cycle

```
Apply First Principles → Take Action → Observe Outcome → Analyze → Update Framework
     ↑                                                                              ↓
     ←←←←←←←←←←←←←←←←←←←← Framework Refinement ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### Outcome Tracking

For each first-principles analysis, track:

```
Case {
  "id": "FP-2024-001",
  "date": "2024-01-15",
  "problem": "Product pricing strategy",
  "axioms_used": [A1, A2, A3],
  "reconstruction": "Value-based pricing",
  "action_taken": "Implemented tiered pricing",
  "outcome": {
    "metric": "Revenue",
    "before": "$1M/month",
    "after": "$1.3M/month",
    "change": "+30%",
    "time_horizon": "6 months"
  },
  "confidence": 0.8,
  "outcome_confidence": 0.9
}
```

### Bayesian Learning

Update axioms based on outcomes:

**If outcome matches prediction**:
```
P(Axiom | Success) ↑ (strengthen confidence)
```

**If outcome contradicts prediction**:
```
P(Axiom | Failure) ↓ (weaken confidence)
```

**Update rule**:
```
P_new(A) = P_old(A) × (1 + α × (outcome - expected) / σ)
```
Where:
- α = learning rate (0 < α ≤ 1)
- outcome = actual result (normalized)
- expected = predicted result (normalized)
- σ = uncertainty

### Learning Rate Adaptation

Adjust learning rate based on outcome certainty:

| Outcome Certainty | Learning Rate |
|-------------------|---------------|
| High (P_outcome > 0.9) | α = 0.8 (learn quickly) |
| Medium (0.5 < P_outcome ≤ 0.9) | α = 0.5 (moderate learning) |
| Low (P_outcome ≤ 0.5) | α = 0.2 (cautious learning) |

---

## Failure Mode Analysis

### Failure Taxonomy

#### 1. Framework Failures

**Type A: Missing Assumptions**
- **Symptom**: Outcome surprises; factors not considered
- **Cause**: Incomplete assumption extraction (missed assumption types)
- **Fix**: Add assumption type to taxonomy; expand extraction process

**Type B: Incorrect Verification**
- **Symptom**: Axiom turns out to be false
- **Cause**: Verification method inadequate (wrong domain test)
- **Fix**: Add new verification test; strengthen verification process

**Type C: Flawed Reconstruction**
- **Symptom**: Solution doesn't work in practice
- **Cause**: Reconstruction method inappropriate; missing constraints
- **Fix**: Try alternative reconstruction method; add real-world constraints

#### 2. Execution Failures

**Type D: Poor Implementation**
- **Symptom**: Good theory, bad execution
- **Cause**: Implementation details, resource constraints, timing
- **Fix**: Improve implementation (not a framework issue)

**Type E: Environmental Shift**
- **Symptom**: Predicted outcome but environment changed
- **Cause**: External factors (market, technology, competition)
- **Fix**: Update assumptions about environment; add scenario analysis

#### 3. Inherent Uncertainty

**Type F: Fundamental Unpredictability**
- **Symptom**: Outcome varies widely despite identical conditions
- **Cause**: Chaotic systems, quantum uncertainty, stochastic processes
- **Fix**: Accept uncertainty; use probabilistic outcomes; ensemble approaches

### Root Cause Analysis

For each failure, perform "Five Whys":

**Example**:
```
Failure: Pricing strategy predicted +30% revenue, actual -5%

Why 1? Customers didn't perceive value as expected
Why 2? Value communication was unclear
Why 3? We assumed customers would read detailed specs
Why 4? We didn't validate customer understanding
Why 5? (Root cause) Missing "communication effectiveness" assumption in axiomatic analysis

Fix: Add "communication effectiveness" as a critical assumption; validate with user testing before implementation
```

### Failure Database

Maintain a structured failure database:

```
{
  "failure_id": "FP-F-023",
  "case_id": "FP-2024-001",
  "type": "A",  // Missing assumptions
  "description": "Customer communication effectiveness not considered",
  "root_cause": "Incomplete assumption taxonomy",
  "impact": "Revenue decreased 5%",
  "fix": "Added communication effectiveness as axiological assumption",
  "date_fixed": "2024-02-01"
}
```

**Use case**: Identify patterns; prevent recurrence.

---

## Success Pattern Extraction

### Success Taxonomy

#### 1. Prediction Success

**Pattern**: Outcome matches prediction within confidence interval

**Metrics**:
- Prediction accuracy: |predicted - actual| / |predicted|
- Confidence calibration: P(outcome in CI) ≈ confidence level

**Example**: Predicted +25% ±10%, actual +28% → Success

#### 2. Decision Quality

**Pattern**: Decision better than alternative (even if prediction imperfect)

**Metrics**:
- Counterfactual: What would have happened with conventional approach?
- Opportunity cost: Did we miss better alternatives?

**Example**: Predicted +25%, actual +10%, but conventional approach would have -5% → Relative success

#### 3. Insight Generation

**Pattern**: Novel insights emerged, even if not directly actionable

**Metrics**:
- Number of non-obvious insights
- Insight applicability to other problems

**Example**: Discovered "value perception lag" effect → Success despite imperfect revenue prediction

### Success Pattern Mining

Use data mining to identify success patterns:

**Features**:
- Problem domain
- Number of assumption types used
- Verification rigor
- Reconstruction method
- Axiom count
- Time invested
- Team expertise level

**Target variable**: Success (binary) or Outcome quality (continuous)

**Models**:
- **Decision tree**: Identify rules (e.g., "If domain = business AND verification = heavy, then success probability = 0.8")
- **Random forest**: More complex pattern recognition
- **Logistic regression**: Identify which features matter most

### Best Practice Extraction

From successful cases, extract best practices:

```
Best Practice 1: For pricing decisions, always test value perception with customers before implementation
Best Practice 2: For technical architecture, use multi-path verification
Best Practice 3: For high-uncertainty environments, develop scenario plans
```

### Success Database

```
{
  "success_id": "FP-S-047",
  "case_id": "FP-2024-005",
  "type": "Prediction Success",
  "pattern": "High verification rigor in technical domain",
  "prediction_accuracy": 0.92,
  "insights": ["value perception lag", "network effects amplify adoption"],
  "best_practices": ["Validate with A/B tests", "Monitor early adoption"],
  "applicability": ["B2C products", "Network-based businesses"]
}
```

---

## Case Management System

### Case Lifecycle

```
New Case → Analysis → Implementation → Outcome → Learning → Archive
```

### Case Attributes

**Mandatory**:
- Problem description
- Domain
- Axioms used
- Reconstruction
- Action taken
- Outcome

**Optional**:
- Team
- Time invested
- Confidence levels
- Failure/success classification
- Lessons learned

### Case Search

Enable search and retrieval:

```
Search queries:
- "Find all cases with axiological assumptions"
- "Find failures in business domain"
- "Find successful pricing analyses"
- "Find cases with high uncertainty"
```

### Case Comparison

Compare cases to identify patterns:

```
Case A: Pricing strategy, 5 axioms, success +30%
Case B: Pricing strategy, 3 axioms, failure -10%
Comparison: Case A included communication effectiveness axiom, Case B did not
```

### Case Reuse

Reuse successful analysis frameworks:

```
Template {
  "name": "SaaS Pricing Analysis",
  "domain": "Business",
  "assumption_types": ["axiological", "causal", "temporal"],
  "verification_methods": ["epistemic", "systemic"],
  "reconstruction_method": "reverse_engineering",
  "axioms": [A1, A2, A3, A4],
  "success_rate": 0.85,
  "cases": ["FP-2024-005", "FP-2024-012", "FP-2024-018"]
}
```

---

## Performance Metrics

### Framework-Level Metrics

#### 1. Predictive Accuracy

```
Accuracy = 1 - |predicted - actual| / |predicted|
```

Track over time to detect drift.

#### 2. Confidence Calibration

```
Calibration = |P(outcome in CI) - confidence_level|
```

Perfect calibration: 0.

#### 3. Decision Improvement

```
Improvement = (outcome - baseline) / |baseline|
```
Where baseline is conventional approach or status quo.

#### 4. Efficiency

```
Efficiency = outcome / time_invested
```

Optimal: High outcome with low time investment.

### Axiom-Level Metrics

#### 1. Axiom Validity Rate

```
Validity = number_times_axiom_held / number_times_axiom_tested
```

Low validity → reconsider or discard axiom.

#### 2. Axiom Usage Frequency

```
Frequency = number_cases_using_axiom / total_cases
```

High frequency, high validity → robust axiom.

#### 3. Axiom Discriminatory Power

```
Discrimination = |P(success | axiom) - P(success | no_axiom)|
```

High discrimination → axiom is valuable for success prediction.

### Learning Metrics

#### 1. Learning Curve

```
Improvement over time: Success_rate(t) vs. Success_rate(t-1)
```

Should increase (learning) or stabilize (maturity).

#### 2. Failure Reduction

```
Reduction = Failure_rate(t-1) - Failure_rate(t)
```

Target: Decreasing failure rate.

#### 3. Knowledge Transfer

```
Transfer = Number_of_reused_templates / Total_cases
```

Higher transfer = more efficient learning.

### Metric Dashboard

```
+------------------+----------+----------+----------+
| Metric           | Month 1  | Month 2  | Month 3  |
+------------------+----------+----------+----------+
| Predictive Acc.  | 0.72     | 0.78     | 0.82     |
| Calibration      | 0.15     | 0.12     | 0.09     |
| Decision Imp.    | 0.25     | 0.32     | 0.38     |
| Efficiency       | 0.05     | 0.07     | 0.08     |
| Failure Rate     | 0.30     | 0.25     | 0.20     |
+------------------+----------+----------+----------+
```

---

## When to Use This Reference

**Use after applying first-principles analysis and taking action.**

**Apply to**:
- Tracking outcomes of decisions
- Learning from successes and failures
- Building a case database
- Measuring framework performance
- Extracting best practices

**Practice Loop Checklist**:
- [ ] Case documented with all attributes
- [ ] Outcome measured and recorded
- [ ] Bayesian learning applied (update axiom confidences)
- [ ] Failure/success classified
- [ ] Root cause analysis performed (for failures)
- [ ] Best practices extracted (for successes)
- [ ] Case added to database
- [ ] Performance metrics updated
- [ ] Patterns identified and templates created
