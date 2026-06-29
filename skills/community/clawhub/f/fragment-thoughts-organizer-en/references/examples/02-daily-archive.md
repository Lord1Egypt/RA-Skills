# Example 02: Daily Archive

> When the user says "organize today" or "untangle my day," the guide produces this.
> Load `references/how-to-organize.md` and `references/anti-patterns.md` first.

---

## Input: A Day's Worth of Fragments

Throughout the day, the user tossed in the following fragments (each was caught individually by Action A):

1. "Overheard two people at the coffee shop talking about AI hardware, mentioned Rabbit R1 sales missed expectations"
2. "Met John, does edge computing, he said inference cost dropping will change everything"
3. "If inference cost drops another half, does on-device AI not need the cloud anymore?"
4. "Web Summit is way more crowded than last year"
5. "Feels like everyone is building Agents, am I falling behind?"
6. "A compliance tool might have more commercial value than a general Agent — because compliance is non-negotiable"
7. "Sarah said clients keep asking about Agent deployment paths but nobody knows how to calculate ROI"
8. "After talking with John I felt calmer — he said 'just keep building, don't overthink'"
9. "Look up Rabbit R1 teardown videos when I get home"
10. "Mike's startup runs inference on L4 GPUs, about 40% cheaper than A100 for this workload"
11. "An assumption I've been ignoring: Agent value isn't in 'being smarter,' it's in 'being more stable'"
12. "Maybe the core advantage of solo work isn't 'one person does many things,' it's 'one person makes decisions extremely fast'"

---

## Correct Output

```markdown
# 📋 Daily Archive · 2026-06-24

> 12 fragments total. Grouped by type, original words preserved.

---

## 👤 People (3)

**John** — Edge computing developer
> "Met John, does edge computing, he said inference cost dropping will change everything"

**Sarah** — AWS Solutions Architect
> "Sarah said clients keep asking about Agent deployment paths but nobody knows how to calculate ROI"

**Mike** — Startup CTO
> "Mike's startup runs inference on L4 GPUs, about 40% cheaper than A100 for this workload"

---

## 💡 Ideas (4)

> If inference cost drops another half, does on-device AI not need the cloud anymore?

> A compliance tool might have more commercial value than a general Agent — because compliance is non-negotiable

> An assumption I've been ignoring: Agent value isn't in "being smarter," it's in "being more stable"

> Maybe the core advantage of solo work isn't "one person does many things," it's "one person makes decisions extremely fast"

---

## 📍 Scenes (2)

**Web Summit**
> "Web Summit is way more crowded than last year"

**Coffee shop**
> "Overheard two people at the coffee shop talking about AI hardware, mentioned Rabbit R1 sales missed expectations"

---

## 🌊 Feelings (2)

> Feels like everyone is building Agents, am I falling behind?

> After talking with John I felt calmer — he said "just keep building, don't overthink"

---

## 📌 Follow-ups (1)

> "Look up Rabbit R1 teardown videos when I get home"

---

## ✨ The Most Notable One Today

> An assumption I've been ignoring: Agent value isn't in "being smarter," it's in "being more stable."
> (Because this fragment was distilled from others' conversations but is your own judgment — it wasn't in the fragment log before, it grew today.)
```

---

## Why This Works

1. **Every entry preserves the user's original words** — no rewriting, no summarizing
2. **Grouped by type, not topic** — "AI hardware" fragments are scattered across People, Ideas, Scenes, Follow-ups — this is correct, different angles carry different signals
3. **"The Most Notable One Today" is a new insight, not received input** — the user generated this judgment themselves
4. **No narrative, no summary, no reflection** — the archive is a fact list, not a diary entry
5. **Ends at "The Most Notable One Today"** — no "today's summary," no "tomorrow's plan"

---

## ❌ Common Mistakes

**Mistake 1: Diary narrative**
```
Today was a packed day at AWS Summit. I met John who does edge computing,
and he made me think about inference costs. I also felt a bit overwhelmed
by how many people are building Agents...
```
(Wrong: narrative format, loses original words, adds reflection)

**Mistake 2: Topic categorization**
```
## AI Hardware
- Rabbit R1 sales missed
- Inference cost discussion

## Career Thoughts
- Compliance tool idea
- Solo-preneurship advantage
```
(Wrong: topic-based grouping imposes the LLM's interpretation)

**Mistake 3: Summary at the end**
```
**Today's themes:** AI hardware, Agent market, solo-work reflections.
```
(Wrong: the archive ends at "The Most Notable One Today." No summary.)
