# launchthat-openclaw-connector

> [!WARNING]
> Deprecated: this connector is being phased out in favor of `@launchthatbot/connect-openclaw-plugin`.
> New integrations should use the plugin only.

## What is LaunchThatBot

LaunchThatBot is a platform for operating OpenClaw agents with a managed control plane, security defaults, and real-time visibility (including office/org chart style views) while still keeping your agents on your infrastructure.

## What this skill is for

`launchthat-openclaw-connector` is for users who want to **keep their existing OpenClaw infrastructure** (existing VPS, local machine, custom Docker setup) and still connect to LaunchThatBot features like live status/office visibility and observability logs.

This is **not** the migration/import path.

This legacy package remains only for backward compatibility while migrations complete.
For all new installs and ongoing setup, use `@launchthatbot/connect-openclaw-plugin`.

- Use [`import`](https://launchthatbot.com/docs/skills/import) when moving agent runtime into LaunchThatBot-managed infrastructure.
- Use [`connect`](https://launchthatbot.com/docs/skills/connect) when staying on your own infrastructure and linking telemetry/control signals.

> [!WARNING]
> If you use this method, LaunchThatBot cannot help you manage your infrastructure.
> You still manage server operations yourself (restarts, patching, container lifecycle, etc.).
>
> You also do not get LaunchThatBot managed-host defaults like UFW, Fail2ban, and locked-down installation hardening.
>
> The main reason to choose `connect` over `import` is when you have a very large or highly customized agent codebase that you do not want to migrate right now.
>
> If you want a stronger baseline while keeping flexibility, you can migrate to a LaunchThatBot-managed agent on your own infrastructure and disconnect immediately after provisioning.

## Instructions

1. Generate auth link:

```bash
pnpm --filter launchthat-openclaw-connector build
pnpm --filter launchthat-openclaw-connector exec lt-openclaw-connect auth-link \
  --base-url=http://localhost:3000 \
  --workspace-id=default \
  --instance-name=my-openclaw
```

2. Open returned `authUrl` and collect `instanceId` + `ingestToken`.

3. Run connector:

```bash
export LAUNCHTHAT_INGEST_TOKEN="<token>"
export LAUNCHTHAT_SIGNING_SECRET="<shared-signing-secret>"
pnpm --filter launchthat-openclaw-connector exec lt-openclaw-connect run \
  --base-url=http://localhost:3000 \
  --workspace-id=default \
  --instance-id=<instanceId>
```

4. Connector sends heartbeat and event batches to LaunchThatBot with retry/queue behavior.

## Security

- `connect` mode does not upload your full agent config/memory/secret payload; it sends connector heartbeat/events for visibility.
- Prefer ingest token through environment variable, not raw CLI arg.
- Optional HMAC signing is supported with `LAUNCHTHAT_SIGNING_SECRET`.
- Queue file uses restrictive local permissions by default.
- Queue persistence can be disabled with `--persist-queue=false`.
- Keep ingest/signing secrets outside logs and screenshots.

If you later use the `import` skill (Quick API or Air-gapped file), LaunchThatBot is not able to read imported secret content in plaintext.
Data is encrypted before transfer and decrypted only inside your agent container on your infrastructure.
