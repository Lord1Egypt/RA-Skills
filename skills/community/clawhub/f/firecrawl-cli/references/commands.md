# Firecrawl CLI Command Reference

## Authentication
```bash
firecrawl login                          # Interactive login
firecrawl login --browser                # Browser auth (recommended for agents)
firecrawl login --api-key fc-YOUR-KEY    # Direct API key
export FIRECRAWL_API_KEY=fc-YOUR-KEY     # Env var
firecrawl view-config                    # Show config/auth status
firecrawl logout                         # Clear credentials
firecrawl --status                       # Check auth + rate limits + credits
```

Self-hosted: `firecrawl --api-url http://localhost:3002 scrape https://example.com`  
Or: `export FIRECRAWL_API_URL=http://localhost:3002`  
Custom API URL skips key auth automatically.

---

## Scrape
```bash
firecrawl https://example.com                          # Default markdown
firecrawl scrape https://example.com
firecrawl https://example.com --only-main-content      # Clean output (recommended)
firecrawl https://example.com --html
firecrawl https://example.com --format markdown,links  # Multiple → JSON
firecrawl https://example.com --format images
firecrawl https://example.com --format summary
firecrawl https://example.com --wait-for 3000          # Wait for JS rendering
firecrawl https://example.com --screenshot
firecrawl https://example.com --include-tags article,main
firecrawl https://example.com --exclude-tags nav,footer
firecrawl https://example.com -o output.md             # Save to file
firecrawl https://example.com --json                   # Force JSON
firecrawl https://example.com --pretty                 # Pretty print JSON
firecrawl https://example.com --timing                 # Show request timing
```

Formats: `markdown`, `html`, `rawHtml`, `links`, `screenshot`, `json`, `images`, `summary`, `changeTracking`, `attributes`, `branding`

---

## Search
```bash
firecrawl search "query"
firecrawl search "AI news" --limit 10
firecrawl search "AI" --sources web,news,images
firecrawl search "react hooks" --categories github
firecrawl search "tech news" --tbs qdr:h    # Last hour (d=day, w=week, m=month, y=year)
firecrawl search "restaurants" --location "Berlin,Germany" --country DE
firecrawl search "docs" --scrape --scrape-formats markdown
firecrawl search "firecrawl" --pretty -o results.json
```

---

## Map (URL Discovery)
```bash
firecrawl map https://example.com
firecrawl map https://example.com --limit 500
firecrawl map https://example.com --search "blog"
firecrawl map https://example.com --include-subdomains
firecrawl map https://example.com --sitemap include   # include | skip | only
firecrawl map https://example.com --ignore-query-parameters
firecrawl map https://example.com --wait --timeout 60
firecrawl map https://example.com -o urls.txt
```

---

## Crawl
```bash
firecrawl crawl https://example.com                    # Returns job ID immediately
firecrawl crawl https://example.com --wait             # Wait for completion
firecrawl crawl https://example.com --wait --progress  # With progress indicator
firecrawl crawl <job-id>                               # Check status
firecrawl crawl https://example.com --limit 100 --max-depth 3 --wait
firecrawl crawl https://example.com --include-paths /blog,/docs --wait
firecrawl crawl https://example.com --exclude-paths /admin,/login --wait
firecrawl crawl https://example.com --allow-subdomains --wait
firecrawl crawl https://example.com --crawl-entire-domain --wait
firecrawl crawl https://example.com --delay 1000 --max-concurrency 2 --wait
firecrawl crawl https://example.com --wait --pretty -o results.json
```

---

## Browser (Cloud Sandbox)
```bash
firecrawl browser launch-session
firecrawl browser launch-session --ttl 600 --stream
firecrawl browser launch-session --ttl 120 --ttl-inactivity 60
firecrawl browser launch-session --profile myprofile   # Save/reuse browser state

# agent-browser commands (recommended for AI agents — auto-prefixed)
firecrawl browser execute "open https://example.com"
firecrawl browser execute "snapshot"       # Returns @ref IDs
firecrawl browser execute "click @e5"
firecrawl browser execute "fill @e3 'query'"
firecrawl browser execute "scrape"
firecrawl browser execute --bash "agent-browser --help"   # 40+ commands

# Playwright Python
firecrawl browser execute --python 'await page.goto("https://example.com"); print(await page.title())'

# Playwright JavaScript
firecrawl browser execute --node 'await page.goto("https://example.com"); console.log(await page.title());'

firecrawl browser list                     # List all sessions
firecrawl browser list active --json
firecrawl browser close                    # Close active session
firecrawl browser close --session <id>
```

---

## Agent (NL Web Queries)
```bash
firecrawl agent "Find top 5 AI startups and funding" --wait
firecrawl agent "Compare pricing" --urls https://slack.com/pricing,https://teams.microsoft.com/pricing --wait
firecrawl agent "Get company info" --urls https://example.com --schema '{"name":"string","founded":"number"}' --wait
firecrawl agent "Get product details" --urls https://example.com --schema-file schema.json --wait
firecrawl agent "Research" --model spark-1-pro --wait   # Higher accuracy (spark-1-mini is default/cheaper)
firecrawl agent "Gather contacts" --max-credits 100 --wait
firecrawl agent <job-id> --status          # Check existing job
```

---

## Credit Usage & Version
```bash
firecrawl credit-usage
firecrawl credit-usage --json --pretty
firecrawl version
firecrawl --version
```

---

## Global Options
`--api-key <key>` · `--api-url <url>` · `--status` · `--help` · `--version`

---

## Output & Piping
```bash
firecrawl https://example.com | head -50
firecrawl https://example.com > output.md
firecrawl https://example.com --format markdown,links --pretty -o data.json
firecrawl map https://example.com | wc -l
firecrawl https://example.com --format links | jq '.links[].url'
```

Single format → raw content. Multiple formats → JSON.

## Telemetry
Disable: `export FIRECRAWL_NO_TELEMETRY=1`  
Collects: CLI version, OS, Node version, dev tool detection only. No URLs or content.
