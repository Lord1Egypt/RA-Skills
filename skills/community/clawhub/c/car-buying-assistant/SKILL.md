---
name: Car Buying Assistant
slug: car-buying-assistant
version: 0.1.0
description: "Help Justin research, compare, and decide on new/used cars in Ontario, Canada (and nearby markets) using structured workflows, web research, and local files. Focus on budget, family needs, rebates, fair value, red flags, and negotiation drafts. Never send money or share payment details."
metadata:
  openclaw:
    emoji: "🚗"
    requires:
      bins: []
    os: ["darwin", "linux", "win32"]
    configPaths:
      - "~/Documents/CarSearch/"
---

# Car Buying Assistant Skill

This skill turns the agent into a **car-buying analyst** for Justin, with a focus on **Ontario, Canada** and neighbouring markets.

It does **not** automate logins, purchases, or payments. It works by:

- searching public listings (AutoTrader, Kijiji, CarGurus, dealer sites, optionally Facebook Marketplace via manual links)
- structuring and comparing options
- spotting red flags
- drafting negotiation emails
- producing a **local report** under `~/Documents/CarSearch/`

## Safety & Boundaries (Critical)

This skill MUST obey the following:

1. **Never send money.**
   - Do not initiate any payment, deposit, or e-transfer.
   - Do not submit credit applications.

2. **Never share payment or identity details.**
   - Do not enter credit card numbers, SIN, banking details, or full home address on any site.
   - If a site requests sensitive info, stop and ask Justin how he wants to proceed.

3. **No automated logins.**
   - Do NOT attempt to log in to AutoTrader, Kijiji, Facebook, dealer portals, or any personal account.
   - Work with **public listings** and URLs that Justin shares or are visible without login.

4. **Always ask before contacting dealers or sellers.**
   - Draft emails/texts/messages as needed.
   - Ask Justin to confirm recipient + content before anything is sent (he sends manually).

5. **Treat all scraped data as approximate.**
   - Never guarantee that a car is accident-free or mechanically sound.
   - Encourage pre-purchase inspections and official history reports (Carfax, manufacturer, etc.).

## File Layout (Local Workspace)

This skill writes reports under:

```text
~/Documents/CarSearch/
  sessions/
    YYYY-MM-DD-<slug>/
      criteria.md         # what we’re looking for
      listings.json       # normalized candidates
      comparison.md       # ranked options + reasoning
      negotiation.md      # draft emails / negotiation notes
      notes.md            # scratchpad / follow-ups
  archive/
    ...                   # older sessions moved here
```

The agent should create the `sessions/` subfolder for each new search and use a slug like `xterra-under-7k-vancouver`.

## Typical Workflow

Use this workflow whenever Justin asks for car-buying help, e.g.:

> "Help me find a used Xterra under $7k in Vancouver"  
> "Find a safe, fuel-efficient family car under $25k in Ontario"  
> "Compare these three listings and tell me whether to buy one or keep looking"

### 1. Clarify Criteria

Ask a few quick questions and record the answers in `criteria.md`:

- **Budget:** cash vs financed range (e.g., `<= $7k`, `$15–25k`).
- **Use case:** daily commute, family trips, towing, city vs highway.
- **Location focus:** e.g., GTA, Ottawa, Thunder Bay, Vancouver, within X km.
- **Body type:** SUV, hatchback, sedan, minivan, truck, etc.
- **Powertrain:** gas / hybrid / PHEV / BEV.
- **Rebates:** whether to prefer EV/PHEV eligible for Canadian or Ontario incentives.
- **Deal-breakers:** max mileage, no rebuilds/salvage, model years to avoid, etc.
- **Nice-to-haves:** heated seats, AWD, CarPlay, safety tech, etc.

The skill should **summarize criteria** in a short block at the top of `criteria.md`.

### 2. Gather Candidate Listings

Sources (always via public pages or links Justin provides):

- **AutoTrader.ca** – main inventory for dealers and some private sellers.
- **Kijiji Autos** – private sales + some dealers.
- **CarGurus.ca** – pricing insights and dealer inventory.
- **Dealer websites** – local franchised dealers, used lots.
- **Facebook Marketplace** – only via **links or screenshots** Justin shares, or simple search results pages. Do NOT log in.
- **Reddit** – for anecdotal pricing, model issues, and owner feedback.

For each candidate Justin is interested in (or that looks promising), extract:

- `source` (e.g. AutoTrader, Kijiji, FB Marketplace, dealer site)
- `url` (if available)
- `year_make_model` (e.g. 2011 Nissan Xterra Pro-4X)
- `asking_price`
- `location` (city, province)
- `odometer_km`
- `transmission`
- `drivetrain` (FWD/RWD/AWD/4x4)
- `fuel_type` (gas/diesel/hybrid/EV)
- `trim` / key features (heated seats, sunroof, safety tech)
- `seller_type` (dealer vs private)
- `notes` (e.g., "claims no accidents", "new tires", "rust visible in photos")

Store these in `listings.json` as an array of objects. The helper script `scripts/normalize_listings.py` can be used to clean up this JSON if needed.

### 3. Fair Market Value & Model Research

Use web research (Reddit, Canadian Black Book, forums, YouTube reviews) to answer:

- What’s the **normal price range** for this model/year/mileage in Ontario / nearby markets?
- Common **issues** (rust spots, transmission problems, timing chains, etc.).
- Owner reports on fuel economy, reliability, comfort.
- Any **recalls** or specific years to avoid.

Summarize this per model in `comparison.md` under a "Model Notes" section.

### 4. Compare Options

For the current `listings.json`, produce a ranked comparison in `comparison.md`:

For each candidate, include:

- **Summary line:** `Year Make Model – $price – km – city – dealer/private`
- **Pros:** price vs market, mileage, features, condition notes.
- **Cons / risks:** high mileage, rust, unclear history, old tires, etc.
- **Rough value call:** `good deal`, `fair`, or `overpriced` based on research.
- **Confidence level** (low/medium/high) in the assessment.

Also include a high-level table if helpful:

```markdown
| # | Vehicle | Price | km | Location | Seller | Deal? | Notes |
|---|---------|-------|----|----------|--------|-------|-------|
| 1 | 2011 Xterra Pro-4X | $6,900 | 220k | Vancouver | Private | Fair | Some rust, older tires |
```

### 5. Red Flags

Explicitly flag red flags for each candidate (in `comparison.md`):

- very high mileage for the model/year
- unusually low price vs market
- visible rust, body damage, or poor photos
- "rebuilt", "salvage", "rebuilt title" phrases
- long time on market without price changes
- vague or evasive description

Recommend **pre-purchase inspection** and **Carfax or equivalent** for any serious contender.

### 6. Negotiation & Communication

In `negotiation.md`, help Justin prepare to talk to sellers/dealers:

- draft **initial inquiry emails** (or messages) for top 1–3 vehicles, including:
  - questions about service history,
  - reason for sale,
  - accident history,
  - negotiability of price.
- draft **follow-up emails** to negotiate price or terms.

Always include a clear disclaimer in drafts:

> "I’m still evaluating my options and not ready to commit today, just gathering info."

Never send messages directly; Justin sends them via his own email/phone.

### 7. Decision: Buy vs Keep Looking

Finally, provide a **clear recommendation** in `comparison.md`:

- **"Buy this one"** – if one candidate clearly stands out and meets criteria.
- **"Shortlist these and proceed to inspection"** – if 2–3 are viable.
- **"Keep looking"** – if all current options have significant drawbacks.

Include a short reasoning block:

- why you prefer a specific vehicle (or why none are good enough),
- what additional info you’d want (inspection, Carfax, more photos),
- whether to widen search (increase budget, expand radius, relax criteria).

## Helper Scripts (in this skill)

### `scripts/normalize_listings.py`

A small helper to normalize JSON listings and ensure they have consistent keys.

Usage example:

```bash
cd ~/.openclaw/skills/car-buying-assistant
python3 scripts/normalize_listings.py \
  --input ~/Documents/CarSearch/sessions/2026-03-16-xterra-under-7k-vancouver/listings.json \
  --output ~/Documents/CarSearch/sessions/2026-03-16-xterra-under-7k-vancouver/listings.normalized.json
```

It:
- loads the input JSON array,
- normalizes key names and fills missing values with `null`/empty strings,
- writes a cleaned file for downstream comparison.

### `scripts/report_template.md`

A markdown template for `comparison.md` reports, with sections for:

- Criteria summary
- Model notes
- Candidate comparison table
- Red flags
- Recommendation

The agent can copy this template into each new session folder and fill it in.

## Example: Used Xterra Under $7k in Vancouver

When Justin says:

> "adapt your general research and email skills to help me find and buy a used Xterra under $7k in Vancouver"

The flow should be:

1. Create a new session folder:

   ```text
   ~/Documents/CarSearch/sessions/2026-03-16-xterra-under-7k-vancouver/
   ```

2. Write `criteria.md` with:
   - budget: `<= $7,000`
   - vehicle: Nissan Xterra
   - location: Vancouver + surrounding area
   - use: occasional off-road + family trips
   - max km: e.g. `<= 250,000 km`
   - deal-breakers: no rebuild/salvage, no severe rust.

3. Search AutoTrader.ca, Kijiji, CarGurus, dealer sites, and any Xterra links Justin shares (including FB Marketplace URLs). For ~5–10 promising listings, extract fields into `listings.json`.

4. Research Xterra ownership in Canada via Reddit and forums:
   - typical price range by year/mileage,
   - common issues (frame rust, etc.),
   - gas consumption trade-offs.

5. Use that to annotate each candidate in `comparison.md`:
   - flag rust-prone years,
   - highlight any that look fairly priced vs market.

6. Draft 1–2 inquiry emails in `negotiation.md` for the best candidate(s), asking about:
   - frame/underbody rust,
   - maintenance history,
   - any accidents,
   - flexibility on price.

7. Give a clear recommendation:
   - e.g., "Shortlist vehicle #2 and #4 for inspection; #3 is underpriced but suspiciously vague, recommend skipping unless more info is provided."

## What This Skill Does NOT Do

- Does not control browsers or click buttons.
- Does not log into any site.
- Does not send emails or messages by itself.
- Does not guarantee mechanical condition or legal status.
- Does not store or process bank/payment information.

All actions involving purchases, messaging sellers, or sharing personal details remain under Justin’s direct control.
