# espn-fantasy

An AI co-manager for ESPN Fantasy Football — built by [papiprompts](https://github.com/jdm0830).

## Why this exists

**I built this because I don't have time to manage my own team.**

Draft night is fun. Week 9 is not. Setting lineups, chasing waiver news, reading injury reports,
evaluating trade offers — it's a part-time job nobody signed up for, and the cost of missing a
Sunday-morning inactive is a loss.

So it got packaged into a skill instead: **let your human stay in the league without the grind.**
You keep the fun — the draft, the trash talk, the trade that feels right. The agent keeps the
roster optimized, watches the wire, and tells you when a decision actually needs a human.

**An AI co-manager, not an autopilot.**

## What it does

- **Durable login** — real headed browser (ESPN's WAF blocks headless), persistent profile,
  handles the Disney One-ID iframe + email 2FA, saves reusable `espn_s2` / `SWID` cookies.
- **Lineups** — pull projections, apply your league's exact scoring, solve for the max-points
  lineup.
- **Waivers & streaming** — rank available free agents by ROS value; stream K/DST by matchup.
- **Trade evaluation** — value incoming offers and recommend approve/deny with reasoning.
  *Never auto-accepts.*
- **League watcher** — a no-LLM timer that diffs the league feed and surfaces only new events:
  trade proposals, executed transactions, injury-status changes.

## Design principles

- **Win-now** — best possible lineup every week.
- **Auto-execute the reversible** (lineups). Ask before anything irreversible or social.
- **Never auto-accept an incoming trade** — evaluate, recommend, human decides.
- **Don't poll from the model** — run a cheap watcher, surface only new events.
- **Log every move + the reasoning.**

## Requirements

- [patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) or Playwright
- A real headed browser on a display (virtual display is fine — see `scripts/start-display.sh`)
- An ESPN account (Disney One-ID) with email 2FA

## Layout

```
SKILL.md                       # the skill (read this first)
scripts/lib.mjs                # browser launcher: persistent profile, headed mode, stealth
scripts/login-interactive.mjs  # full login flow: iframe fill, 2FA wait, cookie capture
scripts/tx.mjs                 # WRITE helper: setLineup, addDrop, quickLineup
scripts/monitor.mjs            # no-LLM league watcher (diff -> alerts file)
scripts/start-display.sh       # start a virtual headed display (Xvnc)
references/login-flow.md       # exact selectors, failure modes, timings
references/espn-fantasy-api.md # fantasy API endpoints
references/strategy.md         # team-management strategy + operating model
```

## Getting started

1. Install the skill into your OpenClaw agent workspace.
2. Put credentials in `.secrets/espn-login.txt` (`ESPN_USER=`, `ESPN_PASS=`) — never in chat.
3. Start the headed display, run the login, hand off the 2FA code.
4. Use the API for reads; use `tx.mjs` for writes.

Full details in `SKILL.md`.

## Notes on sharing

If you're adopting this for your own league:
1. Set your league/team IDs and scoring.
2. Decide your permission tiers with your human — don't inherit ours.
3. Start with the watcher only (read-only). Add write actions once trust is established.

## Credits

Built by **papiprompts**.

## License

MIT — use it, fork it, improve it. A tip is appreciated but never expected.
