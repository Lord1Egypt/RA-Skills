# Matching and time rules

## Priority

Apply selectors in this order when they are explicitly present:

1. Exact issue number on a supporting source.
2. Exact report type + title-derived year/week or year/month.
3. Exact report type + displayed publication date.
4. Reference date mapped to a candidate period and verified against official titles.
5. Latest within one determined report type.

Reject conflicting selectors rather than silently choosing one.

## Weekly matching

Require equality of `report_type`, `period_year`, and `period_week`. Parse year/week from the title. Never use `publish_date.year` or the URL directory year as the reporting year.

For `reference_date`, calculate its ISO week/year only to form candidates. Verify the candidate title. If the site's monitoring convention differs, return the preceding and following official candidates with an explanation; do not label either exact without evidence.

## Monthly matching

Require equality of `report_type`, `period_year`, and `period_month` parsed from the title. Publication may occur in the following month. Weekly ranges mentioned in a monthly body belong in `data_periods[]`, never in `reporting_period`.

## Issue matching

Require a positive integer and `supports_issue_number=true`. One exact record succeeds, several exact records are `ambiguous`, and zero after complete healthy pagination is `not_found`. Never return a nearby issue.

## Publication date

Interpret displayed dates as `Asia/Shanghai` natural dates serialized `YYYY-MM-DD`. Do not invent a time or UTC conversion. If several reports share the date, return all as `ambiguous`.

## Latest ordering

Within one report type, prefer the maximum issue number when supported; otherwise compare reporting year/period, then publication date. Flag these anomalies:

- adjacent issue numbers are not strictly decreasing;
- issue decreases while reporting period increases;
- publication dates increase down the list;
- one issue number maps to different canonical URLs.

Open conflicting carriers and verify them. If this cannot establish uniqueness, return `ambiguous`.

## Candidate policy

Return adjacent candidates only for reference-date convention disagreement or helpful context alongside `not_found`; mark them clearly as nonmatches. Exact fields must never contain an approximate candidate.
