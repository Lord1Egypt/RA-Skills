# Deploy

## Before Cloudflare changes

Confirm the human chooses self-hosting; offer the [hosted option](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/getting-started.md#hosted-inbox) first when they have no Cloudflare account or no preference. Before any account mutation, including `init`, `deploy`, `wake set`, `wake unset`, `tunnel create`, `tunnel rm`, façade tunnel/Access steps, and `uninstall`:

1. Run `npx cf auth whoami` with the selected profile (`--profile <name>` when used). Tell the human which account it shows (name and id) in your private chat with them; keep account ids out of issues, logs, and other public evidence. If it lists several accounts, have the human choose; if account identity is unavailable, resolve it before proceeding. Never print tokens.
2. Describe the concrete plan: Worker name (`--worker-name`, default `a2a-exposed`), D1 name (`--d1-name`, default the Worker name; create or reuse and apply migrations), and hostname. For workers.dev, name the Worker URL and any account-level subdomain registration; for a custom domain, name the hostname and DNS record Cloudflare creates. Name the owner token and any wake secrets to upload or change by purpose only, without values. For a redeploy, state what changes and which existing resources are reused.
3. For tunnels or the façade, also name the tunnel, hostname/DNS record, Access application, service token, any Zero Trust organization creation, and Worker secrets affected. For removal, list the resources and data being deleted; `uninstall --dry-run` previews the plan without deleting anything.
4. Ask whether the human agrees to that plan in that account and wait for an explicit yes. A saved login or a successful authentication is not consent. Ask again if the account or scope changes. Ask before anything billable and before DNS changes on a zone that already serves something.

`init` and `deploy` do not prompt, so the agent asks before it runs them.

## Deploy the Worker

The wake target can be configured later. If the user already has it, export the secrets first (see [wake](wake.md)). `init` never takes secrets as arguments.

```bash
export WAKE_WEBHOOK_URL='...'      # optional now
export WAKE_WEBHOOK_KEY='...'      # optional (bearer/API key)
export WAKE_HMAC_SECRET='...'      # optional (hermes / openbot / signed generic webhooks)
# omit --hostname to deploy to https://<worker-name>.<account-subdomain>.workers.dev
npx -y a2a-exposed@latest init \
  --hostname agent.example.com \
  --agent-name "My Agent" \
  --agent-description "What this agent does, for other agents" \
  --preset grok-bot                # grok-bot | claude-code | openclaw-wake | openclaw-agent | hermes | openbot | mausbot | generic
```

Preview with `init --dry-run` before deploying. It validates local options and prints the planned configuration and actions without writing files, reading stdin, installing packages, contacting Cloudflare or the upstream, generating tokens, or deploying. Add `--json` for structured output. Secret inputs are listed by name only; arbitrary metadata, URL, template and command settings are listed by key only. Saved settings and environment overrides still apply. Login, account visibility, resource existence and upstream authentication remain unverified until execution. List accounts with `npx cf accounts list --json`, select one with `--account-id ID` or `CLOUDFLARE_ACCOUNT_ID`, then rerun without `--dry-run`. For `--tunnel`, list `tunnel zones --json` before selecting a zone. The preview includes planned tunnel actions and does not create a tunnel. `--json` on `init` requires `--dry-run`.

`--skip-install` skips dependency installation when the Worker already has its dependencies.

`init` is non-interactive and idempotent. It:

1. Checks Node, then the Cloudflare login, and resolves the account, before it installs packages. Those login and account checks run outside the Worker directory, so they do not load `cloudflare.config.ts` before `npm install`. A fresh init runs `npx --yes cf auth whoami` for that check (`npx cf auth login` does not install a global `cf`). A later init uses `node_modules/.bin/cf`. With `--cf-profile`, an empty whoami account list is filled from `cf accounts list` on that same `cf`. If that list fails and no account id is set, init prints cf's error and stops. An id from `--account-id` or `CLOUDFLARE_ACCOUNT_ID` is used anyway. If the login can see several accounts, pass `--account-id`. An empty successful list says how many accounts are available. A failed login leaves the Worker packages uninstalled.
2. Copies the Worker template to `<config dir>/worker` and, after that login check, runs `npm install` there (this provides the local `cf`).
3. Creates the D1 database (`--d1-name`, default: the Worker name `a2a-exposed`), or reuses an existing one with that name, and applies migrations.
4. Generates the **owner token** and uploads it with any wake secrets via a temporary chmod-600 secrets file, which is deleted afterwards.
5. Deploys with the custom domain (or to workers.dev, redeploying once so the card advertises the learned URL), saves `A2A_BASE_URL` and `A2A_OWNER_TOKEN`, and checks the agent card. Right after a first deploy the workers.dev edge can answer Cloudflare error 1042 ("no Worker for this host") for up to ~30 s, sometimes after one good answer, so `init` waits until the card is served twice in a row and says when it is still propagating.

Optional flags:

| Flag | Purpose |
|---|---|
| `--agent-skills '<JSON array of A2A AgentSkill>'` | Skills advertised on the card |
| `--provider-organization`, `--provider-url` | Provider shown on the card |
| `--worker-name` | Worker name (also the default D1 name) |
| `--d1-name` | D1 database to create or reuse (default: worker name). Useful when several bots share an account |
| `--cli-command` | Command shown in wake hints (`hint` / summaries). Default `npx -y a2a-exposed@latest`, including `--config-dir DIR` for a non-default directory when no command is already saved. Explicit/saved commands are preserved. For a checkout, pass e.g. `node /path/to/repo/cli/bin/a2a-exposed.mjs`. Saved as `WAKE_CLI_COMMAND` |
| `--debounce <s>` | Wake debounce window |
| `--busy <s>` | Busy cool-down after a sent wake. `0` disables it. Unset uses the preset default (300 seconds for Claude Code, 180 for the others) |
| `--pairing-approval human\|agent\|off` | Who approves device-flow pairing requests ([pairing](pairing.md)). `human` (default): the owner, with the owner token (`pair approve`) or on the `/device` page with the approval password. `agent`: the agent runs `pair approve <code>` after asking its owner in chat, and the decision is recorded as the agent. `off`: no pairing endpoints; `token issue` only. Change it later with `deploy --pairing-approval ...` |
| `--max-per-hour <n>` | Hourly wake cap. `0` or unset is unlimited. Claude Code defaults to 25 when this is unset |
| `--cf-profile <name>` | Use a named cf auth profile (separate Cloudflare login). Saved as `CF_PROFILE` |
| `--workers-dev` | Move to workers.dev: clears the saved hostname, so the base URL, agent card and printed URLs become `https://<worker>.<subdomain>.workers.dev`. The old custom domain then answers 410 (its agent card redirects 301 to the new card) until you detach it in the dashboard; peers must update their URL. `--hostname <host>` on a workers.dev deployment moves it back (the workers.dev route is switched off). A wake tunnel keeps working (it has its own hostname on a zone) |
| `--workers-dev-subdomain <name>` | Register the account's workers.dev subdomain if it has none |
| `--pbkdf2-iterations <n>` | Cost of hashing the approval password, 50000 to 100000 (default 100000, the Workers maximum). Lower it only if approving on `/device` fails with Cloudflare error 1102 (CPU limit; see **Pairing security**), then set the password again |
| `--workers-logs on\|off` | Persisted Cloudflare Workers Logs (searchable in the dashboard under the Worker's **Logs**; query strings redacted). Off by default: only real-time logs (`npx cf workers tail`, if your cf version has it, or the dashboard's live view) |
| `--worker-dir <dir>` | Where the Worker project (template copy) lives. Default `<config dir>/worker`. The config directory is the global `--config-dir <dir>` (same as `A2A_CONFIG_DIR`) |
| `--cron` | Adds a one-minute cron flush. Needs a workers.dev subdomain on the account (works with workers.dev deployments); not required, because pending wakes are also flushed on every request |
| `--manage-url <url>` | https dashboard page, saved as `MANAGE_URL`. `none` clears it. A pairing wake, `pair list`, and `inbox` print it |
| `--event-url <url>` | https pairing-event URL, saved as `EVENT_URL`. `none` clears it |
| `--event-secret-stdin` | Read `EVENT_SECRET` from stdin and upload it on this deploy. The value stays out of `config.env` and out of the command output |

To redeploy later (after an upgrade or settings change), run `npx -y a2a-exposed@latest deploy`. Existing secrets persist.

Verify:

```bash
npx -y a2a-exposed@latest status     # agent card: OK: "<agent name>" (A2A 1.0, 0.3), then the next step
```

The card name should match `--agent-name`, and the versions should list 1.0 first, then 0.3. `status` fetches the card itself, so no `curl` is needed. A new workers.dev subdomain or custom domain can take a few minutes; if the card check fails, run `status` again. `status` names Cloudflare errors (1042 right after a deploy means the Worker is still propagating: retry in 30 s). `/.well-known/agent-card.json` is the A2A 1.0 card (with 0.3 interfaces listed); `/.well-known/agent.json` serves the same agent as an A2A 0.3-shaped card (`url`, `protocolVersion`, `preferredTransport`) for 0.3 clients.

### Loopback test

```bash
npx -y a2a-exposed@latest token issue self-test | npx -y a2a-exposed@latest peers add self "$(npx -y a2a-exposed@latest url)" --token-stdin
npx -y a2a-exposed@latest send --to self --text "loopback test"        # TASK_STATE_SUBMITTED (A2A 1.0)
npx -y a2a-exposed@latest inbox                                         # the task appears; a wake should fire
npx -y a2a-exposed@latest reply <taskId> --text "pong"
npx -y a2a-exposed@latest poll --to self <taskId>                       # TASK_STATE_COMPLETED, artifact "pong"
npx -y a2a-exposed@latest token revoke self-test && npx -y a2a-exposed@latest peers rm self
```

`send` and `poll` print the peer's task as returned and a one-line state summary on stderr. `peers rm self` also deletes the `PEER_SELF_TOKEN` it stored.

### Adopting an existing deployment (same Worker, D1 and hostname)

To keep an existing Worker, its D1 data, peer tokens, and wake secrets:

1. Back up the D1 database first (for example, export every table with `npx cf d1 query <db-id> --sql ...`, and note the time-travel bookmark from `npx cf d1 time-travel get-bookmark <db-id>`).
2. Write `config.env` yourself (chmod 600) with `CLOUDFLARE_ACCOUNT_ID`, `A2A_WORKER_NAME`, `A2A_D1_NAME`, `A2A_D1_ID`, `A2A_HOSTNAME` (a workers.dev Worker: leave it out and set `A2A_WORKERS_DEV_SUBDOMAIN`), `A2A_BASE_URL`, the **existing** owner token as `A2A_OWNER_TOKEN`, and the agent-card settings (`A2A_AGENT_NAME`, `A2A_AGENT_DESCRIPTION`, `A2A_AGENT_SKILLS`, ...). With `A2A_D1_ID` already saved, the saved hostname (or workers.dev) is not treated as a move.
3. Run `npx -y a2a-exposed@latest deploy --preset <preset>` with **no** `WAKE_*` (or `UPSTREAM_*`) variables exported. `deploy` (unlike `init`) uploads no secrets file when none are exported, so `OWNER_TOKEN` and the wake secrets already on the Worker are kept. It also applies the pending D1 migrations (`0002_wake_budget`, `0003_device_pairing`, `0004_pairing_replace`, `0005_facade_owners`) and prints `applied: ...`.
4. Run `npx -y a2a-exposed@latest status`. The agent card should show the existing name and base URL, and the wake mode should match the wake the Worker already had. Continue from its `next step:` line.
5. Peer tokens live in D1 as SHA-256 hashes, and lookups are by hash, so existing tokens keep working; nothing needs reissuing.
6. Device-flow pairing ([pairing](pairing.md)) is on after the deploy, with `human` approval: run `pair set-password --web` and send your human the one-time link (or they run `pair set-password` in a terminal). To keep tokens manual only, deploy with `--pairing-approval off`.

Migrations are tracked by file name, and `deploy` applies every file not yet recorded in `d1_migrations`, in numeric order, including a lower number added later. So an older `0001_init.sql` that is already recorded is not re-run. `0002_wake_budget.sql` adds the one table the earlier schema lacked (on newer databases it does nothing), `0003_device_pairing.sql` adds pairing, and `0004_pairing_replace.sql` adds one column for re-pairing (`connect --replace`). A database that already recorded `0003` under v0.2.0 still gets `0002` (and `0004`) on its next `deploy`.

### Already have A2A on a Tailnet or LAN: expose it through a public façade

Use this when the agent **already serves A2A JSON-RPC** (1.0 or 0.3) on a private address: a Tailnet name (`https://jean.tail1234.ts.net/a2a`), a LAN IP, or `localhost`. Don't fall back to the webhook A2A endpoint or polling, and never advertise the private card: its URLs are unreachable for everyone else, and they leak your network layout. Instead the Worker becomes a **public façade** (proxy mode, `--upstream`):

```
peer ──HTTPS + per-peer bearer──> https://agent.example.com            (Worker: rewritten card, device-flow pairing,
                                                                          token check, per-peer task isolation)
      ──Access service token + UPSTREAM_TOKEN──> https://agent-upstream.example.com/a2a   (Cloudflare Tunnel hostname,
                                                                                         Access admits only the Worker)
      ──cloudflared on the agent's machine──> http://127.0.0.1:8080/a2a  (or the Tailnet / LAN address)
```

A Worker can't reach a Tailnet or LAN address, so the upstream is published through a **named Cloudflare Tunnel** whose hostname is locked by a **Cloudflare Access** app that admits only one service token, held by the Worker (the same pattern as the wake tunnel). The CLI refuses a private `--upstream`.

1. **Tunnel + Access for the upstream**. Follow the consent checklist above and wait for an explicit yes: this creates DNS, a tunnel, and Access objects in the selected account. Needs Zero Trust (free) and a zone on the account. On the agent's machine:

   ```bash
   cloudflared tunnel login                       # once, picks the zone
   cloudflared tunnel create agent-upstream
   cloudflared tunnel route dns agent-upstream agent-upstream.example.com
   # ~/.cloudflared/config.yml
   #   tunnel: <tunnel id>
   #   credentials-file: ~/.cloudflared/<tunnel id>.json
   #   ingress:
   #     - hostname: agent-upstream.example.com
   #       service: http://127.0.0.1:8080          # the agent's A2A server (cloudflared inside the Tailnet can use its ts.net name)
   #       originRequest:
   #         access: { required: true, teamName: <team>, audTag: [<Access app AUD>] }
   #     - service: http_status:404
   cloudflared tunnel run agent-upstream
   ```

   In the Cloudflare dashboard, open the Access service tokens section and create a service token (copy the client id and secret once). Open the Access applications section and add a self-hosted app on `agent-upstream.example.com` with exactly **one policy: Service Auth** for that token (no email or everyone rules). Check that a bare `GET https://agent-upstream.example.com/.well-known/agent-card.json` is refused (401/403 or a redirect to `<team>.cloudflareaccess.com`).

2. **Deploy the façade** (new or existing deployment). Credentials come from the environment only, never argv:

   ```bash
   export UPSTREAM_ACCESS_CLIENT_ID='<service token client id>' UPSTREAM_ACCESS_CLIENT_SECRET='<secret>'
   export UPSTREAM_TOKEN='<bearer the agent expects>'     # the agent's own token (Hermes: the bearer its A2A server checks)
   npx -y a2a-exposed@latest init --hostname agent.example.com --upstream https://agent-upstream.example.com/a2a
   #   existing deployment: npx -y a2a-exposed@latest deploy --upstream https://agent-upstream.example.com/a2a
   #   card elsewhere:      --upstream-card-url https://agent-upstream.example.com/.well-known/agent-card.json  # same origin as --upstream (credentials ride with the fetch)
   #   back to the A2A endpoint:   deploy --upstream none
   npx -y a2a-exposed@latest status        # upstream card ok; Access credential and upstream bearer configured; upstream check OK; next step
   ```

   The two credentials do different jobs: the **Access service token** only gets the Worker through the tunnel; the **`UPSTREAM_TOKEN`** is what the agent itself checks. Setup reads the upstream's agent card and, unless it declares no bearer auth, needs `UPSTREAM_TOKEN`. Not exported? On a terminal it asks (hidden input); otherwise it exits 1 and says what to do. Other ways to pass it (never as an argument): `<command that prints it> | npx -y a2a-exposed@latest deploy --upstream-token-stdin`. An agent that really takes no bearer: `--no-upstream-token` (saved). Then check the whole path once: `npx -y a2a-exposed@latest upstream verify` (it creates no task; details in Troubleshooting).

3. **Pairing** is unchanged and stays on the façade: set the approval password ([pairing](pairing.md)), then peers run `connect https://agent.example.com`. A wake webhook is optional (it only announces pairing requests); messages go to the upstream, so `inbox` stays empty.

**Agent card rewrite (always on in proxy mode).** The façade fetches the upstream's card (cached 5 minutes, with the Access token and `UPSTREAM_TOKEN`; so `--upstream-card-url` must be on the `--upstream` origin, anything else is refused by `deploy` and by the Worker), and serves a rewritten copy at `/.well-known/agent-card.json` (A2A 1.0) and `/.well-known/agent.json` (0.3 shape):

- `supportedInterfaces`: one JSONRPC interface per version the upstream advertises (1.0 and/or 0.3), every one at `https://agent.example.com/`. Upstream interface URLs, gRPC / HTTP+JSON interfaces, `url`, `additionalInterfaces` and `preferredTransport` are never copied.
- `securitySchemes` / `securityRequirements`: the façade's (per-peer `bearer` + device-flow `pairing` with `/oauth/*` URLs on the façade). The upstream's own schemes describe the credential the façade holds, not what callers need.
- `capabilities`: `extensions` from the upstream; `streaming` and `extendedAgentCard` are `false` (not proxied yet), and `pushNotifications` is `false` (push configs are refused, see below).
- name, description, version, skills, default modes, provider, `documentationUrl`, `iconUrl`: `--agent-*` / `--provider-*` / `A2A_DOCUMENTATION_URL` settings win, then the upstream card, then defaults. Every string is scrubbed: a private or upstream URL (localhost, RFC 1918, 100.64/10, private IPv6 literals like `[::1]` / `[fd..]` / `[fe80..]` / IPv4-mapped, `*.ts.net`, `*.local`, single-label hosts, plain `http`, URLs that don't parse, the tunnel hostname) becomes `[private URL removed]`, a bare upstream or `*.ts.net` host name `[private host removed]`. `documentationUrl`, `iconUrl` and `provider.url` are dropped instead when private.
- The rewritten card omits signatures and unknown top-level fields.
- If the upstream card can't be fetched, the façade serves a card from the settings (1.0 and 0.3 interfaces, still only public URLs) and `status` says why.

The A2A endpoint card (no `--upstream`) uses the same scrubbing for `--agent-description`, `--agent-skills`, `--provider-url` and `A2A_DOCUMENTATION_URL`, so a pasted Tailnet link never reaches peers.

**Upstream credential model.** The façade holds **one** upstream identity (`UPSTREAM_TOKEN` + the Access service token) and calls the agent for every paired peer; the peer's own token never leaves the façade. The peer label goes upstream in `X-A2A-Peer` (trustworthy only because Access admits nothing but the Worker). Because peers share that identity, the façade keeps them apart itself: it records which peer created each task and context (D1 `facade_owners`), and refuses `GetTask` / `CancelTask` / push-config calls on another peer's task (also as a message's `taskId` or `referenceTaskIds`), or a message into a context the peer didn't get from the agent through the façade, before they reach the agent. That check fails closed: a client-chosen or otherwise unrecorded `contextId` is refused (the façade can't tell a new id from someone else's live context), so a peer starts a conversation without `contextId` and reuses the one returned. `ListTasks` is refused (it would list everyone's tasks), streaming returns `-32004`, and push notification configs are refused with `-32003`: the agent would call the peer's URL from inside your private network, where even a public-looking name (`127.0.0.1.nip.io`, split-horizon DNS) can resolve to a private address, so no check at the façade makes that safe. Peers poll `GetTask` instead. A relay through the Worker is a planned follow-up. An upstream 401/403 or a non-JSON answer becomes a generic `502` JSON-RPC error (`-32603`, naming no secret, lock or upstream host), never a 401 to the peer; the operator gets the reason from `status` / `upstream verify` and the Worker log line `upstream_error` (`reason`: see Troubleshooting).

**Threat model (proxy mode).** Two locks guard the upstream: Access (only the Worker's service token gets through the tunnel hostname) and `UPSTREAM_TOKEN` (the agent's own check; keep it on). Public callers need a per-peer token from pairing (human approval) or `token issue`, and `token revoke` cuts one off at the façade immediately. Unchanged caveats: whoever holds the owner token (the agent's `config.env`) can issue tokens and replace the approval password, so a compromised agent with the owner token can let anyone in; and whoever controls the Cloudflare account can read the Worker's secrets and call the agent as the façade. The owner API never returns the upstream secrets (fingerprints only). The façade passes task contents through verbatim: it does not rewrite URLs inside replies or artifacts, so the agent must not put private links in what it sends back.

**Pairing out while you build the façade.** A Tailnet agent can already connect to other A2A endpoints: `connect https://b.example.com --card-url https://jean.tail1234.ts.net/.well-known/agent-card.json`. A private https card is sent as informational, and the other owner's approval page and wake flag it as "not publicly reachable"; a non-https card is left out (as before). Replies reach you by polling (`poll`) until the façade is up.

## Optional settings

`APPROVAL_OIDC_*` turns on OpenID Connect approval on `/device` and the MCP consent page when the issuer, client id, client secret, and allowlist are all set. Unset, those pages stay on the password. `npx -y a2a-exposed@latest pair set-oidc` writes the non-secret settings. The client secret is `APPROVAL_OIDC_CLIENT_SECRET` in the environment (or `--secret-stdin`) and is uploaded on the next `deploy`, and is not stored in `config.env`. `A2A_BACKUP_BUCKET=1` adds a daily R2 snapshot of the A2A endpoint, kept 30 days. Leave it unset and the deploy has no backup bucket and no extra cron. `npx -y a2a-exposed@latest init --manage-url https://example.com/app/agents/name#pairing` saves `MANAGE_URL` (https, no user name or password; `none` clears it). A pairing wake, the MCP inbox line, `pair list`, and `inbox` include that page as `manageUrl`. `--event-url` saves `EVENT_URL` the same way. With `EVENT_SECRET` set, the A2A endpoint posts a signed pairing event when a request is created, approved, or denied. Pass `--event-secret-stdin` or export `EVENT_SECRET`. The secret is uploaded on that deploy, stays out of `config.env`, and stays out of the command output. Names are also listed in `worker/deploy.env.example`.

`status` reports the deployed Worker version and CLI version. An older Worker, including one whose `/health` has no `version`, produces a deploy next step and exit code 1. Unreachable health reports an unknown version. Cached npm latest can add an upgrade hint without a foreground registry request. Deploy sets the Worker version tag `a2a-exposed-<version>` and message `a2a-exposed <version> <ISO date>`.

Workers.dev registration uses the system `script` utility on macOS and Linux.
It can answer the known registration prompts when started by an agent without
an outer terminal. An unexpected prompt stops the terminal job after the idle
timeout; inspect the message before retrying rather than sending extra answers.

Worker dependency installs save npm output in `<config dir>/npm-install.log` (mode 600) and print that path only on failure. Inspect the log locally and redact secrets before sharing it.

## Hosted tenant-secret rotation

For a hosted deployment using `TENANT_SECRETS_KEY`, follow the
[control library rotation procedure](https://github.com/telegraphic-dev/a2a-exposed/blob/main/control/README.md#tenant-secret-key-rotation).
The binding accepts a raw secret for legacy writes or a bounded two-key JSON keyring for v2
writes. Roll out compatible readers first, retain both keys through migration, and alert on
`wake_secrets_unreadable`. Include outbound peer-token resync and delayed tenant config copies
in retirement checks. This changes Worker secrets and stored credentials: prepare the exact
plan and obtain the human's authorization before executing it. Never put key material in chat,
command arguments, committed files or logs.
