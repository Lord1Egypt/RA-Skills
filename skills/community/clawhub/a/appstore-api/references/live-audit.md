# Live audit of the Apple App Store API (2026-09-12)

Every claim in this package was checked against the deployed service at `https://api.replynodes.com`
with a real workspace key. This file records what was observed so the skill never documents a
capability that does not work, and never labels a working capability unsupported.

## Deployment truth

| Check | Result |
| --- | --- |
| `GET /v1/capabilities` (public, no key) | `200`, document lists exactly 9 `/v1/appstore/*` routes |
| `GET /v1/appstore/capabilities` (key) | `200` `{"operations":["app","developer","list","privacy","ratings","reviews","search","similar","suggest"],"payment_mode":"prepaid_credit","read_only":true}` |
| No key on a data route | `401 {"error":{"code":"invalid_or_expired_token"}}` |
| Path-style route `/v1/appstore/apps/1232780281` | `404 not_found` — **not deployed**; all identity is query-parameter based |
| Unknown query parameter (`request_id=...`) | `400 invalid_request` — callers cannot set correlation IDs |

## Operation results

| Operation | Request used | Result |
| --- | --- | --- |
| `search` | `?term=Notion&num=3&country=us` | `200`, `data[]` with Notion (`ios:app:1232780281`, `notion.id`) |
| `search` paging | `?term=meditation&num=2&page=2` | `200`, next slice returned |
| `search` idsOnly | `?term=calm&num=2&idsOnly=true` | `200`, identifier-only records |
| `search` bounds | `?num=5` (no `term`) / `num=51` | `400 invalid_request` |
| `app` by ID | `?id=1232780281&country=us` | `200`, single full record (21 fields) |
| `app` by bundle ID | `?appId=notion.id&country=us` | `200`, same record |
| `app` storefront | `?id=571800810&country=gb` | `200` |
| `app` missing identity | no `id`/`appId` | `400 invalid_request` |
| `ratings` by ID | `?id=570060128&country=us` | `200`, `{"ratings":5,"histogram":{...5 buckets}}` |
| `ratings` by bundle ID | `?appId=notion.id&country=us` | `502 upstream_unavailable` (use the numeric ID) |
| `reviews` | `?id=570060128&country=us&page=1` | `200`, `data.reviews[]` with 50 records |
| `reviews` sort | `sort=mostRecent` / `sort=mostHelpful` | `200` both |
| `reviews` bad sort | `sort=recent` | `502 upstream_unavailable` |
| `reviews` page bound | `page=11` | `400 invalid_request` |
| `reviews` by bundle ID | `?appId=notion.id&country=us` | `200` |
| `developer` | `?devId=1232780280&country=us` | `200`, publisher catalog (5 apps) |
| `developer` URN form | `?devId=ios:developer:1232780280` | `502 upstream_unavailable` |
| `developer` wrong id | `?devId=1257896659` | `404 not_found` |
| `similar` | `?id=1232780281&country=us` | `200`, 15 related apps |
| `similar` by bundle ID | `?appId=notion.id&country=us` | `200`, 15 related apps |
| `similar` path style | `/v1/appstore/apps/1232780281/similar` | `404` |
| `suggest` | `?term=medi` | `200`, `data.suggestions[]` (10 terms) |
| `list` | `?collection=topfreeapplications&category=6017&country=us&num=5` and 4 other combinations | `200` with **`data: []`** — no rows returned |
| `privacy` | `?id=1232780281`, `?id=570060128`, `?id=426626861` | `502 upstream_unavailable` on every attempt |

## Response envelope facts

- Success: `data` + `meta` (`request_id`, `contract_version`, `generated_at`, `availability`) plus
  `credit_result` (`outcome`, `credits_consumed`, `settlement_status`).
- `meta.availability` can be `partial` with `detail` and `missing_fields` (observed:
  `["*.release_notes"]`).
- Failure: `error.code` + `message` + `request_id`; provider failures carry
  `credit_result.credits_consumed: 0` and `settlement_status: not_charged`.
- Unknown/missing counters stay `null`; zeros are never fabricated for absent data.

## Known defects / degradations found while auditing

1. **Replay envelope replaces the payload.** A repeated identical `GET` returns
   `{"data":{"settled":true,"replayed":true},"meta":{"price_micro":3000}}` instead of the app data.
   Verified by calling `app?id=1232780281&country=us` and `ratings?id=1232780281&country=us` several
   times in a row. Varying an optional parameter returns the full payload again — verified by
   re-reading with `country=gb` (`ratings`, `developer`, `similar`) and `lang=en` (`search`, `app`).
   Documented as a limitation rather than hidden.
2. **`privacy` is deployed but failing** for every app tried (`502 upstream_unavailable`).
3. **`list` returns empty collections** for the tested collection/category combinations.
4. **Metering:** every successful call consumed 3 credits, whether it returned 1 or 10 records;
   failed calls consumed 0.

## What this package deliberately does not claim

- No availability, uptime, latency or success-rate figures.
- No ranking share, download volume, search volume or market-share estimates.
- No write, account, login, purchase or App Store Connect capability.
- No Apple partnership, endorsement or data-sharing arrangement.
