# Etix consumer endpoints for fpx

Ready-to-run request paths for
`fpx get|post-json 'https://www.etix.com<path>' -p etix`. All paths, field
names, and shapes are transcribed from `etix-mcp`'s `docs/ETIX-API.md` and
`src/parse.ts` — live-verified 2026-06-12 against venue `17987` (Middle C
Jazz Club) and performance `39004863` (NC Jazz Festival). Nothing here is
guessed.

Endpoint host: `https://www.etix.com`. Auth: none — every call still rides
the fetchproxy bridge because the whole zone sits behind DataDome, not
because these routes need an Etix account.

---

## 1. Search — `GET /ticket/api/online/search/suggest?keywords=<kw>` (do this first)

Clean JSON. Returns matching venues, events (performances), and performers.
Use this to resolve a name to an id before calling event/venue detail.

```sh
fpx get 'https://www.etix.com/ticket/api/online/search/suggest?keywords=jazz' -p etix > /tmp/suggest.json
jq '.' /tmp/suggest.json
```

Shape:

```jsonc
{
  "keywords": "jazz",
  "venues":     [ { "venueId": 17987, "venueName": "...", "organization": "...",
                    "address": "...", "city": "...", "state": "...", "country": "USA",
                    "venueSaleUrl": "/ticket/v/17987/middle-c-jazz-club" } ],
  "events":     [ { "eventId": 39004863, "eventName": "...", "categoryName": "Concerts",
                    "dateTime": "2027-02-05T00:30:00Z", "venueId": 4332, "venueName": "...",
                    "city": "...", "state": "...", "imageUrl": "https://cdn.etix.com/...",
                    "directSaleUrl": "/ticket/p/39004863/..." } ],
  "performers": [ { "id": 103251, "name": "Marion Meadows", "muzookaId": "mzoMB0Ym8l",
                    "imageUrl": "https://www.etix.com/ticket/api/online/search/muzooka/.../image" } ]
}
```

`performers` uses `id`/`name` — NOT `artistId`/`artistName` — and only
populates on a close artist match.

```sh
jq -r '.events[]     | "\(.eventId)\t\(.eventName)\t\(.dateTime)"' /tmp/suggest.json
jq -r '.venues[]     | "\(.venueId)\t\(.venueName)\t\(.city), \(.state)"' /tmp/suggest.json
jq -r '.performers[] | "\(.id)\t\(.name)"' /tmp/suggest.json
```

**Do NOT use** `POST /ticket/api/online/search` (the full-text search) — it
returns an encrypted/opaque payload, not JSON.

---

## 2. Event detail — `GET /ticket/p/<eventId>` → SSR HTML

The bare numeric id resolves without the URL slug. No clean JSON endpoint
exists; the page carries a schema.org **JSON-LD `Event`** block (sometimes
nested under `WebPage.mainEntity`) plus a single-quoted `dataLayer`
analytics object and an `og:image` meta tag.

```sh
fpx get 'https://www.etix.com/ticket/p/39004863' -p etix > /tmp/event.html
```

Extract the JSON-LD (it's real JSON once pulled out of the `<script>` tag —
pipe straight to `jq`):

```sh
node -e '
  const html = require("fs").readFileSync("/tmp/event.html", "utf8");
  const blocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
  for (const b of blocks) {
    const doc = JSON.parse(b[1]);
    const entity = doc["@graph"]?.find(e => e["@type"] === "Event")
      ?? (doc.mainEntity?.["@type"] === "Event" ? doc.mainEntity : undefined)
      ?? (doc["@type"] === "Event" ? doc : undefined);
    if (entity) { console.log(JSON.stringify(entity)); break; }
  }
' > /tmp/event.jsonld

jq '{name, url, start_date: .startDate, status: .eventStatus,
     venue: .location.name, city: .location.address.addressLocality,
     state: .location.address.addressRegion, lat: .location.geo.latitude,
     lng: .location.geo.longitude,
     offers: [.offers.offers[] | {name, price, currency: .priceCurrency, availability}]}' \
  /tmp/event.jsonld
```

Pull the numeric org id + cobrand out of the page's `dataLayer` (it's
single-quoted `'key' : 'value'` pairs spread across multiple lines, not
JSON, so `jq` can't touch it directly — and a single-line `grep -oE` can't
either: grep's `.` doesn't match newlines and grep has no lazy quantifier,
so a `dataLayer\s*=\s*\[.*?\]` pattern never matches the real multi-line
block and silently returns nothing):

```sh
node references/extract-datalayer.mjs /tmp/event.html | jq '.'
# {"org_id":"1744","org_name":"...","venue_id":"4332","venue_name":"...","cobrand":"ncjazz",...}
```

`references/extract-datalayer.mjs` is a small, dependency-free port of
`extractDataLayer` from `etix-mcp`'s own `src/parse.ts` — its regex spans
newlines lazily (`[\s\S]*?`), which grep's ERE dialect cannot express.

Price range is derived locally from `offers[].price` (min/max) — there's no
separate range field.

---

## 3. Venue detail — `GET /ticket/v/<venueId>` → SSR HTML

Carries a header `<div itemscope itemtype="http://schema.org/Place">` (the
venue's own address microdata) plus a list of
`<div class="row performance" itemscope itemtype="http://schema.org/MusicEvent">`
rows, one per upcoming event. Venue identity (id/name/org) also rides the
page's `dataLayer` (same format as §2).

```sh
fpx get 'https://www.etix.com/ticket/v/17987' -p etix > /tmp/venue.html
```

Microdata isn't JSON — `node-html-parser` (the same package `etix-mcp`
parses this with) is a one-time local install away, no repo checkout
needed:

```sh
mkdir -p /tmp/etix-parse && cd /tmp/etix-parse && npm install --no-save node-html-parser >/dev/null 2>&1

node -e '
  const { parse } = require("node-html-parser");
  const html = require("fs").readFileSync("/tmp/venue.html", "utf8");
  const root = parse(html);
  const places = root.querySelectorAll("[itemtype$=\"/Place\"]");
  const header = places.find(p => !p.closest(".row.performance"));
  const text = (el, prop) => {
    const n = el?.querySelector(`[itemprop="${prop}"]`);
    return (n?.getAttribute("content") ?? n?.text)?.trim();
  };
  console.log(JSON.stringify({
    name: text(header, "name"),
    street: text(header, "streetAddress"),
    city: text(header, "addressLocality"),
    state: text(header, "addressRegion"),
    postal_code: text(header, "postalCode"),
  }));
  const rows = root.querySelectorAll(".row.performance");
  for (const row of rows) {
    const link = row.querySelector(".performance-name a");
    console.log(JSON.stringify({
      href: link?.getAttribute("href"),
      name: link?.text?.trim(),
      start_date: row.querySelector("meta[itemprop=\"startDate\"]")?.getAttribute("content"),
      when: row.querySelector(".performance-datetime")?.text?.trim(),
    }));
  }
'
```

The header Place is identified the same way `etix-mcp` does it: the first
schema.org `Place` block that is NOT inside a `.row.performance` row.
Without any HTML parser on hand, a cruder `grep -oE` pass over the same
`itemprop="..."` attributes still gets the event ids + names — those
attribute names are the load-bearing part; reproduce them with whatever
HTML tool is available.

`dataLayer` (org id/name, venue id/name) extracts the same way as §2.

---

## 4. Geolocation — `POST /ticket/api/online/geolocation/search`

Body: `{ "cityOrPostalCode": "<city or zip>", "country": "<country, default USA>" }`.
`keywords` is NOT a valid field — the endpoint 400s naming the two known
properties.

```sh
printf '{"cityOrPostalCode":"Charlotte, NC","country":"USA"}' > /tmp/geo.json
fpx post-json 'https://www.etix.com/ticket/api/online/geolocation/search' @/tmp/geo.json -p etix \
  | jq '{latitude, longitude, city, state, postal_code: .postalCode}'
```

## 5. Healthcheck probe — `GET /robots.txt`

A small public path to isolate "bridge/extension down" from "DataDome
challenge on the tab":

```sh
fpx get 'https://www.etix.com/robots.txt' -p etix | head -3
```

A DataDome interstitial body contains `captcha-delivery` and "Please
enable JS and disable any ad blocker" — grep for that before trusting any
HTML response as real content:

```sh
grep -q 'captcha-delivery' /tmp/event.html && echo "BOT WALL — reopen etix.com and let it clear" || echo "ok"
```
