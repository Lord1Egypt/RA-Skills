# Cloudways Integration Implementation

## Purpose

The Cloudways integration gives OpenClaw a secure operational layer for Cloudways-hosted WordPress review and maintenance workflows.

It combines:
- Cloudways account API inventory
- vault-backed secret storage
- server/app credential management
- WordPress review metadata derivation
- database manager login automation
- guarded SQL execution

## Main code references

### 1. Gateway/backend implementation
**Path:** `/home/charl/openclaw/src/gateway/server-methods/cloudways.ts`

This is the core implementation.

Key responsibilities:
- read/write vault-backed Cloudways account credentials
- read/write Cloudways local config
- fetch Cloudways OAuth access token
- fetch and normalize inventory
- store/retrieve server-level secrets
- store/retrieve app-level secrets
- test SSH server connection
- test DB Manager access
- enforce read-only SQL rules
- enforce limited write SQL rules with confirmation + audit log
- derive WordPress metadata for local review flows

Key internal concepts:
- `CloudwaysConfig`
- `CloudwaysServer`
- `CloudwaysApp`
- `CloudwaysInventory`
- `ServerSecretBundle`
- `AppSecretBundle`

Important implementation details:
- account auth vault keys:
  - `CLOUDWAYS_EMAIL`
  - `CLOUDWAYS_API_KEY`
- live config path:
  - `~/.openclaw/workspace/config/cloudways.json`
- live vault path:
  - `~/.openclaw/secrets.json`
- DB audit log path:
  - `~/.openclaw/workspace/logs/cloudways-db-audit.jsonl`
- per-server and per-app secret keys are namespaced with generated prefixes
- inventory is derived from `GET /server` style responses and nested `apps[]`
- DB Manager automation uses Playwright Chromium
- SSH testing uses Python + Paramiko

### 2. UI controller layer
**Path:** `/home/charl/openclaw/ui/src/ui/controllers/cloudways.ts`

This file manages Cloudways UI state transitions and gateway calls.

Key responsibilities:
- initialize Cloudways view state
- load status/configured state
- save/disconnect account config
- refresh inventory
- select server
- select app
- load metadata and secrets for selected app
- patch local form state for secrets and queries
- save server secrets
- save app secrets
- test SSH connection
- test DB access
- run read query
- run write query

Important behavior:
- app selection triggers parallel loading of metadata and app secrets
- if metadata has a server id, server secrets are also loaded
- success messages are transient
- read and write query panes have distinct state

### 3. UI rendering layer
**Path:** `/home/charl/openclaw/ui/src/ui/views/cloudways.ts`

This file defines the visible Cloudways Control UI.

Main sections:
- Cloudways account config card
- servers/applications inventory card
- server master credentials card
- application metadata + app secrets card
- read-only DB inspection section
- guarded DB write section

## Data model overview

### Account-level
- email
- API key
- default local review root
- preferred sync mode

### Server-level secrets
- SSH host
- SSH user
- SSH password
- SSH private key

### App-level secrets
- SSH host/user/password/key override
- WordPress admin URL/user/password
- local path override
- DB name/user/password/host/port
- DB manager URL

### Derived metadata
- app/server labels and ids
- production URL
- WordPress admin URL guess
- local review path
- remote root
- suggested rsync/sftp commands
- review hints

## SQL safety model

### Allowed read-only statements
- `SELECT`
- `SHOW`
- `DESCRIBE`
- `DESC`
- `EXPLAIN`

### Allowed write statements
- `INSERT`
- `UPDATE`
- `DELETE`
- `REPLACE`

### Explicitly blocked
- multi-statement SQL
- `ALTER`
- `DROP`
- `TRUNCATE`
- `CREATE`
- `RENAME`
- `GRANT`
- `REVOKE`
- `SET`
- `LOCK`
- `UNLOCK`
- `CALL`
- `OPTIMIZE`
- `REPAIR`

### Write execution guardrails
- exact confirmation text: `RUN WRITE QUERY`
- optional dry-run path uses `EXPLAIN`
- write attempts are audit logged locally

## Design implications

- This integration is intentionally admin/operator oriented.
- It mixes API inventory with manual secure credential entry because Cloudways inventory alone is not a sufficient source of truth for all access paths.
- The DB tooling is intentionally constrained, not general-purpose SQL access.
- The feature is designed around review/maintenance workflows, not broad Cloudways platform administration.
