# Phase 4 — Debugger

Deep-dive on the Debugger phase. Read this when Phase 3 validation has failed.

## Purpose

Phase 4 is **bounded debugging with documentation**. Its job is to keep debugging from turning into thrashing.

The failure mode it prevents: 12 attempts, no log, no escalation, agent gives up with "I can't figure this out" after burning half the context window. The pipeline caps attempts at 3 and requires every attempt to be documented with a hypothesis, a change, a result, and a reason for failure.

## Hard Rules

### 1. Max 3 Attempts

After 3 failed fixes, STOP. Surface the full attempt log to the user. Do not start a 4th attempt unless the user explicitly authorizes it.

Why 3 is the cap:

- 1 attempt: the obvious fix didn't work — probably a wrong hypothesis
- 2 attempts: a new hypothesis, different approach — still not working
- 3 attempts: you've tested two distinct hypotheses, both wrong — you don't understand the system well enough to fix it alone

At attempt 4, the cost of continuing (context burn, further entrenchment in wrong model) exceeds the cost of asking for help.

### 2. Document Every Attempt

Every attempt — even failures — must be logged. Use this template:

```markdown
### Attempt N
- **Hypothesis**: What I believe is wrong now (one sentence)
- **Change**: What I modified (specific files/lines)
- **Result**: What happened — exact error output, unchanged behavior, new symptom
- **Why it failed**: The actual root cause of this failure
- **Next direction**: What to try next OR "escalate"
```

Log location: `.pipeline-state/attempts-<task>.md` if available, otherwise inline in chat.

The log has two purposes:

1. **Prevent repetition** — you can see what you already tried
2. **Enable escalation** — when you hand off to the user or `systematic-debugging`, the log is the handoff artifact

### 3. Never Repeat a Fix

If attempt 1 modified file X by changing Y to Z, attempt 2 cannot modify file X by changing Y to Z'. Every attempt must be **substantively different** — different file, different approach, different hypothesis.

Minor variations of the same fix are not different attempts. They are the same attempt with noise.

### 4. Every Attempt Needs a New Hypothesis

"Let me just try again" is not a hypothesis. Before attempt N+1, answer:

- **Why did attempt N fail?** (the actual root cause of the failure, not just "didn't work")
- **What does that tell me about the system?**
- **What's my new hypothesis for the real cause?**

If you can't answer those three, you're not ready for attempt N+1.

## Attempt Log — Worked Example

```markdown
### Attempt 1
- **Hypothesis**: Login redirect loops because middleware runs before next-auth sets its cookie
- **Change**: src/middleware.ts — added skip condition for /api/auth/* routes
- **Result**: Redirect loop continues, but now /api/auth/callback is reachable (network tab shows 302)
- **Why it failed**: The hypothesis was half-right — middleware DID block the callback, but the real cause is that next-auth is using secure: true cookies in dev, and the dev server is http://
- **Next direction**: Set cookie to secure: process.env.NODE_ENV === 'production' in next-auth config

### Attempt 2
- **Hypothesis**: next-auth cookies are secure: true in dev, blocking the auth cycle on http://
- **Change**: src/auth/next-auth-config.ts — made cookie secure conditional on NODE_ENV
- **Result**: Dev works. But now production shows the same redirect loop again.
- **Why it failed**: Production has its own issue — NEXTAUTH_URL env var is missing on Railway, so next-auth computes the wrong callback URL
- **Next direction**: Add NEXTAUTH_URL=https://caresys-omega.vercel.app to Railway env vars
```

Attempt 3 either succeeds or escalates.

## Escalation — What to Surface

When 3 attempts are exhausted, surface this to the user:

1. **The original Phase 1 hypothesis**
2. **All 3 attempt logs** (verbatim from the template)
3. **What you now believe is true about the system** (based on what you learned from failures)
4. **Specific questions for the user** — what you need to know to make progress
5. **Optional: handoff to `systematic-debugging`** — the full investigation protocol

Example escalation message:

> **Phase 4 exhausted after 3 attempts.**
>
> Original hypothesis: *login redirect loops because middleware runs before next-auth sets its cookie*
>
> **Attempts:**
> 1. [log]
> 2. [log]
> 3. [log]
>
> **What I now know:**
> - Dev works after attempt 2
> - Production NEXTAUTH_URL is set but redirect still loops
> - The Vercel function logs show the callback reaching next-auth, but the session cookie isn't being set on the response
>
> **Questions for you:**
> - Can you share a Vercel function log from a fresh login attempt?
> - Is there a custom `cookies()` config in production that I'm missing?
> - Should I hand this off to `systematic-debugging` for a deeper investigation?

## Recovery Trigger — New Cycle Instead of Continuing

If during Phase 4 a **fundamentally new hypothesis** emerges — not a refinement, but a different model of what's wrong — return to **Phase 1**, not Phase 2. A new hypothesis means a new cycle.

Example:

- Started with: *"Login fails because cookies aren't being set"*
- Attempt 1 + 2 fail
- You realize: *"Actually, the login API isn't being called at all because the fetch URL is wrong"*

That's a completely different model. Return to Phase 1, write a new hypothesis, start fresh. Don't try to patch your way from the old model to the new one.

## Integration with `systematic-debugging`

When Phase 4 escalates, the next step for complex investigations is the `systematic-debugging` skill. Its protocol picks up where Phase 4 leaves off:

- The Phase 4 attempt log becomes the "what has been tried" section
- The systematic-debugging skill adds structured investigation, parallel hypothesis testing via sub-agents, and deeper instrumentation

If `systematic-debugging` is installed, hand off with a message like:

> Invoking systematic-debugging with Phase 4 attempt log as input.

## Integration with `self-improving-agent`

After every failed attempt in Phase 4, log the learning to `.learnings/ERRORS.md`:

```markdown
## [ERR-YYYYMMDD-XXX] <task-name>

**Priority**: high
**Status**: pending

### Summary
Phase 4 attempt N failed — <one line>

### Error
<redacted error output>

### Context
- Phase 1 hypothesis: <original>
- Attempt N hypothesis: <updated>
- What we learned: <key insight>

### Suggested Fix
If identifiable.
```

This way, next time a similar bug appears, the next session starts with that knowledge instead of repeating the dead ends.

## Common Failures

- **No attempt log** — trying fixes without writing down what was tried or why it failed
- **Repeated fixes** — attempt 2 is a minor variation of attempt 1
- **Unbounded debugging** — going past 3 attempts without escalating
- **Silent give-up** — stopping without surfacing the log to the user
- **Missing hypothesis** — "let me just try…" without a new model
- **Patch through failures** — pretending attempt N "kind of worked" and building on top

Each of these makes the handoff to the human useless when it eventually happens.
