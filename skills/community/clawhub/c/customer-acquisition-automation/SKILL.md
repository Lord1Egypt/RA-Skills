---
name: customer-acquisition-automation
description: Customer-acquisition desk for indie tools. Collects public pain-point leads from Reddit, X, and public competitor threads, writes channel-native drafts, and builds a human approval queue. Does not post until the user confirms. Use when the user says run acquisition, today's acquisition, start the acquisition pipeline, collect promo leads, or draft outreach.
---

# Customer Acquisition Automation

Core loop: **collect → write → approve**. Publish is a separate, human-gated step. This public skill does not auto-post and does not promise signups.

## When to use

The user wants a day's worth of public leads and draft replies, then will decide what (if anything) goes out.

## Rights and AIGC

1. **Public pages only.** Do not bypass logins, CAPTCHAs, or rate limits. Do not use unofficial scrapers against a site's ToS.
2. **No private data.** Handle, public profile URL, public post URL. No scraped emails, DMs, or phone numbers.
3. **Drafts are AIGC.** Label internally as AI-assisted copy. The user owns the send. Do not impersonate a customer or a reviewer.
4. **No invented proof.** Do not write fake metrics, fake testimonials, fake "early-bird" prices, gift codes, or star ratings. If a price is needed, ask the user for the live number first.
5. **No spam.** Each draft must answer a specific public post. Duplicate blasts are out of scope.

If a channel requires an official API token the user has not provided, collect and draft only. Do not post.

## Workflow

### 1. Collect

Build a lead pool for *today* (smoke run: 5–8 rows is enough; a full day aims at ≥10).

Sources (public search / official APIs if the user already configured them):

- Reddit: r/SaaS, r/Entrepreneur, r/sideproject, r/indiehackers — questions, pain, "what tool do you use"
- X: public posts about AI content tools, indie SaaS, prompt workflows
- Public competitor threads: complaints and feature asks only, from pages anyone can open

Each row:

| field | meaning |
| --- | --- |
| date | ISO date |
| source | subreddit / account / site |
| platform | reddit / x / other |
| topic | short label |
| pain_point | one sentence from the post |
| url | original link (required) |
| priority | high / mid / low |
| channel | reddit-comment / reddit-post / x / outreach-draft |
| status | new |

Append to `references/lead-pool.csv` if that file exists; otherwise print a table and save CSV in the working directory. Every row needs a live URL. Drop rows you cannot open.

Creator scouting (optional): public mid-size AI-video accounts. Name, public follower band, niche, public profile URL. Stop at 5–10 for a smoke run.

### 2. Write

From today's leads, draft 5–10 pieces. Match the channel:

- **Reddit comment:** 200–400 words, answers the question, one optional mention of the user's real tool, no hard sell
- **Reddit post:** only if the user asked for a post; 500–800 words; substance first
- **X:** 140–280 characters; one idea; no duplicated copy across the batch
- **Outreach draft:** 150–250 words; first line cites a specific public video or post; soft close. User sends it.

Voice: specific, calm, no hype. Every draft cites the source URL. Hooks in the first line. **Do not insert a price unless the user supplied one this session.**

Save as `assets/daily-content-[YYYY-MM-DD].md`.

### 3. Approve (hard stop)

Build an approval table:

`id | channel | preview | source URL | confirm / edit / drop`

Show it. **Do not publish.** Wait.

Log the decision to `references/approval-log.csv` when the user answers.

### 4. Publish (only after confirm)

If the user confirmed *and* an official API (or the user themselves) is doing the send:

- Reddit: follow subreddit rules; new accounts comment before posting; no link dump on day one
- X: official API only; do not burst
- Outreach: user sends; this skill does not log into DMs
- Competitor sites: drafts only — never auto-comment on a third-party product page

Record `references/publish-log.csv`: URL, time, account (no tokens). If the user has not confirmed, skip this layer entirely.

### 5. Feedback (optional, next day)

If the user pastes public metrics (upvotes, replies), append `references/feedback-log.csv`. Do not scrape private analytics.

## Stop conditions

- No source URL → drop the lead.
- User has not approved → no publish.
- Channel is rate-limited or banned → stop that channel and report.
- Copy would need a discount, gift, or rating the user did not state → omit it.

## License

CC BY-SA 4.0. Commercial use allowed. Credit the author and share derivatives under the same license.
