# docker-mailbox setup

## Requirements

- Docker + Docker Compose
- One or more email accounts with IMAP and/or SMTP credentials
- Username/password authentication supported by the provider. Some providers require app passwords; OAuth-only accounts are unsupported.

## Quick install

```bash
git clone https://github.com/psyb0t/docker-mailbox
cd docker-mailbox
cp config.example.yaml config.yaml
cp .env.example .env
chmod 600 config.yaml .env
# Configure accounts in config.yaml and replace the placeholders in .env.
```

Then either:

```bash
# Plain docker run
docker run --rm --env-file .env -p 127.0.0.1:8000:8000 \
  -v "$PWD/config.yaml:/etc/mailboxd/config.yaml:ro" \
  -v mailboxd-state:/var/lib/mailboxd \
  psyb0t/mailbox:latest

# Or Compose (publishes on 127.0.0.1:${PORT:-8000} and creates the state volume):
docker compose up -d
```

Verify it came up:

```bash
curl -s http://localhost:8000/health
# {"ok": true, "version": "..."}
```

## Configuration

### `config.yaml`

Select the YAML file with `--config`, then `MAILBOXD_CONFIG`, or use the default `/etc/mailboxd/config.yaml`. Mount it read-only in the container.

```yaml
log_level: INFO

# Bearer authentication protects the API and /mcp. Only /health is public.
# Each token has a name, scopes (read | draft | organize | send | delete | admin)
# and a mailbox allowlist. Restart after changing the configuration.
auth:
  tokens:
    - name: mila
      token: ${MAILBOXD_TOKEN_MILA}   # generate with: openssl rand -hex 32
      scopes: [read, draft, organize]
      mailboxes: [personal]           # or "*"
    # - "legacy-bare-token"           # all scopes on all mailboxes (logs a warning)

# SQLite state (audit log, send limits, checkpoints, draft send claims and webhook deliveries): mount a volume on /var/lib/mailboxd
state:
  path: /var/lib/mailboxd/state.db

mailboxes:
  - name: personal                  # URL-safe handle; matches [a-zA-Z0-9_-]+, must be unique
    description: "Gmail"

    imap:
      host: imap.gmail.com
      port: 993                     # default 993
      tls: ssl                      # ssl | starttls | none   (default ssl)
      username: me@gmail.com
      password: "app-password"      # not your real account password
      default_folder: INBOX         # default folder when callers don't specify

    smtp:
      host: smtp.gmail.com
      port: 465                     # default 587
      tls: ssl                      # default starttls
      username: me@gmail.com
      password: "app-password"
      from_address: "Me <me@gmail.com>"

  - name: work
    imap: { host: mail.work.com, port: 143, tls: starttls, username: me, password: "...", default_folder: INBOX }
    smtp: { host: mail.work.com, port: 587, tls: starttls, username: me, password: "...", from_address: me@work.com }
```

### Config rules

- **At least one mailbox** is required.
- Each mailbox must declare at least one of `imap` / `smtp`. Both is fine. Neither is a config error.
- `name` is the URL path segment and the value of the MCP `mailbox` argument. It matches `[a-zA-Z0-9_-]+` and must be unique.
- Defaults are IMAP `993/ssl` and SMTP `587/starttls`. Override them to match the provider.
- **The config file holds plaintext passwords and your bearer tokens.** Treat it like a credential vault: gitignore it (the repo already does), `chmod 600`, mount read-only into the container, don't paste it in chat.

### Provider authentication

Check the provider's current IMAP/SMTP settings and authentication policy. Mailboxd supports username/password login, including app passwords. It does not implement OAuth login. SSL and STARTTLS verify certificates and hostnames; mount a trusted CA bundle for private servers. See the [upgrade notes](https://psyb0t.github.io/docker-mailbox/operations/#upgrade-notes).

## Catch-all senders

To authorize aliases in one domain, add an identity with `address: "*@example.com"` alongside a concrete default identity. Set its `name`, `signature_text` and `signature_html` as needed. Requests must supply a concrete address, never `*`. Exact identities win; patterns match only their exact domain, not subdomains. Patterns cannot be defaults. Replies automatically match To/Cc addresses before using the concrete default. The SMTP provider must also allow the selected sender.

## Ports

| Port | Service                                                                                  |
| ---- | ---------------------------------------------------------------------------------------- |
| 8000 | HTTP API (`/health`, `/mailboxes`, `/inbox`, `/mailboxes/<name>/...`) AND MCP at `/mcp`  |

The image listens on `0.0.0.0:8000` inside the container. Keep that internal address for Docker port forwarding and shared-network clients. The standalone CLI defaults to loopback, but the image's normal startup command explicitly overrides it.

Publish host-local access with `-p 127.0.0.1:8000:8000`, or `-p 127.0.0.1:9000:8000` for another local port. The checked-in Compose file publishes `127.0.0.1:${PORT:-8000}:8000`. Publish on all interfaces only for deliberate remote access, with bearer authentication and HTTPS.

If replacing the image command with `mailboxd http`, pass `--host 0.0.0.0`; otherwise published ports cannot reach the container's loopback listener. A proxy on the same Docker network can instead use `http://mailboxd:8000` without a host-published port.

## Auth

Every request except `GET /health` must carry a token configured under `auth.tokens`:

```
Authorization: Bearer <a configured token>
```

- Missing / malformed / wrong token → `401` with `WWW-Authenticate: Bearer`.
- Tokens are compared in constant time.
- The same bearer authentication protects `/mcp`.
- To rotate tokens, add the new token and restart, switch clients, then remove the old token and restart again.

When `auth.tokens` is empty or omitted, protected requests return `401`; only `/health` remains available. Add a token and restart to use the API or MCP. A token only does what its `scopes` allow and only sees the mailboxes in its `mailboxes` list (a hidden mailbox answers `404`, like a missing one); a bare-string token holds every scope on every mailbox. Give agents the narrowest scopes they need, typically `read`, `draft`, `organize`.

## Management

```bash
# Lifecycle
docker compose up -d         # start
docker compose down          # stop
docker compose logs -f       # tail logs
docker compose pull          # grab a new image
docker compose restart       # restart after editing config.yaml

# Dev (in-repo workflow)
make help                    # list dev targets
make dev-image               # build the sandboxed dev container
make shell                   # drop into it
make run                     # boot the server locally (mounts CONFIG=path/to/config.yaml)
make test                    # full suite (unit + docker-in-docker integration)
make test-unit               # in-process only, fast feedback
make lint                    # flake8 + mypy
make sec                     # semgrep + bandit + pip-audit -> sec.sarif (reports, never fails)
make format                  # isort + black
```

## Logs

mailboxd logs to stdout in the format `%(asctime)s %(levelname)s %(name)s %(message)s`. Control level with `log_level: DEBUG|INFO|WARNING|ERROR` in `config.yaml`. Read with `docker compose logs -f` or whatever your orchestrator does with container logs.

## Remote access through Cloudflare Tunnel

Cloudflare Tunnel can publish an HTTPS endpoint without opening host ports. Configure bearer tokens before exposing the service. Install `cloudflared` using the [official instructions](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

```bash
# Authenticate and create tunnel
cloudflared tunnel login
cloudflared tunnel create mailbox

# Route a subdomain
cloudflared tunnel route dns mailbox mailbox.yourdomain.com

# Keep credentials in the ignored .data directory
mkdir -p .data/cloudflared
TUNNEL_ID=your-tunnel-id
cp "$HOME/.cloudflared/$TUNNEL_ID.json" .data/cloudflared/creds.json
```

Create `.data/cloudflared/config.yml`:

```yaml
tunnel: <tunnel-id>
credentials-file: /etc/cloudflared/creds.json

ingress:
  - hostname: mailbox.yourdomain.com
    service: http://mailboxd:8000
  - service: http_status:404
```

Add `cloudflared` to the existing Compose deployment on its `mailbox` network. Mount `.data/cloudflared` read-only at `/etc/cloudflared` and run `tunnel --config /etc/cloudflared/config.yml run`. Keep the existing mailboxd environment, state volume, healthchecks and isolation settings. The proxy reaches `http://mailboxd:8000` over that network, so mailboxd does not need a host-published port for tunnel access.

Clients connect to `https://mailbox.yourdomain.com` with their configured bearer token. Restrict tunnel credentials and rotate bearer tokens when needed.

## Troubleshooting

| Symptom                                                  | Likely cause                                                                                              |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `401 missing or invalid Bearer token`                    | Forgot `-H "Authorization: Bearer ..."` or token doesn't match anything in `auth.tokens`.                  |
| `502 imap_error` or `smtp_error` | Check credentials, permitted login method, host, port and TLS settings. Upstream error details are sanitized. |
| `409 mailbox 'X' has no imap configured`                 | You called an IMAP endpoint on an SMTP-only mailbox (or vice versa). Check `/mailboxes` for capabilities.  |
| `404 unknown mailbox`                                    | Mailbox `name` in the URL doesn't match anything in `config.yaml`.                                         |
| Self-send lands in Spam | Search the provider's spam folder and check its delivery logs. |
| Container won't start, `config not found: ...`           | Your config mount didn't land at `/etc/mailboxd/config.yaml`. Check the volume path.                       |
| `config ... invalid: ...` on startup | Configuration validation failed. Check the reported field and its documented limits. |
| MCP client gets `Task group is not initialized`          | Server isn't fully started yet (lifespan hasn't completed). Retry after a moment.                          |
| `/inbox` `errors` array has entries | Those accounts failed. Other accounts still return results. Check each per-mailbox `error`. |

## Watcher and recovery

HTTP workers and the watcher share one local SQLite volume. It retains audit records, quotas, checkpoints, draft send claims and webhook metadata. Mail bodies and credentials remain outside the database. Configure `watch.webhooks` and start `docker compose --profile watch up -d`. Delivery is at least once. Verify HMAC over timestamp, period and raw body; reject timestamps outside five minutes and deduplicate event IDs. Failed deliveries retry durably, then remain available for admin replay. See the [webhooks guide](https://psyb0t.github.io/docker-mailbox/webhooks/) for verification and the [operations guide](https://psyb0t.github.io/docker-mailbox/operations/) for upgrades and backups.
