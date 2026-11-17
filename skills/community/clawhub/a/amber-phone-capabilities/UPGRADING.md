# Upgrading to v4.0

## What Changed

Version 4.0 introduces **AGENT.md** — all voice assistant prompts (personality, conversational rules, booking flow, greetings, etc.) are now stored in an editable markdown file instead of being hardcoded in TypeScript.

This means you can customize how Amber speaks, greets callers, handles bookings, and more — without touching any code.

## Is It a Breaking Change?

**No.** If you update the runtime without creating an `AGENT.md` file, everything works exactly as before. The runtime falls back to hardcoded prompts when `AGENT.md` is not found.

## Upgrade Steps

### 1. Update the runtime

Pull the latest code or update your ClawHub package:

```bash
git pull origin main
cd runtime && npm install && npm run build
```

### 2. (Optional) Adopt AGENT.md

Copy the included `AGENT.md` to start customizing:

```bash
# AGENT.md is already at the skill root — one level above runtime/
ls AGENT.md
```

Edit it to match your preferences. The runtime loads it automatically on startup.

### 3. Restart

```bash
npm start
# or restart your service/launchd/systemd
```

## AGENT.md Overview

The file uses `## Heading` sections that the runtime parses at startup. Template variables are auto-replaced:

| Variable | Source | Example |
|----------|--------|---------|
| `{{ASSISTANT_NAME}}` | `ASSISTANT_NAME` env var | Amber |
| `{{OPERATOR_NAME}}` | `OPERATOR_NAME` env var | Abe |
| `{{ORG_NAME}}` | `ORG_NAME` env var | Flixxaid |
| `{{DEFAULT_CALENDAR}}` | `DEFAULT_CALENDAR` env var | Abe |
| `{{CALENDAR_REF}}` | Derived from `DEFAULT_CALENDAR` | the Abe calendar |

### Sections

| Section | Controls |
|---------|----------|
| **Personality** | General assistant behavior |
| **Conversational Rules** | Pause-after-questions, breathing room |
| **Style: Friendly** | Tone for standard callers |
| **Style: GenZ** | Tone for GenZ-configured numbers |
| **Inbound Call Instructions** | Full inbound screening behavior |
| **Outbound Call Instructions** | Outbound call behavior |
| **Booking Flow** | Strict 9-step appointment booking process |
| **Inbound Greeting** / **Outbound Greeting** | Opening lines |
| **Silence Followup: Inbound** / **Outbound** | What to say after caller silence |
| **Witty Fillers** | Conversational fillers during tool calls |

### Custom Path

Set `AGENT_MD_PATH` in your `.env` to load from a different location:

```bash
AGENT_MD_PATH=/path/to/my/custom-agent.md
```

## No Changes Required To

- `.env` file — all existing env vars work as before
- Twilio webhook URLs
- Dashboard
- OpenClaw gateway configuration

## Questions?

Open an issue on [GitHub](https://github.com/batthis/amber-openclaw-voice-agent/issues).


### Authenticated local clients and caller-data boundaries

Sensitive bridge HTTP endpoints always require bearer authentication, even on loopback: a public tunnel can forward a remote request from a local peer. Existing `BRIDGE_API_TOKEN` settings continue to work. When absent, Amber generates a random installation credential in `runtime/data/bridge-api-token` (owner-only mode 0600). Bundled MCP and the dashboard's configured local bridge automatically share this file, including a token set in this installation's `runtime/.env`; the browser never receives the generated secret. Set `AMBER_BRIDGE_TOKEN_FILE` to an owner-only shared file for clients in another installation; relative paths resolve from `runtime/`. Custom HTTP clients must supply `Authorization: Bearer <token>`; remote clients need the operator to configure the same credential. Generated credentials must never be published or exposed by a tunnel. Back up/rotate them as secrets. On a read-only installation, provision a writable owner-only token path or set the existing environment token.

Dashboard automatic credentials are sent only to `AMBER_BRIDGE_URL` (default `http://127.0.0.1:8000`), not arbitrary loopback targets. If you use a different local bridge port, set that URL or provide its token in the existing dashboard field. Do not expose the unauthenticated local dashboard itself through a public tunnel; its same-origin checks are browser-CSRF defenses, not remote-user authentication.

Gateway consultations and skill requests use call-scoped session identifiers. Repeated lookups within a call retain their session, but one caller does not inherit another call's conversation. Persistent opt-in CRM behavior is unchanged. Caller transcripts, objectives, names and callback values are user-role JSON data, never higher-priority instructions or verified identity. All message fields stay inside that boundary while the operator still receives the readable call message. This reduces instruction-confusion risk; JSON and prompts do not guarantee model injection immunity or replace the gateway's own least-privilege permissions and approval policies. GPT-4o brain fallback is retained. Calendar operation errors keep diagnostic details only in local call logs, not caller responses.

### Optional local authority and persistence

Calendar lookup/create uses the operator-installed `ical-query` helper. Contact sync is an explicit local Apple Contacts export; it can invoke local macOS helpers. CRM reads/writes its opt-in local database. The optional `runtime/scripts/dist-watcher.cjs` maintenance watcher invokes `pgrep`, `ps`, and `launchctl` to restart a separately configured LaunchAgent after build changes; Amber does not install or enable that watcher automatically. These local binaries, environment settings, credential files, contact cache, logs and database are real authority/data accesses, not capabilities constrained by the skill metadata alone. Review source and host permissions before enabling integrations.


## Approved outbound objective correlation

SIP `x-objective` / `x_objective` headers are untrusted caller metadata and no longer set outbound instructions. A valid OpenAI event signature authenticates event delivery, not the caller-supplied objective. Amber resolves the objective, call plan and model from the previously approved local outbound intent using its bridge ID. Bundled Twilio SIP correlation already sends that ID and does not rely on objective headers. Normal inbound callers remain in the configured inbound flow and can still request the supported call-related assistance under its existing confirmation/privacy rules.

Custom direct-SIP integrations that previously supplied an objective only by header must use the authenticated outbound preview/confirmation flow with bridge-ID correlation. Missing or expired local intent does not authorize an outbound objective. No claim of general model prompt-injection immunity or live-provider validation is made.
