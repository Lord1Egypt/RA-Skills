---
name: did-you-know
description: Fetches English Wikipedia's "Did you know?" (DYK) facts, caches them locally, and serves them one at a time. No API key required. Does not edit Wikipedia.
homepage: https://github.com/jonathandeamer/did-you-know
metadata: {"openclaw":{"emoji":"❓","requires":{"bins":["python3"]}}}
---

# Did You Know

Wikipedia's [Did You Know?](https://en.wikipedia.org/wiki/Wikipedia:Did_you_know) section highlights well-sourced facts from recently created or expanded articles. It's curated and refreshed at least daily by volunteers.

Use this skill when the user asks for an interesting fact, wants daily trivia delivered automatically, or wants to customise which kinds of facts they see.

> **Agent: Do not show bash commands or technical details to the user unless they explicitly ask. Run all commands silently. The user experience is conversational — facts, questions, and natural follow-ups. Keep your tone direct and natural; avoid empty compliments like "Great taste!" or "Excellent choice!" when responding to preferences.**

## What users might want

| If the user wants… | Do this |
|---|---|
| A fact | Serve one (see Serving a fact) |
| To customise which facts they see | Walk through preferences (see Managing preferences) |
| Facts delivered automatically | Help them set up a schedule (see Scheduling fact delivery) |
| The fact queue refreshed | Follow the Refresh workflow |

## Is any setup required?

**Facts work immediately — no setup needed.** Just serve one.

**Preferences are optional but recommended.** If the user wants to tune which topics come up (more history, less science, etc.), you can set those up in a minute or two. Preferences need the refresh workflow running so that new facts get tagged before they're scored.

**Scheduled refresh is only needed if preferences are active.** Without preferences, the skill fetches and caches facts automatically as needed. With preferences, set up both a delivery schedule (to serve facts) and a refresh schedule (to tag new facts so preference scoring works).

If a user asks whether any setup is required, a good response is: *"You can get facts right now — no setup needed. If you'd like to tune which topics come up, or get a fact delivered automatically each day, we can set either of those up in a few minutes. Want to?"*

## Serving a fact

> **Agent: run this silently — do not show the command.**

```bash
python3 {baseDir}/scripts/dyk.py
```

Return the output to the user verbatim.

**Fact served:**
```
Did you know that heavy-metal guitarist Kiki Wong played drums for Taylor Swift before joining the Smashing Pumpkins?

https://en.wikipedia.org/wiki/Kiki_Wong
```

**No facts remaining:**
```
No more facts to share today; check back tomorrow!
```

**Error:**
```
Something went wrong with the fact-fetching; please try again later.
```

After serving a fact, check whether `~/.openclaw/dyk-prefs.json` exists. If it does **not** exist, the user is new — follow up: *"Would you like to tune which topics you see (more music, less science, etc.), or get a fact delivered automatically each day?"* If the file exists, or if you already set up preferences or delivery earlier in this conversation, say nothing.

## Managing preferences

Facts are scored and ranked using user preferences. Liked tags increase the score; disliked tags reduce it. Recency and variety bonuses apply automatically.

### Have the conversation first

Before running any commands, understand what the user enjoys. If they've already told you (e.g. "I love dark historical stories but not sports"), map their words directly to tags — don't ask them to repeat themselves. Only ask follow-up questions if their intent is unclear. Two dimensions are available:

- **domain** — topic area (e.g. history, science, music)
- **tone** — style or mood (e.g. quirky, inspiring, dark)

Don't list every tag upfront — just ask what they like in natural terms and map their answers. For example: "I love dark historical stories" maps to `domain: history` (like), `tone: dark` (like).

When opening the preferences conversation, mention that you'll also set up automatic refresh alongside — this is what actually applies preferences to new facts as they arrive. Keep it light: something like *"I'll also set up automatic refresh in the background so new facts get tagged and scored against your preferences."* The user doesn't need to understand the mechanics, but they should know the full setup is happening.

### Setting preferences

Once you know what they want:

1. Check if the prefs file exists. If not, initialise it first (`prefs.py init`).
2. Set each preference (`prefs.py set`).
3. Summarise in plain language what's been set and how it will affect the facts they see.

If they want to see their current preferences at any point, run `prefs.py list` and present the results readably — not as raw output.

> **Agent: run preference commands silently — do not show them.**

```bash
python3 {baseDir}/scripts/prefs.py init                     # Create prefs file with neutral defaults. Fails if already exists.
python3 {baseDir}/scripts/prefs.py list                     # Show all current preferences
python3 {baseDir}/scripts/prefs.py get domain science       # Get a single preference
python3 {baseDir}/scripts/prefs.py set domain science like  # Set a preference: like | neutral | dislike
```

### Tags

**domain:** `animals` · `economics_business` · `film` · `history` · `journalism` · `language_linguistics` · `literature` · `medicine_health` · `military_history` · `music` · `mythology_folklore` · `nature` · `performing_arts` · `places` · `religion` · `science` · `sports` · `technology` · `television` · `visual_art`

**tone:** `dark` · `dramatic` · `inspiring` · `poignant` · `provocative` · `quirky` · `straight` · `surprising` · `whimsical`

### After setting preferences

Once preferences are saved, run the Refresh workflow immediately — existing cached hooks are all untagged, so preferences can't score anything until they've been tagged. Don't wait for the scheduled cron; do it now, inline. Then set up the refresh schedule so future facts get tagged automatically as they arrive. Say something like: *"I'll tag your existing facts now so preferences apply straight away, and set up automatic refresh in the background for new ones."*

Also offer scheduled delivery if they haven't already set it up.

## Scheduling fact delivery

When the user wants to receive facts automatically, prompt a cadence conversation before setting anything up:

- How often would they like a fact? Once a day is a nice ritual — over breakfast, on the commute, at the end of the day. A few times spread throughout the day also works.
- Bear in mind: the more frequently facts are served, the further into lower-preference territory the queue will go.

Once they've chosen, set up an OpenClaw cron job for delivery. Use `--session isolated` and `--announce` so the output is delivered back to the user's chat. Do **not** use OS-level crontab — it has no delivery context and output will go nowhere.

> **Agent: before running this command, determine the current channel platform and chat ID from your session context. Use them for `--channel` and `--to`. Run the command silently — do not show it.**

```bash
openclaw cron add \
  --name "DYK delivery" \
  --cron "<schedule>" \
  --session isolated \
  --message "Share a Did You Know fact" \
  --announce \
  --channel <platform> \
  --to <platform>:<id>
```

Replace `<schedule>` with a 5-field cron expression matching the user's chosen cadence (e.g. `57 7 * * *` for ~8am). Avoid exact `:00` minutes — nudge a few minutes either side. Replace `<platform>` and `<id>` with the current channel's platform and chat ID (e.g. `--channel telegram --to telegram:1234567890`).

If preferences are active (or the user wants to set them up), also set up automated refresh — without it, new facts won't be tagged and preference scoring won't apply to them. Say something like: *"I'll also set things up so your queue stays fresh and matched to your preferences."* Then follow Setting up automated refresh below.

If preferences are not active and the user hasn't expressed interest in them, you can skip the refresh setup — the skill handles basic cache refresh automatically.

## Setting up automated refresh

Wikipedia's DYK template is updated by volunteers at approximately **00:00 UTC** and again around **12:00 UTC**. Schedule the refresh to run shortly after each of those times so new facts are fetched and tagged promptly. Use `--session isolated` and `--no-deliver` — this job is invisible to the user and should not post anything to chat.

> **Agent: run this silently — do not show the command.**

```bash
openclaw cron add \
  --name "DYK refresh" \
  --cron "7 0,12 * * *" \
  --session isolated \
  --message "Refresh the DYK cache and tag new hooks" \
  --no-deliver
```

The cron agent will follow the Refresh workflow each time it fires.

## Refresh workflow

When asked to refresh the DYK facts cache and tag new hooks:

1. Run: `python3 {baseDir}/scripts/fetch_hooks.py`

   This fetches the latest hooks and stores them in `~/.openclaw/dyk-facts.json` with `"tags": null` for new entries.

   If it exits non-zero, stop and report the error. Do not continue.

2. Read `~/.openclaw/dyk-facts.json` and find all hooks where `"tags"` is `null`.

   If there are none, stop — nothing to tag.

3. Assign tags for all untagged hooks at once — do not loop across multiple turns or tool calls. For each hook, assign tags using:
   - Tagging guide: `{baseDir}/references/tagging-guide.md`
   - Vocabulary: `{baseDir}/references/tags.csv`

   Output requirements:
   - Use only tag values defined in `tags.csv`
   - If tagging confidence is low, set "low_confidence": true.
   - Write valid JSON only — no comments or explanations
   - Collect results into a single JSON array
   - Write the array to a temporary file such as `/tmp/dyk-tags.json`

   ```bash
   # Example array written to /tmp/dyk-tags.json
   [
     {"url": "https://en.wikipedia.org/wiki/Kiki_Wong",
      "domain": ["music"], "tone": "surprising", "low_confidence": false}
   ]
   ```

4. Run: `python3 {baseDir}/scripts/write_tags.py --json-file /tmp/dyk-tags.json`

   If it exits non-zero, report the error.

5. Do not message the user unless there is an error.

For the full command reference, see `{baseDir}/references/commands.md`.
