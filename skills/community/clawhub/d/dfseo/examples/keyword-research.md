# Keyword Research Workflow

Complete workflow for finding and evaluating keyword opportunities for a domain.

## Step 1: Explore seed keywords

Run volume check for your initial ideas:

```bash
dfseo keywords volume "email hosting" "smtp service" "business email" \
  --location "Italy" --language "Italian" --include-serp-info
```

Look for: high volume, low-medium difficulty (< 50), commercial or transactional intent.

## Step 2: Expand with long-tail suggestions

```bash
dfseo keywords suggestions "email hosting" \
  --location "Italy" --language "Italian" \
  --min-volume 50 --max-difficulty 40 --limit 100
```

Long-tails are easier to rank for and often have higher conversion intent.

## Step 3: Find semantically related keywords

```bash
dfseo keywords ideas "email hosting" "smtp service" \
  --location "Italy" --limit 100
```

These may not contain your exact seed but capture the same topic cluster.

## Step 4: Classify search intent

```bash
dfseo keywords search-intent \
  "buy email hosting" "best email hosting" "what is smtp" "gmail login"
```

Target transactional/commercial intent for conversion pages, informational for blog content.

## Step 5: Bulk difficulty check

Save your best candidates to a file and check difficulty:

```bash
# Create keywords.txt with one keyword per line
dfseo keywords difficulty --from-file candidates.txt --location "Italy"
```

## Step 6: Check the SERP landscape

For top candidates, understand who's ranking and why:

```bash
dfseo serp google "best email hosting Italy" --location "Italy" --depth 20 --output table
```

## Step 7: Check competitor domain keywords

See what keywords your competitors rank for that you don't:

```bash
dfseo keywords for-site "competitor.com" \
  --location "Italy" --min-volume 100 --sort volume --limit 200
```

## Quick one-liner: full research to JSON

```bash
dfseo keywords volume "email hosting" --location "Italy" -q | \
  jq '{keyword: .[0].keyword, volume: .[0].search_volume, kd: .[0].keyword_difficulty}'
```
