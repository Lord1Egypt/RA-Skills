# Delta Reserve Offer Staleness - Anchoring Failure (Aug 27, 2026)

## What happened

User asked for a full report on the Delta SkyMiles Reserve personal card. The report's
Welcome Offer section claimed the live offer was "up to 125,000 miles (100k/$6k + 25k/$3k)"
based on TPG's "June 2026 to now" tracker row. The user flagged that a new offer with
round-trip flight certificates existed. Investigation found the live offer (announced
same day via Doctor of Credit update 8/27/26) was actually:

- 50,000 miles + 2 round-trip Delta Comfort+ flight certificates after $10,000 spend

The 125k structure had expired 7/15/26 (it was a limited-time offer from the June 2026
Delta/Amex 30th-anniversary refresh).

## Root causes

1. **Generic search query.** `Amex Delta SkyMiles Reserve review welcome offer 2026`
   surfaced slow-updating SEO pages (pointsnav, roamingcactus, Upgraded Points) quoting
   stale tiers (70k, 100k@$5k). A structure-keyword query
   (`round-trip flight certificates`) surfaced the DoC page updated that same day.

2. **Trusted a "current" label without checking expiry.** TPG's tracker said "June 2026
   to now," but the Delta newsroom press release showed that structure was a limited-time
   offer expiring 7/15/26. No valid-through check was done.

3. **Anchoring / rationalizing away the correct answer.** The TPG review fetched in the
   FIRST pass stated the live cert offer verbatim ("two domestic round-trip Delta Comfort
   Flight Certificates and 50,000 bonus miles after spending $10,000"). Because it
   contradicted the 125k tracker, it was filed as a "historical variant" instead of
   treated as a conflict. The freshest in-body statement lost to the cached tracker table.

## Fixes applied to this skill

- Search Query Design section: run generic + offer-structure + freshness-targeted queries;
  check valid-through dates; prefer pages updated in last ~30 days.
- Offer Recency & Conflict Resolution section: in-body offer beats tracker table;
  freshest-dated source wins; check issuer newsroom; never rationalize a conflicting
  offer into "historical" without a newer source confirming it.
- Workflow order now includes issuer-newsroom fetch and recency resolution before compiling.

## Checklist to prevent recurrence

- [ ] Today's date noted before any search
- [ ] Structure-keyword query run (certificate / round-trip / statement credit / companion)
- [ ] DoC checked for live/expired roundup posts
- [ ] Every offer claim checked for valid-through date
- [ ] In-body offer vs tracker-table conflicts resolved in favor of freshest in-body
- [ ] Issuer newsroom checked for recent card-refresh announcement
- [ ] Confidence Notes state which source was treated as live and why
