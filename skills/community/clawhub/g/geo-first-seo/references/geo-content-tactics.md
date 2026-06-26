# GEO Content Tactics

Expanded detail for the seven content principles in `SKILL.md`, with before/after rewrites and
per-engine notes. Open this when you need a concrete example of how to apply a principle. The main
workflow does not require this file.

## The seven principles, with rewrites

### 1. Answer-first

Lead every page and section with the conclusion, then support it. Engines extract the opening
sentence as the answer.

- **Before:** "There are many factors to consider when choosing a database, and the right choice
  depends on your situation, which we'll explore below."
- **After:** "For high-write workloads with flexible schemas, choose a document database like
  MongoDB; for strong relational integrity, choose PostgreSQL. Here is how to decide between them."

### 2. Self-contained chunks

Each section must answer one question and make sense in isolation — engines retrieve passages, not
pages. Remove cross-references that only resolve in context.

- **Before:** "As we saw earlier, this makes it the better option for those cases."
- **After:** "Redis is the better option for caching session data because it serves reads from
  memory in under a millisecond."

A quick test: copy any single section into a blank document. If it no longer makes sense, it is not
self-contained.

### 3. Entity & semantic coverage

Name entities explicitly and define key terms inline. Cover the subtopics and follow-up questions a
knowledgeable reader expects. Completeness is an authority signal.

- **Before:** "It uses a popular protocol to keep things in sync."
- **After:** "Git uses a distributed version-control model: every clone is a full repository,
  unlike centralized systems such as Subversion (SVN)."

Include definitions for jargon the target audience may not share, and link related concepts so the
page reads as a complete treatment of the topic.

### 4. Citable elements

Statistics, dated facts, named sources, and direct quotes are the units an engine lifts into an
answer. Attribute every figure. Never fabricate one — mark unknowns `[verify]`.

- **Before:** "Most developers prefer this approach these days."
- **After:** "In the 2024 Stack Overflow Developer Survey, 49% of respondents reported using
  PostgreSQL, making it the most-used database that year. [verify: confirm exact figure and year]"

Prefer primary sources (original studies, official docs, first-party data) over secondary summaries.

### 5. Scannable structure

Use question-style headings, short paragraphs, lists, comparison tables, and a dedicated FAQ block.
Structure helps an engine map a query to the exact passage that answers it.

- Turn "Overview of pricing" into "How much does X cost?"
- Convert dense prose comparisons into a table with one row per option.
- Add an FAQ block answering the literal questions from your Phase 1 query cluster.

### 6. Authority & freshness signals

Show a named author with relevant credentials, link the primary sources you cite, and display a
visible "last updated" date. Engines weigh trust signals when choosing what to cite.

- Add an author byline and a one-line bio establishing relevant expertise.
- Replace "studies show" with the specific linked study.
- Add and genuinely maintain a "Last updated: YYYY-MM-DD" line.

### 7. Plain, unambiguous language

Write so a single sentence can be quoted with no surrounding context. Avoid vague pronouns, hedging,
and phrasing that hides the claim.

- **Before:** "This can sometimes potentially help improve things in certain scenarios."
- **After:** "Adding an index on the `user_id` column reduces this query's runtime from 1.2s to 8ms."

## Per-engine notes

Engines differ in what they reward. Optimize for the content layer first; these are emphasis tweaks,
not separate rewrites.

| Engine | Tends to favor |
| --- | --- |
| **Perplexity** | Fresh content with explicit, linkable primary sources; clear inline attribution. |
| **Google AI Overviews** | Structured answers, FAQ markup, and content that already ranks well in classic search. |
| **ChatGPT (search/browse)** | Authoritative, well-known sources; clear definitions and self-contained explanations. |
| **Gemini** | Strong entity coverage and content backed by Google-indexed, structured pages. |
| **Copilot (Bing)** | Bing-indexed pages with clear structure and citable, attributed facts. |

Common ground across all of them: answer-first passages, self-contained chunks, attributed facts,
and machine-readable structure. When in doubt, strengthen those.
