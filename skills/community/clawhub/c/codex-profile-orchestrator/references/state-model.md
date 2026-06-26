# State Model

## Identity key

Each discovered profile is normalized to:
- email
- user id
- account id

The tuple `email|user_id|account_id` is the exact identity key.

## Canonical ids

- primary identity: `openai-codex:<email-slug>`
- workspace variants: `openai-codex:<email-slug>-ws2`, `-ws3`, and so on

## Health rules

- network outage: do not quarantine, do not delete, prefer staying on the current profile
- invalid profile: 400, 401, 403, missing token, token expired
- usable profile: weekly remaining above zero and five-hour remaining above zero

## Selection rules

1. keep the current profile if it is still healthy and its five-hour remaining stays above threshold
2. otherwise switch to the healthy profile with the best five-hour remaining
3. use weekly remaining as a second tie-breaker
4. prefer primary over workspace variant when the score is tied
