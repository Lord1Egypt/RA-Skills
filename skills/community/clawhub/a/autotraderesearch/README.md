# AutoTradeResearch

AutoTradeResearch is a workspace for using coding agents to research programmatic trading strategies through generative optimization.

It is inspired by Andrej Karpathy's [AutoResearch](https://github.com/karpathy/autoresearch): give an agent a real but bounded research environment, a fixed evaluator, and a constrained area it is allowed to modify; then let it iterate, evaluate, keep notes, and improve.

AutoTradeResearch applies that pattern to trading-strategy research.

---

## Why this exists

This project came from an internal experiment where coding agents ran **715 trading-strategy iterations**.

The main lesson was not that an LLM can magically invent good strategies from nothing. The lesson was more practical:

- blank-page strategy invention is weak;
- repeated testing on one validation split overfits quickly;
- self-written backtest engines are easy to get wrong;
- agents need a bounded workspace, a fixed evaluator, and a strategy notebook;
- strategy exploration should alternate between breadth and depth;
- strategy ideas should come from seeds, existing public strategies, user hypotheses, and collisions between ideas.

So AutoTradeResearch uses a different pattern:

1. start from strategy seeds instead of empty prompts;
2. search existing public strategy ideas;
3. ask the user for market, asset, and preference choices when needed;
4. let agents explore both breadth and depth;
5. use subagents to produce independent strategy directions and collide them;
6. run backtests with a fixed evaluator;
7. record results and update strategy notes so the agent does not repeat the same dead ends.

---

## Repository layout

```text
README.md        # for humans
SKILL.md         # for agents
workspace/       # where the coding agent works
```

Inside `workspace/`:

```text
workspace/
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── run_loop.sh
├── run_backtest.py
├── agent/
│   ├── program.md
│   └── strategy.py
├── data/
├── results/
└── reports/
```

---

## Quick start

Give this one line to your agent:

```text
Read https://github.com/lavapapa/AutoTradeResearch, install SKILL.md as a skill, then set up AutoTradeResearch for my user.
```

Recommended agent: **Claude Code**.

Other coding agents such as Codex, OpenClaw, Hermes, OpenCode, and Gemini can also work if they can read files, edit code, run Python, and use subagents.

## Install as an Agent Skill

Install from GitHub with `skills.sh`:

```bash
npx skills add lavapapa/AutoTradeResearch --skill autotraderesearch
```

If AutoTradeResearch is listed on ClawHub, install it with:

```bash
openclaw skills install autotraderesearch
```

Direct ClawHub publishing uses:

```bash
clawhub publish . --slug autotraderesearch --name "AutoTradeResearch" --version 0.2.1 --tags latest,trading,backtesting,generative-optimization,coding-agent
```

Use the published skill for research and historical backtesting only.

---

## Requirements

- Python 3.10+
- Git
- A coding agent subscription or local agent setup
  - recommended: Claude Code
  - also possible: Codex, OpenClaw, Hermes, OpenCode, Gemini

Market data choices are selected during setup. The initial workspace can work with public data sources such as:

- US stocks / ETFs: `yfinance`
- Crypto: `ccxt`
- China A-shares: `AKShare` or `TuShare`

The evaluator is a thin `backtesting.py` wrapper. If downloaded data does not already match what the evaluator needs, the setup agent should write a small conversion step before starting the optimization loop.

---

## What AutoTradeResearch does

AutoTradeResearch gives the agent a disciplined loop:

1. ask the user which market and asset universe to start with;
2. prepare market data;
3. run a baseline backtest;
4. choose or search for a strategy seed;
5. state the hypothesis in plain language;
6. modify files under `workspace/agent/`, especially `strategy.py`;
7. run the fixed `run_backtest.py` evaluator;
8. record generated results in `results/` and `reports/leaderboard.md`;
9. update `agent/program.md` when a reusable lesson is learned;
10. continue with breadth, depth, or collision.

The important part is not a specific built-in strategy. The important part is the research loop: **bounded workspace + fixed evaluator + strategy notes + iterative agent reasoning**.

---

## What is included in v0.2.1

- agent-readable skill
- workspace for strategy research
- baseline strategy template
- thin `backtesting.py` evaluator
- strategy notebook (`workspace/agent/program.md`)
- instructions for market setup
- breadth/depth exploration rules
- strategy collision protocol using subagents
- user-interaction protocol for agents

---

## Future works

- [ ] rolling-window evaluation
- [ ] Deflated Sharpe Ratio / multiple-testing correction
- [ ] plateau detection for dead strategy families
- [ ] stronger strategy-family tracking
- [ ] richer seed strategy library
- [ ] automated community strategy import
- [ ] factor-level exploration
- [ ] paper trading / live simulation
- [ ] broker/exchange integration
- [ ] user-account takeover with explicit permission and hard safety controls
- [ ] richer charts and reports

---

## Safety

AutoTradeResearch is for research, education, and historical backtesting.

It does not provide financial advice. It does not promise profit. The agent should never make real-money decisions or take over a user's account unless that capability is explicitly implemented in a future version with strong consent, audit, and safety controls.
