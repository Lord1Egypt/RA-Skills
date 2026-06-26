# ClawHub Release Material

## Suggested title
ccdb-factor-search

## Suggested short summary
Search and select the best-fit CCDB emission factor from Carbonstop APIs using bilingual query expansion, multi-round candidate comparison, suitability filtering, and structured result explanations.

## Suggested version
0.1.3

## Suggested full description
`ccdb-factor-search` helps find the most suitable CCDB / Carbonstop emission factor for a user's scenario instead of just returning a raw query result list. It extracts a minimal core search term, searches in both Chinese and English, expands only when necessary, compares candidates across multiple rounds, rejects obviously unsuitable results, and returns a reasoned recommendation with risks, alternatives, and search trace.

It is especially useful when users ask to:
- 查找或匹配排放因子 / 碳因子
- 比较多个候选因子是否适合当前业务场景
- 根据地区、单位、年份、工艺或场景筛选更合适的 CCDB 因子
- 在中英文之间切换检索词
- 对检索结果做“direct / close / fallback / not suitable”判断

## Suggested release stage
Beta / Preview

Reason:
- electricity, natural gas, polyester-related, and aluminium-related cases already show useful behavior
- some steam scenarios still rely on fallback behavior depending on data coverage
- real-world usage feedback will further improve vocabulary and matching rules

## Suggested tags / positioning
- carbon
- emission-factor
- ccdb
- search
- sustainability
- lca
- factor-matching

## Known limitations to disclose
- API-dependent skill
- encrypted factor values may prevent direct numeric output in some cases
- steam scenarios may still return broader heat/steam matches
- data quality and coverage affect final matching quality

## Recommended publish note
This is a 0.1.3 beta release focused on best-fit factor retrieval and suitability judgment. It is designed to be conservative: when no reliable candidate is found, it should prefer `not_suitable` over misleading recommendations.
