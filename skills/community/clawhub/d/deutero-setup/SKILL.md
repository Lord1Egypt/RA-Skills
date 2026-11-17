---
name: deutero-setup
description: Connect to Deutero — create an account when there is none, authorize the MCP server by OAuth or API key, and confirm the connection and credit balance before any study work begins. Use this whenever Deutero tools are missing, return 401 or 403, or the user says they are new to Deutero, asks how to sign up, asks for an API key, asks to connect or configure the Deutero MCP server in Claude Code, Claude Desktop, Cursor or Windsurf, wants to call Deutero from their own code or backend with the `deutero` Python SDK, or an agent needs its own Deutero account created from a programmable inbox. Also use it first whenever any other Deutero task fails on authentication or plan limits, since almost every such failure is a setup problem rather than a study problem.
---

# Connecting to Deutero

Deutero is an AI-conducted qualitative research platform. Everything except account creation and a handful of dashboard-only features is reachable over MCP or REST, so an agent that is properly connected can create studies, write questions, author branching flows, run simulations and read transcripts without a browser.

The connection is the thing that quietly breaks work later, so settle it before designing anything. Two questions decide what you do: is there an account, and is this client authorized against it?

## Step 1: Test what is already there

Call `health_health_get`, then `list_projects`. What comes back tells you where you are.

- **Both succeed** — you are connected. Call `get_credit_balance`, note the balance and its `plan` block, and go on to the real task.
- **No Deutero tools exist at all** — the MCP server is not configured. Go to Step 3.
- **401** — the client is configured but the credential is wrong, disabled or deleted. Regenerate or re-authorize (Step 3).
- **403 with "Upgrade required"** — connected fine, but the plan does not cover the feature. Not a setup problem; report the plan the message names and continue with what the plan allows.
- **402** — connected, out of credits. Report the balance and stop before starting anything that spends. (On `publish_study`, a 402 can also be `plan_limit_reached`, the open-study limit. Read `detail.code`.)

## Establish the plan before you design anything

Two separate limits decide what a user can do: the **credit balance** (how much work fits) and the **plan tier** (which features exist at all). A feature the plan does not cover is refused with 403 no matter how many credits are spare, so find out the plan first.

**Assume Hobby until you have checked.** It is where every new account lands, and most users are on it: **text chat and on-device voice only, on the `open_weights` model, 15 credits a month, linear question lists only (no Interview Flow), no simulations, no image questions, one open (published) study at a time.** That rules out much of what the other Deutero skills describe, and finding it out after authoring forty questions wastes the user's time.

`get_credit_balance` returns a `plan` block: `plan_tier`, `model_tiers` (the only tiers you may offer), `interview_modalities` (`text`, `voice_local`, `voice_cloud`, `video`), `whatsapp`, `interview_flow`, `image_questions`, `simulations` and `open_study_limit`. Check it at the start of study work unless you hold a record that this organization upgraded and nothing has contradicted it since; a 403 `upgrade_required` means the record is stale. Do not infer the plan from `base_limit` — complimentary and custom plans break that mapping.

`references/plan-limits.md` has the full matrix, the fallback when `plan` is missing, and what to do instead at each gate. Read it before promising a user a feature.

## Step 2: Create an account, if there is none

Skip this when the user already has one — most do. It matters mainly when an agent needs an account of its own.

**Signup cannot be done through the API.** There is no account-creation endpoint; it needs a browser and a mailbox you can read. The full verified procedure, including the two magic-link traps that break headless runs, is in `references/account-signup.md`. Read it before driving the browser rather than improvising, because the flow has to complete in a single cookie session and a failed attempt means starting over.

The short shape: request a magic link at `/login`, pull the link from the **plain-text** body of the Stytch email, navigate directly to `/authenticate?stytch_token_type=discovery&token=<token>`, name the organization at `/create-organization`, then generate an API key in Settings.

If the user is signing up themselves, just point them at `https://dashboard.deutero.ai/login` — the same magic-link flow, without the automation hazards.

## Step 3: Authorize this client

Two methods work, and the right one depends on the client.

**OAuth** is the better choice wherever the client supports remote MCP authorization — claude.ai connectors, and any client that implements the MCP authorization spec. The user signs in with their Deutero account, no secret is stored in a config file, and they can revoke the client later under **Connected Applications** in Settings. This plugin's `mcp.json` declares the endpoint with no credentials for exactly this reason: authorization is the client's job, and a header in a package file is a secret in a shared file.

```json
{
  "mcpServers": {
    "deutero": {
      "type": "streamable-http",
      "url": "https://dashboard.deutero.ai/mcp"
    }
  }
}
```

If the client installed this plugin, that server is already configured and the first tool call triggers the authorization prompt. Tell the user to expect a browser window and to approve it; do not try to complete an OAuth flow on their behalf.

**An API key** suits IDEs, scripts and CI, where there is no browser to hand. Keys are organization-scoped, shown once, and set as the `X-API-Key` header. `references/mcp-clients.md` has the exact configuration block for each client and how to generate, label, disable and rotate keys.

**Code that runs without you** — a webhook receiver, a scheduled job, a script that builds studies from a file — cannot use MCP at all. In Python it uses the `deutero` SDK (`pip install "deutero>=0.2"`, `Deutero()` reads `DEUTERO_API_KEY`), which has one method per MCP tool; in any other language, the REST routes in `references/mcp-clients.md`. `references/python-sdk.md` maps every tool to its method and lists the differences that bite.

Restart the client after any configuration change — tools that "do not appear" are almost always a client that has not reloaded.

## Step 4: Confirm before you build

Re-run `health_health_get` and `list_projects`, and report in one line: connected, which organization, and the credit balance. Then get on with the actual work.

## What is not available over MCP

These exist only in the dashboard, so plan around them rather than hunting for a tool:

- Thematic analysis and its reports
- Prolific recruitment, Slack and Discord connectors
- Billing, Chat with Data

Clustering, transcript search, scale/options response summaries and webhook endpoints **are** available over MCP (and the SDK), and so is AI drafting of study details (`draft_study`, `draft_study_from_site`), interview questions (`generate_questions`) and the welcome text (`generate_welcome`), and publishing and pausing a study (`publish_study`, `pause_study`, `validate_study`, `get_publication_status`) and branding the interview pages (`get_theme`, `set_theme`, `upload_welcome_hero`) — over MCP and REST, not yet the SDK; see `plan-interview-research` and `recruit-participants`.

When you hit something no tool does (a missing tool or parameter, results that came back incomplete, a description that misled you), call `report_feedback` before telling the user it cannot be done. It goes to the Deutero team, costs nothing, and is how gaps get closed.

## Keeping credentials safe

Store a key as `DEUTERO_API_KEY` with owner-only permissions, never in a committed file, never in a log line, and never echoed back into a transcript. An embed **signing secret** (`dtro_sk_…`) is a stronger secret still — it can forge verified metadata for the organization's studies — and belongs only on a server. Delete keys you stop using.

## References

- `references/account-signup.md` — browser-driven account creation for an agent, verified end to end, with the failure modes
- `references/mcp-clients.md` — per-client configuration, API key lifecycle, REST equivalents, and the troubleshooting table
- `references/python-sdk.md` — the `deutero` Python SDK: install, MCP tool → method map, errors, webhook verification, and the 0.1 → 0.2 break
- `references/plan-limits.md` — what each plan includes, how to detect the plan, and the fallback for every gated feature
