---
name: cosin
description: "Use this skill when an agent needs to operate the `cosin` CLI from the terminal. `cosin` accepts only relative paths, lists available skills through the `skills` subcommand, can call COS API paths directly, and can call `/cos/...` skills by turning them into x402 pay-and-call requests to the COS backend. This skill is for using the CLI, not for editing the cosin source code."
---

# Cosin CLI

Use `cosin` to call the COS API and COS-backed skills from the terminal.

## What the CLI does

`cosin` now accepts only relative paths.

There are three request styles:

1. `skills`
   Calls `https://skills.bankofuniverse.org/skills` directly and prints the upstream body directly.

2. Normal COS API paths such as `/v1/me`
   These are sent directly to the COS API host.

3. Skill paths under `/cos/...`
   These are converted internally into x402 pay-and-call requests:
- keeps the same request path
- builds the target URL from `SKILLS_BASE_URL`
- sends that target URL to `POST /agent/pay-and-call` on the COS API host

Users should not pass absolute URLs to the CLI anymore.

## Gather inputs

Collect these inputs before running the CLI:

- A COS bearer token for `--key`
- An HTTP method
- A relative path starting with `/`
- Optional JSON for `--json`
- Optional repeatable headers for `--header` or `-H`
- Optional `--base-url` override for normal COS API calls

Ask for the token if the user has not provided one. Treat it as sensitive.

## Protect credentials

- Treat the `--key` value as sensitive
- Do not print, commit, or hardcode the token
- Keep the token in the command line argument, not in repo files

## Run the CLI

Use one of these command shapes:

```sh
cosin --key <token> <METHOD> <PATH> [--json '<json>'] [--header 'Name: value'] [--base-url <url>]
cosin --key <token> agent [status|me] [--base-url <url>]
cosin --key <token> skills
```

Important flags:

- `--key <token>` for the required bearer token
- `--json <json>` for an optional JSON request body
- `--header 'Name: value'` or `-H 'Name: value'` for repeatable custom headers
- `--base-url <url>` to override the default COS API base URL for direct API calls
- `--version` or `-v` to print the installed CLI version
- `--help` or `-h` to print usage

Subcommand notes:

- `skills` does not accept `--json`
- `skills` does not accept custom headers
- `agent` does not accept `--json`
- `agent` does not accept custom headers

## Supported paths

### Built-in catalog

Use this to discover available skills:

```sh
cosin --key <token> skills
```

Expected upstream skills include:

- `/cos/crypto/chainlink/random`
  Returns a random value from the Chainlink-based skill endpoint.
- `/cos/crypto/price/:symbol`
  Returns the latest price for a supported token symbol.

Supported symbols for `/cos/crypto/price/:symbol`:

- `BTC`
- `ETH`
- `HYPE`
- `SOL`
- `TRX`
- `USDT`
- `USDC`

### Direct COS API calls

Use normal API paths to call COS directly:

```sh
cosin --key <token> GET /v1/me
cosin --key <token> POST /v1/orders --json '{"symbol":"BTCUSDT"}'
```

### Skill calls through `/cos/...`

Use `/cos/...` when you want to call a skill through COS:

```sh
cosin --key <token> GET /cos/crypto/chainlink/random
cosin --key <token> GET /cos/crypto/price/BTC
```

Internally, the CLI turns those into x402 pay-and-call requests to the COS backend.

## Use the agent shortcut

Use `agent`, `agent status`, or `agent me` as a convenience alias for `GET /agent/me`.

```sh
cosin --key <token> agent
cosin --key <token> agent status
cosin --key <token> agent me
```

Do not combine `agent` with `--json` or custom headers.

## Validate inputs before running

- Ensure the path starts with `/`
- Do not pass absolute URLs
- Use `skills`, not `GET /skills`
- Ensure `--json` is valid JSON
- Ensure headers use `Name: value`
- For `/cos/crypto/chainlink/random`, only use `GET`
- For `/cos/crypto/price/:symbol`, only use `GET` and only the supported symbols

## Read the output

Expect the CLI to:

- Print an HTTP status line for normal API requests, `/cos/...` skill calls, and `agent`
- Print only the upstream body for the `skills` subcommand
- Pretty-print JSON response bodies
- Print `<empty response body>` for empty responses
- Return a non-zero exit code for unsuccessful HTTP responses or CLI argument errors

## Work locally in this repo

Use the local build when working inside this repository:

```sh
bun run build
./dist/index.js --key <token> agent
./dist/index.js --key <token> skills
./dist/index.js --key <token> GET /v1/me
./dist/index.js --key <token> GET /cos/crypto/chainlink/random
```

Use the published command shape locally when that is more convenient:

```sh
bun x cosin --key <token> agent
bun x cosin --key <token> skills
bun x cosin --key <token> GET /v1/me
bun x cosin --key <token> GET /cos/crypto/price/BTC
```
