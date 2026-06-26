# dfseo Site Audit Commands — Reference

Complete reference for all site audit (On-Page API) commands.

**Note:** Most site audit commands are two-step:
1. Start crawl → get `task_id`
2. Retrieve results using `task_id`

`dfseo site audit` combines both steps automatically.

---

## `dfseo site audit`

All-in-one audit: starts a crawl, waits for completion, and returns the summary. Uses Instant Pages API automatically for single URLs.

```
Usage: dfseo site audit [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain or URL to audit [required]

Options:
  --max-pages         -n  INTEGER  Maximum pages to crawl [default: 100]
  --enable-javascript              Execute JavaScript (costs extra)
  --load-resources                 Load images, CSS, JS (costs extra)
  --enable-browser-rendering       Full browser rendering (costs extra)
  --start-url             TEXT     Starting URL (default: homepage)
  --respect-sitemap/--ignore-sitemap  Follow sitemap.xml [default: respect-sitemap]
  --wait/-w/--no-wait              Wait for completion [default: wait]
  --timeout               INTEGER  Timeout in seconds [default: 300]
  --poll-interval         INTEGER  Seconds between progress checks [default: 10]
  --dry-run          -d            Show estimated cost without executing
  --fields           -f  TEXT     Comma-separated fields to include
  --output           -o  TEXT     Output format: json, table
  --login                TEXT     DataForSEO login
  --password             TEXT     DataForSEO password
  --verbose          -v            Verbose output
```

**Examples:**

```bash
# Full audit (waits for completion)
dfseo site audit "example.com" --max-pages 100

# Quick audit with JavaScript
dfseo site audit "example.com" --max-pages 50 --enable-javascript

# Non-blocking (returns task_id immediately)
TASK_ID=$(dfseo site audit "example.com" --no-wait -q | jq -r '.task_id')
```

---

## `dfseo site instant`

Live instant analysis of a single URL with no polling. Faster than a full crawl for single-page checks.

```
Usage: dfseo site instant [OPTIONS] URL

Arguments:
  url  TEXT  URL to analyze [required]

Options:
  --enable-javascript,--js  Execute JavaScript
  --load-resources          Load resources (images, CSS, JS)
  --output        -o  TEXT  Output format: json, table
  --login             TEXT  DataForSEO login
  --password          TEXT  DataForSEO password
  --verbose       -v        Verbose output
```

**Example:**

```bash
dfseo site instant "https://example.com/blog/post"
dfseo site instant "https://example.com" --js --load-resources
```

---

## `dfseo site crawl`

Start a site crawl and return `task_id` immediately (non-blocking). Use with `dfseo site summary` to check progress.

```
Usage: dfseo site crawl [OPTIONS] TARGET

Arguments:
  target  TEXT  Target domain or URL to crawl [required]

Options:
  --max-pages          -n  INTEGER  Maximum pages to crawl [default: 100]
  --enable-javascript               Execute JavaScript
  --load-resources                  Load images, CSS, JS
  --enable-browser-rendering        Full browser rendering
  --start-url              TEXT     Starting URL (default: homepage)
  --respect-sitemap/--ignore-sitemap  Follow sitemap.xml [default: respect-sitemap]
  --output             -o  TEXT     Output format: json, table
  --login                  TEXT     DataForSEO login
  --password               TEXT     DataForSEO password
  --dry-run                         Show estimated cost
  --fields             -f  TEXT     Comma-separated fields to include
  --verbose            -v           Verbose output
```

**Example:**

```bash
# Start crawl, save task_id
TASK_ID=$(dfseo site crawl "example.com" --max-pages 500 -q | jq -r '.task_id')

# Check status later
dfseo site summary "$TASK_ID"
```

---

## `dfseo site summary`

Get crawl summary and status for a task.

```
Usage: dfseo site summary [OPTIONS] TASK_ID

Arguments:
  task_id  TEXT  Task ID from crawl command [required]

Options:
  --wait        -w           Wait for completion if still crawling
  --timeout         INTEGER  Timeout in seconds for waiting [default: 300]
  --poll-interval   INTEGER  Seconds between progress checks [default: 10]
  --output      -o  TEXT     Output format: json, table
  --login           TEXT     DataForSEO login
  --password        TEXT     DataForSEO password
  --verbose     -v           Verbose output
```

**Example:**

```bash
# Check status
dfseo site summary "$TASK_ID"

# Wait for completion
dfseo site summary "$TASK_ID" --wait --timeout 600
```

---

## `dfseo site pages`

List crawled pages with SEO metrics and check results.

```
Usage: dfseo site pages [OPTIONS] TASK_ID

Arguments:
  task_id  TEXT  Task ID from crawl command [required]

Options:
  --errors-only           Only pages with errors
  --status-code  INTEGER  Filter by HTTP status code (e.g., 404)
  --type         TEXT     Filter by type: html, image, script, stylesheet
  --sort         TEXT     Sort by: onpage_score, status_code, size, load_time
  --order        TEXT     Sort order: asc, desc [default: desc]
  --limit    -n  INTEGER  Max results [default: 100]
  --offset       INTEGER  Offset for pagination [default: 0]
  --output   -o  TEXT     Output format: json, table, csv
  --login        TEXT     DataForSEO login
  --password     TEXT     DataForSEO password
  --verbose  -v           Verbose output
```

**Examples:**

```bash
# Pages with errors only
dfseo site pages "$TASK_ID" --errors-only

# Filter 404 pages
dfseo site pages "$TASK_ID" --status-code 404

# Sort by SEO score (worst first)
dfseo site pages "$TASK_ID" --sort onpage_score --order asc
```

---

## `dfseo site links`

List links found during crawl with filtering by type.

```
Usage: dfseo site links [OPTIONS] TASK_ID

Arguments:
  task_id  TEXT  Task ID from crawl command [required]

Options:
  --type          TEXT     Filter: broken, internal, external, redirect
  --page-from     TEXT     Filter links from a specific page
  --page-to       TEXT     Filter links to a specific page
  --dofollow-only          Only dofollow links
  --limit     -n  INTEGER  Max results [default: 100]
  --output    -o  TEXT     Output format: json, table, csv
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Examples:**

```bash
# Broken links only
dfseo site links "$TASK_ID" --type broken

# External links
dfseo site links "$TASK_ID" --type external --dofollow-only
```

---

## `dfseo site duplicates`

Find duplicate titles, descriptions, or content.

```
Usage: dfseo site duplicates [OPTIONS] TASK_ID

Arguments:
  task_id  TEXT  Task ID from crawl command [required]

Options:
  --type  -t  TEXT     Type: title, description, content [default: title]
  --page      TEXT     For content type: URL of page to compare against
  --limit -n  INTEGER  Max results [default: 100]
  --output-o  TEXT     Output format: json, table, csv
  --login     TEXT     DataForSEO login
  --password  TEXT     DataForSEO password
  --verbose   -v       Verbose output
```

**Examples:**

```bash
dfseo site duplicates "$TASK_ID" --type title
dfseo site duplicates "$TASK_ID" --type description
dfseo site duplicates "$TASK_ID" --type content
```

---

## `dfseo site redirects`

Find redirect chains (important for SEO: chains should be minimized).

```
Usage: dfseo site redirects [OPTIONS] TASK_ID

Arguments:
  task_id  TEXT  Task ID from crawl command [required]

Options:
  --min-hops     INTEGER  Only chains with >= N redirects
  --limit    -n  INTEGER  Max results [default: 100]
  --output   -o  TEXT     Output format: json, table, csv
  --login        TEXT     DataForSEO login
  --password     TEXT     DataForSEO password
  --verbose  -v           Verbose output
```

**Example:**

```bash
# Only multi-hop chains (3+ redirects)
dfseo site redirects "$TASK_ID" --min-hops 3
```

---

## `dfseo site non-indexable`

List pages that cannot be indexed by search engines.

```
Usage: dfseo site non-indexable [OPTIONS] TASK_ID

Arguments:
  task_id  TEXT  Task ID from crawl command [required]

Options:
  --reason       TEXT     Filter: noindex, canonical, robots_txt, redirect
  --limit    -n  INTEGER  Max results [default: 100]
  --output   -o  TEXT     Output format: json, table, csv
  --login        TEXT     DataForSEO login
  --password     TEXT     DataForSEO password
  --verbose  -v           Verbose output
```

**Example:**

```bash
dfseo site non-indexable "$TASK_ID" --reason noindex
```

---

## `dfseo site resources`

List site resources (images, scripts, stylesheets) with size and load info.

```
Usage: dfseo site resources [OPTIONS] TASK_ID

Arguments:
  task_id  TEXT  Task ID from crawl command [required]

Options:
  --type          TEXT     Filter: image, script, stylesheet, broken
  --min-size      INTEGER  Minimum size in bytes
  --external-only          Only external resources
  --limit     -n  INTEGER  Max results [default: 100]
  --output    -o  TEXT     Output format: json, table, csv
  --login         TEXT     DataForSEO login
  --password      TEXT     DataForSEO password
  --verbose   -v           Verbose output
```

**Examples:**

```bash
# Large images (over 100KB)
dfseo site resources "$TASK_ID" --type image --min-size 102400

# All external scripts
dfseo site resources "$TASK_ID" --type script --external-only
```

---

## `dfseo site lighthouse`

Run Google Lighthouse audit on a URL via DataForSEO's Lighthouse API.

```
Usage: dfseo site lighthouse [OPTIONS] URL

Arguments:
  url  TEXT  URL to audit [required]

Options:
  --categories      TEXT     Comma-separated: performance, accessibility, seo, best-practices [default: all]
  --device      -d  TEXT     Device: desktop or mobile [default: desktop]
  --wait        -w/--no-wait  Wait for completion [default: wait]
  --timeout         INTEGER  Timeout in seconds [default: 120]
  --poll-interval   INTEGER  Seconds between checks [default: 5]
  --output      -o  TEXT     Output format: json, table
  --login           TEXT     DataForSEO login
  --password        TEXT     DataForSEO password
  --verbose     -v           Verbose output
```

**Examples:**

```bash
# Full Lighthouse audit
dfseo site lighthouse "https://example.com"

# Performance and SEO only, mobile
dfseo site lighthouse "https://example.com" --categories performance,seo --device mobile
```

---

## `dfseo site tasks`

List all On-Page API tasks for your account.

```
Usage: dfseo site tasks [OPTIONS]

Options:
  --ready           Only show tasks ready for retrieval
  --output  -o TEXT  Output format: json, table
  --login      TEXT  DataForSEO login
  --password   TEXT  DataForSEO password
  --verbose  -v      Verbose output
```

**Example:**

```bash
# List pending tasks
dfseo site tasks --ready
```
