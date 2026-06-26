# ClawHub Publish Copy

## Suggested title
CCDB Factor Search

## Suggested slug
ccdb-factor-search

## Suggested release stage
Beta / Preview

## Short summary
Search and select the best-fit CCDB emission factor from Carbonstop APIs using bilingual query expansion, smallest-core-term search, multi-round candidate comparison, suitability filtering, and structured result explanations.

## Full description
`ccdb-factor-search` helps find the most suitable CCDB / Carbonstop emission factor for a user's scenario instead of simply returning a raw query result list.

It works by extracting a minimal core search term from the user's request, searching in both Chinese and English, expanding only when necessary, comparing candidates across multiple rounds, rejecting obviously unsuitable matches, and returning a reasoned recommendation with risks, alternatives, and search trace.

This skill is especially useful when users want to:
- 查找或匹配排放因子 / 碳因子
- 从 CCDB / Carbonstop API 中找到“最合适”的因子
- 对多个候选因子做适配性判断
- 在中英文之间切换检索词
- 在结果不理想时继续优化搜索词
- 区分 direct match / close match / fallback / not suitable

## Suggested tags
carbon, emission-factor, ccdb, sustainability, lca, search

## Changelog
0.1.3 improves best-fit factor selection with richer README/docs, confirmed API field meanings, better geo-sensitive matching, latest-factor recency handling, stronger authority weighting, clearer carbon-footprint vs emission-factor distinction, and safer direct-use guidance.

## Known limitations
- This skill depends on the Carbonstop CCDB API.
- Some factor values are encrypted in the API response.
- Some scenarios may only yield close/fallback matches rather than direct matches.
- Steam-related queries may still return broader heat/steam fallback candidates depending on data coverage.

## Recommended publish note
This is a beta release focused on best-fit factor retrieval and suitability judgment. It is intentionally conservative: when no reliable candidate is found, it should prefer `not_suitable` over misleading recommendations.
