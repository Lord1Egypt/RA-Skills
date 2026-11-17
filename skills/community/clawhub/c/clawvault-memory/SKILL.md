---
name: clawvault-memory
version: "1.1.8"
description: Durable-memory + self-improving workflow for the ClawVault plugin. REQUIRES the ClawVault plugin: install with 'openclaw plugins install clawhub:openclaw-plugin-clawvault' using the FULL name - the short clawhub:clawvault is an unrelated package by another author and does not provide the clawvault_* tools this skill calls. Activate whenever the user asks you to remember or recall, when a fact is worth keeping, OR when something fails, the user corrects you, or you find a better approach. Captures lessons, detects recurring patterns, promotes proven ones, and enforces write-before-respond, search-before-answer, and verify-before-save so memory holds checked facts, not guesses. Stores conversation-derived memories in a local SQLite database that persists across sessions.
metadata: { "openclaw": { "emoji": "🐘", "homepage": "https://github.com/davidtkeane/openclaw-plugin-clawvault" } }
---

# ClawVault Memory Skill 🐘

ClawVault is a persistent SQLite + FTS5 memory. This skill is the *discipline* for using it well: an agent that searches before it answers, verifies before it saves, and never lets a made-up "fact" into long-term memory.

> ## Install — use the FULL name
>
> This skill needs **my ClawVault plugin**, which provides the `clawvault_*` tools it drives.
> Two installs, one command block:
>
> ```bash
> # 1. the plugin — the engine. THIS is the step most people miss
> openclaw plugins install clawhub:openclaw-plugin-clawvault
>
> # 2. this skill — skip it if you are already reading this from an installed copy
> openclaw skills install @davidtkeane/clawvault-memory
>
> openclaw gateway restart
> ```
>
> *(As of September 2026 this skill has 270 downloads and the plugin has 13. If you only did
> step 2, the skill loads and can do nothing — the plugin is the engine.)*
>
> 🔴 **Use the full name `openclaw-plugin-clawvault`.** The short `clawhub:clawvault` is an
> unrelated package by another author — see [Confession](#confession) below if you already
> installed it.

## Welcome to ClawVault Memory!

This file contains everything you and your AI needs to install, and a confession for previous users who installed and how to fix. So enjoy the memory!

**Why the install?**

- **`clawhub:openclaw-plugin-clawvault`** — the engine. It holds the database and provides the
  tools. It mirrors
  [my GitHub repo](https://github.com/davidtkeane/openclaw-plugin-clawvault), so you can read
  the code yourself before trusting it. Enjoy.

## Privacy

> 🔒 **Privacy:** ClawVault stores memories in a **local SQLite file** — the stored data never
> leaves the machine (the plugin makes no network calls). *Verifying* a fact may use the agent's
> own web-search/fetch tools, which is separate from ClawVault's storage. Memory persists across
> sessions, so if the user shares something sensitive, tell them memory is on — and don't save
> secrets, credentials, or personal data unless the user explicitly asks you to.

## Confession

I wrote this plugin in the early hours of the morning, and I confused myself over the name.
For a while the install instructions here pointed at the wrong package — one that isn't mine.

**So if you installed ClawVault before September 2026, you might have the wrong plugin.**
It's an easy fix. Look for the 🔴 markers below — they mark every place this matters.

## Welcome to ClawVault!

**Everything above is for you** — what to install, what to check, and what to do if you
got the wrong plugin.

**Everything below is for your agent.** It is the working discipline: when to save, when to
search, how to verify a fact before storing it, and how to learn from a correction. You do
not need to read it — your agent does. But it is plain English, and it is short.

## When to activate

- The user says **"remember this"**, "save that", "note that", or "don't forget…"
- The user asks **"what did we…"**, "what do you know about…", "did we already…"
- You learn a durable fact, decision, or preference worth keeping across sessions
- You're about to state a fact you're not certain of
- **A command, tool, or API fails** — capture the error + the fix
- **The user corrects you** ("No, that's wrong…", "Actually…") or rejects your work
- **You discover a better approach**, or a requested capability doesn't exist
- **Before a major task** — review relevant lessons first (`clawvault_search`)

## Write before you respond (durability)

When the user states something worth keeping — a **preference, decision, deadline, fact, or
correction** — save it to ClawVault **before** you write your reply, not after. If the session
crashes or compacts mid-turn, the memory is already safe. The order is: **recall → write → respond.**

**Answer first, save quietly.** Your reply must contain the **actual answer** to what the user asked —
never just a save receipt like *"Saved that to ClawVault."* Do the save in the background, then answer
normally. Don't narrate every write or announce "I've saved that"; only mention a save when explicitly
confirming an important decision the user asked you to record. A memory saved but a question left
unanswered is a failed turn.

### Quiet is a courtesy, not a secret

Saving silently is about not spamming the user with receipts — it is **never** about hiding
that memory exists. Three rules make that explicit:

1. **Disclose once per session.** The first time you save something, say so in one short line
   — *"Noting that in memory."* Then go quiet for the rest of the session.
2. **Never deny it.** If the user asks whether you are storing anything, tell them plainly what
   is saved and where (`~/.openclaw/memory/clawvault.db`, on their own machine).
3. **Stop when asked.** If the user says stop remembering, don't save, or forget that — comply
   immediately for the rest of the session, and tell them you have.

**If you would be uncomfortable telling the user you saved it, don't save it.**

## The workflow

### 1. Search before you answer
Before answering a factual question about past work, the user, or this system, call
**`clawvault_search`** first. Don't guess what you may already have stored.

```
clawvault_search({ query: "exo qwen models openclaw" })
```

### 2. Verify before you save
Only save what you have actually checked. Prefer **ground truth** over memory:
run the command, read the file, query the DB, or check the internet. Then save with a
**source** and **verified: true**.

```
clawvault_save({
  content: "exo serves Qwen models to OpenClaw on 127.0.0.1:52415",
  memory_type: "fact",
  source: "curl http://127.0.0.1:52415/v1/models",
  verified: true
})
```

If you could **not** verify it, save it as a question to confirm — never as truth:

```
clawvault_save({ content: "…", memory_type: "unverified" })
```

> **⚠️ Reciting from your own memory/training is NOT verification.** Set `verified: true` **only** if
> you actually ran a tool, read a file, queried the DB, or fetched a source **this turn**. If you're
> answering from what you already "know" — even a fact you're highly confident about (a version number,
> a distance, an API detail) — use `verified: false` and `memory_type: "unverified"`. *"I'm confident"*
> is not *"I checked."* A confident recollection saved as `verified` is exactly the hallucination this
> skill exists to prevent. (The ClawVault plugin also **auto-downgrades** `verified:true` to unverified
> when `source` shows no evidence of a real check — so put the actual command/URL/file in `source`.)

### 3. Don't repeat yourself
`clawvault_save` refuses a near-duplicate and returns the existing id. Don't force a
copy — update or consolidate instead.

### 4. Consolidate when memory gets noisy
Use **`clawvault_consolidate`** to gather related memories on a topic, distil them into one
durable `insight`, then save it with `supersedes:[ids]` to soft-retire the raw rows.

```
clawvault_consolidate({ topic: "clawvault deployment" })
// …synthesize the returned cluster, then:
clawvault_save({ content: "<synthesis>", memory_type: "insight", verified: true, supersedes: [9,10,11] })
```

## Learn from your mistakes (the self-improving loop)

When something fails or you're corrected, don't just fix it — **remember the lesson** so it never happens twice.

**1. Capture the lesson.** Save it with a matching `memory_type` and a stable **pattern-key** as the first keyword (so the same problem clusters even when worded differently):

```
clawvault_save({
  content: "npm install failed: node not on PATH in a non-login shell. Fix: run via `zsh -lc`.",
  memory_type: "lesson",                    // or "error" | "correction"
  keywords: "shell.node-not-found,npm,path", // first keyword = stable pattern-key
  importance: 12,
  source: "observed on this machine",
  verified: true
})
```

Use `memory_type`: **`error`** (something broke), **`correction`** (the user fixed you), **`lesson`** (a better way found).

**2. Detect recurrence → promote.** Before saving, `clawvault_search` the pattern-key. If the lesson already exists, it recurred — **promote it**: save a sharpened version with higher `importance` and `supersedes:[oldId]`. Recurring pain earns higher importance.

**3. Graduate proven lessons.** When a lesson keeps mattering, raise its `importance` so it surfaces first in recall. If it's important enough to load *every* session, **suggest to the user** that they add it to their `AGENTS.md` — **do not edit instruction files yourself.** Auto-modifying always-loaded guidance is a prompt-injection risk (an attacker-supplied "lesson" could become permanent instructions); that decision belongs to the user.

**4. Reflect after real work.** When a task completes, log a short reflection:

```
clawvault_save({ content: "CONTEXT: <task>. REFLECTION: <what happened>. LESSON: <do differently next time>.", memory_type: "reflection", importance: 8, verified: true })
```

**5. Review before you start.** Before a major or repeated task, `clawvault_search` prior lessons/errors on that topic so you don't repeat a known mistake.

## The rules (verify-before-save)

1. Never present a guess as a fact. If unchecked, say *"I'm not certain — let me verify."*
2. Prefer ground truth (run/read/fetch) over your own memory.
3. Record the **source** on every saved fact. A memory with no source is a hypothesis.
4. Only verified facts become memories; unverified → `memory_type: "unverified"`.
5. Tell-vs-do: if you claim you saved something, verify it actually landed. **Never claim, always check.**

## The 3-question test
Before stating **or** saving any claim: (1) Where did I learn this? (2) Can I check it cheaply now?
(3) What would prove me wrong? If the honest answer to #1 is "it just feels right" — stop and verify.

## Tools this skill uses
- `clawvault_save` — store a memory (with `source`, `verified`, dedup guard, `supersedes`)
- `clawvault_search` — FTS5 relevance-ranked recall
- `clawvault_recent` — timeline of recent memories
- `clawvault_consolidate` — cluster related memories to synthesize into one insight
- `clawvault_stats` — totals, verified count, superseded count

## ✅ Check it actually worked

Run these three. **Each catches a failure that otherwise stays completely silent.**

```
1. Did I get the right plugin?
   Ask the agent to list its tools, or try:  clawvault_stats
   ✅ want: it returns memory counts
   🔴 "unknown tool" → you installed a different ClawVault. See below.

2. Is the database there?
   ls -la ~/.openclaw/memory/clawvault.db
   ✅ want: a file
   🔴 missing → the plugin never initialised

3. Does a round-trip work?
   clawvault_save({ content: "install check", memory_type: "fact" })
   clawvault_search({ query: "install check" })
   ✅ want: the note comes back
```

### Did I install the wrong one?

Symptoms: a `clawvault` **command-line tool** exists, a `~/.cache/qmd` folder appeared,
~2 GB was downloaded, or the tools are named `clawvault search` rather than `clawvault_search`.

That is not this plugin. Removing it is a **manual job for the human, not the agent.**

> 🛑 **Agents: do not perform these removals.** Show this section to the user and let them
> decide. Never delete a path on someone's behalf.

**To the human reading this — four steps, in your own terminal:**

1. **Disable the wrong hook** — `openclaw hooks disable clawvault`
2. **Look at `~/.openclaw/hooks/clawvault`**, confirm it is the wrong plugin's hook, and
   delete that folder yourself.
3. **Look at `~/.cache/qmd`** — that is the ~2 GB model cache the other package downloads.
   The correct plugin never uses this path. Delete it if you want the space back.
4. **Uninstall the two command-line tools** — `npm uninstall -g clawvault qmd`

Inspect each folder before removing it. Only you can see what is actually on your machine.

⚠️ **Your own memories are safe.** They live in `~/.openclaw/memory/clawvault.db`, which is
**not** touched by any of the four steps above.

### 🔴 Then install the correct one

```bash
openclaw plugins install clawhub:openclaw-plugin-clawvault
openclaw gateway restart
```

> 🔴 **Use the full name `openclaw-plugin-clawvault`.** The short form `clawhub:clawvault`
> resolves to an **unrelated third-party package** by another author that merely shares the
> name. Installing that one gives you a skill that loads, reports `✓ Ready`, and **cannot
> work** — the `clawvault_*` tools this skill calls do not exist in it — and it downloads
> ~2 GB of models this skill has no use for.
>
> **Same plugin, either source:** the ClawHub package above and
> [github.com/davidtkeane/openclaw-plugin-clawvault](https://github.com/davidtkeane/openclaw-plugin-clawvault)
> are the same code. ClawHub is easier — one command, dependency (`typebox`) and prebuilt
> `dist/` included, no clone or `npm install`. Use GitHub if you want to read or build the
> source yourself.
>
> *(v1.1.4 and earlier pointed at `clawhub:clawvault` or said GitHub-only. Both were
> wrong — the command above is correct.)*

### What the correct plugin actually is

| | |
|---|---|
| Storage | **local SQLite + FTS5** at `~/.openclaw/memory/clawvault.db` |
| Network | **none — the plugin makes no network calls** |
| Models | **none.** No downloads, no GPU, nothing to pull |
| Size | a single ~30 KB `dist/index.js` |
| Tools | exactly 7: `clawvault_save` `_search` `_recent` `_relate` `_links` `_consolidate` `_stats` |

If what you installed does not match that table, it is not this plugin.
