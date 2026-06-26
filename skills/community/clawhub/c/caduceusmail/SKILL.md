---
name: caduceusmail
description: "☤CaduceusMail lets your OpenClaw automate an enterprise-level communications stack with one domain/mailbox combo."
homepage: https://github.com/lmtlssss/caduceusmail
metadata: {"openclaw":{"emoji":"☤","skillKey":"caduceusmail","requires":{"bins":["bash","node","python3","jq"],"env":["ENTRA_TENANT_ID","ENTRA_CLIENT_ID","ENTRA_CLIENT_SECRET","EXCHANGE_DEFAULT_MAILBOX","EXCHANGE_ORGANIZATION","ORGANIZATION_DOMAIN","CLOUDFLARE_API_TOKEN","CLOUDFLARE_ZONE_ID"]}}}
---

# ☤CaduceusMail 3.6.7

Inbox-reliability optimization engine: automates sender trust hardening, identity rotation, and scale-ready outreach/support flows designed to keep your mail out of junk.

☤CaduceusMail is a shippable skill for enterprise-grade alias/domain control on top of a single Microsoft 365 mailbox and Cloudflare DNS zone.

OpenClaw skill adapter for an audited `caduceusmail` release artifact vendored inside this skill. It manages M365 + Cloudflare mail/DNS without a runtime npm fetch.

## What this does

This skill is a thin adapter around the standalone `caduceusmail` package. On first use the wrapper:

1. Verifies the vendored tarball against a pinned SHA-512 integrity value in `vendor/caduceusmail-release.json`
2. Extracts the audited release into a skill-owned cache under `~/.local/share/caduceusmail-skill/toolchains`
3. Runs the CLI with a reduced environment and owner-only permissions on runtime state directories

It does not fetch code from npm at runtime, install a global package, or execute npm lifecycle scripts.

## First move

Run the doctor through the secure wrapper before you do anything theatrical.

```bash
bash {baseDir}/scripts/run.sh doctor --json
```

## Quick start

```bash
bash {baseDir}/scripts/run.sh bootstrap \
  --organization-domain "example.com" \
  --mailbox "ops@example.com" \
  --bootstrap-auth-mode device
```

## Daily headless run after bootstrap

```bash
bash {baseDir}/scripts/run.sh bootstrap \
  --organization-domain "example.com" \
  --mailbox "ops@example.com" \
  --skip-m365-bootstrap
```

## Lane operations

```bash
bash {baseDir}/scripts/run.sh provision-lane \
  --mailbox "ops@example.com" \
  --local "support" \
  --domain "support-reply.example.com"

bash {baseDir}/scripts/run.sh verify-lane \
  --mailbox "ops@example.com" \
  --alias-email "support@support-reply.example.com" \
  --domain "support-reply.example.com"

bash {baseDir}/scripts/run.sh retire-lane \
  --mailbox "ops@example.com" \
  --alias-email "support@support-reply.example.com"
```

## Hard Rules

* never send group emails from one operation
* never send one message to multiple recipients at once
* treat no-reply lanes as intentional non-receiving identities (no MX + SPF `-all` profile)
* delete defaults are reply-safe: aliases are retired with fallback continuity unless explicitly hard-removed

## What this skill can do

* bootstrap Graph and Exchange auth posture
* hand off Microsoft device-login flows for VPS/SSH setups through OpenClaw gateway/browser hooks
* audit credential and DNS posture
* optimize root mail records
* provision reply and no reply lanes under subdomains
* verify lane readiness
* retire lanes with reply continuity
* generate awareness snapshots and machine readable state artifacts

## OpenClaw runtime pattern

Prefer secret injection through `skills.entries.caduceusmail.env` over editing files. See `examples/openclaw.config.json5`.
The wrapper forwards only the CaduceusMail/OpenClaw/M365/Cloudflare variables it needs plus terminal/headless hints, so unrelated host secrets are not passed through by default.
External script resolution stays disabled unless `CADUCEUSMAIL_ALLOW_EXTERNAL_SCRIPT_RESOLUTION=1` is set explicitly.

## Security and Privilege Disclosure

This skill performs high-privilege operations by design:

* Microsoft Graph app role grants
* Exchange service principal and RBAC role assignments
* Exchange accepted-domain tuning (optional flags)
* Cloudflare DNS mutations for lane records

Runtime state artifacts are written under `~/.caduceusmail/intel` with owner-only permissions. Env/secret persistence remains opt-in in the underlying tool, and any persisted env file is expected to stay owner-readable only.
Use least-privilege credentials: a dedicated Entra service principal scoped to the required Graph/Exchange roles and a Cloudflare token limited to the target zone's DNS permissions.
