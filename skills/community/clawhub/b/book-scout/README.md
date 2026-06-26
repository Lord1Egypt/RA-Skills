# Book Scout

> AI-powered book recommendation engine: Finds high-quality books (Douban ≥7.5 or Goodreads ≥3.8) via web search, with smart deduplication and comprehensive scoring.

---

## What It Does

Finds the **best book** on any topic by:
1. Web search for book recommendations (Douban/Goodreads/professional lists)
2. Extract book metadata (ratings, reviews, publication date)
3. Score each book using a 3-factor formula
4. Return the highest-scoring book you haven't read yet

---

## Quick Start

### Install

```bash
clawhub install book-scout
```

### Use It

```
Ask your AI: "Use book-scout to find a book about: User Growth"
```

**Output**:
```json
{
  "book_title": "《增长黑客》",
  "author": "肖恩·埃利斯",
  "author_nationality": "美国",
  "publish_date": "2015-04",
  "rating": 8.5,
  "review_count": 10000,
  "score": 74.4,
  "summary": "增长黑客方法论：低成本获客、数据驱动迭代、病毒式传播...",
  "reasoning": "评分8.5且有1万真实评价，作者是增长黑客概念提出者"
}
```

---

## Scoring Algorithm

### Formula

```
Total Score = (Base Quality + Popularity Bonus) × Recency Multiplier
```

### Components

**A. Base Quality**:
```
Base = rating × 10
If review_count < 100: Base = Base × 0.8 (small sample penalty)
```

**B. Popularity Bonus**:
```
Bonus = log₁₀(review_count) × 2
(log naturally compresses large numbers, preventing bestseller spam dominance)
```

**C. Recency Multiplier** (based on publish_date):
```
Published within 2 years:   × 1.2
Published 3-5 years ago:    × 1.0
Published 5+ years ago:     × 0.8
```

### Example Calculation

```
Book: 《增长黑客》
- Rating: 8.5, Review Count: 10000, Publish: 2015
- Base = 8.5 × 10 = 85
- Bonus = log₁₀(10000) × 2 = 4 × 2 = 8
- Recency = 0.8 (5+ years old)
- Total = (85 + 8) × 0.8 = 74.4
```

---

## Quality Filters

**Minimum standards**:
- Douban rating ≥ 7.5 OR Goodreads rating ≥ 3.8
- At least 2 authoritative sources mention it (if rating unavailable)

**No hard review count threshold** — books with few reviews get a 0.8× penalty in scoring, so they need to earn their place through exceptional quality.

**Exclusions**:
- Books with "21天", "速成", "一本通" in title
- Marketing-heavy books (no substance)

---

## Search Strategy

For each topic, we run **3 searches**:

| Query | Focus |
|-------|-------|
| `"{topic} 经典书籍推荐"` | Chinese book lists |
| `"{topic} best books goodreads"` | English authority sources |
| `"{topic} 必读书单"` | Professional communities |

**Data extraction**: book title, author, rating, review count, publish date, author nationality.

**Deduplication**: Compare against `used_models` parameter (book title strings) immediately — matched books are discarded before scoring.

---

## Use Cases

### 1. Daily Reading Reports (with cognitive-forge)
`cognitive-forge` calls `book-scout` daily with different topics, building a diverse reading history over time.

### 2. Personalized Reading List
Ask for books on multiple topics, get the highest-scoring book per topic.

### 3. Research Literature Discovery
Find authoritative books on niche topics via web search.

---

## Exclude Previously Read Books

If using `cognitive-forge` daily, it auto-passes `used_models`:

```
Topic: "Business Strategy"
Used Models: ["《精益创业》", "《从0到1》", "《影响力》"]
```

Book Scout will exclude these and find the next best book.

---

## File Structure

```
book-scout/
├── SKILL.md           # Recommendation algorithm
├── README.md          # This file
└── scripts/
    └── score_books.py # Scoring formula (Python implementation)
```

---

## Troubleshooting

**"No books found for my topic"**:
- Try broader topics (e.g., "Psychology" instead of "Neuromarketing of Crypto")
- Or use English keywords

**"Same book recommended multiple times"**:
- Ensure `used_models` parameter is passed when calling the skill

**"Old books ranked too low"**:
- Books published 5+ years ago get a 0.8× recency multiplier
- This is intentional (favor modern, relevant books)

**"Rating seems wrong"**:
- We normalize Goodreads (0-5) to Douban scale (0-10) by multiplying by 2

---

## License

MIT-0

---

*Version: 1.1.0*
*Last updated: 2026-03-27*
*Changes: Aligned scoring formula with SKILL.md, removed incorrect quality filters*
