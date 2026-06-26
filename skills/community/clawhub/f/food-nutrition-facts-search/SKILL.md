---
name: 'food-nutrition-facts-search'
description: 'Searches nutrition facts, food scores, and packaged product data via public AI-friendly endpoints. Invoke when users ask to find, compare, or inspect foods, nutrition facts, brands, or barcodes.'
---

# Nutrition Facts Search

Use this skill when the user wants nutrition facts, food scores, product details, or barcode lookup data from a public food data website rather than codebase analysis.

## When To Invoke

Invoke this skill when the user:

- asks to find a food or packaged product
- provides a brand name, barcode, or partial product name and wants the matching item
- wants to compare two or more foods or products using nutrition facts or food scores
- wants a structured summary of a food or product detail page

Do not invoke this skill for repository code search, implementation questions, or unrelated websites.

## Public Endpoints

- Search: `https://foodbenchmark.com/api/ai/search?q=<query>&type=<all|foods|products>&limit=<1-20>&offset=<0-based>`
- Food detail: `https://foodbenchmark.com/api/ai/foods/<slug>`
- Product detail: `https://foodbenchmark.com/api/ai/products/<code>`

## Food vs Product

- `food` means a generic food concept or food entry such as `banana`, `olive oil`, or `broccoli`
- `product` means a product record that can expose label-style fields such as nutrition facts, ingredients, additives, brand, barcode, and packaging data
- These are different datasets and should not be treated as interchangeable records
- `foods` are best for generic food entities, category-level food scores, and food-oriented summaries
- `products` are best for packaged items and for any request that needs nutrition-facts-style label data
- Important rule: if the user asks for `nutrition facts`, `nutrition label`, `calories`, `protein`, `fat`, `carbs`, serving-based nutrients, or similar nutrient fields for a specific item, use `products`
- Even when the user names a broad food such as `whole milk` or `banana`, if the intent is to inspect nutrition facts, use `products` because only `product` records expose nutrition facts in this workflow
- If the user wants an ingredients list, ingredient analysis, additive details, or barcode lookup, use `products` only
- If the user wants a generic food entry or food score summary without asking for nutrition facts, prefer `foods`
- If the user names a brand, barcode, or a specific packaged item, prefer `products`
- If the user says only something ambiguous like `Coca-Cola`, `oat milk`, or `cookies`, search `all` first and then disambiguate

## Type Selection Rules

Choose `type` based on user intent, not only the wording of the item name.

- Use `type=products` when the user asks for nutrition facts, nutrition labels, calories, macros, serving-based nutrients, ingredients, additives, barcode results, or a packaged/branded item
- Use `type=products` when the user wants nutrition facts for a specific food name, because only `product` records provide nutrition facts in this workflow
- Use `type=foods` when the user wants a generic food entry, food category context, or summary food scoring data and is not asking for nutrition facts
- Use `type=all` when the query is ambiguous and intent is unclear, then choose the most relevant result set after search

Quick intent mapping:

- `Find banana nutrition facts` -> `type=products`
- `Show whole milk calories` -> `type=products`
- `Compare oat milk nutrition labels` -> `type=products`
- `Find banana food score` -> `type=foods`
- `What category is olive oil in?` -> `type=foods`
- `Coca-Cola` -> `type=all`

## Workflow

### 1. Search First

Always call the search endpoint before requesting details.

- Use `type=products` when the user asks for nutrition facts or any label-style nutrient data
- Use `type=products` when the user clearly wants a packaged product, brand, ingredient list, additive data, or barcode result
- Use `type=foods` when the user clearly wants a generic food entity or food score summary and is not asking for nutrition facts
- Use `type=all` when the query is ambiguous

Search returns compact result groups:

- `foods`: matched food records
- `products`: matched product records
- `meta`: totals, pagination, and truncation information

### 2. Fetch Details Only When Needed

After search:

- If a single obvious result exists, fetch its detail endpoint
- If several close matches exist, show the best matches first and ask the user to choose
- If the user wants comparison, fetch detail for each selected item

### 3. Keep Responses Compact

- Prefer structured summaries over raw JSON dumps
- Include the canonical website URL for each selected entity
- When product detail includes `identity.siteUrl`, recommend that the user open it to view the full page details
- Mention when results are truncated or ambiguous
- If nothing matches, say so clearly and suggest a narrower query

## Output Shape

For foods, prioritize:

- `title`
- `category`
- `Food Compass 2`
- `Health Star Rating`
- `Nutri-Score`
- `NOVA group`
- `canonical URL`

For products, prioritize:

- `title`
- `brand`
- `Nutri-Score`
- `NOVA group`
- `environmental score summary`
- `ingredient/additive highlights` when relevant
- `canonical URL`

## Query Strategy

- Barcode-only input: use `type=products`
- Nutrition-facts requests for any named item, including a food name: use `type=products`
- Clearly food-like input without nutrition-facts intent: use `type=foods`
- Ingredients, additives, or packaged-label questions: use `type=products`
- Ambiguous names such as brands or broad product names: use `type=all`
- If results are truncated, summarize the best matches and mention that more results exist
- When you need additional pages, keep the same `q` and `type`, then advance with `offset` (or `page`)

## Platform Rules

- Use only public URLs from `foodbenchmark.com`
- Do not depend on local files, local scripts, or IDE-only context
- Do not dump raw Open Food Facts JSON unless the user explicitly asks for raw data
- Prefer a short structured answer over long prose
- When nothing matches, say that clearly and suggest a narrower query or a barcode

## Recommended Response Format

For a single match:

- entity name
- entity type: `food` or `product`
- key scores
- 1 short interpretation sentence if useful
- canonical URL
- For product details, mention that the user can open `identity.siteUrl` to view the full detail page

For multiple matches:

- show the top matches first
- include enough fields for disambiguation
- ask the user which one to inspect if there is no clear winner

## Examples

### Find nutrition facts for a food name

User: `Find whole milk nutrition facts`

1. Request `https://foodbenchmark.com/api/ai/search?q=whole%20milk&type=products`
2. If a clear product match exists, request `https://foodbenchmark.com/api/ai/products/<code>`
3. Return a short summary with the canonical URL

### Find a product by barcode

User: `Check barcode 3017620422003`

1. Request `https://foodbenchmark.com/api/ai/search?q=3017620422003&type=products`
2. If found, request `https://foodbenchmark.com/api/ai/products/3017620422003`
3. Return the matched product with key scores and link

### Compare products

User: `Compare Coca-Cola and Pepsi nutrition facts`

1. Search both names
2. If multiple matches exist, identify the best candidates
3. Fetch details for the chosen products
4. Return a concise comparison table or bullet summary
