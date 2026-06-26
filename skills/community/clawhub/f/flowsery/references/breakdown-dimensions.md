# Breakdown Dimensions Reference

Use these values with the `GET /breakdown?dimension=<value>` endpoint, or use the dedicated shortcut endpoints listed below.

## Dimensions

| Dimension         | Shortcut Endpoint        | Description                                        |
| ----------------- | ------------------------ | -------------------------------------------------- |
| `device`          | `GET /devices`           | Desktop, Mobile, Tablet                            |
| `page`            | `GET /pages`             | Page path (e.g. `/pricing`, `/blog/post-1`)        |
| `entry_page`      | —                        | Landing page (first page in session)               |
| `exit_link`       | —                        | Last external link clicked                         |
| `hostname`        | `GET /hostnames`         | Hostname/domain                                    |
| `referrer`        | `GET /referrers`         | Referrer domain (e.g. `google.com`, `twitter.com`) |
| `channel`         | `GET /channels`          | Marketing channel (Organic Search, Direct, etc.)   |
| `campaign`        | `GET /campaigns`         | UTM campaign name                                  |
| `goal`            | `GET /goals`             | Custom goal/event name                             |
| `country`         | `GET /countries`         | Country name                                       |
| `region`          | `GET /regions`           | Region/state code                                  |
| `city`            | `GET /cities`            | City name                                          |
| `browser`         | `GET /browsers`          | Browser name (Chrome, Safari, Firefox)             |
| `browser_version` | —                        | Browser name + version (Chrome 133.0)              |
| `os`              | `GET /operating-systems` | Operating system (Mac OS, Windows, iOS)            |
| `os_version`      | —                        | OS + version (Mac OS 14.0)                         |
| `utm_source`      | —                        | UTM source parameter                               |
| `utm_medium`      | —                        | UTM medium parameter                               |
| `utm_campaign`    | —                        | UTM campaign parameter (same as `campaign`)        |
| `utm_term`        | —                        | UTM term parameter                                 |
| `utm_content`     | —                        | UTM content parameter                              |
| `ref`             | —                        | `ref` URL parameter value                          |
| `source`          | —                        | `source` URL parameter value                       |
| `all_params`      | —                        | Combined view of all tracking parameters           |

## Tracking Parameter Dimensions

These dimensions relate to URL parameters used for attribution:

- `utm_source` — Where the traffic came from (e.g. `google`, `newsletter`)
- `utm_medium` — How the traffic arrived (e.g. `cpc`, `email`, `social`)
- `utm_campaign` — Which campaign drove the traffic
- `utm_term` — Paid search keyword
- `utm_content` — Ad variation identifier
- `ref` — Custom referrer tag (e.g. `?ref=partner123`)
- `source` — Custom source tag (e.g. `?source=homepage_banner`)

Use `all_params` to see a combined count across all tracking parameter dimensions.

## Marketing Channel Classification

Flowsery auto-classifies traffic into GA4-aligned channels based on referrer domain and UTM parameters:

| Channel            | Classification Rules                                                                                 |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| **Organic Search** | Known search engine referrer (Google, Bing, DuckDuckGo, Baidu, Yandex, etc.)                         |
| **Paid Search**    | utm_medium: `cpc`, `ppc`, `paid_search`, `paid-search`, `paidsearch`, `sea`                          |
| **Organic Social** | Known social media referrer (facebook.com, twitter.com, linkedin.com, reddit.com, etc.)              |
| **Paid Social**    | utm_medium: `paid_social`, `paid-social`, `paidsocial`, `social_cpc`, `social_ppc`                   |
| **Email**          | utm_medium: `email`, `newsletter` OR utm_source: `mailchimp`, `sendgrid`, `klaviyo`, `hubspot`, etc. |
| **Display**        | utm_medium: `display`, `banner`, `expandable`, `interstitial`, `cpm`, `programmatic`                 |
| **Referral**       | Has referrer domain that isn't search/social                                                         |
| **Direct**         | No referrer domain                                                                                   |
| **Affiliate**      | utm_medium: `affiliate`, `affiliates`, `partner`                                                     |
| **Video**          | utm_medium: `video`, `paid_video`                                                                    |
| **SMS**            | utm_medium: `sms`, `text`                                                                            |
| **Audio**          | utm_medium: `audio`, `podcast`                                                                       |

## Time Series Intervals

| Interval | Default Range  | Description          |
| -------- | -------------- | -------------------- |
| `hour`   | Last 24 hours  | Hourly data buckets  |
| `day`    | Last 30 days   | Daily data buckets   |
| `week`   | Last 30 days   | Weekly data buckets  |
| `month`  | Last 12 months | Monthly data buckets |

Same-day queries automatically upgrade to hourly granularity.

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
