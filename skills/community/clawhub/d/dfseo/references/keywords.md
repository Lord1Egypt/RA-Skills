# dfseo Keywords Commands — Reference

Complete reference for all keyword research commands.

## `dfseo keywords volume`

Get search volume, CPC, competition, keyword difficulty, and search intent for up to 700 keywords at once.

```
Usage: dfseo keywords volume [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to analyze (max 700)

Options:
  --location         -l  TEXT  Location name (e.g., 'Italy')
  --language         -L  TEXT  Language name (e.g., 'Italian')
  --include-serp-info        Include SERP data (featured snippets, PAA count)
  --from-file        -f  TEXT  Read keywords from file (one per line)
  --fields           -F  TEXT  Comma-separated fields to include in output
  --raw-params           TEXT  Raw JSON payload (bypasses all other flags)
  --dry-run                   Show estimated cost without executing
  --output           -o  TEXT  Output format: json, table, csv
  --login                TEXT  DataForSEO login
  --password             TEXT  DataForSEO password
  --verbose          -v        Verbose output
```

**Examples:**

```bash
# Single keyword
dfseo keywords volume "email hosting" --location "Italy"

# Multiple keywords
dfseo keywords volume "email hosting" "smtp provider" "email server" --location "Italy"

# From file with SERP data
dfseo keywords volume --from-file keywords.txt --include-serp-info

# Pipe to jq
dfseo keywords volume "email hosting" -q | jq '.[0].search_volume'
```

**Output JSON (per keyword):**

```json
{
  "keyword": "email hosting",
  "search_volume": 4400,
  "cpc": 2.15,
  "competition": 0.72,
  "keyword_difficulty": 68,
  "search_intent": "commercial",
  "monthly_searches": [
    {"year": 2026, "month": 2, "search_volume": 4200},
    {"year": 2026, "month": 1, "search_volume": 4600}
  ]
}
```

---

## `dfseo keywords suggestions`

Find long-tail keywords that contain your seed keyword. Great for finding specific, lower-competition variants.

```
Usage: dfseo keywords suggestions [OPTIONS] KEYWORD

Arguments:
  keyword  TEXT  Seed keyword [required]

Options:
  --location        -l  TEXT     Location name
  --language        -L  TEXT     Language name
  --limit           -n  INTEGER  Max results (max 1000) [default: 50]
  --min-volume          INTEGER  Minimum search volume filter
  --max-volume          INTEGER  Maximum search volume filter
  --min-difficulty      INTEGER  Minimum keyword difficulty (0-100)
  --max-difficulty      INTEGER  Maximum keyword difficulty (0-100)
  --include-seed                 Include the seed keyword in results
  --sort                TEXT     Sort by: relevance, volume, cpc, difficulty [default: relevance]
  --order               TEXT     Sort order: asc, desc [default: desc]
  --fields          -F  TEXT     Comma-separated fields to include
  --raw-params          TEXT     Raw JSON payload
  --dry-run                      Show estimated cost
  --output          -o  TEXT     Output format [default: auto]
  --login               TEXT     DataForSEO login
  --password            TEXT     DataForSEO password
  --verbose         -v           Verbose output
```

**Examples:**

```bash
# Long-tail keywords with filters
dfseo keywords suggestions "email hosting" \
  --location "Italy" --language "Italian" \
  --min-volume 100 --max-difficulty 40 --limit 50

# Sort by volume
dfseo keywords suggestions "smtp server" --sort volume --limit 100
```

---

## `dfseo keywords ideas`

Find semantically related keywords — not just those containing the seed. Uses DataForSEO's semantic analysis to find associated concepts.

```
Usage: dfseo keywords ideas [OPTIONS] KEYWORDS...

Arguments:
  keywords  KEYWORDS...  Seed keywords (max 20) [required]

Options:
  --location        -l  TEXT     Location name
  --language        -L  TEXT     Language name
  --limit           -n  INTEGER  Max results [default: 100]
  --min-volume          INTEGER  Minimum search volume
  --max-volume          INTEGER  Maximum search volume
  --min-difficulty      INTEGER  Minimum keyword difficulty
  --max-difficulty      INTEGER  Maximum keyword difficulty
  --sort                TEXT     Sort by: relevance, volume, cpc, difficulty [default: relevance]
  --order               TEXT     Sort order: asc, desc [default: desc]
  --fields          -F  TEXT     Comma-separated fields to include
  --raw-params          TEXT     Raw JSON payload
  --dry-run                      Show estimated cost
  --output          -o  TEXT     Output format [default: auto]
  --login               TEXT     DataForSEO login
  --password            TEXT     DataForSEO password
  --verbose         -v           Verbose output
```

**Example:**

```bash
dfseo keywords ideas "email hosting" "smtp service" \
  --location "Italy" --limit 100 --min-volume 50
```

---

## `dfseo keywords difficulty`

Get keyword difficulty score (0-100) for up to 1000 keywords at once. Useful for bulk analysis of content opportunities.

```
Usage: dfseo keywords difficulty [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to analyze (max 1000)

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --from-file -f  TEXT  Read keywords from file (one per line)
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Examples:**

```bash
# Inline keywords
dfseo keywords difficulty "email hosting" "smtp server" --location "Italy"

# From file (up to 1000 keywords)
dfseo keywords difficulty --from-file candidates.txt --location "Italy"
```

**Difficulty levels:** 0-14 easy, 15-29 medium, 30-49 difficult, 50-69 hard, 70-84 very hard, 85-100 super hard.

---

## `dfseo keywords search-intent`

Classify the search intent for up to 1000 keywords. Intent categories: informational, navigational, commercial, transactional.

```
Usage: dfseo keywords search-intent [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to classify (max 1000)

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --from-file -f  TEXT  Read keywords from file
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Example:**

```bash
dfseo keywords search-intent "buy hosting" "what is smtp" "gmail login" "best email server"
```

**Output (per keyword):**

```json
{"keyword": "buy hosting", "search_intent": "transactional", "secondary_intents": ["commercial"]}
```

---

## `dfseo keywords for-site`

Find keywords that a specific domain is ranking for. Useful for competitor keyword analysis.

```
Usage: dfseo keywords for-site [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain (e.g., example.com) [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --limit     -n  INTEGER  Max results [default: 100]
  --min-volume    INTEGER  Minimum search volume
  --max-volume    INTEGER  Maximum search volume
  --sort          TEXT     Sort by: relevance, volume, cpc, difficulty [default: relevance]
  --order         TEXT     Sort order: asc, desc [default: desc]
  --fields    -F  TEXT     Comma-separated fields to include
  --raw-params    TEXT     Raw JSON payload
  --dry-run               Show estimated cost
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo keywords for-site "competitor.com" \
  --location "Italy" --min-volume 100 --sort volume --limit 200
```

---

## `dfseo keywords ads-volume`

Get pure Google Ads search volume data (different from organic volume). Max 20 keywords per request. Rate limit: 12 requests/minute.

```
Usage: dfseo keywords ads-volume [OPTIONS] [KEYWORDS]...

Arguments:
  keywords  [KEYWORDS]...  Keywords to analyze (max 20)

Options:
  --location  -l  TEXT  Location name
  --language  -L  TEXT  Language name
  --date-from     TEXT  Start date for historical data (YYYY-MM)
  --date-to       TEXT  End date for historical data (YYYY-MM)
  --from-file -f  TEXT  Read keywords from file
  --fields    -F  TEXT  Comma-separated fields to include
  --raw-params    TEXT  Raw JSON payload
  --dry-run           Show estimated cost
  --output    -o  TEXT  Output format [default: auto]
  --login         TEXT  DataForSEO login
  --password      TEXT  DataForSEO password
  --verbose   -v        Verbose output
```

**Example:**

```bash
dfseo keywords ads-volume "email hosting" "smtp provider" --location "Italy"
```

---

## `dfseo keywords ads-suggestions`

Get keyword suggestions from Google Ads. Max 20 seed keywords. Rate limit: 12 requests/minute.

```
Usage: dfseo keywords ads-suggestions [OPTIONS] KEYWORDS...

Arguments:
  keywords  KEYWORDS...  Seed keywords (max 20) [required]

Options:
  --location  -l  TEXT     Location name
  --language  -L  TEXT     Language name
  --limit     -n  INTEGER  Max results [default: 100]
  --output    -o  TEXT     Output format [default: auto]
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Example:**

```bash
dfseo keywords ads-suggestions "email hosting" "smtp" --location "Italy" --limit 100
```
