# Dead Reckoning for Fast-Moving Events

## The Problem This Solves

Data sources have lag:
- ACLED: 1–3 days behind
- ReliefWeb: days to weeks
- GDELT: 15 minutes (but only covers news that's been published)
- UN field reports: days to weeks

When events are moving faster than data — military offensives, coup attempts, acute crises — you need a methodology for reasoning about the **current state** from the **last known position + trajectory + elapsed time**.

Sailors called this dead reckoning: when you can't see landmarks, you calculate current position from last known position + heading + speed + time elapsed.

---

## The Dead Reckoning Formula

```
CURRENT STATE = Last Known State + (Trajectory × Time Elapsed) ± Disruption Events
```

**Components:**
- **Last Known State:** The most recent verified data point (ACLED event, field report, GDELT article with timestamp)
- **Trajectory:** The direction and rate of change at last known state (escalating/stable/de-escalating + speed)
- **Time Elapsed:** Hours/days since last known data
- **Disruption Events:** Verified events that would change trajectory (ceasefire announced, leader killed, major military event)

---

## Step-by-Step Process

### Step 1: Anchor on Last Known Position

State clearly and precisely:
> "The most recent verified data point is [source], [date/time], which showed [specific situation]."

Do not summarize loosely. Pin the exact anchor.

### Step 2: Assess Trajectory at Anchor Point

At the moment of the last known data:
- What direction was the situation moving? (escalating / stable / de-escalating)
- How fast? (rapidly / gradually / slowly)
- What was the dominant dynamic? (military advance / political negotiation / humanitarian deterioration / etc.)

### Step 3: Project Forward

Apply trajectory to elapsed time using historical rate comparisons:

| Situation Type | Typical Rate of Change |
|---------------|----------------------|
| Military offensive (mechanized) | 10–50 km/day in open terrain; 1–5 km/day in urban |
| Military offensive (infantry) | 1–10 km/day |
| Political negotiation | Days to weeks between rounds |
| Humanitarian deterioration | Days to weeks per IPC phase change |
| Protest mobilization | Hours to days |
| Coup consolidation | 24–72 hours decisive window |
| Economic deterioration | Weeks to months |

### Step 4: Apply Disruption Corrections

Check for any verified events since the anchor that would alter trajectory:
- New ceasefire / ceasefire collapse
- Leadership change
- Major military event (airstrike, encirclement, surrender)
- External power intervention
- Natural disaster

Each disruption requires recalculating trajectory from the new anchor.

### Step 5: State Current Estimate with Uncertainty Band

```
[CURRENT ESTIMATED STATE — DEAD RECKONING]
Based on: [anchor source + date]
Elapsed time: [X hours/days]
Projected trajectory: [direction + rate]
Disruption corrections: [list or none]
Estimated current state: [description]
Uncertainty band: NARROW / MODERATE / WIDE
Confidence: LOW (dead reckoning always lower than verified data)
Key observable that would confirm/deny estimate: [specific verifiable fact]
```

---

## Uncertainty Band Assessment

| Situation | Uncertainty Band | Why |
|-----------|-----------------|-----|
| Coup in progress (first 12h) | WIDE | Everything is fluid; outcomes binary |
| Active military offensive | MODERATE-WIDE | Front lines move; fog of war |
| Ongoing peace negotiations | MODERATE | Talks can collapse or accelerate unexpectedly |
| Humanitarian situation | NARROW-MODERATE | Deteriorates predictably; disruptions unusual |
| Slow-burn political crisis | NARROW | Structural dynamics don't change quickly |
| Economic crisis trajectory | NARROW | Economic indicators move slowly |

---

## Dead Reckoning for Different Conflict Phases

### Active Military Offensive

**Anchor:** Last confirmed front line position with timestamp

**Projection method:**
- Check historical rate of advance for this force in this terrain type
- Check whether advance was slowing or accelerating at anchor point
- Check for reported resupply/logistics constraints
- Check defender's reserve availability

**Typical error rate:** Front line position estimates using dead reckoning are typically off by 5–30% of the projected advance distance

**Verification trigger:** Satellite imagery, geo-tagged social media, journalist reporting from front

### Political Negotiation

**Anchor:** Last reported round of talks / last known position of each party

**Projection method:**
- Note whether parties were converging or diverging at anchor
- Check whether any deadlines are approaching (external pressure)
- Check whether mediator has signaled progress or impasse
- Estimate based on historical rate: comparable negotiations (list from historical-patterns.md)

### Coup Attempt

**Anchor:** Last confirmed information (which side holds key infrastructure)

**Projection method:**
- The 6-hour rule: if a coup hasn't consolidated within 6 hours, it is likely failing
- The 24-hour rule: if a coup hasn't won within 24 hours, the government has likely survived
- Key infrastructure control is determinative: presidential palace, state TV, military HQ, airport
- If any two of the four remain with government: coup likely fails

### Humanitarian Deterioration

**Anchor:** Last IPC phase classification with date

**Projection method:**
- Check what drove the deterioration (conflict disruption vs seasonal vs structural)
- Apply historical rate for similar contexts
- Check for harvest season, rainy season, aid corridor status changes

---

## Honest Uncertainty Statement

Every dead reckoning assessment must include:

> "This assessment uses dead reckoning methodology — estimating current state from last verified data point plus projected trajectory. It carries higher uncertainty than assessments based on current verified data. The key assumption is [X]. If [key observable] is confirmed, this estimate should be revised to [Y]."

---

## Integration with Main Workflow

Dead reckoning is triggered at Step 2 (Data Acquisition) when:
- Most recent ACLED data is > 48 hours old for a fast-moving situation
- GDELT shows continued coverage but no new field reports
- User is asking about current state during an active crisis

After completing dead reckoning, label the output section clearly:
```
[⚠️ DEAD RECKONING — Last verified data: DATE. Current state estimated, not confirmed.]
```

This ensures the reader understands the epistemic status of the assessment.
