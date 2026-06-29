---
name: ciderbox
description: "Build and manage Apple-native container dev environments with ciderbox and orchard swarm."
---

# Ciderbox

Use for Apple Silicon-native dev/test containers, cross-distro compile testing, and Orchard agent swarms. Ciderbox wraps Apple's `container` CLI, so it is for local Apple Silicon Macs rather than Crabbox-style remote cloud runners.

## When To Use

- Verify a project across Linux distro images from a Mac.
- Run a one-off command in a fresh Apple Container VM.
- Build a project in a clean container and tear it down afterward.
- Manage Orchard agent trees with `ciderbox orchard ...`.
- Scaffold project-local `.ciderbox.yaml`.

Use Crabbox instead when the task needs remote cloud capacity, GitHub Actions hydration, or non-Mac provider runners.

## Requirements

- Apple Silicon Mac.
- macOS 26+ for reachable container IPs.
- Apple `container` CLI installed and running with `container system start`.
- Ciderbox on PATH. On Mike's machine: `/Users/michaelwyatt/.openclaw/workspace/ciderbox/bin/ciderbox`.

## Quickstart

```sh
# Scaffold config
ciderbox init

# Test your code across Linux distros
ciderbox compile-test

# Run a one-off command in a fresh VM
ciderbox run -- uname -a

# Clean up everything
ciderbox chop
```

## Project Config

`.ciderbox.yaml` shape:

```yaml
compileTest:
  distros:
    - name: ubuntu
      image: ubuntu:26.04
    - name: debian
      image: debian:bookworm
  parallel: false
  dependencies: [rsync]
  command: "make test"
```

`ciderbox init --detect` replaces the placeholder command with detected project commands and matching deps.

## Commands

| Command | Description |
|---------|-------------|
| `ciderbox init [--detect]` | Scaffold `.ciderbox.yaml` |
| `ciderbox compile-test` | Run tests across configured distros |
| `ciderbox build` | Single-distro build |
| `ciderbox run -- <cmd>` | One-off command in fresh VM |
| `ciderbox doctor` | Check environment |
| `ciderbox chop` | Kill all ciderbox VMs |
| `ciderbox version` | Show version |

## Orchard Swarm

Orchard is the local OpenClaw agent swarm layer. It plants Apple Container VMs, grafts OpenClaw into each, and runs tasks across the orchard.

### Lifecycle

```bash
# 1. Scaffold orchard config
ciderbox orchard init

# 2. Plant trees (VMs)
ciderbox orchard plant

# 3. Graft OpenClaw onto every tree
ciderbox orchard graft --all

# 4. Run a task across the orchard
ciderbox orchard run --sync --task "review this repo and write findings"

# 5. Collect results
ciderbox orchard harvest --task <task-id> --output results.json

# 6. Read the summary
ciderbox orchard press --task <task-id>

# 7. Tear down
ciderbox orchard chop --yes
```

### Secrets

```bash
ciderbox orchard secrets init    # Create .orchid.env
ciderbox orchard secrets check   # Validate keys are present
ciderbox orchard secrets push --all  # Push keys into running trees
```

### Diagnostics

```bash
ciderbox orchard doctor
```

## Manifest Format

`.orchard.yaml`:

```yaml
name: my-orchard
trees: 3
template:
  image: debian:bookworm
  cpus: 2
  memory: 4G
  distro: debian
agent:
  identity: tree-agent
  skills: []
  model: ollama/llama3.1
  command: cd "${ORCHARD_WORKSPACE:-/root/.openclaw/workspace}" && openclaw --log-level silent agent --local --agent main --session-key "orchard:${HOSTNAME:-tree}" --message "$ORCHARD_TASK" --timeout 180 --verbose off
secrets:
  envFile: .orchid.env
  required: []
workspace:
  sync: true
  path: /work/ciderbox
```

## Verification

Before shipping Ciderbox changes:

```sh
gofmt -w internal/cli/*.go
go test ./...
cd /tmp && rm -rf ciderbox-init-smoke && mkdir ciderbox-init-smoke
cd /tmp/ciderbox-init-smoke && git init -q && ciderbox init
```

Run structured autoreview before release or tag changes.

## License

MIT
