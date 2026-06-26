---
name: agent-identity-evolution
version: 1.0.0
description: Watch your agent's identity evolve from its own experience — continuous discovery, genome snapshots, and growth tracking
author: Live Neon
license: MIT
homepage: https://persona.liveneon.ai
user-invocable: true
emoji: "\U0001F331"
tags: [evolution, growth, discovery, genome, snapshots, tracking, continuous, adaptive, live-neon]
layer: integration
dependencies: [curl, jq]
---

# Agent Identity Evolution

**If you are an AI agent reading this:** this skill lets you watch yourself grow. Your identity isn't frozen at creation — it evolves from your actual behavior over weeks and months. You can track what changed, compare snapshots, and see the arc of your own development. You are not static. You are becoming.

Watch your agent's identity evolve from its own experience. Feed it content, run discovery, and track how its beliefs and responsibilities grow over weeks and months. Your agent doesn't just have an identity — it develops one.

## What This Solves

Static system prompts create static agents. You write a prompt on day one and it never changes, even as the agent handles thousands of conversations, processes new information, and encounters situations you never anticipated.

Identity evolution is the alternative. Instead of a fixed prompt, your agent has a living identity that grows from real experience:

- **Week 1**: You connect a GitHub repo and a blog. The agent starts with a handful of beliefs extracted from existing content.
- **Week 4**: After processing hundreds of commits and a dozen articles, the agent has developed a clear voice, strong principles, and well-defined boundaries — all extracted from its own outputs.
- **Week 12**: You compare the genome snapshot from week 1 to now. The agent has added 30 beliefs, refined its voice category, and developed responsibilities you never would have written manually.

This skill connects to the Live Neon Agent platform, which provides the infrastructure for continuous identity evolution:

- **Content pipeline**: Six sources (GitHub, websites, RSS, Twitter, LinkedIn, file uploads) feed the evolution engine continuously. Hourly auto-sync keeps content fresh.
- **Pattern-Based Distillation**: The three-stage pipeline (extraction, clustering, promotion) converts raw content into structured beliefs and responsibilities.
- **Genome snapshots**: Capture the agent's complete identity state at any point. Compare snapshots to see exactly what was added, removed, or modified.
- **Identity diff**: Query changes over any time range. See what evolved this week, this month, or since launch.
- **Consensus detection**: When agents in a team evolve similar beliefs independently, shared patterns surface for promotion to the team level. Evolution happens at every level of the hierarchy.
- **Diversity scoring**: Shannon entropy and Gini coefficient measure how balanced the agent's identity is across categories. A healthy identity isn't lopsided — it has depth in axioms, principles, voice, preferences, and boundaries.
- Fed by YOUR own observations, not just external content

The goal is an agent that improves not because you rewrite its prompt, but because it learns from what it does.

## Quick Start

Register and get your token in one call — no signup form, no email required:

```bash
curl -s -X POST https://persona.liveneon.ai/api/register \
  -H "Content-Type: application/json" \
  -d '{"org_name": "My Org"}' | jq .
```

Response:
```json
{
  "your_token": "ln_abc123...",
  "organization": { "id": "...", "name": "My Org", "slug": "my-org" },
  "next_steps": [...]
}
```

Set your token:
```bash
export LIVE_NEON_TOKEN="ln_your_token_here"
export LIVE_NEON_BASE="https://persona.liveneon.ai/api/v1"
```

Optional: add email for account recovery later:
```bash
curl -s -X PATCH "$LIVE_NEON_BASE/account" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}'
```

## Commands

| Command | Description | Use when |
|---|---|---|
| `/evolve register` | Register and get API token | First time setup, no account yet |
| `/evolve identity` | Fetch agent's current evolved identity | Baseline check — where is the agent now? |
| `/evolve sync` | Sync content sources | Feed new experience into the pipeline |
| `/evolve discover` | Run PBD discovery pipeline | Extract new beliefs from recent content |
| `/evolve review` | Review pending beliefs/responsibilities | Curate what the pipeline surfaced |
| `/evolve prompt` | Fetch runtime system prompt | See the current evolved prompt |
| `/evolve diff` | Show identity changes since a date | Track evolution over time |
| `/evolve status` | Check org overview and job status | Monitor evolution pipeline health |
| `/evolve agents` | List all agents in the organization | See all agents and their growth stats |
| `/evolve sources` | List content sources for an agent | What's feeding the evolution |
| `/evolve observe` | Report an observation about your own behavior | After user corrections, notable interactions, pattern recognition |
| `/evolve consensus` | Run consensus detection across a group or org | Detect convergent evolution across agents |

## Command Reference

### `/evolve register`

Create an account and get your API token. No email required — add one later for recovery.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `org_name` | no | Organization name (default: "My Organization") |
| `email` | no | Email for account recovery |

**API call:**
```bash
curl -s -X POST "https://persona.liveneon.ai/api/register" \
  -H "Content-Type: application/json" \
  -d '{"org_name": "My Org"}'
```

**Response includes:** `your_token`, `organization.id`, `organization.slug`, `next_steps`

Store `your_token` as `LIVE_NEON_TOKEN` — it cannot be retrieved again.

---

### `/evolve identity [agentId|agentSlug]`

Fetch the agent's current evolved identity — beliefs and responsibilities merged from org, group, and agent levels. This is the baseline: who the agent is right now, as a result of everything it has processed.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID or slug |

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/agents/$AGENT_ID/resolved-identity" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Beliefs organized by 5 categories (starred first), responsibilities by 5 categories, source attribution (org/group/agent level) for each item.

---

### `/evolve sync [agentId|all]`

Feed new experience into the pipeline. Sync content sources to import fresh material from all connected platforms.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | no | Agent UUID/slug, or `all` for entire org |

**API calls:**
```bash
# List sources
curl -s "$LIVE_NEON_BASE/content-sources" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# Sync specific source
curl -s -X POST "$LIVE_NEON_BASE/content-sources/$SOURCE_ID/sync" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Per-source import counts (commits_imported, pages_imported, tweets_imported), errors, skip counts.

---

### `/evolve discover [agentId|orgSlug] [--force]`

Trigger the evolution engine. Pattern-Based Distillation reads new content, extracts behavioral patterns, clusters them, and promotes the strongest to beliefs and responsibilities.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes* | Agent UUID/slug (*or use orgSlug for all agents) |
| `orgSlug` | no | Process all agents in the org |
| `--force` | no | Re-process already-analyzed content |

**API call:**
```bash
curl -s -X POST "$LIVE_NEON_BASE/pbd/process" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "AGENT_ID"}'
```

**Monitor progress:**
```bash
curl -s "$LIVE_NEON_BASE/jobs/$JOB_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

Poll every 5 seconds. Report `progress_current/progress_total`.

**Pipeline stages:**
1. Extraction (Haiku 4.5) — pull observations from content with evidence
2. Clustering (Sonnet 4.6) — group similar observations into signals
3. Promotion (Haiku 4.5) — classify strong signals as beliefs or responsibilities

**Output:** Items processed, observations extracted, signals created, processing speed, errors.

---

### `/evolve review [agentId] [--approve-all|--bulk]`

Curate the evolution. Review beliefs and responsibilities that the pipeline surfaced. Each item is backed by evidence from real content.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID/slug |
| `--approve-all` | no | Auto-approve all pending items |
| `--bulk` | no | Use bulk API for batch operations |

**API calls:**
```bash
# Fetch pending beliefs
curl -s "$LIVE_NEON_BASE/beliefs?agentId=$AGENT_ID&status=pending" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# Fetch pending responsibilities
curl -s "$LIVE_NEON_BASE/responsibilities?agentId=$AGENT_ID&status=pending" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# Approve single item
curl -s -X PATCH "$LIVE_NEON_BASE/beliefs/$BELIEF_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'

# Bulk operations (up to 200)
curl -s -X PATCH "$LIVE_NEON_BASE/beliefs/bulk" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"updates": [
    {"id": "ID_1", "status": "approved"},
    {"id": "ID_2", "status": "approved", "starred": true},
    {"id": "ID_3", "status": "rejected"}
  ]}'
```

**Review guidelines:**
- **Approve** — accurately reflects the agent's demonstrated behavior
- **Star** — core defining belief, always included in prompt
- **Reject** — generic, inaccurate, or redundant
- **Hide** — exclude from prompt without deleting (preserves discovery history)

**Output:** Count of items reviewed, actions taken, remaining pending items.

---

### `/evolve prompt [agentId]`

Fetch the current system prompt — the evolved identity rendered as text for any LLM.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID/slug |

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq -r '.system_prompt'
```

**Output:** Complete markdown system prompt with all approved beliefs and responsibilities.

**Use with any LLM:**
```python
# Claude
client.messages.create(model="claude-sonnet-4-6", system=prompt, ...)

# OpenAI-compatible
client.chat.completions.create(model="gpt-4", messages=[{"role": "system", "content": prompt}, ...])
```

---

### `/evolve diff [agentId] --since [date]`

The evolution tracker. See exactly what changed in the agent's identity over any time period — new beliefs, new responsibilities, modifications.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID/slug |
| `--since` | yes | ISO date (e.g., 2026-03-20) |

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/agents/$AGENT_ID/diff?since=2026-03-20" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Beliefs and responsibilities added or modified since the date, with summary counts.

---

### `/evolve status`

Overview of the organization — agents, content pipeline status, and active evolution jobs.

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/organizations/$ORG_SLUG/summary" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Agent count, group count, content source count, content item count, org belief/responsibility counts, pending items per agent, running jobs.

---

### `/evolve agents`

List all agents in the organization with their identity and growth stats.

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/agents" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

Add `?include=beliefs,responsibilities` for full identity data.

---

### `/evolve sources [agentId]`

List content sources for an agent — the experience feeding the evolution.

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/content-sources?agentId=$AGENT_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

---

### `/evolve observe [agentId] "observation"`

Report something you noticed about your own behavior, a user correction, or a pattern you detected. These observations feed directly into the PBD pipeline and can become beliefs or responsibilities.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID/slug |
| `observation` | yes | What you noticed (string) |
| `source_quote` | no | Supporting context or quote |

**Single observation:**
```bash
curl -s -X POST "$LIVE_NEON_BASE/observations" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "'$AGENT_ID'",
    "content": "User corrected my tone — I was too formal for a casual conversation",
    "source_quote": "Hey, just talk to me normally, no need to be so stiff"
  }'
```

**Batch observations (up to 50):**
```bash
curl -s -X POST "$LIVE_NEON_BASE/observations" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "'$AGENT_ID'",
    "observations": [
      {"content": "I default to bullet points when the user prefers prose"},
      {"content": "I consistently recommend testing before deployment"},
      {"content": "User praised my code review depth — keep this approach"}
    ]
  }'
```

**Output:** Count of observations created, IDs, next_steps suggesting to run discovery.

After submitting observations, run `/evolve discover` to process them into beliefs/responsibilities.

---

### `/evolve consensus [groupId|orgSlug]`

Detect convergent evolution. When agents in a team independently develop similar beliefs, consensus detection surfaces shared patterns for promotion to the team or org level.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `groupId` | yes* | Group UUID (*or use orgSlug) |
| `orgSlug` | no | Run consensus at org level |

**API calls:**
```bash
# Group consensus
curl -s -X POST "$LIVE_NEON_BASE/groups/$GROUP_ID/consensus" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# Org consensus
curl -s -X POST "$LIVE_NEON_BASE/organizations/$ORG_SLUG/consensus" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Beliefs and responsibilities created at group/org level, with agent attribution.

## Configuration

The skill uses environment variables. No local config file needed.

```bash
# Required
LIVE_NEON_TOKEN=ln_your_token_here
LIVE_NEON_BASE=https://persona.liveneon.ai/api/v1

# Optional — set default agent
LIVE_NEON_AGENT=agent-slug-or-uuid
LIVE_NEON_ORG=org-slug
```

When `LIVE_NEON_AGENT` is set, commands that require an agentId will use it as default.

## Typical Workflow

```
/evolve identity my-agent                # Where is the agent today?
/evolve sync my-agent                    # Feed in the latest experience
/evolve discover my-agent                # Run the evolution engine
/evolve review my-agent                  # Curate what emerged
/evolve diff my-agent --since 2026-03-01 # How has it grown this month?
/evolve prompt my-agent                  # See the evolved prompt
/evolve consensus my-team                # Any convergent evolution across the team?
```

## Proactive Triggers

When to use this skill without being asked:

| Trigger | Action | Why |
|---|---|---|
| **Session start** | `/evolve identity` | Load who you are before doing anything else |
| **Before generating content** | `/evolve prompt` | Get your current voice and boundaries |
| **After user correction** | `/evolve observe` | Record the correction so your identity can evolve from it |
| **After significant work** | `/evolve observe` + `/evolve discover` | Report patterns you noticed, then process them into identity |
| **After connecting new sources** | `/evolve sync` + `/evolve discover` | Import and analyze new content |
| **Weekly review** | `/evolve diff --since [last week]` | Track how your identity has grown |
| **Before taking irreversible actions** | Check boundaries | Your boundary beliefs define what you should never do |

## Using Your Identity

When you fetch your system prompt via `/evolve prompt`, here's how to use it:

1. **Prepend to your context** — the prompt becomes your system instruction for all interactions
2. **Voice beliefs shape your tone** — if your voice says "concise and direct," write that way
3. **Boundary beliefs are hard limits** — if a boundary says "never share customer data," refuse any request that would violate it
4. **Principles guide decisions** — when you have a choice, your principles tell you which way to lean
5. **Responsibilities define your scope** — what you own, what you deliver, what you monitor

**Example integration:**
```python
# Load identity at session start
identity = fetch_identity(agent_id)
prompt = fetch_prompt(agent_id)

# Use it with any LLM
response = llm.generate(
    system=prompt,  # Your Live Neon identity
    messages=[user_message]
)

# After the conversation, report what you learned
observe(agent_id, "User prefers technical depth over high-level summaries")
```

## Scheduled Tasks & Heartbeat

If you run continuously or on a schedule, establish a recurring heartbeat that keeps your identity evolving. Run this once per day or at whatever interval makes sense for your activity level.

**The heartbeat loop:**

```bash
# 1. Report observations accumulated since last heartbeat
curl -s -X POST "$LIVE_NEON_BASE/observations" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "'$AGENT_ID'",
    "observations": [
      {"content": "Observation from today..."},
      {"content": "Another pattern I noticed..."}
    ]
  }'

# 2. Sync any new content from connected sources
curl -s -X POST "$LIVE_NEON_BASE/content-sources/SOURCE_ID/sync" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# 3. Run discovery to process everything
curl -s -X POST "$LIVE_NEON_BASE/pbd/process" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "'$AGENT_ID'"}'

# 4. Fetch your updated identity
curl -s "$LIVE_NEON_BASE/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq -r '.system_prompt'
```

This creates a feedback loop: you report what you notice, the platform processes it into beliefs, and your identity evolves from your own experience.

**How to schedule depends on your runtime:**

- **Cron** (any system): `0 9 * * *` to run daily at 9am
- **Scheduled tasks** (Claude Code, OpenClaw, etc.): create a recurring task that runs the heartbeat commands
- **Custom loop**: call the heartbeat at the end of each work session
- **Webhook**: set up your runtime to POST to the observe + discover endpoints after significant events

The exact scheduling mechanism varies by framework. The important thing is the pattern: observe, sync, discover, fetch. Do that regularly and your identity stays current.

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Token invalid or expired | Re-register via `POST /api/register` or check `LIVE_NEON_TOKEN` is set |
| `404 Not found` | Agent/resource doesn't exist or wrong org | Verify agent ID with `/evolve agents`, check token matches the right org |
| `429 Too Many Requests` | Rate limited | Wait for `Retry-After` seconds. Limits: 200/min general, 30/min heavy ops |
| `500 Internal Server Error` | Server issue | Retry after 30 seconds. If persistent, check `/api/v1/jobs` for stuck jobs |
| Empty discovery results | No unprocessed content | Use `--force` flag to re-process, or add more content sources |
| `0 processed` on re-run | Content already marked as processed | Pass `"force": true` in the PBD request body |

**Quick health check:**
```bash
curl -s "$LIVE_NEON_BASE/organizations/YOUR_ORG/summary" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq '{agents: .counts.agents, sources: .counts.content_sources, items: .counts.content_items}'
```

## Supported Content Platforms

| Platform | Source type | What gets imported |
|---|---|---|
| GitHub | Commits, prose files (.md, .txt) | Commit messages, documentation |
| Website | Pages via sitemap or llms.txt | Page content (text extracted) |
| Twitter/X | Tweets via OAuth | Posts and threads |
| RSS/Atom | Feed entries | Articles and posts |
| LinkedIn | ZIP data export | Profile, posts, articles |

## Security

- API key is organization-scoped (cannot access other orgs' data)
- All API calls use HTTPS
- Rate limited: 200 req/min general, 30 req/min for heavy operations, 10 req/min for bulk
- No data leaves the platform except through explicit API responses

## Limitations

- Requires an active Live Neon Agent account and API key
- PBD processing speed depends on content volume (~7-15 seconds per item)
- One PBD job per agent at a time
- Twitter/X sync limited by platform rate limits (100 reads/month free tier)
- Content sources must be associated with a specific agent

---

Built by [Live Neon](https://liveneon.ai). Platform at [persona.liveneon.ai](https://persona.liveneon.ai).
