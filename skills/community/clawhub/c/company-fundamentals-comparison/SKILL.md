---
name: company-fundamentals-comparison
description: Compare public companies' reported financial statements across matched fiscal periods using SEC EDGAR data and Yahoo Finance industry context. Use for sourced peer metrics, not stock valuation or buy/sell recommendations.
---

# Company fundamentals comparison

Build a comparable financial-statement matrix for public issuers. Use
finance-markets-research for a one-ticker lookup, earnings-event-research for
an event-specific preview or recap, and sec-filings-research for filing or
section analysis.

## Define the peer set and reporting basis

- Use the user's company list and comparison question first. If peers are not
  supplied, use Yahoo Finance industries only to suggest candidates, then state
  the source's industry classification and the selection criteria. Its industry
  list is not a complete or authoritative peer group.
- Resolve each company independently through Yahoo Finance lookup and SEC
  company search. Keep legal issuer name, ticker, exchange, and SEC CIK in the
  evidence table; similar names or tickers do not establish the same company.
- Confirm the requested reporting basis before calculating: annual versus
  quarterly, fiscal year or quarter, currency, unit, accounting basis, and
  whether the user wants reported or adjusted values. Do not mix IFRS and GAAP
  facts or translate currencies without a rate source and observation date.

## Retrieve and reconcile statements

1. Use SEC normalized financials for each resolved CIK/ticker and requested
   income, balance-sheet, or cash-flow statement. Record the returned fiscal
   label, start/end dates, form, units, and source URL.
2. Use SEC submissions to identify the matching 10-K/10-Q and filing/report
   dates. Retrieve its filing metadata and relevant sections when a number or
   definition needs primary-document context. A filing date is not a fiscal
   period end date.
3. Use SEC frames only for a standard XBRL concept shared across filers. Match
   taxonomy, concept, unit, and reporting frame. SEC frames align to calendar
   periods; companies can have different fiscal start/end dates, so compare
   their actual fact dates before calling values period-matched.
4. Yahoo Finance industry pages can provide candidate peers and provider
   classifications. Yahoo financial statements or profile fields are secondary
   cross-checks; preserve any conflict with SEC-reported facts instead of
   silently choosing the larger or newer number.
   SEC frame responses are broad and capped; match returned CIKs to the chosen
   peer set and treat a peer omitted past the cap as unavailable, not absent.

## Compare metrics carefully

- Compare the same statement line and fiscal period. A quarterly cash-flow
  amount may be year-to-date; do not derive a standalone quarter unless the
  fact's duration is verified.
- Calculate only requested measures from aligned inputs. Show the formula and
  units for growth, margin, or balance-sheet ratios. Keep missing denominators,
  zero denominators, and unmatched periods as unknown rather than zero.
- Separate GAAP facts from company-defined adjusted metrics. Never use an
  adjusted measure for one company against a GAAP measure for another without
  making the difference explicit.
- SEC normalized values may reflect later restatements. Preserve the retrieval
  time and filing accession; do not imply that today's normalized value was
  known at an earlier date.
- Do not produce a single financial-health score, fair value, price target,
  or investment recommendation. Summarize the evidence and the unresolved
  comparability questions.

## Deliverable

Return a peer matrix with legal issuer, CIK/ticker, fiscal period, statement
line, value, unit/currency, source/accession, retrieval time, and any formula.
Follow with a short comparison of supported changes and material gaps. If a
company is missing a comparable fact, keep it out of that metric's ranking and
explain why.

~~~sh
scripts/crawlora.sh /yahoo-finance/lookup query='NVIDIA' type=equity
scripts/crawlora.sh /yahoo-finance/industries
scripts/crawlora.sh /sec/company/search q='NVIDIA'
scripts/crawlora.sh /sec/financials ticker=NVDA statement=income period=annual limit=5
scripts/crawlora.sh /sec/company/submissions ticker=NVDA form=10-K limit=3
# Use an accession returned by submissions:
scripts/crawlora.sh /sec/filing/sections ticker=NVDA accession=ACCESSION_FROM_SUBMISSIONS items=7 max_chars=20000
scripts/crawlora.sh /sec/frames concept=Revenues period=CY2025 taxonomy=us-gaap unit=USD limit=100
~~~
