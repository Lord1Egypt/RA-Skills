# Brief Templates

Standard structures per brief type. User config and preferences in `~/Clawic/data/brief/` override everything here. On formal channels (exec email, external docs), keep the structure and replace emoji markers with plain headers (`delivery.md`).

Types: Executive · Project · Meeting · Handoff · Decision · Incident · Board · Research. Prose-memo variant at the end for narrative-memo cultures.

## Executive Brief

For leadership, stakeholders, or any reader with minutes, not hours.

```
⚡ BOTTOM LINE
[One sentence: the key takeaway]

📊 STATUS: [On track / At risk / Blocked]

KEY POINTS (3 max)
• [Most important thing]
• [Second most important]
• [Third if truly needed]

🎯 DECISION NEEDED
[What you need from them + by when — or "no action needed"]

📎 CONTEXT (optional)
[Only what changes how they read the points]
```

Sizing: one page ≈ 450-500 words ≈ a two-minute read at average silent-reading speed (~240 wpm, Brysbaert meta-analysis). Execs read on phones between meetings — if bottom line + ask don't fit the first screen, restructure before cutting words.

Key points: 3 max here — executive tightens the general five-max rule in SKILL.md Rule 5.

Context ordering, when included: SCQA (Minto) — Situation → Complication → Question; the Answer is your bottom line, already delivered above.

Worked example:
```
⚡ BOTTOM LINE
Q3 launch slips 2 weeks unless we cut the analytics module.

📊 STATUS: At risk

KEY POINTS
• Payments integration passed review — the critical path is now analytics
• Analytics is 3 weeks behind; vendor API changed mid-build
• Cutting analytics from v1 recovers the date; module ships standalone in Q4

🎯 DECISION NEEDED
Approve the cut by Friday, or accept the 2-week slip.
```

## Project Brief

For recurring status: sprint reviews, stakeholder updates.

```
📋 PROJECT: [Name] — [Date]

⚡ STATUS: [emoji] [On track / At risk / Blocked]

✅ COMPLETED (since last brief)
• [Done item]

🔄 IN PROGRESS
• [Current work] — [% or ETA]

🚧 BLOCKERS
• [Blocker] — [named unblocker] — [specific ask] — [days blocked]

📅 NEXT
• [Upcoming milestone] — [Date]

📊 METRICS (if applicable)
[Each number with its comparator: vs target, vs last period]
```

Principles:
- Recurring briefs report the delta. Repeating unchanged items trains readers to skim — and skimming readers miss the week something changes.
- A blocker line without a named person and a specific ask is a complaint, not an escalation. "Blocked 4 days" signals urgency better than any adjective.
- Status word definitions live in SKILL.md Rule 7; the first buffer slip is "At risk", not "On track with challenges".

## Meeting Brief

Pre-read sent before the meeting — the day before, not the morning of, or nobody reads it.

```
📋 MEETING: [Title] — [Date/Time]

🎯 PURPOSE
[Why this meeting exists — 1 sentence]

👥 ATTENDEES
[Key people and their role in this meeting]

📝 CONTEXT
[What changed since last time — delta only]

❓ DECISIONS NEEDED
• [Decision phrased as a question with options]

📎 PRE-READ (if any)
[Links, each with why it matters]

✅ PREP CHECKLIST
• [ ] [Item doable in minutes — longer items won't get done]
```

Principles:
- Phrase decisions as choices, not topics: "Choose vendor A or B" gets decided; "Vendor discussion" gets discussed.
- A meeting brief with no decisions-needed section is a signal the meeting could be this brief instead.

## Handoff Brief

For knowledge transfer, context passing, onboarding.

```
📋 HANDOFF: [Subject]

⚡ STATE
[Current state in 2-3 sentences]

🗺️ KEY CONTEXT
• [Important context]
• [Why things are the way they are — protects deliberate decisions from being "fixed"]

⚠️ GOTCHAS
• [Non-obvious thing that could bite them]

📌 PRIORITIES
1. [Most important next thing]
2. [Second]
3. [Third]

🔗 RESOURCES
• [Relevant doc]
• [Key contact for questions]

❓ OPEN QUESTIONS
• [Unresolved item + your current best guess]
```

Principles:
- Gotcha test: it cost YOU (or someone) real time. If it never bit anyone, it's context, not a gotcha.
- Open questions carry your best guess — a bare question transfers work; a question with a hypothesis transfers judgment.
- "Why things are the way they are" outranks achievements: the successor will be tempted to undo deliberate choices that look like mistakes.

## Decision Brief

For structured decision support.

```
📋 DECISION: [What needs to be decided]

⚡ RECOMMENDATION
[Your recommended choice — 1 sentence]

📊 OPTIONS (2-3, always including do-nothing)

**Option A: [Name]**
• Pros: [benefits]
• Cons: [drawbacks]
• Risk: [Low/Med/High — name the actual failure, not just the label]

**Option B: Do nothing**
• Cost of the status quo: [what it actually costs to wait]

⚖️ KEY TRADEOFFS
[What you're trading between options]

🎯 WHY [RECOMMENDATION]
[2-3 sentences]

⏰ DEADLINE
[Date + what is lost if it passes: "Decide by Fri or the vendor slot moves to Q4"]
```

Principles:
- Do-nothing is always an option and always has a price; presenting exactly two alternatives frames a false binary.
- Mark the decision reversible or irreversible (two-way vs one-way door, Bezos): reversible + cheap → short brief, recommend and move; irreversible → fuller evidence, and say why the extra length is there.
- A deadline without a consequence is a suggestion. State what expires.

## Incident Brief

Live status during an outage or crisis. Cadence beats completeness: a thin update on schedule beats a full update late.

```
🚨 INCIDENT: [Name] — Update #N — [Time + timezone]

⚡ STATUS: [Investigating / Identified / Mitigating / Resolved]

📉 IMPACT
[Who/what is affected, in user terms — "checkout failing for EU users",
never "pod restarts in cluster B"]

🔎 WHAT WE KNOW
• [Fact — timestamped. Facts only.]

🛠️ WHAT WE'RE DOING
• [Current action] — [owner]

⏰ NEXT UPDATE: [Committed time — send it even if nothing changed]
```

Principles:
- Missing your committed next-update time is its own incident: readers assume the worst in silence.
- Never speculate on cause in writing mid-incident — "under investigation" is a complete sentence; root cause belongs to the postmortem, not update #2.
- Number the updates (#1, #2...) so late joiners know what they missed; keep every edition self-standing (impact restated, not "see above").
- Resolved edition closes the loop: duration, final impact, where the postmortem will land.

## Board Brief

Periodic update to a board, investors, or steering group.

```
📋 BOARD UPDATE: [Company/Project] — [Period]

⚡ HEADLINE
[One sentence you would still stand behind next quarter]

📊 METRICS vs PLAN
[Each metric: actual, vs plan, vs prior period — same metrics,
same order, every edition]

⬇️ LOWLIGHTS
• [What went wrong or is at risk — before highlights]

⬆️ HIGHLIGHTS
• [What worked]

🎯 ASKS
• [Specific: an intro, an approval, a decision — with a date]
```

Principles:
- Lowlights before highlights: a board that discovers buried bad news discounts every future highlight you send.
- The asks are the point — a board holds capital, connections, and sign-off; an update without asks wastes the one resource it offers.
- Metric definitions stay constant across editions; a redefined metric is flagged in the line itself ("counting X differently as of this quarter").
- Send with the agenda, days before the meeting, not hours (`delivery.md` timing).

## Research Brief

Findings that must become a decision — user research, market analysis, technical investigation.

```
📋 QUESTION: [What we needed to learn]

⚡ ANSWER
[Direct answer + confidence: high/medium/low, and what evidence
would change it]

🔍 KEY FINDINGS
• [Finding — tagged (evidence) or (interpretation)]

⚠️ CAVEATS
[Sample size, staleness, method limits — only ones that could
flip the answer]

🎯 SO WHAT
[The decision this enables or changes, and your recommendation]
```

Principles:
- Evidence and interpretation never share a bullet: "7 of 9 users failed checkout (evidence); the flow is too long (interpretation)".
- Confidence without "what would change it" is a vibe. Name the observation that would flip the answer.
- Findings that don't touch the decision go to an appendix or die — a research brief is not a findings dump.

## Prose-Memo Variant

For narrative-memo cultures (silent group read before discussion). Same reverse-order content, rendered as prose:

- Paragraph 1 = bottom line + ask. The memo must survive a reader who stops after it.
- Paragraphs 2-4 = key points, one per paragraph, topic sentence first.
- Context follows in SCQA order; headings optional, structure identical to the bullet version.
- Length: same `default_length` budget — narrative is a rendering choice, not a license to run long.
