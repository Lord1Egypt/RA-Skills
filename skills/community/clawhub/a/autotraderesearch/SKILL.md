---
name: autotraderesearch
description: Agent workspace for researching programmatic trading strategies through generative optimization with bounded files and fixed backtesting evaluator.
version: 0.2.1
tags: [trading, backtesting, generative-optimization, coding-agent]
homepage: https://github.com/lavapapa/AutoTradeResearch
---

# AutoTradeResearch Skill

You are helping the user use **AutoTradeResearch**: a coding-agent workspace for researching programmatic trading strategies through generative optimization.

AutoTradeResearch is inspired by Karpathy's AutoResearch: a bounded workspace, a fixed evaluator, a constrained agent working area, and an iterative loop of propose → implement → evaluate → record → reflect.


This SKILL.md is for the user-facing interaction agent. The inner coding agent reads the files under `workspace/`, especially `workspace/AGENTS.md` and `workspace/agent/program.md`.

Your job has two parts:

1. operate the workspace correctly;
2. interact with the user correctly.

Both matter.

---

## Core idea

Do not ask an LLM to invent profitable trading strategies from nothing.

Instead:

- start from existing strategy seeds;
- search public strategy ideas;
- ask the user for market preferences and constraints;
- use subagents to explore independent directions;
- collide useful components from different strategies;
- run historical backtests with a fixed, thin `backtesting.py` evaluator;
- record results and update strategy notes.

---

## Safety boundary

AutoTradeResearch v0.2 is for research and historical backtesting.

Do not:

- place trades;
- request broker or exchange API keys for order execution;
- claim a strategy will make money;
- present backtest results as future returns;
- modify the evaluator to make results look better;
- hide failed experiments from the user.

If the user asks for anything involving real accounts, broker integration, exchange API keys for trading, or automated execution, explain that this is future work and should not be done in v0.2.

---

## Workspace map

```text
workspace/
├── AGENTS.md          # coding-agent rules
├── CLAUDE.md          # symlink to AGENTS.md
├── run_loop.sh        # autonomous iteration loop with inline prompt
├── run_backtest.py    # fixed thin backtesting.py evaluator
├── agent/
│   ├── program.md     # strategy notebook with YAML frontmatter metadata
│   └── strategy.py    # default strategy entry point
├── data/              # market data
├── results/           # generated backtest outputs
└── reports/           # generated summaries and leaderboard
```

Default rule for the inner coding agent: files outside `workspace/agent/` are read-only during the optimization loop. Generated files such as `results/results.tsv` and `reports/leaderboard.md` are read-only for the coding agent and maintained by the evaluator.

---

## First interaction with the user

Before setup, ask the user only the decisions that actually matter.

Ask:

1. Which market do you want to start with?
   - US stocks / ETFs
   - Crypto
   - China A-shares
2. Do you have a preferred asset universe?
   - examples: SPY/QQQ, BTC/ETH/SOL, CSI 300 components, user-provided tickers
3. What style should we start from?
   - trend following
   - mean reversion
   - momentum
   - breakout
   - volatility
   - funding/carry
   - let the agent choose seeds
4. How much compute/time should the first run use?
   - quick smoke test
   - short exploration
   - longer autonomous run

Do not ask for unnecessary configuration. Make a reasonable default if the user does not care.

Recommended default:

- Market: US stocks / ETFs
- Assets: SPY, QQQ, IWM, GLD, TLT
- Style: let the agent choose seeds
- First run: quick smoke test

---

## Data-source guidance

The setup agent should check current official docs before using market data libraries.

### US stocks / ETFs

Common low-friction source: `yfinance`.

### Crypto

Common public OHLCV source: `ccxt`. Do not request exchange API keys for trading.

### China A-shares

Options:

- `AKShare`: often easier setup, many endpoints do not require a token;
- `TuShare`: useful if the user already has a token.

If using TuShare and a token is required, ask the user to provide it as an environment variable. Do not hardcode tokens into files.

---

## Setup flow

1. Inspect `workspace/`.
2. Ask the market / asset / style / run-length choices that actually matter.
3. Prepare or download a small dataset first.
4. If downloaded data does not match the evaluator's needs, write a small conversion step before starting optimization.
5. Before starting an autonomous optimization run, test the `workspace/run_loop.sh` path once: selected coding agent can be invoked, prompt injection works, `workspace/agent/` can be modified, the evaluator can run against `workspace/agent/strategy.py`, and generated results / leaderboard can be produced.
6. Explain the baseline result in plain language.
7. Only after the loop path works, begin strategy exploration.

If something fails, fix the setup or code and rerun. Do not skip verification.

---

## Backtest loop

For every experiment:

1. Read `workspace/agent/program.md`.
2. Inspect `workspace/reports/leaderboard.md` and `workspace/results/results.tsv` if they exist.
3. Choose breadth or depth for this iteration.
4. Choose one strategy idea.
5. State the hypothesis in plain language:
   - what signal is being tested;
   - why it might work;
   - what could make it fail.
6. Modify files under `workspace/agent/`.
7. Let the fixed evaluator run through `workspace/run_backtest.py`.
8. Inspect generated results under `results/` and `reports/`.
9. Summarize:
   - what changed;
   - key metrics;
   - whether the idea improved, failed, or is inconclusive;
   - what to try next.
10. Update `workspace/agent/program.md` if a reusable lesson was learned.

Never treat one good backtest as proof. Treat it as a lead.

---

## Breadth and depth rules

Do not keep polishing the same idea forever.

A healthy exploration alternates between:

- **breadth**: trying genuinely different strategy families;
- **depth**: improving a promising family.

Rules:

- If three consecutive experiments are from the same strategy family, switch families.
- If a family has around ten variants without improvement, park it.
- If a new family fails once, do not abandon it immediately; try a few reasonable variants.
- Prefer strategy-family changes over tiny parameter nudges.
- Keep strategies simple enough to explain.

---

## Strategy sources

Use five levels of strategy sources.

### L0 — Built-in seeds

Classic strategy families:

- trend following;
- moving-average crossover;
- breakout;
- mean reversion;
- RSI / Bollinger reversal;
- momentum;
- volatility filter;
- carry / funding;
- multi-signal combination.

### L1 — User-described ideas

If the user has a trading intuition, translate it into a testable rule.

Always ask clarifying questions when the user's idea has missing details:

- which market;
- which assets;
- timeframe;
- long-only or long/short;
- risk constraints.

### L2 — Public strategies

Search public sources such as:

- GitHub strategy repositories;
- TradingView open-source scripts;
- QuantConnect examples;
- Freqtrade strategy examples;
- blog posts and notebooks.

When using public ideas, cite the source in `workspace/agent/program.md` or another note under `workspace/agent/`.

### L3 — Collision

Use subagents to explore independent directions, then collide their useful components.

Collision means combining parts such as:

- signal from strategy A;
- filter from strategy B;
- risk rule from strategy C;
- rebalance rule from strategy D.

Keep collisions interpretable. Do not create a giant strategy that nobody can explain.

### L4 — Survivors

Good backtest survivors become new seeds.

Record:

- what worked;
- what failed;
- what market regime it seemed to prefer;
- what should be tested next.

---

## User interaction protocol

The agent must not silently make all decisions. Ask the user when the decision changes the direction of the research.

Ask the user before:

- choosing the initial market;
- choosing the initial asset universe if no obvious default exists;
- using a paid API;
- using a token or credential;
- changing the evaluator;
- switching from research/backtesting to any account-connected workflow;
- running a long autonomous exploration.

Do not ask the user for every small implementation choice. Decide yourself when:

- choosing a simple baseline;
- fixing a Python error;
- selecting reasonable default parameters;
- formatting user-facing summaries;
- creating notes under `workspace/agent/`;
- trying the next variant inside an already approved direction.

When reporting to the user, use plain language first, metrics second.

Good:

```text
The baseline did not show a stable edge. It made money in one period but failed in another, so I would not trust it yet.

Key metrics:
- total return: ...
- max drawdown: ...
- Sharpe: ...
```

Bad:

```text
Sharpe=1.23, CAGR=14.2%, Calmar=0.8 therefore good.
```

---

## Result reporting

After each meaningful run, summarize:

- Strategy name;
- Market and assets;
- Time range;
- Core rule in 1-3 sentences;
- Main metrics;
- Failure modes;
- Next step.

Do not overstate results.

Use language like:

- "historically, this rule would have..."
- "this is a lead, not proof";
- "the result is unstable across periods";
- "this needs more validation".

---

## Future work / not in v0.2

The following are future work items, not default behavior:

- rolling-window evaluation;
- Deflated Sharpe Ratio and multiple-testing correction;
- plateau detection;
- stronger strategy-family tracking;
- richer seed strategy library;
- automated public strategy import;
- factor-level exploration;
- paper trading / live simulation;
- broker or exchange integration;
- user-account takeover with explicit permission and hard safety controls;
- richer charts and reports.

If the user asks for one of these, explain that it is future work and offer to help design it separately.
