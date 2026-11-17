# agentSAFE Deployment Guide

This document describes how the service is architected, how to deploy it
publicly, how to verify a deployment, and how to roll back.

## Architecture

```
MCP client ──x402 payment──▶ agentSAFE MCP service  ──workflow_dispatch──▶ GitHub Actions
                             (FastMCP server)         (docker-audit.yml, ephemeral worker)
                                    ▲                              │
                                    └──── poll status ◀── report artifact ──┘
```

- **MCP service**: FastMCP server (`src/agentsafe/server.py`). Payment-gated
  via the official x402 SDK (verify-before-execution, settle-after-success).
- **Audit worker**: `docker-audit.yml` runs the pinned toolchain (slither,
  aderyn, mythril, heimdall) inside the image built from `Dockerfile`, then
  uploads `report.json` as an artifact (2-day retention).
- The service and the worker communicate only through GitHub's API; no
  inbound access to the worker is needed.

## Environment Variables (all required at runtime)

See `.env.example` for the full annotated list. Groups:

| Group | Variables | Notes |
|---|---|---|
| RPC | `INFURA_ETH_ENDPOINT` | Ethereum Mainnet JSON-RPC |
| Explorer | `ETHERSCAN_API_KEY` | verified-source retrieval |
| LLM | `LLM_PROVIDERS_JSON`, `LLM_GLOBAL_RPM`, … | JSON list of providers |
| GitHub | `GITHUB_TOKEN`, `GITHUB_REPO`, `GITHUB_WORKFLOW_FILE`, `GITHUB_REF` | token needs `workflow` scope to dispatch |
| Payments | `PAYMENTS_ENABLED`, `X402_NETWORK`, `X402_PAY_TO`, `X402_SDK_VERSION`, `X402_FACILITATOR_URL`, `X402_PRICE`, `X402_ASSET`, `X402_MAX_TIMEOUT_SECONDS`, `X402_ALLOW_MAINNET` | see `.env.example` warnings; mainnet is opt-in only |
| Store | `TASK_STORE` (`sqlite`/`memory`), `TASK_DB_PATH` | use `sqlite` in production; `memory` loses task state on restart |

**Never commit credentials.** Locally they live in `.env` (gitignored). On a
hosting provider, use the provider's secret manager (FastMCP Cloud
environment secrets, Docker secrets, or your orchestrator's equivalent).

The worker additionally needs the repo-level GitHub Actions secrets
`INFURA_ETH_ENDPOINT`, `ETHERSCAN_API_KEY`, `LLM_PROVIDERS_JSON` (set via the
repo Settings → Secrets and variables → Actions).

## Option A — FastMCP Cloud (recommended first path)

`fastmcp.json` already declares the zero-arg factory
(`agentsafe.server:create_app`). Cloud builds inspect the server without
environment variables, so validation is deferred to server startup
(`build_server(validate=False)` + lifespan re-validation): a misconfigured
deployment refuses to serve at runtime.

```bash
pip install fastmcp
fastmcp deploy ./fastmcp.json        # interactive; requires a FastMCP account
```

Then, in the FastMCP Cloud dashboard:

1. Set every environment variable from the table above as a deploy secret.
2. Deploy and note the public MCP endpoint URL.
3. Verify (see below).

## Option B — Self-hosted public endpoint

```bash
uv venv && source .venv/bin/activate
pip install . "x402[evm]==2.25.0"
export $(grep -v '^#' .env | xargs)   # or use your process manager's env file
fastmcp run agentsafe.server:create_app --host 0.0.0.0 --port 8000
```

Put the port behind a TLS-terminating reverse proxy (Caddy/nginx) and
restrict access at the network level as appropriate. `TASK_STORE=sqlite`
with a persistent volume is recommended so task state survives restarts.

## Deployment verification (do not skip)

From any machine OUTSIDE the deployment host:

```bash
# 1) tool discovery — health must appear in the tool list
fastmcp call <public-endpoint> list-tools

# 2) safe non-paid request — health never charges and never returns secrets
fastmcp call <public-endpoint> health

# 3) real dispatch — dispatch a dev audit (payments disabled) and confirm
#    the GitHub Actions run appears and completes
```

A deployment is verified only when all three succeed from an external
network. Do not enable live payments just to test deployment; test with
`PAYMENTS_ENABLED=false` first.

## Health checks, timeouts, error handling

- `health` tool: liveness + non-secret config summary; safe for external
  probes and auto-restarts.
- Audit jobs: `AUDIT_TIMEOUT_SECONDS` bounds the worker; the GitHub workflow
  itself has `timeout-minutes: 30`; the service polls with
  `GITHUB_API_TIMEOUT_SECONDS` / `GITHUB_POLL_INTERVAL_SECONDS` and retries
  transient HTTP errors.
- Failed scanners are reported as `tools_failed` in the report and set a
  partial-audit state; they are never reported as "no findings".
- Logs: API keys and payment payloads are never logged; the startup secrets
  report prints masked values only.

## Rollback

- **FastMCP Cloud / self-host**: redeploy the previous git tag or commit;
  keep the previous deployment's env var set alongside the artifact so the
  switch is a single redeploy.
- **Worker**: the workflow runs from the repo `main`; roll back by
  reverting the commit (worker changes take effect on the next dispatch).
- **Config-only rollback**: payment settings are environment variables —
  setting `PAYMENTS_ENABLED=false` instantly reverts to free dev mode
  without a code deploy.

## Outstanding manual steps for go-live

The following require an account/authorization that is not in this repo:

1. FastMCP Cloud account (or a public host) — actual deployment.
2. DNS/TLS if self-hosting.
3. Repository Actions secrets already configured; rotate the GitHub token if
   it was ever exposed.
4. Live-payment smoke test on Base mainnet with a real (small) USDC balance.
