# FlowyTeam MCP

> Connect Claude Code (or any MCP-compatible AI agent) to your FlowyTeam workspace and manage your entire business via natural language.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-blue.svg)](https://modelcontextprotocol.io)
[![Tools](https://img.shields.io/badge/Tools-34-orange.svg)](SKILL.md)
[![Platform](https://img.shields.io/badge/Platform-FlowyTeam-teal.svg)](https://flowyteam.com)
[![ClawhHub](https://img.shields.io/badge/ClawhHub-flowyteam--mcp-purple.svg)](https://clawhub.ai/agungksidik/flowyteam-mcp)

---

## What is FlowyTeam?

[FlowyTeam](https://flowyteam.com) is an all-in-one SaaS platform for team productivity and performance management — OKRs, KPIs, projects, HR, CRM, finance, and more. Trusted by 7,000+ organizations across 140+ countries.

---

## What does this MCP do?

This skill connects Claude Code (or any MCP client) to your FlowyTeam workspace via a remote HTTP MCP server. Once connected, you can manage your entire workspace through natural language — no need to open the app.

**34 tools. Read and write access to your workspace. No extra software required.**

---

## Endpoints

| Endpoint | Auth | Purpose |
|---|---|---|
| `POST /api/mcp/gateway` | None required | **Gateway** — public endpoint; exposes `auth_register`, `auth_verify_email` & `auth_login` plus all authenticated tools (token passed per-call in header) |
| `POST /api/v2/mcp/rpc` | Bearer token | **RPC** — authenticated endpoint; all 31 workspace tools |

Use the **Gateway** if you want a single URL for everything (bootstrap + use).
Use the **RPC** endpoint if you already have a token.

---

## Install via ClawhHub

The easiest way to add FlowyTeam MCP is directly from [ClawhHub](https://clawhub.ai/agungksidik/flowyteam-mcp):

```bash
# Install from ClawhHub registry
clawhub install agungksidik/flowyteam-mcp
```

Or add manually using the steps below.

---

## Quick Start

### Option A — You already have an account & token

#### 1. Get your API Token

Log in to FlowyTeam → **Settings → MCP & AI Integration** → Copy your token.

#### 2. Connect with Claude Code (CLI)

```bash
claude mcp add flowyteam \
  --transport http \
  --url https://flowyteam.com/api/v2/mcp/rpc \
  --header "Authorization: Bearer YOUR_API_TOKEN"
```

#### 3. Or use Claude Desktop / Cursor

Add this to your `mcp.json`:

```json
{
  "mcpServers": {
    "flowyteam": {
      "transport": "http",
      "url": "https://flowyteam.com/api/v2/mcp/rpc",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

---

### Option B — Existing account, no token configured

**Recommended:** Log in to FlowyTeam via the web → **Settings → MCP & AI Integration** → generate and copy your API token, then use Option A above.

If you prefer to retrieve a token via the MCP Gateway instead:

#### 1. Connect to the Gateway without a token

```bash
claude mcp add flowyteam \
  --transport http \
  --url https://flowyteam.com/api/mcp/gateway
```

#### 2. Ask Claude to call `auth_login`

> ⚠️ **Security note:** Your password will be sent to the FlowyTeam API to obtain a token. Use this flow only on a private, trusted device. Avoid pasting credentials in shared chat sessions or CI environments.

```
"Call auth_login with my FlowyTeam email and password to get an API token"
```

Claude calls `auth_login` → returns `api_token`. Save it, then reconnect using Option A with that token and remove the gateway connection.

---

### Option C — New account via Gateway

If MCP registration is enabled on the platform, you can create an account directly from the CLI.

#### 1. Connect to the Gateway and register

> ⚠️ **Security note:** Your password will be sent to the FlowyTeam API during registration. Use a strong, unique password. Avoid running this in shared chat sessions or CI environments.

```
"Register a new FlowyTeam account — company Acme Corp, name Alice Smith, email alice@acme.com — I'll provide my password when prompted"
```

Claude calls `auth_register` → a verification email is sent to your address.

#### 2. Verify your email (choose one path)

**Path A — paste code to CLI (fastest):**
Open the verification email, copy the code from the link URL
(e.g. for `.../email-verification/ABC123XYZ` the code is `ABC123XYZ`), then tell Claude:

```
"Verify my email with code ABC123XYZ"
```

Claude calls `auth_verify_email` → returns `api_token` immediately.

**Path B — click link in browser:**
Click the verification link in the email to activate via the web, then tell Claude:

```
"Call auth_login with my FlowyTeam email and password to get an API token"
```

Claude calls `auth_login` → returns `api_token`.

#### 3. Reconnect with the token

```bash
claude mcp add flowyteam \
  --transport http \
  --url https://flowyteam.com/api/v2/mcp/rpc \
  --header "Authorization: Bearer YOUR_API_TOKEN"
```

#### 4. Reconnect with token for full workspace access

```
"Create a task 'Review Q2 Report' in Marketing project, assign to Sarah, due April 30"
"Show me all open high-priority tickets"
"Who is on leave this week?"
"What are our company OKRs for Q2 2026?"
"Log 8 hours on the Mobile App project for today"
"Create an invoice for Acme Corp, total $5,000, due May 31"
```

---

## Tools (34)

### Authentication Tools (public — no token required)

| # | Tool | Description | Methods |
|---|---|---|---|
| 1 | `auth_register` | Register a new company + admin user account. Sends a verification email — account is inactive until verified. Only available when the platform admin has enabled MCP registration. | POST |
| 2 | `auth_verify_email` | Activate a pending account using the code from the verification email link URL. Returns `api_token` on success. | POST |
| 3 | `auth_login` | Login with email + password (for existing or newly web-verified accounts). Returns `api_token` for use as Bearer token. | POST |

### Workspace Tools (require Bearer token)

| # | Tool | Description | Methods |
|---|---|---|---|
| 4 | `tasks` | Manage tasks and assignments | GET POST PUT DELETE |
| 5 | `projects` | Manage projects and workflow | GET POST PUT DELETE |
| 6 | `employees` | Manage employees and team members | GET POST PUT DELETE |
| 7 | `objectives` | Manage OKR objectives | GET POST PUT DELETE |
| 8 | `key-result` | Manage OKR key results | GET POST PUT DELETE |
| 9 | `indicators` | Manage KPIs and performance indicators | GET POST PUT DELETE |
| 10 | `indicator-record` | Log KPI actual values per period | GET POST DELETE |
| 11 | `leads` | Manage sales leads and prospects | GET POST PUT DELETE |
| 12 | `clients` | Manage clients and relationships | GET POST PUT DELETE |
| 13 | `tickets` | Manage support tickets | GET POST PUT DELETE |
| 14 | `attendance` | Clock in / clock out / attendance history | GET POST PUT |
| 15 | `leave` | Manage leave requests and approvals | GET POST PUT DELETE |
| 16 | `department` | Manage departments and teams | GET POST PUT DELETE |
| 17 | `designation` | Manage job designations | GET POST PUT DELETE |
| 18 | `performance-cycle` | Manage performance / OKR cycles | GET POST PUT DELETE |
| 19 | `holiday` | Manage company public holidays | GET POST PUT DELETE |
| 20 | `project-category` | Manage project categories | GET POST PUT DELETE |
| 21 | `task-category` | Manage task categories | GET POST PUT DELETE |
| 22 | `ticket-type` | Manage ticket types | GET POST PUT DELETE |
| 23 | `ticket-channel` | Manage ticket channels | GET POST PUT DELETE |
| 24 | `ticket-agent` | List ticket agents and groups | GET |
| 25 | `indicator-category` | Manage KPI categories | GET POST PUT DELETE |
| 26 | `leave-type` | Manage leave types (Annual, Sick, etc.) | GET POST PUT DELETE |
| 27 | `invoices` | Manage client invoices | GET POST PUT DELETE |
| 28 | `estimates` | Manage client estimates and quotes | GET POST PUT DELETE |
| 29 | `contracts` | Manage client contracts | GET POST PUT DELETE |
| 30 | `events` | Manage company calendar events | GET POST PUT DELETE |
| 31 | `expenses` | Manage expenses and claims | GET POST PUT DELETE |
| 32 | `expense-category` | Manage expense categories | GET POST PUT DELETE |
| 33 | `notices` | Manage company notice board | GET POST PUT DELETE |
| 34 | `timelogs` | Start/stop timers, log project hours | GET POST PUT DELETE |

---

## How It Works

This MCP uses **Streamable HTTP transport (JSON-RPC 2.0)**. Every workspace tool accepts a `method` parameter to select the operation:

| `method` | Operation |
|---|---|
| `GET` | Read / list records |
| `POST` | Create a new record |
| `PUT` | Update an existing record |
| `DELETE` | Delete a record |

Auth tools (`auth_register`, `auth_verify_email`, `auth_login`) only support `POST` and do not require a `method` field.

### Gateway vs RPC

```
Gateway  POST /api/mcp/gateway           ← single URL for everything
  ├── initialize / tools/list            ← no auth needed
  ├── auth_register                      ← no auth needed (creates account, sends verification email)
  ├── auth_verify_email                  ← no auth needed (activates account, returns api_token)
  ├── auth_login                         ← no auth needed (returns api_token)
  └── all workspace tools                ← reads Bearer token from header

RPC      POST /api/v2/mcp/rpc            ← authenticated only
  └── all workspace tools                ← requires Bearer token (middleware)
```

**MCP Protocol Version:** `2024-11-05`

---

## Smart Features

Several tools support **name-based resolution** — you don't need to look up IDs manually:

- `department` — lookup by `name` string (auto-finds the ID for PUT/DELETE)
- `invoices` — lookup by `invoice_number` (e.g. `INV#0001`)
- `estimates` — lookup by `estimate_number` (e.g. `EST#0003`)
- `contracts` — lookup by `subject` (partial match)
- `events` — lookup by `event_name` (partial match)
- `expenses` — lookup by `item_name` (partial match)
- `timelogs` — resolve `project_name` → ID, `task_name` → ID, `employee_name` → ID
- `timelogs` PUT — without `id`, finds the currently running timer automatically

---

## Permissions

| Role | Capabilities |
|---|---|
| **Admin** | Full read/write access to all tools |
| **Employee** | Read + self-service (own tasks, attendance, leave, expenses, time logs) |

Some modules (`invoices`, `estimates`, `contracts`, `events`, `expenses`, `notices`, `timelogs`) require the corresponding module to be enabled in your FlowyTeam plan.

---

## Security Best Practices

- **Use the lowest-privilege token for your use case.** If you only need to read tasks and log time, use an Employee token — not an Admin token.
- **Never share your API token** in public repositories, shared documents, or chat logs. Treat it like a password.
- **Prefer the API token flow (Option A)** over passing credentials through the agent (Options B/C). Tokens can be rotated; passwords cannot.
- **Rotate your token** via FlowyTeam Settings if you suspect it has been exposed.
- **Avoid using admin tokens in automated or CI/CD workflows** — create a dedicated service account with limited permissions instead.
- **Review and confirm destructive operations** (DELETE) before authorizing the agent to proceed.

---

## Security (Gateway)

The Gateway endpoint applies the following protections:

| Layer | Details |
|---|---|
| **Rate limiting** | 60 requests/minute per IP (throttle:60,1) |
| **Suspicious input check** | Blocks bot-like names and company names |
| **Duplicate email check** | Prevents duplicate account creation |
| **Email verification** | New accounts start as inactive — must be verified via `auth_verify_email` or web link before use |
| **SuperAdmin notification** | Every new MCP registration triggers an email to all SuperAdmins |
| **Platform toggle** | `allow_mcp_registration` must be enabled by SuperAdmin (default: off) |

---

## Full Documentation

- **ClawhHub listing:** [clawhub.ai/agungksidik/flowyteam-mcp](https://clawhub.ai/agungksidik/flowyteam-mcp)
- **MCP Server page:** [flowyteam.com/get/mcp-server](https://flowyteam.com/get/mcp-server)
- **API Reference:** [flowyteam.com/get/mcp-docs](https://flowyteam.com/get/mcp-docs)
- **Tool parameters:** See [SKILL.md](SKILL.md)

---

## Sign Up

Don't have a FlowyTeam account yet? [Sign up free](https://flowyteam.com/register) or use the MCP Gateway with `auth_register` + `auth_verify_email` if MCP registration is enabled by the platform admin.

---

## License

MIT — free to use, modify, and distribute.
