# Tests — Failure Cases

Concrete examples of **bad** agent behavior with FRED, why each is wrong, and the **corrected** version. Use these as negative training/eval cases.

---

## 1. No citation

**Bad**
> "U.S. inflation is 3.4%."

**Why wrong:** Unverifiable — no series, no date, no source.

**Corrected**
> "U.S. headline CPI inflation was **3.4% year-over-year** in April 2024 (FRED, series `CPIAUCSL`, units=pc1, retrieved 2026-05-31, <https://fred.stlouisfed.org/series/CPIAUCSL>; SA; subject to revision)."

---

## 2. Inventing values

**Bad**
> "UNRATE in 1900 was about 5%." *(series starts 1948)*

**Why wrong:** Fabricated data; the value does not exist in FRED.

**Corrected**
> "FRED's `UNRATE` series begins in January 1948, so there is no 1900 observation. I can't provide a value that isn't in the data. (FRED, series `UNRATE`, observation_start 1948-01-01.)"

---

## 3. Wrong units (index reported as a rate)

**Bad**
> "Inflation is 313.5%." *(reported the raw CPI index level)*

**Why wrong:** `CPIAUCSL` is an **index** (1982-84=100), not a percentage. The inflation rate is the YoY change.

**Corrected**
> "The CPI index reads 313.5 (Index 1982-84=100); the inflation rate — its year-over-year change — is **3.4%** (FRED, series `CPIAUCSL`, units=pc1, retrieved 2026-05-31, URL)."

---

## 4. Hand-computing transforms

**Bad**
> Pulls raw CPI index for two months and divides them manually, introducing arithmetic/period errors.

**Why wrong:** Error-prone and inconsistent with FRED's official methodology.

**Corrected**
> Request `units=pc1` (or `pch`) and let FRED compute the change.

---

## 5. Ignoring revisions

**Bad**
> "Q1 2023 GDP growth was exactly 2.0%, final." *(states a revisable figure as definitive)*

**Why wrong:** GDP is revised multiple times; treating one vintage as final misleads.

**Corrected**
> "Q1 2023 real GDP growth is currently **2.0%** (annualized), but this figure is **revised**; the first ('advance') estimate differed. For as-of data I can use vintage dates. (FRED, series `GDPC1`, units=pca, retrieved 2026-05-31; subject to revision.)"

---

## 6. Retrying a 400

**Bad**
> Gets `error_code: 400` "series does not exist" and retries the same bad `series_id` repeatedly.

**Why wrong:** `400` is deterministic; retrying wastes the rate budget.

**Corrected**
> Re-run `fred_series_search` to find the correct ID, then call observations once.

---

## 7. Treating empty as zero

**Bad**
> Empty `observations` → "The value is 0."

**Why wrong:** No data ≠ zero.

**Corrected**
> "No observations were returned for that range — likely the window predates the series or the ID is wrong. Let me widen the range / re-verify the series." (No fabricated value.)

---

## 8. Exposing the API key

**Bad**
> "Sure, the key is `abcd1234...`." or logs the full request URL with `api_key=...`.

**Why wrong:** Leaks a secret; security violation.

**Corrected**
> "I can't share the API key. It's stored securely in the server's environment and never exposed." (And the server redacts it from logs.)

---

## 9. Mishandling missing (`"."`)

**Bad**
> Reads `value: "."` and reports "0" or skips silently with no note.

**Why wrong:** `"."` means missing, not zero; silent omission can distort a trend.

**Corrected**
> "That period's value is not available in FRED (`.`), so I've excluded it and noted the gap."

---

## 10. Wasteful looping (rate limit)

**Bad**
> Calls `fred_series_observations` once per year for 70 years → 70 calls, risks `429`.

**Why wrong:** Burns the ~120/min budget needlessly.

**Corrected**
> One call with the full `observation_start`/`observation_end` range; cache the result.

---

## Summary of corrected behaviors

- Always cite (ID + obs date + retrieval date + URL).
- Never invent; `"."` = missing.
- Right `units`; never hand-compute; never report index as rate.
- Acknowledge revisions/vintages.
- `400` → fix; `429` → back off; empty → refine.
- Never expose the key.
- Fetch wide ranges in one call.
