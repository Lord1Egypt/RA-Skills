# dfseo SERP Commands — Reference

Complete reference for all SERP-related commands.

## `dfseo serp google`

Search Google organic results in real-time.

```
Usage: dfseo serp google [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Search keyword [required]

Options:
  --location  -l  TEXT     Location name (e.g., 'Italy', 'United States')
  --language  -L  TEXT     Language name (e.g., 'Italian', 'English')
  --device    -d  TEXT     Device type: desktop or mobile
  --os            TEXT     Operating system: windows, macos, ios, android
  --depth     -n  INTEGER  Number of results to fetch (max 700) [default: 100]
  --fields    -f  TEXT     Comma-separated fields to include in output
  --raw-params    TEXT     Raw JSON payload — bypasses all other flags
  --dry-run               Show estimated cost without executing
  --output    -o  TEXT     Output format: json, json-pretty, table, csv [default: auto]
  --features-only         Show only SERP features (no organic results)
  --raw                   Output raw API response without parsing
  --login         TEXT     DataForSEO login (overrides config)
  --password      TEXT     DataForSEO password (overrides config)
  --verbose   -v           Verbose output on stderr
  --quiet     -q           Suppress non-error output
```

**Examples:**

```bash
# Basic search
dfseo serp google "email hosting provider"

# With location and language
dfseo serp google "email hosting" --location "Italy" --language "Italian"

# Mobile search
dfseo serp google "keyword" --device mobile --os android

# Get top 50 results as JSON for piping
dfseo serp google "keyword" --depth 50 -q | jq '.organic_results[0].url'

# Only SERP features (featured snippet, PAA, etc.)
dfseo serp google "what is DKIM" --features-only

# Force table output
dfseo serp google "keyword" --output table
```

**Output JSON structure:**

```json
{
  "keyword": "email hosting",
  "location": "Italy",
  "language": "Italian",
  "device": "desktop",
  "results_count": 100,
  "serp_features": ["featured_snippet", "people_also_ask"],
  "organic_results": [
    {
      "rank": 1,
      "rank_group": 1,
      "domain": "example.com",
      "url": "https://example.com/email",
      "title": "Best Email Hosting 2026",
      "description": "Compare providers...",
      "breadcrumb": "example.com › email"
    }
  ],
  "featured_snippet": {
    "text": "...",
    "source_url": "...",
    "source_domain": "..."
  },
  "people_also_ask": [
    {"question": "...", "expanded_text": "..."}
  ],
  "cost": 0.002,
  "timestamp": "2026-03-14T10:00:00Z"
}
```

---

## `dfseo serp bing`

Search Bing organic results.

```
Usage: dfseo serp bing [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Search keyword [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --device    -d  TEXT     Device type: desktop or mobile
  --depth     -n  INTEGER  Number of results (max 700) [default: 100]
  --fields    -f  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo serp bing "email hosting" --location "Italy" --language "Italian"
```

---

## `dfseo serp youtube`

Search YouTube results.

```
Usage: dfseo serp youtube [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Search keyword [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --device    -d  TEXT     Device type
  --depth     -n  INTEGER  Number of results [default: 100]
  --fields    -f  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo serp youtube "email marketing tutorial" --depth 20
```

---

## `dfseo serp compare`

Compare SERP results across multiple search engines. Shows common domains, unique domains per engine, and ranking differences.

```
Usage: dfseo serp compare [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Search keyword [required]

Options:
  --engines  -e  TEXT     Engines to compare (comma-separated) [default: google,bing]
  --location -l  TEXT     Location name
  --language -L  TEXT     Language name
  --device   -d  TEXT     Device type
  --depth    -n  INTEGER  Number of results per engine [default: 50]
  --fields   -f  TEXT     Comma-separated fields to include
  --dry-run              Show estimated cost
  --output   -o  TEXT     Output format [default: table]
  --login        TEXT     DataForSEO login
  --password     TEXT     DataForSEO password
  --verbose  -v           Verbose output
```

**Example:**

```bash
dfseo serp compare "email hosting" --engines google,bing --location "Italy"
```

---

## `dfseo serp locations`

List all available location codes for targeting.

```
Usage: dfseo serp locations [OPTIONS]

Options:
  --search  -s  TEXT  Filter locations by name
  --output  -o  TEXT  Output format [default: table]
  --login       TEXT  DataForSEO login
  --password    TEXT  DataForSEO password
  --verbose -v        Verbose output
```

**Examples:**

```bash
# Search for a location
dfseo serp locations --search "italy"

# Get all as JSON
dfseo serp locations --output json
```

---

## `dfseo serp languages`

List all available language codes.

```
Usage: dfseo serp languages [OPTIONS]

Options:
  --search  -s  TEXT  Filter languages by name
  --output  -o  TEXT  Output format [default: table]
  --login       TEXT  DataForSEO login
  --password    TEXT  DataForSEO password
  --verbose -v        Verbose output
```

**Example:**

```bash
dfseo serp languages --search "ital"
```

---

## `dfseo auth setup`

Set up DataForSEO credentials interactively. Saves to `~/.config/dfseo/config.toml`.

```
Usage: dfseo auth setup [OPTIONS]

Options:
  --login     TEXT  DataForSEO login email
  --password  TEXT  DataForSEO API password
  --verbose   -v    Verbose output
```

---

## `dfseo auth status`

Check authentication status and account balance.

```
Usage: dfseo auth status [OPTIONS]

Options:
  --login     TEXT  DataForSEO login (overrides config)
  --password  TEXT  DataForSEO password (overrides config)
  --output -o TEXT  Output format [default: json]
  --verbose   -v    Verbose output
```

**Example:**

```bash
dfseo auth status
# → {"login": "you@email.com", "balance": 42.50, "rate_limit": 2000}
```

---

## `dfseo config set`

Set a default configuration value. Persisted to `~/.config/dfseo/config.toml`.

```
Usage: dfseo config set [OPTIONS] KEY VALUE

Arguments:
  key    TEXT  Configuration key: location, language, device, output [required]
  value  TEXT  Configuration value [required]
```

**Examples:**

```bash
dfseo config set location "Italy"
dfseo config set language "Italian"
dfseo config set device desktop
dfseo config set output json
```

---

## `dfseo config show`

Show current configuration.

```
Usage: dfseo config show [OPTIONS]

Options:
  --output  -o  TEXT  Output format [default: json]
```
