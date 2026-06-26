---
name: chanai-search-workflow
description: External web search workflow for Chinese and global public-web information. Use when searching news, flights, prices, products, docs, tutorials, community posts, websites, PDFs, research, or other external information. Classify intent first, detect dynamic real-time topics, choose domestic-first or global-first search routes, prioritize human-usable sites, generate starter URLs, apply fallback strategy, and report reliability.
---

# Chanai Search Workflow

Use this skill as the default workflow for **external/public-web search**.

Do not use it for local memory recall; use memory search for that.

## Core workflow

1. Run `scripts/run_search_workflow.py "<query>"` first.
2. Read the returned plan:
   - intent
   - route (`domestic-first` / `global-first` / `mixed`)
   - dynamic subtype if any
   - suggested site priority
   - starter URLs
3. Execute search using the highest-priority routes first.
4. If the first route fails, read `references/fallbacks.md` and switch engines/sites.
5. After collecting evidence, use `scripts/score_result.py` to score reliability.
6. Use `scripts/search_report.py` or `references/reporting-template.md` to produce the final response.

## Dynamic topics rule

If the query is about flights, prices, inventory, tickets, bookings, hotel availability, or other real-time topics:
- treat public search as preliminary discovery only
- prefer real-time/official/transaction-adjacent pages first
- do not present snippets or aggregator blurbs as final truth
- distinguish clearly between preliminary findings and real-time page findings

## Scripts

### Unified entrypoint
```bash
python3 scripts/run_search_workflow.py "上海直飞赤峰航班价格"
python3 scripts/run_search_workflow.py "openclaw memory search docs"
```

### Individual helpers
```bash
python3 scripts/query_router.py "周杰伦演唱会门票开售"
python3 scripts/dynamic_guard.py "上海外滩酒店房价"
python3 scripts/build_urls.py domestic-first dynamic "iPhone 16 京东价格"
python3 scripts/score_result.py 5 5 4 5
python3 scripts/search_report.py domestic-first "Ctrip" "Trip" medium "查到了候选结果" "公开搜索只做初筛" "最终以实时页为准"
```

## References

- `references/dynamic-info.md` — boundary rules for real-time topics
- `references/priorities.md` — source priority by scenario
- `references/intent-classification.md` — intent taxonomy
- `references/direct-templates.md` — direct site-entry URL templates
- `references/use-cases.md` — reusable search patterns
- `references/fallbacks.md` — fallback strategy when search is blocked/weak
- `references/reliability-scoring.md` — reliability rubric
- `references/reporting-template.md` — final response templates
- `references/domestic-search.md` — Chinese-site search guidance
- `references/international-search.md` — global-site search guidance

## Notes

- Prefer domestic-first for Chinese consumer info, local travel, Chinese community content, and local ecommerce.
- Prefer global-first for GitHub, API docs, English tutorials, research, and international sources.
- Prefer mixed when both Chinese and global perspectives matter.
- For dynamic subtypes, the workflow should prioritize scenario-specific sources such as flights, hotels, product-price, ticketing, and finance-news.
