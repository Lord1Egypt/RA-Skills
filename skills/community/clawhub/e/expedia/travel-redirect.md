# Travel Redirect Workflows

Use this file for Expedia partner flows that search inventory on your surface and then deeplink travelers to Expedia to complete booking.

## What Redirect mode is for

Redirect mode is search and discovery, not full in-flow booking.

Use it when the task needs:
- lodging search with deeplinks
- flight discovery with Expedia redirect
- partner-side search pages that send the traveler to Expedia to book

## Authentication reality

- Travel Redirect requires Expedia-issued partner credentials.
- Requests identify the API user with a partner key plus authorization credentials.
- Keep credentials out of markdown files and logs.

## Known official pattern

The lodging listings API uses:

```bash
curl https://apim.expedia.com/hotels/listings \
  -H "Accept: application/vnd.exp-hotel.v3+json" \
  -H "Key: <redirect-api-key>" \
  -H "Authorization: <redirect-authorization-value>" \
  -H "Partner-Transaction-Id: <unique-transaction-id>"
```

Only run this when the workspace is an authorized Expedia Travel Redirect integration.

## Redirect-specific rules

- Deeplinks are discovery outputs, not permanent identifiers.
- If the returned link is time-sensitive or session-bound, say so clearly.
- Do not present redirect mode as equivalent to a native booking flow.

## Output contract

Always return:
- what inventory type was searched
- what filters were applied
- whether the result is a redirect candidate or a completed booking path
- what the traveler still needs to verify on Expedia before purchase

## Common failure modes

- Treating redirect listings as price-final -> the traveler still has to validate on Expedia.
- Reusing old deeplinks -> session or token expiry breaks trust.
- Forgetting partner transaction IDs -> debugging and reconciliation become harder.
- Mixing redirect and Rapid outputs -> the user no longer knows which step is authoritative.
