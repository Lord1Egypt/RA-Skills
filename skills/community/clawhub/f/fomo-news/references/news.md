# Breaking News

Aggregates RSS feeds from 14 major publications across 4 categories.

## Command

```bash
node fetch.mjs <category> [--limit <n>] [--json]
```

Where `<category>` is one of: `news` (all), `tech`, `ai`, `economics`, `politics`.

## Sources

### Tech
| Source | Feed URL |
|--------|----------|
| TechCrunch | `https://techcrunch.com/feed/` |
| Ars Technica | `https://feeds.arstechnica.com/arstechnica/index` |
| The Verge | `https://www.theverge.com/rss/index.xml` |
| Hacker News | `https://hnrss.org/frontpage` |
| Wired | `https://www.wired.com/feed/rss` |

### AI
| Source | Feed URL |
|--------|----------|
| MIT Tech Review AI | `https://www.technologyreview.com/feed/` |
| VentureBeat AI | `https://venturebeat.com/feed/` |

### Economics
| Source | Feed URL |
|--------|----------|
| Reuters Business | `https://www.rss.app/feeds/v1.1/tsYGKBcfOkSPYTXh.xml` |
| CNBC | `https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114` |
| MarketWatch | `https://www.marketwatch.com/rss/topstories` |

### Politics
| Source | Feed URL |
|--------|----------|
| Reuters World | `https://www.rss.app/feeds/v1.1/tsMZOAj38SjPLDn3.xml` |
| AP News | `https://rsshub.app/apnews/topics/politics` |
| BBC News | `https://feeds.bbci.co.uk/news/rss.xml` |
| NPR News | `https://feeds.npr.org/1001/rss.xml` |

## Output Fields

| Field | Description |
|-------|-------------|
| `source` | Publication name |
| `category` | tech, ai, economics, or politics |
| `title` | Article title |
| `link` | Article URL |
| `pubDate` | Publication date |
| `snippet` | Brief excerpt (max 300 chars) |
