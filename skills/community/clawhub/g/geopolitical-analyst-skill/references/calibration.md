# Confidence Tracking & Analytical Learning

## Purpose

Predictions fail. The question is: **by how much, and can we learn from it?**

This module tracks assessments over time:
1. What did we predict?
2. What actually happened?
3. How well did we predict?
4. Why did we miss?
5. What do we do differently next time?

By tracking accuracy systematically, the skill becomes **self-correcting**: it learns which analytical modules are reliable, which regions are harder to predict, which analysts are overconfident.

---

## The Calibration Challenge

**Overconfidence:**
- Analysts say "80% confidence" too often
- Actual 80% confidence predictions should be right 80% of the time
- Most analysts are overconfident: actual accuracy ~60% when they claim 80%

**Underconfidence:**
- Some analysts hide behind "it's complex" and give 50% confidence to everything
- This is useless for decision-making

**Learning:**
- If we said 70% confidence and were actually right 70% of the time = WELL CALIBRATED
- If we said 70% but were only right 50% = OVERCONFIDENT (need to lower claims)
- If we said 70% but were right 90% = UNDERCONFIDENT (can be more confident)

---

## What to Track

### Per-Assessment Record

```json
{
  "assessment_id": "2026-03-20-ukraine-mobilization",
  "date_issued": "2026-03-20",
  "analyst": "[analyst-initials]",
  "region": "Ukraine",
  "topic": "Mobilization patterns",
  "depth_level": "FULL",
  
  "prediction_snapshot": {
    "base_case": "Russian offensive stalls by May; Ukraine begins counter-offensive preparation",
    "base_case_confidence": "MEDIUM (65%)",
    "upside_case": "Negotiation breakthrough in April; ceasefire by May",
    "upside_case_confidence": "LOW (20%)",
    "downside_case": "Russian breakthrough; mass Ukrainian retreat",
    "downside_case_confidence": "LOW (15%)",
    
    "key_assumption": "Russian army remains logistically constrained",
    "sensitivity": "If Russia deploys 100k fresh troops: scenario changes to downside",
    
    "specific_predictions": [
      "Ukrainian artillery output will increase 30-50% by April",
      "Russian mobilization will stall by May (manpower limits)",
      "NATO will increase weapons delivery by March",
      "No major ceasefire movement in next 6 weeks"
    ]
  },
  
  "outcome_tracking": {
    "resolution_date": "2026-06-20",  // 3 months later
    "actual_outcome": "Ukrainian counter-offensive launched May 15; stalled by June. Russian offensive halted March. Base case CORRECT.",
    
    "prediction_accuracy": {
      "base_case": "CORRECT",
      "upside_case": "PARTIALLY (negotiation talks started but no ceasefire)",
      "downside_case": "INCORRECT",
      
      "specific_predictions_accuracy": [
        "Artillery increase: CORRECT (42% increase verified)",
        "Russian mobilization stall: CORRECT (verified by OSINT)",
        "NATO weapons increase: CORRECT (Biden announced delivery acceleration)",
        "No major ceasefire: CORRECT"
      ]
    },
    
    "calibration_check": {
      "confidence_stated": "65% (medium)",
      "accuracy_actual": "CORRECT",
      "calibration": "WELL-CALIBRATED (65% confidence prediction was right)"
    },
    
    "miss_analysis": {
      "what_we_missed": "Ukraine's offensive launch timing (predicted May, actually May 15 — close)",
      "why_we_missed": "Didn't account for political pressure from allies (Warsaw conference effect)",
      "what_we_learn": "NATO political events influence Ukrainian timing more than we modeled"
    }
  }
}
```

---

## Metrics to Calculate

### Individual Assessment Calibration

**Binary Predictions (happened / didn't happen):**
- Predicted 80% confident → Actually happened = CORRECT
- Predicted 80% confident → Didn't happen = OVERCONFIDENT (adjust down)
- Predicted 30% confident → Actually happened = UNDERCONFIDENT (adjust up)

**Multi-Scenario Predictions:**
- Which scenario actually unfolded? (base / upside / downside)
- Did we predict the right one at the highest confidence?
- Did we assign reasonable probabilities?

**Specific Predictions:**
- Artillery output: predicted 30-50% increase, actual 42% = ACCURATE
- Personnel movements: predicted by March, actual March 5 = ACCURATE
- Economic impact: predicted "significant" but no number = VAGUE (downgrade confidence)

### Aggregated Accuracy Metrics

**By Analyst:**
```
Analyst: Sarah Chen
Total predictions: 47
Accuracy when "HIGH" confidence: 82% (27/33 correct)
Accuracy when "MEDIUM" confidence: 61% (8/13 correct)
Accuracy when "LOW" confidence: 50% (0/1 correct) — too few samples

Calibration assessment: GOOD for HIGH, OVERCONFIDENT for MEDIUM
Recommendation: Increase HIGH confidence thresholds, lower MEDIUM claims
```

**By Region:**
```
Region: Eastern Europe
Accuracy: 73% (26/36 correct)

Region: Sub-Saharan Africa
Accuracy: 58% (11/19 correct)

Conclusion: Eastern Europe predictions more reliable than Africa
Reason: More data density, fewer variables, established patterns
```

**By Topic:**
```
Topic: Military operations
Accuracy: 75% — HIGH

Topic: Negotiation outcomes
Accuracy: 52% — LOW

Topic: Economic effects
Accuracy: 68% — MEDIUM

Conclusion: Negotiations are harder to predict; remove overconfidence in negotiation scenarios
```

**By Scenario Type:**
```
Base case accuracy: 71%
Upside case accuracy: 34%
Downside case accuracy: 52%

Conclusion: Base cases are well-calibrated; upside cases are overconfident
Action: When predicting upside, lower confidence by 10-15%
```

---

## Learning from Misses

### Miss Category 1: Black Swan (Unpredictable)
**Definition:** Event had <5% probability assigned; actually occurred

**Example:** Coup in [Country X] when stability assessment was "medium-high"

**Learning:** 
- Identify what was missed (internal factional conflict signal?)
- Check if trend detection would have caught it
- Note: Not all misses are our fault; some events are genuinely low-probability

**Action:** Update elite faction analysis module; improve internal conflict detection

### Miss Category 2: Overconfidence
**Definition:** We said X with HIGH confidence; X didn't happen

**Example:** "Ceasefire will hold by May" — HIGH confidence. Ceasefire collapsed in June.

**Learning:**
- What assumption was wrong? (Outside mediator didn't follow through; domestic politics changed)
- Was confidence justified at the time? (Yes if new info emerged after prediction)
- Does this region/topic pattern show overconfidence? (If repeat, yes)

**Action:** Lower confidence thresholds in similar situations; require additional verification

### Miss Category 3: Information Asymmetry
**Definition:** We predicted correctly given available data; new info proved us wrong

**Example:** Predicted no weapons shipment; secret CIA transfer revealed 6 months later

**Learning:**
- We were right given public info; wrong given secret info
- Not really a calibration problem (we can't predict secret actions)
- But useful to note: if prediction later proved wrong, check for hidden variables

**Action:** Flag assessments where hidden actions could change outcome; plan for re-assessment if new data emerges

---

## Continuous Improvement Loop

### Weekly Calibration Check
- Any predictions reaching resolution? (3-month assessments, 6-month assessments)
- Accuracy check: binary (right/wrong), ordinal (how wrong?), impact (did it matter?)
- Update rolling metrics (current month vs 3-month rolling average)

### Monthly Learning Review
- Aggregate metrics by analyst, region, topic
- Identify patterns (who's overconfident? Which regions are hard?)
- Discussion: Why are negotiations harder to predict? Why is Africa less accurate?

### Quarterly Strategy Adjustment
- Which modules correlate with accuracy? (Use historical patterns well? Less accurate with trend detection?)
- What new signals should we track? (Trend detection identified a gap?)
- How do we improve? (Better data source? Different analytical framework?)

---

## Integration with Skill Workflow

### Step 0: Determine Depth
- **Historical accuracy for this analyst + region + topic?** Use to calibrate confidence claims

### Step 9: Output Generation
- **Confidence assignment:** Don't just guess. Reference analyst's historical calibration
- **Prediction specificity:** More specific predictions = need higher confidence to justify
- **Confidence language:** If analyst historically overconfident: use lower labels

### Post-Assessment (3-6 months later)
- **Resolution tracking:** Log actual outcome vs prediction
- **Calibration check:** Was confidence justified?
- **Learning extraction:** Why did we miss? What do we learn?

---

## Calibration Storage Format

File: `learning/calibration-log.jsonl`

Each line = one completed assessment with resolution data

```json
{"assessment_id":"2026-03-20-xyz","analyst":"SC","region":"Eastern Europe","accuracy":"CORRECT","confidence_stated":"75%","outcome":"Base case occurred","lessons":"NATO signals matter more than we weight"}
{"assessment_id":"2026-03-21-abc","analyst":"JK","region":"Sub-Saharan Africa","accuracy":"OVERCONFIDENT","confidence_stated":"80%","outcome":"Ceasefire collapsed when we predicted hold","lessons":"Negotiation outcomes harder than we think"}
```

---

## Honest Uncertainty

This module is not about becoming perfect. It's about:
1. **Knowing what we know** (and don't know)
2. **Being honest about confidence** (not pretending certainty)
3. **Learning systematically** (not repeating the same mistakes)
4. **Improving over time** (not static)

The best analysts are well-calibrated: when they say 70% confident, they're right ~70% of the time. That's the goal.
