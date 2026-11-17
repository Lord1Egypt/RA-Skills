---
name: domain-cma-valuation
description: Apply the substitution principle to position a compound or keyword-plus-modifier domain within the current asking-price market. Build a Comparative Market Analysis from verified, currently for-sale domains that are credible substitutes in the same value-bearing keyword market, then adjust for TLD, keyword position, length, modifier quality, and linguistic coherence. Use when a user asks what such a domain is worth, wants a competitive listing-positioning range, or needs current replacement-market context for buying or selling. Do not use historical sale prices to set or calibrate the range. Treat exact single-keyword domains, pure short domains, coined names without a shared keyword market, fixed-target buyer situations, and domains with active operating websites as out of scope. Do not use for technical analysis (use domain-analyze) or availability checks (use available).
---

# Domain Substitution-Market CMA

**What this does:** identifies the part of a domain that carries its independent market value, builds a pool of credible substitutes from domains currently offered for sale in that same keyword market, and positions the target against what a buyer can purchase now. It estimates current competitive listing position and replacement cost, not a completed-sale price, official appraisal, or investment outcome.

The core model is the **principle of substitution**: a buyer with a flexible naming goal normally has little reason to pay materially more for the target than for a currently purchasable domain that serves the same naming purpose and is equal or better on the relevant attributes. The analysis therefore starts with current alternatives, not sparse historical transactions. A buyer who must obtain the exact string for a fixed identity, brand, acronym, or strategic reason is not acting in a substitutable market, so this model does not estimate that buyer-specific value.

The real-estate CMA analogy is deliberate: the value-bearing keyword is the neighborhood; TLD, keyword position, length, modifier quality, pronunciation, and semantic coherence are property features. Two domains that share a construction pattern but not the value-bearing keyword are not in the same neighborhood.

Example: for `openrt.com`, if `rt` is the intended value-bearing keyword and `open` is the modifier, compare current `rt*.com` and `*rt.com` listings in which `rt` is a real token. Do not use `opengt.com` merely because both names follow `open` + two letters. A historical price for `opengt.com` says nothing reliable about the current `rt` keyword market.

## Scope

Use this model for compound words, industry word + modifier names, acronym/keyword + modifier names, and prefix/suffix combinations where a primary value-bearing keyword and a credible current substitute market can be identified.

Treat these as out of scope:

- An exact single-keyword domain, where the value rests on the unmodified word + TLD rather than a substitutable modifier relationship.
- A pure short domain (for example a bare 2L / 3L, short numeric string, or short acronym) whose value rests mainly on scarcity, character quality, or many possible buyer-specific meanings rather than one defensible keyword market. A short keyword + modifier construction remains in scope when its value center and substitutes are clear.
- A coined or invented name without an independently shared keyword market.
- A fixed-target situation in which the relevant buyer must obtain the exact string and would not accept a substitute; the model cannot estimate that buyer-specific premium.
- A domain with an active operating website, where business assets, traffic, revenue, customers, and goodwill may materially affect value.
- A domain whose apparent value depends mainly on an existing brand, trademark owner, or competitor.
- A name whose value-bearing keyword or credible substitute set cannot be identified well enough to form a defensible current market.

For an out-of-scope target, explain which condition failed and stop the CMA. For an active website, state that an asset-inclusive business valuation would require operating data not covered here. For an exact single-keyword, pure short, coined, fixed-target, or otherwise exceptional domain, provide only directly observed market evidence if the user asks; do not manufacture a substitution-based range.

## Data interfaces

DomainKits MCP supplies discovery evidence through the tools below; it is not the complete CMA engine. Host-provided browser or WebFetch access verifies the original marketplace pages. Equivalent providers are acceptable. Never assume that an MCP listing contains listing type, listing age, or price-change history when its actual payload does not return those fields. Mark unavailable fields `Not Provided` and continue only when the remaining evidence can still support the model.

- Current comparable for-sale listing leads, DomainKits: `market` / `aged` / `active`
- Cross-TLD registration breadth for the value-bearing keyword, DomainKits: `tld_check`
- Keyword registration activity as supporting context, DomainKits: `keywords_trends`
- Safe Browsing / malware status before fetching the target domain, DomainKits: `safety`
- Web access or browser automation for verifying original marketplace listings
- Current foreign-exchange reference when prices must be normalized across currencies

Optional follow-up capability, used only if the user asks: `monitor` for price tracking.

## Core model

### 1. Identify the value-bearing keyword

Decompose the domain into:

- **Primary value-bearing keyword:** the token whose meaning, audience, industry use, or acronym market gives the name independent relevance.
- **Modifier:** a prefix, suffix, verb, descriptor, or other token that changes the presentation of the keyword.
- **TLD:** a separate pricing dimension, not part of the keyword.

Use the user's intended meaning when provided. Do not assume the first, last, longest, or dictionary token is automatically the value center. If two interpretations would create materially different comparable markets, ask one concise question before continuing.

For short acronyms and concatenated strings, exclude accidental substring matches. A domain contains the keyword only when the keyword is plausibly functioning as an independent token in that name.

Also establish the substitution frame: the target's intended naming purpose, which characteristics a normal buyer in that market must preserve, and whether the user has disclosed a non-substitutable need for the exact string. Do not confuse a user's interest in valuing one target with proof that every buyer must have that target.

### 2. Build the current substitute market

Use only active for-sale listings. Search the value-bearing keyword at both the start and end of the label, then inspect each result manually enough to confirm that it belongs to the same keyword market and could plausibly serve the same naming purpose.

Rank comparables by:

1. Same value-bearing keyword, same TLD, and same keyword position or grammatical role.
2. Same value-bearing keyword and same TLD, with a different but comparable position or modifier.
3. Same value-bearing keyword on another TLD, used only as secondary context and never mixed directly into the primary-TLD price range.

Exclude:

- Domains that share only length, prefix, suffix, word count, or construction pattern.
- Domains built around a different core keyword, even when their surface structure is identical.
- Accidental substring matches.
- Listings whose current status or asking price cannot be sourced.
- Obvious brand-dependent or trademark-dependent names.

Synonyms and adjacent concepts are not substitutes for the exact keyword market when the buyer's direction requires that keyword. Use them only as separately labeled secondary context when the exact-keyword pool is thin; never let them set the primary range. If the user's naming goal is explicitly flexible enough to accept a different keyword, show those names as a separate broader-alternatives layer rather than mixing them into the same-keyword CMA.

### 3. Position the target within current asks

Use the verified current asking-price distribution, not historical transactions. Show the full observed range, the central cluster, and any obvious outliers rather than averaging unlike assets together.

Identify the **closest substitute set** and the **equal-or-better substitution frontier**: the lowest currently verified asking prices among substitutes that are reasonably equal to or better than the target for the stated naming purpose. This frontier is a competitive replacement-price constraint, not a guaranteed sale price or a mechanical hard cap. A target positioned above a cheaper equal-or-better substitute requires a named, evidence-based superiority; otherwise the current substitute market does not support that premium.

Position the target relative to the comparables using:

- TLD, with the target TLD compared primarily against the same TLD.
- Keyword position and role.
- Length and word count.
- Modifier quality and commercial usefulness.
- Pronunciation, spelling, and semantic coherence.
- Cross-language or negative-meaning risk.
- Listing freshness and any visible price-reduction history.

Do not invent fixed percentage adjustments. Explain each relative premium or discount from named comparable differences.

`tld_check` and `keywords_trends` are supporting context only. They can describe keyword breadth or current registration activity, but they do not set the price range and must not be converted mechanically into a premium.

## Historical-price boundary

Historical sale prices do not enter the comparable pool, do not calibrate the asking-price range, and do not create an expected transaction range. A past sale occurred in a different market moment and may reflect a unique buyer, negotiation, use case, or information set.

If the user explicitly asks for historical sales, present them in a separate appendix as background only. State whether each historical item shares the same value-bearing keyword. Do not alter the current listing-positioning range because of it.

## Evidence discipline

- **Asking price is seller intent, not transaction proof.** Never describe the resulting range as a certain sale price or completed-market value.
- **Verify current status.** Check each retained comparable against its original marketplace listing when possible and record source and observation date.
- **Label fallback evidence.** If the original page is blocked, retain a current tool-reported listing only as `marketplace page not verified`; do not call it fully verified or count it toward the minimum verified-comparable rule.
- **Do not invent listing metadata.** Obtain listing type, listing age, and price-reduction history from the original marketplace or another named current source. If the page and tool do not provide a field, write `Not Provided`; do not infer it from the asking price, search snippet, or first observation in this report.
- **Deduplicate.** Count the same domain once even when it appears on several marketplaces; record differing asks rather than treating them as separate comparables.
- **Separate listing types.** Distinguish BIN, minimum offer, current auction bid, and lease-to-own. A monthly lease payment is not the total asking price, and a current bid is not a completed sale.
- **Normalize currency carefully.** Preserve original currency. If prices must be combined, convert with a current FX source and date. If FX data is unavailable, keep currencies separate and do not calculate a combined range.
- **Record listing dynamics when visible.** Capture listing age and price-reduction history; mark either Not Provided when unavailable.
- **Absence is not value evidence.** No comparable found means insufficient current market evidence, not low value.
- Classify findings as Fact, Inference, or Unknown. Cite source and observation date for every external price.

## Workflow

Use information already supplied by the user. Ask at most one question, and only when ambiguity about the value-bearing keyword or substitution frame would materially change the current substitute market.

1. **Check scope, substitutability, and safety.** Determine whether the target is a compositional name with a defensible substitute market, rather than an exact single-keyword, pure short, coined, fixed-target, brand-dependent, or asset-inclusive case. Run `safety` before fetching the target. Never fetch a domain flagged as malicious, phishing, or malware-hosting. For a clean or unavailable safety result, inspect the root domain to distinguish an active business from parking, a for-sale lander, login wall, TLS failure, or unreachable site. Stop if the target is out of scope.

2. **Identify the value center and substitution frame.** Record the primary value-bearing keyword, modifier, TLD, intended meaning, naming purpose, characteristics that substitutes must preserve, and any ambiguity. Do not continue with an unresolved material ambiguity.

3. **Build the listing pool.** Query `market` with `status=forsale`, then use `aged` with `has_sale=true` and `active` with `status=forsale` as additional sources. Search the exact keyword at the start and end. Do not generate pattern-only substitutes.

4. **Verify and classify.** Verify original listings where possible, deduplicate, label listing type and verification status, normalize currency when possible, and assign each retained item to comparable tier 1, 2, or 3.

5. **Apply the sufficiency rule.** Use at least three current tier-1 or tier-2 listings whose current status and asking price were verified from the original marketplace or another named current source to produce a primary positioning range. MCP-only leads labeled `marketplace page not verified` may be shown as fallback evidence but do not satisfy this minimum. With fewer than three verified comparables, present the observed listings and state `Insufficient current comparable market`; do not manufacture a range. Tier-3 or synonym evidence cannot satisfy this minimum.

6. **Position the target.** Identify the closest substitutes and equal-or-better substitution frontier, then describe where the target belongs within the current same-keyword market and why. Produce a listing-positioning range only when the sufficiency rule is met. Never produce an expected transaction range.

7. **Report** using the fixed structure below. Never recommend whether the user should buy, sell, or accept an offer.

## Output structure

1. **Scope, value center, and substitution frame:** target domain, primary value-bearing keyword, modifier, TLD, intended meaning, naming purpose, characteristics a substitute must preserve, and any ambiguity resolved.
2. **Current substitute listings table:** domain, why it is a credible substitute, substitution strength and quality relative to the target, keyword match and position, modifier, TLD, comparable tier, listing type, asking price in original currency, normalized price and FX source/date when converted, verification status, marketplace, listing age, price-reduction history, source, and observation date.
3. **Excluded false comparables:** materially tempting exclusions and why they were rejected, especially pattern-only or different-keyword names.
4. **Current keyword-market asking distribution:** retained comparable count, full observed range, central cluster, outliers, and coverage limits.
5. **Closest substitutes and substitution frontier:** the closest currently purchasable alternatives, the lowest verified asks among equal-or-better substitutes, and the named differences that support or reject a premium for the target. State that this is a competitive replacement-price constraint, not a guaranteed transaction ceiling.
6. **Target listing-positioning range:** only when at least three tier-1 or tier-2 current listings exist; explain the target's relative position using named differences and the substitution frontier.
7. **Supporting keyword signals:** cross-TLD breadth and registration activity, clearly labeled as non-pricing context.
8. **Confidence and limitations:** verification gaps, thin market, stale listings, unavailable marketplaces, currency limitations, brand-risk boundary, and any buyer-specific value the substitution model cannot measure.
9. **Sources and observation dates:** one source trail for every retained asking price and supporting factual claim.
10. **Compliance statement:** use the fixed text below.

Compliance statement: "This is a substitution-based current listing analysis for reference only, not an official appraisal or investment advice. It positions the target against verified seller asking prices for currently purchasable domains in the same value-bearing keyword market. The substitution frontier is a competitive replacement-price constraint, not a guaranteed transaction ceiling. Asking prices are seller intent and do not prove that a domain can transact at those prices. Historical sale prices are not used to set or calibrate the range, and buyer-specific value for an exact target is outside this model."

## Key principles

- Apply the principle of substitution: position the target against what a flexible buyer can purchase now for the same naming purpose.
- The value-bearing keyword defines the primary substitute neighborhood; construction pattern alone never does.
- Use current verified same-keyword for-sale listings as the pricing evidence.
- Identify the closest substitutes and equal-or-better substitution frontier; require named superiority before supporting a premium over a cheaper equal-or-better option.
- Do not apply this model to exact single-keyword, pure short, coined, fixed-target, brand-dependent, or asset-inclusive cases that lack a defensible substitute market.
- Historical sales never set, calibrate, or constrain the range.
- Prefer same-keyword, same-TLD, same-role comparables; keep other TLDs and synonyms as separately labeled secondary context.
- Exclude accidental substring matches, pattern-only analogies, and brand-dependent names.
- Asking prices support listing position, not an expected transaction price.
- Require at least three currently verified tier-1 or tier-2 comparables; MCP-only unverified listing leads do not satisfy the minimum. Otherwise report insufficient evidence without a range.
- Verify, deduplicate, label listing type, preserve provenance, and timestamp every price.
- Do not recommend buying, selling, or accepting an offer.
