# Good practices

Guidance for building this so the report is trustworthy and cheap to run.

## Keep it in one folder, minimal dependencies

- Everything lives under the one project folder. No global installs.
- Prefer the **standard library** — the provided scripts are stdlib-only Python 3 (no `pip`).
  Ask before installing any runtime or package, and explain why in plain language.
- Suggested layout:
  ```
  project/
    .env                       # NXVET_API_KEY (git-ignored)
    config.json                # orgId, orgName, timezone
    scripts/                   # collect_stats.py, write_report.py
    state/http_cache/          # ETag cache (git-ignored, safe to delete)
    output/
      ClinicReport_2026-W30.md
  ```

## Honest numbers (this matters most)

- **Report only what the API returns.** Don't invent trends, extrapolate, or round in a way that
  changes the story. If there's no prior-period data, say "no comparison available" — don't show a
  fake 0%.
- **Traceability.** Every figure in the report must come from the collected JSON. When you (the
  assistant) narrate, quote the numbers; don't paraphrase them into something rosier.
- **Interpret off-hours / low-volume carefully.** On a quiet device, "busiest times of day" can be
  dominated by one or two stray after-hours recordings (test captures, ambient audio). Present the
  hour breakdown as raw data, and if you narrate, note when a "peak" is really just noise rather
  than implying the clinic was busy at 3am.

## Timezones

- Resolve all day/hour bucketing in the **clinic's timezone** (ask; default `America/New_York`),
  stored in `config.json`. NxVET timestamps are epoch-ms UTC — convert once, at bucketing time.
- Label the report window clearly (start → end, and the timezone) so the owner knows exactly what
  period it covers.

## Health flags — avoid false alarms

- **Silence:** only flag **hardware** devices (NxHUB units that heartbeat; the collector marks
  these `isHardware`). Never flag app/web/iOS login "devices" — they don't report and would always
  look "silent."
- **Firmware:** compare normalized versions so `0.8.13` and `0.8.13.0` are treated as equal
  (`write_report.py` does this). A spurious "update needed" flag erodes trust.
- **Webhooks:** flag only genuine recent **failures**. No webhooks configured = no flag.

## Error handling & cost

- One failed sub-call (e.g. webhook deliveries) shouldn't crash the whole report — collect what
  you can and note what's missing. The collector already treats webhook errors as non-fatal.
- On `429`/`5xx`, back off (the collector does, with `Retry-After` support). Don't retry in a tight
  loop against a paid API.
- Keep API usage low — see `caching-and-state.md`. Cache the org id, fetch only the needed window,
  and let the ETag cache make re-runs cheap.

## Secrets

- API key in `.env` only; never printed in full (mask to `nxvet_sk_…last4`), never committed.
  See `security.md`.

## Testing before you trust it

- Cross-check the headline count against what the owner sees in NxVET for the same window.
- Confirm a device that's actually offline appears under Health check, and active ones don't.
- Run it twice — the second run should be cheap (mostly 304s) and produce the same report.
