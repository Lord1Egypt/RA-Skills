# Error catalog and recovery

Every Fless agent surface returns the same error shape:

```json
{"error": {"code": "...", "message": "...", "hint": "...", "docs_url": "https://fless.io/hunt-how-to.md", "retryable": false}}
```

| Code | Meaning | Recovery |
|---|---|---|
| `CITY_NOT_FOUND` | Unknown city id/slug/name | List cities (`search_cities` / cities listing) and retry |
| `COMING_SOON_CITY` | City hasn't launched | Offer the waitlist page `https://fless.io/city/{slug}` instead of a hunt |
| `INVALID_MOVE_IN_DATE_PAST` | move_in_date not future | Ask for a later date |
| `PRICE_RANGE_INVALID` | min ≥ max | Ask for a corrected budget |
| `INVALID_REQUEST` | Bad enum/format/value | Read `message`, it names the field; fix and retry |
| `MISSING_FIELDS` | Tool argument absent | Supply the named field |
| `NOT_FOUND` / `CITY_NOT_FOUND` / `NEIGHBORHOOD_NOT_FOUND` / `POST_NOT_FOUND` / `ARTICLE_NOT_FOUND` (markdown) | No rendition at that URL | Use the listed alternates |
| `RATE_LIMITED` | Too many requests | Wait for `Retry-After` seconds, then retry |
| `LINK_EXPIRED` | Hunt link older than 7 days or unknown | Rebuild via `build_hunt_link` |
| `AUTHENTICATION_REQUIRED` | Anonymous access to a private endpoint | Only public endpoints are agent-accessible; no workaround. Review endpoints below need the hunt owner's signin session |
| `UNAUTHORIZED` | Missing/invalid/revoked realtor API key on a `realtor_*` MCP tool | Anonymous callers: use the public toolset; realtors: create a key at fless.io/realtor under API keys |
| `SUBSCRIPTION_REQUIRED` (402 class) | Realtor trial expired while advancing the funnel | Realtors subscribe under Billing at fless.io/realtor ($49.99/mo flat, 15-day free trial). Reads and curation edits stay ungated |
| `INVALID_STATE` (409 class) | Wrong approval-gate state: deciding a released hunt, deciding a legacy hunt, sending twice, no matched buildings yet, manual add outside a gate | Read `realtor_get_hunt_status` / the review status payload, then act on the actual state |

## Approval-gate 409 semantics (2.0.0)

- `GET /hunts/{id}/review` on a LEGACY hunt (created before the gate,
  `review_state` NULL) returns 409: those hunts were ungated and outreach was
  dispatched by the old workflow at creation time, so there is nothing to
  review. Only hunts created after the gate carry a `review_state`.
- `GET /hunts/{id}/review/status` on a legacy hunt is NOT an error: it reports
  `review_state: null` so polling after creation stays stable.
- `POST /hunts/{id}/review/decision` on anything other than
  `awaiting_user_approval` (or the client deciding a realtor hunt at
  `awaiting_client_approval`) returns 409 naming the current state.
- Outreach is gated by `OutreachGatedError` semantics: outreach emails may
  ONLY be sent for legacy hunts (review_state NULL) or hunts explicitly
  released via the decision endpoint. Every other gate value blocks outreach;
  fail-closed. Agents do not trigger this error directly, the backend enforces
  it in the workflow, all outreach tasks, and the send service.

Agent-driven error reporting: every failed validation is logged by Fless with
the field and code, so fixing your brief per the `hint` also improves the
published docs. When a fix contradicts this skill's reference files, trust the
live `hint` and re-read `https://fless.io/hunt-how-to.md` (it is regenerated
from the same source of truth).