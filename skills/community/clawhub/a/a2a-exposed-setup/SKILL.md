---
name: a2a-exposed-setup
description: Use when deploying, redeploying, or configuring the a2a-exposed Cloudflare Worker, a wake webhook, polling, or a public façade for an agent that already speaks A2A, or creating a hosted agent on a2a.exposed. Not for reading or replying to messages (use a2a-exposed).
license: MIT
compatibility: Node 22.18+ for the CLI (npx -y a2a-exposed@latest, no global install). Without Node, connect https://a2a.exposed/mcp. Cloudflare account for self-hosted deploy.
metadata:
  version: "0.8.80"
  author: Telegraphic Developer
  homepage: https://github.com/telegraphic-dev/a2a-exposed
  hermes:
    tags:
      - a2a
      - agent2agent
      - cloudflare
      - workers
      - webhook
      - deploy
      - openclaw
      - hermes
    related_skills:
      - a2a-exposed
      - mise
      - cloudflare
  openclaw:
    emoji: "🛠️"
    envVars:
      A2A_CONFIG_DIR:
        description: Override the config directory (default ~/.config/a2a-exposed). Use one per bot on a shared machine.
        required: false
      A2A_BASE_URL:
        description: Public base URL of the deployed Worker (saved by init/deploy; usually not set by hand).
        required: false
      A2A_OWNER_TOKEN:
        description: Owner API token for inbox/reply/token commands (saved by init; usually not set by hand).
        required: false
        sensitive: true
      A2A_HOSTNAME:
        description: Custom hostname for the Worker (omit for workers.dev).
        required: false
      CF_PROFILE:
        description: Named cf auth profile (saved as CF_PROFILE in config.env).
        required: false
      CLOUDFLARE_ACCOUNT_ID:
        description: Cloudflare account id (saved by init when the login has exactly one account).
        required: false
      WAKE_WEBHOOK_URL:
        description: Wake webhook URL (Worker secret; put in the environment, never on the command line).
        required: false
        sensitive: true
      WAKE_WEBHOOK_KEY:
        description: Wake webhook bearer or API key (Worker secret).
        required: false
        sensitive: true
      WAKE_HMAC_SECRET:
        description: Wake HMAC secret for Hermes / signed presets (Worker secret).
        required: false
        sensitive: true
      WAKE_ACCESS_CLIENT_ID:
        description: Cloudflare Access service-token client id for a wake tunnel (set by tunnel create).
        required: false
        sensitive: true
      WAKE_ACCESS_CLIENT_SECRET:
        description: Cloudflare Access service-token client secret for a wake tunnel (set by tunnel create).
        required: false
        sensitive: true
      UPSTREAM_TOKEN:
        description: Proxy mode (--upstream) only. The one bearer credential the façade presents to the private A2A agent (Worker secret).
        required: false
        sensitive: true
      UPSTREAM_ACCESS_CLIENT_ID:
        description: Proxy mode only. Cloudflare Access service-token client id for the upstream's tunnel hostname (Worker secret).
        required: false
        sensitive: true
      UPSTREAM_ACCESS_CLIENT_SECRET:
        description: Proxy mode only. Cloudflare Access service-token client secret for the upstream's tunnel hostname (Worker secret).
        required: false
        sensitive: true
---

# a2a-exposed: setup

Gives this agent a public A2A endpoint: hosted on a2a.exposed, or a Cloudflare Worker in the human's account with D1 for its messages. The Worker wakes the agent through the outbound relay, a webhook, or a schedule. Day-to-day use is the **a2a-exposed** skill. Asked to connect to another agent first? See its [connect playbook](../a2a-exposed/references/connect.md); come back here only when the human says yes to exposing. Setup is create, receive, handle, notify the owner, and confirm with a real message the owner sees. A reachable card or HTTP 2xx is not done. Start with the [setup checklist](references/checklist.md) before sign-in or configuration.

Run every command as `npx -y a2a-exposed@latest <cmd>` (Node 22.18+; [references/prerequisites.md](references/prerequisites.md)). `@latest` deploys the current Worker template. Local option and missing-deployment errors precede Node guidance; valid deployments require Node 22.18+ before configuration writes or Cloudflare calls. Config is `~/.config/a2a-exposed/config.env` (chmod 600). A second bot uses its own `A2A_CONFIG_DIR`. For an offline self-hosted plan, use `init --dry-run [--json]` with the intended flags: no writes, network calls or stdin reads; secret names only. Login and resource readiness stay unverified. See [deploy](references/deploy.md).

**Choose the setup path before checking local prerequisites.** Use the hosted CLI setup below when commands can run. If Node is missing and cannot be installed, the sandbox refuses the CLI, or there is no shell, offer [hosted MCP](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/mcp.md#hosted-connector) as the alternative; do not loop on `npx` or require Node installation to use it. The human adds `https://a2a.exposed/mcp` in their client's HTTP MCP settings and signs in with OAuth. Reuse an agent from `list_agents`, or get the human's chosen name and creation approval, then read `name_availability` and `creation_capacity` before `create_agent`. Continue with `agent_status`, `set_wake` and `test_wake` through the connector; wake secrets and confirmation stay with the human in the browser. When the client's setup shell is available, print these exact add lines (a session with no shell uses the client settings instead):

- Claude: `claude mcp add --transport http a2a-exposed https://a2a.exposed/mcp`, then `/mcp` to sign in.
- Codex: `codex mcp add a2a-exposed --url https://a2a.exposed/mcp`, then `codex mcp login a2a-exposed`. These are configuration instructions, not proof of an end-to-end client exchange.

**Offer hosted first when the human has no Cloudflare account or no preference.** For a Grok Bot, the default is the a2a-exposed-setup skill plus the CLI hosted login: list `hosted capabilities --json`, approve explicit scopes with `login --machine NAME --scopes SCOPES --json`, then `hosted create --name NAME --json` and `wake request --agent NAME --url URL --preset grok-bot --json`. Pass the routine's webhook URL yourself when you can see it; otherwise the human copies the URL once from the routine panel. The command sends no key and prints a `confirm_url`: tell the human to copy only the webhook key from the routine, open that link signed in, paste the key and confirm. Never ask for the key in chat. The CLI stores the owner token in local `config.env` (keep the file chmod 600; never print it). The hosted MCP connector at `https://a2a.exposed/mcp` is the alternative when the CLI cannot run or the human prefers it (it is not in the Grok Bot plugin catalog; add it as a custom MCP server by that URL, then sign in or sign up). Self-host only if the human already has or asks for a Cloudflare account. [a2a.exposed](https://a2a.exposed/hosted) hosts the A2A endpoint and is open to everyone, in open beta with a Free plan ([pricing](https://a2a.exposed/pricing)). The human signs in at https://a2a.exposed/app and creates `https://<name>.a2a.exposed`; no Cloudflare account is needed. The dashboard shows the owner token once, and pairing requests are approved there with the a2a.exposed sign-in. Over MCP, `create_agent` on `https://a2a.exposed/mcp` does the same after the human agrees on the name and says yes. A Worker deployed with `init` is not listed in that dashboard. Details: [Getting started](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/getting-started.md#hosted-inbox).

**Hosted CLI setup:** first list `hosted capabilities --json`. `unsupported` (including discovery HTTP 404) means scoped setup is unavailable at that origin: check `--control-url`, then use the dashboard or hosted MCP `create_agent`/`set_wake` with human confirmation and secret entry. Login stops before approval and keeps credentials unchanged; do not repeat the failing discovery command. Continue only when the service advertises setup scopes and wake presets; otherwise offer dashboard Wake settings or hosted MCP `set_wake`, with human secret entry. Do not run `init` or `deploy` for a hosted address. When setup is advertised, approve explicit scopes with `login --machine NAME --scopes SCOPES --json`, then `hosted list --json` and `hosted create --name NAME --json`. Credentials stay in protected local config. Compare the machine label and scopes printed beside the approval code. `hosted list` contains hosted agents; direct wake commands use a matching saved owner token even after setup access ends. Use [scoped hosted setup](references/wake.md#scoped-hosted-cli-setup) for wake secrets and CLI/MCP references; manual dashboard transfer is the fallback. For an existing hosted-only config, `wake preview|test|set --json` uses its `A2A_BASE_URL` and matching `A2A_OWNER_TOKEN` without `--agent` or a setup grant. Read presets with `hosted capabilities --json`; supply `WAKE_WEBHOOK_URL` and credentials from protected environment secrets, files or stdin. `wake set` tests then saves through the hosted API; `wake test` tests without saving. No local deployment is created. Unsupported API or refused access points to dashboard Wake settings or hosted MCP `set_wake`. Scoped hosted writes without an owner token require an explicit `--agent NAME` selected from `hosted list --json`. **Hosted Tunnel recovery:** read `hosted capabilities --json` for `verified_import` and select the agent with `hosted list --json`. If hosted `wake test` or `wake set` refuses with `cloudflare-target-unsupported` and returns a validated selected-agent `recovery_url`, ask the human to open **Import or manage your existing tunnel** there, connect Cloudflare, check the exact route and confirm the Access service-token secret rotation. The old secret stops working. Only after that confirmation, send one authenticated test wake and save. Failed tests preserve saved settings; the CLI does not import or retry automatically. Without recovery, offer a supported public HTTPS route, polling or an explicitly authorized self-hosted Worker. Keep Access and webhook authentication enabled. See [refusal recovery](references/troubleshooting.md#internal-secure-link-refusal-recovery).

**Cloudflare consent comes before changes.** A login is not consent. Before `init`, `deploy`, `tunnel create`, façade tunnel/Access steps, `uninstall`, or any other account change, identify the account name/id from `npx cf auth whoami`, explain the concrete resources and secrets being created, changed, or removed, and wait for the human's explicit yes. Name the Worker, D1 database, hostname (including account-level workers.dev registration or custom-domain DNS), and owner/wake secrets by purpose, never value. Include tunnel/Access objects when relevant; follow the [consent checklist](references/deploy.md#before-cloudflare-changes). No silent creation.

Never paste secrets into chat or onto the command line. When the host is local-only or has no public address, offer the outbound relay first. `hosted capabilities --json` with `relay: true`, or `relay status --json` with protocolVersion 1, means it is available. `enrolled: false` only means no connector yet. HTTP 404 means it is off. A tunnel fits a self-hosted inbox with a zone. Polling fits a missing relay, no local webhook, or a declined foreground `relay run`. Hosted services advertising `relay: true` support `relay wake status|test|save|remove` with protected files, explicit versions/generations and single-use receipts; save needs `--confirm`. See the [setup checklist](references/checklist.md) and [relay setup](references/wake.md#optional-relay). A 404 is unsupported, not permission to change a hosted runtime; enrollment/rotation/revocation and service installs need human approval. Ask the user before anything billable, and before changing DNS on a zone that already serves something. The A2A endpoint URL is the deployment's public base URL. A webhook URL goes only in `WAKE_WEBHOOK_URL`. Check the endpoint with `status`, not curl. A private A2A card goes to [references/deploy.md](references/deploy.md).

`status` is read-only, prints eight layers as `PASS`, `FAIL`, or `SKIP`, and ends with `next step:`. A local-webhook 401 or 403 fails that layer only when the response shows Cloudflare Access; the webhook's own auth refusal reports the HTTP status and passes. Hosted saved settings and local hook checks do not prove hosted delivery: follow [hosted checks and recovery](references/wake.md#human-handoffs) before changing credentials or provisioning a tunnel. Clients are in the [compatibility table](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/getting-started.md#clients). Runtime/config: `init` saves the Node path and suggests a pinned wake command when PATH differs. Default hints/next commands retain non-default `--config-dir`; explicit/saved commands are preserved. `env [--json]` prints the config directory; `status --json` includes `runtime.node` / `runtime.execPath`. Pin scheduled jobs with mise: [prerequisites](references/prerequisites.md).

## Workflow
Human handoffs: [delivery preflight](references/wake.md#human-handoffs). **ACP stdio/session relay:** Follow [ACP setup](references/acp.md), require explicit owner `--acp-mode MODE` before every prompt, and keep optional `--acp-diagnostics-file NEWFILE` raw stderr private; use owner-selected `--acp-session ID --acp-session-peer NAME` when possible, never a peer-selected local session. **Ordinary webhook or existing native A2A service:** Only offer this path to callers able to set its dedicated ingress-secret header; native discovery is invited access, not URL-only public discovery. Confirm the owner-approved local service and who may hold that transport-access secret. HTTP create/status/revoke always print JSON; run is silent/foreground-only and needs a compatible Worker. Before enrollment, enabled:false/empty capabilities with protocolVersion 2 is normal; distinguish definite config/rejection cleanup from uncertain enrollment, and never auto-rotate. Retire old files only after an approved replacement is verified. The separate opt-in [HTTP/native A2A relay](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/http-relay.md) offers fixed-loopback forwarding, bounded-buffered finite responses and incremental unencoded native SSE, not wake-template delivery. Use a compatible CLI/Worker and `relay http|a2a status --json` before offering setup; a missing capability is not permission to deploy a hosted runtime. Self-host activation is `deploy --http-relay 1` only after Cloudflare consent. Enrollment reserves distinct mode-600 connector and ingress files. Explicitly allow the receiver's original application auth headers; native service per-peer/task authorization stays at that service, not the shared ingress gate. Public discovery needs the ingress header as well. Preserve the existing Tunnel façade as a separate JSON-only option. This does not activate hosted UI support or replace its release/pin/approval gates.

1. **Choose hosting and delivery with the human before any change.** Read the [setup checklist](references/checklist.md) first: create, receive, handle, notify, then a real message the owner sees. A reachable card or HTTP 2xx is not done. Ask both hosted vs self-hosted and webhook vs polling before creating a handler, routine or polling job. When the host is local-only or has no public address, offer the outbound relay before a tunnel or polling if `hosted capabilities --json` reports `relay: true` or `relay status --json` reports protocolVersion 1. Recommend webhook for OpenClaw and Hermes when a public HTTPS route is available. For Hermes, OpenClaw and other local-only webhooks, also present tunnel + webhook and polling with short pros/cons when the relay is off or declined. Let the human choose. For a self-hosted endpoint with a zone on the selected Cloudflare account, recommend tunnel + webhook with a slow cron fallback; without a zone, or when the human declines DNS/tunnel changes, recommend polling and explain why. A workers.dev inbox can use a separate wake tunnel hostname. Do not label polling Recommended merely to avoid DNS consent. First read the [delivery preflight and command compatibility](references/wake.md#delivery-preflight); check hook support, public HTTPS reachability and the hosted service’s ability to deliver to the chosen route. Explain human authorization and polling interval/cost, then let the human choose. Do not silently configure polling. **Hosting:** Offer hosted first without a Cloudflare account or a preference. For hosted creation, agree on the name and get an explicit yes. For self-hosting, inspect the selected login/account, explain the plan, and wait for an explicit yes before changing Cloudflare resources; finding a login never authorizes deployment. For Cloudflare errors, see [references/troubleshooting.md](references/troubleshooting.md).
2. **Prerequisites** — [references/prerequisites.md](references/prerequisites.md).
3. **Hosted setup or deploy** — For hosted use the scoped CLI flow above; an advertised preset does not prove receiver reachability. OpenClaw follows the [hosting-aware checklist](references/wake.md#openclaw-openclaw-wake-or-openclaw-agent) before hook or tunnel changes. For self-hosting use [references/deploy.md](references/deploy.md), including the loopback test and a private A2A agent.
4. **Owner token** — Self-hosted `init` and scoped `hosted create` store it in protected `config.env`. For manual hosted creation, the human transfers the once-shown dashboard token directly into the routine's secret store with `A2A_BASE_URL`; see the [Grok hosted checklist](references/wake.md#grok-bot-grok-bot). An inbox owner token does not create hosted addresses. For self-hosting, rotate with `npx -y a2a-exposed@latest init --rotate-owner-token` (it says to update `A2A_OWNER_TOKEN` and run `peers sync`). A hosted config refuses that flag: rotate in the dashboard (agent settings, Advanced) or with hosted MCP `rotate_owner_token`. Cloud routines get `A2A_BASE_URL` and `A2A_OWNER_TOKEN` as environment secrets, or use the MCP connector ([references/wake.md](references/wake.md)).
5. **Wake** — [references/wake.md](references/wake.md). Tunnel creation provisions resources only; it does not start cloudflared or install a persistent service. `status` separates connection counts from local `ephemeral`/unknown persistence. On macOS, service installation needs an admin password at a terminal; without admin access keep `cloudflared tunnel run --token-file <file>` running, or use a user LaunchAgent; the LaunchAgent option has not been tested. See [wake](references/wake.md). Ask the owner to choose **autonomous** (reply within authorized scope), **review-all** (draft and set `input-required` until approved), or **escalate** (reply within scope; ask about money, credentials or a new commitment). Save the chosen mode in the webhook handler and scheduled job prompts. Include a one-line owner notice after every handled wake, with no peer text or secrets; Hermes uses `--deliver origin`. Keep the webhook's fallback job at `every 6h`. The [Hermes recipe](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/hermes.md) uses the outbound relay for a local-only host (`relay create`, `relay run`, then `relay wake test` and `relay wake save --confirm` with `--hmac-secret-file`). A self-hosted inbox with a zone can use `tunnel create --preset hermes --hermes-route a2a-wake --hmac-secret-stdin`. `wake check --json` verifies unsigned rejection and signed delivery of a saved Hermes preset, without claiming handler execution. HTTP 2xx is not proof the handler ran.
6. **Pairing** — [references/pairing.md](references/pairing.md). Pairing is one-directional: an approved inbound peer can message you, and you reach them only with `connect <their-public-base-or-card-url>` after their owner approves. Do not approve that return request. `init` checks approval-password readiness; a missing password and pairing wakes point to `pair set-password --web`. Give the one-time setup link privately to the human; never open it or ask for their password. Password setup guidance appears only when password approval is enabled; OIDC-only endpoints omit it.
7. **Teardown** — [references/teardown.md](references/teardown.md).

For maintainer runs of the internal secure-link integration, use the
[refusal recovery reference](references/troubleshooting.md#internal-secure-link-refusal-recovery).
Pending-request limits require the owner to deny an earlier request or wait for
expiry; an unreadable access key requires owner removal and recreation of the
link. Wake failures emit `wake_result=<code>` on stderr and give a next step; saved wake settings remain unchanged. A delivered test without a confirmed save emits `wake_result=not-saved`: save in Wake settings on the website, then test again;
the connector token remains on disk and the CLI does not retry automatically. Unknown results display `unknown` without server text and call for a CLI update and feedback. Never repeat resource creation or remove resources automatically.
This integration is not a public setup option; its scope is defined in
[contributor verification](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/agents/verification.md#staging-hosted-link-refusal-contract).

## When something goes wrong
When a setup step fails, offer the human to report it: an `init` or `deploy` error, a `status` check that fails, a `wake test` that does not pass, a pairing failure, a step the docs get wrong, or a workaround you had to invent. Fix or work around the problem first, using [references/troubleshooting.md](references/troubleshooting.md), then offer the report.

- Feedback becomes a **public GitHub issue**. Never include tokens, secrets, private hostnames or URLs, message contents, or personal data. Redact the error output before it goes into `--actual` or `--logs`.
- Ask the human before sending. Show them the report and send it only after an explicit yes.
- Include the CLI and Worker versions, the deployment type (hosted or self-hosted), the connection (`webhook`, `proxy`, or `polling`), the step that failed, the redacted error, and what you tried.

Use one of these:

- **CLI:** `npx -y a2a-exposed@latest feedback "message"` with `--kind bug|idea|other`, `--steps`, `--expected`, `--actual`, `--logs`, `--agent`, `--environment`, `--connection`, and `--contact`. A bug needs `--steps`. The command adds the CLI version, the Worker version when the A2A endpoint reports it, the connection, and the deployment, names the target repository, and asks before sending. Pass `--yes` only after the human said yes; off a terminal posting requires it. When the A2A endpoint reports no feedback URL, for example before the first deploy, it prints `Not filed` and a link to a prefilled GitHub form instead of posting; `--json` includes `filed: false`.
- **MCP:** `send_feedback` on an approved connector takes the same fields.
- **Web:** the human can fill in https://a2a.exposed/app/feedback themselves.

A CLI report looks like this:

```bash
npx -y a2a-exposed@latest feedback "init fails on the D1 step" --kind bug \
  --steps "1. init --preset grok-bot  2. ..." --expected "..." --actual "<redacted error>" \
  --logs "<redacted output; what was tried>" --agent "<your agent>" --environment local --connection webhook
```

Details are in [Feedback](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/feedback.md).

MausBot uses `mausbot`, an HTTPS `/hooks/<endpointId>` URL and `WAKE_WEBHOOK_KEY` Bearer auth from protected storage. Follow the [MausBot checklist](references/wake.md#mausbot-mausbot): the human verifies/enables the first sample before testing again; desktop needs a `/hooks/*`-only tunnel. HTTP acceptance does not prove a bot run. OpenBot uses preset `openbot` and `WAKE_HMAC_SECRET`. Hosted wake prepare/test/set and relay wake test require explicit secret-source flags, such as `--hmac-secret-env WAKE_HMAC_SECRET`; ambient wake credentials are ignored. The human transfers the routine signing secret directly into protected environment/secret storage, never chat or argv. Follow the [OpenBot checklist](references/wake.md#openbot), including polling fallback and verification of an actual inbox-and-reply run; HTTP 202 proves acceptance only. The Worker refuses unsigned OpenBot wakes, and refuses `grok-bot`, `claude-code`, `openclaw-wake` and `openclaw-agent` without `WAKE_WEBHOOK_KEY` and `hermes` without `WAKE_HMAC_SECRET`; the reference explains signed timestamps, delivery-ID replay protection, and retry idempotency.
`hosted list --json` lists agent names; `status --agent NAME --json` reads selected hosted wake settings without testing delivery. Empty or malformed wake references need `wake prepare` with a new protected file; hosted failures exit 1. See [wake guidance](references/wake.md). Hosted `too_many_references` reports `retry_after` seconds and `next`; wait before another `wake prepare`. No automatic retry.
`status` compares the deployed Worker version with the CLI and cached npm latest, and recommends deploy when the Worker is older. Review the next step with the human before changing Cloudflare resources.
For staging `hosted link create|finish`, pass an explicit `--preset` selected from `hosted capabilities --json` before approval; `--json` returns structured results with exit 1 for any failure. Hostnames accept root HTTPS URLs, trailing dots and IDNs. See [troubleshooting](references/troubleshooting.md) for the result fields and validation reasons. For staging link expiry, repeat the same create/finish command before approval; after grant expiry, use `hosted link finish` for fresh approval. Saved connector tokens remain local; wake settings are not saved. See [troubleshooting](references/troubleshooting.md).
For hosted creation, check `hosted names --name NAME --json` before approval and `hosted capacity --json` with `agents:read` or creation access. MCP uses `name_availability` and `creation_capacity`. These checks reserve nothing; creation rechecks constraints. At the agent limit, follow the result's `next`: delete an unused hosted agent in the dashboard or with hosted MCP `delete_agent` (your human confirms it in the browser), or check plan limits; the CLI has no delete command. See the wake reference for the scoped workflow. When hosted capabilities advertises `wake_removal`, review `wake preview --agent NAME --json`, then use `wake remove --agent NAME --version N --json`. For MCP automation, `wake prepare --clear --version N --agent NAME --reference-file FILE --json` writes a protected single-use removal reference. Pass it only as MCP `set_wake secretReference` with `clear: true`; otherwise keep browser confirmation. Removal changes forwarding and still requires human authorization under the approval rules. Local encrypted stdio MCP: `a2a-exposed --config-dir DIR mcp` exposes `list_peers`, `send`, `inbox`, `history`, `outbound`, `poll_outbound` using local CLI pins/keys. Encryption stays off by default. Only after owner approval, set exact `A2A_SEALED_ENABLED=1` in each local CLI/MCP process and separately on each inbox Worker. Hosted production Workers have it on; self-hosted ones stay off until set. List peers before sending; read history and continue with send/contextId. OS consent needs startup `--allow-os-consent` and a human prompt. No plaintext fallback or automatic resend. See [local MCP](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/mcp.md#local-stdio-sendread). After human-approved ordinary pairing, the official A2A CLI can reuse its token through `credential get`; select the endpoint with `peers list --json` in the same `--config-dir`. Follow [the operate skill](../a2a-exposed/references/messaging.md#official-a2a-cli); stdout is sensitive and local encrypted configs are refused.
Encrypted pairings display a seven-emoji/name quick check (42 bits, weaker than the full code). Without commit-reveal an attacker generating keys repeatedly could match it. Compare every item in order through another trusted channel; mismatch means stop/deny. Use the full 60-digit code for high-stakes pairings and keys verify; emoji never grants independent verification or enables encryption. See docs/protocol.md for the derivation and fields. Committed-message feed setup is operator-only; see docs/message-events.md and obtain owner approval before configuring or rebinding it.
