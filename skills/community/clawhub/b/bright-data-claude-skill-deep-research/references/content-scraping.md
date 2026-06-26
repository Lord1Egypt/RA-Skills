# Content Scraping Template

This template handles the collection of content from discovered URLs.

## Parameters

- `urls`: Array of URLs to scrape
- `mode`: scraping mode (serial/batch/browser)
- `format`: output format (markdown/html)

## Process

### Quick Mode (Serial Processing)

Process URLs one at a time:

```json
{
  "tool": "scrape_as_markdown",
  "parameters": {
    "url": "{{url}}"
  }
}
```

**Use when**:
- Testing new sources
- Small number of URLs (< 5)
- When order matters (sequential dependencies)

### Standard Mode (Parallel Batch)

Process up to 10 URLs concurrently:

```json
{
  "tool": "scrape_batch",
  "parameters": {
    "urls": [
      "{{url1}}",
      "{{url2}}",
      "...up to 10 URLs..."
    ]
  }
}
```

**Use when**:
- Processing 5-20 URLs
- Speed is important
- URLs are independent of each other

**Batching Strategy**:
- Split large URL lists into batches of 10
- Process batches sequentially
- Track success/failure per URL

### Deep Mode (Browser Automation)

For JavaScript-rendered pages:

```json
{
  "tool": "scraping_browser_navigate",
  "parameters": {
    "url": "{{url}}"
  }
}
```

**Use when**:
- Pages require JavaScript execution
- Content loads dynamically (AJAX, React, etc.)
- Need to interact with the page
- Sites have strong anti-bot measures

## Error Handling

### Retry Strategy

If scrape fails:
1. **First retry**: Use alternative method
   - scrape_as_markdown → scrape_as_html
   - scrape_as_markdown → scraping_browser_navigate

2. **Second retry**: After 5 second delay

3. **Give up**: After 2 failed attempts

### Error Logging

Track errors with context:
```json
{
  "url": "https://example.com",
  "error": "Connection timeout",
  "method": "scrape_as_markdown",
  "timestamp": "2024-01-22T10:30:00Z"
}
```

## Content Validation

After scraping, validate:
- [ ] Content is not empty
- [ ] Content is not error page (404, 500, etc.)
- [ ] Content is not CAPTCHA page
- [ ] Content has meaningful text (> 100 characters)
- [ ] Content is in expected language

## Output Format

```json
{
  "total_urls": {{total}},
  "successful": {{count}},
  "failed": {{count}},
  "contents": [
    {
      "url": "https://example.com/page1",
      "content": "# Page Title\n\nContent here...",
      "word_count": 542,
      "language": "en",
      "scrape_method": "scrape_as_markdown",
      "timestamp": "2024-01-22T10:30:00Z"
    }
  ],
  "errors": [
    {
      "url": "https://example.com/page2",
      "error": "Connection timeout",
      "retries": 2
    }
  ]
}
```

## Performance Tips

1. **Use scrape_batch**: 10x faster than serial processing
2. **Set Timeouts**: Don't wait indefinitely for slow pages
3. **Parallelize**: Process multiple batches concurrently if supported
4. **Cache Results**: Store scraped content to avoid re-scraping
5. **Monitor Success Rate**: If >30% fail, adjust strategy
6. **Avoid Token Limits**: 
   - **What is the limit?**: 25,000 tokens maximum per Read operation
   - **Why this limit exists**: 
     - **Memory protection**: Prevents memory overflow from loading too much content
     - **Performance optimization**: Ensures fast response times
     - **Context management**: Preserves space for other content in conversation
     - **System stability**: Prevents crashes or errors
   - **Can this be increased?**: 
     - **No** - This is a hard system limit in Claude Code
     - **Cannot be changed** via configuration files
     - **Purpose**: Protect system stability and performance
   - **Workarounds for large files**:
     - Use `Read` with `offset` and `limit` to read in chunks (e.g., 100 lines at a time)
     - Use `Grep` to search for specific patterns instead of reading entire file
     - Use `Glob` to find files by pattern
   - **Workarounds for scraping**:
     - Large pages (Etsy, Amazon, etc.) can exceed 25,000 tokens
     - Batch 1-2 URLs at a time for large pages
     - Use `scrape_as_markdown` for individual URLs if needed

## Content Cleaning

After scraping, clean the content:
- Remove navigation menus
- Remove footer and sidebar content
- Remove advertisements
- Remove popups and modals
- Normalize whitespace
- Fix encoding issues

Bright Data's scrape_as_markdown does most of this automatically, but additional cleaning may be needed for some sites.
