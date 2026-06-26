# Output Schema

This skill uses two different JSON shapes and one fixed 14-column workbook:

## 1. Machine / factual JSON

This is the full review row data produced by `collect`, `intake`, or `translate`.

- It can contain factual fields only
- It can also carry helper fields such as `machine` or `delivery` wrappers
- It is the source that `merge-build` should read from

## 2. Labels JSON

This is the model's completed semantic output for the pending rows only.

- It should contain the final semantic fields, not the cropped `prepare-tagging` payload
- It may be a JSON array or an object with `items`
- It is merged back into the full base JSON by `merge-build`

## 3. Delivery workbook

The final workbook always exports these 14 columns, in order:

1. `序号`
2. `评论用户名`
3. `国家`
4. `星级评分`
5. `评论原文`
6. `评论中文版`
7. `评论概括`
8. `情感倾向`
9. `类别分类`
10. `标签`
11. `重点标记`
12. `评论链接网址`
13. `评论时间`
14. `评论点赞数`

## Field Rules

- `评论用户名`: Fill only from the visible review card; if unavailable, leave blank.
- `国家`: Fill only when the page explicitly reveals country/region.
- `星级评分`: Fill only when the page explicitly reveals a star rating.
- `评论原文`: Keep the original review language. If the body is empty, title fallback is allowed.
- `评论中文版`: Faithful Chinese translation.
- `评论概括`: One-sentence summary.
- `情感倾向`: Must be `Positive`, `Negative`, or `Neutral`.
- `类别分类`: Use 1-2 high-signal categories.
- `标签`: Short Chinese tags, ideally <= 10 chars each.
- `重点标记`: Prefer business-relevant dimensions like value, quality, feature requests, competitor mentions.
- `评论链接网址`: Must point back to the original review.
- `评论时间`: Fill only from explicit page content.
- `评论点赞数`: Fill only from explicit page content.

## Default Categories

- `Praise on product`
- `Questions/Worrying`
- `Negative emotions`
- `Suggestion`
- `Nothing particular`
- `Being supportive to the brand`
- `Expecting`
- `Being Sarcastic`
- `Competitor comparison`
- `Status update`

## Focus Mark Control Words

The analyzer normalizes model output into these dimensions:

- `value_for_money`
- `quality`
- `feature_suggestion`
- `competitor_model`
- `software_setup`
- `installation_fit`
- `brand_after_sales`
- `logistics_packaging`
- `accessory_compatibility`
