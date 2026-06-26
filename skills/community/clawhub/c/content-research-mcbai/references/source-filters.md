# Source Filters Reference

Detailed configuration for each research source filter.

## Filter Definitions

### All Sources (`all`)
- Web search: No additional query modifier
- News search: Also executed (past week freshness)
- Returns: Mixed results from all sources, news prioritized

### News Only (`news`)
- Web search: Standard query
- News search: Also executed with priority
- Returns: News articles prioritized, web results as supplement
- Best for: Breaking news, funding announcements, product launches

### LinkedIn (`linkedin`)
- Web search: Append `site:linkedin.com` to query
- News search: Not executed
- Returns: LinkedIn posts, articles, and profiles
- Best for: Thought leadership, industry commentary, professional insights

### YouTube (`youtube`)
- Web search: Append `site:youtube.com` to query
- News search: Not executed
- Returns: YouTube videos, channels
- Best for: Tutorials, interviews, conference talks, demos

### Blogs & Articles (`blogs`)
- Web search: Append `blog OR article OR guide` to query
- News search: Not executed
- Returns: Blog posts, long-form articles, guides
- Best for: Deep dives, how-to content, opinion pieces, technical guides

## Auto-Tag Patterns

Tags are applied based on regex matching against title + summary text:

| Tag | Regex Pattern |
|-----|--------------|
| Funding | `/fund\|raise\|round\|series [a-c]\|seed\|valuation\|invest\|vc\|venture/i` |
| AI | `/\bai\b\|artificial intelligence\|machine learning\|llm\|gpt\|claude\|openai/i` |
| SaaS | `/\bsaas\b\|software as a service\|subscription\|arr\|mrr/i` |
| Tools | `/tool\|platform\|app\|software\|stack\|framework/i` |
| Trends | `/trend\|report\|survey\|data\|statistic\|forecast\|prediction/i` |
| Startup | `/startup\|founder\|launch\|accelerator\|incubator\|yc\|y combinator/i` |
| Growth | `/growth\|marketing\|gtm\|acquisition\|retention\|conversion/i` |

Tags are matched in order — the first match wins. This prevents over-tagging.

## Known Domain Mappings

When extracting source names from URLs, these domains get special display names:

| Domain | Display Name |
|--------|-------------|
| techcrunch.com | TechCrunch |
| crunchbase.com | Crunchbase |
| forbes.com | Forbes |
| bloomberg.com | Bloomberg |
| reuters.com | Reuters |
| cnbc.com | CNBC |
| venturebeat.com | VentureBeat |
| theverge.com | The Verge |
| wired.com | Wired |
| sifted.eu | Sifted |
| pitchbook.com | PitchBook |
| the-information.com | The Information |
| axios.com | Axios |
| businessinsider.com | Business Insider |
| linkedin.com | LinkedIn |

For unlisted domains, capitalize the first letter of the cleaned hostname.

## Freshness Settings

| Search Type | Default Freshness | Description |
|-------------|------------------|-------------|
| Web Search | Past month (`pm`) | Broad enough to find quality content |
| News Search | Past week (`pw`) | News is time-sensitive |

## Sorting Algorithm

Results are sorted with this priority:
1. **News articles first** — they're fresher and more newsworthy
2. **By age within category** — most recent first
3. **Age parsing**: "2 hours ago" → 2h, "3 days ago" → 72h, "1 week ago" → 168h, "1 month ago" → 720h

