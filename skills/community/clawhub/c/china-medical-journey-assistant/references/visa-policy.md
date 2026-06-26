# Visa Policy

Use this policy only for **mainland China entry** questions. Do not apply it to Hong Kong or Macau.

## Allowed Entry-Route Conclusions

Visa answers may return only one of these states:

- `Confirmed visa-free`
- `Confirmed not covered by visa-free / transit policy, check visa route`
- `No sufficient official confirmation found`

Do not use soft language such as `likely`, `probably`, or `大概率`.

## Decision Order

1. Determine whether the user is asking about entry eligibility or about visa application mechanics.
2. Check **ordinary visa-free entry** first.
3. Check **240-hour visa-free transit** only if the itinerary is transit-relevant.
4. Only after those branches are ruled out or not confirmed, check the regular visa route and category/application process.

`S2` is never the default answer. It is only a downstream category to review when a regular-visa path is needed.

## Ordinary Visa-Free Verification Checklist

You may return `Confirmed visa-free` only when current official evidence confirms all required elements:

- nationality
- ordinary passport status
- allowed purpose of visit
- allowed stay duration
- policy validity period

If any element is missing or not clearly supported by current official evidence, do not infer eligibility. Return `No sufficient official confirmation found`.

## 240-Hour Transit Verification Checklist

Check this branch only when transit logic is actually relevant. You may treat the user as covered by the transit route only when current official evidence supports:

- eligible nationality
- onward itinerary to a third country or region
- port eligibility
- region or stay restrictions

If any of those elements cannot be confirmed, return `No sufficient official confirmation found` unless the ordinary visa-free route was already confirmed.

## Source Priority

For visa questions, use sources in this order:

1. PRC State Council or official government policy pages
2. Ministry of Foreign Affairs visa-free or consular pages
3. National Immigration Administration pages for transit or border-entry rules
4. Visa-center or embassy/consulate pages for local application flow after eligibility is resolved

Visa-center pages are for category and process lookup, not for first-pass visa-free eligibility judgment.

## Output Minimum

A visa answer should include:

- `Entry route`
- `Official basis checked`
- `What is still missing`
- `Next official step`

Keep it short. Do not turn this into a long policy essay unless the user asks for detail.
