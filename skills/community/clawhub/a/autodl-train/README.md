# AutoDL Train Operator Skill

This directory is a publishable OpenClaw skill for operating remote model training jobs on an AutoDL Linux server.

## Included

- `SKILL.md`: Skill metadata and workflow.
- `agents/openai.yaml`: Minimal UI metadata for ClawHub/OpenClaw.
- `config.example.json`: Copy to `config.json` and fill with real values.
- `.env.example`: Optional environment variable configuration.
- `scripts/*.py`: CLI tools for start, status, resource checks, and log summarization.
- `references/*.md`: Usage guide and troubleshooting.

## Quick Start

1. Copy `config.example.json` to `config.json`.
2. Fill in SSH host, username, project path, environment settings, training command, and log path.
3. Run one of the scripts from this directory.

```bash
python scripts/remote_train.py --config config.json
python scripts/check_status.py --config config.json
python scripts/monitor_resources.py --config config.json
python scripts/summarize_log.py --config config.json --action summarize
```

## Packaging

If your environment provides `package_skill.py`, package this skill directory as a zip and upload the result to ClawHub.

## Publishing Checklist

1. Keep only publish-safe files inside this skill directory.
2. Store machine-specific config outside the skill directory, or use local-only names such as `config.local.json` and `.env`.
3. Never include real passwords, tokens, hostnames, IP addresses, SSH keys, or personal project paths in uploaded files.
4. Verify that `SKILL.md`, `agents/openai.yaml`, `config.example.json`, `scripts/`, and `references/` are present.
5. Rebuild the zip after any cleanup so the archive matches the final publishable directory.

## Recommended Local Practice

1. Put your private runtime config outside the skill directory, for example in `../local/`.
2. If you keep a local `.env`, do not upload it.
3. Use `config.example.json` as the only config file that ships with the skill.
