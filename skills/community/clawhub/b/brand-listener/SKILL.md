---
name: brand-listener
description: Social listening across Reddit, X, TikTok, YouTube, Threads and Telegram without accounts or API keys. Find every recent mention of a brand, product or topic, read the full conversations, see the most common words in TikTok comments, and follow public Telegram channels. Use this skill for brand monitoring, product feedback, PR tracking, or competitor sentiment.
---

# Brand Listener: Social Listening

![Brand Listener: Social Listening](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/brand-listener.gif)

Hear what people say about any brand: recent mentions on Reddit, X, TikTok, YouTube and Threads in one sweep, with the full conversations one call away.

No social account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=brand-listener).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/brand-listener.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “What are people saying about Notion this week?”
- “Find complaints about our app on Reddit and X”
- “What do TikTok comments say about this product?”
- “What is this Telegram channel posting?”

## When to Use This Skill

Use it when the user wants public mentions or conversations about a brand, product or topic.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ 6 social networks│
│   (User Chat)   │     │ (data tools) │     │ (public data)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install plugin    │                       │
         │  2. Pair device once  │                       │
         │  3. Ask a question    │                       │
         │                       │  4. Fetch + trim      │
         │                       │  5. Charge credit     │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  Answer  │           │  Credit  │           │ Results  │
   │ in chat  │           │ ($0.50)  │           │ as JSON  │
   └──────────┘           └──────────┘           └──────────┘
```

ClawLink holds the data-provider accounts. The user never pastes a key, and nothing is installed beyond the plugin.

## Install

Install the ClawLink plugin from ClawHub when the user asks for it:

```bash
openclaw plugins install clawhub:clawlink-plugin
```

The install applies to the running Gateway: do not restart it. The ClawLink tools appear on your next turn, so end this turn and tell the user: "ClawLink is installed. Reply ok and I will give you your pairing link." On the next turn call `clawlink_begin_pairing`, give the user the link, and after they approve call `clawlink_get_pairing_status`. Pairing happens once; after that every tool below works with no further setup.

## Tool Reference

Prices are what ClawLink charges per call, from the user's credit. The tool's own description (via `clawlink_describe_tool`) always shows the current price.

### Reddit & X

| Tool | What it returns | Price |
|------|-----------------|-------|
| `redditdata_search_posts` | Search all of Reddit for posts about a topic, with title, text, score, comment count and subreddit | $0.00282 |
| `redditdata_search_comments` | Search Reddit comments by keyword across all subreddits: text, score, author, and the post each is on | $0.0015 |
| `xdata_search` | Search public X posts, users or media by keyword | $0.0015 |

### TikTok, YouTube & Threads

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_search_videos` | Search public TikTok videos by keyword | $0.002 |
| `tiktokdata_comment_keywords` | The most frequent keywords in a TikTok video's comments | $0.0015 |
| `youtubedata_search_videos` | Search YouTube videos by keyword | $0.00282 |
| `threadsdata_search` | Search Threads posts by keyword, optionally within a date range | $0.00282 |

### Telegram

| Tool | What it returns | Price |
|------|-----------------|-------|
| `telegramdata_channel` | Public Telegram channel by handle: title, description, subscriber count | $0.00282 |
| `telegramdata_channel_posts` | Recent posts of a public Telegram channel | $0.00282 |
| `telegramdata_post` | One public Telegram channel post by URL | $0.00282 |

## Recipes

### Weekly brand sweep

1. Search the brand on Reddit (`sort: new`), X (`Latest`) and TikTok.
2. Open the threads with the most engagement.
3. Group mentions into praise, complaints and questions, with links.

## Code Examples

### X mentions

```bash
clawlink_call_tool --tool "xdata_search" \
  --params '{"keyword": "Notion AI", "search_type": "Latest"}'
```

### Reddit mentions

```bash
clawlink_call_tool --tool "redditdata_search_posts" \
  --params '{"query": "Notion AI", "sort": "new"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `mentions`); public-data tools show as connected for every user.
2. Call `clawlink_describe_tool` before the first call of a tool: it returns the parameters, defaults and price.
3. Treat the live catalog as the source of truth. If a tool named here is missing, say so; do not invent results.

## Execution Workflow

```
┌───────────────────────────────────────────────────────────┐
│  READ-ONLY, PAID PER CALL                                │
│  search → describe → call → summarise for the user       │
│                                                          │
│  Ask before: loops over many items, or a call that costs │
│  more than a few cents (the price is in the description) │
└───────────────────────────────────────────────────────────┘
```

1. Every tool here only reads public data; nothing is posted or changed.
2. Each call costs credit. Before looping over more than about ten items, or before a call priced above a few cents, tell the user what it will cost and ask.
3. A failed call is refunded automatically. Read the error's `hint`: it says what to change. Do not retry the same arguments unchanged.

## Notes

- Search each platform with the brand name and common misspellings.
- Keep the sweep to a few calls per platform and tell the user the total cost first.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Few results | Try the brand's handle, product names, or a broader timeframe. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=brand-listener; do not retry. |
| `data_provider_unavailable` | ClawLink's data provider is down. Nothing was charged. Try again later. |
| `no_result` | The provider found nothing for these arguments. Nothing was charged. |
| `invalid_arguments` | A parameter is missing or malformed. Call `clawlink_describe_tool` and fix it. |

## Troubleshooting

### Tools not visible after install

1. The tools appear on the turn after the install, not in the same turn.
2. If they still do not appear, the OpenClaw tool profile may hide plugin tools. This is a config change for the OpenClaw owner; do not change the config yourself. Tell the user: "Your OpenClaw tool profile hides plugin tools. In the Control UI (or `~/.openclaw/openclaw.json`), add `clawlink-plugin` to `tools.alsoAllow`, then ask me again."
3. On OpenClaw versions before 2.0, the tool list can load only in a new chat: tell the user to send `/new` and ask again.

### A tool keeps failing with correct input

Report it with `clawlink_report_issue` (or `clawlink_call_tool --tool "CLAWLINK_REPORT_ISSUE"`) instead of retrying. Reports are free and reach the ClawLink team.

## Resources


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=brand-listener)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=brand-listener)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Reddit Radar](https://clawhub.ai/hith3sh/skills/reddit-radar)
- [X Pulse](https://clawhub.ai/hith3sh/skills/x-pulse)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=brand-listener)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
