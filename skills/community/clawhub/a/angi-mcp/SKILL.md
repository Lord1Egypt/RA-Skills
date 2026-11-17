---
name: angi-fpx
description: >-
  Read angi.com (US home-services directory) from a shell with the fpx CLI
  (@fetchproxy/cli) instead of running the angi-mcp server — find pros by trade
  and city, read a pro's profile, ratings breakdown and reviews, and list the
  trade/city taxonomy. Use when you want Angi data without the MCP, in a
  script, or on a machine where the MCP isn't installed.
---

# Angi via fpx (no MCP)

Angi fronts `www.angi.com` with Cloudflare. Every content page returns **403**
to plain `curl`/Node — only `robots.txt`, the sitemaps and `/auth/login` get
through. `fpx` runs the fetch inside the user's own browser tab (the
ContextMint Bridge extension), which has already cleared the challenge, so the same
URL succeeds. No Angi login is needed for the public data below — a normal open
tab is enough; only the optional *Signed-in account data* section needs a
signed-in tab.

Two surfaces, two tools — don't route everything through the bridge:

- **Taxonomy** (which trades and cities exist) → the XML sitemaps, reachable by
  **plain `curl`**. No bridge, no extension.
- **Data** (pros, ratings, reviews) → `fpx get` through the tab.

## One-time setup

```sh
npm install -g @fetchproxy/cli              # provides `fpx`
fpx profile add angi --domain angi.com      # fetch capability only
fpx pair -p angi --subdomain www            # approve the 6-digit code in ContextMint Bridge
```

Requires the **ContextMint Bridge** extension (install from
https://github.com/nullnet-app/contextmint-bridge/releases — load the Chrome zip
unpacked; Safari isn't available yet, so use Chrome for now) with an open
`www.angi.com` tab and its *Site access* allowing `angi.com`. Pairing persists
across invocations.

ContextMint Bridge is the renamed fetchproxy extension (same maintainer; source at
https://github.com/nullnet-app/contextmint-bridge — build it or verify a release
zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`).

**Pair per host you intend to fetch, and keep a tab open on it.** The bridge
relays through a tab on the request's own host, so a bare `fpx pair -p angi`
fails with `no tab matching https://angi.com/` — the apex serves no page. Pass
`--subdomain www`, and if you also want the signed-in account data below, open
a `my.angi.com` tab and run `fpx pair -p angi --subdomain my` as well.
(Alternatively `--via-tab <url>` names the relaying tab explicitly.)

No cookie, storage or header scope is declared — Angi's data is server-rendered
and rides the tab's own session, so nothing needs to be read out of the
browser. Keep it that way: widening scope later forces a fresh pairing.

## The one rule: resolve the trade slug first

Angi URLs are `/companylist/us/<state>/<city>/<trade>.htm`. The trade is a
fixed slug (`plumbing`, `roofing`, `air-duct-cleaning`, …), not free text, and
a wrong slug 404s. Resolve from the sitemaps before fetching — plain `curl`:

```sh
# All ~312 trade slugs
curl -s https://www.angi.com/sitemap/statecat-sitemap.xml \
  | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' \
  | sed -n 's#.*/companylist/us/[a-z][a-z]/\([^/]*\)\.htm#\1#p' | sort -u

# Every city that has pages for one trade (confirms a city/trade combo exists)
curl -s https://www.angi.com/sitemap/angi-geocat-plumbing.xml \
  | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' | grep '/us/nc/'
```

## Core call

Fetch the page through the tab, pipe the HTML into the extractor:

```sh
fpx get 'https://www.angi.com/companylist/us/nc/charlotte/plumbing.htm' -p angi \
  | node references/rsc.mjs legacyId --dedupe id \
  | jq -r '.[] | "\(.businessInfo.businessName)\t\(.rating.averageOverallRating)★ (\(.rating.reviewCount))\t\(.profileUrl)"'
```

`rsc.mjs` exists because the data is **not** in the HTML and **not** `jq`-able.
Angi is Next.js App Router: records arrive as React Server Component flight
rows inside `self.__next_f.push([1,"…"])` string literals, and nested values are
deduplicated behind `"$<rowid>"` references. The extractor concatenates the
chunks, unescapes them, brace-matches the objects owning a key, and resolves
the references. See `references/angi-pages.md` for record shapes and recipes.

**Always pass `--dedupe id` on search pages.** Each provider is emitted twice
(sponsored slot + list row); raw counts are exactly double.

## Signed-in account data (optional)

If the tab is signed in to Angi, the account app on `my.angi.com` is readable
through the same profile (`angi.com` covers the subdomain). It is a **different
Next.js app** — Pages Router, so its data is a plain `__NEXT_DATA__` blob, and
`rsc.mjs` does *not* apply. Use `jq` directly:

```sh
# Identity + project counts
fpx get 'https://my.angi.com/myprojects' -p angi \
  | sed -n 's/.*<script id="__NEXT_DATA__"[^>]*>\(.*\)<\/script.*/\1/p' \
  | jq '.props.pageProps.initialState
        | {user: .projectHomeUser.firstName,
           open: (.openProjectList.projects | length),
           closed: (.closedProjectList.projects | length)}'

# Reviews you've written (plain JSON, session-cookie auth)
fpx get 'https://my.angi.com/account/rating-review/reviews' -p angi | jq
```

Two limits, both verified:

- **Record fields are unknown.** The account these were captured from held zero
  projects and zero reviews, so only the empty envelopes were observed. Read
  field names off the data; don't assume them.
- **The inbox is not readable.** `my.angi.com/inbox` runs on the Twilio
  Conversations SDK; its proxy endpoints reject the session cookie alone
  (`401`, XML body `username or accesskey could not be verified`). `fpx` cannot
  speak that protocol — messages need the Twilio client, not a GET.

Signed-out requests are **redirected to `/auth/login`** rather than 401'd, so a
200 that contains a login page means the tab is signed out.

## In context groups

When angi-mcp runs on a host that groups tools by context (mcp-host), its
tools sit in the **home** group, beside the other home-services, real-estate
and smart-home servers. Every Angi tool is a **lookup** — finding a pro,
reading a profile or its reviews, the trade/city lists, and the signed-in
account, projects and reviews. Angi answers no "what's new", "what's due" or
"what's on" question, so it has **no canonical read and no subject**: a
compound ask such as "anything new at home, and find me a plumber in
Charlotte?" is answered by the group's other members for the first half and
by `angi_search_pros` for the second. Angi is browser-bridged, so when the
ContextMint Bridge is not connected (or no `www.angi.com` tab is open) the
group answers that Angi **needs your browser open** rather than failing the
whole ask.

## Gotchas

- `?page=N` paginates (10 unique pros per page, no overlap between pages).
- **`?zip=` is inert** — verified: `?zip=90210` on a Charlotte page returns the
  identical Charlotte pros. Location comes from the URL path only. Don't offer
  it as a filter.
- JSON-LD (`SearchResultsPage`, `LocalBusiness`) is present and is real JSON,
  but carries only names/addresses/one sample review — no ratings, no ids. Use
  it as a cross-check, not the source.
- A non-HTML or challenge-page 2xx means the tab lost its Cloudflare clearance;
  refresh a `www.angi.com` tab rather than parsing the interstitial.

## Exit codes (fetch verbs)

- `0` success · `2` bridge unavailable (extension disconnected, or pairing
  pending → re-run `fpx pair -p angi --subdomain www`, and confirm a tab is
  open **on the host you are fetching**) ·
  `3` bot wall (tab hasn't cleared Cloudflare → refresh it) · `4` upstream
  non-2xx (usually a bad trade/city slug — re-resolve from the sitemap).

## Notes

- Reads only — nothing here writes to Angi. Everything is public except the
  optional account section, which reads only the signed-in user's own data.
  Stay within angi.com's terms.
- `fpx health -p angi` shows bridge state when a call fails.
- This project is developed and maintained by AI (Claude).
