# Data-Aware Routing Rules

Method selection is based on comprehensive judgment across three dimensions, prioritized as follows:

## Dimension 1: Topic Semantics

Semantic tags extracted from business problems determine the analysis direction:

| Semantic Tag | Keywords | Primary Method | Alternative Method |
|--------------|----------|----------------|---------------------|
| Growth Analysis | growth, increase, rise, acceleration | Decomposition + Regression | Forecasting, Cohort |
| Churn Analysis | churn, decline, decrease, reduction | Funnel + Cohort | Attribution, Causal |
| Attribution Inquiry | why, reason, factor, contribution | Attribution Analysis | Regression, Causal Inference |
| Comparative Analysis | compare, difference, A/B, change | Hypothesis Testing | Causal Inference |
| Forecasting/Planning | forecast, predict, trend, next year | Forecasting Modeling | Time Series Analysis |
| User Segmentation | segment, classify, profile, tier | Clustering + RFM | Factor Analysis |
| Conversion Optimization | conversion, funnel, flow, path | Funnel Analysis | Cohort |
| Anomaly Investigation | anomaly,突变, drop, spike | Anomaly Detection | Descriptive Statistics |
| Effect Evaluation | evaluate, ROI, effect, impact | Causal Inference | Attribution Analysis |
| Metric Relationships | relationship, association, influence, factor | Regression + Correlation | Factor Analysis |
| Text Insights | feedback, review, comment, word cloud | Text Analysis | — |
| Comprehensive Overview | overview, summary, recap, report | Descriptive Statistics | Combine as needed |

## Dimension 2: Data Structure

The natural form of the data limits available methods:

| Data Structure | Characteristics | Applicable Methods | Inapplicable Methods |
|----------------|-----------------|---------------------|----------------------|
| Single table, no time | Pure cross-sectional data | Descriptive Stats, Correlation, Regression, Clustering, Factor | Time Series, Forecasting, Funnel, Cohort |
| Single table, has time | Contains date/time column | All applicable | — |
| Multiple tables, joined | Multiple joinable tables | All applicable (requires joining first) | — |
| Hierarchical data | Nested structure (user→order→item) | Descriptive Stats (stratified), Funnel (stepwise) | Clustering (requires aggregation first) |
| Panel data | id+time dual index | Causal Inference (DID), Panel Regression | Simple Time Series |
| Text data | Unstructured | Text Analysis | Numerical methods |
| Small sample (<100) | Insufficient data volume | Descriptive Stats, Hypothesis Testing (non-parametric) | Clustering, Forecasting, Factor Analysis |
| Severe missing (>30%) | Many null values | Descriptive Stats (include missing analysis) | Clean first before complex analysis |

## Dimension 3: Problem Type

The analysis objective determines the method:

| Problem Type | Definition | Core Methods | Typical Questions |
|--------------|------------|---------------|--------------------|
| Descriptive | What happened | Descriptive Stats, Funnel, Cohort | "What does the data look like", "What is the conversion rate" |
| Diagnostic | Why it happened | Attribution, Causal Inference, Anomaly Detection | "Why the decline", "What is the cause" |
| Predictive | What will happen | Forecasting Modeling, Time Series Analysis | "What will next quarter be like", "What is the trend" |
| Prescriptive | What should be done | All + Business Recommendations | "How to optimize", "What to do better" |

## Routing Decision Process

```
Input: Topic + Data Structure + Problem Type
  ↓
1. Lock candidate methods from Topic Semantics (2-3)
  ↓
2. Filter by Data Structure: exclude inapplicable ones
  ↓
3. Determine priority by Problem Type: Descriptive → Diagnostic → Predictive → Prescriptive (increasing depth)
  ↓
4. Output: Primary Method | Alternative Method | Exclusion Reasons
```

## Validation Rules

- Primary and alternative methods must not belong to the same family (to avoid systematic bias)
- If data structure is "Small Sample", automatically annotate as "Low confidence preset"
- If topic contains multiple semantic tags, method selection prioritizes the highest priority tag