# AllTrails endpoints for fpx

Every request needs the app-key headers captured in `SKILL.md`. All examples
below assume:

```sh
AT_KEY=$(fpx session -p alltrails | jq -r '.capturedHeaders["x-at-key"] // empty')
H=(-H "x-at-key: $AT_KEY" -H 'x-at-caller: Mugen' -H 'x-language-locale: en-US')
```

Base URL: `https://www.alltrails.com`. Paths below are all under
`/api/alltrails/...` unless noted. Endpoints and response shapes are
transcribed from `src/tools/*.ts` / `src/client.ts` / `CLAUDE.md` in
`alltrails-mcp` (live-verified there); no shape here was guessed.

---

## 1. Trail detail

`detail` is `basic` | `medium` (default) | `offline` (adds route geometry).

```sh
fpx get 'https://www.alltrails.com/api/alltrails/v3/trails/10236086?detail=medium' -p alltrails "${H[@]}" \
  | jq '.trails[0] | {id: .objectID, name, overview, length, elevation_gain, difficulty_rating, avg_rating, routeType: .routeType.name, location}'
```

The envelope is `{ "trails": [ {...} ] }` — a one-element array in practice.

## 2. Trail reviews

```sh
cat > /tmp/at_reviews.json <<'JSON'
{"limit": 20}
JSON
fpx post-json 'https://www.alltrails.com/api/alltrails/v2/trails/10236086/reviews/search' @/tmp/at_reviews.json -p alltrails "${H[@]}" \
  | jq '.trail_reviews[] | {user: .user.name, rating, comment}'
```

Envelope: `{ "trail_reviews": [...] }`.

## 3. Trail photos

```sh
fpx get 'https://www.alltrails.com/api/alltrails/v2/trails/10236086/photos' -p alltrails "${H[@]}" \
  | jq --arg key "$AT_KEY" '.photos[] | {
      id, title, likeCount,
      user: ((.user.firstName // "") + " " + (.user.lastName // "")),
      uploadedAt: .metadata.created,
      url: ("https://www.alltrails.com/api/alltrails/photos/" + (.id|tostring) + "/image?size=large&key=" + $key)
    }'
```

Envelope: `{ "photos": [...] }`. The record carries **no direct image URL** —
`GET /api/alltrails/photos/{id}/image?size=large&key=<x-at-key>` 302s to the
CDN original and is **not** DataDome-walled (fetchable directly, no bridge
needed, if you just want the bytes).

## 4. Trail weather

```sh
fpx get 'https://www.alltrails.com/api/alltrails/weather-service/v2/trails/10236086/overview' -p alltrails "${H[@]}" | jq .
```

## 5. Trail route geometry (for GPX / mapping)

```sh
fpx get 'https://www.alltrails.com/api/alltrails/v3/trails/10236086?detail=offline' -p alltrails "${H[@]}" \
  | jq '.trails[0].defaultMap.routes[0].lineSegments[0]'
```

`pointsData` is 2-dim `(lat, lng) × 1e5`; `indexedElevationData` is 2-dim
`(pointIndex × 100, elevationMeters × 1e5)`, one pair per point — decode both
by dividing by `1e5` (elevation index by `100`). alltrails-mcp's
`alltrails_get_trail_gpx` does this decode + emits GPX 1.1 in
`src/gpx.ts`/`decodePolyline` — reproducing that Google-polyline-variant
decoder in shell is impractical, so this skill stops at the raw geometry;
reach for the MCP tool (or port `decodePolyline`) if you need actual GPX XML.

## 6. Your profile / user id

```sh
fpx get 'https://www.alltrails.com/api/alltrails/me' -p alltrails "${H[@]}" | jq -r '.users[0].id'
```

**`{"users":[{"id":...}]}`, not `{"user":{...}}`.** Requires a signed-in tab.

## 7. A user's saved lists

```sh
UID=... # from step 6, or another public profile's numeric id
fpx get "https://www.alltrails.com/api/alltrails/users/$UID/lists" -p alltrails "${H[@]}" | jq .
```

## 8. Items in a saved list

```sh
LISTID=... # from step 7
fpx get "https://www.alltrails.com/api/alltrails/lists/$LISTID/items" -p alltrails "${H[@]}" \
  | jq '.listItems | sort_by(.order) | .[] | {trailId, order, notes, addedAt: .metadata.created}'
```

Envelope: `{ "listItems": [...], "meta": { "items": N } }`. Items are
**sparse references** — only `trailId` (hydrate with endpoint 1) plus the
curator's `order`/`notes`, no trail details inlined.

## 9. A user's completed trails

```sh
fpx get "https://www.alltrails.com/api/alltrails/users/$UID/trails/completed" -p alltrails "${H[@]}" | jq .
```

## 10. Activity feed — directory, then items

```sh
# Directory (available feed names):
fpx get "https://www.alltrails.com/api/alltrails/community/blazes/v0/users/$UID/feeds" -p alltrails "${H[@]}" \
  | jq '.feeds[] | {name, displayName}'

# Items — feed is local | timeline | personal:
fpx get "https://www.alltrails.com/api/alltrails/community/blazes/v0/users/$UID/feeds/personal?maxItems=20" -p alltrails "${H[@]}" \
  | jq '.sections[].itemData | {itemType, timestamp, description, user: ((.user.firstName//"")+" "+(.user.lastName//"")), trail: .trail.name, stats: .activity.summaryStats}'
```

Paginate with `?maxItems=N&cursor=<pageInfo.nextCursor>`. Units:
`summaryStats.distanceTotal`/`elevationGain` are **meters**, `duration` is
**minutes** (`timeTotal`/`timeMoving`, if present, are seconds — don't
confuse the two).

## 11. Search by name (the real search — honors query + limit)

This is the same endpoint the alltrails.com search box uses; body shape
captured verbatim from the live client.

```sh
cat > /tmp/at_search.json <<'JSON'
{
  "query": "angels landing",
  "limit": 20,
  "recordTypesToReturn": ["trail"]
}
JSON
fpx post-json 'https://www.alltrails.com/api/alltrails/explore/v1/suggestions' @/tmp/at_search.json -p alltrails "${H[@]}" \
  | jq '.searchResults[] | {id: .ID, name, length, elevation_gain, difficulty_rating, avg_rating, area: .area_name, region: .state_name}'
```

`recordTypesToReturn` accepts any of `country`, `state`, `city`, `area`,
`poi`, `trail`, `guide`, `filter`, `list`, `sponsored_list`. Pass the place
kinds (`country`/`state`/`city`/`area`/`poi`) instead of `trail` to resolve a
**location** rather than a trail:

```sh
cat > /tmp/at_location.json <<'JSON'
{
  "query": "portland oregon",
  "limit": 10,
  "recordTypesToReturn": ["country", "state", "city", "area", "poi"]
}
JSON
fpx post-json 'https://www.alltrails.com/api/alltrails/explore/v1/suggestions' @/tmp/at_location.json -p alltrails "${H[@]}" \
  | jq '.searchResults[] | {name, kind: (.location_type // .type), id: .ID, objectID, slug, lat: ._geoloc.lat, lng: ._geoloc.lng, label: .location_label}'
```

Note: the resolved location `id`/`objectID` is an **Algolia search id** — it
does **not** feed a `/locations/{id}/trails` listing endpoint (that endpoint
was retired server-side, confirmed 2026-07-08, and now 400s on every
variant). To find trails in/near a resolved place, feed the place **name**
back into the trail search (endpoint above), not its id.

`lat`/`lng` body params are silently **ignored** by this endpoint (verified
2026-07-02/07-08) — results carry an implicit account/IP geo bias instead.

## 12. Search — legacy no-query fallback

Only useful without a text query; every param except `limit` is ignored
(anchored to the signed-in account's location), so this is a weak fallback —
prefer endpoint 11 with a query.

```sh
cat > /tmp/at_search_legacy.json <<'JSON'
{"limit": 20}
JSON
fpx post-json 'https://www.alltrails.com/api/alltrails/explore/v1/search' @/tmp/at_search_legacy.json -p alltrails "${H[@]}" \
  | jq '.searchResults[] | {id: .ID, name}'
```

---

## Response-shape reminders

- Card/listing money-ish numeric fields (`length`, `elevation_gain`) are
  **meters** everywhere — no imperial conversion server-side.
- `objectID` is namespace-prefixed on location records (`state-38`,
  `cityo-6641`, `area-N`) and `"trail-{id}"`-prefixed on trail search results
  — prefer the numeric `ID`/`id` field when one exists.
- A `200` response that isn't valid JSON (`jq` errors on parse) is almost
  always a DataDome interstitial page, not real data — refresh the signed-in
  tab and retry rather than treating the body as an error payload.
