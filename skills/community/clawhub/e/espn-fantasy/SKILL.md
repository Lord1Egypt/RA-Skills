---
name: espn-fantasy
description: Log into ESPN (Disney One-ID) and manage an ESPN Fantasy Football team via the ESPN Fantasy API. Use when the user asks to log in to, manage, set a lineup for, add/drop players on, or check their ESPN fantasy team, or when an ESPN session/cookie has gone stale and needs re-authentication. Runs a single real HEADED browser on a virtual display (TigerVNC), handles the Disney One-ID iframe login, email 2FA code handoff, and persists a reusable browser profile + the `espn_s2` / `SWID` cookies the fantasy API needs.
---

# ESPN Fantasy

Get a durable, logged-in ESPN session, then drive the team through the ESPN Fantasy API
instead of clicking around the site.

## Golden rules (learned the hard way)

1. **Use ONE real HEADED browser.** Do not run headless — ESPN's AWS WAF + invisible
   reCAPTCHA block `chrome-headless-shell` ("Max challenge attempts exceeded"). If the box
   has no usable display, start a **virtual headed display** with TigerVNC:
   `scripts/start-display.sh :1`, then run the browser with `DISPLAY=:1 HEADED=1`.
2. **One login attempt at a time.** Never run two login processes, and never rapid-retry.
   Concurrent/fast attempts trip ESPN's 2FA code-send rate limit
   ("unable to send you any more codes right now"). The script backs off ~12 min itself.
3. **Keep logins persistent.** The browser profile (cookies + localStorage) lives on disk at
   `state/espn-profile/` and is reused every run — you log in once, not every time. Also save
   `espn_s2` + `SWID` to `.secrets/espn-cookies.txt` for API use.
4. **If the profile gets "poisoned"** (repeated failures → the challenge error), throw it away
   and start a fresh profile (`ESPN_PROFILE=state/espn-profile-fresh`); a clean profile loads
   the login form fine.
5. **Never paste keys/cookies/codes into chat.** Creds live in `.secrets/` (600, root-only).
6. **Kill by PID, never by pattern.** `pkill -f login-interactive` matches the calling shell
   and SIGTERMs your own command. Use `kill <pid>` (or `pgrep -x node` + `/proc/<pid>/cmdline`).

## Workflow

### 1. Start the headed display (once)

```bash
cd skills/espn-fantasy/scripts
./start-display.sh :1          # starts Xvnc on :1, no-auth, localhost-only
```

### 2. Run the login (single instance)

```bash
DISPLAY=:1 XAUTHORITY=$HOME/.Xauthority HEADED=1 FULLCHROME=1 node login-interactive.mjs &
```

- Creds from `.secrets/espn-login.txt` (`ESPN_USER=`, `ESPN_PASS=`).
- **Headed** browser on the VNC display; persistent profile `state/espn-profile/`.
- Logs to `state/espn-login.log`; live screenshot `state/espn-live.png`.
- On success writes `.secrets/espn-cookies.txt` and logs `SUCCESS`.

### 3. Hand off the 2FA code

The account has email 2FA. When the log shows `2FA_PROMPT active`, ask the user for the code
from their email and drop it on disk:

```bash
printf '123456' > state/espn-2fa-code.txt
```

The running script picks it up within ~3s (it waits up to 45 min). Code = single-use, ~10 min TTL.

### 4. Use the API

Load `.secrets/espn-cookies.txt` (`espn_s2`, `SWID`) and call the fantasy API. See
`references/espn-fantasy-api.md`.

## Quick env reference

| Var | Effect |
|---|---|
| `HEADED=1` | run the real headed browser (required) |
| `DISPLAY=:1` | the VNC virtual display |
| `FULLCHROME=1` | use full Chromium build (needed for headless; harmless headed) |
| `ESPN_PROFILE=<dir>` | override profile dir (use for a fresh, un-poisoned profile) |

## Monitoring (local, no-LLM)

Never poll the ESPN API from the model (token burn + bot risk). Instead run `scripts/monitor.mjs`
on a **systemd user timer**. It diffs the league feed and appends only NEW events to
`state/espn-alerts.jsonl`; a quiet run produces nothing.

Watches: incoming/pending **trade proposals**, newly **executed transactions** (waivers, FA
adds/drops, completed trades), and **injury-status changes** on the user's roster.

Install (units already on this box):
```
~/.config/systemd/user/espn-monitor.service   # Type=oneshot -> node monitor.mjs
~/.config/systemd/user/espn-monitor.timer     # OnUnitActiveSec=12min
systemctl --user enable --now espn-monitor.timer
```
Surface alerts cheaply from a heartbeat: if `state/espn-alerts.jsonl` is non-empty, relay it to
the user then truncate; if empty, stay silent.

## Resources

- `scripts/start-display.sh` — start the virtual headed display (Xvnc).
- `scripts/lib.mjs` — browser launcher: persistent profile, headed/full-Chromium modes,
  stealth init.
- `scripts/login-interactive.mjs` — full flow: iframe fill, 2FA wait, rate-limit backoff,
  cookie capture.
- `scripts/tx.mjs` — WRITE helper: `setLineup`, `addDrop`, `quickLineup` (uses the verified
  bare-transaction format).
- `scripts/monitor.mjs` — no-LLM league watcher (diff -> alerts file).
- `references/login-flow.md` — exact selectors, failure modes, timings.
- `references/strategy.md` — team-management strategy (weekly rhythm, start/sit, waivers,
  trades/trade-radar, monitoring cron design), open questions, current status, rollout phases.
- `references/espn-fantasy-api.md` — fantasy API endpoints for reading/managing a team.
