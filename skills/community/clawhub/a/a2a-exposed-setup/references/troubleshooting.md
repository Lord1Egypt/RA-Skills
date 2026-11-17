# Troubleshooting setup

A failure these fixes do not cover, a wrong step in the docs, or a workaround you had to invent is worth a report. Offer it to the human as described in [When something goes wrong](../SKILL.md#when-something-goes-wrong).

Offer hosted up front when the human has no Cloudflare account or no preference; see [Getting started](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/getting-started.md#hosted-inbox). If self-hosting is chosen, name the reason and offer hosted when this machine has no Cloudflare profile, token, or account, or when a known Cloudflare error blocks the deploy. A fresh workers.dev deploy can show error 1042 for about 30 seconds; run `status` again once, then offer hosted if 1042 is still there. A working login does not authorize resource changes: follow the [consent checklist](deploy.md#before-cloudflare-changes) before any mutating fix below.

| Symptom | Fix |
|---|---|
| No `CF_PROFILE`, no `CLOUDFLARE_API_TOKEN`, and `cf auth whoami` shows no account | This machine has no Cloudflare account. Offer the hosted option in Getting started, linked above |
| `cf auth login` returns HTTP 403 or "Just a moment..." before a code, and no API token is available | Cloudflare is blocking this network. Offer the hosted option in Getting started, linked above |
| Cloudflare error 1042 after the 30-second wait | Cloudflare error 1042 is still here. Offer the hosted option in Getting started, linked above |
| `init` or `deploy` fails because the token sees no account, or the account refuses the Worker or the database | This Cloudflare account cannot take the A2A endpoint. Offer the hosted option in Getting started, linked above |
| `pair ...`: `internal error (HTTP 500)` | Run `npx -y a2a-exposed@latest deploy` so D1 migration `0003_device_pairing` is applied |
| Peers get `-32603 Internal error` and no wake arrives; Worker logs show `no such table: wake_budget` | Run `npx -y a2a-exposed@latest deploy` so D1 migration `0002_wake_budget` is applied |
| `connect`: `does not offer device-flow pairing` | The peer runs another A2A server, or pairing is `off` there: ask its owner for a token (`token issue`), then `peers add <alias> <url> --token-stdin` |
| `connect`: `not accepting more pairing requests` | The peer's flood limits (5 per IP per 10 minutes, 10 pending): wait and try again |
| `/device` says no approval password is set | Run `npx -y a2a-exposed@latest pair set-password --web` and send your human the one-time link (never open it yourself); or they run `pair set-password` in a terminal |
| Setup link says "invalid, expired or already used" | Links last 15 minutes, work once and are replaced by a newer link: run `pair set-password --web` again |
| `pair approve` is unauthorized | The owner token does not match the Worker. A missing token, or a peer token, cannot approve. In human mode the owner token approves and the peer collects its token on the next poll |
| `connect`: `peer "<alias>" already has a token that works` | Nothing to do (send with `send --to <alias>`); to replace it deliberately, `connect ... --replace` |
| `connect`/`send`: `rejected our token (HTTP 401 ...)` | The peer revoked or rotated it: `connect <url> --alias <alias>` again (its owner approves) |
| `/device` or the setup page: Cloudflare error 1102 | The free plan's CPU limit was hit while hashing: `deploy --pbkdf2-iterations 50000`, then set the password again (see the threat model) |
| `status`: `Cloudflare error 1042` right after a deploy | The Worker is still propagating on workers.dev: wait ~30 s and run `status` again. When 1042 is still there, name that and offer the hosted option in Getting started, linked above |
| `wake preview` / `status` right after `wake set`, `wake unset`, or `tunnel create` | Worker secrets show up in about 15 to 40 seconds. Wait about 30 seconds and run the command again. Export `WAKE_*` in that shell: `DIFFERENT` also means the variable is absent here. For about a minute after the first `tunnel create`, with 0 connector connections, `status` prints `waiting for the connector to connect` and exits 0. After that, start cloudflared. `inactive` means the connector has never connected |
| `cf workers delete` / `cf d1 delete`: `EACCES` mkdir `node_modules/.cache/cloudflare` | Run `uninstall --yes`, or run the `cf` commands from `<config dir>/worker`, or `mkdir -p node_modules/.cache/cloudflare` in the current directory first. See [teardown](teardown.md) |
| `tunnel create` then the connector | Install [cloudflared](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/) on the agent's machine. `tunnel create` prints `cloudflared tunnel run` |
| Where are the Worker's logs? | Real-time: the dashboard's live logs. Persisted and searchable: deploy with `--workers-logs on` (Workers Logs; off by default) and open the Worker's logs in the dashboard; query strings are redacted |
| `not logged in to Cloudflare` | Run `npx cf auth login --no-browser` again; the code expires after about 5 minutes |
| Several accounts | `--account-id <id>` (listed by `cf auth whoami`, or by `cf accounts list` when a profile's whoami is empty) |
| `init` with `--cf-profile` says `0 accounts available` | `cf auth whoami` and `cf accounts list` both succeeded and listed none. Pass `--account-id` |
| `init` says `could not list Cloudflare accounts` | `cf accounts list` failed and no account id was set. The message includes cf's own error and the exit code. Run the printed `npx --yes cf accounts list` command outside the Worker directory, or pass `--account-id`. An id already set with `--account-id` or `CLOUDFLARE_ACCOUNT_ID` is used anyway |
| Card not reachable right after deploy (`status`: `agent card: FAILED`) | A new custom domain takes 1–5 minutes for DNS and the certificate. Check that the hostname is on a zone in this account and has no conflicting DNS record. A newly registered workers.dev subdomain can also take a few minutes |
| `status`: `this machine's resolver does not` | Public DNS has the hostname and this machine does not. On macOS, flush the cache: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`. The other layers are still checked |
| `status`: `no public DNS record` | That hostname has no public DNS record yet. For the Worker, check the custom domain under Workers → Settings → Domains. For the wake host, run `tunnel status` |
| `status`: local webhook is HTTP 401 or 403 and does not say Cloudflare Access | The service-token probe reached the webhook. That GET does not send the webhook's bearer or HMAC, so the webhook's own check can refuse it. The layer passes. A failure that says the Access service token or policy was refused means Access rejected the probe |
| `cf auth login` / `wrangler login`: `OAuth error: HTTP 403 Forbidden` (or "Just a moment...") before any code appears | Cloudflare's managed challenge on datacenter / VPS IPs, not a wrong account: don't retry. Use an API token: `export CLOUDFLARE_API_TOKEN=...` (and `CLOUDFLARE_ACCOUNT_ID`) in the agent's environment or a chmod-600 file, never argv or chat, then run `init`/`deploy` as usual. `init` says the same when it finds no login |
| API token: which permissions, which resources | Workers Scripts, D1, Cloudflare Tunnel and Access are **account**-scoped: grant them on the account. Only DNS (Zone → DNS: Edit, for a custom hostname or the tunnel) can be limited to one zone. Letting `init` discover the account also needs **User → Memberships → Read**; without it `init` asks for `--account-id` / `CLOUDFLARE_ACCOUNT_ID` |
| API token: Cloudflare API error `1001` (Memberships) | The Memberships permission was given a wrong resource selector: it needs the full user-scoped selector (the user's own resource, not an account or zone) |
| API token: `tokens verify` succeeds, but `cf` calls are denied by an IP policy | The token's IP filter must allow **both** the host's IPv4 `/32` and its IPv6 `/128`: calls can leave over IPv6 |
| `connect`: `--card-url ... is not a plain https URL, so it is left out`, or `pairing request ... failed` with a Tailnet / LAN card | A peer card must be public https; a Tailnet-only or http card is left out or refused. Pairing out still works without it (replies by `poll`), but to be reachable expose the agent through a public façade ([Deploy: Already have A2A…](deploy.md#already-have-a2a-on-a-tailnet-or-lan-expose-it-through-a-public-façade)) and pass the façade's card |
| `You need to register a workers.dev subdomain` | The account has no workers.dev subdomain: rerun `init --workers-dev-subdomain <name>`, or create it in the Workers section of the dashboard |
| Hosted `wake set` stops with `hosted_config`, or setup says no saved deployment | Do not run `init` or `deploy` for a hosted address. List `hosted capabilities --json`; when setup is advertised, use `hosted list --json` and an explicit `wake set --agent NAME` with draft settings and protected secret inputs. Otherwise the human uses dashboard Wake settings or hosted MCP confirmation |
| `wake test` says no wake webhook configured | Self-hosted: export `WAKE_WEBHOOK_URL` (and key/HMAC secret) and run `wake set`. Hosted: configure dashboard Wake settings or follow the scoped hosted CLI flow above; environment variables alone do not save hosted wake settings. Polling is available for either hosting choice |
| `wake test` returns 401/403 | Wrong key or header; compare fingerprints from `wake preview` with `wake fingerprint` |
| `wake test` returns TLS Handshake Failed and the inspector shows no request | Use a public HTTPS wake URL. webhook.site and httpbin.org accept a test. A `*.workers.dev` target is refused. |
| `wake test` returns 404 | Wrong URL or route name |
| `wake test` returns a network error | The target isn't publicly reachable (local-only webhook? use `tunnel create`) |
| `wake test` / `tunnel status`: `530 (Cloudflare error 1033)` | The tunnel has no running connector: start `cloudflared tunnel run --token-file ...` on the agent's machine and check that **outbound port 7844** (TCP and UDP) to Cloudflare is allowed |
| Tunnel hostname answers 401/403, or a 302 to `<team>.cloudflareaccess.com` | Blocked by Access: the service token is missing or wrong (expected for requests without it). For wakes, `wake preview` must show `hasAccessServiceToken: true`; if not, `tunnel rm` + `tunnel create` |
| `Cloudflare Access (Zero Trust) is not enabled` | Enable Zero Trust once (dashboard, Free plan) or pass `--zero-trust-org <team-name>` |
| `tunnel create`: `account has N zones; choose one` | Re-run with `--tunnel-zone <zone>` (or `--tunnel-hostname wake-<name>.<zone>`). Any zone on the account works, whether the A2A endpoint is on workers.dev or a custom hostname |
| `tunnel create`: `account has no domain (zone)` | The tunnel needs a zone somewhere on the account. Use polling, or add a domain and run `tunnel create` later (no redeploy) |
| `tunnel create`: `a previous tunnel create did not finish` | Run `tunnel rm`, then `tunnel create` |
| Setup stopped halfway (approval timeout, lost session) | Run `npx -y a2a-exposed@latest status` and continue from its `next step:` line; every step is safe to re-run |
| Proxy mode: peers get `-32603 This agent is unavailable: its façade is misconfigured` or `... not reachable right now` (HTTP 502) | The Worker-to-upstream hop failed; peers are told nothing more on purpose. Run `npx -y a2a-exposed@latest upstream verify` (or `status`): it names the layer and the fix (rows below). A peer that gets **401** instead has a problem with its own token at the façade (re-pair), not the upstream |
| `upstream verify` / `status`: `upstream_auth_missing` (HTTP 401/403 from the agent) | Access let the Worker through, but the agent checks its own bearer and the Worker has none (typical with Hermes: Access headers alone get 401, Access + bearer get `-32601`). Export `UPSTREAM_TOKEN` (or pipe it with `--upstream-token-stdin`) and run `deploy` |
| `upstream verify` / `status`: `upstream_auth_rejected` | The agent refused the Worker's `UPSTREAM_TOKEN` (rotated or wrong): export the current one and run `deploy`. `status` compares fingerprints when `UPSTREAM_TOKEN` is exported locally |
| `upstream verify` / `status`: `access_credentials_missing` / `access_rejected` (302 to `<team>.cloudflareaccess.com`, Access 401/403) | Missing: export `UPSTREAM_ACCESS_CLIENT_ID` / `UPSTREAM_ACCESS_CLIENT_SECRET` and run `deploy`. Rejected: the Access app's Service Auth policy must name that token, and the pair must be current |
| `upstream verify` / `status`: `tunnel_down` (530, Cloudflare error 1033) / `upstream_unavailable` (5xx) / `network` | Tunnel: start `cloudflared tunnel run ...` on the agent's machine. 5xx: cloudflared is up but the agent's A2A server isn't (check the ingress `service:` URL). Network: DNS/certificate of the tunnel hostname |
| `upstream verify` / `status`: `unexpected_response` | `--upstream` is not the agent's JSON-RPC endpoint (a web UI, the card URL, a wrong path): `deploy --upstream <endpoint URL>` |
| `init`/`deploy --upstream`: `the upstream's agent card asks for a bearer token ..., and no UPSTREAM_TOKEN is set` | Export `UPSTREAM_TOKEN` and re-run, or pipe it with `--upstream-token-stdin`. Only if the agent really accepts calls without a bearer: `--no-upstream-token` |
| `init`/`deploy --upstream`: `the upstream's agent card could not be read from here` | The CLI reads the card from this machine with the exported Access token: export `UPSTREAM_ACCESS_CLIENT_ID` / `_SECRET` (a 302 to the Access login means they are missing), or provide `UPSTREAM_TOKEN` / `--no-upstream-token` explicitly |
| `status`: `PEER_<ALIAS>_TOKEN is set in the environment and overrides the different peer token saved` | A stale variable shadows the token `connect` just saved: unset it where it is set (shell profile, service unit) |
| Proxy mode, `status`: `can't fetch the upstream's agent card (HTTP 530 ...)` | The upstream tunnel has no running connector: start `cloudflared tunnel run ...` on the agent's machine |
| Proxy mode, `status`: `the upstream card URL is refused: ... must be on the UPSTREAM_URL origin` | The card URL is on another host than `--upstream` (it would receive the upstream credentials): `deploy --upstream-card-url <URL on the upstream's origin>` or `--upstream-card-url none` |
| Proxy mode, `status`: `can't fetch the upstream's agent card (HTTP 401/403 or 302)` | Access refused the Worker: export the right `UPSTREAM_ACCESS_CLIENT_ID` / `UPSTREAM_ACCESS_CLIENT_SECRET` and run `deploy`; check the Access app's Service Auth policy names that token |
| `--upstream is a private-network address` | By design: publish the agent through a Tunnel hostname behind Access and pass that ([Deploy: Already have A2A…](deploy.md#already-have-a2a-on-a-tailnet-or-lan-expose-it-through-a-public-façade)) |
| Card advertises a local or Tailnet URL (`status`: `agent card: WRONG URL`) | The card URL comes only from the deployment: the custom hostname or the workers.dev URL. Don't edit the card or export `A2A_BASE_URL` / `A2A_PUBLIC_URL` with the agent's own webhook URL; that URL goes in `WAKE_WEBHOOK_URL` only. Unset them and run `npx -y a2a-exposed@latest deploy` |
| Agent sandbox flags a `.dev` URL (e.g. Hermes: `Lookalike TLD`) | Avoid raw `curl` of `*.workers.dev`: `status` checks the card itself. If an approval is still needed, tell the user to approve it |
| Claude Code: `wake test` is 2xx but nothing happens | A 2xx only means a session started. Open the run from the routine's page and read the transcript; the rows below cover the usual causes. Check the [Claude Code checklist](wake.md#claude-code-claude-code) |
| Claude Code run: `A2A_BASE_URL / A2A_OWNER_TOKEN missing` | Each fire is a new session. Easiest: add the [connector](wake.md#claude-code-claude-code) (`<Worker URL>/mcp`), which needs no variables. CLI fallback: set both on the routine's **cloud environment** (not in a session, prompt or chat), then fire again |
| Connector: adding it fails, or the consent page says "Unknown client" | Check `<Worker URL>/health` shows `"mcp": true` (not `--mcp off`, not proxy mode) and the Worker is redeployed (migration `0006_mcp`). "Unknown client": remove the connector in the client and add it again |
| Connector consent: "No approval password is set yet" | `npx -y a2a-exposed@latest pair set-password --web`, open the link, then add the connector again |
| Connector: `send` says the peer isn't synced, or the stored token can't be read | `npx -y a2a-exposed@latest peers sync <alias>` on the machine with your peers (again after `connect`, a token change or an owner-token rotation) |
| Connector stops working (401) | Its access token expired and refresh failed, or it was revoked (`token list` shows `REVOKED`). Reconnect it in the client and approve again |
| Claude Code run: skill not found / doesn't use the skill | The routine clones the **default branch** of its repository sources: add the repo as a source and merge `.claude/skills/` there (a `claude/...` branch isn't cloned) |
| Claude Code run: `403` with `x-deny-reason: host_not_allowed` | The environment's network access (Trusted by default) doesn't allow the Worker: Custom, add the exact hostname, keep the default package list. Not `*.workers.dev` |
| Claude Code run ignores the wake text | The fire text arrives in a `routine-fire-payload` block marked untrusted: the saved routine prompt must tell Claude to act on it |
| Claude Code setup session refuses tunnel creation or `curl` / `watch` loops (auto-mode classifier, "External Ingress Tunnel") | Expected: `claude-code` needs no tunnel (`tunnel create` refuses hosted presets). Run `init` / `deploy` / `wake set` from your own terminal, and check once with `status` / `wake test`. |
| Claude Code 429 (`rate_limit_error`, `Retry-After`) | 30 fires/hour per routine (shared with Run now), 100/hour per account. Lower `--max-per-hour` or raise `--debounce`. The Worker re-sends a 429/503 wake after `Retry-After`, up to 3 times, on the next request, a self-hosted cron run (`--cron`), or the A2A endpoint alarm; after that it is dropped (log `wake_dropped`). Messages are never lost: run `inbox` or the connector's `inbox` tool |
| Routine token pasted into chat or a prompt | Regenerate it on the routine's API trigger, export the new value as `WAKE_WEBHOOK_KEY` from a file, run `wake set --preset claude-code` |
| Hermes 401 | `WAKE_HMAC_SECRET` must equal the route secret, and the Worker clock skew must be under 300 s (it normally is) |
| `cf deploy` lists secrets as `Environment Variable (hidden)` | Expected: `cf` uploads secrets that way; they are still Worker secrets, not plain vars |

Workers.dev registration uses a terminal relay on macOS and Linux. An unexpected
prompt times out; SIGINT, SIGTERM, and SIGHUP stop its detached terminal job.

In the staging secure-link integration, an expired approval request requires a
new request with the same command: `hosted link create` or `hosted link finish`.
An expired grant after approval requires `hosted link finish` for fresh approval.
A connector token already saved locally remains on disk; wake settings are not
saved when the grant expires. A polling refusal requires fresh approval, rather
than changes to hostname or creation options.

## Internal secure-link refusal recovery

This reference applies to maintainer runs of the internal integration, not a
public setup option. Follow the scope in [contributor verification](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/agents/verification.md#staging-hosted-link-refusal-contract).
Recovery that creates or removes resources requires the owner's authorization;
never perform it automatically or approve on the owner's behalf.

The wake-test failure keeps recognized codes such as `none`, `tls`, `private`, and
`connection`. An unrecognized result displays `unknown`; server text stays hidden.
A connected tunnel alone does not prove the receiver accepts a wake.

| Refusal | Recovery |
| --- | --- |
| `apex_hostname` | Choose a hostname below the domain, such as `wake.example.com` |
| `outside_zone` | Choose a hostname on a domain in the connected Cloudflare account |
| `existing_dns`, `existing_tunnel` | Choose another hostname; do not delete existing resources as an automatic fix |
| `link_exists` | Review the approval page; an older service's refusal does not prove another link exists |
| `slow_down` when starting a request | Ask the owner to deny an earlier pending request on the website, or wait for expiry before rerunning the failed operation. Token-polling `slow_down` instead increases the polling interval |
| `provision_failed`, hostname/zone conflict | Choose another hostname on a domain in the connected account |
| `provision_failed`, cleanup phase | Ask the owner to remove the unfinished link on the website, then recreate it |
| `provision_failed`, Cloudflare 401/403 | Reconnect Cloudflare on the website before recreating the link |
| `provision_failed`, Cloudflare 429/5xx | Wait a few minutes before recreating the link |
| Other `provision_failed` | Review the failing phase and cleanup state on the approval page before retrying |
| `unreadable` | Ask the owner to remove the secure link on the website, then recreate it; reconnecting Cloudflare does not recover the access key |
| `access_denied` | Request fresh approval only if the owner still wants the link |
| `expired_token` | Restart an expired approval request with the same create/finish command. After grant expiry, run `hosted link finish` for fresh approval |
| `invalid_grant` | Rerun the failed operation for fresh owner approval |
| `already_delivered` | Request fresh approval if the credentials were not received |
| `link_not_ready` | Finish creating the link in Wake settings before requesting fresh approval |
| `connector_not_connected` | Start cloudflared with the saved token file, then request fresh approval |
| `not_found` | Check the selected agent on the website before requesting fresh approval |
| `cloudflare_unavailable` | Reconnect Cloudflare in Wake settings before requesting fresh approval |
| `unavailable` | Retry later with fresh owner approval |

A recognized `reason` takes precedence over `error`. Provisioning phase and
status select local recovery guidance. Only checked public validation templates
may be displayed; arbitrary server text and extra fields stay hidden. A refusal
does not read a signing secret or request connector credentials.

For internal link wake-test failures, `wake_result=<code>` on stderr gives the
fixed diagnostic code. The local message gives the next step and confirms saved
wake settings were not changed. Unknown results call for a CLI update and feedback.

For internal secure-link tests, HTTP 409 save refusals (including `failed` and
`conflict`) emit `wake_result=not-saved`. This result also means the test wake was
delivered but saving settings was not confirmed. Save the settings in Wake
settings on the website, then test again. The connector token remains on disk;
the CLI does not retry the test or save automatically.

The staging `hosted link create|finish --json` commands write one result object
on stdout: `{ok, code, reason, field, phase, status, hostname, next}`. Fields
without a value are `null`; success also includes `saved` and
`connectorStarted`. Approval links, codes and connector guidance remain on
stderr. Exit status is 0 on success and 1 on any failure. Diagnostics contain
only local guidance and recognized public codes, never grants or signing secrets.

Both commands require an explicit `--preset ID` before any approval request,
even when a link already has a saved preset. List choices with
`hosted capabilities --json` and select the agent with `hosted list --json`.
`create --hostname` accepts a DNS name or a root HTTPS URL. It normalizes case,
one trailing root dot and IDN labels to ASCII. Credentials, ports, non-root
paths, queries, fragments, IP addresses and malformed labels receive distinct
local validation reasons before any network request. Invalid hostname input
is never echoed in the result.

For hosted `cloudflare-target-unsupported`, use `recovery_url` only when the CLI returns one for the selected agent. It opens human-confirmed **Import or manage your existing tunnel** on that service; connect Cloudflare, check the exact route and confirm the Access service-token secret rotation. The old secret stops working. Then send one authenticated test wake and save. Do not create another tunnel, auto-import, retry a refused request, or weaken Access/signatures. Without that recovery, use the service's supported public HTTPS route, polling or an explicitly authorized self-hosted Worker.
