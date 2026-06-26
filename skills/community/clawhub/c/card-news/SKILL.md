---
name: card-news
description: Return material news about one major-US credit card from the last 3 months — direct card changes, issuer updates, and major coverage. Covers 11 major US issuers including co-branded hotel and airline cards.
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

# Card News

Return the last-3-month news view of one exact card variant in compact format.

## When To Use

When the user asks about recent changes, news, or updates for a credit card. Trigger phrases: "card-news", "any changes", "recent news", "what's new with", "updates for".

## Workflow

1. **Resolve card identity** — normalize and match to one exact variant. If ambiguous, return a numbered choice list and stop.
2. **Search** — use `WebSearch` by default with a recent-results bias. If `BRAVE_API_KEY` is available and `curl` exists, you may use one Brave Search API call with freshness filter instead.
3. **Fetch pages** — fetch the top news pages before deciding whether another search is needed.
4. **Filter** — apply 3-month lookback window and inclusion rules.
5. **Pace any follow-up searches** — if another search is needed, wait briefly instead of bursting requests.
6. **Compile** — assemble the news report.
7. **Confidence** — flag uncertain or conflicting claims.

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

## Step 2: Search

Use the platform's **WebSearch** and **WebFetch** tools by default. If `BRAVE_API_KEY` is available and the runtime also provides `curl`, you may use Brave Search API instead for faster and more repeatable search results.

Optional Brave template:

```bash
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+news+CURRENT_YEAR&count=20&freshness=p3m" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

The `freshness=p3m` parameter limits results to the past 3 months, matching the lookback window. Replace `CURRENT_YEAR` with the actual current year.

### Search Budget Rule

Treat search as scarce and paced. Built-in web search is the default path; if Brave mode is used, it may rate-limit after only a few closely spaced requests.

- Start with one search.
- Fetch the top result pages before deciding whether another search is needed.
- If an extra search is needed, wait about **2 to 5 seconds** first.
- If Brave returns **429**, wait about **8 to 15 seconds** and retry once.
- If Brave is unavailable, continue with `WebSearch` + `WebFetch`.
- If it still fails, continue with the best evidence already gathered and note the limitation in `## 📋 Confidence Notes`.

### Source Policy

- **Issuer newsrooms first**: check issuer blogs and press release pages.
- **Max 5 secondary sources** from: Doctor of Credit (preferred), The Points Guy (preferred), One Mile at a Time (preferred), NerdWallet (preferred), Bankrate (preferred), Upgraded Points.
- **Disallowed**: Reddit, Facebook, Instagram, TikTok, X, YouTube, referral links, user forums.

## Recency Rules

- Use a **3-month lookback window** only.
- **Include**: direct card changes, issuer updates that materially affect the card, major approved-site coverage that changes how the card should be understood.
- **Exclude**: generic issuer chatter, evergreen "best card" articles that do not describe a recent change.

## Step 4: Fetch Pages

Pick up to 2 top article URLs (prefer doctorofcredit.com and thepointsguy.com) from the search results. Fetch in parallel with `WebFetch`.

Approved news pages are limited to issuer newsroom pages and the approved news/article domains named in this skill. Do not fetch or cite article pages from any other domain.

### URL Safety Rules

- Prefer `WebFetch` for page retrieval. Use `curl` only for the optional Brave Search API calls above, not for arbitrary result URLs.
- Never execute a shell command that interpolates a raw URL taken directly from search results.
- Only fetch URLs when all of the following are true:
  1. scheme is `https`
  2. hostname matches a supported issuer domain or an approved article domain from this skill
  3. the URL is being passed to `WebFetch`, not inserted into a shell pipeline
- If a result URL fails those checks, skip it and use the next valid result.

News snippets often lack dates and detail — the full article has the complete story and timeline.

## Required Output Sections

### `## 📅 News Window`
Start and end dates of the 3-month lookback window.

### `## 📰 Recent Updates`
Numbered list of material changes with date and short summary per item.

### `## 📝 Summary`
2-3 sentence synthesis of what changed and what stayed the same.

### `## 📋 Confidence Notes`
Flag any uncertain, unconfirmed, or conflicting claims.

### `## 🔗 Sources`
Numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels.

## Output Rules

- Use one emoji per section heading and numbered lists
- When listing credits, fees, or any monetary amounts, sort from highest to lowest dollar value. for updates.
- Keep content to condensed facts — no prose padding.
- Omit the Card Identity section when the match is confident.
- Do not show YAML blocks in output.
- End every report with a `## 🔗 Sources` section listing each URL fetched during research as a markdown hyperlink with a short "Site - Topic" label, e.g. `[Doctor of Credit - Amex Gold Changes](https://...)`.

## Confidence Definitions

- **confirmed**: supported by issuer terms or multiple approved sources
- **unconfirmed**: plausible but not fully resolved
- **conflicting**: sources disagree on a material fact
