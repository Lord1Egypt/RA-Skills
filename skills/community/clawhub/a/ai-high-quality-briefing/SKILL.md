---
name: ai-high-quality-briefing
description: Generate high-quality Chinese information briefings for AI, technology, and global expansion topics. Use when the user wants daily news digests, weekly deep briefings, trend tracking, high-signal information filtering, publishable newsletter copy, WeChat/public-account style summaries, internal briefing notes, or recurring scheduled brief generation. Especially use for themes like AI updates, frontier models, arXiv papers, GitHub projects, Hacker News discussions, Hugging Face releases, tech media trends, overseas market intelligence, and 'search the whole web first, then filter for high quality'.
---

# AI / 科技 / 出海高质量信息简报

Produce concise, high-signal Chinese briefings from broad web research.

Read `/Users/youke/.openclaw/workspace/skills/ai-high-quality-briefing/references-query-patterns.md` when you need search starters.
Read `/Users/youke/.openclaw/workspace/skills/ai-high-quality-briefing/references-scoring-and-format.md` when you need ranking, de-duplication, or publishable copy structure.
Read `/Users/youke/.openclaw/workspace/skills/ai-high-quality-briefing/references-no-key-sources.md` when `web_search` is unavailable or the environment has no search API key.

## Core workflow

1. Clarify the briefing mode if the user did not specify it:
   - **每日快讯**: 5–12 items, short and fast
   - **每周深度版**: 3–6 themes, grouped analysis, stronger commentary
2. Define the scope:
   - Topic: AI / technology / overseas expansion, or a narrower subtopic the user gives
   - Time window: today / last 24h / this week / custom range
   - Audience: public post / internal briefing / founder / investor / operator
3. Discover candidate items using one of these paths:
   - **Preferred path**: `web_search` for broad discovery, then `web_fetch` for verification
   - **No-key fallback path**: if `web_search` is unavailable, use curated public pages and `web_fetch` directly; optionally use browser snapshot on already-open or login-required pages
4. Score and rank candidate items before writing.
5. Remove duplicates, weak reposts, and thin summaries.
6. Write in Chinese with an editor’s judgment, not a raw link dump.
7. If the user wants publishable copy, produce platform-ready versions instead of one neutral block.

## No-key fallback policy

If `web_search` fails because the environment has no API key:

1. Do not stop.
2. Switch to the fallback source list in `references-no-key-sources.md`.
3. Fetch a small set of strong public pages directly with `web_fetch`.
4. Prefer official or source-near pages over commentary pages.
5. Be explicit in the output that this run is based on curated public sources instead of broad web search, if that limitation materially affects coverage.

## Source priorities

Prefer this order unless the user says otherwise:

1. arXiv
2. GitHub
3. Hacker News
4. Hugging Face
5. Mainstream tech media
6. Official product / company blogs

When covering overseas expansion, also prioritize:
- official company announcements
- product pages / docs
- reputable global business or tech reporting
- region-specific market signals if relevant

## Output standards

Always include:
- a sharp title
- a short opening summary
- the main items grouped logically
- why each item matters
- source links

Do **not** just summarize. Add editorial value:
- what changed
- why it matters
- who should care
- whether it is signal or noise

## Default output templates

### Template A — 每日快讯

Use this for fast-moving updates.

Structure:

```markdown
# 今日 AI / 科技 / 出海简报｜YYYY-MM-DD

一句话总览：用 1–2 句话总结今天最值得关注的主线。

## 1. 最重要的 3 条
### [标题]
- 发生了什么：
- 为什么重要：
- 适合谁关注：
- 来源：

## 2. 值得关注的新工具 / 新模型 / 新项目
- [名称]：一句话说明 + 为什么值得看
- 来源：

## 3. 可直接拿去发的短文案
### 朋友圈/社媒版
...

### 公众号/内部群版
...
```

### Template B — 每周深度版

Use this for synthesis and stronger interpretation.

Structure:

```markdown
# 本周 AI / 科技 / 出海高质量简报

## 本周结论
- 结论 1
- 结论 2
- 结论 3

## 一、本周最重要趋势
### 趋势标题
- 发生了什么
- 背后逻辑
- 影响判断
- 代表案例
- 来源

## 二、值得重点追踪的项目 / 公司 / 论文 / 工具
### 名称
- 核心信息
- 亮点
- 局限或风险
- 适用场景
- 来源

## 三、对内容运营 / 产品 / 出海的启发
- 启发 1
- 启发 2
- 启发 3

## 四、可直接发布的文案
### 公众号版
...

### 朋友圈版
...

### 内部汇报版
...
```

## Writing style

Use:
- Chinese, clean and publishable
- Dense but readable language
- Concrete judgment instead of hype
- Short paragraphs and bullets

Avoid:
- empty adjectives like “震撼”“炸裂” unless the user explicitly wants hype
- too many items with no hierarchy
- long untranslated English passages
- fake certainty when evidence is weak

## Ranking heuristic

When you have many candidates, rank by:
1. importance
2. novelty
3. practical relevance
4. discussion / traction quality
5. credibility of source

A smaller high-quality briefing beats a larger noisy one.

## Publishable copy generation

When the user wants “可发布文案”, provide at least 2 versions:
- a shorter social version
- a fuller article/internal briefing version

If the user’s platform is unknown, default to:
- **社媒短版**: 80–180 Chinese characters
- **长版摘要**: 300–800 Chinese characters

## Scheduling guidance

When the user wants recurring briefings:
- use `cron`
- prefer reminders that clearly state the theme, cadence, and desired format
- mention whether it is a daily fast digest or weekly deep digest
- include the latest scope in the reminder text so future runs stay consistent

Example reminder text:
- `提醒：生成今日 AI / 科技 / 出海高质量信息简报。先全网搜索，再筛高质量信号，优先 arXiv、GitHub、Hacker News、Hugging Face 和主流科技媒体；若搜索工具不可用，则改用公开页面与站点直抓；输出中文每日快讯，并附可直接发布的短版与长版文案。`
- `提醒：生成本周 AI / 科技 / 出海高质量信息深度简报。按趋势分组，突出最重要变化、项目、论文、工具与出海启发；若搜索工具不可用，则改用公开页面与站点直抓；输出中文每周深度版，并附公众号版、朋友圈版、内部汇报版文案。`

## Tool use pattern

### Path A — With search key
1. Start with `web_search` using focused topic queries
2. Collect 5–15 promising candidates
3. Use `web_fetch` to verify the best ones
4. Write only after filtering

### Path B — No search key
1. Open the fallback source list
2. Fetch 1–3 public pages per source with `web_fetch`
3. Extract only fresh, concrete items
4. Merge duplicates
5. Write only after filtering

Suggested query patterns:
- `latest AI model releases this week`
- `best new GitHub AI tools this week`
- `important arXiv AI papers this week`
- `Hacker News AI startup tools this week`
- `global expansion SaaS AI trends this week`

When a topic is broad, split queries by source or theme instead of relying on one giant search.

## Quality bar before finalizing

Before sending, check:
- Is each item actually worth the reader’s time?
- Did I explain why it matters?
- Did I avoid repeating the same story from multiple angles?
- Is the output already usable as a post, summary, or internal brief?

If not, tighten it.
