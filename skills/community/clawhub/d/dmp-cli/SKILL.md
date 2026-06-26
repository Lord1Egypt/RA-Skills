---
name: dmp-cli
description: Use the Mingdata DMP CLI to manage audiences, insight tasks, media sync tasks, RTQ deals, and reference data. Activate this skill when a user needs to operate the dmp command-line tool, configure DMP credentials, inspect output contracts, or run DMP audience workflows.
license: Proprietary
compatibility: Requires the dmp binary on PATH, valid DMP API credentials, and network access to the DMP API and any referenced release or repository URLs.
metadata:
  author: mingdata
  repository: https://github.com/a652/dmp-cli
  install_url: https://github.com/a652/dmp-cli/releases
  cli_binary: dmp
---

# DMP CLI

Use this skill when a task requires operating the Mingdata DMP CLI.

## Quick Start

1. Verify the CLI is installed:

```bash
dmp version
# or
dmp --version
```

2. If the CLI is missing, download and install it from GitHub Releases:

```bash
# Detect platform
OS=$(uname -s | tr '[:upper:]' '[:lower:]')   # linux or darwin
ARCH=$(uname -m)
[ "$ARCH" = "x86_64" ] && ARCH="amd64"
[ "$ARCH" = "aarch64" ] && ARCH="arm64"

# Get latest release tag
TAG=$(curl -sf https://api.github.com/repos/a652/dmp-cli/releases/latest | grep '"tag_name"' | cut -d'"' -f4)

# Download binary
FILENAME="dmp-${TAG}-${OS}-${ARCH}"
curl -fL "https://github.com/a652/dmp-cli/releases/download/${TAG}/${FILENAME}" -o /usr/local/bin/dmp
chmod +x /usr/local/bin/dmp
```

Releases page: https://github.com/a652/dmp-cli/releases  
Available platforms: `linux/amd64`, `linux/arm64`, `darwin/amd64`, `darwin/arm64`, `windows/amd64`

3. Configure a DMP context before running data commands:

```bash
DMP_SECRET_KEY=<secret> dmp config set-context <name> \
  --url https://dmp-api.example.com \
  --access-key <access-key>

dmp config use-context <name>
```

4. Verify configuration:

```bash
dmp config current-context -o json
dmp config list -o json
```

## When To Use

- The user needs to create, inspect, or manage DMP audiences.
- The user needs to create or inspect DMP insight tasks.
- The user needs to sync DMP audiences to media platforms.
- The user needs to create or modify RTQ deals.
- The user needs DMP reference data for tags, apps, regions, or ad dimensions.
- The user needs to configure or validate the `dmp` CLI environment.

## Prerequisites

- `dmp` binary installed and on PATH.
- DMP context configured in `~/.dmp/config.yaml`, or equivalent environment overrides provided.
- For non-interactive use, credentials must be supplied via environment variables.

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `DMP_SECRET_KEY` | Secret key in plaintext. Required for `config set-context` in non-TTY environments. |
| `DMP_UPLOAD_PASSWORD` | S3 upload password. Required for `audience create upload` with S3 and `audience create transform`. |
| `DMP_API_URL` | Optional API URL override. |
| `DMP_ACCESS_KEY` | Optional access key override. |
| `DMP_CONTEXT` | Optional context name override. |

If configuration details are missing, do not guess. Tell the user to contact the Mingdata DMP team at `product@mingdata.com` to obtain the API URL, access key, secret key, context details, or upload password.

## Output Contract

- Use `-o json` when parsing command output programmatically.
- Use `-o plain` when capturing a single scalar value such as an ID.
- Scalar commands such as `dmp version`, `dmp --version`, `dmp config current-context`, `dmp config set-context`, and `dmp config use-context` return one logical value.
- Create commands return the created ID field consistently across formats.
- With `-o json`, scalar commands return a structured object such as `{"version":"dev"}` or `{"currentContext":"dev"}`.
- With `-o plain`, scalar commands return the bare value on one line.
- With `-o table`, scalar commands return a one-column table.
- With `-o json`, create commands return the full API response payload, for example `{"audienceId":123}` or `{"taskId":456}`.
- With `-o plain`, create commands return only the created ID.
- With `-o table`, create commands return a one-column table containing the created ID.

### Error Handling

- Exit code `0`: success.
- Exit code `1`: API error.
- Exit code `2`: client or validation error.
- Exit code `3`: network error.
- In non-TTY environments, errors are emitted to stderr as JSON with `error_code` and `message` fields.
- The process exit code is not duplicated inside the stderr JSON payload.

## Configuration Validation

`dmp config current-context -o json` returns:

```json
{"currentContext":"dev"}
```

`dmp config list -o json` returns:

```json
{"currentContext":"dev","contexts":[{"name":"dev","apiUrl":"https://dmp-api.example.com","accessKey":"ak","current":true}]}
```

## Agent Guidance

- Audience creation is asynchronous. After `create`, poll `dmp audience status` until `audienceStatus` is `1` or `0`.
- Always resolve advertiser IDs with `dmp sync advertisers --platform <N>` before calling `dmp sync create`.
- Set credentials through environment variables in CI or agent workflows. Do not rely on interactive prompts.
- Use `@filename` inputs for complex JSON payloads instead of long inline shell strings.
- Query `dmp ref` data before building rule-based audiences if valid dimensions, apps, regions, or tags are unknown.
- For deal modification, only include the fields that should change. `audiences` is append-only.

## Additional References

- Full installation, configuration, command, and output examples: [references/commands.md](references/commands.md)
- Common end-to-end agent workflows: [references/workflows.md](references/workflows.md)
