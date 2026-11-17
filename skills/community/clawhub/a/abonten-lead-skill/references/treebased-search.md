# TreeBased Search

TreeBased search is a bounded evidence graph for resolving a business from incomplete offline advertising. It is not a method for uncovering private individuals.

## Branches

Start from one or more observed seeds:

business text / phone / URL / handle / location

Expand only as needed:

- **Identity:** exact name with city, neighborhood, country, and spelling variants.
- **Phone:** exact number, formatted variants, WhatsApp/business listings, and references tied to the same location.
- **Official footprint:** website, map/business listing, company page, service pages, contact page, and official social profiles.
- **People and roles:** owner, founder, director, manager, or other decision-maker named on an official or credible professional source.
- **Social:** official page first; then public professional profiles that clearly connect the person to the business.
- **Need/fit:** evidence such as an outdated site, missing booking/contact path, active offline promotion with a weak digital presence, or a stated growth/marketing need.
- **Corroboration:** a second independent source for identity, role, or contact details.

Do not expand every branch mechanically. Follow the branch most likely to resolve the next missing field.

## Search order

1. Search the exact observed business name in quotes with the observed location.
2. Search the exact phone number and a normalized variant, without inventing digits.
3. Search any observed domain, handle, slogan, or distinctive offer with the business name.
4. Open the strongest official result and collect only claims it actually supports.
5. Search a named person with the confirmed business and role.
6. Cross-check the role and contact path against an independent public source.

If a search result conflicts with the poster, keep both values and mark the conflict. Do not choose the more convenient result.

## Evidence ledger

For each researched field, record:

- claim — the fact being asserted;
- value — exact value as published;
- source_url — direct page URL;
- source_type — official, professional, directory, registry, news, or other;
- accessed_at — date of access;
- confidence — confirmed, probable, or unresolved;
- notes — why the source connects the value to this business.

Use confirmed when an official source supports the claim or two independent credible public sources agree. Use probable for one credible but non-authoritative source. Use unresolved for weak, stale, ambiguous, or conflicting evidence.

## Contact handling

Keep these categories separate:

- general_business — the number or inbox printed on the sign or published on the business's contact page;
- role_based_business — a business email or business phone publicly associated with a named owner/executive/manager;
- professional_social — an official business account or a public professional profile that clearly represents the person's business role.

A CEO/founder title must be explicitly supported. Do not infer ownership from a surname, profile photo, or a search snippet. Do not guess email formats, scrape behind a login, use data brokers, or store personal addresses, family details, or unrelated personal phone numbers.

## Need and fit signals

Record the evidence before the interpretation:

- **Observed:** what the poster or sign visibly says.
- **Verified:** what a cited public source confirms.
- **Hypothesis:** what the evidence may imply for the user's offer.

For example, an offline promotion plus an outdated website may support the hypothesis “possible digital conversion opportunity.” It does not prove the business wants help or can afford it.

## Stop conditions

Stop a lead's research when any of these is true:

- identity is confirmed and at least one suitable public business contact is verified;
- a decision-maker is not discoverable after the targeted branches were tried;
- two consecutive branches add no new evidence;
- the normal budget of 6–10 targeted queries or about five minutes per lead is reached.

Report the stopping reason. Never fill a missing field with a guess just to make the row look complete.
