---
name: bavlio
description: Run lead discovery and outreach through Bavlio, the AI SDR that researches every lead before it writes. Plan and run lead searches, enrich datasets, write campaign copy, and manage LinkedIn plus email sequences via the Bavlio MCP server.
---

# Bavlio

Bavlio is an AI SDR platform: lead database with natural-language search, email
finding and verification, research-first personalization, and multichannel
campaigns (email + LinkedIn) with a unified inbox. This skill connects an agent
to a Bavlio workspace through the hosted MCP server.

## Setup

1. Create an account at https://bavlio.com and generate an API key in Settings.
2. Add the MCP server: `https://mcp.bavlio.com/mcp` with header
   `Authorization: Bearer <YOUR_API_KEY>`.

Claude Code:

```bash
claude mcp add bavlio --transport http https://mcp.bavlio.com/mcp \
  --header "Authorization: Bearer $BAVLIO_API_KEY"
```

## What you can do

19 tools, the important flows:

- **Find leads**: `bavlio_plan_lead_search` (always plan first; it returns the
  parsed plan and the maximum credit charge) then `bavlio_run_lead_search`
  with explicit confirmation. Natural-language queries like "owners of HVAC
  companies in Texas with 10-50 employees".
- **Enrich**: `bavlio_enrich_dataset` finds and verifies work emails for a
  dataset's rows.
- **Campaigns**: `bavlio_create_campaign`, `bavlio_set_campaign_sequence`,
  `bavlio_write_step_copy`, `bavlio_preview_message`, `bavlio_launch_campaign`.
  Multi-step LinkedIn + email sequences with per-step gates, variants, and AI
  personalization.
- **Inbox**: `bavlio_list_inbox` and `bavlio_get_thread` read replies across
  email and LinkedIn in one place.
- **Account**: `bavlio_get_balance` for credits, `bavlio_list_channels` for
  connected sending identities.

## Ground rules for agents

- Always show the user the plan and maximum credit charge from
  `bavlio_plan_lead_search` and get explicit confirmation before running a
  search. Plans expire after 15 minutes.
- Never call `bavlio_launch_campaign` without the user explicitly approving
  the final sequence and audience.
- Lead searches and enrichment spend credits; treat them as paid operations.

Docs: https://bavlio.com/docs · Support: support@bavlio.com
