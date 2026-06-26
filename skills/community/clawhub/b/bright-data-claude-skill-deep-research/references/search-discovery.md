# Search Discovery Template

This template handles the discovery phase of research, finding relevant URLs through search engines.

## Parameters

- `query`: Search query
- `engine`: Search engine to use (google/bing/yandex)
- `max_results`: Maximum number of URLs to discover
- `site_filter`: Optional site restriction (e.g., "site:etsy.com")

## Process

### Step 1: Initial Search

```json
{
  "tool": "search_engine",
  "parameters": {
    "query": "{{query}}",
    "engine": "{{engine}}",
    "cursor": "0"
  }
}
```

### Step 2: Extract URLs

Parse the SERP results and extract all URLs. Look for:
- Organic search results
- Exclude: ads, sponsored content, social media links

### Step 3: Filter and Validate

For each URL:
- Check domain reputation
- Verify URL is accessible
- Filter out irrelevant domains
- Deduplicate URLs

### Step 4: Paginate if Needed

If URL count < max_results:
```json
{
  "tool": "search_engine",
  "parameters": {
    "query": "{{query}}",
    "engine": "{{engine}}",
    "cursor": "1"
  }
}
```

Continue until max_results reached or no more results available.

### Step 5: Prioritize and Rank

Sort URLs by:
1. Domain authority (established sites first)
2. Title relevance (keyword matching)
3. URL structure (clean, descriptive URLs)
4. Expected content quality

## Output Format

```json
{
  "query": "{{query}}",
  "total_found": {{total}},
  "urls": [
    {
      "url": "https://example.com/page1",
      "title": "Page Title",
      "relevance_score": 0.95,
      "domain_authority": "high"
    },
    {
      "url": "https://example.com/page2",
      "title": "Another Page",
      "relevance_score": 0.87,
      "domain_authority": "medium"
    }
  ]
}
```

## Best Practices

1. **Use Specific Queries**: "site:etsy.com nba jerseys" instead of "nba"
2. **Check Multiple Engines**: If Google fails, try Bing or Yandex
3. **Validate URLs**: Remove malformed or suspicious URLs
4. **Set Realistic Limits**: 10-20 URLs is usually sufficient for standard mode
5. **Log Search Metadata**: Record search engine, cursor, total results for transparency
