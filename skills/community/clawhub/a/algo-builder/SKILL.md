# Algo Builder Skill

Use this skill when the user wants to build a trading algorithm, develop a trading strategy, test a signal, backtest a strategy, research alpha, validate a trading hypothesis, or structure a systematic trading process.

---

## Scope

This pipeline is optimized for **daily-to-weekly frequency strategies** (swing trading, factor investing, systematic macro, crypto position trading).

**Does NOT apply to HFT** (millisecond to minute): HFT requires order book simulation, tick data, latency modeling, and queue position analytics. If the user is building HFT, redirect them to those specialized tools.

For **intraday strategies** (1min to 4hr): use intraday IC horizons, model bid-ask explicitly, consider volume or dollar bars instead of time bars.

---

## The Correct Order of Operations

Most people start at backtesting. That is wrong. Backtesting is a confirmation tool, not a discovery tool — as Marcos Lopez de Prado puts it: *"Backtesting is not a research tool. Feature importance is."* Starting at backtesting causes overfitting, wasted time, and false confidence.

The correct pipeline:

```
HYPOTHESIS → SIGNAL TEST → STRATEGY CONSTRUCTION → IN-SAMPLE BACKTEST → WALK-FORWARD → PAPER TRADE → LIVE
```

Never skip steps. Never go backward except intentionally.

---

## Step 1: Hypothesis

Before any code, write the hypothesis in plain English.

Prompt the user to answer:
1. What market inefficiency are you exploiting?
2. Why does this edge exist? What is the behavioral or structural reason?
3. Who is on the other side of this trade and why are they consistently wrong?
4. What market conditions would break this edge?
5. What is your expected holding period?

If the user cannot answer all five, the hypothesis is not ready. Do not proceed.

Write the hypothesis into a file: `algo-builder/hypotheses/<strategy-name>.md`

Template:
```
## Hypothesis: <name>
**Edge:** <one sentence>
**Mechanism:** <why the edge exists>
**Counterparty:** <who is wrong and why>
**Regime dependency:** <when it breaks>
**Holding period:** <timeframe>
**Trials so far:** 0  (increment each time you test a variation — needed for DSR in Step 5)
**Status:** [HYPOTHESIS | SIGNAL_TESTED | BACKTESTED | LIVE]
```

---

## Step 2: Signal/Feature Testing

Test each signal component IN ISOLATION before combining them into a strategy. This is the most important and most skipped step.

### What to measure

**Information Coefficient (IC)**
IC = Spearman rank correlation between signal value and forward return over N periods. Use Spearman (not Pearson) — it is robust to outliers and works for non-linear rank relationships.

Calibrated thresholds (per Grinold & Kahn, academic literature, and practitioner consensus):
- IC > 0.15: **Exceptional** — verify data quality first, suspect snooping or data error
- IC 0.05–0.15: **Strong** — pursue aggressively; professional-grade in liquid markets
- IC 0.02–0.05: **Moderate** — viable in ensemble; common in efficient US equity markets
- IC 0.01–0.02: **Weak** — only viable at scale (100+ assets, high breadth)
- IC < 0.01: **No edge** — discard
- IC < 0 (negative): signal may be inversely useful — investigate before discarding

Note: In crypto (less efficient than equities), IC thresholds can be higher. In highly liquid large-cap equities, IC 0.03 is genuinely good. Calibrate to your asset class.

**IC Information Ratio (ICIR) — equally important as IC itself**
ICIR = mean(IC) / std(IC) over rolling windows. Measures consistency of the signal over time.
- ICIR > 1.0: Highly stable — strong independent evidence of real edge
- ICIR 0.5–1.0: Acceptable stability — proceed
- ICIR < 0.5: Unstable — even a decent IC here is unreliable; do not proceed

A signal with IC 0.08 but ICIR 0.3 is more dangerous than a signal with IC 0.04 and ICIR 0.9. Consistency matters as much as magnitude.

**IC Stability (Rolling)**
Plot rolling IC over time. Consistent positive IC across multiple market regimes is required. IC that only appears in one regime has conditional validity — you must then condition entry on that regime.

**Decay Analysis**
Test IC at 1-bar, 3-bar, 5-bar, 10-bar, 20-bar forward horizons. Does the signal's predictive power decay gracefully or cliff-edge? This reveals the natural holding period.

**T-stat on IC**
IC must be statistically significant: t-stat > 2.0 (p < 0.05) over the test period.

**Regime Conditioning**
Test IC separately in different market regimes (bull/bear, high-vol/low-vol). A signal with IC 0.06 in all regimes is far better than IC 0.12 only in bull markets. Document regime dependency clearly.

Simple regime proxies:
```python
# Price above/below 200-day MA
def bull_bear_regime(prices):
    ma200 = prices.rolling(200).mean()
    return (prices > ma200).astype(int)  # 1=bull, 0=bear

# VIX-based volatility regime
def vol_regime(vix):
    return pd.cut(vix, bins=[0, 15, 25, 100], labels=['low', 'medium', 'high'])
```

### Signal testing template

Ask the user for:
- Signal name and definition (exact calculation)
- Asset and data source
- Test period
- Forward return horizon to test
- How many other signals have been tested so far (needed for multiple testing correction)

Write `scripts/test_signal.py`:

```python
import pandas as pd
import numpy as np
from scipy import stats

def compute_ic(signal: pd.Series, forward_returns: pd.Series) -> dict:
    """Compute Information Coefficient using Spearman rank correlation."""
    combined = pd.concat([signal, forward_returns], axis=1).dropna()
    signal_col, return_col = combined.columns

    ic, pvalue = stats.spearmanr(combined[signal_col], combined[return_col])
    t_stat = ic * np.sqrt((len(combined) - 2) / (1 - ic**2))

    return {
        "IC": round(ic, 4),
        "p_value": round(pvalue, 4),
        "t_stat": round(t_stat, 4),
        "n_obs": len(combined),
        "verdict": _verdict(ic, pvalue)
    }

def _verdict(ic: float, pvalue: float) -> str:
    if pvalue > 0.05:
        return "REJECT: Not statistically significant"
    if ic < 0.01:
        return "REJECT: IC too low, no edge"
    if ic > 0.15:
        return "FLAG: Exceptional IC — verify data quality before proceeding"
    if 0.01 <= ic < 0.02:
        return "WEAK: Viable only at high breadth/scale"
    if 0.02 <= ic < 0.05:
        return "MODERATE: Viable in ensemble"
    if 0.05 <= ic < 0.15:
        return "STRONG: Pursue this signal"
    return "STRONG: Pursue this signal"

def compute_icir(rolling_ic: pd.Series) -> dict:
    """Compute IC Information Ratio from rolling IC series."""
    icir = rolling_ic.mean() / rolling_ic.std()
    return {
        "ICIR": round(icir, 4),
        "mean_IC": round(rolling_ic.mean(), 4),
        "std_IC": round(rolling_ic.std(), 4),
        "verdict": "STABLE" if icir > 0.5 else "UNSTABLE — do not proceed even with good IC"
    }

def test_ic_decay(signal: pd.Series, prices: pd.Series, horizons=[1,3,5,10,20]) -> pd.DataFrame:
    """Test IC at multiple forward horizons to find natural holding period."""
    results = []
    for h in horizons:
        fwd_ret = prices.pct_change(h).shift(-h)
        result = compute_ic(signal, fwd_ret)
        result["horizon"] = h
        results.append(result)
    return pd.DataFrame(results).set_index("horizon")

def test_ic_stability(signal: pd.Series, forward_returns: pd.Series, window=52) -> pd.Series:
    """Rolling IC to check stability over time."""
    rolling_ic = []
    for i in range(window, len(signal)):
        s = signal.iloc[i-window:i]
        r = forward_returns.iloc[i-window:i]
        ic, _ = stats.spearmanr(s.dropna(), r.dropna())
        rolling_ic.append(ic)
    return pd.Series(rolling_ic, index=signal.index[window:])

def test_ic_by_regime(signal, forward_returns, regime_indicator, regime_labels):
    """Test IC conditional on market regime."""
    results = {}
    for regime_id, regime_name in regime_labels.items():
        mask = regime_indicator == regime_id
        s = signal[mask]
        r = forward_returns[mask]
        if len(s) > 20:
            ic, pval = stats.spearmanr(s.dropna(), r[s.notna()])
            results[regime_name] = {
                "IC": round(ic, 4),
                "p_value": round(pval, 4),
                "n_obs": len(s.dropna())
            }
    return results
```

### Gate

A signal passes to Step 3 ONLY IF ALL of the following:
- IC is statistically significant (p < 0.05)
- IC > 0.02 (adjust higher for less efficient markets like crypto)
- ICIR > 0.5 (stability is required, not optional)
- IC positive in at least 55% of rolling windows
- IC holds in at least one market regime with sufficient observations

Document results in `algo-builder/signals/<signal-name>.md`.

**Multiple testing note:** If this is the Nth signal tested, flag it. The more signals tested, the higher the probability that a passing signal is a false positive. Track trial count in the hypothesis file. This feeds into DSR in Step 5.

---

## Step 3: Strategy Construction

Combine validated signals into a complete strategy. Define each component explicitly before writing backtest code.

### Required components

**Entry logic**
- Which signals trigger entry?
- How are they combined (AND, OR, weighted score)?
- Minimum signal threshold to enter?
- Regime condition required? (if signal only works in one regime, entry must be conditioned on that regime)

**Exit logic** (define ALL of these — do not leave any as "figure it out later")
- Signal-based exit: when signal reverses
- Time-based exit: max hold period
- Stop loss: fixed % or ATR-based
- Take profit: fixed target or trailing

**Position sizing**
- Fixed fractional (% of portfolio per trade)
- Kelly Criterion (if you have reliable win rate and avg win/loss)
- ATR-normalized (size inversely proportional to volatility)
- Never: "all in" or undefined sizing

**Risk controls** (separate from signal logic, always on)
- Max position size per asset
- Max correlated positions open simultaneously
- Daily loss limit (halt trading if breached)
- Max drawdown circuit breaker

**Transaction Cost Budget** (quantify before backtesting — not a checkbox)

Specify:
- Expected gross edge (rough estimate from IC × √Breadth approximation)
- Commission: __ bps
- Bid-ask spread: __ bps
- Market impact estimate: use `8bps × (position_size / ADV)^0.5` as a rough rule
- Total TC: __ bps

Red flags:
- Total TC > 30% of gross alpha: strategy likely not viable after costs
- Turnover > 500%/year at daily frequency: TC will likely destroy the edge
- Position > 1% of ADV: model market impact explicitly, don't use the rough rule

**Capacity check**
- What is the average daily volume of the instruments traded?
- At what AUM does market impact exceed signal value?
- Small-cap and crypto strategies can have very low capacity ceilings

Write the full strategy specification into `algo-builder/strategies/<name>.md` before writing any backtest code.

---

## Step 4: In-Sample Backtest

Split your data: 70% train, 30% test. Seal the test set. Do not touch it.

Run the backtest on the TRAIN set only.

### Minimum acceptance criteria (in-sample)
- Sharpe Ratio > 1.0 (> 1.5 preferred)
- Max Drawdown within stated tolerance
- Profit Factor > 1.3
- Win Rate > 40% (or Expectancy clearly positive)
- Minimum 30 trades (for statistical significance)

If the strategy fails these, go back to Step 3. Max 3 parameter adjustment cycles before reconsidering the hypothesis. **Each adjustment cycle increments your trial count** — this matters for DSR in Step 5.

### Bias checklist (check all before accepting results)
- [ ] No look-ahead bias: signals computed only from data available at bar close
- [ ] Survivorship bias addressed: include delisted assets if testing equities
- [ ] Transaction costs included with realistic estimates (not just a checkbox — see Step 3 TC budget)
- [ ] Liquidity check: can you actually fill at these prices given your size?
- [ ] No data-snooping: have you looked at the test set at all? (honest answer required)
- [ ] For crypto: wash trading filtered from volume-based signals

---

## Step 5: Walk-Forward Validation + Overfitting Correction

This is what separates a real strategy from a backtest artifact.

### Walk-Forward Method
1. Define in-sample window (e.g., 6 months)
2. Define out-of-sample window (e.g., 1 month)
3. Optimize parameters on in-sample window
4. Test on out-of-sample window (no reoptimization)
5. Roll forward. Repeat across full history.

**Acceptance criteria:**
- Out-of-sample Sharpe > 0.7 (degradation from in-sample is expected and normal)
- Out-of-sample / In-sample Sharpe ratio > 0.5
- Out-of-sample profitable in > 60% of windows
- No cliff-edge degradation in recent windows (suggests regime change or alpha decay)

If walk-forward fails: the strategy is overfit. Return to Step 3.

### Deflated Sharpe Ratio (DSR) — Multiple Testing Correction

Walk-forward gives you ONE path through history. The DSR asks: given how many variations you tested to get here, how likely is this Sharpe to be real?

After only 1,000 independent backtests, the expected maximum Sharpe is ~3.26 even if the true SR of every strategy is zero (Bailey & Lopez de Prado, 2013). This is the #1 cause of false discoveries in systematic trading.

```python
def deflated_sharpe_ratio(sharpe_obs, n_trials, obs_per_year=252):
    """
    Adjust observed Sharpe for selection bias from multiple testing.
    Based on Bailey & Lopez de Prado (2013), Journal of Portfolio Management.

    Args:
        sharpe_obs: Observed annualized Sharpe ratio
        n_trials: Total strategy/parameter variations tested (be honest)
        obs_per_year: Trading days per year
    Returns:
        dict with DSR assessment
    """
    import scipy.stats as ss
    import numpy as np

    euler_gamma = 0.5772
    expected_max_sr = (1 - euler_gamma) * ss.norm.ppf(1 - 1/max(n_trials, 2)) + \
                      euler_gamma * ss.norm.ppf(1 - 1/(max(n_trials, 2) * np.e))
    sr_benchmark = expected_max_sr / np.sqrt(obs_per_year)

    return {
        "observed_sharpe": sharpe_obs,
        "expected_max_sr_if_all_noise": round(expected_max_sr, 3),
        "n_trials": n_trials,
        "passes_dsr": sharpe_obs > sr_benchmark,
        "verdict": "PASSES" if sharpe_obs > sr_benchmark else "FAIL: Sharpe may be a false positive given number of trials"
    }
```

Track `n_trials` from the start (in the hypothesis file). Include every parameter variation, every signal variant, and every strategy reformulation you tested.

### CPCV (Optional but recommended for higher confidence)

Combinatorial Purged Cross-Validation generates a distribution of OOS paths rather than one, making overfitting detection more robust than walk-forward alone. Implement from Lopez de Prado's AFML Chapter 12 or use the `mlfinlab` library.

Write walk-forward + DSR results into `algo-builder/results/<name>_walkforward.md`.

---

## Step 6: Paper Trade

Before live capital, run on live data with simulated fills for a minimum of:
- 20 completed trades, OR
- 4 weeks, whichever is longer

Compare paper trade metrics to backtest expectations:
- Is the entry fill rate reasonable?
- Is slippage within assumed bounds?
- Are signals triggering as expected?

If paper trade significantly underperforms backtest: find out why before going live. Common culprits: execution assumptions, data latency, bid-ask spread not modeled, regime shift since backtest period.

---

## Step 7: Live Deployment (small size)

Start at 10-25% of intended position size. Scale up only after:
- Live performance within reasonable band of backtest expectations
- At least 20 live trades completed
- No unexplained drawdowns

---

## Output Files

Maintain this folder structure:
```
algo-builder/
  hypotheses/        # Step 1 - one file per strategy idea (includes trial count)
  signals/           # Step 2 - IC, ICIR, decay, regime results per signal
  strategies/        # Step 3 - full strategy specs including TC budget
  results/           # Steps 4+5 - backtest + walkforward + DSR results
  scripts/           # reusable Python scripts
    test_signal.py
    backtest.py
    walkforward.py
    fetch_data.py
```

---

## Working with the User

When the user describes a strategy idea:
1. Ask the 5 hypothesis questions before touching code
2. Identify all distinct signals in the strategy
3. Ask how many signals/strategies have already been tested (for DSR tracking)
4. Run signal tests FIRST, report IC AND ICIR results
5. Only proceed to backtest if signals pass the full gate (IC + ICIR + regime)
6. Always report both in-sample AND walk-forward + DSR results
7. Never call a strategy "good" based on in-sample only

When the user presents backtest results for review:
- Ask if walk-forward was done
- Ask how many variations were tested (DSR check)
- Check the bias checklist
- Ask for number of trades (flag if < 30)
- Ask what the transaction cost assumption was and if it was quantified

When the user wants to just "write the strategy code":
- Redirect to hypothesis and signal testing first
- Explain why: "A backtest without signal validation is just curve-fitting. We test the signals first so we know the edge is real before spending time on the full backtest."

---

## Asset Class Notes

**US Equities (daily):** IC 0.03–0.05 is genuinely good in efficient large-cap markets. Breadth (number of independent bets) matters as much as IC magnitude. Include delisted stocks to avoid survivorship bias.

**Crypto:** Less efficient — IC thresholds can be higher (0.05–0.10 achievable). Regime instability is extreme (bull/bear cycles are fast and severe). IC by regime is essential. Filter wash trading from volume signals. Shorter valid history (2017–present for liquid multi-exchange data).

**Futures/Macro:** Trend-following factors have longer holding periods — IC decay analysis is especially important. Model roll yield and funding costs in TC budget.

**HFT:** This pipeline does not apply. See Scope section above.

---

## Common Mistakes to Flag

- "I backtested and got 300% returns": ask about max drawdown, number of trades, transaction costs, walk-forward, and how many strategies were tested before this one
- "I optimized the parameters until it looked good": this is overfitting, explain the bias and check DSR
- "I'll add a stop loss later": stops are part of strategy construction, not an afterthought
- "IC is 0.12, that's strong": flag as exceptional — verify data quality before celebrating
- "I just need to backtest this one idea": ask how many ideas came before it — that's your trial count
- Using daily close prices for intraday strategies: look-ahead bias
- Testing on the same data used to get the idea: data-snooping bias
- Skipping ICIR: a signal with inconsistent IC is more dangerous than a weak but consistent one

---

## Key References

- Grinold & Kahn, *Active Portfolio Management* (1999) — IC framework, Fundamental Law
- Lopez de Prado, *Advances in Financial Machine Learning* (2018) — CPCV, feature importance, production pipeline
- Bailey & Lopez de Prado, "The Deflated Sharpe Ratio" (2013) — multiple testing correction
- Almgren & Chriss (2000) — market impact modeling
