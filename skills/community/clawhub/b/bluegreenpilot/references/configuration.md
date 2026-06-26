# BlueGreenPilot Configuration

Use `.bluegreenpilot/config.yaml` for versioned topology and workflow. It must
not contain secrets.

Use `.bluegreenpilot/state.<env>.yaml` or an external state backend for runtime
facts such as active slot and last successful release.

## Required Concepts

- **Environment**: dev, homolog, prod, or custom.
- **Slot**: blue or green for blue-green environments.
- **Active slot**: currently serving traffic.
- **Inactive slot**: safe deploy target.
- **Switch method**: how traffic moves from one slot to the other.
- **Rollback method**: how traffic returns to last stable state.
- **State backend**: where active slot and release state persists between
  developer machines, homolog, CI, and production.

## Minimal Config

```yaml
version: 1
app: my-app
strategy: blue-green

branches:
  dev: dev
  homolog: homolog
  prod: main

environments:
  prod:
    strategy: blue-green
    deploy_mode: docker

slots:
  prod:
    blue_url: https://blue.example.com
    green_url: https://green.example.com
    public_url: https://example.com

checks:
  healthcheck_path: /health
  smoke_commands: []

state:
  backend: repo
  path: .bluegreenpilot/state.{environment}.yaml

switch:
  method: manual
  command: ""

rollback:
  method: manual
  command: ""
```

## Minimal State

```yaml
version: 1
environment: prod
active_slot: blue
inactive_slot: green
last_successful_release: abc1234
last_switch_at: 2026-06-02T15:20:00Z
last_snapshot: ""
```

## State Storage Options

- Repo-local file for simple internal projects.
- Server-local file for production state.
- CI artifact for CI-managed deployments.
- Object storage for shared deployment state.
- Secret manager metadata only if the secret manager supports non-secret data.

If state cannot be read, stop and ask the user how to retrieve it.
