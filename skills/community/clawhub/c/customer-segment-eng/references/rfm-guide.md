# RFM Model Reference

RFM (Recency, Frequency, Monetary) is the most classic methodology for customer value analysis.

## Three Dimensions

| Dimension | Meaning | Calculation Method | Direction |
|-----------|---------|-------------------|-----------|
| Recency (R) | Days since last transaction | (Analysis date - Last transaction date).days | Smaller is better |
| Frequency (F) | Transaction frequency | Sum of transactions in the period | Larger is better |
| Monetary (M) | Transaction amount | Sum of transaction amounts in the period | Larger is better |

## Score Calculation (5-point scale)

Divide each dimension into 5 tiers by quantiles:
- R: Most recent 20% of days → 5 points, furthest 20% → 1 point
- F: Highest 20% frequency → 5 points, lowest 20% → 1 point
- M: Highest 20% amount → 5 points, lowest 20% → 1 point

## Composite Score

```
RFM_Score = R × 100 + F × 10 + M
```

| Composite Score | Customer Type | Recommended Strategy |
|-----------------|---------------|----------------------|
| 555 | Key Retention | VIP one-on-one maintenance |
| 554-545 | High-Value Customers | Value-added services |
| 535-425 | Potential Customers | Targeted marketing |
| 414-324 | Churn Risk | Retention activities |
| <224 | Low-Value Customers | Cost reduction |

## Extended Dimensions (Banking Scenario)

For banking scenarios, the following dimensions can be added to RFM:

| Extended Dimension | Field | Description |
|--------------------|--------|-------------|
| Tenure (T) | account_open_date | Customer duration |
| Product Depth (P) | product_count | Number of products held |
| Channel (C) | channel_touch | Channel touchpoints |
| Risk (R2) | risk_score | Risk rating |

## Banking Data Considerations

1. **Asset balance** (balance) is more stable than Monetary: Prefer balance instead of M
2. **Customer segmentation should be hierarchical**: First stratify by assets, then refine by behavior
3. **Cross-selling opportunities**: Analyze product ownership rates by segment to identify cross-selling targets
4. **Compliance requirements**: Segmentation results cannot be used for discriminatory pricing and require desensitization