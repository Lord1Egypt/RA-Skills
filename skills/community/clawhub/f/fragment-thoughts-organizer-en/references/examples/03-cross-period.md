# Example 03: Cross-Period Connections (Daily Life)

> When the user says "what have I been thinking about lately" or "any connections in my fragments."
> Load `references/patterns.md` and `references/anti-patterns.md` first.

---

## Context

The user has been tossing in fragments for about two weeks. Today (6/20) they ask: "What have I been thinking about this week?"

The guide retrieves fragments from the past 7 days (6/14–6/20) and surfaces connections.

---

## Input: Fragments from 6/14–6/20

```
6/14: "Saw a YouTube video about someone going solo as an indie developer, kind of inspiring"
6/14: "Calculated my runway — savings can last about 6 months"
6/15: "Talked to my partner about possibly quitting, they were surprisingly supportive"
6/15: "But what if I can't find clients? The fear is real"
6/16: "Rabbit R1 flop reminds me that hardware is brutal — glad I'm in software"
6/17: "Overheard two people at the coffee shop talking about AI hardware, mentioned Rabbit R1"
6/17: "Met John, does edge computing, he said inference cost dropping will change everything"
6/17: "If inference cost drops another half, does on-device AI not need the cloud anymore?"
6/18: "Couldn't sleep, kept thinking about whether to take the leap"
6/18: "Maybe the core advantage of solo work isn't doing many things, it's making decisions fast"
6/19: "Found out my old colleague Lisa also went solo last month, she seems happy"
6/19: "Emailed Lisa, want to grab coffee and hear her experience"
6/20: "Lisa replied with three notes about pricing her first retainer"
6/20: "Woke up feeling surprisingly calm today. Maybe the decision is already made, I just haven't admitted it"
```

---

## Correct Output

```markdown
# 🔮 Cross-Period Connections · Past 7 Days

> From fragments between 6/14 and 6/20, the following connections surfaced.
> These are factual observations, not conclusions.

---

## 🔗 3 Connections Found

### Connection 1: [Temporal Clustering] Solo Work / Career Change

Between 6/14 and 6/20, 9 fragments relate to "quitting / going solo":
- 6/14: "Saw a YouTube video about someone going solo as an indie developer, kind of inspiring"
- 6/14: "Calculated my runway — savings can last about 6 months"
- 6/15: "Talked to my partner about possibly quitting, they were surprisingly supportive"
- 6/15: "But what if I can't find clients? The fear is real"
- 6/18: "Couldn't sleep, kept thinking about whether to take the leap"
- 6/18: "Maybe the core advantage of solo work isn't doing many things, it's making decisions fast"
- 6/19: "Found out my old colleague Lisa also went solo last month, she seems happy"
- 6/20: "Lisa replied with three notes about pricing her first retainer"
- 6/20: "Woke up feeling surprisingly calm today. Maybe the decision is already made, I just haven't admitted it"

The topic appeared on 5 out of 7 days. No gap longer than 2 days.

---

### Connection 2: [Emotional Curve] Solo Work

Around the topic of "going solo," your emotion signals shifted:
- 6/14: "kind of inspiring" (positive)
- 6/15: "they were surprisingly supportive" (positive)
- 6/15: "The fear is real" (negative)
- 6/18: "Couldn't sleep, kept thinking about whether to take the leap" (negative)
- 6/20: "feeling surprisingly calm today" (recovery to positive)

Emotion shifted: positive → negative → positive, over 6 days.

---

### Connection 3: [People Links] Lisa

"Lisa" appeared in these fragments:
- 6/19: "Found out my old colleague Lisa also went solo last month, she seems happy"
- 6/19: "Emailed Lisa, want to grab coffee and hear her experience"
- 6/20: "Lisa replied with three notes about pricing her first retainer"

Mentioned 3 times across 2 days. First mention was discovery, second was proactive outreach, third was a reply with concrete advice.

---

## 📊 Fragment Overview

- Total fragments: 14
- Time span: 7 days
- Active days: 6 (6/14, 6/15, 6/17, 6/18, 6/19, 6/20)
- Most frequent type: 💡 Ideas (5)

---

## ⚠️ Dimensions With No Connections Found

- Scene resonance: Insufficient (fewer than 2 Feeling-type fragments with similar descriptions in different scenes)
- Semantic (non-career): No other topic appeared ≥2 times

(This is normal. The week had a clear dominant theme.)
```

---

## Why This Works

1. **Connection 1 surfaces a temporal cluster** — 8 fragments in 7 days, 5 active days. But it does NOT say "you're clearly leaning toward quitting." It just states the facts.
2. **Connection 2 surfaces an emotional curve** — the shift from inspired → fearful → calm. But it does NOT say "you've gone through a decision-making journey." It just charts the signals.
3. **Connection 3 surfaces a people link** — Lisa appeared twice. But it does NOT say "Lisa is your role model." It just notes the mentions.
4. **"The decision is already made, I just haven't admitted it"** — the guide quotes this in Connection 1 but does NOT comment on it. The user said it; the guide preserves it. That's the job.

---

## ❌ What Would Be Wrong

**Wrong interpretation**:
```
Connection 1 analysis: The density of career-change fragments suggests
you've essentially decided to quit. The emotional trajectory from
inspiration through fear to calm confirms that you've processed the
decision and are ready to act.
```
(Wrong: this is interpreting and drawing conclusions. The guide surfaces; the user concludes.)
