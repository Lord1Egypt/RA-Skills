---
name: book-scout
description: Expert book recommendation engine via web search. Finds high-quality books (Douban ≥7.5 or Goodreads ≥3.8) based on topic, with deduplication and comprehensive scoring. Use when you need to recommend books for reading tasks, skill building, or research.
permissions:
  filesystem:
    read:
      - memory/reading-history.json  # Deduplication: exclude previously analyzed books
config:
  reads:
    - memory/reading-history.json
---

# Book Scout

Expert book recommendation engine that finds high-quality books via web search.

## When to Use

- Recommending books for a specific topic (e.g., "user growth", "decision science")
- Finding books for reading tasks (morning/noon/evening reading reports)
- Building a reading list for skill development
- Need to avoid previously analyzed books

## Input

- **topic** (required): Subject/theme (e.g., "用户增长", "决策科学", "AI技术")
- **used_models** (optional): Array of book title strings to exclude (e.g., `["《精益创业》", "《从0到1》"]`)

## Output

JSON object with the highest-scoring book:

```json
{
  "book_title": "书名",
  "author": "作者",
  "author_nationality": "国籍或'未知'",
  "publish_date": "YYYY-MM或YYYY",
  "rating": 8.9,
  "review_count": 15000,
  "score": 112.08,
  "summary": "100字核心简介",
  "reasoning": "推荐理由"
}
```

## Core Workflow (Two-Phase Search)

### Phase 1: Discover Book Titles

**Goal**: Get a list of 5-8 candidate book names. Do NOT try to get ratings here.

**Search Queries** (execute 2-3 queries in parallel):

| Query Type | Template | Example |
|------------|----------|---------|
| Chinese book lists | `"{topic} 经典书籍推荐 书单"` | `"用户增长 经典书籍推荐 书单"` |
| English book lists | `"{topic_en} best books goodreads"` | `"user growth best books goodreads"` |
| Community picks | `"{topic} 必读书 知乎推荐"` | `"用户增长 必读书 知乎推荐"` |

**Extract**: Collect book titles + authors from search results. Ignore ratings at this stage.

**Deduplicate immediately**: Compare against `used_models` — remove any matches.

**Minimum**: Need at least 3 candidate books after dedup. If fewer, broaden the topic and search again.

### Phase 2: Get Ratings (Per-Book Lookup)

**Goal**: Get accurate rating + review_count for each candidate.

**Strategy** (try in order, stop at first success):

#### Method A: WebFetch Douban Page (Preferred)

For each candidate book, search for its Douban page then fetch it:

1. `web_search`: `"{book_title}" site:book.douban.com`
2. If a `book.douban.com/subject/` URL is found → `web_fetch` that URL
3. Extract: rating, review_count, publish_date, author from the page

**Why this works**: Douban book pages have structured rating data that WebFetch can reliably parse.

#### Method B: Direct Search (Fallback)

If Method A fails (no Douban URL found, or WebFetch blocked):

- `web_search`: `"{book_title}" "{author}" 豆瓣评分 评价人数`
- Extract rating and review_count from search snippets

#### Method C: Goodreads Lookup (For English Books)

- `web_search`: `"{book_title}" "{author}" site:goodreads.com`
- If URL found → `web_fetch` the Goodreads page
- Extract rating and ratings_count

**Important Rules**:
- Each book gets its OWN individual lookup — never combine multiple books into one query
- Each book gets up to **2 attempts** (e.g., Method A fails → try Method B)
- Process books in parallel when possible

### Phase 2.5: Handle Missing Data

After Phase 2, some books may still lack ratings. Apply these rules:

| Missing Field | Action |
|---------------|--------|
| rating missing after 2 attempts | Use LLM estimate from search context (mark as `"rating_source": "estimated"`). If no context at all, drop the book. |
| review_count missing | Default to `500` (neutral — neither penalized nor boosted) |
| publish_date missing | Default to `2020` |
| author_nationality missing | Output `"未知"` (NEVER fabricate) |

**LLM Estimation Rule**: If multiple search results consistently describe a book as "高分" / "经典" / "highly rated" but no exact number is found, estimate conservatively (7.5-8.0 for Chinese, 3.8-4.0 for English). Always mark estimated ratings.

### Phase 3: 3D Scoring Algorithm

**Action**: Collect ALL surviving candidate books into a single JSON array. Pass this entire array to `scripts/score_books.py` via stdin for batch scoring. The script returns sorted results.

(If script unavailable, calculate manually using the formula below.)

**Formula**:
```
Total Score = (Base Quality + Popularity Bonus) × Recency Multiplier
```

**A. Base Quality**:
```
Base = rating × 10
If review_count < 100: Base = Base × 0.8 (small sample penalty)
```

**B. Popularity Bonus**:
```
Bonus = log₁₀(review_count) × 2
```

**C. Recency Multiplier** (based on publish_date):
```
Published within 2 years (2024-now):  × 1.2
Published 3-5 years ago (2021-2023):  × 1.0
Published 5+ years ago (≤2020):       × 0.8
```

**Example**:
```
《增长黑客》: rating=8.5, review_count=10000, publish=2015
Base = 8.5 × 10 = 85
Bonus = log₁₀(10000) × 2 = 8
Recency = 0.8
Total = (85 + 8) × 0.8 = 74.4
```

### Phase 4: Output

Return the **highest-scoring book** in the structured JSON format.

**Reasoning field must include**: score justification, recency consideration, author background (if known).

If `rating_source` is `"estimated"`, add a note: `"注意：评分为根据多源信息估算，非精确数据"`

## Quality Filters

**Minimum Standards**:
- Douban rating ≥ 7.5 OR Goodreads rating ≥ 3.8
- Estimated ratings: apply the same thresholds

**Exclusions**:
- Books with "21天", "速成", "一本通" in title
- Marketing-heavy books with no substance

## Fallback & Error Handling

### Scenario 1: Web Search Failure

- Retry once after 2-3 seconds
- If still fails, try alternative query phrasing
- After 3 total failures, return error:

```json
{
  "error": "网络连接连续 3 次超时，无法获取最新书单数据，请稍后重试。"
}
```

### Scenario 2: Topic Too Niche

- Broaden search: remove professional jargon, use parent category
- Example: "认知负荷理论" → "认知心理学 经典书籍"

If broad search also fails:
```json
{
  "error": "该主题下未找到具备足够评价数据的经典书籍，请尝试更换更宽泛的主题或行业大词。"
}
```

### Scenario 3: All Candidates Dropped

If after Phase 2.5 no books survive:
- Return to Phase 1 with broader topic
- Lower quality filter temporarily to ≥ 7.0 / ≥ 3.5
- If still nothing, return the best estimated candidate with a warning

## Implementation Notes

- **Phase 1** (discover): pure `web_search`, focus on book list articles
- **Phase 2** (ratings): `web_search` + `web_fetch` combo, target Douban/Goodreads pages
- **Phase 3** (scoring): `scripts/score_books.py` (deterministic)
- **Parallelism**: Phase 1 queries can run in parallel; Phase 2 per-book lookups can run in parallel
- Prioritize Douban/Goodreads/Zhihu/Reddit sources; ignore ads and promotional content
