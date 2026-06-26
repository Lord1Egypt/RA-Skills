# Technical Reference: Game Theory Methodologies

## Table of Contents
1. Mechanism Design & Incentive Alignment
2. Counterfactual Regret Minimization (CFR)
3. Behavioral Game Theory & Bounded Rationality
4. The Price of Anarchy (PoA)
5. Brinkmanship & Dynamic Crises
6. Key Theorists

---

## 1. Mechanism Design & Incentive Alignment

Mechanism design is the science of designing the rules of a game to achieve a specific outcome, even when participants are self-interested. In personal coaching, this translates to setting up boundaries, contracts, or relationship dynamics where individuals have an incentive to behave as intended.

- **Individual Rationality (IR):** Participating in the agreement is better than the outside option (BATNA). If IR fails, the agent will walk away.
- **Incentive Compatibility (IC):** Acting truthfully or cooperatively is the dominant strategy. If IC fails, the agent has a rational reason to defect or misrepresent.
- **Revelation Principle:** Any equilibrium outcome of an arbitrary mechanism can be replicated by an incentive-compatible direct mechanism. Implication: you can always redesign the game so truth-telling is optimal without loss of generality.
- **Vickrey-Clarke-Groves (VCG):** A class of mechanisms that achieve IC in multi-player settings by making each agent pay the social cost of their presence.

**Practical application:** When a relationship/agreement is failing, check IR and IC first. Most chronic conflicts are IC failures — one party has an incentive to shirk because defection is costless. Fix: add monitoring, vesting cliffs, performance milestones, or credible penalties.

---

## 2. Counterfactual Regret Minimization (CFR)

CFR is an iterative learning algorithm for finding Nash Equilibria in imperfect-information games. It works by repeatedly simulating play and adjusting strategy to minimize the regret of not having played differently.

**Regret** = (payoff of best action in hindsight) − (payoff of action actually taken)

CFR guarantees convergence to a Nash Equilibrium in two-player zero-sum games. In n-player or non-zero-sum games it finds correlated or coarse correlated equilibria.

**Application to life decisions:**
- Model the decision as a repeated game against an uncertain "environment"
- Each iteration = a simulated life period with random utility draws
- After N iterations, the average strategy weights are the optimal hedge
- High-variance options (Start Business) can dominate in expected value but lose in regret-minimized mixed strategy when variance is high

**See:** `scripts/regret_calculator.py` for implementation.

---

## 3. Behavioral Game Theory & Bounded Rationality

Classical game theory assumes perfect rationality and common knowledge of rationality. Behavioral GT relaxes this:

- **Bounded Rationality (Simon, 1955):** Agents have limited information, limited computation, and limited time. They satisfice (find "good enough" solutions) rather than optimize.
- **Level-k Thinking:** Level-0 plays randomly; Level-1 best-responds to Level-0; Level-2 best-responds to Level-1. Most humans play Level-1 or Level-2.
- **Inequity Aversion (Fehr-Schmidt):** People reject unfair offers even at personal cost (Ultimatum Game). Rational by social norm enforcement, irrational by classical theory.
- **Loss Aversion (Kahneman-Tversky):** Losses loom ~2x larger than equivalent gains. Exploit this in negotiations by framing your offer as preventing a loss, not delivering a gain.
- **Anchoring:** First number stated in a negotiation disproportionately influences the final outcome. Go first with a high anchor when you have information advantages.
- **Nudges & Boosts (Thaler, Sunstein):** Nudges preserve autonomy while steering choices via defaults and framing. Boosts improve decision competence directly. Both are valid coaching tools.

---

## 4. The Price of Anarchy (PoA)

The Price of Anarchy measures how much social welfare degrades when agents act selfishly versus cooperating optimally.

PoA = (Social cost of worst Nash Equilibrium) / (Social cost of optimal centralized solution)

- PoA = 1.0: Selfish behavior is socially optimal (rare)
- PoA = 2.0: Selfishness causes 2x the social cost of cooperation
- Braess's Paradox: Adding capacity to a network can *increase* total congestion — the social optimum requires coordinated restraint

**Application:** In household, team, or co-founder settings, identify the current Nash and compare it to the Pareto frontier. The gap is the PoA. Coaching intervention = design a coordination mechanism that closes this gap.

---

## 5. Brinkmanship & Dynamic Crises

Derived from Schelling's analysis of the Cuban Missile Crisis and nuclear deterrence.

- **Brinkmanship:** A "competition in risk-taking." Leverage is created not by making a direct threat but by taking steps that credibly raise the probability of mutual disaster.
- **The Threat That Leaves Something to Chance:** Pure threats are often not credible. A threat that involves genuine shared risk is more believable — and therefore more effective.
- **Commitment Devices:** Burn bridges (publicly, irreversibly) to make threats credible. Odysseus tied to the mast; Cortés burning his ships.
- **Focal Points (Schelling Points):** In coordination games without communication, people gravitate toward salient, "natural" solutions. Useful when designing agreements — make the fair/efficient solution the obvious Schelling point.

**Application to negotiation:** Don't just threaten to leave. Actually activate the alternative (get the competing offer, file the paperwork, post the listing). This transforms the threat from cheap talk to credible commitment and shifts the Nash Equilibrium.

---

## 6. Key Theorists

| Theorist | Contribution |
|---|---|
| John von Neumann | Minimax theorem, normal/extensive form games |
| John Nash | Nash Equilibrium, bargaining solution |
| Reinhard Selten | Subgame Perfect Equilibrium, trembling-hand perfection |
| John Harsanyi | Bayesian games, incomplete information |
| Thomas Schelling | Focal points, brinkmanship, commitment devices |
| Roger Myerson | Mechanism design, revelation principle |
| William Vickrey | Incentive-compatible auctions |
| Daniel Kahneman | Prospect theory, cognitive biases in decisions |
| Herbert Simon | Bounded rationality, satisficing |
| Ariel Rubinstein | Bargaining theory, alternating-offers model |
