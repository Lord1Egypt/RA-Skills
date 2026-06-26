# Query Patterns

Read this file when the user needs concrete command examples for Google Search
Console sitemap queries through MyBrandMetrics.

## Default Sitemap Status

```bash
python3 google-search-console/scripts/searchconsole.py \
  --connection-id "sc-domain:example.com" \
  --limit 200
```

## Select Specific Metrics

```bash
python3 google-search-console/scripts/searchconsole.py \
  --connection-id "sc-domain:example.com" \
  --metrics "warnings,errors,contents_submitted,contents_indexed" \
  --limit 200
```

## Select Specific Dimensions

```bash
python3 google-search-console/scripts/searchconsole.py \
  --connection-id "sc-domain:example.com" \
  --dimensions "site_url,sitemap_path,last_downloaded,is_pending" \
  --limit 200
```

## Filter Results

Filters use `field:operator:value` format and can be repeated.

```bash
python3 google-search-console/scripts/searchconsole.py \
  --connection-id "sc-domain:example.com" \
  --filter "content_type:equals:web" \
  --limit 100
```

## Compact JSON

```bash
python3 google-search-console/scripts/searchconsole.py \
  --connection-id "sc-domain:example.com" \
  --compact
```

## Analysis Tips

- Flag any sitemap where `contents_indexed` is `0`.
- Flag non-zero `errors` or `warnings`.
- Treat `is_pending` as a sign that Google has not finished processing the
  sitemap.
- Remember that GSC data can lag by several days.
