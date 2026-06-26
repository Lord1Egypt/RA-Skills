---
name: research-brightdata
description: This skill should be used when the user asks to "research web data", "scrape websites", "extract web data", "perform market research", "analyze competitors", "monitor prices", "collect product information", "search and analyze web content", or mentions Bright Data MCP, web scraping, web data extraction, or automated research. Provides comprehensive web research workflows using Bright Data MCP tools including search, scraping, extraction, and browser automation capabilities.
version: 1.0.0
---

# Bright Data Research Skill

Advanced web research powered by Bright Data MCP - perform market analysis, competitive intelligence, data extraction, and comprehensive web research with anti-bot protection.

## Overview

This skill provides complete workflows for automated web research using Bright Data MCP. Handle search discovery, content collection, structured data extraction, and comprehensive analysis with browser automation support.

## When This Skill Applies

Activate this skill when the user's request involves:
- Web scraping and data collection
- Market research and competitive analysis
- Price monitoring and comparison
- Product information extraction
- Search engine result analysis
- Large-scale web data gathering
- Research requiring anti-bot protection

## Core Capabilities

### Search and Discovery

Use `search_engine` tool to find relevant sources:

```json
{
  "tool": "search_engine",
  "parameters": {
    "query": "site:etsy.com nba merchandise",
    "engine": "google",
    "cursor": "0"
  }
}
```

**Search strategies:**
- Use site operators: `"site:etsy.com keywords"`
- Use exact phrases: `"machine learning in healthcare"`
- Exclude terms: `"iphone -case -cover"`
- Paginate with cursor: "0", "1", "2" for more results

### Content Collection

Three collection modes based on research depth:

**Quick Mode** (3-5 URLs, serial processing):
- Use `scrape_as_markdown` for each URL
- Best for: Fast overviews, fact-checking

**Standard Mode** (10-20 URLs, parallel batch):
- Use `scrape_batch` for up to 10 URLs concurrently
- Best for: Market research, competitive analysis

**Deep Mode** (20-50 URLs, browser automation):
- Use `scraping_browser_navigate` for JavaScript-rendered pages
- Use `scraping_browser_links` to discover page links
- Use `scraping_browser_click` for interactions
- Best for: Dynamic content, multi-page extraction

### Data Extraction

Use `extract` tool for AI-powered structured data extraction:

```json
{
  "tool": "extract",
  "parameters": {
    "url": "https://example.com/product",
    "extraction_prompt": "Extract: product name, price as number, rating (0-5), number of reviews, seller name, availability status"
  }
}
```

**Common extraction schemas:**
- **E-commerce**: name, price, rating, reviews, seller, availability
- **Articles**: title, author, date, summary, key points
- **Companies**: name, industry, founded, headquarters, employee count

### Output Formats

Three report formats for different use cases:

**Report Format** (default):
- Executive summary
- Key findings with evidence
- Detailed analysis
- Methodology and recommendations
- Source references

**JSON Format**:
- Structured data for API integration
- All raw and processed data
- Metadata and provenance
- Statistical analysis

**Markdown Format**:
- Clean, readable content
- Tables and lists
- Source links
- Minimal formatting

## Research Workflow

### Phase 1: Query Analysis

Understand the research intent:
- **Scope**: How broad/deep should research be?
- **Key entities**: Products, companies, topics
- **Target sources**: Which sites/platforms?
- **Data needed**: What fields to extract?

### Phase 2: Source Discovery

Use `search_engine` to find URLs:
1. Execute initial search
2. Extract URLs from SERP
3. Filter irrelevant domains
4. Paginate if needed
5. Prioritize by relevance

### Phase 3: Content Collection

Choose appropriate mode:
- **Quick**: `scrape_as_markdown` per URL
- **Standard**: `scrape_batch` 10 URLs at once
- **Deep**: `scraping_browser_navigate` + browser tools

Handle errors gracefully:
- Retry failed URLs with alternative methods
- Log errors for transparency
- Continue with available data

### Phase 4: Data Extraction

Apply extraction schema:
- Use `extract` with custom prompts
- Validate extracted data
- Handle missing/malformed data
- Ensure data quality

### Phase 5: Analysis & Synthesis

Process and analyze:
- Clean and normalize data
- Perform statistical analysis
- Identify patterns and trends
- Cross-reference sources
- Validate findings

### Phase 6: Report Generation

Generate output:
- **Report**: Comprehensive document with all sections
- **JSON**: Structured data for processing
- **Markdown**: Clean, readable content

## Best Practices

### Search Strategy
- Start broad, then narrow down
- Use site operators for targeted searches
- Try multiple search engines if needed
- Set realistic limits (10-20 URLs usually sufficient)

### Performance
- Use `scrape_batch` for parallel processing (10x faster)
- Only use `deep` mode when necessary (much slower)
- Set appropriate timeouts
- Monitor success rates
- **Avoid token limits**: Batch 1-2 URLs at a time for large pages (Etsy, Amazon, etc.)

### Data Quality
- Always validate extracted data
- Cross-reference multiple sources
- Check for outliers and anomalies
- Normalize formats (dates, currencies, units)

### Error Handling
- Implement retry logic
- Have fallback strategies
- Log errors for debugging
- Don't fail on individual URL errors

### Ethical Considerations
- Respect robots.txt
- Don't overwhelm servers
- Rate limit requests
- Cite sources properly
- Don't misuse personal data

## Common Research Scenarios

### E-commerce Market Research

```
Query: "site:etsy.com nba merchandise"
Mode: standard
Extract: product name, price, rating, reviews, seller
Output: report
```

Expected: Price analysis, popular products, top sellers

### Price Comparison

```
Query: "iphone 15 pro max 256GB price comparison"
Mode: standard
Extract: retailer, price, availability, shipping
Output: json
```

Expected: Structured comparison with best deal identified

### Academic Research

```
Query: "machine learning in healthcare 2024 papers"
Mode: standard
Extract: title, authors, date, key findings, methodology
Output: report
```

Expected: Literature review with trends and insights

### Competitive Intelligence

```
Query: "competitor.com features pricing"
Mode: deep
Extract: feature name, description, pricing tier, availability
Output: report
```

Expected: Feature comparison, pricing analysis, recommendations

## Tool Reference

### search_engine
**Purpose**: Find relevant web pages
**Parameters**: query (required), engine (google/bing/yandex), cursor (page number)
**Returns**: SERP results in markdown

### scrape_as_markdown
**Purpose**: Get clean, AI-ready markdown
**Parameters**: url (required)
**Returns**: Formatted markdown without ads/clutter

### scrape_as_html
**Purpose**: Get raw HTML
**Parameters**: url (required)
**Returns**: Complete HTML document

### extract
**Purpose**: AI-powered structured data extraction
**Parameters**: url (required), extraction_prompt (optional)
**Returns**: JSON object with extracted data

### scrape_batch
**Purpose**: Process multiple URLs in parallel
**Parameters**: urls (array, max 10)
**Returns**: Array of page contents

### scraping_browser_navigate
**Purpose**: Navigate JavaScript-rendered pages
**Parameters**: url (required)
**Returns**: Page info (title, URL, status)

### scraping_browser_click
**Purpose**: Click elements on page
**Parameters**: selector (CSS selector)
**Returns**: Action result

### scraping_browser_links
**Purpose**: Get all links on current page
**Parameters**: None
**Returns**: Array of links with text, href, selector

## Troubleshooting

### No search results
- Try different search engine (bing, yandex)
- Simplify the query
- Check for typos
- Use broader search terms

### Scraping fails
- URL might be JavaScript-rendered → use `mode=deep`
- URL might be blocked → try alternative URL
- Check if URL is accessible in browser

### Extraction incomplete
- Provide more specific extraction prompt
- Check if data exists on page
- Try scraping as markdown first to see content

### Slow performance
- Reduce `max_results`
- Use `mode=standard` instead of `deep`
- Check network connectivity
- Close unnecessary browser sessions

### Token limit exceeded
- **Symptom**: "Output exceeds maximum allowed tokens" error
- **Cause**: Batch scraping too many large pages at once OR reading large files
- **Why this limit exists**: 
  - **Memory protection**: Prevents memory overflow from loading too much content
  - **Performance optimization**: Ensures fast response times
  - **Context management**: Preserves space for other content in the conversation
  - **System stability**: Prevents crashes or errors
- **Can this limit be increased?**: 
  - **No** - This is a hard system limit in Claude Code
  - **Cannot be changed** via configuration files
  - **Purpose**: Protect system stability and performance
- **Workarounds**: 
  - **For scraping**: Reduce batch size to 1-2 URLs for large pages
  - **For reading files**: Use `Read` with `offset` and `limit` to read in chunks
  - **For specific content**: Use `Grep` to search for specific patterns
  - **For finding files**: Use `Glob` to find files by pattern

## Additional Resources

### Reference Files

For detailed workflows and techniques:
- **`references/search-discovery.md`** - Search strategies and URL discovery
- **`references/content-scraping.md`** - Content collection methods
- **`references/data-extraction.md`** - Extraction schemas and validation
- **`references/deep-scraping.md`** - Browser automation techniques
- **`references/analysis-report.md`** - Analysis and report generation

### Example Files

Complete research examples:
- **`examples/market-research-etsy-nba.md`** - E-commerce market research
- **`examples/competitive-analysis-pricing.md`** - Price comparison workflow
- **`examples/academic-research-ml-healthcare.md`** - Academic literature review

## Limitations

- Requires Bright Data MCP server configuration
- Needs valid Bright Data API token
- Subject to API rate limits
- Browser automation is slower than direct scraping
- Some sites may still block access
- Quality depends on source content

## Progressive Disclosure

This SKILL.md provides core workflows and quick reference (approximately 2,000 words).

For detailed implementation patterns, advanced techniques, and comprehensive examples, consult the `references/` files which load as needed during research tasks.
