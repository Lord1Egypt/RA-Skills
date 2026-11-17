# Eventbrite discovery API (`www.eventbrite.com/api/v3/destination/…`) — fpx recipes

Public event search/discovery. WAF-blocked server-side; every call here goes
through the fpx bridge (`-p eventbrite`). Request shapes below were captured
live from the site's own network traffic (2026-07-30, web_app discover
v10.14.65).

## CSRF (search POST only)

GETs need nothing extra. The search POST requires the Django CSRF header,
whose value is the `csrftoken` cookie (32 chars, JS-readable). Read it
through the bridge — the profile must declare the cookie scope (see SKILL.md
setup):

```sh
CSRF=$(fpx cookies csrftoken -p eventbrite | jq -r '.csrftoken')
```

If the cookie is absent, load any eventbrite.com page in the browser first.

## Resolve a place id first

Searches take internal place ids (e.g. Charlotte NC = `85981333`), never
place names. The site itself resolves locations via Google Places, but the
scriptable route is the SSR page store: fetch the browse page for the
location slug and pull `placeId` out of the embedded `__SERVER_DATA__`:

```sh
# slug format: <state>--<city> (US) or <country>--<city>
fpx get 'https://www.eventbrite.com/d/co--denver/events/' -p eventbrite \
  | grep -oE '"placeId":"[0-9]+"' | head -1
```

The same SSR page embeds the full first page of results in
`search_data.events` — for a quick "what's on in <city>" that GET alone may
be all you need.

## Event search

```sh
CSRF=$(fpx cookies csrftoken -p eventbrite | jq -r '.csrftoken')
cat > /tmp/eb-search.json <<'EOF'
{
  "browse_surface": "search",
  "event_search": {
    "q": "blues",
    "places": ["85981333"],
    "dates": ["current_future"],
    "dedup": true,
    "page": 1,
    "page_size": 20
  },
  "expand.destination_event": [
    "primary_venue", "image", "ticket_availability",
    "event_sales_status", "primary_organizer"
  ]
}
EOF
fpx post-json 'https://www.eventbrite.com/api/v3/destination/search/' @/tmp/eb-search.json \
  -p eventbrite -H "X-CSRFToken: $CSRF" -H "X-Requested-With: XMLHttpRequest" \
  | jq '.events.results[] | {id, name, start: .start_date, venue: .primary_venue.name, url}'
```

Body knobs (all inside `event_search`, all optional except you want at least
`q` or `places`):

- `q` — keyword text.
- `places` — array of place-id strings (resolve first, above).
- `dates` — array; `"current_future"` plus optionally one of `"today"`,
  `"tomorrow"`, `"this_weekend"`; or `date_range: {from, to}` (ISO dates).
- `tags` — category/format filters: `"EventbriteCategory/<id>"` (103 =
  Music …), `"EventbriteSubCategory/<id>"`, `"EventbriteFormat/<id>"`. Ids
  match the documented API's `/categories/` etc. (see token-api.md).
- `online_events_only` — bool.
- `price` — `"free"` or `"paid"`.
- `page`, `page_size` (site uses 20), `dedup: true`.

Response: `{events: {pagination: {object_count, page_count, continuation},
results: [...]}, ...}` — paginate by incrementing `page`.

## Event detail by id (GET, no CSRF)

```sh
fpx get 'https://www.eventbrite.com/api/v3/destination/events/?event_ids=<id>,<id>&expand=primary_venue,image,ticket_availability,event_sales_status,primary_organizer' \
  -p eventbrite | jq '.events[]'
```

Event ids are the trailing digits in event URLs (`…-tickets-<id>`). For
full ticket-class detail prefer the documented API (`token-api.md`) —
`/events/<id>/` works for any public event with just a token.

## Your account data through the bridge (no token needed)

The www host proxies the documented v3 API with the browser session's auth,
so the whole `token-api.md` surface also works session-authed via fpx —
same paths, `www.eventbrite.com` host (live-verified: `/api/v3/users/me/`):

```sh
fpx get 'https://www.eventbrite.com/api/v3/users/me/orders/?expand=event&time_filter=current_future' \
  -p eventbrite | jq '.orders[] | {id, event: .event.name.text}'
```

Prefer the token + curl for scripts (no browser dependency); use this when
no token is configured.

## Gotchas

- A non-JSON 2xx body from any of these = the WAF interstitial leaked
  through — refresh a signed-in eventbrite.com tab and retry.
- `log_requests` / `log_engagement` endpoints seen in captures are
  analytics — don't call them.
- The `?stable_id=` query param on the site's own search calls is a client
  analytics uuid — omit it.
