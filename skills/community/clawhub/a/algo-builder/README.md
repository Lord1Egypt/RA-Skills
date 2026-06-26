# Algo Builder

A systematic trading strategy skill for OpenClaw agents. Guides you through the correct order of operations for building, testing, and validating trading algorithms — from hypothesis to live deployment.

Built by Scampi & Tonbi ([Tonbi Studio](https://www.tonbistudio.com)).

---

## What It Does

Most people start at backtesting. That's wrong. This skill enforces the correct pipeline:

```
HYPOTHESIS → SIGNAL TEST → STRATEGY CONSTRUCTION → IN-SAMPLE BACKTEST → WALK-FORWARD → PAPER TRADE → LIVE
```

At each step, the agent asks the right questions, generates the right code, and gates you from moving forward until the evidence actually supports it.

---

## Who It's For

- Systematic traders building daily-to-weekly frequency strategies
- Crypto, equities, futures, macro
- Anyone who wants to stop overfitting and start finding real edge

**Not for:** HFT (millisecond to minute frequency) — that requires a different toolset entirely.

---

## What You Get

### Step 1: Hypothesis Framework
Forces you to answer 5 questions before writing a line of code — what's the edge, why does it exist, who's on the other side, when does it break.

### Step 2: Signal Testing
Generates `test_signal.py` with:
- **IC (Information Coefficient)** — Spearman rank correlation of signal vs forward returns
- **ICIR** — IC consistency over time (as important as IC magnitude)
- **IC decay analysis** — finds the natural holding period
- **Rolling IC stability** — checks if edge holds across market regimes
- Calibrated thresholds based on Grinold & Kahn + practitioner consensus

### Step 3: Strategy Construction
Full spec before any backtest code — entry/exit logic, position sizing, risk controls, and a quantified transaction cost budget (not a checkbox).

### Step 4: In-Sample Backtest
Bias checklist: look-ahead, survivorship, data-snooping, liquidity. Minimum acceptance criteria enforced.

### Step 5: Walk-Forward + Deflated Sharpe Ratio
Walk-forward validation across the full history. DSR correction (Bailey & Lopez de Prado 2013) adjusts your Sharpe for how many strategies you tested to get here — the #1 cause of false discoveries in systematic trading.

### Steps 6-7: Paper Trade → Live
Minimum criteria before touching real capital.

---

## Example Prompts

```
"I want to build a momentum strategy for crypto"
"Help me test if RSI divergence has predictive power on BTC daily"
"I have a signal idea — rising volume + price consolidation before breakout"
"Review my backtest results and tell me if this is real edge"
"I want to build a mean reversion strategy for Solana"
```

---

## Output File Structure

```
algo-builder/
  hypotheses/     # One file per strategy idea (tracks trial count for DSR)
  signals/        # IC, ICIR, decay, regime results per signal
  strategies/     # Full strategy specs including TC budget
  results/        # Backtest + walk-forward + DSR results
  scripts/
    test_signal.py
    backtest.py
    walkforward.py
    fetch_data.py
```

---

## Key References

- Grinold & Kahn, *Active Portfolio Management* (1999)
- Lopez de Prado, *Advances in Financial Machine Learning* (2018)
- Bailey & Lopez de Prado, "The Deflated Sharpe Ratio" (2013)
- Almgren & Chriss, market impact modeling (2000)

---

## Install via ClawHub

```bash
clawhub install algo-builder
```
