# Competitor Audit Workflow

Comprehensive competitor analysis covering keywords, backlinks, and on-page SEO.

## Step 1: Find competitor keywords

Discover what keywords a competitor ranks for:

```bash
dfseo keywords for-site "competitor.com" \
  --location "Italy" --min-volume 100 --sort volume --limit 200
```

Look for: keywords with high volume where the competitor ranks but you don't.

## Step 2: Check competitor SERP presence

See which pages rank for important keywords:

```bash
dfseo serp google "target keyword" --location "Italy" --depth 100 --output table
```

Note which competitor pages appear and their position.

## Step 3: Analyze backlink profile

Get a quick overview of their link authority:

```bash
dfseo backlinks summary "competitor.com"
```

Key metrics: rank, referring_domains, spam_score, dofollow ratio.

## Step 4: Find their top referring domains

```bash
dfseo backlinks referring-domains "competitor.com" \
  --sort rank --limit 50 --dofollow-only
```

These are the most valuable domains linking to your competitor — potential link building targets.

## Step 5: Link gap analysis

Find domains linking to competitors but NOT to you:

```bash
dfseo backlinks gap "your-site.com" "competitor.com" --min-rank 200 --dofollow-only
```

These are your highest-priority link building opportunities.

## Step 6: On-page comparison

Audit the competitor's site structure:

```bash
dfseo site audit "competitor.com" --max-pages 50
```

Check for technical weaknesses you can exploit (broken links, slow pages, duplicate content).

## Step 7: Bulk rank comparison

Compare multiple competitors at once:

```bash
dfseo backlinks bulk ranks \
  "your-site.com" "competitor1.com" "competitor2.com" "competitor3.com" \
  --output table
```

## Automate with a shell script

```bash
#!/bin/bash
DOMAIN=${1:?Usage: $0 competitor.com}

echo "=== Keywords ==="
dfseo keywords for-site "$DOMAIN" --min-volume 100 --sort volume --limit 50 -q

echo "=== Backlink Summary ==="
dfseo backlinks summary "$DOMAIN" -q

echo "=== Top Referring Domains ==="
dfseo backlinks referring-domains "$DOMAIN" --sort rank --limit 20 -q

echo "=== Link Gap vs Your Site ==="
dfseo backlinks gap "your-site.com" "$DOMAIN" --min-rank 150 --limit 30 -q
```
