# Link Building Workflow

Find and prioritize link building opportunities using backlink gap analysis.

## Step 1: Discover your competitors

Find domains sharing a similar backlink profile to yours:

```bash
dfseo backlinks competitors "your-site.com" --sort rank --limit 20
```

Note the top competitors — these are your link building benchmarks.

## Step 2: Run link gap analysis

Find domains that link to competitors but NOT to you:

```bash
dfseo backlinks gap "your-site.com" "competitor1.com" "competitor2.com" "competitor3.com" \
  --min-rank 200 --dofollow-only --limit 100
```

The `--min-rank 200` filter ensures you only target quality domains.

## Step 3: Analyze top opportunities

For each high-rank domain from the gap analysis, investigate further:

```bash
# See how many times the domain links to competitors
dfseo backlinks list "competitor1.com" --from-domain "opportunity-domain.com" --limit 5
```

This shows the context in which they link — helps you craft your outreach.

## Step 4: Check your anchor text distribution

Before building more links, audit your current profile health:

```bash
dfseo backlinks anchors "your-site.com" --sort backlinks --limit 30 --output table
```

Healthy profile: branded anchors (your brand name) > exact-match keyword anchors.
Red flag: too many exact-match anchors (over-optimization).

## Step 5: Find your most-linked pages

Understand which content earns links naturally:

```bash
dfseo backlinks pages "your-site.com" --sort backlinks --limit 20 --output table
```

Create more content similar to your top-linked pages.

## Step 6: Monitor new and lost backlinks

Track your backlink profile changes:

```bash
# New backlinks (what you've earned recently)
dfseo backlinks list "your-site.com" --status new --sort first_seen --limit 20

# Lost backlinks (what you need to recover)
dfseo backlinks list "your-site.com" --status lost --sort last_seen --limit 20
```

## Step 7: Bulk competitor comparison

Compare your rank against multiple competitors:

```bash
dfseo backlinks bulk ranks \
  "your-site.com" "competitor1.com" "competitor2.com" \
  --output table
```

## Complete link building audit script

```bash
#!/bin/bash
YOUR_SITE="your-site.com"
COMPETITORS="competitor1.com competitor2.com competitor3.com"

echo "=== Current Backlink Profile ==="
dfseo backlinks summary "$YOUR_SITE" -q

echo ""
echo "=== Link Gap Opportunities ==="
dfseo backlinks gap "$YOUR_SITE" $COMPETITORS --min-rank 200 --dofollow-only --limit 50 -q

echo ""
echo "=== Recently Lost Backlinks ==="
dfseo backlinks list "$YOUR_SITE" --status lost --limit 20 -q

echo ""
echo "=== Anchor Text Distribution ==="
dfseo backlinks anchors "$YOUR_SITE" --limit 15 -q
```

## Tips

- **Focus on referring domains, not raw backlinks** — one domain linking 100 times counts less than 100 different domains
- **Prioritize by rank** — a rank 500+ domain is far more valuable than rank 50
- **Check spam score** — avoid links from domains with spam score > 30
- **Context matters** — a link from a relevant industry page is worth more than a generic directory
