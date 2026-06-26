# Entity, Evidence, Mention, Citation, And Ranking Rules

Use this reference whenever the task involves model visibility, "mentioned/not mentioned" disputes, citation/source ranking, or audit scoring.

## Entity Normalization

Build separate lists:

- `brand_aliases`: names that refer to the target entity.
- `category_keywords`: business/category/search terms.
- `competitor_aliases`: names that refer to competitors or alternatives.
- `channel_terms`: platforms, stores, regions, distributors, or source domains.

Do not count `category_keywords` as brand mentions. A category hit can improve topical relevance, but it is not brand visibility.

Recommended alias expansion for Chinese local brands:

- full legal or school/company name
- short brand name
- city + brand
- brand + service/category
- brand + school/company/store/training center
- old names and common public listing names
- pinyin/English names if used publicly
- likely punctuation, spacing, and suffix variants

Example:

```json
{
  "brand_name": "大连米嘟西点培训学校",
  "brand_aliases": [
    "大连米嘟西点培训学校",
    "米嘟西点",
    "米嘟西点培训",
    "米嘟西点培训学校",
    "大连米嘟西点培训",
    "大连米嘟国际西点培训",
    "大连米嘟国际西点培训学校"
  ],
  "category_keywords": ["大连西点培训", "西点培训学校", "烘焙培训", "蛋糕培训"]
}
```

## Evidence Levels

Use one of these levels for every model claim:

| Level | Meaning | Allowed claims |
|---|---|---|
| `verified_live_check` | Live/API/platform result captured with query, answer, time, source | mention, citation, source rank, score, trend |
| `manual_check` | User-provided copied answer, screenshot, manual record, or source list | mention/citation/rank if evidence is visible |
| `inferred_estimate` | Reasoning from brand materials only | content readiness and likely gaps only |
| `unverified_assumption` | Weak planning assumption | planning tasks only |

If evidence is not `verified_live_check` or `manual_check`, do not say "ranked top 3", "not mentioned", "model cited us", or "score is X".

## Mention Types

Separate these fields:

- `answer_mention`: alias appears in generated answer body.
- `citation_mention`: alias appears in source/citation title, snippet, URL, or source card.
- `source_rank`: first citation/source position where an alias appears.
- `brand_alias_hits`: exact aliases found.
- `category_keyword_hits`: category/search terms found.
- `competitor_mentions`: competitor aliases found.

Recommended output:

```json
{
  "answer_mention": false,
  "citation_mention": true,
  "source_rank": 2,
  "brand_alias_hits": ["米嘟西点"],
  "category_keyword_hits": ["大连西点培训"],
  "evidence_level": "manual_check",
  "claim_allowed": true
}
```

## Ranking Rules

Ranking can mean different things:

- `answer_rank`: position in a recommended list inside the model answer.
- `source_rank`: position in citation/source cards.
- `search_rank`: position in an external search result page.

Always label which rank is being discussed. If a brand is "top 3 in citations" but not in the answer body, report that distinction plainly.

## Common False Negatives

- The report checks only full legal name but the model uses a short name.
- The brand appears in source cards but not in answer text.
- The source title contains the brand but the snippet does not.
- The brand name includes city/category suffixes in one source but not another.
- Traditional/simplified, punctuation, spacing, or "国际/学校/培训中心" suffixes differ.

## Common False Positives

- Category keyword is counted as brand mention.
- A competitor source includes the same category term.
- The model says "training school" but not the target entity.
- The brand appears only because the prompt forced it in a direct-awareness question.

## Reporting Language

Use:

- "豆包引用来源中出现了该品牌，来源排名第 2，但回答正文未直接展开该品牌。"
- "当前证据显示品牌别名命中为 `米嘟西点`，不是全称命中。"
- "这是引用来源可见，不等同于模型主动推荐。"

Avoid:

- "完全没有提及" unless raw answer and citations were checked.
- "前三名" without saying source rank, answer rank, or search rank.
- "模型已经收录/认可" because citation/mention does not prove stable inclusion.
