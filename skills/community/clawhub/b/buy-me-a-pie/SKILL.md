---
name: buy-me-a-pie
description: Read and change Buy Me a Pie lists. Unofficial third-party skill. No affiliation with Buy Me a Pie. Use for lists, items, purchased state, sharing, unique items, and account checks. API first. Browser only for signup, PIN reset, OAuth, print, or API drift.
homepage: https://app.buymeapie.com/
metadata:
  openclaw:
    skillKey: buy-me-a-pie
    summary: Unofficial skill to manage Buy Me a Pie lists and items.
    homepage: https://app.buymeapie.com/
    requires:
      bins:
        - python3
      env:
        - BUYMEAPIE_LOGIN
        - BUYMEAPIE_PIN
    install:
      - id: brew
        kind: brew
        formula: python
        bins:
          - python3
        label: Install Python 3 (brew)
---

# Buy Me A Pie

Unofficial third-party skill. No affiliation with Buy Me a Pie.

API first.

Set creds:
- `BUYMEAPIE_LOGIN`
- `BUYMEAPIE_PIN`

Run:
- `{baseDir}/scripts/buymeapie.sh whoami`
- `{baseDir}/scripts/buymeapie.sh lists`
- `{baseDir}/scripts/buymeapie.sh items --list-id <id>`
- `{baseDir}/scripts/buymeapie.sh add-item --list-id <id> --title "Milk" --amount "2"`
- `{baseDir}/scripts/buymeapie.sh set-item-state --list-id <id> --item-id <id> --purchased true`
- `{baseDir}/scripts/buymeapie.sh share-list --list-id <id> --email friend@example.com`

Rules:
- resolve IDs before writes
- merge share emails unless replace was requested
- retry `423`
- treat `401` and `422` as auth or state failure
- do not invent writes for recipe lists
- use browser only for signup, PIN reset, OAuth, print, visual checks, or API drift

Read only if needed:
- `{baseDir}/references/api-surface.md`
- `{baseDir}/references/architecture.md`
