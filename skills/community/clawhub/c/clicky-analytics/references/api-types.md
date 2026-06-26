# Clicky API Data Types

Request multiple types in one call: `type=visitors,countries,searches`

## Popular Items (ordered by frequency)
- `pages` — top pages
- `pages-entrance` — landing pages
- `pages-exit` — exit pages
- `downloads` — file downloads
- `events` — JS events
- `links` — incoming links (full URL)
- `links-domains` — incoming links (by domain)
- `links-outbound` — outbound links
- `searches` — search queries
- `searches-keywords` — individual keywords
- `searches-engines` — search engines
- `searches-rankings` — Google rankings (best→worst)
- `countries` — by country
- `cities` — by city
- `regions` — by region
- `languages` — by language
- `web-browsers` — by browser
- `operating-systems` — by OS
- `screen-resolutions` — by resolution
- `hardware` — mobile devices
- `traffic-sources` — how visitors arrive (link/search/email/etc)
- `goals` — goal completions
- `campaigns` — campaign tracking
- `engagement-actions` — by actions performed
- `engagement-times` — by time on site

## Chronological Items (newest→oldest)
- `visitors-list` — visitor details (filter by ip_address or uid)
- `actions-list` — visitor actions (filter by session_id)
- `searches-recent` — recent search referrals
- `links-recent` — recent link referrals

## Tallies (counts/averages)
- `visitors` — visitor count
- `visitors-online` — currently active (always live)
- `visitors-unique` — unique visitors
- `visitors-new` — first-time visitors
- `actions` — total actions (pageviews + downloads + outbound)
- `actions-pageviews` — pageview count
- `actions-average` — avg actions per visitor
- `time-average` — avg time on site (seconds)
- `time-average-pretty` — avg time (formatted: 3m 10s)
- `time-total-pretty` — total time (formatted: 6d 19h 5m)
- `bounce-rate` — bounce rate percentage

## Date Formats
- `today`, `yesterday`, `last-7-days`, `last-30-days`
- `YYYY-MM-DD` — specific date
- `YYYY-MM-DD,YYYY-MM-DD` — date range (max 31 days, 366 for Pro)

## Limits
- Default: 50, max: 1000 (use `page` param to paginate)
- visitors-list/actions-list: max 31-day range, max 1000 items
