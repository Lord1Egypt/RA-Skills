# Web Search Reference

Complete reference for web search operations via `bdata search`.

## Command Syntax

```bash
bdata search "<query>" [options]
```

## All Options

| Flag | Description | Default |
|------|-------------|---------|
| `--engine <name>` | Search engine: `google`, `bing`, `yandex` | `google` |
| `--country <code>` | ISO country code for localized results | *(none)* |
| `--language <code>` | Language code (e.g. `en`, `fr`, `de`) | *(none)* |
| `--page <n>` | Page number, 0-indexed | `0` |
| `--type <type>` | `web`, `news`, `images`, `shopping` | `web` |
| `--device <type>` | `desktop`, `mobile` | `desktop` |
| `--zone <name>` | SERP zone name | stored default |
| `-o, --output <path>` | Write output to file | stdout |
| `--json` | Force JSON output | *(off)* |
| `--pretty` | Pretty-print JSON | *(off)* |

## Output Structure (Google JSON)

```json
{
  "organic": [
    {
      "link": "https://example.com/page",
      "title": "Page Title",
      "description": "Snippet from the page..."
    }
  ],
  "paid": [
    {
      "link": "https://ad.example.com",
      "title": "Ad Title",
      "description": "Ad description..."
    }
  ],
  "people_also_ask": [
    "Related question 1?",
    "Related question 2?"
  ],
  "related_searches": [
    "related term 1",
    "related term 2"
  ]
}
```

Bing and Yandex return **markdown** by default (not structured JSON).

## Search Patterns

### Basic Search
```bash
bdata search "best CI/CD tools for startups"
```

### Research Deep Dive (multi-page)
```bash
# Page 1
bdata search "kubernetes vs docker swarm 2026" --json

# Page 2
bdata search "kubernetes vs docker swarm 2026" --json --page 1

# Page 3
bdata search "kubernetes vs docker swarm 2026" --json --page 2
```

### Localized Search
```bash
# German results about restaurants in Berlin
bdata search "beste restaurants" --country de --language de

# Japanese tech news
bdata search "AI technology" --country jp --language ja
```

### News Search
```bash
bdata search "OpenAI announcements" --type news --json
```

### Shopping Search
```bash
bdata search "wireless noise cancelling headphones" --type shopping --json
```

### Mobile Results
```bash
bdata search "responsive design testing" --device mobile --json
```

### Cross-Engine Comparison
```bash
# Compare results across engines
bdata search "best web scraping tools" --engine google --json -o google.json
bdata search "best web scraping tools" --engine bing --json -o bing.json
```

## Pipeline Patterns

### Search → Scrape (most common research pattern)
```bash
# Find relevant pages, then read them
bdata search "react server components tutorial" --json \
  | jq -r '.organic[0].link' \
  | xargs bdata scrape
```

### Search → Extract URLs
```bash
# Get all result URLs
bdata search "fintech startups 2026" --json | jq -r '.organic[].link'
```

### Search → Batch Scrape Top N
```bash
# Scrape top 3 results
bdata search "kubernetes security best practices" --json \
  | jq -r '.organic[:3][].link' \
  | xargs -I{} bdata scrape {} --json -o "results/{}.json"
```

### Search → Filter by Domain
```bash
# Only results from specific domains
bdata search "site:github.com web scraping framework" --json
```

## Tips

- **Quote the query**: Always wrap the search query in quotes to handle spaces and special characters.
- **Use `--json` for programmatic use**: The default human-readable table is for quick inspection only.
- **Google gives the richest output**: Structured JSON with organic, paid, PAA, and related searches. Bing/Yandex return markdown.
- **Pagination is 0-indexed**: `--page 0` is the first page (default), `--page 1` is the second.
- **Combine with jq**: The JSON output pipes cleanly to `jq` for filtering, mapping, and extraction.
