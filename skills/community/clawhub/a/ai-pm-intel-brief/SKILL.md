---
name: ai-pm-intel-brief
description: Create a daily AI PM intelligence brief from Twitter/X or similar high-signal sources. Use when the user asks for an AI product manager news brief, signal brief, trend roundup, account digest, "今天 AI 圈在聊什么", "整理成简报", or wants recent posts from selected people/accounts summarized into: key signals, product insights, original excerpts, and links. Also use when turning raw social posts into a concise brief for product strategy, workflow design, agent products, growth, or market positioning.
---

# AI PM Intel Brief

Create a high-signal daily brief for an AI product manager.

## Output goal

Turn a noisy stream of recent posts into a compact brief that helps a product-minded reader:

- notice meaningful shifts
- ignore low-signal chatter
- extract product implications
- decide what is worth discussing further

Default audience: an AI product manager who values directness, judgment, and concrete implications over hype.

## Core workflow

Follow these steps in order.

### 1. Define the source set

Identify one of these source patterns:

- a user-provided list of X/Twitter accounts
- a website/page containing recommended people to follow
- a topic query plus a short list of anchor accounts
- a previously curated watchlist

If the user provides too many accounts, prefer a high-signal subset over exhaustive coverage.

### 2. Collect recent posts

Gather posts from the last 24 hours by default unless the user specifies another range.

Prioritize sources in this order:

1. Stable API access
2. First-party or structured endpoints
3. CLI/browser scraping only when needed

When rate limits are possible:

- prefer fewer, larger pulls
- avoid aggressive parallel fan-out
- batch conservatively
- keep partial results if coverage is incomplete

### 3. Filter aggressively

Remove or downrank:

- pure reposts/retweets unless the quoted point is strategically important
- generic motivational posts
- short reactions with no product implication
- social banter
- duplicate points from multiple accounts
- posts with high engagement but low insight

Keep posts that contain at least one of:

- a non-obvious product insight
- a workflow change
- a notable market/adoption signal
- a meaningful user behavior signal
- a new interaction pattern
- a concrete lesson about agents, tooling, design, growth, infra, or product strategy

### 4. Rank for AI PM relevance

Prefer posts that help answer questions like:

- What is changing in how people build with AI?
- What product pattern is emerging?
- Where is user value moving?
- What assumptions are becoming outdated?
- What interaction model is winning?
- What should a product team reconsider now?

Do not rank purely by likes or views.

Use engagement only as a weak secondary signal.

### 5. Synthesize, do not merely list

For each selected item, produce:

- **Who / Theme**
- **Content summary** — what they actually said
- **Insight** — why it matters for an AI PM
- **Original excerpt** — short quoted excerpt when useful
- **Original link**

The insight should be the value-add. Do not just paraphrase the post.

### 6. End with a compressed readout

After the itemized list, produce a short section such as:

- Top 3 judgments
- 5 signals to remember
- Product implications
- What to watch next

This section should feel like the distilled brain of the brief.

## Recommended structure

Use this structure unless the user asks otherwise:

### Title

`AI PM 今日情报简报｜MM.DD`

### Section A: Most important judgments

3 high-level judgments, written crisply.

### Section B: Top signals

Usually 5-10 items.

For each item:

- `账号/人物` or `Who`
- `主题`
- `内容总结`
- `洞察`
- `原文` (optional if too long or weak)
- `原文链接`

### Section C: Compressed conclusion

Examples:

- 如果今天只记住 5 句话
- 给 AI PM 的建议
- 今天最值得继续深挖的 3 个方向

## Style rules

- Be direct.
- Be selective.
- Sound like someone with product judgment, not a clipping bot.
- Prefer insight density over completeness.
- Call out weak or overhyped signals when appropriate.
- It is acceptable to disagree with popular takes.

## Quality bar

A good brief should make the reader feel:

- "I now know what actually mattered today."
- "I see the product implications more clearly."
- "This saved me from doomscrolling."

A bad brief feels like:

- a feed dump
- engagement-chasing summaries
- generic trend commentary
- lots of posts, little judgment

## Handling partial coverage

If rate limits, missing APIs, or unavailable accounts prevent full coverage:

- say so briefly
- continue with the strongest partial set
- do not block the whole brief waiting for perfect completeness
- prefer a sharp brief from 8-20 good accounts over a bloated weak summary from 50

## Useful dimensions for interpretation

When extracting insights, pay special attention to these recurring lenses:

- agent vs copilot
- workflow vs one-shot generation
- review/critique vs creation
- system design vs prompt design
- product moat via loop/data/tooling
- professional workflow adoption
- AI-native interface patterns
- model freedom vs guardrails
- vertical use case maturity
- market signals vs hype signals

## If turning this into recurring output

When the user likes a particular style:

- preserve the section order
- preserve the tone
- keep the signal threshold high
- maintain stable formatting so briefs are easy to skim day after day
