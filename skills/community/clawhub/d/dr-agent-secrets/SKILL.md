---
name: "dr-agent-secrets"
description: "Manage persistent local OpenClaw secrets safely."
---

# DR Agent Secrets

Use when setting up, adding, inspecting, validating, or troubleshooting persistent local secrets or environment variables for Daniel-owned OpenClaw/Codex agents across sessions.

This skill stores procedures only. It must never store secret values.

## Core Rules

1. Do not put secret values in chat, memory files, AGENTS.md, TOOLS.md, git repos, logs, screenshots, transcripts, or final answers.
2. Redact secret values in commands and diagnostics. Show key names and presence/absence, not values.
3. Prefer native OpenClaw secret references when configuring OpenClaw-managed config fields.
4. Use protected local env fragments for service-level environment variables that the gateway or child processes must inherit.
5. Add secrets additively. Do not replace one global env file containing unrelated secrets.
6. Ask before restarting `openclaw-gateway.service` if a restart could interrupt live work.
7. Ask before changing secret paths, credential mechanisms, permissions policy, or production/customer-impacting auth.

## Preferred Patterns

### Pattern A, OpenClaw SecretRefs for OpenClaw config fields

Use this when the secret belongs to an OpenClaw config field that supports secret references.

Examples:
- provider API keys
- memory embedding API keys
- plugin config secrets
- other OpenClaw-managed secret-bearing config fields

Workflow:
1. Use the OpenClaw secret mechanism, such as `openclaw secrets configure` or `openclaw secrets apply`, when available.
2. Audit config for plaintext secrets when supported:
   ```bash
   openclaw secrets audit --check
   ```
3. Verify the relevant feature after gateway reload/restart.
4. Record only the non-secret mapping or convention in memory, for example: `memory embeddings use secret id OPENAI_API_KEY`.

Do not copy secret values into memory notes.

### Pattern B, env.d fragments for service-level environment

Use this when a gateway service or tools spawned by the gateway need environment variables across sessions.

Preferred layout:

```text
~/.config/openclaw/env.d/
  10-ikara-platform.env
  20-azure-devops.env
  30-m365-mail.env
```

Keep the systemd override stable and additive:

```bash
install -d -m 700 "$HOME/.config/openclaw"
install -d -m 700 "$HOME/.config/openclaw/env.d"
install -d -m 700 "$HOME/.config/systemd/user/openclaw-gateway.service.d"

cat > "$HOME/.config/systemd/user/openclaw-gateway.service.d/override.conf" <<'EOF'
[Service]
EnvironmentFile=-%h/.config/openclaw/env.d/*.env
EOF

chmod 700 "$HOME/.config/openclaw" "$HOME/.config/openclaw/env.d"
systemctl --user daemon-reload
```

The leading `-` makes missing files non-fatal. If the host/systemd version does not support glob expansion for `EnvironmentFile`, use multiple explicit `EnvironmentFile=-%h/.config/openclaw/env.d/<name>.env` lines instead.

## Adding A Secret Group

Create one file per project/system instead of replacing a global file.

```bash
umask 077
cat > "$HOME/.config/openclaw/env.d/10-example.env" <<'EOF'
EXAMPLE_API_URL=replace-with-url
EXAMPLE_USERNAME=replace-with-username
EXAMPLE_PASSWORD=replace-with-secret
EOF

chmod 600 "$HOME/.config/openclaw/env.d/10-example.env"
```

Rules:
- Use placeholder values in shared instructions.
- Add or update the specific relevant env file only.
- Do not overwrite unknown existing values casually.
- Prefer scoped names like `10-ikara-platform.env` over one giant file.
- Keep filenames stable so restore steps and diagnostics are predictable.

## Reload And Restart

After changing only env file contents:

```bash
systemctl --user restart openclaw-gateway.service
```

After changing systemd override files:

```bash
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
```

Ask Daniel before restarting if the gateway is doing live work or if interruption risk is unclear.

## Validation

Check permissions:

```bash
ls -ld "$HOME/.config/openclaw" "$HOME/.config/openclaw/env.d"
ls -l "$HOME/.config/openclaw/env.d"
```

Check that systemd sees the env files without printing secret values:

```bash
systemctl --user show openclaw-gateway.service -p EnvironmentFiles
```

Avoid printing full `Environment` because it may reveal values.

Prefer presence checks from inside the service context or a controlled diagnostic that prints only key names/status. Example shape:

```bash
systemctl --user show openclaw-gateway.service -p EnvironmentFiles
# Then verify feature behavior directly, such as memory status, provider auth, git access, or API health.
```

For OpenClaw memory/provider secrets, verify with the relevant command, for example:

```bash
openclaw memory status --index --deep
```

If a diagnostic must mention a value, show only a suffix/prefix approved by Daniel or a hash, never the full secret.

## Git And Backup Safety

Ensure secret files are excluded from git.

Recommended `.gitignore` entries:

```gitignore
.config/openclaw/env.d/*.env
.config/openclaw/*.env
*.env
gateway.systemd.env
gateway.systemd.env.*
.env
```

Before committing:

```bash
git status --short
git diff --cached --name-only
```

If a secret-bearing file is staged, stop and unstage it. Do not rely on later cleanup.

## Restore Notes

Backup procedures may record:
- secret file path conventions
- key names
- which subsystem expects them
- how to re-run validation

Backup procedures must not record:
- values
- tokens
- passwords
- private keys
- OAuth files
- copied env file contents

## Troubleshooting

If a secret works in the shell but not in the gateway:
1. Check whether the gateway service inherited the file.
2. Check whether `systemctl --user daemon-reload` is needed.
3. Restart the gateway if approved.
4. Verify the feature, not just the variable.
5. Check for stale env files in old OpenClaw paths such as `~/.openclaw/.env` or `~/.openclaw/gateway.systemd.env` only when investigating a known conflict.
6. Remove or update stale files only after confirming ownership and risk.

## What To Report

When done, report:
- files created or changed, with paths only
- permissions applied
- whether daemon reload ran
- whether gateway restart ran
- validation command and result
- any remaining approval needed

Never report secret values.
