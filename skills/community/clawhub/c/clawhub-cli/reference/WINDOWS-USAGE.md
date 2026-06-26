# Windows Usage (No `.ps1` Scripts)

This skill package intentionally avoids shipping `.ps1` scripts.

On Windows, run `clawhub` commands directly from **PowerShell** or **Command Prompt**, or use Git Bash/WSL to run the shell scripts under `scripts/linux/`.

## Install

- Install latest:

```bash
clawhub install <skill-slug>
```

- Install pinned version:

```bash
clawhub install <skill-slug> --version <semver>
```

- Verify:

```bash
clawhub list
```

## Update

- Update all:

```bash
clawhub update --all
```

- Update one:

```bash
clawhub update <skill-slug>
```

- Update one to pinned version:

```bash
clawhub update <skill-slug> --version <semver>
```

## Publish

```bash
clawhub publish <skill-folder> --slug <slug> --name "<Display Name>" --version <semver> --tags latest
```

Example:

```bash
clawhub publish .\skills\my-skill --slug my-skill --name "My Skill" --version 0.1.0 --tags latest
```

## Sync

```bash
clawhub sync --all
```

If supported, consider:

- `--dry-run`
- `--bump patch|minor|major`
- `--changelog "Update skills"`

## Running the `.sh` scripts on Windows

If you want to use the shell scripts:

- **Git Bash**: run `bash scripts/linux/install-skill.sh <slug>`
- **WSL**: run the same commands inside WSL

