# exa-research-openclaw-skill

An OpenClaw-adapted skill for using the [`exa` CLI](https://github.com/jdegoes/exa) as a research/search workflow inside OpenClaw.

## What this repo is

This repository contains a reusable OpenClaw skill package built from the upstream Exa project's generated skill text plus OpenClaw-specific adaptations.

Contents:

- `SKILL.md` — the agent-facing skill instructions
- `scripts/exa-with-key.sh` — a wrapper that loads credentials securely and then runs `exa`
- `.gitignore` — basic repo-local junk-file ignores
- `LICENSE` — MIT license for this adaptation

## Upstream project

This skill is based on the upstream Exa project:

- Upstream repo: <https://github.com/jdegoes/exa>
- Upstream generated skill source: `exa skill`

The upstream project provides the Exa CLI itself, including the `exa skill` generator that emits a generic skill description.

## What changed from upstream

Compared with the raw upstream `exa skill` output, this OpenClaw version was adapted to:

- use OpenClaw-native metadata (`homepage`, `metadata.openclaw`, `primaryEnv`)
- use `{baseDir}` in skill instructions like mainstream OpenClaw skills do
- point usage at a bundled wrapper script instead of assuming `exa` is called directly
- support OpenClaw-native credential wiring via `skills.entries.exa-research.apiKey`
- keep the repo free of secrets
- focus documentation on OpenClaw-specific setup instead of duplicating upstream Exa install docs

## Prerequisites

- OpenClaw installed
- Exa CLI installed from the upstream Exa project
- a valid Exa API key
- `bash` and `curl`
- `jq` recommended (used by `exa diagnostics`)

## Install Exa

Follow the upstream Exa installation instructions:

- <https://github.com/jdegoes/exa>

This repo intentionally does **not** duplicate Exa installation steps. The only requirement here is that `exa` is installed and either:

- available on your `PATH`, or
- reachable via `EXA_BIN`

## Install this skill into OpenClaw

Install this repo into one of your OpenClaw skill directories using whatever skill layout your OpenClaw setup expects.

A common default is:

```bash
mkdir -p ~/.openclaw/skills
cp -R exa-research-openclaw-skill ~/.openclaw/skills/exa-research
chmod 700 ~/.openclaw/skills/exa-research/scripts/exa-with-key.sh
```

## Secure credential setup

This repo does **not** contain any API keys.

### Most idiomatic OpenClaw setup

Set the skill credential in OpenClaw config:

```json5
{
  skills: {
    entries: {
      "exa-research": {
        apiKey: { source: "file", provider: "exafile", id: "value" }
      }
    }
  }
}
```

Or set an explicit env entry:

```json5
{
  skills: {
    entries: {
      "exa-research": {
        env: {
          EXA_API_KEY: "..."
        }
      }
    }
  }
}
```

### Other supported auth sources

The wrapper supports auth in this order:

1. `EXA_API_KEY` already present in the environment
2. `EXA_API_KEY_FILE` pointing at a readable file
3. the default file path `~/.openclaw/credentials/exa/api-key.txt`

### Simple file-based setup

For personal/self-hosted installs, a locked-down file is also fine:

```bash
mkdir -p ~/.openclaw/credentials/exa
printf '%s\n' '<your-exa-api-key>' > ~/.openclaw/credentials/exa/api-key.txt
chmod 600 ~/.openclaw/credentials/exa/api-key.txt
```

You can also point somewhere else:

```bash
export EXA_API_KEY_FILE="$HOME/.config/exa/api-key.txt"
```

### Security notes

- never commit your API key
- keep key files outside the repo
- use `chmod 600` on file-based secrets
- prefer `skills.entries.exa-research.apiKey` or runtime env injection if you already use OpenClaw secrets or a secret manager

## Verify the setup

```bash
~/.openclaw/skills/exa-research/scripts/exa-with-key.sh diagnostics
~/.openclaw/skills/exa-research/scripts/exa-with-key.sh search -n 1 "latest OpenAI news"
```

## Intended use

This skill is meant to help OpenClaw choose Exa when a task needs:

- live web search
- grounded answers with citations
- page contents/highlights/summary
- similar-link discovery
- code context
- Exa research workflows

## Attribution

Credit for the Exa CLI, API surface, and the original generated skill text belongs to the upstream Exa project and its authors.
