# Drakeling Setup Guide

This skill connects to a local Drakeling daemon. The daemon must be installed and running before the skill can function.

## 1. Install the Drakeling package

Pick one:

```bash
pipx install drakeling        # recommended — isolated environment
pip install drakeling          # standard pip
uv tool install drakeling      # uv
```

After installation, two commands are available: `drakelingd` (daemon) and `drakeling` (terminal UI).

## 2. Start the daemon

```bash
drakelingd
```

On first run, the daemon:
- Creates a platform data directory (see paths below)
- Walks you through interactive LLM setup (pick a provider, enter credentials)
- Generates an ed25519 identity keypair and a local API token
- Begins listening on `http://127.0.0.1:52780`

Leave the daemon running in its own terminal or set it up as a background service.

## 3. Retrieve the API token

The daemon writes an `api_token` file to the data directory on first run.

| Platform | Command |
|----------|---------|
| Linux | `cat ~/.local/share/drakeling/api_token` |
| macOS | `cat ~/Library/Application\ Support/drakeling/api_token` |
| Windows | `type "%APPDATA%\drakeling\drakeling\api_token"` |

## 4. Configure the token in OpenClaw

Add the token to `~/.openclaw/openclaw.json`:

```json5
{
  "skills": {
    "entries": {
      "drakeling": {
        "env": {
          "DRAKELING_API_TOKEN": "paste-token-here"
        }
      }
    }
  }
}
```

If your config already has a `skills` section, merge `entries.drakeling` into it.

**Alternative:** If `skills.entries.drakeling` causes issues with OpenClaw doctor, use a top-level `env` block instead:

```json5
{
  "env": {
    "DRAKELING_API_TOKEN": "paste-token-here"
  }
}
```

## 5. Start a new OpenClaw session

OpenClaw loads skills when a session starts. After installing and configuring the token, start a new session so it picks up the drakeling skill.

## Data directory paths

| Platform | Path |
|----------|------|
| Linux | `~/.local/share/drakeling/` |
| macOS | `~/Library/Application Support/drakeling/` |
| Windows | `%APPDATA%\drakeling\drakeling\` |

## Custom port

If the daemon runs on a non-default port, set `DRAKELING_PORT` in the skill env config alongside the token:

```json5
{
  "skills": {
    "entries": {
      "drakeling": {
        "env": {
          "DRAKELING_API_TOKEN": "paste-token-here",
          "DRAKELING_PORT": "9999"
        }
      }
    }
  }
}
```

## Troubleshooting

**Skill not appearing in OpenClaw:** The skill requires `drakelingd` on your PATH. Install the drakeling package first (step 1).

**403 Forbidden:** The request has no `Authorization` header — the `DRAKELING_API_TOKEN` env var is not reaching the skill. Check that your config uses `skills.entries.drakeling.env`, not `skills.drakeling.env` (the latter is ignored by OpenClaw). Restart OpenClaw after fixing the config.

**401 Invalid API token:** The token was sent but does not match the daemon's token. Ensure the value in OpenClaw config exactly matches the contents of the `api_token` file in the data directory.

**Connection refused:** The daemon is not running. Start it with `drakelingd`.

**OpenClaw doctor strips the config:** Use the top-level `env` block alternative shown in step 4.

## Full documentation

https://github.com/BVisagie/drakeling
