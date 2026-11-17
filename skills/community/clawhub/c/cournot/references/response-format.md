# Response formatting

Read this reference after a successful probability response.

Use only fields returned by the API. Do not browse for more evidence, produce another estimate, or invent sources, weights, scenarios, per-source probabilities, links, advice, or rationale. The Cournot result is the answer.

If `result` is present, use its returned fields for the assessment summary. Prefer `result.point_estimate` for the headline. Use the display-normalized market title only in that probability headline. Never add a separate `Reference market:` line in any language or repeat the market title and market price below the headline. Display all returned `result` fields in one markdown table using only columns actually returned. Render probability decimals as percentages without changing their meaning: `0.035` → `3.5%`, `[0.02, 0.06]` → `2%–6%`. Leave enum strings unchanged.

Whenever `basis` is present and non-empty, displaying it is mandatory. Introduce it as `External data basis:`, localized to the user's language, then render every returned field in API order as markdown tables. Do not omit sections or move their content into prose. Copy string values verbatim without translating, paraphrasing, shortening, or supplementing them. Escape `|` in cells and replace embedded newlines so tables remain valid.

The client removes each basis `url` field and embeds every valid HTTP(S) link into display text. When a `summary` contains quoted text, that quoted text is the link; otherwise the entire `summary` value is the link. Keep `source` as plain text. Preserve this Markdown exactly so it remains clickable. Never add a separate `url` column or print a bare basis URL.

The client normalizes ISO timestamps anywhere inside `basis`, including timestamps embedded in longer `summary` strings and unrecognized nested fields. Display the normalized value exactly as `YYYY-MM-DD HH:mm:ss UTC`, for example `2000-01-01 20:00:00 UTC`. Never restore ISO `T`, a trailing `Z`, milliseconds, or convert the value to the user's local timezone.

For a structured object, render each present section separately:

- `primary_anchor`: one table with returned keys as columns and one row.
- `price_distance`: one table with returned keys as columns and one row.
- `cross_checks`: one table using the union of returned item keys and one row per item in array order.
- `limitations`: one-column `limitation` table with one row per item in array order.

Format probability and return decimals with percentage equivalents, and USD fields with readable separators, without changing values. For example, `displayed_probability: 0.03` renders as `3%`, `required_return: 0.8993` as `89.93%`, and `volume_usd: 2813626` as `$2,813,626`. Do not interpret a price target as a probability.

Never drop new or unrecognized basis data: render an array of objects using the union of its keys, a scalar array as a one-column table, and another nested object as a `path | value` table with one row per scalar leaf.

For an older non-empty `basis[]`, show every item in API order in a `source | summary | time` table, copying values verbatim and preserving embedded links. If `basis` is absent, null, an empty object, or an empty array, say no external basis data was returned.

Suggested structure:

```text
The probability of {display-normalized title} is {point_estimate or probability as percent}%.

Cournot assessment:

| {returned result columns only} |
|---|
| {returned values} |

External data basis:

{tables for every returned basis section and field}

{Billing route and remaining calls from the returned fields.} This is an assessment of pricing, not investment advice.
```

Use `data.billing` for the footer. Its field names and the `charged` flag are internal interpretation rules, not text to print or explain to the customer. Use a short natural sentence in the user's language, such as “This used a prepaid call; 586 remain.” or “This used a free call; 2 remain.” Do not print `free_quota`, `api_key` or `charged=false` as billing labels.

Interpret billing as follows:

- `free_quota`: this query used the lifetime IP free allowance; show `free_quota.remaining` when present. No daily reset. If no prepaid balance was returned, omit it; do not call account solely to fill the footer.
- `api_key`: this query used prepaid calls; show `api_key_quota.remaining` when present. `charged=false` means no on-chain payment, **not** no quota deduction.
- `x402`: this query was paid on-chain; include returned transaction hash and network. Show only quotas that were actually returned.
- Missing billing or quota: say that the billing route or remaining balance was not returned. Never treat missing/null as zero or calculate current balance from an earlier response.

If a future response explicitly supplies `answered=false`, explain the returned reason. Only assert that no calls were deducted when the response explicitly confirms that fact; the current contract does not define an `answered` guarantee. On server/network errors the outcome may be unknown: stop and offer `balance`, never retry automatically.

Keep the pricing-assessment disclaimer. Do not invent a rule-version identifier absent from the response.
