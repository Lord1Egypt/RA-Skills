# Post-Match Review & Learning Framework

## Table of Contents
1. [Input Format](#input-format)
2. [Review Procedure](#review-procedure)
3. [Framework Storage](#framework-storage)
4. [Accuracy Tracking](#accuracy-tracking)

---

## Input Format

Accept match result in either way:
- **User provides result**: "本場比賽最終比分X比X"
- **Auto-fetch**: Read result from m.nowscore.com match page after match ends

---

## Review Procedure

### 1. Full Data Recall
- Recall ALL pre-match data and information provided for this match
- Recall the complete analysis framework used for prediction

### 2. Deviation Analysis (偏差分析)
Use deviation analysis method to review:

**Compare predicted vs actual for each component:**

| Component | Predicted | Actual | Deviation |
|-----------|-----------|--------|-----------|
| Final score | X-X | X-X | +/- |
| Asian handicap result | Win/Lose | Win/Lose | Correct/Wrong |
| Over/under result | Over/Under | Over/Under | Correct/Wrong |
| Key factor accuracy | - | - | Analysis |

**Analyze root causes of deviations:**
- Was the odds analysis correct but fundamentals misjudged?
- Were lineup impacts over/underestimated?
- Were there unforeseeable events (red cards, penalties, injuries)?
- Was the bookmaker's intent correctly identified?

### 3. Framework Optimization
Based on deviation analysis:

**Parameter adjustments:**
- Adjust feature weights in logistic regression model
- Update league-specific factors and coefficients
- Calibrate motivation and environment factor scaling
- Refine squad power decay calculations

**Pattern recognition:**
- Remember pre-match data features of this match
- Remember league-specific odds patterns (盤路數據特徵)
- Build league-specific calculation frameworks and analysis logic

**Goal**: Achieve 70%+ accuracy for both Asian handicap and over/under predictions.

---

## Framework Storage

Save the optimized analysis framework including:

1. **Data reading & statistics** - What data points proved most predictive
2. **Fundamental analysis logic** - Refined analysis methodology
3. **Analysis methods** - Updated model parameters and weights
4. **Win probability calculation** - Calibrated probability formulas
5. **Prediction model** - Updated logistic regression parameters

### Storage Location
Save framework updates to memory files for persistence across sessions:
- `~/.claude/projects/*/memory/football-prediction-framework.md` - Core framework parameters
- `~/.claude/projects/*/memory/football-league-profiles.md` - League-specific profiles
- `~/.claude/projects/*/memory/football-match-history.md` - Historical match records and accuracy

---

## Accuracy Tracking

### Per-Match Tracking
After each review, record:
```
Match: [Teams] | Date: [Date] | League: [League]
Handicap: [Predicted] vs [Actual] -> [Correct/Wrong]
Over/Under: [Predicted] vs [Actual] -> [Correct/Wrong]
Score: [Predicted] vs [Actual]
Key Learning: [Brief note]
```

### Cumulative Statistics
Maintain running totals across ALL analyzed matches (including migrated history):

```
Total matches analyzed: N
Asian Handicap accuracy: X/N (XX%)
Over/Under accuracy: X/N (XX%)
By league breakdown:
  - [League 1]: Handicap XX%, O/U XX% (N matches)
  - [League 2]: Handicap XX%, O/U XX% (N matches)
```

Output cumulative statistics at the end of every review session.
