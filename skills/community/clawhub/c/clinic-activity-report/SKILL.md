---
name: clinic-activity-report
description: Generate a plain-English weekly CLINIC ACTIVITY REPORT for a veterinary clinic owner from NxVET data — total recordings, per-device and per-day/hour breakdown, week-over-week trend, and health flags (silent devices, out-of-date firmware, failing webhooks). Read-only and local; nothing is sent or changed. Use when a clinic owner/manager wants a recurring "how's the clinic doing" summary.
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - NXVET_API_KEY
    primaryEnv: NXVET_API_KEY
    emoji: "📊"
    homepage: https://api.nx.vet/skills.html#clinic-activity
---

# Clinic Activity Report (local, read-only)

> **A NxVET recipe for AI coding agents.** Point Claude Code, Codex, Cursor, or any
> LLM-based agent at this file and say *"Read SKILL.md and implement it — start with Phase 0."*
> The recipe is agent-neutral: plain Markdown plus two dependency-free Python scripts.
> See `INSTALL.md` for how to load it into a specific agent.

Build a small, **local, read-only** tool that gives a veterinary **clinic owner or manager** a
recurring, plain-English snapshot of how the clinic is doing — the kind of thing they'd want
every Monday morning:

- **How busy** — total recordings this week, and the trend vs last week.
- **Where** — a breakdown by device (exam room), by weekday, and by time of day.
- **What needs attention** — a health check flagging devices that have gone **silent**, devices
  on **out-of-date firmware**, and **failing webhooks**.

Output is a readable **markdown report** (`output/ClinicReport_YYYY-Www.md`) the owner opens and
reads. Optionally also a simple self-contained **HTML dashboard**.

## Ground rules (non-negotiable)

1. **Read-only.** The tool only makes authenticated `GET` calls to the NxVET API
   (`https://app.nx.vet`). It never creates, edits, deletes, or sends anything.
2. **Local-only.** No telemetry, no third-party services, no email. The report is a local file
   the owner reads. There is **no send path** — if they want to share it, they do so themselves.
3. **Secrets hygiene.** The API key lives in `.env` as `NXVET_API_KEY=nxvet_sk_...`. Never print
   the full key; never commit it; never paste it anywhere that leaves the machine. See
   `reference/security.md`.
4. **Honest numbers.** Report what the API actually returns. Don't invent trends or extrapolate;
   if there's no prior-period data, say so. Flag data you're unsure about rather than guessing.

## Prerequisites (tell the user if they're missing any)

1. **A NxVET account** — sign up at https://app.nx.vet/ if the clinic isn't set up yet.
2. **A NxVET API key** — https://app.nx.vet/integrations → API Keys tab (starts `nxvet_sk_`).
3. **At least one recording device** capturing consults. Owners typically have one or more
   **NxHUB** devices (https://nx.vet/products/nxhub); the report is most useful with real
   recording activity to summarize.

## How to build it — phases

### Phase 0 — Connect and verify

1. Ask the owner for the API key. Write `.env` with `NXVET_API_KEY=...`. Confirm `.env` is
   git-ignored.
2. Call `GET /api/auth/me` (or the `get_identity` MCP tool). Confirm HTTP 200 and capture the
   `organizationId` and `organizationName`. Save them to `config.json`, along with the clinic
   **timezone** (ask; default `America/New_York`).

### Phase 1 — Collect the stats

Use `{baseDir}/scripts/collect_stats.py` (stdlib-only Python 3; no pip installs). It reads `.env` +
`config.json` and prints a single JSON object with the week's numbers:

```bash
python3 {baseDir}/scripts/collect_stats.py --days 7        # last 7 days, clinic timezone
python3 {baseDir}/scripts/collect_stats.py --days 7 --end 2026-07-20   # a specific week
```

It gathers: total recordings in the window and the **previous** window (for the trend), a
per-device / per-weekday / per-hour breakdown, the **device fleet** with last-seen times and
firmware, and **webhook** delivery health. See `reference/nxvet-api.md` for the endpoint quirks
it handles (the transcript/label gotchas, `types=` filter, epoch-ms timestamps).

### Phase 2 — Write the report

Two ways, pick based on how the tool runs:

- **Deterministic (headless / scheduled):** pipe the JSON through `scripts/write_report.py`:
  ```bash
  python3 {baseDir}/scripts/collect_stats.py --days 7 \
    | python3 {baseDir}/scripts/write_report.py --out "output/ClinicReport_$(date +%Y-W%V).md"
  ```
- **Narrated (interactive):** you (the assistant) read the JSON and write the report yourself,
  adding a short plain-English interpretation at the top ("Quiet week — down 18%, and the
  Reception device has been offline since Tuesday; worth checking."). Keep the same sections.
  Do **not** invent numbers the JSON doesn't contain.

Report sections: **At a glance** (total + trend + device count), **Recordings by device**,
**Busiest days**, busiest **times of day**, and a **Health check** (silent devices, firmware,
webhooks). Every figure traces back to the collected JSON.

### Phase 3 — Health flags (get these right)

- **Silent device:** only flag **hardware** devices (NxHUB units that heartbeat — the collector
  marks these `isHardware`). Never flag app/web/iOS login "devices" as silent. Default threshold:
  no report in **3+ days**.
- **Firmware:** flag only when the installed version genuinely differs from the target. Treat
  `0.8.13` and `0.8.13.0` as the **same** (ignore trailing-zero formatting) — `write_report.py`
  already does this.
- **Webhooks:** flag a webhook only if it has recent **failed** deliveries. No webhooks = no flag.

### Phase 4 — Run it weekly (optional)

Set it up with the OS-native scheduler (detect the OS first): `launchd` on macOS, Task Scheduler
on Windows, `cron` on Linux. A good default is **Monday 7am**. Each run writes a new dated report
and leaves the previous ones in place, so the owner builds a history.

## Acceptance checklist (the demo)

- [ ] Run the tool → a `ClinicReport_YYYY-Www.md` appears and reads clearly.
- [ ] The total and per-device counts match what the owner sees in NxVET.
- [ ] A device that's actually offline shows under Health check; active devices don't.
- [ ] Firmware that only differs by trailing `.0` is **not** flagged.
- [ ] Re-running doesn't change anything in NxVET (it's read-only).

## Keeping API cost low

The collector keeps a small ETag cache in `state/http_cache/` and sends `If-None-Match` on
repeat calls, so re-runs and the rarely-changing prior-period window mostly return cheap
`304 Not Modified` responses. Cache the org id in `config.json` so `/auth/me` isn't re-called,
and fetch only the window you need. Full detail in `reference/caching-and-state.md`.

## Reference files

- `reference/nxvet-api.md` — endpoints, auth, and the data-format gotchas the collector relies on.
- `reference/security.md` — secrets, the read-only/local guarantee, what to send if stuck.
- `reference/caching-and-state.md` — how the tool keeps NxVET API usage (and your server cost) low.
- `reference/good-practices.md` — honest numbers, timezones, avoiding false health alarms, testing.
