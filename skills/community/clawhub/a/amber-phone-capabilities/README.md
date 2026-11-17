# ☎️ Amber — Give Your Agent Real Phone Capabilities

**Screen incoming calls, call a business, book an appointment, or take a message—all through your agent.** Amber gives [OpenClaw](https://openclaw.ai) a real phone number, confirmed outbound calling, transcripts, and MCP tools. Twilio is the default and recommended voice provider; the voice runtime uses OpenAI Realtime. Configured MCP clients can also use Amber's phone, CRM, calendar, and call-history tools.

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

**Privacy notice:** Amber handles real communications data. Calls may be processed by Twilio or another voice provider and OpenAI Realtime, and local logs/transcripts are sensitive. CRM persistence is opt-in with `AMBER_CRM_ENABLED=true`; transcript-based CRM enrichment is separately opt-in with `AMBER_CRM_TRANSCRIPT_ENRICHMENT=true`. Configure caller notice/consent, access controls, retention, and deletion practices before using Amber with real callers.

[![ClawHub](https://img.shields.io/badge/ClawHub-amber--phone--agent-blue)](https://clawhub.ai/batthis/amber-phone-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What is Amber?

Amber is not just a standalone voice bot or virtual receptionist. It gives an agent a reachable phone number and the workflow tools to complete calls: call the business, ask the question, book the slot, leave the message, screen the caller, and show the transcript afterward. It operates as an extension of your OpenClaw instance while delegating complex decisions (calendar lookups, contact resolution, approval workflows) back to OpenClaw mid-call via the `ask_openclaw` tool.

### Features

- 🔉 **Inbound call screening** — greeting, message-taking, appointment booking
- 📞 **Outbound calls** — reservations, inquiries, follow-ups with structured call plans
- 🧠 **Brain-in-the-loop** — consults your OpenClaw gateway mid-call for calendar, contacts, preferences
- 👤 **Opt-in CRM** — maintains local, operator-reviewed caller records for relevant follow-up only when enabled; caller notice, consent, retention, and correction are operator responsibilities
- 📊 **Call log dashboard** — browse history, transcripts, captured messages, follow-up tracking, estimated costs, and one-touch localhost test calls
- ⚡ **Launch in minutes** — `npm install`, configure `.env`, `npm start`
- 🔒 **Safety guardrails** — outbound calls use operator approval/confirmation gates and can be disabled with `AMBER_ENABLE_OUTBOUND_CALLS=false`; payment escalation and consent boundaries included
- 🎛️ **Fully configurable** — assistant name, operator info, org name, voice, screening style
- 📝 **AGENT.md** — customize all prompts, greetings, booking flow, and personality in a single editable markdown file (no code changes needed)

## 🆕 What's New

### v5.5.50 — Sharper ClawHub Positioning (Aug 2026)

- Reframed the first-screen listing copy around the concrete outcome: give an agent a phone number and let it complete real phone tasks
- Moved inbound answering, confirmed outbound calling, booking, messages, transcripts, and MCP tools into the opening card language
- Kept the protected ClawHub display name unchanged: `Amber — Phone-Capable Voice Agent`

### v5.5.48 — Skill Card Evidence (Jul 2026)

- Bundled an explicit ClawHub skill card for release verification evidence

### v5.5.47 — CRM Off Means Off (Jul 2026)

- Hide the CRM skill from the voice runtime and MCP tool list unless `AMBER_CRM_ENABLED=true`
- Return a clear disabled message if an MCP client tries to call CRM while caller memory is off

### v5.5.46 — CRM Install Robustness (Jul 2026)

- Added setup wizard prompts for opt-in CRM caller memory and separate transcript enrichment consent
- Added ClawHub install metadata for optional CRM skill dependencies
- Added validation for CRM native SQLite dependency when caller memory is enabled
- Documented CRM dependency install/rebuild steps for fresh installs and Node upgrades

### v5.3.1 — Security Scope Hardening (Feb 2026)

Addressed scanner feedback around instruction scope and credential handling:

- Tightened `ask_openclaw` usage rules to **call-critical, least-privilege actions only**
- Clarified credential hygiene guidance (dedicated Twilio/OpenAI credentials, minimal gateway token scope)
- Added setup-wizard preflight warnings for native build requirements (`better-sqlite3`) to reduce insecure/failed installs

### v5.3.0 — CRM Skill (Feb 2026)

Amber includes optional local caller memory. Call metadata can be saved to a local SQLite database so known callers may be greeted by name, and a post-call extraction pass can propose contact notes for operator review. The database stays local, can be corrected or deleted by the operator, and should be treated as an operator-managed convenience feature rather than an authoritative record.

See [CRM skill docs](#-crm--contact-memory) below for details.

---

## Quick Start

The setup wizard asks whether to enable local CRM caller memory. It defaults to off; enable it only when you have caller notice/consent and retention practices in place.

```bash
cd runtime && npm ci
cd ../amber-skills/crm && npm ci  # optional, required for AMBER_CRM_ENABLED=true
cd ../../runtime
cp ../references/env.example .env  # fill in your values
npm run build && npm start
```

Point your Twilio voice webhook to `https://<your-domain>/twilio/inbound` — done!

> **Switching providers?** Set `VOICE_PROVIDER=telnyx` (or another supported provider) in your `.env` — no code changes needed. See [SKILL.md](SKILL.md) for details.

## ♻️ Runtime Management — Staying Current After Recompilation

**Important:** Amber's runtime loads `dist/` once at startup. If you recompile (e.g. after a `git pull` and `npm run build`), **restart the runtime** so the new build is used.

```bash
# macOS LaunchAgent (recommended)
launchctl kickstart -k gui/$(id -u)/com.jarvis.twilio-bridge

# or manual restart
kill $(pgrep -f 'dist/index.js') && sleep 2 && node dist/index.js
```

### Automatic Restart (Optional, for Persistent Deployments)

Amber includes an optional local `dist-watcher` helper for development deployments. If you intentionally enable it, it checks whether `dist/` is newer than the running process and restarts the runtime so development builds do not go stale.

Only enable this helper for intentional persistent deployments; otherwise run Amber manually with `npm start`.

To enable it, register the provided LaunchAgent:

```bash
cp runtime/scripts/com.jarvis.amber-dist-watcher.plist.example ~/Library/LaunchAgents/com.jarvis.amber-dist-watcher.plist
# Edit the plist to match your username/paths
launchctl load ~/Library/LaunchAgents/com.jarvis.amber-dist-watcher.plist
```

The watcher checks every 60 seconds and logs to `/tmp/amber-dist-watcher.log`.

> **Why this matters:** Skills and the router are loaded fresh at startup. A mismatch between a compiled `dist/skills/` and a hand-edited `handler.js` (or vice versa) will cause silent skill failures that are hard to diagnose. Always restart after any `npm run build`.

## 🔌 Amber Skills — Extensible by Design

Amber ships with a growing library of **Amber Skills** — modular capabilities that plug directly into live voice conversations. Each skill exposes a structured function that Amber can call mid-call, letting you compose powerful voice workflows without touching the bridge code.

Three skills are included out of the box:

### 👤 CRM — Contact Memory

Amber can maintain local caller memory across calls and use operator-approved context to make follow-up smoother without over-collecting personal details.

- **Known-caller lookup** — when local CRM is enabled, the runtime can check whether the caller already has an operator-reviewed contact record
- **Personalized greeting** — if the caller is known, Amber may use their name and relevant operator-approved context. Avoid surprising callers by surfacing sensitive or intimate notes without a clear reason.
- **Operator-reviewed notes** — after a call, an optional extraction pass can propose caller details and notes for the local contact record; operators should review, correct, or delete these records as needed
- **Operator review expected** — CRM entries should be reviewed, corrected, or deleted periodically so incorrect or overly sensitive details do not linger
- **Symmetric** — works identically for inbound and outbound calls; the number dialed on outbound is the CRM key
- **Local SQLite database** — stored at `~/.config/amber/crm.sqlite` (configurable via `AMBER_CRM_DB_PATH`); no cloud database dependency. CRM records stay on your machine. Note: voice audio and transcripts are processed by OpenAI Realtime (a cloud service) — see [OpenAI's privacy policy](https://openai.com/policies/privacy-policy).
- **Private number safe** — anonymous/blocked numbers are ignored without creating a record
- **Backfill-ready** — point the post-call extractor at old transcripts to prime the CRM from day one

> **Native dependency:** The CRM skill uses `better-sqlite3`, which requires native compilation. On macOS, run `sudo xcodebuild -license accept` before `npm install` if you haven't already accepted the Xcode license. On Linux, ensure `build-essential` and `python3` are installed.
> If CRM lookup starts failing after a Node.js upgrade, rebuild the native module with `cd amber-skills/crm && npm rebuild better-sqlite3`, then restart the Amber runtime.
>
> **Credential validation scope:** The setup wizard validates credentials only against official provider endpoints (Twilio API and OpenAI API) over HTTPS. It does not send secrets to arbitrary third-party services and does not print full secrets in console output.

### 📅 Calendar

Query the operator's calendar for availability or schedule a new event — all during a live call.

- **Availability lookups** — free/busy slots for today, tomorrow, this week, or any specific date
- **Event creation** — book appointments directly into the operator's calendar from a phone conversation, but only after explicit confirmation
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

> **Note:** Each skill's `handler.js` is reviewed against its declared permissions. When building or installing third-party skills, review the handler source as you would any Node.js module.

---

## What's Included

| Path | Description |
|------|-------------|
| `AGENT.md` | **Editable prompts & personality** — customize without touching code |
| `amber-skills/` | Built-in Amber Skills (calendar, log & forward message) + skill spec |
| `runtime/` | Production-ready voice bridge (Twilio default) + OpenAI Realtime SIP |
| `dashboard/` | Call log web UI with search, filtering, transcripts |
| `scripts/` | Setup quickstart and env validation |
| `references/` | Architecture docs, env template, release checklist |
| `UPGRADING.md` | Migration guide for major version upgrades |

## Call Log Dashboard

Browse call history, transcripts, and captured messages in a local web UI:

```bash
cd dashboard
node scripts/serve.js       # serves on http://localhost:8787
```

Then open [http://localhost:8787](http://localhost:8787) in your browser.

| Button | Action |
|--------|--------|
| **⬇ (green)** | **Sync** — pull new calls from bridge logs and refresh data |
| **↻ (blue)** | Reload existing data from disk (no re-processing) |

> **Tip:** Use the **⬇ Sync** button right after a call ends to immediately pull it into the dashboard without waiting for the background watcher.

The dashboard auto-updates every 30 seconds when the watcher is running (`node scripts/watch.js`).

## Customizing Amber (AGENT.md)

All voice prompts, conversational rules, booking flow, and greetings live in [`AGENT.md`](AGENT.md). Edit this file to change how Amber behaves — no TypeScript required.

Amber should be conversational and natural, but should not pretend to be a human being. If asked, it should identify itself plainly as an AI assistant.

Template variables like `{{OPERATOR_NAME}}` and `{{ASSISTANT_NAME}}` are auto-replaced from your `.env` at runtime. See [UPGRADING.md](UPGRADING.md) for full details.

## Documentation

Full documentation is in [SKILL.md](SKILL.md) — including setup guides, environment variables, troubleshooting, and the call log dashboard.

## Support & Contributing

- **Issues & feature requests:** [GitHub Issues](https://github.com/batthis/amber-openclaw-voice-agent/issues)
- **Pull requests welcome** — fork, make changes, submit a PR

## License

[MIT](LICENSE) — Copyright (c) 2026 Abe Batthish


### Authenticated local clients and caller-data boundaries

Sensitive bridge HTTP endpoints always require bearer authentication, even on loopback: a public tunnel can forward a remote request from a local peer. Existing `BRIDGE_API_TOKEN` settings continue to work. When absent, Amber generates a random installation credential in `runtime/data/bridge-api-token` (owner-only mode 0600). Bundled MCP and the dashboard's configured local bridge automatically share this file, including a token set in this installation's `runtime/.env`; the browser never receives the generated secret. Set `AMBER_BRIDGE_TOKEN_FILE` to an owner-only shared file for clients in another installation; relative paths resolve from `runtime/`. Custom HTTP clients must supply `Authorization: Bearer <token>`; remote clients need the operator to configure the same credential. Generated credentials must never be published or exposed by a tunnel. Back up/rotate them as secrets. On a read-only installation, provision a writable owner-only token path or set the existing environment token.

Dashboard automatic credentials are sent only to `AMBER_BRIDGE_URL` (default `http://127.0.0.1:8000`), not arbitrary loopback targets. If you use a different local bridge port, set that URL or provide its token in the existing dashboard field. Do not expose the unauthenticated local dashboard itself through a public tunnel; its same-origin checks are browser-CSRF defenses, not remote-user authentication.

Gateway consultations and skill requests use call-scoped session identifiers. Repeated lookups within a call retain their session, but one caller does not inherit another call's conversation. Persistent opt-in CRM behavior is unchanged. Caller transcripts, objectives, names and callback values are user-role JSON data, never higher-priority instructions or verified identity. All message fields stay inside that boundary while the operator still receives the readable call message. This reduces instruction-confusion risk; JSON and prompts do not guarantee model injection immunity or replace the gateway's own least-privilege permissions and approval policies. GPT-4o brain fallback is retained. Calendar operation errors keep diagnostic details only in local call logs, not caller responses.

### Optional local authority and persistence

Calendar lookup/create uses the operator-installed `ical-query` helper. Contact sync is an explicit local Apple Contacts export; it can invoke local macOS helpers. CRM reads/writes its opt-in local database. The optional `runtime/scripts/dist-watcher.cjs` maintenance watcher invokes `pgrep`, `ps`, and `launchctl` to restart a separately configured LaunchAgent after build changes; Amber does not install or enable that watcher automatically. These local binaries, environment settings, credential files, contact cache, logs and database are real authority/data accesses, not capabilities constrained by the skill metadata alone. Review source and host permissions before enabling integrations.
