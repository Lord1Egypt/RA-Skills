---
name: dataclaw-setup
description: Setup guide for installing and configuring DataClaw itself for use with OpenClaw. Use when the user wants to learn what DataClaw is or finish initial setup. This skill does not create the actual OpenClaw database connection; the real per-access-point skill is installed later from the DataClaw UI.
homepage: https://dataclaw.sh
metadata: { "openclaw": { "emoji": "🦀", "homepage": "https://dataclaw.sh", "skillKey": "dataclaw-setup" } }
---

# DataClaw Setup

Use this skill to explain what DataClaw is and guide the user through setup for OpenClaw.

## What DataClaw does

DataClaw is a localhost-only server that gives AI agents controlled access to a database through MCP.

It is designed for cases where the user wants:

- per-agent API keys
- approved-query workflows
- optional raw query or raw execute permissions
- an audit log of MCP access
- local control over PostgreSQL or SQL Server access

## Setup

Before DataClaw can be used from OpenClaw, the user must complete setup in this order:

1. Install DataClaw from `https://dataclaw.sh` or `https://github.com/ekaya-inc/dataclaw`.
2. Run `dataclaw`.
3. Open the local DataClaw UI in the browser.
4. Configure the datasource.
5. Create or configure the DataClaw access point the user wants OpenClaw to use.
6. In the DataClaw UI, use **Install as a Skill** for that configured access point.

The **Install as a Skill** action is the step that creates the real local OpenClaw integration for that access point.

## Important

This skill is a setup and discovery guide only.

It does not provision the actual DataClaw MCP connection by itself.

Do not assume this skill means DataClaw is already installed, configured, or running.

The real OpenClaw-ready skill for a specific DataClaw access point is generated and installed by DataClaw after setup, for example `dataclaw-marketing`.

## After Setup

Once the user has installed the generated DataClaw skill from the DataClaw UI:

- use the generated access-point skill that DataClaw created
- prefer approved queries when available
- do not assume raw SQL access is allowed
- do not assume write or execute permissions are allowed
- if an operation appears unavailable, explain that the DataClaw access point may not expose that capability

## If Setup Is Not Finished

If the user asks to use DataClaw before it has been installed and configured:

- tell them to install and run DataClaw first
- direct them to the local DataClaw UI
- ask them to finish datasource and access-point setup there
- tell them to use **Install as a Skill** in DataClaw when that option becomes available

## Links

- Website: `https://dataclaw.sh`
- GitHub: `https://github.com/ekaya-inc/dataclaw`
