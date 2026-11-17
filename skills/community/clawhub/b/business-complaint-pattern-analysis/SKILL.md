---
name: business-complaint-pattern-analysis
description: Analyze public BBB business complaint narratives, response threads, statuses, and reporting-window totals using Crawlora. Use for a sourced complaint-pattern or response-process comparison with business identity, incomplete lists, redactions, allegations, and customer-volume limits preserved.
---

# Business complaint pattern analysis

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare reported complaint themes or response patterns for selected businesses.
Establish business/location scope, reporting/date window, and comparable complaint
categories. Keep complainant allegations, business responses, customer replies,
and BBB's presented status as distinct attributed evidence.

## Resolve the entity and retrieve complaint evidence

1. Use BBB dataset facets/search or live search to identify exact business profiles.
   Match business ID, name/alternate names, location, website, and HQ relationships.
   A multi-location HQ profile can aggregate branches; do not assign its count
   to each location or combine it with branch counts as independent complaints.
2. Stored BBB profiles do not embed full complaints. Use the returned profile
   URL or verified HQ URL with live business/complaints/more-info routes, not a
   guessed complaint-page slug. Preserve crawl time versus live collection time.
3. `total_complaints` has its own reporting window, typically the presented
   three-year window; `closed_last_12_months` is a different measure. Retain the
   returned `period_text` rather than inventing a common time span across firms.
   There is no date filter/pagination parameter on the complaints route: filter
   returned itemized dates locally and mark bounded coverage.
4. `complaints_list_incomplete=true` means real aggregate totals can accompany
   unavailable itemized detail. Do not substitute an empty list for zero complaints
   or fabricate theme/status counts. A genuine `total_complaints=0` can be normal,
   but it only describes that source/window, not all customers' experience.
5. Preserve complaint ID, date/type/status, narrative and response-thread roles.
   BBB statuses include `Resolved`, `Unresolved`, `Answered`, `Unanswered`,
   `Unpursuable`; an answer is not automatically a resolution or admission.
   Keep BBB's `REMOVED` redactions intact rather than reconstructing identities.

```sh
scripts/crawlora.sh /datasets/bbb-businesses/facets facet=category
scripts/crawlora.sh /bbb/search query="plumbing" location="Austin, TX" page=1
# Use a verified returned profile URL, for example:
# scripts/crawlora.sh /bbb/business/complaints url="$BBB_PROFILE_URL"
# scripts/crawlora.sh /bbb/business/more-info url="$BBB_PROFILE_URL"
```

## Report patterns with defensible denominators

Deduplicate by complaint ID; multiple response rounds are one complaint with
several observations. Code themes with uncertain/multi-label states and cite
short attributed excerpts. Show itemized sample size, aggregate totals, missing
lists, and date filters separately. A sample resolution/response proportion uses
that sample's comparable statuses, not the total number of customers or a mismatched
aggregate window. Response intervals need actual role/date pairs; a rounded date
is not an exact elapsed-hour measurement.

Return identity/coverage, complaint and response evidence tables, theme/status
counts, source reasons-for-rating where relevant, and unresolved questions.
The main profile's reasons list can be shallow boilerplate; `more-info` supplies
the fuller per-factor list. Reviews, accreditation, and letter grades are separate
measures. Counts without comparable customer/transaction volume cannot rank a
business's complaint rate or prove fraud, quality, liability, or consumer outcomes.
Do not file complaints, contact businesses, publish accusations, or initiate a
legal action from a research request.
