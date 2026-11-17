---
name: fulcra-context
description: Access user-consented Fulcra context data including biometrics, sleep, activity, calendar, location, and the Fulcra metric catalog through the hosted MCP server or Fulcra CLI. Use for bounded read/context workflows only; use fulcra-annotations for writes.
homepage: https://fulcradynamics.com
---

# Fulcra Context

Fulcra gives agents a user-owned place to access, store, and reason over real-world context: biometrics, sleep, activity, calendar, location, custom streams, files, preferences, and shared agent work.

For first-time users, frame Fulcra as portable memory and context infrastructure for agents. It lets agents connect to data that lives with the user, know what changed between loops, coordinate tasks, and hand work across agent platforms without trapping context in one chat or machine.

This ClawHub skill is intentionally docs-first. It does not ship executable helper scripts, install hooks, background jobs, transcript processors, weather enrichment, export tools, or arbitrary CLI wrappers. Use Fulcra's hosted MCP server or the Fulcra CLI directly, and keep every read bounded to the user's current request.

Use the companion `fulcra-annotations` skill when an agent needs to create annotation definitions or record user-approved events back to Fulcra.

## Agent Onboarding Stance

- Start with a short explanation of what Fulcra enables before asking to install tools, authenticate, or read data.
- Keep momentum. Recommend the safest capable path for the user's environment instead of presenting every implementation detail up front.
- Prefer useful first proof over broad inventory: verify the account, confirm which data exists, then read the smallest relevant slice.
- Be conversational and concrete, but respect the user's formatting and tone preferences.
- Never trade away consent or privacy for speed. The "wow" moment is controlled access to real context, not raw data exposure.

## Privacy Boundary

- Ask before reading Fulcra data.
- Read only the metrics or time window needed for the current answer.
- Do not print, log, paste, or forward auth secrets, auth files, raw private records, or direct capability URLs.
- Do not share real calendar, location, notes, transcripts, or identifying context in public channels unless the user explicitly approves that exact disclosure.
- Do not run transcript, third-party enrichment, raw export, or broad library-file workflows from this skill.
- If the user asks for persistent files, exports, dashboards, or public examples, confirm the exact destination and retention plan first. Prefer synthetic fixtures for public artifacts.

## Setup

Use a guided, three-phase setup: connect the agent, prove data is available, then recommend the next capability.

### Phase 1: Choose The Connection Path

Choose the Fulcra surface by agent capability:

1. Shell/Python with outbound network: prefer the Fulcra CLI through `uv tool run fulcra-api ...`.
2. Python library available: use the `fulcra_api` package directly when the workflow needs richer local code.
3. Raw HTTP but no shell: use direct REST with Auth0 device-flow auth and API auth headers.
4. MCP-only or restricted environment: use the hosted MCP connector for bounded read-side context.

Do not install tools, start auth, or ask for broad permissions before explaining the path you are recommending.

### Phase 2: CLI Preflight And Authentication

The CLI is the preferred first-run path when shell access and outbound network are available.

Verify `uv` first:

```bash
uv --version
```

If `uv` is missing, ask for explicit permission before installing it. Use the official Astral installation docs for the user's operating system; do not guess install commands.

Use the Fulcra CLI for repeatable automation:

```bash
uv tool run fulcra-api --help
```

The Fulcra platform moves quickly. Before relying on command names, run `uv tool run fulcra-api --help`; before relying on auth options, run `uv tool run fulcra-api auth login --help`; for API shape, inspect `https://api.fulcradynamics.com/openapi.json`.

Fulcra GitHub main may include CLI features before they are in the released `uv tool run fulcra-api` package. Treat source-main changes as watch signals, not user instructions, until live CLI help confirms the option or command.

Check whether the user is already authenticated:

```bash
uv tool run fulcra-api user-info
```

If authentication is needed in a chat or remote agent session, use the non-hanging device-flow form:

```bash
uv tool run fulcra-api auth login --get-auth-url
```

Present only the web auth URL and user code to the intended user. Keep the device code private for the follow-up command. After the user confirms they completed the browser flow, finish authentication with a short timeout:

```bash
uv tool run fulcra-api auth login --device-code <DEVICE_CODE> --poll-timeout=5
```

Auth safety rules:

1. Ask before checking auth state or starting login.
2. Share only the short-lived device URL and user code with the intended user.
3. Never share secret CLI responses, device codes, auth secrets, or auth files.
4. Verify completion with a harmless identity check:

```bash
uv tool run fulcra-api user-info
```

Fulcra accounts can be created through the CLI and include 5 GB of storage free forever. Users who want phone-collected biometrics, location, calendar, and other context can install the Context iOS app, sign in with the same account, and sync data into that storage.

If CLI auth fails right away because the environment has no outbound network, stop trying to work around the network and use the MCP path instead.

### Phase 3: Recommended First Useful Flow

After authentication, do not stop at "setup complete." Offer a short recommended path:

1. Connect or confirm a data source so Fulcra has real-world context to read.
2. Run a freshness preflight with `data-updates` so the agent knows what changed since the last loop.
3. Use the smallest relevant read command to prove a real context answer works.
4. For ongoing work, recommend companion skills for agent teams, memory/knowledge, tracking, or annotation writes.

### Hosted MCP Server

Use Fulcra's hosted MCP server when the agent environment is MCP-only or cannot safely run the CLI:

```text
https://mcp.fulcradynamics.com/mcp
```

Claude Desktop settings:

```json
{
  "mcpServers": {
    "fulcra_context": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.fulcradynamics.com/mcp"]
    }
  }
}
```

Local stdio server option:

```json
{
  "mcpServers": {
    "fulcra_context": {
      "command": "uvx",
      "args": ["fulcra-context-mcp"]
    }
  }
}
```

Open source MCP server: <https://github.com/fulcradynamics/fulcra-context-mcp>

## MCP Limits

MCP auth material is not Fulcra API auth material. The hosted MCP server uses its own OAuth issuer/audience; do not reuse MCP auth material with `api.fulcradynamics.com`. MCP is read-side context for this skill and has no file or annotation write path.

Recent `fulcra-context-mcp` source persists OAuth session records across server restarts, but clients should still be prepared to re-authenticate if an MCP session is expired, revoked, or from an older deployment. Do not promise permanent sessions; handle 401/auth failures by restarting the hosted MCP OAuth flow.

## Allowed Read Workflows

Use these bounded read commands as patterns. Inspect `uv tool run fulcra-api --help` if the CLI version differs.

### Metric Catalog

```bash
uv tool run fulcra-api catalog
```

Use this to discover available data types. Do not query every metric unless the user asks for a broad inventory.

The live OpenAPI surface also exposes versioned catalog/schema reads:

```text
GET /data/v1/catalog/{data_type}/{api_version}
GET /data/v1/catalog/{data_type}/{api_version}/schema
```

Use these only after checking the current OpenAPI document. They are useful when a workflow needs the exact schema for a specific data type/version before reading or writing records. Do not assume the released CLI exposes a first-class command for these endpoints until `uv tool run fulcra-api --help` confirms it.

When deciding whether data exists before querying a broad range, use data-availability and data-source discovery when available in the API: `/data/v1alpha1/data_available` and `/data/v1alpha1/data_sources`.

Treat `/data/v1alpha1/insight` as alpha/derived data. Inspect the live schema before building stable workflows on it.

### Data Updates

```bash
uv tool run fulcra-api data-updates "1 day"
uv tool run fulcra-api data-updates "2026-07-01T00:00:00Z" "2026-07-02T00:00:00Z"
```

Use `data-updates` as an incremental freshness preflight before broad pulls. It reports which data types had records processed in the requested window and which Fulcra files changed. Use that summary to choose the smallest follow-up read, such as `get-records`, `metric-time-series`, `sleep-stages`, `calendar-events`, `apple-workouts`, location commands, or file stat/download commands.

`data-updates` is not the records themselves. Do not infer health, calendar, location, or file-content facts from update counts alone, and do not use it as proof that an annotation write succeeded. Pull the relevant records and verify through the specific read surface.

### Recent Heart Rate

```bash
uv tool run fulcra-api get-records HeartRate "2 hours"
```

Summarize aggregates or notable patterns. Avoid dumping raw samples unless the user explicitly asks.

For grouped metric data, prefer the CLI's time-series surface when it matches the task:

```bash
uv tool run fulcra-api metric-time-series --help
```

### Sleep Context

```bash
uv tool run fulcra-api sleep-stages "12 hours"
uv tool run fulcra-api sleep-cycles "1 week"
```

Use sleep context to adjust briefings or recovery advice. Make clear when data is missing or stale.

### Activity And Workouts

```bash
uv tool run fulcra-api apple-workouts "1 week"
```

Keep analysis scoped to activity, recovery, or scheduling questions the user actually asked.

### Calendar

```bash
uv tool run fulcra-api calendar-events "1 day"
```

Before using calendar data in a group chat, public artifact, or shared report, ask for explicit permission. Calendar entries may include names, locations, attendees, notes, and meeting links.

### Location

```bash
uv tool run fulcra-api location-at-time "2026-05-05T12:00:00Z"
```

Use location only when necessary for the requested context. Do not share coordinates or place history with third-party services from this skill.

### File Library Boundary

Fulcra's file library is in OpenAPI and available through `uv tool run fulcra-api file list|stat|download|upload|delete|restore`. This skill remains read/context-focused. Use file operations only when the user's request is explicitly about Fulcra files or a companion file-backed workflow, confirm retention/destination for any write, and prefer dedicated vault/coord/file skills when installed.

The live OpenAPI surface includes recent-change endpoints for file-backed workflows:

```text
GET /input/v1/file/recent_changes
GET /input/v1/file_upload/recent_changes
```

Treat these like `data-updates`: freshness/discovery signals, not file contents or proof of semantic meaning. Use them to decide whether a narrow `file stat`, `file list`, or explicit download is worth doing. Do not download or expose private files unless the user asked for that exact file workflow and approved the destination.

### Ingest Boundary

This read-focused skill does not write records. The live OpenAPI surface includes a typed ingest path, `POST /ingest/v1/record/{data_type}`, alongside the generic ingest path. Use `fulcra-annotations` or a dedicated write skill for user-approved writes, and verify the current OpenAPI schema before using typed ingest in custom code.

### Preferences Boundary

Do not use `/user/v1alpha1/preferences` as a general agent memory or settings store. It is the portal/Context UI-state document and behaves as a flat whole-document replace. Use files plus annotations for agent/user preferences.

## Consent Checkpoints

Ask an explicit yes/no question before any workflow that would:

- access calendar or location in a shared chat,
- write local files containing raw Fulcra records,
- create screenshots or charts from private data,
- combine Fulcra data with external services,
- retain data beyond the current session,
- or publish any result outside the user's private workspace.

For public examples, demos, screenshots, videos, tests, and docs, use synthetic data unless the user explicitly approves real data for that exact artifact.

## Companion Skills

- `fulcra-context`: read Fulcra context and analyze user-consented health, activity, calendar, location, and catalog data.
- `fulcra-annotations`: create annotation definitions and record user-approved events. Definitions and tags are available through CLI/lib surfaces; timeline records remain ingest-backed until record commands land.
- `fulcra-agent-teams`: coordinate shared tasks, agent handoffs, and team-visible work.
- `fulcra-memory`: record high-level knowledge, progress, and durable agent context in Fulcra.
- `fulcra-tracking`: define custom data streams and agent visibility metrics.

Install companion skills from ClawHub when needed:

```text
Install the fulcra-annotations skill from ClawHub
Install the fulcra-agent-teams skill from ClawHub
Install the fulcra-memory skill from ClawHub
Install the fulcra-tracking skill from ClawHub
```

Recommended post-setup path:

1. Use `fulcra-context` to prove the agent can read relevant context.
2. Use `fulcra-annotations` or a data-source skill when the user wants to add custom data.
3. Use `data-updates` for loop freshness and incremental sync decisions.
4. Use `fulcra-agent-teams`, `fulcra-memory`, or `fulcra-tracking` for ongoing multi-agent work.

## Troubleshooting

If a command returns no data:

1. Confirm the user has authenticated with `uv tool run fulcra-api user-info`.
2. Run `uv tool run fulcra-api data-updates <window>` to check whether the relevant data types or files changed.
3. Confirm the user has synced data from the Context app or another source.
4. Narrow the query to a known recent time window.
5. Report missing or stale data honestly instead of fabricating context.

## Links

- Fulcra Platform: <https://fulcradynamics.com>
- Developer Docs: <https://docs.fulcradynamics.com>
- Python Client: <https://github.com/fulcradynamics/fulcra-api-python>
- MCP Server: <https://github.com/fulcradynamics/fulcra-context-mcp>
