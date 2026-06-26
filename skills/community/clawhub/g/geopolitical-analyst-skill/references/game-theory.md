# Game Theory & Strategic Interaction

## Purpose

Game theory asks: **Given the incentives, what's rational?**

Most analysis asks "what will actor X do?" Game theory asks "what SHOULD actor X do given:
- Their goals
- Their costs/benefits
- Their opponent's probable response
- Uncertainty about the future"

This forces rigor. It reveals:
- Why apparently irrational actors are actually rational
- Why conflicts persist even when both sides lose
- When compromise is possible vs impossible
- Who has leverage and why

---

## Core Games in Geopolitics

### Game 1: Prisoner's Dilemma (PD)
**Setup:** Two actors; each has two choices: Cooperate or Defect

**Payoff matrix:**
```
              Actor B: Cooperate  |  Actor B: Defect
Actor A: Cooperate     (3,3)      |      (0,5)
Actor A: Defect        (5,0)      |      (1,1)
```

*Higher number = better payoff*

**Rational outcome:** Both defect → (1,1) = worst outcome for both

**Why:** Defecting is always better for each actor individually, even though both cooperating is better for both together

**Real-world example:** Arms race
- Cooperate = both limit weapons → both safe, cheaper
- Defect = build weapons → you're stronger, but opponent responds
- Rational = both build (costly, but you're not left behind)
- Result = expensive arms race that benefits neither

**Escape route:** Repeated interactions (play again next round) → reputation becomes valuable → cooperation becomes rational

---

### Game 2: Coordination Game
**Setup:** Both actors want the same outcome but disagree on how to get it

**Payoff matrix:**
```
              Actor B: Plan A  |  Actor B: Plan B
Actor A: Plan A     (5,5)      |      (0,0)
Actor A: Plan B     (0,0)      |      (5,5)
```

**Rational outcome:** Multiple equilibria — either (Plan A, Plan A) or (Plan B, Plan B) works

**The problem:** Actors must coordinate on the same plan

**Real-world example:** Currency peg or trade standard
- Both benefit if everyone uses the same standard
- Both lose if they use different standards
- But which standard? Whoever moves first determines it

**Escape route:** Focal points (natural coordination points) or agreed rules

---

### Game 3: Battle of the Sexes (BoS)
**Setup:** Two actors want different outcomes; both want to stay together

**Payoff matrix:**
```
              B: Opera  |  B: Football
A: Opera      (3,2)    |    (0,0)
A: Football   (0,0)    |    (2,3)
```

**Rational outcome:** Uncertain (multiple equilibria) — depends on bargaining power

**Real-world example:** Trade agreement structure
- Both want agreement but disagree on terms
- Disagreement leaves both worse off
- Whoever has more leverage gets their preferred terms

---

### Game 4: Chicken / Hawk-Dove
**Setup:** Two actors in confrontation; backing down loses face

**Payoff matrix:**
```
              B: Aggressive  |  B: Backs Down
A: Aggressive    (-10,-10)   |    (5,0)
A: Backs Down    (0,5)       |    (2,2)
```

**Rational outcome:** Mutually aggressive = disaster, but backing down is worse (politically)

**The problem:** Commitment to not backing down becomes rational even though mutual backing down is better

**Real-world example:** Territorial dispute
- Aggressive posturing makes sense (shows strength)
- But if both are aggressive → war
- Backing down costs domestic legitimacy
- Rational outcome: One side backs down, but which one?

**Escape route:** De-escalation mechanism (save face while backing down) or third-party mediation

---

## Strategic Analysis Framework

For any conflict, identify the game being played:

### Step 1: List the Options
```
Actor A can: [Option 1, Option 2, Option 3]
Actor B can: [Option 1, Option 2, Option 3]
```

### Step 2: Assign Payoffs
Payoff = Actor's goals achieved (0-10 scale)
```
A: Wants [X, Y, Z] — payoff is achievement of each
B: Wants [X, Y, Z] — payoff is achievement of each
```

### Step 3: Build Payoff Matrix
```
          B: Option 1  |  B: Option 2  |  B: Option 3
A: Opt 1    (a,b)     |     (c,d)     |     (e,f)
A: Opt 2    (g,h)     |     (i,j)     |     (k,l)
A: Opt 3    (m,n)     |     (o,p)     |     (q,r)
```

### Step 4: Find Nash Equilibrium
Nash Equilibrium = outcome where neither actor wants to unilaterally deviate

**How to find it:**
- For each of A's choices, what's B's best response?
- For each of B's choices, what's A's best response?
- Where do the best responses intersect? That's Nash Equilibrium

### Step 5: Assess Stability
- Stable: Actors will stay at Nash Equilibrium naturally
- Unstable: Actors want to deviate if they can
- Multiple equilibria: Which will actors coordinate on?

---

## Common Geopolitical Game Types

| Game | Setup | Key Dynamic | Escape Route |
|------|-------|-------------|-------------|
| **Prisoner's Dilemma** | Both prefer mutual cooperation but individually prefer defection | Costly arms race or competition | Reputation/repeated interaction |
| **Coordination** | Both want to cooperate but disagree on terms | Need to agree on focal point | Clear signal or agreement |
| **Chicken** | Confrontation; backing down is costly | Escalation spiral risk | De-escalation mechanism / face-saving |
| **Stag Hunt** | Cooperation benefits all, but risky if other defects | Weak cooperation (fragile) | Strong enforcement mechanism |
| **Bargaining** | Actors want different deals but both prefer agreement to war | Negotiation breakdown risk | Good-faith bargaining framework |

---

## Red Flags: Games You Don't Want

### Prisoner's Dilemma with No Reputation
- Actors won't cooperate even if mutual cooperation is better
- Example: Arms race with no treaties

### Chicken with Escalation Spiral
- Both sides committed to not backing down
- Rational escalation → war
- Example: Nuclear brinksmanship, territorial standoff

### Coordination Game with Incompatible Demands
- No focal point exists
- Actors can't agree on which equilibrium
- Example: Two states both claim the same territory

---

## Game Theory Integration into Assessments

**In FULL assessments, add:**

```markdown
### Strategic Interaction Analysis

**Game identified:** [Which game structure describes this?]

**Payoff matrix:**
[Show payoffs for each actor's options]

**Nash Equilibrium:** [Where will the game settle rationally?]

**Stability:** [Stable / Unstable / Multiple equilibria?]

**If unstable:** [What could trigger deviation? Escalation risk?]

**Escape routes:** [How can actors avoid worst outcome?]

**Probability each escapes route:** [High / Medium / Low for each option]
```

This grounds strategy in incentive logic, not just rhetoric.
