# dfseo Backlinks Commands — Reference

Complete reference for all backlinks analysis commands.

**Note:** Backlinks API requires a **$100/month minimum commitment** to DataForSEO. All endpoints return results immediately (no polling needed).

**Target formats accepted:**
- `"example.com"` — domain root
- `"blog.example.com"` — subdomain
- `"https://example.com/page"` — specific URL

---

## `dfseo backlinks summary`

Get a comprehensive backlink profile overview for a target.

```
Usage: dfseo backlinks summary [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain or URL [required]

Options:
  --include-subdomains/--exclude-subdomains  Include subdomains [default: include-subdomains]
  --dofollow-only                            Only dofollow backlinks
  --status              TEXT                 Status: all, live, new, lost [default: all]
  --dry-run        -d                        Show estimated cost
  --fields         -f  TEXT                 Comma-separated fields to include
  --raw-params          TEXT                 Raw JSON payload
  --output         -o  TEXT                 Output format: json, table [default: auto]
  --login               TEXT                 DataForSEO login
  --password            TEXT                 DataForSEO password
  --verbose        -v                        Verbose output
```

**Examples:**

```bash
dfseo backlinks summary "example.com"
dfseo backlinks summary "example.com" --dofollow-only
dfseo backlinks summary "https://example.com/page"
```

**Output JSON:**

```json
{
  "target": "example.com",
  "rank": 245,
  "backlinks": 1420,
  "referring_domains": 312,
  "referring_main_domains": 280,
  "spam_score": 5,
  "broken_backlinks": 12,
  "links_summary": {
    "dofollow": 980,
    "nofollow": 440,
    "anchor": 1050,
    "image": 180
  },
  "cost": 0.02
}
```

---

## `dfseo backlinks list`

Get a detailed list of backlinks with full metadata.

```
Usage: dfseo backlinks list [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain or URL [required]

Options:
  --include-subdomains/--exclude-subdomains  Include subdomains [default: include-subdomains]
  --dofollow-only                            Only dofollow backlinks
  --status       TEXT     Status: all, live, new, lost, broken [default: live]
  --sort         TEXT     Sort: rank, page_from_rank, domain_from_rank, first_seen, last_seen [default: rank]
  --order        TEXT     Sort order: asc, desc [default: desc]
  --from-domain  TEXT     Filter by source domain
  --min-rank     INTEGER  Minimum backlink rank
  --limit    -n  INTEGER  Max results (max 1000) [default: 100]
  --offset       INTEGER  Offset for pagination [default: 0]
  --dry-run  -d           Show estimated cost
  --fields   -f  TEXT     Comma-separated fields to include
  --raw-params   TEXT     Raw JSON payload
  --output   -o  TEXT     Output format: json, table, csv [default: auto]
  --login        TEXT     DataForSEO login
  --password     TEXT     DataForSEO password
  --verbose  -v           Verbose output
```

**Examples:**

```bash
# Top dofollow backlinks
dfseo backlinks list "example.com" --dofollow-only --sort rank --limit 50

# New backlinks
dfseo backlinks list "example.com" --status new

# Lost backlinks
dfseo backlinks list "example.com" --status lost

# Broken backlinks
dfseo backlinks list "example.com" --status broken

# Links from a specific domain
dfseo backlinks list "example.com" --from-domain "techblog.com"
```

**Output JSON (per backlink):**

```json
{
  "domain_from": "techblog.it",
  "url_from": "https://techblog.it/article",
  "url_to": "https://example.com/page",
  "anchor": "example text",
  "rank": 185,
  "domain_from_rank": 310,
  "dofollow": true,
  "is_new": false,
  "is_lost": false,
  "first_seen": "2024-06-15T08:30:00Z",
  "last_seen": "2026-03-01T12:00:00Z",
  "spam_score": 2
}
```

---

## `dfseo backlinks anchors`

Analyze the distribution of anchor text used in backlinks.

```
Usage: dfseo backlinks anchors [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain or URL [required]

Options:
  --include-subdomains/--exclude-subdomains  Include subdomains [default: include-subdomains]
  --dofollow-only                            Only dofollow backlinks
  --search       TEXT     Search for text within anchor (substring match)
  --sort         TEXT     Sort by: backlinks, referring_domains [default: backlinks]
  --order        TEXT     Sort order: asc, desc [default: desc]
  --limit    -n  INTEGER  Max results [default: 100]
  --dry-run  -d           Show estimated cost
  --fields   -f  TEXT     Comma-separated fields to include
  --raw-params   TEXT     Raw JSON payload
  --output   -o  TEXT     Output format: json, table, csv [default: auto]
  --login        TEXT     DataForSEO login
  --password     TEXT     DataForSEO password
  --verbose  -v           Verbose output
```

**Examples:**

```bash
# All anchors sorted by count
dfseo backlinks anchors "example.com" --sort backlinks

# Search for brand anchors
dfseo backlinks anchors "example.com" --search "brand name" --sort backlinks

# Dofollow only
dfseo backlinks anchors "example.com" --dofollow-only --limit 20
```

---

## `dfseo backlinks referring-domains`

List all domains that link to the target.

```
Usage: dfseo backlinks referring-domains [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain or URL [required]

Options:
  --include-subdomains/--exclude-subdomains  Include subdomains [default: include-subdomains]
  --dofollow-only                            Only dofollow backlinks
  --min-backlinks  INTEGER  Minimum backlinks from a domain
  --sort           TEXT     Sort by: rank, backlinks [default: rank]
  --order          TEXT     Sort order: asc, desc [default: desc]
  --limit      -n  INTEGER  Max results [default: 100]
  --dry-run    -d           Show estimated cost
  --fields     -f  TEXT     Comma-separated fields to include
  --raw-params     TEXT     Raw JSON payload
  --output     -o  TEXT     Output format: json, table, csv [default: auto]
  --login          TEXT     DataForSEO login
  --password       TEXT     DataForSEO password
  --verbose    -v           Verbose output
```

**Examples:**

```bash
# Top referring domains by rank
dfseo backlinks referring-domains "example.com" --sort rank --limit 50

# Only domains with 5+ backlinks
dfseo backlinks referring-domains "example.com" --min-backlinks 5
```

---

## `dfseo backlinks history`

View backlink profile history over time (data from 2019 onwards). Accepts only domain names (not URLs).

```
Usage: dfseo backlinks history [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain [required] — domain only, not a URL

Options:
  --from     TEXT  Start date (YYYY-MM)
  --to       TEXT  End date (YYYY-MM)
  --dry-run  -d    Show estimated cost
  --fields   -f TEXT  Comma-separated fields to include
  --raw-params  TEXT  Raw JSON payload
  --output   -o TEXT  Output format: json, table, csv [default: auto]
  --login        TEXT  DataForSEO login
  --password     TEXT  DataForSEO password
  --verbose  -v        Verbose output
```

**Examples:**

```bash
# Full history
dfseo backlinks history "example.com"

# Specific date range
dfseo backlinks history "example.com" --from 2025-01 --to 2026-03
```

---

## `dfseo backlinks competitors`

Find domains that share a similar backlink profile with the target (likely competitors).

```
Usage: dfseo backlinks competitors [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain or URL [required]

Options:
  --include-subdomains/--exclude-subdomains  Include subdomains [default: include-subdomains]
  --sort      TEXT     Sort by: rank, backlinks, referring_domains [default: rank]
  --order     TEXT     Sort order: asc, desc [default: desc]
  --limit -n  INTEGER  Max results [default: 50]
  --dry-run -d         Show estimated cost
  --fields -f TEXT     Comma-separated fields to include
  --raw-params TEXT    Raw JSON payload
  --output -o TEXT     Output format: json, table, csv [default: auto]
  --login     TEXT     DataForSEO login
  --password  TEXT     DataForSEO password
  --verbose -v         Verbose output
```

**Example:**

```bash
dfseo backlinks competitors "example.com" --sort rank --limit 20
```

---

## `dfseo backlinks gap`

**Most powerful backlinks command.** Link gap analysis: find domains linking to competitors but NOT to your site. Essential for link building strategy.

The **first** target is your site. All subsequent targets are competitors (up to 20 total).

```
Usage: dfseo backlinks gap [OPTIONS] TARGETS...

Arguments:
  targets  TARGETS...  Your site first, then competitors [required]

Options:
  --mode         TEXT     Intersection mode: domain, page [default: domain]
  --exclude      TEXT     Domains to exclude from results (repeatable)
  --dofollow-only         Only dofollow backlinks
  --min-rank     INTEGER  Minimum domain rank
  --sort         TEXT     Sort by: rank, backlinks [default: rank]
  --order        TEXT     Sort order: asc, desc [default: desc]
  --limit    -n  INTEGER  Max results [default: 100]
  --dry-run  -d           Show estimated cost
  --fields   -f  TEXT     Comma-separated fields to include
  --raw-params   TEXT     Raw JSON payload
  --output   -o  TEXT     Output format: json, table, csv [default: auto]
  --login        TEXT     DataForSEO login
  --password     TEXT     DataForSEO password
  --verbose  -v           Verbose output
```

**Examples:**

```bash
# Find domains linking to competitors but not to you
dfseo backlinks gap "your-site.com" "competitor1.com" "competitor2.com"

# With filters — only high-authority, dofollow links
dfseo backlinks gap "your-site.com" "competitor.com" --min-rank 200 --dofollow-only

# Page-level intersection
dfseo backlinks gap "your-site.com" "competitor.com" --mode page

# Exclude spam domains
dfseo backlinks gap "your-site.com" "competitor.com" --exclude "spam-domain.com"
```

---

## `dfseo backlinks pages`

List the pages on the target that have the most backlinks.

```
Usage: dfseo backlinks pages [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain or URL [required]

Options:
  --include-subdomains/--exclude-subdomains  Include subdomains [default: include-subdomains]
  --sort      TEXT     Sort by: backlinks, rank, referring_domains [default: backlinks]
  --order     TEXT     Sort order: asc, desc [default: desc]
  --limit -n  INTEGER  Max results [default: 50]
  --output -o TEXT     Output format: json, table, csv [default: auto]
  --login     TEXT     DataForSEO login
  --password  TEXT     DataForSEO password
  --verbose -v         Verbose output
```

**Example:**

```bash
dfseo backlinks pages "example.com" --sort backlinks --limit 20
```

---

## `dfseo backlinks bulk` — Bulk Operations

Compare backlink metrics for up to 1000 targets at once.

### `dfseo backlinks bulk ranks`

Get domain rank and page rank for multiple targets.

```
Usage: dfseo backlinks bulk ranks [OPTIONS] [TARGETS]...

Arguments:
  targets  [TARGETS]...  Target domains/URLs to analyze

Options:
  --from-file  -f  TEXT  Read targets from file (one per line)
  --output     -o  TEXT  Output format: json, table, csv [default: auto]
  --login          TEXT  DataForSEO login
  --password       TEXT  DataForSEO password
  --verbose    -v        Verbose output
```

```bash
dfseo backlinks bulk ranks "site1.com" "site2.com" "site3.com"
dfseo backlinks bulk ranks --from-file domains.txt
```

### `dfseo backlinks bulk backlinks`

Get backlink count for multiple targets.

```bash
dfseo backlinks bulk backlinks "site1.com" "site2.com"
dfseo backlinks bulk backlinks --from-file domains.txt
```

### `dfseo backlinks bulk spam-score`

Get spam scores for multiple targets.

```bash
dfseo backlinks bulk spam-score "site1.com" "site2.com"
dfseo backlinks bulk spam-score --from-file domains.txt
```

### `dfseo backlinks bulk referring-domains`

Get referring domain count for multiple targets.

```bash
dfseo backlinks bulk referring-domains --from-file domains.txt
```

### `dfseo backlinks bulk new-lost`

Get new and lost backlink counts for multiple targets since a date.

```
Options:
  --from-file  -f  TEXT  Read targets from file
  --from-date      TEXT  Start date (YYYY-MM-DD)
  --output     -o  TEXT  Output format
```

```bash
dfseo backlinks bulk new-lost --from-file domains.txt --from-date 2025-09-01
```

**All bulk commands share these options:**
- `--from-file / -f` — file with one target per line (max 1000)
- `--output / -o` — json, table, csv
- `--login`, `--password`, `--verbose`
