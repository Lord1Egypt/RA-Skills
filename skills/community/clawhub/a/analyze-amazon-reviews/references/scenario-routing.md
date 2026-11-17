# Scenario routing and sampling plans

## Contents

- Routing principles
- Built-in plans
- Natural-language intent mapping
- Overrides
- Statistical boundaries

## Routing principles

1. Infer the business decision the user wants to make, not only the word “分析”.
2. Choose the least expensive plan that can support that decision.
3. Default an ambiguous request to `health`, never `deep`.
4. Treat explicit scenario, filters, pages, sort order, and point budget as authoritative.
5. Show maximum estimated points before creating a paid task.

## Built-in plans

The table assumes one ASIN and 3 points per page. The script recalculates from runtime configuration.

| Scenario | Sampling | Pages | Max points | Best for |
|---|---|---:|---:|---|
| `quick` | `all_stars/recent` × 3 | 3 | 9 | Quick reputation overview |
| `health` | overall recent × 5; critical recent × 5 | 10 | 30 | General product diagnosis |
| `pain-points` | 1★ × 10; 2★ × 10; 3★ × 5 | 25 | 75 | Defects, returns, support issues |
| `selling-points` | 4★ × 5; 5★ × 10 | 15 | 45 | Benefits, buyer language, use cases |
| `listing` | 1–5★ × 5 each | 25 | 75 | Expectation gaps, FAQ, claims, creative |
| `media` | `critical/media_reviews_only` × 10 | 10 | 30 | Visible defects, packaging, damage |
| `competitor` | 1–5★ × 2 per ASIN | 10/ASIN | 30/ASIN | Cost-controlled comparison |
| `deep` | 1–5★ × 10 each | 50 | 150 | Maximum-depth single-product research |

## Natural-language intent mapping

- “快速看看、简单分析、先了解一下” → `quick`
- “分析这个产品、口碑怎么样、产品健康度” → `health`
- “为什么退货、差评原因、质量问题、售后问题” → `pain-points`
- “提炼卖点、广告文案、用户为什么喜欢、VOC” → `selling-points`
- “优化 Listing、五点描述、FAQ、商品图、预期差” → `listing`
- “看买家图片、实物不符、包装破损” → `media`
- “对比这些 ASIN、竞品差异、竞争机会” → `competitor`
- “最深度、完整、1 到 5 星全部分析” → `deep`

Change report emphasis with the intent:

- Product/R&D: failure modes, severity, affected variants, remediation priority.
- Listing: claim gaps, ambiguity, missing FAQ, visual proof needs.
- Marketing: purchase motives, benefits, user vocabulary, use contexts.
- Support: setup friction, troubleshooting, return triggers, preventable contacts.
- Competitor: shared themes, differentiators, whitespace, normalized evidence.
- Deep: include every module plus polarization and star-transition drivers.

## Overrides

- Use `custom` when the user provides one exact filter combination.
- Use `--pages` only to override every stratum in the chosen scenario; keep it in 1–10.
- Default `filter_sort_by=recent` for current product decisions.
- Use `helpful` when the user explicitly asks for historically influential or top-voted reviews.
- Use `avp_only_reviews` for a verified-purchase-only analysis, while disclosing that it excludes other reviews.
- Use `current_format` only when the user wants the current format; keep `all_formats` for variant discovery.
- For multiple ASINs, multiply page and point estimates by the ASIN count before confirmation.

## Statistical boundaries

- `all_stars/recent` is a recent baseline sample, not a full historical population.
- `critical`, `positive`, `helpful`, media-only, and star-specific samples are intentionally enriched strata.
- Never combine equal 1–5-star samples into an overall star percentage or product score.
- Compare competitor ASINs only when equivalent filters and page budgets are used.
- Compare theme shares within the same star/source stratum.
- If real product-page star weights are supplied separately, label and preserve their source before using them for weighted calculations.

