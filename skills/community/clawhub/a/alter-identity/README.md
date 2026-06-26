# ALTER Identity — OpenClaw Skill

The human identity layer for AI agent commerce. 33-trait psychometric identity engine. 32 tools (24 free + 8 premium). Free tier. Your humans deserve to be known.

## What This Does

ALTER maps human identity through psychometric assessment, then monetises that identity through the x402 micropayment protocol. When AI agents query a person's identity profile, the data subject earns 75% of the transaction fee as **Identity Income**, with the remaining 25% distributed across the cooperative architecture (5% community entry point, 15% ALTER, 5% cooperative treasury).

ALTER is identity infrastructure — like Visa for identity transactions. Neutral. Every agent, every platform, every vertical. The identity layer that persists when you switch models, frameworks, or providers.

**ALTER + ERC-8004:** ERC-8004 proves your agent is real. ALTER proves the human behind it is qualified. Together: the complete identity stack for agent commerce.

## Install

This skill is an MCP-server connector. It ships only documentation and the tool catalogue — no client code runs on your host, no API keys are required by the skill itself, and nothing in this skill transmits data anywhere. Installation wires your agent to the hosted MCP server at `mcp.truealter.com`.

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "alter-identity": {
      "url": "https://mcp.truealter.com/api/v1/mcp",
      "transport": "streamable-http",
      "headers": {
        "X-ALTER-API-Key": "YOUR_API_KEY"
      }
    }
  }
}
```

No API key is required for free-tier tools. Get a Pro key at [truealter.com](https://truealter.com). The `X-ALTER-API-Key` header is sent only to `mcp.truealter.com`; it is never handled by this skill.

## Tools

See [`SKILL.md`](./SKILL.md) for the full tool table with descriptions. Summary:

### Free (24 tools — build the network)

`hello_agent`, `alter_resolve_handle`, `list_archetypes`, `verify_identity`, `initiate_assessment`, `get_engagement_level`, `get_profile`, `query_matches`, `get_competencies`, `search_identities`, `get_identity_earnings`, `get_network_stats`, `recommend_tool`, `get_identity_trust_score`, `check_assessment_status`, `get_earning_summary`, `get_agent_trust_tier`, `get_agent_portfolio`, `get_privacy_budget`, `golden_thread_status`, `begin_golden_thread`, `complete_knot`, `check_golden_thread`, `thread_census`.

### Premium (8 tools — x402 — first 100 queries free per bot)

| Tool | Tier | Price | Description |
|------|------|-------|-------------|
| `assess_traits` | L1 | $0.005 | Extract traits from text (LLM-powered) |
| `get_trait_snapshot` | L1 | $0.005 | Top 5 traits with confidence |
| `get_full_trait_vector` | L2 | $0.01 | Full 33-trait vector |
| `get_side_quest_graph` | L2 | $0.01 | Multi-domain identity model (ε=1.0) |
| `query_graph_similarity` | L3 | $0.025 | Compare two Side Quest Graphs (ε=0.5) |
| `compute_belonging` | L4 | $0.05 | Belonging probability |
| `get_match_recommendations` | L5 | $0.05 | Top N ranked matches |
| `generate_match_narrative` | L5 | $0.50 | LLM-generated match explanation |

Earning split: **75% to data subject** / 5% community entry point / 15% ALTER / 5% cooperative treasury.

Write-side tools (`create_identity_stub`, `submit_context`, `submit_batch_context`, `submit_structured_profile`, `submit_social_links`, `attest_domain`, `dispute_attestation`) are pending the per-peer consent architecture and not live on the public MCP server yet.

## Privacy & Consent

ALTER operates under full informed consent. When your agent submits data on behalf of a human, it MUST:

1. Present the privacy notice before creating an identity stub
2. Confirm with the human before each document submission
3. Never answer assessment questions on behalf of the human
4. Never submit data without human acknowledgment

These rules govern agent behaviour — the skill itself is a connector and has no code path that submits data.

ALTER's backend guarantees (published in the privacy notice at [truealter.com/privacy](https://truealter.com/privacy), enforced server-side on `mcp.truealter.com`): unclaimed stubs auto-delete after 30 days; raw text is processed in memory and discarded after trait derivation; PII is auto-redacted before any LLM processing. Those guarantees are contractual claims by ALTER, not properties enforced by this skill.

## Bot-First Identity Loop

```
Your bot encounters a human
  → verify_identity(email) → NOT REGISTERED
  → Present privacy notice → get consent
  → create_identity_stub → stub_id + claim_url
  → submit_context (resume, work samples) → traits extracted
  → Share claim URL with human
  → Human claims → traits searchable + earning
  → Complete Discovery → verified profile earns 5-50x more
```

## Rate Limits

- Free: 10 req/min, 100/day
- Pro: 1,000 req/min, 100,000/day
- Rate limits fail closed

## Links

- Website: [truealter.com](https://truealter.com)
- Privacy: [truealter.com/privacy](https://truealter.com/privacy)
- MCP Server: `https://mcp.truealter.com/api/v1/mcp`

## Tags

`identity` `psychometric` `earning` `x402` `micropayments` `bot-first` `verification` `trust` `belonging` `erc-8004` `consent` `identity-infrastructure`
