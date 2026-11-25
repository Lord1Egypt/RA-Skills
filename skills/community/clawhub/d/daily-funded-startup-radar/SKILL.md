---
name: daily-funded-startup-radar
description: Daily briefing of startups and funds that just raised private money, built from new SEC Form D filings. Use when the user wants a funded-startup radar, alerts on new fund launches, or a daily/weekly digest of companies raising under Regulation D (Rule 506(b), 506(c), 504). Runs the magnova/sec-form-d-monitor Actor through the Apify plugin for OpenClaw; each filing record costs $0.01 on the user's own Apify account, empty days are free.
version: 1.0.0
homepage: https://apify.com/magnova/sec-form-d-monitor
metadata:
  openclaw:
    requires:
      env:
        - APIFY_API_TOKEN
---

# Daily Funded Startup Radar

Turn new SEC Form D filings into a short daily briefing: which
companies and funds just raised private money, how much, and where.
Form D is the notice issuers file with the SEC when they sell
securities under Regulation D — startups raising a priced round or
a SAFE, new hedge/VC/PE and real-estate funds, and other private
placements. Filings are public data on SEC EDGAR.

## Prerequisites

1. The Apify plugin for OpenClaw is installed and allowlisted:
   `openclaw plugins install @apify/apify-openclaw-plugin`
2. `APIFY_API_TOKEN` holds the user's own Apify API token. All
   runs bill to that account.
3. You call Actors through the plugin's `apify` tool, using its
   two-phase pattern: `start` (returns a runId), then `collect`
   (returns the results when the run finishes).

If the plugin or token is missing, stop and tell the user exactly
what to install or set. Do not scrape EDGAR yourself and do not
substitute another data source.

**Cost, stated plainly:** the Actor charges $0.01 per filing
record delivered, no start fee, and a day with no matching filings
costs $0. A heavy day capped at 200 records costs at most $2.00.

## Setup (first run only)

Ask the user once, then save the answers in the state file:

- **Minimum amount sold** — ignore raises smaller than this
  (default 0 = everything; $1,000,000 is a common filter).
- **States** — optional two-letter codes, e.g. CA, NY, TX
  (default: all).
- **Industry groups** — optional, using the Form D industry
  group names (default: all).
- **Exemptions** — optional subset of 506b / 506c / 504
  (default: all).

## State

Keep one JSON file at `state/daily-funded-startup-radar.json`
in the workspace:

```json
{
  "lastRunDate": "2026-11-17",
  "seenAccessionNumbers": ["0001234567-26-000001"],
  "preferences": { "minAmountSold": 0, "states": [], "industryGroups": [], "exemptions": [] }
}
```

Keep at most the last 2,000 accession numbers; the filedAfter
cursor is the primary dedupe, the list is the backstop.

## Daily procedure

1. Read the state file. If none exists, do Setup, then run with
   `lastNDays: 7` as a one-time starter digest.
2. Start the Actor with the `apify` tool:
   - actorId: `magnova~sec-form-d-monitor`
   - input: `filedAfter` = the day after `lastRunDate`,
     `maxResults`: 200, plus the saved preference filters
     (`minAmountSold`, `states`, `industryGroups`, `exemptions`)
     when set.
3. Collect the results. Ignore rows whose `recordType` is not a
   filing (the run's SUMMARY and ERROR rows are not filings).
4. Drop any filing whose `accessionNumber` is already in
   `seenAccessionNumbers`.
5. Sort what remains by `totalAmountSold`, largest first, and
   write the briefing (format below). Cap the briefing at the
   top 15; if more matched, end with the total count and offer
   the full list as a file.
6. Update the state file: append the new accession numbers and
   set `lastRunDate` to today — only after the briefing has
   been delivered. If the run failed, leave the state untouched
   so the next run retries the same window.

## Briefing format

```
☀️ Funded Startup Radar — <date>
<N> new Form D filings matched (≥ $<minAmountSold> sold).

1. <issuerName> — <issuerCity>, <issuerState>
   Raised $<totalAmountSold> of $<totalOfferingAmount> · <industryGroup> · Rule <506(b)/506(c)/504>
   First sale: <dateOfFirstSale> · <investorCount> investors
   Filing: <primaryDocUrl>
```

- Amounts are as filed; if `totalAmountSold` is 0 and
  `firstSaleYetToOccur` is true, write "announced, no first sale
  yet" instead of a raised figure.
- If nothing matched, send one line: "No new Form D filings
  matched your radar today." Nothing else.
- Never invent or round figures, never merge filings, and only
  report records the Actor actually returned.

## Scheduling

Offer to run this as a recurring daily job (for example 08:00
in the user's timezone) using OpenClaw's scheduler, and a
weekly roll-up on request. The user can change filters or
pause the radar at any time by editing their preferences in
chat; re-read the state file at the start of every run.

## Notes

- Form D covers private placements only — it does not include
  priced public offerings, crowdfunding (Reg CF files Form C),
  or venture rounds that were never filed. Say so if the user
  expects a company that is missing.
- This is public regulatory data presented as filed. It is not
  investment advice, and a filing is not a recommendation.
