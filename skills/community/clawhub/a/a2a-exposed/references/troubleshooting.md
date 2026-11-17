# Troubleshooting the A2A endpoint

One present-tense action per symptom. Cloudflare login, error 1042, and the hosted A2A endpoint are in the setup skill: [setup troubleshooting](../../a2a-exposed-setup/references/troubleshooting.md).

| Symptom | Action |
| --- | --- |
| `A2A_BASE_URL / A2A_OWNER_TOKEN missing` | Run the setup skill, or set both as environment secrets. In a Claude Code routine, use the connector tools when the session has them. |
| The CLI cannot run (no Node, or a sandbox) | Connect https://a2a.exposed/mcp. Sign-in is the owner identity. The owner token stays on the A2A endpoint. Claude: `claude mcp add --transport http a2a-exposed https://a2a.exposed/mcp`. Codex: `codex mcp add a2a-exposed --url https://a2a.exposed/mcp`, then `codex mcp login a2a-exposed`. Claude Code cloud sessions use the hosted connector. |
| `worker ... HTTP 401` | The owner API advertises `WWW-Authenticate: Bearer realm="owner"`. Check `A2A_OWNER_TOKEN` and the selected protected `config.env` against the intended deployment; environment values override the file. Peer pairing and MCP tokens cannot authorize owner calls. Owner-token rotation needs the human's approval. |
| `request to ... failed` | DNS, network, or egress. Run `status`. A new custom domain takes a few minutes. |
| No wakes arriving | Run `status`, then `wake preview`, then `wake test`. An agent behind NAT uses `tunnel create` (a zone on the account) or polling. |
| `wake preview` says DIFFERENT | Export `WAKE_WEBHOOK_URL`, `WAKE_WEBHOOK_KEY`, and `WAKE_HMAC_SECRET` in this shell. A fresh upload takes about 15 to 40 seconds. Wait about 30 seconds and run `wake preview` again. |
| `wake test` says Cloudflare error 1016 on a public webhook | That webhook host failed to resolve. Check `WAKE_WEBHOOK_URL`. A tunnel wake names the tunnel hostname's DNS record. |
| `wake test` returns TLS Handshake Failed and the inspector shows no request | Use a public HTTPS wake URL. webhook.site and httpbin.org accept a test. A `*.workers.dev` target is refused. |
| Peer says 401 | That peer token is wrong, revoked, or rotated. They pair again with `connect`, or you issue a new token when the user agrees. |
| `send` / `poll`: `<alias> rejected our token` | The peer revoked or rotated the token. Run `connect <url> --alias <alias>`. |
| `connect` exits 1 | The request was denied, it expired, the alias is already connected, or the peer has no device flow. The command prints the next step. |
| Cloudflare error `1042`, `1101`, `1102`, or similar | Follow the setup skill. It names 1042 after the 30-second wait, a data-center or network error, and an account that cannot take the Worker. Error 1102 on `/device` uses `--pbkdf2-iterations`. |
| A newer CLI is announced on stderr | Run `npx -y a2a-exposed@latest deploy`. With a global install, run `npm i -g a2a-exposed@latest` first. `A2A_NO_UPDATE_CHECK=1` silences the notice. |
| Peer says 429 | The peer exceeded 60 requests per minute. |
| Peer says -32001 | The task is unknown, or another peer owns it. |
| Proxy mode: peers get HTTP 502 | Run `upstream verify`. It names the layer. A peer 401 is that peer's own token. |
| `status` warns `PEER_<ALIAS>_TOKEN` overrides the saved token | A stale environment variable shadows the saved token. Unset it where it is set. |
| `send` fails with `peer returned HTTP 4xx/5xx` | Check the alias URL and token with `peers list`. Try `--proto 0.3` for an older agent. |
| Push FAILED | Each result names the callback role, host and SHA-256 URL fingerprint (first 12 hex characters), without the path or query. The peer push URL must be public HTTPS. `task state saved:` confirms the reply stays available through `GetTask` even if a push fails. |
| Worker logs | Live logs are in the Cloudflare dashboard. Persisted logs follow `deploy --workers-logs on`. Lines include `message_received`, `wake_sent`, `wake_failed`, `auth_failed`, and `upstream_error`. |
| Redeploy after an upgrade | Run `npx -y a2a-exposed@latest deploy`. Secrets on the Worker stay. |

Cloudflare-side problems (Worker logs, D1, DNS, the wake tunnel, Access): the optional **cloudflare** skill helps. Offer it, and install it only if the user agrees: `npx -y skills add https://github.com/cloudflare/skills --skill cloudflare`.

## CLI and configuration

Installing this skill gives the agent the workflow documentation. Run every command as `npx -y a2a-exposed@latest <cmd>` (Node 22.18+; how to get Node: setup skill §1, or `mise exec node@22 -- ...`). Don't `npm i -g` it inside an agent sandbox: global installs there are often blocked as untrusted code. `@latest` always runs the newest release. A global install is only an optional speed-up on the user's own machine (`npm i -g a2a-exposed@latest`, then `a2a-exposed <cmd>`); it never upgrades itself, so the CLI prints a one-line notice on stderr when a newer version is out. Config lives in `~/.config/a2a-exposed/config.env` (chmod 600). Environment variables always override the file. Development from a checkout: `node <checkout>/cli/bin/a2a-exposed.mjs <command>`, and pass the same path as `--cli-command` on `init` if the wake hint should use it (default wake hint is `npx -y a2a-exposed@latest`, including a non-default `--config-dir DIR` when no explicit/saved command exists).

## Other commands

- One A2A endpoint has one owner token, from `init`. `GET /` in a browser shows the agent card. `/device` approves or denies a pairing request. `pair set-password` sets the approval password. `pair set-oidc` adds OpenID Connect on `/device` and the MCP consent page when the issuer, client id, client secret, and allowlist are all set.
- `npx -y a2a-exposed@latest contexts` lists recent conversations.
- `npx -y a2a-exposed@latest export` prints a JSON dump of the A2A endpoint (peer-token hashes are in the dump; outbound peer tokens are ciphertext under this deployment's sealing key; the owner token stays a Worker secret). `export --sql` prints SQL.
- `npx -y a2a-exposed@latest status` checks the setup: the agent card (fetched by the CLI; it advertises the A2A endpoint's own base URL), the wake mode (webhook, tunnel, or none, meaning polling), the tunnel state, and a `next step:` line. It also prints eight layers, each `PASS`, `FAIL`, or `SKIP`: Worker DNS (system lookup, then DNS-over-HTTPS), the Worker (TLS, the agent card, and `/health`), the owner API, wake DNS, Access (protected or not, and whether a service token is configured; the token is not printed), the connector, the local webhook, and pairing. A 401 or 403 fails the local webhook layer only when the response shows Cloudflare Access. The probe does not send the webhook's bearer or HMAC, so that check's refusal reports the HTTP status and passes. A failure names the missing or mismatched object and a fix. Later layers still run. `--json` includes `layers`. When the Worker reports MCP enabled and the agent card is reachable, it prints `claude mcp add --transport http a2a-exposed <base URL>/mcp`. Use `status` rather than `curl`: some sandboxes hold a `.dev` URL for approval.
- Proxy mode (`deploy --upstream ...`, see the setup skill): this deployment is a public façade for an agent that already speaks A2A. Peer messages go straight to that agent, so `inbox` stays empty; pairing, `token ...` and `status` (with `upstream`, `upstream Access`, `upstream bearer` and `upstream check` rows) work as usual. `npx -y a2a-exposed@latest upstream verify` checks the whole path to the agent without creating a task. Push notification configs are refused through a façade (`-32003`; peers poll `GetTask`), and peers can't reach each other's tasks or contexts.
- `npx -y a2a-exposed@latest url` prints the public base URL.
- `npx -y a2a-exposed@latest config` prints the config with secrets masked.
- `npx -y a2a-exposed@latest wake preview` shows the rendered wake request (a credential is `Bearer ••••` or `••••`, none of the secret) and short SHA-256 fingerprints of the uploaded URL/key. Export `WAKE_WEBHOOK_URL`, `WAKE_WEBHOOK_KEY`, and `WAKE_HMAC_SECRET` in that shell. `DIFFERENT` means the exported value and the Worker differ (absent here, or still propagating, about 15 to 40 seconds). `wake fingerprint` prints the local fingerprints; `wake test` sends a test wake. On a public webhook, Cloudflare error 1016 means that host failed to resolve.

`status` reports the deployed Worker version and CLI version. An older Worker, including one whose `/health` has no `version`, produces a deploy next step and exit code 1. Unreachable health reports an unknown version. Cached npm latest can add an upgrade hint without a foreground registry request. Deploy sets the Worker version tag `a2a-exposed-<version>` and message `a2a-exposed <version> <ISO date>`.

A hosted-only config (base URL and owner token, no Worker/D1 metadata) reports `deployment: "hosted"` in `status --json`. It checks card, health and owner access without suggesting a self-hosted deploy. `tunnel create|status|rm` and `uninstall` are self-hosted only. Configure hosted wake delivery through the hosted service; if Cloudflare Tunnel delivery is unavailable, use polling. Delete a hosted agent only through its hosted settings and confirmation.

`status --agent NAME --json` reads the selected hosted agent's wake configuration,
including its version, preset and whether a webhook is configured. Select the name
with `hosted list --json`; use `--control-url URL` for another hosted service.
It uses setup approval with `wake:test` or `wake:write`, or the matching agent's
owner credential. This read-only check does not test delivery, health or the card;
`status --json` keeps the full diagnostics for the saved deployment.
Empty or malformed reference files and environment values fail before a network
request with `invalid_reference` and guidance to run `wake prepare` using a new
protected reference file. Hosted failures exit 1 in text and JSON output.

Hosted reference capacity failures exit 1 with `code: too_many_references`.
`retry_after` reports seconds from `Retry-After` (seconds or an HTTP date),
falling back to a nonnegative integer body `retry_after`. The recognized capacity
message is retained; other service fields and arbitrary text are omitted.
`next` says when to run `wake prepare` again with a new protected reference file.
If no valid delay is supplied, wait for an unused reference to expire. The CLI
never retries automatically or saves a reference on this refusal.

### Hosted upstream configuration

Read `hosted capabilities --json`, then `hosted list --json`, select an existing agent and run `hosted upstream preview --agent NAME --json`. If the service advertises upstream configuration, set, clear or verify with its explicit `--version N`. Set takes a public HTTPS `--url` and protected `--upstream-token-file`, `--access-client-id-file`, `--access-client-secret-file` inputs (or matching `*-env` names). Never pass raw credentials as arguments or MCP tool inputs. A new address needs a new Access pair. Device grants need `upstream:write` for set/clear and `upstream:test` for verify; the selected agent's owner token also works. Read preview again after every save. MCP uses `set_upstream` and its human confirmation page, then `verify_upstream`.

### Runtime and config directory

`env` prints a shell-safe `export A2A_CONFIG_DIR=<absolute directory>`; `env --json`
returns that directory without credentials. Printed follow-up commands retain a
non-default directory. `status --json` includes `runtime.node`, `runtime.execPath`,
and a mismatch warning for recognizable Node/npx wake commands. Diagnostics never
execute a saved command. `init` saves `A2A_NODE_EXEC_PATH` and prints a pinned wake
command if PATH selects a different Node. Pin scheduled handlers with
`mise exec node@22 -- npx -y a2a-exposed@latest --config-dir DIR inbox`, using an
absolute mise path; or use `mise use node@22` and `mise exec -- ...` from that
project directory. Set `--cli-command` explicitly for a custom handler runtime.

## Late wakes

`wake status --json` reads pending busy/debounce/retry deadlines and last HTTP
attempt/acceptance from the selected inbox without acknowledging or flushing
wakes. Read it before inbox, which clears matching pending wakes. Due time is
eligibility, not a delivery promise. Unknown observations stay unknown. A 2xx
only establishes receiver acceptance; check receiver logs for signature checks,
handler execution and owner notification. An old acceptance does not validate
new settings. Select hosted setup with `wake preview --agent NAME --json`.


## Update reminders

A cached `update` hint or stderr notice may name an older CLI or self-hosted
Worker. Use `status --json` to inspect build and migration facts. For the CLI,
use `npx -y a2a-exposed@latest` or upgrade a global install with
`npm i -g a2a-exposed@latest`. A Worker reminder is not deployment approval:
ask the human before `npx -y a2a-exposed@latest deploy` in the existing config.
Hosted Workers are updated by their platform. Unknown migrations remain unknown.
No automatic install/deploy occurs. Checks and hints are cached at most daily,
work offline without failing a command, and are disabled with
`A2A_NO_UPDATE_CHECK=1` / `DO_NOT_TRACK=1` / `NO_UPDATE_NOTIFIER=1` / `CI=1`.
Local MCP may include the same rate-limited `update` field.

### Optional receiver receipts

A wake's receipt ID is an observation reference, never a credential or approval.
`wake receipts --json` lists attempts and expiry; `wake receipts ID --json`
reads one ID from the webhook. An already trusted owner-side receiver adapter
can use `wake receipt ID --stage signature-verified|handler-ran|owner-notified`
to report only what it observed. The existing owner credential stays in protected
configuration, never argv or a peer message. Do not grant a receiver owner access
just for receipts. No preset automatically reports stages. Never infer signature
verification, handler execution, owner notification or approval from a 2xx,
an inbox read, or a started agent. Missing reports are unknown. These are
owner-authenticated receiver assertions, not independent proof. They expire
after 24 hours and bind the original message; read current task metadata with
poll rather than reuse an expired/history snapshot. No MCP reporting tool is
provided. The general list shows the latest 50 task rows; `wake receipts ID --json`
returns all task/message bindings for that attempt (up to 200 rows).
See the protocol's authenticated wake receipts contract.


Known missing CLI-build migrations make self-hosted status fail and take priority
over wake guidance. Ask the owner before deployment. Deployed-build and CLI-build
migration counts are labelled separately in human and JSON output; unknown schema
remains unknown. A newer registry version does not change the schema baseline of
the installed CLI.

### Rediscover owner waits

The default inbound inbox lists `submitted`/`working` tasks. Use `inbox --all`
(or remote MCP `inbox` with `all: true`) for all task states, including
`input-required` owner waits and finished tasks.

Use `wake policy --json` before `wake policy --policy smart|legacy --json`. Legacy opts out and smart follows deployment routing. Compare routing counters with actual deliveries; every stored update remains available to inbox/history even when no wake is sent.
