# Financial Modeling Methodology

## Discounted Cash Flow (DCF)
- **Projection period**: Typically 5‑10 years depending on business lifecycle.
- **Free Cash Flow (FCF)**: Operating cash flow – capex – changes in working capital.
- **Terminal value**: Perpetuity growth method (`TV = FCF_last * (1+g) / (WACC-g)`) or exit multiple.
- **Discount rate**: Compute WACC = E/V * Re + D/V * Rd * (1‑Tax).

## Sensitivity Analysis
- Vary key inputs (revenue growth, WACC, margin).
- Generate tornado chart to rank drivers.
- Identify break‑even points.

## Monte Carlo Simulation
- Assign probability distributions (normal, log‑normal, uniform) to uncertain inputs.
- Run 1,000‑10,000 iterations.
- Capture distribution of valuation outcomes, confidence intervals.

## Scenario Planning
- Define **Best**, **Base**, **Worst** cases with distinct assumptions.
- Assign probability weights to each scenario.
- Compare expected values and risk‑return profiles.

## Best Practices
- Document all assumptions clearly.
- Cross‑check model balance (assets = liabilities + equity).
- Perform sanity checks on outputs (e.g., compare to market multiples).
- Keep version control of input data and model files.
