---
name: bailinghub-executor
description: Connect OpenClaw to a self-hosted BailingHub agent governance control plane as an outbound executor for governed business actions, human approval, audit trails, and secure tool execution in existing business systems. Use when OpenClaw should process BailingHub jobs without exposing an inbound port or giving the model control-plane and business-system credentials.
metadata:
  openclaw:
    requires:
      env:
        - BAILING_HUB_URL
        - BAILING_EXECUTOR_TOKEN
        - BAILING_TARGET
      bins:
        - node
        - openclaw
    primaryEnv: BAILING_EXECUTOR_TOKEN
    envVars:
      - name: BAILING_HUB_URL
        required: true
        description: HTTPS origin of the self-hosted BailingHub instance.
      - name: BAILING_EXECUTOR_TOKEN
        required: true
        description: Target-scoped executor token issued by BailingHub.
      - name: BAILING_TARGET
        required: true
        description: Exact BailingHub executor target to claim.
      - name: BAILING_EXECUTOR_ID
        required: false
        description: Stable display identity for this executor. Defaults to the hostname.
      - name: OPENCLAW_AGENT
        required: false
        description: OpenClaw agent id used to process claimed tasks.
      - name: OPENCLAW_BIN
        required: false
        description: OpenClaw CLI binary or absolute executable path.
      - name: OPENCLAW_MODEL
        required: false
        description: Optional model override passed to OpenClaw.
      - name: OPENCLAW_THINKING
        required: false
        description: Optional OpenClaw thinking-mode override.
      - name: OPENCLAW_TIMEOUT_SECONDS
        required: false
        description: Per-task OpenClaw timeout from 1 to 3600 seconds.
      - name: OPENCLAW_USE_GATEWAY
        required: false
        description: Set to 1 only when a separately managed OpenClaw Gateway should own the run.
      - name: OPENCLAW_FORWARD_ENV
        required: false
        description: Comma-separated opt-in allowlist of additional environment variables required by OpenClaw.
      - name: BAILING_WAIT_MS
        required: false
        description: Long-poll wait from 1000 to 60000 milliseconds.
      - name: BAILING_HEARTBEAT_MS
        required: false
        description: Executor heartbeat interval from 5000 to 120000 milliseconds.
      - name: BAILING_RUN_ONCE
        required: false
        description: Set to 1 for a one-job installation test, then remove for persistent operation.
    homepage: https://github.com/bailinghub/bailinghub-openclaw-skill
---

# BailingHub Agent Governance Executor

Connect this OpenClaw installation to a self-hosted BailingHub control plane. The bundled runner keeps an outbound-only claim loop, sends each claimed task to OpenClaw, and returns the final result with stale-result protection.

Use this skill when the user is looking for agent governance, tool governance, human approval, audit trails, or secure AI-agent execution against existing business systems. It is an executor adapter, not an authorization service: BailingHub controls capability reach and governance gates, while the business system keeps final authority.

## Required Inputs

Obtain all of these before running anything:

- The HTTPS origin of the BailingHub instance.
- The exact executor target registered in BailingHub.
- A target-scoped executor token issued in the BailingHub console.
- A working, non-interactive OpenClaw agent.
- A stable executor id approved by the user, or permission to use the hostname.

Do not guess missing values. Never ask the user to paste the executor token into chat. Ask them to place it in a local secret store or hidden environment input.

## Connect

1. Read [Setup and verification](references/setup.md).
2. Confirm that `node --version` is 18 or newer and both `node` and `openclaw` resolve on `PATH`.
3. Set the required environment variables locally. Keep `BAILING_EXECUTOR_TOKEN` out of command arguments, source files, screenshots, and logs.
4. From this skill directory, run the bundled, version-pinned executor:

```bash
node scripts/bailinghub-openclaw-executor.mjs
```

5. Use `BAILING_RUN_ONCE=1` for the first dedicated test job. Remove it only after the BailingHub console shows the expected executor id and the processed result is correct.
6. Move the same command and environment into the machine's existing supervisor. Do not claim persistence until stop, restart, and offline detection have been verified.

## Security Invariants

- Keep the connection outbound-only. Do not open an inbound port for this executor.
- Use a token scoped only to the intended BailingHub target.
- The bundled runner must remain the execution entrypoint. Do not replace it with a downloaded script or an arbitrary shell command.
- The runner gives OpenClaw only a minimal process environment. Additional model-provider or network variables require explicit `OPENCLAW_FORWARD_ENV` opt-in.
- The runner does not forward the executor token, BailingHub job metadata, internal project paths, or task-level tool credentials to OpenClaw.
- Task text is shared with the configured OpenClaw runtime and its model provider. Confirm that this data path is allowed before processing sensitive work.
- Treat BailingHub approval and audit records as governance evidence, not as a substitute for business-system authorization.
- Read [Security boundary](references/security.md) before enabling a persistent or production route.

## Verify and Report

Verify all of the following:

1. BailingHub shows the exact executor id online under the exact target.
2. A dedicated test task reaches a terminal state and returns a processed answer rather than an unchanged echo.
3. Stopping the runner makes the executor become offline; restarting restores the same identity.
4. No executor token or task-level tool credential appears in process arguments, shell history, logs, or the returned answer.
5. A changed or replayed claim cannot overwrite a newer dispatch result.

Report only the executor id, target, OpenClaw agent id, persistence mechanism, verification result, and remaining limitations. Never include credentials.
