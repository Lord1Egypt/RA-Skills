---
name: apcli
description: Search, read and edit Apple Contacts from the command line on macOS: find people by name, nickname or company, show a card, create, update and delete contacts, with JSON output for agent use.
author: gopaljigaur
license: MIT
platform: macOS
requires:
  binaries: [apcli]
  install: "npm install -g @gopaljigaur/apcli"
tags: [contacts, address-book, macos, productivity, apple]
---

# apcli: Apple Contacts CLI

Use this when the user wants to look someone up, or add or change a contact,
on a Mac. It talks to the Contacts framework through JXA, so Contacts.app never
opens, and it sees every account Contacts syncs (iCloud, Google, Exchange).

## First run

```bash
apcli setup        # asks macOS for Contacts access once
```

Exit code `10` means access was not granted: the user has to allow it in
System Settings > Privacy & Security > Contacts.

## Commands

| command | does |
| --- | --- |
| `apcli search <query> [--limit n]` | contacts whose name, nickname or company contains the query; case and accent insensitive |
| `apcli contact <id>` | one contact, every field |
| `apcli create --given <name> [fields]` | add a contact |
| `apcli update <id> [fields]` | change one; repeatable fields add, `--remove-*` take away |
| `apcli delete <id>` | asks first; `--yes` when there is no terminal |

Fields: `--given`, `--family`, `--nickname`, `--org`,
`--phone [label:]<number>`, `--email [label:]<address>`,
`--social <service>:<handle>` (handles for services Contacts has no field for,
such as `telegram:@ana` or `discord:<user id>`), and
`--remove-phone`, `--remove-email`, `--remove-social`.

Always pass `--json` when reading the output; errors come back as JSON too.

```bash
apcli search ana --json
apcli create --given Ana --phone mobile:+491701234567 --email ana@example.com --json
apcli update <id> --nickname "Annie" --social telegram:@ana --json
```

Search first and use the id it returns; names are not unique.

## Exit codes

`0` ok, `1` runtime error, `2` bad arguments, `10` Contacts access not granted.
