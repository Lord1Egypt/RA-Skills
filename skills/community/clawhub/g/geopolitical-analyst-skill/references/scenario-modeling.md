# Scenario Simulation & Futures Modeling

## Purpose

Rather than predicting a single outcome, generate **three plausible futures** at 6-month and 12-month horizons:
- **Base case** (most likely path from current trajectory)
- **Upside case** (de-escalation, negotiation success, cooperation emerges)
- **Downside case** (escalation, spiral, conflict expands)

Each scenario includes: probability, trigger events, actor responses, economic/humanitarian effects.

**Why three scenarios:** Single-point forecasts fail. Decision-makers need to plan for multiple futures and identify which observable signals distinguish between them.

---

## Scenario Architecture

### Base Case
**Definition:** Current trajectory continues. Trend direction unchanged.

**Probability:** 40-55% (the modal outcome)

**Characteristics:**
- No major policy shifts
- No unexpected external shocks
- Actors continue existing strategies
- Previous trend continues (at similar pace)

**Key assumption:** "Things continue as they are"

### Upside Case
**Definition:** Unexpected positive development. De-escalation, negotiation breakthrough, cooperation emerges.

**Probability:** 15-30%

**Characteristics:**
- Leadership change or shift in strategy
- External mediation succeeds
- Cost of conflict becomes evident → policy shift
- Economic incentive to cooperate overcomes strategic tension
- Third party introduces new incentive structure

**Trigger examples:**
- Regime change (new leadership, different priorities)
- Economic shock that changes cost-benefit (commodity collapse, investor flight)
- Military stalemate → both sides open to negotiation
- New mediator with leverage (UN, regional power, economic bloc)
- Public pressure (election in democratic country, protest in authoritarian one)

### Downside Case
**Definition:** Current tensions escalate. Conflict expands, spiral dynamics activate.

**Probability:** 15-30%

**Characteristics:**
- Military incident becomes precedent
- Retaliation cycles strengthen commitment
- Third-party intervention (ally enters)
- Economic coercion triggers counter-coercion
- Miscalculation/accident triggers larger confrontation

**Trigger examples:**
- Military clash that's misinterpreted as prelude to attack
- Sponsor state provides advanced weapons → arms spiral
- Economic sanctions → counter-sanctions
- Atrocity allegation → retaliatory strikes
- Domestic pressure forces leader to take harder line

---

## Scenario Model Template

```markdown
## Scenario Analysis: [SITUATION] — 6-Month Horizon

### Base Case
**Probability:** [%]
**Narrative:** [2-3 sentences describing the most likely path]

**Key assumptions:**
1. [Assumption that must hold]
2. [Assumption that must hold]
3. [Assumption that must hold]

**Actor behavior:**
- [Actor 1]: [Most likely move]
- [Actor 2]: [Most likely move]
- [Actor 3]: [Most likely move]

**Observable milestones (early warning):**
- By Week 4: [What should happen if base case is unfolding?]
- By Week 8: [Next signal of base case?]
- By Week 12: [By this point, base case confirmed or denied?]

**Economic effects:**
- GDP impact: [None / slight / significant]
- Trade: [Status quo / minor disruption / major]
- Finance: [Stable / volatility / capital flight]

**Humanitarian effects:**
- Casualties: [None / limited / high]
- Displacement: [None / thousands / millions]
- Food security: [Stable / stressed / crisis]

---

### Upside Case (De-Escalation)
**Probability:** [%]
**Narrative:** [2-3 sentences describing the positive path]

**Trigger event needed:** [What would need to happen to shift to this scenario?]

**Most likely trigger:** [Which of the possible triggers is most probable?]

**Actor behavior in this scenario:**
- [Actor 1]: [What they do differently]
- [Actor 2]: [What they do differently]
- [Actor 3]: [What they do differently]

**Observable milestones (early warning this scenario is happening):**
- Week 1-2: [First sign of shift]
- Week 4-6: [Confirmation signal]
- Week 8-12: [Point of no return (too far toward cooperation to reverse)]

**Economic effects:**
- Sanctions lifted: [Yes / Partial / No]
- Trade restored: [Timeline]
- Finance: [Recovery signals]

**Humanitarian effects:**
- Ceasefire holds: [Probability / Duration]
- Reconstruction begins: [Timeline]

---

### Downside Case (Escalation)
**Probability:** [%]
**Narrative:** [2-3 sentences describing the escalatory path]

**Trigger event needed:** [What incident could tip the balance?]

**Most likely trigger:** [Which possible trigger is most probable?]

**Escalation chain:**
1. [Initial incident]: Probability [%]
2. [Response cycle]: Actor A → Actor B → Actor A
3. [Third-party entry?]: Probability [%]
4. [Point of no return?]: When does this become unstoppable?

**Actor behavior in this scenario:**
- [Actor 1]: [Hardened position]
- [Actor 2]: [Escalatory response]
- [Actor 3]: [Possible intervention]

**Observable milestones (early warning of escalation):**
- Week 1-2: [First danger signal]
- Week 4-6: [Commitment point]
- Week 8-12: [Escalation spiral activated?]

**Economic effects:**
- Market shock: [Size / Duration]
- Supply disruption: [What goods / regions affected]
- Recession risk: [Regional / Global / Minimal]

**Humanitarian effects:**
- Combat intensity: [Scale]
- Civilian casualties: [Estimate range]
- Displacement: [Scale]
- Economic collapse: [Regions affected]

---

## 12-Month Extension

For each scenario, extrapolate forward to 12 months:

**Base case at 12 months:** [Has situation stabilized? Deteriorated slowly?]

**Upside case at 12 months:** [Is peace holding? Who re-arms?]

**Downside case at 12 months:** [Has conflict expanded regionally? Leveled off?]

**Scenario divergence by 12 months:** [Are the three scenarios still plausible or has one been eliminated?]
```

---

## Key Probabilities to Include

### Conditional Probabilities
"If trigger event X occurs, what's the probability of outcome Y?"

Example:
- If military incident occurs: P(escalation) = 70%, P(contained) = 30%
- If new mediator enters: P(negotiation breakthrough) = 45%, P(talks fail) = 55%

### Updated Probabilities
After each major event, reassess:
- Has base case probability increased or decreased?
- Has a "black swan" event (previously low-probability) occurred?
- Should we shift to a different scenario as base case?

---

## Scenario Application in Decision-Making

### For Policy Makers
- **Contingency planning:** What resources/allies do we need for each scenario?
- **Red lines:** At what point do we shift strategy?
- **Window of opportunity:** When can we influence which scenario?

### For Risk Management
- **Early warning system:** Which observable milestones tell us which scenario is unfolding?
- **Decision triggers:** When do we commit to a response?
- **Reversibility:** Can we switch strategies if scenario changes?

### For Communication
- **Stakeholder alignment:** All parties understand the scenarios?
- **Public messaging:** Are we preparing populations for multiple futures?
- **Commitment credibility:** Do our stated policies match the scenarios we claim to expect?

---

## Integration with Main Workflow

**Triggered:** In Step 9 (Output), mandatory for FULL assessments

**Input data from earlier steps:**
- Actor capabilities (Step 5)
- Historical patterns (Step 6)
- Red team analysis (Step 8)

**Output:** 
- 3 scenarios × 2 time horizons = 6 detailed futures
- Probability confidence (high/medium/low)
- Observable divergence points (when do we know which scenario is unfolding?)

**Use case:** Decision-makers who need to plan for multiple futures, identify key decision points, and know what observable signals matter.
