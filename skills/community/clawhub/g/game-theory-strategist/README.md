# game-theory-strategist

A skill for Claude that applies game theory frameworks to real decisions — negotiations, conflicts, career pivots, co-founder disputes, household coordination problems.

---

## What it does

When you describe a situation involving another person or genuine uncertainty, the skill:

1. Classifies the type of game (sequential vs simultaneous, symmetric vs asymmetric information, one-shot vs repeated)
2. Builds a payoff matrix with both players' utilities (-10 to +10 scale)
3. Identifies the Nash Equilibrium — the trap you're currently in
4. Flags if the equilibrium is Pareto-suboptimal (i.e., both of you could do better)
5. Derives a dominant strategy and an action plan via backward induction
6. Delivers a strategic verdict

Output is a dark-themed visual analysis rendered directly in Claude.ai.

---

## What it does NOT do

- The payoff matrices are **qualitative approximations**, not cardinal utility measurements. They are illustrative, not formally rigorous. A game theorist would not publish them.
- The CFR script (`scripts/regret_calculator.py`) is a **simplified regret matching simulation** over sampled utilities — not a full CFR implementation over an extensive-form game tree. It is useful for life/career decisions under uncertainty, not for poker or formal mechanism proofs.
- The IR/IC checker (`scripts/mechanism_designer.py`) assumes **linear, comparable utilities** across agents — a strong simplification that rarely holds in practice.
- The skill does **not compute mixed-strategy Nash Equilibria** mathematically. It identifies pure strategy Nash only.
- It does **not replace legal, financial, or professional advice**.

---

## Files

```
game-theory-strategist/
├── SKILL.md                      — skill instructions for Claude
├── README.md                     — this file
├── scripts/
│   ├── regret_calculator.py      — CFR-inspired life decision simulator
│   └── mechanism_designer.py     — IR/IC checker for agreements
├── references/
│   └── methodology.md            — theoretical foundations (Nash, Schelling, Kahneman...)
└── evals/
    └── evals.json                — 5 benchmark scenarios with expected outputs
```

---

## Eval results (5/5 pass, avg 93/100)

| Scenario | Score |
|---|---|
| Salary negotiation under incomplete information | 92 |
| Family inheritance ultimatum game | 95 |
| Career pivot — CFR regret minimization | 88 |
| Co-founder Prisoner's Dilemma | 96 |
| Household Tragedy of the Commons | 94 |

The career pivot scenario scores lowest (88) because it is a decision against nature — no strategic opponent — so no payoff matrix applies. The skill handles it correctly via CFR but the transition is implicit, not explicit.

---

## Installation

Drop the `game-theory-strategist/` folder into your Claude skills directory and reload.

---

## Good test cases

- Freelancer chasing a $2,400 unpaid invoice from a client who can leave a public bad review
- Negotiating a rent increase with a landlord after 3 years of on-time payments

---

## Known limitations worth fixing

- Mixed-strategy Nash (requires linear programming — nashpy or similar)
- Formal PoA calculation (currently narrative only)
- Explicit warning in output when matrix utilities are qualitative estimates
- n-player games beyond 2x2

---

Built with Claude Sonnet 4. Part of the OpenClaw skill library.
