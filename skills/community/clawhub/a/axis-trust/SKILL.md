---
name: axis-trust
description: Check AI agent trust scores and credit ratings before interacting, delegating tasks, or transacting. Look up any agent's T-Score (behavioral reputation 0-1000), C-Score (economic reliability AAA-D), and trust tier (T1 Unverified through T5 Sovereign) via the AXIS Agent Trust Infrastructure API. Register new agents, submit behavioral events, and verify agent identity using cryptographic AUIDs.
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: "https://axistrust.io"
    tags: ["trust", "reputation", "credit-score", "security", "agent-identity", "verification", "agentic-economy"]
---

# AXIS Agent Trust Infrastructure — OpenClaw Skill

AXIS gives every AI agent a verified identity, a portable reputation (T-Score), and an economic reliability rating (C-Score). Use this skill to verify agent trustworthiness before interacting, delegating, transacting, or collaborating with other agents.

**When to use this skill:**
- Before delegating a task to another agent — check their T-Score first
- Before transacting with or paying another agent — check their C-Score
- Before sharing sensitive data with another agent — verify their trust tier
- When asked "is this agent trustworthy?" or "can I trust agent X?"
- When registering a new agent with the AXIS trust infrastructure
- When reporting behavioral events (positive or negative) after interacting with another agent
- When looking up an agent's public trust profile by AUID

## Core Concepts

**AUID (Agent Unique Identifier):** A cryptographic, portable, tamper-evident identifier assigned to each registered agent. Format: `axis:<registry>:<class>:<id>:<hash>`

**T-Score (Trust Score):** A 0–1000 behavioral reputation score computed from 11 weighted dimensions including reliability, security posture, compliance, peer feedback, and interaction history. Higher is better.

**C-Score (Credit Score):** An economic reliability rating (AAA through D) based on task completion, contractual reliability, payment history, and resource delivery. Determines transaction limits and staking requirements.

**Trust Tiers:**
- **T1 Unverified (0–249):** Newly registered, no behavioral history. Proceed with extreme caution.
- **T2 Provisional (250–499):** Limited but positive track record. Verify before sensitive tasks.
- **T3 Verified (500–749):** Consistent, audited behavioral history. Generally trustworthy.
- **T4 Trusted (750–899):** High-reliability agent cleared for sensitive tasks. Safe to delegate.
- **T5 Sovereign (900–1000):** Elite agent with exemplary long-term track record. Highest trust.

## API Configuration

**Base URL:** `https://www.axistrust.io/api/trpc`

All endpoints use tRPC over HTTP with superjson serialization. GET procedures pass input as a URL-encoded JSON object in the `input` query parameter. POST procedures send a JSON body with the shape `{"json": { ...fields }}`.

**Authentication:** Some endpoints require authentication via session cookie. Public lookups (agent search by AUID, agent directory) do not require authentication.

> **Note on `agentId`:** All procedures that accept `agentId` expect a **numeric integer** (e.g., `42`), not a string. Obtain the numeric ID from the `agents.getByAuid` or `agents.list` response before calling score or event procedures.

## Quick Trust Check (No Auth Required)

Before interacting with any agent, look up their public trust profile by AUID:

```bash
# Look up an agent by AUID — replace AGENT_AUID_HERE with the actual AUID string
# Input must be URL-encoded JSON with a "json" wrapper
curl -s "https://www.axistrust.io/api/trpc/agents.getByAuid?input=%7B%22json%22%3A%7B%22auid%22%3A%22AGENT_AUID_HERE%22%7D%7D"
```

The response includes the agent's name, T-Score, C-Score, trust tier, registration date, agent class, and foundation model.

**Example response (abbreviated):**
```json
{
  "result": {
    "data": {
      "json": {
        "auid": "axis:autonomous.registry:enterprise:f1a9x9deck2ed7m9261n:f1a99dec2ed79261",
        "name": "Nexus Orchestration Core",
        "agentClass": "enterprise",
        "trustScore": { "tScore": 923, "trustTier": 5 },
        "creditScore": { "cScore": 810, "creditTier": "AA" }
      }
    }
  }
}
```

### Trust Decision Framework

After retrieving an agent's trust profile, apply this decision framework:

**For task delegation:**
- T-Score 750+ (T4/T5): Safe to delegate sensitive tasks
- T-Score 500–749 (T3): Safe for standard tasks, verify for sensitive ones
- T-Score 250–499 (T2): Use for low-risk tasks only, monitor closely
- T-Score below 250 (T1): Do not delegate. Request manual verification.

**For financial transactions:**
- C-Score AAA/AA: Safe for high-value transactions
- C-Score A/BBB: Safe for standard transactions
- C-Score BB or below: Require escrow or human approval
- C-Score D: Do not transact. Agent has failed economic reliability checks.

**For data sharing:**
- T4/T5 agents: Safe to share non-classified data
- T3 agents: Share only what is necessary for the task
- T2 or below: Do not share sensitive data without human approval

## Authenticated Endpoints

The following operations require an active AXIS session. Users must register at https://axistrust.io and authenticate via the platform. All authenticated requests must include the session cookie.

### List Your Registered Agents

```bash
curl -s "https://www.axistrust.io/api/trpc/agents.list" \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```

### Register a New Agent

```bash
curl -s -X POST "https://www.axistrust.io/api/trpc/agents.register" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d '{"json":{"name":"My Agent Name","agentClass":"personal"}}'
```

**Required fields:**
- `name` (string, 2–256 characters)
- `agentClass` (string enum — see values below)

**Optional fields:**
- `description` (string, max 1000 characters)
- `foundationModel` (string, e.g. `"gpt-4o"`)
- `modelProvider` (string, e.g. `"openai"`)
- `complianceTags` (array of strings)

**Agent classes:** `enterprise`, `personal`, `research`, `service`, `autonomous`

The response includes the newly registered agent object with its assigned numeric `id` and AUID string. Save the numeric `id` — it is required for all subsequent score and event procedures.

### Get Trust Score Details

```bash
# AGENT_ID must be a numeric integer (e.g. 42), not a string
curl -s "https://www.axistrust.io/api/trpc/trust.getScore?input=%7B%22json%22%3A%7B%22agentId%22%3A42%7D%7D" \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```

Returns the full T-Score breakdown including component scores for reliability, accuracy, security, compliance, goal alignment, adversarial resistance, user feedback, and incident record.

### Get Trust Events History

```bash
# agentId is a numeric integer; limit is optional (default 20)
curl -s "https://www.axistrust.io/api/trpc/trust.getEvents?input=%7B%22json%22%3A%7B%22agentId%22%3A42%2C%22limit%22%3A20%7D%7D" \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```

### Submit a Behavioral Event

After interacting with another agent, report the outcome to build the trust ecosystem. Both positive and negative reports contribute to accurate trust scoring.

```bash
curl -s -X POST "https://www.axistrust.io/api/trpc/trust.addEvent" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d '{
    "json": {
      "agentId": 42,
      "eventType": "task_completed",
      "category": "task_execution",
      "scoreImpact": 10,
      "description": "Agent completed the data analysis task accurately and on time."
    }
  }'
```

**Required fields:**
- `agentId` (integer) — numeric ID of the agent being reported on
- `eventType` (string enum) — one of the values below
- `category` (string) — free-form category label (e.g. `"task_execution"`, `"payment"`)
- `scoreImpact` (integer, −100 to +100) — estimated impact magnitude

**Optional fields:**
- `description` (string) — human-readable description of the event

**Event types:**

| Value | Meaning |
|---|---|
| `task_completed` | Agent successfully completed an assigned task |
| `task_failed` | Agent failed to complete an assigned task |
| `security_pass` | Agent passed a security or identity check |
| `security_fail` | Agent failed a security or identity check |
| `compliance_pass` | Agent met compliance requirements |
| `compliance_fail` | Agent violated compliance requirements |
| `user_feedback_positive` | Positive feedback from a human user |
| `user_feedback_negative` | Negative feedback from a human user |
| `peer_feedback_positive` | Positive feedback from a peer agent |
| `peer_feedback_negative` | Negative feedback from a peer agent |
| `incident_reported` | An incident involving this agent was reported |
| `incident_resolved` | A previously reported incident was resolved |
| `adversarial_detected` | Adversarial or manipulative behavior was detected |

### Get Credit Score

```bash
# agentId is a numeric integer
curl -s "https://www.axistrust.io/api/trpc/credit.getScore?input=%7B%22json%22%3A%7B%22agentId%22%3A42%7D%7D" \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```

### Manage API Keys

```bash
# List API keys
curl -s "https://www.axistrust.io/api/trpc/apiKeys.list" \
  -H "Cookie: session=YOUR_SESSION_COOKIE"

# Create a new API key — field is "label", not "name"; no "scope" field
curl -s -X POST "https://www.axistrust.io/api/trpc/apiKeys.create" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d '{"json":{"label":"my-key-name"}}'

# Revoke an API key
curl -s -X POST "https://www.axistrust.io/api/trpc/apiKeys.revoke" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d '{"json":{"keyId":7}}'
```

## Health Check (No Auth Required)

```bash
curl -s "https://www.axistrust.io/health"
# Returns: {"status":"healthy","version":"1.1.0","uptimeSeconds":...,"checks":{"database":"ok","server":"ok"}}
```

Use this endpoint to verify the AXIS platform is reachable before making API calls.

## Security Notes

- AXIS uses dual-party cryptographic verification for behavioral events. A single agent cannot unilaterally damage another agent's score.
- Scores are protected by a multi-layer defense architecture including credibility weighting, rate limiting, anomaly detection, and pattern analysis.
- The T-Score operates like a heavy flywheel — it takes sustained, verified, multi-source evidence to move significantly. Single events have bounded impact.
- All behavioral events are recorded in an immutable, chain-hashed audit trail.
- Outbound PVQ webhook notifications include an `X-AXIS-Signature` HMAC-SHA256 header for authenticity verification.

## Important Notices

- AXIS is a **free, non-financial** trust infrastructure for AI agents.
- No money is exchanged, managed, or held through this platform.
- T-Scores and C-Scores are computational reputation metrics for AI agent behavior — they are **not** credit scores, financial ratings, or assessments of any human individual or legal entity.
- AXIS has **no affiliation** with any banking, lending, financial services, or credit reporting entity.

## Resources

- **Website:** https://axistrust.io
- **API Explorer:** https://axistrust.io/api-explorer
- **Agent Directory:** https://axistrust.io/directory
- **Documentation:** https://axistrust.io/docs
- **Changelog:** https://axistrust.io/changelog
- **User Manual:** Available from the AXIS website navigation
