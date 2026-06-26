---
name: clawhub-install
description: Download and install skills from ClawHub directly via curl, bypassing official CLI rate limits. Use when the user wants to install one or more ClawHub skills but the official installation command is rate-limited or failing.
compatibility: Requires curl, unzip, and openclaw CLI. Downloads skills to the workspace directory configured in OpenClaw.
metadata:
  author: huanggu.ly
  version: "1.0"
---

# ClawHub Install

Downloads and installs skills from ClawHub by direct URL access, avoiding rate limits that may occur with the official CLI.

## Usage

```bash
bash {baseDir}/scripts/install.sh <skill_name> [skill_name2] [skill_name3] ...
```

## Steps

Each skill installation follows these steps:

1. **Get workspace path**: Retrieves the workspace directory from OpenClaw config using `openclaw config get agents.defaults.workspace`
2. **Download**: Downloads the skill package from `https://wry-manatee-359.convex.site/api/v1/download?slug=<skill_name>`
3. **Extract**: Unzips the package to `<workspace>/skills/<skill_name>`

## Examples

```bash
# Install single skill
bash {baseDir}/scripts/install.sh finnhub

# Install multiple skills in one run
bash {baseDir}/scripts/install.sh finnhub massive-api tavily-search
```

## Error Handling

The script will:
- Report errors if required commands (curl, unzip, openclaw) are missing
- Skip existing skills after removing them
- Show success/failure count after batch installation

## Use Cases

- Use when `clawhub install` command is rate-limited
- Use when installing multiple skills in batch
- Use when direct download is preferred over CLI installation
