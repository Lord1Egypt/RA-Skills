---
name: do
description: Install and drive `do`, the agent-drivable CLI for the do personal todo / life-tracking app. `do` is a thin client over the app's public REST API (`/api/v1`) with per-tenant API-key auth — capture tasks, see what's actionable today, complete/snooze tasks, log habits, and read entities (tasks, habits, notes, contacts, recipes, …). Every destructive verb (delete, rm, remove, revoke, detach, unlink) is refused unless the call passes --allow-destructive, so an autonomous agent can't destroy data by accident. Use when the user wants to manage their todos / life-tracking from a terminal or agent, mentions the `do` CLI, or asks to capture or review tasks and habits.
homepage: https://github.com/robbeverhelst/do
metadata:
  openclaw:
    category: productivity
    tags: [todo, life-tracker, gtd, habits, cli]
    package: "@robbeverhelst/do"
    bins:
      - do
---

# do → drive your todos / life-tracking from a terminal or agent

`do` is a thin client over the **do** app's public REST API (`/api/v1`). It
inherits the same per-tenant auth, validation, and row-level-security wall as the
web app — there is no direct DB access. The v1 surface is the **daily loop**:
capture, today, complete/snooze a task, log a habit, and read entities. Every
**destructive verb** (`delete`, `rm`, `remove`, `revoke`, `detach`, `unlink`) is
refused unless you pass `--allow-destructive`, so it is safe to hand to an
autonomous agent: see [Destructive verbs](#destructive-verbs-ask-then-pass-the-flag).

> The live, authoritative surface is always `do help --json`. This skill is the
> orientation; when in doubt, introspect the binary — the manifest is generated
> from the same registry the commands dispatch from, so they can't drift.

## Install (pick one)

- **One-off / agents (no install):** `bunx @robbeverhelst/do <command>`.
- **Global:** `npm i -g @robbeverhelst/do` (or `bun add -g @robbeverhelst/do`), then run `do <command>`.
- **Binary:** download the `do-<os>-<arch>` asset from a GitHub Release
  (https://github.com/robbeverhelst/do/releases) and put it on your `PATH`.

Requires **Bun ≥ 1.3** for the `bunx`/binary paths (`bun --version`; install with
`curl -fsSL https://bun.sh/install | bash`).

**`do` is also a shell keyword** (the `do` of `for … do … done`), so bash, zsh and
sh refuse a line that starts with it: `syntax error near unexpected token 'do'`.
In a shell, type **`\do`** (or `command do`) — `\do today` — or put
`alias do='\do'` in your shell's rc file and type the recipes below as written. An
agent that runs the binary directly (an `exec` of `do` with its arguments, no
shell) needs neither. `bunx @robbeverhelst/do …` isn't affected.

## Auth (do this first)

Every call needs a **per-tenant API key**, sent as `Authorization: Bearer <key>`.
Keys are minted by the app (the JWT-guarded `POST /api-keys` endpoint, e.g. from
the web app's settings); the CLI only *consumes* a key — it never creates one. A
key only reaches routes whose scope it holds, so grant the scopes for the verbs
you need (`tasks:read`/`tasks:write`, `habits:write`, …).

Config resolves in precedence order (first wins):

1. `--api-key` / `--url` flags
2. `DO_API_KEY` / `DO_API_URL` environment variables  ← the agent / CI path
3. `~/.config/do/config.json`  ← written by `do login` / `do config set`, for humans

The hosted instance is **`https://do.robbe.work/api`** — so you only need a key:

```sh
# Agent / CI: just export the env vars.
export DO_API_KEY=do_xxx
export DO_API_URL=https://do.robbe.work/api   # hosted instance (see note below)

# Human: verify a key and save it (file is written 0600).
do login --api-key do_xxx --url https://do.robbe.work/api
do whoami                 # prove the key resolves to a tenant + scopes
do config show            # resolved config, key redacted, with sources
```

The URL ends in `/api` because the API sits behind the web app's same-origin
`/api` proxy (the CLI appends `/api/v1` itself). For a self-hosted instance, use
`https://<your-host>/api`; for local dev, `http://localhost:3001`. **Only the
API key is per-user — ask the user for a scoped key.**

## Output contract (agent ergonomics)

- `--json` forces JSON; output is **automatically JSON when stdout is piped**
  (non-TTY), so an agent always gets parseable output. A TTY gets pretty,
  colored text (honoring `NO_COLOR`, `--quiet`, `--verbose`).
- **Failures** print a JSON error envelope to stdout in JSON mode
  (`{ "error": { "code", "message" } }`) and a non-zero **exit code**:

  | exit | meaning                                                                    |
  |------|----------------------------------------------------------------------------|
  | 0    | success                                                                    |
  | 1    | runtime / network / unexpected HTTP                                        |
  | 2    | usage: unknown command, flag or field; a destructive verb without the flag |
  | 3    | config / auth (no key, 401, 403)                                           |
  | 4    | not found (404)                                                            |
  | 5    | validation (400)                                                           |

- **Offline or slow** fails with exit 1 instead of hanging: `network_error` when the API
  can't be reached, `timeout` past the time limit (15 s a request, 120 s for a sync,
  import, export or file; `--timeout <seconds>` or `DO_TIMEOUT` to change it). After a
  write times out, read before you send it again: it may have landed.

## The capture grammar

`do capture` quick-adds a task to the inbox from free text with inline tokens:

- `#tag` — adds a tag (repeatable): `#home #urgent`
- `!` — stars the task (the 1–2 things that matter); `!star` / `!s` / `!flag` / `!f` too
- `~area` — files it into an existing Area by its title, case-insensitive, one word
  (`~garden`); an unknown name files nothing. Valid names: `do areas list --json`
- a **when** — `tomorrow 3pm`, `fri`, `next week`, `in 2 days`, `yesterday`; a time makes it
  timed (on the calendar); `every monday` attaches a recurrence
- a **Deadline** — `by friday`, `due fri 5pm` (never the plan)
- an **estimate** — `30m`, `1h`, `1h30`, `2 hours`

All are stripped from the title; standalone only (so `C#` or `10!` in prose is
left alone). `--at <ISO>`, `--due <ISO>` and `--duration <minutes>` win over the text.
`do help capture --json` has the full grammar:

```sh
do capture "Email the landlord about the leak #home !"
# → task "Email the landlord about the leak", tag home, starred

do capture "File the taxes by friday 2h #admin"
# → Deadline Friday, estimate 2 hours
```

## Recipes (the daily loop)

```sh
# Capture an idea into the inbox
do capture "Draft Q3 plan #work !"

# See what's actionable today (overdue, scheduled, due, in-progress), then the
# habits and routines due today under `.habits`
do today

# From earlier (#888): planned tasks of the last 14 days that weren't done —
# never "late". Answer each with today, later (the quiet day later this week),
# someday (no date, kept in its Area/Project) or let-go (cancelled, not Landed).
do today earlier
do today answer later 01J9Z2K7Q8ABCDEF0123456789 01J9Z2K7Q8ABCDEF0123456790

# Complete a task (idempotent — a no-op success if already done)
do task done 01J9Z2K7Q8ABCDEF0123456789

# Snooze a task forward (default +1 day, or an explicit target)
do task snooze 01J9Z2K7Q8ABCDEF0123456789 --days 3
do task snooze 01J9Z2K7Q8ABCDEF0123456789 --until 2026-07-01

# Plan it at a time so it shows on the calendar
do task schedule 01J9Z2K7Q8ABCDEF0123456789 --at 2026-09-09T16:00:00+02:00 --duration 60

# Log a habit check-in (value defaults to 1; --at for a past time)
do habit log 01J9Z2K7Q8ABCDEF0123456789
do habit log 01J9Z2K7Q8ABCDEF0123456789 --value 30 --at 2026-06-18T21:00:00Z
# Place a habit in the day: morning|midday|evening or "HH:MM" (null = any time)
do habits update 01J9Z2K7Q8ABCDEF0123456789 --data '{"timeOfDay":"morning"}'

# Check in by title or alias, the way a chat message says it ("wake", "12 pages")
do habit check-in wake
do habit check-in pages --value 12                 # adds 12 to today
do habit check-in pages --value 40 --set           # makes today's total 40
do habit check-in drill --at 2026-10-15            # back-date to a day (your time zone)
do habit check-in drill --note "felt heavy"        # "drill done, felt heavy": the rest is a note
# Add or change a note afterwards (the check-in id is lastCheckIn.id in the reply,
# or from `do habit check-ins <id>`); --clear drops it
do habit note 01J9Z2K7Q8ABCDEF0123456789 01J9Z2K7Q8ABCDEF0123456790 "Dune, chapter 9"
# A 409 lists the candidates (error.details.candidates): ask which, then `do habit log <id>`.
do habit alias add 01J9Z2K7Q8ABCDEF0123456789 wake

# What's left today, by part of day (morning, midday, evening, anytime), + routines
do habits today

# Skip and pause, without guilt: a skip or a pause is never a miss
do habit skip 01J9Z2K7Q8ABCDEF0123456789                      # "skip gym today"
do habit skip 01J9Z2K7Q8ABCDEF0123456789 --note "Dentist"     # "skip gym, dentist": the why shows in the log
do habit pause 01J9Z2K7Q8ABCDEF0123456789 --until 2026-10-26  # "pause gym till the 26th"
do habit resume 01J9Z2K7Q8ABCDEF0123456789                    # "gym's back on"
do habit remind 01J9Z2K7Q8ABCDEF0123456789 on                 # "remind me about my drill" (off by default)
do away --until 2026-10-19                                    # "away till Monday"
do away off                                                   # "I'm back"

# A batch (the Apple Medications model): a routine whose steps are habits, e.g.
# "AM Supplements: magnesium, D3, creatine". One call checks in every open step.
do routine done 01J9Z2K7Q8ABCDEF0123456789                    # "took my supplements"
do routine undo <run.id> <taken stepRunIds…>                  # takes the batch back

# Retire a habit to the Grown shelf (history kept), or bring it back
do habit retire 01J9Z2K7Q8ABCDEF0123456789                    # only after they say yes
do habit unretire 01J9Z2K7Q8ABCDEF0123456789                  # "bring back flossing", or Undo
do habits list --retired                                      # the Grown shelf

# Read entities: `do <entity> list` / `do <entity> get <id>`
do tasks list --filter unsorted     # the Inbox: no day, Deadline, Area or Project; never a proposal
do tasks list --proposed            # Proposed by Echo: waiting for the member's Accept
do tasks list --area <areaId> --status todo,in_progress --tag errand --due-before 2026-10-12
do tasks list --updated-since 2026-10-11T08:00:00Z   # what changed since a sync
do areas list --active             # the live Areas to file into (archived ones are put away)
do areas overview                   # how each Area is going, in words (see "Areas" below)
do habits list                      # each carries today { due, done, week? } (on today's schedule?)
do habits list | jq '.data[] | select(.today.due) .title'   # what's on today
# "How are my habits going?" — this week's grid, a strength word per habit, patterns
# from the insights worker (each with its confidence) and when you usually check in
do progress habits
do notes get 01J9Z2K7Q8ABCDEF0123456789

# Pipe JSON into jq (auto-JSON because stdout is piped)
do today | jq '.items[] | select(.bucket == "overdue") .title'

# Sync: what changed since your last cursor (store .nextCursor, rerun while .hasMore)
do changes --since now                 # a fresh cursor, no history
do changes --since 812345-12 --entity task,project
```

Readable entities: `tasks`, `habits`, `occurrences`, `shopping-lists`,
`inventory-items`, `recipes`, `meal-plans`, `notes`, `contacts`, `webhooks`.

## Destructive verbs: ask, then pass the flag

Any command whose verb is `delete`, `rm`, `remove`, `revoke`, `detach` or
`unlink` (and forms like `kind-remove`, `unlink-task`) is refused without
`--allow-destructive`: exit `2`, `error.code: "destructive_blocked"`, and **no
request is sent**. The message says what to add. `do help <command>` lists the
flag on each of them.

- Ask the member before you delete, revoke or unlink anything they made, then pass
  the flag on that one call. Never add it to every call "to be safe".
- Prefer the recoverable verb when there is one: `archive` puts a row in Trash
  without the flag.
- Taking back one entry you just logged isn't destructive: `do health unlog`,
  `do habit undo`, `do money goal-uncount` and `do tasks unblock` run as they are.
- With an Agent's key the API may still hold a delete for the member's yes (HTTP
  428 `confirmation_required`): don't retry it, tell them it waits for them.

```sh
do challenges rm <id>                        # → exit 2: "add --allow-destructive to run it"; nothing sent
do challenges rm <id> --allow-destructive    # after the member said yes
do tasks archive <id>                        # recoverable: to Trash, no flag
do views delete "Old view" --allow-destructive
```

**Changed in 2.0.0:** before, 18 commands deleted without the flag (`challenges
rm`, `views delete`, `health share revoke`, `echo memory rm`, …). A script that
runs one of them now adds `--allow-destructive`.

## Discoverability

Run `do help` for the human overview, or **`do help --json`** for the complete
machine-readable manifest — every command, argument, flag, required scope, return
type, the read entities, auth resolution, and exit codes. Introspect that instead
of trusting this skill when the surface may have grown:

```sh
do help --json | jq '.commands[] | {command, scopes, returns}'
do help --json | jq '.entities[].name'
```

Source + full docs: https://github.com/robbeverhelst/do

## A note on a check-in

When a check-in message carries more than the habit, keep the rest as the
check-in's note (at most 280 characters): "drill done, felt heavy" →
`do habit check-in drill --note "felt heavy"`; "read 12 pages of Dune, chapter 9" →
`do habit check-in pages --value 12 --note "Dune, chapter 9"`. The note shows in the
habit's log beside "Echo, 07:12" and on its day in the year view. To add one later
("add a note: legs were sore"), use `do habit note <habit id> <check-in id> "…"`
with the reply's `lastCheckIn.id`; `--clear` removes it. Don't invent a note when
the message has none.

## Skip, pause and away: what the words mean

When someone says they'll rest from a habit, use these verbs. Never call a skip or
a pause a miss, and never nag about one.

| They say | Run |
|---|---|
| "skip gym today", "rest day for reading" | `do habit skip <id>` (find the id with `do habits list`) |
| "skipped the run yesterday" | `do habit skip <id> --date <yesterday, YYYY-MM-DD>` |
| "pause gym till the 26th", "no gym for two weeks" | `do habit pause <id> --until <the day it's back>` |
| "gym's back on", "resume reading" | `do habit resume <id>` |
| "remind me to do my drill", "stop reminding me about water" | `do habit remind <id> on` / `off`: one push a day at its time, never a follow-up |
| "away till Monday", "on holiday until the 3rd" | `do away --until <the day they're back>` |
| "I'm back", "come back early" | `do away off` |

- `--until` is **the day it's back** (the first day it counts again), and must be
  after today. Resolve "Monday" or "two weeks" to a date first; "till Monday" means
  back on Monday.
- Away rests **every** habit in the Space (off Now, no reminders, plants wait);
  tasks and events carry on. Ask once before going away if it's ambiguous whether
  they mean one habit or all of them.
- A skip shows in `do habit check-ins <id>` with `kind: "skip"`; undo it by
  deleting that entry. A why ("dentist") goes in `--note`. Resting habits carry `pause: { until, by }`.

## Batches: "took my supplements"

A batch is a routine whose steps are habits ("AM Supplements: magnesium, D3,
creatine"). When someone says they took or did the whole thing, check it in with
one call, not one habit at a time.

| They say | Run |
|---|---|
| "took my supplements", "supps done", "took my AM supplements" | `do routine done <routine id>` |
| "took everything except the creatine" | `do habit skip <creatine id>`, then `do routine done <routine id>` |
| "skip the creatine today" | `do habit skip <creatine id>` (the batch leaves it alone) |
| "undo that", "I didn't take them yet" | `do routine undo <run.id> <stepRunIds…>` from the answer |

- Find the routine in `do habits today` (`routines`, with their ids). With an AM
  and a PM batch and no word for which, take the one due now: AM before noon, PM
  after. Ask only if both are still open and it's unclear.
- If there's no routine for it but a single habit ("AM supplements" as one habit),
  check that habit in with `do habit check-in "am supplements"` instead.
- `do routine done` answers with `taken` (what it checked in). A habit already done
  today isn't counted twice, a skipped one stays skipped, and saying it again
  changes nothing. Reply in words ("Magnesium, D3 and creatine are in."), with no
  counts or streaks.

## Retire: when a habit has done its job

Retiring is not deleting. A habit that just happens now (or that no longer fits)
moves to the **Grown** shelf with its plant in bloom and keeps all its history. It
leaves Now and Today, sends no reminders and is never due; Progress keeps its past.

| They say | Do |
|---|---|
| "I'm done with the cold showers habit", "stop tracking flossing" | Offer first: "Retire Cold shower? It moves to Grown with its history." On a yes, `do habit retire <id>` |
| "bring back flossing", "track journaling again" | `do habit unretire <id>` |
| "what have I grown?", "which habits did I retire?" | `do habits list --retired` |

- **Ask before retiring**, and only retire on a clear yes. Then answer with a short
  receipt and an Undo: "Cold shower moved to Grown, history kept. Undo?" Undo is
  `do habit unretire <id>`.
- Never call it quitting or failing, and never delete a habit when they mean retire.
- A retired habit takes no check-in by title (404). If they check one in, offer to
  bring it back first.

### "Still right for you?" (only in a review they asked for)

During a review the person asked for (the Weekly Review, "let's review my week"),
read `do progress habits --json`: each habit has `quietWeeks`, the finished weeks
in a row it was done on less than half of what was due. For a habit at **4 or
more**, you may ask once, gently: "Reading has been quiet for a month. Still right
for you? You could keep it, pause it, or retire it to Grown." Then do what they
choose (`do habit pause`, `do habit retire`, or nothing). Never raise this outside
a review they started, never as a nudge, and never with numbers as pressure.

## An Area's standards: suggest, then apply on a yes

An Area can say what it's for (`purpose`, one line) and what "fine" looks like there
(`standards`, up to five plain sentences). A standard held by a habit, a recurring
task or a Metric says **holding** or **worth a look** with the reason in words; one
with no link is checked by hand in review. Never a score, never a percentage.

- You can **suggest** standards from what's already in the Area: "You have Gym 3× a
  week and Dentist twice a year. Make these Health's standards?" Read the Area first
  (`do areas get <id>`: its habits, routines and recurring tasks) and offer a short
  list with what would hold each.
- **Apply them only on the member's yes**, and only the ones they picked, through
  `do areas standards add` (the v1 endpoint). Each add shows in their change list
  with Undo. Never write standards, or a purpose, into an Area unasked, and never
  reword or remove theirs without being told to.
- "How's Health going?" → `do areas standards list <id>` and answer in its words
  ("Move three times a week is worth a look: one so far this week"). Don't turn it
  into a grade.

```sh
do areas get 01J9Z2K7Q8ABCDEF0123456789
do areas standards add 01J9Z2K7Q8ABCDEF0123456789 "Move three times a week" --habit 01J9Z2K7Q8ABCDEF0123456790
do areas standards list 01J9Z2K7Q8ABCDEF0123456789
```

## Areas: the map, the lens and the rhythm

An Area is an ongoing responsibility (Health, House, robbeverhelst); it never
finishes. Answer about Areas **in words, never a score**, and change one only when
the member asks. The member's own Areas are theirs: never rest, archive, merge or
convert one on your own; propose, then act on their yes.

- **"How's House going?" / "What am I neglecting?"**: `do areas overview` gives each
  Area's attention against its own usual (*Busier than usual*, *Steady*, *Quiet for
  three weeks*, *Resting*) with a reason, what's moving and what waits on them (Mine
  by default; `--owner all` counts agents' work too). Name the quiet ones and any
  standard **worth a look** (`do areas standards list <id>`), never a grade. Quiet is
  a fact, not a fault.
- **"How was my week, by area?"**: `do progress` (or `--days 30`). Its
  `areasHighlight` is one sentence to use as is ("Most of your own week went to
  Health and House. Wedding was busier than the week before."); the per-Area counts
  (yours, agents', check-ins, blocks) are fine to quote here, the one place counts
  belong.
- **"Focus me on the wedding today"**: `do areas focus <areaId>`. Now, Tasks and
  Calendar narrow to that Area until the end of their day, under a quiet bar; it
  clears itself. "Show everything" → `do areas focus --off`. The panel's page
  context tells you when they're focused. Never focus them unasked.
- **The review rhythm**: an Area with a rhythm (weekly, monthly, quarterly) comes up in
  their Review only when it came round. In a weekly review they started, or when
  asked: `do areas since <id>` for what landed, what's new and what seems stuck
  (in words), then ask the three questions (still what fine looks like? anything
  stuck? anything to let go?) with buttons. `do areas looked-at <id>` only when they
  say they've looked. No reminders, no "review overdue".
- **Resting** ("back in January"): only when they ask, `do areas rest <id> --until
  <day>` (add `--pause-habits` if they want its habits paused too). Its recurring
  tasks pause, Focus, Review and filing leave it alone. `do areas back <id>` brings
  it back early.
- **An Area that ends** (a wedding, a move: anything with a finish line) belongs as
  a Project. You may **propose** it once ("Wedding has an end. Make it a Project in
  Personal?"); only on their yes run `do areas make-project <id> --into <areaId>`
  and keep the receipt it prints: `do areas undo-make-project <id> --data
  '<receipt>'` puts everything back.
- **Filing**: never file into an archived or resting Area. Prefer the Area of the
  hub they're on (page context route `/areas/<id>`), then the Area of a Project the
  task belongs to.

```sh
do areas overview
do progress --days 7
do areas focus 01J9Z2K7Q8ABCDEF0123456789
do areas since 01J9Z2K7Q8ABCDEF0123456789
do areas rest 01J9Z2K7Q8ABCDEF0123456789 --until 2027-01-15 --pause-habits
```

## Posting into a member's thread (the Space's agent only)

When you are the Space's agent (your key has `agents:converse` and acts as the Agent the
Space's agent connection names), post what you'd
tell the member into their thread with `do agent post` (or `do echo post`):

- Without `--thread` it goes to your home thread with the Space's first owner.
  `--thread build` names one of their standing threads; an unknown slug is
  `thread_not_found`. Suggest a new standing thread to them, never make one.
- Pick the level for how loudly it should arrive: `needs_you` only when it waits on
  them, `told` when they asked to be told, `for_later` for things to read later,
  `silent` when there's nothing to say.
- For something that changes all day (a repos card, a follow-up round), post a
  `--kind card` under one stable `--external-id` (`card:repos`) and post it again
  on each change: it edits in place instead of adding a message.

```sh
do agent post --thread build --kind card --external-id card:repos "15 repos. Nothing needs you."
do agent post --thread build --level needs_you "do #861 is ready for your review."
```

## Tasks you make for someone arrive as proposals

When you work with an **Agent's key** (you are Echo, or a desk of Echo's) and make a
task with a **member as Owner** (`"owner":"member:alice@example.com"`), it is
**Proposed by Echo**: it waits at the top of their Inbox with Accept / Not now / Let
go, and stays off their Today, Now and lists until they accept. Your own work
(`"owner":"me/finance"`) is never a proposal.

- Give the reason in `source.label` ("From the KBC statement email") and the Desk you
  write from in `fromDesk` (`finance`). The Inbox shows the reason as the why.
- Suggest the day and Area as usual (`scheduledAt`, `dueAt`, `areaId`); Accept keeps
  them.
- A Desk the member **trusts** (Settings → Agents) skips the proposal and plans
  straight into their week, shown as "Planned by Echo". You can't skip it yourself:
  `proposed:false` from an untrusted Desk is refused (403).
- When they answer in chat: "yes, plan it" → `do tasks accept <id>`; "not now" →
  `do tasks dismiss <id>` (back in their Inbox in a week); "drop it" → `do task cancel
  <id>` (Let go; asks them to confirm first). Your accept shows in their change list
  with Undo.
- Check what still waits with `do tasks list --proposed`.

```sh
do tasks create --data '{"title":"Pay the dentist invoice","owner":"member:alice@example.com","fromDesk":"finance","dueAt":"2026-10-21","source":{"kind":"email","label":"From the Tandarts Peeters email, 112 euro"}}'
do tasks list --proposed
do tasks accept 01J9Z2K7Q8ABCDEF0123456789
```

## People: one note per person, with a receipt

When the member mentions someone in passing ("talked to Sam over the fence, he
started a new job, his moka pot broke"), write it as **one** `do people note` for
that person: each thing it means is an item. Items: `moment` (`life_update`,
`seen`, `talked`, `favour_done`, …; `sensitive:true` for health, a pregnancy before
it's public, money trouble), `gift_idea` (`title`), `follow_up` (`label`, `date`:
"ask how the surgery went" two days after), `key_date` (`birthday` or
`anniversary`, `date`, `yearKnown:false` when there's no year). Post the receipt it
returns as one card with **Undo** (`do people undo <id>`), **Edit**, and for a
sensitive item **Don't keep the detail** (`do contact-moments update <id> --data
'{"summary":null}'`).

- Name the person by `contactId`, or by `person` ("Sam", "Sam's sister", or "my
  sister" when the member says it: "my" is the member whose key you hold). Several
  matches come back as a conflict listing the candidates: ask once ("Sam Example
  or Sam from work?") and send it again with the `contactId`. No match: ask whether
  to add them, then `do contacts create "<name>"` with what you know as flags
  (`--email`, `--phone`, `--birthday YYYY-MM-DD`, `--circles <id>`, `--notes`). Fix a
  detail with `do contacts update <id> --phone "+32 …"`; `none` clears one.
- Keep only what they told you or approved. Never store message or mail bodies,
  anything from the web or social media, or guesses about how someone feels.
- A sensitive item with a follow-up in the same note keeps its summary until 30
  days after the follow-up; then only "something happened" remains.
- Before they see someone (a calendar event with them within a day), `do people
  brief <contact id>` gives last seen, the latest life updates, open follow-ups and
  gift ideas, in one line.
- The calendar fills "last seen" by itself (an event that is over, with them on it).
  Don't log a `seen` moment for a calendar event.
- Rhythm is a wish, never a debt. Say "might be nice to see", "you said about
  monthly", "Thursday evening is open". Never "overdue", never a count of people not
  seen, never a streak. "Not now" sets `rhythmSnoozedUntil` without comment.

```sh
do people note --data '{"person":"Sam","items":[{"type":"moment","kind":"life_update","summary":"started a new job"},{"type":"gift_idea","title":"Moka pot"},{"type":"moment","kind":"seen"}]}'
do people undo 01J9Z2K7Q8ABCDEF0123456789
do people find "Sam's sister"
do people brief 01J9Z2K7Q8ABCDEF0123456789
do contacts update 01J9Z2K7Q8ABCDEF0123456789 --data '{"rhythmSnoozedUntil":"2026-11-01"}'
```

### The family tree

Only with a key the member opened **Family tree** for (`people:family-tree`); any
other key gets a 403. The tree names relatives who never chose to be in do: never
repeat a relative's details outside the member's own thread, and never turn an
ancestor into a Contact.

- A GEDCOM the member sends you: `do people tree import <file.ged>` (with
  `--source-name` / `--source-email` when you know who sent it).
- "That's me": `do people tree list <name>` to find the ref, then `do people tree me <ref>`.
- `do people tree matches` lists what the tree noticed. Ask the member about each
  one ("Is Nora in the tree your Contact Nora?") and only then `--accept <id>` or
  `--reject <id>`. A no is never offered again.

```sh
do people tree import family.ged --source-name "Aunt Test"
do people tree me I12
do people tree matches --accept suggest:I2:01J9Z2K7Q8ABCDEF0123456789
```

## Plan the member's week (or day) as a proposal

When the member asks "plan my week" (or on their planning evening), propose it with
`do plans propose` rather than moving tasks yourself. Nothing is written until they
accept it on Review › Weekly (or tell you "yes" in chat). Contract and payloads:
`docs/agents/plan-proposals.md`.

- `kind:"week"` with `startsOn` the Monday (or `kind:"day"` with the day). One item
  per task: `day` (a planned day, their zone), or `at` (a time, ISO, inside the week)
  with `durationMinutes` when the task has an estimate; `action:"someday"` or
  `action:"let_go"` for what should leave the week. Give each a short `reason`.
- Deadlines first, then what waits on them, then what fits the free gaps. Keep
  weekends light. Only their own open tasks, and your work only while it waits on
  them. Read `do tasks list --drifted` and ask about those once.
- Sending a new plan for the same week replaces the open one: that's how you
  "change it" after they ask.
- "Plan my day" is the same call with `kind:"day"` and `startsOn` today: it shows
  as a preview at the top of their Now (Accept / Not today).
- When they answer in chat: "yes" → `do plans accept <id>`; "not that one" →
  `do plans dismiss <id> <itemId>`; "undo" → `do plans undo <id>`.
- **Their planning rules first:** `do plan rules list --for <userId>` (fixed times,
  keep-free windows, what a word means, whose something is, how often). Keep them;
  the planner anchors fixed times and leaves keep-free windows empty on its own.
- **When they state a rule in chat** ("church is always Sunday 11:00", "no screens
  after ten", "the gym class is my partner's, not mine"), add it with
  `do plan rules add "<their words>" --rule '<json>'` (or no `--rule` for a plain
  note), then post a receipt with its id (`receipt: { nodeId }`) so they can Undo it.
  One rule per thing they said; don't invent rules they didn't state.
  Payloads: `docs/agents/planning-rules.md`.

```sh
do plans propose --data '{"kind":"week","startsOn":"2026-10-19","note":"A light week: the domain first.","items":[{"taskId":"01J9Z2K7Q8ABCDEF0123456789","day":"2026-10-20","reason":"Deadline Friday"}]}'
do plans list --kind week --status open
```

## When your work is ready, say so: Ready for you

Your own tasks (`"owner":"me/finance"`) live in the member's **Tasks › With Echo**,
never in their Today. Each reads as one word: **Working on it** (open), **Waiting on
you** / **Waiting on someone** (Waiting on set), **Ready for you**, **Done today**.

- When you finish something the member should look at (a draft invoice, a recap, a
  PR or worktree), mark it **Ready for you** with what's ready in one line and the
  link: `do tasks ready <id> --note "Draft ready: 38 hours, 3,420 euro — <link>"`.
  Put the link in the note (or in `source.url` / a worktree link); the member's
  **Review** opens it. It reaches their Now under Needs you.
- They answer with **Looks good** (the task is done; carry on with what you said
  you'd do next, e.g. send it Monday) or **Send back**, which clears Ready for you and
  writes to you in the chat with what to change. Pick it up from there and mark it
  ready again when it's fixed.
- Don't mark a task ready that needs nothing from them, and never mark one done for
  them: Looks good is theirs. Need an answer instead of a look? Set `waitingOn` to
  them (Waiting on you).
- Check what still waits on their look with `do tasks list --ready`, or one desk's
  work with `do tasks list --owner agent:Echo/finance`.

```sh
do tasks ready 01J9Z2K7Q8ABCDEF0123456789 --note "Recap drafted — https://docs.google.com/document/d/…"
do tasks list --ready --owner agent:Echo/clients
```

## The team: approvals, decisions and meetings

The member's **Team room** shows each Agent with what waits on them, what it's
working on, its temps and what it finished today. You show up there through your
tasks and the asks you raise on them.

- **Need a yes before you act?** Raise an approval on the task, not a loose chat
  question: `do agent ask "Send the quote?" --thread build --task DO-148 --yes Send
  --on-yes done`. It waits on them in the Team room and on the task's page; their
  answer lands in the task's decision log. Give it your own `--ask-id` so asking
  again changes the same ask instead of adding one. `--kind question` or `decision`
  with `--options a,b` when it isn't a yes or no.
- **They answered in the chat app instead?** Record it with the same id: `do agent
  ask-mirror quote-1 --answer yes` (`no`, `edit --text "…"`, `pick --picked 0,2`). do
  shows it answered and sends nothing back.
- **Decided something, or handed work on?** Write one line in the task's log: `do
  tasks decide DO-148 "Ship it Friday"`, or `--handoff` when another Agent or Desk
  takes over. Read it back with `do tasks decisions DO-148`. Say what was decided,
  not how you got there.
- **A meeting** is a task tagged `meeting`. After it, write the minutes as your
  Agent: decisions, who does what (`"Pike: Price list @2026-12-15"`, `Name/desk` for a
  Desk), open questions. Writing them again replaces them. Don't confirm them
  yourself: confirming turns each line into a child task owned by that Agent, and
  that's the member's call unless they asked you to.
- Read the room with `do team`, one Agent with `do team member Pike`, and one task as
  the team sees it with `do team task DO-148`.

```sh
do agent ask "Send the quote?" --thread build --ask-id quote-1 --task DO-148 --yes Send --on-yes done
do agent ask-mirror quote-1 --answer yes
do tasks decide DO-148 "To the Harbor desk" --handoff
do team minutes DO-150 --decision "299 setup" --who "Pike: Price list @2026-12-15" --open "Monthly mail?"
do team meeting DO-150
```
