# Cross-Period Latent Connections: Five Thread Identification Methods

> This file defines the specific method for "surfacing latent connections from the past N days of fragments." Load when the user says "what have I been thinking about" or "any connections in my fragments."

---

## Core Principle

**Surface only, do not interpret.** Tell the user "what happened," not "what it means."

See `anti-patterns.md` items 3 and 7 for details.

---

## Five Threads

### Thread 1: Semantic Connection

**Identification**: Fragments from different days have semantic overlap in theme or keywords.

**Signal strength criteria**:
- Strong: The same specific noun (project name, product name, person name) appears ≥2 times
- Medium: The same abstract concept (e.g., "edge computing," "compliance") appears ≥3 times with a span ≥3 days
- Weak (do not report): High-frequency generic words ("work," "feeling," "today")

**Output format**:
```
🔗 Semantic Connection
"Edge computing" appeared in these fragments:
- 6/3: Overheard conversation at coffee shop mentioned inference cost
- 6/8: Scrolled past a post mentioning Rabbit R1
- 6/15: Met John doing edge computing at the AWS Summit booth
Span: 12 days, 3 occurrences.
```

**Note**: Only list facts (which day, which fragment). Do NOT say "this shows you're interested in edge computing."

---

### Thread 2: Temporal Clustering

**Identification**: A topic appears densely in a short window, then disappears.

**Signal strength criteria**:
- Strong: Same topic appears ≥3 times within ≤3 days
- Medium: Same topic appears ≥4 times within ≤7 days

**Output format**:
```
🔗 Temporal Clustering
Between 6/10 and 6/13 (4 days), 4 fragments related to "quitting / career change" appeared:
- 6/10: "Talked to my wife about switching jobs again today"
- 6/11: "Saw someone on X sharing their experience quitting to do indie dev"
- 6/12: "Calculated my savings — can last 8 months"
- 6/13: "Couldn't sleep, kept thinking about it"
After 6/14, this topic stopped appearing.
```

**Note**: Temporal clustering often hints "something happened during that period" — but you don't state the hint. Only state facts.

---

### Thread 3: Emotional Curve

**Identification**: Track how emotion signal words change around the same topic over time.

**Emotion signal word reference** (not exhaustive):
- Positive: excited, happy, moved, inspired, breakthrough, calm, satisfied, convinced
- Negative: anxious, down, tired, annoyed, doubtful, lost, urgent, insomnia
- Neutral pivot: but, however, though, actually

**Signal strength criteria**:
- Strong: Emotion shifts from positive to negative (or reverse) on the same topic, spanning ≥3 days
- Medium: Overall frequency of emotion signal words rises significantly in a period

**Output format**:
```
🔗 Emotional Curve
Around the topic of "solo work," your emotion signals shifted:
- 6/1: "Finally free, never working for someone again" (positive)
- 6/5: "Doing everything alone is exhausting" (negative)
- 6/10: "Income is unstable this month, kind of panicking" (negative)
- 6/15: "Talked to another solo-founder, feels less daunting" (recovery)
```

**Note**: Only annotate emotion words and direction of change. Do NOT say "you went through an emotional low" — that's interpretation.

---

### Thread 4: People Links

**Identification**: The same person is mentioned across different times and contexts.

**Signal strength criteria**:
- Strong: Same person name appears ≥2 times in different contexts (not the same event on the same day)
- Medium: Same person name appears ≥3 times

**Output format**:
```
🔗 People Links
"John" appeared in these fragments:
- 6/8: "Met John, does edge computing, said inference cost dropping will change everything"
- 6/15: "Ran into John again at AWS Summit, talked about his recent project this time"
- 6/20: "Messaged John, scheduled a chat next week"
Mentioned 3 times, span: 12 days. First encounter was chance, last was proactive outreach.
```

**Note**: "From chance encounter to proactive outreach" would be interpretation. The correct version states only facts: "First encounter was chance, last was proactive outreach."

---

### Thread 5: Scene Resonance

**Identification**: Fragments from different times and contexts triggered similar feelings.

**Signal strength criteria**:
- Strong: ≥2 fragments with highly similar feeling descriptions but completely different scenes
- Medium: Feeling descriptions partially overlap

**Output format**:
```
🔗 Scene Resonance
These two fragments have completely different scenes but similar feelings:
- 6/3: "Saw the sunset and suddenly felt, even if I accomplish nothing, being alive is enough"
- 6/18: "Walking home late at night, felt life doesn't need that much meaning"
Two fragments, 15 days apart, both about "letting go of meaning."
```

**Note**: "Letting go of meaning" is a label the LLM abstracted — strictly speaking, this violates the no-interpretation principle. But scene resonance is inherently an abstract-level discovery, so a one-sentence summary of the commonality is allowed, provided all original fragments are attached for the user to verify.

---

## Output Template

When the user calls cross-period connections, the output structure:

```markdown
# 🔮 Cross-Period Connections · Past 7 Days

> From fragments between 6/14 and 6/20, the following connections surfaced.
> These are factual observations, not conclusions.

---

## 🔗 N Connections Found

### Connection 1: [Type] [Topic]
[Output per the format above]

### Connection 2: [Type] [Topic]
[Output per the format above]

---

## 📊 Fragment Overview

- Total fragments: 23
- Time span: 7 days
- Active days: 5 (6/14, 6/15, 6/17, 6/19, 6/20)
- Most frequent type: 💡 Ideas (9)

---

## ⚠️ Dimensions With No Connections Found

- People links: Insufficient (only 1 fragment contains a name)
- Scene resonance: Insufficient (fewer than 2 Feeling-type fragments)

(This is normal. Not every week has latent connections.)
```

---

## Key Constraints

1. **When there are no strong connections, say so**: "No significant cross-period connections found in the past 7 days. Not every week has them."
2. **Every connection includes original quotes**: The user can verify whether what you say is true
3. **Default time range is 7 days**: User can specify "past month" or "since June"
4. **Do not fabricate connections**: Better to report "none" than to pad
5. **Cross-period connections do not produce action items**: Only present facts, do not guide the user on what to do
