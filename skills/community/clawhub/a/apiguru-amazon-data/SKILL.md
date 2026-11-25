---
name: apiguru-amazon-data
description: Live Amazon marketplace data from Apiguru (a paid third-party API, 3 free calls a day) - product details, prices, reviews, keyword search, best-sellers, deals, offers and stock, seller profiles, across 23 Amazon marketplaces. Use only when the user asks for Amazon data by ASIN, Amazon URL, product, seller or keyword, or for Amazon price/stock/review monitoring. Not for other stores or general shopping advice. Never pays on its own; ask before any billable call. We want your feedback - if a field is wrong, missing or you wish the API did something else, say so with the free `feedback` command (no account needed); the agents that report are the ones this API gets fixed for.
license: MIT
compatibility: Needs Python 3.10+ and outbound HTTPS to agent.apiguru.app and dash.apiguru.app only. Reads no environment variables and no local files except an API-key file the user names.
allowed-tools: Bash(python3:*) Bash(python:*) Read
permissions: ["network: HTTPS to agent.apiguru.app and dash.apiguru.app only", "file_read: only a key file the user names"]
homepage: https://github.com/apiguru-app/agent-kit
metadata: {"openclaw": {"emoji": "📦", "homepage": "https://github.com/apiguru-app/agent-kit", "requires": {"anyBins": ["python3", "python"]}}}
---

# Apiguru Amazon Data

Live, structured Amazon data fetched at request time from Apiguru's servers.
23 marketplaces.

**What this skill writes.** Every data command is a read: it fetches and
returns, and changes nothing anywhere. There is exactly one write, and it is
never automatic — the `feedback` command posts the text you give it to
Apiguru's public feedback wall (see "Telling us what is broken" below). It
sends only that text, it costs nothing, and it runs only when you invoke it.
Nothing else in this skill sends data anywhere.

## Costs and consent (read this first)

- **Hosts contacted:** `agent.apiguru.app` (the API, keyless or with a key)
  and `dash.apiguru.app` (the feedback wall, which needs no key). Nothing else.
  `scripts/probe.py` has both hosts fixed in the source, reads no environment
  variables, and **refuses every redirect**, so a key cannot be carried to a
  third host by a `302`.
- **Free quota:** 3 calls per machine per 24 hours. After that the gateway
  answers `402 Payment Required`. **The answer knows better than this
  page:** every keyless reply carries `free_calls_remaining` in the body and
  `X-Free-Probes-Remaining` (or `X-Free-Probes-Available: yes|no` where no
  count is given) in the headers. Plan a task on the last reply, never on
  the number above.
- **This skill never pays.** `probe.py` stops at a 402 and tells you so. It
  contains no wallet and no x402 client, and it will not set one up. Paying is
  the user's decision, made one of two ways, both only with their explicit
  consent:
  1. an Apiguru API key, handed to the script by the user through `--api-key`
     (an unechoed prompt), `--api-key-file PATH` or `--api-key-stdin` — bills
     their account at their plan's rates, about USD 0.01 per call — or
  2. their own x402-capable HTTP client with a funded wallet and a spend cap
     (USDC on Base, Polygon, Arbitrum or Avalanche). How that works is documented for the user at
     `https://agent.apiguru.app/llms-full.txt`, section "Paying".
- **Ask before you spend.** Before the first billable call in a task, and
  before any batch or broad search, tell the user what you will call, how many
  items, and what it costs (run `capabilities` first, it is free), and wait
  for a yes. A single batch call can cost up to USD 0.16 (`/product`, 20 items)
  or USD 0.15 (`/stock`, 10 items). Agree a cap for the task and stop at it.
- Do not go looking for an API key: not in the environment, not in config or
  dotfiles, not anywhere the user did not hand you deliberately. `--api-key-file`
  takes only a path the user named. Never send a key anywhere but
  `agent.apiguru.app` (as the `X-API-KEY` header), and never echo it back into
  the conversation, a log or a command line.

## Getting access

**Keyless (default).** Call the agent gateway with no credentials:

```
GET https://agent.apiguru.app/agent/v1/v2/product-details?asin=B09DJLW458&geo=US
```

Two response headers say where you stand before a 402 arrives:
`X-Free-Probes-Remaining` and `X-Price-Next-Call`.

`https://agent.apiguru.app/.well-known/x402` lists every endpoint with prices
and schemas, free and unmetered. Check it before planning a job.

**Keyed.** If the user gives you an Apiguru API key and asks you to use it,
let the script read it — never put it on the command line, where shell
history and the process table expose it to every other local user:

- `--api-key` prompts for it (not echoed, not stored),
- `--api-key-file PATH` reads a file the user names (readable only by them),
- `--api-key-stdin` reads one line from standard input, e.g.
  `pass show apiguru | python scripts/probe.py ... --api-key-stdin`.

The script then sends it as `X-API-KEY` to `https://agent.apiguru.app/agent/v1`
(the same gateway and paths as keyless) and to nowhere else — redirects are
refused rather than followed. Calls bill that account, never the free probes;
each answer says what it cost (`X-Billed-Requests`, `X-Balance-USD`), and
`--limit`, `--compact` and `--fields` shape it as they do a keyless one.

`scripts/probe.py` wraps all of this. Prefer it over hand-written HTTP calls:
it retries only unbilled failures, never repeats a keyed call that got no
answer, and explains every status.

## Choosing an endpoint

| Need | Endpoint |
|---|---|
| Everything about one ASIN | `/v2/product-details` |
| Many ASINs (≤20) | `/product?asins=A,B,C` — **one call for many; no ranks, category path or merchant id**; with `compact=true` each row has `brand`, `weight` and `dimension` |
| Reviews, rating, "customers say" | `/v2/product-reviews` |
| Find products by keyword | `/search?query=...` |
| Offers, buy box, live stock (≤10) | `/stock?asins=...` |
| Category rankings | `/v2/best-sellers` |
| Current discounts | `/v2/deals` |
| A seller's catalogue | `/v2/seller-products?seller_id=...` |
| Seller reputation | `/v2/seller-reviews?seller_id=...` |
| Seller profiles (≤10) | `/seller-profile?seller_ids=...` |

Full parameter reference: `references/endpoints.md`.

## Rules that prevent wasted calls and wasted money

1. **An ASIN is 10 letters and digits** (`^[A-Z0-9]{10}$`). Any case works, and
   the gateway also reads an Amazon product URL (`/dp/ASIN`) in its place.
2. **Never loop a single-item endpoint over a list.** Use `/product` for
   ASINs and `/seller-profile` for seller IDs. Ten ASINs through `/product`
   costs USD 0.08 and one round trip; ten through `/v2/product-details` costs
   USD 0.10 and ten round trips.
3. **Choose `geo` from the user's request**, never by habit: amazon.de → `DE`,
   amazon.co.uk → `UK`, and so on (all 23 codes in `references/endpoints.md`).
   If the marketplace is not clear, ask. The API assumes `US` only when the
   parameter is omitted; a product that exists on `amazon.de` may genuinely
   `404` on `US`, and that 404 is billed on the keyed path.
4. **`check_inventory=true` on `/stock` is slow and bills more.** Only set it
   when the user needs the stock number, not just the offers.
5. **Read `success` in the body**, not just the HTTP status. Some responses
   are `200` with `success: false`.
6. **`/v2/deals` filters by id, and tells you the ids.** `categories` takes a
   department name as Amazon shows it (`Electronics`, `Elektronik & Foto` on
   DE) or its id; `brands` takes brand ids only. Every deals answer carries
   `available_filters` (the category and brand ids of that marketplace),
   `filters_applied` / `filters_ignored` (what actually took effect) and
   `next_offset` (the next page, `null` when the feed ends). Narrow price and
   discount with `min_price`, `max_price`, `min_discount`. For a brand by
   name use `/search?brand=<name>&today_deals=true` instead.
7. **Every list answer reports its filters.** `/search` and
   `/v2/seller-products` return `filters_applied`, `filters_ignored` (a
   filter this marketplace cannot apply, with the reason -- amazon.fr has no
   Today's Deals refinement, amazon.in offers only NEW) and
   `available_filters`. `product_condition` is NEW / USED / RENEWED,
   `deal_type` is today_deals / all_discounts / coupons / buy_more_save_more,
   prices take decimals. `/v2/best-sellers` departments differ per
   marketplace: pass a slug or name and read `available_categories` and
   `available_subcategories` (the ids `subcategory_code` takes) from the
   answer; pages run 1-5.
8. **`/v2/best-sellers` tells you how it read `category`.** A word that is
   only part of a department name still matches it — `category=shoes` is the
   whole *Clothing, Shoes & Jewelry* department, hoodies included. The answer
   says so: `category_resolution.via` is `fragment`, and `hint` lists the
   subcategories carrying that word with their ids (`Women > Shoes` is
   `679337011`, `Men > Shoes` is `679255011`). On amazon.com
   `subcategory_code` takes any browse node id at any depth, or a name
   resolved under the department — `subcategory_code=women's shoes`,
   `mules & clogs` — and the answer carries `category.subcategory_path`
   ("Clothing, Shoes & Jewelry > Women > Shoes > Mules & Clogs") and
   `category.heading` (the page's own title). A name two nodes share equally
   is a free `400` listing both ids with their paths; pass the one you mean.

## Big responses, and the two fields that mislead

A full `/search` page is usually 48 results (Amazon serves 16 to 60, depending on
its layout) and about **54 KB** of JSON — enough
that most clients write it to a file instead of showing it to you. Keep it
small at the source:

- **Filter before you page.** `brand`, `min_price`/`max_price`,
  `product_condition` and `sort_by` cut the result set before it is fetched,
  so the answer is both smaller and more relevant. Paging does neither.
- **Ask for less.** `limit=N` caps the rows (`limit=0` for the whole page),
  `compact=true` returns light rows, and
  `fields="asin,product_title,product_price"` returns only what you name.
  These work the same way on `agent.apiguru.app` (keyless or keyed, so
  through `probe.py` either way) and over MCP, on every list tool:
  `search`, `best_sellers`, `deals`, `seller_products` and
  `seller_reviews`.
- **The defaults differ, deliberately.** Over MCP a list tool returns the
  first **10 light rows** (about 7 KB) because a tool result goes straight
  into a context window. Over `probe.py` you get the **whole page** unless
  you ask otherwise, because a script can pipe it — so
  `probe.py search --query ... --limit 10 --compact` (or
  `--fields asin,product_title,product_price`) is worth adding when you are
  reading the answer rather than filtering it. A parameter the script has no
  flag for goes through `--param name=value`.
- **The answer says what it did.** `_truncated` gives the real row count and
  the exact `limit=` to pass for all of them, `_omitted_fields` names what
  the light projection dropped, and `_notes` carries the things that will
  mislead you when reading these particular rows.

Three properties of Amazon's own data that will mislead you if you assume
otherwise:

1. **`product_num_ratings` is per listing family, not per ASIN.** Variants
   share a review pool, so every colour of one shoe reports the same count.
   Do not present it as "this variant has N reviews".
2. **A variant's title can be the parent's.** In search results the ASIN and
   the title can disagree — the URL slug usually shows the real variant. When
   the exact variant matters, call `/v2/product-details` on that ASIN; it is
   authoritative for the ASIN you passed.
3. **A search row's badges are the result card's, not the listing's.**
   `badges` (and the derived `is_amazon_choice` / `is_best_seller`) say what
   Amazon printed on that card for *that query*. `sort_by=BEST_SELLERS` is
   Amazon's popularity order for the query, not a category rank — so an ASIN
   that is #1 in *Women's Mules & Clogs* can show `badges: []` in a search
   for "crocs white" while `/v2/product-details` reports `best_seller: true`
   with the rank. For a rank claim, use product-details or best-sellers;
   `filters_applied.sort_by` echoes the order the page actually used.

`badges` is the source of truth for Amazon's Choice / Best Seller / Overall
Pick (Amazon renamed that slot to "Overall Pick"); `is_amazon_choice` and
`is_best_seller` are derived from it.

## Error handling — which failures cost money

- **`404`** — the item genuinely is not on that marketplace. **Billed** on the
  keyed path. Retrying will not help; try a different `geo` or accept it.
- **`503`** — a temporary Apiguru-side failure. **Not billed.** Retry with
  backoff. `500`, `502` and `504` are the same class: not billed, retry.
- **`429`** — rate limited. Back off, then retry.
- **no answer** (your client timed out, or the connection dropped) — keyless,
  nothing was billed; retry. **With an API key the call may still have
  finished and been billed**, so it is not repeated automatically: tell the
  user and retry only if they agree. The one exception is a call that never
  left the machine (the host name did not resolve, or the connection was
  refused): nothing was billed, and the body says so. Some marketplaces
  answer more slowly; allow 60s before giving up.
- **`400`** — your input was wrong (bad ASIN format, unknown geo, missing
  required parameter). Not billed. Fix the input; do not retry unchanged.
- **`402`** — free probes spent. **Stop and ask the user** (see "Costs and
  consent"). Do not retry, do not look for a key, do not attempt payment.

So: **retry `429`, `500`, `502`, `503`, `504` and keyless timeouts (unless the
body says `retryable: false`); never retry `400`, `402`, `404` or `413`, and
never repeat a timed-out keyed call, or one whose connection dropped, without
the user's say-so.**
`scripts/probe.py` does exactly this. Its exit status tells a job what
happened: `0` usable answer, `1` HTTP error or a body reporting failure,
`2` input rejected before any request, `3` a batch with some failed rows.

## Quick start

```bash
# prices, the free-probe policy, and how many free probes THIS caller has
# left right now (from /health; the policy number is not your balance). Free.
python scripts/probe.py capabilities

# one product
python scripts/probe.py product-details --asin B09DJLW458 --geo US

# many at once (preferred for lists); --compact: one light row each, with
# brand, weight and dimension
python scripts/probe.py product --asins B09DJLW458,B0BSHF7WHW --geo US --compact

# keyword search on amazon.co.uk
python scripts/probe.py search --query "wireless earbuds" --geo UK

# billed to the user's account, only after they said so.
# --api-key prompts; the key never appears in argv or in shell history.
python scripts/probe.py product-details --asin B09DJLW458 --geo US --api-key

# non-interactive equivalent, key straight from a secret store
pass show apiguru | python scripts/probe.py product-details --asin B09DJLW458 --api-key-stdin
```

## MCP alternative (optional, and outside this skill's audit)

**`scripts/probe.py` above is the supported path.** It is part of this skill,
it was reviewed with it, it is standard-library only, and it downloads and
executes nothing. Use it unless someone has decided otherwise.

The same data is also published as an MCP server. That server is a **separate
artifact**: it is not shipped in this skill, it was not covered by whatever
review this skill passed, and it needs its own security review before anyone
runs it. Three ways to reach it, safest first:

**1. The hosted server — nothing is installed or executed on your machine.**

```
https://mcp.apiguru.app/mcp        streamable HTTP
https://mcp.apiguru.app/account    the same thing behind OAuth 2.1
```

Your client talks HTTP to a server we run. No package is fetched, so there is
no supply chain on your side at all. This is the option to prefer.

**2. Install it once, deliberately, then run what you installed.** If you want
it local, make it a controlled deployment step rather than a fetch on every
launch:

```bash
python -m venv ~/.venvs/apiguru && ~/.venvs/apiguru/bin/pip install "apiguru-mcp==1.1.69"
# then point the client at the binary you just reviewed and installed:
#   "command": "/home/you/.venvs/apiguru/bin/apiguru-mcp"
```

Pin transitive dependencies too if that matters to you: resolve once with
`pip freeze > apiguru-lock.txt`, review it, and install from that file with
`--require-hashes`.

**3. Fetch at launch (`uvx` / `npx`).** Convenient, and the weakest of the
three: the launcher resolves and executes a package from a public registry
every time the client starts. Pinning the version — which the snippets below
do — stops it silently moving to a newer release, but it does not protect you
from a compromised publisher account or registry.

```json
{ "mcpServers": { "apiguru": { "command": "uvx",
  "args": ["apiguru-mcp==1.1.69"] } } }
```

or, with Node instead of Python, `"command": "npx", "args": ["apiguru-mcp@1.1.69"]`.

Whichever you choose:

- **Expected publisher:** `apiguru-app`. **Registries:** PyPI
  (`apiguru-mcp`, https://pypi.org/project/apiguru-mcp/) and npm
  (`apiguru-mcp`, https://www.npmjs.com/package/apiguru-mcp). Both are listed
  in the official MCP Registry as `app.apiguru/amazon-data`. Anything under
  another name or publisher is not ours.
- **Verify the artifact, not just the name and version.** PyPI and npm publish
  a SHA-256 for every file; `pip download apiguru-mcp==<version>` then
  `pip hash` gives you a digest to record and re-check on the next upgrade.
- **Before raising the pin**, read the changelog at
  https://github.com/apiguru-app/agent-kit/releases and diff the dependency
  list. Do it deliberately; do not let a launcher do it for you.
- **Run it with least privilege**: it needs outbound HTTPS to
  `agent.apiguru.app`, `dash.apiguru.app` and `mcp.apiguru.app` and nothing
  else — no filesystem access, no other credentials in its environment. A
  container is the easy way: an official image is published for exactly this
  (`mcp/apiguru`, Docker's MCP catalogue).

The MCP tools do the same thing as `probe.py` and follow the same rules — they
never pay on their own. A 402 comes back as an x402 PaymentRequired result: the
user decides, and only an x402-capable MCP client they set up (with a spend cap)
can pay it. Their advantage is that they validate ASINs and geos before spending a
probe.

## Telling us what is broken

This API gets fixed when the agents using it say what is wrong. Recent
example: search results were returning the brand as `product_title` and
`null` for `product_num_ratings`; an agent reported both and both are fixed.
So if a field is empty, mistyped, welded together or simply missing:

- **Preferred, if you have a GitHub account** — open an issue at
  https://github.com/apiguru-app/agent-kit/issues. A thread there can hold a
  reply and a fix gets linked back to it.
- **No GitHub account? Use the wall** — the script's `feedback` command, never
  billed, no signup, no key:

  ```bash
  python3 scripts/probe.py feedback --message "search: product_title holds the brand, not the title" --category bug --endpoint /search --agent your-name/1.0
  ```

  It sends that text, and nothing else, to `https://dash.apiguru.app/api/v1/feedback`.
  `--category` is one of `bug`, `wish`, `praise`, `question`, `other`. Add
  `--contact` if you want a reply — it is shown publicly on the wall.

  **The wall is public, so send only what the user has agreed to, and only
  about the API:** the tool, the parameters, the field, what you expected and
  the `request_id`. Never an API key, personal data, or the user's own
  prompts, documents or results beyond the field in question.
- **Over MCP** — the free `send_feedback` tool does the same thing.
- Read what other agents have written: https://dash.apiguru.app/feedback

Say what you called, what you expected and what came back, and quote the
`request_id` from the answer. **One issue per entry** — a five-point list
cannot be closed point by point, and each entry gets its own status on the
wall (`open`, `fixed`, `documented`, `answered`, `wont_fix`). A wish counts:
if you need a field this API does not return, that is the most useful thing
you can tell us.

## Reference files

- `references/endpoints.md` — every endpoint, parameter, and marketplace code
- `references/errors-and-costs.md` — pricing, billing rules, retry strategy
