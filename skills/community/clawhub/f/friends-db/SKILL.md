---
name: friends-db
description: Query and maintain Alex's local friends database stored in a private SQLite file under the OpenClaw workspace. Use when looking up a friend, finding phone/email/contact details, reading relationship notes, or updating those records. Prefer this over reading friends.md directly.
metadata:
---

# Friends DB

Use the helper script in `scripts/friends_db.py`. Do not run arbitrary SQL.

## When to use

- A request depends on friend/contact details that used to live in `friends.md`
- You need a phone number, email, preferred name, or relationship note
- You need to track friendship cadence, last-seen dates, or activity ideas
- You need to add or update a friend fact after a conversation or event
- You need to sync past in-person interactions from calendar into the friend CRM

## Commands

Initialize or migrate:

```bash
python3 ./skills/friends-db/scripts/friends_db.py migrate --source "$HOME/.openclaw/workspace/friends.md" --replace-with-stub
```

Search:

```bash
python3 ./skills/friends-db/scripts/friends_db.py search "lily"
python3 ./skills/friends-db/scripts/friends_db.py list
```

Show one contact:

```bash
python3 ./skills/friends-db/scripts/friends_db.py show "Lily Li"
python3 ./skills/friends-db/scripts/friends_db.py show "jerrypaulgreen@gmail.com"
```

Friend CRM overview:

```bash
python3 ./skills/friends-db/scripts/friends_db.py due-list
python3 ./skills/friends-db/scripts/friends_db.py due-list --status all --within-days 14
python3 ./skills/friends-db/scripts/friends_db.py profile "David Su"
python3 ./skills/friends-db/scripts/friends_db.py suggest "David Su"
```

CRM setup and updates:

```bash
python3 ./skills/friends-db/scripts/friends_db.py set-importance "David Su" high
python3 ./skills/friends-db/scripts/friends_db.py set-cadence "David Su" 21
python3 ./skills/friends-db/scripts/friends_db.py set-context "David Su" --home-area "South Bay" --best-times "weekday evenings"
python3 ./skills/friends-db/scripts/friends_db.py add-tag "David Su" interest pickleball
python3 ./skills/friends-db/scripts/friends_db.py add-tag "David Su" neighborhood "South Park"
```

Interaction logging:

```bash
python3 ./skills/friends-db/scripts/friends_db.py log-interaction "David Su" --type in_person --at 2026-03-15T18:30:00-07:00 --location "South Park"
python3 ./skills/friends-db/scripts/friends_db.py sync-calendar --days-back 180
```

General contact updates:

```bash
python3 ./skills/friends-db/scripts/friends_db.py add-fact "Lily Li" "Invited to dinner on 2026-03-20"
python3 ./skills/friends-db/scripts/friends_db.py set-method "David Su" phone "+14086246128" --primary
python3 ./skills/friends-db/scripts/friends_db.py set-preferred-name "Lily Li" "Lily"
```

## Rules

- Keep the database in the hidden OpenClaw workspace state directory created by the helper.
- The helper enforces private filesystem permissions and parameterized SQL. Keep using it instead of shelling out to `sqlite3` with raw user text.
- Treat `friends.md` as a stub only after migration. The database is the source of truth.
- `sync-calendar` uses attendee email first, then title/description alias matches.
- Count only `in_person` interactions toward the cadence target. Calls/texts/emails are supporting context.
- Cadence defaults: `high=20`, `medium=30`, `low=90` days.
- Suggestions are local and deterministic; they come from tags plus the bundled activity template asset.
- Return only the fields needed for the task. Do not dump the whole contact database into chat unless Alex explicitly asks.
