# Platform playbook: Docker / Docker Compose

## Threat assumptions

- Docker does **not** make an exposed service safe.
- If you publish `18789/tcp` to `0.0.0.0`, the LAN or internet can still reach it.
- Volume mounts often contain the most sensitive OpenClaw data: config, credentials, transcripts, workspace.
- Host networking or privileged containers turn a bot misconfiguration into a host incident quickly.

## Audit checks

1. **Published ports**
   - good: `127.0.0.1:18789->18789/tcp`
   - risky: `0.0.0.0:18789->18789/tcp`

   Commands:

   ```bash
   docker ps --format 'table {{.Names}}	{{.Image}}	{{.Ports}}'
   docker compose ps || true
   docker port openclaw-gateway 18789 || true
   ```

2. **Gateway auth and bind mode**
   - even on localhost publishing, keep Gateway auth enabled
   - use `openclaw gateway probe --json` to see the effective target the CLI can reach

3. **Volume mounts**
   - identify mounts for `~/.openclaw` and workspace
   - avoid mounting your entire home directory
   - keep host-side permissions on the mounted state dir restrictive

4. **Container privileges**
   - avoid `privileged: true`
   - avoid `network_mode: host`
   - avoid unnecessary capabilities
   - run as a non-root user where practical

5. **Control UI and reverse proxy**
   - if a proxy fronts the container, configure `gateway.trustedProxies`
   - for non-loopback Control UI, set `gateway.controlUi.allowedOrigins`
   - do not enable Host-header origin fallback casually

## Hardening actions

### Publish localhost only

```yaml
ports:
  - "127.0.0.1:18789:18789"
```

### Reduce tool surface

For inbox-facing agents, start with `tools.profile: "messaging"` and deny runtime/fs/automation until a specific need appears.

### Keep secrets out of the repo

Use host env files or a secrets manager, not committed config values.

### Treat browser + exec as high risk

If untrusted users can message the bot, runtime/browser/node surfaces need especially tight controls.

## Verification

```bash
openclaw security audit --deep --json
openclaw gateway probe --json
openclaw channels status --probe
```

External reachability tests from another machine/network should fail unless the exposure is deliberate and defended.
