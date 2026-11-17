# Divergence ranking

Read for `/cournot divergence [count]`, including its payment and error follow-ups. This ranks cached Cournot probabilities against cached market prices. Do not resolve markets, request a fresh probability, browse for evidence, or add analysis.

## Input and request

Only the first word after `/cournot` triggers `divergence`; an event containing that word elsewhere stays in [query-flow.md](query-flow.md). Interpret all text after the command as a count: `50`, `top 20`, and equivalent natural-language counts in the user's language become integer limits. No text means omit `--limit` entirely so the backend uses its default of 10. For ambiguous, noninteger or out-of-range counts, explain the integer range 1–100 and ask for a new count without making an API call. Never truncate, clamp, or ignore unrecognized text.

An explicit count requires both `--limit` and `--count-text`: copy the entire original count suffix unchanged, using safe shell quoting. Examples: `--limit 50 --count-text '50'`, `--limit 20 --count-text 'top 20'`. Preserve non-English count text in its original language too. The client rejects mismatched numeric conversions, including truncating `2.5` to `2` or clamping `101` to `100`. Do not change the original text to bypass a rejection. For an omitted count, omit both flags. The original text is validation context only and is never sent to the API.

Before making the request, determine the reply language from the user's actual request and conversation. The English `divergence` keyword, API titles and documentation examples do not select the reply language. Supply all three row labels in that language with the required `--labels-json`, including for an omitted/default count. You choose the wording once; JS applies it to every row without detecting a language or falling back to English. Missing or incomplete labels fail locally before the request. Direction labels must mean only "Cournot above market" and "Cournot below market". The `link` label is the visible link text and means "View"; do not append the URL to that text.

- Chinese request: `--labels-json '{"cournot_above":"Cournot 高于市场","cournot_below":"Cournot 低于市场","link":"查看"}'`
- English request: `--labels-json '{"cournot_above":"Cournot above market","cournot_below":"Cournot below market","link":"View"}'`
- Other languages: localize all three values to the user's language too. These examples do not restrict supported languages to Chinese and English.

Never pass `--language` to `divergence`, including payment previews with `--per-call true`. That option belongs to pack commands; divergence accepts localized row labels only.

Example in English (localize the values for the actual user):

```sh
node <skill-root>/scripts/cournot-client.mjs divergence --labels-json '{"cournot_above":"Cournot above market","cournot_below":"Cournot below market","link":"View"}' > '<unique-page-result.json>'
```

Divergence uses the same production default as event queries, `https://interface.cournot.ai`. An explicit supported environment override takes precedence. Preserve the same origin for this operation's payment preview, execution, credential setup and account follow-ups, and use only credentials belonging to that origin.

Use default JSON output and save it to a unique local result file. It contains only the current page's `rows_markdown`, `pagination`, and `response.data` with batch timestamps and billing evidence. Raw market items are omitted from this model-facing result. For more than 20 items, the client automatically saves the full sanitized snapshot privately and returns its path in `pagination.snapshot_file`. Do not print or read that full snapshot into model context. `--output markdown` is a rows-only convenience; it omits the pagination and metadata needed for a complete answer. Do not make a second request to recover metadata. Labels are local rendering context and are not sent to the API.

Save stdout with shell redirection as above; there is no `--output-file` flag. A local CLI argument-validation error happens before any HTTP request: correct unsupported flags or missing localized labels using this reference, then make the initial query once. This does not permit repeating a query after a network, API or response-validation failure.

The client sends GET `/intelligence/v1/divergence`, appending `?limit=N` only for an explicit count, with no request body. A configured origin-bound key is included internally. One invocation authorizes one request; count does not change billing. Use the selected service's returned free allowance, prepaid balance and payment requirements; do not infer that they are shared with a different origin. Never automatically retry or fall back to a wallet.

For exhausted allowance, offer topup, import or per-call payment. Only after the user selects per-call payment, repeat the same command with `--per-call true` and follow [payment.md](payment.md). Keep the count, row labels, operation and origin through confirmation. `execute` replays the same GET and returns `rows_markdown` with response metadata. A topup does not automatically rerun it. Interpret other errors with [errors.md](errors.md).

## Pagination

One reply contains one page with at most 20 markets. The requested count is the total ranking size, not the page size: `divergence 100` makes one GET with `limit=100`, saves the full result locally, and returns page 1 (items 1–20) to the model. Do not issue five GETs with `limit=20`, fetch additional pages from the backend, read all 100 raw items into context, or output five tables in the first reply. This applies to free, prepaid and confirmed paid results alike.

Use `pagination.total_items` for the actual number of returned markets and `pagination.requested_limit` for the requested count. Do not mistake 20 visible rows for a short backend result when 100 were fetched. Preserve all returned ranks and their order; each page continues the same ranking without restarting ranks at 1.

Keep the current page and `pagination.snapshot_file` in this chat's context. On "next page"/"下一页", increment `pagination.page`; on "previous page"/"上一页", decrement it; resolve an explicit page number directly. Read only that page using the bundled local command, then compose and verify its reply with the same procedure as the first page:

```sh
node <skill-root>/scripts/cournot-client.mjs divergence-page --snapshot '<pagination.snapshot_file>' --page 2
```

This command is entirely local: it does not read credentials, contact the backend, use a wallet or consume another call. It returns only the selected page's rows, original metadata and updated pagination. Keep the snapshot path internal. Never substitute a different or globally latest snapshot from another chat. If no next/previous page exists, explain the available range without making a query. If the snapshot is missing or invalid, explain that the saved ranking is unavailable; a new paid query requires a new user request, not an automatic retry.

For a nonempty multipage result, add a short localized navigation line after the table, such as "第 1/5 页，本页显示第 1–20 条，共 100 条；可回复‘下一页’或‘第 N 页’。" Use actual pagination metadata. Do not append another page unprompted. On a cached page (`pagination.from_cache=true`), say that viewing this page used the saved result and incurred no additional query charge; the returned quota belongs to the original query and is not a fresh balance check. Keep the original snapshot times and localize all prose, direction labels and link text consistently.

## Successful output

You compose the presentation; JS generates only the Markdown data rows. Write the heading, table header and explanatory lines in the user's language, with natural wording that preserves the PRD meanings. Check that both direction labels and the visible link text use that same language before calling the client; a Chinese header above English direction/link labels is not a localized response. Do not rebuild data rows from JSON or translate them after rendering. API titles stay in their original language. There is no fixed English/Chinese header or footer template in the script.

Required notices have not been removed: for empty/short results, missing time, missing quota or unknown billing, apply the corresponding meanings in [errors.md](errors.md#divergence-notices-and-incomplete-metadata). Explain failures using that guide too; never output an empty answer just because no data rows were generated.

**Every final link destination must equal its original API `url` character for character.** Everything after `?` is part of the supplied link, including `op_market_ticker` even when its value repeats the path. Never treat a parameter as redundant, shorten to a market page, repair a ticker, change case or encoding, or use a remembered URL. Copy the entire target between `<` and `>`, through its last query value or fragment.

Compose the complete answer as follows:

- A short heading describing the markets with the largest divergence between Cournot and market prices.
- One Markdown table with exactly nine columns in this order: rank, market title, platform, direction, Cournot probability, market price, divergence, liquidity and link. You generate localized column labels and the Markdown separator. Insert this page's `rows_markdown` unchanged immediately below them, at most 20 rows per reply. Keep the nine columns together in each market row; never rewrite the table as repeated vertical field/value blocks or cards. All rows and ranks stay in the backend's order across pages; do not re-sort, filter, deduplicate, pad or substitute items.
- The generated rows already remove `at any time` and convert title timestamps `YYYY-MM-DD HH:MM UTC` to English `Month D, YYYY`, display Cournot probabilities as percentages rounded to exactly one decimal place (for example, `51.8932%` → `51.9%`), preserve market-price precision in cents, round unsigned divergence to integer pp, and display liquidity in USD. Do not infer missing outcome names from URLs.
- Leave a blank line after the last data row so the following text renders outside the table. Mention the actual count when fewer than requested were returned, followed by both batch timestamps on one line. Use `cournot_updated_time` and `market_updated_time`; the latter represents the earliest included market snapshot. Do not substitute current time. Convert explicit offsets to UTC; preserve a timestamp with no zone and state that its timezone was not provided. Report missing timestamps as unavailable.
- A separate paragraph states the returned billing route and actual remaining calls, followed by the meaning "This is an assessment of pricing, not investment advice." Use the user's language. `billing=api_key` means prepaid, `free_quota` means free allowance, and `x402` means on-chain payment. For x402 include returned network and transaction details. Use the quota belonging to the returned route; missing/null quota is unknown, not zero. `charged=false` does not make a nonempty prepaid query free. Never call balance just to fill this line.
- For zero items, `rows_markdown` is empty. State that no markets meet the criteria, no charge was made, and the actual remaining calls if returned. Do not add a heading, table, timestamp line or disclaimer. The client rejects contradictory or unconfirmed empty-result billing.
- No Buy YES/NO, profit/opportunity claims, investment recommendations, analysis or reasons outside the ranking. No code fence, file attachment replacing the inline table, process narration or follow-up question.

Save the final draft separately. Use JSON parsing to insert `rows_markdown` directly between your own header and footer; do not manually retype its rows or URLs. Read the saved draft in smaller chunks if a tool truncates it. Check the complete draft locally:

```sh
node <skill-root>/scripts/verify-output.mjs '<client-result.json>' '<final-draft.md>'
```

The verifier checks that every data row and link matches this page's generated rows, the table has nine columns, and the reply contains at most 20 markets. Use the current page's client-result file, not the full snapshot. It intentionally allows your own heading, column-label wording and footer; you must check their meanings and metadata against the requirements above. On failure, restore the data rows from the saved page JSON and check again without another HTTP request. On success, stdout is the complete draft and stderr is the verification receipt. Send the checked draft in chat, excluding the receipt. Verification covers the saved draft, not a later rewrite: preserve its data rows in the final reply too. The Markdown structure is controlled here; a host may choose its own visual layout, so do not claim that a prompt or pagination disables a CLI's automatic table reflow.

`invalid_response` preserves the sanitized response and its billing evidence. Do not improvise a table, omit malformed rows or retry. Explain that the ranking could not be displayed reliably and offer balance/support. A returned `billing=api_key` confirms prepaid consumption even when display fails; uncertainty applies only when billing evidence is missing or contradictory.

## Current wire mapping

Successful responses use `code=0`, `data.divergence.items[]` and these fields (not the PRD's illustrative camelCase schema):

| Field | Meaning |
|---|---|
| `rank`, `title`, `source`, `url` | Rank, market title, platform, platform market link |
| `cournot_price`, `market_price` | Probability and market price as fractions |
| `deviation` | Absolute difference as a fraction; display rounded ×100 pp |
| `direction` | `cournot_above` / `cournot_below` |
| `market_liquidity` | USD liquidity |
| `data.divergence.cournot_updated_time` | Batch probability calculation time |
| `data.divergence.market_updated_time` | Batch market-price time |
| `data.billing`, `data.charged`, `data.x402` | Shared billing route and settlement evidence |
| `data.free_quota`, `data.api_key_quota` | Actual remaining calls; IP is removed before display |

Backend responsibilities are eligibility (monitored, binary, overlapping across at least two platforms, unexpired, price 5¢–95¢, minimum deviation when defined) and sorting by rounded 1pp deviation, then liquidity descending. The skill displays the returned snapshot; it must not silently repair backend data or invent missing markets, IDs, outcomes or a minimum-deviation threshold.
