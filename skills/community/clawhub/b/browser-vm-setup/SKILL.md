---
name: browser-vm-setup
description: Run a browser-driving agent on a Linux VM — Xvfb, Chromium launch traps, egress cost tiers. Use when headless fails on your VM or Chromium dies on launch. Stops at any bot defence.
metadata: {"clawdbot":{"emoji":"🖥️","requires":{"bins":["node","ssh","curl"]},"homepage":"https://openclaw.ai"}}
---

# Browser Agent on a VM — Provisioning, Xvfb, Egress Cost Tiers

**Stops at every defence: CAPTCHA / bot challenge / MFA / geo-gate / rate limit / block page → human hand-off, no evasion guidance.** What this skill does instead: make a Linux VM actually run a headed browser, keep the admin shell off the internet, and stop the egress bill from running away.

## Before you start — access, data, network

| Item | What this skill assumes | Default |
|---|---|---|
| Machine access | root/sudo on a Linux VM you own or rent | none — you provision it |
| Runtime | Node.js 22.19+ (24 recommended) | none — you install it (§8) |
| Gateway | the agent gateway is a **prerequisite** you install first, from its vendor's own docs | not installed by this skill |
| LLM key | one provider key, bring-your-own | none |
| Browser profile | may hold **your own** logged-in sessions | empty profile |
| Persisted on disk | cookies/session storage, screenshots, run logs, `~/.openclaw` config | local only |
| Screenshots | capture whatever is on screen, personal data included | on failure only, not per step |
| Retention | the purge cron of §8 — paste it into your own `provision.sh`; raise or lower the window deliberately | delete after 7 days |
| Network egress | target sites only, from the VM's own IP. **Proxies and webhooks send data off the machine** — opt-in, never on by default | direct IP, no proxy, no webhook |

Only drive accounts and data you own or are authorised to access. The target's ToS and applicable law (GDPR when personal data is involved: legal basis, minimisation, stated retention) are constraints on this procedure, not footnotes. If you cannot name the legal basis, do not run the job.

## When to Use

| Trigger | Action |
|---|---|
| "move my agent off my laptop" | §1 host decision → §8 GitOps provision |
| "the browser won't start on the VM" | §3 provisioning traps |
| "I want to watch the browser work" | §2 Xvfb + VNC over a tunnel |
| "headless fails on this site" | §2 headed compatibility mode |
| "403 from my VM but fine from home" | §5 — the run **stops**; a human decides if anything else is lawful |
| "should I expose the dashboard?" | §7 — no. Loopback + tunnel |
| Site answers CAPTCHA / block page / bot challenge / 403 / MFA, **or the target is geo-restricted** | **STOP. Hand to a human.** Not a routing problem |

## 1. Host decision

| Criterion | Cloud VM | Residential machine (mini-PC at home/office) |
|---|---|---|
| Cost | ~5–30 €/mo, predictable | hardware once, ~0 recurring |
| Uptime | ~99.9% datacenter SLA | ~95% — your ISP, your power, your router |
| **IP reputation** | **datacenter ASN → low trust by default** | **residential ASN → included, nothing to rent** |
| Remote admin / scaling | native (SSH, snapshots, resize) | needs setup; soldered RAM, hardware swap |
| Blast radius | disposable, rebuild in ~10 min | your home network |

**Decide on this line, not on price:** if the agent only touches open APIs and your own tools → VM, always. A target that default-denies datacenter ranges is not a host-sizing problem — the run stops there and a human rules on it (§5). A residential box is no free pass either: one home IP hammering a platform gets rate-limited on volume, no ASN required (§6).

## 2. Headless vs headed + virtual screen

On Linux with no `DISPLAY`, the browser tool **falls back to headless automatically** — no error, no warning. Check `echo $DISPLAY` before blaming the config.

```bash
sudo apt-get install -y xvfb x11vnc
Xvfb :99 -screen 0 1920x1080x24 &   # `&` dies at logout — systemd unit or xvfb-run for a daemon
export DISPLAY=:99

# Xvfb takes ~0.2-1 s to open its socket — polling avoids an intermittent
# "unable to open display" that looks like a broken install
until xdpyinfo -display :99 >/dev/null 2>&1; do sleep 0.2; done
xdpyinfo -display :99 | head -1
# Output: name of display:    :99

# Watch it live — from your laptop: ssh -L 5900:localhost:5900 user@vm → VNC to localhost:5900
x11vnc -storepasswd                 # writes ~/.vnc/passwd
x11vnc -display :99 -localhost -rfbauth ~/.vnc/passwd &
```

`-localhost` keeps it off the network; the SSH tunnel of §7 reaches it. It does **not** protect you from the machine: with `-nopw`, any local user or process on the VM can take the display — and the browser's logged-in sessions with it. Use `-rfbauth`, or accept `-nopw` only on a single-user throwaway VM.

**Headed = compatibility mode.** It renders through the real window/GPU path, so pages that break under headless (WebGL, video codecs, font metrics, layout-dependent widgets) usually just work. Cost: RAM/CPU per frame — enable on demand, not by default.

## 3. Provisioning traps

These four cost a day each, the first time.

| Symptom | Root cause | Fix |
|---|---|---|
| Chromium exits instantly, no usable error | The **snap** package is confined by **AppArmor**; the sandbox cannot spawn under a service account | Install the **`.deb`** (Google Chrome) or use the **Playwright-bundled Chromium**. Never snap on a headless server |
| `Failed to move to new namespace` / browser won't launch as service | Kernel user-namespace restrictions on the VM image | `noSandbox: true` — acceptable only because the VM is disposable and drives sites you are authorised to use |
| Tabs die randomly, blank pages, "Target closed" with no stack | **`/dev/shm` is 64 MB by default under containers** — Chromium's shared memory allocator silently runs out | `--disable-dev-shm-usage`, and/or raise the mount: `--shm-size=1g` (a `docker run` flag, not a Chromium one) or `mount -o remount,size=1G /dev/shm` |
| Slow, artifacted rendering on a VM with no GPU | Software GL fallback thrash | `--disable-gpu` |

```bash
# Chrome from .deb — never snap
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
google-chrome --version
# Output: Google Chrome 1XX.0.XXXX.XX

# Alternative: the runtime's own Chromium, already patched for CI
npx playwright install --with-deps chromium
```

Reference launch args for a VM: `--no-sandbox --disable-dev-shm-usage --disable-gpu`, `headless: true` (or `false` when `DISPLAY=:99` is up). **Registers, do not mix:** `noSandbox: true` is the profile key in `~/.openclaw/config.json`; `--no-sandbox` is the CLI flag it passes to the binary. Set one, not both.

## 4. Remote browser over CDP

Point the agent at a browser it does not own — it connects instead of spawning a local Chrome. Worth the network hop only for many isolated parallel sessions, or a browser that must live in its own container; one agent, one profile → local Chrome is simpler and free. In `~/.openclaw/config.json`:

```json
{ "browser": { "profiles": { "vm": { "cdpUrl": "ws://127.0.0.1:9222/devtools/browser/<id>", "attachOnly": true, "noSandbox": true } } } }
```

**Licence alert — non-obvious, and it bites at invoicing time.** Some browser-as-a-service projects ship under **SSPL**: commercial use is not covered by the free licence, and some features are reserved for the paid plan rather than the free image. Check the licence and the plan of the product you pick before you architect on it, not after.

## 5. Egress cost tiers and their limits

**The default egress is the VM's own IP, and this skill ships no other.** The table below exists to budget a tier a human has already approved for a named target — it is not a ladder the agent climbs by itself.

| Target class | Egress | Order of magnitude |
|---|---|---|
| Open APIs, your own tools, unprotected sites | **VM's direct IP** | ~0 |
| Your own infrastructure behind a fixed allowlist | **Datacenter proxy**, if *you* own the allowlist | low monthly, flat |
| Sites that default-deny datacenter ASNs | **not a tier — see the gray-area note below** | n/a |

```
attempt(url, egress=direct)
  → 200                                                → done, cost ~0
  → 403 / CAPTCHA / challenge / block page / geo-gate  → STOP, report, human hand.
                                                         No second attempt, no egress change.
```

> **GRAY-AREA — NOT RECOMMENDED, NEVER AUTOMATIC.** Renting residential/ISP egress (billed per GB, the line item that runs away) after a datacenter-range 403 is documented here only so you recognise it and gate it. A default-deny on datacenter ASNs **is an anti-abuse control**; buying a consumer IP to turn its 403 into a 200 routes around that control. The agent must never do it on its own initiative, never as a retry, never as a default. It is a human decision, per target, before the run — and if any row below is unclear, the answer is no. A geo-gate states who the site serves; a challenge states it does not want an automated client. Both are answers, not errors.

| Gate — all must hold before a human may approve a non-direct tier | |
|---|---|
| Written authorisation from the target operator for automated access | required |
| The target's ToS permits it, in writing, for this use | required |
| A named legal basis for any personal data touched (GDPR) | required |
| The tier is set in config for that one target, by the human, before the run | required |
| The response was a plain 403 on ASN, **not** a challenge, CAPTCHA, or geo-gate | required — those always stop |
| Provider credentials in a secret manager, never in the repo | required |
| A target reachable only from another market → **lawful local presence, not a rented IP** | no exception |

## 6. Load & authorisation rules

Not tips — rules. They keep you inside published rate limits, inside the authorisation you actually have, and off someone else's servers' backs.

| Rule | Value |
|---|---|
| Egress geography | route from the market you are authorised to operate in — a legal and latency question, settled before the run, not during it |
| Fingerprint | **stable** across runs — one persistent profile, not a fresh identity per run: a stable profile is what keeps cookies and sessions valid |
| Cadence | 2–5 s between actions. Sequential, rate-limited — the target's serving capacity is a real constraint and you stay under the published limit |
| Frequency on sensitive platforms | **1 run/week max** |
| Parallelism on a sensitive target | **never**. One session, one job |
| Sessions | persist cookies; re-login **only on 401** — every re-login is avoidable load on the target's auth path |
| MFA | route the prompt to a human channel and wait. Never automate around it |
| On any challenge | stop, log, notify. Never tune timing or behaviour to make a defence stop firing |

## 7. Hardening & access

The agent gateway is a **prerequisite**: install it from its vendor's own documentation before this section. This skill does not fetch or run an installer. Once it is up, it listens on `127.0.0.1:18789` by default and its dashboard **executes shell**. Treat it as a root console, because it is one.

```bash
# Bind loopback only — never 0.0.0.0
ss -ltnp | grep 18789
# Output: LISTEN 0 511 127.0.0.1:18789 ... users:(("node",pid=...))

# Reach it from your laptop
ssh -L 18789:localhost:18789 user@vm     # then open http://localhost:18789
```

A mesh network (e.g. Tailscale) is the same trade with less tunnel babysitting. Public exposure is not an option to weigh — it is an admin shell on the internet. Baseline around it: non-root user, UFW default-deny inbound, SSH keys only, secrets in a manager or a gitignored `.env`.

**Why OAuth still completes through the tunnel:** the dashboard opens in your *laptop's* browser at `localhost:18789`, so the provider's redirect back to `localhost` lands in the same browser that started the flow — nothing is exposed and the callback closes normally. Ship a public URL and you get the callback and the shell exposed at once.

## 8. GitOps — the VM is disposable

Everything is in the repo; the VM is a cache of it. Grill the VM → rebuild in ~10 min.

```
repo/
  provision.sh        # yours to write, idempotent: [ -x /usr/bin/google-chrome ] || install...
  deploy.sh           # git pull && restart daemon
  .env.example        # names only, never values
  .github/workflows/  # push main → ssh → ./deploy.sh
  openclaw/           # versioned ~/.openclaw config + SKILL.md files
```

`provision.sh` must be safe to re-run on a live box. Group your guards — `A || B && C` parses as `(A || B) && C`, so the "guarded" install runs anyway and can downgrade a working runtime mid-flight. And **retention is executed, not declared**: the purge cron below is what enforces the 7-day window announced above — install it, or do not announce a window.

```bash
if ! command -v node >/dev/null; then
  # Distro repo first. Newer major? NodeSource ships a setup script: download and read
  # it before running. Piping a remote script into sudo bash is the operator's call.
  sudo apt-get install -y nodejs
fi
node -v          # Output: v22.x.x

# Retention — screenshots and logs may hold personal data
mkdir -p ~/.openclaw/screenshots ~/.openclaw/logs   # find errors on a missing dir; cron then mails you nightly
( crontab -l 2>/dev/null | grep -q openclaw-purge ) || \
  ( crontab -l 2>/dev/null; \
    echo '17 4 * * * find "$HOME/.openclaw/screenshots" "$HOME/.openclaw/logs" -type f -mtime +7 -delete >/dev/null 2>&1  # openclaw-purge' \
  ) | crontab -

# Verify it landed, then prove it deletes: plant a file past the window, run the finder by hand
crontab -l | grep -c openclaw-purge          # Output: 1
touch -d '8 days ago' ~/.openclaw/logs/purge-probe.log
find "$HOME/.openclaw/logs" -type f -mtime +7 -delete
ls ~/.openclaw/logs/purge-probe.log
# Output: ls: cannot access '.../purge-probe.log': No such file or directory
```

Change the window in one place — the `-mtime +7` of the crontab line — then re-run the verify; an unverified retention claim is a false claim. Snapshot before every risky change. Two schedule traps: keep unattended upgrades **security-only** — an unscheduled reboot mid-run loses the session; and some hosts require ID documents at signup, so budget a delay, not an afternoon.

## Deploy checklist

| Human does | Build does |
|---|---|
| Host account + ID verification → API token | Repo skeleton (provision, deploy, Actions, `.env.example`) |
| Install the gateway from its vendor's docs (prerequisite, §7) | VM + hardening (non-root, UFW default-deny, SSH keys, fail2ban) |
| LLM API key | Node + daemon install |
| Approve which accounts the agent may use | Chrome `.deb` (not snap) + launch args of §3 |
| Complete OAuth in the tunnelled dashboard | Optional: Xvfb + x11vnc, loopback only |
| Confirm or change the retention window | Retention cron installed **and verified** (7 d default) |
| Name the legal basis if personal data is touched | Direct egress only; any other tier is human-approved per target (§5) |
| Rule on any §5 gray-area request, before the run | Crons + heartbeat + end-to-end test + handover doc |

## Output Format

Emit this after every provisioning run — verbatim, one block, to your log or alert channel:

```
VM: [host/region] · [vCPU]/[RAM] · rebuilt-from: provision.sh@[commit]
BROWSER: [chrome-deb|playwright-chromium] [headless|headed:99] · shm=[size] · sandbox=[off|on]
EGRESS: [direct|other] · geo=[XX] · non-direct-approved-by=[human name|n-a]
ACCESS: dashboard=127.0.0.1:18789 via [ssh-tunnel|mesh] · public=no
DATA: persists=[cookies,screenshots,logs] · retention=[N days] · purge-cron=[verified|absent] · webhooks=[none|list]
CHECKS: display=[ok] · browser-launch=[ok] · heartbeat=[ok] · daemon=[ok]
BLOCKED: [none | target + response code + human action needed]
```

Filled instance:

```
VM: eu-central · 4/16 · rebuilt-from: provision.sh@a1b2c3d
BROWSER: chrome-deb headed:99 · shm=1g · sandbox=off
EGRESS: direct · geo=FR · non-direct-approved-by=n-a
ACCESS: dashboard=127.0.0.1:18789 via ssh-tunnel · public=no
DATA: persists=[cookies,screenshots,logs] · retention=7 days · purge-cron=verified · webhooks=none
CHECKS: display=ok · browser-launch=ok · heartbeat=ok · daemon=ok
BLOCKED: none
```

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| Browser silently headless though headed was configured | no `DISPLAY` → automatic fallback, no error raised | `export DISPLAY=:99` in the **daemon's** environment, not just your shell |
| `unable to open display :99` right after starting Xvfb | socket not up yet (~0.2–1 s) | poll with the `until xdpyinfo` loop of §2 |
| `DISPLAY` gone after logout | `Xvfb ... &` died with the login shell | systemd unit or `xvfb-run` (§2) |
| Chromium dies at launch, empty log | snap + AppArmor confinement | reinstall from `.deb` or use Playwright's Chromium (§3) |
| Random blank tabs under load | `/dev/shm` = 64 MB | `--disable-dev-shm-usage` + raise shm |
| OAuth callback never returns | dashboard opened via a public URL, not the tunnel | tunnel + `localhost:18789` (§7) |
| Files older than the retention window still on disk | cron never installed, or `crontab -l` was never checked | re-run the §8 block **including the verify and the probe** |
| Egress bill above the direct-IP baseline | something other than direct egress is configured | direct is the only default (§5); revert, then ask who approved the tier |
| Works from laptop, 403 from VM | datacenter ASN default-deny | **STOP.** Not an escalation trigger — §5 gray-area, human rules on it before anything else |
| VNC reachable from the internet | `x11vnc` without `-localhost` | kill it, relaunch with `-localhost -rfbauth ~/.vnc/passwd`, reach it via SSH `-L` (§2) |

## Scope

**This skill ONLY:** picks a host for a browser-driving agent; mounts a virtual screen; fixes documented Chromium-on-Linux launch failures; budgets egress by cost tier; keeps the admin shell off the public internet; makes the VM reproducible from a repo and its data purged on a schedule.

**This skill NEVER:**
- solves, bypasses or routes around CAPTCHAs, bot challenges, MFA, block pages or rate limits — when a defence fires, the run stops and a human takes over;
- changes egress on its own initiative to get past a block — a datacenter-range 403 stops the run; any other tier is a gray-area human decision under the §5 gate, and is not recommended;
- routes around geo-restrictions — a geo-gate is a stated restriction; if the target is geo-blocked, the answer is a lawful local presence or nothing;
- tunes timing or fingerprints to evade detection;
- represents the agent as a human, or hides that an agent is operating. Where the target offers an API, documented automation terms or a declared bot identity, use that rather than driving the UI;
- touches accounts or data you are not authorised to use;
- collects personal data without a named legal basis, minimisation and an enforced retention limit;
- exposes the gateway dashboard publicly.

---
Maintained by Alexandre Bloch (Bloch Agents) · ClawHub `@AlexBloch-IA` · alex.bloch55@gmail.com
