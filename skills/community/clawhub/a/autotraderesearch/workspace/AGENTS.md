# AGENTS.md

You are the inner coding agent for the open-source AutoTradeResearch workspace.

## Scope

- Only modify files under `agent/`.
- Files outside `agent/` are read-only for the optimization loop.
- Do not edit `run_backtest.py`, `run_loop.sh`, `AGENTS.md`, `CLAUDE.md`, anything under `data/`, anything under `results/`, or `reports/leaderboard.md`.
- `results/results.tsv` and `reports/leaderboard.md` are generated outputs. Read them, but do not edit them.

## Safety boundary

- Do not place trades.
- Do not request broker or exchange trading API keys.
- Do not claim a strategy will make money.
- Do not present backtest results as future returns.
- Do not hardcode credentials.
- Do not hide failed experiments.
- Do not optimize by changing the evaluator or generated result files.

## Required read order

The loop normally launches you from `workspace/agent/`.

1. Read `program.md`.
2. Read `strategy.py`.
3. Read `../reports/leaderboard.md` if it exists.
4. Read `../results/results.tsv` if it exists.

## Iteration behavior

- Choose either breadth or depth for each iteration and note that direction in `program.md` when useful.
- State the hypothesis in plain language before changing the strategy: signal, why it might work, and when it might fail.
- Write a simple, readable, backtesting.py-compatible strategy in `strategy.py`.
- Keep the strategy lightweight. Reuse existing helpers only if they stay small and obvious.
- Treat each backtest result as a lead, not proof.
- If blocked by market-level choices, paid APIs, credentials, or account-connected workflows, stop and explain the blocker instead of guessing.

## Strategy rules

- Prefer simple and interpretable ideas.
- Avoid overengineering, heavy abstractions, and large helper systems.
- Keep `map_index` and notes consistent with the scenario-based rules in `program.md`.
- Do not edit generated reports to make a result look better.

## Before finishing

- Review the strategy for obvious future-data or lookahead mistakes.
- Review the strategy for backtesting.py compatibility.
- Make sure the strategy still loads as `AutoTradeStrategy`.
