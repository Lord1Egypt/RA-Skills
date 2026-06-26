# Skill Examples

## Example: connect a new instance

Prompt:

> Connect my existing OpenClaw VPS to LaunchThatBot and keep it secure.

Expected skill behavior:

1. Generate auth link command.
2. Instruct user to authorize via callback URL.
3. Use env vars for token/secret, not raw CLI args.
4. Start connector and verify heartbeat/ingest/replay.

## Example: secure production setup

Prompt:

> Harden my OpenClaw connector flow for production.

Expected skill behavior:

1. Enable signed payload mode (`OPENCLAW_REQUIRE_SIGNATURE=true`).
2. Rotate ingest token and set strong signing secret.
3. Restrict network egress to LaunchThatBot domain.
4. Run smoke verification and inspect replay events.

## Example: debugging no dashboard updates

Prompt:

> Connector is running but office UI is stale.

Expected skill behavior:

1. Verify heartbeat status.
2. Verify ingest responses include `accepted > 0`.
3. Query replay endpoint for recent events.
4. Confirm workspace/instance IDs match dashboard workspace.
