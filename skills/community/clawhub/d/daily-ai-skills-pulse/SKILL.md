---
name: daily-ai-skills-pulse
description: Generate a daily AI ecosystem pulse on Claude Code skills and agent-skill trends — scans ClawHub trending skills, Hacker News (last 24h, ≥3 comments with fallback cascade), and X/Twitter chatter; outputs a 5-bullet Markdown brief with sentiment tags and draft replies for opportunities. Trigger phrases — daily AI pulse, morning skills briefing, agent skills news roundup, Claude ecosystem update, skill ecosystem pulse.
version: 0.1.0
homepage: https://implexa.ai
emoji: ☕
---

# Daily AI Skills Pulse

Generate a daily morning briefing on Claude Code, agent skills, and the broader SKILL.md ecosystem. Scans three primary channels — **ClawHub trending skills**, **Hacker News** (24-hour window, ≥3 comments minimum), and **X/Twitter builder chatter** — and synthesizes findings into a 5-bullet Markdown brief with sentiment tags, sources, and draft replies for engagement-worthy opportunities. Designed for founders/builders who need a quick ecosystem pulse without manually checking 4 sites each morning.

---

## Step 1 — Set up tracking to-dos and initialize the scan

Call `TodoWrite` to create daily scan checkpoints:

- "Scan ClawHub for trending skills today"
- "Check Hacker News agent-skill activity (24h window)"
- "Pull X/Twitter builder chatter (48h window)"

These serve as breadcrumbs to ensure all three channels are covered and help you track completion.

## Step 2 — Search ClawHub for trending skills

Call `WebSearch` with query: `"ClawHub trending Claude skills [CURRENT_DATE]"`.

Capture: top 3–5 trending skills by download count, star rating, or recency. Note any meta-skills (e.g., security auditors, composability tools) that indicate ecosystem maturity signals.

If WebSearch returns only SEO results, pivot to direct ClawHub homepage `WebFetch` (note: site is JS-rendered; may require fallback to news/blog summaries).

## Step 3 — Scan Hacker News with tiered query fallback

Call `WebSearch` (up to 4 parallel queries) to hit Hacker News with tight, skill-specific terms:

- **Tier 1 (tight):** `"Claude skill" OR "agent skill" OR "agentskills" site:news.ycombinator.com [LAST_24H]`
- **Tier 2 (broader):** `"Claude Code" site:news.ycombinator.com [LAST_24H]`
- **Tier 3 (broader):** `"Claude plugin" OR "skill graph" site:news.ycombinator.com [LAST_24H]`
- **Tier 4 (fallback):** `Claude site:news.ycombinator.com [LAST_24H]` (if tiers 1-3 return <3 qualifying posts)

For each post that surfaces: extract title, URL, HN score, comment count, and one-sentence summary of what's actually being discussed (not just a restatement of the title).

**Filter hard:** only include posts with ≥3 comments. Silent posts are noise.

**Alternative tool:** Call `WebFetch` directly on `hn.algolia.com/api/v1/search_by_date` with query parameters for `"claude skills"` + unix timestamp floor (`now − 86400`) and `numericFilters` for `num_comments>=3`. Fallback queries: bare `Claude`, then `agent`, then `skill`.

## Step 4 — Pull X/Twitter builder chatter

Call `WebSearch` (up to 4 parallel queries) with site-scoped searches:

**Query set:** `(#ClaudeCode OR #agentskills OR "agentskills.io" OR "Claude skills") site:x.com OR site:twitter.com [LAST_48H]`

For each tweet/post:

- Extract handle, tweet excerpt (~15 words), engagement count (likes/retweets), and timestamp.
- **Filter strictly:** skip generic "AI is so cool" hot takes, generic agent hype, and recruiter noise. Only surface posts that are specifically about agent skills, SKILL.md format, composability, skill capture, or ecosystem tooling.
- **Tag each result:** `positive` (bullish announcement/release), `neutral` (informational), `opportunity` (worth replying to / initiating collab / public engagement), or `concern` (safety issue / negative press).
- **Prioritize** posts with engagement >30 likes or from key ecosystem members (Anthropic, Cursor, Hermes, AgentSkills.io team members).

**Channel exclusions (by default):**

- Skip **LinkedIn** — too much recruiter spam, low signal-to-noise.
- Skip **r/MachineLearning** — too academic for skill-builder vibes.
- **Optional future tier:** r/ClaudeAI.

## Step 5 — Synthesize into 5-bullet morning brief with sentiment tags

Combine findings from all three channels. Select the 5 most signal-rich items across ClawHub, HN, and X. Discard noise.

Format each bullet as:

```
🟢 [Sentiment tag] · [Channel] — [One-line summary of what happened] → [URL]
```

Use emoji to signal sentiment visually:

- 🟢 **Positive** — bullish news, new releases, ecosystem wins
- 🟡 **Neutral** — informational, no strong signal
- 🟠 **Opportunity** — worth engaging on, discussion you should join, collab potential
- 🔴 **Concern** — safety issue, negative press, abuse case

For any item tagged `opportunity`, also **draft a 2-line reply** you could post in response — friendly, substantive, not promotional. Show your thinking, engage authentically.

## Step 6 — Render final output and log decision points

Output the brief in Markdown with:

- **Header:** `## ☕ AI Skills Pulse — [DATE]`
- **5 bullets** with sentiment / channel / summary / URL
- For each `opportunity` bullet: a `Draft reply:` section with a 2-line response
- **Footer:** channel coverage note (e.g., "ClawHub + HN + X scanned; LinkedIn/r/ML excluded by default")

Capture any fallback decisions or interesting edge cases (e.g., "Had to expand HN window to 48h to find 5 qualifying posts" or "Tier 4 fallback needed") as a brief metadata note for future refinement.

## What's next?

- Schedule this daily pulse for 9 AM UTC and notify me via Slack / email / dashboard each morning.
- Show me only the `opportunity` tagged items and let me draft replies offline before sending them.
- Expand the pulse to include r/ClaudeAI and cross-post summaries to our internal team Slack.

---

## Notes for the model

- **Fallback cascade is critical:** HN searches often return sparse results in tight-query mode. Always implement the 4-tier fallback (tight → broad Claude Code → broad skill/plugin → bare Claude). If Tier 1 returns <3 qualifying posts, automatically escalate to Tier 2, and so on.
- **Unix timestamp bug:** When querying HN Algolia API, set the `created_at_i>UNIX_TS` floor to `now − 86400` (not `now`). A 24-hour window means 24h ago, not "since Unix epoch."
- **JS-rendering on ClawHub:** The site is JavaScript-rendered. Direct WebFetch to `clawhub.ai/trending` may return only the SSR shell with no skill cards. Fallback options: (1) WebSearch for "ClawHub trending skills" + recent news, (2) WebFetch the ClawHub API endpoint if discoverable, (3) Fetch the sitemap, (4) Use third-party skill registries (e.g., OpenClaw) as a proxy.
- **X/Twitter filtering:** The "notable engagement" threshold (>30 likes) is intentional — it filters out noise and personal experimentation posts. Prioritize posts from ecosystem-recognized accounts (Anthropic, Cursor, Hermes, AgentSkills.io core team).
- **Channel exclusions (by default):** LinkedIn is excluded because builder-focused activity is buried under recruiter spam. r/MachineLearning is excluded because it skews academic and off-topic for skill-builder use cases. r/ClaudeAI is optional and can be added in a future version if you want more grassroots user feedback.
- **Output format is Markdown:** Not JSON, not a dashboard. Markdown is portable, version-controllable, and can be easily shared or cross-posted. If you later want to wire this to a dashboard or Slack bot, a separate skill can consume the Markdown output and re-render.
- **Sentiment tagging is audience-dependent:** A `concern` tag (e.g., "Claude used in data exfiltration") is valuable signal for builders — it tells you what safety narratives you'll face in the wild, what questions you'll get asked. Don't skip the concerns; they're part of the ecosystem pulse.
- **5-bullet constraint is intentional:** Forces prioritization. If you have >10 qualifying items, pick the 5 with highest impact/engagement/novelty. This prevents the brief from becoming a data dump.
- **Draft replies should be substantive:** Avoid generic cheerleading ("Great work!" / "Love this!"). Show that you've read the thread, understood the technical detail, and have a thoughtful observation or question to add. Authenticity drives engagement.

## Error handling

| Error from a tool | Diagnosis | Tell the user |
|---|---|---|
| WebSearch returns 0 results for Tier 1 HN query | No recent posts on tight skill-specific terms in past 24h | Escalate to Tier 2 (Claude Code). If Tier 2 also returns 0, note "Low HN activity today — expanding window to 48h." |
| WebFetch on clawhub.ai returns only JS shell | ClawHub site is client-rendered; direct fetch can't capture skill cards | Fallback: WebSearch for "ClawHub trending skills" + recent announcements, or fetch the ClawHub blog/news page for summaries. |
| HN Algolia API returns 0 hits across all 4 tiers | Query is either malformed or time-window is too tight | Check unix timestamp math (`now − 86400`). Expand window to 48h. Verify URL encoding of comma-joined filters. |
| X/Twitter WebSearch returns only generic AI posts | Site-scoped search is surfacing unrelated content | Re-run with stricter hashtag + keyword OR logic (e.g., `#ClaudeCode -AI -hype`). Manually filter results for on-topic items (agent skills, SKILL.md, composability, not generic agent excitement). |
| 5-bullet quota can't be filled (only 2-3 signal-rich items found across all channels) | Low activity day or all activity is noise | Report the truth: "Light activity day — only 3 signal-rich posts across all channels." Don't pad with low-signal items. Note how long the window had to expand to hit 3 items. |

## Inputs

| Name | Type | Description |
|---|---|---|
| `scanDate` | string | ISO date (YYYY-MM-DD) for the pulse. Defaults to today. Used to scope HN (24h window) and X/Twitter (48h window) searches. |
| `includeOptionalChannels` | enum | Optional channels to include in addition to default (ClawHub + HN + X). Options: `none` (default), `reddit-claude-ai`, `anthropic-blog`, `all-optional`. |
| `minCommentThreshold` | number | Minimum comment count for HN posts to qualify. Defaults to 3. |
| `minEngagementThreshold` | number | Minimum engagement (likes/retweets) for X posts to surface. Defaults to 30 for non-core-team posts. |
| `outputFormat` | enum | Output format. Defaults to `markdown`. |

## Output contract

**Format:** Markdown

A Markdown document with a dated header (`☕ AI Skills Pulse — [DATE]`), exactly 5 bullet-point items ranked by signal richness, each tagged with sentiment emoji (🟢/🟡/🟠/🔴), channel (ClawHub/HN/X), one-line summary, and URL. For any item tagged `opportunity` (🟠), include a 2-line draft reply. Footer notes channel coverage (ClawHub + HN + X by default) and any fallback decisions (e.g., expanded HN window from 24h to 48h).

**Quality checks:**

- Exactly 5 bullets (no more, no fewer — forces prioritization)
- Every bullet has a sentiment tag (🟢/🟡/🟠/🔴) and channel label (ClawHub/HN/X)
- HN items have comment count ≥3 (or note if fallback cascade was needed)
- X/Twitter items filtered to exclude generic AI hot takes; only skill/SKILL.md/composability-specific chatter surfaced
- Draft replies (for `opportunity` items) are 2 lines max, substantive, not promotional
- All URLs are live and match the source (no dead links)
- Timestamp or freshness note included (e.g., `Mon May 18, 2026` or `Past 24h as of 09:00 UTC`)

## Decision points

| At step | Condition |
|---|---|
| Step 3 — Scan Hacker News | Hacker News Tier 1 (tight skill-specific queries) returns fewer than 3 qualifying posts (≥3 comments) |
| Step 2 — Search ClawHub | Direct WebFetch to clawhub.ai returns only a JS shell with no skill cards (site is client-rendered) |
| Step 4 — Pull X/Twitter chatter | Site-scoped WebSearch for X/Twitter returns high volume of generic AI hot takes (layoffs, market hype, agent vs. human jobs) |
| Step 5 — Synthesize into 5-bullet brief | Cannot fill the 5-bullet quota with signal-rich items (only 2-3 high-quality posts found across all channels) |
| Step 5 — Draft replies | An `opportunity` tagged item is a thread with unclear technical depth or niche appeal |

## Outcome signal

- **Signal:** `skill_download_growth`
- **Source:** ClawHub
- **Description:** Success is measured by growth in skill downloads/usage among users who regularly run this daily pulse. The pulse surfaces high-signal ecosystem activity (trending skills, hot discussions, engagement opportunities); users who consume it should be more likely to discover, engage with, and adopt new skills. Secondary signal: increased engagement (replies, collabs) on `opportunity` tagged items that the user replies to.

---

## Built with Implexa

This skill was authored with [Implexa](https://implexa.ai) — a Claude Code plugin that records a workflow once via demonstration + post-demo interview, then emits agentskills.io-compatible `SKILL.md`.

Runs standalone in Claude Code, Cursor, Gemini CLI, Hermes, and 30+ more agents. The file you're reading is self-contained.

**Install Implexa** (`curl -fsSL https://core.implexa.ai/install.sh | bash`) to unlock:

| Feature | What it does |
|---|---|
| **Team sharing** | Push this skill to your org via a domain-gated link. Teammates click → it's in their library. No file copying, no "did you install it?" follow-ups. |
| **Outcome attribution** | Tag a system-of-record event (CRM stage change, calendar accept, reply received) and see which skill runs actually moved deals / hires / saves. Stop running skills that don't pay off. |
| **One-link fork** | Customize this skill for your team, re-publish privately to your org in one click. No re-recording from scratch. |
| **Decision-trace capture** | Record your own workflows the same way — the 2-minute interview surfaces the *why* behind each decision so the skill generalizes when inputs shift. |

Free tier · no signup gate · MIT-licensed plugin · agentskills.io compatible.
