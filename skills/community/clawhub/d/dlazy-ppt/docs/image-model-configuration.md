# Image Model Configuration

Use this reference only when the runtime config is missing or must be changed.

Do not manually parse `.env`. The CLI loads the shared config automatically. Run the command first, then use this document only if the CLI reports missing or invalid configuration.

Ask the user for configuration only when:

- The CLI reports a missing `DLAZY_API_KEY`.
- The user explicitly wants to change the key, base URL, or model.
- A real API call fails with an authentication, permission, credit, or model-not-found error.

## Getting An API Key

1. Sign in at [dlazy.com](https://dlazy.com).
2. Open [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key).
3. Copy the key from the API Key section.

The key is scoped to the user's dLazy organization and can be rotated or revoked at any time from the same page. Slide generation consumes that organization's credits.

## Required And Optional Values

- `DLAZY_API_KEY` is required.
- `DLAZY_BASE_URL` is optional and defaults to `https://dlazy.com`. Set it only for a self-hosted deployment.
- `DLAZY_PPT_IMAGE_MODEL` is optional and defaults to `gpt-image-2`. Change it only to use a different dLazy image tool.

## Configuring

```bash
python3 {skill_root}/scripts/dlazy_ppt_runtime.py config \
  --api-key "your-dlazy-api-key"
```

This produces:

```env
DLAZY_API_KEY=your-dlazy-api-key
```

Self-hosted deployment, or a different image tool:

```bash
python3 {skill_root}/scripts/dlazy_ppt_runtime.py config \
  --api-key "your-dlazy-api-key" \
  --base-url "https://dlazy.example.com" \
  --model gpt-image-2
```

`--clear-base-url` drops a previously set base URL and returns to `https://dlazy.com`.

## Verifying

```bash
python3 {skill_root}/scripts/dlazy_ppt_runtime.py doctor --check-api
```

The check fetches the account's tool manifest. A `401` means the key is wrong; a model reported as not in the manifest means that tool is not available to this organization.

## Runtime Config

The config is written to:

```text
~/.dlazy-ppt/.env
```

The file is created with mode `0600`. It is shared by Codex, Claude Code, OpenClaw, Hermes Agent, and other local agents, so the key is configured once per machine.

Process environment variables override `.env` values. A command-line `--model` overrides `DLAZY_PPT_IMAGE_MODEL` for that single command.
