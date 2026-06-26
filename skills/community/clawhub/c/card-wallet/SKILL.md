---
name: card-wallet
description: Audit a multi-card wallet — earning map, credit stack, overlaps, gaps, and total annual cost. Evaluates a user's full card lineup. Covers 11 major US issuers including co-branded hotel and airline cards.
allowed-tools:
  - WebSearch
  - WebFetch
  - AskUserQuestion
metadata:
  openclaw:
    requires:
      optionalEnv:
        - BRAVE_API_KEY
      optionalBins:
        - curl
---

# Card Wallet

Return a compact wallet audit for a set of cards the user holds.

## When To Use

When the user asks to evaluate their card lineup, check for overlap, or optimize their wallet. Trigger phrases: "card-wallet", "wallet audit", "my cards", "do I have overlap", "which cards should I keep".

## Input Format

The user provides a comma-separated list of card names:
- `card-wallet Chase Sapphire Preferred, Amex Gold, Citi Double Cash`

## Workflow

1. **Parse card list** from comma-separated input.
2. **Resolve each card** — normalize and match to exact variants. If any card is ambiguous, return a numbered choice list for that card and stop.
3. **Search** — use `WebSearch` by default per card. If `BRAVE_API_KEY` is available and `curl` exists, you may use one Brave Search API call per card instead. Classify results as issuer or secondary by domain.
4. **Fetch pages** — fetch issuer and approved secondary pages before deciding whether more searches are needed.
5. **Pace batch searches** — when multiple cards require searches, serialize or batch them gently instead of firing a large burst.
6. **Collect** — for each card: annual fee, top earning categories, statement credits, key benefits.
7. **Analyze** — identify overlapping earn categories, uncovered categories, redundant benefits, total fee burden.
8. **Confidence** — flag uncertain claims.

## Step 1: Card Identity Resolution

### Common Abbreviations

Only shorthands and ambiguous names need entries here. Cards with full, unambiguous names (e.g., "Chase Marriott Bonvoy Boundless", "Chase United Explorer", "American Express Hilton Honors Aspire") are resolved via search — no table entry needed.

| Input | Resolved |
|---|---|
| CSP | Chase Sapphire Preferred |
| CSR | Chase Sapphire Reserve |
| CFU | Chase Freedom Unlimited |
| CFF | Chase Freedom Flex |
| CIP | Chase Ink Business Preferred |
| CIC | Chase Ink Business Cash |
| CIU | Chase Ink Business Unlimited |
| Amex Gold | American Express Gold Card |
| Amex Plat | American Express Platinum Card |
| Amex Biz Gold | American Express Business Gold Card |
| Amex Biz Plat | American Express Business Platinum Card |
| Amex Blue Biz Plus | American Express Blue Business Plus Card |
| Amex Blue Biz Cash | American Express Blue Business Cash Card |
| Venture X | Capital One Venture X Rewards Credit Card |
| Venture X Business | Capital One Venture X Business Card |
| Savor | Capital One SavorOne / Savor (ambiguous — ask) |
| Spark Cash Plus | Capital One Spark Cash Plus |
| Spark Miles | Capital One Spark Miles |
| Double Cash | Citi Double Cash Card |
| Custom Cash | Citi Custom Cash Card |
| Ink Preferred | Chase Ink Business Preferred |
| Ink Cash | Chase Ink Business Cash |
| Ink Unlimited | Chase Ink Business Unlimited |
| Bilt | Bilt Blue / Obsidian / Palladium (ambiguous — ask) |
| Robinhood | Robinhood Gold Card / Cash Card (ambiguous — ask) |
| Aviator Red | Barclays AAdvantage Aviator Red World Elite Mastercard |
| Wyndham Rewards | Barclays Wyndham Rewards Earner Card / Plus / Business (ambiguous — ask) |
| Altitude Reserve | U.S. Bank Altitude Reserve Visa Infinite Card |
| Altitude Connect | U.S. Bank Altitude Connect Visa Signature Card |
| Altitude Go | U.S. Bank Altitude Go Visa Signature Card |
| Delta Gold | American Express Delta SkyMiles Gold Card |
| Delta Platinum | American Express Delta SkyMiles Platinum Card |
| Delta Reserve | American Express Delta SkyMiles Reserve Card |
| Delta Biz Gold | American Express Delta SkyMiles Gold Business Card |
| Delta Biz Plat | American Express Delta SkyMiles Platinum Business Card |
| Delta Biz Reserve | American Express Delta SkyMiles Reserve Business Card |

### Supported Issuers

American Express, Bank of America, Barclays, Bilt, Capital One, Chase, Citi, Discover, Robinhood, U.S. Bank, Wells Fargo.

## Step 2: Search (Per Card)

Use the platform's **WebSearch** and **WebFetch** tools by default. If `BRAVE_API_KEY` is available and the runtime also provides `curl`, you may use Brave Search API instead for faster and more repeatable search results.

Optional Brave template:

```bash
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+benefits+credits&count=10" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

Do not assume any search provider tolerates a large burst of parallel searches.

### Search Budget Rule

Treat search as scarce and paced. Built-in web search is the default path; if Brave mode is used, it may rate-limit after only a few closely spaced requests.

- Start with the most important cards first.
- Fetch issuer and approved secondary pages before deciding whether more searches are needed.
- When multiple cards require searches, serialize them in small batches or add short waits of about **2 to 5 seconds** between bursts.
- If Brave returns **429**, wait about **8 to 15 seconds** and retry once for the still-missing search.
- If Brave is unavailable, continue with `WebSearch` + `WebFetch`.
- If it still fails, continue with the best evidence already gathered and note the limitation in `## 📋 Confidence Notes`.

Classify results by domain: issuer pages (use Issuer Domains table below) vs approved secondary sources. Optionally use 1 secondary source (prefer thepointsguy.com) for cross-checking.

### Fetch Pages

For each card, fetch the top issuer URL from search results. Optionally fetch 1 secondary URL with `WebFetch`.

An approved secondary page means a URL whose hostname matches the preferred secondary domains named in this skill. Do not fetch or cite secondary pages from any other domain.

### URL Safety Rules

- Prefer `WebFetch` for page retrieval. Use `curl` only for the optional Brave Search API calls above, not for arbitrary result URLs.
- Never execute a shell command that interpolates a raw URL taken directly from search results.
- Only fetch URLs when all of the following are true:
  1. scheme is `https`
  2. hostname matches a supported issuer domain or an approved secondary domain from this skill
  3. the URL is being passed to `WebFetch`, not inserted into a shell pipeline
- If a result URL fails those checks, skip it and use the next valid result.

Run fetches in parallel. Search snippets alone miss detailed credit and rate info. Combine fetched page content + search snippets + training knowledge.

### Issuer Domains (for classifying results, not constraining searches)

| Issuer | Domain |
|---|---|
| American Express | americanexpress.com |
| Bank of America | bankofamerica.com |
| Barclays | cards.barclaycardus.com |
| Bilt | bfrrewards.com |
| Capital One | capitalone.com |
| Chase | chase.com |
| Citi | citi.com |
| Discover | discover.com |
| Robinhood | robinhood.com |
| U.S. Bank | usbank.com |
| Wells Fargo | wellsfargo.com |

## Required Output Sections

### `## 💰 Annual Cost`
Total annual fees across all cards, listed per card.

### `## 📈 Earning Map`
Table showing the best card for each major spend category (dining, travel, groceries, gas, streaming, other).

### `## 🏷️ Credits Stack`
Statement credits, cash-back rebates, and complimentary subscriptions only — not enhanced earn rates or point multipliers. All credits across the wallet with total annual value.

### `## 🔁 Overlap`
Numbered list of redundant earn categories or duplicate benefits.

### `## 🕳️ Gaps`
Numbered list of common spend categories not covered at a bonus rate by any card.

### `## 📋 Confidence Notes`
Flag any uncertain, unconfirmed, or conflicting claims.

### `## 🔗 Sources`
Numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels.

## Output Rules

- Use one emoji per section heading and numbered lists for overlap/gaps.
- When listing credits, fees, or any monetary amounts, sort from highest to lowest dollar value.
- Keep content to condensed facts — no prose padding.
- Omit the Card Identity section when all matches are confident.
- Do not show YAML blocks in output.
- End every report with a `## 🔗 Sources` section listing each URL fetched during research as a markdown hyperlink with a short "Site - Topic" label, e.g. `[Chase - Sapphire Preferred](https://...)`.

## Confidence Definitions

- **confirmed**: supported by issuer terms or multiple approved sources
- **unconfirmed**: plausible but not fully resolved
- **conflicting**: sources disagree on a material fact
