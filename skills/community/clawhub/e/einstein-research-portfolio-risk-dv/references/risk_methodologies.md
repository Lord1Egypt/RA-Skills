# Risk Methodologies Reference

*Einstein Research — Portfolio Risk Management*

---

## Table of Contents

1. [Value at Risk (VaR)](#value-at-risk)
2. [CVaR / Expected Shortfall](#cvar--expected-shortfall)
3. [Maximum Drawdown & Circuit Breakers](#maximum-drawdown--circuit-breakers)
4. [Correlation Analysis & Diversification](#correlation-analysis--diversification)
5. [Stress Testing Framework](#stress-testing-framework)
6. [Portfolio Beta Calculation](#portfolio-beta)
7. [Risk Budgeting](#risk-budgeting)
8. [Sector & Factor Concentration](#sector--factor-concentration)
9. [Common Pitfalls](#common-pitfalls)
10. [Recommended Reading](#recommended-reading)

---

## Value at Risk (VaR)

### Definition

VaR answers: *"What is the maximum loss I will incur with probability X% over a given time horizon?"*

Formally, if `r` is a portfolio return and `α` is the confidence level:

```
VaR_α = -Q_α(r)
```

Where `Q_α(r)` is the α-quantile of the return distribution.

**Important**: A 95% VaR is *exceeded* 5% of the time. Over 252 trading days, that's ~13 days per year. VaR is not a worst-case number.

---

### Method 1: Parametric (Variance-Covariance)

**Assumption**: Returns are normally distributed.

**Formula** (1-day, single asset):
```
VaR_α = -(μ + z_α × σ)
```

Where:
- `μ` = mean daily return
- `σ` = standard deviation of daily returns
- `z_α` = inverse normal CDF at confidence level α
  - z₀.₉₅ = -1.645
  - z₀.₉₉ = -2.326

**Portfolio extension**:
```
σ_portfolio² = wᵀ Σ w
```

Where `w` is the weight vector and `Σ` is the covariance matrix.

**When to use**: Normal market conditions, large diversified portfolios.

**Limitations**:
- Underestimates tail risk (real returns are fat-tailed / leptokurtic)
- Assumes stable correlation structure
- Fails during stress events when correlations spike

---

### Method 2: Historical Simulation

**Assumption**: The future will look like the past (within the lookback window).

**Procedure**:
1. Collect N days of portfolio returns (typically 252–504 days)
2. Sort returns from worst to best
3. VaR at α confidence = loss at the (1-α)×N percentile

**Formula**:
```
VaR_α = -percentile(r_historical, (1-α) × 100)
```

**When to use**: When the return distribution is known to be non-normal; as the primary VaR estimate in stressed regimes.

**Limitations**:
- Depends entirely on the lookback period (recent history may not include tail events)
- Equally weights all historical days — a 2008 event from 10 years ago counts the same as last week
- "Quiet periods" in history lead to underestimating risk

**Lookback guidance**:
- 1 year (252 days): Captures recent regime, misses past crises
- 2 years (504 days): Balanced
- 5 years (1260 days): Captures major cycles but may dilute recent regime

---

### Method 3: Monte Carlo Simulation

**Procedure**:
1. Estimate mean vector `μ` and covariance matrix `Σ` from historical returns
2. Generate N simulated 1-day return vectors using correlated multivariate normal:
   ```
   r_sim = μ + L × z
   ```
   Where `L` is the Cholesky decomposition of `Σ` (so `Σ = LLᵀ`) and `z ~ N(0, I)`
3. Compute portfolio return for each simulation: `r_portfolio = wᵀ r_sim`
4. Take the empirical percentile of simulated portfolio returns

**When to use**:
- Portfolios with derivatives (options, structured products)
- When you want to model non-normal marginal distributions
- Scenario-based "what-if" analyses

**Limitations**:
- Quality depends on the assumed distribution and covariance estimate
- Standard MC assumes multivariate normality — same fat-tail limitation as parametric
- Computationally heavier (10,000 simulations typical)

**Extension — Student-t MC**: Replace `z ~ N(0,I)` with `z ~ t(ν)` (Student-t with ν degrees of freedom) to capture heavier tails. ν = 4–6 is typical for equity returns.

---

### Scaling VaR Across Time Horizons

The *square-root-of-time rule* scales 1-day VaR to longer horizons:

```
VaR_T = VaR_1 × √T
```

**Warning**: This assumes i.i.d. returns (no autocorrelation). It underestimates multi-day VaR when returns exhibit autocorrelation (e.g., momentum or mean-reversion regimes) or when risk factors are trending.

For regulatory purposes (Basel III): use 10-day VaR = VaR_1 × √10

---

## CVaR / Expected Shortfall

### Definition

CVaR (Conditional Value at Risk), also called Expected Shortfall (ES), answers: *"Given that I am in the worst X% of outcomes, what is my average loss?"*

```
CVaR_α = -E[r | r < -VaR_α]
```

### Why CVaR is Superior to VaR

VaR tells you nothing about severity beyond the threshold. Two portfolios with identical VaR can have wildly different tail behavior:
- Portfolio A: loses exactly 2% on bad days (thin tail)
- Portfolio B: has 2% VaR but occasional 10%+ crashes (fat tail)

CVaR captures this distinction. It is:
- **Sub-additive**: CVaR(A + B) ≤ CVaR(A) + CVaR(B) — combining portfolios can only reduce risk
- **Convex**: Enables proper risk optimization
- **Coherent**: Satisfies all four axioms of coherent risk measures (monotonicity, sub-additivity, positive homogeneity, translation invariance)

VaR is *not* sub-additive, which is why it can understate diversification benefits and is being replaced by CVaR in regulatory frameworks.

### Numerical Calculation

For historical simulation:
```python
var_95 = np.percentile(returns, 5)    # 5th percentile for 95% confidence
cvar_95 = returns[returns <= var_95].mean()   # Average of tail returns
```

### CVaR Optimization

Modern portfolio theory optimized for CVaR minimization (Rockafellar-Uryasev 2000):

```
min CVaR_α(w) subject to:
  Σ wᵢ = 1
  wᵢ ≥ 0 (long-only)
  expected return ≥ target
```

This is a linear programming problem solvable with scipy or cvxpy.

---

## Maximum Drawdown & Circuit Breakers

### Maximum Drawdown Definition

```
MDD = min over time t of: (W_t - max(W_s for s ≤ t)) / max(W_s for s ≤ t)
```

Where `W_t` is portfolio wealth at time t.

Equivalently: the percentage decline from the highest peak to the subsequent trough.

### Key Drawdown Metrics

| Metric | Description |
|---|---|
| Maximum Drawdown | Largest peak-to-trough decline in history |
| Current Drawdown | Current decline from the most recent peak |
| Drawdown Duration | Days from peak to full recovery |
| Calmar Ratio | Annual return / Max Drawdown |
| MAR Ratio | CAGR / Max Drawdown |

### Circuit Breaker Design

Circuit breakers are **pre-committed rules** for drawdown response. Their value comes from pre-commitment — you agree to the rules before the drawdown happens, when you're thinking rationally.

**Default circuit breakers** (customize to your risk tolerance):

| Level | Threshold | Required Action |
|---|---|---|
| Yellow | -10% from peak | Document rationale for continuing to hold. Review all theses. |
| Red | -20% from peak | Reduce all positions by 50%. Reassess before adding back. |
| Critical | -30% from peak | Exit to 100% cash. Full portfolio review before re-entry. |

**Why these thresholds?**
- A -10% drawdown is within normal volatility for a diversified equity portfolio (one standard deviation event)
- A -20% drawdown is bear market territory; the thesis needs revalidation
- A -30% drawdown indicates systematic failure; capital preservation takes priority

**Behavioral finance rationale**: Investors who pre-commit to circuit breakers outperform those who rely on in-the-moment judgment. The Kahneman/Tversky loss aversion bias causes investors to hold losers too long and sell winners too early. Circuit breakers override this bias.

### Drawdown and Position Sizing

Kelly Criterion suggests position sizes consistent with expected drawdown tolerance:

```
f* = (p × b - q) / b
```

Where `p` = win probability, `b` = win/loss ratio, `q = 1 - p`.

Half-Kelly is recommended for real portfolios to account for parameter estimation error.

---

## Correlation Analysis & Diversification

### Correlation Matrix

The Pearson correlation coefficient between assets i and j:

```
ρᵢⱼ = Cov(rᵢ, rⱼ) / (σᵢ × σⱼ)
```

### Diversification Score

Our diversification score ranges 0–100:

```
diversification_score = (1 - avg_pairwise_correlation) × 100
```

Where `avg_pairwise_correlation` is the mean of all |ρᵢⱼ| for i ≠ j.

**Interpretation**:
- 80–100: Excellent diversification
- 60–79: Good
- 40–59: Moderate — consider adding uncorrelated assets
- 20–39: Poor — essentially concentrated in one factor
- 0–19: No diversification — all assets move together

### Correlation Breakdown in Crises

**The Crisis Correlation Problem**: In normal markets, correlations between different sectors and asset classes are moderate (0.3–0.6). During systemic stress events:

- Equity-equity correlations spike toward 1.0 (everyone sells everything)
- Defensive stocks (XLP, XLU) lose their low-correlation property
- International diversification fails (global selloffs are synchronized)
- Only a few assets maintain or improve diversification:
  - **Long Treasuries (TLT)**: Negative correlation during risk-off events (flight to safety) — *exception: 2022, where both equities and bonds fell due to inflation*
  - **Gold (GLD)**: Near-zero to negative correlation in systemic events
  - **Cash (BIL, SGOV)**: Perfect negative correlation to any drawdown
  - **Long Volatility (UVXY, VXX)**: Strongly negative to equity in crashes, but costly carry

### Correlation Clustering

Use hierarchical clustering on the correlation matrix to identify "risk groups":
- Assets within a cluster tend to move together
- True diversification requires owning assets from different clusters

The risk_portfolio.py script outputs the raw correlation matrix; use a heatmap for visual clustering.

---

## Stress Testing Framework

### Philosophy

Stress testing answers: *"How bad could it get, given a scenario I care about?"*

Unlike VaR (which is statistical), stress tests are scenario-based and deliberately pick specific events rather than estimating probabilities.

### Historical Scenario Selection Rationale

**2008 Global Financial Crisis (Sep 2008 – Mar 2009)**
- Triggered by: Subprime mortgage collapse, Lehman Brothers bankruptcy
- Characteristic: Systemic financial contagion, credit market freeze, forced deleveraging
- Why it matters: Tests behavior during a *liquidity crisis* where normal correlations break down and all risky assets fall together
- Benchmark loss: SPY -50%, TLT +25%, GLD +15%

**2020 COVID Flash Crash (Feb 19 – Mar 23, 2020)**
- Triggered by: Pandemic lockdowns, economic shutdown uncertainty
- Characteristic: Fastest bear market in history (34 days), then rapid recovery
- Why it matters: Tests behavior during an *exogenous shock* with high VIX (85+) and extreme short-term volatility
- Benchmark loss: SPY -34%, followed by +100% recovery within 5 months

**2022 Rate Hike Cycle (Jan 2022 – Oct 2022)**
- Triggered by: Fed pivot from 0% to 4.5% rates to combat 8%+ inflation
- Characteristic: Growth stock re-rating, duration risk in bonds, unusual equity+bond correlation
- Why it matters: The ONLY recent period where the 60/40 portfolio severely underperformed — tests *duration and rate sensitivity*
- Notable: TLT fell -30%, QQQ fell -35%, traditional safe havens failed

### Custom Stress Tests

Beyond historical scenarios, consider forward-looking scenarios:

| Scenario | Shock Parameters | Implementation |
|---|---|---|
| Rate shock +200bps | Duration-weighted bond losses; growth stock multiple compression | Apply to positions based on duration/growth exposure |
| Dollar +15% (strong USD) | EM equities -20%, US multinationals -5-10% | Apply to positions with overseas revenue |
| Oil +$50/barrel | Energy +30%, airlines/transports -15%, consumer -5% | Apply by sector |
| China hard landing | EM Asia -40%, luxury goods -20%, semiconductors -15% | Apply by revenue exposure |
| US recession | Cyclicals -30%, defensives -5%, TLT +20% | Apply by economic sensitivity |

---

## Portfolio Beta

### Definition

Beta measures a portfolio's sensitivity to market movements:

```
β = Cov(r_portfolio, r_benchmark) / Var(r_benchmark)
```

**Interpretation**:
- β = 1.0: Portfolio moves 1:1 with the benchmark
- β = 1.5: Portfolio moves 1.5% for every 1% benchmark move (amplified)
- β = 0.5: Portfolio moves 0.5% for every 1% benchmark move (defensive)
- β = 0: Market-neutral
- β < 0: Inverse to market (rare for long-only portfolios)

### Calculating Portfolio Beta

The portfolio beta is the weighted average of individual asset betas:

```
β_portfolio = Σᵢ wᵢ × βᵢ
```

Where `βᵢ` is each asset's regression beta vs the benchmark and `wᵢ` is portfolio weight.

Alternatively, compute directly from portfolio and benchmark return series (more accurate for multi-asset portfolios).

### Beta vs Different Benchmarks

| Benchmark | Use Case |
|---|---|
| SPY (S&P 500) | Overall market sensitivity |
| QQQ (Nasdaq 100) | Tech/growth sensitivity |
| IWM (Russell 2000) | Small cap factor exposure |
| TLT (20+ Year Treasury) | Duration/rate sensitivity |
| GLD (Gold) | Inflation hedge sensitivity |

A portfolio with high SPY beta and low QQQ beta is more value/financial oriented. High QQQ beta relative to SPY signals tech/growth concentration.

### Managing Beta

**When to reduce beta**:
- Pre-earnings season for concentrated portfolios
- Before FOMC meetings if macro-sensitive
- When VIX > 25 (elevated uncertainty)
- When circuit breaker yellow is triggered

**Beta reduction tools**:
- Add TLT (typically negative beta to SPY)
- Short SPY/QQQ via puts or inverse ETFs
- Add cash (BIL, SGOV)
- Trim highest-beta positions

---

## Risk Budgeting

### Concept

Risk budgeting allocates portfolio risk capacity across positions rather than allocating dollar capital. It answers: *"How much of my total portfolio risk does each position contribute?"*

### Component VaR (Marginal Risk Contribution)

The contribution of position i to total portfolio variance:

```
RC_i = wᵢ × (Σw)ᵢ / σ²_portfolio
```

Where:
- `wᵢ` = weight of position i
- `(Σw)ᵢ` = i-th element of the covariance matrix times weight vector
- `σ²_portfolio = wᵀΣw`

Note: `Σᵢ RC_i = 1` (risk contributions sum to 100%)

### Interpreting Risk Budget

**Risk/Weight Ratio** = RC_i / w_i

- Ratio = 1.0: Position's risk contribution matches its dollar weight (neutral)
- Ratio > 1.0: Position is oversized on a risk basis (high volatility or high correlation to portfolio)
- Ratio < 1.0: Position punches below its weight in risk (low volatility or diversifying)

**Example**:
- NVDA is 10% of portfolio but contributes 30% of variance → ratio 3.0 → NVDA is 3× too large on risk basis
- TLT is 10% of portfolio but contributes 2% of variance → ratio 0.2 → TLT is a net diversifier

### Equal Risk Contribution (ERC) Portfolio

The "risk parity" portfolio allocates weights so each position contributes equally to total risk:

```
RC_i = RC_j for all i, j
```

This requires an iterative solver (the ERC weights are not analytically solvable in general). The result is a portfolio that is intrinsically diversified by risk, not by dollars.

### Risk Budget Limits

Common institutional rules:
- Single position max risk contribution: 20–25%
- Largest sector max risk contribution: 40%
- Single country max risk contribution: 30%

---

## Sector & Factor Concentration

### Sector Concentration Analysis

Compare portfolio sector weights to a benchmark (SPY GICS weights):

```
concentration_ratio = portfolio_weight_sector / benchmark_weight_sector
```

**Thresholds**:
- Ratio > 2×: Significant overweight — intentional or accidental?
- Ratio > 3×: High concentration risk — requires explicit rationale

### Factor Exposure

Beyond sectors, consider factor exposures:

| Factor | High Exposure Characteristics | How to Check |
|---|---|---|
| Market beta | High-beta stocks, leveraged ETFs | Beta vs SPY > 1.3 |
| Size | Small/micro-cap concentration | IWM beta vs SPY beta |
| Value | Low P/E, high dividend yield | Holdings' P/B ratios |
| Growth | High P/E, high revenue growth | Holdings' P/E ratios |
| Momentum | Recent 12-month winners | Holdings' 12-month returns |
| Quality | High ROE, low debt | Holdings' fundamentals |
| Volatility | High daily % moves | Average position beta |

### Hidden Concentration: Revenue Exposure

A portfolio of "diversified" US companies can have hidden concentration through:

- **China revenue exposure**: AAPL, QCOM, AVGO, NVDA all generate 20-30%+ from China
- **Interest rate sensitivity**: REITs, utilities, banks all respond strongly to rate changes
- **Ad revenue dependency**: GOOGL, META, TTD, SNAP
- **Consumer credit exposure**: V, MA, PYPL, consumer finance names

Traditional sector analysis misses these cross-sector correlations.

---

## Common Pitfalls

### 1. VaR Gives False Comfort

VaR at 99% is exceeded ~2.5 times per year on average. It tells you nothing about severity when it's exceeded. Always pair VaR with CVaR.

### 2. Short History = Underestimated Risk

A portfolio analyzed only over 2021–2022 bull market will have artificially low historical VaR. Use at least 3–5 years; ideally spanning a full market cycle including a 20%+ drawdown.

### 3. Correlation ≠ Causation ≠ Stability

Correlations measured in calm markets break down in crises. Always run crisis stress tests *in addition to* correlation analysis.

### 4. Beta is Not Static

Beta changes with market regimes. A stock with β = 0.8 in bull markets can have β = 1.5 in bear markets (pro-cyclical behavior). Use rolling 60-day beta to detect shifts.

### 5. Normality Assumption Failure

Equity returns have:
- **Fat tails** (kurtosis > 3): Extreme events happen more often than a normal distribution predicts
- **Negative skew**: Crashes are larger than rallies on a per-move basis
- **Volatility clustering**: High-vol periods cluster (GARCH effect)

Parametric VaR ignores all of these. Use it only as a baseline; primary risk estimates should come from historical simulation or fat-tailed MC.

### 6. Survivorship Bias in Stress Tests

The tickers in your portfolio may not have data for 2008 (especially if they were founded after). When testing against 2008 GFC, any ticker with missing 2008 data will silently exclude from the stress test. Check `trading_days` in stress results — if far less than the expected period length, data is sparse.

### 7. Risk Budget Drift

As prices move, portfolio weights drift, and so does the risk budget. A position that was 15% of risk on January 1 might be 25% of risk by July 1 if it outperformed. Review risk budget quarterly or after major moves.

---

## Recommended Reading

### Academic Papers

1. **Markowitz (1952)** — "Portfolio Selection" — *Journal of Finance*
   - Foundation of mean-variance optimization and the efficient frontier

2. **Jorion (2006)** — *Value at Risk: The New Benchmark for Managing Financial Risk*
   - Standard textbook on VaR methods; comprehensive parametric and simulation approaches

3. **Rockafellar & Uryasev (2000)** — "Optimization of Conditional Value-at-Risk" — *Journal of Risk*
   - Formal treatment of CVaR as a linear programming problem; the basis for CVaR optimization

4. **Longin & Solnik (2001)** — "Extreme Correlation of International Equity Markets" — *Journal of Finance*
   - Demonstrates that correlations increase in bear markets; foundational for understanding diversification failure in crises

5. **Ang & Chen (2002)** — "Asymmetric Correlations of Equity Portfolios" — *Journal of Financial Economics*
   - Correlations between US stocks are higher during downturns than upturns

### Books

- **Nassim Taleb — The Black Swan (2007)**: Fat tails, tail risk, why normal distribution models fail
- **Petter Kolm & Roy Kouwenberg — Advanced Risk & Portfolio Management**: Practitioner-level risk systems
- **Philippe Jorion — Value at Risk**: The definitive reference text on VaR methodology
- **Emanuel Derman — The Volatility Smile**: Deep dive into options-based risk management

### Practical Resources

- **MSCI Risk Manager documentation**: Industry-standard factor model descriptions
- **Bloomberg PORT**: Professional risk system; useful to compare against for methodology validation
- **QuantLib**: Open source library for derivatives pricing and risk analytics (Python binding: `QuantLib-Python`)

---

*Last updated: 2024 | Einstein Research Portfolio Risk v1.0.0*
