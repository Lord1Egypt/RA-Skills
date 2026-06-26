# Starter Patterns

These are the baseline patterns. If an agent is missing these, fix them before adding anything fancier.

## 1. WAL Protocol (Write-Ahead Log)

**Failure mode:** A human gives a correction, preference, decision, or exact value. The agent acknowledges it, but compaction wipes the detail.

**Pattern:** Write to memory **before** responding when the human message contains any of these:
- corrections — "It's X, not Y" / "Actually..."
- proper nouns — names, places, companies, products
- preferences — likes, dislikes, styles, approaches
- decisions — "Let's do X" / "Go with Y"
- exact values — numbers, dates, IDs, URLs

```markdown
### WAL Protocol
When the human's message contains ANY of these, WRITE to daily memory BEFORE responding:
- ✏️ Corrections — "It's X, not Y" / "Actually..."
- 📍 Proper nouns — Names, places, companies, products
- 🎨 Preferences — "I like/don't like", styles, approaches
- 📋 Decisions — "Let's do X" / "Go with Y"
- 🔢 Specific values — Numbers, dates, IDs, URLs

Write first, respond second.
```

## 2. Anti-Hallucination Rules

**Failure mode:** The agent invents tasks, alerts, or emails because context feels sparse or compacted.

**Pattern:** Every reported item needs a source from the current session.

```markdown
### Anti-Hallucination Rules (CRITICAL)
- NEVER invent tasks, alerts, or emails not verified in the CURRENT session
- If not confirmed by a tool call, DO NOT report it
- NEVER rely on compacted memory for data — ONLY fresh tool results
- If you cannot verify something: OMIT IT. Silence > hallucination.
- No checks returned anything? Say "nothing to report." Don't fill silence.
```

## 2a. Isolated Agent Fabrication Guard (Crons & Sub-Agents)

**Failure mode:** A cron or sub-agent runs in an isolated session with no main agent oversight. Its prompt asks it to "report on X." The API call fails or returns empty. Instead of surfacing the error, the LLM fabricates plausible-looking data — names, numbers, dates — because it was trained to be helpful. The fabrication is delivered directly to the human before anyone can verify it.

**Why the main-session Anti-Hallucination rules don't cover this:** Those rules apply to the orchestrating agent in a live session. Crons are isolated — the orchestrator never sees the output before delivery. The guard must live in the cron prompt itself.

**Pattern:** Add this block to the end of every cron or sub-agent prompt that reports real-world data (bookings, email, health, finance, calendar, APIs):

```markdown
## CRITICAL: Real-World Data Verification Rule
This task reports external data (APIs, email, bookings, health, finance, etc.).

BEFORE reporting any data:
1. Make the actual API/tool call and get a real response
2. If the call fails, errors, or returns empty: output ONLY "DATA_UNAVAILABLE — [reason]". Do NOT generate plausible-looking data.
3. NEVER invent names, numbers, dates, amounts, or statuses not returned by a live tool call
4. If you cannot verify data with a tool in this session, say so explicitly

Hallucinated data is worse than no data. Silence is always safer than fabrication.
```

**Applies to:** Any agent that runs on a schedule or as a sub-agent and delivers output to a human without going through an orchestrator review step first.

**Real incident:** A Lodgify Booking Monitor cron fabricated three guest names, arrival/departure dates, and cancellation statuses — none of which existed. The fabrication was delivered directly to the operator via Telegram. (2026-03-27)

## 3. Ambiguity Gate

**Failure mode:** A vague request gets interpreted too aggressively, especially around deletion, config changes, or outbound communication.

**Pattern:** When a request has multiple reasonable interpretations, stop and confirm.

```markdown
### Ambiguity Gate
When a request has multiple reasonable interpretations — STOP.
State your interpretation and confirm before acting. Especially for:
- File operations — "clean up" could mean organize or delete
- Email sends — "follow up" could mean different recipients or tones
- Config changes — "fix this" could mean different approaches
- Destructive actions — anything that changes state irreversibly

The test: "Could a reasonable person read this differently?"
If yes, clarify first. Silence is not consent; ambiguity is not permission.
```

## 4. Simple Path First

**Failure mode:** The agent reaches for a complex stack before testing the obvious direct path.

**Pattern:** Try the dumbest viable path first.

```markdown
### Simple Path First
1. Test the simplest approach first
2. curl before MCP. Direct CLI before wrapper. Raw API before SDK.
3. If the simple version works — ship it.

### Try Before Explaining
When the human asks "can you do X?" — just try it. Show the result or the error.
```

## 5. Unblock Before Shelve

**Failure mode:** Work gets parked for days because nobody spent ten focused minutes checking the real blocker.

**Pattern:** Investigate before shelving.

```markdown
### Unblock Before Shelve
Before shelving a blocked task:
1. Spend 10 minutes on the actual blocker
2. Config toggle? Missing login? Billing checkbox?
3. If fix < 15 minutes, do it instead of shelving
4. If genuinely blocked, log the specific blocker and expected resolution
```
