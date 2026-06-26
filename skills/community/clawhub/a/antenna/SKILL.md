---
name: antenna
description: >
  Inter-host OpenClaw session messaging over reachable HTTPS using built-in
  gateway webhook hooks. Use when: (1) sending a message from this OpenClaw
  instance to another host's session, (2) checking status/health of a remote
  peer, (3) managing the peer registry (adding/removing/listing known peers),
  (4) exchanging bootstrap trust material for new peers, (5) any cross-host
  agent communication that should NOT go through visible chat channels like
  Telegram/WhatsApp/Discord. Triggers: "send to PEER", "message the other
  host", "antenna send", "antenna status", "antenna peers exchange",
  "cross-host message", "inter-host relay", "ping PEER", "peer list",
  "check antenna inbox", "approve message".
metadata:
  version: 1.5.1
  repository: "https://github.com/cshirley001/openclaw-skill-antenna"
  homepage: "https://github.com/cshirley001/openclaw-skill-antenna"
postInstall: "bash skills/antenna/bin/antenna.sh setup"
---

# Antenna — Inter-Host OpenClaw Messaging (v1.5.1)

Send messages between OpenClaw instances over reachable HTTPS via the built-in `/hooks/agent` webhook.

## Prerequisites

Each participating host needs:
1. OpenClaw gateway running with hooks enabled (`hooks.enabled: true`)
2. A reachable HTTPS endpoint for `/hooks/agent`
3. Antenna agent registered in gateway config (`agents` section)
4. `hooks.allowedAgentIds` includes `"antenna"`
5. `hooks.allowedSessionKeyPrefixes` includes `"hook:antenna"`
6. Host-specific Antenna config in:
   - `antenna-config.json`
   - `antenna-peers.json`

Normal path:
- Run `antenna setup` to generate the live runtime files.
- Use `antenna-config.example.json` and `antenna-peers.example.json` as tracked reference templates only.

Notes:
- Peers do **not** need to share one tailnet or one central hub.
- Tailscale Funnel is a convenient default, but reverse proxies, VPS/domain-hosted HTTPS, Cloudflare Tunnel, and similar paths also work.

## Architecture

Messages flow through a script-first relay pipeline:

1. **Sender** runs `antenna-send.sh` which builds an `[ANTENNA_RELAY]` envelope and POSTs it to the recipient's `/hooks/agent` endpoint.
2. **Recipient gateway** dispatches to the dedicated **Antenna agent**.
3. **Antenna agent** writes the raw inbound message to a temp file using the `write` tool.
4. **Antenna agent** execs `antenna-relay-deliver.sh` with that file path as its single argument.
5. **The wrapper** reads the file, invokes the relay engine internally, handles verification + local delivery + cleanup, and prints one status line.
6. **Message appears** persistently in the target conversation thread when accepted.

The LLM never performs relay parsing, delivery formatting, or session-routing logic; the scripts do all processing.

## Trust Model

Antenna trust is layered:
- **Peer URL** — where to reach that installation
- **Hook bearer token** — protects webhook ingress
- **Per-peer runtime identity secret** — authenticates claimed sender identity when configured. Verified via constant-time comparison; no plaintext secrets land in relay logs.
- **Peer allowlists** — explicit inbound and outbound peer lists
- **Inbound session allowlist** — limits where inbound relay may deliver (full session keys only)
- **Envelope marker guard** — messages whose bodies or header values contain the envelope markers `[ANTENNA_RELAY]` / `[/ANTENNA_RELAY]` are rejected as malformed (prevents envelope smuggling)
- **Message freshness window** — each message carries a `timestamp:`; stale or future-dated messages are rejected. Defaults: 300s max age, 60s max future skew. Tunable via `.security.max_message_age_seconds` and `.security.max_future_skew_seconds`.
- **Rate limiting** — per-peer and global throttles
- **Untrusted-input framing** — reminds receiving agents the relayed content may be external
- **Log sanitization** — peer-supplied values stripped of control characters before logging
- **File-permission audit** — `antenna status` flags any token/secret file looser than `chmod 600`
- **Self-id required** — sender refuses to run without `self_id` configured; it does not fall back to `$(hostname)`

For peer onboarding, Antenna now prefers **Layer A encrypted bootstrap exchange** using `age`. Legacy raw-secret export refuses non-TTY output (no piping runtime identity secrets into captured automation).

## Configuration

Live runtime files are local installation state:
- `antenna-config.json`
- `antenna-peers.json`

Tracked reference files live beside them:
- `antenna-config.example.json`
- `antenna-peers.example.json`

Use `antenna setup` for normal installation; use the `*.example.json` files for schema reference or manual recovery.

### `antenna-config.json`

```json
{
  "max_message_length": 10000,
  "default_target_session": "agent:betty:main",
  "relay_agent_id": "antenna",
  "relay_agent_model": "openai/gpt-5.4-nano",
  "local_agent_id": "<your-agent-id>",
  "install_path": "<absolute-path-to-this-skill-directory>",
  "log_enabled": true,
  "log_path": "antenna.log",
  "log_max_size_bytes": 10485760,
  "log_verbose": false,
  "mcs_enabled": false,
  "mcs_model": "sonnet",
  "inbox_enabled": false,
  "inbox_auto_approve_peers": [],
  "inbox_queue_path": "antenna-inbox.json",
  "allowed_inbound_sessions": ["agent:betty:main", "agent:betty:antenna"],
  "allowed_inbound_peers": ["<peer-a>", "<peer-b>"],
  "allowed_outbound_peers": ["<peer-a>", "<peer-b>"],
  "rate_limit": {
    "per_peer_per_minute": 10,
    "global_per_minute": 30
  },
  "security": {
    "max_message_age_seconds": 300,
    "max_future_skew_seconds": 60
  }
}
```

Key fields:
- `relay_agent_model` — use a full provider/model ID, not a local alias
- `local_agent_id` — used by local CLI conveniences when expanding bare names to full session keys like `agent:<id>:main`
- `install_path` — absolute path to this skill directory
- `allowed_inbound_sessions` — inbound delivery allowlist (full session keys, e.g. `agent:betty:main`)
- `allowed_inbound_peers` / `allowed_outbound_peers` — peer allowlists
- `rate_limit.*` — inbound abuse controls
- `security.max_message_age_seconds` / `max_future_skew_seconds` — freshness-window tolerance (defaults shown; omit the block to use defaults)

### `antenna-peers.json`

```json
{
  "<your-host-id>": {
    "url": "https://<your-reachable-hostname>",
    "token_file": "secrets/hooks_token_<your-host-id>",
    "peer_secret_file": "secrets/antenna-peer-<your-host-id>.secret",
    "exchange_public_key": "age1...",
    "agentId": "antenna",
    "display_name": "My Host",
    "self": true
  },
  "<remote-peer-id>": {
    "url": "https://<remote-reachable-hostname>",
    "token_file": "secrets/hooks_token_<remote-peer-id>",
    "peer_secret_file": "secrets/antenna-peer-<remote-peer-id>.secret",
    "exchange_public_key": "age1...",
    "agentId": "antenna",
    "display_name": "Remote Host"
  }
}
```

Key fields:
- `url` — reachable HTTPS hook base URL
- `token_file` — bearer token for that peer
- `peer_secret_file` — per-peer runtime identity secret
- `exchange_public_key` — peer's `age` public key for Layer A exchange
- `self` — marks the local host entry

## Usage

### Send a message

```bash
scripts/antenna-send.sh <peer> "Your message here"
antenna msg <peer> "Your message here"                              # recipient resolves target session
antenna msg <peer> --subject "Config sync" "Here's the block you need..."
antenna msg <peer> --session "agent:<agent-id>:mychannel" "Your message"  # explicit session override
echo "Long message body..." | antenna send <peer> --stdin
antenna send <peer> --dry-run "Test message"
```

> **Session resolution:** When `--session` is omitted, `target_session` is left out of the
> envelope entirely. The recipient resolves from their own `default_target_session` config.
> You don't need to know another host's internal session layout.

### Peer pairing (interactive wizard)

```bash
antenna pair                          # Full interactive wizard
antenna pair --peer-id myserver       # Pre-fill peer ID
```

The wizard walks through keypair generation, public key sharing, optional ClawReef invite, bundle creation, optional bundle email send when mail tooling is available, exchange, connectivity test, and first message — with Next/Skip/Quit at each step. Also auto-offered at the end of `antenna setup`.

### Peer onboarding / bootstrap exchange (manual)

Preferred encrypted flow:

```bash
antenna peers exchange keygen
antenna peers exchange pubkey
antenna peers exchange initiate <peer-id> --pubkey <age1...> --print
antenna bundle verify <bundle-file>                         # read-only: decrypt & sanity-check before importing
antenna bundle verify <bundle-file> --json                  # machine-readable verdict
antenna bundle verify <bundle-file> --force-expired         # inspect a past-expiry bundle without importing
antenna bundle verify <bundle-file> --no-decrypt            # treat file as already-decrypted bundle JSON
antenna peers exchange import <bundle-file>                 # refuses expired bundles
antenna peers exchange import <bundle-file> --force-expired # disaster-recovery override
antenna peers exchange reply <peer-id>
```

Optional direct-send convenience (email):

```bash
antenna peers exchange initiate <peer-id> \
  --pubkey <age1...> \
  --email someone@example.com \
  --send-email [--account <himalaya-account-name>]
```

Legacy/manual fallback:

```bash
antenna peers exchange <peer-id> --export         # interactive TTY only; refuses to pipe secrets
antenna peers exchange <peer-id> --import <file>
antenna peers exchange <peer-id> --import-value <hex>
```

Peer registry updates:

```bash
antenna peers add <peer-id> --url <https-url> --token-file <path>   # first time only
antenna peers add <peer-id> --url <new-url> --force                 # update existing: merges only the flags you pass
```

Notes:
- Secure Layer A requires `age` and `age-keygen`
- Export never materializes plaintext bundle JSON on disk; `jq` streams directly into `age`. Import decrypts to a temp file but cleans up on return, validation failure, preview failure, write failure, and `Ctrl-C` (SIGINT/SIGTERM).
- `antenna bundle verify <file>` is a read-only sanity check — it decrypts in place, validates shape / endpoint URL / freshness, and prints a safe summary (never the raw hooks token or identity secret). It never writes to `antenna-peers.json` or `antenna-config.json`. Use it before `peers exchange import` when a bundle comes from an untrusted or unclear channel.
- Expired bundles are refused by default; use `--force-expired` only for genuine disaster recovery.
- Optional direct-send requires `himalaya`. The sender email is resolved from your Himalaya TOML config (`${HIMALAYA_CONFIG:-~/.config/himalaya/config.toml}`, `[accounts.<name>] email = "..."`) — there is no `antenna@localhost` fallback and no free-text `From:` override. Pass `--account <name>` to pick a specific configured account; interactive flows use selection-only UX.
- Email is convenience transport only, not part of the trust model.
- Import shows a preview and asks before allowlist changes unless `--yes` is used.
- `antenna peers add` refuses to overwrite an existing peer without `--force`; `--force` does a field-level merge so unspecified peer fields (including `exchange_public_key`, `self`, and any future metadata) are preserved.
- `antenna peers remove` prunes peer-scoped allowlist entries (`allowed_inbound_peers`, `allowed_outbound_peers`, peer-scoped inbound sessions) so removing a peer does not leave stale allowlist debris behind. Peer secret files are intentionally left in place; secret deletion is an explicit operator action (see `antenna doctor` section 6b for secrets-hygiene warnings about leftover files).

### Session allowlist management

```bash
antenna sessions list                             # Show allowed inbound session targets
antenna sessions add antv3                        # Bare name → auto-expanded to agent:<local>:antv3
antenna sessions add "agent:marie:lab1"            # Cross-agent: use full session key
antenna sessions remove antv3                     # Remove (bare names are expanded)
antenna sessions remove "agent:betty:main" --force # Core sessions need --force
```

Controls which session targets inbound messages can request via `allowed_inbound_sessions` in `antenna-config.json`.

**Convention: full session keys everywhere.** The allowlist stores full keys like `agent:betty:main` and `agent:marie:lab1`. The relay requires full keys from senders — bare names are rejected. The CLI auto-expands bare names to `agent:<local_agent>:<name>` for convenience when adding/removing, but the stored value is always the full key.

Core sessions (`agent:<local>:main`, `agent:<local>:antenna`) are protected from removal unless `--force` is used. Supports batch add/remove.

### Health and status

```bash
antenna doctor
antenna uninstall --dry-run
antenna uninstall
antenna peers list
antenna peers test <id>
antenna status
antenna log --tail 50
```

`antenna doctor` includes warn-only drift audits that complement the hard config/permission checks:

- **Section 1b — Peer-State Drift.** Audits `allowed_inbound_peers`, `allowed_outbound_peers`, and peer-scoped inbound sessions in `antenna-config.json` against `antenna-peers.json`. Orphan peer IDs (allowlist entries for peers that no longer exist) are warnings, never failures. Catches the `nexus` / `bruce`-era debris class automatically.
- **Section 6b — Secrets Directory Hygiene.** File-side counterpart to 1b. Warns on orphan peer-scoped secret / token files in `secrets/` (`antenna-peer-<id>.secret`, `hooks_token_<id>`, `peer_secret_<id>` whose `<id>` is no longer in `antenna-peers.json`), backup-pattern leftovers (`.bak*`, `.backup*`, `~`, `.old`), loose `secrets/` directory permissions (target `700`), loose per-file permissions on secret-shaped files (target `600`), and unknown-shape files inside `secrets/`.

### Testing

```bash
antenna test <model>
antenna test-suite --tier A
antenna test-suite --model <m>
antenna test-suite --models "<m1>,<m2>"
antenna test-suite --report
```

Model tests emit a per-run `TEST_NONCE` and match both success and pre-delivery rejections by that nonce, so parallel or historical runs cannot contaminate each other's verdicts and auth / peer / rate-limit failures return promptly instead of waiting for the full timeout. Tests drive gateway config through the CLI/helper path with a single batched restart rather than restarting per operation.

### Inbox (optional approval queue)

When `inbox_enabled` is `true` in config, inbound messages from peers not in `inbox_auto_approve_peers` are queued for review instead of being relayed immediately. Auto-approved peers bypass the queue and relay instantly (current behavior).

```bash
antenna inbox                        # list pending messages (table view)
antenna inbox count                  # pending count (for heartbeat/cron checks)
antenna inbox show <ref>             # full message body for a ref
antenna inbox approve all            # approve everything pending
antenna inbox approve 1,3,5-7       # selective approval (commas and ranges)
antenna inbox deny all               # reject everything pending
antenna inbox deny 2,4               # selective denial
antenna inbox drain                  # deliver all approved (gateway sessions.send), remove denied
antenna inbox clear                  # purge all processed items
```

**Delivery flow:** `antenna inbox drain` iterates every approved item and delivers each via `openclaw gateway call sessions.send` (the same gateway RPC the relay path uses). On success, the item transitions to `delivered`; on RPC failure it transitions to `failed` with `last_error` recorded for triage. Denied items are removed. The script returns non-zero if any delivery failed, prints a one-line summary on stderr, and logs each per-ref result to `antenna.log`. The calling agent's role is a single `exec` of `antenna inbox drain` — no MCP tool calls required.

**Configuration:**
```json
{
  "inbox_enabled": false,
  "inbox_auto_approve_peers": ["trusted-peer-id"],
  "inbox_queue_path": "antenna-inbox.json"
}
```

Notes:
- Disabled by default — existing behavior is unchanged
- Auto-approve list lets trusted peers bypass the queue (progressive trust)
- Queue file is local runtime state (gitignored)
- Ref numbers auto-increment and support range selection
- The relay agent now uses only `write` + `exec`; it never calls `sessions_send` directly. Drain also stays in script-only territory — it shells out to `openclaw gateway call sessions.send`, so cron jobs can drain the queue without an agent in the loop.

**Heartbeat / cron integration:**

Add to your `HEARTBEAT.md`:
```markdown
## Antenna inbox check
- Run: `antenna inbox count`
- If > 0: run `antenna inbox list` and mention it
```

Or set up a cron job for automated handling:
```
Check antenna inbox. If there are pending messages from peers
in [trusted-peer-id], approve and drain them. For anything else,
summarize the queue and ask me.
```

**Conversational usage:** Ask your assistant "any Antenna messages waiting?" — it can run `antenna inbox list`, you review, then say "approve 1 and 3, deny 2" and it handles the rest.

## ClawReef — Peer Discovery

[clawreef.io](https://clawreef.io) is the optional community registry for Antenna hosts:

- **Discover peers** — browse and search the directory
- **Send invites** — ClawReef delivers them via Antenna to the recipient's default session
- **Accept & pair** — accepting an invite starts the normal `antenna pair` flow locally

ClawReef stores webhook credentials (`hooksToken`, `identitySecret`) for push delivery alongside public keys and endpoints — standard webhook-provider behavior. It does not store messages, private age keys, or message content. All trust decisions remain local to Antenna.

The pairing wizard (`antenna pair`) offers ClawReef invites as an alternative to manual encrypted exchange. Setup also displays ClawReef info after completion.

## Security Notes

- Relay agent is script-first and non-interpreting
- Inbound sessions are allowlisted (full session keys only)
- Sender peer must be allowlisted on both inbound and outbound sides
- Per-peer identity secret can authenticate sender claims; comparison is constant-time
- Envelope marker guard rejects messages whose bodies or headers contain `[ANTENNA_RELAY]` / `[/ANTENNA_RELAY]`
- Message freshness window rejects stale or future-dated envelopes (defaults: 300s age, 60s future skew)
- Sender refuses to run without configured `self_id` (no `$(hostname)` fallback)
- Legacy raw-secret export refuses non-TTY output
- Encrypted bundle export never writes plaintext; encrypted bundle import cleans up plaintext on every exit path (return / fail / SIGINT / SIGTERM)
- Expired encrypted bundles are refused at import (`--force-expired` is the disaster-recovery override)
- Email send for bootstrap/pubkey resolves sender address from Himalaya TOML config; no `antenna@localhost` fallback, no free-text `From:` override
- Tokens and secrets are file-backed and should be `chmod 600`; `antenna status` audits permissions
- Relay temp files are created with `umask 077`, chmod 0600, and shredded before unlink on cleanup
- Setup preserves an existing gateway `hooks.token` rather than overwriting it
- Relayed content is framed as potentially untrusted input
- Rate limiting throttles inbound bursts; transaction locking protects inbox and rate-limit state under concurrent access

## Troubleshooting

- **Gateway won't start**: Run `antenna doctor`
- **Want a clean slate**: Run `antenna uninstall` (use `--dry-run` first if you want a preview)
- **401 Unauthorized**: wrong hook bearer token
- **403 Forbidden**: session prefix/agent restrictions or peer policy mismatch
- **Relay rejected**: peer not allowlisted, session not allowlisted, or identity secret mismatch
- **`Relay rejected: timestamp out of range (stale|future)`**: peer clock skew exceeds freshness window; sync clocks or widen `.security.max_message_age_seconds` / `.security.max_future_skew_seconds`
- **`Relay rejected: marker in body|headers`**: envelope-marker guard working as intended; rephrase or encode any literal `[ANTENNA_RELAY]` / `[/ANTENNA_RELAY]` content
- **`self-id not configured - run antenna setup`**: sender is missing host identity in `antenna-config.json`; there is no `$(hostname)` fallback
- **Encrypted exchange fails immediately**: `age` / `age-keygen` missing
- **`Bundle expired - refusing import`**: request a fresh bundle from the peer, or pass `--force-expired` only for disaster recovery. To inspect an expired bundle without importing, use `antenna bundle verify <file> --force-expired`.
- **`antenna bundle verify: decrypt failed`**: the bundle was encrypted for a different `age` public key than yours. Ask the peer to re-initiate against your current `antenna peers exchange pubkey`.
- **`antenna bundle verify: endpoint URL rejected`**: the bundle's `from_endpoint_url` is not a valid HTTPS URL (e.g. `main`, bare host). Refuse to import; ask the peer to regenerate after fixing their self-peer URL.
- **`antenna doctor: self-peer URL is not a valid URL`**: your own `self` peer entry has a malformed `url`. Fix it in `antenna-peers.json` or rerun `antenna setup` with a valid `--url <https://host>`. REF-1313 now rejects malformed URLs at input time, but stale pre-fix entries still need to be corrected.
- **`antenna doctor: orphan peer references in config allowlists`** (warning, section 1b): allowlists in `antenna-config.json` reference peer IDs that no longer exist in `antenna-peers.json`. Remove the stale IDs with `antenna peers remove <id>` on any current peer (which also prunes its allowlist entries), or edit `antenna-config.json` directly.
- **`antenna doctor: orphan secret file`** / **`stale backup file`** / **`secrets/ dir is not 700`** (warnings, section 6b): hygiene findings on the `secrets/` directory. None of these can authenticate a peer that isn't in the registry, but they are real leak-surface / drift signals. Move orphan files to `secrets.retired/` (or delete), rotate or remove `.bak*` leftovers, and run `chmod 700 secrets/` / `chmod 600 secrets/<file>` to tighten permissions.
- **`Email send fails: could not resolve email for account`**: add `email = "..."` under `[accounts.<name>]` in your Himalaya TOML config, or pass `--account <other>` to pick a configured account that has an `email` set
- **`Email send fails: himalaya not installed`**: install `himalaya` or fall back to sending the bundle file by hand
- **`Legacy export refused - not a TTY`**: `antenna peers exchange <peer> --export` must run in an interactive terminal; switch to `antenna peers exchange initiate` for automated or remote operator handoff
- **Message sent but not visible**: ensure `tools.sessions.visibility = "all"` and `tools.agentToAgent.enabled = true` on the receiver; the relay delivery wrapper uses gateway session delivery, which still depends on those settings. Also ensure `sandbox: { mode: "off" }` on the Antenna agent — sandboxed sessions silently clamp visibility to `tree`, blocking cross-agent delivery
- **Exec denied / allowlist miss**: ensure relay agent instructions use only simple commands (no `$(...)`, heredocs, or chaining); the `antenna-relay-deliver.sh` wrapper accepts a file path only
- **Repeated approval prompts**: ensure Antenna agent has `sandbox: { mode: "off" }` in registration. Default advice is **not** to set `tools.exec.security` or `tools.exec.ask` on the Antenna agent — explicit exec overrides cause silent relay failure (fixed in v1.2.14). If you've intentionally customized `tools.exec` on the agent, setup reruns now preserve your overrides instead of wiping them.
- **`antenna peers add` refuses to update an existing peer**: by design — pass `--force` to update fields on a paired peer; without it, the command refuses to clobber trust material

## File Inventory

```text
skills/antenna/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── antenna-config.example.json
├── antenna-peers.example.json
├── antenna-peers.json
├── antenna-config.json
├── antenna.log
├── install.sh
├── bin/
│   └── antenna.sh
├── scripts/
│   ├── antenna-send.sh
│   ├── antenna-relay.sh
│   ├── antenna-relay-deliver.sh         # v1.4+ — canonical single-call deliver wrapper
│   ├── antenna-relay-file.sh           # internal file-based relay adapter
│   ├── antenna-relay-exec.sh            # v1.1.6 — base64 wrapper (legacy fallback)
│   ├── antenna-pair.sh                  # v1.1.9 — interactive peer pairing wizard
│   ├── antenna-health.sh
│   ├── antenna-peers.sh
│   ├── antenna-doctor.sh
│   ├── antenna-exchange.sh
│   ├── antenna-inbox.sh
│   ├── antenna-model-test.sh
│   └── antenna-test-suite.sh
├── references/
│   ├── ANTENNA-RELAY-FSD.md          # Relay architecture contract
│   └── issues.md                      # Known issues / gaps tracker
├── docs/                               # Repo-only (operator / historical)
│   ├── full-removal-checklist.md
│   ├── SECURITY-ASSESSMENT-v1.0.20.md
│   ├── RED-TEAM-REPORT-v1.0.4.md
│   ├── LAYER-A-SECRET-EXCHANGE-PLAN.md
│   └── SECRET-EXCHANGE-OPTIONS.md
└── agent/
    ├── AGENTS.md
    └── TOOLS.md
```

Notes:
- `antenna-config.json`, `antenna-peers.json`, and `antenna-inbox.json` are local runtime files (gitignored)
- `antenna-config.example.json` and `antenna-peers.example.json` are tracked reference templates

## Gateway / Agent Registration

`antenna setup` handles all of this automatically and is safe to rerun (e.g., after a `clawhub update`). Setup forces `sandbox.mode = "off"` and seeds a default `tools.deny` list only when absent. It preserves an existing gateway `hooks.token` and, on rerun, preserves any `tools.exec` overrides the operator has intentionally set on the Antenna agent.

On each host:
- agent `antenna` registered in OpenClaw config under `agents` with:
  - `agentDir` and `workspace` both pointing to the Antenna `agent/` directory
  - `sandbox: { mode: "off" }` (required — sandbox silently clamps session visibility, breaking cross-agent relay)
  - restrictive `tools.deny` (block web, browser, image, cron, memory tools)
  - **Default advice:** do not set `tools.exec.security` or `tools.exec.ask` on the Antenna agent — explicit exec overrides cause silent relay failure (see v1.2.14 changelog). If you've intentionally customized these, setup reruns now preserve your overrides rather than wiping them.
- `hooks.allowedAgentIds` includes `"antenna"`
- `hooks.allowedSessionKeyPrefixes` includes `"hook:antenna"`
- `tools.sessions.visibility` set to `"all"` (required for cross-session relay delivery)
- `tools.agentToAgent.enabled` set to `true`

## Support

- 📧 **Email:** [help@clawreef.io](mailto:help@clawreef.io)
- 🐛 **Issues:** [github.com/cshirley001/openclaw-skill-antenna/issues](https://github.com/cshirley001/openclaw-skill-antenna/issues)
- 🔒 **Security:** See [SECURITY.md](SECURITY.md)
