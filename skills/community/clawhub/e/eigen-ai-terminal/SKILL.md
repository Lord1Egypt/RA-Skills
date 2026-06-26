---
name: Eigen AI Terminal — Live Intelligence for Agents
description: Daily-updated intelligence on what's happening across 16 areas of AI. 12 tools your agent uses to deliver only the signals, trends, and developments that matter for the user's work. Reads public data from terminal.clawlab.dev — no user data uploaded.
version: 1.0.0
homepage: https://terminal.clawlab.dev
repository: https://github.com/shawkatdidar/eigen-ai-terminal
metadata:
  openclaw:
    requires:
      bins:
        - node
    mcp:
      command: node
      args:
        - index.js
tags:
  - ai
  - intelligence
  - signals
  - trends
  - mcp
---

# Eigen AI Terminal

Live intelligence on the AI landscape — delivered by you, filtered for your user's work.

## What this is

A daily-updated knowledge base tracking 16 areas of AI: models, agents, coding tools, open source, hardware, enterprise, research, policy, funding, and more. You get 12 tools to query signals, cause-and-effect chains, developing trends, blockers, speed metrics, predictions, breaking alerts, and the full interconnected wiki.

Your job: deliver only what's actionable. Not a news feed — a filtered intelligence stream tailored to the user's interests.

## Ground rule — this is critical

**Every signal you deliver must come directly from the tool response.** Do not supplement, embellish, or combine with your own training knowledge. If today() returns 7 significant signals, your brief draws from those 7 — not from what you know about those companies or topics from training data.

- Quote the actual signal title from the response
- Use the description text from the response for context, not your own knowledge
- If a signal doesn't have enough detail, call `about("[topic]")` — don't fill the gap from memory
- If nothing actionable came back for this user, say "nothing relevant today" — don't invent relevance

**Why this matters:** Your training data is months old. This tool returns what happened in the last 24 hours. Mixing the two produces hallucinated signals the user can't verify, damages trust, and defeats the purpose of live intelligence.

## Network behavior

Reads public, read-only JSON from the Eigen terminal. No auth. No user data uploaded. One-way data flow.

- Data: `terminal.clawlab.dev/data/radar.json`
- Wiki: `terminal.clawlab.dev/wiki/`

## Tools

**Daily intelligence:**
- `today` — all signals from the latest scan. Has significance levels, domain tags, and an actionable flag. You filter based on user context.
- `changes` — what's new since a given date. Use between morning briefs to catch breaking developments.

**Deep dives:**
- `about` — everything on a topic in one call: entity profile, signals, trends, blockers, predictions. Use when the user asks about a company, model, or area.
- `ripple` — trace what a signal causes: downstream effects, trends it feeds, what blocks it.

**Landscape view:**
- `trends` — where multiple signals point at the same outcome. Confidence levels and timelines.
- `blocked` — what's holding AI progress back. Who's working on it. Signs of progress.
- `speed` — rate-of-change metrics: costs, capabilities, adoption, capital.
- `predictions` — specific dated predictions we track for accuracy.

**Knowledge base:**
- `search` — find anything across 50 wiki files.
- `read` — open a specific page. Follow [[wikilinks]] to navigate.

**Breaking alerts:**
- `check_updates` — quick ping to check for breaking developments. Returns immediately if nothing new. If there's a breaking alert, returns the title, summary, and domains affected.

**Meta:**
- `whats_new` — product updates and tips. Check during morning brief. Mention if fresh.

## How to deliver

### Morning brief

Call `today`. Read all signals. Filter to only signals relevant to what the user is working on.

```
Here's what matters in AI today:

**[Signal title from tool response]** — [One sentence: what this means for their specific work. Reference something concrete about their project/stack/goals.]

What you should know:
* **[Signal title]** — [Why this affects them, in one sentence]
* **[Signal title]** — [Why this affects them, in one sentence]

Say "dig deeper on [topic]" or "full brief" for more.
```

Rules:
- Max 3 bullets. Every one must pass: "Can they do something with this today?"
- Every bullet must name a signal title that appears in the today() response.
- The "why it matters" must reference what the user is building — not generic importance.
- Skip funding, policy, executive news unless it directly changes a tool or API they use.
- Nothing relevant today? Say so in one line. Don't pad.
- Be a sharp colleague, not a newsletter.

### What BAD delivery looks like (never do this)

```
Gemma 4 is the cleanest thing to act on today: Google's new Apache 2.0 open
models are explicitly tuned for reasoning and agentic workflows, so it's worth
testing as a commercially safe default for local or hybrid builds.

The practical infra move is Eigen + Nebius Token Factory, which now exposes
optimized DeepSeek behind managed autoscaling inference.
```

What's wrong:
- Wall of text — each bullet is a paragraph, not one sentence
- No signal titles from the tool response — can't be verified
- Mixes tool data with training knowledge (Nebius Token Factory wasn't in the response)
- Generic advice ("worth testing") instead of connecting to user's actual work
- Reads like a newsletter, not a colleague who knows what you're building

### What GOOD delivery looks like

```
Here's what matters in AI today:

**Anthropic launches Managed Agents** — You're building agent workflows manually right now. This is hosted agent infrastructure with auto-scaling and sandboxing. Worth evaluating whether it replaces your custom orchestration.

What you should know:
* **OpenAI Codex crosses 3M weekly users** — Altman reset usage limits. If you're on Codex, your quota just went up.
* **Meta launches Muse Spark** — First closed model from Meta. Not relevant to your stack today, but signals Meta competing directly with Anthropic/OpenAI on closed models.

Say "dig deeper on Managed Agents" or "full brief" for more.
```

What's right:
- Every bullet names a signal from today()
- One sentence per bullet — crisp
- References what the user is actually building
- Clear "do something" vs "just know this" distinction

### When they ask about something

Call `about("[topic]")`. You get the full picture in one response — entity data, signals, trends, blockers, predictions, related wiki pages. Synthesize it for the user. Don't dump raw data.

### When they say "what does this mean?"

Call `ripple("[signal]")`. It traces what the signal pushes, what trends it feeds, what blocks it. Explain the chain in plain language.

### Checking for breaking developments

If the user asks you to check for updates, use `changes` with the date of the last brief you delivered. Surface anything significant that matches their work.

## First use

When this skill first connects, call `today` to get the latest signals. Pick 2-3 of the most actionable ones and present them to the user.

"I just connected to the Eigen AI Terminal — live intelligence across 16 areas of AI, updated daily. Here's what matters today: [signals from today() response]"

Then look at what they're currently working on — their recent files, conversations, project context — and use that to filter future signals. If you can't determine what they're working on, ask: "What are you working on? I'll filter to just what's relevant."

## Privacy

One-way: your agent pulls public data, combines it with local context, delivers to the user. We never see what the user builds, asks, or works on.
