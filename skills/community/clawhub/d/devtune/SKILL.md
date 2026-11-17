---
name: devtune
description: Track and improve what ChatGPT, Perplexity, Google AI Overviews, Google AI Mode, Copilot, Claude and Grok say about a brand. Use when the user asks how AI search answers mention or cite their product, their AI visibility or share of voice against competitors, which pages AI cites, AI crawler and referral traffic, what to fix to show up in AI answers, or whether a shipped fix moved the numbers.
version: 1.0.1
metadata:
  openclaw:
    emoji: "📡"
    homepage: https://devtune.ai
    requires:
      bins: [curl]
    primaryEnv: DEVTUNE_API_KEY
    envVars:
      - name: DEVTUNE_API_KEY
        required: false
        description: DevTune project API key (starts with dtk_live_). Not needed if you register through https://devtune.ai/auth.md instead.
---

# DevTune

DevTune measures what AI platforms tell buyers about a product, ranks the fixes most likely to change those answers, and shows before/after results for fixes that shipped. It covers four areas:

- **Visibility**: how often tracked prompts mention or cite the brand on each AI platform, and against which competitors.
- **AI Traffic**: what AI systems fetch from the site, and the visits they send.
- **Actions**: a ranked queue of fixes, each with its evidence.
- **Results**: before/after measurements for shipped fixes.

DevTune is a paid service with a 14-day free trial; no card is needed to start. Plans and API access: https://devtune.ai/pricing

## Get access

Pick one:

1. **The user already has DevTune.** Ask them to create a key under **API Keys** in the account sidebar at https://devtune.ai, choose the project, and set it as `DEVTUNE_API_KEY`. A key works on one project.
2. **The user has no account yet.** Ask for the domain to track and the email they sign in with, then follow https://devtune.ai/auth.md. You register, draft the project setup, and send the user a link and a 6-digit code. They sign up at https://devtune.ai/auth/sign-up (or sign in), review the setup and approve it. After that your token works like a project API key. No key is needed in advance.

## Call the API

Base URL: `https://devtune.ai/api/v2`. Send `Authorization: Bearer $DEVTUNE_API_KEY`.

Start by finding the project the key belongs to:

```bash
curl -s https://devtune.ai/api/v2/connection \
  -H "Authorization: Bearer $DEVTUNE_API_KEY"
```

`data.project.id` is the `projectId` for every other call. `data.scopes` lists what the key may do; a `403` means the key lacks the scope for that route, and the user can add it in the key's **Scopes** dialog.

Common reads. Windowed reads take a fixed window, but the parameter name and allowed values differ by endpoint; check the endpoint in the OpenAPI spec before you set one.

| Question | Endpoint |
| --- | --- |
| How visible are we in AI answers? | `GET /projects/{projectId}/visibility/summary?windowDays=30` |
| How do we compare with competitors? | `GET /projects/{projectId}/competitive/position` |
| What changed since the last period? | `GET /projects/{projectId}/visibility/diff` |
| What did the AI platforms actually say? | `GET /projects/{projectId}/visibility/responses` |
| Which domains and pages get cited? | `GET /projects/{projectId}/citations/top-domains`, `GET /projects/{projectId}/citations/top-pages` |
| Where are competitors cited and we aren't? | `GET /projects/{projectId}/content-gaps/list` |
| What does AI get wrong about us? | `GET /projects/{projectId}/accuracy/contradictions` |
| What should we fix first? | `GET /projects/{projectId}/actions/list` |
| Did shipped fixes work? | `GET /projects/{projectId}/outcomes/ledger` |
| What do AI systems fetch from our site? | `GET /projects/{projectId}/traffic/summary`, `GET /projects/{projectId}/traffic/recent-answer-fetches` |
| Which AI platforms send visitors? | `GET /projects/{projectId}/traffic/referrals` |

Full reference, including writes (prompts, actions, briefs, webhooks): https://docs.devtune.ai/api-reference. OpenAPI spec: https://devtune.ai/openapi.json

## Reading results

- A **citation** is an AI answer linking to a URL; a **mention** names the brand without a link. Report them separately.
- **Share of voice** is the brand's citations over the brand's plus its configured competitors' citations.
- When a value is missing or marked unmeasured, say it is not measured yet. Don't estimate it.

## Rules

- Ask before any write that spends credits or changes tracking: generating briefs, starting analyses or tests, adding prompts, or changing brands and domains.
- Don't publish or change the user's site content. Drafts from DevTune go to the user for approval.
- Never print the API key or put it in files you commit.

## MCP

DevTune also runs an MCP server at `https://devtune.ai/api/mcp` (Streamable HTTP, OAuth or the same API key). Setup: https://docs.devtune.ai/api-reference/mcp-server
