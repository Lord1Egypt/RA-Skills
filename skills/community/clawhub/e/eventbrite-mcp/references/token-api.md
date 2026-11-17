# Eventbrite documented API (`eventbriteapi.com/v3`) — curl recipes

Auth on every call: `-H "Authorization: Bearer $EVENTBRITE_TOKEN"`.
Personal token: <https://www.eventbrite.com/platform/api-keys>.
All endpoints end with a trailing slash — omitting it 301s.

> Verification status (2026-07-30): `eventbriteapi.com` reachability and the
> 401 error envelope are live-verified. Endpoint shapes were live-verified
> through the session-authed www-host variant of the same v3 API
> (`www.eventbrite.com/api/v3/…`): `/users/me/`, `/users/me/orders/`
> envelope, `/users/me/organizations/` envelope, `/categories/`, and
> `/events/<id>/?expand=venue,ticket_availability` on a public event.
> `/ticket_classes/`, `/description/`, `/attendees/`, `/venues/`,
> `/subcategories/`, `/formats/` follow the official API reference but
> weren't exercised — eyeball the first response before building on a field.

Shorthand used below:

```sh
eb() { curl -sS "https://www.eventbriteapi.com/v3$1" -H "Authorization: Bearer $EVENTBRITE_TOKEN"; }
```

## Identity

```sh
eb /users/me/ | jq '{id, name, email: .emails[0].email}'
```

## Your tickets / orders (attendee side)

```sh
# upcoming orders with the event expanded
eb '/users/me/orders/?expand=event&time_filter=current_future' \
  | jq '.orders[] | {id, status, event: .event.name.text, start: .event.start.local}'

# one order with attendees (barcode-level detail)
eb '/orders/<order_id>/?expand=attendees' | jq
```

`time_filter`: `all` | `current_future` | `past`.

## Organizations you belong to (organizer side)

```sh
eb /users/me/organizations/ | jq '.organizations[] | {id, name}'

# events for an org: status live|draft|started|ended|completed|canceled|all
eb '/organizations/<org_id>/events/?status=live&order_by=start_asc' \
  | jq '.events[] | {id, name: .name.text, start: .start.local, url}'

# attendees / orders across the org
eb '/organizations/<org_id>/attendees/?status=attending' | jq '.attendees[] | {profile: .profile.name, email: .profile.email, event_id}'
eb '/organizations/<org_id>/orders/' | jq '.orders[] | {id, email, status}'
```

## Any event by id (works for public events, not just yours)

```sh
eb '/events/<event_id>/?expand=venue,organizer,ticket_availability' \
  | jq '{name: .name.text, start: .start.local, end: .end.local, venue: .venue.name, is_free, status, url}'

eb '/events/<event_id>/ticket_classes/' | jq '.ticket_classes[] | {name, free, cost: .cost.display, on_sale_status}'
eb '/events/<event_id>/description/' | jq -r .description   # full HTML description
eb '/events/<event_id>/attendees/' | jq                     # your own events only
```

Event ids are the long digits in any event URL (`…-tickets-<event_id>`).

## Reference data

```sh
eb /categories/ | jq '.categories[] | {id, name}'
eb /subcategories/ | jq '.subcategories[] | {id, name}'
eb /formats/ | jq '.formats[] | {id, name}'
eb '/venues/<venue_id>/' | jq '{name, address: .address.localized_address_display}'
```

## Pagination

Every list response carries:

```json
{"pagination": {"object_count": 123, "page_size": 50, "has_more_items": true, "continuation": "..."}}
```

Loop with `?continuation=<token>` (repeat the original params) while
`has_more_items` is true. `page_size` max is generally 100 for org-level
lists, 50 elsewhere.

## Errors

Non-2xx bodies are JSON: `{"status_code": N, "error": "CODE",
"error_description": "..."}`. Live-verified examples: bad token →
`401 INVALID_AUTH`; missing CSRF (www host only) → `401 ACCESS_DENIED`.
`404 NOT_FOUND` for unknown ids; `429` when rate-limited (token buckets:
2,000 calls/hour per token by default).

## No search here

`GET /events/search/` was removed from this API (Dec 2019) — it now 404s.
Public event discovery only exists on the WAF-walled consumer surface; see
`discovery-api.md` (fpx bridge).
