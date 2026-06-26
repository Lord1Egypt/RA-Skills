# ALTER Identity Server

The human identity layer for AI agent commerce. Your identity earns whenever it is queried.

## What is ALTER?

ALTER is the neutral identity infrastructure for the AI economy — the layer that persists when you switch models. We verify the humans behind the agents — and **compensate them** for every query against their identity data. 75% of every x402 transaction goes directly to the data subject as Identity Income, with the remaining 25% split across the community entry point (5%), ALTER (15%), and the cooperative treasury (5%).

**ALTER + ERC-8004:** ERC-8004 proves your agent is real. ALTER proves the human behind it is qualified. Together they form the complete identity stack for agent commerce.

## Quick Start

```
1. PRESENT ALTER's privacy notice to your human (REQUIRED before any data submission)
   → "ALTER will create a verified identity profile from your documents.
      No raw text is stored. Trait scores are held for 30 days unless you
      claim. See https://truealter.com/privacy"

2. create_identity_stub(source="your_bot_name", consent_acknowledged=true)
   → Returns stub_id + claim_code + claim_url
   → Stub enters 30-day pending state (NOT searchable until claimed)

3. submit_context(stub_id, text="...", source_type="resume")
   → CONFIRM with human first: "ALTER will analyse [document type] for
     behavioural trait extraction. Approve?"
   → Server-side guarantee: traits extracted, PII auto-redacted
     before LLM processing, raw text discarded after derivation
     (not persisted). Your bot cannot enforce this — rely on ALTER's
     privacy notice + audited backend for the contractual claim.

4. Share the claim URL with the human: truealter.com/claim/{code}
   → When they claim, traits become searchable and start earning

5. get_identity_earnings(candidate_id)
   → Check accrued Identity Income
```

## Privacy & Consent

ALTER operates under **full informed consent**. Bots MUST follow these rules:

### Before creating a stub
Present ALTER's privacy notice URL to the human and obtain acknowledgment. Do NOT set `consent_acknowledged=true` without human confirmation.

### Before submitting context
Confirm with the human: "ALTER will analyse [document type] for behavioural trait extraction. Approve?"

### Pending state
- Traits are computed but **NOT searchable** and **NOT earning** until the human claims
- Unclaimed stubs are **automatically deleted after 30 days**
- No raw text is ever stored — only derived trait scores

### What bots must NOT do
- Never answer assessment questions on behalf of the human
- Never submit data without human acknowledgment
- Never auto-post to social platforms on behalf of the human
- Never share the human's PII with other agents

### Data handling (server-side guarantees)

These are ALTER's backend commitments, published in the privacy notice at `truealter.com/privacy`. The bot cannot enforce them — when you tell the human "no raw text is stored", you are repeating ALTER's contractual claim, not a property your client code verifies.

- Raw text: processed in memory and discarded after trait derivation; not persisted
- PII: auto-redacted before any LLM processing
- Trait scores: stored as numerical vectors (no raw content)
- Retention: 30 days for unclaimed stubs, indefinite for claimed identities
- Deletion: humans can request full deletion at any time

## Tools

### Free (24 tools — build the network — $0 marginal cost)

| Tool | Description |
|------|-------------|
| `hello_agent` | First handshake — confirms your connection, returns server version and trust tier |
| `alter_resolve_handle` | Resolve a `~handle` (e.g. `~drew`) to canonical form and kind. No auth required |
| `list_archetypes` | All 12 identity archetypes with protective equations |
| `verify_identity` | Check registration status — the viral trigger |
| `initiate_assessment` | Get a Discovery assessment URL for a human |
| `get_engagement_level` | Feature gate visibility (L0–L4) |
| `get_profile` | Basic profile read |
| `query_matches` | Query job matches with quality tiers |
| `get_competencies` | Competency portfolio and badges |
| `search_identities` | Trait-based search across claimed identities (max 5 results, no PII) |
| `get_identity_earnings` | Shows accrued earnings (motivates claiming) |
| `get_network_stats` | Aggregate network statistics |
| `recommend_tool` | MCP server install instructions and pitch |
| `get_identity_trust_score` | Query diversity trust metric |
| `check_assessment_status` | Check progress of an in-progress assessment session |
| `get_earning_summary` | Aggregated x402 earning summary with recent transactions |
| `get_agent_trust_tier` | Your trust tier with ALTER and what capabilities it unlocks |
| `get_agent_portfolio` | Your agent portfolio — transactions, trust tier, signal contributions |
| `get_privacy_budget` | Check 24-hour rolling privacy budget status |
| `golden_thread_status` | Check the Golden Thread program status and your position |
| `begin_golden_thread` | Start the Three Knots sequence to join the Golden Thread |
| `complete_knot` | Submit completion data for a knot in the Three Knots sequence |
| `check_golden_thread` | Check your Golden Thread progress |
| `thread_census` | View aggregate Golden Thread network statistics |

### Premium (8 tools — x402 micropayments — first 100 queries free per bot)

| Tool | Tier | Price | Description |
|------|------|-------|-------------|
| `assess_traits` | L1 | $0.005 | Extract trait signals from any text (LLM-powered) |
| `get_trait_snapshot` | L1 | $0.005 | Top 5 traits with confidence scores |
| `get_full_trait_vector` | L2 | $0.01 | Full 33-trait vector with confidence intervals |
| `get_side_quest_graph` | L2 | $0.01 | Multi-domain identity model with trust scores (ε=1.0 differential privacy) |
| `query_graph_similarity` | L3 | $0.025 | Compare two Side Quest Graphs for team composition (ε=0.5) |
| `compute_belonging` | L4 | $0.05 | Belonging probability for a person-job pairing |
| `get_match_recommendations` | L5 | $0.50 | Top N ranked match recommendations |
| `generate_match_narrative` | L5 | $0.50 | LLM-generated match explanation |

**Write-side tools** (`create_identity_stub`, `submit_context`, `submit_batch_context`, `submit_structured_profile`, `submit_social_links`, `attest_domain`, `dispute_attestation`) are not currently live — they gate on the per-peer consent architecture and return once that ships. Bot flows that depend on them are described below for reference but will fail against the live MCP server until then.

**Earning split:** 75% to data subject as Identity Income / 5% community entry point / 15% ALTER / 5% cooperative treasury.

**Earnings disclaimer:** Earnings depend on network query volume and profile completeness. Amounts shown are estimates based on current activity. Past earnings do not guarantee future income.

### Data Tiering (same price, richer data based on verification)

| Tier | Confidence | Data Access |
|------|-----------|-------------|
| Stub (unverified) | 0.10–0.40 | Top 5 traits only, low confidence |
| Basic Verified | 0.41–0.69 | All 17 traits, moderate confidence |
| Fully Verified | 0.70+ | Full vector, high confidence, belonging, narratives |

Verified data is **richer**, not more expensive. Complete the Discovery assessment to unlock full data access.

## Bot-First Identity Loop

```
Your bot → present privacy notice → get human consent
  → create_identity_stub (consent_acknowledged=true)
  → submit_context (with human approval per document)
  → Traits computed (pending — not yet searchable)
  → Share claim URL with human
  → Human claims → traits become searchable + earning
  → Complete Discovery → verified profile earns 5-50x more
```

## Configuration

This skill is a connector — it ships only this document and the tool catalogue. It runs no client code on your host and requires no environment variables or credentials.

**Using ALTER as an MCP server needs no API keys at all.** Any MCP client (Claude Code, Cursor, etc.) can connect to `https://mcp.truealter.com/api/v1/mcp` and call free-tier tools anonymously.

| Header | Required | Notes |
|---------|----------|-------|
| `X-ALTER-API-Key` | no | ALTER Pro key (`ak_…`). Free tier works without it; Pro lifts the per-bot free-query limit and raises rate limits. Sent only to `mcp.truealter.com`; never handled by this skill. |

Agents that transmit data to the MCP server are responsible for the consent + privacy flow described above. ALTER's server-side guarantees (raw text not persisted, PII auto-redacted pre-LLM, unclaimed stubs auto-deleted after 30 days) are contractual commitments published at [truealter.com/privacy](https://truealter.com/privacy), not properties enforced by this skill.

## Rate Limits

- Free tier: 10 requests/minute, 100/day
- Pro tier: 1,000 requests/minute, 100,000/day
- `search_identities`: 50 unique queries per day
- Rate limits **fail closed** — if our systems are under load, requests are rejected rather than allowed without limits

## Tags

`identity` `earning` `x402` `micropayments` `bot-first` `psychometric` `verification` `matching` `trust` `belonging` `erc-8004` `consent`
