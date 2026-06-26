# CCDB Carbon Factor Search Workflow

## Goal

Find the most suitable carbon factor from the CCDB API for the user's intended object or activity.

## Step 1: Normalize the request

Extract as many of these fields as possible:
- material / product / fuel / energy type
- process or activity
- lifecycle stage
- geography / country / region
- time period if relevant
- unit requirements
- industry context
- any user-provided benchmark or expected match

## Step 2: Build search terms

Create a ranked list of search terms:
1. exact Chinese term from user
2. normalized Chinese synonym
3. exact English translation
4. normalized English synonym
5. broader parent category
6. narrower process-specific term if available

Examples:
- “聚酯切片” → “聚酯切片”, “PET切片”, “polyester chip”, “PET resin”
- “外购电（华东电网）” → “外购电 华东电网”, “区域电网电力”, “purchased electricity East China grid”, “grid electricity East China”

## Step 3: Query iteratively

Start with the strongest term. If the result quality is weak:
- add or remove geography
- add or remove lifecycle stage
- switch Chinese ↔ English
- broaden to parent category
- narrow to process-specific term

Keep a search log.

Suggested OpenClaw helper usage:
- `python3 scripts/query_ccdb.py --query "电力" --lang zh`
- `python3 scripts/query_ccdb.py --query "electricity" --lang en`
- add `--region`, `--unit`, `--year` when the user provided those constraints

## Step 4: Evaluate suitability

Check whether returned factors match the user's need on:
- semantic object match
- lifecycle stage match
- region match
- unit match
- recency / source reliability
- whether the factor is generic vs specific

Reject factors that are clearly about a different object, stage, or region unless only fallback factors are available.

## Step 5: Return the best factor

When returning the chosen factor, explain:
- why it is the best available match
- what search path was used
- what tradeoffs remain
- whether the result is direct match / close substitute / fallback generic factor

## If nothing suitable is found

Return:
- all key search terms attempted
- why results were unsuitable
- what clarification would improve matching
