###### WIP Computer

# Private-to-Public Sync

Publish safely. Syncs your private working repo to a clean public mirror. Excludes internal `ai/` folders automatically.

## What it does

- Copies everything except `ai/` and `.git/` to the public repo
- Creates a PR on the public repo, merges it
- Syncs GitHub releases from private to public
- Cleans up deploy branches

## Usage

```bash
bash deploy-public.sh /path/to/private-repo org/public-repo
```

## Requirements

- git
- gh (GitHub CLI)
- bash

## Interfaces

- **CLI**: Shell script
- **Skill**: SKILL.md for agent instructions

## Part of [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)
