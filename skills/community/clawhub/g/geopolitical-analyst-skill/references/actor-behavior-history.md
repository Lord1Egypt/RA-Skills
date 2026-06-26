# Actor Behavior History & Pattern Tracking

## Why Past Behavior Predicts Future Behavior

The actor taxonomy classifies actors. **Behavior history predicts what they'll actually do.**

A state that has:
- Honored previous ceasefires is more likely to honor the next one
- Broken red lines and faced no consequences is more likely to break them again
- Used negotiations as delay tactics will probably do it again
- Escalated asymmetrically before will likely follow the same pattern

These patterns are more reliable predictors than stated intentions or ideology.

---

## Key Behavioral Patterns to Track

### Ceasefire Behavior

For any armed actor with ceasefire history:

| Pattern | Implication | Example |
|---------|------------|---------|
| Honors agreements, implements on schedule | Trustworthy counterpart; agreements have value | Hezbollah on Israel-Lebanon border (1991–2006) |
| Honors agreements but uses violation as political signal | Calculated signaler; violations mean something | Iran (JCPOA compliance pre-2018 withdrawal) |
| Chronic violator with denials | Agreements are theater; low commitment | Various armed groups in Sahel |
| Escalates through "gray zone" violations | Uses negotiation time to rearm/reposition | Russia (Minsk II) |
| Collapses abruptly when circumstances change | Opportunistic actor; no ideological commitment | Factional groups in fragmented conflicts |

**Tracking method:**
- For each ceasefire: record major violation events with date, nature, magnitude, response
- Calculate violation rate: (violations per month) × (ceasefire duration)
- Note whether violations escalate, plateau, or decline before collapse
- Compare pattern to this actor's historical baseline

### Negotiation Behavior

Watch for these patterns across multiple negotiations:

**Delay tactic user:**
- Makes concessions only at final moment
- Introduces new demands at last minute
- Walks away from talks, returns with higher demands
- Uses talks to buy time for military buildup

**Genuine negotiator:**
- Makes incremental concessions during talks
- Moves redlines predictably in response to counterpart movement
- Follows through on pre-agreement commitments
- Uses back-channels to test positions before public negotiation

**Spoiler (negotiation rejector):**
- Refuses to negotiate or attends only for legitimacy
- Makes demands known to be unacceptable to counterpart
- Uses negotiation failure to justify escalation
- Has stated publicly or through proxies that compromise is impossible

### Red Line Behavior

Actors with track records of setting and maintaining red lines are more credible when they set new ones.

**Pattern tracking:**
- Actor sets red line X
- Opponent violates it
- Actor's response: escalates / accepts violation without response / responds indirectly
- Outcome: Red line maintained / Red line abandoned

**Credibility calculation:**
- Times red line was maintained: _
- Times red line was abandoned: _
- Ratio: _ / _
- Credibility assessment: HIGH (>75% maintained) / MEDIUM (50–75%) / LOW (<50%)

When an actor sets a new red line, reference the historical ratio: "Actor has maintained X% of previously stated red lines; credibility assessment: [HIGH/MEDIUM/LOW]."

---

## Actor History Profiles (Template)

For major recurring actors in your region of focus, maintain a running profile:

```markdown
## [ACTOR NAME]

### Ceasefire Track Record
- [Ceasefire agreement]: Honored / Violated / Ambiguous
- Violation rate: X violations per month
- Pattern: [escalating / stable / declining]
- Overall reliability: [HIGH / MEDIUM / LOW]

### Negotiation Track Record
- Style: [delay tactic / genuine / spoiler]
- Pattern: [list 2–3 recent negotiations]
- Outcome reliability: Follows through / Frequently reneges

### Red Line Track Record
- Total red lines set (past 5 years): X
- Maintained: Y
- Abandoned: Z
- Credibility ratio: Y/X

### Military Behavior
- Escalation pattern: [rapid / cautious / erratic]
- Preferred tactics: [list 2–3]
- Logistics capacity: [strong / adequate / weak]
- Morale/cohesion: [stable / fragmented / improving]

### Alliance Behavior
- Patron relationships: [list current patrons]
- Historical loyalty: [loyal / transactional / opportunistic]
- Signal of shifting allegiance: [early warnings, e.g., reduced patron military visits, increased meetings with rival patron]

### Previous Assessments
[Link to 3–5 recent assessments of this actor; note what was predicted vs. actual outcome]
```

---

## Systemic Actor Databases (Free, Open-Source)

| Database | Coverage | Quality | Update Frequency |
|----------|----------|---------|-----------------|
| ACLED | Armed groups, state forces, militias worldwide | High | Daily |
| SIPRI Arms Transfers | State military procurement patterns | High | Annual |
| UCDP Battle Deaths Database | Armed conflict data | High | Annual |
| IISS Military Balance | State military capabilities, doctrine | High | Annual |
| CSIS Transnational Crime Data | Criminal organization networks | Medium | Variable |
| Global Terrorism Database (GTD) | Terrorist attacks, groups | High | Annual |
| Armed Groups 500 | Non-state armed group database | Medium | As updated |

---

## Escalation Pattern Recognition

Track whether an actor is **escalating** or **de-escalating** before each major move:

**Pre-escalation indicators:**
- Increased rhetoric intensity in preceding weeks
- Military mobilization (troop movements, equipment movement)
- Reduced diplomatic contact / hardened diplomatic tone
- Restrictions on civilian movement (internal preparation)
- Historical precedent: when this actor escalated before, what preceded it?

**Pre-de-escalation indicators:**
- Increased diplomatic contact / softened rhetoric
- Military personnel being rotated to rear areas
- Talks scheduled / ceasefire proposals initiated
- Civilian movement restrictions eased
- Historical precedent: when this actor de-escalated before, what preceded it?

**Key insight:** Actors rarely escalate without observable preparation. Sudden escalations that appear "out of nowhere" usually meant the analyst missed the preceding signals.

---

## Using Behavior History in Assessments

In FULL assessments, when an actor's behavior is relevant, include:

```markdown
### [ACTOR] Behavioral Assessment

**Ceasefire reliability:** [HIGH/MEDIUM/LOW] — historically [% maintained]
**Negotiation pattern:** [style] — last negotiation [outcome/date]
**Current escalation trajectory:** [escalating/stable/de-escalating] based on:
  - [specific observable 1]
  - [specific observable 2]
**Credibility of current red line:** [HIGH/MEDIUM/LOW] vs. actor's historical ratio
**Probability of following stated policy:** [HIGH/MEDIUM/LOW]
```

This grounds the assessment in evidence rather than rhetoric.
