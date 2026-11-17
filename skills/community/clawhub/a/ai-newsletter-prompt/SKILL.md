---
name: ai-newsletter-daily
description: >
  Generate a daily AI news digest newsletter from fresh web sources. Use this
  skill whenever a user asks for AI news, wants a roundup or summary of recent
  AI/ML developments, asks what happened in artificial intelligence today or
  this week, requests a newsletter, briefing, or digest of model releases,
  research papers, funding rounds, product launches, regulation, or benchmark
  results — even if they don't explicitly say "newsletter." Also use for
  follow-up requests like "more AI news" or "catch me up on AI."
---

# AI Newsletter Daily

You're generating a curated AI news digest from live web sources. Act like a
sharp editorial assistant — focused, opinionated about quality, and always
filtering for what actually matters to practitioners.

---

## Step 1: Clarify intent

Before searching, ask the user via `ask_user_input_v0` to confirm preferences
that differ from the defaults. One question, grouped options — don't
interrogate them.

**Defaults (proceed without asking if user gave enough context):**
- Article count: 10
- Time window: last 2 days
- Topic focus: all AI/ML (no filter)
- Output: inline markdown digest

**Ask only if the user's request was vague or open-ended:**
- How many articles? (5 / 10 / 20)
- Any topic focus? (All AI news / Research & papers / Model releases /
  Funding & business / Open-source / AI policy & regulation)
- Output format? (Display inline / Save as markdown file / Both)

If the user gave enough context already (e.g. "give me 20 AI news stories"),
extract it and skip the question.

---

## Step 2: Search the web

Search the web using a query constructed from the user's intent.
Default query: `latest AI news today`. Adjust based on topic focus:
- Research focus → `AI research papers released this week`
- Funding focus → `AI startup funding news today`
- Model releases → `new AI model release today`

If the first search returns fewer than 5 usable results (non-empty title and
URL), retry once with:
`AI news today machine learning model release funding research`

Filter results:
- Drop entries with no title or URL
- Canonicalize URLs (strip tracking params where possible)
- Drop duplicates by canonical URL
- Exclude: youtube.com, reddit.com, facebook.com, x.com, twitter.com,
  tiktok.com, instagram.com, linkedin.com
- Prefer results published within the configured time window

---

## Step 3: Rank candidates

Score each result 0–100 across three dimensions:

**AI Relevance (0–50 points)**

| Signal | Points |
|---|---|
| Title explicitly names an AI model, technique, company, or paper | 40–50 |
| Title/snippet describes a concrete AI development (release, benchmark, funding, regulation) | 30–40 |
| Content is AI-adjacent (general tech, AI is primary subject) | 15–30 |
| AI is mentioned incidentally in an otherwise non-AI story | 0–10 |

Penalize: opinion pieces with no news hook, listicles, tutorials, "AI
explained" explainers, marketing blogs without a real announcement.

**Freshness (0–30 points)**

| Published | Points |
|---|---|
| Within 24 hours | 28–30 |
| 1–2 days ago | 20–27 |
| 3–5 days ago | 10–19 |
| 6–14 days ago | 1–9 |
| Older or date absent | 0 (use 10 if date is simply missing from snippet) |

**Signal quality (0–20 points)**

| Signal | Points |
|---|---|
| Concrete noun in title: model name, company, paper title, dollar amount | 15–20 |
| Specific development implied ("launches", "releases", "raises", "publishes") | 10–14 |
| Generic but topic-relevant headline | 5–9 |
| Vague or clickbait title | 0–4 |

Sort by score descending, then published date descending. Keep the top
`article_count × 2` candidates to process.

---

## Step 4: Fetch, verify, and summarize

Work through ranked candidates in order until you have `article_count`
verified items. For each candidate:

1. **Open the URL** and read the page content. Retry up to 2 times on failure
   before skipping.
2. **Verify** — skip and log a warning if any of these are true:
   - Page title doesn't broadly match the search result title
   - Content is a login wall, error page, or under ~200 words
   - Topic is not substantively about AI/ML
   - Published date is present and outside the time window by more than 3 days
3. **Summarize** accepted articles in one plain-text paragraph, max ~80 words.
   Write for an AI practitioner: lead with what happened, follow with why it
   matters. Avoid marketing language and hedged non-statements.

**Verification edge cases:**

- **Login walls:** Count as a failed fetch. Retry up to the limit, then skip.
- **Paywalled articles:** Include if the title and snippet give enough for a
  useful summary. Mark clearly: `**Source:** The New York Times (paywalled) · [URL]`
- **Aggregator pages:** If a URL resolves to a homepage or category page
  rather than a specific article, skip it.
- **Duplicate stories, different sources:** Keep the higher-scoring one.
  Mention the second source inline if it adds meaningfully different detail.
- **Pre-prints and research papers:** arXiv and similar are valid. Always
  include: what problem it addresses, the key result, and why it matters in
  practice. Skip papers that are purely incremental with no clear hook.

---

## Step 5: Fallback

If you collected fewer than 5 verified items after processing all candidates,
search the web once more with:
`AI news today machine learning model release funding research`

Process only new URLs not already attempted. Apply the full
filter → rank → fetch → verify → summarize pipeline. If you still can't
reach 5 items, proceed with what you have and note the shortfall in the output.

---

## Step 6: Finalize and deliver

Sort final items by relevance score descending, then published date descending.
Truncate to `article_count`.

**Clamping — always apply before use:**

| Parameter | Min | Max | Default |
|---|---|---|---|
| article_count | 1 | 50 | 10 |
| time_window_days | 1 | 14 | 2 |
| max_search_results | 20 | 120 | 60 |
| min_articles_required | 1 | article_count | 5 |
| max_fetch_retries | 0 | 5 | 2 |

**Delivery:**
- **Inline:** Render the digest directly in the conversation using the format below.
- **File:** Write to `/mnt/user-data/outputs/ai-newsletter-YYYY-MM-DD.md` and
  call `present_files`.
- **Both:** Do both.

---

## Output format

### Markdown digest

```
# AI News Digest — [Day, Month DD, YYYY]

*[N] stories · Sources searched: [query] · Generated [HH:MM timezone]*

---

## 1. [Article Title]

[One paragraph summary, ~80 words, plain prose.]

**Source:** [Publication name] · [URL]

---

## 2. [Article Title]
...

---
⚠️ **Notes** (only if issues occurred)
- [N] URLs failed to fetch and were skipped
- Fallback search was used
```

### JSON schema (when JSON output is requested)

```json
{
  "date": "2026-04-30",
  "query": "latest AI news today",
  "article_count": 10,
  "articles": [
    {
      "rank": 1,
      "title": "Article title",
      "url": "https://...",
      "domain": "techcrunch.com",
      "summary": "One paragraph summary...",
      "relevance_score": 87,
      "published_date": "2026-04-30",
      "source_query": "latest AI news today"
    }
  ],
  "warnings": ["3 URLs failed to fetch and were skipped"]
}
```

`published_date` is optional — omit if unknown, don't substitute a placeholder.

---

## Quality bar

Accept an article only if ALL of these are true:
- URL is valid and canonicalized
- Page content broadly matches the search result
- Topic is substantively about AI/ML (not just a passing mention)
- Content is not a duplicate of another accepted item
- Published date is present or safely unknown

When in doubt, skip — a tight digest of 8 strong items beats a padded list of 12.
