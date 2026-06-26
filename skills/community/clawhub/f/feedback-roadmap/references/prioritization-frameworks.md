# Prioritization Frameworks

Pick one primary framework per roadmap and document the inputs. Mixing frameworks mid-list makes scores incomparable. Below: the formula, a worked ecommerce example, and when to reach for each.

---

## 1. RICE — Reach × Impact × Confidence ÷ Effort

The workhorse for ecommerce roadmaps because every factor maps to data you already have.

**Formula:**
```
RICE score = (Reach × Impact × Confidence) ÷ Effort
```

| Factor | Meaning | Suggested scale |
| --- | --- | --- |
| **Reach** | How many customers affected per time period (quarter is common) | Actual count (e.g. 1,400 buyers/qtr) |
| **Impact** | How much it moves the needle per affected customer | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| **Confidence** | How sure you are of the reach/impact estimates | 1.0 = high (hard data), 0.8 = medium, 0.5 = low |
| **Effort** | Total work to ship | Person-weeks (or person-months — be consistent) |

**Worked example** — adding a bulb-inclusion module to a PDP:
- Reach = 1,400 affected buyers/qtr
- Impact = 2 (high; directly cuts the top return reason)
- Confidence = 0.9 (return-code data is solid)
- Effort = 1 person-week
- **RICE = (1,400 × 2 × 0.9) ÷ 1 = 2,520**

Compare to a wishlist feature: (300 × 0.5 × 0.6) ÷ 4 = **22.5**. The 100x gap makes the call obvious and defensible.

**Use RICE when:** you have decent reach data (traffic, order counts, mention frequency), effort estimates from the people who'd build it, and stakeholders who want an auditable, single-number ranking. **Watch out:** Reach can swamp Impact — a tiny-reach Blocker may need a manual override or a separate urgency gate (see §4).

---

## 2. ICE — Impact × Confidence × Ease

A lighter, faster cousin of RICE. Drops explicit reach and uses Ease (inverse of effort) so all three factors point the same direction (higher = better).

**Formula:**
```
ICE score = Impact × Confidence × Ease     (each scored 1-10)
```

**Worked example** — "free returns for loyalty members":
- Impact = 7
- Confidence = 6
- Ease = 4 (operationally costly)
- **ICE = 7 × 6 × 4 = 168** (out of a max 1,000)

**Use ICE when:** you're triaging many ideas quickly, reach is hard to estimate, or you're in an early/scrappy stage. **Watch out:** scores are subjective and inflate easily — anchor each 1-10 score to a written definition, and have two people score independently to reduce bias.

---

## 3. Impact / Effort 2x2

A visual sort, not a precise score. Plot each item on two axes and read off the quadrant.

```
            High Impact
                 |
   Big Bets      |   Quick Wins   <- do these first
                 |
-----------------+------------------ 
   Time Sinks    |   Fill-ins
   (avoid)       |   (maybe, if idle)
                 |
            Low Impact
        High Effort <---- Low Effort
```

- **Quick Wins** (high impact, low effort): do now.
- **Big Bets** (high impact, high effort): plan and resource deliberately.
- **Fill-ins** (low impact, low effort): batch into spare cycles.
- **Time Sinks** (low impact, high effort): drop or park.

**Use the 2x2 when:** communicating to non-analytical stakeholders or doing a fast first-pass sort before scoring. **Watch out:** no urgency dimension and it hides ties within a quadrant — pair it with a scored framework for the final ranking.

---

## 4. Weighted Urgency Scoring

When a deadline, escalating trend, or risk (legal, safety, churn, seasonal) must explicitly influence rank, make urgency a weighted factor instead of an afterthought.

**Formula:**
```
Score = (Impact × wI) + (Urgency × wU) + (EffortInverse × wE)
where wI + wU + wE = 1.0,  each factor on a 1-5 scale,
and EffortInverse = (maxScale + 1) − Effort   (so low effort scores high)
```

**Worked example** — fixing an Apple Pay card rejection right before peak season. Weights: Impact 0.5, Urgency 0.3, Effort 0.2.
- Impact = 4, Urgency = 5, Effort = 2 → EffortInverse = (6 − 2) = 4
- **Score = (4×0.5) + (5×0.3) + (4×0.2) = 2.0 + 1.5 + 0.8 = 4.3**

**Anchor urgency to objective triggers, not feelings:**

| Urgency | Trigger examples |
| --- | --- |
| 5 | Safety/legal risk, active revenue leak, hard seasonal deadline this cycle |
| 4 | Sharp rising trend, churn driver, deadline next cycle |
| 3 | Steady recurring friction, no deadline |
| 2 | Mild, intermittent |
| 1 | No time pressure |

**Use weighted urgency when:** timing genuinely changes the answer (peak season, a compliance date, a competitor move). **Watch out:** document the weights up front and don't re-tune them mid-ranking to get a preferred result.

---

## 5. Kano-Style Must-Have vs Delighter Lens

A qualitative classifier to run *alongside* a scoring framework. It answers "what kind of value is this?" not "what's the number?"

| Category | Definition | Roadmap implication |
| --- | --- | --- |
| **Must-have (Basic)** | Absence causes anger; presence is merely expected | Fix first — these are table stakes (working checkout, accurate sizing, items arriving intact) |
| **Performance (Linear)** | More is better; satisfaction scales with quality | Invest proportionally to ROI (faster shipping, better fit accuracy) |
| **Delighter (Exciter)** | Unexpected; absence isn't missed, presence wows | Do after must-haves are solid (surprise samples, personalization) |
| **Indifferent** | Customers don't care either way | Deprioritize or drop |

**Worked example:** A broken Apple Pay flow is a **Must-have** failure — no amount of delighters compensates. A wishlist feature is a **Delighter** at best. Even if a scoring framework put them close, the Kano lens says fix the must-have first. Rule of thumb: **never trade a broken must-have for a delighter**, regardless of raw score.

**Use Kano when:** sequencing across categories or sanity-checking a score-driven list. **Watch out:** categories drift — yesterday's delighter (free 2-day shipping) becomes today's must-have.

---

## Choosing fast

- Lots of ideas, need a quick cut → **Impact/Effort 2x2** then **ICE**.
- Solid data, want an auditable number → **RICE**.
- Timing or risk changes the answer → **Weighted Urgency**.
- Always, as a final gate → **Kano**: have you fixed the must-haves before chasing delighters?
