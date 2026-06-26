# EKB Decision Algorithm — Methodology

## Overview

The EKB framework combines three mathematical tools into a unified decision-making system:

- **E** — Expected Value: Determines whether a decision is worth making at all
- **K** — Kelly Criterion: Determines optimal resource allocation
- **B** — Bayes' Theorem: Enables continuous judgment refinement

## The Four Dimensions

### 1D: Win Rate + Odds

The simplest level of analysis. What's the probability of success, and what's the payoff ratio?

Key insight: High win rate does not equal good decision. A 70% chance of gaining 1% vs 30% chance of losing 10% has an EV of -2.3%.

### 2D: Expected Value

```
EV = p × Gain - (1-p) × Loss
```

If EV is negative, stop here. No amount of clever position sizing or updating can fix a fundamentally bad bet.

### 3D: Kelly Criterion

```
f* = (p × b - q) / b
where p = win rate, q = 1-p, b = odds (gain/loss ratio)
```

Determines the optimal fraction of resources to allocate. In practice:
- Use **half-Kelly** when estimates are uncertain
- Use **quarter-Kelly** when venturing outside your circle of competence
- Never use full Kelly with leveraged positions

### 4D: Bayesian Updating

The 16-character mantra: **Respect priors. Stay open. Act first. Keep updating.**

Decision-making is iterative. Each new piece of information should update your probability estimates and potentially change your resource allocation.

## The 7-Question Self-Check

Before applying any math, run the decision through 7 quality-control questions:

1. Do I know what I actually want?
2. Am I fighting a battle I can win?
3. Am I willing to invest scarce resources?
4. Do I know what I can't afford to lose?
5. Do I have a retreat plan?
6. How will I optimize dynamically?
7. Will this make me a better person?

## The 8 Decision Traps

Common failure modes to screen for:

1. **AI Trap**: Outsourcing your decision authority entirely
2. **Rumination Trap**: Endless deliberation from lack of framework
3. **Delegation Trap**: Confusing delegation with abdication
4. **Inertia Trap**: Deciding by habit rather than analysis
5. **Success Trap**: Past wins becoming future constraints
6. **Certainty Trap**: Waiting for certainty that never comes
7. **Manipulation Trap**: Following someone else's designed path
8. **Bargain-Hunting Trap**: Penny-wise, pound-foolish

## The 5-Resource Flywheel

Every decision allocates five interconnected resources:

1. **Time** — Manage attention, not hours
2. **Money** — Seeds, not fruit
3. **Cognition** — Stay within competence
4. **Relationships** — You are the average of your 5 closest people
5. **Health** — The "1" that makes all other digits meaningful

Good decisions across these resources create a positive flywheel: better resources enable better decisions, which generate better resources.
