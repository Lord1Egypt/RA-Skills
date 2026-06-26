# Reference — Common Errors

FRED returns errors as `{ "error_code": N, "error_message": "..." }`. Here are the ones you will hit, their causes, and the **exact reaction** to take.

---

## `400` — Bad Request

A deterministic client error. **Do not retry** — fix the request.

| `error_message` (typical) | Cause | Reaction |
|---------------------------|-------|----------|
| "...api_key is not registered." | Missing/invalid `FRED_API_KEY` | Surface a setup message ("FRED_API_KEY is missing or invalid"). **Never reveal the key.** Do not retry. |
| "...series does not exist." | Wrong `series_id` | Re-run `fred_series_search`; pick the correct ID; retry. |
| "Variable observation_start is not a valid date." | Bad date format | Use `YYYY-MM-DD`; retry. |
| "Variable units is not one of ..." | Invalid enum | Use a valid `units`/`frequency`/`aggregation_method`; retry. |
| "Variable tag_names is required." (generic) | Missing required param | Add the required param for that endpoint; retry. |

---

## `429` — Too Many Requests

Rate limit (~120 req/min per key). **Transient** — the server already retries with backoff.

| Cause | Reaction |
|-------|----------|
| Too many calls too fast | Slow down. Rely on **cache**. Stop looping per-item; fetch wide ranges in one call. If it still surfaces after retries, tell the user briefly and try again shortly. |

---

## Empty result (not an error)

A successful response with no data. The server adds a `note`.

```json
{ "observations": [], "count": 0, "note": "No observations for the given parameters..." }
```

| Cause | Reaction |
|-------|----------|
| Date range excludes all data | Widen `observation_start`/`observation_end`. |
| Wrong `series_id` | Re-search with `fred_series_search`. |
| Infrequent series in a narrow window | Use a broader window or coarser `frequency`. |
| Transform drops early periods (e.g. `pc1` removes first year) | Extend the start date. |

**Never** treat empty as zero, and **never** invent values to fill it.

---

## Transient upstream (`5xx` / timeout)

The server retries up to `FRED_MAX_RETRIES`. If it still fails:

| Reaction |
|----------|
| Report a temporary upstream issue; suggest retrying later. Do **not** fabricate data. |

---

## Golden rules

1. **`400` → fix, don't retry.**
2. **`429` → back off + cache.**
3. **Empty → refine, don't fabricate.**
4. **Never expose the API key** in any error explanation.

> Verification needed: confirm exact error strings at <https://fred.stlouisfed.org/docs/api/fred/>.
