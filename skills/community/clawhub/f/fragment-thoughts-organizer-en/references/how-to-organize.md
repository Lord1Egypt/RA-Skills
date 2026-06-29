# Daily Fragment Organizing Method

> This file defines the specific method for "organizing today's fragments into an archive." Load when the user says "organize today" or "untangle my day."

---

## Core Principle

Archive ≠ Diary ≠ Summary ≠ Conclusion

An archive is a **factual listing**, grouped by fragment type, preserving original words. No narrative, no reflection, no summary.

---

## Five Fragment Types

Group by the shape of the fragment, NOT by topic:

### 1. 👤 People
A specific person appears in the fragment.

Format:
```
👤 John (edge computing developer)
   Original: "Met John, does edge computing, he said inference cost dropping will change everything"
   Context: Conference expo booth
```

Judgment: The fragment contains a name, role, or pronoun clearly pointing to a person.

### 2. 💡 Idea
A judgment, opinion, or question that popped into the user's head.

Format:
```
💡 Idea
   Original: "If inference cost drops another half, does on-device AI not need the cloud anymore?"
   Context: Thought triggered by overhearing a conversation at a coffee shop
```

Use a plain type label (`Idea`) rather than a synthesized title. The original line is the entry.

Judgment: It's the user's "internal product," not a description of external facts.

### 3. 📍 Scene
A specific time, place, or event.

Format:
```
📍 Web Summit, conference expo hall
   Original: "More people than last year, booth area too crowded to walk"
   Time: 6/24 morning
```

Judgment: Has a specific time, place, or event.

### 4. 🌊 Feeling
An emotion, mood, or physical reaction.

Format:
```
🌊 An indescribable sense of urgency after the booth tour
   Original: "Feels like everyone is building Agents, am I falling behind?"
```

Judgment: Describes an internal state, not external facts.

### 5. 📌 Follow-up
The user explicitly says "want to follow up" or it contains to-do intent.

Format:
```
📌 Find time to watch Rabbit R1 teardown
   Original: "Look up Rabbit R1 teardown videos when I get home"
```

Judgment: The user explicitly expressed intent for future action.

---

## What if a Fragment Belongs to Multiple Types?

This is normal. Do not force single categorization.

Example:
> "Met John, he said inference cost dropping will change everything, I was kind of convinced, want to look into it when I get home"

This fragment is simultaneously:
- 👤 People (John)
- 💡 Idea (inference cost drop)
- 🌊 Feeling (convinced)
- 📌 Follow-up (want to look into it)

In the archive, this fragment appears under each type, **preserving the same original words**. This is correct — the same fragment carries different signals from different angles.

---

## Archive Format

```markdown
# 📋 Daily Archive · 2026-06-24

> 12 fragments total. Grouped by type, original words preserved.

---

## 👤 People (3)

**John** — Edge computing developer
> "Met John, does edge computing, he said inference cost dropping will change everything"

**Sarah** — AWS Solutions Architect
> "Sarah said a lot of clients are asking about Agent deployment paths, but nobody knows how to calculate ROI"

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

**Web Summit, conference expo hall**
> "More people than last year, booth area too crowded to walk"

**Lunch area**
> Shared a table with two indie devs, chatted for an hour

---

## 🌊 Feelings (2)

> An indescribable sense of urgency after the booth tour — feels like everyone is building Agents, am I falling behind?

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

## How to Choose "The Most Notable One Today"

Criterion: **Something new that grew today, not something received today.**

- ✅ "Agent value is in stability not smarts" — the user's own judgment
- ✅ "Maybe the core advantage of solo work is fast decisions" — a new-born insight
- ❌ "John said inference cost will change everything" — someone else's words the user received
- ❌ "Look up Rabbit R1" — a to-do, not an insight

What if you can't pick one? Say so:
> Today's fragments are mostly received input, with no clear "new-growth" insight. That's normal — not every day has one.

---

## What Not to Do

Before each organizing session, self-check against `anti-patterns.md`. The three most common mistakes:

1. **Writing the archive as a diary narrative** — "Today was a fulfilling day..." ❌
2. **Adding topic tags to each fragment** — "#AI-hardware #startup-thinking" ❌
3. **Adding a summary at the end** — "Today mainly focused on AI hardware direction" ❌

The archive ends at "The Most Notable One Today." No summary, no reflection, no next-day plan.
