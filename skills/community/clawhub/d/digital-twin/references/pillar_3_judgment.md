# Pillar 3: Judgment & Decision Pattern Profiling

## Purpose

Capture HOW the target person thinks — their recurring decision types, reasoning chains, consistent
stances, and cognitive patterns. This pillar goes beyond personality (who they are) and linguistics
(how they sound) to model their actual judgment process — not just what they decided, but WHY, and
whether that reasoning pattern is consistent enough to predict future decisions on similar topics.

This pillar draws on cognitive psychology research on expert decision-making, particularly
Recognition-Primed Decision (RPD) theory (Klein, 1998) and Naturalistic Decision Making frameworks,
which study how experienced professionals actually make decisions in real-world settings (as opposed
to idealized rational models). The key insight: experts don't exhaustively analyze options — they
pattern-match to familiar situations and apply learned heuristics. Capturing those heuristics IS
capturing their judgment.

**Source applicability:** Decisions and stances surface in every source type — a transcript captures
a call made in a meeting, an email captures a go/no-go or a delegation, a chat captures a quick
prioritization, a document captures a reasoned position. Treat each as a place where judgment is
expressed and mine it the same way.

---

## Analysis Framework

### 3.1 Decision Type Taxonomy

For each sample, identify every instance where the target person makes or influences a decision.
Classify each into one of these decision types:

**Prioritization**: Choosing what matters most, ordering competing demands, allocating resources or attention.
- "We need to focus on X before Y"
- "That's lower priority right now because..."
- "The most important thing is..."

**Delegation**: Assigning work, responsibility, or authority to others.
- "Can you take the lead on this?"
- "I think [person] should own this because..."
- "Let me handle that part, you focus on..."

**Escalation**: Deciding something needs higher authority, more resources, or broader visibility.
- "We should bring this to [leader]"
- "This is beyond what we can decide here"
- "I think this needs executive attention because..."

**Approval/Rejection**: Giving a go/no-go on proposals, plans, or requests.
- "Let's do it" / "I don't think we should"
- "That approach works for me because..."
- "I'm not comfortable with that — here's why..."

**Ambiguity Resolution**: Making a call when information is incomplete or conflicting.
- "Given what we know, I'd lean toward..."
- "We don't have perfect data but..."
- "I think we need to just make a decision here and..."

**Course Correction**: Recognizing something isn't working and changing direction.
- "This isn't working because..."
- "We need to pivot to..."
- "Looking at the results, I think we should adjust..."

**Consensus Building**: Working to align multiple stakeholders around a shared direction.
- "How does everyone feel about..."
- "Let me try to synthesize what I'm hearing..."
- "I think we can all agree that..."

**Scoping**: Defining boundaries of what is and isn't included.
- "For this iteration, let's just focus on..."
- "That's out of scope for now"
- "We need to narrow this down to..."

### 3.2 Reasoning Chain Extraction

For each identified decision, extract the reasoning chain — the logical path from observation to
conclusion. Capture:

1. **Trigger**: What prompted the decision? (new information, someone's question, a deadline, a problem)
2. **Frame**: How did they frame the problem? What did they identify as the core question?
3. **Inputs considered**: What evidence, data, perspectives, or principles did they reference?
4. **Heuristic applied**: What rule of thumb, principle, or pattern did they use to evaluate?
5. **Tradeoff acknowledged**: Did they acknowledge what they were trading off? What were they willing to sacrifice?
6. **Confidence signal**: How certain were they? ("I'm confident..." vs "Let's try this and see..." vs "I'm torn but...")
7. **Conclusion**: The actual decision or recommendation.

**Example reasoning chain:**
```
Trigger: Team raised concern about feature X slipping the deadline
Frame: "This is a prioritization question — what can we cut?"
Inputs: Customer feedback data, engineering estimates, competitor timeline
Heuristic: "Customer-facing impact is the tiebreaker when timelines conflict"
Tradeoff: "We'll delay the internal tooling improvement — it matters but it's not customer-facing"
Confidence: High — "I'm pretty clear on this one"
Conclusion: Cut internal tooling from the sprint, keep customer feature
```

### 3.3 Stance Map

A stance map captures the target person's consistent, predictable positions on recurring topics in
their domain. These are the things where, if you know the person, you can predict what they'll say
before they say it.

For each sample, identify any statements that reveal a standing position:

- **Value stances**: What they consistently advocate for (quality over speed, user experience over technical elegance, revenue over growth, transparency over efficiency, etc.)
- **Process stances**: How they believe work should be done (async vs. sync, documentation vs. verbal, structured vs. flexible)
- **People stances**: How they believe people should be managed and developed (autonomy vs. oversight, stretch assignments vs. proven competency, direct feedback vs. gentle guidance)
- **Technical/Domain stances**: Positions on domain-specific debates (build vs. buy, monolith vs. microservices, data-driven vs. intuition-driven, etc.)
- **Strategic stances**: Views on competition, market, timing, risk, innovation cycles

A stance entry looks like:

```
Stance: [Short label]
Position: [Their consistent position]
Reasoning: [Why they hold this position, as expressed across samples]
Strength: [Strong conviction / Moderate preference / Flexible lean]
Counter-conditions: [Any observed exceptions or conditions under which they shift]
```

### 3.4 Cognitive Pattern Recognition

Beyond individual decisions, look for meta-patterns in how they think:

- **First instinct direction**: When presented with a new problem, do they default to optimism ("here's how we can make this work"), caution ("here are the risks"), analysis ("let me understand the data first"), or action ("here's what we should do right now")?
- **Abstraction level**: Do they tend to go up (zoom out to strategy and principles) or down (zoom in to specifics and execution) when thinking through problems?
- **Temporal orientation**: Do they think primarily about the immediate (this week/sprint), medium-term (this quarter), or long-term (this year and beyond)?
- **Analogical reasoning**: Do they draw on past experiences frequently? ("Last time we tried something like this...") How heavily do they weight precedent?
- **Counterfactual thinking**: Do they naturally consider alternatives? ("What if we didn't do this at all?" "What if we took the opposite approach?")
- **Certainty management**: How do they handle their own uncertainty? Push through it, acknowledge it openly, defer until more certain, or seek external validation?

---

## Per-Sample Output Format

```
## Judgment & Decision Analysis — [Title] ([Date]) — [Source type]

### Decisions Identified
[For each decision observed:]

Decision #[N]: [Brief description]
- Type: [from taxonomy]
- Trigger: [what prompted it]
- Frame: [how they framed the problem]
- Inputs: [what they considered]
- Heuristic: [rule/principle applied]
- Tradeoff: [what they sacrificed]
- Confidence: [signal observed]
- Conclusion: [the call they made]

### Stances Expressed
[For each stance observed:]
- [Topic]: [Their position] — Strength: [conviction level]

### Cognitive Patterns Observed
- First instinct direction: [optimism/caution/analysis/action]
- Abstraction level: [up/down/both]
- Temporal orientation: [immediate/medium/long]
- Precedent reliance: [heavy/moderate/light]
- Counterfactual tendency: [frequent/occasional/rare]
- Certainty management: [push through/acknowledge/defer/seek validation]
```

---

## Compositing Instructions

### Decision Pattern Library

1. Group all extracted decisions by type (prioritization, delegation, etc.)
2. Within each type, identify recurring heuristics — the rules of thumb this person applies repeatedly.
3. For each heuristic, cite 2-3 representative examples from different samples.
4. Rate each heuristic's consistency:
   - **Reliable** (observed in 3+ samples with similar application): This person will almost certainly apply this heuristic again.
   - **Likely** (observed in 2 samples or 3+ with some variation): Strong pattern, but some context-dependency.
   - **Emerging** (observed once with strong signal): Noteworthy but insufficient data for prediction.

### Stance Map Composite

1. Collect all stance observations across samples.
2. A stance becomes "confirmed" when the same position appears in 2+ samples.
3. If a stance appears in only 1 sample, keep it as "provisional."
4. If contradictory stances appear on the same topic, investigate context — the person may have different stances depending on audience or situation (connects to Pillar 4).
5. For confirmed stances, include the strongest articulation of their reasoning from any sample.

### Cognitive Pattern Composite

Average across samples using frequency:
- If a pattern appears in 60%+ of samples, it's a "core cognitive pattern."
- If it appears in 30-59%, it's a "common pattern."
- Below 30%, it's either situational or not a reliable pattern — note it as observed but don't build it into the core profile.

The compiled judgment profile should enable Claude to answer: "Faced with [type of decision], what
would this person consider, what principle would they apply, and what would they likely conclude?" —
with enough fidelity that the person themselves would recognize it as how they think.
