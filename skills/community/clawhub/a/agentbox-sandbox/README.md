# agentbox-clawhub

A text-only skill bundle for ClawHub and AgentSkills-compatible runtimes.

## Purpose

This skill helps an agent answer common AgentBox questions using a curated summary of the official documentation.

## Included files

- `SKILL.md` - trigger metadata and operating instructions
- `references/agentbox-official.md` - compact documentation summary
- `manifest.yaml` - publish metadata for ClawHub-style registries
- `agents/openai.yaml` - UI metadata for ChatGPT-compatible skill tooling

## Intended use

Use this skill when users ask how to:

- get started with AgentBox
- install the CLI or authenticate
- use the Python SDK
- create or customize a sandbox template
- set timeouts
- run shell commands
- read or write files in a sandbox
- pass environment variables safely

## Publish notes

ClawHub publication normally requires logging in and publishing from the skill root, for example:

```bash
openclaw clawhub login
openclaw skill publish .
```

If your ClawHub environment uses the standalone `clawhub` CLI instead, publish with the matching command set for that installation.
