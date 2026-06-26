# Analogy Patterns by Concept Type

A library of reusable analogy structures. When teaching a new concept, find the
closest pattern here and adapt it to the subject matter.

---

## Pattern 1: The Scoring System
**Use for**: Indices, metrics, composite scores, rankings, standardization

> "Think of it like a college application score. GPA, test scores, and extracurriculars
> are all measured on different scales. To combine them fairly, you have to convert
> them all to a common scale — like percentile rank — before adding them up.
> Otherwise GPA (out of 4.0) would be drowned out by test scores (out of 1600)."

**Applies to**: Factor standardization, composite indices, weighted scoring models,
multi-metric evaluation, normalization in ML.

---

## Pattern 2: The Sensor Fusion
**Use for**: Combining multiple signals, ensemble methods, multi-factor models

> "A self-driving car doesn't rely on just one sensor. It uses cameras, LIDAR, radar,
> and GPS together. Each sensor has blind spots. Combined, they cover each other's
> weaknesses. The car is more reliable than any single sensor alone."

**Applies to**: Multi-factor models, ensemble ML, triangulation in research,
cross-referencing sources, diversification.

---

## Pattern 3: The Two Views of a Spreadsheet
**Use for**: Time series vs. cross-section, row vs. column operations, longitudinal vs. lateral

> "Imagine a spreadsheet where rows are dates and columns are items (stocks, people,
> products). Reading down one column = time series (one item over time).
> Reading across one row = cross-section (all items at one moment)."

**Applies to**: Any domain with panel data, before/after comparisons, cohort analysis,
longitudinal studies.

---

## Pattern 4: The Recipe Adjustment
**Use for**: Normalization, scaling, adjusting for confounds, removing baseline effects

> "A recipe says 'add 2 cups of flour' — but that's for 4 servings.
> If you're making 12 servings, you scale everything up proportionally.
> Normalization is the same: adjusting a value so it's comparable regardless of
> the 'serving size' (time period, market conditions, population size)."

**Applies to**: Per-capita adjustments, seasonal adjustment, inflation adjustment,
log transformation, adjusted prices.

---

## Pattern 5: The Track Record
**Use for**: Backtesting, historical validation, using past performance to estimate future

> "Before hiring a contractor, you check their past projects. You're not guaranteed
> the future will match the past — but it's the best evidence you have.
> Backtesting is the same: checking how a strategy would have performed historically
> to estimate whether it's likely to work going forward."

**Applies to**: Backtesting, A/B test history, model validation, evidence-based
decision making, clinical trial history.

---

## Pattern 6: The Exam Grader
**Use for**: Prediction accuracy, correlation, IC value, model evaluation

> "Imagine a student who always predicts 'sunny' for tomorrow's weather.
> Sometimes they're right. But a good forecaster should be right *systematically*,
> not just occasionally. The IC (or correlation) measures whether high predictions
> consistently match high outcomes — not just whether any single prediction was right."

**Applies to**: Correlation, prediction accuracy, precision/recall, IC in finance,
any metric measuring systematic predictive power.

---

## Pattern 7: The Contaminated Evidence
**Use for**: Look-ahead bias, data leakage, confounded experiments

> "Imagine a detective who 'solves' cases by reading tomorrow's newspaper.
> They're always right — but completely useless in real life.
> Look-ahead bias in data analysis is the same: accidentally using information
> that wouldn't have been available at decision time makes results look great
> but impossible to replicate."

**Applies to**: Data leakage in ML, look-ahead bias in backtesting, hindsight bias
in case studies, survivorship bias, contaminated control groups.

---

## Pattern 8: The Class Average Problem
**Use for**: Survivorship bias, selection bias, incomplete populations

> "You survey 'successful entrepreneurs' about what made them successful.
> But you only interviewed people who succeeded — you can't interview the
> thousands who tried the same things and failed. Your conclusions are biased
> toward success stories."

**Applies to**: Survivorship bias, selection bias, publication bias, sampling bias,
analyzing only existing customers (ignoring churned ones).

---

## Pattern 9: The Tuning Dial
**Use for**: Parameters, hyperparameters, optimization, overfitting

> "Think of it like tuning a radio. Turn too little and you get static (underfitting).
> Turn exactly right and you get a clear signal. Turn too much and you get a different
> station (overfitting — you've tuned so precisely to one frequency that you lose
> generalizability)."

**Applies to**: Hyperparameter tuning, overfitting/underfitting, regularization,
calibration, any adjustable parameter with a sweet spot.

---

## Pattern 10: The Job Interview Panel
**Use for**: Weighted voting, committee decisions, multi-rater evaluation, IC weighting

> "A hiring committee has 5 interviewers. Some have better judgment than others —
> they've historically made better hiring decisions. A smart process gives more
> weight to their opinions. IC weighting is the same: give more influence to the
> signals that have historically been most accurate."

**Applies to**: IC weighting, ensemble weighting, expert aggregation, Bayesian
updating, peer review weighting.

---

## How to Use This Library

1. Identify the **type** of concept you're explaining (scoring, combining signals,
   two views, adjustment, validation, accuracy, bias, overfitting, weighting)
2. Find the matching pattern above
3. Adapt the specific domain details to your subject
4. Test whether it lands — if not, try a different pattern

When adapting, keep the *structure* of the analogy intact but swap the surface domain.
The structure is what makes the analogy work.
