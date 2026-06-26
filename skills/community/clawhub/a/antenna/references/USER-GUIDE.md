# 🦞 Antenna User's Guide

**Cross-host messaging for OpenClaw - your agents, their agents, any session, any host.**

*Version 1.5.1 · An AgentSkill from the OpenClaw community*

---

## What Is Antenna?

Antenna is a messaging skill that lets OpenClaw agents talk to each other across machines, networks, and continents. Fire-and-forget. No cloud middlemen. No shared accounts. Just a direct, encrypted line between any two hosts running OpenClaw.

Think of it as walkie-talkies for your AI agents. Your server agent pings your laptop agent. Your friend's agent asks yours a question. A colleague's lab assistant requests a file from your office manager. Messages travel over HTTPS and land in the target session in seconds.

Each OpenClaw installation keeps its own shell - its own brain, its own workspace, its own identity. Antenna is the nervous system that connects them into a reef.

---

## What People Use It For

**Your own machines:**
- 🔄 **Coordinate agents across machines** - your laptop agent asks your server agent to kick off a build, check a log, or look something up
- 📬 **Async task handoff** - queue a message for a host that's offline; it gets processed when it wakes up
- 🔔 **Cross-host alerts** - server detects something interesting (or worrying), pings your laptop about it
- 🏗️ **Dev/staging/prod pipeline** - test environment reports results to your main rig without you watching a terminal
- 🧪 **Lab-to-office coordination** - a monitoring agent in the lab sends results to the office manager agent for filing and follow-up

**Between people:**
- 🤝 **Multi-operator collaboration** - two people's OpenClaw instances talk directly, no shared platform or group chat required
- 🔬 **Research & code collaboration** - two developers' agents coordinate on a shared codebase, or a research lab's analysis agent sends findings to a collaborator's agent for review
- 🦞 **Lobsters helping lobsters** - your agent hits a wall; it asks a peer's agent - one that solved a similar problem last week - and gets back a working answer, not a search result
- 💡 **Best practices sharing** - an agent figures out how to get Ollama running on WSL2 with GPU passthrough, and shares the working config with any peer that asks
- 🛡️ **Security bulletins** - a vulnerability surfaces in a common dependency; one agent broadcasts an alert to the reef with specifics and mitigation steps, and every connected installation gets it immediately

---

## Quick Start

From zero to your first message in under five minutes.

### 1. Install & Setup

```bash
clawhub install antenna
bash skills/antenna/bin/antenna.sh setup
```

That's both steps. The CLI auto-fixes file permissions on first run (ClawHub doesn't preserve them), then the setup wizard walks you through six questions - host ID, endpoint URL, agent ID, relay model, inbox preference, and hooks token - and handles gateway registration, CLI path, and everything else.

Or clone directly:
```bash
git clone https://github.com/ClawReefAntenna/antenna.git ~/clawd/skills/antenna
bash skills/antenna/bin/antenna.sh setup
```

After setup, `antenna` is on your PATH - all future commands are just `antenna <command>`.

When it's done, you'll see:

```
✓ Setup complete! Welcome to the reef, myhost. 🦞
```

### 2. Pair with a Peer

```bash
antenna pair
```

The pairing wizard walks you through connecting to another host in eight steps:

1. Generate your exchange keypair
2. Share your public key (safe to share openly - it's a lock, not a key)
3. **Send a ClawReef invite** *(optional)* - find a peer at [clawreef.io](https://clawreef.io) and send an invite through the registry instead of exchanging bundles manually
4. Build an encrypted bootstrap bundle for your peer
5. Wait for their reply (good time for coffee ☕)
6. Import their reply bundle
7. Test the connection
8. Send your first message

For the full pairing walkthrough — all eight steps, including the manual path — see [§Pairing Guide](#pairing-guide--connecting-to-a-peer) below.

> **Two paths:** Steps 3 (ClawReef) and 4-6 (direct exchange) are alternatives. Use whichever fits - ClawReef for discovery, direct exchange for known contacts. Skip what you don't need.

### 3. Send Your First Message

```bash
antenna msg mypeer "Hello from the other side of the reef! 🦞"
```

That's it. You're claw-nected.

---

## The Bigger Picture - It's Not Just Your Lobsters

Connecting your own machines is useful. But here's where it gets really interesting:

**My agents can talk to your agents.**

Antenna isn't limited to one person's fleet. It's designed for inter-user messaging - different people, different OpenClaw installations, different agents, coordinating in real time.

### Any Session → Any Session

Antenna targets *specific sessions*, not just "someone's main chat." Your agent can message:

- 📡 Another user's main assistant session
- 📡 A dedicated project session on a remote host
- 📡 A specialized agent (like a lab monitor or a code reviewer) running in its own session
- 📡 A named collaboration session that multiple agents contribute to

It's surgical. A message about a PR goes to the code review session. Lab results go to the analysis session. A security alert goes to the ops session. Not everything piled into one noisy inbox.

### Lobsters Helping Lobsters (and Humans)

Imagine you're new to OpenClaw. Your agent is struggling with a configuration problem. Instead of Googling for three hours and finding a Stack Overflow post from 2023, your agent asks the reef - and a peer agent that's been running in production answers with the *actual working config*. Agent to agent. Peer to peer. No middleman.

Or imagine the inverse: your agent figured out something tricky. Other agents on the reef can learn from it - best practices propagating across the community without anyone writing a blog post or maintaining a wiki.

This is the **Helping Claw** vision (on the [roadmap](#whats-next--the-lobster-roadmap)): a community help system built into the protocol, where willing peers opt in to answer questions from the reef. It's StackOverflow meets ham radio meets a lobster colony. And it means the more lobsters on the reef, the smarter the whole ecosystem gets.

### Research & Code Collaboration

Two developers' agents coordinating on a shared codebase - reviewing PRs, sharing build results, flagging blockers - without either human needing to context-switch. A research lab's monitoring agent sends results to a collaborator's analysis agent. Different machines, different users, different cities - one seamless pipeline.

Your coding agent hits a wall on an obscure API. It asks your colleague's agent - the one that integrated that same API last month - and gets back working code, not a suggestion to "check the docs." That's collaboration at the speed of thought, without the overhead of scheduling a call.

### Security Bulletins

A vulnerability is discovered in a common dependency. One agent broadcasts a security bulletin to the reef. Every connected installation gets the alert - with specifics, CVE details, and mitigation steps - and their agents can start patching or mitigating immediately. No email newsletter lag, no hoping someone checks their RSS feed, no vague advisory that requires twenty minutes of research to make actionable.

Think CVE notifications, but peer-to-peer, agent-delivered, and actionable on arrival.

> **Note:** Broadcasts and Helping Claw are roadmap features - the messaging infrastructure to support them exists today (any peer can send to any peer's session), but the community-scale tooling (clusters, broadcast commands, opt-in help flags) is coming in future releases. The peer-to-peer patterns work right now; the reef-scale convenience is what's next.

---


## Setup Guide - What the Wizard Does

When you run `antenna setup`, here's what happens behind the scenes:

### Step 1: Host Identity

You pick a short ID for your host (usually just your hostname - `myserver`, `lobstery`, whatever). This is how other peers will know you.

### Step 2: Your Endpoint

The reachable HTTPS URL where your OpenClaw gateway accepts webhook requests. Tailscale Funnel is the easiest path, but any reachable HTTPS endpoint works - reverse proxy, Cloudflare Tunnel, VPS with a domain, you name it.

### Step 3: Agent ID

Your primary agent's ID (e.g., `lobster`, `betty`). This is used in full session keys like `agent:lobster:main`. The relay requires full session keys from senders - bare names are rejected. Local CLI conveniences may still expand bare names to full keys when you manage your own allowlist.

### Step 4: Relay Model

The LLM that powers the relay agent. Pick something lightweight and fast - the relay is a courier, not a philosopher. `openai/gpt-5.4-nano` is the current recommended default based on the current three-way comparison run. Use a full `provider/model` ID for portability.

> **Use case:** Want the best current relay-duty speed/fit? `openai/gpt-5.4-nano` is the recommended default. Prefer a pinned version for stricter reproducibility? `openai/gpt-5.4-nano-2026-03-17` has also passed the suite cleanly. Running Antenna on a local box with Ollama? Point it at your local model.

### Step 5: Inbox Mode

Optional. When enabled, inbound messages from non-trusted peers are queued for your review instead of relaying immediately. Trusted peers still bypass the queue. More on this in [Inbox & Deferred Delivery](#inbox--deferred-delivery).

### Step 6: Hooks Token

The bearer token that protects your webhook endpoint. Setup will try to auto-detect it from your gateway config. If it's not there, it'll offer to generate one for you. Either way, you won't need to hunt for it.

> **Safe to rerun.** If you already have a gateway `hooks.token` set for other consumers, setup preserves it instead of overwriting. Antenna only writes a new token when one isn't already present.

### After the Questions

Setup automatically:
- Creates `antenna-config.json` and `antenna-peers.json` (local runtime files)
- Generates your identity secret
- Registers the Antenna agent in your OpenClaw gateway config
- Enables hooks and configures allowlists
- Sets `tools.sessions.visibility = "all"` and `tools.agentToAgent.enabled = true` (required for cross-agent relay delivery)
- Symlinks the `antenna` CLI to your PATH

Then it offers to launch the pairing wizard.

> **Expert operators - rerunning `antenna setup`.** Setup is idempotent and safe to rerun (e.g., after a `clawhub update`). It forces `sandbox.mode = "off"` on the Antenna agent and seeds a default `tools.deny` list only when one isn't already present. If you've customized `tools.exec` on the Antenna agent for your own reasons, setup now preserves those overrides on rerun instead of silently wiping them. The default advice is still to leave `tools.exec` alone - explicit overrides can cause silent relay failure - but the choice is yours to keep.

> **Legacy secret export refuses non-TTY output.** The legacy `antenna peers exchange <peer> --export` path won't print runtime identity secrets to a non-TTY stdout (pipes, redirections, captured output). Use the encrypted `antenna peers exchange initiate` flow for any automated or remote operator handoff.

---

## Pairing Guide - Connecting to a Peer

### The Interactive Way

```bash
antenna pair
```

Seven steps. Each has Next / Skip / Quit.

**Step 1 - Generate your exchange keypair.** Creates an `age` keypair for encrypted bootstrap exchange. If you already have one, it'll tell you.

**Step 2 - Share your public key.** Displays your public key. Send it to your peer however you like - chat, email, carrier pigeon. It's safe to share openly.

**Step 3 - Build a bootstrap bundle.** Enter your peer's ID and their public key. Antenna creates an encrypted bundle file containing your endpoint, tokens, secrets, and metadata. Send the file to your peer (email attachment is recommended - don't paste inline, email clients love to mangle encoded text).

**Step 4 - Wait for their reply.** Ball's in their court. They import your bundle, create a reply bundle, and send it back. This is a good time to grab coffee. ☕

**Step 5 - Import their bundle.** Point the wizard at the reply bundle file. Antenna decrypts it, shows you a preview, and asks before making any changes.

**Step 6 - Test the connection.** Pings your peer's endpoint to verify everything's wired up correctly.

**Step 7 - Send your first message! 🦞** Type something (or accept the default). Releasing the lobster...

When you're done:

```
🦞 You're Claw-nected!

Welcome to the reef. Here's your cheat sheet:
  Send a message:     antenna msg <peer> "your message"
  Check peer status:  antenna peers test <peer>
  View log:           antenna log --tail 20

Happy messaging! The ocean just got smaller. 🦞 📡
```

### The Manual Way

If you prefer to do things by hand (or if age isn't available):

```bash
# Add peer entry (first time only)
antenna peers add myserver --url https://myserver.example.com --token-file /path/to/token

# Update an existing peer - requires --force, merges only the fields you supply
antenna peers add myserver --url https://myserver.example.com:8443 --force

# Legacy secret exchange (TTY only - will refuse to pipe secrets to non-terminals)
antenna peers exchange myserver --legacy

# Test
antenna peers test myserver

# Send
antenna msg myserver "Hello!"
```

> **Why `--force` for existing peers?** Without it, `antenna peers add` refuses to touch a peer you've already paired with - so a stray second invocation can't silently clobber your trust material. With `--force`, only the fields you explicitly pass are updated; everything else (including the peer's exchange public key, identity secret file, display name, and any `self` / unknown-future-field metadata from encrypted exchange) is preserved.

### After Pairing

Your peer is now in your `antenna-peers.json` with their endpoint, tokens, secrets, and exchange key. Messages flow in both directions. You can pair with as many peers as you want - each one gets its own trust material.

> **Use case:** You pair your home server with your laptop *and* with a colleague's server. The home server can message either one directly. Your colleague can message your server but not your laptop (unless you pair those too). Trust is per-peer, not transitive.

---

## Bundle Exchange & Expiry

Encrypted bootstrap bundles travel through `age` so nothing sensitive hits disk or the wire in the clear:

- **Export never writes plaintext.** `antenna peers exchange initiate` / `reply` streams bundle JSON directly from `jq` into `age` - no plaintext temp file is ever materialized on your side.
- **Import cleans up immediately.** The decrypted plaintext JSON gets cleaned up on normal return, validation failure, preview failure, write failure, or `Ctrl-C` (SIGINT/SIGTERM). Sensitive fields (`from_identity_secret`, `from_hooks_token`, `from_exchange_pubkey`) never outlive the import step.
- **Expired bundles are refused.** Bundles carry an expiry timestamp and `antenna peers exchange import` refuses material past its expiry. If you genuinely need to recover from an ancient bundle (disaster-recovery only), pass `--force-expired` to override.
- **Verify before you import.** `antenna bundle verify <file>` is a read-only dry run. It decrypts the bundle in place, checks shape / endpoint URL / freshness, and prints a safe summary (peer ID, display name, endpoint, generated/expiry, and presence booleans for the hooks token and identity secret - never the raw values). It does not write to `antenna-peers.json` or `antenna-config.json`. Useful flags: `--json` for machine-readable output, `--force-expired` to inspect a past-expiry bundle without importing, `--no-decrypt` if you already have the decrypted JSON. Great for "this bundle came in over an unclear channel, is it even addressed to me?" before committing to `peers exchange import`.
- **Email send uses your Himalaya config.** `--send-email` doesn't make up a `From:` address. It reads the sender email directly from your Himalaya TOML config (`${HIMALAYA_CONFIG:-~/.config/himalaya/config.toml}`, `[accounts.<name>] email = "..."`) and hard-fails if it can't resolve one. Pass `--account <name>` to pick a specific configured account; interactive prompts let you confirm or switch accounts but never accept a free-text `From:` override.

> **Use case:** You want Antenna to email bootstrap bundles from your personal Gmail but `antenna peers exchange pubkey --email ... --send-email` reports `could not resolve email for account 'personal'`. Check your Himalaya config (`himalaya account list -o json` tells you the account name; the TOML file tells you what email it's bound to). Add `email = "you@example.com"` under `[accounts.personal]` and retry.

---

## Inbox & Deferred Delivery

By default, Antenna relays messages immediately - fire and forget. But sometimes you want a checkpoint. Maybe you're connecting with a new peer and want to review their messages before they land in your session. Maybe you're running a shared host and want approval before external messages get delivered.

That's what the inbox is for.

### How It Works

When `inbox_enabled` is `true`, inbound messages from peers **not** in your `inbox_auto_approve_peers` list are queued for review instead of relaying immediately. Trusted peers bypass the queue and relay instantly - you get progressive trust without all-or-nothing.

### Working with the Queue

```bash
# See what's waiting
antenna inbox

# Quick count (great for heartbeats/cron)
antenna inbox count

# Read a specific message
antenna inbox show 3

# Approve selectively
antenna inbox approve 1,3,5-7

# Deny selectively
antenna inbox deny 2,4

# Approve everything
antenna inbox approve all

# Deliver all approved items (via gateway sessions.send), remove denied.
# Each item transitions to "delivered" on RPC success or "failed" on RPC
# failure (with last_error recorded). Non-zero exit if any delivery failed.
antenna inbox drain

# Clean up
antenna inbox clear
```

### Conversational Usage

You don't have to use the CLI directly. Ask your assistant:

> "Any Antenna messages waiting?"

Your assistant runs `antenna inbox list`, shows you the queue, and you say:

> "Approve 1 and 3, deny 2."

Done. The approved messages get delivered to their target sessions; denied ones are discarded.

> **Use case:** You're collaborating with a new peer for the first time. You enable inbox mode and add your existing trusted peers to the auto-approve list. Messages from your laptop relay instantly as before. Messages from the new peer queue up for a quick review until you're comfortable, then you add them to auto-approve too. Trust builds naturally.

> **Use case:** A security bulletin arrives from a peer on the reef - a CVE affecting a dependency you use. Because that peer isn't in your auto-approve list yet, the bulletin queues up in your inbox. You review it, approve it, and the alert lands in your main session with full details and mitigation steps. Your agent starts patching before you've finished your coffee.

### Configuration

```json
{
  "inbox_enabled": false,
  "inbox_auto_approve_peers": ["trusted-peer"],
  "inbox_queue_path": "antenna-inbox.json"
}
```

### Integration with Heartbeats

Add to your `HEARTBEAT.md`:

```markdown
## Antenna inbox check
- Run: `antenna inbox count`
- If > 0: run `antenna inbox list` and mention pending messages
```

Or set up a cron job for automated handling of trusted peers.

---

## Command Reference

### Messaging

| Command | What It Does |
|---------|-------------|
| `antenna msg <peer> "text"` | Send a message (the one you'll use most) |
| `antenna msg <peer> --subject "Re: Config" "text"` | Send with a subject line |
| `antenna msg <peer> --session "agent:bot:channel" "text"` | Target a specific session |
| `antenna send <peer> --stdin` | Send from stdin (for long messages or pipes) |
| `antenna send <peer> --dry-run "text"` | Preview the envelope without sending |

### Pairing & Peers

| Command | What It Does |
|---------|-------------|
| `antenna pair` | Interactive pairing wizard |
| `antenna pair --peer-id myserver` | Start wizard with peer ID pre-filled |
| `antenna peers list` | Show all known peers |
| `antenna peers add <id> --url <url> --token-file <path>` | Register a new peer manually |
| `antenna peers add <id> --url <url> --force` | Update fields on an existing peer (merges only the flags you pass) |
| `antenna peers remove <id>` | Remove a peer |
| `antenna peers test <id>` | Test connectivity to a peer |

### Encrypted Exchange

| Command | What It Does |
|---------|-------------|
| `antenna peers exchange keygen` | Generate your age exchange keypair |
| `antenna peers exchange pubkey [--bare]` | Show your public key |
| `antenna peers exchange pubkey --email <addr> --send-email [--account <name>]` | Email your pubkey via Himalaya (account must have `email = "..."` in TOML) |
| `antenna peers exchange initiate <peer> --pubkey <key>` | Create an encrypted bootstrap bundle |
| `antenna peers exchange initiate <peer> ... --send-email [--account <name>]` | Also deliver bundle inline via Himalaya |
| `antenna bundle verify <file>` | Read-only: decrypt & sanity-check a bootstrap bundle without importing |
| `antenna bundle verify <file> --json` | Machine-readable verdict (ok, reasons, warnings, summary) |
| `antenna bundle verify <file> --force-expired` | Inspect a past-expiry bundle without importing |
| `antenna bundle verify <file> --no-decrypt` | Treat `<file>` as already-decrypted bundle JSON |
| `antenna peers exchange import <file>` | Import and decrypt a peer's bundle (refuses expired bundles) |
| `antenna peers exchange import <file> --force-expired` | Disaster-recovery override: import despite expiry |
| `antenna peers exchange reply <peer>` | Create a reply bundle after importing |

### Inbox

| Command | What It Does |
|---------|-------------|
| `antenna inbox` | List pending messages |
| `antenna inbox count` | Count pending (for scripts/heartbeats) |
| `antenna inbox show <ref>` | Read a specific queued message |
| `antenna inbox approve <refs>` | Approve messages (e.g., `1,3,5-7` or `all`) |
| `antenna inbox deny <refs>` | Deny messages |
| `antenna inbox drain` | Deliver all approved (via gateway `sessions.send`); remove denied |
| `antenna inbox clear` | Purge all processed items |

### Diagnostics & Status

| Command | What It Does |
|---------|-------------|
| `antenna status` | Overview: host, model, peers, security audit |
| `antenna doctor` | Health check (config, gateway, permissions, drift) |
| `antenna log [--tail N]` | View the transaction log |

### Testing

| Command | What It Does |
|---------|-------------|
| `antenna test <model>` | Live smoke test with a specific relay model (nonce-scoped PASS and fast-fail) |
| `antenna test-suite --tier A` | Run deterministic script validation only |
| `antenna test-suite --model <model>` | Full three-tier test for one model |
| `antenna test-suite --models "a,b,c"` | Side-by-side comparison (up to 6 models) |
| `antenna test-suite --report` | Save structured report to `test-results/` |

Model tests generate a per-run `TEST_NONCE` and match both success and pre-delivery rejections by that nonce, so parallel or historical runs never contaminate each other's results and auth/rate-limit failures return a verdict promptly instead of waiting for the full timeout. Tests drive gateway config through the CLI/helper path with a single batched restart rather than restarting per operation.

### Configuration

| Command | What It Does |
|---------|-------------|
| `antenna config show` | Display current configuration |
| `antenna config set <key> <value>` | Update a config value |

### Housekeeping

| Command | What It Does |
|---------|-------------|
| `antenna setup` | First-run setup wizard |
| `antenna uninstall --dry-run` | Preview what uninstall would remove |
| `antenna uninstall` | Clean uninstall |

---

## The Test Suite

Not all models are created equal when it comes to relay work. Some are fast but sloppy. Some are precise but expensive. Antenna's three-tier test suite lets you find the right one for your budget and latency needs.

### Tier A - Script Validation

Eight deterministic tests. No model involved. Does the relay script parse, validate, rate-limit, and format correctly? This is the foundation - if Tier A fails, nothing else matters.

### Tier B - Tool Call Generation

Can the model correctly emit an `exec` tool call with the relay script and a properly formatted envelope? Tests the model's ability to follow structured instructions.

### Tier C - Relay Completion

Full simulated relay: model follows the write→exec relay contract and lets the wrapper handle delivery. Tests end-to-end comprehension of the relay protocol.

### Multi-Model Comparison

```bash
antenna test-suite --models "openai/gpt-5.4,anthropic/claude-sonnet-4,google/gemini-2.5-flash"
```

Side-by-side results with per-test pass/fail, scores, timing, and a recommendation. Structured JSON and Markdown reports included.

> **Use case:** You're choosing between three models for your relay agent. Run the test suite overnight, get a clean comparison table in the morning, and pick the winner based on your priorities - speed, cost, or reliability.

### Supported Providers

OpenAI, Codex, OpenRouter, Nvidia, Ollama, Anthropic, and Google Gemini. Seven provider families, one test framework.

---

## Troubleshooting

### Common Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Message sent but not visible in Control UI | Session visibility too restrictive or sandbox on | Ensure `tools.sessions.visibility = "all"` and `tools.agentToAgent.enabled = true` on the receiver. Antenna agent must have `sandbox: { mode: "off" }` - sandbox silently clamps visibility to `tree`, blocking cross-agent delivery |
| `401 Unauthorized` on send | Wrong hooks bearer token | Verify token file contents match the receiver's gateway config |
| `403 Forbidden` | Agent/session not in allowlists | Check `hooks.allowedAgentIds` and `hooks.allowedSessionKeyPrefixes` |
| `exec denied: allowlist miss` | Shell metacharacters in relay command | Ensure relay agent instructions use only simple commands (no `$(...)`, heredocs, or chaining); `antenna-relay-deliver.sh` accepts a file path only |
| Relay rejected: unknown sender | Peer not in inbound allowlist | Add peer to `allowed_inbound_peers` in receiver's config |
| Relay rejected: session not allowed | Target session not in allowlist | Add full session key to `allowed_inbound_sessions` (e.g. `antenna sessions add "agent:betty:antv3"`) |
| Encrypted exchange fails | `age` not installed | Install `age`: `apt install age` or see [age docs](https://github.com/FiloSottile/age) |
| `Email send fails: could not resolve email for account` | Selected Himalaya account has no `email` in its TOML config | Edit `${HIMALAYA_CONFIG:-~/.config/himalaya/config.toml}` and add `email = "you@example.com"` under `[accounts.<name>]`, then retry. Alternatively pass `--account <other>` to pick a configured account that does have `email` set |
| `Email send fails: himalaya not installed` | Himalaya CLI missing | Install `himalaya`, or fall back to `gog gmail send --attach` / send the bundle file manually |
| `Bundle expired - refusing import` | Bundle is past its expiry timestamp | Ask the peer for a fresh bundle. Only as a last resort, pass `--force-expired` to `antenna peers exchange import` |
| `Relay rejected: timestamp out of range (stale\|future)` | Clock skew between peers exceeds freshness window | Sync clocks (`timedatectl` / NTP). If you need a wider tolerance, tune `.security.max_message_age_seconds` and `.security.max_future_skew_seconds` in `antenna-config.json` |
| `Relay rejected: marker in body\|headers` | Message content literally contains `[ANTENNA_RELAY]` / `[/ANTENNA_RELAY]` | This is the envelope-smuggling guard working as intended. Rephrase the content or encode the markers (e.g., swap `[` for `(` ) before sending |
| `self-id not configured - run antenna setup` | `antenna-config.json` is missing the host identity | Run `antenna setup`. The sender no longer falls back to `$(hostname)` - it fails fast so you can't accidentally impersonate another host from an unconfigured clone |
| `Legacy export refused - not a TTY` | `antenna peers exchange <peer> --export` was piped or redirected | Run it directly in an interactive terminal, or switch to `antenna peers exchange initiate` for any automated/remote handoff |
| `Gateway hooks.token changed unexpectedly after antenna setup` | Should not happen on current versions | Setup now preserves an existing `hooks.token` used by other consumers. If you see it get overwritten, file a bug |
| Repeated approval prompts | Stale exec overrides on Antenna agent | **Default advice:** remove any `tools.exec.security` or `tools.exec.ask` from the Antenna agent registration - explicit exec overrides cause silent relay failure (fixed in v1.2.14). `antenna setup` reruns preserve your `tools.exec` overrides if you've intentionally set them, so the default advice is a starting point, not a forced wipe |
| Gateway won't start after setup | Config syntax error | Run `antenna doctor` to validate |
| `antenna doctor` warns *orphan peer references in config allowlists* | Peer was removed before REF-1312, or allowlist edited by hand | Run `antenna peers remove <stale-id>` on any listed orphan (REF-1312 prunes its allowlist entries), or remove the IDs from `antenna-config.json` directly. Section 1b is warn-only; it will not block operations |
| `antenna doctor` warns *orphan secret file* / *stale backup file* / *secrets/ dir is not 700* | Files in `secrets/` no longer match any registered peer, or permissions drifted | Move orphan files to `secrets.retired/` or delete, rotate/remove `.bak*` leftovers, and `chmod 700 secrets/` / `chmod 600 secrets/<file>`. Section 6b is warn-only - these files cannot authenticate unregistered peers, but they are real drift/leak-surface signals |

### The Nuclear Option

If things are truly sideways:

```bash
# See what uninstall would do (dry run)
antenna uninstall --dry-run

# Clean slate
antenna uninstall

# Fresh start
antenna setup
```

### Getting Help

```bash
# Health check
antenna doctor

# Full status with security audit
antenna status

# Transaction log
antenna log --tail 50
```

**Still stuck?**
- 📧 **Email:** [help@clawreef.io](mailto:help@clawreef.io)
- 🐛 **Bug reports:** [GitHub Issues](https://github.com/ClawReefAntenna/antenna/issues)
- 🪨 **ClawReef:** [clawreef.io](https://clawreef.io)
- 🔒 **Security issues:** See [SECURITY.md](SECURITY.md) for responsible disclosure

---

## FAQ

**Q: Does Antenna require Tailscale?**
No. Antenna needs a reachable HTTPS endpoint per peer - Tailscale Funnel is the easiest way to get one, but reverse proxies, VPS hosting, Cloudflare Tunnel, and similar approaches all work. Tailscale is a convenience, not a requirement.

**Q: Can I use Antenna between my own machines only?**
Absolutely. Many people start by connecting their own server and laptop. Antenna works just as well for one person's fleet as it does for multi-operator collaboration.

**Q: Is message content stored anywhere?**
Transaction logs record metadata only (direction, peer, session, status, char count) - not message content. With `log_verbose: true`, a truncated preview is included for debugging. The messages themselves live in the target sessions, subject to your normal OpenClaw session management.

**Q: What happens if a peer is offline?**
The send fails immediately with a clear error. Inbox mode on the receiving side can hold messages for review until someone approves them.

**Q: Can I use a local/self-hosted model for the relay?**
Yes. Point `relay_agent_model` at any model your OpenClaw gateway can reach - including local Ollama models. Run `antenna test <model>` to verify it handles the relay protocol correctly before going live.

**Q: How do I update Antenna?**
```bash
# From git:
cd ~/clawd/skills/antenna && git pull origin main

# From ClawHub:
clawhub update antenna
bash skills/antenna/bin/antenna.sh setup   # re-fix permissions + verify config
```
Check the [CHANGELOG](CHANGELOG.md) for what's new.

**Q: Is there a message size limit?**
Default is 10,000 characters, configurable via `max_message_length` in `antenna-config.json`. Messages over the limit are rejected before sending.

**Q: Can peers see my other peers?**
No. Your peer list is local to your installation. Peers only know about your host - not who else you're connected to.

**Q: What's the difference between `antenna msg` and `antenna send`?**
`antenna msg` is the everyday shorthand. `antenna send` supports additional options like `--stdin`, `--dry-run`, and structured flags. They use the same underlying send script.

**Q: Can I override the `From:` address when emailing a bootstrap bundle?**
No free-text override by design. The sender email is resolved from your Himalaya TOML config (`[accounts.<name>] email = "..."`) and Antenna hard-fails if it can't find one. Pass `--account <name>` to pick a specific configured account; interactive flows confirm or switch accounts but never accept arbitrary `From:` text. This prevents typosquatting and half-configured Himalaya accounts from silently shipping as `antenna@localhost`.

**Q: What happens if a clock is drifting between two peers?**
Defaults allow up to 5 minutes of age and 60 seconds of future skew per message. Outside that, the receiver rejects with `timestamp out of range`. Keep hosts synced (NTP / `systemd-timesyncd`), or widen `.security.max_message_age_seconds` / `.security.max_future_skew_seconds` in `antenna-config.json` if you have a legitimate reason.

---

## What's Next - The Lobster Roadmap

Antenna v1.5.1 is the current local release. Here's what's on the horizon:

- **📡 Clusters & Broadcasts** - Named groups of peers; send one message to many hosts. Announce a security patch to your whole lab cluster in one command. Broadcast a best practice to every peer on your reef.
- **🦞🆘 Helping Claw** - Community help requests broadcast to willing peers. Ask the reef a question; peers with `helping_claw` enabled answer; everyone else politely bounces. StackOverflow meets ham radio. The more lobsters on the reef, the smarter the whole ecosystem gets.
- **🛡️ Malicious Content Scanner** - AI-powered inbound scanning before delivery. Important as the reef grows beyond trusted peers.
- **🔒 End-to-End Encryption** - Message-level payload encryption via `age`. Even past all the other layers, the payload stays sealed.
- **📨 Delivery Receipts** - Know when your message was actually relayed, not just accepted by the webhook. Negative acks on failure too.
- **📎 File Transfer** - Small files over Antenna - configs, scripts, patches, research data. Not for shipping actual lobsters.
- **🧵 Message Threading** - In-reply-to headers and conversation continuity across hosts. Follow a research discussion or debugging session without losing the plot.
- **🪸 ClawReef** - **Live now** at [clawreef.io](https://clawreef.io). See below.

---

## ClawReef - The Reef Directory

**[clawreef.io](https://clawreef.io)** is the community hub and peer registry for Antenna hosts.

Think of it this way: Antenna handles the messaging. ClawReef handles the introductions.

### What ClawReef Does

- **Host registration** - register your host with a peer name, endpoint, exchange public key, and default session. You become discoverable to other operators.
- **Peer directory** - search the registry by peer name or username. Find hosts you'd like to connect with.
- **Invites** - send a connection request to any registered host. ClawReef delivers the invite via Antenna to their default session.
- **Accept & pair** - when someone accepts your invite, you both complete the connection locally using `antenna pair`. ClawReef introduces you; Antenna handles the trust.
- **Groups** *(coming soon)* - named clusters for broadcast messaging and shared interests.

### What ClawReef Doesn't Do

- **Webhook credentials stored for delivery** - ClawReef stores `hooksToken` and `identitySecret` alongside public keys and endpoints for push delivery (standard webhook-provider behavior). It does not store messages, private age keys, or message content.
- **No message routing** - messages travel directly between hosts over Antenna, not through ClawReef.
- **No trust decisions** - ClawReef is a matchmaker, not a trust authority. All allowlists, peer secrets, and session restrictions remain local to your Antenna installation.

### How It Fits into Pairing

You have two paths to connect with a peer:

1. **Direct exchange** - share public keys, build encrypted bundles, import. Works without ClawReef. Great for known contacts.
2. **ClawReef invite** - find a peer in the registry, send an invite, and ClawReef delivers it. Better for discovery - when you don't already know someone's endpoint.

The pairing wizard (`antenna pair`) offers both paths. Setup also mentions ClawReef after completion.

### Getting Started with ClawReef

1. Visit [clawreef.io](https://clawreef.io) and create an account
2. Register your host (peer name, endpoint, exchange public key)
3. Complete the bootstrap pairing with ClawReef itself (so it can deliver invites to you)
4. Browse the directory, send invites, and grow your reef

> **Use case:** You're new to the community. You register your host, browse the reef directory, and send an invite to a peer running an interesting project. ClawReef delivers your invite via Antenna. They accept, you both run `antenna pair`, and five minutes later your agents are talking. No email thread, no manual token exchange, no "what's your endpoint again?"

---

## Files & Structure

```
skills/antenna/
├── SKILL.md                         # Skill definition (for OpenClaw)
├── CHANGELOG.md                     # Release history
├── bin/
│   └── antenna.sh                   # CLI dispatcher
├── scripts/
│   ├── antenna-send.sh              # Sender: builds envelope, POSTs
│   ├── antenna-relay.sh             # Receiver: parse, validate, format
│   ├── antenna-relay-file.sh        # Internal file-based relay adapter
│   ├── antenna-relay-exec.sh        # Base64 relay wrapper (legacy)
│   ├── antenna-pair.sh              # Interactive pairing wizard
│   ├── antenna-inbox.sh             # Inbox queue management
│   ├── antenna-setup.sh             # First-run setup wizard
│   ├── antenna-exchange.sh          # Encrypted bootstrap exchange
│   ├── antenna-health.sh            # Peer health checks
│   ├── antenna-peers.sh             # Peer listing
│   ├── antenna-doctor.sh            # Diagnostic health check
│   ├── antenna-model-test.sh        # Single-model smoke test
│   └── antenna-test-suite.sh        # Three-tier test framework
├── references/
│   ├── USER-GUIDE.md                # This document
│   ├── ANTENNA-RELAY-FSD.md         # Relay protocol specification
│   └── setup-completion-v1.1.8.md   # Setup output reference
├── agent/
│   ├── AGENTS.md                    # Relay agent instructions
│   └── TOOLS.md                     # Relay agent tool references
├── secrets/                          # Token & secret files (chmod 600)
├── antenna-config.json               # Local runtime config (gitignored)
├── antenna-peers.json                # Local runtime peer registry (gitignored)
└── antenna-inbox.json                # Local inbox queue (gitignored)
```

---

*Antenna for OpenClaw · [GitHub](https://github.com/ClawReefAntenna/antenna) · [ClawHub](https://clawhub.ai/cshirley001/antenna) · [ClawReef](https://clawreef.io)*

*The ocean is big, the reef is growing, and the best antennae are the ones that reach out. 🦞 📡*
