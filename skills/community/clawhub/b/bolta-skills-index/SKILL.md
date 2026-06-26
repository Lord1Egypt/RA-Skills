---
name: bolta.skills.index
version: 2.0.1
description: Bolta Skills Registry - canonical index and orchestration layer for all Bolta skills, organized by plane
category: registry
type: documentation
roles_allowed: []
agent_types: []
tools_required: []
inputs_schema:
  type: object
  description: "This is a registry index, not a callable skill"
  properties: {}
outputs_schema:
  type: object
  description: "This is a registry index, not a callable skill"
  properties: {}
organization: bolta.ai
author: Max Fritzhand
---

## Metadata

```json
{
  "name": "bolta.skills.index",
  "version": "2.0.0",
  "publisher": "bolta.ai",
  "verified": true,
  "sourceRepository": "https://github.com/boltaai/bolta-skills",
  "requiredEnvironmentVariables": [
    {
      "name": "BOLTA_API_KEY",
      "required": true,
      "sensitive": true,
      "description": "Bolta API key (obtain at bolta.ai/register)",
      "format": "sk_live_[64 characters]",
      "scope": "workspace"
    },
    {
      "name": "BOLTA_WORKSPACE_ID",
      "required": true,
      "sensitive": false,
      "description": "Workspace UUID for API operations",
      "format": "UUID"
    },
    {
      "name": "BOLTA_AGENT_ID",
      "required": false,
      "sensitive": false,
      "description": "Agent principal UUID (for audit logging)",
      "format": "UUID"
    }
  ],
  "trustedDomains": [
    "platty.boltathread.com",
    "bolta.ai",
    "mcp.bolta.ai"
  ],
  "permissions": [
    "network:https:platty.boltathread.com",
    "network:https:bolta.ai",
    "network:https:mcp.bolta.ai"
  ],
  "relatedRepositories": [
    {
      "name": "bolta-skills",
      "description": "Official Bolta Skills Pack",
      "url": "https://github.com/boltaai/bolta-skills"
    },
    {
      "name": "boltaclaw-self-hosted",
      "description": "Self-hosted Bolta agent runtime (BoltaClaw)",
      "url": "https://github.com/boltaai/boltaclaw-self-hosted"
    }
  ],
  "mcpEndpoint": "https://mcp.bolta.ai/mcp",
  "apiDocumentation": "https://bolta.ai/docs/api"
}
```

## Security Notice

**This skill requires sensitive API credentials. Read this section carefully before installing.**

### Required Credentials

**BOLTA_API_KEY** (REQUIRED, SENSITIVE)
- **Format:** `bolta_sk_` followed by alphanumeric characters
- **Obtain at:** https://bolta.ai/register (agent keys) or bolta.ai/settings (regular keys)
- **Scoping:** Each key is scoped to a SINGLE workspace only
- **Key Types:** Bolta issues two distinct key types (see [API Key Types](#api-key-types) below)
- **Rotation:** Rotate every 90 days using `bolta.team.rotate_key` skill
- **Storage:** NEVER commit to git - use environment variables or secret managers only

**BOLTA_WORKSPACE_ID** (REQUIRED)
- **Format:** UUID (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- **Source:** Provided during agent registration at bolta.ai/register
- **Purpose:** Identifies which workspace the API key is authorized for

**BOLTA_AGENT_ID** (OPTIONAL — required for Agent API keys)
- **Format:** UUID
- **Purpose:** Links API activity to specific agent principal for audit logs
- **Benefit:** Enables traceability and compliance reporting
- **Note:** Automatically set when using an Agent API key; must be provided manually with Regular API keys if audit attribution is desired

### API Key Types

Bolta has **two distinct API key types** with different permission models. Skills must handle both correctly.

#### Regular API Keys (`key_type: "regular"`)

Created in **Settings → API Keys** by workspace members. Use **granular permission scopes** — each key is issued with an explicit list of allowed scopes.

**Available scopes:**

| Scope | Description |
|-|-|
| `posts:read` | View posts and schedules |
| `posts:write` | Create and update posts |
| `posts:delete` | Delete posts and scheduled content |
| `accounts:read` | View connected social accounts |
| `accounts:connect` | Initiate OAuth connections |
| `recurring:manage` | Manage recurring post suggestions |
| `voice:read` | View brand voice profiles |
| `voice:write` | Modify brand voice profiles |
| `ai:generate` | Use AI content generation |
| `content:bulk` | Perform bulk content operations |

**Permission groups (shortcuts):**
- **READ_ONLY** — `posts:read`, `accounts:read`, `voice:read`
- **CONTENT_CREATOR** — READ_ONLY + `posts:write`, `ai:generate`
- **FULL_ACCESS** — All scopes

**When to use:** Integrations, CI/CD pipelines, custom scripts, third-party tools that need specific scopes.

#### Agent API Keys (`key_type: "agent"`)

Created in **Settings → AI Agents → Add Agent** by workspace admins. Use **role-based permissions** — the key inherits all scopes from the assigned agent role, plus agent-specific scopes not available to regular keys.

**Agent roles and their scopes:**

| Role | Scopes | Best for |
|-|-|-|
| `viewer` | `posts:read`, `accounts:read`, `voice:read`, `workspace:read` | Monitoring, reporting agents |
| `creator` | viewer + `posts:write`, `voice:write`, `ai:generate`, `review:submit`, `recurring:manage` | Content drafting agents (recommended default) |
| `editor` | creator + `posts:delete`, `review:approve`, `content:bulk`, `audit:export`, `team:manage_keys` | Content managers, approval workflows |
| `admin` | editor + `accounts:connect`, `team:manage` | Orchestrator agents, workspace automation |

**Agent-only scopes** (not available on regular keys):

| Scope | Description |
|-|-|
| `workspace:read` | View workspace policy and capabilities |
| `review:submit` | Submit content for approval |
| `review:approve` | Approve and route reviewed content |
| `audit:export` | Export workspace audit and activity logs |
| `team:manage` | Create and manage agent teammates |
| `team:manage_keys` | Rotate and manage API keys |

**Additional agent key behaviors:**
- **Safe Mode** is always enforced for `creator` role agents
- **Review required** — creator agents cannot publish directly; content goes through approval
- Agent keys carry an `agent_id` that is automatically used for audit attribution
- Agent keys link to an `AgentPrincipal` record for identity tracking

#### Skill Plane Access by Role

Agent roles determine which skill planes are accessible. Skills should check the caller's role before executing plane-restricted operations.

| Skill Plane | Min Role | Skills |
|-|-|-|
| Review | `viewer` | Inbox triage, approve/reject, review digest |
| Control | `viewer` | Audit export, key rotation, quota status, workspace config |
| Init (Voice) | `creator` | Voice bootstrap, learn from samples |
| Content | `creator` | Draft post, week plan, list recent posts |
| Automation | `creator` | Cron generate & schedule, generate to review |

A `viewer` can access Review and Control planes. A `creator` can access all planes. `editor` and `admin` can access all planes with additional capabilities within each.

#### How Skills Should Handle Key Types

1. **Check `key_type` on the API response** — the server returns `key_type: "regular" | "agent"` on authenticated responses
2. **Regular keys:** Validate required scopes exist in the key's `permissions` array before executing
3. **Agent keys:** The role determines capabilities — check the role rather than individual scopes
4. **Agent-only operations** (review workflows, audit export, team management) — reject if `key_type` is `"regular"` since these scopes are not available
5. **Audit attribution:** If `key_type` is `"agent"`, the `agent_id` is automatically attached; for regular keys, pass `BOLTA_AGENT_ID` env var if attribution is needed

### Trusted Network Endpoints

This skill makes HTTPS requests to:
- `https://platty.boltathread.com` - Bolta API server
- `https://bolta.ai` - Main application and agent registration portal
- `https://mcp.bolta.ai` - MCP protocol endpoint (for Claude Desktop / Claude Code)

**No other domains are contacted.** All requests are authenticated with your API key.

### Related Projects & Resources

- **Bolta Skills Pack** — Official skills repository
  - **Source:** https://github.com/boltaai/bolta-skills
- **BoltaClaw** — Self-hosted Bolta agent runtime
  - **Source:** https://github.com/boltaai/boltaclaw-self-hosted
- **Bolta MCP Server** — Remote MCP endpoint for Claude Desktop / Claude Code integration
  - **Endpoint:** `https://mcp.bolta.ai/mcp`
- **Bolta API Documentation** — Full API reference
  - **Docs:** https://bolta.ai/docs/api

### Pre-Installation Checklist

Before installing this skill, you MUST:
- [ ] Verify the source repository: https://github.com/boltaai/bolta-skills
- [ ] Review the SKILL.md and confirm version matches metadata (currently 2.0.1)
- [ ] Obtain a LEAST-PRIVILEGE API key from https://bolta.ai/register
- [ ] Store API key in environment variables (NEVER hardcode or commit)
- [ ] Verify you trust the domains: `platty.boltathread.com`, `bolta.ai`, and `mcp.bolta.ai`
- [ ] Test in a disposable/test workspace first (recommended)
- [ ] Confirm your API key is scoped ONLY to the intended workspace

### Security Best Practices

1. **Credential Management**
   - Use environment variables: `export BOLTA_API_KEY="sk_live_..."`
   - Or use secret managers: AWS Secrets Manager, 1Password, etc.
   - NEVER paste API keys in chat, logs, or public places

2. **Key Rotation**
   - Rotate keys every 90 days minimum
   - Use `bolta.team.rotate_key` skill for zero-downtime rotation
   - Revoke compromised keys immediately at bolta.ai/settings

3. **Permission Scoping**
   - Grant ONLY required permissions (e.g., `posts:write`, `voice:read`)
   - Avoid `workspace:admin` unless absolutely necessary
   - Review permissions quarterly

4. **Monitoring**
   - Review audit logs weekly via `bolta.audit.export_activity`
   - Monitor quota usage via `bolta.quota.status`
   - Set up alerts for unusual API activity

5. **Workspace Isolation**
   - One API key per workspace (NEVER share keys across workspaces)
   - Use separate keys for dev/staging/production environments
   - Revoke keys when decommissioning workspaces

---

## Purpose

**The canonical registry and orchestration layer for all Bolta skills.**

This skill serves as the single source of truth for skill discovery, installation recommendations, and workspace-aware capability bootstrapping. It does not execute content operations directly — instead, it provides intelligent routing to the appropriate skills based on:
- **Workspace policy** (Safe Mode, autonomy mode, quotas)
- **Principal identity** (user role, agent permissions)
- **Operational context** (what you're trying to accomplish)

**Key Responsibilities:**
1. **Discovery** - Index all available skills with metadata
2. **Recommendation** - Suggest install sets based on workspace policy and role
3. **Orchestration** - Guide multi-skill workflows
4. **Compatibility** - Enforce skill compatibility with workspace settings
5. **Bootstrapping** - Help new workspaces get started quickly

**When to Use:**
- Setting up a new workspace ("What skills should I install?")
- Discovering available capabilities ("What can Bolta do?")
- Troubleshooting skill compatibility ("Why can't I use this skill?")
- Planning multi-step workflows ("Which skills do I need?")

**Data Access:**
This skill accesses:
- Workspace configuration (policy, quotas, autonomy mode)
- Voice profile metadata (names, IDs, not full content)
- Post counts and quota usage
- Agent principal types

This skill does NOT access:
- Post content or scheduled posts
- Social media credentials
- User passwords or authentication tokens
- Files or media uploads

## Source & Verification

https://github.com/boltaai/bolta-skills

---

## Bolta Ecosystem: How It All Fits Together

Bolta is composed of four interconnected pieces. Understanding how they relate helps you choose the right setup path.

```
┌─────────────────────────────────────────────────────────────┐
│                      bolta.ai                               │
│            Workspace management, dashboards,                │
│            account connections, review UI                    │
│                                                             │
│  API Docs: https://bolta.ai/docs/api                       │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                  MCP Server (mcp.bolta.ai/mcp)               │
│     Bridges Claude Desktop / Claude Code to the Bolta API    │
│     Exposes workspace tools: create posts, manage agents,    │
│     approve content, run analytics — all via MCP protocol    │
└──────────────────────┬───────────────────────────────────────┘
                       │ uses
                       ▼
┌──────────────────────────────────────────────────────────────┐
│            Bolta Skills Pack (this repo)                      │
│     github.com/boltaai/bolta-skills                          │
│                                                              │
│     Structured prompts, workflows, and orchestration logic   │
│     that teach AI agents HOW to use the API effectively:     │
│     voice creation, content planning, review flows,          │
│     automation, analytics, engagement, governance            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│            BoltaClaw (turnkey self-hosted runtime)            │
│     github.com/boltaai/boltaclaw-self-hosted                 │
│                                                              │
│     Everything above — pre-configured and ready to run.      │
│     Ships with the skills pack, MCP integration, agent       │
│     runtime, cron scheduler, and CLI out of the box.         │
│     Clone, set your API key, and go.                         │
└──────────────────────────────────────────────────────────────┘
```

### How they work together

1. **The API** (`bolta.ai/docs/api`) is the foundation — every operation (creating posts, managing agents, approving content) flows through it. You can call it directly with `curl` or any HTTP client.

2. **The MCP Server** (`mcp.bolta.ai/mcp`) wraps the API into the MCP protocol so Claude Desktop and Claude Code can call Bolta tools natively. Point your MCP config at the endpoint and your AI assistant gains full workspace access.

3. **The Skills Pack** (`github.com/boltaai/bolta-skills`) provides the intelligence layer — structured prompts and multi-step workflows that teach agents *how* to use the API well. Skills handle things like voice-aware drafting, week planning, review triage, and cron automation that go beyond raw API calls.

4. **BoltaClaw** (`github.com/boltaai/boltaclaw-self-hosted`) is the turnkey solution. It bundles the skills pack, MCP connectivity, agent runtime, job scheduler, and a **CLI** into a single self-hosted package. The CLI lets you manage posts, agents, jobs, and workspace settings directly from your terminal — no browser required. If you want to skip manual setup and get a fully operational Bolta agent running on your own infrastructure, BoltaClaw is the fastest path — clone, configure your API key, and you're live.

### Which path is right for you?

| Goal | Start here |
|-|-|
| Explore the API directly | [API Docs](https://bolta.ai/docs/api) |
| Add Bolta tools to Claude Desktop / Claude Code | [MCP Server](https://mcp.bolta.ai/mcp) — configure the endpoint |
| Customize agent workflows and prompts | [Skills Pack](https://github.com/boltaai/bolta-skills) — clone and adapt |
| Manage Bolta from the terminal (CLI) | [BoltaClaw](https://github.com/boltaai/boltaclaw-self-hosted) — includes the CLI |
| Get everything running immediately, self-hosted | [BoltaClaw](https://github.com/boltaai/boltaclaw-self-hosted) — turnkey, pre-configured |

---

## Getting Started: API Setup

Before using Bolta skills, you need an API key. Choose the path that matches your use case.

### Path A: Agent API Key (Recommended for AI Agents)

Use this if you're setting up an AI agent (Claude, BoltaClaw, custom agent) to operate as a workspace member.

#### Step 1: Create Agent Principal

Go to **Settings → AI Agents → Add Agent** in your Bolta workspace.

Configure:
- **Agent Name** — Human-readable name for audit logs (e.g., "Claude Content Agent")
- **Agent Role** — Determines permissions and skill plane access:

| Role | What it can do | Recommended for |
|-|-|-|
| `creator` | Draft content, use voice profiles, submit for review | Most agents (default) |
| `viewer` | Read-only access to all content | Monitoring / reporting |
| `editor` | Full content management + approvals | Approval workflow agents |
| `admin` | Everything + agent/account management | Orchestrators only |

**Recommendation:** Start with `creator` role. Safe Mode is enforced and all content requires human review.

#### Step 2: Copy Your Agent API Key

After creation, you'll see the full key **once**:

```
API Key: bolta_sk_00000000000000000000000000000000
Workspace ID: 550e8400-e29b-41d4-a716-446655440000
Agent ID: 660e8400-e29b-41d4-a716-446655440001
```

The agent ID is automatically linked — no need to set `BOLTA_AGENT_ID` separately.

### Path B: Regular API Key (For Integrations & Scripts)

Use this for CI/CD pipelines, custom integrations, or scripts that need specific scopes.

#### Step 1: Create API Key

Go to **Settings → API Keys → Create New Key**.

Select **only the scopes you need** (least privilege):
- Content creation: `posts:write`, `voice:read`
- Full content: `posts:read`, `posts:write`, `voice:read`, `ai:generate`
- Read-only: `posts:read`, `accounts:read`, `voice:read`

**Note:** Regular keys cannot access agent-only scopes (`review:submit`, `review:approve`, `audit:export`, `team:manage`, `team:manage_keys`, `workspace:read`). If you need those, use an Agent API key instead.

#### Step 2: Copy Your API Key

```
API Key: bolta_sk_00000000000000000000000000000000
```

**IMPORTANT:** The full key is shown only once and cannot be recovered (only regenerated via `bolta.team.rotate_key`).

### Configure Your Environment (Both Key Types)

**Set Required Environment Variables:**

```bash
# Required: Your Bolta API key (agent or regular)
export BOLTA_API_KEY="bolta_sk_your_actual_key_here"

# Required: Your workspace UUID
export BOLTA_WORKSPACE_ID="550e8400-e29b-41d4-a716-446655440000"

# Optional: Agent principal UUID (automatic for agent keys, manual for regular keys)
export BOLTA_AGENT_ID="660e8400-e29b-41d4-a716-446655440001"
```

**For Claude Desktop / Claude Code (MCP):**

Connect via the remote MCP endpoint at `https://mcp.bolta.ai/mcp`:

```json
{
  "mcpServers": {
    "bolta": {
      "type": "url",
      "url": "https://mcp.bolta.ai/mcp",
      "headers": {
        "Authorization": "Bearer bolta_sk_your_actual_key_here",
        "X-Workspace-ID": "550e8400-e29b-41d4-a716-446655440000"
      }
    }
  }
}
```

**For self-hosted deployments**, see [BoltaClaw](https://github.com/boltaai/boltaclaw-self-hosted) for running your own agent runtime.

**For Direct API Calls:**

See the full [API documentation](https://bolta.ai/docs/api) for all available endpoints.

```bash
curl https://platty.boltathread.com/v1/posts \
  -H "Authorization: Bearer ${BOLTA_API_KEY}" \
  -H "X-Workspace-ID: ${BOLTA_WORKSPACE_ID}" \
  -H "Content-Type: application/json" \
  -d '{ "prompt": "Create a post about productivity" }'
```

**Security Reminder:**
- Never hardcode API keys in your code
- Use `.env` files locally (add `.env` to `.gitignore`)
- Use secret managers in production (AWS Secrets Manager, Vercel Secrets, etc.)
- Rotate keys every 90 days via `bolta.team.rotate_key`

### Verify Setup

Test your configuration:

```bash
curl https://platty.boltathread.com/v1/workspaces/${BOLTA_WORKSPACE_ID} \
  -H "Authorization: Bearer ${BOLTA_API_KEY}"

# Expected response:
# {
#   "id": "550e8400-...",
#   "name": "My Workspace",
#   "safe_mode": true,
#   "autonomy_mode": "managed",
#   "max_posts_per_day": 100,
#   "key_type": "agent",        ← indicates which key type authenticated
#   "agent_role": "creator"     ← present only for agent keys
# }
```

### Troubleshooting Setup

**Error: "Invalid API Key"**
- Verify key matches exactly (no extra spaces)
- Check if key was rotated — get new key at bolta.ai/settings
- Ensure you're using the correct workspace key
- Confirm key prefix starts with `bolta_sk_`

**Error: "Workspace Not Found"**
- Verify workspace_id matches your registration
- Confirm you have access to this workspace (visit bolta.ai/workspaces)
- Check if workspace was deleted

**Error: "Permission Denied"**
- **Regular keys:** Check granted scopes at Settings → API Keys
  - Content creation: Need `posts:write` minimum
  - Voice access: Need `voice:read` or `voice:write`
- **Agent keys:** Check agent role at Settings → AI Agents
  - Content creation: Need `creator` role or higher
  - Approvals: Need `editor` role or higher
  - Agent management: Need `admin` role
- Agent-only scopes (`review:submit`, `audit:export`, etc.) are not available on regular keys — switch to an Agent API key if you need them

**Error: "Insufficient Role"** (Agent keys only)
- The agent's role doesn't have access to the requested skill plane
- `viewer` cannot access Init, Content, or Automation planes
- Upgrade the agent role at Settings → AI Agents, or use a different agent

---

## Installation & First Run

### Skill Pack Installation

**Option 1: Install Full Skill Pack (Recommended)**

```bash
# Clone the complete Bolta skills repository
git clone https://github.com/boltaai/bolta-skills.git

# Or download the latest release
curl -L https://github.com/boltaai/bolta-skills/archive/refs/heads/main.zip -o bolta-skills.zip
unzip bolta-skills.zip
```

**What You Get:**
```
bolta-skills/
├── README.md                    # START HERE - Complete getting started guide
├── skills/
│   ├── bolta.skills.index/      # You're here (registry)
│   ├── voice-plane/
│   │   ├── bolta.voice.bootstrap/
│   │   └── bolta.voice.learn_from_samples/
│   ├── content-plane/
│   │   ├── bolta.draft.post/
│   │   ├── bolta.draft_post/
│   │   ├── bolta.get_account_info/
│   │   ├── bolta.get_business_context/
│   │   ├── bolta.get_voice_profile/
│   │   ├── bolta.list_recent_posts/
│   │   ├── bolta.loop.from_template/
│   │   └── bolta.week.plan/
│   ├── review-plane/
│   │   ├── bolta.add_comment/
│   │   ├── bolta.approve_post/
│   │   ├── bolta.reject_post/
│   │   ├── bolta.inbox.triage/
│   │   ├── bolta.review.approve_and_route/
│   │   └── bolta.review.digest/
│   ├── automation-plane/
│   │   ├── bolta.cron.generate_to_review/
│   │   └── bolta.cron.generate_and_schedule/
│   ├── agent-plane/
│   │   ├── bolta.agent.activate_job/
│   │   ├── bolta.agent.configure/
│   │   ├── bolta.agent.hire/
│   │   ├── bolta.agent.memory/
│   │   ├── bolta.agent.mention/
│   │   └── bolta.job.execute/
│   ├── analytics-plane/
│   │   ├── bolta.get_audience_insights/
│   │   ├── bolta.get_best_posting_times/
│   │   └── bolta.get_post_metrics/
│   ├── engagement-plane/
│   │   ├── bolta.get_comments/
│   │   ├── bolta.get_mentions/
│   │   └── bolta.reply_to_mention/
│   └── control-plane/
│       ├── bolta.team.create_agent_teammate/
│       ├── bolta.team.rotate_key/
│       ├── bolta.policy.explain/
│       ├── bolta.audit.export_activity/
│       ├── bolta.quota.status/
│       └── bolta.workspace.config/
├── docs/
│   ├── getting-started.md
│   ├── autonomy-modes.md
│   ├── safe-mode.md
│   ├── automation-setup.md
│   └── multi-agent.md
```

**Option 2: Install Individual Skills (Manual)**

```bash
# Install voice bootstrap skill
curl -L https://raw.githubusercontent.com/boltaai/bolta-skills/main/skills/voice-plane/bolta.voice.bootstrap/SKILL.md \
  -o bolta.voice.bootstrap.md

# Install draft post skill
curl -L https://raw.githubusercontent.com/boltaai/bolta-skills/main/skills/content-plane/bolta.draft.post/SKILL.md \
  -o bolta.draft.post.md
```

### First Run: Read the README

**IMPORTANT: After installation, read the README for complete setup instructions.**

**What the README Covers:**
1. Prerequisites and system requirements
2. Installation verification
3. Environment variable configuration
4. First skill execution (test workflow)
5. Troubleshooting common issues
6. Recommended skill installation order
7. Best practices for production use

### Recommended First-Run Flow

**Step 1: Read Documentation**
```bash
# Must-read files in order:
# 1. README.md              - Complete getting started guide
# 2. docs/getting-started.md - Quickstart tutorial
# 3. docs/autonomy-modes.md  - Understand autonomy levels
# 4. docs/safe-mode.md       - Understand safety controls
```

**Step 2: Verify Installation**
```bash
# Check that all skills are present
ls -la skills/*/SKILL.md skills/*/*/SKILL.md

# Should see 36+ skills across 8 planes
```

**Step 3: Configure Agent**
```bash
export BOLTA_API_KEY="sk_live_..."
export BOLTA_WORKSPACE_ID="..."

# Test API connectivity
curl https://platty.boltathread.com/v1/workspaces/${BOLTA_WORKSPACE_ID} \
  -H "Authorization: Bearer ${BOLTA_API_KEY}"
```

**Step 4: Install Recommended Skills**
```bash
# The registry will recommend skills based on your:
# - Safe Mode setting
# - Autonomy mode
# - User role
# - Current quotas
```

### Common First-Run Mistakes

1. **Skipping the README** - Installing skills without reading README
2. **Missing Environment Variables** - Running skills without BOLTA_API_KEY set
3. **Installing Skills Out of Order** - Running bolta.draft.post before creating voice profile
4. **Not Understanding Autonomy Modes** - Using autopilot mode without understanding routing
5. **Hardcoding API Keys** - Putting API keys directly in skill files instead of env vars

### Post-Installation Checklist

- [ ] README.md has been read
- [ ] Environment variables set (BOLTA_API_KEY, BOLTA_WORKSPACE_ID)
- [ ] All 36+ skills present in skills/ directory
- [ ] docs/ directory contains markdown files
- [ ] API connectivity verified (test curl command works)
- [ ] MCP endpoint configured (if using Claude Desktop / Claude Code — see mcp.bolta.ai/mcp)
- [ ] Workspace policy reviewed (safe_mode, autonomy_mode)
- [ ] First skill executed successfully (test run)
- [ ] Autonomy mode documentation read (docs/autonomy-modes.md)
- [ ] Safe Mode documentation read (docs/safe-mode.md)

### Next Steps After Setup

1. **Create Voice Profile** (if new workspace)
   - Run: `bolta.voice.bootstrap`
   - Establishes your brand voice

2. **Test Content Creation**
   - Run: `bolta.draft.post` or `bolta.draft_post`
   - Creates a test post in Draft status

3. **Install Recommended Skills**
   - Run: `bolta.skills.index`
   - Returns personalized skill recommendations

4. **Configure Workspace**
   - Review: Safe Mode (ON/OFF)
   - Review: Autonomy Mode (assisted/managed/autopilot)
   - Set: Daily quota limits

---

## Architecture: The Eight Planes

Skills are organized into **planes** — logical groupings that separate concerns and enable modular capability composition. V2 expands from five planes to eight, adding Agent, Analytics, and Engagement planes.

### Plane 0: Voice
**Purpose:** Brand voice creation, evolution, and validation

Voice is the foundation of all content operations. These skills help establish, refine, and maintain consistent brand voice across all generated content.

**Core Principle:** Voice should be learned from examples, validated against real content, and evolved over time.

**Skills:**
| Skill | Purpose |
|-|-|
| `bolta.voice.bootstrap` | Interactive voice profile creation from scratch |
| `bolta.voice.learn_from_samples` | Extract voice patterns from existing content |
| `bolta.voice.evolve` | Refine voice based on approved posts (planned) |
| `bolta.voice.validate` | Score content against voice profile 0-100 (planned) |

**Typical Flow:**
1. Bootstrap initial voice profile
2. Learn from sample content
3. Validate generated content
4. Evolve voice as brand matures

---

### Plane 1: Content
**Purpose:** Content creation, planning, data retrieval, and scheduling

The execution layer for post creation. These skills transform ideas into scheduled social media posts, and provide workspace context for informed content decisions.

**Core Principle:** Content should be intentional, planned, and aligned with voice.

**Skills:**
| Skill | Purpose |
|-|-|
| `bolta.draft.post` | Create a single post in Draft status (original interface) |
| `bolta.draft_post` | Create a draft post using workspace voice profile, routes to Inbox |
| `bolta.get_account_info` | Retrieve connected social account details |
| `bolta.get_business_context` | Fetch workspace business DNA and context |
| `bolta.get_voice_profile` | Read voice profile configuration |
| `bolta.list_recent_posts` | List recent posts for context and continuity |
| `bolta.loop.from_template` | Generate multiple posts from a template (deprecated) |
| `bolta.week.plan` | Plan a week's worth of content with scheduling |

**Output:** Draft or Scheduled posts (subject to Safe Mode routing)

---

### Plane 2: Review
**Purpose:** Human-in-the-loop review, approval, and feedback workflows

Enables teams to review, approve, reject, and provide feedback on agent-generated content before publishing.

**Core Principle:** Autonomy with oversight — agents generate, humans decide.

**Skills:**
| Skill | Purpose |
|-|-|
| `bolta.add_comment` | Add feedback comments to posts under review |
| `bolta.approve_post` | Approve a draft, moving it to Approved status |
| `bolta.reject_post` | Reject a draft with feedback for revision |
| `bolta.inbox.triage` | Organize pending posts by priority/topic |
| `bolta.review.digest` | Daily summary of posts awaiting review |
| `bolta.review.approve_and_route` | Bulk approve + schedule posts |

**Typical Flow:**
1. Agent creates posts -> Pending Approval
2. `review.digest` sends daily summary
3. Human reviews via `inbox.triage`
4. Approve/reject individual posts or bulk approve via `approve_and_route`

---

### Plane 3: Automation
**Purpose:** Scheduled, recurring, and autonomous content generation

The autonomy layer. These skills enable hands-off content operations with guardrails.

**Core Principle:** Predictable automation with quota enforcement and safety nets.

**Skills:**
| Skill | Purpose |
|-|-|
| `bolta.cron.generate_to_review` | Daily content generation -> Pending Approval |
| `bolta.cron.generate_and_schedule` | Autonomous scheduling (requires Safe Mode OFF) |

**Safety Guardrails:**
- Quota enforcement (max posts/day, max API requests/hour)
- Job run tracking (observability for all executions)
- Autonomy mode compatibility checks
- Safe Mode routing (autopilot incompatible with Safe Mode ON)

---

### Plane 4: Agent
**Purpose:** AI agent lifecycle management — hiring, configuration, job activation, and memory

V2 introduces a dedicated agent plane for managing AI teammates that operate autonomously within your workspace.

**Core Principle:** Agents are first-class principals with defined roles, jobs, and memory.

**Skills:**
| Skill | Purpose |
|-|-|
| `bolta.agent.hire` | Create and onboard a new AI agent from marketplace presets |
| `bolta.agent.configure` | Update agent settings, permissions, and job parameters |
| `bolta.agent.activate_job` | Activate or pause an agent's scheduled job |
| `bolta.agent.memory` | Read/write agent memory for cross-session context |
| `bolta.agent.mention` | Notify or hand off work to another agent |
| `bolta.job.execute` | Documentation for job execution lifecycle |

**Typical Flow:**
1. Hire an agent from presets (`agent.hire`)
2. Configure agent settings and jobs (`agent.configure`)
3. Activate the job to start autonomous work (`agent.activate_job`)
4. Agent builds memory over time (`agent.memory`)
5. Agents collaborate via mentions (`agent.mention`)

---

### Plane 5: Analytics
**Purpose:** Performance measurement, audience insights, and posting optimization

Provides data-driven insights to inform content strategy and measure impact.

**Core Principle:** Measure what matters, optimize what works.

**Skills:**
| Skill | Purpose |
|-|-|
| `bolta.get_post_metrics` | Retrieve performance metrics (likes, comments, shares, views) |
| `bolta.get_best_posting_times` | Analyze historical data for optimal posting windows |
| `bolta.get_audience_insights` | Audience demographics, growth trends, engagement patterns |

---

### Plane 6: Engagement
**Purpose:** Community interaction — monitoring mentions, replying, and managing conversations

Closes the feedback loop between publishing and audience interaction.

**Core Principle:** Respond authentically in brand voice, escalate what needs human judgment.

**Skills:**
| Skill | Purpose |
|-|-|
| `bolta.get_comments` | Retrieve comments on published posts |
| `bolta.get_mentions` | Monitor brand mentions across platforms |
| `bolta.reply_to_mention` | Draft a reply maintaining brand voice |

---

### Plane 7: Control
**Purpose:** Workspace governance, policy, security, and audit

The management layer for teams, permissions, security, and compliance.

**Core Principle:** Visibility and control for workspace administrators.

**Skills:**
| Skill | Purpose |
|-|-|
| `bolta.team.create_agent_teammate` | Provision agent principals with specific roles |
| `bolta.team.rotate_key` | Rotate API keys for security |
| `bolta.policy.explain` | Explain authorization decisions ("Why was this blocked?") |
| `bolta.audit.export_activity` | Export audit logs (PostActivity, JobRuns) |
| `bolta.quota.status` | View current quota usage (daily posts, hourly API calls) |
| `bolta.workspace.config` | View/update autonomy mode, Safe Mode, quotas |

**Typical Use Cases:**
- Onboarding new team members (human or agent)
- Investigating authorization failures
- Compliance reporting (SOC2, GDPR data exports)
- Quota monitoring and adjustment

---

## Full Skill Index

### Voice Plane Skills

#### bolta.voice.bootstrap
**Path:** `skills/voice-plane/bolta.voice.bootstrap/SKILL.md`
**Purpose:** Interactive voice profile creation wizard
**Inputs:** Brand name, industry, target audience, sample content
**Outputs:** Complete VoiceProfile (tone, dos, don'ts, constraints)
**Permissions:** `voice:write`
**Safe Mode:** Compatible
**Roles:** Viewer, Creator, Editor, Admin
**Typical Duration:** 5-10 minutes (interactive)

#### bolta.voice.learn_from_samples
**Path:** `skills/voice-plane/bolta.voice.learn_from_samples/SKILL.md`
**Purpose:** Extract voice patterns from existing content
**Inputs:** URLs or text samples (3-10 examples)
**Outputs:** Voice profile draft with auto-detected patterns
**Permissions:** `voice:write`
**Safe Mode:** Compatible
**Typical Duration:** 2-3 minutes

#### bolta.voice.evolve (planned)
**Purpose:** Refine voice based on approved posts
**Inputs:** Date range for approved posts
**Outputs:** Updated VoiceProfile (version incremented)
**Permissions:** `voice:write`, `posts:read`
**Safe Mode:** Compatible

#### bolta.voice.validate (planned)
**Purpose:** Score content against voice profile
**Inputs:** Post ID or content text
**Outputs:** Compliance score (0-100), deviation report
**Permissions:** `voice:read`, `posts:read`
**Safe Mode:** Compatible

---

### Content Plane Skills

#### bolta.draft.post
**Path:** `skills/content-plane/bolta.draft.post/SKILL.md`
**Purpose:** Create a single post in Draft status (original interface)
**Inputs:** Topic, platform(s), optional voice profile ID
**Outputs:** Post ID (Draft status)
**Permissions:** `posts:write`
**Safe Mode:** Always routes to Draft
**Autonomy Mode:** Respects assisted/managed routing
**Quota Impact:** +1 to daily post count
**Typical Duration:** 30-60 seconds

#### bolta.draft_post
**Path:** `skills/content-plane/bolta.draft_post/SKILL.md`
**Purpose:** Create a draft post using workspace voice profile, routes to Inbox for review
**Inputs:** content, platform, account_id, optional voice_profile_id
**Outputs:** Post ID (Draft/Inbox status)
**Permissions:** `posts:write`
**Safe Mode:** Always routes to Inbox
**Roles:** Viewer, Creator, Editor, Admin
**Safe Defaults:** never_publish_directly, always_route_to_inbox

#### bolta.get_account_info
**Path:** `skills/content-plane/bolta.get_account_info/SKILL.md`
**Purpose:** Retrieve connected social account details
**Inputs:** account_id (optional, returns all if omitted)
**Outputs:** Account metadata (platform, handle, status)
**Permissions:** `accounts:read`
**Safe Mode:** N/A (read-only)

#### bolta.get_business_context
**Path:** `skills/content-plane/bolta.get_business_context/SKILL.md`
**Purpose:** Fetch workspace business DNA and context
**Inputs:** workspace_id
**Outputs:** Business DNA (industry, audience, positioning)
**Permissions:** `workspace:read`
**Safe Mode:** N/A (read-only)

#### bolta.get_voice_profile
**Path:** `skills/content-plane/bolta.get_voice_profile/SKILL.md`
**Purpose:** Read voice profile configuration
**Inputs:** voice_profile_id (optional, returns active if omitted)
**Outputs:** Voice profile (tone, style, constraints)
**Permissions:** `voice:read`
**Safe Mode:** N/A (read-only)

#### bolta.list_recent_posts
**Path:** `skills/content-plane/bolta.list_recent_posts/SKILL.md`
**Purpose:** List recent posts for context and continuity
**Inputs:** account_id, limit, status filter
**Outputs:** Array of recent posts with metadata
**Permissions:** `posts:read`
**Safe Mode:** N/A (read-only)

#### bolta.loop.from_template (deprecated)
**Path:** `skills/content-plane/bolta.loop.from_template/SKILL.md`
**Purpose:** Generate multiple posts from a template
**Inputs:** Template ID, count (1-50), variation parameters
**Outputs:** Array of Post IDs
**Permissions:** `posts:write`, `templates:read`
**Note:** Deprecated in V2. Use `bolta.agent.hire` with template-based presets instead.

#### bolta.week.plan
**Path:** `skills/content-plane/bolta.week.plan/SKILL.md`
**Purpose:** Plan a week's content with scheduling
**Inputs:** Start date, posting frequency, themes
**Outputs:** 7-day content calendar with scheduled posts
**Permissions:** `posts:write`, `posts:schedule`
**Safe Mode:** Routes to Pending Approval if ON
**Quota Impact:** +5-15 to daily post count (spread across week)

---

### Review Plane Skills

#### bolta.add_comment
**Path:** `skills/review-plane/bolta.add_comment/SKILL.md`
**Purpose:** Add feedback comments to posts under review
**Inputs:** post_id, comment text
**Outputs:** Comment record
**Permissions:** `posts:read`, `posts:review`
**Safe Mode:** N/A (feedback operation)

#### bolta.approve_post
**Path:** `skills/review-plane/bolta.approve_post/SKILL.md`
**Purpose:** Approve a draft post, moving it from Inbox to Approved status
**Inputs:** draft_id, optional notes, optional schedule_time
**Outputs:** Updated post status
**Permissions:** `posts:write`, `posts:approve`
**Roles:** Editor, Admin
**Safe Defaults:** require_editor_role

#### bolta.reject_post
**Path:** `skills/review-plane/bolta.reject_post/SKILL.md`
**Purpose:** Reject a draft with feedback for revision
**Inputs:** draft_id, rejection_reason
**Outputs:** Updated post status (Rejected)
**Permissions:** `posts:write`, `posts:review`
**Roles:** Editor, Admin

#### bolta.inbox.triage
**Path:** `skills/review-plane/bolta.inbox.triage/SKILL.md`
**Purpose:** Organize pending posts by priority
**Inputs:** Optional filters (platform, date range)
**Outputs:** Categorized list of posts awaiting review
**Permissions:** `posts:read`, `posts:review`
**Safe Mode:** N/A (read-only)

#### bolta.review.digest
**Path:** `skills/review-plane/bolta.review.digest/SKILL.md`
**Purpose:** Daily summary of posts awaiting review
**Inputs:** None (workspace context)
**Outputs:** Formatted summary with quick approve links
**Permissions:** `posts:read`, `posts:review`
**Safe Mode:** N/A (read-only)
**Note:** Designed for cron execution (daily 9am)

#### bolta.review.approve_and_route
**Path:** `skills/review-plane/bolta.review.approve_and_route/SKILL.md`
**Purpose:** Bulk approve and schedule posts
**Inputs:** Post IDs or filter criteria
**Outputs:** Updated post statuses
**Permissions:** `posts:write`, `posts:approve`, `posts:schedule`
**Safe Mode:** N/A (human override)
**Note:** Bypasses Safe Mode (human decision)

---

### Automation Plane Skills

#### bolta.cron.generate_to_review
**Path:** `skills/automation-plane/bolta.cron.generate_to_review/SKILL.md`
**Purpose:** Daily content generation -> Pending Approval
**Inputs:** None (uses workspace settings)
**Outputs:** Posts in Pending Approval status
**Permissions:** `posts:write`, `cron:execute`
**Safe Mode:** Compatible (routes to Pending Approval)
**Autonomy Mode:** Recommended for managed/governance
**Quota Impact:** +3-10 posts/day (configurable)
**Execution:** Daily cron (configurable time)

#### bolta.cron.generate_and_schedule
**Path:** `skills/automation-plane/bolta.cron.generate_and_schedule/SKILL.md`
**Purpose:** Autonomous scheduling (no human review)
**Inputs:** None (uses workspace settings)
**Outputs:** Posts in Scheduled status
**Permissions:** `posts:write`, `posts:schedule`, `cron:execute`
**Safe Mode:** **INCOMPATIBLE** (requires Safe Mode OFF)
**Autonomy Mode:** **REQUIRES autopilot**
**Warning:** Bypasses human review — use with caution

---

### Agent Plane Skills

#### bolta.agent.hire
**Path:** `skills/agent-plane/bolta.agent.hire/SKILL.md`
**Purpose:** Create and onboard a new AI agent teammate from marketplace presets
**Inputs:** Agent preset selection, workspace context, voice profile
**Outputs:** Agent record + configured job(s)
**Permissions:** `agents:create`, `workspace:read`
**Roles:** Editor, Admin
**Safe Defaults:** jobs_start_paused, require_preview_approval
**Tools Required:** get_workspace_policy, get_my_capabilities, get_voice_profile, list_agent_presets, create_agent, create_job, draft_post, get_business_context

#### bolta.agent.configure
**Path:** `skills/agent-plane/bolta.agent.configure/SKILL.md`
**Purpose:** Update agent settings, permissions, and job parameters
**Inputs:** agent_id, configuration updates
**Outputs:** Updated agent record
**Permissions:** `agents:manage`
**Roles:** Editor, Admin

#### bolta.agent.activate_job
**Path:** `skills/agent-plane/bolta.agent.activate_job/SKILL.md`
**Purpose:** Activate or pause an agent's scheduled job
**Inputs:** job_id, action (activate/pause)
**Outputs:** Updated job status
**Permissions:** `agents:manage`, `cron:execute`
**Roles:** Editor, Admin

#### bolta.agent.memory
**Path:** `skills/agent-plane/bolta.agent.memory/SKILL.md`
**Purpose:** Read/write agent memory for cross-session context
**Inputs:** agent_id, memory operation (read/write/clear)
**Outputs:** Memory contents or confirmation
**Permissions:** `agents:read` (read), `agents:manage` (write)

#### bolta.agent.mention
**Path:** `skills/agent-plane/bolta.agent.mention/SKILL.md`
**Purpose:** Notify or hand off work to another agent
**Inputs:** target_agent_id, context, task description
**Outputs:** Mention record
**Permissions:** `agents:read`

#### bolta.job.execute
**Path:** `skills/agent-plane/bolta.job.execute/SKILL.md`
**Purpose:** Documentation for job execution lifecycle
**Type:** Documentation (not directly callable)
**Describes:** How agent jobs run, retry logic, observability

---

### Analytics Plane Skills

#### bolta.get_post_metrics
**Path:** `skills/analytics-plane/bolta.get_post_metrics/SKILL.md`
**Purpose:** Retrieve performance metrics for published posts
**Inputs:** account_id, optional limit/date_from/date_to/platform
**Outputs:** Metrics (likes, comments, shares, views, engagement rate)
**Permissions:** `analytics:read`
**Roles:** Viewer, Creator, Editor, Admin
**Safe Mode:** N/A (read-only)

#### bolta.get_best_posting_times
**Path:** `skills/analytics-plane/bolta.get_best_posting_times/SKILL.md`
**Purpose:** Analyze historical data for optimal posting windows
**Inputs:** account_id, optional platform filter
**Outputs:** Recommended posting times by day/hour
**Permissions:** `analytics:read`
**Safe Mode:** N/A (read-only)

#### bolta.get_audience_insights
**Path:** `skills/analytics-plane/bolta.get_audience_insights/SKILL.md`
**Purpose:** Audience demographics, growth trends, engagement patterns
**Inputs:** account_id, optional date range
**Outputs:** Audience profile and trend data
**Permissions:** `analytics:read`
**Safe Mode:** N/A (read-only)

---

### Engagement Plane Skills

#### bolta.get_comments
**Path:** `skills/engagement-plane/bolta.get_comments/SKILL.md`
**Purpose:** Retrieve comments on published posts
**Inputs:** post_id or account_id
**Outputs:** Comment list with metadata
**Permissions:** `engagement:read`
**Safe Mode:** N/A (read-only)

#### bolta.get_mentions
**Path:** `skills/engagement-plane/bolta.get_mentions/SKILL.md`
**Purpose:** Monitor brand mentions across platforms
**Inputs:** account_id, optional date range
**Outputs:** Mention list with sentiment and context
**Permissions:** `engagement:read`
**Safe Mode:** N/A (read-only)

#### bolta.reply_to_mention
**Path:** `skills/engagement-plane/bolta.reply_to_mention/SKILL.md`
**Purpose:** Draft a reply to a mention, comment, or DM in brand voice
**Inputs:** mention_id, reply_text, optional tone
**Outputs:** Reply draft (routed for approval)
**Permissions:** `engagement:write`
**Roles:** Viewer, Creator, Editor, Admin
**Safe Defaults:** always_draft_for_approval, escalate_sensitive_topics

---

### Control Plane Skills

#### bolta.team.create_agent_teammate
**Path:** `skills/control-plane/bolta.team.create_agent_teammate/SKILL.md`
**Purpose:** Provision agent principals with roles
**Inputs:** Agent name, role (creator/editor/reviewer), permissions
**Outputs:** AgentPrincipal record + API key
**Permissions:** `workspace:admin`, `agents:create`
**Role Required:** Owner or Admin

#### bolta.team.rotate_key
**Path:** `skills/control-plane/bolta.team.rotate_key/SKILL.md`
**Purpose:** Rotate API keys for security
**Inputs:** API key ID or agent ID
**Outputs:** New API key (old key revoked)
**Permissions:** `workspace:admin`, `agents:manage`
**Role Required:** Owner or Admin
**Note:** Old key immediately invalidated

#### bolta.policy.explain
**Path:** `skills/control-plane/bolta.policy.explain/SKILL.md`
**Purpose:** Explain authorization decisions
**Inputs:** Action attempt (e.g., "Why can't I publish?")
**Outputs:** Policy analysis with specific blockers
**Permissions:** None (informational)
**Use Case:** Troubleshooting "Access Denied" errors

#### bolta.audit.export_activity
**Path:** `skills/control-plane/bolta.audit.export_activity/SKILL.md`
**Purpose:** Export audit logs
**Inputs:** Date range, filters (principal, action type, denied actions)
**Outputs:** CSV or JSON export of PostActivity records
**Permissions:** `workspace:admin`, `audit:read`
**Role Required:** Owner or Admin
**Use Case:** Compliance reporting, SOC2 audits

#### bolta.quota.status
**Path:** `skills/control-plane/bolta.quota.status/SKILL.md`
**Purpose:** View current quota usage
**Inputs:** None (workspace context)
**Outputs:** Daily post count, hourly API usage, limits, percentage
**Permissions:** `workspace:read`

#### bolta.workspace.config
**Path:** `skills/control-plane/bolta.workspace.config/SKILL.md`
**Purpose:** View/update workspace settings
**Inputs:** Settings to update (autonomy_mode, safe_mode, quotas)
**Outputs:** Updated workspace configuration
**Permissions:** `workspace:admin`
**Role Required:** Owner or Admin
**Warning:** Changing autonomy mode affects all agent operations

---

## Recommended Install Sets

Install sets are curated skill bundles tailored to specific autonomy modes and use cases.

### Assisted Mode Install Set
**Autonomy Level:** Low (maximum human control)
**Safe Mode:** Must be ON
**Use Case:** New users, high-stakes brands, learning Bolta

**Skills:**
- `bolta.voice.bootstrap` - Set up initial voice profile
- `bolta.draft.post` / `bolta.draft_post` - Create individual posts (always Draft)
- `bolta.get_account_info` - View connected accounts
- `bolta.get_voice_profile` - Read voice configuration
- `bolta.list_recent_posts` - Context from recent posts
- `bolta.week.plan` - Plan content calendar

**Rationale:** Prioritizes learning and control. All content goes to Draft for manual review before scheduling. Ideal for teams new to AI content generation, brands with strict compliance requirements, or users learning Bolta patterns before automating.

---

### Managed Mode Install Set
**Autonomy Level:** Medium (guided automation with oversight)
**Safe Mode:** ON (recommended) or OFF
**Use Case:** Established users, moderate volume, review workflows

**Skills:**
- All Assisted skills +
- `bolta.inbox.triage` - Organize posts for review
- `bolta.review.digest` - Daily review summaries
- `bolta.approve_post` / `bolta.reject_post` - Individual review actions
- `bolta.review.approve_and_route` - Bulk approval workflow
- `bolta.add_comment` - Feedback on drafts
- `bolta.cron.generate_to_review` - Daily automated generation
- `bolta.get_post_metrics` - Performance tracking
- `bolta.get_best_posting_times` - Scheduling optimization

**Rationale:** Balances efficiency with oversight. Agent generates content autonomously, but humans approve before publishing. Ideal for teams with 1-2 reviewers publishing 3-10 posts/day.

---

### Autopilot Mode Install Set
**Autonomy Level:** High (hands-off automation)
**Safe Mode:** Must be OFF (incompatible)
**Use Case:** High volume, trusted voice, minimal oversight

**Skills:**
- All Managed skills +
- `bolta.cron.generate_and_schedule` - Autonomous scheduling
- `bolta.agent.hire` - Onboard AI agents
- `bolta.agent.configure` - Configure agent behavior
- `bolta.agent.activate_job` - Activate agent jobs
- `bolta.get_audience_insights` - Audience intelligence
- `bolta.get_comments` / `bolta.get_mentions` - Engagement monitoring
- `bolta.reply_to_mention` - Automated engagement
- `bolta.quota.status` - Monitor quota usage

**Rationale:** Maximizes efficiency for high-volume operations. Agent schedules directly without human approval. Only use with well-tested voice profiles, configured quota limits, and regular validation spot-checks.

**Warning:** Autopilot bypasses human review. Recommended safeguards:
- Well-tested voice profiles (version 5+)
- Quota limits configured (max 20 posts/day recommended)
- Regular validation spot-checks (review 10% of published posts)

---

### Governance Mode Install Set
**Autonomy Level:** N/A (control & audit focused)
**Safe Mode:** N/A
**Use Case:** Admins, compliance teams, workspace management

**Skills:**
- `bolta.policy.explain` - Authorization troubleshooting
- `bolta.audit.export_activity` - Compliance exports
- `bolta.team.create_agent_teammate` - Agent provisioning
- `bolta.team.rotate_key` - Security operations
- `bolta.workspace.config` - Workspace administration
- `bolta.quota.status` - Usage monitoring
- `bolta.agent.configure` - Agent management
- `bolta.agent.memory` - Agent memory inspection

**Rationale:** Control plane install set for administrators. Ideal for workspace owners managing teams, compliance officers conducting audits, and security teams rotating keys.

---

## Decision Matrix: Skill Recommendations

This matrix determines which skills to recommend based on workspace context.

### Input Variables
1. **Safe Mode** (ON/OFF)
2. **Autonomy Mode** (assisted/managed/autopilot/governance)
3. **User Role** (owner/admin/editor/creator/reviewer/viewer)
4. **Agent Permissions** (if principal is agent)
5. **Workspace Quotas** (daily post limit, hourly API limit)
6. **Voice Profile Status** (exists, version number)

### Decision Rules

#### Rule 1: Voice Bootstrapping (First-Time Setup)
```
IF voice_profile_count == 0:
  RECOMMEND: bolta.voice.bootstrap (HIGH PRIORITY)
  RATIONALE: Cannot create content without voice profile
```

#### Rule 2: Safe Mode + Autopilot Incompatibility
```
IF safe_mode == ON AND autonomy_mode == "autopilot":
  ERROR: Incompatible configuration
  RECOMMEND: Either disable Safe Mode OR switch to "managed"
  RATIONALE: Autopilot bypasses review; contradicts Safe Mode intent
```

#### Rule 3: Agent Permission Gating
```
IF principal_type == "agent":
  IF agent.permissions NOT IN required_permissions:
    EXCLUDE: Skills requiring missing permissions
    RECOMMEND: bolta.policy.explain to understand blockers
```

#### Rule 4: Role-Based Filtering
```
IF role IN ["viewer", "reviewer"]:
  EXCLUDE: All write operations (posts:write, voice:write)
  INCLUDE: Read-only skills (audit.export, policy.explain, analytics, engagement reads)

IF role IN ["creator", "editor"]:
  INCLUDE: Content plane + Review plane + Analytics + Engagement skills
  EXCLUDE: Control plane skills (team.*, workspace.config)

IF role IN ["admin", "owner"]:
  INCLUDE: All skills (no restrictions)
```

#### Rule 5: Quota-Based Warnings
```
IF daily_posts_used >= (daily_post_limit * 0.8):
  WARN: "Approaching daily quota limit"
  RECOMMEND: bolta.quota.status to view usage

IF daily_posts_used >= daily_post_limit:
  BLOCK: All posts:write skills
  RECOMMEND: Increase quota via bolta.workspace.config
```

#### Rule 6: Autonomy Mode Routing
```
IF autonomy_mode == "assisted":
  INCLUDE: Content plane (draft only) + Analytics + Engagement (read-only)
  EXCLUDE: Automation plane (no cron jobs)

IF autonomy_mode == "managed":
  INCLUDE: Content + Review + Analytics + Engagement planes
  INCLUDE: bolta.cron.generate_to_review (safe automation)
  EXCLUDE: bolta.cron.generate_and_schedule (requires autopilot)

IF autonomy_mode == "autopilot":
  INCLUDE: All automation + agent skills
  REQUIRE: Safe Mode OFF
  RECOMMEND: Quota monitoring (quota.status)
```

---

## Registry Flow (Detailed)

### Step 1: Gather Workspace Context
**API Call:** `GET /api/v1/workspaces/{workspace_id}`

**Extract:**
- `safe_mode` (boolean)
- `autonomy_mode` (assisted/managed/autopilot/governance)
- `max_posts_per_day` (int, nullable)
- `max_api_requests_per_hour` (int, nullable)

### Step 2: Identify Principal
**API Call:** `GET /api/v1/me` or use request context

**Extract:**
- `principal_type` (user or agent)
- `role` (owner/admin/editor/creator/reviewer/viewer)
- If agent: `permissions` array, `autonomy_override`

### Step 3: Check Voice Profile Status
**API Call:** `GET /api/v1/workspaces/{workspace_id}/voice-profiles`

**Extract:**
- `voice_profile_count` (0 = needs bootstrap)
- Latest `version` (higher version = more refined)
- `status` (active/draft/archived)

### Step 4: Check Quota Usage
**API Call:** `GET /api/v1/workspaces/{workspace_id}/quota-status` (via `bolta.quota.status`)

**Extract:**
- `daily_posts.used` / `daily_posts.limit`
- `hourly_api_requests.used` / `hourly_api_requests.limit`

### Step 5: Apply Decision Rules
Run through decision matrix (see above) to filter skills.

**Output:**
- `recommended_skills` - Array of skill slugs
- `excluded_skills` - Array with exclusion reasons
- `warnings` - Array of configuration issues

### Step 6: Return Structured Response
```json
{
  "workspace_id": "uuid",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "role": "editor",
  "principal_type": "user",
  "voice_profile_status": {
    "exists": true,
    "version": 3,
    "status": "active"
  },
  "quota_status": {
    "daily_posts": { "used": 12, "limit": 100, "percentage": 12 },
    "hourly_api_requests": { "used": 45, "limit": 1000, "percentage": 4.5 }
  },
  "recommended_skills": [
    "bolta.draft.post",
    "bolta.draft_post",
    "bolta.get_account_info",
    "bolta.get_voice_profile",
    "bolta.list_recent_posts",
    "bolta.week.plan",
    "bolta.inbox.triage",
    "bolta.review.digest",
    "bolta.approve_post",
    "bolta.reject_post",
    "bolta.review.approve_and_route",
    "bolta.cron.generate_to_review",
    "bolta.get_post_metrics",
    "bolta.get_best_posting_times"
  ],
  "excluded_skills": [
    {
      "skill": "bolta.cron.generate_and_schedule",
      "reason": "Requires autonomy_mode=autopilot (current: managed)"
    },
    {
      "skill": "bolta.workspace.config",
      "reason": "Requires role owner/admin (current: editor)"
    }
  ],
  "warnings": [],
  "next_steps": [
    "Install recommended skills via MCP or API",
    "Configure daily digest via bolta.review.digest",
    "Monitor performance via bolta.get_post_metrics"
  ]
}
```

---

## Output Examples

### Example 1: New Workspace (First-Time Setup)
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "safe_mode": true,
  "autonomy_mode": "assisted",
  "role": "owner",
  "principal_type": "user",
  "voice_profile_status": { "exists": false, "version": 0, "status": null },
  "quota_status": {
    "daily_posts": { "used": 0, "limit": 100, "percentage": 0 },
    "hourly_api_requests": { "used": 0, "limit": 1000, "percentage": 0 }
  },
  "recommended_skills": ["bolta.voice.bootstrap"],
  "excluded_skills": [],
  "warnings": [
    {
      "type": "missing_voice_profile",
      "message": "No voice profile found. Run bolta.voice.bootstrap to get started.",
      "severity": "high"
    }
  ],
  "next_steps": [
    "1. Run bolta.voice.bootstrap to create your brand voice",
    "2. After voice setup, install content plane skills",
    "3. Create your first post with bolta.draft_post"
  ]
}
```

### Example 2: Managed Mode (Typical Production)
```json
{
  "workspace_id": "660e8400-e29b-41d4-a716-446655440001",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "role": "admin",
  "principal_type": "user",
  "voice_profile_status": { "exists": true, "version": 5, "status": "active" },
  "quota_status": {
    "daily_posts": { "used": 18, "limit": 50, "percentage": 36 },
    "hourly_api_requests": { "used": 142, "limit": 1000, "percentage": 14.2 }
  },
  "recommended_skills": [
    "bolta.draft.post",
    "bolta.draft_post",
    "bolta.get_account_info",
    "bolta.get_business_context",
    "bolta.get_voice_profile",
    "bolta.list_recent_posts",
    "bolta.week.plan",
    "bolta.inbox.triage",
    "bolta.review.digest",
    "bolta.approve_post",
    "bolta.reject_post",
    "bolta.add_comment",
    "bolta.review.approve_and_route",
    "bolta.cron.generate_to_review",
    "bolta.get_post_metrics",
    "bolta.get_best_posting_times",
    "bolta.get_audience_insights",
    "bolta.team.create_agent_teammate",
    "bolta.audit.export_activity",
    "bolta.quota.status"
  ],
  "excluded_skills": [
    {
      "skill": "bolta.cron.generate_and_schedule",
      "reason": "Requires autonomy_mode=autopilot AND safe_mode=OFF"
    }
  ],
  "warnings": [],
  "next_steps": [
    "Configure daily content generation via bolta.cron.generate_to_review",
    "Set up review workflow with digest notifications",
    "Monitor post performance via bolta.get_post_metrics"
  ]
}
```

### Example 3: Autopilot Mode (High Volume)
```json
{
  "workspace_id": "770e8400-e29b-41d4-a716-446655440002",
  "safe_mode": false,
  "autonomy_mode": "autopilot",
  "role": "owner",
  "principal_type": "user",
  "voice_profile_status": { "exists": true, "version": 12, "status": "active" },
  "quota_status": {
    "daily_posts": { "used": 47, "limit": 200, "percentage": 23.5 },
    "hourly_api_requests": { "used": 523, "limit": 2000, "percentage": 26.15 }
  },
  "recommended_skills": [
    "bolta.draft.post", "bolta.draft_post", "bolta.get_account_info",
    "bolta.get_business_context", "bolta.get_voice_profile",
    "bolta.list_recent_posts", "bolta.week.plan",
    "bolta.inbox.triage", "bolta.review.digest",
    "bolta.approve_post", "bolta.reject_post", "bolta.add_comment",
    "bolta.review.approve_and_route",
    "bolta.cron.generate_to_review", "bolta.cron.generate_and_schedule",
    "bolta.agent.hire", "bolta.agent.configure", "bolta.agent.activate_job",
    "bolta.agent.memory", "bolta.agent.mention",
    "bolta.get_post_metrics", "bolta.get_best_posting_times",
    "bolta.get_audience_insights",
    "bolta.get_comments", "bolta.get_mentions", "bolta.reply_to_mention",
    "bolta.quota.status", "bolta.workspace.config"
  ],
  "excluded_skills": [],
  "warnings": [
    {
      "type": "high_autonomy",
      "message": "Autopilot mode bypasses human review. Monitor quota usage and validate voice compliance regularly.",
      "severity": "medium"
    }
  ],
  "next_steps": [
    "Monitor quota usage daily via bolta.quota.status",
    "Hire AI agents for specialized content via bolta.agent.hire",
    "Track engagement via bolta.get_mentions and bolta.reply_to_mention"
  ]
}
```

### Example 4: Agent Principal (Limited Permissions)
```json
{
  "workspace_id": "880e8400-e29b-41d4-a716-446655440003",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "role": "creator",
  "principal_type": "agent",
  "agent": {
    "id": "agent-uuid",
    "name": "Content Bot",
    "permissions": ["posts:write", "posts:read", "templates:read"]
  },
  "voice_profile_status": { "exists": true, "version": 7, "status": "active" },
  "quota_status": {
    "daily_posts": { "used": 8, "limit": 30, "percentage": 26.67 },
    "hourly_api_requests": { "used": 67, "limit": 500, "percentage": 13.4 }
  },
  "recommended_skills": ["bolta.draft.post", "bolta.draft_post", "bolta.list_recent_posts"],
  "excluded_skills": [
    { "skill": "bolta.week.plan", "reason": "Requires posts:schedule permission (agent lacks this)" },
    { "skill": "bolta.approve_post", "reason": "Requires posts:approve permission (agent lacks this)" },
    { "skill": "bolta.workspace.config", "reason": "Requires workspace:admin permission (agent role: creator)" }
  ],
  "warnings": [
    {
      "type": "limited_permissions",
      "message": "Agent has limited permissions. Some skills are unavailable.",
      "severity": "info"
    }
  ],
  "next_steps": [
    "Use bolta.draft_post to create content",
    "Human reviewers should use bolta.approve_post to publish"
  ]
}
```

### Example 5: Quota Limit Reached
```json
{
  "workspace_id": "990e8400-e29b-41d4-a716-446655440004",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "role": "editor",
  "principal_type": "user",
  "voice_profile_status": { "exists": true, "version": 4, "status": "active" },
  "quota_status": {
    "daily_posts": { "used": 100, "limit": 100, "percentage": 100 },
    "hourly_api_requests": { "used": 234, "limit": 1000, "percentage": 23.4 }
  },
  "recommended_skills": [
    "bolta.inbox.triage", "bolta.review.digest",
    "bolta.approve_post", "bolta.reject_post",
    "bolta.review.approve_and_route",
    "bolta.get_post_metrics",
    "bolta.quota.status", "bolta.policy.explain"
  ],
  "excluded_skills": [
    { "skill": "bolta.draft.post", "reason": "Daily quota limit reached (100/100 posts)" },
    { "skill": "bolta.draft_post", "reason": "Daily quota limit reached (100/100 posts)" },
    { "skill": "bolta.week.plan", "reason": "Daily quota limit reached (100/100 posts)" }
  ],
  "warnings": [
    {
      "type": "quota_exceeded",
      "message": "Daily post quota limit reached. No new posts can be created until tomorrow (resets at UTC midnight).",
      "severity": "high"
    }
  ],
  "next_steps": [
    "Review and approve existing posts in queue",
    "Consider increasing daily quota via bolta.workspace.config (admin only)",
    "Check quota status at midnight UTC for reset"
  ]
}
```

### Example 6: Incompatible Configuration (Autopilot + Safe Mode)
```json
{
  "workspace_id": "aa0e8400-e29b-41d4-a716-446655440005",
  "safe_mode": true,
  "autonomy_mode": "autopilot",
  "role": "owner",
  "principal_type": "user",
  "voice_profile_status": { "exists": true, "version": 8, "status": "active" },
  "quota_status": {
    "daily_posts": { "used": 5, "limit": 150, "percentage": 3.33 },
    "hourly_api_requests": { "used": 12, "limit": 1500, "percentage": 0.8 }
  },
  "recommended_skills": [],
  "excluded_skills": [
    { "skill": "ALL", "reason": "Incompatible configuration: autopilot mode requires Safe Mode OFF" }
  ],
  "warnings": [
    {
      "type": "configuration_conflict",
      "message": "Autopilot mode is incompatible with Safe Mode ON. Autopilot bypasses human review, which contradicts Safe Mode's intent.",
      "severity": "critical"
    }
  ],
  "next_steps": [
    "Choose one of the following:",
    "  A) Disable Safe Mode to use autopilot (workspace.config)",
    "  B) Switch to 'managed' autonomy mode to keep Safe Mode ON",
    "Current config blocks all agent operations until resolved."
  ],
  "error": {
    "code": "INCOMPATIBLE_CONFIGURATION",
    "message": "Autopilot autonomy mode requires Safe Mode to be OFF. Please update workspace configuration."
  }
}
```

---

## Integration with Authorization System

The registry integrates with Bolta's authorization layer to ensure skill recommendations respect workspace policies.

### Authorization Flow Integration

**Step 1: Pre-flight Authorization Check**
Before recommending a skill, check if the principal is authorized:

```python
from users.authorization import authorize, PostAction

# Check if user can create posts
auth_result = authorize(
    principal_type="user",
    role="editor",
    workspace=workspace,
    action=PostAction.CREATE,
    requested_status="Scheduled",
    agent=None  # or agent instance if principal is agent
)

if not auth_result.allowed:
    excluded_skills.append({
        "skill": "bolta.week.plan",
        "reason": auth_result.reason
    })
```

**Step 2: Respect Autonomy Mode Routing**
Skills that create posts must account for autonomy mode routing:

```python
AUTONOMY_ROUTING = {
    "assisted": {
        "Draft": "Draft",
        "Scheduled": "Draft",
        "Posted": "Draft"
    },
    "managed": {
        "Draft": "Draft",
        "Scheduled": "Pending Approval",
        "Posted": "Pending Approval"
    },
    "autopilot": {
        "Draft": "Draft",
        "Scheduled": "Scheduled",
        "Posted": "Posted"
    },
    "governance": {
        "Draft": "Pending Approval",
        "Scheduled": "Pending Approval",
        "Posted": "Pending Approval"
    }
}
```

**Step 3: Quota Enforcement**
Skills that create posts must respect quota limits:

```python
from posts.quota_enforcement import QuotaEnforcer

allowed, reason = QuotaEnforcer.check_daily_post_quota(
    workspace=workspace,
    count=10  # e.g., bolta.loop.from_template with count=10
)

if not allowed:
    excluded_skills.append({
        "skill": "bolta.loop.from_template",
        "reason": reason
    })
```

**Step 4: Safe Mode Compatibility**
Some skills are incompatible with Safe Mode:

```python
SAFE_MODE_INCOMPATIBLE = [
    "bolta.cron.generate_and_schedule",  # Bypasses review
]

if workspace.safe_mode and skill in SAFE_MODE_INCOMPATIBLE:
    excluded_skills.append({
        "skill": skill,
        "reason": "Incompatible with Safe Mode ON (requires human review bypass)"
    })
```

---

## Skill Metadata Schema

Each skill provides structured metadata via YAML frontmatter for registry indexing:

```yaml
---
name: bolta.draft.post
version: 2.0.1
description: Create a single post in Draft status
category: content
roles_allowed: [Creator, Editor, Admin]
agent_types: [content_creator, custom]
safe_defaults:
  never_publish_directly: true
  always_route_to_inbox: true
tools_required:
  - bolta.create_post
  - bolta.get_voice_profile
inputs_schema:
  type: object
  required: [content, platform, account_id]
  properties:
    content: { type: string }
    platform: { type: string }
    account_id: { type: string }
    voice_profile_id: { type: string }
outputs_schema:
  type: object
  properties:
    post_id: { type: string }
    status: { type: string }
---
```

**V2 Frontmatter Fields:**
| Field | Required | Description |
|-|-|-|
| `name` | Yes | Skill identifier (e.g., `bolta.draft.post`) |
| `version` | Yes | Semver version (all V2 skills are `2.0.0`) |
| `description` | Yes | One-line purpose |
| `category` | Yes | Skill category (content, review, agent_lifecycle, etc.) |
| `roles_allowed` | Yes | Array of roles that can use this skill |
| `agent_types` | Yes | Array of compatible agent types |
| `safe_defaults` | No | Default safety behaviors |
| `tools_required` | Yes | MCP tools this skill calls |
| `inputs_schema` | Yes | JSON Schema for inputs |
| `outputs_schema` | Yes | JSON Schema for outputs |
| `organization` | No | Publisher organization |
| `author` | No | Skill author |

---

## Version History

**2.0.0** (Current) - V2 Refactor
- **BREAKING: Expanded from 5 planes to 8 planes** (added Agent, Analytics, Engagement)
- **Added 18 new skills** across all planes
- **Added V2 YAML frontmatter schema** for all skills (replaces JSON metadata)
- Added agent lifecycle skills (hire, configure, activate_job, memory, mention)
- Added analytics skills (get_post_metrics, get_best_posting_times, get_audience_insights)
- Added engagement skills (get_comments, get_mentions, reply_to_mention)
- Added content data skills (get_account_info, get_business_context, get_voice_profile, list_recent_posts)
- Added review action skills (add_comment, approve_post, reject_post)
- Added safe_defaults to skill metadata (never_publish_directly, always_route_to_inbox, etc.)
- Deprecated `bolta.loop.from_template` in favor of agent-based presets
- Marked `bolta.voice.evolve` and `bolta.voice.validate` as planned (not yet implemented)
- Updated install sets to include new planes
- Total skill count: 36 (up from 21)

**0.5.4** - Version bump

**0.5.3** - Installation & First Run Guidance
- Added comprehensive "Installation & First Run" section
- Added complete skill pack installation instructions
- Added README.md reading prompt
- Added directory structure overview
- Added recommended first-run flow
- Added common first-run mistakes guide
- Added post-installation checklist

**0.5.1** - Security Patch
- Added explicit Required Environment Variables section
- Declared BOLTA_API_KEY, BOLTA_WORKSPACE_ID as required
- Added trusted domains list
- Enhanced security best practices

**0.5.0** - Getting Started Guide
- Added comprehensive Getting Started guide
- Added Agent API setup instructions
- Added setup verification and troubleshooting

**0.4.0** - Full Skill Descriptions
- Added comprehensive skill descriptions with metadata
- Added detailed decision matrix and authorization integration
- Added 6 output examples covering all scenarios
- Added skill metadata schema

**0.3.0** - Install Sets & Planes
- Added recommended install sets
- Added plane groupings and registry flow

**0.2.0** - Initial Index
- Added initial skill index and plane definitions

**0.1.0** - Genesis
- Initial registry structure

---

## Support

For skill installation issues, contact: support@bolta.ai
