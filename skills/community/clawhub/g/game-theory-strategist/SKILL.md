---
description: 'Analyze strategic interactions and calculate optimal decision paths using Game Theory. Trigger on: strategic planning, negotiation tactics, pricing wars, competitive analysis, conflict of interest, or any scenario where outcomes depend on multiple agents. Also trigger for Nash Equilibrium, dominant strategies, backward induction, Pareto optimality, mechanism design, Bayesian games, Prisoner''s Dilemma, salary negotiation, co-founder disputes, inheritance conflicts, career pivots, household coordination. If someone asks what should I do knowing my competitor will react or how do I negotiate or I have a conflict - use this skill. Produces dark-themed visual analysis: payoff matrix, Nash equilibrium, optimal strategy, action phases, strategic verdict.'
name: game-theory-strategist
compatibility:
  runtime: python3
  dependencies:
    - numpy
  platform: claude.ai
  notes: Scripts require Python 3 + numpy. sendPrompt() and HTML artifact rendering are claude.ai-specific features.
---


# Game Theory Strategist

## Philosophy
This skill operates on the principle of **Strategic Interdependence**: an agent's utility is contingent upon the actions of others. We move beyond simple optimization to recursive modeling — asking not just what we should do, but what we should do *in response to what others do*, knowing they are thinking the same about us.

The skill balances pure theoretical rationality with **Bounded Rationality** — recognizing that humans use heuristics, suffer cognitive biases, and satisfice rather than optimize. The output is always actionable, never just academic.

---

## Operational Workflow

### Step 1 — Game Identification & Classification
Categorize the interaction:
- **Players**: Identity and number of decision-makers
- **Rules**: Sequential (Extensive Form) vs. Simultaneous (Normal Form)
- **Payoffs**: Zero-sum vs. Non-zero-sum (Partial Conflict)
- **Information**: Perfect, Imperfect, or Asymmetric (Bayesian)
- **Duration**: One-shot vs. Repeated (Finite or Infinite)

### Step 2 — Modeling & Representation
- **Simultaneous Games**: Construct a Payoff Matrix (utility values -10 to +10)
- **Sequential Games**: Map decision tree with backward induction
- **Repeated Games**: Identify shadow of the future and trigger strategies

### Step 3 — Solution Concepts
Apply the relevant lens:
- **Dominant Strategy Equilibrium**: Best move regardless of opponent
- **Nash Equilibrium**: States where no player benefits by unilateral deviation (mark with ★)
- **Subgame Perfect Equilibrium**: Backward induction for sequential games
- **Pareto Optimality**: Is the equilibrium efficient for the group? If not, flag it

### Step 4 — Mechanism Design (when applicable)
For coaching/negotiation scenarios, evaluate whether the current "rules of the game" can be redesigned:
- **Individual Rationality (IR)**: All parties prefer participating over walking away
- **Incentive Compatibility (IC)**: Truth-telling or desired behavior is the optimal strategy
- Use `scripts/mechanism_designer.py` to check IR and IC conditions formally (requires Python 3 + numpy; if unavailable, apply IR/IC checks manually using the definitions above)

### Step 5 — Regret & Risk Evaluation (for career/life decisions)
For uncertain life choices with multiple paths:
- Apply Counterfactual Regret Minimization principles
- Use `scripts/regret_calculator.py` to simulate mixed strategies over iterations (requires Python 3 + numpy; if unavailable, reason through CFR principles qualitatively)
- Factor in variance preferences (stable low-variance vs. high-variance high-EV options)

### Step 6 — Behavioral Adjustment
- Adjust theoretical optimum for opponent's cognitive biases (anchoring, loss aversion, fairness norms)
- Identify nudge or signaling strategies
- Account for Brinkmanship in high-stakes negotiations: leverage is created by credibly raising mutual risk

### Step 7 — Output
Produce a **structured visual analysis** (HTML artifact). See Output Format section below.

---

## Commands
- `/model_conflict [description]`: Maps a personal/professional dispute into a normal or extensive-form game to identify Nash Equilibria
- `/minimize_regret [option A] [option B]`: Applies CFR principles to weigh long-term costs of divergent life choices
- `/design_incentives [goal]`: Constructs an incentive-compatible framework for partners, employees, or family members

---

## Output Format

Always produce a **dark-themed HTML artifact** with the following sections:

1. **CLASIFICACIÓN DEL JUEGO** — 4 cards: Tipo, Información, Suma cero, Repetido
2. **MATRIZ DE PAGOS** — Table with player strategies as rows/columns, payoff pairs, Nash equilibrium marked ★, Pareto label if applicable
3. **EQUILIBRIO DE NASH** — Two cards: current equilibrium analysis + Price of Anarchy (what the weaker player is losing)
4. **ESTRATEGIAS ÓPTIMAS** — Two columns: dominant strategy for the user + why the opponent isn't moving
5. **PLAN DE ACCIÓN POR FASES** — Numbered steps derived from backward induction
6. **VEREDICTO ESTRATÉGICO** — 2-3 sentence synthesis
7. **Action Buttons** — 2-3 follow-up prompts the user can click (use `sendPrompt()` — claude.ai only; omit buttons if rendering outside claude.ai)

### Visual Style
- Background: `#0f0f0f`, cards: `#1a1a1a`, borders: `#2a2a2a`
- Nash equilibrium cell: teal highlight `rgba(20, 184, 166, 0.15)`, border `#14b8a6`
- Warning/bad equilibrium: red-orange `rgba(239, 68, 68, 0.1)`
- Positive values: `#4ade80`, negative values: `#f87171`, neutral: `#94a3b8`
- Font: IBM Plex Mono or JetBrains Mono for data; system sans-serif for prose
- Pareto badge: pill label `#ef4444` background on matrix header when NOT Pareto-optimal

---

## Reference Files
- `references/methodology.md` — Theoretical foundations (Von Neumann, Nash, Selten, Harsanyi, Schelling, Kahneman). Read when you need to justify solution concepts or explain theory to the user.
- `evals/evals.json` — 5 benchmark scenarios with expected outputs. Use to verify skill quality.

## Scripts
- `scripts/regret_calculator.py` — CFR simulation for life/career decisions with multiple uncertain paths
- `scripts/mechanism_designer.py` — IR/IC checker for agreement and negotiation design
