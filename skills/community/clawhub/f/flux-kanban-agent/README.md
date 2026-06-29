# Flux skill for OpenClaw

An [OpenClaw](https://openclaw.ai) skill that teaches AI agents to operate
[Flux](https://flux.umin.ai) through its REST API: create and move cards,
manage boards and columns, assign members, toggle labels, run full-text
search, and build board automations.

## Install

```bash
openclaw skills install flux-skill
```

## Setup

The skill needs a Flux API key.

| Variable | Required | Notes |
|---|---|---|
| `FLUX_API_KEY` | yes | Create one in Flux under **Settings → API Keys**. It starts with `flux_`. |
| `FLUX_BASE_URL` | no | Base URL of your Flux instance. Defaults to `https://flux.umin.ai`. |

Run `openclaw skills check` to confirm the key is set.

## What it covers

Workspaces, boards, columns, cards (with checklists, comments, labels, and
attachments), board-level label definitions, full-text search, and one-click
undo. See [`SKILL.md`](SKILL.md) for the full endpoint reference and common
workflows.

The always-current API reference is also served live at
[flux.umin.ai/llms.txt](https://flux.umin.ai/llms.txt), with interactive docs
at [flux.umin.ai/api-docs](https://flux.umin.ai/api-docs).

## License

[MIT](LICENSE) © Redbite Solutions Ltd
