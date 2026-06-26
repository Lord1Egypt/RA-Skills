---
name: card-profile-recommend
description: Analyze a multi-card portfolio — grade each card (MVP / Keep / Consider Dropping), recommend 2–3 new additions with churning strategy, apply issuer rules (Chase 5/24, Amex lifetime bonus, Citi 8/65), and sequence applications to maximize signup bonuses. Covers 11 major US issuers including co-branded hotel and airline cards.
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

# Card Profile Recommend

Return a graded portfolio audit plus opinionated new-card recommendations with signup bonus strategy, churning paths, and issuer rule checks.

## When To Use

When the user wants to know which cards to keep, drop, or add next. Trigger phrases: "card-profile-recommend", "recommend cards", "what cards should I add", "credit card recommendations", "optimize my wallet", "what card should I get next", "improve my card lineup".

## Input Format

The user provides a comma-separated list of cards they currently hold:
- `card-profile-recommend Chase Sapphire Preferred, Amex Gold, Citi Double Cash`

Optional: opening dates per card (inline or separate list):
- `card-profile-recommend CSP (Jan 2024), Amex Gold (Mar 2023), Double Cash (2021)`

When opening dates are provided, calculate exact 5/24 count and factor into grading decisions.

## Workflow

1. **Parse card list** from comma-separated input.
2. **Resolve each card** — normalize and match to exact variants. If any card is ambiguous, return a numbered choice list for that card and stop.
3. **Search** — use `WebSearch` by default for each card plus any needed gap-category searches. If `BRAVE_API_KEY` is available and `curl` exists, you may use Brave Search API instead, but do not burst requests blindly.
4. **Fetch pages** — for each card, fetch the top issuer URL + 1 secondary (prefer thepointsguy.com). For new-card candidates, fetch up to 2 secondary pages.
5. **Pace any follow-up searches** — if more searches are needed, serialize them with short waits rather than firing them all at once.
6. **Collect** — for each card: annual fee, statement credits (with conditions), earning categories with rates, welcome offer status, notable benefits.
6. **Portfolio economics** — compute total gross fees, total claimable credits, net annual cost. Per-card net cost.
7. **Grade each card** — MVP / Keep / Consider Dropping per grading criteria below.
8. **Point valuations** — determine effective cpp for each currency using TPG valuations + transfer-access rule.
9. **Earning map** — best card per category with effective value (rate × cpp).
10. **Identify gaps** — categories earning below 2x / 2%.
11. **Recommend 2–3 new personal cards** — fill gaps, add ecosystems, maximize SUB windows, include churning strategy.
12. **Build application sequence** — ordered by priority with timing notes.
13. **Confidence** — flag uncertain claims.

## Step 1: Card Identity Resolution

### Common Abbreviations

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
| Venture X | Capital One Venture X Rewards Credit Card |
| Double Cash | Citi Double Cash Card |
| Custom Cash | Citi Custom Cash Card |
| Bilt | Bilt Blue / Obsidian / Palladium (ambiguous — ask) |
| Robinhood | Robinhood Gold Card / Cash Card (ambiguous — ask) |

### Supported Issuers

American Express, Bank of America, Barclays, Bilt, Capital One, Chase, Citi, Discover, Robinhood, U.S. Bank, Wells Fargo.

## Step 2: Search

Use the platform's **WebSearch** and **WebFetch** tools by default. If `BRAVE_API_KEY` is available and the runtime also provides `curl`, you may use Brave Search API instead for faster and more repeatable search results.

Optional Brave template:

```bash
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+benefits+credits+annual+fee&count=10" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

Do not assume any search provider tolerates a large burst of parallel searches.

### Search Budget Rule

Treat search as scarce and paced. Built-in web search is the default path; if Brave mode is used, it may rate-limit after only a few closely spaced requests.

- Start with the most important cards first.
- Fetch issuer and approved secondary pages before deciding whether more searches are needed.
- When multiple searches are required, serialize them in small batches or add short waits of about **2 to 5 seconds** between bursts.
- If Brave returns **429**, wait about **8 to 15 seconds** and retry once for the still-missing search.
- If Brave is unavailable, continue with `WebSearch` + `WebFetch`.
- If it still fails, continue with the best evidence already gathered and note the limitation in `## 🔍 Confidence Notes`.

Additionally, search for new-card candidates targeting gap categories.

### Fetch Pages

For each card, fetch the top issuer URL + 1 secondary with `WebFetch`.

An approved secondary page means a URL whose hostname matches an approved secondary domain used by this skill, such as `thepointsguy.com` for card cross-checks. Do not fetch or cite secondary pages from any other domain.

### URL Safety Rules

- Prefer `WebFetch` for page retrieval. Use `curl` only for the optional Brave Search API calls above, not for arbitrary result URLs.
- Never execute a shell command that interpolates a raw URL taken directly from search results.
- Only fetch URLs when all of the following are true:
  1. scheme is `https`
  2. hostname matches a supported issuer domain or an approved secondary domain from this skill
  3. the URL is being passed to `WebFetch`, not inserted into a shell pipeline
- If a result URL fails those checks, skip it and use the next valid result.

### Issuer Domains (for classifying results)

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

## Grading Criteria

### MVP
- Net cost ≤ $50, OR unique 3x+ earn category, OR unique high-value benefit (lounge, hotel status, primary travel insurance)
- Best rate in at least one major spend category
- Not rendered redundant by another card in wallet

### Keep
- Partially justifying benefit or earn rate
- Long credit history
- Transferable points diversification
- Under 12 months old

### Consider Dropping
- Fees exceed claimable credits with no unique benefit
- All categories duplicated at equal or better rate
- No-fee downgrade path exists
- **Never** grade Consider Dropping if the card is the sole source of a transferable-points program

### Unused Card Check
After building the earning map, flag any card that does not appear as "Best Card" in any category and has an annual fee.

## Point Valuation: Transfer-Access Rule

A currency is only worth full TPG value if the wallet has a card that unlocks transfers. Without one, value is 1.0¢ (cash back).

| Currency | Transfer-enabling cards | Full value |
|---|---|---|
| Chase UR | Sapphire Preferred, Sapphire Reserve | ~2.0¢ |
| Amex MR | Gold, Platinum, Green | ~2.0¢ |
| Capital One Miles | Venture X, Venture | ~1.8¢ |
| Citi TYP | Strata Premier, Strata Elite (NOT Custom Cash/Double Cash alone) | ~1.7¢ |
| Bilt Points | Any Bilt card | ~1.8¢ |
| World of Hyatt | Chase Hyatt card | ~1.8¢ |
| Marriott Bonvoy | Any Marriott co-brand | ~0.7¢ |
| Cash back | Any | 1.0¢ |

## Recommendation Logic

Select 2–3 new **personal** cards only. Never recommend business cards. Priority order:
1. Fill highest-value spend gap
2. Add new transferable-points ecosystem
3. Maximize signup bonus window (Chase-first if 5/24 allows)
4. Avoid worsening overlap
5. Prioritize elevated offers
6. Diversify issuers
7. Churning value — favor cards with SUB ≥ 5x annual fee, no-fee downgrade paths, and reasonable bonus cooldown windows. Note churn path explicitly.

## Issuer Rules Reference

| Issuer | Rule | Detail |
|---|---|---|
| Chase | 5/24 | <5 new personal cards (all issuers) in 24 months |
| Chase | Same-day | Max 1 personal Chase app per day |
| Chase | Bonus cooldown | 48 months since last bonus on same product |
| Amex | Lifetime bonus | Once per lifetime per person per card |
| Amex | 5-credit-card limit | Max 5 Amex credit cards (charge cards excluded) |
| Amex | 1-in-5/2-in-90 | 1 app per 5 days, 2 per 90 days |
| Citi | 8/65 | No 2 Citi cards in 8 days; max 2 in 65 days |
| Citi | 48-month family | No bonus if same family opened/closed in 48 months |
| Capital One | 2-card limit | Max 2 personal cards |
| Capital One | 6-month cooling | Declines if new account in last 6 months |

## Required Output Sections

### `## 🃏 Cards Entered`
Echo back every card with resolved full official name and opening date if provided.

### `## 📊 Portfolio Summary`
Total cards, gross fees, claimable credits, net annual cost. Note credit utilization assumptions.

### `## 🏅 Card Grades`
Each card graded MVP / Keep / Consider Dropping with one-line rationale. Always use full official card names. Sort MVP first, then Keep, then Consider Dropping.

### `## 🗺️ Earning Map`
Table: Category, Best Card, Rate, Currency, CPP, Effective Value. Use full official card names. CPP reflects transfer-access rule.

### `## 🔻 Consider Dropping`
Only when applicable. Per card: fee drag, what would be lost, downgrade path. Flag unused cards (not winning any earning map category). Omit entirely when all cards grade MVP or Keep.

### `## 🕳️ Portfolio Gaps`
Numbered list of categories earning below 2x / 2%.

### `## ➕ Recommended Additions`
2–3 new cards. Per card: name, welcome offer, annual fee, why it fits, net first-year value, issuer rule status, priority label, churn path if applicable.

### `## 🎯 Signup Bonus Strategy`
Ordered application sequence with timing and spend feasibility.

### `## ⚖️ Issuer Rules Check`
Only rules relevant to recommended cards. Bold blocking rules.

### `## 🔍 Confidence Notes`
Flag uncertain, unconfirmed, or conflicting claims.

### `## 🔗 Sources`
Numbered list of URLs fetched, as markdown hyperlinks with "Site - Topic" labels.

## Output Rules

- Use one emoji per section heading.
- Always use full official card names (e.g., "Chase Sapphire Reserve" not "CSR").
- Use numbered lists for list-heavy sections.
- Keep content to condensed facts — no prose padding.
- Omit Card Identity section when all matches are confident.
- Do not show YAML blocks in output.

## Confidence Definitions

- **confirmed**: supported by issuer terms or multiple approved sources
- **unconfirmed**: plausible but not fully resolved
- **conflicting**: sources disagree on a material fact
