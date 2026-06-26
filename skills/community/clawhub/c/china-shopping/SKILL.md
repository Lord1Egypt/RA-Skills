---
name: china-shopping
description: Recommend suitable Chinese shopping platforms for a user-provided product type, product name, or shopping need. Use when the user asks where to buy something in China, which Chinese e-commerce platform fits a product category, where to shop for electronics, clothing, groceries, beauty products, or similar items, or asks questions like "买这个去哪", "推荐购物网站", "哪里买比较合适", or "中国购物推荐".
metadata:
  openclaw:
    requires:
      bins: ["python3"]
---

# China Shopping

Recommend suitable Chinese shopping platforms based on product category and shopping intent.

This is a lightweight Python-backed skill. It uses a local Python script plus bundled JSON data to map product names to shopping categories and recommend suitable Chinese e-commerce platforms.

It does **not** perform live browsing, real-time price checks, or seller verification. For live page inspection, real-time pricing, or store-level comparison, switch to browser-based workflows instead of pretending this skill does live retrieval.

## Runtime requirement

Require:
- `python3`

Do not require:
- `jq`
- shell helper scripts
- install scripts
- writable config or log paths
- credentials or API keys

## Files used by this skill
- `china-shopping.py` — local CLI implementation
- `data/categories.json` — category and platform recommendation data
- `data/product_mapping.json` — product keyword mapping
- `data/general_fallback.json` — fallback recommendations

Read these references as needed:
- `references/category-guide.md` for category-to-platform guidance
- `references/output-patterns.md` for answer structure

## Workflow

1. Identify the product category or shopping intent.
   - Accept a product type, shopping need, or product name.
   - If the request is too broad, ask one short clarifying question.

2. Use the local Python implementation when execution is appropriate.
   - Run `python3 china-shopping.py recommend "<product>"` for the default recommendation flow.
   - Use `python3 china-shopping.py categories` when the user wants to inspect supported categories.

3. Explain the recommendation.
   - Say why the recommended platforms fit.
   - Mention meaningful trade-offs when useful.

4. Add practical guidance.
   - Suggest what the user should check next, such as official stores, seller reputation, user reviews, authenticity, or delivery terms.

## Output

Use this structure unless the user asks for something else:

### Recommended Platforms
List the most suitable 2-4 platforms.

### Why
Explain why each platform fits the product or need.

### Best Choice
State which platform is the strongest default recommendation.

### Caveats
Mention important cautions, such as seller quality differences, authenticity risk, or category-specific trade-offs.

### Final Advice
Give a practical buying suggestion in plain language.

## Quality bar

Do:
- recommend platforms by category fit
- explain trade-offs clearly
- mention official stores or trusted sellers when relevant
- stay honest about not doing real-time price retrieval

Do not:
- pretend to check live listings or prices
- claim a platform is cheapest without real-time evidence
- suggest weak-fit platforms just because they are famous
