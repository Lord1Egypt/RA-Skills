---
name: creator-scout
description: Influencer and creator research across TikTok, Instagram and YouTube with no accounts or API keys. Find creators by niche and country, read profiles and follower counts, see where a creator's audience lives, find similar creators, get public business contact emails, and review recent posts and engagement. Use this skill for influencer marketing, creator vetting, brand partnerships, or UGC sourcing.
---

# Creator Scout: Influencer Research

![Creator Scout: Influencer Research](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/creator-scout.gif)

Vet a creator before you pay them: follower counts, recent posts and engagement, where their audience actually lives, similar creators to compare, and the business contact they publish.

No TikTok, Instagram or YouTube account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=creator-scout).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/creator-scout.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “Where is Khaby Lame's TikTok audience?”
- “Find TikTok creators in the US with 100K-1M followers”
- “Find creators similar to @mkbhd on YouTube and their business emails”
- “Compare the engagement on these three Instagram accounts”

## When to Use This Skill

Use it when the user wants to find, compare or vet creators on TikTok, Instagram or YouTube using public data.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ TikTok/IG/YouTube│
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

### TikTok

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_popular_creators` | Popular TikTok creators, filtered by size and country | $0.00282 |
| `tiktokdata_user_profile` | Public TikTok profile by username: follower and like counts, bio, verified flag, user id | $0.002 |
| `tiktokdata_user_posts` | Recent public videos of a TikTok user with views, likes, comments and shares | $0.002 |
| `tiktokdata_audience_demographics` | Where a TikTok creator's audience is: share of followers by country (and age and gender when TikTok exposes them) | $0.027 |
| `tiktokdata_user_region` | The country a TikTok account is registered in | $0.00282 |
| `tiktokdata_similar_users` | Accounts similar to a TikTok creator | $0.0015 |
| `tiktokdata_profile_contact` | Contact details a TikTok account publishes on its profile (business email, phone or links) for partnership outreach | $0.00174 |
| `tiktokdata_fake_views_check` | Estimates how much of a TikTok video's view count is fake or inorganic | $0.015 |

### Instagram

| Tool | What it returns | Price |
|------|-----------------|-------|
| `instagramdata_search_users` | Search public Instagram accounts by a keyword in their bio or captions | $0.00282 |
| `instagramdata_user_profile` | Public Instagram profile by username: follower, following and post counts, bio, category, verified flag | $0.00282 |
| `instagramdata_user_posts` | Recent public posts of an Instagram account with likes, comments and captions | $0.00282 |
| `instagramdata_similar_users` | Accounts Instagram suggests as similar to a given account | $0.003 |

### YouTube

| Tool | What it returns | Price |
|------|-----------------|-------|
| `youtubedata_search_channels` | Search YouTube channels by keyword; returns handles and channel ids for channel_info and channel_videos | $0.002 |
| `youtubedata_channel_info` | A YouTube channel's subscriber count, video count, description and links | $0.002 |
| `youtubedata_channel_videos` | Recent uploads of a YouTube channel | $0.002 |
| `youtubedata_channel_contact_email` | The business inquiry email a YouTube creator publishes behind the channel's 'View email address' button, for… | $0.1077 |

## Recipes

### Vet one creator

1. Profile: `tiktokdata_user_profile` / `instagramdata_user_profile` / `youtubedata_channel_info`.
2. Recent posts for real engagement (views, likes, comments per post).
3. `tiktokdata_audience_demographics` to check the audience is in your market.
4. `tiktokdata_fake_views_check` on a suspicious video.

### Build a shortlist

1. `tiktokdata_popular_creators` filtered by follower range and country, or `tiktokdata_similar_users` from one creator you like.
2. Contacts: `tiktokdata_profile_contact` or `youtubedata_channel_contact_email`, only for outreach the user asked for.

## Code Examples

### Audience by country

```bash
clawlink_call_tool --tool "tiktokdata_audience_demographics" \
  --params '{"handle": "khaby.lame"}'
```

### Popular creators

```bash
clawlink_call_tool --tool "tiktokdata_popular_creators" \
  --params '{"followerCount": "100K-1M", "creatorCountry": "US"}'
```

### YouTube business email

```bash
clawlink_call_tool --tool "youtubedata_channel_contact_email" \
  --params '{"handle": "@mkbhd"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `creator`); public-data tools show as connected for every user.
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

- `youtubedata_channel_contact_email` costs about $0.11 and takes about 20 seconds; confirm before running it on many channels.
- Contact details are the business contacts creators publish; use them for the outreach the user asked for.
- `tiktokdata_similar_users` needs the creator's `sec_uid`: get it from `tiktokdata_user_ids`.
- `tiktokdata_popular_creators` depends on TikTok's Creative Center and is sometimes unavailable.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Account is private | Private accounts return little or nothing. Choose a public creator. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=creator-scout; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=creator-scout)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=creator-scout)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [TikTok Trend Radar](https://clawhub.ai/hith3sh/skills/tiktok-trend-radar)
- [Ad Spy](https://clawhub.ai/hith3sh/skills/ad-spy)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=creator-scout)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
