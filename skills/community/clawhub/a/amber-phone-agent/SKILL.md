---
name: amber-voice-assistant
title: "Amber — Give Your Agent Real Phone Capabilities"
description: "Give your agent a phone number. Amber answers calls, places confirmed outbound calls, completes phone tasks, logs transcripts, and exposes MCP tools."
homepage: https://github.com/batthis/amber-openclaw-voice-agent
metadata: {"openclaw":{"emoji":"☎️","requires":{"env":[],"optionalEnv":["AMBER_ENABLE_OUTBOUND_CALLS","AMBER_REALTIME_MODEL","AMBER_REALTIME_VAD_THRESHOLD","AMBER_REALTIME_VAD_PREFIX_PADDING_MS","AMBER_REALTIME_VAD_SILENCE_DURATION_MS","AMBER_CRM_ENABLED","AMBER_CRM_TRANSCRIPT_ENRICHMENT","OPENCLAW_GATEWAY_URL","TWILIO_WEBHOOK_STRICT","VOICE_PROVIDER","VOICE_WEBHOOK_SECRET","ASSISTANT_NAME","OPERATOR_NAME","AMBER_CRM_DB_PATH","AGENT_MD_PATH","DEFAULT_CALENDAR","AMBER_CONTACTS_EXTENDED"],"anyBins":["node","ical-query"]},"permissions":{"network":true,"env":true,"webhooks":true,"localFiles":["runtime/logs/","runtime/contacts-cache.json","~/.config/amber/crm.sqlite"],"localBinaries":["node","ical-query"],"mcpTools":["make_call","get_call_status","get_call_history","crm","contacts_lookup","calendar_query","start_screening","stop_screening","bridge_health"],"externalServices":["Twilio or compatible voice provider","OpenAI Realtime/API","optional OpenClaw Gateway"]},"install":[{"id":"runtime","kind":"node","cwd":"runtime","label":"Install Amber runtime (cd runtime && npm ci && npm run build)"},{"id":"crm-skill","kind":"node","cwd":"amber-skills/crm","label":"Install optional CRM skill dependencies (cd amber-skills/crm && npm ci)"}]}}
---

# Amber — Give Your Agent Real Phone Capabilities

## Overview

**Screen incoming calls, call a business, book an appointment, or take a message—all through your agent.** Amber connects a real phone number to your agent with a Twilio + OpenAI Realtime bridge (`runtime/`), confirmed outbound calling, transcripts, and MCP tools.

Use it when you want an agent to do the plain-English phone job: call this business, ask this question, book the slot, leave the message, screen this caller, or show me what happened. Amber is built for operators who want the phone capability layer under their own Twilio or compatible voice account, with local logs, a local dashboard, and confirmation gates before outbound calls or calendar writes.

## Capability and data scope

Beyond phone calls, configured MCP clients can query availability and create calendar events through `ical-query`, and independently use optional CRM contact creation, updates, history, and interaction logging. Calendar writes require explicit confirmation. Contact lookup uses an operator-generated local Apple Contacts cache; the sync helper exports contact names/numbers, with optional extended notes, relationships, and addresses only when `AMBER_CONTACTS_EXTENDED=true`. CRM and transcript enrichment remain separately opt-in. Review local cache, database and transcript retention before use.

Maintainer documentation includes optional ClawHub publishing and demo-recording upload commands. Those commands are manual release/demo workflows, not actions performed at runtime or during installation.

## Security upgrade notes

- OpenAI webhooks now require valid `webhook-id`, `webhook-timestamp`, and `webhook-signature` headers, signing `id.timestamp.rawBody` with the configured webhook secret. Missing/invalid signatures and timestamps outside five minutes are rejected; the old unsigned-development override is no longer supported.
- Every outbound bridge request now requires a preview from `/call/preview`, followed by the exact same number, objective, model and optional call plan with `confirmed=true` and its single-use `approvalToken` within five minutes. The MCP `make_call` tool and dashboard use this flow. Direct integrations must migrate. A token proves a matching preview occurred; it cannot prove human consent. Clients must obtain explicit operator approval and must not autonomously approve previews.
- The dashboard accepts state-changing requests only as JSON from its exact same origin. Open it on its own configured loopback URL, not another site's embedded view. The bridge rejects direct browser-origin requests; use the dashboard proxy or authenticated non-browser integration.
- Caller-derived CRM names/context are passed only as bounded, untrusted user-message data, never inserted into higher-priority greeting instructions or treated as verified identity.

## Try asking your agent

- “Screen my incoming calls and take a message with a callback number.”
- “Prepare a call to the restaurant to ask about a table for four at 7 p.m.; show me the details before dialing.”
- “Check my availability for Friday afternoon and help the caller confirm an appointment.”

## What you need

- **A phone number and voice-provider account** — Twilio is the default and recommended provider.
- **OpenAI API access** — the voice runtime uses OpenAI Realtime.
- **A running host with Node.js and a reachable webhook endpoint** — plus OpenClaw or a configured MCP client for your chosen workflows. Local calendar integration uses `ical-query`.
- **Usage budget** — voice-provider number/call charges and OpenAI API usage are separate; installing the skill does not include those services. The dashboard shows estimated call costs.

Amber is a sensitive communications system. It can process call audio/transcripts through configured voice and AI providers, store local call logs, maintain a local CRM, read/write the operator calendar, expose local MCP tools, and optionally use an Apple Contacts export for name-to-number resolution. Operators should configure caller notice/consent, retention/deletion practices, and least-privilege provider credentials before production use.

Privacy defaults: local CRM lookup/logging is disabled unless `AMBER_CRM_ENABLED=true`, and post-call transcript enrichment is disabled unless `AMBER_CRM_TRANSCRIPT_ENRICHMENT=true`. Enable those only after setting caller notice/consent and retention/deletion practices.

**You stay in control:** prepare calls before dialing, review call history afterward, and enable optional caller memory only when you want it.

**✨ v5.4.0:** Amber ships as an **MCP plugin** with 9 tools — prepare confirmed calls by name, check call history, query CRM contacts, manage calendar, and control call screening. It works with Claude Desktop/Cowork and other MCP-capable clients or agent harnesses once configured. Includes Apple Contacts integration and a code-enforced call confirmation safeguard to prevent wrong-number dials.

**✨ Also:** Interactive setup wizard (`npm run setup`) validates credentials in real-time and generates a working `.env` file — no manual configuration needed. Once setup is complete, Amber is prompt-based: ask your OpenClaw agent to prepare confirmed calls, answer/screen callers, schedule confirmed appointments, or handle phone workflows in natural language.

## Setup walkthrough

![Setup Wizard Demo](demo/demo.gif)

**[▶️ Watch the interactive demo on asciinema.org](https://asciinema.org/a/l1nOHktunybwAheQ)** (copyable text, adjustable speed)

*The interactive wizard validates credentials, detects ngrok, and generates a complete `.env` file in minutes.*

### What's included

- **Phone number + runtime bridge** (`runtime/`) — a complete Node.js server that connects a Twilio or compatible phone number to OpenAI Realtime with OpenClaw brain-in-the-loop
- **Amber Skills** (`amber-skills/`) — modular mid-call capabilities (CRM, calendar, log & forward message) with a spec for building your own
- **Built-in CRM** — local SQLite contact database; Amber can greet callers by name and use operator-approved context naturally on calls, with operator review/correction responsibility
- **Call log dashboard** (`dashboard/`) — browse call history, transcripts, captured messages, estimated costs, and one-touch localhost test calls with regular/mini Realtime model selection
- **Setup & validation scripts** — preflight checks, env templates, quickstart runner
- **Architecture docs & troubleshooting** — call flow diagrams, common failure runbooks
- **Safety guardrails** — outbound calls require code-enforced confirmation; payment escalation, consent boundaries, and explicit confirmation for calendar writes are documented

## 🔌 Amber Skills — Extensible by Design

Amber ships with a growing library of **Amber Skills** — modular capabilities that plug directly into live voice conversations. Each skill exposes a structured function that Amber can call mid-call, letting you compose powerful voice workflows without touching the bridge code.

### 👤 CRM — Contact Memory *(v5.3.0)*

Amber can maintain operator-reviewed caller memory across calls, limited to relevant follow-up context under the operator's notice, consent, and retention policy.

- **Opt-in runtime management** — set `AMBER_CRM_ENABLED=true` to enable automatic known-caller lookup and interaction logging
- **Personalized greeting** — known callers can be greeted by name; optional notes are used only when relevant to the call objective
- **Optional enrichment** — set `AMBER_CRM_TRANSCRIPT_ENRICHMENT=true` to allow post-call extraction to propose caller details and notes for the local CRM
- **Operator review expected** — review, correct, or delete CRM records periodically so bad transcript extraction, misleading caller input, or overly sensitive details do not persist indefinitely
- **Symmetric** — works identically for inbound and outbound calls
- **Local SQLite CRM** — contact memory is stored at `~/.config/amber/crm.sqlite`; CRM records are not cloud-hosted. Live call audio/transcripts still pass through Twilio/OpenAI as part of the phone bridge. Tell callers when calls are handled by an AI assistant and may be logged/used for follow-up, according to your local consent requirements.
- **Native dependency** — requires `better-sqlite3` (native build). macOS: `sudo xcodebuild -license accept` before `npm install`. Linux: `build-essential` + `python3`.

### 📅 Calendar

Query the operator's calendar for availability or schedule a new event — all during a live call.

- **Availability lookups** — free/busy slots for today, tomorrow, this week, or any specific date
- **Event creation** — create calendar events from a phone conversation only after the required details are collected and the caller explicitly confirms the slot
- **Privacy by default** — callers are only told whether the operator is free or busy; event titles, names, and locations are never disclosed
- Powered by `ical-query` — local-only, zero network latency

### 📬 Log & Forward Message

Let callers leave a message that is automatically saved and forwarded to the operator.

- Captures the caller's message, name, and optional callback number
- **Always saves to the call log first** (audit trail), then delivers via the operator's configured messaging channel
- Confirmation-gated — Amber confirms with the caller before sending
- Delivery destination is operator-configured — callers cannot redirect messages

### Build Your Own Skills

Amber's skill system is designed to grow. Each skill is a self-contained directory with a `SKILL.md` (metadata + function schema) and a `handler.js`. You can:

- **Customize the included skills** to fit your own setup
- **Build new skills** for your use case — CRM lookups, inventory checks, custom notifications, anything callable mid-call
- **Share skills** with the OpenClaw community via [ClawHub](https://clawhub.com)

See [`amber-skills/`](amber-skills/) for examples and the full specification to get started.

**Contacts privacy:** Apple Contacts sync is opt-in. By default it exports only names and phone numbers needed for call-by-name. Set `AMBER_CONTACTS_EXTENDED=true` only if you explicitly want extra local-only fields such as email, organization, relationships, addresses, and notes in `runtime/contacts-cache.json`.

> **Note:** Each skill's `handler.js` is reviewed against its declared permissions. When building or installing third-party skills, review the handler source as you would any Node.js module.

### Call log dashboard

```bash
cd dashboard && node scripts/serve.js   # → http://localhost:8787
```

- **⬇ Sync button** (green) — immediately pulls new calls from `runtime/logs/` and refreshes the dashboard. Use this right after a call ends rather than waiting for the background watcher.
- **↻ Refresh button** (blue) — reloads existing data from disk without re-processing logs.
- **One-touch test calls** — when opened through `node scripts/serve.js`, the dashboard can call a test number through the local Amber bridge and choose `gpt-realtime` or `gpt-realtime-mini` per call.
- **Cost visibility** — estimates telephony and Realtime token cost from call duration and saved usage metadata; rates are editable in the dashboard.
- Background watcher (`node scripts/watch.js`) auto-syncs every 30 seconds when running.

## Why Amber

- **Ship a voice assistant in minutes** — `npm install`, configure `.env`, `npm start`
- **Give an agent a real phone number** — callers can reach it, and it can place confirmed outbound calls for concrete phone tasks
- Full inbound screening: greeting, message-taking, appointment booking with calendar integration
- Outbound calls with structured call plans (reservations, inquiries, follow-ups), with confirmation gates and a runtime disable switch
- **OpenClaw gateway lookup (least-privilege)** — voice agent consults your OpenClaw gateway only for call-critical needs (availability checks, confirmed scheduling, required factual lookups), not for unrelated tasks
- Configurable speech detection and waiting acknowledgments to help reduce awkward pauses during lookups
- Fully configurable: assistant name, operator info, org name, calendar, screening style — all via env vars
- Operator safety guardrails for approvals/escalation/payment handling

## Personalization requirements

Before deploying, users must personalize:
- assistant name/voice and greeting text,
- own Twilio number and account credentials,
- own OpenAI project + webhook secret,
- own OpenClaw gateway/session endpoint,
- own call safety policy (approval, escalation, payment handling).

Do not reuse example values from another operator.

## 5-minute quickstart

### Option A: Interactive Setup Wizard (recommended) ✨

The easiest way to get started:

1. `cd runtime`
2. `npm run setup`
3. Follow the interactive prompts — the wizard will:
   - Validate your Twilio and OpenAI credentials in real-time
   - Auto-detect and configure ngrok if available
   - Ask whether to enable opt-in local CRM caller memory
   - Generate a working `.env` file
   - Optionally install dependencies and build the project
4. Configure your Twilio webhook (wizard shows you the exact URL)
5. Start the server: `npm start`
6. Call your Twilio number — your voice assistant answers!

**Benefits:**
- Real-time credential validation (catch errors before you start)
- No manual `.env` editing
- Automatic ngrok detection and setup
- Step-by-step guidance with helpful links

### Option B: Manual setup

1. From the Amber skill folder: `cd runtime && npm ci`
2. `cd ../amber-skills/crm && npm ci` if you plan to enable CRM caller memory.
3. `cd ../..` and copy `references/env.example` to `runtime/.env`, then fill in your values.
4. Set `AMBER_CRM_ENABLED=true` only if you want local caller memory/known-caller greetings.
5. `cd runtime && npm run build && npm start`
6. Point your Twilio voice webhook to `https://<your-domain>/twilio/inbound`
7. Call your Twilio number — your voice assistant answers!

### Option C: Validation-only (existing setup)

1. Copy `references/env.example` to your own `.env` and replace placeholders.
2. Export required variables (`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_CALLER_ID`, `OPENAI_API_KEY`, `OPENAI_PROJECT_ID`, `OPENAI_WEBHOOK_SECRET`, `PUBLIC_BASE_URL`).
3. Run quick setup:
   `scripts/setup_quickstart.sh`
4. If preflight passes, run one inbound and one outbound smoke test.
5. Only then move to production usage.

## Credential scope (recommended hardening)

Use least-privilege credentials for every provider:

- **Twilio:** use a dedicated subaccount for Amber and rotate auth tokens regularly.
- **OpenAI:** use a dedicated project API key for this runtime only; avoid reusing keys from unrelated apps.
- **OpenClaw Gateway token:** only set `OPENCLAW_GATEWAY_TOKEN` if you need brain-in-the-loop lookups; keep token scope minimal.
- **Dependency integrity:** runtime dependencies are pinned by `runtime/package-lock.json`; review dependency changes before publishing updates.
- **Secrets in logs:** never print full credentials in scripts, setup output, or call transcripts.
- **Setup wizard validation scope:** credential checks call only official Twilio/OpenAI API endpoints over HTTPS for auth verification; no arbitrary exfiltration endpoints are used.

These controls reduce blast radius if a host or config file is exposed.

## Safe defaults

- Outbound calling is enabled by default for the full phone-agent experience. Set `AMBER_ENABLE_OUTBOUND_CALLS=false` to disable the outbound call endpoint.
- Require explicit approval before outbound calls. **Note on confirmation enforcement:** The bridge enforces a matching, expiring, single-use preview token plus `confirmed=true` before dialing, including MCP and dashboard calls. This enforces the two-step protocol, not proof of human consent; the MCP client must still obtain explicit operator approval.
- If payment/deposit is requested, stop and escalate to the human operator.
- Keep greeting short and clear.
- Use timeout + graceful fallback when `ask_openclaw` is slow/unavailable.

## Workflow

1. **Confirm scope for V1**
   - Include only stable behavior: call flow, bridge behavior, fallback behavior, and setup steps.
   - Exclude machine-specific secrets and private paths.

2. **Document architecture + limits**
   - Read `references/architecture.md`.
   - Keep claims realistic (latency varies; memory lookups are best-effort).

3. **Run release checklist**
   - Read `references/release-checklist.md`.
   - Validate config placeholders, safety guardrails, and failure handling.

4. **Smoke-check runtime assumptions**
   - Run `scripts/validate_voice_env.sh` on the target host.
   - Fix missing env/config before publishing.

5. **Publish**
   - Publish to ClawHub (example):  
     `clawhub publish <skill-folder> --slug amber-voice-assistant --name "Amber Voice Assistant" --version 1.0.0 --tags latest --changelog "Initial public release"`
   - Optional: run your local skill validator/packager before publishing.

6. **Ship updates**
   - Publish new semver versions (`1.0.1`, `1.1.0`, `2.0.0`) with changelogs.
   - Keep `latest` on the recommended version.

## Troubleshooting (common)

- **"Missing env vars"** → re-check `.env` values and re-run `scripts/validate_voice_env.sh`.
- **"Call connects but assistant is silent"** → verify TTS model setting and provider auth.
- **"ask_openclaw timeout"** → verify gateway URL/token and increase timeout conservatively.
- **"CRM lookup fails after a Node upgrade"** → run `cd amber-skills/crm && npm rebuild better-sqlite3`, then restart the Amber runtime.
- **"Webhook unreachable"** → verify tunnel/domain and Twilio webhook target.

## Guardrails for public release

- Never publish secrets, tokens, phone numbers, webhook URLs with credentials, or personal data.
- Include explicit safety rules for outbound calls, payments, and escalation.
- Mark V1 as beta if conversational quality/latency tuning is ongoing.

## Install safety notes

- Amber does **not** execute arbitrary install-time scripts from this repository.
- Runtime install uses standard Node dependency installation in `runtime/`, with dependencies pinned in `runtime/package-lock.json`.
- CRM uses `better-sqlite3` (native module), which compiles locally on your machine.
- Review `runtime/package.json` dependencies before deployment in regulated environments.

## Resources

- **Runtime bridge:** `runtime/` (full source + README)
- Architecture and behavior notes: `references/architecture.md`
- Release gate: `references/release-checklist.md`
- Env template: `references/env.example`
- Quick setup runner: `scripts/setup_quickstart.sh`
- Env/config validator: `scripts/validate_voice_env.sh`


### Authenticated local clients and caller-data boundaries

Sensitive bridge HTTP endpoints always require bearer authentication, even on loopback: a public tunnel can forward a remote request from a local peer. Existing `BRIDGE_API_TOKEN` settings continue to work. When absent, Amber generates a random installation credential in `runtime/data/bridge-api-token` (owner-only mode 0600). Bundled MCP and the dashboard's configured local bridge automatically share this file, including a token set in this installation's `runtime/.env`; the browser never receives the generated secret. Set `AMBER_BRIDGE_TOKEN_FILE` to an owner-only shared file for clients in another installation; relative paths resolve from `runtime/`. Custom HTTP clients must supply `Authorization: Bearer <token>`; remote clients need the operator to configure the same credential. Generated credentials must never be published or exposed by a tunnel. Back up/rotate them as secrets. On a read-only installation, provision a writable owner-only token path or set the existing environment token.

Dashboard automatic credentials are sent only to `AMBER_BRIDGE_URL` (default `http://127.0.0.1:8000`), not arbitrary loopback targets. If you use a different local bridge port, set that URL or provide its token in the existing dashboard field. Do not expose the unauthenticated local dashboard itself through a public tunnel; its same-origin checks are browser-CSRF defenses, not remote-user authentication.

Gateway consultations and skill requests use call-scoped session identifiers. Repeated lookups within a call retain their session, but one caller does not inherit another call's conversation. Persistent opt-in CRM behavior is unchanged. Caller transcripts, objectives, names and callback values are user-role JSON data, never higher-priority instructions or verified identity. All message fields stay inside that boundary while the operator still receives the readable call message. This reduces instruction-confusion risk; JSON and prompts do not guarantee model injection immunity or replace the gateway's own least-privilege permissions and approval policies. GPT-4o brain fallback is retained. Calendar operation errors keep diagnostic details only in local call logs, not caller responses.

### Optional local authority and persistence

Calendar lookup/create uses the operator-installed `ical-query` helper. Contact sync is an explicit local Apple Contacts export; it can invoke local macOS helpers. CRM reads/writes its opt-in local database. The optional `runtime/scripts/dist-watcher.cjs` maintenance watcher invokes `pgrep`, `ps`, and `launchctl` to restart a separately configured LaunchAgent after build changes; Amber does not install or enable that watcher automatically. These local binaries, environment settings, credential files, contact cache, logs and database are real authority/data accesses, not capabilities constrained by the skill metadata alone. Review source and host permissions before enabling integrations.
