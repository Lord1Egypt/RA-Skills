---
name: event-finder
description: Find events on Facebook without an account or API key. Search public events by keyword, browse a city's events, read an event's date, venue and description, and list the events a page hosts. Use this skill for finding things to do, scouting conferences and meetups, competitor event tracking, or planning a calendar.
---

# Event Finder: Facebook Events

![Event Finder: Facebook Events](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/event-finder.gif)

Find events from chat: search public Facebook events by topic, browse what is on in a city, and open any event for its date, venue and details.

No Facebook account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=event-finder).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/event-finder.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “Find upcoming tech events on Facebook”
- “What's on in Lisbon this weekend?”
- “Which events is this venue's page hosting?”
- “Give me the details of this event”

## When to Use This Skill

Use it when the user wants public Facebook events by topic, city or page.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Facebook Events  │
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

### Events

| Tool | What it returns | Price |
|------|-----------------|-------|
| `facebookdata_events_search` | Search public Facebook events by keyword | $0.00282 |
| `facebookdata_city_events` | Public Facebook events in one city | $0.00282 |
| `facebookdata_event_details` | One public Facebook event by id or URL: name, description, time, place, host, going and interested counts | $0.00282 |
| `facebookdata_page_events` | Upcoming public events of a Facebook page by URL | $0.00282 |

## Recipes

### Plan a weekend

1. `facebookdata_city_events` with the city's Facebook events page and `time` set to `this_week`.
2. Open the interesting ones with `facebookdata_event_details`.
3. List them by day with venue and time.

## Code Examples

### Search events

```bash
clawlink_call_tool --tool "facebookdata_events_search" \
  --params '{"query": "tech"}'
```

### A city's events

```bash
clawlink_call_tool --tool "facebookdata_city_events" \
  --params '{"url": "https://www.facebook.com/events/explore/saint-petersburg-florida/111326725552547"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `events`); public-data tools show as connected for every user.
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

- Search mixes past and upcoming events: keep the ones with `is_past: false`.
- Short queries (‘tech’, ‘yoga’) find more than long ones.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| No events | Try a shorter query or the city events page. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=event-finder; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=event-finder)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=event-finder)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Marketplace Finder](https://clawhub.ai/hith3sh/skills/marketplace-finder)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=event-finder)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
