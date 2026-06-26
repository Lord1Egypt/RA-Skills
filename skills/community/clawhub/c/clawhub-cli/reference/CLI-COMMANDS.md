# ClawHub CLI Commands (Reference)

This document is a **quick reference** for common ClawHub CLI workflows used by the `clawhub-cli` skill.

> If you are unsure about supported flags in the user's environment, run:
>
> - `clawhub --help`
> - `clawhub <command> --help`

## Authentication

- Login (interactive):

```bash
clawhub login
```

- Login with token:

```bash
clawhub login --token <api-token>
```

## Discovery

- Search skills by keyword query:

```bash
clawhub search "postgres backup"
```

Search tips:

- use **domain + verb + platform** (e.g. `"docker cleanup"`, `"git release"`, `"kubernetes logs"`)
- keep queries short; try 2-5 variations

## Install / List / Update

- Install latest:

```bash
clawhub install <skill-slug>
```

- Install pinned version:

```bash
clawhub install <skill-slug> --version <semver>
```

- List installed skills (as recorded by the CLI; may be lockfile-backed depending on your setup):

```bash
clawhub list
```

- Update all skills:

```bash
clawhub update --all
```

- Update one skill:

```bash
clawhub update <skill-slug>
```

- Update one skill to a pinned version:

```bash
clawhub update <skill-slug> --version <semver>
```

## Publish / Sync

- Publish one local skill folder:

```bash
clawhub publish ./skills/my-skill \
  --slug my-skill \
  --name "My Skill" \
  --version 0.1.0 \
  --tags latest
```

- Sync all skill folders under a root:

```bash
clawhub sync --all
```

If available, prefer safety options for bulk ops:

- `--dry-run`
- `--bump patch|minor|major`

