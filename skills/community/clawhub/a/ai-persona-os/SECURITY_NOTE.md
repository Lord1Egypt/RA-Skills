# Security Note — AI Persona OS

Some automated security scanners (e.g. VirusTotal Code Insight, ClawScan static analysis) may flag this skill due to heuristic pattern matching. This document explains why those flags are **false positives**.

## What scanners detect vs. what the code actually does

### "Crypto key handling patterns"
- **Trigger:** `scripts/security-audit.sh` contains regex patterns like `api_key`, `secret_key`, `access_token`, etc.
- **Reality:** This script *searches your workspace for accidentally leaked credentials*. It does not store, transmit, or handle any secrets. All checks are local `grep` scans with no network calls.
- **Trigger:** `examples/coding-assistant/KNOWLEDGE.md` references environment variable names like `YOUR_API_KEY` and `DATABASE_URL`.
- **Reality:** These are placeholder names in a documentation template — no actual credentials are present.

### "External API calls"
- **Trigger:** Code examples in `examples/coding-assistant/KNOWLEDGE.md` show a TypeScript `fetch()` pattern.
- **Reality:** This is an illustrative code snippet (`/api/endpoint` is not a real URL). No files in this skill make any network requests.
- **Trigger:** URLs to `jeffjhunter.com` and `aimoneygroup.com` appear in attribution footers.
- **Reality:** These are the author's homepage links in documentation — not API endpoints.

### "Eval or dynamic code execution"
- **Trigger:** Words like "execute," "execution," and "execute commands" appear frequently in documentation.
- **Reality:** These describe the *concept* of AI agent task execution within the persona framework. There are **zero** `eval()`, `exec()`, or dynamic code execution calls in any script.

## v1.8.0 additions (OpenClaw 5.x compatibility)

### "Reading sensitive config file" — `cat ~/.openclaw/openclaw.json`
- **Trigger:** The `route check` in-chat command (and the `configure Discord` flow) inspect `~/.openclaw/openclaw.json` with patterns like:
  ```
  exec: cat ~/.openclaw/openclaw.json | grep -E '"default"|"defaultAccount"|"target"|"requireMention"'
  ```
- **Reality:** The command **only greps for routing-related keys** (`default`, `defaultAccount`, `target`, `requireMention`). The `gateway.auth.token` is in the same file but is **never read, displayed, transmitted, or written by this skill**. The user already has read access to their own config — this is a read-only audit, not a privilege escalation.

### "Config file modification"
- **Trigger:** The `configure Discord` flow writes updated routing keys back to `~/.openclaw/openclaw.json` (with the user's explicit per-step approval).
- **Reality:** Only three specific keys are modified: `accounts.default`, `channels.discord.defaultAccount`, and `agents.defaults.heartbeat.target`. The auth token, model providers, and other secrets are not touched. Every write is gated by the OpenClaw Approve dialog — the user sees the exact diff before it commits.

### "Auth/credential string references"
- **Trigger:** SKILL.md and CHANGELOG.md mention `gateway.auth.token`, `accounts.default`, `DISCORD_TOKEN`, `SLACK_TOKEN`, etc.
- **Reality:** These are **config key names referenced in documentation** to help the user understand routing. The skill does not read, store, log, or transmit any token values. `DISCORD_TOKEN` / `SLACK_TOKEN` appear in `envVars` frontmatter declared as `required: false` — they're optional channel credentials the gateway uses, not the skill.

### "Docker image references"
- **Trigger:** v1.8.0 references `openclaw-sandbox:bookworm-slim` and recommends the user enable sandboxing.
- **Reality:** These are **documentation references** to OpenClaw's official sandbox image. The skill does not run, build, push, or pull any Docker images. Sandbox configuration is a recommendation, applied to `~/.openclaw/openclaw.json` by the user (with approval) if they choose.

### "Memory tool invocations" — `memory_search`, `memory_get`
- **Trigger:** v1.8.0 switched many file reads from `exec: cat MEMORY.md` to the dedicated `memory_get` / `memory_search` tools.
- **Reality:** These are **built-in OpenClaw 5.x tools** with explicit allow rules in the host policy. They read from the gateway's indexed memory store (`~/.openclaw/memory/<agentId>.sqlite`) — they do not make network calls or escape the workspace.

## Verification

You can verify this yourself:

```bash
# Confirm no eval/exec calls exist
grep -rn "eval\|exec(" scripts/ --include="*.sh"

# Confirm no network calls exist in scripts
grep -rn "curl\|wget\|nc \|netcat\|/dev/tcp" scripts/ --include="*.sh"

# Review the security audit script directly
cat scripts/security-audit.sh
```

## Questions?

If you have security concerns, please open an issue or contact the author directly.

- **Author:** Jeff J Hunter
- **Website:** https://jeffjhunter.com
