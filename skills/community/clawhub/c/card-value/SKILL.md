---
name: card-value
description: Estimate first-year value for one major-US credit card — welcome bonus + annual earn + credits minus annual fee. Accepts an optional spending breakdown. Covers 11 major US issuers including co-branded hotel and airline cards.
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

# Card Value

Return a compact first-year value estimate for one exact card variant.

## When To Use

When the user asks about a card's value, worth, or first-year return. Trigger phrases: "card-value", "is it worth it", "first year value", "value estimate", "how much is the card worth".

## Input Format

The user provides a card name followed by an optional spending breakdown:
- `card-value Chase Sapphire Preferred` — uses default spend profile
- `card-value Chase Sapphire Preferred $500/mo dining, $200/mo travel, $3000/mo other` — uses provided breakdown

Default moderate-spender profile (if none given): $500/mo dining, $200/mo travel, $100/mo streaming, $200/mo groceries, $2000/mo other.

## Workflow

1. **Resolve card identity** — normalize and match to one exact variant. If ambiguous, return a numbered choice list and stop.
2. **Search** — use `WebSearch` by default for current welcome offer and fee details. If `BRAVE_API_KEY` is available and `curl` exists, you may use one Brave Search API call instead.
3. **Fetch pages** — use `WebFetch` by default to fetch the issuer and approved secondary pages before deciding whether another search is needed.
4. **Pace any follow-up searches** — if another search is needed, wait briefly instead of bursting requests.
5. **Research** — collect annual fee, welcome offer (bonus + spend requirement), earning rates by category, and statement credits.
6. **Compute** — `first_year_value = welcome_bonus_value + annual_earn_value + total_credits - annual_fee`.
7. **Confidence** — flag uncertain claims. Use 1 cpp baseline unless a known portal/transfer premium exists.

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
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+welcome+offer+annual+fee&count=20" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

### Search Budget Rule

Treat search as scarce and paced. Built-in web search is the default path; if Brave mode is used, it may rate-limit after only a few closely spaced requests.

- Start with one search.
- Fetch the issuer and approved secondary pages before deciding whether any additional search is needed.
- If an extra search is needed, wait about **2 to 5 seconds** first.
- If Brave returns **429**, wait about **8 to 15 seconds** and retry once.
- If Brave is unavailable, continue with `WebSearch` + `WebFetch`.
- If it still fails, continue with the best evidence already gathered and note the limitation in `## 📋 Confidence Notes`.

### Source Policy

- **Issuer-first**: check the card's official product page first.
- **Max 5 secondary sources** from: NerdWallet (preferred), The Points Guy (preferred), Bankrate (preferred), One Mile at a Time (preferred), Doctor of Credit (preferred), Upgraded Points.
- **Disallowed**: Reddit, Facebook, Instagram, TikTok, X, YouTube, referral links, user forums.

## Step 4: Fetch Pages

Pick the top issuer URL and up to 2 secondary URLs (prefer nerdwallet.com and thepointsguy.com) from the search results. Fetch in parallel with `WebFetch`.

An approved secondary page means a URL whose hostname matches one of the approved secondary domains named in this skill. Do not fetch or cite secondary pages from any other domain.

### URL Safety Rules

- Prefer `WebFetch` for page retrieval. Use `curl` only for the optional Brave Search API calls above, not for arbitrary result URLs.
- Never execute a shell command that interpolates a raw URL taken directly from search results.
- Only fetch URLs when all of the following are true:
  1. scheme is `https`
  2. hostname matches a supported issuer domain or an approved secondary domain from this skill
  3. the URL is being passed to `WebFetch`, not inserted into a shell pipeline
- If a result URL fails those checks, skip it and use the next valid result.

Search snippets are too shallow for value calculations — the actual pages have complete credit values, earning rates, and offer details.

## Required Output Sections

### `## 💳 Spend Profile`
The spending breakdown being used (default or user-provided), formatted as a compact table.

### `## 🎁 Welcome Bonus`
Bonus amount, spend requirement, qualification window, point valuation used.

### `## 📈 Annual Earn`
Earn by category based on the spend profile, with point values.

### `## 🏷️ Credits`
Statement credits, cash-back rebates, and complimentary subscriptions only — not enhanced earn rates or point multipliers. Show applicable credits with annual total.

### `## 💰 Net First-Year Value`
Show the math clearly: `welcome_bonus + annual_earn + credits - annual_fee = net_value`.

### `## 📋 Confidence Notes`
Flag any uncertain claims. Note the cpp valuation assumed.

### `## 🔗 Sources`
Numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels.

## Output Rules

- Use one emoji per section heading.
- When listing credits, fees, or any monetary amounts, sort from highest to lowest dollar value.
- Show the math clearly in the Net First-Year Value section.
- Keep content to condensed facts — no prose padding.
- Omit the Card Identity section when the match is confident.
- Do not show YAML blocks in output.
- End every report with a `## 🔗 Sources` section listing each URL fetched during research as a markdown hyperlink with a short "Site - Topic" label, e.g. `[Chase - Sapphire Preferred](https://...)`.

## Confidence Definitions

- **confirmed**: supported by issuer terms or multiple approved sources
- **unconfirmed**: plausible but not fully resolved
- **conflicting**: sources disagree on a material fact
