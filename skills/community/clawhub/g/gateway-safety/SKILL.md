---
name: gateway-safety
description: Safely update OpenClaw gateway configuration (openclaw.json) with automatic validation, backup, and 30-second health-check rollback. Use this skill whenever an agent needs to modify gateway settings, ports, provider credentials, or network bindings to ensure the session is not permanently lost due to a bad configuration.
license: MIT
---

# Gateway Safety

This skill ensures that any modifications to the OpenClaw gateway configuration are done safely. It prevents "death loops" and permanent session loss by verifying the gateway can successfully reboot before committing to a new config.

## Core Rules

1. **Mandatory Script Use**: Never edit `~/.openclaw/openclaw.json` directly. Always use the provided `safe-gateway-update.sh` script.
2. **Anti-Loop Policy**: If the script fails 3 times consecutively, it will create a `GATEWAY_LOCKOUT` file. If this file exists, **STOP ALL OPERATIONS** and wait for Kevin. Do not attempt to bypass the lockout.
3. **Backup Awareness**: The script maintains its own backups, but for critical changes, manually verify `~/.openclaw/openclaw.json.known-good` is up to date.

## Usage

To update the gateway configuration:

1. Prepare the new configuration JSON file (e.g., at `/tmp/new_config.json`).
2. Execute the safety script:
   ```bash
   [SKILL_PATH]/scripts/safe-gateway-update.sh /tmp/new_config.json [timeout_seconds]
   ```
3. The script will:
   - Validate the JSON syntax.
   - Backup the current config.
   - Apply the new config and restart the gateway.
   - Poll for a successful "RPC probe: ok" status.
   - Roll back to the previous config if the health check fails or times out.

## Authorship
Created by Kevin Smith & Rook (Orbit Smith), March 2026.
