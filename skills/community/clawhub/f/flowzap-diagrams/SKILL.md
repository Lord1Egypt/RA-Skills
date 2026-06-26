---
name: flowzap-diagrams
description: >
  Generate, validate and publish workflow, sequence and architecture diagrams, using FlowZap Code DSL.
  Use when the user asks to create a workflow, flowchart, sequence diagram, process map or an architecture diagram.
  Produces .fz code and instant shareable playground URLs via the FlowZap MCP server.
tags:
  - workflow
  - flowchart
  - sequence-diagram
  - architecture
  - mcp
  - automation
  - no-code
  - agent-tools
---

# FlowZap Diagram Skill

Generate valid FlowZap Code (`.fz`) diagrams from natural-language requests,
validate them, and return shareable FlowZap playground URLs.

This skill is designed to be paired with the `flowzap-mcp` server. The skill
gives the agent FlowZap-specific diagram knowledge and output rules; the MCP
server provides the actual tools.

## Trust and privacy summary

- This skill bundle is documentation only: `SKILL.md` plus reference files. It
  does not execute code by itself.
- The `flowzap-mcp` server runs locally on the user's machine over stdio.
- Outbound requests are restricted to `https://flowzap.xyz`.
- Raw HTTP logs, OpenAPI specs, and code snippets are parsed locally inside the
  MCP package. Only generated FlowZap Code is sent to FlowZap public endpoints
  when validation or playground creation is requested.

## When to use this skill

- User asks for a **workflow**, **flowchart**, **process diagram**, **sequence diagram**, or **architecture diagram**.
- User pastes HTTP logs, OpenAPI specs, or code and wants them visualised.
- User wants to **compare** two diagram versions (diff) or **patch** an existing diagram.

## Installation model

This setup has two parts:

1. Install the **skill bundle** so your agent knows when to use FlowZap and how
   to produce correct FlowZap Code.
2. Install the **MCP server** so your agent can validate code, create
   playground URLs, diff diagrams, and apply structured changes.

### Install the skill bundle

Recommended:

```bash
npx skills add flowzap-xyz/flowzap-mcp --skill flowzap-diagrams
```

If your agent does not support `skills.sh`, install this bundle through your
agent's skill manager or by copying the folder into the agent's local skills
directory.

Manual locations:

- Claude Code: `.claude/skills/flowzap-diagrams/SKILL.md`
- Windsurf: `.windsurf/skills/flowzap-diagrams/SKILL.md`
- Cursor: `.cursor/skills/flowzap-diagrams/SKILL.md`

### Install the MCP server (required for tools)

If the FlowZap MCP server is not already configured, install it:

```bash
# Claude Code
claude mcp add --transport stdio flowzap -- npx -y flowzap-mcp@1.3.6

# Or add to .mcp.json / claude_desktop_config.json / cursor / windsurf config:
{
  "mcpServers": {
    "flowzap": {
      "command": "npx",
      "args": ["-y", "flowzap-mcp@1.3.6"]
    }
  }
}
```

### Package verification

The pinned version `1.3.6` can be verified against the npm registry:

| Field | Value |
|-------|-------|
| **npm** | [flowzap-mcp@1.3.6](https://www.npmjs.com/package/flowzap-mcp/v/1.3.6) |
| **Integrity (SHA-512)** | `sha512-9pnsETVvbCj5+cDEbiwRBWbqaA+FDMIJFU/vylXCnJOAt6nuvlFQf3/M8WI6EeBoVtGw/OyBZtJTQSjFUh4U0w==` |
| **Shasum** | `86a434a49f4ec9e6fae76cc34acb73f357e81b1f` |
| **Source** | [github.com/flowzap-xyz/flowzap-mcp](https://github.com/flowzap-xyz/flowzap-mcp) |
| **License** | MIT |

To verify locally before use:
```bash
npm view flowzap-mcp@1.3.6 dist.integrity dist.shasum
```

Compatible tools: Claude Desktop, Claude Code, Cursor, Windsurf, OpenAI Codex,
Warp, Zed, Cline, Roo Code, Continue.dev, Sourcegraph Cody.

**Not compatible:** Replit, Lovable.dev.

Without the MCP server, this skill can still help an agent draft FlowZap Code,
but it cannot validate diagrams, create playground URLs, or use the FlowZap
tooling workflow described below.

## Available MCP tools

| Tool | Purpose |
|------|---------|
| `flowzap_validate` | Check .fz syntax before sharing |
| `flowzap_create_playground` | Get a shareable playground URL |
| `flowzap_get_syntax` | Retrieve full DSL docs at runtime |
| `flowzap_export_graph` | Export diagram as structured JSON (lanes, nodes, edges) |
| `flowzap_artifact_to_diagram` | Parse HTTP logs / OpenAPI / code → diagram + playground URL |
| `flowzap_diff` | Structured diff between two .fz versions |
| `flowzap_apply_change` | Patch a diagram (insert/remove/update nodes/edges) |

## FlowZap Code DSL — quick reference

FlowZap Code is **not** Mermaid, **not** PlantUML. It is a unique DSL offering a simple syntax for a triple-view option to workflow, sequence and architecture diagrams.

### Shapes (only 4)

| Shape | Use for |
|-------|---------|
| `circle` | Start / End events |
| `rectangle` | Process steps / actions |
| `diamond` | Decisions (Yes/No branching) |
| `taskbox` | Assigned tasks (`owner`, `description`, `system`) |

### Syntax rules

- **Node IDs** are globally unique, sequential, no gaps: `n1`, `n2`, `n3` …
- **Node attributes** use colon: `label:"Text"`
- **Edge labels** use equals inside brackets: `[label="Text"]`
- **Handles** are required on every edge: `n1.handle(right) -> n2.handle(left)`
- **Directions**: `left`, `right`, `top`, `bottom`
- **Cross-lane edges**: prefix target with lane name: `sales.n5.handle(top)`
- **Lane display label**: one `# Label` comment on the same line as the opening brace
- **Loops**: `loop [condition] n1 n2 n3` — flat, inside a lane block
- **Layout**: prefer horizontal left→right; use top/bottom only for cross-lane hops

### Multi-lane sequence design

- **Ping-pong rule**: For multi-participant processes, every cross-lane interaction must alternate back-and-forth between lanes. A request from Lane A → Lane B must be followed by a response from Lane B → Lane A before any new major cross-lane request begins. This is now a strict validation requirement, not just a readability suggestion.
- **Chronological order**: The sequence view follows cross-lane edge definition order. Define request, response, then next request in the exact order they happen.

### Gotchas — never do these

- Do NOT use `label="Text"` on nodes (must be `label:"Text"`).
- Do NOT use `label:"Text"` on edges (must be `[label="Text"]`).
- Do NOT skip node numbers (n1, n3 → invalid; must be n1, n2).
- Do NOT omit lane prefix on cross-lane edges.
- Do NOT output Mermaid, PlantUML, or any other syntax.
- Do NOT add comments except the single `# Display Label` per lane.
- Do NOT place `loop` outside a lane's braces.
- Do NOT use a `taskbox` shape unless the user explicitly requests it.

### Minimal templates

**Single lane:**

```
process { # Process
n1: circle label:"Start"
n2: rectangle label:"Step"
n3: circle label:"End"
n1.handle(right) -> n2.handle(left)
n2.handle(right) -> n3.handle(left)
}
```

**Two lanes with cross-lane edge:**

```
user { # User
n1: circle label:"Start"
n2: rectangle label:"Submit"
n5: rectangle label:"Receive result"
n1.handle(right) -> n2.handle(left)
n2.handle(bottom) -> app.n3.handle(top) [label="Send"]
}

app { # App
n3: rectangle label:"Process"
n4: rectangle label:"Respond"
n3.handle(right) -> n4.handle(left)
n4.handle(top) -> user.n5.handle(bottom) [label="Result"]
}
```

**Decision branch:**

```
flow { # Flow
n1: rectangle label:"Check"
n2: diamond label:"OK?"
n3: rectangle label:"Fix"
n4: rectangle label:"Proceed"
n1.handle(right) -> n2.handle(left)
n2.handle(bottom) -> n3.handle(top) [label="No"]
n2.handle(right) -> n4.handle(left) [label="Yes"]
}
```

**For the full DSL specification and advanced multi-lane examples**: See [references/syntax.md](references/syntax.md)

## Workflow: how to generate a diagram

1. Identify the **actors/systems** (→ lanes) and **steps** (→ nodes) from the user's description.
2. Write FlowZap Code following all rules above.
3. Call `flowzap_validate` to verify syntax.
4. If valid, call `flowzap_create_playground` to get a shareable URL.
5. Return the FlowZap Code **and** the playground URL to the user.
6. Always output **only** raw FlowZap Code when showing the diagram — no Markdown fences wrapping .fz content, no extra commentary mixed in.

Full MCP documentation: [flowzap.xyz/docs/mcp](https://flowzap.xyz/docs/mcp)

## Security and data transparency

The trust boundary is intentionally narrow:

- The skill bundle is static Markdown and reference text.
- The MCP server runs locally and only calls public FlowZap APIs.
- Outbound traffic is restricted to `https://flowzap.xyz`.
- Validation is stateless; playground sessions are time-limited.

The `flowzap-mcp` server runs locally on the user's machine (stdio transport) and enforces the following safeguards:

| Control | Detail |
|---------|--------|
| **TLS only** | All outbound requests require `https://` and are restricted to `flowzap.xyz` (SSRF protection) |
| **No authentication** | Uses only public FlowZap APIs; no API keys, tokens, or user credentials are stored or transmitted |
| **No user-data access** | Cannot read diagrams, accounts, or any data beyond what the agent explicitly passes in |
| **Input validation** | Code capped at 50 KB, total input at 100 KB; null bytes and control characters stripped |
| **Rate limiting** | Client-side 30 requests/minute sliding window |
| **Request timeout** | 30-second hard timeout with `AbortController` |
| **Response sanitization** | Only expected fields are returned; playground URLs validated against allowlist |
| **Audit logging** | All tool calls and API requests logged to `stderr` (not exposed to the MCP client) |

### Data flow scope

The MCP server processes raw inputs locally and sends only generated or agent-provided FlowZap Code to FlowZap public endpoints:

1. `POST https://flowzap.xyz/api/validate` — returns syntax validation result
2. `POST https://flowzap.xyz/api/playground/create` — returns an ephemeral playground URL (60-minute TTL, non-guessable token)

If the agent uses `flowzap_artifact_to_diagram`, the raw HTTP logs, OpenAPI spec,
or code snippet are parsed locally inside the MCP package first. Only the
resulting FlowZap Code is sent when a playground URL is created.

No local file paths, environment variables, user identity, repository contents,
or credentials are transmitted by the MCP package.

### Playground URL access controls

Playground URLs are ephemeral, time-limited (60-minute TTL), and use non-guessable cryptographic tokens. They are read-only views of the diagram code submitted at creation time. No account or login is required to view them; no data persists beyond the TTL.

### Data lifecycle

| Endpoint | Data stored | Retention |
|----------|-------------|-----------|
| `POST /api/validate` | **None** — stateless; code is parsed in memory and discarded after the response | 0 (not persisted) |
| `POST /api/playground/create` | FlowZap Code only (in PostgreSQL) | 60 minutes (database row + playground URL both expire) |

The playground session is stored server-side with a cryptographic token (UUID v4). After the 60-minute TTL, the session is deleted — either on the next access attempt or during a periodic sweep. No user identity, file paths, environment variables, or host metadata are attached to the session.

### What the MCP server does NOT do

- **No filesystem access** — cannot read or write files on the host machine
- **No environment variable access** — does not read or transmit `process.env` or shell variables
- **No code execution** — does not evaluate, compile, or run any user code; it only transmits FlowZap DSL text
- **No network scanning** — outbound connections are restricted to `flowzap.xyz` over TLS (SSRF-protected allowlist)
- **No long-term data persistence** — playground sessions expire after 60 minutes; the validate endpoint stores nothing
- **No telemetry or tracking** — no analytics, device fingerprinting, or usage data is collected by the MCP server; server-side API logs record only IP, user-agent, and code length (not code content)

## Further resources

- [FlowZap Code full spec](https://flowzap.xyz/flowzap-code)
- [LLM context file](https://flowzap.xyz/llms-full.txt)
- [JSON syntax schema](https://flowzap.xyz/api/flowzap-code-schema.json)
- [200+ workflow templates](https://flowzap.xyz/templates)
- [MCP server docs](https://flowzap.xyz/docs/mcp)
- [npm package — flowzap-mcp v1.3.6](https://www.npmjs.com/package/flowzap-mcp)
- [GitHub](https://github.com/flowzap-xyz/flowzap-mcp)
