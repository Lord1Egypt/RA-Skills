---
name: backlink-detective
description: Backlink and domain research with no SEO subscription or API key. Backlink summary (total backlinks, referring domains, domain rank, spam score), the backlinks and referring domains themselves, a domain's traffic overview, its organic competitors, and the keywords it ranks for. Use this skill for link building, competitor SEO analysis, domain due diligence, or auditing a site's authority.
---

# Backlink Detective: Domain & Backlink Research

![Backlink Detective: Domain & Backlink Research](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/backlink-detective.gif)

Size up any website: how many sites link to it, who they are, how authoritative it is, which competitors fight it in search, and which keywords bring it traffic.

No SEO-tool account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=backlink-detective).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/backlink-detective.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “How strong is notion.so's backlink profile?”
- “Who links to my competitor but not to me?”
- “Which keywords does ahrefs.com rank for?”
- “Who are this domain's organic competitors?”

## When to Use This Skill

Use it when the user wants backlinks, domain authority, competitors or ranking keywords for a domain.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Backlink index   │
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

### Backlinks

| Tool | What it returns | Price |
|------|-----------------|-------|
| `seodomaindata_backlinks_summary` | A domain's backlink profile: total backlinks, referring domains, domain rank (0-1000), spam score and broken links | $0.036054 |
| `seodomaindata_backlinks` | Backlinks pointing to a domain or page: linking URL, anchor text, dofollow flag, rank and first-seen date | $0.03708 |
| `seodomaindata_referring_domains` | Domains that link to a domain or page, with how many backlinks each gives and its rank | $0.03708 |

### Domain & Competitors

| Tool | What it returns | Price |
|------|-----------------|-------|
| `seodomaindata_domain_overview` | A domain's Google organic and paid footprint: ranking keyword count, estimated monthly traffic and how many keywords… | $0.01818 |
| `seodomaindata_competitors` | Domains that compete with a domain in Google organic search: shared keywords, average position and their estimated… | $0.0198 |
| `seodomaindata_ranked_keywords` | Keywords a domain or URL ranks for in Google, with position, ranking URL, search volume and estimated traffic,… | $0.0216 |

## Recipes

### Find link opportunities

1. `seodomaindata_referring_domains` for a competitor.
2. The same for your own domain.
3. List domains that link to them and not to you, strongest first.

## Code Examples

### Backlink summary

```bash
clawlink_call_tool --tool "seodomaindata_backlinks_summary" \
  --params '{"target": "notion.so"}'
```

### Referring domains

```bash
clawlink_call_tool --tool "seodomaindata_referring_domains" \
  --params '{"target": "notion.so", "limit": 20}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `backlinks`); public-data tools show as connected for every user.
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

- Pass a bare domain (`notion.so`), not a URL with a path, for domain-wide data.
- Backlink tools cost a few cents and are priced per row: keep `limit` modest.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Invalid target | Use a domain like example.com, without https:// or a path. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=backlink-detective; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=backlink-detective)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=backlink-detective)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Site Auditor](https://clawhub.ai/hith3sh/skills/site-auditor)
- [Keyword Miner](https://clawhub.ai/hith3sh/skills/keyword-miner)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=backlink-detective)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
