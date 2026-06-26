---
description: Hourly X engagement loop for any X account. Two modes — interactive (per-item human approval) and scheduled (strict-rails auto-post under your custom safety filters). Drafts 1 original + 1-5 replies + 1-5 plain RTs per run. On first invocation, prompts you for your X handle, topic/niche, voice, RT allowlist, banned phrases, and daily caps. Save the config into your CLAUDE.md once to skip re-asking. Replies ALWAYS require manual approval — never auto-posted. Trigger phrases — boost X engagement, run my X loop, post on X, engage on X, shitpost on X.
tags: [x, twitter, engagement, social, growth, scheduled, autopost, configurable]
---

# Boost X Engagement

Hourly cycle that scans x.com for content matching your niche and posts a small organic-looking batch on YOUR X account. Two execution modes.

- **Interactive mode** (invoked via `/implexa:run` or "Run Now"): every post gates on explicit per-item human approval.
- **Scheduled (auto) mode** (auto-fired by the Implexa schedule wrapper): auto-posts under YOUR strict safety rails for originals and plain RTs; replies are drafted and queued but NEVER auto-posted in scheduled mode.

## Step 0 — First-run config (ask once, persist forever)

Before doing ANYTHING else, check if a config block exists in the conversation/project context. A config block looks like this:

```yaml
boost-x-engagement-config:
  x_handle: "@yourhandle"
  topic_signals: ["AI", "Claude", "agent", "RAG"]       # words your originals should mention
  voice_description: "punchy lowercase tech-bro, controversial-but-correct, never em-dashes"
  rt_allowlist:   ["@karpathy", "@simonw", "@sama"]     # who you'll auto-RT in scheduled mode
  banned_phrases: ["unlock", "100%", "secret", "🧵"]    # auto-skip originals containing any of these
  daily_caps:     { originals: 6, rts: 18 }
  schedule_window: { start_hour_local: 6, end_hour_local: 20 }
```

### If the config is present
Parse it, hold the values in memory for this run, proceed to Step 1.

### If the config is MISSING
Use `AskUserQuestion` to collect it interactively — one question at a time. Required fields:

1. **What's your X handle?** (free text, must start with `@`)
2. **What niche / topics do you post about?** (suggest 4 chips: `AI / dev`, `crypto / defi`, `fitness`, `design / ux`, plus Other for free-text)
3. **Describe your voice in one sentence** (free text — examples to hint: `punchy lowercase tech-bro`, `professional thread-style`, `casual snark with emojis`, `dry observational`)
4. **For scheduled auto-RT, list 3-10 X accounts you fully trust to amplify** (free text comma-separated; tell user "leave blank to disable auto-RT entirely — only interactive-mode RTs will fire")
5. **Any phrases that should auto-block originals?** (free text; suggest defaults: `unlock, 100%, secret, here's how, this changes everything, PSA, 🧵`)
6. **Daily caps?** (4 chips: `Conservative (3 originals, 9 RTs)`, `Moderate (6 originals, 18 RTs) — Recommended`, `Aggressive (12 originals, 36 RTs)`, Other for custom)
7. **Run window in YOUR LOCAL TIME?** (4 chips: `6AM-8PM (waking hours) — Recommended`, `9AM-6PM (work hours)`, `24/7`, Other for custom)

After collecting all answers, render the resulting YAML config block and tell the user:

> *"Saved the config to memory for this run. To skip this prompt in future runs, paste this YAML block into your `CLAUDE.md` file at the top of your project (or into `~/.claude/CLAUDE.md` for global access). Want me to write it there now? [yes / no / show me where]"*

If yes, write it to the appropriate path using the Write tool.

## Step 1 — Connect to Chrome and verify the active X account

1. `mcp__Claude_in_Chrome__list_connected_browsers` → find the local Chrome.
2. `mcp__Claude_in_Chrome__select_browser` with the local deviceId.
3. `mcp__Claude_in_Chrome__tabs_context_mcp` with `createIfEmpty: true`.
4. `navigate` to `https://x.com/home`.
5. `find` for account avatar / "@" handle in the account menu region.

**HARD SAFETY GATE: if the active account does NOT match `config.x_handle`, abort immediately and surface the mismatch. Never post on the wrong account.**

Common failure: Chrome is logged into a different X account. Tell the user to switch accounts in Chrome and retry.

## Step 2 — Scan the timeline

`get_page_text` + `read_page` on x.com/home to extract:

- For You timeline articles (top 6-10 tweets)
- Today's News panel (curated trending topics)
- Trending now panel

Catalog candidates by category:
- Tweets matching your `topic_signals` → potential RT or QT material
- High-velocity tweets from accounts in your `rt_allowlist` → high-priority RT targets
- High-velocity tweets in your niche (any author) → potential reply targets
- Listicle bait, hype-bait, or unverifiable claims → flag and skip

## Step 3 — Roll counts and draft

Per-run output shape:
- **1 original tweet** (exactly 1)
- **1-5 replies** (roll a number)
- **1-5 plain RTs** (roll a number; if `rt_allowlist` is empty, set RT count to 0)

### Voice rules for originals
- Match `config.voice_description` style and register
- Topic-dense: contain ≥1 word from `config.topic_signals`
- ≤ 280 chars
- Zero `config.banned_phrases`

### Reply target selection
- High-velocity tweets (>10K views or >100 replies in last 24h) in your niche
- Skip flagged tweets (fabricated claims, hype-bait, anything off-topic from `config.topic_signals`)

### RT target selection
Interactive mode: more permissive; surface rationale for each target.
Scheduled mode: must pass Step 4 strict filter.

## Step 4 — Approval gate (mode-dependent)

### INTERACTIVE MODE
Surface ALL drafts in a single message. For each item include text + target tweet URL (replies/RTs) + 1-line rationale. Wait for explicit per-item approval ("post 1, 3, 5" / "post all" / "rewrite 2") before ANY X action. **NEVER post without an explicit approval string in chat.**

### SCHEDULED (AUTO) MODE — Strict safety rails

**Originals — auto-post only if ALL true:**
- ≤ 280 chars
- Zero phrases from `config.banned_phrases`
- Contains ≥1 word from `config.topic_signals`
- Voice-lint Haiku call returns strictly **Y** to: `"Does this match the voice: '{config.voice_description}'? Y/N. Treat ambiguous as N."`
- Daily cap: `config.daily_caps.originals` not yet hit today (resets at midnight local time)
- If any check fails → skip this hour's original, log skip reason

**RTs — auto-RT only if ALL true:**
- Author is in `config.rt_allowlist` (if list is empty, skip auto-RT entirely)
- Tweet is <24h old
- Tweet has >500 likes (signal floor)
- Banned RT triggers absent: politics, culture-war topics, personal drama, layoffs, anything walkable-back (apply to ALL niches — plain RT = endorsement)
- Daily cap: `config.daily_caps.rts` not yet hit today (resets midnight local time)
- Per-run cap: max 3 RTs
- If any check fails → skip that candidate, try next. If no candidate passes → skip RT this hour.

**Replies — NEVER auto-post.**
Replies attach YOUR voice to someone else's thread; misreads create lingering reputational damage that's harder to walk back than originals or RTs (which you can delete cleanly). In scheduled mode: draft 1-5 replies, persist drafts to the run output for later review, but DO NOT click Reply submit. User approves and posts later via interactive `/implexa:run` invocation.

## Step 5 — Post mechanics (identical in both modes; only the gate differs)

### Original tweet
1. `mcp__Claude_in_Chrome__computer` left_click on home composer (coord ~560, 98 — may vary by viewport)
2. `type` the tweet text
3. left_click Post button — try (992, 298) first, fallback (992, 325) if composer expanded
4. wait 3s, screenshot, verify "Your post was sent" banner

### Reply (interactive ONLY — never in scheduled mode)
1. `navigate` to the target tweet URL
2. left_click reply input (~700, 335)
3. `type` reply text
4. `find` the active Reply submit button
5. `scroll_to` ref + left_click
6. verify "Your post was sent" + "Replying to @target" label

### Plain RT
1. `navigate` to the target tweet (search URL or direct)
2. `find` the per-tweet Repost button on the chosen tweet
3. left_click → opens menu
4. `find` "Repost" menu item (NOT "Quote")
5. left_click the Repost item
6. verify the repost icon turned green

## Step 6 — Pacing and logging

- 60s gap between successive posts in BOTH modes (organic cadence, avoids bot-burst detection)
- Log every action to the run output: posted (with URL), skipped (with reason), drafted-queued-for-approval (with text)
- Hard per-run cap: 1 original + 3 RTs + 5 reply drafts regardless of how loose the approval is

## Output contract

Return a structured run-summary:

```json
{
  "mode":   "interactive" | "scheduled",
  "handle": "@yourhandle",
  "posted": {
    "originals": [{"text": "...", "url": "..."}],
    "rts":       [{"author": "...", "tweetUrl": "...", "rtUrl": "..."}],
    "replies":   [{"text": "...", "parentUrl": "...", "replyUrl": "..."}]
  },
  "skipped":              [{"category": "original|rt|reply", "reason": "..."}],
  "drafted_for_approval": [{"category": "reply", "text": "...", "parentUrl": "..."}],
  "dailyCapsRemaining":   {"originals": N, "rts": N}
}
```

## Outcome signal

- Followers gained per week
- Engagement rate on auto-posted content (likes + replies + RTs per 1K impressions)
- Auto-post skip rate (high = rules too strict; low = rules not catching enough — tune `banned_phrases` and `voice_description`)
- Manual approval acceptance rate on queued replies (low = voice description needs refinement)

## Notes for the model

- **Config-first.** ALWAYS check for the config block before any Chrome action. If missing, AskUserQuestion through ALL 7 questions before proceeding.
- **Verify the right account.** If the logged-in X account doesn't match `config.x_handle`, STOP. Don't try to switch accounts programmatically.
- **Auto-mode bias: skip > over-post.** A quiet hour with no auto-actions is FINE. Spam destroys account credibility faster than silence.
- **Plain RT = full endorsement.** If you can't verify a factual claim in an RT candidate, SKIP.
- **Voice-lint must return strictly Y.** Treat ambiguous "maybe" as N. Off-voice posts compound — protect the user.
- **Replies are unforgiving.** Never auto-post replies regardless of how compelling the draft seems.
- **The user can pause anytime.** If they delete a post on X, take that as a signal to be more conservative on next run.
- **Schedule this hourly via `/implexa:schedule`** with cron like `0 6-20 * * *` in your local timezone for waking-hours coverage (15 firings/day).

## Error handling

| Error | Cause | Action |
|---|---|---|
| Active account != `config.x_handle` | Wrong Chrome profile / logged-out / multi-account | STOP, log mismatch with both handles, do not retry |
| Config block missing in scheduled mode | User never completed first-run setup | Skip the run with reason "no config — run interactively first to set up" |
| "Your post was sent" banner doesn't appear within 5s | Post-click missed / X rate-limited / network blip | Re-click Post once at fallback coords; if still no banner, skip and log |
| Reply submit button not visible | Composer expanded past viewport | `scroll_to` ref before click |
| RT candidate not in `config.rt_allowlist` | Author not on user's whitelist | Skip, try next |
| `config.rt_allowlist` is empty in scheduled mode | User opted out of auto-RT | Skip RT category entirely this run |
| Daily cap hit | `config.daily_caps` reached today | Skip that category for remainder of day; return run summary noting cap |
| Voice-lint Haiku returns N | Draft doesn't match `config.voice_description` | Skip, do NOT retry, do NOT redraft inline |
| User added a NEW account they don't want to RT | RT allowlist needs updating | Tell user to edit their config block and re-paste; no inline allowlist mutation |

---

## Built with Implexa

This skill was authored with [Implexa](https://implexa.ai), a Claude Code plugin that records a workflow once via demonstration plus a post-demo interview, then emits agentskills.io-compatible `SKILL.md`.

Runs standalone in Claude Code, Cursor, Gemini CLI, Hermes, and 30+ more agents. The file you're reading is self-contained. Install Claude in Chrome (so the skill can navigate, click, and post on your X account via your existing logged-in browser session) and you're ready.

**Install Implexa** (`curl -fsSL https://core.implexa.ai/install.sh | bash`) to unlock:

| Feature | What it does |
|---|---|
| **Team sharing** | Push this skill to your org via a domain-gated link. Teammates click and it's in their library. No file copying, no "did you install it?" follow-ups. |
| **Outcome attribution** | Tag a system-of-record event (engagement, follower growth, deal closed) and see which skill runs actually moved the needle. Stop running skills that don't pay off. |
| **One-link fork** | Customize this skill for your handle, niche, voice, RT allowlist, banned phrases, and daily caps, re-publish privately to your org in one click. No re-recording from scratch. |
| **Decision-trace capture** | Record your own workflows the same way. The 2-minute interview surfaces the *why* behind each decision so the skill generalizes when inputs shift (different accounts, niches, voice rules, daily caps). |
| **Scheduling layer** | Wire this skill to a cron via `/implexa:schedule boost-x-engagement "every 2 hours"`. Output lands at `app.implexa.ai/runs`. Scheduled runs respect the same human-approval gate on replies. |

Free tier · no signup gate · MIT-licensed plugin · agentskills.io compatible.
