# Quality Control Tools Reference

## SPC (Statistical Process Control)

### Control Chart Interpretation

| Pattern | Meaning | Action |
|---------|---------|--------|
| 7 points one side of center | Process shift | Investigate cause |
| 6 points steadily increasing | Trend | Check for wear |
| 14 points alternating up/down | Over-control | Reduce adjustment |
| 2 of 3 points beyond 2σ | Warning | Monitor closely |
| Any point beyond 3σ | Out of control | Immediate investigation |

### Cpk Assessment Criteria

| Cpk Value | Process Capability | Action |
|-----------|-------------------|--------|
| Cpk ≥ 2.0 | Excellent | Maintain |
| 1.67 ≤ Cpk < 2.0 | Good | Minor improvement |
| 1.33 ≤ Cpk < 1.67 | Acceptable | Monitor |
| 1.0 ≤ Cpk < 1.33 | Barely capable | Improve required |
| Cpk < 1.0 | Not capable | Significant improvement |

---

## MSA (Measurement System Analysis)

### Gauge R&R Acceptance Criteria

| %GRR | Assessment | Action |
|------|------------|--------|
| < 10% | Acceptable | Use measurement system |
| 10-30% | Marginal | Review if acceptable for application |
| > 30% | Unacceptable | Improve measurement system |

### Measurement Linearity

- Compare measurements across expected operating range
- Reference standard vs bias should be consistent
- Bias should be < 10% of tolerance

---

## FMEA (Failure Mode and Effects Analysis)

### RPN Calculation

```
RPN = Severity × Occurrence × Detection
```

### Severity Rating (1-10)

| Rating | Effect | Example |
|--------|--------|---------|
| 10 | Safety/regulatory without warning | Seizure causing stall |
| 9 | Safety/regulatory with warning | Engine warning light |
| 8 | Very high | Vehicle inoperable |
| 7 | High | Performance severely affected |
| 6 | Moderate | Vehicle operable but comfort affected |
| 5 | Low | Minor inconvenience |
| 4 | Very low | Minor fit/finish issue |
| 3 | Minor | Fit/finish noticed by most customers |
| 2 | Very minor | Fit/finish noticed by discriminating customers |
| 1 | None | No discernible effect |

### Occurrence Rating (1-10)

| Rating | Likelihood | Approximate Failure Rate |
|--------|-------------|-------------------------|
| 10 | Very high | ≥ 100 per thousand |
| 9 | High | 50 per thousand |
| 8 | Moderately high | 20 per thousand |
| 7 | Moderate | 10 per thousand |
| 6 | Low | 2 per thousand |
| 5 | Very low | 0.1 per thousand |
| 4 | Remote | 0.01 per thousand |
| 3 | Very remote | ≤ 0.001 per thousand |
| 2 | Nearly impossible | 0.0001 per thousand |
| 1 | Impossible | Failure eliminated |

### Detection Rating (1-10)

| Rating | Detection | Likelihood of Detection |
|--------|-----------|-------------------------|
| 10 | Absolute uncertainty | Cannot detect |
| 9 | Very remote | Very slight chance of detection |
| 8 | Remote | Slight chance |
| 7 | Very low | Low chance |
| 6 | Low | Moderately low chance |
| 5 | Moderate | Moderate chance |
| 4 | Moderately high | Moderately high chance |
| 3 | High | High chance |
| 2 | Very high | Very high chance |
| 1 | Almost certain | Almost certain to detect |

### Action Priority

| Priority | RPN Range | Action |
|----------|-----------|--------|
| Critical | RPN ≥ 100 | Immediate action required |
| High | 50 ≤ RPN < 100 | Action in current cycle |
| Medium | 20 ≤ RPN < 50 | Monitor and improve |
| Low | RPN < 20 | Document and monitor |

---

## 5-Why Analysis Template

```
Problem Statement: [Describe the problem clearly]

Why 1: [First level cause]
  ↓ Why?
Why 2: [Second level cause]
  ↓ Why?
Why 3: [Third level cause]
  ↓ Why?
Why 4: [Fourth level cause]
  ↓ Why?
Why 5: [Root cause - should be controllable]

Verification: [How to confirm root cause]
Countermeasure: [What will fix the root cause]
```

---

## 8D Problem Solving

### D1: Establish Team
- Team leader appointed
- Team members with relevant expertise
- Customer involvement if required

### D2: Problem Description
- What is the problem?
- How many affected?
- What are the symptoms?
- What is the severity?

### D3: Interim Containment Actions
- Sort good/bad parts
- 100% inspection of suspect lots
- Customer notification if required
- Time-bound actions

### D4: Root Cause Identification
- Use 5-Why or Fishbone
- Verify with data
- Test potential causes
- Confirm with experiments

### D5: Permanent Corrective Actions
- Select based on root cause
- Consider cost/benefit
- Verify with small batch
- Validate against similar processes

### D6: Implementation
- Implement on production parts
- Train operators
- Update documentation
- Set up monitoring

### D7: Prevent Recurrence
- Update FMEA
- Update Control Plan
- Update PFMEA if needed
- Set up long-term monitoring

### D8: Team Recognition
- Document lessons learned
- Recognize team contributions
- Share knowledge
