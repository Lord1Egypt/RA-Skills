---
name: clawhub-publish
description: Publish agent skills to ClawHub marketplace. Search, install, update, and publish skills from clawhub.com.
tags: ['marketplace', 'skills', 'agents', 'sharing', 'publish']
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["clawhub"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "clawhub",
              "bins": ["clawhub"],
              "label": "Install ClawHub CLI (npm)",
            },
          ],
      },
  }
---

# ClawHub Publish

## Overview

Use the ClawHub CLI to search, install, update, and publish agent skills to the ClawHub marketplace.

## Install CLI

```bash
npm i -g clawhub
```

## Authentication (for publishing)

```bash
clawhub login
clawhub whoami
```

## Search Skills

```bash
clawhub search "postgres backups"
```

## Install Skills

```bash
clawhub install my-skill
clawhub install my-skill --version 1.2.3
```

## Update Skills

```bash
clawhub update my-skill
clawhub update my-skill --version 1.2.3
clawhub update --all
clawhub update my-skill --force
clawhub update --all --no-input --force
```

## List Installed Skills

```bash
clawhub list
```

## Publish Skills

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

## Notes

- Default registry: https://clawhub.com (override with CLAWHUB_REGISTRY or --registry)
- Default workdir: cwd (falls back to OpenClaw workspace); install dir: ./skills (override with --workdir / --dir / CLAWHUB_WORKDIR)
- Update command hashes local files, resolves matching version, and upgrades to latest unless --version is set
