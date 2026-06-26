# Dimensions and Metrics

Read this file when choosing dimensions, metrics, or filters for the
`google_search_console_sitemaps` source.

## Source Key

| Source key | Description |
|---|---|
| `google_search_console_sitemaps` | Sitemap status and health data from Google Search Console |

## Default Dimensions

| Dimension | Description |
|---|---|
| `site_url` | Search Console site URL or property identifier |
| `sitemap_path` | Full sitemap URL or sitemap path |
| `content_type` | Sitemap content type, such as `web`, `image`, or `video` |
| `last_downloaded` | Last time Google downloaded the sitemap |
| `is_pending` | Whether sitemap processing is still pending |

## Default Metrics

| Metric | Description |
|---|---|
| `warnings` | Number of sitemap warnings |
| `errors` | Number of sitemap errors |
| `contents_submitted` | Number of submitted URLs |
| `contents_indexed` | Number of indexed URLs |
| `sitemaps_count` | Number of sitemap files represented in the row |

## Filter Format

The script accepts repeatable filters in this shape:

```text
field:operator:value
```

Example:

```bash
--filter "content_type:equals:web"
```

Use filters only when the user asks for a narrower report or when the full result
set is too noisy.
