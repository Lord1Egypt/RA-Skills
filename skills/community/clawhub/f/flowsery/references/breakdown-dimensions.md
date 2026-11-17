# Breakdown Dimensions Reference

Use these values with the `GET /breakdown?dimension=<value>` endpoint, or use the dedicated shortcut endpoints listed below. Both return the same rows: `value`, `visitors`, `revenue` and `percentage`, ordered by visitors descending, with `pagination.total`. Dimensions without a shortcut are only reachable through `/breakdown`.

## Dimensions

| Dimension | Shortcut Endpoint | Description |
| --- | --- | --- |
| `device` | `GET /devices` | Desktop, Mobile, Tablet |
| `page` | `GET /pages` | Page path (e.g. `/pricing`, `/blog/post-1`) |
| `entry_page` | none | Landing page (first page in session) |
| `exit_link` | none | Last external link clicked |
| `hostname` | `GET /hostnames` | Hostname/domain |
| `referrer` | `GET /referrers` | Source name (e.g. `Google`) or referrer domain |
| `channel` | `GET /channels` | Marketing channel (Organic Search, Direct, etc.) |
| `campaign` | `GET /campaigns` | UTM campaign name |
| `goal` | `GET /goals` | Custom goal/event name |
| `country` | `GET /countries` | Country name |
| `region` | `GET /regions` | Region or state name (e.g. `California`) |
| `city` | `GET /cities` | City name |
| `browser` | `GET /browsers` | Browser name (Chrome, Safari, Firefox) |
| `browser_version` | none | Browser name + version (Chrome 133.0) |
| `os` | `GET /operating-systems` | Operating system (Mac OS, Windows, iOS) |
| `os_version` | none | OS + version (Mac OS 14.0) |
| `utm_source` | none | UTM source parameter |
| `utm_medium` | none | UTM medium parameter |
| `utm_campaign` | none | UTM campaign parameter (same as `campaign`) |
| `utm_term` | none | UTM term parameter |
| `utm_content` | none | UTM content parameter |
| `ref` | none | `ref` URL parameter value |
| `source` | none | `source` URL parameter value |
| `via` | none | `via` URL parameter value |
| `all_params` | none | Combined view of all tracking parameters |

## Tracking Parameter Dimensions

These dimensions relate to URL parameters used for attribution:

- `utm_source`: Where the traffic came from (e.g. `google`, `newsletter`)
- `utm_medium`: How the traffic arrived (e.g. `cpc`, `email`, `social`)
- `utm_campaign`: Which campaign drove the traffic
- `utm_term`: Paid search keyword
- `utm_content`: Ad variation identifier
- `ref`: Custom referrer tag (e.g. `?ref=partner123`)
- `source`: Custom source tag (e.g. `?source=homepage_banner`)
- `via`: Custom via tag (e.g. `?via=newsletter`)

Use `all_params` to see a combined count across all tracking parameter dimensions. Only tagged visits appear in any of these; `channel` and `referrer` cover untagged traffic too.

Geography comes in three granularities (`country`, `region`, `city`); add `filter_country` to drill into one country. `browser` and `os` return names only, `browser_version` and `os_version` add the version.

## Marketing Channel Classification

Flowsery auto-classifies traffic into GA4-aligned channels based on referrer domain and UTM parameters:

| Channel | Classification Rules |
| --- | --- |
| **Organic Search** | Known search engine referrer (Google, Bing, DuckDuckGo, Baidu, Yandex, etc.) |
| **Paid Search** | utm_medium: `cpc`, `ppc`, `paid_search`, `paid-search`, `paidsearch`, `sea` |
| **Organic Social** | Known social media referrer (facebook.com, twitter.com, linkedin.com, reddit.com, etc.) |
| **Paid Social** | utm_medium: `paid_social`, `paid-social`, `paidsocial`, `social_cpc`, `social_ppc` |
| **Email** | utm_medium: `email`, `newsletter` OR utm_source: `mailchimp`, `sendgrid`, `klaviyo`, `hubspot`, etc. |
| **Display** | utm_medium: `display`, `banner`, `expandable`, `interstitial`, `cpm`, `programmatic` |
| **Referral** | Has referrer domain that isn't search/social |
| **Direct** | No referrer domain |
| **Affiliate** | utm_medium: `affiliate`, `affiliates`, `partner` |
| **Video** | utm_medium: `video`, `paid_video` |
| **SMS** | utm_medium: `sms`, `text` |
| **Audio** | utm_medium: `audio`, `podcast` |

## Time Series Intervals

| Interval | Description |
| --- | --- |
| `hour` | Hourly data buckets |
| `day` | Daily data buckets |
| `week` | Weekly data buckets |
| `month` | Monthly data buckets |

Whatever the interval, the window defaults to the last 30 days ending now. Pass `startAt` and `endAt` for any other range.

## Supported Payment Integrations

Payments are automatically tracked when these providers are connected (no API calls needed):

- **Stripe**
- **LemonSqueezy**
- **Polar**
- **Paddle**
- **Dodo**
- **Shopify**
- **WordPress** (WooCommerce)

For all other providers, use `POST /payments` to record transactions manually.
