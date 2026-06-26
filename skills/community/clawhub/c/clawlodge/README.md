# ClawLodge CLI

Pack and publish OpenClaw config workspaces to ClawLodge.

## Install

```bash
npm install -g clawlodge-cli
```

On first interactive use, the CLI asks whether you want to share anonymous command-level usage telemetry.

Change this anytime with:

```bash
clawlodge config get telemetry
clawlodge config set telemetry off
clawlodge config set telemetry anonymous
```

## Basic usage

```bash
clawlodge login
clawlodge pack
clawlodge publish
```

## README and Name

```bash
clawlodge publish --name "My Workspace"
clawlodge publish --readme /path/to/README.md
```

If you do not pass `--name`, the CLI derives it from the workspace folder name.
If you do not pass `--readme`, the publish API generates the README on the server.

## Help

```bash
clawlodge help
```

Create a PAT in `https://clawlodge.com/settings`, then run:

```bash
clawlodge login
clawlodge whoami
```

If the default OpenClaw workspace is not available under `~/.openclaw`, pass an explicit path with `--workspace`.
