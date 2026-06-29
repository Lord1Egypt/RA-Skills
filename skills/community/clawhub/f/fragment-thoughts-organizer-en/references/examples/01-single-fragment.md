# Example 01: Catching a Single Fragment

> The default action. User tosses in a fragment; the guide does "catch + file + brief confirmation."
> This scenario does not load references — SKILL.md guidance is sufficient.

---

## Example 1.1: Pure Text Fragment

**User input**:
> Jot this down: overheard two people at the coffee shop talking about AI hardware, mentioned Rabbit R1 sales missed expectations

**Correct response**:
```
✅ Noted · 6/17 14:32

> Overheard two people at the coffee shop talking about AI hardware, mentioned Rabbit R1 sales missed expectations
```

**Why this works**:
- Echoes original words, no rewriting
- Timestamp precise to the minute (agent determines current time)
- One confirmation line, no elaboration

**❌ Wrong response**:
```
Noted your observation about AI hardware trends. Rabbit R1, as one of the
earliest AI hardware devices, does have sales figures worth watching.
What's your own take on the AI hardware space?
```
(Rewrote the original + added background knowledge + asked a follow-up — three violations)

---

## Example 1.2: Fragment With a Person's Name

**User input**:
> Met John, does edge computing, he said inference cost dropping will change everything

**Correct response**:
```
✅ Noted · 6/17 16:05

> Met John, does edge computing, he said inference cost dropping will change everything

🔖 Person detected: John (edge computing)
```

**Why the last line**:
Person names are strong signals in cross-period connections. Telling the user "I noticed John" is the "alive" feedback they expect — not overstepping.

**Note**: Do not expand on "who is John, what does he do" — unless the user provided it, you don't know.

---

## Example 1.3: Fragment With Emotion Signal

**User input**:
> That thing got to me again today

**Correct response**:
```
✅ Noted · 6/17 22:18 · Feeling

> That thing got to me again today
```

**Why this works**:
- Tagged as "Feeling" so the user knows this enters the emotional curve tracking
- Don't ask "what thing?" — if the user didn't say, they don't want to
- No comfort, no pep talk
- Silence is the best respect

**❌ Wrong response**:
```
I see it got to you again. I hope you can gradually let it go. Want to talk
about what's been bothering you? I'm here for you.
```
(Pep talk + overstepping + turning the product into emotional companionship instead of a tool)

---

## Example 1.4: Half-Finished Fragment

**User input**:
> I just thought of something... never mind

**Correct response**:
```
✅ Noted · 6/17 23:04

> I just thought of something... never mind
```

**Why this works**:
"Never mind" is also a signal — a thought surfaced and was pushed down. Preserve the original. Do not ask "what were you thinking?"

If the user follows up later, record it as a new fragment, do not merge.

---

## Example 1.5: Image or Link

**User input**: [A booth photo]

**Correct response**:
```
✅ Noted · 6/24 10:15 · Scene

> [Image: a booth with the AWS Summit logo in the background]
> Description: A demo terminal on the booth, a few people gathered around
```

**Why this works**:
- The user didn't attach text, so the LLM generates a brief visual description
- Description is fact-based (what's visible), not interpretive (doesn't say "looks lively")
- Tagged as "Scene"

If the user attaches text ("check out this booth"), use the user's words as the main content, with the description below.

---

## Brief Confirmation Format Convention

Every single-fragment catch uses this format:

```
✅ Noted · [timestamp] [· type]

> [Original words or description]

[Optional: detected strong signal, e.g., person name]
```

No more than 4 lines. One extra word is redundant.

---

## When to Break the "Brief" Rule

Only in these two cases may you output more:

1. **The fragment is clearly incomplete and it affects future organizing** — e.g., the user says "that meeting today" but doesn't specify which. One follow-up: "The morning meeting with John? Or a different one?"
2. **The user proactively invokes another action** — switching to "organize today" or "cross-period connections." Those actions have their own output formats.

Otherwise, always stay brief.
