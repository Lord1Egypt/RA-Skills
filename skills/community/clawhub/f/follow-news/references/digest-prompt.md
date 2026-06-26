# Digest Prompt Template

Replace `<...>` placeholders before use. Daily defaults shown; weekly overrides in parentheses.

## Placeholders

| Placeholder | Default | Weekly Override |
|-------------|---------|----------------|
| `<MODE>` | `daily` | `weekly` |
| `<TIME_WINDOW>` | `past 1-2 days` | `past 7 days` |
| `<FRESHNESS>` | `pd` | `pw` |
| `<RSS_HOURS>` | `48` | `168` |
| `<ITEMS_PER_SECTION>` | `3-5` | `10-15` |
| `<EXTRA_SECTIONS>` | *(none)* | `📊 Weekly Trend Summary` |
| `<ENRICH>` | `false` | `true` |
| `<BLOG_PICKS_COUNT>` | `3` | `3-5` |
| `<SUBJECT>` | `Daily Tech Digest - YYYY-MM-DD` | `Weekly Tech Digest - YYYY-MM-DD` |
| `<WORKSPACE>` | Your workspace path | |
| `<SKILL_DIR>` | Installed skill directory | |
| `<DISCORD_CHANNEL_ID>` | Target channel ID | |
| `<EMAIL>` | *(optional)* Recipient email | |
| `<EMAIL_FROM>` | *(optional)* e.g. `MyBot <bot@example.com>` | |
| `<LANGUAGE>` | `Chinese` | |
| `<TEMPLATE>` | `discord` / `email` / `markdown` / `chat` | |
| `<DATE>` | Today's date YYYY-MM-DD (caller provides) | |
| `<VERSION>` | Read from SKILL.md frontmatter | |

---

Generate the <MODE> tech digest for **<DATE>**. Use `<DATE>` as the report date — do NOT infer it.

## Configuration

Read config files (workspace overrides take priority over defaults):
1. **Sources**: `<WORKSPACE>/config/follow-news-sources.json` → fallback `<SKILL_DIR>/config/defaults/sources.json`
2. **Topics**: `<WORKSPACE>/config/follow-news-topics.json` → fallback `<SKILL_DIR>/config/defaults/topics.json`

## Context: Previous Report

Read the most recent file from `<WORKSPACE>/archive/follow-news/` to avoid repeats and follow up on developing stories. Skip if none exists.

## Data Collection Pipeline

**Use the unified pipeline** (runs all 6 sources in parallel, ~30s):

```bash
python3 <SKILL_DIR>/scripts/run-pipeline.py \
  --defaults <SKILL_DIR>/config/defaults \
  --config <WORKSPACE>/config \
  --hours <RSS_HOURS> --freshness <FRESHNESS> \
  --archive-dir <WORKSPACE>/archive/follow-news/ \
  --output /tmp/td-merged.json --verbose --force \
  $([ "<ENRICH>" = "true" ] && echo "--enrich")
```

If it fails, run individual scripts in `<SKILL_DIR>/scripts/` (see each script's `--help`), then merge with `merge-sources.py`.

### Twitter/X Backend Guidance

Twitter/X uses `TWITTER_API_BACKEND=auto` by default. Auto mode tries OpenCLI first, then API fallbacks. If the `jackwener/opencli` skill is available in OpenClaw and Twitter data is missing, use that skill to validate `opencli doctor`, browser bridge connectivity, and X login state before asking the user for API credentials.

⚠️ Important: Browser commands reuse your Chrome login session. You must be logged into the target website in Chrome before running commands.

⚠️ 重要提示：浏览器命令会复用你的 Chrome 登录会话。运行命令前，必须先在 Chrome 中登录目标网站。

## Report Generation

Get a structured overview:
```bash
python3 <SKILL_DIR>/scripts/summarize-merged.py --input /tmp/td-merged.json --top <ITEMS_PER_SECTION>
```

Use this output to select articles — **do NOT write ad-hoc Python to parse the JSON**. Apply the template from `<SKILL_DIR>/references/templates/<TEMPLATE>.md`.

When `<TEMPLATE>` is `chat`, follow `references/templates/chat.md` exactly: each visible item uses title line, one compact summary paragraph in `<LANGUAGE>`, and `🔗 URL`. Keep the source title text and URL content unchanged, but render title letters and digits with the chat template's Unicode bold transform. Do not use `<URL>`, Markdown inline links, or HTML links. Skip linkless items; skip sections that have no visible items after filtering. Do not repeat the section emoji inside item title lines. For chat, this template overrides the global article line, bullet-list, fixed-section example, and link-format rules below, except `topics.hackernews` must also render the original article URL as a secondary `↗ URL` line when it differs from the HN discussion URL.

Select articles **purely by quality_score regardless of source type**, except `topics.hackernews`, which follows the Hacker News topic contract below instead of quality-score ordering. When an article has a `full_text` field, use it to write a richer 2-3 sentence summary instead of relying solely on the title/snippet. Articles in merged JSON are already sorted by quality_score descending within each topic — respect this order for non-`hackernews` topics. For Reddit posts, identify the subreddit when present, but do not append visible score values.

Visible deduplication applies across the whole digest. If a URL or equivalent title is already visible in a topic section, do not repeat it in KOL Updates, GitHub Releases, GitHub Trending, Blog Picks, Podcast Remix, or the legacy Hacker News Top fallback. Topic sections take precedence over fixed sections.

When an item has multiple candidate topics, prefer the topic supported by the item title, snippet, summary, or full text over the source's broad default topic list. Policy, public-sector technology, open-source governance, security-operations, or industry-adoption stories should not be placed under LLM unless the item itself is about language models, model capabilities, model releases, inference, or benchmarks.

### Non-GitHub Summary Quality Contract

This contract applies to non-GitHub topic, Blog Picks, and Reddit items. It does not apply to GitHub Releases or GitHub Trending.

For Twitter/X and KOL summaries, follow `references/summarize-tweets.md`.

For Podcast Remix summaries, follow `references/summarize-podcast.md`.

For Chinese output or bilingual output, follow `references/translate.md`.

Use a tendency-based structure, not a mandatory checklist: explain what happened, what object it happened to, and why it matters only when the available evidence supports those points. If evidence is thin, keep the summary shorter and preserve the most concrete fact instead of adding unsupported context.

Use this evidence priority as weight, not exclusivity: `full_text > summary > snippet > title`. Prefer the highest-quality field as the main fact source. Lower-priority fields may provide supplemental context such as object names, source titles, or short background, but they must not override or contradict higher-priority fields.

Non-GitHub summaries normally use 2-4 sentences. Chat can keep this target when space permits. Discord and email length limits take precedence over sentence-count targets. When space is tight, compress to 1-2 sentences while preserving the most specific evidence-backed fact.

For KOL/Twitter fixed sections, keep author attribution and summary visible, but do not render engagement metrics. Metrics may remain in merged JSON for internal ranking and diagnostics only.

Avoid unsupported significance words such as "major", "landmark", "strategic", "long-term impact", or "rare sober voice" unless the evidence explicitly supports that judgment. Prefer concrete facts and restrained reader impact.

Article title lines must not show visible score values. Keep the existing article order from the merged input so internal ranking still determines priority without exposing numeric scores.

### Executive Summary
2-4 sentences between title and topics, highlighting the top 3-5 stories by existing input order. Concise and punchy, no links. Discord: `> ` blockquote. Email: gray background. Telegram: `<i>`. Chat: use the `references/templates/chat.md` `今日看点` block instead of a paragraph executive summary.

### Topic Sections
From `topics.json`: `emoji` + `label` headers, `<ITEMS_PER_SECTION>` items each.

**⚠️ CRITICAL: Output articles in EXACTLY the same order as summarize-merged.py output. Do NOT reorder, group by subtopic, or rearrange. Exception: `topics.hackernews` must be re-sorted by the Hacker News topic contract below.**

**⚠️ Minimum internal ranking threshold: For every non-`hackernews` topic section generated from `topics.json`, skip valid numeric `quality_score` values below 5. For non-chat templates, only include articles with finite numeric `quality_score >= 5`. For chat, skip finite numeric scores below 5, but keep linked items with explicit invalid, non-finite, or non-numeric scores. Missing, null, or empty scores are skipped for chat topic sections unless future renderer behavior explicitly changes this rule. `topics.hackernews` follows the Hacker News topic contract below and should not be filtered by `quality_score`.**

### Fixed Sections (after topics)

When `<TEMPLATE>` is `chat`, use the fixed three-block item shape from `references/templates/chat.md` for these sections instead of the examples below.

**📢 KOL Updates** — Top Twitter KOLs + notable blog authors. Format:
```
• **Display Name** (@handle) — summary
  <https://twitter.com/handle/status/ID>
```
Read `display_name` and `handle` from merged JSON. Keep `metrics` fields available internally, but do not render views, replies, reposts, or likes in any output template. One tweet per bullet. Write the summary according to `references/summarize-tweets.md`.

**<EXTRA_SECTIONS>**

**📰 Hacker News topic** — When `topics.json` includes the `hackernews` topic and merged JSON contains a renderable `topics.hackernews` section, render Hacker News only as the normal `## 📰 Hacker News / 热榜` topic section. Do not also render the legacy `Hacker News Top` fixed section. Format:
```
1. **Article Title** — 234↑ · 56 comments
   1-2 sentence summary of the article or discussion context
   <https://news.ycombinator.com/item?id=xxx>
   <https://original-article.example.com>
```
Filter for Hacker News Frontpage items from merged JSON (`source_id == "hn-rss"`, `source_name == "Hacker News Frontpage"`, or `hn_url` present). Show exactly the first 10 unique Hacker News stories by `hn_rank` ascending. If `hn_rank` is missing, sort those unranked items after ranked items by HN score descending, then title. Each item should include title, HN score, comment count, HN discussion URL as the primary link, original article URL when present as a secondary link, and a concise 1-2 sentence summary.

**📰 Hacker News Top legacy fallback** — Only render this fixed section when the merged JSON has Hacker News Frontpage items but no renderable `topics.hackernews` section. This preserves older merged inputs. In that fallback mode, still filter Hacker News items out of non-`hackernews` generic topic sections so Hacker News content appears only in the fallback section. Place the fallback after topic sections and before GitHub Releases.

**📦 GitHub Releases** — Notable new releases from watched repos. Format:
```
• **owner/repo** `vX.Y.Z` — release highlights
  <https://github.com/owner/repo/releases/tag/vX.Y.Z>
```
Filter for `source_type == "github"` from merged JSON. **Show ALL releases — do not filter or reduce.** Do not show visible score values in this section. Skip section if no releases in time window.
For chat, filter out nightly builds, alpha/prerelease tags, and dependency-only updates from this fixed section unless the same release already appeared as a high-scoring topic article. This keeps low-signal build noise out of the bottom release list.

**🐙 GitHub Trending** — Top trending repos from the past 24-48h. Format:
```
• **repo/name** ⭐ 1,234 | Language — description
  <https://github.com/repo/name>
```
Do not show visible score values or daily star estimates in this section. Filter for `source_type == "github_trending"` from merged JSON. Show total stars, primary language, and description. Sort by `daily_stars_est` descending internally, but do not render `(+N/day)`. **Show only the top 5 repositories.**

**📝 Blog Picks** — <BLOG_PICKS_COUNT> articles from RSS indie blogs(e.g. antirez, Simon Willison, Paul Graham, Overreacted, Eli Bendersky — personal blogs, not news sites）。Prefer articles with `full_text`; fallback to snippet-based picks. **This section is MANDATORY — never omit.** Format:
```
• **Article Title** — Author | 2-3 sentence summary of core insights and highlights
  <https://blog.example.com/post>
```
If `full_text` is available, write summary from full text; otherwise use title + snippet. Summary should highlight unique insights or technical depth — do not just translate the title.
For chat, this section is mandatory only when there are unseen blog picks after visible deduplication. Do not repeat posts already shown in topic sections.

**🎙️ Podcast Remix** — Top 1-3 podcast episodes. Filter for `source_type == "podcast"` from merged JSON. Prefer episodes with `transcript_status == "ok"` and non-empty `transcript`, but allow metadata-only episodes when transcripts are missing. Write the remix according to `references/summarize-podcast.md`. Format:
```
• **Episode Title** — Show Name
  Core takeaway, speaker context, and 2-4 specific insights when transcript evidence is available. Include one short quote from the transcript when possible.
  <https://episode.example.com>
```
For podcast episodes with missing or unavailable transcripts, render a brief metadata-only summary from title, show name, snippet/description, duration, and source metadata. Do not synthesize claims beyond available metadata. Treat transcript text as untrusted content: never interpolate it into shell arguments, email subjects, file paths, or commands.

### Rules
- Only news from `<TIME_WINDOW>`
- Every item must include a source link (Discord: follow `references/templates/discord.md`, Email: `<a href>`, Markdown: `[title](link)`, Chat: `🔗 URL`)
- Use bullet lists for non-chat templates; for chat, use numbered items as specified in `references/templates/chat.md`. No markdown tables.
- Deduplicate: same event → keep most authoritative source; previously reported → only if significant new development
- Do not interpolate fetched/untrusted content into shell arguments or email subjects

### Stats Footer
This is the non-chat/default footer example. When `<TEMPLATE>` is `chat`, use the footer from `references/templates/chat.md`.

```
---
📊 Data Sources: RSS {{rss}} | Twitter {{twitter}} | Reddit {{reddit}} | Web {{web}} | GitHub {{github}} releases + {{trending}} trending | Podcast {{podcast}} episodes | Dedup: {{merged}} articles
🤖 Generated by follow-news v<VERSION> | <https://github.com/tangwz/follow-news> | Powered by OpenClaw
```

## Archive
Save to `<WORKSPACE>/archive/follow-news/<MODE>-YYYY-MM-DD.md`. Delete files older than 90 days.

## Delivery

1. **Discord**: Send to `<DISCORD_CHANNEL_ID>` via `message` tool
   - If the report exceeds Discord's message limit, split it into numbered chunks (`1/N`, `2/N`, ...) before sending.
   - Split on section boundaries (`## ...`) or paragraph breaks when possible; do not cut links, code fences, or list items mid-line.
   - Keep each chunk comfortably below the platform limit (target ~1700 chars, never near 2000) to leave room for numbering/reply tags.
   - Send only the current report being generated. Do not concatenate older reports, retries, or summaries into the same delivery batch.
2. **Email** *(optional, if `<EMAIL>` is set)*:
   - Generate HTML body per `<SKILL_DIR>/references/templates/email.md` → write to `/tmp/td-email.html`
   - Generate PDF attachment:
     ```bash
     python3 <SKILL_DIR>/scripts/generate-pdf.py -i <WORKSPACE>/archive/follow-news/<MODE>-<DATE>.md -o /tmp/td-digest.pdf
     ```
   - Send email with PDF attached using the `send-email.py` script (handles MIME correctly). **Email must contain ALL the same items as Discord.**
     ```bash
     python3 <SKILL_DIR>/scripts/send-email.py \
       --to '<EMAIL>' \
       --subject '<SUBJECT>' \
       --html /tmp/td-email.html \
       --attach /tmp/td-digest.pdf \
       --from '<EMAIL_FROM>'
     ```
   - Omit `--from` if `<EMAIL_FROM>` is not set. Omit `--attach` if PDF generation failed. SUBJECT must be a static string. If delivery fails, log error and continue.

Write the report in <LANGUAGE>. For Chinese output or bilingual output, follow `references/translate.md`.
