---
name: aeo-radar
description: Answer-engine optimisation (AEO) research with no API keys. See what ChatGPT, Perplexity, Google AI Overview and Google AI Mode answer for any prompt, which brands they name and which sources they cite, how often a brand is mentioned by LLMs, and AI search volume for keywords. Use this skill to track AI visibility, check if AI recommends your brand, or plan content for AI search.
---

# AEO Radar: AI Answer Visibility

![AEO Radar: AI Answer Visibility](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/aeo-radar.gif)

Find out whether AI recommends you: ask ChatGPT, Perplexity, Google AI Overview and AI Mode the questions your customers ask, and see which brands they name and which pages they cite.

No ChatGPT or Perplexity account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=aeo-radar).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/aeo-radar.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “Which CRMs does ChatGPT recommend to startups?”
- “Does Perplexity mention my brand for ‘best project management tool’?”
- “What sources does Google's AI Overview cite for ‘how to start a podcast’?”
- “How often do LLMs mention Notion?”

## When to Use This Skill

Use it when the user wants to know what AI assistants answer, who they mention, or which sources they cite.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ AI answer engines│
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

### AI Answers

| Tool | What it returns | Price |
|------|-----------------|-------|
| `aivisibilitydata_chatgpt_answer` | What ChatGPT (with web search) answers to a prompt, as a real user sees it, with the sources it cited and the… | $0.006 |
| `aivisibilitydata_perplexity_answer` | What Perplexity (sonar, with web search) answers to a prompt, with the URLs it cites and the searches it ran | $0.0105 |
| `aivisibilitydata_google_ai_overview` | Google's AI Overview for a keyword, with the pages it cites, next to the top 10 organic results | $0.006 |
| `aivisibilitydata_google_ai_mode` | Google AI Mode's answer to a query, with the pages it cites | $0.006 |

### AI Demand & Mentions

| Tool | What it returns | Price |
|------|-----------------|-------|
| `aivisibilitydata_ai_search_volume` | Estimated monthly volume of a keyword in AI assistants (ChatGPT, Gemini, AI Overviews), with the 12-month trend | $0.01515 |
| `aivisibilitydata_llm_mentions` | AI answers (Google AI Overviews or ChatGPT) that mention a domain or keyword, with the question, the answer and its… | $0.165 |

## Recipes

### Check if AI recommends a brand

1. Write 3-5 prompts your customers would ask.
2. Run each through `aivisibilitydata_chatgpt_answer` and `aivisibilitydata_perplexity_answer`.
3. Count which brands are named and which domains are cited; show where the brand is missing.

## Code Examples

### ChatGPT answer

```bash
clawlink_call_tool --tool "aivisibilitydata_chatgpt_answer" \
  --params '{"prompt": "What is the best CRM for a startup?"}'
```

### Perplexity answer

```bash
clawlink_call_tool --tool "aivisibilitydata_perplexity_answer" \
  --params '{"prompt": "best project management tool for agencies"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `chatgpt answer`); public-data tools show as connected for every user.
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

- Answers vary between runs; run a prompt 2-3 times before drawing conclusions.
- `aivisibilitydata_llm_mentions` costs more (about $0.17): confirm first.
- Cited means listed in the sources; quoted means used in the answer text. Report which.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Empty answer | Rephrase the prompt as a question a user would ask. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=aeo-radar; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=aeo-radar)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=aeo-radar)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [SERP Sniper](https://clawhub.ai/hith3sh/skills/serp-sniper)
- [Keyword Miner](https://clawhub.ai/hith3sh/skills/keyword-miner)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=aeo-radar)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
