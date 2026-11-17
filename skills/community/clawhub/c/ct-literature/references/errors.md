# Error Catalogue · ct-literature

| Error | Cause | Fix |
|---|---|---|
| `urllib.error.URLError` / timeout (after retries) | No network / proxy / outage | Auto-retried with exponential backoff (4 attempts, honors `Retry-After`); if still failing, confirm api.openalex.org reachable; configure proxy |
| Semantic Scholar HTTP 429 | No-key rate limit | Expected — source is skipped; rely on OpenAlex + Europe PMC |
| OpenAlex HTTP 401 / persistent 429 | Invalid key / daily quota exhausted | Re-copy key from settings/api; confirm `.env` loaded (see references/openalex_key.md) |
| Empty results | Topic too narrow / wrong spelling | Broaden topic; drop `--review-type` / year filter |
| DOI dedupe merged too aggressively | Two papers share a DOI typo | Rare; inspect `merged.json` and re-run a single source if needed |
