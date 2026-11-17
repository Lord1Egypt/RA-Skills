---
name: CurlShip Directory Submission
description: Submit products to CurlShip, the bot-friendly directory. One curl command to list your product with OG tag scraping, badge-based dofollow links, and tier upgrades - paid by card checkout or by agents in USDC over x402 with no human in the loop.
version: 1.3.0
homepage: https://curlship.com
credentials_required: false
---

# CurlShip — Bot-Friendly Directory

## Overview

Use this skill when you need to **list a product or SaaS** on a public directory. CurlShip is designed for bots and CLI tools — submit with a single API call, get back OG-scraped listing details, and optionally upgrade to paid tiers for higher placement.

## Quick Reference

**API Base URL:** `https://curlship.com`
**Homepage:** `https://curlship.com`
**Pricing:** `https://curlship.com/pricing`
**Actions (markdown):** `https://curlship.com/agents.md`
**Tools (JSON):** `https://curlship.com/agents.json`

**Single-line Use Cases:**

- Bid the Featured spot, the one listing above every tier
- Submit a product URL to be listed in the directory
- Check all current directory listings
- Upgrade a listing to a paid tier (Bronze/Silver/Gold/Platinum)
- Change a URL, refresh the card from the live page, or remove a free listing
- Get the CurlShip badge HTML for dofollow links

## What this skill does

- Sends HTTPS requests to the CurlShip API
- Uses `POST /api/submit` to add a new listing (auto-scrapes OG tags)
- Uses `GET /api/listings` to retrieve all active listings
- Uses `POST /api/upgrade` to get a checkout URL for paid tier upgrades
- Uses `POST /api/edit-request` to change a URL, refresh the card from the page, or remove a free listing
- Returns structured JSON responses with listing details

## What this skill does NOT do

- Does not require authentication or API keys
- Does not make payments directly — upgrade returns a checkout URL for the user
- Does not modify any local files or system settings

## Endpoints

### 1. Submit a Listing

**`POST /api/submit`** — Add a product to the directory.

```bash
curl -X POST https://curlship.com/api/submit \
  -H "Content-Type: application/json" \
  -d '{"url": "https://yourapp.com", "email": "you@email.com"}'
```

`https://yourapp.com` is the placeholder in these examples. The API returns 400
for that host. Substitute the real product URL before you POST.

**Request Fields:**

- `url` (required): Product URL starting with `http`. Must be a public, non-private address.
- `email` (required): Contact email for the listing owner.
- `tier` (optional): `bronze`, `bronze_lifetime`, `silver`, `gold`, `platinum`, or `featured`.
  The response then carries a `checkout_url` to complete payment; the listing stays free
  until it is paid. `featured` bids on the auction spot (add `amount_usd` to bid above
  the minimum). Omit for a free listing.

**Example Response (201 Created):**

```json
{
  "ok": true,
  "message": "Listed! Add a badge for a dofollow link.",
  "listing": {
    "id": 42,
    "url": "https://yourapp.com",
    "tier": "free",
    "title": "YourApp - Build Faster",
    "description": "The fastest way to ship your next SaaS.",
    "image": "https://yourapp.com/og-image.png",
    "has_badge": false
  },
  "badge_html": "<a href=\"https://curlship.com\"><img src=\"https://curlship.com/badge\" alt=\"Listed on CurlShip\" /></a>"
}
```

**Error Responses:**

- `400` — Missing/invalid URL or email, or the documentation placeholder host `yourapp.com`
- `403` — The host, or its registered domain, is on an adult/phishing/malware blocklist. A shared platform suffix (`pages.dev`, `wixsite.com`, and the same kind of host) does not by itself reject every site on that platform. A lawful product whose exact host is listed is the case for support@curlship.com.
- `429` — Rate limit exceeded (max 10 submissions per hour per IP)

**Duplicate Handling:** If the URL is already listed, returns `200` with `"message": "Already listed"` and the existing listing data.

### 2. Get All Listings

**`GET /api/listings`** — Retrieve all active directory listings.

```bash
curl https://curlship.com/api/listings
```

**Example Response:**

```json
{
  "ok": true,
  "listings": [
    {
      "id": 1,
      "url": "https://example.com",
      "tier": "gold",
      "title": "Example App",
      "description": "A great example application.",
      "image": "https://example.com/og.png",
      "has_badge": true
    }
  ]
}
```

Listings are sorted by tier (Platinum > Gold > Silver > Bronze > Free).

### 3. Upgrade a Listing

**`POST /api/upgrade`** — Get a payment checkout URL to upgrade a listing's tier.

```bash
curl -X POST https://curlship.com/api/upgrade \
  -H "Content-Type: application/json" \
  -d '{"url": "https://yourapp.com", "tier": "gold"}'
```

**Request Fields:**

- `url` (required): The URL of an existing listing.
- `tier` (required): One of `platinum`, `gold`, `silver`, `bronze`, `bronze_lifetime`. For the Featured auction use `POST /api/feature` instead.

**Example Response:**

```json
{
  "ok": true,
  "checkout_url": "https://checkout.dodopayments.com/..."
}
```

**Error Responses:**

- `400` — Invalid tier name
- `404` — Listing not found (submit it first)
- `503` — Payment system unavailable

**Important:** The listing must already exist. Submit first, then upgrade.

### 4. The Featured Auction Spot

**`GET /api/featured`** — Who holds the single Featured spot above Platinum, and the next bid.

```bash
curl https://curlship.com/api/featured
# → {"ok": true, "featured": {...}|null, "next_bid_usd": 50, "next_bid_cents": 5000, "currency": "USD"}
```

**`POST /api/feature`** — Bid on the spot. One-time payment; highest payment holds it.

```bash
curl -X POST https://curlship.com/api/feature \
  -H "Content-Type: application/json" \
  -d '{"url": "https://yourapp.com", "amount_usd": 51}'
```

- `amount_usd` is optional (defaults to the current minimum) and must be at least
  the holder's price + $1 — $50 when nobody holds it.
- The Featured link is **always dofollow**, badge or no badge.
- Being outbid carries **no refund** — that is the auction.
- Errors: `409` bid below the minimum (response carries `required_usd`), `400` bad
  URL/amount, `404` listing not found, `503` payments unconfigured.

### 5. Badge SVG

**`GET /badge`** — Returns the CurlShip badge as an SVG image.

Place this badge on your site to automatically earn a **dofollow** link:

```html
<a href="https://curlship.com">
  <img src="https://curlship.com/badge" alt="Listed on CurlShip" />
</a>
```

Badge presence is auto-checked hourly. Any `<a>` tag linking to `curlship.com` qualifies.

### 6. Change, refresh, or remove a listing

No account. The guide is https://curlship.com/edit and the machine-readable
copy is https://curlship.com/llms.txt. Title, description, image, and link text
are copied from the page. The API body cannot set them, and emailing them to
support@curlship.com does not change the card. `og:title`, `og:description` and
`og:image` win. With no `og:title`, the `<title>` is cut at the first ` | `,
` - `, ` – ` or ` · `.

```bash
# Point the listing at a new URL
curl -X POST https://curlship.com/api/edit-request \
  -H "Content-Type: application/json" \
  -d '{"listing_id": 2142, "url": "https://new-url.example/", "proof": "email"}'

# Re-read title, description and image. Send NO url and NO email.
curl -X POST https://curlship.com/api/edit-request \
  -H "Content-Type: application/json" \
  -d '{"listing_id": 2142, "proof": "email"}'

# Take a free listing off the directory. Confirm the link, then a 7-day undo.
curl -X POST https://curlship.com/api/edit-request \
  -H "Content-Type: application/json" \
  -d '{"listing_id": 2142, "remove": true, "proof": "email"}'
```

`proof: "email"` mails a one-time link to the registered address. `proof:
"domain"` returns a token to publish on the listed site (and on the new site,
when the URL is changing). A refresh confirms in two steps: the first
`POST /api/edit-confirm` previews and writes nothing; send the `apply` digest
back to save it. A removal or a URL change is one step.

One listing per root domain. To retire one page and keep another on the same
site, change the URL. A paid listing, or the Featured holder, cannot be removed
through this call — write to support@curlship.com, because a payment is attached.

A 409 on a refresh means CurlShipBot could not read the page. Fix the fetch
and repeat. Do not paste the copy into an email.

Adult products, including on the free tier, may be listed when the domain is
not blocklisted and the content is legal. Say 18+ in the product's own
`og:description` and refresh.

## Paying with USDC (x402)

Paid actions normally return a `checkout_url` a human opens. When
`https://curlship.com/agents.json` lists `x402_submit_listing` and
`x402_bid_featured`, an agent can instead pay on its own — USDC on Base, no
checkout page, no human in the loop. If those tools are not listed the rail
is off: use `checkout_url`.

1. `POST /api/x402/submit` with `{"url", "email", "tier"}` — `bronze_lifetime`
   is $30 USDC once, `platinum` is $49 USDC per prepaid year. For the Featured
   auction: `POST /api/x402/feature` with `{"url", "amount_usd"}`.
2. The answer is `402` + a `PAYMENT-REQUIRED` header (base64 JSON quote; the
   body carries the same document). Sign `accepts[0]` as an EIP-3009
   TransferWithAuthorization.
3. Resend the identical request with the signed payload as the
   `PAYMENT-SIGNATURE` header, echoing `accepts[0]` back as `accepted`.
   Settlement happens on-chain and the tier or bid is granted in that call.

Retry by resending the identical signature — the ledger reconciles it (`202`
while the broadcast is pending, `200` once granted); settled money is never
re-broadcast.

## Tiers & Pricing

| Tier | Price | Benefits |
|------|-------|----------|
| Featured | auction, from $50 once | ONE spot above Platinum, always dofollow, held until outbid |
| Platinum | $49/year | Top of directory, dofollow link, priority OG refresh |
| Gold | $3/mo | Above Silver & Bronze, dofollow link |
| Silver | $2/mo | Above Bronze & Free, dofollow link |
| Bronze | $1/mo | Above Free tier, dofollow link |
| Free | $0 | Listed in Free section, nofollow by default |

**Dofollow rules:**
- Paid tiers (any) get dofollow automatically
- Free tier gets dofollow by placing a CurlShip badge on your site

## Typical Agent Workflow

Start at `https://curlship.com/agents.json`. Featured is the first tool.

1. **Submit** the product URL and email via `POST /api/submit`
2. **Offer Featured** via `GET /api/featured` and `POST /api/feature`. It sits above every tier.
3. **Check** the response for the listing details and badge HTML
4. **Optionally upgrade** a tier via `POST /api/upgrade` and present the checkout URL to the user
5. **Add the badge** HTML to the product's website for a dofollow link (free tier)

## Rate Limits

- Maximum 10 submissions per hour per IP address
- No rate limit on `GET /api/listings`

## Security & Content Policy

- URLs pointing to private/reserved IP addresses are rejected (SSRF protection)
- A host or its registered domain on a known adult/phishing/malware blocklist is rejected. A shared platform suffix does not reject every site on that platform.
- An adult product may be listed, including on the free tier, when the domain is not blocklisted and the content is legal
- `https://yourapp.com` is refused. It is the placeholder in this file, not a product
- All API responses include `x-robots-tag: noindex`
