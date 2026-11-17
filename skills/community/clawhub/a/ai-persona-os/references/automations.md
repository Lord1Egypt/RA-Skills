# Automations Guide: Pulse, Briefings and Routing

> **⚠️ OPT-IN ONLY:** Nothing in this guide runs automatically when the skill is installed.
> The pulse and the cron jobs below are **manual setup steps** that the user must explicitly
> choose. The core skill works fully without any of them. Cron jobs run in **isolated
> sessions**: they read and write local workspace files only, make **no network calls of
> their own, and need no credentials**.

**Requires:** OpenClaw 2026.8.1 or later.
**Changed in:** v2.1.0 (this file replaces `heartbeat-automation.md`)

---

## What Changed in v2.1.0

OpenClaw retired workspace `HEARTBEAT.md` files in 2026.8.1. The heartbeat is now a system-owned scheduled job, and the runtime never reads `HEARTBEAT.md`. So AI Persona OS no longer ships or installs a heartbeat:

- No `HEARTBEAT.md` template, no `HEARTBEAT.md` in the starter packs, and setup no longer copies one.
- No heartbeat prompt override. OpenClaw's built-in heartbeat prompt already tells the agent to reply `NO_REPLY` when nothing needs attention and not to rehash old tasks. Replacing it loses that guard.
- One optional extra, the **pulse**: a short context and memory check written into the heartbeat job's scratch. Nothing else.

| Piece | Owned by | What AI Persona OS does |
|-------|----------|-------------------------|
| Heartbeat schedule and delivery | OpenClaw (`agents.defaults.heartbeat`) | Nothing, except pinning delivery to Discord on request (see Routing) |
| Heartbeat checklist | OpenClaw (the heartbeat job's scratch) | Writes the pulse text, only when the user asks |
| Daily and weekly briefings | Cron jobs | Templates below, opt-in |

---

## The Pulse (optional)

A 30-minute check that rides on OpenClaw's heartbeat: it catches a filling context window and a bloated MEMORY.md, fixes what it can, and stays silent when everything is fine.

### Set it up (`set up pulse`)

The agent does each step itself, explaining it before the Approve prompt:

1. **Find the heartbeat job.**
   ```
   exec: openclaw cron list --all --json
   ```
   Pick the job whose `payload.kind` is `heartbeat` and whose `agentId` is this agent (usually named `heartbeat-main`, shown as "Heartbeat (main)"). If there is none, OpenClaw has not created one yet: tell the user to run `openclaw doctor --fix` once, then try again.
2. **Check it is enabled.** If the job shows `enabled: false`, the heartbeat is switched off (`agents.defaults.heartbeat.every` is `"0m"`). Ask the user whether they want it on before going further. The pulse does nothing while the heartbeat is off.
3. **Show what is there now.**
   ```
   exec: openclaw cron scratch <jobId>
   ```
   If the scratch has the user's own checklist, show it and ask before replacing it. OpenClaw's default scratch (comment lines only) can be replaced.
4. **Write the pulse.**
   ```
   exec: openclaw cron scratch <jobId> --set "<pulse text below>"
   ```
5. **Confirm:** `✅ Pulse on: checks context and memory every 30 minutes, silent when all green.`

**Turn it off:** `openclaw cron scratch <jobId> --unset`. The heartbeat itself keeps whatever schedule OpenClaw has.

### Pulse text

```
AI Persona OS pulse. Check, fix what you can, and report only problems.
- Context: if 70% or more, write a checkpoint to memory/YYYY-MM-DD.md now and skip the rest. If over 50% and the last checkpoint is more than 30 minutes old, write one.
- Memory: MEMORY.md must exist and stay under 4KB. If it is over, move entries older than 30 days to memory/archive/.
- If everything is fine and you took no action, reply NO_REPLY.
- Otherwise reply with one line per item and a blank line between them: 🟢/🟡/🔴 Context, Memory, Workspace, Tasks. Then add → lines saying what you did.
```

Keep it this short: the scratch is added to every heartbeat turn.

### What a pulse report looks like

All clear: nothing is delivered (`NO_REPLY`).

Something needed attention:
```
🟡 Context: 58%, checkpoint written

🟢 Memory: MEMORY.md 2.1KB

🟢 Workspace: Clean

🟢 Tasks: None pending

→ Checkpoint written to memory/2026-11-03.md
```

Emergency:
```
🔴 Context: 84%, EMERGENCY

🔴 Memory: last checkpoint 2h ago

🟢 Workspace: Clean

🟡 Tasks: 1 blocked

→ Emergency checkpoint written. Recommend starting a fresh session.
```

### Indicator reference

| Indicator | Context | Memory | Workspace | Tasks |
|-----------|---------|--------|-----------|-------|
| 🟢 | <50% | Checkpoint <30m old | All files OK | 0 pending |
| 🟡 | 50-69% | Checkpoint 30-60m old | Minor issues | 1-3 items |
| 🔴 | ≥70% | Checkpoint >60m old | Files inaccessible | Blocked items |

---

## Daily Briefings (Cron Jobs)

For the full 4-step Session Management protocol, use isolated cron jobs that run once or twice a day. Ready-to-run copies are in `assets/cron-templates/`.

On hosts with more than one chat channel, an announce job **must** name its channel. To deliver to the user's Discord DMs, add `--channel discord --to "user:<your-discord-user-id>"` (or `--to "channel:<channel-id>"` for a server channel).

### Morning Briefing

```bash
openclaw cron add \
  --name "ai-persona-morning-briefing" \
  --cron "0 8 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run the AI Persona OS daily protocol:

Step 1: Load previous context — Read today's and yesterday's memory logs. Summarize key state.

Step 2: System status — Check MEMORY.md size, workspace structure, stale logs.

Step 3: Priority scan — Check channels in priority order (P1 critical → P4 background). Surface anything requiring attention.

Step 4: Assessment — System health summary, blocking issues, time-sensitive items, recommended first action.

Format as a daily briefing with 🟢🟡🔴 indicators for each section." \
  --announce --channel discord --to "user:<your-discord-user-id>"
```

### End-of-Day Checkpoint

```bash
openclaw cron add \
  --name "ai-persona-eod-checkpoint" \
  --cron "0 18 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "End-of-day checkpoint:

1. Write a full checkpoint to today's memory log with all decisions, action items, and open threads.

2. Review MEMORY.md — promote any repeated learnings from today's log. Prune anything stale.

3. Check .learnings/ — any pending items that should be promoted after 3+ repetitions?

4. Brief summary: what was accomplished, what carries over to tomorrow." \
  --announce --channel discord --to "user:<your-discord-user-id>"
```

### Weekly Review

```bash
openclaw cron add \
  --name "ai-persona-weekly-review" \
  --cron "0 9 * * 1" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Weekly review protocol:

1. Scan memory/ for the past 7 days. Summarize key themes, decisions, and outcomes.

2. Review .learnings/LEARNINGS.md — promote items with 3+ repetitions to MEMORY.md or AGENTS.md.

3. Archive logs older than 90 days to memory/archive/.

4. Check MEMORY.md size — prune if >3.5KB.

5. Review WORKFLOWS.md — any new patterns worth documenting?

Deliver a weekly summary with wins, issues, and focus areas for the coming week." \
  --announce --channel discord --to "user:<your-discord-user-id>"
```

Drop the `--channel`/`--to` pair on a single-channel host. Use `--no-deliver` instead of `--announce` for internal-only runs.

---

## Channel Routing — Keeping Unsolicited Messages on Discord

OpenClaw routes replies back to the channel a message came from; the model never picks a channel. Drift only happens on **unsolicited** messages: heartbeat alerts (including the pulse) and cron briefings.

### The Three Settings

1. **`accounts.default`** — required in multi-account setups. Without it, fallback picks "the first normalized account ID", which is often the web account.

   ```json
   "accounts": { "default": "discord-<account-id>" }
   ```

2. **`channels.discord.defaultAccount`** — a per-channel anchor so Discord-originated sessions are never re-homed to web.

   ```json
   "channels": { "discord": { "defaultAccount": "discord-<account-id>" } }
   ```

3. **`agents.defaults.heartbeat.target` and `.to`** — where heartbeat alerts go. The default is `owner` (the owner's DM, from `commands.ownerAllowFrom`); `last` follows the most recent conversation and drifts; `none` keeps them internal. To pin them to Discord:

   ```json
   "heartbeat": { "target": "discord", "to": "user:<your-discord-user-id>" }
   ```

   Keep `to` a string. If `openclaw doctor --lint` warns that `directPolicy` is unset, set `"directPolicy": "allow"` to keep DM delivery.

Cron briefings use their own `--channel`/`--to` (see above), not these settings.

### Verifying

Run `route check` in chat. It reads the config and shows a 🟢🟡🔴 dashboard with the exact snippet for anything missing.

### After Editing openclaw.json

Run `/new` in chat to reload, or `openclaw gateway restart` as a fallback.

---

## Upgrading from v2.0.x or v1.x (`upgrade`)

Older versions installed a `HEARTBEAT.md` into the workspace. On OpenClaw 2026.8.1+ it is dead weight, or worse: `openclaw doctor --fix` imports it into the heartbeat job's scratch word for word, and the old text points at files v2.1.0 no longer ships (`assets/HEARTBEAT-template.md`, "compare to skill version 2.0.0").

The agent walks through these one at a time, with approval for each:

1. **Check the OpenClaw version.** `exec: openclaw --version`. Below 2026.8.1: stop. Tell the user v2.1.0 needs OpenClaw 2026.8.1+; keep v2.0.0 until OpenClaw is upgraded.
2. **Archive the workspace HEARTBEAT.md**, if one exists:
   ```
   exec: mkdir -p <WORKSPACE>/memory/archive && mv <WORKSPACE>/HEARTBEAT.md <WORKSPACE>/memory/archive/HEARTBEAT-pre-2.1.0.md
   ```
3. **Check the heartbeat job's scratch** (Pulse steps 1 and 3). If it holds an old AI Persona OS checklist (it mentions `HEARTBEAT-template.md`, "Migration check (run once)" or "AI Persona OS v"), offer two choices: replace it with the pulse, or clear it with `--unset`.
4. **Remove an old heartbeat prompt override.** If `agents.defaults.heartbeat.prompt` contains "AI Persona OS", offer to delete that key so OpenClaw's default prompt applies again. Leave any other custom prompt alone.
5. **Update the version file:** `exec: cp assets/VERSION.md <WORKSPACE>/VERSION.md`
6. **Tidy the workspace AGENTS.md:** if it still says "HEARTBEAT runs every session", offer to delete that line. Ask first; it is the user's file.

Nothing else in the workspace changes: memory files, SOUL.md, USER.md, AGENTS.md (apart from that line), WORKFLOWS.md and all other content are untouched.

---

## Troubleshooting

**Heartbeat messages are noisy:**
- Check the scratch is the pulse text, not an old checklist: `openclaw cron scratch <jobId>`
- Make it less frequent: `"every": "1h"`, or limit it with `activeHours`
- Turn the pulse off: `openclaw cron scratch <jobId> --unset`

**The pulse never reports anything:**
- That is normal when all is green (`NO_REPLY`)
- Check the job is enabled: `openclaw cron list --all`
- Check the last run: `openclaw system heartbeat last`

**`NO_REPLY` or `HEARTBEAT_OK` shows up in chat:**
- The reply must be the token alone (or with at most 300 characters around it). Remove any custom heartbeat prompt that asks for extra text.

**Heartbeat alerts land on web instead of Discord:**
- Set `target` and `to` (Routing, setting 3)

**Agent responds in Discord when not mentioned:**
- Set `requireMention: true` for ALL Discord guilds in the gateway config. Tell the agent: "List ALL Discord guilds in your config. Set requireMention: true for EVERY guild."

**MEMORY.md too large (burning tokens):**
- Tell the agent to prune; facts older than 30 days go to memory/archive/
- MEMORY.md should stay under 4KB; it is read at every session start

**Agent's config file is clawdbot-mac.json or clawdbot.json (not openclaw.json):**
- Older installs may use the pre-rename config file. All settings work the same regardless of filename.

---

*Part of AI Persona OS by Jeff J Hunter — https://os.aipersonamethod.com*
