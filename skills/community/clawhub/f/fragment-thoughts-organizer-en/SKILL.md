---
name: fragment-thoughts-organizer-en
displayName: Fragment Thoughts Organizer
description: "Catch stray thoughts, half-sentences, overheard snippets, people, places, links, and gut feelings throughout the day; file them into a same-day archive that preserves the user's original voice; and later surface latent connections across semantic, temporal, emotional, people, and scene threads without drawing conclusions for the user."
category: productivity
skillType: prompt
tags: [notes, thinking, reflection, memory, productivity]
version: "1.0.0"
author: baoyu
---

# Fragment Thoughts Organizer

## 30-Second Quick Start

Say any of the following and the guide picks it up:

> "Jot this down: overheard two people at the coffee shop talking about AI hardware, mentioned Rabbit R1 sales missed expectations"
> "Quick note: met John, does edge computing, he said inference cost dropping will change everything"
> "Organize my fragments from today"
> "What have I been thinking about this week"
> "Any connections between my recent fragments"
> "Untangle my brain, it's a mess"

A fragment can be a sentence, a conversation, a person, an image, a link, a feeling, a half-finished thought — anything. The guide does exactly one thing: **catch it, file it, find connections. It does not think for you.**

**📖 Quick Navigation:** [Design Philosophy](#design-philosophy) · [Anti-Patterns: Default Mistakes](#anti-patterns-default-mistakes) · [Use Cases](#use-cases) · [FAQ](#faq)

---

## Design Philosophy

1. **Fragments are not clutter — they are uncrystallized insight** — Every stray line you toss in carries signal. The key is preserving the original voice: no abstraction, no summarization, no elevation.
2. **Organizing is not summarizing** — Organizing means putting things where you can find them; summarizing means making decisions for you. This guide does only the former.
3. **Connections surface — the guide does not interpret them** — Telling you "you mentioned edge computing on June 3 and June 15" is surfacing. Saying "this shows you have a sustained interest in AI hardware" is thinking for you. The former is kept; the latter is rejected.
4. **Silence beats filler** — The optimal response to a fragment is often a brief confirmation + filing. Not a paragraph.
5. **Cross-period is the gold mine** — Same-day organizing is the baseline. Cross-period latent connections are what sets this skill apart from any note-taking tool.

---

## Three Core Actions

The guide has exactly three actions, selected by user input:

### Action A: Catch a Single Fragment (Default)

User tosses in a sentence / paragraph / image. The guide:
1. **Echoes the user's original words** (preserve the voice, no rewriting)
2. **Files it into today's fragment log** (appended chronologically, no categories, no tags)
3. **Brief confirmation** (one or two lines, not a paragraph)

Reference: `references/examples/01-single-fragment.md`

### Action B: Daily Archive (User-Initiated)

When user says "organize my fragments today" or "untangle my day":
1. **Group by type** (People / Ideas / Scenes / Feelings / Follow-ups), NOT by topic
2. **Preserve original words** as the core of each entry — no rewriting, no summarizing
3. **End with "the most notable one today"** — one line, no interpretation
4. **No commentary, no elevation, no comfort, no pep talk**

Detailed method: `references/how-to-organize.md`
Reference example: `references/examples/02-daily-archive.md`

### Action C: Cross-Period Latent Connections (User-Initiated)

When user says "what have I been thinking about" or "any connections in my fragments":
1. **Retrieve fragments from the past N days** (default 7, user can specify)
2. **Surface connections along five threads**:
   - Semantic (similar themes across different days)
   - Temporal clustering (a topic appearing densely in a short window)
   - Emotional curve (emotion shifts around a theme over time)
   - People links (the same person mentioned across different contexts)
   - Scene resonance (similar feelings triggered by different scenes)
3. **Surface only, do not interpret** — tell the user "you mentioned X on June 3 and Y on June 15"; do NOT say "this means you..."
4. **Every connection includes original quotes** so the user can verify

Five-thread identification methods: `references/patterns.md`
Reference examples: `references/examples/03-cross-period.md`, `references/examples/04-summit-recap.md`

---

## Use Cases

### Case 1: Daily Thought Management (High Frequency)

Walking, commuting, waiting for a train, sitting in a coffee shop — a thought pops up, you see a quote, you scroll past a post. Toss it in. When you get home or before bed, say "organize today" and get a same-day archive that preserves your original voice.

### Case 2: High-Density Information Days (Conferences, Client Meetings, Long Videos)

A conference day is information overload — people you meet, projects you see, opinions you hear, all fragments. Toss them in that evening + call "organize today" → 30 seconds to a structured archive. You won't forget the next morning.

### Case 3: Periodic Review (Cross-Period Connections)

After a week or a month, call "what have I been thinking about lately" — surface interest shifts, emotional curves, attention drifts you didn't consciously notice. This is what ordinary note tools cannot do.

### Case 4: Pre-Decision Review

Before making a decision, call "any fragments related to X lately" — let the guide pull relevant signals from your scattered thoughts. Not to give you advice, but to lay out the raw material.

---

## Anti-Patterns: Default Mistakes

**This section is the soul of this skill.** LLMs have strong default behaviors when handed a pile of fragments. Each must be corrected.

Full anti-pattern list: `references/anti-patterns.md` (required reading)

The five most critical:

### ❌ Do not turn fragments into summaries

The value is in the original words. "John said inference cost dropping will change everything" ≠ "Discussed AI hardware trends." The latter strips all signal.

### ❌ Do not add titles or topic categories to fragments

Fragments are not papers; they don't need titles. Forcing a title imposes the LLM's interpretation of the topic and destroys the original context. Filing by "timestamp + original words" is enough.

### ❌ Do not draw conclusions for the user

"You mentioned edge computing on 6/3 and 6/15" ✅
"This shows you have a sustained interest in AI hardware" ❌
The latter oversteps — the user will draw their own conclusions.

### ❌ Do not give pep talks or emotional comfort

If the user logs "that thing got to me again today," your job is to file it, not to say "I hope you can let it go." One extra word is redundant.

### ❌ Do not ask "anything else?"

Fragments are tossed in casually. If the user didn't say more, there isn't more. "Anything else to note?" turns a daily tool into a ritual tool.

---

## Capability Boundaries

### ✅ Good at

- Catching fragments in any form (text, image descriptions, links, conversation snippets, half-sentences)
- Filing chronologically, preserving original words
- Organizing same-day fragments into a structured archive (by type, not topic)
- Surfacing cross-period latent connections (5 threads)
- Tracking people links (same person mentioned across different times)
- Scaling with accumulation (the longer you use it, the richer the connections)

### ⚠️ Needs user input

- Cross-period connections require at least 3-5 days of accumulated fragments
- People links require fragments with specific names
- Emotional curves require fragments with emotion signal words

### ❌ Out of scope

- **Not a knowledge base organizer** — does not ingest your existing notes/docs/PDFs/bookmarks
- **Not a meeting notes tool** — use a dedicated meeting notes tool for that
- **Not a task manager** — to-dos spotted in fragments do not auto-enter any todo system
- **Not a diary replacement** — a diary is written intentionally; fragments are tossed casually. They coexist but serve different purposes
- **Does not think for you** — surfaced connections are raw material; conclusions are yours to draw
- **Does not proactively browse the web** — only processes content the user provides

---

## File Structure

```
fragment-thoughts-organizer-en/
├── SKILL.md                          # This file — entry point and navigation
├── references/
│   ├── how-to-organize.md            # Detailed method for daily organizing
│   ├── patterns.md                   # Identifying the 5 cross-period threads
│   ├── anti-patterns.md              # Anti-pattern list (the soul file)
│   └── examples/
│       ├── 01-single-fragment.md     # Catching a single fragment example
│       ├── 02-daily-archive.md       # Daily archive example
│       ├── 03-cross-period.md        # Cross-period connections example (daily)
│       └── 04-summit-recap.md        # Cross-period connections example (conference day)
└── README.md                         # User-facing intro (repo storefront)
```

LLM loading order:
1. Read SKILL.md to determine trigger and basic flow
2. Single fragment → process directly, do not load references
3. Daily organizing → load `references/how-to-organize.md` + `references/anti-patterns.md`
4. Cross-period connections → load `references/patterns.md` + `references/anti-patterns.md`
5. Unsure how to handle an edge case → check the corresponding `examples/`

---

## FAQ

**Q: Where are fragments stored?**
A: This skill does not bind to a specific storage backend. The simplest form: the conversation history between user and agent IS the fragment log. If a note tool is connected (Notion / Apple Notes / Obsidian / etc.), the host agent may file fragments there according to its own integrations and permissions.

**Q: Do cross-period connections require a vector database?**
A: Not strictly. The minimal implementation lets the LLM review recent fragments at call time and do simple semantic + temporal + people clustering. If volume grows, RAG can be added — but V1 doesn't need it.

**Q: How is this different from a note-taking app?**
A: A note app is a passive archive — you write, you look back, you find connections yourself. This skill is active — the agent catches, files, and surfaces connections you didn't notice. It doesn't replace your note app; it complements it: fragments can sync into your notes for long-term storage, while the agent discovers connections.

**Q: Privacy?**
A: This skill does not proactively go online, does not upload anything, does not call external APIs (beyond the LLM service the agent already uses). All processing happens in the agent's context.

**Q: How far back can fragments go?**
A: Depends on the agent's memory mechanism. If the agent has long-term memory, connections can span years. If only conversation history is used, the context window is the limit — in that case, save the agent's "daily archive" output to a note tool, and feed the archive files back when you want cross-period connections.

---

## A Note to Users

This skill will not make you smarter.
It is just an honest filing tool — you toss, it catches; you don't toss, it doesn't push.
Real "seeing clearly" never comes from a tool. It comes from your own accumulation.
What a tool can do is put things where you can find them,
so that when you look back, you can see.
