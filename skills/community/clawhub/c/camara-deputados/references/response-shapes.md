# Chamber response, pagination, and time rules

## Envelope

A collection normally returns:

```json
{
  "dados": [{"id": 1}],
  "links": [{"rel": "next", "href": "https://..."}]
}
```

A detail resource normally uses the same envelope with `dados` as an object. Preserve the complete envelope while paginating; extracting `dados` too early discards the navigation links.

## Pagination

1. Send the initial filters and page size.
2. Append `dados` to the result.
3. Follow the exact `href` whose `rel` is `next`.
4. Do not resend the original query parameters with a next-link URL.
5. Stop when `next` is absent or the caller's `max_pages` limit is reached.

This remains correct when the API returns a full last page or changes its default page size.

## Reference codes

Fetch the appropriate `/referencias/...` endpoint and match its returned code and description. Cache reference data for a bounded period if necessary, but retain the retrieval time. Never assume `codSituacao=903` means every proposition in progress.

## Dates and timezone

- API date filters use `YYYY-MM-DD`.
- Timestamps may include an offset; retain it when parsing.
- Interpret relative dates such as “today” in `America/Sao_Paulo`, not the host's timezone.
- If a result is used for monitoring, record the query interval and retrieval timestamp.

## Errors versus empty results

- HTTP 404: requested resource is absent.
- HTTP 400: parameters or route do not match the current contract.
- HTTP 429 and 5xx: retry with bounded exponential backoff.
- A valid `200` response with an empty `dados` list is a real empty result.
- Do not convert malformed JSON or a failed upstream request into an empty business result.
