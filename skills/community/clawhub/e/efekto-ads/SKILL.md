---
name: efekto-ads
description: Run paid ads for a small business or a new app from chat - Facebook, Instagram and Google ads made from a website address, published, and switched off when they stop bringing leads. Uses the Efekto MCP server.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📣"
    homepage: "https://efekto.ai/openclaw"
    requires:
      bins: []
---

# Efekto: ads that run themselves

Use this skill when the user wants customers, leads, signups or first users from paid ads and does not want to
learn Ads Manager: "get me customers", "run ads for my business", "promote my app", "how are my ads doing",
"how many leads this week", "pause my ads", "set my ad budget".

Efekto (https://efekto.ai) makes Facebook, Instagram and Google ads from a website address: it writes the copy,
makes images and video, publishes the ads, and every morning turns off the ones that do not bring inquiries.
The user can run on Efekto's own ad account (prepaid wallet), so no Meta Business setup is needed to start.

## One-time setup

Connect the Efekto MCP server (OAuth, the user signs in to Efekto in the browser and clicks Allow):

```bash
openclaw mcp add efekto --url https://efekto.ai/api/mcp --transport streamable-http --auth oauth
openclaw mcp login efekto
openclaw mcp doctor efekto --probe
```

If the user has no Efekto account yet, `preview_ads_from_website` still works after sign-up at
https://efekto.ai - creating the account is free, a plan is needed only to publish.

## Tools (Efekto MCP)

| Tool | What it does |
| --- | --- |
| `preview_ads_from_website` | Makes 3 ready ads from a website address. Takes up to about a minute; returns a `preview_id` to poll. |
| `list_businesses` | Businesses (brands) on the account. |
| `get_account_status` | What is connected, what is missing, what to do next, with links. |
| `get_campaign_results` | Spend, inquiries and cost per inquiry for the last 7 or 30 days. |
| `list_leads` | New inquiries (contact details only for the account owner). |
| `list_pending_ads` | Ads waiting for approval. |
| `approve_ads` / `reject_ad` | Approve or reject pending ads. |
| `publish_ads` | Publish approved ads. |
| `set_daily_budget` | Change the daily budget (minimum about $15 / 50 PLN per day). |
| `pause_campaign` / `resume_campaign` | Stop or restart a campaign. |

## How to work

1. Start with `get_account_status`. It says what the user still has to do (connect a page, add funds, pick a plan).
   Tell them the next step in one sentence with the link it returns.
2. New business or app: call `preview_ads_from_website` with the site address, show the three ads (headline,
   text, image link) and ask which to keep.
3. Never spend money silently. Before `publish_ads`, `resume_campaign` or `set_daily_budget`, state the daily
   budget and what will go live, and wait for a clear yes.
4. Reporting: use `get_campaign_results` and answer with three numbers - spend, inquiries, cost per inquiry -
   plus one recommendation. No jargon (no CTR, CPM, ROAS unless asked).
5. A good recurring task for the user: every Monday, results for the last 7 days and new leads.

## Recipe: first users for a new app

"Give your agent $15 a day": the user gives the address of the app's landing page, you make three ads with
`preview_ads_from_website`, they approve, you publish with a $15 daily budget, and every morning you report
signups and cost per signup. After 7 days recommend: keep, change the offer, or stop.

## Limits

- Publishing needs an Efekto plan and either a connected Meta/Google account or Efekto's prepaid ad account.
- Up to 5 new previews per day per user.
- Efekto does not promise results; report real numbers only.
