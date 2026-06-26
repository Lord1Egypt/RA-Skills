# decision-algorithm

> *"Major life decisions shouldn't rely on momentary passion — they need a repeatable decision algorithm."*

Based on 20 years of decision research, fusing **Expected Value + Kelly Criterion + Bayesian Theorem (EKB Framework)** to help you build a self-correcting decision loop.

## Install

```bash
# skills.sh
npx skills add truenorth-lj/decision-algorithm-skill

# ClawHub
clawhub install truenorth-lj/decision-algorithm-skill

# Manual (Claude Code)
cp -r . ~/.claude/skills/decision-algorithm
```

## Directory Structure

```
decision-algorithm-skill/
├── SKILL.md                    # Core skill entry point (self-contained EKB framework)
├── meta.json                   # Skill metadata
├── tools/
│   └── decision_calculator.py  # EV & Kelly Criterion CLI calculator
├── docs/
│   └── methodology.md          # Framework methodology deep-dive
├── README.md
└── LICENSE
```

## Usage

Once installed, just ask naturally:

```
Should I quit my job to start a business?
Is this investment worth making?
I'm torn about whether to break up.
How risky is this opportunity?
How should I allocate my capital?
I feel lost about my life direction.
```

### Analysis Depth

- **Quick judgment**: "Help me quickly assess this decision" — 7 Questions + EV sign
- **Deep analysis**: "Help me analyze this in detail" — Full 8-step workflow + 5-Resource Audit
- **Specific framework**: "Use Kelly to calculate how much I should invest" — Single tool focus
- **Life planning**: "Help me plan my direction" — Personal Evolution Formula + Resource Audit

### Calculator Tool

```bash
# Expected Value — Is it worth doing?
python3 tools/decision_calculator.py --ev -p 0.3 -g 100000 -l 20000

# Kelly Criterion — How much to bet?
python3 tools/decision_calculator.py --kelly -p 0.4 -o 3

# Full analysis — All metrics at once
python3 tools/decision_calculator.py --full -p 0.3 -g 100000 -l 20000 --capital 500000

# Conservative mode (half-Kelly for uncertain estimates)
python3 tools/decision_calculator.py --full -p 0.3 -g 100000 -l 20000 --capital 500000 --conservative
```

## Core Framework

| Dimension | Tool | Problem Solved |
|-----------|------|---------------|
| 1D | Win Rate + Odds | What's the probability and payoff? |
| 2D | Expected Value | Is this decision worth making? |
| 3D | Kelly Criterion | How much resource to allocate? |
| 4D | Bayesian Updating | How to adjust with new information? |

## Key Principles

- **Only do things with positive expected value**
- **Never invest what you can't afford to lose**
- **Act first, keep updating** (Bayesian mantra)
- **Don't test human nature — set rules in advance**
- **Circle of competence > intelligence**
- **Stay at the table**

## Attribution

English translation and adaptation of the [EKB Decision Algorithm](https://github.com/caomz/decision-algorithm) framework, originally based on Lao Yu's decision research.

## License

MIT
