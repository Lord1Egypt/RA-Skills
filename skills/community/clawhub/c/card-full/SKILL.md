---
name: card-full
description: Return a compact full report for one major-US credit card — fees, welcome offer, earning rates, redemption, credits, travel benefits, protections, mechanics, eligibility, and strategy. Covers 11 major US issuers including co-branded hotel and airline cards.
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

# Card Full

Research any major US credit card and return a compact, complete report.

## When To Use

When the user asks for a full credit card review, breakdown, or "tell me about [card]". Trigger phrases: "card-full", "full report", "tell me about the [card name]", "review [card name]".

## Workflow

1. **Resolve card identity** — normalize the input, fix abbreviations, and match to one exact card variant.
2. **Run the main search first** — use `WebSearch` by default to discover the issuer page plus likely secondary sources. If `BRAVE_API_KEY` is available and `curl` exists, you may use one Brave search instead for faster results.
3. **Fetch issuer + secondary pages** — fetch the issuer page and up to 3 approved secondary pages as needed.
4. **Search for best public offer** — run a second search only after a short delay, and only after the first fetch pass is complete.
5. **Search for historical offers** — run a third search only after another short delay, preserving historical-offer coverage without bursting requests.
6. **Recover welcome-offer data explicitly** — if the issuer page does not expose the live offer cleanly, use approved secondary sources to identify the current public offer and the best public offer.
7. **Compile** — assemble the report using the required sections below.
8. **Confidence** — flag uncertain or conflicting claims in the Confidence Notes section, especially around welcome offers.

## Step 1: Card Identity Resolution

Normalize the card name and resolve to an exact issuer + family + variant.

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

### Business vs Personal

Both personal and business credit cards are supported. If the user specifies "business" or "biz", resolve to the business variant. If a card name exists in both versions and the user does not specify, treat as ambiguous and ask.

### Ambiguity Rules

- If the input maps to 2+ plausible variants (e.g., "Chase Sapphire" could be Preferred or Reserve), return a **numbered choice list** and stop. Do not guess.
- If no match exists, return: "Could not match a card. Try including the full card name with issuer."

### Supported Issuers

American Express, Bank of America, Barclays, Bilt, Capital One, Chase, Citi, Discover, Robinhood, U.S. Bank, Wells Fargo. If the card is from an unsupported issuer, return: "This card is not from a supported issuer."

## Step 2: Search

Use the platform's **WebSearch** and **WebFetch** tools by default. If `BRAVE_API_KEY` is available and the runtime also provides `curl`, you may use Brave Search API instead for faster and more repeatable search results.

Optional Brave template:

```bash
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+review+welcome+offer&count=10" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

Parse the JSON response — results are in `.web.results[]` with `.title`, `.url`, `.description` fields.

### Search Budget Rule

Treat search as scarce and **paced**. Built-in web search is the default path; if Brave mode is used, it may rate-limit after only a few requests.

- Searches may be required for the main report, best public offer, and historical offers.
- Do **not** fire those searches in one burst.
- Serialize them.
- Wait briefly between searches.
- If Brave returns **429**, back off before trying the next search.
- If Brave is unavailable, continue with `WebSearch` + `WebFetch`.
- Preserve historical-offer coverage when possible, but never at the cost of bursty request patterns.

### Pacing Rule

When multiple searches are needed, use this pacing. Apply it to Brave searches and also avoid bursting platform `WebSearch` requests:

1. Run the main search.
2. Fetch issuer + secondary pages.
3. Wait about **2 to 5 seconds** before the next search.
4. Run the best-public-offer search.
5. Wait about **2 to 5 seconds** before the historical-offers search.
6. Run the historical-offers search.

If a search returns **429**:

1. Wait about **8 to 15 seconds**.
2. Retry once if the information is important and still missing.
3. If it still fails, continue the report with the best evidence already gathered and mark the affected section accordingly.

### Source Policy

- **Issuer-first for fees/terms/benefits**, but **not issuer-only for welcome offers**.
- Use the issuer page as the baseline truth source for annual fee, earning rates, credits, protections, and restrictions.
- For welcome offers, always compare against approved secondary sources because the best public offer may be broader than the issuer page or the issuer page may not extract cleanly.
- An **approved secondary page** means a URL whose hostname matches one of the approved domains listed below. Do not fetch or cite secondary pages from any other domain.
- **Max 5 secondary sources** from this approved list:
  1. NerdWallet (nerdwallet.com) — preferred
  2. The Points Guy (thepointsguy.com) — preferred
  3. Doctor of Credit (doctorofcredit.com)
  4. Bankrate (bankrate.com)
  5. One Mile at a Time (onemileatatime.com)
  6. Upgraded Points (upgradedpoints.com)
- Prefer **2 to 3 secondary pages** for welcome-offer verification when the issuer page is weak, JS-heavy, stale, or missing offer text.
- **Stop early** once all required sections are covered.
- **Disallowed**: Reddit, Facebook, Instagram, TikTok, X, YouTube, referral links, user forums.

### Issuer Domains (for classifying results, not constraining searches)

| Issuer | Domains |
|---|---|
| American Express | americanexpress.com, aboutamex.com |
| Bank of America | bankofamerica.com |
| Barclays | cards.barclaycardus.com |
| Bilt | bfrrewards.com |
| Capital One | capitalone.com |
| Chase | chase.com, media.chase.com |
| Citi | citi.com, citicards.com |
| Discover | discover.com |
| Robinhood | robinhood.com |
| U.S. Bank | usbank.com |
| Wells Fargo | wellsfargo.com |

## Step 3: Fetch Pages

Pick the top issuer URL and up to 3 secondary URLs (prefer thepointsguy.com, nerdwallet.com, and doctorofcredit.com when present) from the search results. Fetch in parallel with `WebFetch`.

Do not rely on snippets alone for welcome offers.

### URL Safety Rules

- Prefer `WebFetch` for page retrieval. Use `curl` only for the optional Brave Search API calls above, not for arbitrary result URLs.
- Never execute a shell command that interpolates a raw URL taken directly from search results.
- Only fetch URLs when all of the following are true:
  1. scheme is `https`
  2. hostname matches a supported issuer domain or an approved secondary domain from this skill
  3. the URL is being passed to `WebFetch`, not inserted into a shell pipeline
- If a result URL fails those checks, skip it and use the next valid result.

### Welcome Offer Recovery Rules

If the issuer page does **not** expose the welcome offer clearly in fetched text:

1. Use the issuer page for everything else it supports.
2. Use approved secondary sources to identify:
   - the **current public offer**
   - the **best public offer currently visible from approved sources**
3. Prefer consistency across at least 2 approved sources for welcome-offer claims when issuer extraction fails.
4. If the welcome offer is still unresolved after issuer + up to 3 approved secondary pages, mark it **unconfirmed** and say so explicitly.
5. Do **not** pretend the report is complete if the welcome offer is missing.

### Issuer Extraction Caveat

Some issuer pages, especially **American Express**, may be JS-heavy or may not expose the live offer cleanly to simple fetch tools. In those cases, use approved secondary sources for the welcome-offer section while keeping issuer pages as the primary source for fees, terms, and benefit structure.

## Step 4: Best Public Offer Search

After the first fetch pass is complete, run a second search for the best currently available public offer. Use `WebSearch` by default, or Brave if the key is available.

Do not run it immediately after the first search. Follow the pacing rule above.

```bash
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+best+public+offer&count=10" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

Look for elevated offers via CardMatch, incognito, referral links, or specific application URLs. Include the best available public offer in the Welcome Offer section, even if it matches the standard offer.

## Step 5: Historical Offers Search

After another short delay, run a third search for past notable offers. Use `WebSearch` by default, or Brave if the key is available.

Do not burst this search immediately after the best-offer search. Follow the pacing rule above.

```bash
curl -sS "https://api.search.brave.com/res/v1/web/search?q=CARD+NAME+historical+welcome+offers&count=10" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

If results are found, include a compact table of notable past offers with approximate date ranges and amounts in the Welcome Offer section.

If Brave rate-limits this step even after pacing and one retry, continue without historical data and say so in `## 📋 Confidence Notes`. If Brave is unavailable, use `WebSearch` + `WebFetch`.

## Step 6: Required Output Sections

Return compact markdown with these sections in order:

### `## 💰 Fees`
Annual fee, authorized user fee, foreign transaction fee, balance transfer fee, cash advance fee, late fee.

### `## 🎁 Welcome Offer`
Current public offer, best available public offer (if elevated), spend requirement, qualification window, eligibility restrictions, lifetime/family language.

Rules:
- This section is **required**.
- If issuer extraction fails, use approved secondary sources.
- If the exact live offer still cannot be verified, explicitly say: `Could not verify the exact live welcome offer after checking issuer and approved secondary sources.`
- Include a historical offers table only when historical data is actually available.

### `## 📈 Earning Rates`
Base rate, bonus categories with multipliers, caps, point currency.

### `## 🔄 Redemption`
Transfer partners summary, portal options, cash-out rates, minimum redemption.

### `## 🏷️ Credits`
Statement credits, cash-back rebates, and complimentary subscriptions with concrete dollar values only. Each credit with amount, cadence, trigger, and restrictions. Do NOT include enhanced earning rates (e.g., "5x on Lyft"), bonus point multipliers, or anniversary point bonuses — those go in Earning Rates.

### `## ✈️ Travel Benefits`
Lounge access, hotel status, rental car benefits, travel credits, companion fares.

### `## 🛡️ Protections`
Purchase protection, extended warranty, return protection, cell phone protection, fraud protections.

### `## ⚙️ Account Mechanics`
Virtual cards, authorized user handling, app capabilities, autopay notes.

### `## ✅ Eligibility`
Issuer family rules, known restriction language (e.g., Chase 5/24, Amex lifetime language).

### `## 🧭 Strategy`
Downgrade paths, no-fee fallback, ecosystem role, keeper value after year one.

### `## 👤 Who Is This Card For?`
Describe the ideal cardholder profile (spending habits, travel frequency, lifestyle), who benefits most from this card's specific strengths, and who should look elsewhere and why.

### `## 🃏 Similar Cards`
4-6 competing cards with annual fee and a one-line summary of why each is comparable.

### `## 📋 Confidence Notes`
Flag any uncertain, unconfirmed, or conflicting claims.

### `## 🔗 Sources`
Numbered list of URLs fetched, as markdown hyperlinks with short "Site - Topic" labels.

## Output Rules

- Use one emoji per section heading.
- When listing credits, fees, or any monetary amounts, sort from highest to lowest dollar value.
- Use numbered lists for list-heavy sections.
- Keep content to condensed facts — no prose padding.
- Omit the Card Identity section when the match is confident.
- Do not include YAML blocks in user-facing output.
- End every report with a `## 🔗 Sources` section listing each URL fetched during research as a markdown hyperlink with a short "Site - Topic" label, e.g. `[Chase - Sapphire Preferred](https://...)`.
- Do not show a "Why It Matters" section.
- If the welcome offer is unresolved, say that plainly in both `## 🎁 Welcome Offer` and `## 📋 Confidence Notes`.
- Do not silently downgrade to an incomplete report.

## Confidence Definitions

- **confirmed**: supported by issuer terms or multiple approved sources without disagreement
- **unconfirmed**: plausible but not fully resolved from approved sources
- **conflicting**: approved sources disagree on a material fact

Every report must include a `## 📋 Confidence Notes` section. Keep notes short and tied to concrete uncertainties.

## Practical Retrieval Strategy

Use this order of operations:

1. Resolve the exact card.
2. Run the main search.
3. Fetch the issuer page.
4. Fetch up to 3 approved secondary pages.
5. Wait briefly.
6. Run the best-public-offer search.
7. Wait briefly.
8. Run the historical-offers search.
9. Resolve the welcome offer from issuer + approved sources.
10. Compile the report with confidence notes for anything rate-limited or unresolved.

This skill should optimize for **accurate current answer first**, while preserving best-offer and historical-offer coverage through sane pacing rather than bursty search behavior.
