---
name: creator-skill
description: Creator SKILL — search TikTok, Instagram, and YouTube influencers via Deinai MCP (searchInfluencers, get_location_ids). Requires a Deinai account, MCP token, and team credits.
metadata:
  openclaw:
    requires:
      env: []
    primaryEnv: null
  displayName: Creator SKILL
---

# Creator SKILL

Use this skill when the user wants to **discover or search influencers** on **TikTok**, **Instagram**, or **YouTube** with natural-language criteria, filters (followers, region, language, email, etc.), or location-based targeting.

**Production API:** [https://deinai.ai](https://deinai.ai) · MCP: `https://deinai.ai/mcp`

## When to use

- User asks to find creators/KOLs/influencers on social platforms.
- User provides niche, audience, follower range, country/city, or brand-collab requirements.
- User needs location filters → call `get_location_ids` first, then `searchInfluencers` with `locations`.

## When NOT to use

- Negotiation, outreach email drafting, payments, or in-app campaign management (not exposed on this MCP).
- Platforms other than `tiktok`, `instagram`, `youtube`.

## Prerequisites

1. **Deinai account** ([deinai.ai](https://deinai.ai)) with a team that has search credits.
2. **MCP token** (JWT, `type: mcp`) — see [references/install.md](references/install.md).
3. **OpenClaw MCP server** pointing to `https://deinai.ai/mcp` with `Authorization: Bearer <MCP_TOKEN>`.

## Required workflow for agents

1. If **platform** is missing → ask user to pick: `tiktok` | `instagram` | `youtube`. **Do not guess.**
2. If **search topic / query** is missing → ask for niche, keywords, or creator handle.
3. If user gives **location names** (country, city) → call `get_location_ids` → pass returned IDs to `searchInfluencers.locations`.
4. Call `searchInfluencers` with only declared parameters; put extra requirements in `query` as natural language.
5. On `code: 402` or `errorCode: CREDITS_INSUFFICIENT` → tell user to top up credits at [deinai.ai](https://deinai.ai).

## Tools (summary)

| Tool | Purpose |
|------|---------|
| `ping` | Health check |
| `get_location_ids` | Resolve location names → numeric IDs |
| `searchInfluencers` | AI text search + filters; **credits = number of rows returned** |

Details: [references/tools.md](references/tools.md). Errors: [references/errors.md](references/errors.md).

## Billing

Credits are charged per **influencer record returned** (feature `search`), not per API call attempt. See tools reference for `page_size` (max 50).

## Install MCP connection (OpenClaw)

See [references/install.md](references/install.md) for `openclaw mcp set creator-skill` (replace `<MCP_JWT_TOKEN>` only).
