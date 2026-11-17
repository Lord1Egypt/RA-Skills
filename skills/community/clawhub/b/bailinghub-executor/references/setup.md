# Setup and verification

## 1. Prepare BailingHub

In the self-hosted BailingHub console:

1. Create or select the executor target that should receive OpenClaw work.
2. Issue a new executor token scoped only to that target.
3. Choose a stable executor id, such as `openclaw-finance-worker-01`.
4. Keep the token in a local secret manager or a mode-0600 environment file.

The skill does not create a BailingHub instance, target, route, approval rule, or business-system permission.

## 2. Prepare OpenClaw

Verify the local runtime before connecting it to BailingHub:

```bash
node --version
openclaw --help
openclaw agent --help
```

Node.js 18 or newer is required. The selected OpenClaw agent must support non-interactive runs and must already have any model-provider credentials it needs.

## 3. Set configuration

Required variables:

```bash
export BAILING_HUB_URL="https://hub.example.com"
export BAILING_TARGET="finance-agent"
export BAILING_EXECUTOR_ID="openclaw-finance-worker-01"
read -rsp 'BailingHub executor token: ' BAILING_EXECUTOR_TOKEN
printf '\n'
export BAILING_EXECUTOR_TOKEN
```

Optional OpenClaw variables:

```bash
export OPENCLAW_AGENT="bailinghub-executor"
export OPENCLAW_MODEL=""
export OPENCLAW_THINKING=""
export OPENCLAW_TIMEOUT_SECONDS="600"
```

`OPENCLAW_USE_GATEWAY=1` switches from local execution to a separately managed OpenClaw Gateway. Leave it unset unless that gateway is already part of the deployment design.

The child process receives only a minimal system environment by default. If this OpenClaw installation reads a model-provider key, proxy setting, or custom certificate path from an environment variable, opt in to only those exact names:

```bash
export OPENCLAW_FORWARD_ENV="OPENAI_API_KEY,HTTPS_PROXY,NODE_EXTRA_CA_CERTS"
```

Do not add unrelated shell, cloud, database, CI, or business-system credentials. `BAILING_*` control-plane variables and process-injection variables such as `NODE_OPTIONS` and `LD_PRELOAD` are always rejected.

## 4. Run one job

From the installed skill directory:

```bash
export BAILING_RUN_ONCE=1
node scripts/bailinghub-openclaw-executor.mjs
```

Create a dedicated non-sensitive test task in BailingHub. Confirm that the executor claims exactly one task, OpenClaw processes it, and BailingHub receives the final result.

Do not use an echo command as the acceptance test. Echo proves transport only and can return private task text unchanged.

## 5. Run persistently

After the one-job test succeeds:

1. Remove `BAILING_RUN_ONCE`.
2. Put the same environment in the host's existing secret-aware supervisor.
3. Start `node scripts/bailinghub-openclaw-executor.mjs` as a non-root service account.
4. Verify automatic restart and BailingHub offline detection.

Do not copy credentials into a service command line. On systemd, use a root-readable `EnvironmentFile`; on launchd or another supervisor, use its protected secret mechanism.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Configuration exits immediately | Required env vars, HTTPS URL, target name, timeout ranges |
| `401` from claim | Token is wrong, revoked, or issued by another BailingHub instance |
| `403` from claim | Token exists but is not scoped to the requested target |
| Executor online but no work | Route target and `BAILING_TARGET` do not match exactly |
| OpenClaw process fails | Agent id, local/gateway mode, OpenClaw CLI version, and whether required provider variables were explicitly named in `OPENCLAW_FORWARD_ENV` |
| Result is rejected | Task was re-dispatched; the old claim token is intentionally stale |
