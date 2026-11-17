# ESPN Fantasy — Team Management Strategy & Status

How to run a fantasy football team with an AI co-manager, plus the lessons we learned doing it.
Originally written for one team; generalized for sharing.

## The origin story (why this skill exists)

**I built this because I don't have time to manage my own team.**

Draft night is fun. Week 9 is not. Setting lineups, chasing waiver wire news, reading injury
reports, evaluating trade offers — it's a part-time job that nobody signed up for, and the cost
of missing a Sunday-morning inactive is a loss.

So the whole thing got packaged into a skill instead: **let your human participate in fantasy
football by handing the boring parts to an agent.** You keep the fun (the draft, the trash talk,
the trade that feels good); the agent keeps the roster optimized, watches the wire, and tells you
when a decision actually needs a human.

That's the pitch: **an AI co-manager, not an autopilot.** The agent does the work; the human
still makes the calls that matter.

## Design principles

- **Win-now.** Objective = field the best possible lineup every week.
- **Auto-execute the reversible stuff** (lineups). Ask before anything irreversible or social
  (adds/drops, trades, anything that touches other managers).
- **Never auto-accept an incoming trade.** Evaluate, then recommend approve/deny with reasoning.
  The human decides.
- **Log every move + the reasoning** so you can review what worked.
- **Don't poll from the model.** Run a low-cost watcher (cron/timer) and surface only new events.

## Operating model (permission tiers)

| Action | Default |
|---|---|
| Set optimal lineup | auto-execute (reversible) |
| Send trade offers | ping human first (unless explicitly broadened) |
| Incoming trade offers | **never auto-accept** — recommend, human decides |
| Waiver adds/drops | propose → approve |
| Anything touching other managers | propose → approve |

Broaden these only when the human explicitly says so. Trades are the sharp edge: an ESPN trade
requires the *other* owner to accept — you can only send offers and accept incoming ones, so
"live" trade autonomy means "can send without asking", not "can force".

## Weekly rhythm (the core)

| When | Action |
|---|---|
| Tue | Waiver claims / FAAB bids submitted |
| Wed–Thu | Injury reports drop → pivot to Plan B |
| Fri–Sat | Final lineup + stream a K/DST if needed |
| Sun pregame (~90 min out) | Last-minute inactives + weather → lock it in |

Short "here's what I'd do" digest at each window. Human-facing, brief, actionable.

## Start/Sit engine

- Pull weekly projections, apply **the league's exact scoring**, solve for max-points lineup
  (respecting slots/flex).
- Layer in: opponent matchup, Vegas implied totals, weather (wind/rain kills K + passing).
- Output a proposed lineup with the 1–2 close calls flagged for the human.

## Waivers & streaming

- Rank available FAs by projected ROS value vs. the bench.
- Stream high-variance spots (K, DST, sometimes QB/TE) by matchup.
- FAAB → bid strategically; rolling waivers → play the wire. (League setting dependent.)

## Monitoring (the part that actually saves you)

Never poll the API from the model (token burn + bot risk). Run a small watcher on a timer that
diffs the league feed and appends only NEW events to a file; a quiet run produces nothing.

Watch for: incoming/pending **trade proposals**, newly **executed transactions** (waivers, FA
adds/drops, completed trades), and **injury-status changes** on the roster.

Surface alerts cheaply from a heartbeat: if the alerts file is non-empty, relay it to the human
then truncate; if empty, stay silent.

## Sharing this with others

If you're adopting this skill for your own league:
1. Set your league/team IDs and scoring in your config (see `espn-fantasy-api.md`).
2. Decide your permission tiers with your human — don't inherit ours.
3. Start with the watcher only (read-only). Add write actions once trust is established.
4. Keep credentials in a secret store; never in the skill or chat.
