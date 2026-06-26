---
name: cloudways-integration
description: OpenClaw Cloudways integration reference and workflow guide. Use when creating, editing, reviewing, debugging, or extending the built-in Cloudways feature; when working with Cloudways account auth, inventory, vault-backed server/app credentials, WordPress review flows, DB Manager access, guarded SQL execution, or the Control UI for Cloudways.
---

# Cloudways Integration

Use this skill when working on OpenClaw's built-in **Cloudways** integration.

## What this system does

The Cloudways integration adds a Control UI workflow and gateway methods for:
- storing Cloudways account auth in the vault
- loading server and application inventory from the Cloudways API
- storing server-level master SSH/SFTP credentials
- storing app-level SSH, WordPress admin, and DB access secrets
- deriving WordPress review metadata for local code review/edit flows
- testing SSH access and DB Manager access
- running guarded read-only SQL queries
- running tightly constrained write SQL with confirmation + audit logging

## Core workflow

1. Read `references/implementation.md` first.
2. If UI work is involved, also read `references/ui-design.md`.
3. If API behavior matters, read `references/cloudways-api-notes.md`.
4. If you need payload shapes or examples, read `references/request-methods.md` and `assets/examples/`.
5. When changing behavior, keep gateway handlers, controller state, and the UI in sync.

## Source of truth files

Read these files in the OpenClaw repo when making code changes:
- `src/gateway/server-methods/cloudways.ts`
- `ui/src/ui/controllers/cloudways.ts`
- `ui/src/ui/views/cloudways.ts`

## Important behaviors

- Account auth is validated before storage.
- Cloudways account email + API key are stored in the vault, not plain config.
- App and server secrets are stored in the vault under generated key prefixes.
- Inventory is read from Cloudways API responses, with applications flattened from server inventory.
- WordPress admin passwords should be treated as manual secure inputs, not assumed retrievable from Cloudways inventory.
- DB Manager read queries are limited to read-only statements.
- Write queries require an exact confirmation phrase and are audit logged locally.
- SQL shape is intentionally restricted to single statements; DDL and multi-statement SQL are blocked.

## Security requirements

When packaging or documenting this system:
- **Do not include** `~/.openclaw/secrets.json`
- **Do not include** `workspace/config/cloudways.json` from a live setup
- **Do not include** any live email addresses, API keys, DB manager URLs, SSH keys, passwords, DB hosts, app ids, or server ids from local memory/config
- Use placeholders in examples
- Keep examples obviously fake

## Debugging checklist

- Does `cloudways.status` reflect configured/unconfigured state correctly?
- Does `cloudways.save` validate credentials before storing them?
- Does `cloudways.inventory` flatten apps from server inventory correctly?
- Do server-level credentials load/save independently from app-level credentials?
- Does app metadata correctly inherit server credentials when app SSH fields are blank?
- Does DB access test succeed only when DB Manager launcher URL + credentials are valid?
- Do read queries reject write statements?
- Do write queries require exact confirmation text and produce audit log entries?

## References in this skill

- `references/implementation.md` — architecture and code map
- `references/request-methods.md` — gateway request methods and behaviors
- `references/cloudways-api-notes.md` — Cloudways API usage notes for this integration
- `references/ui-design.md` — Control UI layout and UX notes
- `assets/examples/cloudways-status-response.json`
- `assets/examples/cloudways-metadata-response.json`
- `assets/examples/cloudways-read-query-response.json`
