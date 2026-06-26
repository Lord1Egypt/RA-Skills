# FMP Common Errors Reference

How to recognize each failure and react correctly. Golden rules: **fix-don't-retry** for auth; **back-off-and-cache** for rate limits; **re-resolve** for empty results; **never expose the key** in any error path.

---

## 1. `{"Error Message":"..."}`

- **Shape:** JSON object with an `Error Message` field instead of the expected array.
- **Cause:** malformed request — bad/missing param, unknown symbol format, invalid endpoint, or a plan restriction described in the message.
- **Agent reaction:** read the message; correct the specific problem (fix the param, re-resolve the symbol, switch endpoint). Do **not** present partial or fabricated data. If the message indicates a plan limit, tell the user this data isn't available on the current plan.

---

## 2. HTTP 401 — invalid API key

- **Shape:** 401 status and/or a message like "Invalid API KEY".
- **Cause:** missing, wrong, or revoked `FMP_API_KEY`.
- **Agent reaction:** **Stop. Do not retry** (retrying never fixes auth and wastes attempts). Tell the user the key is invalid and must be corrected in the environment. Never display the key value.

---

## 3. Account suspended

- **Shape:** error/message indicating the account is suspended or disabled (may accompany 401/403).
- **Cause:** billing/quota/ToS issue on the FMP account.
- **Agent reaction:** **Do not retry.** Inform the user the FMP account is suspended and needs attention in their FMP dashboard. Do not attempt other endpoints hoping one works.

---

## 4. HTTP 429 — rate / quota limit

- **Shape:** 429 status, possibly a "limit reached" message.
- **Cause:** too many calls — free tier is ~250 calls/day; per-second/minute caps may also apply.

> Verification needed: confirm current limits at https://site.financialmodelingprep.com/developer/docs.

- **Agent reaction:** **back off** (wait, then retry with increasing delay), and **cache** results to avoid repeat calls. Reduce call volume (batch quotes, lower `limit`). Tell the user if you're rate-limited and may be slower or incomplete. Do **not** hammer in a tight loop.

---

## 5. Empty array `[]`

- **Shape:** HTTP 200 with an empty JSON array.
- **Cause:** **wrong/unknown symbol**, or the symbol/data **isn't covered by the plan** (e.g. non-US ticker on the US-only free tier), or no rows for the requested period/range.
- **Agent reaction:** do **not** interpret as zero. Re-run symbol resolution (search + profile); widen/adjust `period`/`from`/`to`; or explain the coverage limitation. State clearly "no data returned" rather than inventing a value.

---

## 6. Timeout / 5xx (transient)

- **Shape:** request hangs, 500/502/503/504.
- **Cause:** temporary server/network issue.
- **Agent reaction:** retry a small number of times with backoff. If it persists, report a likely FMP outage and stop.

---

## Quick decision table

| Symptom | Retry? | Action |
|---------|--------|--------|
| `{"Error Message"}` | No (fix first) | Correct param/symbol/endpoint |
| 401 invalid key | **No** | Stop; tell user to fix key |
| Account suspended | **No** | Stop; tell user to resolve account |
| 429 | Yes, with backoff | Wait + cache + reduce calls |
| `[]` empty | No (re-resolve) | Fix symbol or explain coverage |
| Timeout / 5xx | Yes, limited backoff | Retry few times, else report outage |
