---
name: Google Search Console
description: >
  Google Search Console sitemap status skill for MyBrandMetrics. Use it to
  query connected Google Search Console sitemap data, submitted URL counts,
  indexed URL counts, sitemap warnings, sitemap errors, pending processing
  status, content type, and last downloaded time through the
  google_search_console_sitemaps source.
compatibility:
  tools:
    - bash
    - python
  dependencies:
    - requests
---

# Google Search Console

Check Google Search Console sitemap status through the MyBrandMetrics API.

Use this skill to review sitemap health for a connected Google Search Console
property: submitted URL counts, indexed URL counts, warning counts, error
counts, pending status, content type, and last downloaded time.

Website: [https://www.clawbus.com/](https://www.clawbus.com/)  
MyBrandMetrics API: [https://mybrandmetrics.com/](https://mybrandmetrics.com/)

## Core Capabilities

| Capability | Details |
| --- | --- |
| Google Search Console sitemap data | Query the `google_search_console_sitemaps` source through MyBrandMetrics. |
| Sitemap status | List sitemap rows for a connected Search Console property. |
| Submitted and indexed URLs | Compare `contents_submitted` and `contents_indexed` for sitemap health. |
| Warnings and errors | Review sitemap warning and error counts. |
| Pending processing | Check whether a sitemap row is still pending. |
| Last downloaded time | See when Google last downloaded each sitemap. |
| Filtered queries | Use metrics, dimensions, filters, and row limits for narrower reports. |

## Setup Flow

1. Open [https://mybrandmetrics.com/](https://mybrandmetrics.com/) and sign in
   with Google.
2. In MyBrandMetrics, open **Data sources**.
3. Connect Google Search Console as a data source.
4. Wait until the Google Search Console connection is ready.
5. In [https://mybrandmetrics.com/](https://mybrandmetrics.com/), get the
   MyBrandMetrics API key.
6. Install the `clawbus-google-search-console` skill.
7. Start a Google Search Console sitemap status workflow with natural-language
   instructions.

## Workflow

Use natural-language prompts after the skill is installed. Include:

- the Google Search Console connection ID, such as `sc-domain:example.com`;
- whether to list all sitemap rows or focus on a specific sitemap issue;
- the metrics to review, such as warnings, errors, submitted URLs, indexed
  URLs, and sitemap count;
- the dimensions to group by, such as site URL, sitemap path, content type,
  last downloaded time, and pending status;
- any filters or row limit needed for the analysis.

Example:

```text
Check the Google Search Console sitemap status for sc-domain:example.com and summarize warnings, errors, submitted URLs, and indexed URLs.
```

## Search-Friendly Workflows

Common Google Search Console sitemap workflows include:

- list Google Search Console sitemap status rows;
- check sitemap warnings and errors;
- compare submitted URLs and indexed URLs;
- find pending sitemap records;
- review sitemap content type and last downloaded time;
- summarize sitemap health for a connected Search Console property.

## Use The Script Directly

Use `scripts/searchconsole.py`.

List sitemap status:

```bash
python3 scripts/searchconsole.py \
  --api-key "YOUR_API_KEY" \
  --connection-id "sc-domain:example.com" \
  --limit 200
```

Use custom metrics and dimensions:

```bash
python3 scripts/searchconsole.py \
  --api-key "YOUR_API_KEY" \
  --connection-id "sc-domain:example.com" \
  --metrics "warnings,errors,contents_submitted,contents_indexed" \
  --dimensions "site_url,sitemap_path,content_type,last_downloaded,is_pending" \
  --limit 100
```

Use an environment variable instead of passing the API key in the command:

```bash
export MYBRANDMETRICS_API_KEY="YOUR_API_KEY"
python3 scripts/searchconsole.py \
  --connection-id "sc-domain:example.com" \
  --limit 200
```

## Parameters

| Parameter | Required | Purpose |
| --- | --- | --- |
| `--api-key` | Yes, unless `MYBRANDMETRICS_API_KEY` is set | MyBrandMetrics API key. |
| `--connection-id` | Yes | Google Search Console property connection ID, such as `sc-domain:example.com`. |
| `--account-id` | No | Account ID. Defaults to the connection ID when omitted. |
| `--metrics` | No | Comma-separated sitemap metrics. |
| `--dimensions` | No | Comma-separated sitemap dimensions. |
| `--filter` | No | Filter in `field:operator:value` format. Repeat for multiple filters. |
| `--limit` | No | Maximum rows to return. Default is `200`. |
| `--compact` | No | Print compact JSON instead of indented JSON. |

## Available Metrics And Dimensions

Default metrics:

- `warnings`
- `errors`
- `contents_submitted`
- `contents_indexed`
- `sitemaps_count`

Default dimensions:

- `site_url`
- `sitemap_path`
- `content_type`
- `last_downloaded`
- `is_pending`

Google Search Console data can lag by several days, so new sitemap submissions
or recent indexing changes may not appear immediately.
