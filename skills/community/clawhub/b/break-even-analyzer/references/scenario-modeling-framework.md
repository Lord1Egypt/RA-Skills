# Scenario Modeling Framework for Break-Even Analysis

## Why Scenario Modeling Matters

A single break-even number creates false precision. Real-world outcomes depend on multiple variables that can shift simultaneously. Scenario modeling captures this uncertainty and helps decision-makers understand the range of possible outcomes.

## The Three-Scenario Model

### Pessimistic Scenario (25% weight)
Represents the worst realistic case — not a disaster, but things going poorly.

**Assumptions to stress**:
- Price: 5-15% lower (competitive pressure or required discounting)
- Volume: 30-50% below target (slower market adoption)
- COGS: 10-20% higher (supply chain issues, smaller order quantities)
- Fixed costs: 5-10% higher (unexpected expenses)
- Return rate: 50-100% above baseline

### Base Scenario (50% weight)
Represents the most likely outcome based on available data and reasonable assumptions.

**Grounding assumptions in data**:
- Price: Current planned price validated by competitor analysis
- Volume: Based on comparable product launches or market testing
- Costs: Based on supplier quotes and historical data
- Return rate: Industry average or your historical rate

### Optimistic Scenario (25% weight)
Represents things going better than expected — not a home run, but favorable conditions.

**Assumptions to adjust**:
- Price: Maintained or 5-10% premium (strong differentiation)
- Volume: 25-50% above target (viral moment, strong word-of-mouth)
- COGS: 5-15% lower (volume discounts, supplier negotiation)
- Fixed costs: At or slightly below plan
- Return rate: Below industry average

## Building the Model

### Step 1: Identify Key Variables

List every variable that affects break-even. Rank by impact:

| Variable | Impact on Break-Even | Controllability | Uncertainty |
|---|---|---|---|
| Selling price | High | High | Medium |
| COGS | High | Medium | Medium |
| Monthly volume | High | Low | High |
| Fixed costs | Medium | Medium | Low |
| Shipping costs | Medium | Low | Medium |
| Return rate | Medium | Medium | High |
| Payment fees | Low | Low | Low |

Focus scenarios on the top 3-4 highest-impact, highest-uncertainty variables.

### Step 2: Define Variable Ranges

For each key variable, establish realistic bounds:

| Variable | Pessimistic | Base | Optimistic | Source |
|---|---|---|---|---|
| Price | $42.99 | $49.99 | $54.99 | Competitor range |
| COGS | $14.40 | $12.00 | $10.80 | Supplier tiers |
| Volume/mo | 150 | 250 | 375 | Market analysis |
| Return rate | 12% | 8% | 5% | Industry data |

### Step 3: Calculate Each Scenario

Run the full break-even calculation for each scenario independently. Don't mix variables across scenarios.

### Step 4: Weight and Combine

```
Expected Break-Even = (Pessimistic × 0.25) + (Base × 0.50) + (Optimistic × 0.25)
```

### Step 5: Sensitivity Matrix

Create a two-variable sensitivity table showing break-even across price and volume combinations:

| | Vol 150 | Vol 200 | Vol 250 | Vol 300 | Vol 375 |
|---|---|---|---|---|---|
| **$42.99** | 8.2 mo | 6.1 mo | 4.9 mo | 4.1 mo | 3.3 mo |
| **$46.99** | 6.5 mo | 4.9 mo | 3.9 mo | 3.2 mo | 2.6 mo |
| **$49.99** | 5.6 mo | 4.2 mo | 3.4 mo | 2.8 mo | 2.2 mo |
| **$52.99** | 4.9 mo | 3.7 mo | 2.9 mo | 2.4 mo | 2.0 mo |
| **$54.99** | 4.5 mo | 3.4 mo | 2.7 mo | 2.2 mo | 1.8 mo |

## Monte Carlo Simulation (Advanced)

For high-stakes decisions, run a Monte Carlo simulation:

1. Define probability distributions for each variable (not just 3 points)
2. Run 1,000-10,000 simulations randomly sampling from each distribution
3. Plot the distribution of break-even outcomes
4. Report: median break-even, 10th percentile (likely worst case), 90th percentile (likely best case)

**Interpretation guide**:
- If 90%+ of simulations break even within your timeline → Strong go
- If 60-90% break even → Conditional go with risk mitigation
- If < 60% break even → Reconsider or restructure

## Presenting Scenarios to Stakeholders

### Executive Summary Format

"Under our base case assumptions, we expect to break even at **427 units** (**$21,346 revenue**), achievable in approximately **3.4 months**. In our pessimistic scenario, break-even extends to 582 units (5.6 months). Our optimistic case reaches break-even at 338 units (2.2 months). Across all weighted scenarios, the expected break-even is **478 units in 3.8 months**."

### Visual Recommendations
- **Tornado chart**: Shows which variables have the largest impact on break-even
- **Scenario comparison bar chart**: Side-by-side break-even units for each scenario
- **Cash flow projection**: Monthly cumulative profit/loss curves for all three scenarios
- **Sensitivity heat map**: Color-coded break-even across two-variable grid
