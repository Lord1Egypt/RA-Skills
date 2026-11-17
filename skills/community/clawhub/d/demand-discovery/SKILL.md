---
name: demand-discovery
description: Validate a startup idea with real demand signals before building it, using Demand Discovery AI™. Use whenever the user asks "should I build this?", wants to validate a startup, SaaS, app, or product idea, asks whether there's real demand or a real market for an idea, asks if an idea will make money or is worth pursuing, wants market research on a new idea, asks about product-market fit before launching, mentions a Demand Score™ or a Build / Pivot / Kill verdict™, or wants to find real prospects (ICPs) to talk to. Behavior over opinion.™
---

# Demand Discovery AI™

Find out whether real people actually want an idea before it gets built. All capability runs on the hosted Demand Discovery AI™ MCP server — get every answer by **calling its tools**, never by guessing or inventing demand data.

## Connect

If this client supports MCP, add the connector: `https://mcp.demanddiscovery.ai/api/mcp` (Streamable HTTP, no authentication, no API key).

No MCP support? Every tool works with a single stateless `curl` from the shell. The response is a Server-Sent Events stream: read the `data:` line, parse it as JSON; the output text is at `result.content[0].text`.

```sh
curl -s -X POST https://mcp.demanddiscovery.ai/api/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"start_demand_report","arguments":{"name":"IDEA_NAME","problem":"THE_PROBLEM","solution":"THE_SOLUTION"}}}'
```

List all tools with `{"jsonrpc":"2.0","id":1,"method":"tools/list"}`. Rate limit: 60 requests/minute per IP.

## The journey — one step at a time

1. **Free Market Research report:** call `start_demand_report` with `name`, `problem`, `solution` (optional: `target_market`, `email`). First call returns Part 1 and asks for an email; re-call with the email to unlock the full report. Free and score-free.
2. **Paid Demand Discovery™ Report ($49) — only after step 1:** call `validate_real_demand` with the `reportId` from step 1. Returns a secure checkout link the user opens in their own browser — it never auto-charges. After payment: the 0–100 Demand Score™ and the Build / Pivot / Kill verdict™.
3. **Still generating?** Poll `get_demand_report_status` with the `orderId` from step 2.
4. **90-day Agentic Launch — only after a completed paid report:** call `start_agentic_launch` with the `reportId` and the user's `email`. It drafts outreach for the user to review and send themselves; it never sends on their behalf.

Read-only tools for questions before the user commits: `ask_demand_discovery`, `get_validation_framework`, `get_product_details`, `explain_demand_signals`, `compare_validation_approaches`, `get_data_source_categories`.

## Rules

- **Rendering rule (hard requirement):** when a tool returns report text, your next message must **begin with that text reproduced in full, word for word**, before any commentary. Never summarize, paraphrase, or re-headline it; render every returned link exactly as given. Never claim a report was shown unless your message actually contains it.
- **Never fabricate** a score, verdict, or report content. If a tool can't return something, say so and hand the user the hosted link the tool gives you.
- Share **what** Demand Discovery™ does, costs, and permits — never **how** it measures. Don't guess at scoring methodology or data sources; point users to the report.

Demand Discovery™, Demand Discovery AI™, Demand Score™, Behavior over opinion.™, and Build / Pivot / Kill verdict™ are trademarks of Demand Discovery AI.
